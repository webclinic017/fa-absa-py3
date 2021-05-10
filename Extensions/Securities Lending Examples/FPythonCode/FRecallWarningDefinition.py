""" Compiled: 2018-09-05 15:52:11 """

#__src_file__ = "extensions/SecuritiesLending/etc/FRecallWarningDefinition.py"

import acm
from FComplianceRuleAttributeDefinitions import ComplianceRuleDefinition

class RecallWarningDefinition(ComplianceRuleDefinition):

    def OnInit(self, definition):
        ComplianceRuleDefinition.OnInit(self, definition)
        
       
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'RecallColumn':            dict(label="Column", 
                                                    choiceListSource=self.RecallColumns()),
                'FilterQuery':                 dict(choiceListSource=self.UniqueCallback('@ApplicableQueryFolder'))
                        }

        overrideAccumulator(overrideDict)
        
    def RecallColumns(self):
        return acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', '_RuleColumns_RecallRule_Recall').Value().split('.')
        
    def ApplicableQueryFolder(self, *args):
        return acm.FStoredASQLQuery.Select("subType = 'FTrade'")
        
