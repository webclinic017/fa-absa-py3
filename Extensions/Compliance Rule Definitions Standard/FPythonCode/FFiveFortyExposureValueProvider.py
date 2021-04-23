""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FFiveFortyExposureValueProvider.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFiveFortyExposureValueProvider

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Value provider for calculating 5/40 Exposure rules
-------------------------------------------------------------------------------------------------------"""
import acm
import FGrouperUtils
from FExposureValueProvider import ExposureValueProvider

class FiveFortyExposureValueProvider(ExposureValueProvider):
    
    def __init__(self, appliedRule):
        self._issuers = []
        super(FiveFortyExposureValueProvider, self).__init__(appliedRule)
        
    def Values(self, anObject=None):
        self.InitializeNodes()
        return [self.ValueResult()]
        
    def ValueResult(self):
        nodesAboveLimit = []
        totalValue = 0
        self._issuers = []
        for node in self._NodesForEach(self._filteredPortfolioNode):
            value = float(self._ValueAsPercent(node, self._relativeToNode))
            if value >= self.ExposureLimit():
                totalValue += value
                nodesAboveLimit.append(node)
                issuer = node.Item().Grouping().GroupingValue()
                if issuer:
                    self._issuers.append(issuer.Name())
                    
        result = acm.FValueResult()
        try:
            result.Result(totalValue)
            result.Entity(self._filteredPortfolioNode.Item())
            result.Info(self.Info(totalValue))
        except Exception as e:
            result.IsError(True)
            result.Info(str(e))
        return result

    def ExposureLimit(self):
        return self.Definition().ExposureLimit()
    
    def Grouper(self):
        return FGrouperUtils.GetGrouper('Issuer', acm.FPortfolioSheet)
        
    def Info(self, value):
        issuers = ', '.join(self._issuers)
        return '{0:.2f} {1} , Issuers: {2}'.format(value, '%', issuers)
        

def _QueryForInstruments(instruments):
    query = acm.FASQLQuery()
    query.AsqlQueryClass(acm.FTrade)
    opNode = query.AddOpNode('OR')
    for instrument in instruments:
        opNode.AddAttrNode('Instrument.Name', 'EQUAL', instrument.Name())
    return query
