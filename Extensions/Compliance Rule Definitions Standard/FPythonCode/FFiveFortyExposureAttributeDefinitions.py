""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FFiveFortyExposureAttributeDefinitions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFiveFortyExposureAttributeDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FExposureRuleAttributeDefinitions import ExposureRuleDefinition

class FiveFortyExposureAttributeDefinitions(ExposureRuleDefinition):
    

    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'ExposureLimit':        dict(label='Single issuer limit'),
                'ForEach':              dict(label='for each',
                                            enabled=False,
                                            visible=False),
                'RelativeTo':           dict(label='as percentage of',
                                            enabled=False),
                'selectForEachGrouper':  dict(label='Select',
                                            visible=False)
                            }
        overrideAccumulator(overrideDict)
    
    def QueryStringVisible(self, *args):
        return self.IsShowModeDetail() and self.IsApplicable()
    
    def SelectQueryVisible(self, *args):
        return self.IsShowModeDetail() and self.IsApplicable()
    
    def AdvancedFilterChoices(self, *args):
        return ['', 'Compound query']
    
    def GetRuleLayout(self):
        return """vbox(;
                    hbox(;
                        Column;
                        selectColumn;
                        );
                    hbox(;
                        queryString;
                        selectQuery;
                        );
                    advancedFilterChoices;
                    FilterQuery;
                    hbox(;
                        addQuery;
                        removeQuery;
                        CompoundQueryLogicalOperator;
                        );
                    RelativeTo;
                    hbox(;
                        RelativeToColumn;
                        selectRelativeToColumn;
                        );
                        ExposureLimit;
                );"""
