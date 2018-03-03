import time
from utill import memoize, read_config
from logger import *
import shutil

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
        logger.info("s3 bucket path - "+params['target_s3_path'])

        return params

    except Exception as e:
        logger.exception("Config file couldn't load")

def upload_log_file(s3_bucket_path):
    command = "aws s3 sync ./log " + s3_bucket_path + "/" + time.strftime('%Y%m%d/%H%M%S') + "/"
    subprocess.call(command, shell=True)

def clear_dir(path):
    shutil.rmtree(path)

def _process(params):
    upload_log_file(params['target_s3_path'])
    clear_dir("log")

if __name__ == '__main__':
    logger=jobLogger('root')
    try:
        params = read_params(logger)
        _process(params)
    except Exception as e:
        logger.exception("Couldn't start process.")