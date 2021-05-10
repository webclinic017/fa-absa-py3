""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsEngines.py"

from FOperationsLogger import Logger
from FOperationsWriter import Writer
from FOperationsValidator import Validator

#-------------------------------------------------------------------------
class HookCaller(object):
    
    def HA_CallHook(self, idx, *args):
        pass

    def HA_IsCustomHook(self, idx):
        pass

#-------------------------------------------------------------------------
class ParameterOwner(object):
    
    def Param(self, param):
        pass

#-------------------------------------------------------------------------
class SimpleEngine(Logger, Writer):
    pass

#-------------------------------------------------------------------------
class Engine(SimpleEngine, ParameterOwner, HookCaller, Validator):
    pass
