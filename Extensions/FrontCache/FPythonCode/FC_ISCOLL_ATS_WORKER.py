'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_ISCOLL_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for Instrument Sensitivity Collection ATSs. It
                                will connect to the AMB and prcess Instrument Sensitivity Collection Requests.
                                It will retreive the data from Front Arena, save the data to the database and
                                post reponse messages to the AMB.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''
'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_COLL_ATS_WORKER_BASE as COLL_ATS_WORKER_BASE
import FC_DATA_HELPER as DATA_HELPER
import FC_ENUMERATIONS as ENUMERATIONS
from FC_MESSAGE_OBJECT_IS_REQUEST import FC_MESSAGE_OBJECT_IS_REQUEST as MESSAGE_OBJECT_REQUEST
from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE
from FC_MESSAGE_PROCESS_REQUEST import FC_MESSAGE_PROCESS_REQUEST as MESSAGE_PROCESS_REQUEST
from FC_DATA_SEN_BUILDER_OPTIONS import FC_DATA_SEN_BUILDER_OPTIONS as  fcDataSensitivityBuilderOptions
from FC_UTILS import FC_UTILS as UTILS
import FC_ENUMERATIONS
import FC_UTILS
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''


class FC_ISCOLL_ATS_WORKER(COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE):
    def __init__(self):
        COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE.__init__(self)
        self._sensitivityType = UTILS.Constants.fcGenericConstants.INSTRUMENT
        self.portfolioName = ''
        self.portfolioNumber = 0

    def SaveData(self, requestId, reportDate, startIndex, numbers, buildControlMeasures, retryCount, requestType, scopeName):
        self._buildOptions = fcDataSensitivityBuilderOptions()
        self._buildOptions.SerializationType = ENUMERATIONS.SerializationType.PROTOBUF
        self._buildOptions.HistoricalCashflowRange = 5
        return DATA_HELPER.BuildAndSaveSensitivities(requestId,
                                                     reportDate,
                                                     startIndex,
                                                     numbers,
                                                     self._buildOptions,
                                                     self._sensitivityType,
                                                     self.portfolioName,
                                                     self.portfolioNumber)

    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        '''----------------------------------------------------------------------------------------------------------
        The AMBA message will be validated and an IncomingMessageObject will be created which will contain all
        detail needed to process the incoming message further.
        ----------------------------------------------------------------------------------------------------------'''
        self.incomingMessageObject = MESSAGE_OBJECT_REQUEST()

        MESSAGE_PROCESS_REQUEST(self.incomingAMBAMessageData, self.incomingMessageObject)

    def processIncommingAMBAMessage(self):
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_I_OF_I_I_ITEMS % (
        self.incomingMessageObject.requestBatchNo, self.incomingMessageObject.requestBatchCount,
        self.incomingMessageObject.requestBatchTradeCount))

        # If the ats historical date is not equal to the reportdate then the registry will be updated and the ats restarted to
        # process the message correctly
        if str(self.incomingMessageObject.isDateToday) == "1" and FC_UTILS.RestartAtsForDateToday(FC_UTILS.dateStringFromDateTimeString(FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)), FC_UTILS.Ats_service_name, FC_UTILS.DateToday):
            UTILS.Logger.flogger.info("Ats is not the correct date_today. Ats will update registry and restart")
            self.RestartAts()
        elif str(self.incomingMessageObject.isDateToday) == "0" and FC_UTILS.RestartAtsForHistoricalDate(FC_UTILS.dateStringFromDateTimeString(FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)), FC_UTILS.Ats_service_name, FC_UTILS.HistoricalDate):
            UTILS.Logger.flogger.info("Ats is not the correct historical date. Ats will update registry and restart")
            self.RestartAts()

        primaryKeyRange = self.incomingMessageObject.scopeNumber
        self.portfolioName = str(self.incomingMessageObject.portfolioName)
        self.portfolioNumber = int(self.incomingMessageObject.portfolioNumber)

        chunkCheckerResult = DATA_HELPER.CheckChunkHasCompleted(self.incomingMessageObject.requestCollectionTrackerId)

        if (self.last_processed_messageId == self.currentMessageId):
            UTILS.Logger.flogger.info("Ats is attempting to reprocess amb messageId %s" % self.currentMessageId)
            UTILS.Logger.flogger.info("Ats will enter into recovery mode for the sensitivity")
            self._recovery_mode = True  # Recover from the items already created
        # Check if the chunk to be processed has already been completed
        else:
            DATA_HELPER.RegisterMessageId(serviceComponentId=FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), messageId=self.currentMessageId, requestId=self.incomingMessageObject.requestId, retryCount=0)
        (staticIds, errors) = ([0], '')
        # Check if the chunk to be processed has already been completed
        processCount = 0
        errorCount = 0
        self._expectedObjectCount = 0
        if chunkCheckerResult == 0:
            #Check here if trades may already exist in the db if in recovery_mode
            if self._recovery_mode is True and self.incomingMessageObject.scopeName is not None and DATA_HELPER.CheckIfSensitivityExistForRequestId(
                    self.incomingMessageObject.requestId, self.incomingMessageObject.scopeName, FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)) is True:
                processCount = DATA_HELPER.GetProcessedCountForRequestCollectionTrackerId(self.incomingMessageObject.requestCollectionTrackerId)
                if processCount > 0: processCount = 0 # Prevent messing up the requestTracker processedCount
                else:
                    if self.incomingMessageObject.scopeName is not None:
                        processCount = 1
                        self._expectedObjectCount = processCount# Correct the requestTracker processedCount
                errorCount = 0
            else:
                (staticIds, errors) = self.SaveData(self.incomingMessageObject.requestId,
                                                    self.incomingMessageObject.reportDate,
                                                    self.incomingMessageObject.requestBatchStartIndex, primaryKeyRange)
                if self.incomingMessageObject.scopeName is not None:
                    processCount = 1
                    self._expectedObjectCount = processCount# Correct the requestTracker processedCount
            errorCount = len(errors)
            if errorCount > 0:
                UTILS.Logger.flogger.info('Save Data errors: %s' % errors)
                if self.retryCount + 1 <= UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
                    DATA_HELPER.RegisterMessageId(serviceComponentId=FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), messageId=self.currentMessageId, requestId=self.incomingMessageObject.requestId, retryCount=self.retryCount+1)
                    UTILS.Logger.flogger.info('ATS will restart due to errors, retry attempt (%s)', self.retryCount+1)
                    self.RestartAts()

            if self.retryCount > 0:
                DATA_HELPER.RegisterMessageId(serviceComponentId=FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), messageId=self.currentMessageId, requestId=self.incomingMessageObject.requestId, retryCount=0)
                self.retryCount = 0

        hbcounter = int(self.incomingMessageObject.requestBatchTradeCount)
        if hbcounter > 0:
            DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -hbcounter)  # Decrease queue
        '''----------------------------------------------------------------------------------------------------------
        Trade batch complete, update the request tracker
        ----------------------------------------------------------------------------------------------------------'''
        trackerResult = ''
        trackerResult = DATA_HELPER.SetRequestTrackerEnd(self.incomingMessageObject.requestId,
                                                         processCount - errorCount, errorCount,
                                                         self.incomingMessageObject.requestCollectionTrackerId,
                                                         self.incomingMessageObject.batchId, errors)
        self._requestComplete = self.isRequestComplete(trackerResult)
        self._batchComplete = self.isBatchComplete(trackerResult)

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.REQUEST_COMPLETE_S % str(self._requestComplete))
        if self._requestComplete > 0:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.PROCESSED_I_ERRORS % (
            self.incomingMessageObject.requestBatchNo, processCount, errorCount))
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.COMPLETE_RESPONSE)

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_COMPLETE_S % str(self._batchComplete))
        if self._batchComplete > 0:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_COMPLETE_RESPONSE \
                                      % int(self.incomingMessageObject.batchId))

        if self._requestComplete == 0 and self._batchComplete == 0:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.PROCESSED_I_ERRORS % (
            self.incomingMessageObject.requestBatchNo, processCount, errorCount))

        return

    def createOutgoingMessageObjects(self):
        if self._requestComplete > 0:
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
            outgoingMessageObject.scopeName = self.incomingMessageObject.portfolioName
            outgoingMessageObject.scopeNumber = self.incomingMessageObject.portfolioNumber
            outgoingMessageObject.topic = self.incomingMessageObject.topic
            outgoingMessageObject.type = UTILS.Constants.fcGenericConstants.Response
            outgoingMessageObject.responseType = UTILS.Constants.fcFloggerConstants.S_END %self.incomingMessageObject.requestType
            outgoingMessageObject.replay = self.incomingMessageObject.replay
            outgoingMessageObject.expectedObjectCount = self._expectedObjectCount
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))

        if self._batchComplete > 0:
            '''----------------------------------------------------------------------------------------------------------
            Generate the response message to be send to the Collection ATSs.
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
            outgoingMessageObject.scopeName = self.incomingMessageObject.portfolioName
            outgoingMessageObject.scopeNumber = self.incomingMessageObject.portfolioNumber
            outgoingMessageObject.topic = self.incomingMessageObject.topic
            outgoingMessageObject.type = UTILS.Constants.fcGenericConstants.Response
            outgoingMessageObject.responseType = UTILS.Constants.fcGenericConstants.BatchEnd
            outgoingMessageObject.expectedObjectCount = self._expectedObjectCount
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))
