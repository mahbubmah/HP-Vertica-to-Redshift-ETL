source env/bin/activate && \
python stage_data.py --host "ec2-52-90-229-247.compute-1.amazonaws.com" \
-U "dbadmin" -P "vfr45tgb" -d "sabredb" -t "DimMktSource" -T "s3://ash.data/vertica/02-13" \
--src_driver "com.vertica.jdbc.Driver" \
--src_db_url "jdbc:vertica://ec2-52-90-229-247.compute-1.amazonaws.com/sabredb"

# ec2-52-90-229-247.compute-1.amazonaws.com
# jdbc:vertica://172.31.29.108/sabredb