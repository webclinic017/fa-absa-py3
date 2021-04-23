""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FAppliedRuleEngine.py"
"""--------------------------------------------------------------------------
MODULE
    FAppliedRuleEngine

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
        
-----------------------------------------------------------------------------"""
import acm
from collections import defaultdict
from FComplianceRulesUtils import (CreateOrUpdateAlertsFromCheck,
                                   CommitAlerts, 
                                   RuleCheck,                                   
                                   logger)


class RulesCollection(object):

    def __init__(self):
        self._rules = defaultdict(set)
        
    def Add(self, rule):
        self._rules[rule.ComplianceRule()].add(rule)
        
    def Remove(self, rule):
        cRule = rule.ComplianceRule()
        self._rules[cRule].remove(rule)
        if not self._rules.get(cRule):
            del self._rules[cRule]
                
    def __contains__(self, item):
        if item.IsKindOf(acm.FComplianceRule):
            return item in self.ComplianceRules()
        elif item.IsKindOf(acm.FAppliedRule):
            return item in self.Rules()
        
    def Rules(self):
        return (r for cr in self._rules for r in self._rules[cr])
        
    def ComplianceRules(self):
        return self._rules.iterkeys()
        
    def Clear(self):
        self._rules.clear()
        
        
class WorkItem(object):

    def __init__(self, action, *args, **kwargs):
        self._action = action
        self._args = args
        self._kwargs = kwargs
        
    def Exec(self):
        return self._action(*self._args, **self._kwargs)
        
        
class WorkQueue(object):

    def __init__(self):
        self._queue = []
        
    def Add(self, item):
        self._queue.append(item)
        
    def Pop(self, index):
        return self._queue.pop(index)
        
    def __nonzero__(self):
        return bool(self._queue)
        
        
class FAppliedRuleHandler(object):

    def __init__(self, engine):
        self._engine = engine
        
    def Handle(self, rule, param):
        if param and not param.IsKindOf(acm.FAlert):
            self._engine.HandleRule(rule, param, False)
        
class FComplianceRuleHandler(object):

    def __init__(self, engine):
        self._engine = engine
        
    def Handle(self, cRule, param):
        if param and param.IsKindOf(acm.FComplianceRule):
            for rule in cRule.AppliedRules():
                self._engine.HandleRule(rule)


class Engine(object):

    def __init__(self):
        self._workQueue = WorkQueue()
        self._monitored = RulesCollection()

    def Work(self):
        while self._workQueue:
            item = self._workQueue.Pop(0)
            item.Exec()
            
    def Stop(self):
        for rule in self._monitored.Rules():
            self._StopObserving(rule)
        self._monitored.Clear()
        
    def Add(self, rule):
        if rule not in self._monitored:
            logger.debug('Adding rule {0} to engine for monitoring'.format(rule.Oid()))
            self._monitored.Add(rule)
            item = WorkItem(self._Process, rule)
            self._workQueue.Add(item)
            self._StartObserving(rule)        
            
    def Remove(self, rule):
        if rule in self._monitored:
            self._monitored.Remove(rule)
            self._StopObserving(rule)
        else:
            logger.debug('Rule {0} is not being monitored '
                'and can\'t be removed').format(rule.Oid())
            
    def HandleRule(self, rule, param=None, recede=True):
        item = WorkItem(self._Process, rule, param, recede)
        self._workQueue.Add(item)

    def _Process(self, rule, anObject=None, recede=True):
        logger.debug('Checking rule {0} with param {1}'.format(rule.Oid(), self.GetDomainName(anObject)))
        check = RuleCheck(rule, anObject)
        alerts = CreateOrUpdateAlertsFromCheck(check, recedeNotFound=recede)
        CommitAlerts(alerts)
        
    def _StartObserving(self, rule):
        if self not in rule.Dependents():
            logger.debug('Start observing rule {0}'.format(rule.Oid()))
            rule.AddObserver(self)
        if self not in rule.ComplianceRule().Dependents():
            logger.debug('Start observing compliance rule {0}'.format(rule.ComplianceRule().Oid()))    
            rule.ComplianceRule().AddDependent(self)
            
    def _StopObserving(self, rule):
        if self in rule.Dependents():
            logger.debug('Stop observing rule {0}'.format(rule.Oid()))        
            rule.RemoveObserver(self)
        cRule = rule.ComplianceRule()
        if not cRule in self._monitored:
            logger.debug('Stop observing compliance rule {0}'.format(rule.ComplianceRule().Oid()))            
            cRule.RemoveDependent(self)
        
    @staticmethod
    def GetDomainName(obj):
        try:
            name = obj.ClassName()
            for o in obj:
                return '{0}({1})'.format(name, o.ClassName())
        except TypeError:
            try:
                return '{0}({1})'.format(name, obj.Oid())
            except AttributeError:
                return '{0}'.format(name)
        except AttributeError:
            return obj
        
    def ServerUpdate(self, sender, aspect, param):
        try:
            logger.debug('{0} {1} {2}'.format(self.GetDomainName(sender), aspect, self.GetDomainName(param)))
            clname = '{0}{1}'.format(sender.ClassName(), 'Handler')
            mod = __import__(__name__)
            cl = getattr(mod, clname, None)
            if cl: cl(self).Handle(sender, param)
        except Exception as err:
            logger.error(err)