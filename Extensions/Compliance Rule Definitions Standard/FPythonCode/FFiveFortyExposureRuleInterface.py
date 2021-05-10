""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FFiveFortyExposureRuleInterface.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFiveFortyExposureRuleInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils
from FFiveFortyExposureValueProvider import FiveFortyExposureValueProvider
from FFiveFortyExposureAttributeDefinitions import FiveFortyExposureAttributeDefinitions
from FExposureRuleInterface import ExposureRuleInspector, ExposureAlertGenerator

class FiveFortyExposureRuleInterface(object):

    def CreateValueSource(self, appliedRule):
        return FiveFortyExposureValueProvider(appliedRule)
    
    def CreateCompositeAttributes(self, ruleDefinition):
        return FiveFortyExposureAttributeDefinitions(ruleDefinition)
    
    def CreateAlertGenerator(self, params):
        return ExposureAlertGenerator(params)
    
    def OnDetails(self, appliedRule, alert=None):
        RuleInspectorFiveFortyExposure(appliedRule, alert).Display()
    
    
class RuleInspectorFiveFortyExposure(ExposureRuleInspector):

    def InsertRelativeNode(self):
        if self._RelativeNodeShouldBeInserted():
            folder = acm.FASQLQueryFolder()
            folder.AsqlQuery(self._valueSource._FilteredPortfolioItem())
            folder.Name(self._QueryName())
            self._sheet.InsertObject(folder, 'IOAP_LAST')
            self.ApplyGrouper()
            FSheetUtils.ExpandTree(self._sheet, 2)
    
    def _RelativeNodeShouldBeInserted(self):
        return self._valueSource.Definition().FilterQuery()