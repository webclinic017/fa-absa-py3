""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FPositionUtils.py"
"""----------------------------------------------------------------------------
MODULE
    FPositionUtils
        - Utility functions for positions
        - Position instance creator

DESCRIPTION
----------------------------------------------------------------------------"""


import acm

from ACMPyUtils import Transaction
from FTransactionHandler import ACMHandler


__all__ = ['PositionsFromSpec', 
           'DeleteNotTradedPositionsInSpec',
           'DeletePositionsInSpec',
           'PositionCreator',
           'GetAttributeValue',
           'PositionSummary']


def PositionsFromSpec(positionSpec):
    query = acm.CreateFASQLQuery(acm.FCalculationRow, 'AND')
    query.AddAttrNode("Attributes.Specification.Oid", 
                      'EQUAL', 
                      positionSpec.Oid())
    return query.Select()


def DeleteNotTradedPositionsInSpec(positionSpec):
    for position in PositionsFromSpec(positionSpec):
        portfolio = acm.PositionStorage.CreatePortfolioFromPosition(position)
        if not portfolio.Trades():
            with Transaction():
                position.Attributes().Delete()
                position.Delete()


def DeletePositionsInSpec(positionSpec):
    with Transaction():
        for position in PositionsFromSpec(positionSpec):
            position.Attributes().Delete()
            position.Delete()


def GetAttributeValue(position, definitionAsString):
    for attr in position.Attributes():
        if attr.DefinitionAsString() == definitionAsString:
            return attr.AttributeValue()
    return None


class PositionSummary(object):

    def __init__(self):
        self._newPositions = []
        self._existingPositions = []

    def NewPositions(self, positionOid=None):
        if positionOid is not None:
            self._newPositions.append(positionOid)
        return self._newPositions

    def ExistingPositions(self, positionOid=None):
        if positionOid is not None:
            self._existingPositions.append(positionOid)
        return self._existingPositions


class PositionCreator(object):

    def __init__(self, positionSpec, transHandler=ACMHandler()):
        self._positionSpec = positionSpec
        self._transHandler = transHandler
        self._attrDefs = positionSpec.AttributeDefinitions()
        self._attrDefsPosAt = dict((k, v) for v, k in enumerate(self._attrDefs))     
        self._positions = None

    def FindOrCreatePositions(self, trades, PositionSummary=None):
        positions = []
        self._ResetPositions()
        for values in self._AttrValuesSet(trades):
            position = self._GetPosition(values)
            if position is None:
                position = self._CreatePosition(values)
                if PositionSummary is not None:
                    PositionSummary.NewPositions(position.Oid())
            else:
                if PositionSummary is not None:
                    PositionSummary.ExistingPositions(position.Oid())
            positions.append(position)
        return positions

    def _Positions(self):
        if self._positions is None:
            self._positions = PositionsFromSpec(self._positionSpec)
        return self._positions

    def _ResetPositions(self):
        self._positions = None

    def _GetAttrValues(self, trade):
        values = []
        for attrDef in self._attrDefs:
            methodChain = attrDef.Definition().split('.')
            value = trade
            for methodName in methodChain:
                method = getattr(value, methodName, None)
                if method is None:
                    value = None
                    break
                else:                
                    value = method()
            values.append(str(value))
        return tuple(values)

    def _AttrValuesSet(self, trades):
        return set(self._GetAttrValues(trade) for trade in trades)

    def _GetPosition(self, values):
        definitionsLen = len(self._attrDefs)
        for position in self._Positions():
            attrs = position.Attributes()
            if len(attrs) != definitionsLen:
                continue
            for attr in attrs:
                attrDefIndex = self._attrDefsPosAt[attr.Definition()]
                if values[attrDefIndex] != attr.AttributeValue():
                    break
            else:
                return position
        return None

    def _CreateAttr(self, attrDef, position, value):
        posAttr = acm.FPositionAttribute()
        posAttr.Specification(self._positionSpec)
        posAttr.Definition(attrDef)
        posAttr.AttributeValue(value)
        posAttr.PositionInstance(position)
        return posAttr

    def _CreatePosition(self, values):
        postion = None
        with self._transHandler.Transaction():
            position = acm.FCalculationRow()
            self._transHandler.Add(position)
            for attrDefIndex, value in enumerate(values):
                attrDef = self._attrDefs[attrDefIndex]
                attr = self._CreateAttr(attrDef, position, value)
                self._transHandler.Add(attr)
        return position
