""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskProducer.py"
# acm
import acm

# Pace Core Producer
import FPaceProducer

# operations
from FOperationsLoggers import ProxyLogger
from FOperationsQueries import CreateFilter

# accounting
from FAccountingEngineBaseCreator import CreateEngineForTrades, CreateEngineForSettlements, CreateParameters
from FAccountingOperations import Operation


#-------------------------------------------------------------------------
def CreateProducer():
    return Producer()

#-------------------------------------------------------------------------
class Producer(FPaceProducer.Producer):

    engineCbByType = {0 : CreateEngineForTrades,
                      1 : CreateEngineForSettlements}

    objClassbyType = {0 : acm.FTrade,
                      1 : acm.FSettlement}

    #-------------------------------------------------------------------------
    class TaskInstance(object):

        refreshInterval = 0.25

        #-------------------------------------------------------------------------
        @staticmethod
        def IsSupportedObjCb(obj):
            if  obj.IsKindOf(acm.FJournal) or \
                obj.IsKindOf(acm.FJournalLink) or \
                obj.IsKindOf(acm.FJournalInformation):
                return True
            return False

        #-------------------------------------------------------------------------
        def __init__(self, taskId, definition, producer):
            super(Producer.TaskInstance, self).__init__()

            self._taskId = taskId
            self._producer = producer
            self._partitionSize = 10

            self._created = 0
            self._updated = 0
            self._exceptions = 0
            self._failedObjects = list()

            self._objClass = Producer.objClassbyType[definition.targetClass]
            self._partitions = self.__CreatePartitions(definition.objIds)
            self._numOfPartitions = len(self._partitions)
            self._engine = self.__CreateEngine(definition)

        #-------------------------------------------------------------------------
        def Clear(self):
            self._created = 0
            self._updated = 0
            self._exceptions = 0
            del self._failedObjects[:]

        #-------------------------------------------------------------------------
        def Destroy(self):
            self._engine.ClearCalculations()
            self._engine.ClearProcessedPositions()

        #-------------------------------------------------------------------------
        def GenerateAndSendResults(self):
            partition = self._partitions.pop() if len(self._partitions) else None

            if partition:
                self.OnProcessPartition(partition)
                if self.__EligibleToClearCalculations(len(self._partitions), self._numOfPartitions):
                    self._engine.ClearCalculations()
            else:
                self.OnFinished()

        #-------------------------------------------------------------------------
        def OnFinished(self):
            self._producer.OnFinishedTask(self._taskId)
            self.OnGenerateResultLog("INFO: Task with taskId {} finished.".format(self._taskId))
            self.OnGenerateResultStatistics()
            self.Clear()

        #-------------------------------------------------------------------------
        def OnGenerateResultLog(self, msg):
            resultKey = self._producer.Traits().ResultKey()
            result = self._producer.Traits().Result()
            resultTypeDescriptor = resultKey.ResultType.DESCRIPTOR

            resultKey.resultType = resultTypeDescriptor.values_by_name['RT_LOG'].number
            result.log.logMessage = msg.decode('latin1')

            self._producer.SendInsertOrUpdate(self._taskId, resultKey, result)

        #-------------------------------------------------------------------------
        def OnGenerateResultStatistics(self):
            resultKey = self._producer.Traits().ResultKey()
            result = self._producer.Traits().Result()
            resultTypeDescriptor = resultKey.ResultType.DESCRIPTOR

            resultKey.resultType = resultTypeDescriptor.values_by_name['RT_RESULT'].number

            result.result.created = self._created
            result.result.updated = self._updated
            result.result.exceptions = self._exceptions
            result.result.objIds.extend(self._failedObjects)

            self._producer.SendInsertOrUpdate(self._taskId, resultKey, result)

        #-------------------------------------------------------------------------
        def OnProcessPartition(self, partition):
            try:
                objects = [self._objClass[oid] for oid in partition]

                engineResult = self._engine.Process(objects)

                self._created += engineResult.RE_ResultOpAndObjectType(Operation.CREATE, 'FJournal')
                self._updated += engineResult.RE_ResultOpAndObjectType(Operation.UPDATE, 'FJournal')
                self._exceptions += len(engineResult.RE_Exceptions())
                self._failedObjects.extend(engineResult.RE_FailedObjects())

            except Exception as e:
                self.OnGenerateResultLog('ERROR: Exception caught when executing accounting task and partition {}: {}'.format(str(partition), str(e)))

        #-------------------------------------------------------------------------
        def __CreateEngine(self, definition):
            import FAccountingParams as Params
            engineCb = Producer.engineCbByType[definition.targetClass]

            params = self.__CreateParameters(definition)
            logger = ProxyLogger(Params.detailedLogging, self.OnGenerateResultLog)
            isSupportedObjCb = Producer.TaskInstance.IsSupportedObjCb

            return engineCb(params, logger, None, isSupportedObjCb)

        #-------------------------------------------------------------------------
        def __CreateParameters(self, definition):
            startDate = definition.startDate.encode('utf-8')
            endDate = definition.endDate.encode('utf-8')
            endOfDayDate = definition.endOfDayDate.encode('utf-8')
            processDate = definition.processDate.encode('utf-8')

            bookFilter = None
            if len(definition.bookIds):
                bookFilter = CreateFilter(acm.FBook, 'OR', 'Oid', definition.bookIds, 'EQUAL')

            bookLinkFilter = None
            if len(definition.treatmentIds):
                bookLinkFilter = CreateFilter(acm.FBookLink, 'OR', 'Treatment.Oid', definition.treatmentIds, 'EQUAL')

            treatmentLinkFilter = None
            if len(definition.aiIds):
                treatmentLinkFilter = CreateFilter(acm.FTreatmentLink, 'OR', 'AccountingInstruction.Oid', definition.aiIds, 'EQUAL')

            return CreateParameters(startDate, endDate, endOfDayDate, processDate, bookFilter, bookLinkFilter, treatmentLinkFilter)

        #-------------------------------------------------------------------------
        def __CreatePartitions(self, objIds):
            return [objIds[i:i+self._partitionSize] for i in range(0, len(objIds), self._partitionSize)]

        #-------------------------------------------------------------------------
        def __EligibleToClearCalculations(self, entitiesLeft, totalEntities):
            eligible = False

            if entitiesLeft:
                prevScore = (float(entitiesLeft + 1)/float(totalEntities)) % Producer.TaskInstance.refreshInterval
                nextScore = (float(entitiesLeft - 1)/float(totalEntities)) % Producer.TaskInstance.refreshInterval
                currScore = (float(entitiesLeft)/float(totalEntities)) % Producer.TaskInstance.refreshInterval

                if currScore < prevScore and entitiesLeft + 1 != totalEntities and currScore < nextScore:
                    eligible = True

            return eligible

    #-------------------------------------------------------------------------
    def __init__(self):
        super(Producer, self).__init__()
        self._taskInstances = {}
        self._runningTasks = []

    #-------------------------------------------------------------------------
    def OnCreateTask(self, taskId, definition):
        try:
            taskInstance = Producer.TaskInstance(taskId, definition, self)
            self._taskInstances[taskId] = taskInstance
            self._runningTasks.append(taskId)

        except Exception as e:
            acm.Log('ERROR: Exception occurred when creating task: {}'.format(str(e)))

    #-------------------------------------------------------------------------
    def OnDoPeriodicWork(self):
        taskId = self._runningTasks[0] if len(self._runningTasks) else None

        if taskId:
            taskInstance = self._taskInstances[taskId]
            taskInstance.GenerateAndSendResults()

    #-------------------------------------------------------------------------
    def OnFinishedTask(self, taskId):
        self._runningTasks.remove(taskId)

    #-------------------------------------------------------------------------
    def OnDestroyTask(self, taskId):
        task = self._taskInstances.pop(taskId)

        if task:
            task.Destroy()
