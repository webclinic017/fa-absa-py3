""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pace_runner/etc/FPaceAelTaskConsumer.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import FPaceConsumer
import uuid

def GetTaskDef(taskDefName):
    allTaskDefs = acm.GetDefaultContext().GetAllExtensions(acm.FPaceTaskDefinition, None, True, True, '', '')
    for taskDef in allTaskDefs:
        if taskDef.TaskName() == taskDefName:
            return taskDef     
    return None

class FPacePfeTaskConsumer(FPaceConsumer.Events):
    
    def __init__(self):
        self._taskDef = GetTaskDef("FrontArena.Pace.AelTaskPythonProducer")
        self._taskPbModule = __import__(self._taskDef.PythonTraitsModule())
        self._paceConsumer = None
        self._observer = None
        self._taskName = ""
        
    def SetObserver(self, observer):
        self._observer = observer
        
    def CreateTask(self, aelTaskName):
        if aelTaskName:
            self._taskName = aelTaskName
            self.__CreateTask(aelTaskName)
        else:
            self.__NotifyFail( "No Ael Task name specified." )
    
    def __CreateTask(self, aelTaskName):
        self.RemovePaceConsumer()
        taskMsg = self.__CreateTaskMessage(aelTaskName)
        self._paceConsumer = FPaceConsumer.Create(self._taskDef.TaskName(), taskMsg)
        self._paceConsumer.AddObserver(self)
        
    def __CreateTaskMessage(self, aelTaskName):
        if not self._taskPbModule:
            return None
        message = self._taskPbModule.Definition()
        message.taskName = aelTaskName
        return message
    
    def OnResultUpdated(self, resultKey, resultEvent, result):
        try:
            msg = self.__ParseResult(result)
            self.__NotifySuccess( msg )
        except Exception as e:
            self.__NotifyFail("Error: %s" % str(e))
        finally:
            self._taskName = ""
            self.RemovePaceConsumer()
    
    def __ParseResult(self, result):
        msg = 'Running task ' + self._taskName 
        
        if not result.success:
            msg += " is failed."
        else:
            msg += " is successed."
        
        if result.infoMsg != str("", "utf-8"): 
            msg += " Info: " + result.infoMsg
        
        if result.warningMsg != str("", "utf-8"): 
            msg += " Warning: " + result.warningMsg
        
        if result.errorMsg != str("", "utf-8"): 
            msg += " Error: " + result.errorMsg
        
        return msg
      
    def RemovePaceConsumer(self):
        if self._paceConsumer:
            self._paceConsumer.Destroy()
            self._paceConsumer = None
    
    def OnDispatcherState(self):
        self.__NotifyStatus(self._paceConsumer.StatusText())
    
    def __NotifySuccess(self, msg):
        if self._observer:
            self._observer.OnTaskSuccess(msg)
    
    def __NotifyFail(self, msg):
        if self._observer:
            self._observer.OnTaskFail(msg)
    
    def __NotifyStatus(self, msg):
        if self._observer:
            self._observer.OnTaskStatus(msg)
