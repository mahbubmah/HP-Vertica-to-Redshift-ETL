import sys
sys.path.append('./env/lib/python2.7/site-packages/')
sys.path.append('./env/lib64/python2.7/site-packages/')
import argparse
import subprocess
import psycopg2
import multiprocessing
from functools import partial
from multiprocessing import Pool
import os
import pdb
import shlex
import shutil
import tempfile
import boto3
from utill import *

def destroy_s3_bucket(s3_bucket_path):
    command = "aws s3 rm "+s3_bucket_path+" --recursive"
    subprocess.call(command,shell=True)

def lower_table_column_names(table_name):
    connection=connect_vertica_db()
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
    
    sql+="select lower(column_name) l_column_name from v_catalog.columns t  where t.table_name='"+table_name_only+"' "+sql_schema_condition+";"
    print(sql)
        

    cursor.execute(sql)
    column_names=cursor.fetchall()
    connection.close()
    return column_names

def get_table_desc(tables):
    if(tables.startswith("s3")):
        download_s3_data(tables,os.getcwd())
        file_name = tables.split("/")[-1]
        table_file = open(file_name,'r')
        list_table = list(table_file)
        table_file.close()
    else:
        list_table= tables.split(",")

    return list_table

def stage_src_data(table,s3_bucket_path,src_driver,src_db_url,src_username,src_password,number_of_mappers,split_column):
    print(s3_bucket_path)
    l_column_names=lower_table_column_names(table)
    print(l_column_names)
    destroy_s3_bucket(s3_bucket_path) 

    
    query = "select "+(', '.join(str(v[0]) for v in l_column_names))+" FROM "+table+"  where $CONDITIONS"
    print(query)
    if(number_of_mappers>1):
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url +" --username "+ src_username+" --password " + src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m "+str(number_of_mappers) + " --split-by t."+split_column
    else:
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url +" --username "+ src_username+" --password " + src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m 1"
    subprocess.call(cmd_dump_to_s3,shell=True)

def process(args,table_desc):
    table_desc = table_desc.strip()
    split_column =""
    table_desc = table_desc.split(" ")
    table = table_desc[0]
    if(len(table_desc)>1):
        split_column = table_desc[1]
        number_of_mappers=args.number_of_mappers
    else:
        number_of_mappers=1

    s3_bucket_path = args.target_s3_path +"/"+table+"/"
    #try:
    stage_src_data(table,s3_bucket_path,args.src_driver,args.src_db_url,args.src_username,args.src_password,number_of_mappers,split_column)
    #except:
    #    print("ERROR PROCESSING TABLE : "+table)


def sync_data(args):
    max_process= multiprocessing.cpu_count()
    if(max_process<=args.degree_of_parallelism):
        pool = Pool(max_process)
    elif(args.degree_of_parallelism<=0):
        pool = Pool(1)
    else:
        pool = Pool(args.degree_of_parallelism)

    # process(args,'DimMktSource')
    table_desc_list = get_table_desc(args.tables)
    sub_process=partial(process, args)
    pool.map(sub_process, table_desc_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='data transfer')
    parser.add_argument('--aws_role_arn', action="store", dest="aws_role_arn", required=True)

    parser.add_argument('--target_s3_path', action="store", dest="target_s3_path", required=True)
    parser.add_argument('--tables', action="store", dest="tables", required=False)
    parser.add_argument('--src_driver', action="store", dest="src_driver", required=True)
    parser.add_argument('--src_db_url', action="store", dest="src_db_url", required=True)
    parser.add_argument('--src_username', action="store", dest="src_username", required=True)
    parser.add_argument('--src_password', action="store", dest="src_password", required=True)


    parser.add_argument('--degree_of_parallelism', action="store", dest="degree_of_parallelism", type=int, default=1)
    parser.add_argument('--number_of_mappers', action="store", dest="number_of_mappers", type=int, default=1)

    args = parser.parse_args()
    sync_data(args)
