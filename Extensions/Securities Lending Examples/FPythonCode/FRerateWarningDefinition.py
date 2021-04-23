""" Compiled: 2018-09-05 15:52:11 """

#__src_file__ = "extensions/SecuritiesLending/etc/FRerateWarningDefinition.py"

import acm
from FComplianceRuleAttributeDefinitions import ComplianceRuleDefinition

class RerateWarningDefinition(ComplianceRuleDefinition):

    def OnInit(self, definition):
        ComplianceRuleDefinition.OnInit(self, definition)
        
       
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'CurrentFeeColumn':            dict(label="Current Fee", 
                                                    choiceListSource=self.CurrentFeeColumns()),

                'ReferenceFeeColumn':          dict(label="Reference Fee", 
                                                choiceListSource=self.ReferenceFeeColumns()),
                                                
                'DiffType':          dict(toolTip="The comparison is done such that a 'Greater than'-threshold will be broken if the current fee is bigger than the reference fee.",
                                        choiceListSource=self.DiffType()),
                
                'FilterQuery':                 dict(choiceListSource=self.UniqueCallback('@ApplicableQueryFolder'))
                            }
        overrideAccumulator(overrideDict)
        
    def ReferenceFeeColumns(self):
        return acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', '_RuleColumns_RerateRule_ReferenceFee').Value().split('.')
        
    def CurrentFeeColumns(self):
        return acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', '_RuleColumns_RerateRule_CurrentFee').Value().split('.')
        
        
    def ApplicableQueryFolder(self, *args):
        return acm.FStoredASQLQuery.Select("subType = 'FTrade'")

    def DiffType(self):
        return ['Basis Points', 'Relative %']

        
    def GetRuleLayout(self):
        return """vbox(;
                    FilterQuery;
                    DiffType;
                    CurrentFeeColumn;
                    ReferenceFeeColumn;
                );"""

