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

def destroy_s3_bucket(s3_bucket_path):
    command = "aws s3 rm "+s3_bucket_path+" --recursive"
    subprocess.call(command,shell=True)

def create_db_connection(hostname,database,username,password,port):
    try:
        connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = hostname,
            port = port)
    except:
        print ("unable to connect to database")

    return connection

def download_s3_data(source,dest):
    bucket_name = source.split('/')[2]
    prefix = '/'.join(source.split('/')[3:])

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    object_coll = bucket.objects.filter(Prefix=prefix)
    for object_ in object_coll:
        file_name = object_.key.split('/').pop()
        if file_name == '':
            continue

        s3.Object(bucket_name, object_.key).download_file(
            dest + os.sep + file_name)

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
    destroy_s3_bucket(s3_bucket_path)
    query = 'SELECT t.* FROM '+table+' t where $CONDITIONS'
    if(number_of_mappers>1):
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url +" --username "+ src_username+" --password " + src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m "+str(number_of_mappers) + " --split-by t."+split_column
    else:
        cmd_dump_to_s3 = "sqoop import --driver " + src_driver + " --connect " + src_db_url +" --username "+ src_username+" --password " + src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m 1"
    # print(cmd_dump_to_s3)
    subprocess.call(cmd_dump_to_s3,shell=True)
    
def store_data(trgt_db_conn,table,s3_bucket_path,aws_role_arn):
    cur = trgt_db_conn.cursor()

    cur.execute("TRUNCATE "+table)
    cur.execute("COMMIT;")
    cmd_copy_to_trgt = "copy "+ table +" from '"+ s3_bucket_path +"'"+" iam_role '"+aws_role_arn+"'"+" format as avro 'auto' ACCEPTANYDATE DATEFORMAT 'YYYY-MM-DD' TIMEFORMAT 'epochmillisecs';"
    cur.execute (cmd_copy_to_trgt)
    cur.execute("COMMIT;")
    print ("PROCESSING COMPLETE FOR TABLE : "+table)

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

    trgt_db_conn = create_db_connection(args.trgt_db_host,args.trgt_db_name,args.trgt_username,args.trgt_password,args.trgt_port)
    s3_bucket_path = args.target_s3_path +"/"+table
    stage_src_data(table,s3_bucket_path,args.src_driver,args.src_db_url,args.src_username,args.src_password,number_of_mappers,split_column)
    store_data(trgt_db_conn,table,s3_bucket_path,args.aws_role_arn)


def sync_data(args):
    max_process= multiprocessing.cpu_count()
    if(max_process<=args.degree_of_parallelism):
        pool = Pool(max_process)
    elif(args.degree_of_parallelism<=0):
        pool = Pool(1)
    else:
        pool = Pool(args.degree_of_parallelism)

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


    parser.add_argument('--trgt_db_host', action="store", dest="trgt_db_host", required=True)
    parser.add_argument('--trgt_db_name', action="store", dest="trgt_db_name", required=True)
    parser.add_argument('--trgt_username', action="store", dest="trgt_username", required=True)
    parser.add_argument('--trgt_password', action="store", dest="trgt_password", required=True)
    parser.add_argument('--trgt_port', action="store", dest="trgt_port", required=True)
    parser.add_argument('--degree_of_parallelism', action="store", dest="degree_of_parallelism", type=int, default=1)
    parser.add_argument('--number_of_mappers', action="store", dest="number_of_mappers", type=int, default=1)

    args = parser.parse_args()
    sync_data(args)
