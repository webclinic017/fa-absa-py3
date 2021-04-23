""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEventHook.py"
from FOperationsHook import DefaultHook
import types
from FOperationsTypeComparators import PrimitiveTypeComparator

class ConfirmationEventHook(DefaultHook):

    def __init__(self, moduleName, hookName):
        DefaultHook.__init__(self, moduleName, hookName, PrimitiveTypeComparator(bool))

    def IsSatisfiedBy(self, fObject, trade = None):
        if trade == None:
            return self.CallHook(fObject)
        return self.CallHook(fObject, trade)