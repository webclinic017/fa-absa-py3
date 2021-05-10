""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FOpenPosition.py"
"""--------------------------------------------------------------------------
MODULE
    FOpenPosition

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
from FQuantityCalculator import QuantityCalculator


class FOpenPosition(object):

    def __init__(self, row, trade, columnId, inputValue):
        self.row = row
        self.columnId = columnId
        self.trade = trade
        self.inputValue = inputValue

    def Trade(self):
        quantity = QuantityCalculator(
            targetRow=self.row,
            trade=self.trade,
            targetColumn=self.columnId,
            isTarget=False
            ).Quantity(self.inputValue)
        if quantity:
            self.trade.Quantity(quantity)
        return self.trade
