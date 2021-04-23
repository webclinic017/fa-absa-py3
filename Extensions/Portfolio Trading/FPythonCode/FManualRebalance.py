""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FManualRebalance.py"
"""--------------------------------------------------------------------------
MODULE
    FManualRebalancing

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Subclass to FTradeProgramAction
    FManualRebalancing gives a user the possibility to create a trade program
    that changes the disposition of one or several positions to match input
    values in terms of one specified column. These input values can be either
    of type difference or target. They can be relative(percentage) or absolute.
    Lastly, if they are relative they can either refer to itself or to a parent row.
    Difference: Trades are generated so that the specified column changes exactly
    as much as the input value.
    Target: Trades are generated so that the specified column becomes exactly
    equal to the input value.

-----------------------------------------------------------------------------"""
import acm
from FTradeProgramUtils import CandidateTradeCreator
from FQuantityCalculator import QuantityCalculator
from FTradeCreator import TradeFromRowCreator
import FSheetUtils

class FManualRebalance(object):

    def __init__(self, rowsAndInputs, columnId, isTarget, 
                 relativeToEnum=None):
        self.relativeToEnum = relativeToEnum
        self.rowsAndInputs = rowsAndInputs
        self.isTarget = isTarget
        self.columnId = columnId
        self.trades = self.Trades()
    
    @staticmethod
    def _PortfolioRow(row):
        portfolio = TradeFromRowCreator.Portfolio(row)
        try:
            return acm.Risk.CreatePortfolioInstrumentAndTrades(portfolio)
        except RuntimeError as e:
            raise Exception('Could not find portfolio from row {0}'.format(row))
    
    def Trades(self):
        trades = []
        for row, inputValue, currency in self.rowsAndInputs:
            creator = CandidateTradeCreator(row)
            trade = creator.CreateTrade()
            relativeTo = None
            if self.relativeToEnum == 'Top':
                relativeTo = FSheetUtils.TopRow(row)
            elif self.relativeToEnum == 'Parent':
                relativeTo = row.Parent()
            elif self.relativeToEnum == 'Portfolio':
                relativeTo = self._PortfolioRow(row)
            elif self.relativeToEnum == 'Self':
                relativeTo = row
            quantity = QuantityCalculator(
                row, trade, self.columnId, 
                relativeTo, self.isTarget, currency).Quantity(inputValue)
            trade.Quantity(quantity)
            trades.append(trade)
        return trades
