#!/usr/bin/env bash
export MACHINE_ENV=STAGE
#export MACHINE_ENV=DEV
#export MACHINE_ENV=PROD
source env/bin/activate
#python store.py --tables s3://ash.data/vertica/metadata/SmallTables.json --config s3://ash.data/khirul/config.json
python store.py --tables s3://ash.data/khirul/tables-3.json --config s3://ash.data/khirul/config.json
