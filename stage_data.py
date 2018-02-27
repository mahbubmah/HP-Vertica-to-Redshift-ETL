import sys
sys.path.append('./env/lib/python2.7/site-packages/')
sys.path.append('./env/lib64/python2.7/site-packages/')
import argparse
import subprocess
import psycopg2
import vertica_python
import os
import pdb
import shlex
import boto3
import json
from utill import download_s3_data, memoize, read_config

@memoize
def ssm_pass():
    out = subprocess.Popen('aws ssm get-parameters --names "'+params['ssm_name']+'" --with-decryption',stdout=subprocess.PIPE,shell=True)
    params = json.loads(out.stdout.read())
    # taking first or last version only
    return params['Parameters'][0]['Value']


def read_params():
    config = read_config()
    params = {}
    params['password']= config['source_db']['password']
    params['ssm_name']= config['source_db']['ssm_name']
    params['src_driver']= config['source_db']['driver']
    params['host']= config['source_db']['host']
    params['port']= config['source_db']['port']
    params['username']= config['source_db']['username']
    params['db_name']= config['source_db']['db_name']
    params['tables']= config['source_db']['tables']
    params['number_of_mappers']= config['aws']['number_of_mappers']
    params['target_s3_path']= config['aws']['s3_path']

    return params
    

def connect_vertica_db(params):   
    host = params['host']
    port = params['port']
    username = params['username']
    password = params['password']
    if not password:
        password = ssm_pass()
    db = params['db_name']
    conn_info = {'host': host, 'port': port,'user': username,'password': password, 'database': db,'read_timeout': 600,'unicode_error': 'strict','ssl': False,'connection_timeout': 5}
    connection = vertica_python.connect(**conn_info)
    return connection

def destroy_s3_bucket(s3_bucket_path):
    command = "aws s3 rm "+s3_bucket_path+" --recursive"
    subprocess.call(command,shell=True)

def lower_table_column_names(table_name):
    connection=connect_vertica_db(params)
    cursor=connection.cursor()
    table_name_with_schema=[]
    table_name_only=table_name
    table_schema=''
    sql=''
    sql_schema_condition=''
    if '.' in table_name:
        table_name_with_schema=table_name.split('.')
        table_name_only=table_name_with_schema[1]
        table_schema=table_name_with_schema[0]
        sql_schema_condition+=" and t.table_schema='"+table_schema+"'"   


    sql+="select lower(column_name) l_column_name, lower(data_type) data_type from v_catalog.columns t  where t.table_name='"+table_name_only+"' "+sql_schema_condition+";"
    # print(sql)

    cursor.execute(sql)
    column_names=cursor.fetchall()
    connection.close()
    return column_names

def get_table_name_list(table_src):
    if(table_src.startswith("s3")):
        download_s3_data(table_src,os.getcwd())
        file_name = table_src.split("/")[-1]
        table_file = open(file_name,'r')
        list_table = list(table_file)
        table_file.close()
    else:
        list_table= table_src.split(",")

    return list_table

def stage_src_data(table,s3_bucket_path,src_driver,src_db_url,src_username,src_password,number_of_mappers,split_column):
    print(s3_bucket_path)
    l_column_names=lower_table_column_names(table)
    print(l_column_names)
    destroy_s3_bucket(s3_bucket_path) 
    select_str=', '.join('cast(to_hex('+str(v[0])+') as varchar) '+str(v[0]) if 'binary' in v[1] else str(v[0])  for v in l_column_names)
    query = "select "+select_str+" FROM "+table+" t where $CONDITIONS"
    print(query)
    if(number_of_mappers>1):
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url +" --username "+ src_username+" --password " + src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m "+str(number_of_mappers) + " --split-by t."+split_column
    else:
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url +" --username "+ src_username+" --password " + src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m 1"
    subprocess.call(cmd_dump_to_s3,shell=True)

def _process(params,table_line):
    table_line = table_line.strip()
    split_column =""
    table_line = table_line.split(" ")
    table = table_line[0]
    if(len(table_line)>1):
        split_column = table_line[1]
        number_of_mappers=params['number_of_mappers']
    else:
        number_of_mappers=1

    s3_bucket_path = params['target_s3_path'] +"/"+table+"/"
    src_db_url = "jdbc:vertica://"+params['host']+"/"+params['db_name']
    password = params['password']
    if not password:
        password = ssm_pass()
    #try:
    stage_src_data(table,s3_bucket_path,params['src_driver'],src_db_url,params['username'],password,number_of_mappers,split_column)
    #except:
    #    print("ERROR PROCESSING TABLE : "+table)


def sync_data(params):
    table_name_list = get_table_name_list(params['tables'])
    for table_line in table_name_list:
        _process(params, table_line)


if __name__ == '__main__':
    params = read_params()
    sync_data(params)