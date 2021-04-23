'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_INTRADAY_WORKER
PROJECT                 :       (Pegasus) Data Distribution Model - ATS
PURPOSE                 :       This module receives DDM intraday messages from the AMBA and processes it
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
import acm
import amb
import os
import time
import FLogger
import collections
from datetime import datetime, date
from xml.etree.ElementTree import Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params
import DDM_SQL_HELPER as sqlHelper
import DDM_INTRADAY_MESSAGE as intradayMessage
from DDM_TRADE_WORKER import DDM_TRADE_WORKER
import AMB_Reader_Writer as ambReaderWriter


#Static Globals
logger = FLogger.FLogger('DDM_INTRADAY_WORKER', params.logLevel)
ambWriter = None
ambReader = None
readerSubjects = None
readerMBName = None
messageQueue = collections.deque()
lastTradeEventListenerIndex = 0

global ATS_STATUS
ATS_STATUS = 'RUNNING'
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
# Forces the ATS service to restart
#*******************************************************************************************************************************
def restartATS():
    global ATS_STATUS
    global ambWriter
    global ambReader
    global logger
    
    ATS_STATUS = 'SHUTTING DOWN'
    logger.info('Closing the AMB reader connection...')
    ambReader.close_AMB_Connection()
    logger.info('Closing the AMB writer connection...')
    ambWriter.close_AMB_Connection()
    os._exit(1)


def checkMemoryThreshold():
    global messageQueue
    global logger
    currentVirtualMemory  = helper.getVirtualMemory()
    if params.restartIfMemoryThresholdExceeded:
        if(int(currentVirtualMemory) > int(params.memoryThreshold)):
            messageQueue.clear()
            logger.warn('Current virtual memory usage exceeds the memory threshold of %s KB, forcing a restart...' % str(params.memoryThreshold))
            restartATS()


#********************************************************************************************************
# DDM_INTRADAY_WORKER class
#******************************************************************************************************** 
class DDM_INTRADAY_WORKER():
    
    #Class locals
    atsName = None
    #Create a element builder 
    #tradeElementBuilder = None 
    tradeWorker = None
            
    #Class Constructor
    def __init__(self, pATSName, pReaderMBName, pReaderSubjects):
        global readerSubjects
        global readerMBName
        #Set local class variables
        self.atsName = pATSName
        readerMBName = pReaderMBName
        readerSubjects = pReaderSubjects
        
    #Start the ATS    
    def start(self):
        global messageQueue
        global readerSubjects
        global readerMBName
        try:
            logger.info('****************************************************************************')
            logger.info('ATS started at %s' % str(time.ctime()))
            logger.info('****************************************************************************')
            logger.info(' ATS Name                              : %s' % str(self.atsName))
            logger.info(' Platform                              : %s' % str(helper.platformName))
            logger.info(' Process Id                            : %s' % str(helper.processId))
            logger.info(' Restart on memory threshold           : %s' % str(params.restartIfMemoryThresholdExceeded))
            logger.info(' Memory Threshold                      : %s KB' % str(params.memoryThreshold))
            logger.info('****************************************************************************')
            logger.info('* Setting up AMB connections... ')
            logger.info('****************************************************************************')
            logger.info(' AMB Host            :                 %s' % str(params.ambAddress))
            logger.info(' AMB Reader          :                 %s' % str(readerMBName))
            logger.info(' AMB Reader subjects :                 %s' % str(readerSubjects))
            logger.info('****************************************************************************')
            logger.info('Message queue length at %i', len(messageQueue))
            #Create the AMB reader and writer
            createAMBWriter()
            logger.info('AMB writer ready!')
            createAMBReader()
            logger.info('AMB reader ready!')
            
            #create the trade element builder
            self.tradeWorker = DDM_TRADE_WORKER()
            logger.info('Trade worker created!')
            
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
        global ambReader
        global ATS_STATUS
        if ATS_STATUS != 'RUNNING':
            return
        
        
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
            
            #First try accept the message off the AMB (to elminate duplicates when the ATS restarts
            acceptResult = amb.mb_queue_accept(channel, message, str(message.id))
            #accept not successfull
            if acceptResult != None:
                raise Exception('  could not accept message %s. %s' % (str(message.id), str(error)))
            logger.info('  message accepted (messageId:%i)' % int(message.id))
            #Poll
            amb.mb_poll()
            
            #Check the queue count
            logger.info('%s messages remaining in the queue' % str(len(messageQueue)))
            logger.info('     ')
                    
            #First check the memory before processing the next message and restart if it exceeds the threshold
            checkMemoryThreshold()
            
        except Exception, error:
            #log the error to the log file
            logger.error('A fatal error was encountered. %s. shutting down the ATS...', str(error))
            
            #log the error to the database
            try:
                sqlHelper.callStoredProc('DDMInsertErrorLog', self.atsName, error)
                sqlHelper.commit()
            except Exception, sqlError:
                logger.error('Could not log the error to the database...', str(sqlError))
            
            #exit the process
            raise SystemExit('cannot continue')
            
        
    
    #Reads the message content as a string
    def processMessage(self, message):
        global sqlConnection
        global messageQueue
        global ambReader
        global ambWriter
        #Start the processing if the queue contains messages
        try:
            messageStartTime = datetime.now()
            messageEndTime = datetime.now()
            logger.info('')
            logger.info('************************************************************************************')
            logger.info('Processing message (messageId:%i)...' % int(message.id))
            
            #Read the message content
            buffer = amb.mbf_create_buffer_from_data(message.data_p)
            messageData = buffer.mbf_read()
            
            #Create an instance of a request message by using the received AMB message
            intradayMsg = intradayMessage.DDM_INTRADAY_MESSAGE(messageData)
            if not intradayMsg:
                raise Exception('Could not construct the intraday message')
            
            #Log the message detail
            logger.debug(' ')
            logger.debug('Message details:')
            logger.debug(' Source:                     %s' % str(intradayMsg.source))
            logger.debug(' Type:                       %s' % str(intradayMsg.type))
            logger.debug(' Time:                       %s' % str(intradayMsg.time))
            logger.debug(' Transaction Number:         %s' % str(intradayMsg.txNbr))
            logger.debug(' Instrument address:         %s' % str(intradayMsg.instrumentAddress))
            logger.debug(' Trade number:               %s' % str(intradayMsg.tradeNumber))
            
            #Process the batch
            logger.info('  processing event...')
            
            #Process the event based on type
            trades = acm.FArray()
            if intradayMsg.type=='INSERT_TRADE' or intradayMsg.type=='UPDATE_TRADE':
                trade = acm.FTrade[intradayMsg.tradeNumber]
                if not trade:
                    logger.error(' Trade not found %s' % str(intradayMsg.tradeNumber))
                    tradeInfo, tradeElement = self.tradeWorker.buildTrade(reportDate, trade)
                else:
                    trades.Add(trade)
                    
                    
            #Fetch the request id and report date
            reportDate = datetime.strptime(intradayMsg.time, '%Y-%m-%d %H:%M:%S')
            
            #Create SQL string for the dates
            sqlIntradayEventDateTimeStr = reportDate.strftime("%d %b %Y %H:%M:%S")
            sqlReportDateStr = reportDate.strftime("%d %b %Y 00:00:00")
            messageString = messageData.mbf_object_to_string() 
            
            #Insert the intraday event 
            intradayEventId=0
            sqlHelper.callStoredProc('DDMInsertIntradayEvent',
                                            sqlIntradayEventDateTimeStr, 
                                            sqlReportDateStr, 
                                            intradayMsg.source,
                                            intradayMsg.type,  
                                            message.id,
                                            messageString)
            
            
            intradayEventCursor = sqlHelper.callStoredProcWithCursor('DDMGetIntradayEventIdBySourceMessageId',  message.id)
            intradayEventId = long(intradayEventCursor.fetchone()[0])
            sqlHelper.commit()
                        
            #Process the trades if any
            logger.info('  processing trade(s)...')
            
            
            #Count the trades processed
            tradeCounter = 0
            
            #fetch the trades
            trades = self.getTrades(intradayMsg)
            expectedTradeCount = 0
            if trades:
                expectedTradeCount = len(trades)
                
            if trades:
                for trade in trades:
                    tradeNumber = trade.Oid()
                    tradeCounter = tradeCounter + 1
                    logger.debug('    processing trade %i of %i...(tradeNumber:%s)'\
                                , int(tradeCounter), int(expectedTradeCount), str(trade.Oid()))
                    #build the trade element
                    tradeInfo, tradeElement = self.tradeWorker.buildTrade(reportDate, trade)
                        
                    #set the additional trade infomation
                    tradeInfo.eventDateTime = intradayMsg.time
                    tradeInfo.eventType = 'IntradayTrade'
                    tradeInfo.eventSource = self.atsName
                    tradeInfo.isEODVersion = False
                    
                    #Create the trade info element and trade message xml
                    tradeMessageElement=Element('tradeMessage')
                    tradeInfoElement = tradeInfo.createElement()
                    tradeMessageElement.append(tradeInfoElement)
                    tradeMessageElement.append(tradeElement)
                    
                    #Compress the trade data
                    compressedTradeData = helper.deflate_and_base64_encode(tostring(tradeMessageElement))
           
                    #write the trade element to the insert cursor
                    sqlHelper.callStoredProcWithCursor('DDMInsertIntradayEventTrade',
                                                        intradayEventId, 
                                                        sqlReportDateStr, 
                                                        tradeInfo.tradeNumber, 
                                                        tradeInfo.tradeDomain,  
                                                        tradeInfo.versionHash,
                                                        self.atsName,
                                                        tradeInfo.bookId,
                                                        tradeInfo.productMainType,
                                                        tradeInfo.sourceCounterpartyNumber,
                                                        tradeInfo.sourceCounterpartySystem,
                                                        tostring(tradeInfoElement),
                                                        compressedTradeData)
                    #commit to the database
                    sqlHelper.commit()
                    logger.info('  %i trades committed to the database' % int(tradeCounter))
                
                    #Send the request end subscription event
                    self.sendSubscriptionEvent('IntradayTrade', intradayEventId)
                
            
            #Cleanup
            messageData.mbf_destroy_object()
            buffer.mbf_destroy_buffer()
            self.cleanup()
            
            #calculate the processing time
            processingSeconds = helper.calcLapsedTimeInSeconds(messageStartTime, datetime.now() )
            tradesPerSecond = tradeCounter
            if processingSeconds!=0:
                tradesPerSecond =tradeCounter/processingSeconds
                
            logger.info('Message processing completed in %s seconds at %s trades/s (messageId:%s)', str(processingSeconds), str(tradesPerSecond), str(message.id))
            logger.info('************************************************************************************')
                
        except Exception, error:
            raise Exception('Message processing failed. %s' % str(error))
    
    def getTrades(self, intradayMsg):
        try:
            trades = acm.FArray()
            if intradayMsg.type=='INSERT_TRADE' or intradayMsg.type=='UPDATE_TRADE':
                trade = acm.FTrade[intradayMsg.tradeNumber]
                if not trade:
                    logger.error(' Trade not found %s' % str(intradayMsg.tradeNumber))
                else:
                    trades.Add(trade)
            elif intradayMsg.type=='UPDATE_INSTRUMENT':
                instrument = acm.FInstrument[intradayMsg.instrumentAddress]
                if not instrument:
                    logger.error(' Instrument not found %s' % str(intradayMsg.instrumentAddress))
                else:
                    trades = instrument.Trades()
            else:
                logger.info('%s event type requires no action' % str(intradayMsg.type))
                
            #return the trades
            return trades
            
        except Exception, error:
            raise Exception('Could not fetch the trades. %s' % str(error))
    
    def getTradeEventListenerIndex(self):
        global lastTradeEventListenerIndex
        #Determine the trade event listener to send the message to
        if lastTradeEventListenerIndex < params.tradeEventListenerInstances:
            lastTradeEventListenerIndex = lastTradeEventListenerIndex + 1
        else:
            lastTradeEventListenerIndex=1
        return lastTradeEventListenerIndex
        
    def sendSubscriptionEvent(self, eventType, intradayEventId):
        try:
            #Create the subscription event to send
            subscriptionEvent = helper.createSubscriptionEvent(self.atsName, eventType, intradayEventId)
        
            #Define the subject on which to send the message
            tradeEventListenerSubject = '%s%i' %(params.tradeEventListenerSubjectTemplate, int(self.getTradeEventListenerIndex()))
            
            #Send the request start event
            if not ambWriter:
                raise Exception('AMB writer not initialised')
                
            ambWriter.post_Message_To_AMB_Raw(subscriptionEvent, tradeEventListenerSubject)
            logger.info("  '%s' subscription event sent to AMB with subject '%s'" % (str(eventType), str(tradeEventListenerSubject)))
        except Exception, error:
            raise Exception('Could send the subscription event. %s' % str(error))
            
            
    def cleanup(self):
        for eb in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
            eb.Reset()
        acm.Memory().GcWorldStoppedCollect()    
        acm.FCache.Select01('.StringKey = "evaluators"', "").Statistics()
        acm.FCache.Select01('.StringKey = "evaluator builders"', "").Statistics()

