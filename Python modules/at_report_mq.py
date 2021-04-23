'''
Created on 8 Dec 2016

@author: conicova
'''
from itertools import izip_longest
import json
from at_logging import getLogger

from async_publisher import MQMessage, RabbitMQPublisher
from at_mq_config import FAMQConfig, REPORTS_LOCATIONS

LOGGER = getLogger(__name__)

class FAReportPublisherMQConfig(FAMQConfig):
    
    def __init__(self):
        super(FAReportPublisherMQConfig, self).__init__()
        

class FAReportRow(object):
    
    def __init__(self, row_nr, columns, values):
        values = map(lambda i: str(i), values)
        items = izip_longest(columns, values)
        self.data = dict(items)
        self.row_nr = row_nr

class FAReportInfo(object):
    
    def __init__(self, full_path):
        self.full_path = full_path

class FAReportMessage(MQMessage):
    
    def __init__(self, report_id, report_row, report_info):
        super(FAReportMessage, self).__init__()
        self.report_id = report_id
        self.report_row = report_row
        self.report_info = report_info
        
    def to_json(self):
        try:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
        except:
            print(self)
            print(self.data)
            raise
    
class FAReportMQ(object):
    
    def __init__(self, report_id, full_path):
        self.report_id = report_id
        self.full_path = full_path

        self._rabbit_mq_publisher = None
        try:
            mq_config = FAReportPublisherMQConfig()
            mq_config.load_fa_config(REPORTS_LOCATIONS)
        
            self._rabbit_mq_publisher = RabbitMQPublisher(mq_config, True)
        except FAMQConfigException as ex:
            LOGGER.warning("MQ Configuration failed to load. %s", ex)
        except:
            LOGGER.exception("Failed to start FAReportMQ")
    
    def __enter__(self):
        if self._rabbit_mq_publisher:
            self._rabbit_mq_publisher.start()
        
        return self
    
    def __exit__(self, type, value, traceback):
        if self._rabbit_mq_publisher:
            self._rabbit_mq_publisher.stop()
        
    def save_row(self, row_nr, header, line):
        if self._rabbit_mq_publisher:
            msg = FAReportMessage(self.report_id,
                                  FAReportRow(row_nr, header, line),
                                  FAReportInfo(self.full_path))
            self._rabbit_mq_publisher.publish(msg)
        LOGGER.debug(msg.to_json())

        
