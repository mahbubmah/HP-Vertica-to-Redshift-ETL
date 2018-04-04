import sys
import time
import subprocess
import vertica_python
import json
from utill import *
import os
from logger import *
import multiprocessing
from functools import partial
from multiprocessing import Pool
import json
import argparse

@memoize
def ssm_pass(ssm_name):
    assert ssm_name is not None
    out = subprocess.Popen('aws ssm get-parameters --names "' + ssm_name + '" --with-decryption',
                           stdout=subprocess.PIPE, shell=True)
    params = json.loads(out.stdout.read())
    # taking first or last version only
    if type(params['Parameters'])==list:
        return params['Parameters'][0]['Value']
    return params['Parameters']['Value']


def read_params(args,logger,config,params):
    try:
        logger('Starting reading configuration....','info','root')

        
        params['password'] = config['source_db'].get('password', None)
        params['ssm_name'] = config['source_db'].get('ssm_name', None)

        params['src_driver'] = config['source_db']['driver']
        logger("Source Driver - "+params['src_driver'],'info','root')

        params['host'] = config['source_db']['host']
        logger("Source Host - "+params['host'],'info','root')

        params['port'] = config['source_db']['port']
        logger("Source port - "+str(params['port']),'info','root')

        params['username'] = config['source_db']['username']
        logger("Source username - "+params['username'],'info','root')

        params['db_name'] = config['source_db']['db_name']
        logger("Source database - "+params['db_name'],'info','root')

        

        params['target_s3_path'] = config['aws']['s3_path']
        logger("s3 bucket path - "+params['target_s3_path'],'info','root')

        params['dop']= args.dop

        logger("Degree of parallelism - "+ str(params['dop']),'info','root')

        logger('Reading configuration successfully.','info','root')
        return params

    except Exception as e:
        logger("Config file couldn't load",'exception','root')

def connect_vertica_db(logger,params):
    try:
        host = params['host']
        port = params['port']
        username = params['username']
        password = params['password']
        if not password:
            password = ssm_pass(params['ssm_name'])
        db = params['db_name']
        conn_info = {'host': host, 'port': port, 'user': username, 'password': password, 'database': db,
                     'read_timeout': 600, 'unicode_error': 'strict', 'ssl': False, 'connection_timeout': 5}
        
        connection = vertica_python.connect(**conn_info)
        return connection
    except Exception as e:
        logger("Can't connect to vertica database.",'exception','root')


def destroy_s3_bucket(s3_bucket_path,exclude_dir=''):
    command = "aws s3 rm " + s3_bucket_path + " --recursive" +((" --exclude "+exclude_dir) if exclude_dir != '' else '')
    print(command)
    subprocess.call(command, shell=True)


def lower_table_column_names(logger,table_name):
    try:
        connection = connect_vertica_db(logger,params)
        cursor = connection.cursor()
        table_name_only = table_name
        sql = ''
        sql_schema_condition = ''
        if '.' in table_name:
            table_name_with_schema = table_name.split('.')
            table_name_only = table_name_with_schema[1]
            table_schema = table_name_with_schema[0]
            sql_schema_condition += " and t.table_schema='" + table_schema + "'"

        sql += "select lower(column_name) l_column_name, lower(data_type) data_type from v_catalog.columns t  where t.table_name='" + table_name_only + "' " + sql_schema_condition + ";"

        logger('Query for select column: \n\n'+sql+'\n','info',table_name)

        cursor.execute(sql)
        column_names = cursor.fetchall()
        connection.close()
        return column_names
    except Exception as e:
        logger("Couldn't read table column name",'exception','root')



def stage_src_data(logger,schema,table, s3_bucket_path, src_driver, src_db_url, src_username, src_password, number_of_mappers,split_column,filter_column,upper_value,lower_value,delta_time,delta_time_unit,delta_time_pattern):
    try:
        table_log = schema+"."+table
        l_column_names = lower_table_column_names(logger,schema+'.'+table)

        destroy_s3_bucket(s3_bucket_path)
        select_str = ', '.join(
            'cast(to_hex(' + str(v[0]) + ') as varchar) ' + str(v[0]) if 'binary' in v[1] else str(v[0]) for v in
            l_column_names)
        if schema:
            table = schema + "." + table

        query="select " + select_str + " FROM " + table         


        if filter_column!='' and (upper_value!='' or lower_value!='' or delta_time!=-1):
            query=" select * from ( "+query+" ) as fil "
            if delta_time!=-1:

                for col in l_column_names:
                    if str(col[0]).lower()==filter_column.lower():
                        if 'char' in str(col[1]).lower():
                            filter_column=" to_timestamp( "+filter_column+" ,'"+delta_time_pattern+"') "


                query+=" where "+filter_column
                query+=" >= current_timestamp+interval '-"+str(delta_time)+"  "+delta_time_unit+"'  "
            else:
                query+=" where "+filter_column
                if upper_value!='' and lower_value!='':
                    query+=" between '"+lower_value+"' and '"+upper_value+"' "

                if upper_value!='' and lower_value=='':
                    query+=" <= '"+upper_value+"' "

                if upper_value=='' and lower_value!='':
                    query+=" >= '"+lower_value+"' "

        con = connect_vertica_db(logger,params)
        cur = con.cursor()

        cur.execute('select count(*) rcnt from ( '+query+' ) as t')
        total_record_res=cur.fetchone()
        logger('Total number of row will process: '+str(total_record_res[0]),'info',table_log)
        con.close()


        query = "select * from ( "+query + " ) as t  where \$CONDITIONS"
        logger(' Sqoop job query: \n\n'+query+'\n','debug',table_log)
        tmp_file =open("tmp.txt","r")
        date_prefix = tmp_file.read()
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url + " --username " + src_username + " --password " + src_password + " --query \"" + query + "\" --target-dir " + s3_bucket_path + " --direct --as-avrodatafile -m " + str(
                number_of_mappers) + ((" --split-by " + split_column) if split_column !='' else '')  + " -- --schema "+schema
        logger("Sqoop job command \n\n"+cmd_dump_to_s3+"\n\n",'info',table_log)
        logger('Sqoop job starting...','info',table_log)
        pipe=subprocess.Popen(cmd_dump_to_s3, shell=True,stdout = subprocess.PIPE, bufsize=10**8)
        pipe.wait()
        
        

        if filter_column=='':
            logger('deleting previous files.....','info',table_log)
            destroy_s3_bucket(s3_bucket_path.replace(date_prefix+"/",""),date_prefix+"/*")

        logger('Sqoop job finished.','info',table_log)
    except Exception as e:
        logger("Sqoop job process step error.",'exception',table_log)


def _process(params, table):
    table_log = table['schema']+"."+table['name']
    jobLogger(table_log)
    try:        
        process_start_time= time.time()

        logger('Starting process...','info',table_log)
        

        table_name = table['name']

        number_of_mappers =1
        if 'mappers' in table:  
            number_of_mappers= table['mappers']
            if table['mappers']==1:
                logger("You've set the job to sun on single mapper, this might take longer time for procssing.",'info',table_log)

        logger(table['name']+' process using '+str(number_of_mappers)+' mapper(s)','info',table_log)
        
        if table['schema']:
            schema = table['schema']
        else:
            schema = ''

        split_column=''
        if 'split_column' in table:            
            if table['split_column'] is None:
                logger('There is no split column found. sqoop job might run on single mapper. this will take longer time to run job','warning',table_log)
            else:
                split_column = table['split_column']
        else:
            logger('There is no split column found. sqoop job might run on single mapper. this will take longer time to run job','warning',table_log)

        filter_column=''
        if 'filter_column' in table:
            filter_column=table['filter_column'] if table['filter_column'] is not None else ''
        
        upper_value=''
        if 'upper_value' in table:
            upper_value=str(table['upper_value']) if table['upper_value'] is not None else ''
        
        lower_value=''
        if 'lower_value' in table:
            lower_value=str(table['lower_value']) if table['lower_value'] is not None else ''

        delta_time=-1
        if 'delta_time' in table:
            delta_time=table['delta_time']

        delta_time_unit="hour"
        if 'delta_time_unit' in table:
            delta_time_unit=table['delta_time_unit']

        delta_time_pattern="YYYY-MM-DD HH:MI:SS"
        if 'delta_time_pattern' in table:
            delta_time_pattern=table['delta_time_pattern']

        tmp_file =open("tmp.txt","r")
        date_prefix = tmp_file.read()
        s3_bucket_path = params['target_s3_path'] + "/"+schema+"/" + table_name + "/" + date_prefix + "/" 
        
        
        

        logger('Processed file will save to - '+s3_bucket_path,'info',table_log)

        src_db_url = "jdbc:vertica://" + params['host'] + "/" + params['db_name']
        logger('Source Database URL: '+src_db_url,'info',table_log)
        password = params['password']
        if not password:
            logger('Logging using ssm_pass','info',table_log)
            password = ssm_pass(params['ssm_name'])

        stage_src_data(logger,schema,table_name, s3_bucket_path, params['src_driver'], src_db_url, params['username'], password,number_of_mappers, split_column,filter_column,upper_value,lower_value,delta_time,delta_time_unit,delta_time_pattern)

        process_end_time= time.time()
        logger('Process successfully completed.','info',table_log)
        logger('Total time taken - '+str(round(process_end_time - process_start_time, 2))+' sec.','info',table_log)
    except Exception as e:
        logger("Couldn't start process.",'exception',table_log)
    


def sync_data(params):
    pool = Pool(params['dop'])

    sub_process=partial(_process, params)
    pool.map(sub_process, params['tables'])
    

if __name__ == '__main__':

    date_prefix = time.strftime('dt=%Y-%m-%d-%H-%M')
    tmp_file =open("tmp.txt","w")
    tmp_file.write(date_prefix)
    tmp_file.close() 
    jobLogger('root')
    try:
        parser = argparse.ArgumentParser(description='data transfer')
        params = {}
        profile='DEV'
        if 'MACHINE_ENV' in os.environ:
            profile = os.environ['MACHINE_ENV']
        parser.add_argument('--config', action="store", required=False , dest="config", default='config.json')
        parser.add_argument('--dop', action="store", required=False
        , dest="dop", type=int)
        parser.add_argument('--tables', action="store", required=False
        , dest="tables", default='tables.json')
        
        args = parser.parse_args()

        print(args.config)
        if '.json' in str(args.config):
            config = read_config(profile=profile,path=args.config)

        if args.dop is None:
            args.dop=config['aws']['dop']


        if '.json' in str(args.tables):
            params['tables'] = read_tables(path=str(args.tables))

        else:
            if '.' not in args.tables:
                logger('Please provide the schema name','error','root')

            table_name_with_schema = str(args.tables).split('.')
            table_name_only = table_name_with_schema[1]
            table_schema = table_name_with_schema[0]

            params['tables'] = json.loads('[{"schema": "'+table_schema+'","name": "'+table_name_only+'"}]')
        
        params = read_params(args,logger,config,params)
        print(params)

        sync_data(params)
    except Exception as e:
        logger("Couldn't start process.",'exception','root')

