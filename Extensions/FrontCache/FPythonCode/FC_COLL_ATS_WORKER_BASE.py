'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_COLL_ATS_WORKER_BASE
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for  Collection ATSs. It will connect to the
                                AMB and prcess  Collection Requests. It will retreive the data from Front
                                Arena, save the data to the database and post reponse messages to the AMB.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''
'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_UTILS 
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_HELPER as DATA_HELPER
import FC_ATS_WORKER_BASE as ATS_WORKER_BASE
import FC_ERROR_HANDLER_DEFAULT as ERROR_HANDLER_DEFAULT
from FC_MESSAGE_PROCESS_REQUEST import FC_MESSAGE_PROCESS_REQUEST as MESSAGE_PROCESS_REQUEST
from FC_MESSAGE_OBJECT_REQUEST import FC_MESSAGE_OBJECT_REQUEST as MESSAGE_OBJECT_REQUEST
from FC_MESSAGE_OBJECT_RESPONSE import FC_MESSAGE_OBJECT_RESPONSE as MESSAGE_OBJECT_RESPONSE
from FC_CALCULATION_SINGLETON import FC_CALCULATION_SINGLETON as CALCULATION_SINGLETON
from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as ENVIRONMENT
import FC_ENUMERATIONS

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_COLL_ATS_WORKER_BASE(ATS_WORKER_BASE.FC_ATS_WORKER_BASE):
    def _init_(self):
        ATS_WORKER_BASE.FC_ATS_WORKER_BASE._init_(self)
        self._expectedObjectCount = None
        self._requestComplete = None
        self._batchComplete = None

    def getLastProcessedMessageId(self):
        self.last_processed_messageId, self.requestId, self.retryCount = DATA_HELPER.GetLastProcessedMessageInfo(FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName))

    def mapIncomingAMBAMessageToIncomingMessageObject(self):
        '''----------------------------------------------------------------------------------------------------------
        The AMBA message will be validated and an IncomingMessageObject will be created which will contain all
        detail needed to process the incoming message further.
        ----------------------------------------------------------------------------------------------------------'''
        self.incomingMessageObject = MESSAGE_OBJECT_REQUEST()

        MESSAGE_PROCESS_REQUEST(self.incomingAMBAMessageData, self.incomingMessageObject)
    
    def SaveData(self, requestId, reportDate, startIndex, numbers, retryCount=0, requestType=0, scopeName=None):
        raise Exception(UTILS.Constants.fcExceptionConstants.SAVE_DATA_NOT_IMPLEMENTED_ERROR)

        
    def processIncommingAMBAMessage(self):
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_I_OF_I_I_ITEMS % (self.incomingMessageObject.requestBatchNo, self.incomingMessageObject.requestBatchCount, self.incomingMessageObject.requestBatchTradeCount))

        # If the ats historical date is not equal to the reportdate then the registry will be updated and the ats restarted to
        # process the message correctly
        if str(self.incomingMessageObject.isDateToday) == "1" and FC_UTILS.RestartAtsForDateToday(FC_UTILS.dateStringFromDateTimeString(FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)), FC_UTILS.Ats_service_name, FC_UTILS.DateToday):
            UTILS.Logger.flogger.info("Ats is not the correct date_today. Ats will update registry and restart")
            self.RestartAts()
        elif str(self.incomingMessageObject.isDateToday) == "0" and FC_UTILS.RestartAtsForHistoricalDate(FC_UTILS.dateStringFromDateTimeString(FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)), FC_UTILS.Ats_service_name, FC_UTILS.HistoricalDate):
            UTILS.Logger.flogger.info("Ats is not the correct historical date. Ats will update registry and restart")
            self.RestartAts()

        self._expectedObjectCount = 0
        primaryKeyRange = self.incomingMessageObject.requestCollectionPrimaryKeys
        self._expectedObjectCount = len(primaryKeyRange)
        #In the case of a replay of a message we will need to use a new RequestId
        chunkCheckerResult = DATA_HELPER.CheckChunkHasCompleted(self.incomingMessageObject.requestCollectionTrackerId)
        if (self.last_processed_messageId == self.currentMessageId):
            UTILS.Logger.flogger.info("Ats is attempting to reprocess amb messageId %s" % self.currentMessageId)
            UTILS.Logger.flogger.info("Ats will enter into recovery mode for the trade numbers")
            self._recovery_mode = True  # Recover from the items already created
        # Check if the chunk to be processed has already been completed
        else:
            DATA_HELPER.RegisterMessageId(serviceComponentId=FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), messageId=self.currentMessageId, requestId=self.incomingMessageObject.requestId, retryCount=0)

        processCount = 0
        errorCount = 0
        (staticIds, errors) = ([0], '')
        if chunkCheckerResult == 0:
            #Check here if trades may already exist in the db if in recovery_mode
            if self._recovery_mode is True and len(primaryKeyRange)> 0 and DATA_HELPER.CheckIfTradesExistForRequestId(
                    self.incomingMessageObject.requestId, primaryKeyRange, FC_UTILS.dateTimeStringFromISODateTimeString(self.incomingMessageObject.reportDate)) is True:
                processCount = DATA_HELPER.GetProcessedCountForRequestCollectionTrackerId(self.incomingMessageObject.requestCollectionTrackerId)
                if processCount > 0: processCount = 0 # Prevent messing up the requestTracker processedCount
                else: processCount = len(primaryKeyRange) # Correct the requestTracker processedCount
                errorCount = 0
            else:
                DATA_HELPER.UpdateRequestCollectionStart(self.incomingMessageObject.requestId, self.incomingMessageObject.requestBatchStartIndex)
                (staticIds, errors) = self.SaveData(self.incomingMessageObject.requestId,
                                                    self.incomingMessageObject.reportDate,
                                                    self.incomingMessageObject.requestBatchStartIndex, primaryKeyRange,
                                                    self.incomingMessageObject.buildControlMeasures, self.retryCount,
                                                    self.incomingMessageObject.requestType,
                                                    self.incomingMessageObject.scopeName)
                processCount = len(staticIds)
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

                DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -processCount) # Decrease queue
        '''----------------------------------------------------------------------------------------------------------
        Trade batch complete, update the request tracker
        ----------------------------------------------------------------------------------------------------------'''
        trackerResult = DATA_HELPER.SetRequestTrackerEnd(self.incomingMessageObject.requestId, processCount, errorCount,
                                                         self.incomingMessageObject.requestCollectionTrackerId,
                                                         self.incomingMessageObject.batchId, errors)

        self._requestComplete = self.isRequestComplete(trackerResult)
        self._batchComplete = self.isBatchComplete(trackerResult)

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.REQUEST_COMPLETE_S %str(self._requestComplete))
        if self._requestComplete > 0:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.PROCESSED_I_ERRORS % (self.incomingMessageObject.requestBatchNo, processCount, errorCount))
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.COMPLETE_RESPONSE)

        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_COMPLETE_S %str(self._batchComplete))
        if self._batchComplete > 0:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_COMPLETE_RESPONSE \
                                      % int(self.incomingMessageObject.batchId))

        if self._requestComplete == 0 and self._batchComplete == 0:
            UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.PROCESSED_I_ERRORS % (self.incomingMessageObject.requestBatchNo, processCount, errorCount))

        '''----------------------------------------------------------------------------------------------------------
        Clear Calc Space Worksheets.
        ----------------------------------------------------------------------------------------------------------'''
        for workSheetName in CALCULATION_SINGLETON.Instance().worksheetCalcSpaces:
            try:
                CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[workSheetName].Clear()
            except Exception, e:
                raise Exception(UTILS.Constants.fcFloggerConstants.THE_FOLLOWING_ERROR_S % (workSheetName, str(e)))
        
        return

    def isRequestComplete(self, trackerResultInput):
        return int(trackerResultInput[0])

    def isBatchComplete(self, trackerResultInput):
        return int(trackerResultInput[1])

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
            outgoingMessageObject.scopeName = self.incomingMessageObject.scopeName
            outgoingMessageObject.scopeNumber = self.incomingMessageObject.scopeNumber
            outgoingMessageObject.topic = self.incomingMessageObject.topic
            outgoingMessageObject.type = UTILS.Constants.fcGenericConstants.Response
            outgoingMessageObject.responseType = UTILS.Constants.fcFloggerConstants.S_END %self.incomingMessageObject.requestType
            outgoingMessageObject.replay = self.incomingMessageObject.replay
            outgoingMessageObject.expectedObjectCount = self._expectedObjectCount
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))   

        if self._batchComplete > 0:
            '''----------------------------------------------------------------------------------------------------------
            Get failed independent selection portfolios and send email notification
            ----------------------------------------------------------------------------------------------------------'''
            try:
            
                results = DATA_HELPER.getInvalidTradePortfolioCounts(self.incomingMessageObject.reportDate, self.incomingMessageObject.batchId)
                results = [int(result[0]) for result in results]
                if results:
                    warnInf = 'Book Id(s) with possible issues - {}'.format(results)
                    subj = '%s FrontCache Warning - Portfolio trade selection issue detected' % ENVIRONMENT.environment_name
                    batchId = self.incomingMessageObject.batchId
                    requestId = self.incomingMessageObject.requestId
                    dateString = FC_UTILS.dateStringFromDateTimeString(outgoingMessageObject.reportDate)
                    batchTopic = self.incomingMessageObject.topic
                    warn = 'Warning'
                    warnGroup = 'WarningEmailNotificationGroup'
                    msgEod = 'Possible missing trades in EOD Batch'
                    msgPrf = 'Portfolio trade selection issue detected' 
                    ERROR_HANDLER_DEFAULT.handle(warn, subj, warnGroup, batchId, requestId, dateString, batchTopic, warnInf, msgEod, msgPrf)
            except Exception as e:
                UTILS.Logger.flogger.info('Unable to reach smtp server: {}'.format(e))
                
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
            outgoingMessageObject.topic = self.incomingMessageObject.topic
            outgoingMessageObject.type = UTILS.Constants.fcGenericConstants.Response
            outgoingMessageObject.responseType = UTILS.Constants.fcGenericConstants.BatchEnd
            outgoingMessageObject.expectedObjectCount = self._expectedObjectCount
            self.outgoingAMBADataDictionaries.append((outgoingMessageObject.type, outgoingMessageObject.mapMessageObjectToAMBADataDictionary()))
