
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_PSCOLL_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for Portfolio Sensitivity Collection ATSs. It
                                will connect to the AMB and prcess Portfolio Sensitivity Collection Requests.
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
from FC_DATA_SEN_BUILDER_OPTIONS import FC_DATA_SEN_BUILDER_OPTIONS as  fcDataSensitivityBuilderOptions
from FC_UTILS import FC_UTILS as UTILS
import FC_UTILS

'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_PSCOLL_ATS_WORKER(COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE):
    def __init__(self):
        COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE.__init__(self)
        self._sensitivityType = UTILS.Constants.fcGenericConstants.PORTFOLIO

    def SaveData(self, requestId, reportDate, startIndex, numbers, buildControlMeasures, retryCount, requestType, scopeName):
        self._buildOptions =   fcDataSensitivityBuilderOptions()
        self._buildOptions.SerializationType = ENUMERATIONS.SerializationType.PROTOBUF
        self._buildOptions.HistoricalCashflowRange = 5
        return DATA_HELPER.BuildAndSaveSensitivities(requestId,
                                                     reportDate,
                                                     startIndex,
                                                     numbers,
                                                     self._buildOptions,
                                                     self._sensitivityType)

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
        processCount = self.incomingMessageObject.requestBatchTradeCount
        errorCount = 0
        chunkCheckerResult = 0
        if self.incomingMessageObject.replay == 'False':
            chunkCheckerResult = DATA_HELPER.CheckChunkHasCompleted(self.incomingMessageObject.requestCollectionTrackerId)

        # Check if the chunk to be processed has already been completed                
        if chunkCheckerResult == 0:                
            (staticIds, errors) = self.SaveData(self.incomingMessageObject.requestId,
                                                self.incomingMessageObject.reportDate,
                                                self.incomingMessageObject.requestBatchStartIndex,
                                                self.incomingMessageObject.scopeNumber,
                                                self.incomingMessageObject.buildControlMeasures, self.retryCount,
                                                self.incomingMessageObject.requestType,
                                                self.incomingMessageObject.scopeName)

            errorCount = len(errors)
            if errorCount > 0:
                UTILS.Logger.flogger.critical(errors)
        else:
            (staticIds, errors) = ([0], '')        

        if processCount > 0:
            DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -processCount) # Decrease queue
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
        UTILS.Parameters.fcGenericParameters.RestartAfterWork = True
        return
