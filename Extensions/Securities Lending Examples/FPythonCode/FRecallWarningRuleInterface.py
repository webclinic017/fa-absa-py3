""" Compiled: 2018-09-05 15:52:11 """

#__src_file__ = "extensions/SecuritiesLending/etc/FRecallWarningRuleInterface.py"

import acm
import FGrouperUtils
from FTradeCreator import TradeFromRowCreator
from FCalculationSpaceUtils import CalculationGridRowColumn
from FCalculationValueSourceUtils import Params
from FSecLendRuleInterfaceUtils import CreateValueResult, IteratorsAtSubLevel
from FRecallWarningDefinition import RecallWarningDefinition
from FComplianceRulesUtils import logger
import FNotificationsHooks

class Interface(object):

    def CreateValueSource(self, appliedRule):
        return RecallWarningValueSource(appliedRule)
    
    def CreateCompositeAttributes(self, ruleDefinition):
        return RecallWarningDefinition(ruleDefinition)
    
    def OnHandle(self, alerts, *args):
        return FNotificationsHooks.OnHandleRecallAlerts(alerts, *args)
    
    def OnDetails(self,alerts, *args):
        return FNotificationsHooks.OnDetailsRecallAlerts(alerts, *args)


class RecallParams(Params):

    def __init__(self, rule):
        super(RecallParams, self).__init__(rule)
        self._rule = rule

    def ColumnId(self):
        return self._definition.RecallColumn()
        
    def Entity(self):
        
        if self._definition.FilterQuery():
            filter = self._definition.FilterQuery().Clone()
            query = filter.Query()
            compQuery = acm.Filter.CompositeAndQuery(acm.FTrade, query, self._PortfolioQuery())
            return compQuery
        else:
            return self._Portfolio()
            
    def _Portfolio(self):
        prtf = self._rule.Target()
        assert prtf.IsKindOf(acm.FPortfolio)
        return prtf
        
    def _PortfolioQuery(self):
        query = acm.FASQLQuery()
        query.AsqlQueryClass(acm.FTrade)
        opNode = query.AddOpNode('AND')
        opNode.AddAttrNode('Portfolio.Name', 'EQUAL', self._Portfolio().Name())
        return query
        
    def Grouper(self):
        return  FGrouperUtils.GetGrouper(self._definition.Grouper(), acm.FPortfolioSheet)
    

class RecallWarningValueSource(CalculationGridRowColumn):
    
    def __init__(self, appliedRule):
        super(RecallWarningValueSource, self).__init__(RecallParams(appliedRule))
        self._appliedRule = appliedRule
        
    def Values(self, anObject=None):
        results = []
        for node in self.NodeIterator():
            results.append(self.ValueResult(node))
        return results

    def ValueResult(self, node):
        result = acm.FValueResult()
        try:
            result.Result(self.Value(node))
            result.Entity(self.Entity(node))
            result.Info(self.Info(result.Result()))
        except StandardError as e:
            result.IsError(True)
            result.Info(str(e))
        return result

    def Entity(self, node):
        """ Creates an FCustomArchive with a dictionary containing the grouper attributes 
            and values for the current node """
        if self.Grouper():
            return CreateAlertSubjectFromNode(node)
        else:
            return node.Item().Instrument()

    def Value(self, node):
        """ Returns the value of the selected column for the node """
        return self.GetValue(node) or 0
    
    def Info(self, value):
        return '{0:.2f}'.format(value)
    
    def Grouper(self):
        return self._grouper
        
    def _SubLevel(self):
        grouper = self.Grouper()
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            return len(grouper.Groupers())
        else:
            return 1
            
    def NodeIterator(self):
        iter = self.EntityNode().Iterator()
        return IteratorsAtSubLevel(iter, self._SubLevel())


def _CustomArchiveName(attributes):
    text = []
    for property, value in attributes.iteritems():
        text.append('{0}={1}'.format(property, value.Name() if hasattr(value, 'Name') else value))
    return ';'.join(text)

def _GetCustomArchive(name):
    try:
        return acm.FCustomArchive.Select('name="{0}" and subType="Recall Alert" and user="0"'.format(name))[0]
    except IndexError:
        return None

def _GetOrCreateCustomArchive(attributes):
    archive = acm.FCustomArchive()
    archive.ToArchive('attributes', attributes)
    archive.SubType('Recall Alert')
    name = _CustomArchiveName(attributes)
    existingArchive = _GetCustomArchive(name)
    if existingArchive:
        return existingArchive
    else:
        archive.Name(name)
        archive.AutoUser(False)
        archive.Commit()
        return archive

def CreateAlertSubjectFromNode(node):
    properties = {}
    for property, value in TradeFromRowCreator.PropertiesFromGrouper(node.Item()):
        properties[property] = value
    return _GetOrCreateCustomArchive(properties)
