'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQT_IS_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will receive a Instrument Sensitivity Request. It will the send a
                                response to the response coordinating ATS detailing how many instruments are
                                expected. It will then send a Request to the Instrument Sensitivity Collection
                                ATSs to retreive the instrument detail.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import acm
import time
import FC_REQT_ATS_WORKER_BASE as REQT_ATS_WORKER_BASE
from FC_DATA_SELECTION import FC_DATA_SELECTION as DATA_SELECTION
import FC_DATA_HELPER as DATA_HELPER
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import FC_ENUMERATIONS
from FC_MESSAGE_OBJECT_IS_REQUEST import FC_MESSAGE_OBJECT_IS_REQUEST as MESSAGE_OBJECT_REQUEST
from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE


'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''


class FC_REQT_IS_ATS_WORKER(REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE):
    def __init__(self):
        REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE.__init__(self)

    def GetControlMeasureAttribute(self):
        return UTILS.Parameters.fcComponentParameters.componentControlMeasureFlag

    def processIncommingAMBAMessage(self):

        # DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -1) # Decrease queue

        self._batchesToSend = []
        '''----------------------------------------------------------------------------------------------------------
        Fetch all the trades to calculated the expected trade count
        ----------------------------------------------------------------------------------------------------------'''

        dataSelectionObject = DATA_SELECTION(self.incomingMessageObject.requestType,\
                                            self.incomingMessageObject.scopeNumber,\
                                            self.incomingMessageObject.scopeName,\
                                            self.incomingMessageObject.isEOD,\
                                            self.incomingMessageObject.reportDate)

        dataSelection = dataSelectionObject.getDataSelectionReturnNameandNumber()

        self._expectedObjectCount = 0
        """if acm.FPhysicalPortfolio[self.incomingMessageObject.scopeNumber] is not None:
            self._expectedObjectCount = acm.FPhysicalPortfolio[
                self.incomingMessageObject.scopeNumber].Instruments().Size()
        else:"""
        self._expectedObjectCount = len(dataSelection)
        # if dataSelection:
        #    self._expectedObjectCount = trade_count
        UTILS.Logger.flogger.info('%s instruments found.' % (int(self._expectedObjectCount)))

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
        batches = self.getTradeIndexBatches(1, self._expectedObjectCount)
        self.incomingMessageObject.requestBatchCount = 0
        counter = 0
        for batch in batches:
            counter+=1
            UTILS.Logger.flogger.info('Creating instrument message %s/%s' % (counter, len(batches)))
            self.incomingMessageObject.requestBatchCount += 1
            requestBatchNo = self.incomingMessageObject.requestBatchCount
            requestBatchStartIndex, requestBatchEndIndex = batch

            dataSelectionList = dataSelection[requestBatchStartIndex:requestBatchEndIndex + 1]

            name = ''
            if len(dataSelectionList) > 0:
                requestCollectionPrimaryKey, name = dataSelectionList[0]
                start = time.time()
                query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
                query.AddAttrNodeString('Instrument.Oid', requestCollectionPrimaryKey, 'EQUAL')
                query.AddAttrNodeString('Portfolio.Oid', self.incomingMessageObject.scopeNumber, 'EQUAL')
                query.AddAttrNodeString('Status', ['Simulated', 'Void'], 'NOT_EQUAL')
                requestBatchTradeCount = query.Select().Size()
                UTILS.Logger.flogger.info('     Trades found (%s) Duration (%s)' % (str(requestBatchTradeCount), str(time.time()-start)))
            else:
                requestCollectionPrimaryKey = ','.join(map(str, dataSelectionList))
                requestBatchTradeCount = 0

            '''----------------------------------------------------------------------------------------------------------
            DB write to insert Request Collection Tracker with internal batch specific details.
            ----------------------------------------------------------------------------------------------------------'''
            collectionRequestMessage = UTILS.Parameters.fcComponentParameters.componentCollectionRequestMessageSubject
            isRT = self.incomingMessageObject.isEOD == 0
            start = time.time()
            heartbeatComponent = DATA_HELPER.GetHeartbeatCandidateComponent(collectionRequestMessage,
                                                                            requestBatchTradeCount, isRT)
            UTILS.Logger.flogger.info('     Component found (%s) Duration (%s)' % (heartbeatComponent, str(time.time()-start)))

            if heartbeatComponent is None:
                UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.HEARTBEAT_COMPONENT_IS_NONE)
                UTILS.Logger.flogger.info("Resetting the requestId and messageId in ComponentMessageTracker table.")
                DATA_HELPER.ResetRegisterMessageIdRequestId(
                    FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName))
                self.RestartAts()

            if heartbeatComponent in self._componentSubscriptionSubjects:
                UTILS.SenderSubject = self._componentSubscriptionSubjects[heartbeatComponent]
            else:
                UTILS.SenderSubject = FC_UTILS.GetSenderSubject(heartbeatComponent)
                self._componentSubscriptionSubjects[heartbeatComponent] = UTILS.SenderSubject

            #tradeNumberXml = ','.join(str(x) for x in dataSelectionList)

            #Create request tracker with the expected count
            requestCollectionTrackerId = self._requestCollectionTrackerRepository.createRequestCollectionTracker(
                int(self.incomingMessageObject.requestId), UTILS.ComponentName, heartbeatComponent, requestBatchNo, 1,
                requestBatchStartIndex, requestBatchEndIndex, 1, None, self._recovery_mode)

            self._batchesToSend.append((requestBatchNo,
                                        requestBatchStartIndex,
                                        requestBatchEndIndex,
                                        requestBatchTradeCount,
                                        requestCollectionTrackerId,
                                        requestCollectionPrimaryKey,
                                        UTILS.SenderSubject, name))
        DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -1)  # Decrease queue
        return

    def getLastProcessedMessageId(self):
        self.last_processed_messageId, self.requestId, self.retryCount = DATA_HELPER.GetLastProcessedMessageInfo(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName))
    def registerMessageId(self):
        DATA_HELPER.RegisterMessageId(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), self.currentMessageId, self.incomingMessageObject.requestId)

    def createOutgoingMessageObjects(self):
        '''----------------------------------------------------------------------------------------------------------
        Generate the response message to be send to the Collection Trade ATSs.
        ----------------------------------------------------------------------------------------------------------'''
        outgoingMessageObject = MESSAGE_OBJECT_RESPONSE()
        outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
        outgoingMessageObject.batchId = self.incomingMessageObject.batchId
        outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
        outgoingMessageObject.reportDate = FC_UTILS.dateTimeStringFromISODateTimeString(
            self.incomingMessageObject.reportDate)
        outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(
            self.incomingMessageObject.requestDateTime)
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
        outgoingMessageObject.responseType = UTILS.Constants.fcGenericConstants.S_START % self.incomingMessageObject.requestType
        outgoingMessageObject.expectedObjectCount = str(self._expectedObjectCount)
        self.outgoingAMBADataDictionaries.append(
            (outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))

        # Generate the request message to be send to the Collection Trade ATSs.
        for batch in self._batchesToSend:
            outgoingMessageObject = MESSAGE_OBJECT_REQUEST()
            outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
            outgoingMessageObject.batchId = self.incomingMessageObject.batchId
            outgoingMessageObject.buildControlMeasures = self.GetControlMeasureAttribute()
            outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
            outgoingMessageObject.isDateToday = self.incomingMessageObject.isDateToday
            outgoingMessageObject.reportDate = FC_UTILS.dateTimeStringFromISODateTimeString(
                self.incomingMessageObject.reportDate)
            outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(
                self.incomingMessageObject.requestDateTime)
            outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
            outgoingMessageObject.requestId = self.incomingMessageObject.requestId
            outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
            outgoingMessageObject.requestType = self.incomingMessageObject.requestType
            outgoingMessageObject.requestUserId = self.incomingMessageObject.requestUserId
            outgoingMessageObject.scopeName = str(batch[7])
            outgoingMessageObject.scopeNumber = str(batch[5])
            outgoingMessageObject.senderSubject = str(batch[6])  # _AL
            outgoingMessageObject.topic = self.incomingMessageObject.topic
            outgoingMessageObject.type = UTILS.Parameters.fcComponentParameters.componentCollectionRequestMessageSubject
            outgoingMessageObject.requestBatchCount = self.incomingMessageObject.requestBatchCount
            outgoingMessageObject.requestBatchNo = str(batch[0])
            outgoingMessageObject.requestBatchStartIndex = str(batch[1])
            outgoingMessageObject.requestBatchEndIndex = str(batch[2])
            outgoingMessageObject.requestBatchTradeCount = str(batch[3])
            outgoingMessageObject.requestCollectionTrackerId = str(batch[4])
            outgoingMessageObject.requestCollectionPrimaryKeys = str(batch[5])
            outgoingMessageObject.portfolioName = self.incomingMessageObject.scopeName
            outgoingMessageObject.portfolioNumber = self.incomingMessageObject.scopeNumber
            self.outgoingAMBADataDictionaries.append(
                (outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))
        self._previous_processed_requestId = self.incomingMessageObject.requestId
