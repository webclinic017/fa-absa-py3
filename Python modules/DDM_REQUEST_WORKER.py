'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_REQUEST_WORKER
PROJECT                 :       (Pegasus) Data Distribution Model - ATS
PURPOSE                 :       This module receives DDM request messages, generates trade batch reports and 
                                sends it to an external Trade Event listener service
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
import DDM_REQUEST_MESSAGE as requestMessage
from DDM_TRADE_WORKER import DDM_TRADE_WORKER
import DDM_REPORT_API as reportAPI
import AMB_Reader_Writer as ambReaderWriter


#Static Globals
logger = FLogger.FLogger('DDM_REQUEST_WORKER', params.logLevel)
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
# DDM_REQUEST_WORKER class
#******************************************************************************************************** 
class DDM_REQUEST_WORKER():
    
    #Class locals
    atsName = None
    #Create a element builder 
    #tradeElementBuilder = None 
    tradeWorker = None
    #static objects
    legReportBuilder = None

            
            
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
            #self.tradeElementBuilder = elementBuilder.TRADE_ELEMENT_BUILDER()
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
                sqlHelper.callStoredProc('DDMInsertErrorLog', self.atsName, 0, 'ProcessRequestBatch', str(error))
                sqlHelper.commit()
            except Exception, sqlError:
                logger.error('Could not log the error to the database. %s', str(sqlError))
            
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
            logger.info(' Request Batch %s of %s' % (str(requestMsg.requestBatchNo), str(requestMsg.requestBatchCount))) 
            logger.info('   Start Index:              %s' % str(requestMsg.requestBatchStartIndex))
            logger.info('   End Index:                %s' % str(requestMsg.requestBatchEndIndex))
            logger.info('   Trade Count:              %s' % str(requestMsg.requestBatchTradeCount))
            
            #Fetch the trades for the request
            logger.debug('  ')
            
            #Process the batch
            logger.info('  processing batch...')
            
            #Fetch the trades and get the trade count
            trades = self.getTrades(requestMsg)
            expectedTradeCount = 0
            if trades:
                expectedTradeCount = len(trades)
            
            #Build the trade elements and add them to a insert cursor
            actualTradeCount  = self.processTradeElements(requestMsg, trades)
            
            #Fetch the request's committed trade count to test if the request is finished
            committedTradeCount = self.getCommittedTradeCount(requestMsg.requestId)
            if committedTradeCount >= expectedTradeCount:
                #Update the request tracker
                self.updateRequestTracker(requestMsg.requestId, committedTradeCount)
                #Send the request end subscription event
                self.sendSubscriptionEvent('RequestEnd', requestMsg.requestId)
            
            #Cleanup
            messageData.mbf_destroy_object()
            buffer.mbf_destroy_buffer()
            self.cleanup()
            
            #calculate the processing time
            processingSeconds = helper.calcLapsedTimeInSeconds(messageStartTime, datetime.now() )
            tradesPerSecond = actualTradeCount
            if processingSeconds!=0:
                tradesPerSecond =actualTradeCount/processingSeconds
                
            logger.info('Message processing completed in %s seconds at %s trades/s (messageId:%s)', str(processingSeconds), str(tradesPerSecond), str(message.id))
            logger.info('************************************************************************************')
                        
        except Exception, error:
            raise Exception('Message processing failed. %s' % str(error))
    
    def getTrades(self, requestMsg):
        try:
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
                
            return trades
        except Exception, error:
            raise Exception('Could not get the trades. %s' % str(error))
    
    #Process the trades and return the trade count
    def processTradeElements(self, requestMsg, trades):
        try:
            
            #Count the trades processed
            tradeCounter = 0
            
            #Fetch the request id and report date
            requestId = requestMsg.requestId
            reportDate = datetime.strptime(requestMsg.reportDate, '%Y-%m-%d')
             
            #Process the trades if any
            logger.info('  processing trades...')
            if trades:
                #Initialise the trade index counter to the start index
                tradeIndex = int(requestMsg.requestBatchStartIndex)
                
                #Get the trade range for the given start and end index
                tradeRange = trades.FromTo(int(requestMsg.requestBatchStartIndex), int(requestMsg.requestBatchEndIndex)+1)
                
                #Fetch the multi legged trades and generate the xml report if any exists
                tradesLegCollection = acm.FDictionary()
                multileggedReportOutput=None
                multileggedTrades=[]
                for trade in tradeRange:
                    if trade.Instrument():
                        if len(trade.Instrument().Legs()) > 1:
                            multileggedTrades.append(trade.Oid())
                
                if len(multileggedTrades) > 0:
                    logger.info('    %i multilegged trades found in batch' % len(multileggedTrades))
                    logger.info('    generating multilegged report...')
                    multileggedReportOutput = self.generateMultiLeggedReport(multileggedTrades)
                    tradesLegCollection = helper.getTradesLegCollection(multileggedReportOutput)
                    logger.info('    multilegged report generated for %i trades' % len(tradesLegCollection))
                    
                
                #Build the individual trade elements
                sqlParams = []
                for trade in tradeRange:
                    tradeNumber = trade.Oid()
                    tradeCounter = tradeCounter + 1
                    logger.debug('    processing trade %i of %i...(tradeNumber:%s, batch:%i of %i)'\
                            , int(tradeCounter), int(requestMsg.requestBatchTradeCount), str(trade.Oid()), int(requestMsg.requestBatchNo), int(requestMsg.requestBatchCount))
                    #build the trade element
                    tradeInfo, tradeElement = self.tradeWorker.buildTrade(reportDate, trade, tradesLegCollection[tradeNumber])
                    
                    #self.tradeElementBuilder.build(reportDate, trade) 
                    #set the additional trade infomation
                    tradeInfo.eventDateTime = requestMsg.requestDateTime
                    tradeInfo.eventType = 'RequestTrade'
                    tradeInfo.eventSource = self.atsName
                    tradeInfo.requestId = requestMsg.requestId
                    tradeInfo.requestDateTime = requestMsg.requestDateTime
                    tradeInfo.requestSource = requestMsg.requestSource
                    tradeInfo.requestEventType = requestMsg.requestEventType
                    tradeInfo.requestType = requestMsg.requestType
                    tradeInfo.scopeNumber = requestMsg.scopeNumber
                    tradeInfo.scopeName = requestMsg.scopeName
                    tradeInfo.batchNumber = requestMsg.batchNumber
                    tradeInfo.batchName = requestMsg.batchName
                    if requestMsg.requestEventType=='EOD_REQUEST_EVENT':
                        tradeInfo.isEODVersion = True
                    else:
                        tradeInfo.isEODVersion = False
                    
                    #Create the trade info element and trade message xml
                    tradeMessageElement=Element('tradeMessage')
                    tradeInfoElement = tradeInfo.createElement()
                    tradeMessageElement.append(tradeInfoElement)
                    tradeMessageElement.append(tradeElement)
                    
                    #SQL specific date formatting as a string
                    sqlReportDateStr = tradeInfo.reportDate.strftime("%d %b %Y")
                    compressedTradeData = helper.deflate_and_base64_encode(tostring(tradeMessageElement))
                    #add the sql params
                    sqlParams.append((requestId, 
                                    sqlReportDateStr, 
                                    tradeInfo.tradeNumber, 
                                    tradeIndex,
                                    tradeInfo.tradeDomain,  
                                    tradeInfo.versionHash,
                                    self.atsName,
                                    tradeInfo.bookId,
                                    tradeInfo.productMainType,
                                    tradeInfo.sourceCounterpartyNumber,
                                    tradeInfo.sourceCounterpartySystem,
                                    tostring(tradeInfoElement),
                                    compressedTradeData))
                    
                    #finally increase the tradeIndex which gets stored with each trade
                    tradeIndex = tradeIndex + 1
            
                #commit batch to the database
                sqlHelper.callStoredProcMany('DDMInsertRequestTrade', sqlParams)
                logger.info('  %i trades committed to the database' % int(tradeCounter))
            
            #return the processed trade count
            return tradeCounter
        except Exception, error:
            sqlHelper.rollback()
            raise Exception('Could not process the trades. %s' % str(error))
       

    def getCommittedTradeCount(self, requestId):
        try:
            committedTradeCount=0
            requestTradeCountCursor = sqlHelper.callStoredProcWithCursor("DDMGetRequestActualTradeCount", requestId)
            if requestTradeCountCursor:
                try:
                    rows = requestTradeCountCursor.fetchall()
                    if len(rows)==1:
                        if rows[0][0]:
                            committedTradeCount = int(rows[0][0])
                    #print dir(rows)
                    
                except Exception, error:
                    raise Exception('Could not read the committed trade count. %s' % str(error))
            sqlHelper.commit()    
            return committedTradeCount
        except Exception, error:
            raise Exception('Could not get the committed trade count. %s' % str(error))
            
    
    
    def updateRequestTracker(self, requestId, actualTradeCount):
        try:
            logger.debug('  updating a request tracker with %i actual trades', int(actualTradeCount))
            sqlHelper.callStoredProc('DDMUpdateRequestTracker', requestId, actualTradeCount)
            sqlHelper.commit()
        except Exception, error:
            raise Exception('Could not create the request tracker. %s' % str(error))
    
    def getTradeEventListenerIndex(self):
        global lastTradeEventListenerIndex
        #Determine the trade event listener to send the message to
        if lastTradeEventListenerIndex < params.tradeEventListenerInstances:
            lastTradeEventListenerIndex = lastTradeEventListenerIndex + 1
        else:
            lastTradeEventListenerIndex=1
        return lastTradeEventListenerIndex
    
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
        
    def generateMultiLeggedReport(self, trades):
        try:
            if not self.legReportBuilder:
                logger.debug('    loading the report builder...')
                self.legReportBuilder = reportAPI.DDMReportBuilder()
                self.legReportBuilder.clearSheetContent = True
                self.legReportBuilder.includeDefaultData = False
                self.legReportBuilder.includeFormattedData = True
                self.legReportBuilder.includeFullData = False
                self.legReportBuilder.includeRawData = False
                self.legReportBuilder.includeColorInformation = False
                self.legReportBuilder.instrumentParts = True
                self.legReportBuilder.reportName = 'legReport'
                self.legReportBuilder.templateName = params.legSheetTemplateName
                self.legReportBuilder.xslStyleSheetName = params.portfolioSheetXsl
            
            self.legReportBuilder.rawReportOutput = None
            self.legReportBuilder.transformedReportOutput = None
            #self.legReportBuilder.tradeNumbers = [trades[0]]
            self.legReportBuilder.tradeNumbers = trades
            self.legReportBuilder.generateReportOutput()
            #get the report output
            reportOutput = self.legReportBuilder.transformedReportOutput
            return reportOutput
            
        except Exception, error:
            raise Exception('Could not generate the multilegged report. %s' % str(error))
            
    def cleanup(self):
        for eb in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
            eb.Reset()
        acm.Memory().GcWorldStoppedCollect()    
        acm.FCache.Select01('.StringKey = "evaluators"', "").Statistics()
        acm.FCache.Select01('.StringKey = "evaluator builders"', "").Statistics()
