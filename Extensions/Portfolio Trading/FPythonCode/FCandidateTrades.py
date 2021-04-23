""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FCandidateTrades.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCandidateTrades

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    CandidateTrades implements logic to keep track of all performed trade program actions and 
    their respective candidate trades. It also makes sure to simulate, unsimulate and delete 
    cadidate trades when needed. 
-------------------------------------------------------------------------------------------------"""

import acm
import itertools
from collections import defaultdict

class CandidateTrades(object):
    
    def __init__(self, simulateTrades=True): 
        self._tradesPerAction = defaultdict(list)
        self._simulateTrades = simulateTrades
    
    def AddTrades(self, action, trades):
        self.ClearAction(action)
        tradesToAdd = list(self._TradesToInclude(trades))
        if tradesToAdd:
            self._tradesPerAction[action].extend(tradesToAdd)
            if self._simulateTrades:
                self._Simulate(tradesToAdd)
    
    def Trades(self):
        """ Returns flattened list of all candidate trades for all actions """
        return list(itertools.chain.from_iterable(list(self._tradesPerAction.values())))
    
    def ClearAction(self, action):
        if action in self._tradesPerAction and not action.AppendTradesForSameAction():
            trades = self._tradesPerAction.pop(action)
            self._ClearTrades(trades)
                
    def SimulateAllTrades(self):
        for trades in list(self._tradesPerAction.values()):
            self._Simulate(trades)
            
    def UnsimulateAllTrades(self):
        for action in list(self._tradesPerAction.keys()):
            self._Unsimulate(action)
    
    def ClearAll(self):
        for trades in list(self._tradesPerAction.values()):
            self._ClearTrades(trades)
        self._tradesPerAction = defaultdict(list)
    
    def AlwaysSimulateTrades(self, simulateTrades):
        self._simulateTrades = simulateTrades
        if self._simulateTrades:
            self.SimulateAllTrades()
        else:
            self.UnsimulateAllTrades()
    
    def _Simulate(self, trades):
        for trade in trades:
            trade.Simulate()
            
    def _Unsimulate(self, action):       
        unsimulatedTrades = []
        for trade in self._tradesPerAction.get(action, []):
            newTrade = acm.FTrade()
            newTrade.Apply(trade)
            unsimulatedTrades.append(newTrade)
            trade.Unsimulate()
        self._tradesPerAction[action] = unsimulatedTrades
        
    def _ClearTrades(self, trades):
        for trade in trades:
            trade.Unsimulate()
    
    @classmethod
    def _TradesToInclude(cls, trades):
        return [trade for trade in trades if cls._ShouldBeIncluded(trade)]
        
    @classmethod
    def _ShouldBeIncluded(cls, trade):
        return not cls._IsZeroQuantity(trade)

    @classmethod
    def _IsZeroQuantity(cls, trade):
        return acm.Math.AlmostZero(trade.Quantity(), 1.e-10)


class PlaceholderTrades(CandidateTrades):
    
    @classmethod
    def _ShouldBeIncluded(cls, trade):
        return True
