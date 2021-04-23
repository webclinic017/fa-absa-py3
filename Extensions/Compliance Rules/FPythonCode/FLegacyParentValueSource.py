""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FLegacyParentValueSource.py"
"""--------------------------------------------------------------------------
MODULE
    FLegacyParentValueSource

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm

from collections import deque
from FEventUtils import Observable

from FLegacyValueSource import LegacyValueSource


class LegacyParentValueSource(Observable):

    def __init__(self, appliedRule):
        super(LegacyParentValueSource, self).__init__()
        self.appliedRule = appliedRule
        self._subLevel = appliedRule.ComplianceRule().Definition().SubLevel()
        self._node = None
        self._children = {}
        
    def Values(self, anObject=None):
        return [self.CreateResult(node, calc) for node, calc in self.CalcResult().iteritems()]

    def CreateResult(self, entity, calc):
        result = acm.FValueResult()
        result.Entity(entity)
        value = None
        try:
            value = calc.Value()
            result.Result(float(value))
        except StandardError as err:
            result.IsError(True)
            info = 'Could not convert {0} to a number. {1}'.format(value, err)
            result.Info(info)
        return result
        
    def CalcResult(self):
        return dict(list(zip(self.NodesOnSubLevel(), self.CalcHandlers())))
        
    def CalcHandlers(self):
        for node in self.NodesOnSubLevel():
            if node not in self._children:
                valueSource = LegacyValueSource(self.appliedRule)
                valueSource.Node(node)
                valueSource.AddDependent(self)
                self._children[node] = valueSource
            yield self._children[node]
        
    def ServerUpdate(self, sender, aspect, param):
        if str(aspect) == 'Remove':
            self._children[param].RemoveDependent(self)
            del self._children[param]
        super(LegacyParentValueSource, self).ServerUpdate(sender, aspect, param)
        
    def Node(self):
        if self._node is None:
            valueSource = LegacyValueSource(self.appliedRule)
            self._node = valueSource.Node()
            self._node.AddDependent(self)
        return self._node
            
    def NodesOnSubLevel(self):
        nodes = []
        if self._subLevel == 0:
            nodes.append(self.Node())
        else:
            parentDepth = self.Node().Depth()
            #TODO: Fix sublevel/depth inconsistencies in a robust way
            compoundPortfolioDepths = deque([parentDepth, ])
            iterator = self.Node().Iterator().FirstChild()
            while iterator and iterator.Tree().Depth() != 1:
                depth = iterator.Tree().Depth()
                rowTreeItem = iterator.Tree().Item()
                if (rowTreeItem.IsKindOf(acm.FPortfolioInstrumentAndTrades) and
                    rowTreeItem.Portfolio().IsKindOf(acm.FCompoundPortfolio)):
                    compoundPortfolioDepths.append(parentDepth)
                    parentDepth = depth
                elif depth <= parentDepth and compoundPortfolioDepths:
                    parentDepth = compoundPortfolioDepths.pop()

                targetDepth = parentDepth + self._subLevel
                if depth > targetDepth:
                    iterator = self._ParentNextSibling(iterator)
                elif depth == targetDepth:
                    nodes.append(iterator.Tree())
                    iterator = iterator.NextSibling() or self._ParentNextSibling(iterator)
                else:
                    iterator = (iterator.FirstChild() or 
                                iterator.NextSibling() or 
                                self._ParentNextSibling(iterator))
        return nodes
        
    def _ParentNextSibling(self, nodeIter):
        parent = nodeIter.Parent()
        if parent and parent.Tree() != self.Node():
            return parent.NextSibling() or self._ParentNextSibling(parent)
        return None