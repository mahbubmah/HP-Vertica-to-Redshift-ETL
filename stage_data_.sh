source env/bin/activate && \
python stage_data.py --host "10.0.2.114" \
-U "dbadmin" -P "vfr45tgb" -d "uav01d1" -t "SHSCRSWHGSummary.DimMktSource" -T "s3://ash.data/vertica/02-13" \
--src_driver "com.vertica.jdbc.Driver"