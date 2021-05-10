""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionElectionPosition.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCorpActionElectionPosition

DESCRIPTION

-------------------------------------------------------------------------------------------------"""
import acm
import math
from FCorpActionUtils import PortfolioFromInstance

from contextlib import contextmanager

__all__ = ['Position', 
           'PositionCalculator']


class Position(object):

    def __init__(self, obj, value):
        self._obj = obj
        self._value = value
        
    def Instrument(self):
        return self._obj.Instrument()
        
    def Trades(self):
        return self._obj.Trades().AsArray()
            
    def Value(self):
        try:
            retval = float(self._value)
            if retval != 0.0:
                return retval
            else:
                trades = self.Trades()
                if len(trades) == 1:
                    if trades[0].Status() == 'Simulated' and trades[0].Type() == 'Corporate Action':
                        return trades[0].Quantity()
                return 0
        except (TypeError, ValueError):
            return float('nan')
        
    def HasValue(self):
        return (bool(self.Value()) and 
                not math.isnan(self.Value()))
        
        
class PositionCalculator(object):

    _COLUMNID = 'Corp Action Eligible Position'
    _PARAM_COLUMNID = 'Corp Action Parameter'
    _spaceCollection = None

    def __init__(self, corpAction):
        self._action = corpAction
        self._space = None
        
    def Positions(self, positionInstance):
        positions = []
        with self._ApplyCorpAction():
            positions.extend(self._IterPositions(positionInstance))
        self._Flush()
        return positions
                               
    def HasEligiblePositions(self, positionInstance):
        retValue = False
        with self._ApplyCorpAction():
            for position in self._IterPositions(positionInstance):
                if position.HasValue() and abs(position.Value()) > 1:
                    retValue = True
                    break
        self._Flush()
        return retValue
    
    def EligiblePosition(self, positionInstance):
        eligiblePosition = 0
        with self._ApplyCorpAction():
            for position in self._IterPositions(positionInstance):
                eligiblePosition += position.Value()
        self._Flush()
        return eligiblePosition
    
    def EligiblePositions(self, trades, positionSpec):
        positions = []
        unionObject = acm.FAdhocPortfolio()
        unionObject.Name("Corporate Action Trades")
        unionObject.AddAll(trades)
        with self._ApplyCorpAction():
            groupers = []
            for attr in positionSpec.AttributeDefinitions():
                groupers.append(acm.FAttributeGrouper("Trade." + attr.Definition()))
                
            node = self._Space().InsertItem(unionObject)
            node.ApplyGrouper(acm.FChainedGrouper(groupers))
            self._Space().Refresh()
            for position in self._IterTrades(node):
                positions.append(position)
        self._Flush()
        return positions
        
    def _IterPositions(self, instance):
        node = self._Space().InsertItem(PortfolioFromInstance(instance))
        self._Space().Refresh()
        nodeIter = node.Iterator()
        while nodeIter.NextUsingDepthFirst():
            tree = nodeIter.Tree()
            yield Position(tree.Item(), 
                           self._Value(tree))
    
    def _IterTrades(self, node):
        nodeIter = node.Iterator()
        while nodeIter.NextUsingDepthFirst():
            tree = nodeIter.Tree()
            yield Position(tree.Item(), 
                           self._Value(tree))
        
    @contextmanager
    def _ApplyCorpAction(self):
        try:
            self._Space().SimulateGlobalValue(self._PARAM_COLUMNID,
                                              self._action)
            yield
        finally:
            self._Space().RemoveGlobalSimulation(self._PARAM_COLUMNID)

    def _Value(self, tree):
        return self._Space().CalculateValue(tree, self._COLUMNID)

    def _SpaceCollection(self):
        if self._spaceCollection is None:
            self._spaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
        return self._spaceCollection

    def _Space(self):
        if self._space is None:
            self._space = self._SpaceCollection().GetSpace(
                    'FPortfolioSheet',
                    acm.GetDefaultContext(),
                    None, False)
        return self._space
        
    def _Flush(self):
        self._Space().Clear()
        self._space = None
        for eb in acm.FCache.Select01('.StringKey="evaluator builders"', None).Contents():
            eb.Reset()
        acm.Memory.GcWorldStoppedCollect()

