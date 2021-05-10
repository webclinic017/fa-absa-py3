""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FClosePosition.py"
"""--------------------------------------------------------------------------
MODULE
    FClosePosition

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This Trade Program Action will enable you to fully close out a position,
    that is you will get a trade program of candidate trades that negates
    you current position.
-----------------------------------------------------------------------------"""
from FTradeProgramUtils import CandidateTradeCreator
from FQuantityCalculator import QuantityCalculator


class FClosePosition(object):

    def __init__(self, instrumentRows, columnId):
        self.instrumentRows = instrumentRows
        self.columnId = columnId
    
    def Trades(self):
        trades = []
        for row in self.instrumentRows:
            trade = CandidateTradeCreator(row).CreateTrade()
            quantity = QuantityCalculator(row, trade, 
                self.columnId, isTarget=True).Quantity(0)
            if quantity:
                trade.Quantity(quantity)
                trades.append(trade)
        return trades
