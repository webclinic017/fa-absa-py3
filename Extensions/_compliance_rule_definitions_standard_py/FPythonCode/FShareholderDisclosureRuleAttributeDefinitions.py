""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FShareholderDisclosureRuleAttributeDefinitions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FShareholderDisclosureRuleAttributeDefinitions

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FExposureRuleAttributeDefinitions import ExposureRuleDefinition
from DealPackageDevKit import Action, UXDialogsWrapper, DealPackageChoiceListSource

class ShareholderDisclosureRuleDefinition(ExposureRuleDefinition):
    
    def AttributeOverrides(self, overrideAccumulator):
        overrideDict = {
                'RelativeToColumn':  dict(choiceListSource=['Total Issued'],
                                            enabled=False),
                'RelativeTo':           dict(enabled=False),
                            }
        overrideAccumulator(overrideDict)
    
    def UpdateGrouperChoices(self):
        groupers = {grouper for grouper in ['Instrument', 'Underlying']}
        if self.SafeDefinition().ForEach():
            groupers.add(self.SafeDefinition().ForEach())
        self._grouperChoices.Clear()
        self._grouperChoices.AddAll(list(groupers))
    
    def UpdateColumnChoices(self):
        columns = {str(column.Name()) for column in self._DefaultColumnChoices()}
        if self.SafeDefinition().Column():
            columns.add(self.SafeDefinition().Column())
        self._columnChoices.Clear()
        self._columnChoices.AddAll(list(columns))
    
    @classmethod
    def _DefaultColumnChoices(cls):
        return cls._PublishedExtensions(acm.FColumnDefinition, 'FTradingSheet', 'shareholder disclosure columns')
    
    @staticmethod
    def _QueryClass():
        return acm.FInstrument
    
    def GetRuleLayout(self):
        return """vbox(;
                    hbox(;
                        Column;
                        selectColumn;
                        );
                    hbox(;
                        ForEach;
                        selectForEachGrouper;
                        );
                    hbox(;
                        queryString;
                        selectQuery;
                        );
                    advancedFilterChoices;
                    PythonFilterMethodName;
                    FilterQuery;
                    hbox(;
                        addQuery;
                        removeQuery;
                        );
                    RelativeTo;
                    RelativeToColumn;
                );"""