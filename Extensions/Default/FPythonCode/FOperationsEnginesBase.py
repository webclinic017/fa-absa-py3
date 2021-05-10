""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsEnginesBase.py"

from FOperationsExceptions import UnSupportedObjectException
from FOperationsEngines import SimpleEngine, Engine

#-------------------------------------------------------------------------
class OperationsSimpleEngine(SimpleEngine):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        self._loggerIF = configuration.loggerIF

        self._writerIF = configuration.writerIF
        self._writerIF.PO_Init(self)

        self._isSupportedObjectCb = configuration.isSupportedObjectCb

    #-------------------------------------------------------------------------
    def Clear(self):
        self._writerIF.PO_Clear()
        self._loggerIF.LP_Flush()

    #-------------------------------------------------------------------------
    def WR_AddItem(self, op, item):
        if not self._isSupportedObjectCb(item):
            raise UnSupportedObjectException

        self._writerIF.WR_AddItem(op, item)

    #-------------------------------------------------------------------------
    def WR_AddItems(self, items):
        for op, item in items:
            self.WR_AddItem(op, item)

    #-------------------------------------------------------------------------
    def WR_Commit(self):
        return self._writerIF.WR_Commit()

        #-------------------------------------------------------------------------
    def WR_CreateResult(self):
        return self._writerIF.WR_CreateResult()

    #-------------------------------------------------------------------------
    def LP_Log(self, text):
        self._loggerIF.LP_Log(text)

    #-------------------------------------------------------------------------
    def LP_LogVerbose(self, text):
        self._loggerIF.LP_LogVerbose(text)

    #-------------------------------------------------------------------------
    def LP_Flush(self):
        self._loggerIF.LP_Flush()


#-------------------------------------------------------------------------
class OperationsEngine(OperationsSimpleEngine, Engine):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        self._params = configuration.params
        self._hookAdminIF = configuration.hookAdminIF
        self._validatorsIF = configuration.validatorsIF

        super(OperationsEngine, self).__init__(configuration)

    #-------------------------------------------------------------------------
    def Clear(self):
        super(OperationsEngine, self).Clear()

    #-------------------------------------------------------------------------
    def HA_CallHook(self, hookIndex, *args):
        return self._hookAdminIF.HA_CallHook(hookIndex, *args)

    #-------------------------------------------------------------------------
    def HA_IsCustomHook(self, hookIndex):
        return self._hookAdminIF.HA_IsCustomHook(hookIndex)

    #------------------------------------------------------------------------
    def VA_IsValidObject(self, op, obj):
        validator = self._validatorsIF.get(str(obj.ClassName()))
        return validator.VA_IsValidOperation(op, obj) if validator else True

    #------------------------------------------------------------------------
    def Param(self, param):
        value = None
        try:
            value = self._params[param]
        except KeyError as _:
            pass
        return value

#-------------------------------------------------------------------------
class OperationsTaskEngine(OperationsEngine):
    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        super(OperationsTaskEngine, self).__init__(configuration)        
        self.__tasks = configuration.tasks
        assert self.__tasks != None

        for taskObject, _, _ in self.__tasks:
            taskObject.PO_Init(self)


    #-------------------------------------------------------------------------
    def Process(self, msg, obj):
        for taskObject, verifier, exception in self.__tasks:
            try:
                if(verifier(msg, obj)):
                    taskObject.ST_Run(msg, obj)
                    break
            except exception as error:
                self.LP_Log("Caught an exception in OperationsTaskEngine: {}".format(error))
                break
        else:
            raise NotImplementedError("The engine did not match the msg to any of the tasks")
