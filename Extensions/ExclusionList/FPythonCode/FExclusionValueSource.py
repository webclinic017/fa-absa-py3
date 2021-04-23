""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FExclusionValueSource.py"
"""--------------------------------------------------------------------------
MODULE
    FExclusionValueSource

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm
from FCalculationSpaceUtils import CalculationGridRowColumn, logger


class ExclusionParams(object):

    def __init__(self, rule):
        self._rule = rule
        self._definition = rule.ComplianceRule().Definition()
        self._columnId, self._config = self.ColumnAndConfiguration()
    
    def ColumnId(self):
        return self._columnId
    
    def CalculationConfiguration(self):
        return self._config
        
    def Entity(self):
        return self._rule.Target()
            
    def ColumnAndConfiguration(self):
        columnId = None
        parameters = None
        ruleDefinition = self._definition
        
        if ruleDefinition.ExclusionTarget() == 'Instrument':        
            if ruleDefinition.ListType() == 'Query':
                columnId = '{0} Instrument Query'.format(self._BlackOrWhiteList())
                parameters = {acm.FSymbol('ExclusionListInstrumentQuery') : ruleDefinition.FilterQuery()}
            elif ruleDefinition.ListType() == 'Alias':
                columnId = '{0} Instrument Alias'.format(self._BlackOrWhiteList())
                parameters[acm.FSymbol('InstrumentExclusionAliasType')] = ruleDefinition.AliasType()
            elif ruleDefinition.ListType() == 'Identifiers':
                parameters = {acm.FSymbol('InstrumentIdentifierExclusionList') :  self._IdentifierList()}
                columnId = '{0} Instrument Identifiers'.format(self._BlackOrWhiteList())
            elif ruleDefinition.ListType() == 'PageGroup':
                columnId = '{0} Instruments'.format(self._BlackOrWhiteList())
                parameters = {acm.FSymbol('PageGroupBlacklist') : ruleDefinition.PageGroup()}           
        
        elif ruleDefinition.ExclusionTarget() == 'FX':
            parameters = {acm.FSymbol('ExclusionListCurrencyPairQuery') : ruleDefinition.FilterQuery(),
                          acm.FSymbol('ExclusionListIgnoreFXSpot') : ruleDefinition.IgnoreFXSpot()}
            columnId = '{0} Currency Pairs'.format(self._BlackOrWhiteList())
            
        elif ruleDefinition.ExclusionTarget() == 'Issuer':
            if ruleDefinition.ListType() == 'PartyGroup':
                parameters = {acm.FSymbol('PartyGroupBlacklist') : ruleDefinition.PartyGroup()}
                columnId = '{0} Issuers'.format(self._BlackOrWhiteList())
            elif ruleDefinition.ListType() == 'Alias':
                columnId = '{0} Issuer Alias'.format(self._BlackOrWhiteList())
                parameters[acm.FSymbol('IssuerExclusionAliasType')] = ruleDefinition.AliasType()
            elif ruleDefinition.ListType() == 'Identifiers':
                columnId = '{0} Issuer Identifiers'.format(self._BlackOrWhiteList())
                parameters = {acm.FSymbol('IssuerIdentifierExclusionList') : self._IdentifierList()}
            
        return (columnId, acm.SheetColumn.ConfigurationFromColumnParameterDefinitionNamesAndValues(parameters))
    
    def _BlackOrWhiteList(self):
        return 'Blacklisted' if self._definition.BlacklistOrWhitelist() == 'Blacklist' else 'Whitelisted'
    
    def _IdentifierList(self):
        return acm.GetDefaultContext().GetExtension('FExtensionValue', acm.FObject, self._definition.IdentifierList())
    
class ExclusionValueSource(CalculationGridRowColumn):

    def __init__(self, appliedRule):
        super(ExclusionValueSource, self).__init__(ExclusionParams(appliedRule))
        self.appliedRule = appliedRule
        
    def Values(self, anObject=None):
        valueResults = []
        for node in self.Nodes():
            valueResults.append(self.ValueResult(node))
        return valueResults
        
    def ValueResult(self, node):
        result = acm.FValueResult()
        result.Entity(self._Entity(node))
        value = None
        try:
            value = self.GetValue(node)
            if value:
                result.Result(1)
                result.Info(str(value))
        except Exception as err:
            result.IsError(True)
            result.Info(str(err))
            logger.info(err)
        return result        
            
    def Nodes(self):
        return self.EntitySubNodes()
                            
    @staticmethod
    def _Entity(node):
        ins = node.Item().Instrument()
        if ins.IsKindOf(acm.FFxRate):
            ins = ins.DomesticCurrency().CurrencyPair(ins.ForeignCurrency())
        return ins
