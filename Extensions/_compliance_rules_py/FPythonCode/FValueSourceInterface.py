""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FValueSourceInterface.py"
"""--------------------------------------------------------------------------
MODULE
    FValueSourceInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""


class ObserverInterface(object):
    
    def Update(self, sender, aspect, param):
        pass
        

class ValueSourceInterface(object):

    def Values(self, anObject=None):
        # Return a collection of FValueResult
        raise NotImplementedError
        
    def AddObserver(self, observer):
        pass
        
    def RemoveObserver(self, observer):
        pass
