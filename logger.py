import logging
import logging.config
import os
import time

def jobLogger(name):
	log_file_name=	'log'+os.sep;
	if not os.path.exists(log_file_name):
		os.makedirs(log_file_name)

	# log_file_name+=time.strftime("%Y%m%d")+os.sep
	if not os.path.exists(log_file_name):
		os.makedirs(log_file_name)

	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)-12s - %(levelname)-8s: %(message)s',
                    filename=log_file_name+name+'.log',
                    filemode='a+')
	console = logging.StreamHandler()
	console.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s: %(message)s')
	console.setFormatter(formatter)
	logger=logging.getLogger(name)
	logger.addHandler(console)
	return logger