""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTaskManagerDistributed.py"

# acm
import acm

# operations
from FOperationsTaskManager import TaskManager
from FOperationsTaskObserver import TaskObserver
from functools import reduce

#-------------------------------------------------------------------------
# TaskManagerDistributed - a manager of 0..m TaskObservers
#-------------------------------------------------------------------------
class TaskManagerDistributed(TaskManager):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        super(TaskManagerDistributed, self).__init__()

        # Task parameters
        self._name = configuration.name
        self._objectClass = configuration.objectClass
        self._taskName = configuration.taskName
        self._partitioner = configuration.partitioner
        self._messageCls = configuration.messageCls
        self._msgParams = configuration.parameters
        self._batchMode = configuration.batchMode

        self._nbrOfTasks = acm.OS.GetNumberOfCores()

        self._taskObservers = {}
        self._finishedTasks = {}

        # Result
        self._resultCls = configuration.resultCls
        self._result = self._resultCls()

    #-------------------------------------------------------------------------
    def Configuration(self):
        return {'Name' : self._name,
                'TaskName' : self._taskName,
                'Partitioner' : self._partitioner,
                'MessageCls' : self._messageCls,
                'MsgParams' : self._msgParams,
                'NbrTasks' : self._nbrOfTasks,
                'BatchMode' : self._batchMode,
                'ResultCls' : self._resultCls}

    #-------------------------------------------------------------------------
    def TM_Name(self):
        return self._name

    #-------------------------------------------------------------------------
    def TM_ObjectClass(self):
        return self._objectClass

    #-------------------------------------------------------------------------
    def TM_Destroy(self):
        self.OO_RemoveObservers()

        self._taskObservers.clear()
        self._finishedTasks.clear()
        self._result.TMR_Clear()

    #-------------------------------------------------------------------------
    def TM_Run(self, data):
        self.PrivateOnRun(data)

    #-------------------------------------------------------------------------
    def PrivateOnRun(self, data):
        partitions = self.PrivateCreatePartitions(data)

        if len(partitions):
            for partition in partitions:
                partitionKey = self._taskName + str(len(self._taskObservers))
                taskObserver = TaskObserver.Create(self._taskName, partitionKey, self._messageCls, self._msgParams, partition)
                taskObserver.OO_AddObserver(self)

                self._taskObservers[taskObserver.TO_ObserverId()] = taskObserver
                self._finishedTasks[taskObserver.TO_ObserverId()] = False

            if self._batchMode:
                self.__WhileNotFinished()
        else:
            self.OnFinished()

    #-------------------------------------------------------------------------
    def PrivateCreatePartitions(self, data):
        partitions = self._partitioner.PA_CreatePartitions(data, self._nbrOfTasks)
        return [part for part in partitions if part != []]

    #-------------------------------------------------------------------------
    # OperationsTaskManager:Events interface calls
    #-------------------------------------------------------------------------
    def OnOutput(self, msg):
        self.OO_NotifyObservers('TME_OnOutput', self.TM_Name(), msg)

    #-------------------------------------------------------------------------
    def OnFinished(self):
        self.OO_NotifyObservers('TME_OnFinished', self.TM_Name(), self._result)

    #-------------------------------------------------------------------------
    def OnResultLog(self, observerId, taskResult):
        self.OnOutput(taskResult.log.logMessage.encode('latin1'))

    #-------------------------------------------------------------------------
    def OnResult(self, observerId, taskResult):
        self._result.TMR_AddResult(taskResult)

        self._finishedTasks[observerId] = True

        self._taskObservers[observerId].TO_Destroy()

        if self.IsFinished():
            self.OnFinished()

    #-------------------------------------------------------------------------
    # OperationsTaskObserver:Events interface
    #-------------------------------------------------------------------------
    def TOE_OnResult(self, observerId, resultKey, resultEvent, taskResult):
        descriptor = resultKey.ResultType.DESCRIPTOR

        if(resultKey.resultType == descriptor.values_by_name['RT_LOG'].number):
            self.OnResultLog(observerId, taskResult)
        elif(resultKey.resultType == descriptor.values_by_name['RT_RESULT'].number):
            self.OnResult(observerId, taskResult)

    #-------------------------------------------------------------------------
    def TOE_OnDispatcherState(self, observerId, stateMsg):
        self.OnOutput('Dispatcher State called for {}: {}'.format(observerId, stateMsg))

    #-------------------------------------------------------------------------
    def TOE_OnTaskState(self, observerId, stateMsg):
        self.OnOutput('Task State called for {}: {}'.format(observerId, stateMsg))

    #-------------------------------------------------------------------------
    def TOE_OnProgress(self, observerId, progressText):
        self.OnOutput(progressText)

    #-------------------------------------------------------------------------
    # Workaround for not exiting early when running in batch mode
    #-------------------------------------------------------------------------
    def __WhileNotFinished(self):
        while not self.IsFinished():
            acm.PollAllEvents()
            acm.Sleep(20)

    #-------------------------------------------------------------------------
    def IsFinished(self):
        return reduce(lambda x, y: x and y, self._finishedTasks.values(), True)

