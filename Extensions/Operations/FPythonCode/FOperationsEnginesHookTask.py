""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsEnginesHookTask.py"
# Settlement
from FOperationsProvidedObject import IEngineTask

#-------------------------------------------------------------------------
class FOperationsEnginesHookTask(IEngineTask):
    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        pass
        self.__hook = configuration.hookIF

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        pass

    #-------------------------------------------------------------------------
    def ST_Run(self, msg, obj):
        self.__provider.HA_CallHook(self.__hook, obj)
