""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramAction.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgramAction

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    The class FTradeProgramAction is a super class giving support for 
    creating trade programs. Derived classes implements common trading
    tasks for portfolio managers. Examples of such include closing a
    position, rolling a future or rebalancing a portfolio.
-----------------------------------------------------------------------------"""

class Action(object):
    
    _actions = []

    def __init__(self, func):
        self._func = func
        if self._func not in self.__class__._actions:
            self.__class__._actions.append(self._func)
            
    @classmethod
    def GetActions(cls):
        return cls._actions
        
    def __call__(self, *args):
        return self._func(*args)
    
class TradeProgramAction(object):
    
    def __init__(self, name):
        self._name = name
        
    def Name(self):
        return self._name
        
    def AppendTradesForSameAction(self):
        """ Determines if invoking the same type of action many times shouldappend new trades 
            each time or if previous trades should be removed and replaced. """
        return False
    
    def __eq__(self, other):
        return isinstance(self, TradeProgramAction) and self.Name() == other.Name()
                
    def __hash__(self):
        return hash(self._name)
    
    def __str__(self):
        return self._name
    
class RebalancingAction(TradeProgramAction):
    
    def __init__(self, name, targetColumnId=None):
        self._targetColumnId = targetColumnId
        super(RebalancingAction, self).__init__(name)
        
    def TargetColumnId(self):
        return self._targetColumnId
        
    def __eq__(self, other):
        return (isinstance(self, RebalancingAction) 
                and self.Name() == other.Name()
                and self.TargetColumnId() == other.TargetColumnId())
                
    def __hash__(self):
        return hash((self._name, self._targetColumnId))
    
    def __str__(self):
        return '{0} - {1}'.format(self._name, self._targetColumnId)

class OpenPositionAction(TradeProgramAction):

    def AppendTradesForSameAction(self):
        return True
