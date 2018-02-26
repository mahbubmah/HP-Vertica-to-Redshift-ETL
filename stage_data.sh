source env/bin/activate && \
python stage_data.py -h "ec2-52-90-229-247.compute-1.amazonaws.com" \
-u "dbadmin" -p "vfr45tgb" -t "DimMktSource" -T "s3://ash.data/vertica/02-13"\
--src_driver "com.vertica.jdbc.Driver"\
--src_db_url "jdbc:vertica://ec2-52-90-229-247.compute-1.amazonaws.com/sabredb"

# ec2-52-90-229-247.compute-1.amazonaws.com
# jdbc:vertica://172.31.29.108/sabredb