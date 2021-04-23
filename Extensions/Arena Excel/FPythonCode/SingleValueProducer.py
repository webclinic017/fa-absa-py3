""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/SingleValueProducer.py"
import FPaceProducer
import SingleValueTask

import traceback
import threading


def CreateProducer():	
    return SingleValueProducer()


class SingleValueProducer(FPaceProducer.Producer):

    def __init__(self):
        super(SingleValueProducer, self).__init__()
        self.taskByTaskId = {}
        self.taskDefinitionByTaskId = {}
        self.lock = threading.Lock()
        
    """Inherited from FPaceProducer.Producer"""
    def OnDoPeriodicWork(self):
        if self.lock.acquire(False):
            self.InitTasks()
            self.DoPeriodicTaskWork()
            self.lock.release()
        
    """Inherited from FPaceProducer.Producer"""
    def OnCreateTask(self, taskId, definition): 
        self.taskDefinitionByTaskId[taskId] = definition

    """Inherited from FPaceProducer.Producer"""
    def OnDestroyTask(self, taskId):
        if self.taskByTaskId.has_key(taskId):
            task = self.taskByTaskId.pop(taskId)
            try:
                task.Destroy()
            except Exception as err:
                self.SendException(taskId, traceback.format_exc())
                
    def InitTasks(self):
        for taskId in self.taskDefinitionByTaskId.keys():
            try:
                definition = self.taskDefinitionByTaskId.pop(taskId)
                task = SingleValueTask.Task(self, taskId, definition)
                self.taskByTaskId[taskId] = task
            except Exception as err:
                self.SendException(taskId, traceback.format_exc())
                
    def DoPeriodicTaskWork(self):
        for taskId, task in self.taskByTaskId.iteritems():
            try:
                task.OnDoPeriodicWork()
            except Exception as err:
                self.SendException(taskId, traceback.format_exc())
                del self.taskByTaskId[taskId]
