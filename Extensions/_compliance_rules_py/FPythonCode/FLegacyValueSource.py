""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FLegacyValueSource.py"
"""--------------------------------------------------------------------------
MODULE
    FLegacyValueSource

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

import acm
from FCalculationSpaceUtils import CalculationGridRowColumn
from FCalculationValueSourceUtils import Node


class LegacyParams(object):

    def __init__(self, rule):
        self._appliedRule = rule
        self._definition = rule.ComplianceRule().Definition()
    
    def Entity(self):
        return self._appliedRule.Target()
                    
    def Grouper(self):
        return self.TreeSpecification().Grouper()
    
    def CalculationConfiguration(self):
        return self.Definition().CalculationSpecification().Configuration()

    def Definition(self):
        return self._appliedRule.ComplianceRule().Definition()
    
    def Context(self):
        return self.Definition().CalculationSpecification().ContextName()

    def ColumnId(self):
        return self.Definition().CalculationSpecification().ColumnName()
    
    def Projection(self):
        return self.Definition().ProjectionParts()
    
    def __getattr__(self, attr):
        return getattr(self._definition, attr)

class LegacyValueSource(CalculationGridRowColumn):
    """Calculation for a legacy compliance rule value."""

    def __init__(self, appliedRule):
        super(LegacyValueSource, self).__init__(LegacyParams(appliedRule))
        self._appliedRule = appliedRule
        self._node = None
             
    def Values(self, anObject=None):
        wNode = Node.Create(self.Node())
        result = acm.FValueResult()
        result.Entity(wNode.Instrument())
        value = None
        try:
            value = self.GetValue(self.Node())
            result.Result(float(value))
        except Exception as err:
            result.IsError(True)
            info = 'Could not convert {0} to a number. {1}'.format(value, err)
            result.Info(info)
        return [result]
    
    def Definition(self):
        return self._appliedRule.ComplianceRule().Definition()
    
    def TreeSpecification(self):
        return self.Definition().TreeSpecification()
        
    def Node(self, node=None):
        if node is None:
            if self._node is None:
                treeSpec = self.TreeSpecification()
                topNode = self._InsertTreeSpec(treeSpec)
                try:
                    self._node = topNode.Iterator().Find(treeSpec).Tree()
                except AttributeError:
                    raise AttributeError('Failed to find target node in origin tree')
            return self._node
        else:
            self._node = node

    def _InsertTreeSpec(self, treeSpec):
        try:
            node = self.EntityNode()
            self._ResetOriginObject(treeSpec, node)
            return node
        except RuntimeError as e:
            raise RuntimeError('No calculation for limit target: %s', str(e))

    @staticmethod
    def _ResetOriginObject(treeSpec, node):
        # Comparing two instances of an ASQL portfolio or query folder
        # only works if the instances are the same. Since we are caching
        # these objects, it is necessary to reset the object on the treespec
        # to find it in the TreeIterator::Find method
        try:
            if treeSpec.OriginObject().IsKindOf(acm.FASQLPortfolio):
                treeSpec.OriginObject(node.Item().Portfolio())
            elif treeSpec.OriginObject().IsKindOf(acm.FASQLQueryFolder):
                treeSpec.OriginObject(node.Item())
        except AttributeError:
            pass
