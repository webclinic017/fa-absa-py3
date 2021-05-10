""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTaskManager.py"

from FOperationsObservable import Observable

#-------------------------------------------------------------------------
class TaskManager(Observable):
    
    #-------------------------------------------------------------------------
    class MessageCreator(object):
        
        def MC_CreateMessage(self, params, objIds):
            pass
        
    #-------------------------------------------------------------------------
    class Partitioner(object):
        
        def PA_CreatePartitions(self, objects, nbrPartitions):
            pass
    
    #-------------------------------------------------------------------------
    class Events(object):
        
        def TME_OnOutput(self, msg):
            pass
        
        def TME_OnFinished(self):
            pass
        
    def TM_Name(self):
        pass

    def TM_ObjectClass(self):
        pass

    def TM_Destroy(self):
        pass
    
    def TM_Run(self, objects):
        pass
    
    