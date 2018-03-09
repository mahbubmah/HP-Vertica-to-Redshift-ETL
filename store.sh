#!/usr/bin/env bash
#export MACHINE_ENV=STAGE
export MACHINE_ENV=DEV
#export MACHINE_ENV=PROD
source env/bin/activate
#python store.py --tables s3://ash.data/vertica/scripts/LargeTables.json --config s3://ash.data/vertica/scripts/config.json 
#python store.py --tables s3://ash.data/vertica/scripts/LargeTables.json --config s3://ash.data/vertica/scripts/config.json 
python store.py --tables s3://ash.data/vertica/scripts/SmallTables-4.json --config s3://ash.data/vertica/scripts/config.json 
