import sys
sys.path.append('./env/lib/python2.7/site-packages/')
sys.path.append('./env/lib64/python2.7/site-packages/')
import psycopg2
import os
from utill import *
from utill import memoize, read_config


@memoize
def ssm_pass():
    out = subprocess.Popen('aws ssm get-parameters --names "' + params['ssm_name'] + '" --with-decryption',
                           stdout=subprocess.PIPE, shell=True)
    params = json.loads(out.stdout.read())
    # taking first or last version only
    return params['Parameters'][0]['Value']

@memoize
def read_params():
    profile = os.environ['MACHINE_ENV']
    config = read_config(profile=profile)
    params = {}
    params['password'] = config['target_db']['password']
    params['ssm_name'] = config['target_db']['ssm_name']
    params['src_driver'] = config['target_db']['driver']
    params['host'] = config['target_db']['host']
    params['port'] = config['target_db']['port']
    params['username'] = config['target_db']['username']
    params['db_name'] = config['target_db']['db_name']
    params['tables'] = config['tables']
    params['target_s3_path'] = config['aws']['s3_path']
    params['role_arn'] = config['aws']['role_arn']

    return params

def create_db_connection(hostname,database,username,password,port):
    try:
        connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = hostname,
            port = port)
        return connection
    except:
        print ("unable to connect to database")

def store(trgt_db_conn,table,s3_bucket_path,aws_role_arn):
    cur = trgt_db_conn.cursor()

    cur.execute("TRUNCATE "+table)
    cur.execute("COMMIT;")
    cmd_copy_to_trgt = "copy "+ table +" from '"+ s3_bucket_path +"'"+" iam_role '"+aws_role_arn+"'"+" format as avro 'auto' ACCEPTANYDATE DATEFORMAT 'YYYY-MM-DD' TIMEFORMAT 'epochmillisecs';"
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

def _process(params,table):
    table_name = table['name']

    s3_bucket_path = params['target_s3_path'] + "/" + table_name + "/"
    src_db_url = "jdbc:vertica://" + params['host'] + "/" + params['db_name']
    password = params['password']
    if not password:
        password = ssm_pass()

    connection = create_db_connection(params['host'] , params['db_name'], params['username'],password,params['password'])

    try:
       store(connection,table_name,s3_bucket_path,params['role_arn'])
    except:
       print("ERROR PROCESSING TABLE : "+table_name)

def store_data(params):
    for table in params['tables']:
        _process(params, table)


if __name__ == '__main__':
    params = read_params()
    store_data(params)
