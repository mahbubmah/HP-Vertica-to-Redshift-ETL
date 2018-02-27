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
from functools import wraps

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
    with open(path,'r') as f:
        config=json.load(f)

    return config[profile]

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