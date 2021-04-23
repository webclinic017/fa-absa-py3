""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FAppliedRuleService.py"
"""--------------------------------------------------------------------------
MODULE
    FAppliedRuleService

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
        
-----------------------------------------------------------------------------"""

import acm
import FAppliedRuleEngine

from FComplianceRulesUtils import logger

logger.Reinitialize(level=2)


class Service(object):

    def __init__(self, freq):
        self._freq = freq
        self._workLoop = None
        self._workQueue = []        

    def Start(self):
        if not self._workLoop:
            self._workLoop = acm.Time.Timer().CreatePeriodicTimerEvent(
                self._freq, 
                self._WorkLoop,
                None)
            
    def Stop(self):
        if self._workLoop:
            acm.Time.Timer().RemoveTimerEvent(self._workLoop)
            self._workLoop = None
        
    def Work(self):
        pass

    def PostWork(self, work, args=[]):
        self._workQueue.append((work, args))

    def _WorkLoop(self, *rest):
        self.Work()
        while self._workQueue:
            try:
                work, args = self._workQueue.pop(0)
                work(*args)
            except Exception as err:
                logger.error(err, exc_info=True)
                
                
class Monitoring(Service):

    def __init__(self, freq=0.5):
        super(self.__class__, self).__init__(freq)
        self._engine = FAppliedRuleEngine.Engine()
        
    def Stop(self):
        self._engine.Stop()
        super(self.__class__, self).Stop()
        
    def Work(self):
        self._engine.Work()
        
    def Add(self, rule):
        self._engine.Add(rule)
        
    def Remove(self, rule):
        self._engine.Remove(rule)