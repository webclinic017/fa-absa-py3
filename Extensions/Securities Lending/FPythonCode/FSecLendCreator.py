""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendCreator.py"
from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendCreator

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for the creation of security loan instruments and trades.

------------------------------------------------------------------------------------------------"""
import acm
from ACMPyUtils import Transaction
import contextlib
import FSecLendUtils
from FSecLendDealUtils import SecurityLoanCreator
import FSecLendHooks

def TradeFromInstrument(underying, **kwargs):
    loan = FSecLendUtils.CreateInstrument(underying, **kwargs)
    return SecurityLoanCreator.CreateTrade(loan) if loan else None

class SecurityLoanTrades(object):

    def __init__(self, portfolio, listener=None):
        self._trades = acm.FArray()
        self._portfolio = portfolio
        self._updating = False
        self._listener = listener

    def __iter__(self):
        return iter(self._trades)

    def __nonzero__(self):
        return bool(self._trades)

    def __len__(self):
        return len(self._trades)

    def __call__(self):
        return self._trades

    def Add(self, trade):
        trade.Simulate()
        self._trades.Add(self.SetAttributes(trade))
        trade.AddDependent(self)
        self.UpdateListener('OnTradeAdded', trade)

    def AddAll(self, trades):
        for trade in trades:
            self.Add(trade)

    def AssertValidity(self):
        for trade in self:
            assert trade.Counterparty(), 'Missing counterparty'
            assert trade.FaceValue() != 0, 'Quantity must not be zero'
            FSecLendHooks.AssertTradeValidity(trade)

    def Clear(self):
        if self._trades:
            while not self._trades.IsEmpty():
                self.Remove(self._trades.First())

    def Commit(self, chunkSize=50):
        for chuned_trades in [self._trades[x:x+chunkSize] for x in range(0, len(self._trades), chunkSize)]:
            with Transaction():
                for trade in chuned_trades:
                    if trade.Instrument().IsInfant():
                        trade.Instrument().Commit()
                    trade.Commit()
        return self._trades

    def Counterparty(self, trade, counterparty):
        with self._TradeUpdate():
            if trade.IsInfant():
                trade.Counterparty(counterparty)

    def Remove(self, trade):
        self._trades.Remove(trade)
        trade.RemoveDependent(self)
        self.UpdateListener('OnTradeRemoved', trade)

    def SetAttributes(self, trade):
        with self._TradeUpdate():
            if trade.IsInfant() and not trade.Status():
                trade.Status(FSecLendHooks.DefaultTradeStatus())
            return trade

    def ServerUpdate(self, trade, symbol, _params):
        aspect = str(symbol)
        if aspect == 'update' and not self._updating:
            self.SetAttributes(trade)
            self.UpdateListener('OnTradeUpdated', trade)
        elif aspect == 'delete':
            self.Remove(trade)

    def UpdateListener(self, methodName, trade):
        if self._listener:
            try:
                callback = getattr(self._listener, methodName)
                if callback:
                    callback(trade)
            except Exception as e:
                print('Error in trade collection callback', e)

    def UpdateTrades(self):
        for trade in self:
            self.SetAttributes(trade)

    @contextlib.contextmanager
    def _TradeUpdate(self):
        self._updating = True
        yield
        self._updating = False
