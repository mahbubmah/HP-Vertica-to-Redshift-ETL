source env/bin/activate && python store.py --aws_role_arn "arn:aws:iam::324827999179:role/myRedshiftRole"   --tables "s3://ash.data/khirul/sqoop-script-2/tables.txt"   --target_s3_path "s3://ash.data/vertica/02-13"   --trgt_db_host "rsdata.c5y5lcyfmqhg.us-east-1.redshift.amazonaws.com"   --trgt_db_name "qsdata"   --trgt_username "admin"   --trgt_password "Vfr45tgb"   --trgt_port "5439" --degree_of_parallelism 1