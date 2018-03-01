import sys
import time
sys.path.append('./env/lib/python2.7/site-packages/')
sys.path.append('./env/lib64/python2.7/site-packages/')
import subprocess
import vertica_python
import json
from utill import memoize, read_config
import os
from logger import *
import multiprocessing
from functools import partial
from multiprocessing import Pool

@memoize
def ssm_pass():
    out = subprocess.Popen('aws ssm get-parameters --names "' + params['ssm_name'] + '" --with-decryption',
                           stdout=subprocess.PIPE, shell=True)
    params = json.loads(out.stdout.read())
    # taking first or last version only
    return params['Parameters'][0]['Value']


@memoize
def read_params(logger):
    try:
        logger.info('Starting reading configuration....')
        profile='DEV'
        if 'MACHINE_ENV' in os.environ:
            profile = os.environ['MACHINE_ENV']
        config = read_config(profile=profile)
        params = {}
        params['password'] = config['source_db']['password']
        params['ssm_name'] = config['source_db']['ssm_name']

        params['src_driver'] = config['source_db']['driver']
        logger.info("Source Driver - "+params['src_driver'])

        params['host'] = config['source_db']['host']
        logger.info("Source Host - "+params['host'])

        params['port'] = config['source_db']['port']
        logger.info("Source port - "+str(params['port']))

        params['username'] = config['source_db']['username']
        logger.info("Source username - "+params['username'])

        params['db_name'] = config['source_db']['db_name']
        logger.info("Source database - "+params['db_name'])

        params['tables'] = config['tables']

        params['target_s3_path'] = config['aws']['s3_path']
        logger.info("s3 bucket path - "+params['target_s3_path'])

        max_process = multiprocessing.cpu_count()
        if(max_process<=config['aws']['degree_of_parallelism']  or config['aws']['degree_of_parallelism'] <0):
            logger.info ("Setting degree of parallelism to cpu count "+ str(max_process))
            params['degree_of_parallelism'] = max_process
        else:
            params['degree_of_parallelism']= config['aws']['degree_of_parallelism']

        logger.info("Degree of parallelism - "+ str(params['degree_of_parallelism']))

        logger.info('Reading configuration successfully.')

        return params

    except Exception as e:
        logger.exception("Config file couldn't load")

def connect_vertica_db(logger,params):
    try:
        host = params['host']
        port = params['port']
        username = params['username']
        password = params['password']
        if not password:
            password = ssm_pass()
        db = params['db_name']
        conn_info = {'host': host, 'port': port, 'user': username, 'password': password, 'database': db,
                     'read_timeout': 600, 'unicode_error': 'strict', 'ssl': False, 'connection_timeout': 5}
        
        connection = vertica_python.connect(**conn_info)
        return connection
    except Exception as e:
        logger.exception("Can't connect to vertica database.")


def destroy_s3_bucket(s3_bucket_path):
    command = "aws s3 rm " + s3_bucket_path + " --recursive"
    subprocess.call(command, shell=True)


def lower_table_column_names(logger,table_name):
    try:
        connection = connect_vertica_db(logger,params)
        cursor = connection.cursor()
        table_name_with_schema = []
        table_name_only = table_name
        table_schema = ''
        sql = ''
        sql_schema_condition = ''
        if '.' in table_name:
            table_name_with_schema = table_name.split('.')
            table_name_only = table_name_with_schema[1]
            table_schema = table_name_with_schema[0]
            sql_schema_condition += " and t.table_schema='" + table_schema + "'"

        sql += "select lower(column_name) l_column_name, lower(data_type) data_type from v_catalog.columns t  where t.table_name='" + table_name_only + "' " + sql_schema_condition + ";"
        # print(sql)
        logger.info('Query for select column: \n\n'+sql+'\n')

        cursor.execute(sql)
        column_names = cursor.fetchall()
        connection.close()
        return column_names
    except Exception as e:
        logger.exception("Couldn't read table column name")


def stage_src_data(logger,schema,table, s3_bucket_path, src_driver, src_db_url, src_username, src_password, number_of_mappers,split_column):
    try:
        l_column_names = lower_table_column_names(logger,table)

        destroy_s3_bucket(s3_bucket_path)
        select_str = ', '.join(
            'cast(to_hex(' + str(v[0]) + ') as varchar) ' + str(v[0]) if 'binary' in v[1] else str(v[0]) for v in
            l_column_names)
        if schema:
            table = schema + "." + table
        query = "select " + select_str + " FROM " + table + " t where $CONDITIONS"
        logger.debug(' Sqoop job query: \n\n'+query+'\n')
        if (number_of_mappers > 1):
            cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url + " --username " + src_username + " --password " + src_password + " --query '" + query + "' --target-dir " + s3_bucket_path + " --direct --as-avrodatafile -m " + str(
                number_of_mappers) + " --split-by t." + split_column + " -- --schema "+schema
        else:
            cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url + " --username " + src_username + " --password " + src_password + " --query '" + query + "' --target-dir " + s3_bucket_path + " --direct --as-avrodatafile -m 1" + " -- --schema "+schema
        
        logger.debug('Sqoop job command: \n\n'+cmd_dump_to_s3+'\n')
        logger.info('Sqoop job starting...')
        sq_p=subprocess.Popen(cmd_dump_to_s3,stdout=subprocess.PIPE, shell=True)
        logger.debug('Sqoop job output: \n\n'+sq_p.stdout.read()+'\n')
        logger.info('Sqoop job finished.')
    except Exception as e:
        logger.exception("Sqoop job process step error.")


def _process(params, table):
    logger=jobLogger(table['name'])
    try:        
        process_start_time= time.time()

        logger.info('Starting process...')
        logger.info(table['name']+' process using '+str(table['mappers'])+' mapper(s)')

        if table['mappers']==1:
            logger.info("You've set the job to sun on single mapper this might take longer procssing.")
        
        table_name = table['name']
        number_of_mappers = table['mappers']
        if table['schema']:
            schema = table['schema']
        else:
            schema = ''
        split_column = table['split_column']

        if split_column is None:
            logger.warn('There is no split column found. sqoop job might run on single mapper. this will take longer time to run job')

        s3_bucket_path = params['target_s3_path'] + "/" + table_name + "/"
        logger.info('Processed file will save to - '+s3_bucket_path)

        src_db_url = "jdbc:vertica://" + params['host'] + "/" + params['db_name']
        logger.info('Source Database URL: '+src_db_url)
        password = params['password']
        if not password:
            logger.info('Logging using ssm_pass')
            password = ssm_pass()

        stage_src_data(logger,schema,table_name, s3_bucket_path, params['src_driver'], src_db_url, params['username'], password,number_of_mappers, split_column)
        
        process_end_time= time.time()
        logger.info('Process successfully completed.')
        logger.info('Total time taken - '+str(round(process_end_time - process_start_time, 2))+' sec.')
    except Exception as e:
        logger.exception("Couldn't start process.")
    


def sync_data(params):
    max_process= multiprocessing.cpu_count()
    if(max_process<=params['degree_of_parallelism']  or params['degree_of_parallelism'] <0):
        pool = Pool(max_process)
    else:
        pool = Pool(params['degree_of_parallelism'])

    sub_process=partial(_process, params)
    pool.map(sub_process, params['tables'])
    

if __name__ == '__main__':
    logger=jobLogger('root')
    try:        
        params = read_params(logger)
        sync_data(params)
    except Exception as e:
        logger.exception("Couldn't start process.")