""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pace_runner/etc/FPaceAelTaskSchedule.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import FPaceAelTaskConsumer
import FPaceAelTaskLogger

TASK_INITIALISED = 0
TASK_STARTED = 1
TASK_FINISHED = 2
TASK_ERROR = 3

logger = FPaceAelTaskLogger.getLogger()

class FPaceAelTaskSchedule:

    def __init__(self, aelTaskName):
        self._aelTaskName = aelTaskName
        self._paceConsumer = FPaceAelTaskConsumer.FPacePfeTaskConsumer()
        self._paceConsumer.SetObserver(self)
        self._status = TASK_INITIALISED
        self._taskResult = 'Initialized'
    
    def OnTaskSuccess(self, msgDic):
        self._status = TASK_FINISHED
        self._taskResult = 'Succeeded'
        msg = "Task " + self._aelTaskName + " Successed"
        logger.LOG(msg)
        
    def OnTaskFail(self, msg):
        self._status = TASK_FINISHED
        self._taskResult = 'Failed'
        msg = "Task " + self._aelTaskName + " Failed"
        logger.LOG(msg)
        
    def OnTaskStatus(self, msg):
        msg = " Task " + self._aelTaskName + " Get Status msg: " + msg
        logger.LOG(msg)
        
    def Status(self):
        return self._status
        
    def CreateTask(self):
        try:
            self._taskResult = 'Initialized'
            self._status = TASK_STARTED
            self._paceConsumer.CreateTask(self._aelTaskName)
            
        except Exception as e:
            self._status = TASK_ERROR
            self._taskResult = str(e)
            msg = "create task " + self._aelTaskName + " get Exception: " + str(e)
            logger.Error(msg)
    
    def ServerUpdate(self, sender, aspect, parameter):
        logger.Error(str(aspect))
