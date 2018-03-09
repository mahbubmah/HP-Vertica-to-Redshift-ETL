SYNTAX:  
  python sync.py \
  --aws_account_id "AWS ACCOUNT ID" \
  --role_name "AWS ROLE NAME" \
  --src_driver "SRC DATABASE DRIVER" \
  --src_db_url "SRC DATABASE URL" \
  --src_username "SRC DATABASE USER NAME" \
  --src_password "SRC DATABASE USER PASSWORD PASSWORD" \
  --tables "[TABLE_NAME_1,TABLE_NAME_1]/S3 PATH" \
  --target_s3_path "S3 PATH FOR STAGED DATA" \
  --trgt_db_host "TARGET DB HOST" \
  --trgt_db_name "TARGET DB NAME" \
  --trgt_username "TARGET DATABASE USER NAME" \
  --trgt_password "TARGET DATABASE USER PASSWORD PASSWORD" \
  --trgt_port "TARGET DB PORT"\
  [--degree_of_parallelism "Number of tables to process in parallel"
  [--number_of_mappers "[Number of mappers for sqoop]"]
