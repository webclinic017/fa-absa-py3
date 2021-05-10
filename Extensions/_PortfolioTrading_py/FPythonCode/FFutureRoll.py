""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FFutureRoll.py"
"""--------------------------------------------------------------------------
MODULE
    FFutureRoll

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
from FTradeProgramUtils import Logger, CandidateTradeCreator
from FQuantityCalculator import QuantityCalculator

class FFutureRoll(object):

    def __init__(self, rowsAndInputs, columnId):
        self.rowsAndInputs = rowsAndInputs
        self.columnId = columnId

    def Trades(self):
        trades = []
        for row, contract, _curr in self.rowsAndInputs:
            rollTrade = self.RollTrade(row, contract)
            closeTrade = self.CloseTrade(row)
            if rollTrade and closeTrade:
                trades.extend([rollTrade, closeTrade])
            else:
                Logger().info('No trades created for {0}'.format(contract))
        return trades

    def RollTrade(self, row, contract):
        contract = acm.FInstrument[contract]
        creator = CandidateTradeCreator(row, contract)
        rollTrade = creator.CreateTrade()
        rollQuantity = QuantityCalculator(
            row, rollTrade,
            self.columnId, relativeTo=row).Quantity(100)
        if rollQuantity:
            rollTrade.Quantity(rollQuantity)
            return rollTrade

    def CloseTrade(self, row):
        creator = CandidateTradeCreator(row)
        closeTrade = creator.CreateTrade()
        closeQuantity = QuantityCalculator(
            row, closeTrade,
            self.columnId, isTarget=True).Quantity(0)
        if closeQuantity:
            closeTrade.Quantity(closeQuantity)
            return closeTrade

