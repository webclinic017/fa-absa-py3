""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FExposureRuleInterface.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExposureRuleInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FSheetUtils
from FTradeCreator import TradeFromTMPositionCreator
from FParameterSettings import ParameterSettingsCreator
from FComplianceRuleInspector import ComplianceRuleInspectorPortfolioSheet
from FAlertGenerator import Generator
from FExposureValueProvider import ExposureValueProvider
from FExposureRuleAttributeDefinitions import ExposureRuleDefinition


class ExposureRuleInterface(object):

    def CreateValueSource(self, appliedRule):
        return ExposureValueProvider(appliedRule)
    
    def CreateCompositeAttributes(self, ruleDefinition):
        return ExposureRuleDefinition(ruleDefinition)
        
    def CreateAlertGenerator(self, params):
        return ExposureAlertGenerator(params)
    
    def OnDetails(self, appliedRule, alert=None):
        ExposureRuleInspector(appliedRule, alert).Display()

class ExposureAlertGenerator(Generator):
    
    def ToSubject(self, entity):
        if entity.IsKindOf(acm.FPortfolioInstrumentAndTrades):
            return self.PortfolioFromRow(entity)
        if  entity.IsKindOf(acm.FSingleInstrumentAndTrades): #or entity.GrouperOnLevel().IsKindOf(acm.FDefaultGrouper):
            return self.InstrumentFromRow(entity)
        else:
            subject = entity.Grouping().GroupingValue()
            if subject and (isinstance(subject, str) or subject.IsKindOf(acm.FSymbol)):
                subject = self._GetOrCreateCustomArchive(entity)
            return subject
    
    @staticmethod
    def InstrumentFromRow(row):
        ins = row.Instrument()
        if ins.IsKindOf(acm.FFxRate):
            ins = ins.DomesticCurrency().CurrencyPair(ins.ForeignCurrency())
        return ins
    
    @staticmethod
    def PortfolioFromRow(row):
        return TradeFromTMPositionCreator._PhysicalPortfolio(row.Portfolio())
    
    @staticmethod
    def _GetCustomArchive(name):
        try:
            return acm.FCustomArchive.Select('name="{0}" and subType="Alert Subject" and user="0"'.format(name))[0]
        except IndexError:
            return None
    
    @classmethod
    def _GetOrCreateCustomArchive(cls, rowItem):
        """ Creates a custom archive object to represent a string value as the subject of an alert. """
        text = '{0}: {1}'.format(rowItem.GrouperOnLevel().DisplayName(), rowItem.Grouping().GroupingValue())
        archive = acm.FCustomArchive()
        archive.ToArchive('subject', text)
        archive.SubType('Alert Subject')
        existingArchive = cls._GetCustomArchive(text)
        if existingArchive:
            return existingArchive
        else:
            archive.Name(text)
            archive.AutoUser(False)
            return archive
    
class ExposureRuleInspector(ComplianceRuleInspectorPortfolioSheet):

    def InsertRuleTarget(self):
        self._valueSource.InitializeNodes()
        if self._RelativeNodeShouldBeInserted():
            items = [self._appliedRule.Target(), self.FilteredPortfolioFolder()]
        else:
            items = [self.FilteredPortfolioFolder()]
        self._sheet.InsertObject(items, 'IOAP_LAST')
        self.ApplyGrouper()
        FSheetUtils.ExpandTree(self._sheet, 2)
    
    def FilteredPortfolioFolder(self):
        filteredPortfolioItem = self._valueSource._FilteredPortfolioItem()
        if filteredPortfolioItem.IsKindOf(acm.FASQLQuery):
            folder = acm.FASQLQueryFolder()
            folder.AsqlQuery(filteredPortfolioItem)
            folder.Name('{0} ({1})'.format(self._appliedRule.Target().Name(), self._QueryName()))
            return folder
        else:
            return filteredPortfolioItem
    
    def ApplyGrouper(self):
        FSheetUtils.ApplyGrouperInstanceToSheet(self._sheet, self._valueSource.Grouper())
    
    def Columns(self):
        columns = [self._valueSource.ColumnName()]
        if self._valueSource.RelativeToColumnName():
            columns.append(self._valueSource.RelativeToColumnName())
        return columns
    
    #def ColumnCreators(self):
    #    creators = super(ExposureRuleInspector, self).ColumnCreators()
    #    creators.Add(self.RuleValueColumnCreator())
    #    return creators
    
    #def RuleValueColumnCreator(self):
    #    config = {acm.FSymbol('ComplianceRule'): self._appliedRule.ComplianceRule()}
    #    columnConfig = acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues(config)
    #    columnCreator = acm.GetColumnCreators(['Rule Value'], acm.GetDefaultContext())
    #    return columnCreator.At(0).Template().CreateCreator(columnConfig, None)
        
    def _QueryName(self):
        res = [query.Name() for query in self._valueSource.Definition().FilterQuery() or []]
        if self._valueSource.Definition().PythonFilterMethodName():
            res.append(self._valueSource.Definition().PythonFilterMethodName().split('.')[1])
        operator = self._valueSource.Definition().CompoundQueryLogicalOperator()
        return ' {0} '.format(operator).join(res)
    
    def _RelativeNodeShouldBeInserted(self):
        return self._valueSource._relativeToNode and (self._valueSource._PythonFilterMethod()  
                                                      or self._valueSource.Definition().FilterQuery())
    
    def SheetTemplate(self):
        settings = ParameterSettingsCreator.FromRootParameter('InspectRuleSheetTemplate')
        return acm.FTradingSheetTemplate[settings.Exposure()]
