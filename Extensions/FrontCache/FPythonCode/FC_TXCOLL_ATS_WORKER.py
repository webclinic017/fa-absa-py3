
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_TCOLL_ATS_WORKER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module is the base module for Trade Collection ATSs. It will connect to the
                                AMB and prcess Trade Collection Requests. It will retreive the data from Front
                                Arena, save the data to the database and post reponse messages to the AMB.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_COLL_ATS_WORKER_BASE as COLL_ATS_WORKER_BASE
from FC_DATA_TRD_BUILDER_OPTIONS import FC_DATA_TRD_BUILDER_OPTIONS as  fcDataTradeBuilderOptions
import FC_ENUMERATIONS as ENUMERATIONS

import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_HELPER as DATA_HELPER
import FC_ENUMERATIONS
import acm
'''----------------------------------------------------------------------------------------------------------
Main Real Time ATS Worker Class. Contains the main Start, Stop and Work function for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_TXCOLL_ATS_WORKER(COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE):
    def __init__(self):
        COLL_ATS_WORKER_BASE.FC_COLL_ATS_WORKER_BASE.__init__(self)
        self._requestComplete = True
        self._batchComplete = None
        self.methodDict = {
            'Call 32 Day notice':DATA_HELPER.BuildAndSaveCallTx,
            'Call 7 Day notice':DATA_HELPER.BuildAndSaveCallTx,
            'Call Deposit':DATA_HELPER.BuildAndSaveCallTx,
            'Call Loan':DATA_HELPER.BuildAndSaveCallTx,
            'Call Deposit DTI':DATA_HELPER.BuildAndSaveCallTx,
            'Call Deposit NonDTI':DATA_HELPER.BuildAndSaveCallTx,
            'Call Loan DTI':DATA_HELPER.BuildAndSaveCallTx,
            'Call Loan NonDTI': DATA_HELPER.BuildAndSaveCallTx,
            'Call 48 Hour Notice':DATA_HELPER.BuildAndSaveCallTx,
            'Access Deposit Note 95d':DATA_HELPER.BuildAndSaveCallTx,
            'Access Deposit Note 95d Note 2':DATA_HELPER.BuildAndSaveCallTx,
            'Fixed Term Loan':DATA_HELPER.BuildAndSaveTermTx,
            'FDC':DATA_HELPER.BuildAndSaveTermTx,
            'FDE':DATA_HELPER.BuildAndSaveTermTx,
            'FDI':DATA_HELPER.BuildAndSaveTermTx,
            'FRD':DATA_HELPER.BuildAndSaveTermTx,
            'FRD Pre Payable 1M':DATA_HELPER.BuildAndSaveTermTx,
            'FRD Pre Payable 3M':DATA_HELPER.BuildAndSaveTermTx,
            'FTL':DATA_HELPER.BuildAndSaveTermTx,
            'FDI Access Deposit Note 370d':DATA_HELPER.BuildAndSaveTermTx,
            'FDI Access Deposit Note 95d':DATA_HELPER.BuildAndSaveTermTx,
            'FDC 7 Day Notice':DATA_HELPER.BuildAndSaveTermTx,
            'FDC 48 Hour Notice':DATA_HELPER.BuildAndSaveTermTx,
            'FDE 32 Day Notice':DATA_HELPER.BuildAndSaveTermTx
        }

    def isDeposit(self, objRef, numbers, requestType):
        try:
            UTILS.Logger.flogger.info('Checking if deposit')
            if requestType == 'INSTRUMENT_TRADES':
                isDeposit = acm.FInstrument[objRef].InsType() == 'Deposit'
                UTILS.Logger.flogger.info('Deposit %s' %str(isDeposit))
                return isDeposit
            elif len(numbers) > 0:
                isDeposit = acm.FTrade[numbers[0]].Instrument().InsType() == 'Deposit'
                UTILS.Logger.flogger.info('Deposit %s' % str(isDeposit))
                return isDeposit
        except:
            UTILS.Logger.flogger.info('Error in deposit check, returning false')
            return False

    def getFundingInsType(self, objRef, numbers, requestType):
        try:
            UTILS.Logger.flogger.info('Checking if fundinging insType for requestType (%s)' % requestType)
            if  'TRANSACTIONS' in requestType:
                try:
                    for trade in acm.FInstrument[objRef].Trades():
                        fInsType = trade.AdditionalInfo().Funding_Instype()
                        UTILS.Logger.flogger.info('Found funding ins type (%s)' % fInsType)
                        return fInsType
                except:
                    fInsType = acm.FTrade[numbers[0]].AdditionalInfo().Funding_Instype()
                    UTILS.Logger.flogger.info('Found funding ins type (%s)' % fInsType)
                    return fInsType
        except:
            return 'Invalid FundingInsType'

    def SaveData(self, requestId, reportDate, startIndex, numbers, buildControlMeasures, retryCount, requestType, scopeName):
        self._buildOptions =   fcDataTradeBuilderOptions()
        self._buildOptions.SerializationType = ENUMERATIONS.SerializationType.XML_COMPRESSED
        self._buildOptions.HistoricalCashflowRange = 5
        self._buildOptions.BuildControlMeasures = buildControlMeasures
        try:
            #if self.isDeposit(scopeName,numbers,requestType):
            self.methodDict[self.getFundingInsType(scopeName, numbers, requestType)](requestId, reportDate, startIndex, scopeName, numbers, self._buildOptions, retryCount)
                #return DATA_HELPER.BuildAndSaveCallTx(requestId, reportDate, startIndex, scopeName, self._buildOptions, retryCount)
            #else:
                #return DATA_HELPER.BuildAndSaveTermTx(requestId, reportDate, startIndex, numbers, self._buildOptions, retryCount)
            return ([0], '')
        except Exception, e:
            UTILS.Logger.flogger.info('Error (%s)' %str(e))
            return ([0], '')



    def processIncommingAMBAMessage(self):
        UTILS.Logger.flogger.info(UTILS.Constants.fcFloggerConstants.BATCH_I_OF_I_I_ITEMS % (self.incomingMessageObject.requestBatchNo, self.incomingMessageObject.requestBatchCount, self.incomingMessageObject.requestBatchTradeCount))

        self._expectedObjectCount = 0
        primaryKeyRange = self.incomingMessageObject.requestCollectionPrimaryKeys
        self._expectedObjectCount = len(primaryKeyRange)
        #In the case of a replay of a message we will need to use a new RequestId

        DATA_HELPER.RegisterMessageId(serviceComponentId=FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), messageId=self.currentMessageId, requestId=self.incomingMessageObject.requestId, retryCount=0)

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

        #if self.retryCount > 0:
        DATA_HELPER.RegisterMessageId(serviceComponentId=FC_ENUMERATIONS.ServiceComponent.fromstring(UTILS.ComponentName), messageId=self.currentMessageId, requestId=self.incomingMessageObject.requestId, retryCount=0)
        self.retryCount = 0

        if self.incomingMessageObject.requestType == "TRANSACTIONS_EOD":
            trackerResult = DATA_HELPER.SetRequestTrackerEnd(self.incomingMessageObject.requestId, processCount, errorCount,
                                                             self.incomingMessageObject.requestCollectionTrackerId,
                                                             self.incomingMessageObject.batchId, errors)

        DATA_HELPER.UpdateComponentQueueDepth(UTILS.ComponentName, -processCount) # Decrease queue

        return
#print FC_TXCOLL_ATS_WORKER.SaveData(1111, '2019-02-01', 0, '1231312-1321', 0, 5, 'INSTRUMENT_TRADES')
