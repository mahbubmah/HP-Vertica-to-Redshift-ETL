import sys
import time
sys.path.append('./env/lib/python2.7/site-packages/')
sys.path.append('./env/lib64/python2.7/site-packages/')
import psycopg2
import os
from utill import *
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
        params['password'] = config['target_db'].get('password', None)
        params['ssm_name'] = config['target_db'].get('ssm_name', None)

        params['host'] = config['target_db']['host']
        logger("Target host - "+params['host'],'info','root')

        params['port'] = config['target_db']['port']
        logger("Target port - "+ str(params['port']),'info','root')

        params['username'] = config['target_db']['username']
        logger("Target username - "+params['username'],'info','root')

        params['db_name'] = config['target_db']['db_name']
        logger("Target Database - "+params['db_name'],'info','root')
        

        params['target_s3_path'] = config['aws']['s3_path']
        logger("s3 bucket path - "+params['target_s3_path'],'info','root')

        params['role_arn'] = config['aws']['role_arn']

        params['dop']= args.dop

        logger("Degree of parallelism - "+ str(params['dop']),'info','root')

        logger('Reading configuration successfully.','info','root')

        return params
    except Exception as e:
        logger("Config file couldn't load",'exception','root')

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
        logger("Can't connect to redshift database.",'exception','root')

def store(logger,trgt_db_conn,table,s3_bucket_path,aws_role_arn,filter_column,upper_value,lower_value,unique_column):
    try:
        cur = trgt_db_conn.cursor()

        cur.execute('select count(*) rcnt from  '+table)
        total_record_res_before=cur.fetchone()
        logger('Total number of row before copy: '+str(total_record_res_before[0]),'info',table)        
        
        if int(total_record_res_before[0])==0:
            logger('There is no data in target table. Full copy process will run.','info',table)

        query=''

        if filter_column!=''  and int(total_record_res_before[0])>0:
            query+=" create table #temp as select * from "+table + " limit 1; "
            query+=" TRUNCATE #temp ; "
        else:
            query+=" TRUNCATE "+table +"; "

        query+=" copy "+ (table if filter_column=="" or int(total_record_res_before[0])==0 else " #temp ") +" from '"
        query+= s3_bucket_path +"'  iam_role '"
        query+= aws_role_arn+"' format as avro 'auto' ACCEPTANYDATE DATEFORMAT 'YYYY-MM-DD' TIMEFORMAT 'epochmillisecs'; "
        
        if filter_column!='' and int(total_record_res_before[0])>0:
            query+=" delete from "+table
            query+=" using #temp where 1=1 "
            if len(unique_column)>0:
                query+='  '.join( ' and #temp.'+uc+'='+table+'.'+uc for uc in unique_column)

            query+="; commit; insert into "+table+" select * from #temp; "
            query+=" commit; drop table #temp; "        

        query+=" commit;"
        logger("Executing redshift copy command...",'info',table)
        logger('\n\n'+query+'\n\n','info',table)
        cur.execute (query)


        cur.execute('select count(*) rcnt from  '+table)
        total_record_res_after=cur.fetchone()
        logger('Total number of row after copy: '+str(total_record_res_after[0]),'info',table)

        logger('Total number of row copied: '+str(int(total_record_res_after[0])-int(total_record_res_before[0])),'info',table)
        
        logger("Redshift copy process finished",'info',table)

    except Exception as e:
        logger("Redshift copy process step error.",'exception',table)

def _process(params,table):
    table_name = table['schema']+"."+table['name']
    jobLogger(table_name)

    try:
        process_start_time= time.time()
        logger('Starting process...','info',table_name)
        logger(table['name']+' process','info',table_name)
        
        src_schema =  table['schema']

        filter_column=''
        if 'filter_column' in table:
            filter_column=table['filter_column'] if table['filter_column'] is not None else ''
        
        upper_value=''
        if 'upper_value' in table:
            upper_value=str(table['upper_value']) if table['upper_value'] is not None else ''
        
        lower_value=''
        if 'lower_value' in table:
            lower_value=str(table['lower_value']) if table['lower_value'] is not None else ''

        unique_column=[]
        if 'unique_column' in table:
            unique_column=table['unique_column'] if table['unique_column'] is not None else []

        tmp_file =open("tmp.txt","r")
        date_prefix = tmp_file.read()
        s3_bucket_path =  params['target_s3_path'] +"/"+src_schema+"/" +table['name'] + "/" + date_prefix +"/" 
        logger('Processed file will save to - '+s3_bucket_path,'info',table_name)

        password = params['password']
        if not password:
            logger('Logging using ssm_pass','info',table_name)
            password = ssm_pass(params['ssm_name'])

        connection = create_db_connection(logger,params['host'] , params['db_name'], params['username'],password,params['port'])
        store(logger,connection,table_name,s3_bucket_path,params['role_arn'],filter_column,upper_value,lower_value,unique_column)

        process_end_time= time.time()
        logger('Process successfully completed.','info',table_name)
        logger('Total time taken - '+str(round(process_end_time - process_start_time, 2))+' sec.','info',table_name)
    except:
        logger("Couldn't start process.","exception",table_name)

def store_data(params):
    pool = Pool(params['dop'] )

    sub_process=partial(_process, params)
    pool.map(sub_process, params['tables'])


if __name__ == '__main__':
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

        if '.json' in str(args.config):
            config = read_config(profile=profile,path=args.config)

        if args.dop is None:
            args.dop=config['aws']['dop']

        if '.json' in str(args.tables):
            params['tables'] = read_tables(path=str(args.tables))
        else:
            if '.' not in args.tables:
                logger('Please provide the schema name','error','root')
                
            table_name_with_schema = args.tables.split('.')
            table_name_only = table_name_with_schema[1]
            table_schema = table_name_with_schema[0]

            params['tables'] = json.loads('[{"schema": "'+table_schema+'","name": "'+table_name_only+'"}]')
        
        params = read_params(args,logger,config,params)

        store_data(params)
    except Exception as e:
        logger("Couldn't start process.","exception","root")

