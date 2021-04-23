'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_REQUEST_CONTROL
PROJECT                 :       Pegasus - Data Distribution Model (DDM)
PURPOSE                 :       This module handles external DDM requests and routes request to the DDM Trade Workers
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
import sys
import acm
import amb
import time
import collections
import FLogger
from datetime import datetime, date
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params
import AMB_Reader_Writer as ambReaderWriter
import DDM_REQUEST_MESSAGE as requestMessage
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils
import DDM_SQL_HELPER as sqlHelper

#Static globals
logger = FLogger.FLogger('DDM_REQUEST_CONTROL', params.logLevel) 
ambWriter = None
ambReader = None
readerSubjects = None
readerMBName = None
messageQueue = collections.deque()
lastRequestWorkerIndex = 0
lastTradeEventListenerIndex = 0

#*******************************************************************************************************************************
# Event callback function for writing AMB messages. The events are placed in a queue that is then processed InvokeWork function. 
#*******************************************************************************************************************************
def event_cb_writer(channel, event, arg):
    global ambWriter    
    global logger
    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Disconnect':
        raise Exception('The AMB writer received a disconnect event')

#*******************************************************************************************************************************
# Event callback function for writing AMB messages. The events are placed in a queue that is then processed InvokeWork function. 
#*******************************************************************************************************************************
def event_cb_reader(channel, event, arg):
    global messageQueue
    global ambReader
    global logger
    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Disconnect':
        raise Exception('The AMB reader received a disconnect event')
    elif eventString == 'Message':
        messageQueue.append((amb.mb_copy_message(event.message), channel))
        
#*******************************************************************************************************************************
# Create the AMB reader for receiving messages from the external request services
#*******************************************************************************************************************************
def createAMBReader():
    global ambReader
    global readerSubjects
    global readerMBName
    global logger
    try:
        #Create the AMB reader
        ambReader = ambReaderWriter.AMB_Reader(params.ambAddress, readerMBName, event_cb_reader, readerSubjects)
    
        #Open the reader to start receiving messages
        if not ambReader.open_AMB_Receiver_Connection():
            raise Exception('Could not open the AMB reader')
                
    except Exception, error:
        raise Exception('Could not create the AMB reader. %s' % str(error))
        
#*******************************************************************************************************************************
# Create the AMB writer for writing batch report messages to the external trade event listener
#*******************************************************************************************************************************
def createAMBWriter():
    global ambWriter
    global logger
    try:
        #Create the AMB writer (create without subjects)
        ambWriter = helper.AMB_WriterExtension(params.ambAddress, params.writerMBName, event_cb_writer, 'DDM_ATS_WORKER', 'NoSubject')
        
        #Open writer
        if not ambWriter.open_AMB_Sender_Connection():
            raise Exception('Could not open the AMB writer')
        
    except Exception, error:
        raise Exception('Could not create the AMB writer. %s' % str(error))
        
#*******************************************************************************************************************************
# DDM_REQUEST_CONTROL class
#*******************************************************************************************************************************
class DDM_REQUEST_CONTROL():
    #Class locals
    atsName = None
    
    #Class Constructor
    def __init__(self, pATSName, pReaderMBName, pReaderSubjects):
        print 'init'
        global readerSubjects
        global readerMBName
        #Set local class variables
        self.atsName = pATSName
        readerSubjects = pReaderSubjects
        readerMBName = pReaderMBName
        
                
    #Start the ATS    
    def start(self):
        global readerSubjects
        global readerMBName
        try:
            logger.info('****************************************************************************')
            logger.info('ATS started at %s' % str(time.ctime()))
            logger.info('****************************************************************************')
            logger.info(' ATS Name              : %s' % str(self.atsName))
            logger.info(' Platform              : %s' % str(helper.platformName))
            logger.info(' Process Id            : %s' % str(helper.processId))
            logger.info(' Memory Threshold      : %s KB' % str(params.memoryThreshold))
            logger.info(' Request Workers       : %s' % str(params.requestWorkerInstances))
            logger.info('****************************************************************************')
            logger.info('* Setting up AMB connections... ')
            logger.info('****************************************************************************')
            logger.info(' AMB Host            :                 %s' % str(params.ambAddress))
            logger.info(' AMB Reader          :                 %s' % str(readerMBName))
            logger.info(' AMB Reader subjects :                 %s' % str(readerSubjects))
            logger.info('****************************************************************************')
            
            #Create the AMB reader and writer
            createAMBWriter()
            logger.info('AMB writer ready!')
            createAMBReader()
            logger.info('AMB reader ready!')
            
            #Ready!
            logger.info('*** ATS ready for action ***')
            logger.info('************************************************************************************')
            logger.info('')
            
            #Poll for messages that might already be waiting for which an read event was not raised
            amb.mb_poll()
            
        except Exception, error:
            raise Exception('ATS startup failed. %s' % str(error))
            
    #ATS Work command - called by the ATS work
    def work(self):
        global messageQueue
        global ambWriter 
        
        
        #If no available for processing, return
        if len(messageQueue) == 0:
            return
        
        try:
            #pop the first message off the queue (left)
            messageQueueItem = messageQueue.popleft()
            (message, channel) = messageQueueItem
            logger.info('Message event received. (messageId:%i)' % int(message.id))
            
            #Process the message
            self.processMessage(message)
            
            #Try accept the message off the AMB
            acceptResult = amb.mb_queue_accept(channel, message, str(message.id))
            if acceptResult:
                raise Exception('Could not accept message %s. %s' % (str(message.id), str(error)))
            logger.info('Message accepted (messageId:%i)' % int(message.id))
            logger.info('%s messages remaining in the queue' % str(len(messageQueue)))
            logger.info('     ')
            
        except Exception, error:
            #write the error to the error log
            logger.error('A fatal error was encountered. %s. shutting down the ATS...', str(error))
            
            #log the error to the database
            try:
                logger.info('logging the error to the database...')
                sqlHelper.callStoredProc('DDMInsertErrorLog', self.atsName, 0, 'SubmitRequestBatches', str(error))
                sqlHelper.commit()
            except Exception, sqlError:
                logger.error('Could not log the error to the database. %s', str(sqlError))
            
            #Exit the process
            raise SystemExit('cannot continue')
            
    #Reads the message content as a string
    def processMessage(self, message):
        global lastRequestWorkerIndex 
        #Process the message
        try:
            logger.LOG('')
            logger.info('************************************************************************************')
            logger.info('Processing message (messageId:%i)...' % int(message.id))
            
            #Read the message content
            buffer = amb.mbf_create_buffer_from_data(message.data_p)
            messageData = buffer.mbf_read()
            #Create a request message from the amb message
            requestMsg = requestMessage.DDM_REQUEST_MESSAGE(messageData)
            if not requestMsg:
                raise Exception('Could not construct the request message')
            
            #Log the message detail
            logger.info(' ')
            logger.info('Message details:')
            logger.info(' Request Id:                 %s' % str(requestMsg.requestId))
            logger.info(' Request Date Time:          %s' % str(requestMsg.requestDateTime))
            logger.info(' Report Date:                %s' % str(requestMsg.reportDate))
            logger.info(' Request Source:             %s' % str(requestMsg.requestSource))
            logger.info(' Batch Number:               %s' % str(requestMsg.batchNumber))
            logger.info(' Batch Name:                 %s' % str(requestMsg.batchName))
            logger.info(' Request Event Type:         %s' % str(requestMsg.requestEventType))
            logger.info(' Request Type:               %s' % str(requestMsg.requestType))
            logger.info(' Scope Number:               %s' % str(requestMsg.scopeNumber))
            logger.info(' Scope Name:                 %s' % str(requestMsg.scopeName))
            
            #Fetch the trades for the request
            logger.info('  loading trades...')
            trades = acm.FSortedCollection()
            if requestMsg.requestType=='PORTFOLIO_TRADES':
                trades = helper.getPortfolioTrades(requestMsg.scopeNumber, requestMsg.scopeName)
            elif requestMsg.requestType=='INSTRUMENT_TRADES':
                trades = helper.getInstrumentTrades(requestMsg.scopeNumber, requestMsg.scopeName)
            elif requestMsg.requestType=='SINGLE_TRADE':
                trade = acm.FTrade[requestMsg.scopeNumber]
                if trade:
                    trades.Add(trade)
            else:
                raise Exception("Request type '%s' not supported" % str(requestMsg.requestType))
            
            #Fetch the trade count
            tradeCount=0
            if trades:
                tradeCount = len(trades)
            logger.info('  %i trades found', (int(tradeCount)))
           
            #Create the request tracker
            self.createRequestTracker(requestMsg.requestId, tradeCount)
            #Send the subscription event
            self.sendSubscriptionEvent('RequestStart', requestMsg.requestId)
            
            #Fetch the index batches for the trade count
            batches = helper.getTradeIndexBatches(tradeCount)
            logger.info('  %i batch(s) created (maxBatchSize:%i)' % (len(batches), params.batchTradeSize))
            batchCounter = 0
            for batch in batches:
                
                #add the batch information to the original message
                batchCounter = batchCounter + 1
                startIndex, endIndex = batch
                batchTradeCount=0
                if tradeCount>0:
                    batchTradeCount=(endIndex - startIndex) + 1
                
                #Remove any existing request batch tags
                requestBatchTag = ambaUtils.object_by_name(messageData, [''], 'REQUEST_BATCH')
                if requestBatchTag:
                    requestBatchTag.mbf_remove_object()
                #Find the datatag to add after
                dataTag = ambaUtils.object_by_name(messageData, [''], 'DATA')
                #Start a new request batch tag
                requestBatchList = messageData.mbf_start_list('REQUEST_BATCH')
                requestBatchList.mbf_add_string('REQUEST_BATCH_COUNT', str(len(batches)))
                requestBatchList.mbf_add_string('REQUEST_BATCH_NO', str(batchCounter))
                requestBatchList.mbf_add_string('REQUEST_BATCH_START_INDEX', str(startIndex))
                requestBatchList.mbf_add_string('REQUEST_BATCH_END_INDEX', str(endIndex))
                requestBatchList.mbf_add_string('REQUEST_BATCH_TRADE_COUNT', str(batchTradeCount))
                requestBatchList.mbf_end_list()
                #Fetch a string representation of the message
                messageString = messageData.mbf_object_to_string() 
                #print messageString
            
                #Send the request batch to a request worker for further processing 
                if not ambWriter:
                    raise Exception('AMB writer not initialised')
                
                #Define the subject on which to send the message
                requestWorkerReaderSubject = '%s%i' %(params.requestWorkerReaderSubjectTemplate, int(self.getRequestWorkerIndex()))    
                logger.info("  sending batch %i of %i (startIndex:%i, endIndex:%i, tradeCount:%i) to AMB with worker subject '%s'"\
                            %(batchCounter, len(batches), startIndex, endIndex, batchTradeCount, requestWorkerReaderSubject))
                ambWriter.post_Message_To_AMB_Raw(messageString, requestWorkerReaderSubject)
                
            
            #Cleanup
            messageData.mbf_destroy_object()
            buffer.mbf_destroy_buffer()
            logger.info('Message processing completed (messageId:%s)', str(message.id))
            logger.info('************************************************************************************')
            return batches
        except Exception, error:
            raise Exception('Message processing failed. %s' % str(error))
    
    def createRequestTracker(self, requestId, expectedTradeCount):
        try:
            logger.debug('  creating a request tracker with %i expected trades...', int(expectedTradeCount))
            sqlHelper.callStoredProc('DDMInsertRequestTracker', requestId, expectedTradeCount)
            sqlHelper.commit()
        except Exception, error:
            raise Exception('Could not create the request tracker. %s' % str(error))
    
    def sendSubscriptionEvent(self, eventType, requestId):
        try:
            #Create the subscription event to send
            subscriptionEvent = helper.createSubscriptionEvent(self.atsName, eventType, requestId)
        
            #Define the subject on which to send the message
            tradeEventListenerSubject = '%s%i' %(params.tradeEventListenerSubjectTemplate, int(self.getTradeEventListenerIndex()))
            
            #Send the request start event
            if not ambWriter:
                raise Exception('AMB writer not initialised')
                
            ambWriter.post_Message_To_AMB_Raw(subscriptionEvent, tradeEventListenerSubject)
            logger.info("  '%s' subscription event sent to AMB with subject '%s'" % (str(eventType), str(tradeEventListenerSubject)))
        except Exception, error:
            raise Exception('Could send the subscription event. %s' % str(error))
    
    def getRequestWorkerIndex(self):
        global lastRequestWorkerIndex
        if lastRequestWorkerIndex < params.requestWorkerInstances:
            lastRequestWorkerIndex = lastRequestWorkerIndex + 1
        else:
            lastRequestWorkerIndex=1
        return lastRequestWorkerIndex
        
    def getTradeEventListenerIndex(self):
        global lastTradeEventListenerIndex
        if lastTradeEventListenerIndex < params.tradeEventListenerInstances:
            lastTradeEventListenerIndex = lastTradeEventListenerIndex + 1
        else:
            lastTradeEventListenerIndex=1
        return lastTradeEventListenerIndex

    
    
    
