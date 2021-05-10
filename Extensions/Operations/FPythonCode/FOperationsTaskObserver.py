""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTaskObserver.py"

# Pace consumer
import FPaceConsumer

# operations
from FOperationsObservable import Observable

#-------------------------------------------------------------------------
# TaskObserver - an observer of events from a FPaceConsumer
#-------------------------------------------------------------------------
class TaskObserver(FPaceConsumer.Events, Observable):
    
    #-------------------------------------------------------------------------
    class Events(object):
        
        def TOE_OnResult(self, observerId, resultKey, resultEvent, result):
            pass
        
        def TOE_OnDispatcherState(self, observerId, stateMsg):
            pass
        
        def TOE_OnTaskState(self, observerId, stateMsg):
            pass
        
        def TOE_OnProgress(self, observerId, progressText):
            pass

    #-------------------------------------------------------------------------
    def __init__(self, taskName, partitionKey, msgClass):
        super(TaskObserver, self).__init__()
        
        self._taskName = taskName
        self._partitionKey = partitionKey
        self._msgClass = msgClass
        self._paceConsumer = None
    
    #-------------------------------------------------------------------------    
    def TO_Destroy(self):
        self.OO_RemoveObservers()
        assert self._paceConsumer != None
        self._paceConsumer.Destroy()
        self._paceConsumer = None
        
    #-------------------------------------------------------------------------    
    def TO_ObserverId(self):
        assert self._paceConsumer != None
        return self._paceConsumer.ObserverId()
    
    #-------------------------------------------------------------------------
    def OnCreate(self, msgParams, partition):
        self.PrivateOnCreate(self._msgClass.MC_CreateMessage(msgParams, partition))
    
    #-------------------------------------------------------------------------    
    def PrivateOnCreate(self, definition):
        self._paceConsumer = FPaceConsumer.Create(self._taskName, definition, self._partitionKey)
        self._paceConsumer.AddObserver(self)
    
    #-------------------------------------------------------------------------
    # FPaceConsumer.Events interface
    #-------------------------------------------------------------------------    
    def OnResultUpdated(self, resultKey, resultEvent, result):  
        self.OO_NotifyObservers('TOE_OnResult', self.TO_ObserverId(), resultKey, resultEvent, result)
        
    #-------------------------------------------------------------------------
    def OnDispatcherState(self):
        dispatcherState = 'DispatcherState: ' + self._paceConsumer.DispatcherState().name + ' Status: ' + self._paceConsumer.StatusText()
        self.OO_NotifyObservers('TOE_OnDispatcherState', self.TO_ObserverId(), dispatcherState)
    
    #-------------------------------------------------------------------------
    def OnTaskState(self):
        taskState = 'TaskState: ' + self._paceConsumer.TaskState().name + ' Status: ' + self._paceConsumer.StatusText()
        self.OO_NotifyObservers('TOE_OnTaskState', self.TO_ObserverId(), taskState)
    
    #-------------------------------------------------------------------------
    def OnProgressUpdated(self, percent, progressText):
        self.OO_NotifyObservers('TOE_OnProgress', self.TO_ObserverId(), progressText)
    
    #-------------------------------------------------------------------------
    # Static method to create a task observer
    #-------------------------------------------------------------------------
    @staticmethod
    def Create(taskName, partitionKey, msgClass, msgParams, partition):
        taskObserver = TaskObserver(taskName, partitionKey, msgClass)
        taskObserver.OnCreate(msgParams, partition)
        return taskObserver
    