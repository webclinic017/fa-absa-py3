""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FAppliedRuleServer.py"
"""--------------------------------------------------------------------------
MODULE
    FAppliedRuleServer

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
        
-----------------------------------------------------------------------------"""
import ael
import acm

from FAppliedRuleEngine import Engine
from FComplianceRulesUtils import logger


class Server(object):

    def __init__(self, source):
        self._source = source
        self._engine = Engine()
        self._appliedRuleCB = None
        
    def Start(self):
        self._StartSubscriptions()
        for rule in self._source.Select():
            self._engine.Add(rule)
            
    def Stop(self):
        self._StopSubscriptions()
        self._engine.Stop()

    def Run(self):
        self._engine.Work()
            
    def _StartSubscriptions(self):
        if self._appliedRuleCB is None:
            self._appliedRuleCB = self._Unbind(self._AppliedRuleTableCB)
            ael.AppliedRule.subscribe(self._appliedRuleCB)
        
    def _StopSubscriptions(self):
        if self._appliedRuleCB:
            ael.AppliedRule.unsubscribe(self._appliedRuleCB)
            self._appliedRuleCB = None
            
    def _Unbind(self, function):
        def inner(*args, **kwargs):
            return function(*args, **kwargs)
        return inner
        
    def _Handle(self, event, rule):
        if event == 'insert':
            self._engine.Add(rule)
        elif event == 'delete':
            self._engine.Remove(rule)
    
    def _AppliedRuleTableCB(self, _anObject, ael_entity, _arg, event):
        if event in ('insert', 'delete'):
            rule = acm.FAppliedRule[ael_entity.seqnbr]
            if self._source.IsSatisfiedBy(rule):
                logger.debug('{0} rule {1}'.format(rule.Oid(), event))
                self._Handle(event, rule)