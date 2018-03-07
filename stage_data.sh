#!/usr/bin/env bash
#export MACHINE_ENV=STAGE
export MACHINE_ENV=DEV
#export MACHINE_ENV=PROD
source env/bin/activate
python stage_data.py --dop 1 --tables s3://ash.data/vertica/scripts/SmallTables.json --config s3://ash.data/khirul/config.json
#python stage_data.py --dop 1 --tables s3://ash.data/khirul/SmallTables.json
# ec2-52-90-229-247.compute-1.amazonaws.com
# jdbc:vertica://172.31.29.108/sabredb
