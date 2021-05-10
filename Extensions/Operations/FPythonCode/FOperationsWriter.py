""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsWriter.py"

from FOperationsProvidedObject import Provided

#-------------------------------------------------------------------------
class Writer(Provided):
    
    #-------------------------------------------------------------------------
    class Modifier(Provided):
        
        def MO_Prepare(self, objs):
            pass
        
    #-------------------------------------------------------------------------
    class Committer(Provided):
    
        def CO_CreateResult(self):
            pass
        
        def CO_RegisterLogHook(self, objClass, idx):
            pass
    
        def CO_Commit(self, objs):
            pass

    #-------------------------------------------------------------------------
    def WR_CreateResult(self):
        pass

    def WR_AddItem(self, op, item):
        pass
    
    def WR_AddItems(self, items):
        pass

    def WR_Commit(self):
        pass