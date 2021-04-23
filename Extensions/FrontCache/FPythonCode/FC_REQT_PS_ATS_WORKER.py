
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_REQT_PS_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will receive a Portfolio Sensitivity Request. It will the send a
                                response to the response coordinating ATS detailing how many Portfolios are
                                expected. It will then send a Request to the Portfolio Sensitivity Collection
                                ATSs to retreive the trade detail.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom modules
----------------------------------------------------------------------------------------------------------'''
import FC_REQT_ATS_WORKER_BASE as REQT_ATS_WORKER_BASE
import FC_DATA_HELPER as DATA_HELPER
import FC_UTILS as FC_UTILS
from FC_DATA_SELECTION import FC_DATA_SELECTION as DATA_SELECTION
from FC_UTILS import FC_UTILS as UTILS
import FC_ENUMERATIONS
import acm
import time
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_REQT_PS_ATS_WORKER(REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE):
    def __init__(self):
        REQT_ATS_WORKER_BASE.FC_REQT_ATS_WORKER_BASE.__init__(self)

    def GetControlMeasureAttribute(self):
        return UTILS.Parameters.fcComponentParameters.componentControlMeasureFlag

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
        trade_count = acm.FPhysicalPortfolio[self.incomingMessageObject.scopeNumber].Trades().Size()
        if dataSelection:
            self._expectedObjectCount = trade_count
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.S_TRADES_FOUND % (int(self._expectedObjectCount)) )
        
        DATA_HELPER.SetRequestTrackerStart(int(self.incomingMessageObject.requestId), self._expectedObjectCount)

        self.incomingMessageObject.requestBatchCount = 0

        self.incomingMessageObject.requestBatchCount = self.incomingMessageObject.requestBatchCount + 1
        requestBatchNo = self.incomingMessageObject.requestBatchCount
        requestBatchStartIndex, requestBatchEndIndex = (0, 1)
        requestBatchTradeCount = trade_count
            
        dataSelectionList = dataSelection[requestBatchStartIndex:requestBatchEndIndex + 1]
        requestCollectionPrimaryKeys = ','.join(map(str, dataSelectionList))

        collectionRequestMessage = UTILS.Parameters.fcComponentParameters.componentCollectionRequestMessageSubject
        isRT = self.incomingMessageObject.isEOD == 0

        heartbeatComponent = None
        dbRetryCount = 0
        while (heartbeatComponent is None) and dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                heartbeatComponent = DATA_HELPER.GetHeartbeatCandidateComponent(collectionRequestMessage, requestBatchTradeCount, isRT)
                if heartbeatComponent is None:
                    raise RuntimeError, 'HearbeatComponent is None'
            except Exception, e:
                dbRetryCount += 1
                time.sleep(UTILS.Parameters.fcGenericParameters.HeartbeatTrackInterval)

        if heartbeatComponent == None:
            UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.HEARTBEAT_COMPONENT_IS_NONE)
            UTILS.Logger.flogger.info("Cannot find heartbeat candidate component, ats will restart.")
            self.RestartAts()
        
        if heartbeatComponent in self._componentSubscriptionSubjects:
             UTILS.SenderSubject = self._componentSubscriptionSubjects[heartbeatComponent]
        else:
             UTILS.SenderSubject = FC_UTILS.GetSenderSubject(heartbeatComponent)
             self._componentSubscriptionSubjects[heartbeatComponent] = UTILS.SenderSubject

        tradeNumbers = ','.join(str(x) for x in dataSelectionList)
        #Create request tracker with the expected count
        requestCollectionTrackerId = self._requestCollectionTrackerRepository.createRequestCollectionTracker(
            int(self.incomingMessageObject.requestId), UTILS.ComponentName, heartbeatComponent, requestBatchNo, 1,
            requestBatchStartIndex, requestBatchEndIndex, requestBatchTradeCount, tradeNumbers, False)

        self._batchesToSend.append((requestBatchNo,
                                    requestBatchStartIndex,
                                    requestBatchEndIndex,
                                    requestBatchTradeCount,
                                    requestCollectionTrackerId,
                                    requestCollectionPrimaryKeys,
                                    UTILS.SenderSubject))
            
        return

    def registerMessageId(self):
        return
