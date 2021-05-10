""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FCalculationValueSourceUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FCalculationValueSourceUtils

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm


class Params(object):

    def __init__(self, rule):
        self._definition = rule.ComplianceRule().Definition()
        
    def __getattr__(self, attr):
        return getattr(self._definition, attr)
        

class Node(object):
    
    def __init__(self, obj):
        self._obj = obj
        
    def Unwrap(self):
        return self._obj
        
    def Instrument(self):
        raise NotImplementedError
        
    @classmethod
    def Create(cls, obj):
        if isinstance(obj, acm._pyClass('FTreeProxy')):
            return TreeProxy(obj)
        if isinstance(obj, acm._pyClass('FInstrument')):
            return Instrument(obj)            
        if isinstance(obj, acm._pyClass('FTrade')):
            return Trade(obj)
        if isinstance(obj, acm._pyClass('FCalculation')):
            return Calculation(obj)            
        return None


class Trade(Node):

    def __init__(self, trade):
        super(Trade, self).__init__(trade)
        
    def Instrument(self):
        return self._obj.Instrument()
        
        
class Instrument(Node):

    def __init__(self, ins):
        super(Instrument, self).__init__(ins)
        
    def Instrument(self):
        return self._obj


class TreeProxy(Node):

    def __init__(self, trade):
        super(TreeProxy, self).__init__(trade)
        
    def Instrument(self):
        return self._obj.Item().Instrument()


class Calculation(Node):

    def __init__(self, calculation):
        super(Calculation, self).__init__(calculation)
        
    def Instrument(self):
        insid = self._obj.StringKey().split('[')[0].strip() 
        return acm.FInstrument[insid]