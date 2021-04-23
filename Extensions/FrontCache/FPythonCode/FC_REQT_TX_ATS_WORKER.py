'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQT_SS_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will receive a Settlement Request. It will the send a response
                                to the response coordinating ATS detailing how many settlements are expected. It
                                will then send a Request to the collection settlement ATSs to retreive the settlement detail.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Aaron Andy
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import FC_REQT_ATS_WORKER_BASE as REQT_ATS_WORKER_BASE
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
from FC_DATA_SELECTION import FC_DATA_SELECTION as DATA_SELECTION
import FC_DATA_HELPER as DATA_HELPER
import FC_ENUMERATIONS
from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE
import time
from datetime import datetime
from datetime import timedelta
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_REQT_TX_ATS_WORKER(REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE):
    def __init__(self):
        REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE.__init__(self)
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
        self._expectedObjectCount = 1

        if dataSelection:
            self._expectedObjectCount = len(dataSelection)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.S_TRADES_FOUND % (int(self._expectedObjectCount)))

        isRT = self.incomingMessageObject.isEOD == 0

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
        if self.incomingMessageObject.requestType == "TRANSACTIONS_EOD":
            DATA_HELPER.SetRequestTrackerStart(int(self.incomingMessageObject.requestId), self._expectedObjectCount)
            self.registerMessageId()
        '''----------------------------------------------------------------------------------------------------------
        Break into batch sizes
        ----------------------------------------------------------------------------------------------------------'''
        batches = self.getTradeIndexBatches(UTILS.Parameters.fcComponentParameters.componentBatchSizeForCollectionATS, self._expectedObjectCount)
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.I_BATCHES_CREATED_I % (len(batches), UTILS.Parameters.fcComponentParameters.componentBatchSizeForCollectionATS))
        self.incomingMessageObject.requestBatchCount = 0
        back_date_start = self.incomingMessageObject.backDateStart
        reportDate = datetime.strptime(str(FC_UTILS.dateTimeStringFromISODateTimeString(str(self.incomingMessageObject.reportDate))), '%Y-%m-%d %H:%M:%S')
        try:
            if back_date_start == 'None':
                back_date_start = reportDate
            else:
                back_date_start = datetime.strptime(str(FC_UTILS.dateTimeStringFromISODateTimeString(str(self.incomingMessageObject.backDateStart))), '%Y-%m-%d %H:%M:%S')
        except:
            back_date_start = reportDate

        while back_date_start <= reportDate:
            self.incomingMessageObject.requestBatchCount += 1
            requestBatchNo = self.incomingMessageObject.requestBatchCount
            requestBatchStartIndex, requestBatchEndIndex = (0, 0)
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
                    heartbeatComponent = DATA_HELPER.GetHeartbeatCandidateComponent(collectionRequestMessage, 1, isRT)
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
            #requestCollectionTrackerId = self._requestCollectionTrackerRepository.createRequestCollectionTracker(
               # int(self.incomingMessageObject.requestId), UTILS.ComponentName, heartbeatComponent, requestBatchNo,
                #len(batches), requestBatchStartIndex, requestBatchEndIndex, requestBatchTradeCount, tradeNumbers, self._recovery_mode)


            self._batchesToSend.append((requestBatchNo,
                                        requestBatchStartIndex,
                                        requestBatchEndIndex,
                                        requestBatchTradeCount,
                                        0,#requestCollectionTrackerId,
                                        requestCollectionPrimaryKeys,
                                        UTILS.SenderSubject,
                                        back_date_start))
            back_date_start = datetime.strptime(str(FC_UTILS.dateTimeFromStringDateOrStringDateTime(str(back_date_start))), '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -1) # Decrease queue
        return

    def GetControlMeasureAttribute(self):
        return UTILS.Parameters.fcComponentParameters.componentControlMeasureFlag

    def createOutgoingMessageObjects(self):
        '''----------------------------------------------------------------------------------------------------------
        Generate the response message to be send to the Collection Trade ATSs.
        ----------------------------------------------------------------------------------------------------------'''

        """
        from datetime import datetime
        from datetime import timedelta

        datestr = '2019-03-28'

        startDate = '2019-02-01'

        while datetime.strptime(startDate,"%Y-%m-%d").date() < datetime.strptime(datestr,"%Y-%m-%d").date():
            startDate = str(datetime.strptime(startDate,"%Y-%m-%d").date() + timedelta(days=1))
            print startDate

        """

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
        outgoingMessageObject.responseType = UTILS.Constants.fcGenericConstants.S_START % 'TRANSACTIONS'
        outgoingMessageObject.expectedObjectCount = str(self._expectedObjectCount)
        self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))

        #Generate the request message to be send to the Collection Trade ATSs.
        """
        back_date_start = self.incomingMessageObject.backDateStart

        if back_date_start == 'None':
            back_date_start = datetime.strptime(str(FC_UTILS.dateTimeStringFromISODateTimeString(str(self.incomingMessageObject.reportDate))),'%Y-%m-%d %H:%M:%S')
        else:
            back_date_start = datetime.strptime(str(FC_UTILS.dateTimeStringFromISODateTimeString(str(self.incomingMessageObject.backDateStart))),'%Y-%m-%d %H:%M:%S')
        reportDate = datetime.strptime(str(FC_UTILS.dateTimeStringFromISODateTimeString(str(self.incomingMessageObject.reportDate))),'%Y-%m-%d %H:%M:%S')
        while back_date_start <= reportDate:
        """
        for batch in self._batchesToSend:
            outgoingMessageObject = MESSAGE_OBJECT_REQUEST()
            outgoingMessageObject.ambaTxNbr = self.incomingMessageObject.ambaTxNbr
            outgoingMessageObject.batchId = self.incomingMessageObject.batchId
            outgoingMessageObject.buildControlMeasures = self.GetControlMeasureAttribute()
            outgoingMessageObject.isEOD = self.incomingMessageObject.isEOD
            outgoingMessageObject.isDateToday = self.incomingMessageObject.isDateToday
            outgoingMessageObject.reportDate = batch[7]#FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)
            outgoingMessageObject.requestDateTime = FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.requestDateTime)
            outgoingMessageObject.requestEventType = self.incomingMessageObject.requestEventType
            outgoingMessageObject.requestId = self.incomingMessageObject.requestId
            outgoingMessageObject.requestSource = self.incomingMessageObject.requestSource
            if 'TRANSACTIONS' not in self.incomingMessageObject.requestType:
                outgoingMessageObject.requestType = 'TRANSACTIONS'
            else:
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
            outgoingMessageObject.requestCollectionPrimaryKeys = self.incomingMessageObject.scopeNumber
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))

        self._previous_processed_requestId = self.incomingMessageObject.requestId
