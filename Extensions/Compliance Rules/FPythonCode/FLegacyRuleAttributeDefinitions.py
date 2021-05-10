""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FLegacyRuleAttributeDefinitions.py"
"""--------------------------------------------------------------------------
MODULE
    FLegacyRuleAttributeDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""


from FComplianceRuleAttributeDefinitions import ComplianceRuleDefinition

class LegacyRuleDefinition(ComplianceRuleDefinition):

    def OnInit(self, definition):
        ComplianceRuleDefinition.OnInit(self, definition)

    def RuleAttributes(self):
        return ComplianceRuleDefinition.Attributes(self)
    
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'SheetType':                    dict(enabled=False),
                                  
                'ColumnLabel':                  dict(label='Column',
                                                enabled=False),
                                            
                'CalculationEnvironment':       dict(label='Environment'),
                                                
                'TemplatePath':                 dict(label='TemplatePath',
                                                enabled=False,
                                                visible=False),
                
                'TreeSpecification':            dict(label='TreeSpecification',
                                                enabled=False,
                                                visible=False),
                        }
        overrideAccumulator(overrideDict)
        
    
    def GetRuleLayout(self):
        return ComplianceRuleDefinition.GetRuleLayout(self)
