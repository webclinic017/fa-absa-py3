""" Compiled: 2018-09-05 15:52:11 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendRuleInterfaceUtils.py"
import acm

from FCalculationValueSourceUtils import Node
from FComplianceRulesUtils import logger


class NodeIterator(object):
    # Node selection criteria
    def __init__(self, topNode, entity, anObject=None):
        self._anObject = anObject
        self._topNode = topNode
    
    def Nodes(self):
        if self._anObject is not None:
            yield self._anObject
        else:
            rowIter = self._topNode.Iterator()
            while rowIter.NextUsingDepthFirst():
                if self._IsApplicable(rowIter.Tree().Item()):
                    yield rowIter.Tree()

    def _IsApplicable(self, row):
        return not row.Instrument().IsExpired() and \
            acm.GetCalculatedValue(row, acm.GetDefaultContext(), 'isOpenPosition')
        return True
        

def CreateValueResult(node, result):
    wNode = Node.Create(node)
    valueResult = acm.FValueResult()
    valueResult.Entity(wNode.Instrument())
    valueResult.Result(result['value'])
    valueResult.Info(result['info'])
    valueResult.IsError(result['error'])
    return valueResult

def IteratorsAtSubLevel(iter, subLevel, currentLevel=1):
    iterators = []
    if iter.HasChildren():
        # Get a list of all children
        iter = iter.FirstChild()
        children = [iter.Tree().Iterator()]
        while iter.NextSibling():
            children.append(iter.Tree().Iterator())
        
        # Return all items in this level if subLevel is reached
        if currentLevel == subLevel:
            childrenTrees = [c.Tree() for c in children]
            return childrenTrees
        else: # Get all children for all iterators on this level
            for childIter in children:
                iterators.extend(IteratorsAtSubLevel(childIter, subLevel, currentLevel+1))
            return iterators
