""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsProvidedObject.py"
from abc import ABCMeta, abstractmethod

#-------------------------------------------------------------------------
class Provided(object):
    
    def PO_Init(self, provider):
        pass

    def PO_Clear(self):
        pass

#-------------------------------------------------------------------------
class IEngineTask(Provided, metaclass=ABCMeta):
    @abstractmethod
    def ST_Run(self, msg, obj):
        raise NotImplementedError
