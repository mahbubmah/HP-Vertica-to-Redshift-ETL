import sys
import time
import psycopg2
import os
from utill import *
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
        profile='DEV'
        if 'MACHINE_ENV' in os.environ:
            profile = os.environ['MACHINE_ENV']
        config = read_config(profile=profile)
        params = {}

        params['password'] = config['target_db']['password']
        params['ssm_name'] = config['target_db']['ssm_name']

        params['host'] = config['target_db']['host']
        logger.info("Target host - "+params['host'])

        params['port'] = config['target_db']['port']
        logger.info("Target port - "+ str(params['port']))

        params['username'] = config['target_db']['username']
        logger.info("Target username - "+params['username'])

        params['db_name'] = config['target_db']['db_name']
        logger.info("Target Database - "+params['db_name'])

        params['tables'] = config['tables']
        params['target_s3_path'] = config['aws']['s3_path']
        logger.info("s3 bucket path - "+params['target_s3_path'])

        params['role_arn'] = config['aws']['role_arn']

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

def create_db_connection(logger,hostname,database,username,password,port):
    try:
        connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = hostname,
            port = port)
        return connection
    except:
        logger.exception("Can't connect to redshift database.")

def store(logger,trgt_db_conn,table,s3_bucket_path,aws_role_arn,filter_column,upper_value,lower_value,unique_column):
    try:
        cur = trgt_db_conn.cursor()

        query=''

        if filter_column!='':
            query+=" create table #temp as select * from "+table + " limit 1; "
            query+=" TRUNCATE #temp ; "
            query+=" COMMIT; "
        else:
            query+=" TRUNCATE "+table +";"
            query+=" COMMIT; "

        query+ = " copy "+ (table if filter_column=="" else " #temp ") +" from '"+ s3_bucket_path +"'  iam_role '"+aws_role_arn+"' format as avro 'auto' ACCEPTANYDATE DATEFORMAT 'YYYY-MM-DD' TIMEFORMAT 'epochmillisecs'; "
        
        if filter_column!='':
            query+ = " delete from "+table+ " m"
            query+ = " using #temp t where 1=1 "
            if len(unique_column)>0:
                query+ ='  '.join( ' and m.'+uc+'=t.'+uc for uc in unique_column)

            query+="; commit; insert into "+table+" select * from #temp; "
            query+=" commit; drop table #temp; "        

        query+=" commit;"
        logger.info("Executing redshift copy command...")
        logger.info('\n\n'+query+'\n\n')
        cur.execute (query)
        logger.info("Redshift copy process finished")
    except Exception as e:
        logger.exception("Redshift copy process step error.")

def _process(params,table):
    logger=jobLogger(table['name'])

    try:
        process_start_time= time.time()
        logger.info('Starting process...')
        logger.info(table['name']+' process')
        table_name = table['name']

        filter_column=table['filter_column'] if table['filter_column'] is not None else ''
        upper_value=str(table['upper_value']) if table['upper_value'] is not None else ''
        lower_value=str(table['lower_value']) if table['lower_value'] is not None else ''
        unique_column=table['unique_column'] if table['unique_column'] is not None else []

        s3_bucket_path = params['target_s3_path'] + "/" + table_name + "/"
        logger.info('Processed file will save to - '+s3_bucket_path)

        password = params['password']
        if not password:
            logger.info('Logging using ssm_pass')
            password = ssm_pass()

        connection = create_db_connection(logger,params['host'] , params['db_name'], params['username'],password,params['port'])
        store(logger,connection,table_name,s3_bucket_path,params['role_arn'],filter_column,upper_value,lower_value,unique_column)

        process_end_time= time.time()
        logger.info('Process successfully completed.')
        logger.info('Total time taken - '+str(round(process_end_time - process_start_time, 2))+' sec.')
    except:
        logger.exception("Couldn't start process.")

def store_data(params):
    max_process= multiprocessing.cpu_count()
    if(max_process<=params['degree_of_parallelism']  or params['degree_of_parallelism'] <0):
        pool = Pool(max_process)
    else:
        pool = Pool(params['degree_of_parallelism'] )

    sub_process=partial(_process, params)
    pool.map(sub_process, params['tables'])


if __name__ == '__main__':
    logger=jobLogger('root')
    try:
        params = read_params(logger)
        store_data(params)
    except Exception as e:
        logger.exception("Couldn't start process.")
