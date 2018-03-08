
ETL job sync data between vertica and redshift database. It load data from vertica database and stage data into a s3. Then copy the data from s3 to redshift database. It supports both full load or delta load. Sqoop is used to read data from vertica and store data from vertica database to s3. Redshift copy command is used to copy data from s3 to redshift. Two database (vertica and redshift) must have the same table structure.

There are three steps. Sage data , store data and finalize. Stage data process store the data from source database(vertica) to target database(redshift). Basic usage :
  

    Step-1:
    
    python stage_data.py --tables "s3 path for table.json file" \
    
    --config "s3 path for config.json"\
    
    \[--dop 1\]
    
    In this step data will be stored from source database to s3.
    
    Step- 2:
    
    python store.py --tables "s3 path for table.json file" \
    
    --config "s3 path for config.json"\
    
    \[--dop 1\]
    
    In this step data will be copied from s3 to target database.
    
    Step- 3:
    
    python finalizer.py
    
      
    
    This step will store the generated log files to s3.

  
  

**Parameter description :**

 1. table: S3 path to table.json will be specified here. (required)
 2. config: s3 path to config.json will be specified here. (required)
 3.  dop: dop stands for degree of parallelism. It denotes the total number of tables we want to process in parallel. Config.json (described later) also contain this parameter. If we specify this parameter at command line, it will override the json configuration.
 
Examples are config.json and table.json description are given below.

**Config.json:**
config .json file contains required aws configuration , source database configuration and target database configuration. File format as follow.

    {
    
    "aws": {
    
    "role_arn": "aws role arn",
    
    "s3_path": "target s3 path to store stage data",
    
    "dop": "number of tables to process in parallel"
    
    },
    
    "source_db": {
    
    "password": "source database password",
    
    "ssm_name": "vertica-pw",
    
    "driver": "source database driver class",
    
    "host": "source database host",
    
    "port": "source database port",
    
    "db_name": "source database name",
    
    "username": "source database user name"
    
    },
    
    "target_db": {
    
    "password": "target database password",
    
    "ssm_name": "vertica-pw",
    
    "driver": "target database driver class",
    
    "host": "target database host",
    
    "port": "target database port",
    
    "db_name": "target database database name",
    
    "username": "target database username"
    
    }
    
    }

  
*Note : Here all the parameters are required. Except ssm_name and password . If password is specified then the script will use the password. Otherwise ssm_name. One of the parameters must be specified.*

**Table.json:**
Table.json file is and array containing the tables description. File format as follow.

    [{
    
    "schema": "table schema name",
    
    "name": "table name",
    
    "split_column": "split column name for sqoop job",
    
    "mappers": "number of mappers for for sqoop job",
    
    "filter_column": "filter column name for delta load",
    
    "upper_value": "upper value of filter column for delta load",
    
    "lower_value:" lower value of filter column for delta load "
    
    "unique_column": ["array of unique columns"]
    
    },
    
    {
    
    "schema": "table schema name",
    
    "name": "table name"
    
    }]

  

*Note: Split\_column , mappers , filter\_column , upper\_value, lower\_value are optional column*


