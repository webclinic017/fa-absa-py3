
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQT_ATS_WORKER_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for Request Type ATSs. This module will know
                                how to trade an incoming Request Type and how to transform it into an
                                outgoing Collection ATS Request Message.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_MESSAGE_PROCESS_REQUEST import FC_MESSAGE_PROCESS_REQUEST as MESSAGE_PROCESS_REQUEST
from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE
from FC_DATA_SELECTION import FC_DATA_SELECTION as DATA_SELECTION
import FC_ATS_WORKER_BASE as ATS_WORKER_BASE
import FC_DATA_HELPER as DATA_HELPER
import FC_DATA_REQ_COLL_TRK_REPOSITORY as fcDataRequestCollectionTrackerRepository
import FC_ENUMERATIONS

import time

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_REQT_ATS_WORKER_BASE(ATS_WORKER_BASE.FC_ATS_WORKER_BASE):
    def __init__(self):
        ATS_WORKER_BASE.FC_ATS_WORKER_BASE.__init__(self)
        self._expectedObjectCount = None
        self._batchesToSend = None
        self._componentSubscriptionSubjects = {}
        self._dbProvider = DATA_HELPER.getSqlDBProvider()
        self._previous_processed_requestId = None
        self._requestCollectionTrackerRepository = fcDataRequestCollectionTrackerRepository.FC_DATA_REQ_COLL_TRK_REPOSITORY(self._dbProvider)

    def getLastProcessedMessageId(self):
        pass

    def registerMessageId(self):
        pass

    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        '''----------------------------------------------------------------------------------------------------------
        The AMBA message will be validated and an IncomingMessageObject will be created which will contain all 
        detail needed to process the incoming message further.
        ----------------------------------------------------------------------------------------------------------'''
        self.incomingMessageObject = MESSAGE_OBJECT_REQUEST()
        
        MESSAGE_PROCESS_REQUEST(self.incomingAMBAMessageData, self.incomingMessageObject)


    def processIncommingAMBAMessage(self):

        #DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -1) # Decrease queue

        self._batchesToSend = []
        '''----------------------------------------------------------------------------------------------------------
        Fetch all the trades to calculated the expected trade count
        ----------------------------------------------------------------------------------------------------------'''
        dataSelectionObject = DATA_SELECTION(self.incomingMessageObject.requestType,
                                             self.incomingMessageObject.scopeNumber,
                                             self.incomingMessageObject.scopeName,
                                             self.incomingMessageObject.isEOD,
                                             self.incomingMessageObject.reportDate)
        
        dataSelection = dataSelectionObject.getDataSelection()
        self._expectedObjectCount = 0
        
        if dataSelection:
            self._expectedObjectCount = len(dataSelection)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.S_TRADES_FOUND % (int(self._expectedObjectCount)))

        isRT = self.incomingMessageObject.isEOD == 0
        '''----------------------------------------------------------------------------------------------------------
        Validate trade count against independent selection
        ----------------------------------------------------------------------------------------------------------'''

        if self.incomingMessageObject.isEOD == 1:
            independentTradeCount = DATA_HELPER.GetIndependentTradeCount(self.incomingMessageObject.reportDate, self.incomingMessageObject.scopeNumber)
            if self._expectedObjectCount < independentTradeCount:
                # up flag in table and store message to be possibly replayed;
                DATA_HELPER.RecordFailedSelection(self.incomingMessageObject.reportDate, self.incomingMessageObject.scopeNumber, self.incomingAMBAMessageData.mbf_object_to_string())
        #Recovery from ats startup
        if (self.last_processed_messageId == self.currentMessageId):
            UTILS.Logger.flogger.info("Ats is attempting to reprocess amb messageId %s" % self.currentMessageId)
            UTILS.Logger.flogger.info("Ats will enter into recovery mode for the RequestCollectionTrackerId's")
            self._recovery_mode = True  # Recover from the items already created

        # In memory check to prevent duplication.
        if self._previous_processed_requestId == self.incomingMessageObject.requestId:
            UTILS.Logger.flogger.info('Already processed requestId (%s)' % self.incomingMessageObject.requestId)
            return

        '''----------------------------------------------------------------------------------------------------------
        DB write to update request with expected number of records.
        ----------------------------------------------------------------------------------------------------------'''
        DATA_HELPER.SetRequestTrackerStart(int(self.incomingMessageObject.requestId), self._expectedObjectCount)
        self.registerMessageId()
        '''----------------------------------------------------------------------------------------------------------
        Break into batch sizes
        ----------------------------------------------------------------------------------------------------------'''
        batches = self.getTradeIndexBatches(UTILS.Parameters.fcComponentParameters.componentBatchSizeForCollectionATS, self._expectedObjectCount)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.I_BATCHES_CREATED_I % (len(batches), UTILS.Parameters.fcComponentParameters.componentBatchSizeForCollectionATS))
        self.incomingMessageObject.requestBatchCount = 0
        for batch in batches:
            self.incomingMessageObject.requestBatchCount += 1
            requestBatchNo = self.incomingMessageObject.requestBatchCount
            requestBatchStartIndex, requestBatchEndIndex = batch
            requestBatchTradeCount = 0
            if self._expectedObjectCount > 0:
                requestBatchTradeCount = (requestBatchEndIndex - requestBatchStartIndex) + 1
                
            dataSelectionList = dataSelection[requestBatchStartIndex:requestBatchEndIndex + 1]
            requestCollectionPrimaryKeys = ','.join(map(str, dataSelectionList))
            '''----------------------------------------------------------------------------------------------------------
            DB write to insert Request Collection Tracker with internal batch specific details.
            ----------------------------------------------------------------------------------------------------------'''
            collectionRequestMessage = UTILS.Parameters.fcComponentParameters.componentCollectionRequestMessageSubject
            #print 'Collection request message: ', collectionRequestMessage
            heartbeatComponent = None
            dbRetryCount = 0
            while (heartbeatComponent is None) and dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
                try:
                    heartbeatComponent = DATA_HELPER.GetHeartbeatCandidateComponent(collectionRequestMessage, requestBatchTradeCount, isRT)
                    if heartbeatComponent is None:
                        raise RuntimeError, 'HearbeatComponent is None'
                except Exception, e:
                    UTILS.Logger.flogger.info("Hearbeatcomponent retry failed with reason %s" % str(e))
                    dbRetryCount += 1
                    time.sleep(UTILS.Parameters.fcGenericParameters.HeartbeatTrackInterval)

            if heartbeatComponent == None:
                UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.HEARTBEAT_COMPONENT_IS_NONE)
                UTILS.Logger.flogger.info("Resetting the requestId and messageId in ComponentMessageTracker table.")
                DATA_HELPER.ResetRegisterMessageIdRequestId(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName))
                self.RestartAts()
            
            if heartbeatComponent in self._componentSubscriptionSubjects:
                 UTILS.SenderSubject = self._componentSubscriptionSubjects[heartbeatComponent]
            else:
                 UTILS.SenderSubject = FC_UTILS.GetSenderSubject(heartbeatComponent)
                 self._componentSubscriptionSubjects[heartbeatComponent] = UTILS.SenderSubject

            tradeNumbers = ','.join(str(x) for x in dataSelectionList)

            if tradeNumbers == '':
                tradeNumbers = None

            #Create request tracker with the expected count for restarts
            requestCollectionTrackerId = self._requestCollectionTrackerRepository.createRequestCollectionTracker(
                int(self.incomingMessageObject.requestId), UTILS.ComponentName, heartbeatComponent, requestBatchNo,
                len(batches), requestBatchStartIndex, requestBatchEndIndex, requestBatchTradeCount, tradeNumbers, self._recovery_mode)


            self._batchesToSend.append((requestBatchNo,
                                        requestBatchStartIndex,
                                        requestBatchEndIndex,
                                        requestBatchTradeCount,
                                        requestCollectionTrackerId,
                                        requestCollectionPrimaryKeys,
                                        UTILS.SenderSubject))
        DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -1) # Decrease queue
        return
    
    def GetControlMeasureAttribute(self):
        raise NotImplementedError('Control measure flag cannot be set')
        
        
    def createOutgoingMessageObjects(self):        
        '''----------------------------------------------------------------------------------------------------------
        Generate the response message to be send to the Collection Trade ATSs.
        ----------------------------------------------------------------------------------------------------------'''

        outgoingMessageObject = MESSAGE_OBJECT_RESPONSE()
        outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
        outgoingMessageObject.batchId = self.incomingMessageObject.batchId   
        outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
        outgoingMessageObject.reportDate = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)
        outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.requestDateTime)
        outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
        outgoingMessageObject.requestId = self.incomingMessageObject.requestId
        outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
        outgoingMessageObject.requestType = self.incomingMessageObject.requestType
        outgoingMessageObject.requestUserId = self.incomingMessageObject.requestUserId
        outgoingMessageObject.scopeName = self.incomingMessageObject.scopeName
        outgoingMessageObject.scopeNumber = self.incomingMessageObject.scopeNumber
        outgoingMessageObject.senderSubject = UTILS.SenderSubject
        outgoingMessageObject.topic = self.incomingMessageObject.topic
        outgoingMessageObject.type = UTILS.Constants.fcGenericConstants.Response
        outgoingMessageObject.responseType = UTILS.Constants.fcGenericConstants.S_START %self.incomingMessageObject.requestType
        outgoingMessageObject.expectedObjectCount = str(self._expectedObjectCount)
        self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))   

        #Generate the request message to be send to the Collection Trade ATSs.
        for batch in self._batchesToSend:
            outgoingMessageObject = MESSAGE_OBJECT_REQUEST()
            outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
            outgoingMessageObject.batchId = self.incomingMessageObject.batchId
            outgoingMessageObject.buildControlMeasures = self.GetControlMeasureAttribute()
            outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
            outgoingMessageObject.isDateToday = self.incomingMessageObject.isDateToday
            outgoingMessageObject.reportDate = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)
            outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.requestDateTime)
            outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
            outgoingMessageObject.requestId = self.incomingMessageObject.requestId
            outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
            outgoingMessageObject.requestType = self.incomingMessageObject.requestType
            outgoingMessageObject.requestUserId = self.incomingMessageObject.requestUserId
            outgoingMessageObject.scopeName = self.incomingMessageObject.scopeName
            outgoingMessageObject.scopeNumber = self.incomingMessageObject.scopeNumber
            outgoingMessageObject.senderSubject = str(batch[6])  #_AL
            outgoingMessageObject.topic = self.incomingMessageObject.topic
            outgoingMessageObject.type = UTILS.Parameters.fcComponentParameters.componentCollectionRequestMessageSubject
            outgoingMessageObject.requestBatchCount = self.incomingMessageObject.requestBatchCount
            outgoingMessageObject.requestBatchNo = str(batch[0])
            outgoingMessageObject.requestBatchStartIndex = str(batch[1])
            outgoingMessageObject.requestBatchEndIndex = str(batch[2])
            outgoingMessageObject.requestBatchTradeCount = str(batch[3])
            outgoingMessageObject.requestCollectionTrackerId = str(batch[4])
            outgoingMessageObject.requestCollectionPrimaryKeys = str(batch[5])
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))
        self._previous_processed_requestId = self.incomingMessageObject.requestId
