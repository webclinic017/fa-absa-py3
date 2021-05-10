""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FExclusionRuleInterface.py"
"""--------------------------------------------------------------------------
MODULE
    FExclusionRuleInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

from FExclusionValueSource import ExclusionValueSource
from FExclusionRuleAttributeDefinitions import ExclusionRuleDefinition

class ExclusionRuleInterface(object):

    def CreateValueSource(self, appliedRule):
        return ExclusionValueSource(appliedRule)  
            
    def CreateCompositeAttributes(self, ruleDefinition):
        return ExclusionRuleDefinition(ruleDefinition)