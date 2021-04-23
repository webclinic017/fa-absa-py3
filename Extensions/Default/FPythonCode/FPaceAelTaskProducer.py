""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pace_runner/etc/FPaceAelTaskProducer.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import FPaceProducer
import FPaceAelTaskTraits
import FPaceAelTaskLogger

logger = FPaceAelTaskLogger.getLogger()
TaskSucceeded = 2

def CreateProducer():
    logger.LOG('Creating Pace AelTask Producer')
    return AelTaskProducer()

class AelTaskProducer(FPaceProducer.Producer):

    def __init__(self):         
        super(AelTaskProducer, self).__init__()
                 
    def OnCreateTask(self, taskId, definition):
        resultKey = self.__CreateResultKey()
        result = self.__CreateResult(definition)
        self.SendInsertOrUpdate(taskId, resultKey, result)
    
    def __CreateResultKey(self):
        UNNECESSARY_UPDATE_ID = 1
        resultKey = FPaceAelTaskTraits.ResultKey()
        resultKey.updateId = UNNECESSARY_UPDATE_ID
        return resultKey
    
    def __CreateResult(self, definition):
        result = self.__InitializeNewResult()
        try:
            theAelTask = acm.FAelTask[str(definition.taskName)]
            theAelTask.LogToFile(True)
            res = theAelTask.Execute()
            history = theAelTask.History().AsList().Last()
            result.success = history.Status() == 'Succeeded'

        except Exception as e:
            logger.LOG('Got a exception %s' %(str(e)))
        return result
    
    def __InitializeNewResult(self):
        result = FPaceAelTaskTraits.Result()
        result.success = False
        result.infoMsg = str("", "utf-8")
        result.warningMsg = str("", "utf-8")
        result.errorMsg = str("", "utf-8")
        return result

