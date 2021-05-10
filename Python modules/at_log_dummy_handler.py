'''
Created on 2 Aug 2016

@author: conicova
'''
import logging
from at_log_message import LogMessage

class DummyHandler(logging.Handler):
    
    def __init__(self, process_name, level=logging.NOTSET, run_name=None, timeout=None, is_async=True):
        logging.Handler.__init__(self, level)
        self.msg_id = 0
        self.process_name = process_name
        if not run_name:
            self.process_run_name = LogMessage.generate_run_name(process_name)
        else:
            self.process_run_name = run_name
        self._session_info = ''
        
    def emit(self, record):
        self.msg_id += 1
       
    def close(self):
        try:
            logging.Handler.close(self)
        except Exception:
            logging.exception("Something went wrong while closing the logging handler.")