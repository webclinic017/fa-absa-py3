""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendReturnDeal.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendReturnDeal

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Deal entry for returning of security loans.

------------------------------------------------------------------------------------------------"""
import itertools

import acm
from DealPackageDevKit import (DealPackageDefinition, CustomActions, Settings,
                               Float, Object, Action)
from DealPackageUtil import IsFObject
import FSecLendUtils
import FUxCore
import FSecLendHooks


class ReturnAction(FSecLendUtils.ActionCommandActionBase):
    DISPLAY_NAME = 'Return'
    ATTRIBUTE_NAME = 'returnLoans'


@CustomActions(submit=ReturnAction)
@Settings(MultiTradingEnabled=False, GraphApplicable=False, SheetApplicable=False)
class FSecLendReturnDefinition(DealPackageDefinition):

    loans  =            Object( label='Stocks',
                                domain='FSortedCollection(FTrade)',
                                elementDomain='FTrade',
                                objMapping='Loans',
                                columns='@LoanColumns',
                                onSelectionChanged='@SetSelectedLoan')

    selectedLoan =      Object(domain='FTrade')

    quantity =           Float( label='Return Qty',
                                formatter='InstrumentDefinitionNominal',
                                backgroundColor='@QuantityBackgroundColor')

    update =            Action( label='Update',
                                action='@OnUpdateLoan',
                                enabled='@UpdateLoanEnabled')

    returnLoans =       Action( label='Return',
                                action='@OnReturnLoans',
                                enabled='@ReturnLoansEnabled')

    # *************************************************
    # Object/Value Mapping

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanReturn')

    def Loans(self):
        return self._loans

    # *************************************************
    # Callbacks

    def LoanColumns(self, *args):
        return [{'label': 'ID',                 'methodChain': 'OriginalOrSelf.StorageId'},
                {'label': 'Stock Loan',         'methodChain': 'Instrument.VerboseName'},
                {'label': 'Isin',               'methodChain': 'Instrument.Underlying.Isin'},
                {'label': 'Created',            'methodChain': 'TradeTime'},
                {'label': 'Rate/Fee',           'methodChain': 'Instrument.FirstFixedLeg.FixedRate'},
                {'label': 'Orig. Qty',          'methodChain': 'FaceValue'},
                {'label': 'Return Qty',         'methodChain': 'Tax'}]

    def OnReturnLoans(self, *args):
        today = acm.Time.DateToday()
        closingTrades = acm.FArray()
        for t in self.loans:
            ct = acm.TradeActions.CloseTrade(
                t.OriginalOrSelf(), today, today, t.Tax() * -1, t.Premium() * -1, [])
            ct.Status(FSecLendHooks.ReturnTradeStatus())
            closingTrades.Add(ct)
        closingTrades.Commit()

    def OnUpdateLoan(self, *args):
        if self.selectedLoan:
            remainingQty = FSecLendUtils.RemainingNominal(self.selectedLoan)
            returnQty = (-1 if remainingQty < 0 else 1) * abs(self.quantity)
            if abs(returnQty) > abs(remainingQty):
                returnQty = remainingQty
            self.selectedLoan.Tax(returnQty)

    def QuantityBackgroundColor(self, *args):
        if self.selectedLoan:
            direction = 'Buy' if self.selectedLoan.Quantity() >= 0 else 'Sell'
            return 'BkgSecurityLoanPriceRequest' + direction

    def ReturnLoansEnabled(self, *args):
        for loan in self.loans:
            if not loan.Tax():      # Placeholder for return qty
                return False
        return not self.loans.IsEmpty()

    def SetSelectedLoan(self, attributeName, selectedLoan):
        self.selectedLoan = selectedLoan
        if self.selectedLoan:
            self.quantity = abs(self.selectedLoan.Tax())    # Placeholder for return qty

    def UpdateLoanEnabled(self, *args):
        return bool(self.selectedLoan)

    # *************************************************
    # Deal Package Interface Methods

    def AssemblePackage(self, optArg=None):
        def CreatePlaceholderTrade(trade):
            nominalRemaining = FSecLendUtils.RemainingNominal(trade)
            order = trade.Clone()
            order.Tax(nominalRemaining)     # Placeholder for return qty
            return order

        trades = FSecLendUtils.TradesFromObject(optArg)
        if trades:
            self._loans.AddAll([CreatePlaceholderTrade(t) for t in trades])

    def OnInit(self):
        self._loans = acm.FSortedCollection()

    def OnCopy(self, original, aspect):
        if str(aspect) == 'copying':
            self._loans.Clear()
            self._loans.AddAll(original.GetAttribute('loans'))

    def OnSave(self, saveConfig):
        # TODO: Disable once support toolbar customisation is available on the web
        #raise NotImplementedError('Cannot save stock loan return deal package')
        if self.ReturnLoansEnabled():
            self.OnReturnLoans()


class StartSecurityLoanReturnMenuItem(FUxCore.MenuItem):
    def Invoke(self, eii):
        StartSecurityLoanReturnApplication(eii)


def StartSecurityLoanReturnApplication(*args):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Security Loan Return')

def CreateStartSecurityLoanReturnMenuItem(eii):
    return StartSecurityLoanReturnMenuItem()
