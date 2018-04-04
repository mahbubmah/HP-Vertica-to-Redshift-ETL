import time
import logging
import logging.config
import os

def jobLogger(name):
    log_file_name=  'log'+os.sep;
    if not os.path.exists(log_file_name):
        os.makedirs(log_file_name)

    tmp_file =open("tmp.txt","r")
    date_prefix = tmp_file.read()
    # log_file_name+=time.strftime("dt=%Y-%m-%d-%H-%M")+os.sep
    log_file_name+=time.strftime(date_prefix)+os.sep
    if not os.path.exists(log_file_name):
        os.makedirs(log_file_name)
    

    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s: %(message)s')
    fileHandler = logging.FileHandler(log_file_name+name+'.log', mode='a+')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)


def logger(msg, level, logfile):   
    log = logging.getLogger(logfile)
    if level == 'info'    : log.info(msg) 
    if level == 'warning' : log.warning(msg)
    if level == 'error'   : log.error(msg)
    if level == 'debug'   : log.debug(msg)
    if level == 'exception'   : log.exception(msg)
