""" Compiled: 2018-09-05 15:52:11 """

#__src_file__ = "extensions/SecuritiesLending/etc/FRerateWarningRuleInterface.py"

import acm

from FCalculationSpaceUtils import CalculationGridRowColumn
from FCalculationValueSourceUtils import Params
from FSecLendRuleInterfaceUtils import CreateValueResult, IteratorsAtSubLevel
from FRerateWarningDefinition import RerateWarningDefinition
from FComplianceRulesUtils import logger
import FNotificationsHooks

class Interface(object):

    def CreateValueSource(self, appliedRule):
        return RerateWarningValueSource(appliedRule)
    
    def CreateCompositeAttributes(self, ruleDefinition):
        return RerateWarningDefinition(ruleDefinition)
    
    def OnHandle(self, alerts, *args):
        return FNotificationsHooks.OnHandleRerateAlerts(alerts, *args)
    
    def OnDetails(self,alerts, *args):
        return FNotificationsHooks.OnDetailsRerateAlerts(alerts, *args)
        
class CalcParams(Params):

    def ColumnName(self):
        return (self._definition.CurrentFeeColumn(), self._definition.ReferenceFeeColumn())
        
    
class RerateParams(Params):

    def __init__(self, rule):
        super(RerateParams, self).__init__(rule)
        self._rule = rule

    def ColumnId(self):
        return (self._definition.CurrentFeeColumn(), self._definition.ReferenceFeeColumn())
        
    def Entity(self):
        
        if self._definition.FilterQuery():
            filter = self._definition.FilterQuery().Clone()
            query = filter.Query()
            opNode = query.AddOpNode('AND')
            opNode.AddAttrNode('Portfolio.Name', 'EQUAL', self._rule.Target().Name())
            filter.Query(query)
            return filter
        else:
            return self._rule.Target()
           
        
class RerateWarningValueSource(CalculationGridRowColumn):
    
    def __init__(self, appliedRule):
        super(RerateWarningValueSource, self).__init__(RerateParams(appliedRule))
        self._appliedRule = appliedRule
        
    def Values(self, anObject=None):
        results = []
        for node in self.NodeIterator():
            value = self._CalculateValueResult(node)
            results.append(CreateValueResult(node, value))
        return results
  
    def _CalculateValueResult(self, node):
        result = {}
        try:
            result['value'] = self._GetValue(node)
            result['info'] = self._Info(float(result['value']))
            result['error'] = False
        except Exception as err:
            result['value'] = None
            result['error'] = True
            result['info'] = 'Error: {0}'.format(str(err))
            logger.debug(result['info'])
        return result
        
    def _Definition(self):
        return self._appliedRule.ComplianceRule().Definition()
        
    def _Info(self, value):
        return '{0:.2f} {1}'.format(value, '%' if self._Definition().DiffType() == "Relative %" else '')

    def _GetValue(self, node):
        values = self.GetValue(node)
        bigNumber = 1000
        if values is None:
            raise 
        else:
            if self._Definition().DiffType() == "Basis Points":
                val = 100*(values[0] - values[1])
            elif self._Definition().DiffType() == "Relative %":
                if values[1] == 0:
                    if values[0] == 0:
                        return 0
                    else:
                        val = bigNumber
                else:
                    val = 100*(values[0] - values[1])/values[1]
        return val

    def _SubLevel(self):
        return 1
        
    def NodeIterator(self):
        iter = self.EntityNode().Iterator()
        return IteratorsAtSubLevel(iter, self._SubLevel())
