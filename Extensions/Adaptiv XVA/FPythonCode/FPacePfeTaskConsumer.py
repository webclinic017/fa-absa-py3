""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/FPacePfeTaskConsumer.py"
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
        self._taskDef = GetTaskDef("FrontArena.Pace.PfePythonProducer")
        self._taskPbModule = __import__(self._taskDef.PythonTraitsModule())
        self._paceConsumer = None
        self._observer = None
    
    def SetObserver(self, observer):
        self._observer = observer
        
    def CreateTask(self, trdnbr):
        if trdnbr:
            self.__CreateTask(trdnbr)
        else:
            self.__NotifyFail( "The trade has to be saved." )
    
    def __CreateTask(self, trdnbr):
        self.RemovePaceConsumer()
        taskMsg = self.__CreateTaskMessage(trdnbr)
        self._paceConsumer = FPaceConsumer.Create(self._taskDef.TaskName(), taskMsg)
        self._paceConsumer.AddObserver(self)
        
    def __CreateTaskMessage(self, trdnbr):
        if not self._taskPbModule:
            return None
        message = self._taskPbModule.Definition()
        message.trdnbr = trdnbr
        message.guid = str(uuid.uuid4())
        return message
    
    def OnResultUpdated(self, resultKey, resultEvent, result):
        try:
            msgDic = self.__ParseResult(result)
            self.__NotifySuccess( msgDic )
        except Exception as e:
            self.__NotifyFail("Error: %s" % str(e))
        finally:
            self.RemovePaceConsumer()
    
    def __ParseResult(self, result):
        if not result.success:
            raise Exception("Calculation Failed")
        
        msgDic = {}
        msgDic['IncPFE'] = result.IncPFE
        msgDic['PFE'] = result.PFE
        msgDic['AfterPFE'] = result.AfterPFE
        return msgDic
      
    def RemovePaceConsumer(self):
        if self._paceConsumer:
            self._paceConsumer.Destroy()
            self._paceConsumer = None
    
    def OnDispatcherState(self):
        self.__NotifyStatus(self._paceConsumer.StatusText())
    
    def __NotifySuccess(self, msgDic):
        if self._observer:
            self._observer.OnTaskSuccess(msgDic)
    
    def __NotifyFail(self, msg):
        if self._observer:
            self._observer.OnTaskFail(msg)
    
    def __NotifyStatus(self, msg):
        if self._observer:
            self._observer.OnTaskStatus(msg)
