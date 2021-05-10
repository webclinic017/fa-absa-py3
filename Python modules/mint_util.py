'''
Created on 19 May 2017

@author: conicova
'''

import logging
from at_logging_handlers import FileHandlerMINT

def close_mint_file_handlers():
    ''' Close all the existing FileHandlerMINT instances
    '''
    FileHandlerMINT.close_all()

def init_logger(log_path="", log_tag="", msg_tag="fa_mint", close_existing=True):
    ''' This will create a new logging handler of type FileHandlerMINT that will output all the
    logging messages to a file.
    By default all other FileHandlerMINT instances will be closed.
    '''
    try:
        # This will create the handler that will output to the console
        logging.basicConfig()
        
        if close_existing:
            close_mint_file_handlers()
        
        _LOGGER_HANDLER = FileHandlerMINT.get_instance(log_path, log_tag, msg_tag)

        logging.root.addHandler(_LOGGER_HANDLER)
        logging.root.setLevel(logging.NOTSET)
        logging.root.info("MINT logger initialised")
    except Exception:
        logging.root.exception("Something went wrong.")