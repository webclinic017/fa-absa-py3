""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FLegacyRuleInterface.py"
"""--------------------------------------------------------------------------
MODULE
    FLegacyRuleInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

from FLegacyValueSource import LegacyValueSource
from FLegacyParentValueSource import LegacyParentValueSource
from FLegacyRuleAttributeDefinitions import LegacyRuleDefinition


class LegacyRuleInterface(object):

    def CreateValueSource(self, appliedRule):
        return LegacyValueSource(appliedRule)
           
    def CreateCompositeAttributes(self, ruleDefinition):
        return LegacyRuleDefinition(ruleDefinition)
        
        
class LegacyParentRuleInterface(LegacyRuleInterface):

    def CreateValueSource(self, appliedRule):
        return LegacyParentValueSource(appliedRule)
