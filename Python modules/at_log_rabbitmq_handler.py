'''
Created on 28 Jun 2016

@author: conicova
'''
import logging

from async_publisher import RabbitMQPublisher, FAHeart
from at_log_message import LogMessage, LogRecord, SessionInfo, LogException, TaskArgs
from at_mq_config import FAMQConfig

LOGGER = logging.getLogger(__name__)

""" make the publisher singleton 
There seem to be issues on the ATS level (segmentation fault), when creating and closing multiple threads.
As a solution we could try and create only one publisher (for each type sync/async), and close it only when ALL FA work is done.
For this we will remember which handler has created the publisher, and when it closes, we will stop the 
publisher.
""" 

class LoggingMQConfig(FAMQConfig):
    
    def __init__(self):
        super(LoggingMQConfig, self).__init__()
        
        self.connection_string = ""
        self.host = "http://jhbdwmvdi000210:8080/"
        
# load this here so that it fails, if the Handler not defined
# for the current environment
    
RABBIT_MQ_PUBLISHERS = {}

class RabbitMQHandler(logging.Handler):
    
    def __init__(self, process_name, level=logging.NOTSET, run_name=None, timeout=None, is_async=True, ael_main_args=None):
        self.is_publisher_parent = False
        self.is_async = is_async
        self.msg_id = 0
        
        self._init_publisher()

        self._publisher = RABBIT_MQ_PUBLISHERS[is_async]
        self._publisher.timeout = timeout
        self.process_name = process_name
        if not run_name:
            self.process_run_name = LogMessage.generate_run_name(process_name)
        else:
            self.process_run_name = run_name
        self._session_info = SessionInfo.get_current(self.process_run_name)
        self._task_args = TaskArgs(ael_main_args)
        self._heart = FAHeart(self.process_name, self.process_run_name)
        self._publisher.publisher.register_heart(self._heart)
        logging.Handler.__init__(self, level)
        
        if not self._publisher.was_started:
            # !!! this has to be the last call
            self._publisher.start()
    
    def _init_publisher(self):
        """
        Create the publisher if it does not exist
        If it exists check if it is not stopping.
        """
        if self.is_async in RABBIT_MQ_PUBLISHERS and not RABBIT_MQ_PUBLISHERS[self.is_async].stopping:
            return
        if self.is_async in RABBIT_MQ_PUBLISHERSand RABBIT_MQ_PUBLISHERS[self.is_async].stopping:
            RABBIT_MQ_PUBLISHERS.pop(self.is_async)
        self.is_publisher_parent = True
        if self.is_async not in RABBIT_MQ_PUBLISHERS:
            
            mq_config = LoggingMQConfig()
            mq_config.load_fa_config()
            # Hack, need to update the configuration file
            mq_config.queue = mq_config.queue_dashboard
            
            rabbit_mq_publisher = RabbitMQPublisher(mq_config, self.is_async)
            RABBIT_MQ_PUBLISHERS[self.is_async] = rabbit_mq_publisher
            return
    
    def emit(self, record):
        self.msg_id += 1
        log_msg = LogMessage(self.process_name, self.process_run_name,
                             LogRecord.from_logging(record, self.msg_id, self),
                             self._session_info,
                             LogException.from_logging(record),
                             self._task_args)
        try:
            self._publisher.publish(log_msg)
        except Exception as ex:
            LOGGER.error("Could not publish the msg: %s", ex)
       
    def close(self):
        try:
            self._heart.is_alive = False
            self._publisher.publisher.unregister_heart(self._heart)
            # stop the publisher, only in the handler where it was created
            if self.is_publisher_parent and self.is_async in RABBIT_MQ_PUBLISHERS:
                RABBIT_MQ_PUBLISHERS.pop(self.is_async)
                self._publisher.stop()
            logging.Handler.close(self)
        except Exception:
            LOGGER.exception("Something went wrong while closing the logging handler.")
