import logging
import Configuration
from os import path
from distutils.log import INFO


logging.config.fileConfig( path.join([ Configuration.CONFIGPATH,'logging.conf']) )

def get_logger(name,loglevel=None):
    
    logger = None
    try:
        logger=logging.getLogger(name)
    except:
        print('{} is not a predefined loglevel. Using root instead.')
        logger=logging.getLogger('root')
        
    if loglevel:
        logger.setLevel( logging.__dict__[loglevel] )
        
    return logger
