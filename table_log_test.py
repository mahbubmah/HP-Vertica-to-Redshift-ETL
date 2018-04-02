import time
from logger import *



if __name__ == '__main__':

    tables = ["one", "two"]

    for table in tables:
        logger=jobLogger(table)
        date_prefix = time.strftime('dt=%Y-%m-%d-%H-%M-%S')
        logger.info(date_prefix +"\n\n")