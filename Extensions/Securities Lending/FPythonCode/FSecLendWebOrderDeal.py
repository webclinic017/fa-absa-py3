""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendWebOrderDeal.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendWebOrderDeal

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order entry deal for multiple security loan instruments in Arena Web.

------------------------------------------------------------------------------------------------"""
import acm
import ACMPyUtils
from DealPackageDevKit import (DealPackageDefinition, Settings, DealPackageUserException,
                               Str, Float, Object, Text, Action, AttributeDialog,
                               CustomActions, DealPackageChoiceListSource)
import FSecLendUtils
import FSecLendHooks

from FTradeStreamBase import FStreamReader, ParsingError
StreamReader = FStreamReader()

class SubmitOrderAction(FSecLendUtils.ActionCommandActionBase):
    DISPLAY_NAME = 'Submit'
    ATTRIBUTE_NAME = 'submit'

@CustomActions(submit=SubmitOrderAction)
@Settings(MultiTradingEnabled=False, GraphApplicable=False, SheetApplicable=False)
class FSecLendWebOrderDefinition(DealPackageDefinition):

    orders =            Object( label='Orders',
                                domain='FSortedCollection(FTrade)',
                                elementDomain='FTrade',
                                dialog=AttributeDialog(
                                    label='Edit order',
                                    customPanes='@EditDialogPanes',
                                    btnLabel='Update'),
                                onDoubleClick='@OnOrderDoubleClicked',
                                objMapping='Orders',
                                columns='@OrderColumns',
                                onSelectionChanged='@SetSelectedOrder' )

    selectedOrder =     Object( domain='FTrade' )

    add =               Action( label='Add',
                                dialog=AttributeDialog(
                                    label='Add new order',
                                    customPanes='@EditDialogPanes',
                                    btnLabel='Add'),
                                action='@OnAddOrder' )

    remove =            Action( label='Remove',
                                action='@RemoveOrder',
                                enabled='@HasSelectedOrder' )

    edit =              Action( label='Edit',
                                dialog=AttributeDialog(
                                    label='Edit order',
                                    customPanes='@EditDialogPanes',
                                    btnLabel='Update'),
                                action='@OnUpdateOrder',
                                enabled='@HasSelectedOrder' )

    clipboard =           Text( label='',
                                height=200,
                                width=400 )

    import_ =           Action( label='Import',
                                dialog=AttributeDialog(
                                    label='Paste clipboard contents here',
                                    customPanes='@ImportDialogPanes',
                                    btnLabel='Import'),
                                action='@OnImport' )

    underlying =        Object( label='Stock',
                                domain='FStock',
                                choiceListSource='@UnderlyingChoices',
                                onChanged='@OnUnderlyingChanged',
                                transform='@TransformInstrument' )

    buySell =              Str( label='Quantity',
                                choiceListSource=['Borrow', 'Lend'],
                                defaultValue='Borrow',
                                maxWidth=15,
                                backgroundColor='@QuantityBackgroundColor',
                                onChanged='@OnBuySellChanged' )

    quantity =           Float( label='',
                                formatter='InstrumentDefinitionNominal',
                                onChanged='@OnQuantityChanged',
                                backgroundColor='@QuantityBackgroundColor' )

    price =              Float( label='@PriceLabel',
                                formatter='InstrumentDefinitionStrikePrice',

                                enabled=True )

    submit =            Action( label='Submit',
                                action='@OnSubmit',
                                enabled='@SubmitEnabled' )

    # *************************************************
    # UI Panes

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanOrder')

    def EditDialogPanes(self, *args):
        return self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanOrderEdit')

    def ImportDialogPanes(self, *args):
        return self.GetCustomPanesFromExtValue('CustomPanes_SecurityLoanOrderImport')

    # *************************************************
    # Object/Value Mapping

    def Orders(self):
        return self._orders

    def OrderColumns(self, *args):
        return [{'label': 'Stock',          'methodChain': 'Instrument.Underlying.VerboseName'},
                {'label': 'Isin',           'methodChain': 'Instrument.Underlying.Isin'},
                {'label': 'Borrow/Lend',    'methodChain': 'Direction'},
                {'label': 'Quantity',       'methodChain': 'Quantity'},
                {'label': 'Fee/Rate',       'methodChain': 'Instrument.FirstFixedLeg.StartingFee'}]

    def UnderlyingChoices(self, *args):
        return self._underlyings

    # *************************************************
    # Callbacks

    def HasSelectedOrder(self, *args):
        return bool(self.selectedOrder)

    def OnAddOrder(self, name, add):
        if add and self.underlying:
            instrument = FSecLendUtils.CreateInstrument(self.underlying)
            trade = FSecLendUtils.CreateTrade(instrument)

            direction = self.Direction(self.quantity)
            FSecLendUtils.SetSource(trade, 'Arena Web')
            trade.Counterparty(FSecLendHooks.ClientCounterparty(acm.User()))
            FSecLendUtils.SetSecurityLoanRate(trade, self.price/100)
            FSecLendUtils.SetTradeQuantity(trade, direction * abs(self.quantity))
            self.SetSelectedOrder(None, trade)
            trade.Acquirer(FSecLendHooks.DefaultAcquirer())
            FSecLendHooks.OnAddWebOrder(trade)
            self.orders.Add(trade)

    def OnBuySellChanged(self, name, oldValue, newValue, *args):
        self.SetAttribute('quantity', self.Direction() * abs(self.quantity), silent=True)
        self.UpdatePrice()

    def OnImport(self, name, run):
        if run and self.clipboard:
            try:
                trades = StreamReader.TradesFromString(self.clipboard, Source='Arena Web', Reference="ClipBoard")
                for t in trades:
                    # Trades are created from trader perspective - invert the quantity
                    # to reflect the clients point of view here
                    FSecLendUtils.SetTradeQuantity(t, -1 * t.FaceValue())
                    t.Counterparty(FSecLendHooks.ClientCounterparty(acm.User()))
                self.orders.AddAll(trades)
                self.clipboard = ''
            except ParsingError:
                raise DealPackageUserException('Could not parse clipboard contents for order information.')

    def OnUnderlyingChanged(self, name, oldValue, newValue, *args):
        self.UpdatePrice(underlying=newValue)

    def OnOrderDoubleClicked(self, name, item, update):
        return self.OnUpdateOrder(name, update)

    def OnQuantityChanged(self, name, oldValue, newValue, *args):
        self.UpdateBuySell(newValue)
        self.SetAttribute('quantity', newValue, silent=True)

    def OnSubmit(self, *args):
        with ACMPyUtils.Transaction():
            instruments = acm.FArray()
            instruments.AddAll([t.Instrument() for t in self.orders])
            instruments.Commit()
            self.orders.Commit()

    def OnUpdateOrder(self, name, update):
        if update:
            if self.selectedOrder.Instrument().Underlying() != self.underlying:
                instrument = FSecLendUtils.CreateInstrument(self.underlying)
                self.selectedOrder.Instrument(instrument)
            FSecLendUtils.SetTradeQuantity(self.selectedOrder, self.Direction() * abs(self.quantity))
            FSecLendUtils.SetSecurityLoanRate(self.selectedOrder, self.price/100)
            self.SetAttribute('price', self.price/100, silent=True)
            self.SetAttribute('quantity', self.Direction() * abs(self.quantity), silent=True)

            for n, i in enumerate(self.orders):
                if i.Oid() == self.selectedOrder.Oid():
                    self.orders.Remove(i)
                    self.orders.AtInsert(n, self.selectedOrder)

    def PriceLabel(self, *args):
        return 'Fee' if self.Direction() > 0 else 'Rate'

    def QuantityBackgroundColor(self, *args):
        # Colours from customer's perspective (opposite of trader)
        direction = 'Buy' if self.buySell == 'Borrow' else 'Sell'
        return 'BkgSecurityLoanPriceRequest' + direction

    def RemoveOrder(self, *args):
        self.orders.Remove(self.selectedOrder)
        self.selectedOrder = None

    def SetSelectedOrder(self, name, selectedOrder):
        self.selectedOrder = selectedOrder
        if self.selectedOrder:
            self.underlying = self.selectedOrder.Instrument().Underlying()
            self.quantity = self.selectedOrder.Quantity()
            self.buySell = self.BuySellValue(self.selectedOrder.FaceValue())
            self.price = self.selectedOrder.Instrument().FirstFixedLeg().StartingFee()*100

    def SubmitEnabled(self, *args):
        for order in self.orders:
            if not order.Quantity():
                return False
        return not self.orders.IsEmpty()

    def TransformInstrument(self, name, value):
        if isinstance(value, str):
            return acm.FInstrument[value]
        return value

    # *************************************************
    # Misc. Util Methods

    def BuySellValue(self, quantity):
        return 'Lend' if quantity < 0 else 'Borrow'

    def Direction(self, buySellValue=None):
        if buySellValue is None:
            buySellValue = self.buySell
        return -1 if buySellValue == 'Lend' else 1

    def UpdateBuySell(self, quantity):
        self.SetAttribute('buySell', self.BuySellValue(quantity), silent=True)

    def UpdatePrice(self, underlying=None):
        underlying = underlying or self.underlying
        #q>0 borrow in, price is always positive
        trade = FSecLendUtils.TradeFromInstrument(underlying)
        trade.Counterparty(FSecLendHooks.ClientCounterparty(acm.User()))
        FSecLendUtils.SetSource(trade, 'Arena Web')
        self.price = FSecLendUtils.SetDefaultRate(trade)*100


    def UpdateUnderlyingChoices(self, *args):
        self._underlyings.Clear()
        loans = acm.FSecurityLoan.Select('underlyingType="Stock" and generic=True')
        underlyings = [l.Underlying() for l in loans if l.Underlying()]
        self._underlyings.AddAll(sorted(underlyings))

    # *************************************************
    # Deal Package Interface Methods


    def AssemblePackage(self, optArg=None):
        def CreatePlaceholderTrade(trade):
            nominalRemaining = FSecLendUtils.RemainingNominal(trade)
            order = trade.Clone()
            order.Tax(nominalRemaining)     # Placeholder for return qty
            return order

        if optArg:
            trades = FSecLendUtils.TradesFromObject(optArg)
            if trades:
                self._orders.AddAll([CreatePlaceholderTrade(t) for t in trades])

    def OnInit(self):
        self._underlyings = DealPackageChoiceListSource()
        self._orders = acm.FSortedCollection()

    def OnNew(self):
        self.UpdateUnderlyingChoices()

    def OnCopy(self, original, aspect):
        if str(aspect) == 'copying':
            self.UpdateUnderlyingChoices()
            self._orders.Clear()
            self._orders.AddAll(original.GetAttribute('orders'))

    def OnSave(self, saveConfig):
        # TODO: Disable once support toolbar customisation is available on the web
        #raise NotImplementedError('Cannot save order deal package')
        if self.SubmitEnabled():
            self.OnSubmit()



@CustomActions(submit=SubmitOrderAction)
@Settings(MultiTradingEnabled=False, GraphApplicable=False, SheetApplicable=False)
class FSecLendWebOrderSelection(FSecLendWebOrderDefinition):
    pass
