""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FExposureValueProvider.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExposureValueProvider

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Value provider for calculating Exposure rules
-------------------------------------------------------------------------------------------------------"""
import acm
import FGrouperUtils
import FAssetManagementUtils
from FCalculationSpaceUtils import CalculationGrid

class ExposureValueProvider(CalculationGrid):
    
    def __init__(self, appliedRule):
        super(ExposureValueProvider, self).__init__()
        self.appliedRule = appliedRule
        self._relativeToNode = None
        self._filteredPortfolioNode = None
        
    def InitializeNodes(self):
        self._relativeToNode = self._RelativeToNode()
        self._filteredPortfolioNode = self.InsertItem(self._FilteredPortfolioItem(), self.Grouper())
    
    def Values(self, anObject=None):
        self.InitializeNodes()
        results = []  
        for node in self._Nodes():
            results.append(self.ValueResult(node))
        return results
    
    def ValueResult(self, node):
        result = acm.FValueResult()
        try:
            result.Entity(self.Entity(node))
            result.Result(self.Value(node))
            result.Info(self.Info(result.Result()))
        except Exception as e:
            result.IsError(True)
            result.Info(str(e))
        return result
    
    def _FilteredPortfolioItem(self):
        """ Returns an ASQLQuery based on the entity of the applied rule and all queries defined
            in the rule defintion including those created by a "Python Filter Method" """
        filterQueries = [f.Query() for f in self.Definition().FilterQuery() or []]
        if self._PythonFilterMethod():
            filterQueries.append(self._PythonFilterMethod()(self))
        if filterQueries:
            operator = self.Definition().CompoundQueryLogicalOperator()
            compoundQuery = self._CompositeQuery(acm.FTrade, filterQueries, operator=operator)
            portfolioQuery = self._PortfolioQuery(self._Portfolio())
            return self._CompositeQuery(acm.FTrade, [portfolioQuery, compoundQuery], operator='AND')
        else:
            return self._Portfolio()
    
    def _Nodes(self):
        """ Returns nodes for the subjects that the exposure should be checked against, either a filtered 
        subset of the whole portfolio or a list of nodes based on the "For Each"-level """
        if self.IsCalculatedForEach():
            return self._NodesForEach(self._filteredPortfolioNode)
        else:
            return [self._filteredPortfolioNode]  
    
    def Entity(self, node):
        if self.IsCalculatedForEach():
            return node.Item()
        else:
            return self._relativeToNode.Item()
    
    def Value(self, node):
        if self._relativeToNode:
            return self._ValueAsPercent(node, self._relativeToNode)
        else:
            return self.GetValue(node, self.ColumnName()) or 0
    
    def _ValueAsPercent(self, node, relativeToNode):
        self._SimulateCurrency(node)
        self._SimulateCurrency(relativeToNode)
        value = self.GetValue(node, self.ColumnName())
        topValue = self.GetValue(relativeToNode, self.RelativeToColumnName())
        return 100 * value / topValue
    
    def Info(self, value):
        return '{0:.2f} {1}'.format(value, '%' if self.IsRelativeTo() else '')
    
    def _PythonFilterMethod(self):
        if self.Definition().PythonFilterMethodName():
            return FAssetManagementUtils.GetFunction(self.Definition().PythonFilterMethodName())
    
    def _RelativeToNode(self):
        if self.IsRelativeTo():
            return self.InsertItem(self._Portfolio(), None)
        else:
            return None
    
    def _SimulateCurrency(self, node):
        self.SimulateValue(node, 'Portfolio Currency', self._Portfolio().Currency())
    
    def Grouper(self):
        grouperName = self.Definition().ForEach()
        if grouperName and not grouperName == 'Instrument':
            return FGrouperUtils.GetGrouper(grouperName, acm.FPortfolioSheet)
        else:
            return None # Use default grouper 
    
    def NodesForEach(self):
        return self._NodesForEach(self._filteredPortfolioNode)
        
    def IsRelativeTo(self):
        return self.Definition().RelativeTo()

    def IsCalculatedForEach(self):
        return bool(self.Definition().ForEach())
    
    def ColumnName(self):
        return self.Definition().Column()    

    def RelativeToColumnName(self):
        return self.Definition().RelativeToColumn()
    
    def Definition(self):
        return self.appliedRule.ComplianceRule().Definition()
    
    def _Portfolio(self):
        return self.appliedRule.Target()
    
    @staticmethod
    def _PortfolioQuery(portfolio):
        if portfolio.IsKindOf(acm.FStoredASQLQuery):
            return portfolio.Query()
        else:
            query = acm.FASQLQuery()
            query.AsqlQueryClass(acm.FTrade)
            prtfs = portfolio.AllPhysicalPortfolios() if portfolio.IsKindOf(acm.FCompoundPortfolio) else [portfolio]
            prtfNode = query.AddOpNode('OR')
            for prtf in prtfs:
                prtfNode.AddAttrNode('Portfolio.Name', 'EQUAL', prtf.Name())
            return query
    
    @staticmethod
    def _CompositeQuery(queryClass, queries, operator='AND'):
        if queries:
            compQuery = queries[0]
            for query in queries[1:]:
                if operator == 'AND':
                    compQuery = acm.Filter.CompositeAndQuery(queryClass, compQuery, query)
                elif operator == 'OR':
                    compQuery = acm.Filter.CompositeOrQuery(queryClass, compQuery, query)
                else:
                    raise ValueError('Unknown operator: {0}. Must be AND or OR'.format(operator))
            return compQuery
            
    def _NodesForEach(self, node):
        self.Refresh()
        iter = node.Iterator().FirstChild()
        nodes = []
        while iter:
            if iter.Tree().Item().Grouping().GroupingValue():
                nodes.append(iter.Tree())
            iter = iter.NextSibling()
        return nodes
        