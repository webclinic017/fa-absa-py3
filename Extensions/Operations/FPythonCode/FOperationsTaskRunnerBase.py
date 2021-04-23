""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTaskRunnerBase.py"

from FOperationsTaskRunner import TaskRunner
from functools import reduce

#-------------------------------------------------------------------------
class TaskRunnerBase(TaskRunner):
    
    #-------------------------------------------------------------------------
    def __init__(self, logger, result):
        super(TaskRunnerBase, self).__init__()
        
        self._logger = logger
        self.__taskManagers = {}
        self.__finishedTaskManagers = {}

        self._result = result
        
        self._processingFailed = False
        
    #-------------------------------------------------------------------------
    def TR_OnCreate(self, configurations):
        if not self._processingFailed:
            self.TR_OnStart()
        
        if len(configurations):
            for name, taskManager in self.CreateTaskManagers(configurations).iteritems():
                self.__taskManagers[name] = taskManager
                self.__finishedTaskManagers[name] = False
                taskManager.OO_AddObserver(self)
        else:
            self.OnFinished()
                        
    #-------------------------------------------------------------------------
    def TR_Run(self, tmID, data):
        try:
            self.__taskManagers[tmID].TM_Run(data)
        except KeyError as e:
            raise Exception('ERROR: No task manager by id: {}'.format(tmID))
        except Exception as e:
            raise Exception('ERROR: Exception caught when running task: {}'.format(str(e)))
    
    #-------------------------------------------------------------------------    
    def TR_TaskManagerObjectClass(self, tmID):
        try:
            objClass = self.__taskManagers.get(tmID).TM_ObjectClass()
        except Exception as e:
            raise Exception('ERROR: Could not fetch object class from task manager with ID {}: {}'.format(tmID, str(e)))
        
        return objClass

    #-------------------------------------------------------------------------
    def TR_Result(self):
        return self._result

    #-------------------------------------------------------------------------
    def TME_OnOutput(self, _, msg):
        self._logger.LP_Log(msg)
        self._logger.LP_Flush()
    
    #-------------------------------------------------------------------------    
    def TME_OnFinished(self, tmID, taskManagerResult):
        self._result.TRR_AddResult(tmID, taskManagerResult)
        
        self.__finishedTaskManagers[tmID] = True
                
        if self.IsFinished():
            self.OnFinished()
    
    #-------------------------------------------------------------------------        
    def CreateTaskManagers(self, configurations):
        taskManagers = {}
        
        try:
            for taskManagerCls, configuration in configurations:
                taskManager = taskManagerCls(configuration)
                taskManagers[taskManager.TM_Name()] = taskManager
        except Exception as e:
            self._logger.LP_Log('ERROR: Exception caught when initializing task: {}'.format(str(e)))
            self._logger.LP_Flush()
            raise e
        
        return taskManagers
            
    #-------------------------------------------------------------------------
    def IsFinished(self):
        return reduce(lambda isFinished1, isFinished2: isFinished1 and isFinished2, self.__finishedTaskManagers.values(), True)
            
    #-------------------------------------------------------------------------   
    def OnFinished(self):

        self.__Destroy()

        if self._result.TRR_ContainsFailedData():
            self._processingFailed = True
            self.TR_OnProcessedFailedData()
            self._processingFailed = False
        
        if not self._processingFailed:
            self.TR_OnFinished()
            self._result.TRR_Clear()

        
    #-------------------------------------------------------------------------
    def __Destroy(self):
        for taskManager in self.__taskManagers.values():
            taskManager.TM_Destroy()
        
        self.__taskManagers.clear()
        self.__finishedTaskManagers.clear()

