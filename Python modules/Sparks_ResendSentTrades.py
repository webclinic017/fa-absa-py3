import sys
import acm, ael
from xml.etree.ElementTree import SubElement, tostring, ElementTree, fromstring
import Sparks_Util
from at_logging import getLogger

LOGGER = getLogger(__name__)

mongo_egg_path = 'c:\\Python27\\lib\\site-packages\\pymongo-3.3.0-py2.7-win-amd64.egg'
xml_egg_path = 'c:\\Python27\\lib\\site-packages\\xmltodict-0.10.2-py2.7.egg'
sys.path.append(mongo_egg_path)
sys.path.append(xml_egg_path)

from pymongo import MongoClient
from collections import OrderedDict
import xmltodict
from at_ael_variables import AelVariableHandler
from datetime import datetime

client = MongoClient(document_class=OrderedDict)
db = client.spark_db
posts = db.posts

required_send_status = 'Sent'

ael_variables = AelVariableHandler()

trades_to_exclude = ''

def ael_main(variables):

    with open('c:/temp/excluded_trades.txt', 'r') as myfile:
        trades_to_exclude = myfile.read()
    
    LOGGER.info('Excluded trades:%s'%trades_to_exclude)
    
    for post in posts.find({}):
    
        LOGGER.info('------------------------------------------------------')
        
        message_timestamp = datetime.fromtimestamp(post["Timestamp"])
        message_date = datetime.strftime(message_timestamp, '%Y-%m-%d')
        
        message_id = post["CashflowMessage"]["Identifiers"]["SettlementId"]
        message_trade_number = post["CashflowMessage"]["Identifiers"]["TradeNumber"]
        message_send_status = post["CashflowMessage"]["Tracking"]["@Status"]
        message_pay_date =  post["CashflowMessage"]["Financials"]["PayDate"]
        
        LOGGER.info('Processing message_id:%s'%message_id)
        LOGGER.info('processing message of trade_number:%s'%message_trade_number)
        LOGGER.info('Message date:%s'%message_date)
        LOGGER.info('send_status == required_send_status:%s'%(message_send_status == required_send_status))

        count = 1
    
        while count < 6:
            
            date_offset = count * -1
            rundate = ael.date_today().add_banking_day(ael.Instrument["ZAR"], date_offset).to_string("%Y-%m-%d")
            LOGGER.info('\t\tRunning for date:%s'%rundate)
            
            count += 1
            
            LOGGER.info('message_date == rundate:%s'%(message_date == rundate))
            # and message_date == rundate
            if message_send_status == required_send_status:
                
                sparks_util = Sparks_Util.SparksUtil(rundate)
                sparks_util.connect_queue_manager()
                try:
                    currency_changed = None
                    LOGGER.info('\t\tDeleting money flow:%s and resending moneyflows for trade.'%message_id)
                    message_id = {'_id': message_id}
                    
                    if message_trade_number not in trades_to_exclude:
                        posts.delete_one(message_id)
                        LOGGER.exception('message_trade_number: %s' % str(message_trade_number))
                        LOGGER.exception('message_trade_number: %s' % type(message_trade_number))
                        sparks_util.process_trades([acm.FTrade[str(message_trade_number)]])
                    else:
                            LOGGER.info('Excluding trade:%s'%message_trade_number)
                        
                except Exception as exc:
                    LOGGER.exception('Task failed: %s' % str(exc))
                    raise
                else:
                    LOGGER.info('\t\tCompleted successfully')
                finally:
                    sparks_util.disconnect_queue_manager()
                    LOGGER.info('Done')
