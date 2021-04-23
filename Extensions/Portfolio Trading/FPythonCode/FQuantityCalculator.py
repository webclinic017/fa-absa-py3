""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FQuantityCalculator.py"
"""--------------------------------------------------------------------------
MODULE
    FQuantityCalculator

    (c) Copyright 2016 FIS Global. All rights reserved.

DESCRIPTION
    Class used to calculate the quantity needed for a trade to
-----------------------------------------------------------------------------"""

import acm
import math
from FTradeProgramUtils import Logger
from contextlib import contextmanager
import FSheetUtils

SPACE_COLLECTION = acm.Calculations().CreateCalculationSpaceCollection()

def GetCalcSpace():
    return SPACE_COLLECTION.GetSpace('FPortfolioSheet', acm.GetDefaultContext())

class QuantityCalculator(object):

    CURRENCY_COLUMNID = 'Portfolio Currency'

    def __init__(self, targetRow, trade, targetColumn,
                 relativeTo=None, isTarget=False, curr=None):
        self._targetRow = targetRow
        self._trade = acm.FTrade()
        self._trade.Apply(trade)
        self._relativeTo = relativeTo
        self._isTarget = isTarget
        self._currency = curr
        self._targetColumn = targetColumn
        self._grouper = FSheetUtils.GetGrouper(FSheetUtils.TopRow(targetRow))

    def Quantity(self, inputValue):
        if self._trade is not None:
            targetTopNode = self._TopNode(self._targetRow)
            relativeToTopNode = self._TopNode(self._relativeTo)
            with self._SubNodes(targetTopNode, relativeToTopNode) as (relativeNode, targetNode):
                Logger().debug('Input value {0}'.format(inputValue))
                if self._relativeTo:
                    inputValue = self._InputAsRelative(inputValue, relativeNode)
                if self._isTarget:
                    inputValue -= self._TargetValue(targetNode)
                quantity = (inputValue / self._GetDelta()
                            if inputValue else 0)
                Logger().debug('Quantity {0}'.format(quantity))
                roundedQuantity = self._RoundQuantity(quantity)
                Logger().debug('Quantity rounded {0}'.format(roundedQuantity))
                return roundedQuantity
        return 0

    def _InputAsRelative(self, inputValue, relativeNode):
        Logger().debug('Relative to {0}'.format(
            self._relativeTo.StringKey()))
        relativeValue = self._GetValue(relativeNode)
        inputValue = 0.01 * inputValue * relativeValue
        Logger().debug('Relative To value {0}'.format(relativeValue))
        return inputValue

    def _TargetValue(self, targetNode):
        targetValue = self._GetValue(targetNode)
        Logger().debug('Target {0}'.format(self._targetRow.StringKey()))
        Logger().debug('Target value {0}'.format(targetValue))
        return targetValue
    
    def _TopNode(self, row):
        if row:
            topRow = FSheetUtils.TopRow(row)
            portfolio = topRow.Portfolio()
            grouper = FSheetUtils.GetGrouper(topRow)
            return Node(portfolio, grouper=grouper)
        else:
            return None        
        
    
    @contextmanager
    def _SubNodes(self, targetTopNode, relativeToTopNode):
        try:
            relativeToNode, targetNode = None, None
            if self._relativeTo:
                relativeToNode = FindNode(relativeToTopNode, self._relativeTo)
            if self._isTarget:
                targetNode = FindNode(targetTopNode, self._targetRow)
            yield relativeToNode, targetNode
        except Exception as e:
            Logger().error('Couldn\'t calculate a valid quantity for {0}'
                           ''.format(self._targetRow.StringKey()))
            Logger().debug(e, exc_info=True)
        finally:
            self._Flush()

    def _Flush(self):
        if self._trade is not None:
            self._trade.Unsimulate()

    def _SetupPortfolio(self):
        self._trade.Quantity(1)
        self._trade.Status('FO Confirmed')
        self._trade.Simulate()
        portfolio = acm.FAdhocPortfolio()
        portfolio.Add(self._trade)
        return portfolio

    def _GetTargetKey(self):
        instrument = self._trade.Instrument()
        if instrument.IsKindOf(acm.FCurrency):
            return '/'.join((instrument.Name(),
                             self._trade.Currency().Name()))
        return instrument.Name()
    
    def _GetDelta(self):
        portfolio = self._SetupPortfolio()
        target = self._GetTargetKey()
        node = Node(item=portfolio, target=target, grouper=self._grouper)
        delta = self._GetValue(node)
        Logger().debug('Delta {0}'.format(delta))
        if not delta:
            Logger().debug('Column {0} value remained unchanged by new trade in {1}'
                           ''.format(self._targetColumn, self._trade.Instrument().Name()))
        elif math.isnan(delta):
            Logger().debug('Column {0} value is NaN for {1} position'
                           ''.format(self._targetColumn, node.Item().StringKey()))
            return 0
        return delta

    def _GetValue(self, node, targetColumn=None):
        space = GetCalcSpace()
        if self._currency:
            space.SimulateValue(node, self.CURRENCY_COLUMNID, self._currency)
        try:
            value = space.CalculateValue(node, targetColumn or self._targetColumn)
            return value.Number()
        except AttributeError:
            return value or 0
        except RuntimeError:
            return 0
        finally:
            space.RemoveSimulation(node, self.__class__.CURRENCY_COLUMNID)

    def _RoundQuantity(self, quantity):
        base = self._trade.Instrument().MinimumIncremental() or 1
        rounded = round(quantity / base) * base
        return (rounded if not
                acm.Math.AlmostZero(rounded, 1.e-10)
                else 0)
        
class NodeCache(object):

    def __init__(self, func):
        self._func = func
        self._cache = {}

    def __call__(self, item, target=None, grouper=None):
        if target is not None:
            return self._func(item, target, grouper)
        key = (item, grouper)
        if key not in self._cache:
            value = self._func(item, target, grouper)
            self._cache[key] = value
            return value
        GetCalcSpace().Refresh()
        return self._cache[key]

@NodeCache
def Node(item, target=None, grouper=None):
    assert item, 'Can\'t insert nil object in calculation space.'
    space = GetCalcSpace()
    node = space.InsertItem(item)
    if grouper is not None:
        node.ApplyGrouper(grouper)
    space.Refresh()
    if target is not None:
        targetIter = node.Iterator().Find(target)
        while targetIter and targetIter.Tree().Item().IsKindOf(acm.FSingleInstrumentAndTrades) is False:
            try:
                targetIter = targetIter.FirstChild().Find(target)
            except AttributeError:
                break
        if targetIter:
            return targetIter.Tree()
    return node


def GetPath(treeSpecification):
    limitTarget = acm.FLimitTarget()
    limitTarget.TreeSpecification(treeSpecification)
    return limitTarget.Path()

def FindNode(topNode, row):
    spec = acm.Limits.TreeSpecificationForObject(row)
    if spec.Grouper() is None:
        grouping = row.Grouping()
        grouper = grouping.Grouper() if grouping else acm.FDefaultGrouper()
        spec.Grouper(grouper)
    try:
        return topNode.Iterator().Find(spec).Tree()
    except Exception as e:
        Logger().error('Failed to find path ({0})'.format(GetPath(spec)))
        Logger().debug(e, exc_info=True)