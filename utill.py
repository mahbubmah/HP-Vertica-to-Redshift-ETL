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
import ConfigParser
import json
import vertica_python

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


def read_config(path='config.json'):
    config=ConfigParser.ConfigParser()

    with open(path,'r') as f:
        config=json.load(f)

    return config



def connect_vertica_db():   
    
    conn_info = {'host': 'ec2-52-90-229-247.compute-1.amazonaws.com', 'port': 5433,'user': 'dbadmin','password': 'vfr45tgb', 'database': 'sabredb','read_timeout': 600,'unicode_error': 'strict','ssl': False,'connection_timeout': 5}
    connection = vertica_python.connect(**conn_info)
    return connection
