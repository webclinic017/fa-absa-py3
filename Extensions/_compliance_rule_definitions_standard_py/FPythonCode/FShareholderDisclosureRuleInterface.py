""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FShareholderDisclosureRuleInterface.py"
"""--------------------------------------------------------------------------
MODULE
    FShareholderDisclosureRuleInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""
import acm
import FSheetUtils
from FParameterSettings import ParameterSettingsCreator
from FExposureValueProvider import ExposureValueProvider
from FExposureRuleInterface import ExposureAlertGenerator
from FShareholderDisclosureRuleAttributeDefinitions import ShareholderDisclosureRuleDefinition
from FComplianceRuleInspector import ComplianceRuleInspectorPortfolioSheet


class ShareholderDisclosureRuleInterface(object):

    def CreateValueSource(self, appliedRule):
        return ShareholderDisclosureValueProvider(appliedRule)  
    
    def CreateCompositeAttributes(self, ruleDefinition):
        return ShareholderDisclosureRuleDefinition(ruleDefinition)
        
    def CreateAlertGenerator(self, params):
        return ExposureAlertGenerator(params)
    
    def OnDetails(self, appliedRule, alert=None):
        RuleInspectorShareholderDisclosure(appliedRule, alert).Display()


class ShareholderDisclosureValueProvider(ExposureValueProvider):
            
    def _Instruments(self):
        filterQueries = [f.Query() for f in self.Definition().FilterQuery() or []]
        if filterQueries:
            return self._CompositeQuery(acm.FInstrument, filterQueries).Select()
        else:
            return self._Portfolio().Instruments()

    def Value(self, node):
        """ Returns percent of total issued quantity of the instrument in the portfolio. """
        value = self.GetValue(node, self.ColumnName()) or 0
        try:
            return value / self._TotalIssued(node) * 100
        except ZeroDivisionError:
            raise ValueError('Total issued size is set to 0 for {0}'.format(self.Entity(node).Name()))
    
    def _TotalIssued(self, node):
        return self.GetValue(node, 'Shareholder Disclosure Total Issued') or 0
    
    def _Nodes(self):
        iter = self._filteredPortfolioNode.Iterator().FirstChild()
        nodes = []
        for instrument in self._Instruments():
            iter = self._filteredPortfolioNode.Iterator().Find(instrument)
            if iter:
                nodes.append(iter.Tree())
        return nodes
        
    def _FilteredPortfolioItem(self):
        return self._Portfolio()
    
    def _RelativeToNode(self):
        return None


class RuleInspectorShareholderDisclosure(ComplianceRuleInspectorPortfolioSheet):
    
    def Columns(self):
        return [self._valueSource.ColumnName(), 'Shareholder Disclosure Total Issued']
    
    #def ColumnCreators(self):
    #    creators = super(RuleInspectorShareholderDisclosure, self).ColumnCreators()
    #    creators.Add(self.RuleValueColumnCreator())
    #    return creators
    
    #def RuleValueColumnCreator(self):
    #    config = {acm.FSymbol('ComplianceRule'): self._appliedRule.ComplianceRule()}
    #    columnConfig = acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues(config)
    #    columnCreator = acm.GetColumnCreators(['Rule Value'], acm.GetDefaultContext())
    #    return columnCreator.At(0).Template().CreateCreator(columnConfig, None)
    
    def RuleTarget(self):
        self._valueSource.InitializeNodes()
        return [node.Item() for node in self._valueSource._Nodes()]
    
    def SheetTemplate(self):
        settings = ParameterSettingsCreator.FromRootParameter('InspectRuleSheetTemplate')
        return acm.FTradingSheetTemplate[settings.ShareholderDisclosure()]
