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

def stage_src_data(args,table_name,p_kyes):
    s3_bucket_path = args.target_s3_path +"/"+table_name    
    destroy_s3_bucket(s3_bucket_path)

    query = 'SELECT t.* FROM '+table_name+' t where $CONDITIONS'
    cmd_dump_to_s3 = "sqoop import --driver " + args.src_driver + " --connect " + args.src_db_url +" --username "+ args.src_username+" --password " + args.src_password +   " --query '"+ query +"' --target-dir "+ s3_bucket_path +" --direct --as-avrodatafile -m "+str( args.number_of_mappers)

    if( args.number_of_mappers>1 and p_kyes!=[]):
        split_column=' t.'+(', t.'.join(p_kyes))        
        cmd_dump_to_s3 += " --split-by "+split_column

    subprocess.call(cmd_dump_to_s3,shell=True)

def process(args,table):    
    p_kyes=[]
    if p_kyes is not None:
        for p_kye in table['kyes']:
            p_kyes.append(p_kye)
    
    stage_src_data(args,table['name'],p_kyes)


def sync_data(args):
    max_process= multiprocessing.cpu_count()
    if(max_process<=args.degree_of_parallelism or args.degree_of_parallelism<0):
        pool = Pool(max_process)
        print('Maximun '+str(max_process)+' process using...')
    else:
        pool = Pool(args.degree_of_parallelism)

    sub_process=partial(process, args)
    pool.map(sub_process, args.tables)


if __name__ == '__main__':
    config=read_config()
    parser = argparse.ArgumentParser(description='data transfer')
    parser.add_argument('--aws_role_arn', action="store", dest="aws_role_arn"
        , required=False, default=config['aws']['role_arn'])

    parser.add_argument('--target_s3_path', action="store", dest="target_s3_path"
        , required=False, default=config['aws']['s3_path'])
    parser.add_argument('--tables', action="store", dest="tables"
        , required=False, default=config['tables'])
    parser.add_argument('--src_driver', action="store", dest="src_driver"
        , required=False, default=config['source_db']['driver'])
    parser.add_argument('--src_db_url', action="store", dest="src_db_url"
        , required=False, default=config['source_db']['db_url'])
    parser.add_argument('--src_username', action="store", dest="src_username"
        , required=False, default=config['source_db']['username'])
    parser.add_argument('--src_password', action="store", dest="src_password"
        , required=False, default=config['source_db']['password'])


    parser.add_argument('--degree_of_parallelism', action="store", required=False
        , dest="degree_of_parallelism", type=int, default=config['aws']['degree_of_parallelism'])
    parser.add_argument('--number_of_mappers', action="store", dest="number_of_mappers"
        , type=int, default=config['aws']['number_of_mappers'], required=False)

    args = parser.parse_args()
    sync_data(args)