""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceRuleInterface.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceRuleInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

class ComplianceRuleInterface(object):

    def CreateValueSource(self, appliedRule):
        raise NotImplementedError      