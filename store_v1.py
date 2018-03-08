import sys
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

def store(trgt_db_conn,table,s3_bucket_path,aws_role_arn):
    cur = trgt_db_conn.cursor()

    cur.execute("TRUNCATE "+table)
    cur.execute("COMMIT;")
    cmd_copy_to_trgt = "copy "+ table +" from '"+ s3_bucket_path +"'"+" iam_role '"+aws_role_arn+"'"+
    " format as avro 'auto' ACCEPTANYDATE DATEFORMAT 'YYYY-MM-DD' TIMEFORMAT 'epochmillisecs';"
    cur.execute (cmd_copy_to_trgt)
    cur.execute("COMMIT;")
    print ("PROCESSING COMPLETE FOR TABLE : "+table)

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

def process(args,table_desc):
    table_desc = table_desc.strip()
    table_desc = table_desc.split(" ")
    table = table_desc[0]

    trgt_db_conn = create_db_connection(args.trgt_db_host,args.trgt_db_name,args.trgt_username,args.trgt_password,args.trgt_port)
    s3_bucket_path = args.target_s3_path +"/"+table
    try:
       store(trgt_db_conn,table,s3_bucket_path,args.aws_role_arn)
    except:
       print("ERROR PROCESSING TABLE : "+table)

def store_data(args):
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


    parser.add_argument('--trgt_db_host', action="store", dest="trgt_db_host", required=True)
    parser.add_argument('--trgt_db_name', action="store", dest="trgt_db_name", required=True)
    parser.add_argument('--trgt_username', action="store", dest="trgt_username", required=True)
    parser.add_argument('--trgt_password', action="store", dest="trgt_password", required=True)
    parser.add_argument('--trgt_port', action="store", dest="trgt_port", required=True)
    parser.add_argument('--degree_of_parallelism', action="store", dest="degree_of_parallelism", type=int, default=1)

    args = parser.parse_args()
    store_data(args)
