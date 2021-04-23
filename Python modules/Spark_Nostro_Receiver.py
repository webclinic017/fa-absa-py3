'''-----------------------------------------------------------------------------
PROJECT                 :  Spark Non ZAR Cashflow Feed
PURPOSE                 :  Receive responses from TAP for the non zar settlements to MidasPlus
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Nick Bance
DEVELOPER               :  Anwar Banoo
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer               Description
--------------------------------------------------------------------------------
2011-10-25   XXXXXX                                Initial Implementation
2015-09-04                 Bhavik Mistry           Emailing of failures as they occur
2016-04-05  CHNG0003546459 Paseka Motsoeneng       Directing log emails as per source environment. 
2018-07-19  CHG1000679237  Libor Svoboda           Fix the Front - Sparks
'''
import sys
import time
import acm
from collections import OrderedDict
from datetime import datetime
from xml.etree.ElementTree import SubElement, tostring, ElementTree, fromstring
import xml.etree.ElementTree as etree
from Spark_Nostro_MQWrapper import MqMessenger  
from Sparks_Config import SparksConfig
import Spark_Nostro_HTML_Exception_Rep as exRep
from at_logging import getLogger

# Dashboard Settings/imports ---------------------------------------------------------
mongo_egg_path = 'c:\\Python27\\lib\\site-packages\\pymongo-3.3.0-py2.7-win-amd64.egg'
xml_egg_path = 'c:\\Python27\\lib\\site-packages\\xmltodict-0.10.2-py2.7.egg'
sys.path.append(mongo_egg_path)
sys.path.append(xml_egg_path)
import pymongo
import xmltodict


config = None
mqMessenger = None
posts = None
LOGGER = getLogger(__name__)

    
def __processMessage(message):
    LOGGER.info('Process the following message\n%s' % message)
    
    if len(message) > 10:
        
        try:
            tree = ElementTree(fromstring(message))
            element = tree.find('FrontArenaSettlementId')
            LOGGER.info('Check if incoming message has FrontArenaSettlementId')
            if element is not None and element.text is not None:
                object_id = element.text
                LOGGER.info('Incoming message has FrontArenaSettlementId=%s' % object_id)
                
                id_filter = {'_id': object_id}
                diary = posts.find_one(id_filter)
                element = tree.find('Result')
                
                if (diary) and (element is not None):
                    LOGGER.info('Prepare to update status to %s' % element.text)
                    
                    del diary['_id']
                    timestamp    = datetime.fromtimestamp(float(diary['Timestamp'])).strftime('%d-%m-%Y %H:%M:%S')
                    del diary['Timestamp']
                    
                    root = ElementTree(fromstring(xmltodict.unparse(diary, full_document=False)))
                    tracking = root.find('Tracking')
                    payday = root.find('Financials/PayDate').text
                    curr = root.find('Financials/CurrencyName').text
                    amount = root.find('Financials/Amount').text
                    trade_num = root.find('Identifiers/TradeNumber').text
                    acquirer = root.find('Acquirer/AcquirerName').text
                    portfolio = root.find('Acquirer/AcquirerPortfolio').text
                    cust_num = root.find('Acquirer/AcquirerMidasCustomerNbr').text
                    counterparty = root.find('Counterparty/CounterpartyName').text
                    instype = root.find('Identifiers/InstrumentType')
                    midas_ref = tree.find('MidasPaymentReference')
                    default_nostro = tree.find('DefaultNostroAccount')
                    tracking.set('Status', element.text)
                    
                    identifiers = root.find("Identifiers")
                    original_default_nostro = identifiers.find("DefaultNostro")                    
                    
                    if original_default_nostro == None:
                        LOGGER.info('Creating new "DefaultNostro" element with value %s'%default_nostro.text)
                        default_nostro_element = etree.Element("DefaultNostro")
                        identifiers.append(default_nostro_element)
                        default_nostro_element.text = default_nostro.text
                    else:
                        LOGGER.info('Setting existing "DefaultNostro" element with value %s'%default_nostro.text)
                        original_default_nostro.text = default_nostro.text
                    
                    if midas_ref.text is not None:
                        tracking.set('MidasPaymentReference', midas_ref.text)
                        
                    result = element.text
                    error = None
                    if result == 'Failure':
                        element = tree.find('MidasResponse/Errors')
                        for node in element: 
                            error = node.text
                            SubElement(tracking, "Error").text = node.text
                            LOGGER.info('Node contents: %s' % node.text)
                            
                    LOGGER.info(tostring(root.getroot()))
                    
                    id_filter = {'_id': object_id}
                    posts.delete_one(id_filter)
                    
                    document = xmltodict.parse(tostring(root.getroot()))
                    document['_id'] = object_id
                    document['Timestamp'] = time.time()

                    try:
                        posts.insert_one(document)
                    except pymongo.errors.DuplicateKeyError:
                        LOGGER.error('Receiver: Cannot insert document: %s.' % object_id)
                    else:
                        LOGGER.info('Receiver: Moneyflow object %s commited to MongoDb.' % object_id)

                    if result in config.status_to_report:
                        if config.intraday_reporting_active.lower() == 'yes':
                            classifier = {}
                            classifier_backdates = {}
                            
                            if payday >= acm.Time.DateToday():
                                classifier[result] = []
                                classifier[result].append([trade_num,
                                       result,   
                                       acquirer,     
                                       portfolio,    
                                       counterparty, 
                                       cust_num,     
                                       curr,         
                                       amount,       
                                       instype,
                                       payday,      
                                       midas_ref,    
                                       timestamp,
                                       error])
                            else:
                                classifier_backdates[result] = []
                                classifier_backdates[result].append([trade_num,
                                       result,   
                                       acquirer,     
                                       portfolio,    
                                       counterparty, 
                                       cust_num,     
                                       curr,         
                                       amount,       
                                       instype,
                                       payday,      
                                       midas_ref,    
                                       timestamp,
                                       error])
                                   
                            body = exRep.__reportOutput(classifier, classifier_backdates)
                            exRep.email_report(body, 'Sparks Intraday Report - %s' %config.environment, config.email_group2, 'Sparks Feed', None)
                            
                    LOGGER.info('Message processed successfully')
                else:
                    LOGGER.info('Diary identifier not recognized:%s' % object_id) 
            else:
                LOGGER.info('Response message improperly formatted - FrontArenaSettlementId node')

        except Exception as exc:
            LOGGER.exception('Error while processing message: %s' % str(exc))

    
def work():
    if mqMessenger:
        message = mqMessenger.ReadMessage()
        if message:
            __processMessage(message)
            mqMessenger.AcceptMessage()
    
def start():
    global config, mqMessenger, posts
    
    LOGGER.info('ATS attempting startup...')
    config = SparksConfig('Receive')
    mqMessenger = MqMessenger(config)   

    client = pymongo.MongoClient(config.mongo_db_repl_set_conn_str)
    db = client.spark_db
    posts = db.posts
    

def stop():   
    mqMessenger.DisconnectQueueManager()

def status():
    pass
