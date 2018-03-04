import time
from utill import memoize, read_config
from logger import *
import shutil
import subprocess
import multiprocessing
from functools import partial
from multiprocessing import Pool

@memoize
def read_params(logger):
    try:
        logger.info('Starting reading configuration....')
        profile='DEV'
        if 'MACHINE_ENV' in os.environ:
            profile = os.environ['MACHINE_ENV']
        config = read_config(profile=profile)
        params = {}

        params['target_s3_path'] = config['aws']['s3_path']
        params['tables'] = config['tables']
        logger.info("s3 bucket path - "+params['target_s3_path'])

        max_process = multiprocessing.cpu_count()
        if(max_process<=config['aws']['degree_of_parallelism']  or config['aws']['degree_of_parallelism'] <0):
            logger.info ("Setting degree of parallelism to cpu count "+ str(max_process))
            params['degree_of_parallelism'] = max_process
        else:
            params['degree_of_parallelism']= config['aws']['degree_of_parallelism']

        return params

    except Exception as e:
        logger.exception("Config file couldn't load")

def upload_log_file(s3_bucket_path,logger):
    logger.info("Uploading log file")
    command = "aws s3 sync ./log " + s3_bucket_path + "/logs/" + time.strftime('%Y%m%d/%H%M%S') + "/"
    subprocess.call(command, shell=True)
    logger.info("Log file uploaded successfully")

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
    max_process= multiprocessing.cpu_count()
    if(max_process<=params['degree_of_parallelism']  or params['degree_of_parallelism'] <0):
        pool = Pool(max_process)
    else:
        pool = Pool(params['degree_of_parallelism'])

    # sub_process=(stage_temp_file, params)
    # pool.map(sub_process, params['tables'])

    upload_log_file(params['target_s3_path'],logger)
    clear_dir("log")

if __name__ == '__main__':
    logger=jobLogger('root')
    try:
        params = read_params(logger)
        _process(params,logger)
    except Exception as e:
        logger.exception("Couldn't start process.")