import time
from utill import memoize, read_config
from logger import *
import shutil
import subprocess
import multiprocessing
from functools import partial
from multiprocessing import Pool
import json

@memoize
def read_params(logger):
    try:
        logger('Starting reading configuration....','info','root')
        profile='DEV'
        if 'MACHINE_ENV' in os.environ:
            profile = os.environ['MACHINE_ENV']
        config = read_config(profile=profile)
        params = {}

        params['target_s3_path'] = config['aws']['s3_path']
        table_config = json.load(open("tables.json"))
        params['tables'] = table_config
        logger("s3 bucket path - "+params['target_s3_path'],'info','root')
        
        print (config)
        max_process = multiprocessing.cpu_count()
        if(max_process<=config['aws']['dop']  or config['aws']['dop'] <0):
            logger("Setting degree of parallelism to cpu count "+ str(max_process),'info','root')
            params['degree_of_parallelism'] = max_process
        else:
            params['degree_of_parallelism']= config['aws']['dop']

        return params

    except Exception as e:
        logger("Config file couldn't load",'exception','root')

def upload_log_file(s3_bucket_path,logger):
    logger("Uploading log file",'info','root')
    command = "aws s3 sync ./log " + s3_bucket_path + "/logs/"
    subprocess.call(command, shell=True)
    logger("Log file uploaded successfully",'info','root')

def clear_dir(path):
    shutil.rmtree(path)

def destroy_s3_folder(s3_bucket_path):
    command = "aws s3 rm " + s3_bucket_path + " --recursive"
    subprocess.call(command, shell=True)

def sync_two_s3_folder(src,dest):
    command = "aws s3 sync " + src + " "+ dest
    subprocess.call(command, shell=True)

def stage_temp_file(params,table):
    table_name = table['name']
    s3_bucket_path = params['target_s3_path'] + "/" + table_name + "/"
    destroy_s3_folder(s3_bucket_path)
    s3_bucket_path_tmp = params['target_s3_path'] + "/" + table_name + "_tmp/"
    sync_two_s3_folder(s3_bucket_path_tmp,s3_bucket_path)
    destroy_s3_folder(s3_bucket_path_tmp)

def _process(params,logger):
    # max_process= multiprocessing.cpu_count()
    # if(max_process<=params['degree_of_parallelism']  or params['degree_of_parallelism'] <0):
    #     pool = Pool(max_process)
    # else:
    #     pool = Pool(params['degree_of_parallelism'])

    # sub_process=(stage_temp_file, params)
    # pool.map(sub_process, params['tables'])

    upload_log_file(params['target_s3_path'],logger)
    clear_dir("log")

if __name__ == '__main__':
    jobLogger('root')
    try:
        params = read_params(logger)
        _process(params,logger)
    except Exception as e:
        logger("Couldn't start process.",'exception','root')
