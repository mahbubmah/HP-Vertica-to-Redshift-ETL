import sys
sys.path.append('./env/lib/python2.7/site-packages/')
sys.path.append('./env/lib64/python2.7/site-packages/')
import boto3
import os
import json
from functools import wraps
import subprocess

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


def read_config(path='config.json',profile="DEV"):
    if 's3:/' in path.lower():
        try:
            os.remove('config.json')
        except OSError:
            pass
        file_name = path.split("/").pop()
        download(path)
        os.rename(file_name,"config.json")
        path='config.json'
    config = json.load(open(path))
    
    return (config[profile] if profile in config else config)

def download(path):  
    file_name = path.split("/").pop()
    cmd =" aws s3 cp "+ path + " ./"
    subprocess.call(cmd, shell=True)

def read_tables(path='tables.json'):
    
    
    if 's3:/' in path.lower():
        try:
            os.remove('tables.json')
        except OSError:
            pass
        file_name = path.split("/").pop()    
        # download_s3_data(path,'/')
        download(path)
        os.rename(file_name,"tables.json")
        path='tables.json'
    
    with open(path,'r') as f:
        tables=json.load(f)

    return tables

def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper
