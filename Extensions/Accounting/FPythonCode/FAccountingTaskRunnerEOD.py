""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskRunnerEOD.py"

# core
import acm, time

# operations
from FOperationsTaskRunnerBase import TaskRunnerBase
from FOperationsTaskPartitioner import MethodChainPartitioner
from FOperationsTaskConfiguration import Configuration
from FOperationsTaskManagerDistributed import TaskManagerDistributed

# accounting
from FAccountingTaskManagerClassic import AccountingTaskManagerClassic
from FAccountingTaskMessages import AccountingTaskMessage
from FAccountingTaskRunnerResult import AccountingTaskRunnerResult
from FAccountingTaskManagerResult import AccountingTaskManagerResult
from FAccountingTaskManagerResultClassic import AccountingTaskManagerResultClassic

import FAccountingEngineBaseCreator as Engines


#-------------------------------------------------------------------------
class AccountingTaskRunnerEOD(TaskRunnerBase):

    #-------------------------------------------------------------------------
    TRADE = 0
    SETTLEMENT = 1

    #-------------------------------------------------------------------------
    def __init__(self, logger, eodParams, engineParams, batchMode):
        super(AccountingTaskRunnerEOD, self).__init__(logger, AccountingTaskRunnerResult())

        self._books = eodParams['books']
        self._runTradeEOD = eodParams['runTradeEOD']
        self._runSettlementEOD = eodParams['runSettlementEOD']
        self._runDistributed = eodParams['runDistributed']
        self._afterMidnight = eodParams['afterMidnight']
        self._processDate = eodParams['processDate']
        self._updateProcessDate = eodParams['updateProcessDate']

        self._nbrTradesProcessed = 0
        self._nbrSettlementsProcessed = 0
        self._engineParams = engineParams

        self._batchMode = batchMode

    #-------------------------------------------------------------------------
    def TR_OnStart(self):
        self._logger.LP_Log('Accounting EOD started by user {} at {}. afterMidnight flag is {}'.format(str(acm.UserName()), time.ctime(), str(self._afterMidnight)))
        self._logger.LP_Flush()

    #-------------------------------------------------------------------------
    def TR_OnProcessedFailedData(self):
        self._logger.LP_Log('Post-processing objects due to synchronization dependencies.')
        self._logger.LP_Flush()

        failedObjects = self.TR_Result().TRR_FailedData().copy()

        self.TR_OnCreate(self.CreateConfigurations(AccountingTaskManagerClassic))

        for tmID, objIds in failedObjects.items():
            objClass = self.TR_TaskManagerObjectClass(tmID)
            objects = [objClass[objId] for objId in objIds]
            self.TR_Run(tmID, objects)

    #-------------------------------------------------------------------------
    def TR_OnFinished(self):
        self.__PostProcessing()

        self._logger.LP_Log('Accounting EOD finished at {}.'.format(time.ctime()))
        self._logger.LP_Log('{} trades were processed and considered for journal creation.'.format(self._nbrTradesProcessed))
        self._logger.LP_Log('{} settlements were processed and considered for journal creation.'.format(self._nbrSettlementsProcessed))
        self._logger.LP_Log('{} journals were created.'.format(self.TR_Result().ATRR_Created()))
        self._logger.LP_Log('{} journals were updated.'.format(self.TR_Result().ATRR_Updated()))
        self._logger.LP_Log('{} transactions failed to commit.'.format(self.TR_Result().ATRR_Exceptions()))
        self._logger.LP_Flush()

    #-------------------------------------------------------------------------
    def CreateConfigurations(self, instanceClass = None):
        configurations = []

        instanceClass = instanceClass if instanceClass else self.InstanceClass()

        if self._runTradeEOD:

            configuration = {}
            engineParams = self._engineParams.copy()
            engineParams['targetClass'] = AccountingTaskRunnerEOD.TRADE

            partitionExtension = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FTrade', 'AccountingPartitionKey')
            idFunction = lambda obj: obj.Oid()
            configuration['partitioner'] = MethodChainPartitioner(partitionExtension, idFunction)

            configuration['name'] = 'Trade'
            configuration['objectClass'] = acm.FTrade
            configuration['taskName'] = 'FrontArena.Accounting'
            configuration['messageCls'] = AccountingTaskMessage
            configuration['parameters'] = engineParams
            configuration['createEngineCb'] = Engines.CreateEngineForTrades
            configuration['resultCls'] = AccountingTaskManagerResult if instanceClass == TaskManagerDistributed else AccountingTaskManagerResultClassic
            configuration['batchMode'] = self._batchMode
            configurations.append((instanceClass, Configuration(configuration)))

        if self._runSettlementEOD:

            configuration = {}
            engineParams = self._engineParams.copy()
            engineParams['targetClass'] = AccountingTaskRunnerEOD.SETTLEMENT

            partitionExtension = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FSettlement', 'AccountingPartitionKey')
            idFunction = lambda obj: obj.Oid()
            configuration['partitioner'] = MethodChainPartitioner(partitionExtension, idFunction)

            configuration['name'] = 'Settlement'
            configuration['objectClass'] = acm.FSettlement
            configuration['taskName'] = 'FrontArena.Accounting'
            configuration['messageCls'] = AccountingTaskMessage
            configuration['parameters'] = engineParams
            configuration['createEngineCb'] = Engines.CreateEngineForSettlements
            configuration['resultCls'] = AccountingTaskManagerResult if instanceClass == TaskManagerDistributed else AccountingTaskManagerResultClassic
            configuration['batchMode'] = self._batchMode
            configurations.append((instanceClass, Configuration(configuration)))

        return configurations

    #-------------------------------------------------------------------------
    def CreateRequests(self):
        requests = {}

        if self._runTradeEOD:
            trades = Engines.CreateTradeFilter().GetObjects()
            self._logger.LP_Log('Found {} trades that will be considered for accounting processing.'.format(len(trades)))
            self._logger.LP_Flush()
            self._nbrTradesProcessed = len(trades)
            requests['Trade'] = trades

        if self._runSettlementEOD:
            settlements = Engines.CreateSettlementFilter().GetObjects()
            self._logger.LP_Log('Found {} settlements that will be considered for accounting processing.'.format(len(settlements)))
            self._logger.LP_Flush()
            self._nbrSettlementsProcessed= len(settlements)
            requests['Settlement'] = settlements

        return requests

    #-------------------------------------------------------------------------
    def InstanceClass(self):
        if self._runDistributed:
            return TaskManagerDistributed
        else:
            return AccountingTaskManagerClassic

    #-------------------------------------------------------------------------
    def __PostProcessing(self):
        self.__UpdateAccountingPeriods()

        if self._updateProcessDate:
            self.__UpdateBooks()

    #-------------------------------------------------------------------------
    def __UpdateBooks(self):
        self._logger.LP_Log('Updating processdate on accounting books...')

        for book in self._books:
            try:
                book.ProcessDate(self._processDate)
                book.Commit()
            except Exception as e:
                self._logger.LP_Log('Failed to update processdate on book {}: {}'.format(book.Name(), str(e)))

        self._logger.LP_Flush()

    #-------------------------------------------------------------------------
    def __UpdateAccountingPeriods(self):
        self._logger.LP_Log('Updating hasjournals on accounting periods...')

        query = "status = {} hasJournals = {}".format('\'Open\'', False)
        accountingPeriods = [accountingPeriod for accountingPeriod in acm.FAccountingPeriod.Select(query)]

        for accPeriod in accountingPeriods:

            if accPeriod.Book() in self._books and len(accPeriod.Journals()) > 0:
                try:
                    accPeriod.HasJournals(True)
                    accPeriod.Commit()
                except Exception as e:
                    self._logger.LP_Log('Failed to update hasjournals on accounting period {}: {}'.format(accPeriod.Name(), str(e)))

        self._logger.LP_Flush()

    #-------------------------------------------------------------------------
    @staticmethod
    def CreateAndRun(logger, eodParams, engineParams):
        runner = AccountingTaskRunnerEOD(logger, eodParams, engineParams, not acm.IsSessionUserInteractive())
        runner.TR_OnCreate(runner.CreateConfigurations())

        for tmID, objects in runner.CreateRequests().items():
            runner.TR_Run(tmID, objects)
