
import acm
from CashManagementHooksHelper import AdjustmentInitialAttributeValues,\
                                      FXRateFixingInitialSourceAttributeValues,\
                                      FXRateFixingInitialDestinationAttributeValues,\
                                      TransferInitialSourceAttributeValues,\
                                      TransferInitialDestinationAttributeValues

def AddCashPayment(trade, currency=None, paymentType='Cash', amount=0):
    payment = acm.FPayment()
    payment.Trade(trade)
    payment.RegisterInStorage()
    payment.Amount(amount)
    if currency:
        payment.Currency(currency)
    else:
        payment.Currency(trade.Currency())
    payment.Type(paymentType)
    trade.Payments().Add(payment)

def SetPaymentDates(payment, valueDay):
    dateToday = acm.Time().DateToday()
    if acm.Time().DateDifference(valueDay, dateToday) >= 0:
        # future date
        payment.PayDay(valueDay)
        payment.ValidFrom(dateToday)
    else:
        # historical date
        payment.PayDay(valueDay)
        payment.ValidFrom(valueDay)
    return

def CommonTradeInit(trade):
    if trade.Instrument().IsInfant():
        trade.Instrument(trade.Currency())
    if trade.IsInfant():
        trade.ValueDay(acm.Time().DateToday())        
    if not trade.Counterparty():
        trade.Counterparty('FMAINTENANCE')
    trade.AcquireDay(trade.ValueDay())
    trade.Quantity(0)
    trade.Price(0)
    trade.Premium(0)

def InitCashEntryTrade(trade):
    CommonTradeInit(trade)
    trade.Type('Cash Entry')
    if trade.Payments().IsEmpty():
        if trade.Instrument().IsKindOf(acm.FCurrency):
            trade.TradeCategory('Subscription')
            AddCashPayment(trade, paymentType='Subscription/Redemption', amount=1)
        else:
            trade.TradeCategory('Cash')
            AddCashPayment(trade, paymentType='Cash', amount=1)
    payment = trade.Payments().Element()
    SetPaymentDates(payment, trade.ValueDay())    

    if trade.Counterparty():
        payment.Party(trade.Counterparty())

def InitAccountAdjustmentTrade(trade):
    CommonTradeInit(trade)
    trade.Type('Account Adjustment')
    if trade.Payments().IsEmpty():
        trade.TradeCategory('Cash')
        AddCashPayment(trade, paymentType='Account Adjustment')
    payment = trade.Payments().Element()
    SetPaymentDates(payment, trade.ValueDay())    
    if trade.Counterparty():
        payment.Party(trade.Counterparty())

def InitAccountTransferTrade(trade):
    CommonTradeInit(trade)
    if not trade.Acquirer():
        trade.Acquirer('FMAINTENANCE')
    trade.Type('Account Transfer')  
    if trade.Payments().IsEmpty():
        trade.TradeCategory('Cash')
        AddCashPayment(trade, paymentType='Account Transfer')
    payment = trade.Payments().Element()
    SetPaymentDates(payment, trade.ValueDay())    
    if trade.Counterparty():
        payment.Party(trade.Counterparty())     

def InitCashTransferTrade(trade):
    CommonTradeInit(trade)
    if trade.IsInfant():
        trade.Status('Internal')
    if not trade.Acquirer():
        trade.Acquirer('FMAINTENANCE')
    trade.Type('Cash Transfer')  
    if trade.Payments().IsEmpty():
        trade.TradeCategory('None')
        AddCashPayment(trade, paymentType = 'Premium')

    payment = trade.Payments().Element()
    SetPaymentDates(payment, trade.ValueDay())    

    if trade.Counterparty():
        payment.Party(trade.Counterparty())
    
def InitCashFxRateFixingTrade(trade):
    CommonTradeInit(trade)
    if trade.IsInfant():
        trade.Status('Internal')
    if not trade.Acquirer():
        trade.Acquirer('FMAINTENANCE')
    trade.Type('FX Rate Fixing')

    if trade.Payments().IsEmpty():
        trade.TradeCategory('None')
        if trade.Instrument().IsKindOf(acm.FCurrency):
            AddCashPayment(trade, paymentType='Premium')
            AddCashPayment(trade, paymentType='Premium')
        else:
            AddCashPayment(trade, paymentType='Premium')
            AddCashPayment(trade, acm.UsedAccountingCurrency(), paymentType='Premium')
    for payment in trade.Payments():
        SetPaymentDates(payment, trade.ValueDay())    
        if trade.Counterparty():
            payment.Party(trade.Counterparty())    

def StartCashAdjustment(eii):
    return CashAdjustmentDialogMenuItemTM(eii)

def StartCashTransfer(extObj):
    return CashTransferDialogMenuItemTM(extObj)
    
def StartCashFxRateFixing(extObj):
    return CashFXRateFixingDialogMenuItemTM(extObj)
    
def StartAccountAdjustmentApplication(settlement):
    trade = acm.DealCapturing().CreateNewCustomTrade('Account Adjustment', None)
    trade.Currency(settlement.Currency())
    accountAdjustment = acm.FAccountAdjustment(trade)
    accountAdjustment.AdjustmentAcquirer(settlement.Acquirer())
    accountAdjustment.Currency(settlement.Currency())
    accountAdjustment.AdjustmentAccount(settlement.AcquirerAccountRef())
    initData = acm.DealCapturing().UX().InitDataFromTemplate(accountAdjustment.Trade(), 'Account Adjustment')
    acm.StartApplication('Instrument Definition', initData)
    
def StartAccountTransferApplication(settlement):
    accountTransfer = acm.FAccountTransfer(settlement.Currency())
        
    accountTransfer.Amount(0.0)
    accountTransfer.Currency(settlement.Currency())
    
    source = accountTransfer.Source()
    destination = accountTransfer.Destination()
    
    acquirer = settlement.Acquirer()
    account = settlement.AcquirerAccountRef()
    
    source.Counterparty(acquirer)
    source.Trade().Acquirer(acquirer)
    accountTransfer.SourceAcquirerAccount(account)
    
    destination.Counterparty(acquirer)
    destination.Trade().Acquirer(acquirer)
    accountTransfer.DestinationAcquirerAccount(account)
    
    initData = acm.DealCapturing().UX().InitDataFromTemplate(source.Trade(), 'Account Transfer')
    acm.StartApplication('Instrument Definition', initData)

import FUxCore

class BaseCashDialogMenuItemTM(FUxCore.MenuItem):

    def __init__(self, extObj):
        self.m_extObj = extObj

    def CurrencyColumnId(self):
        return 'Portfolio Realized Profit and Loss'

    def FindRPLColumn(self):
        def DoFindRPLColumn(it):
            if it and it.GridColumn():
                if str(it.GridColumn().ColumnId()) == self.CurrencyColumnId():                
                    return it
                else:
                    return DoFindRPLColumn(it.Next())
            return None
            
        if hasattr(self.m_extObj, 'ActiveSheet'):
            activeSheet = self.m_extObj.ActiveSheet()   
            return DoFindRPLColumn(activeSheet.GridColumnIterator().First())
        else:
            return None
    
    def ListRows(self):
        if hasattr(self.m_extObj, 'ActiveSheet'):
            activeSheet = self.m_extObj.ActiveSheet()
            for row in activeSheet.Selection().SelectedRowObjects():
                if row.IsKindOf(acm.FSingleInstrumentAndTrades) or (row.IsKindOf(acm.FDistributedRow) and row.Instrument()):
                    yield row
        yield None

    def IsMenuApplicable(self, extObj):
        return True
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        if hasattr(extObj, 'ActiveSheet'):
            activeSheet = extObj.ActiveSheet()
            colIter = self.FindRPLColumn()
            for row in self.ListRows():
                if row:
                    rowIter = activeSheet.RowTreeIterator(False).Find(row)
                    cellInfo = activeSheet.GetCell(rowIter, colIter)
                    self.LaunchCallback(row, cellInfo.Value())                
    
    def Enabled(self):
        return bool(next(self.ListRows()) and self.FindRPLColumn())

    def LaunchCallback(self, row, val):
        pass
        
    def SetAttributesFromDictionary(self, acmObj, attDict):
        for methodChain, attValue in list(attDict.items()):
            self._setAttribute(acmObj, methodChain, attValue)
            
    def _setAttribute(self, acmObj, methodChain, attValue):
        methodChain = methodChain.split('.')
        setAtt = methodChain.pop()
        
        for m in methodChain:
            acmObj = acmObj.GetProperty(m)
            
        acmObj.SetProperty(setAtt, attValue)
            
class CashAdjustmentDialogMenuItemTM(BaseCashDialogMenuItemTM):

    def Enabled(self):
        return next(self.ListRows()) is not None

    def CurrencyColumnId(self):
        return 'Portfolio Currency'
        
    def LaunchCallback(self, row, val):
        ce = self.InitCashAdjustment(row, val)
        initData = acm.DealCapturing().UX().InitDataFromTemplate(ce.Trade(), 'Cash Entry')
        acm.StartApplication('Instrument Definition', initData)
        
    def InitCashAdjustment(self, row, val):
        instrument = row.Instrument().StorageImage()
        ce = acm.FCashEntry(instrument)
        if val and val.IsKindOf(acm.FCurrency):
            ce.Currency(val)
        if not row.Trades().AsArray().First().IsInfant():
            self.SetAttributesFromDictionary(ce,
                                         AdjustmentInitialAttributeValues(row))
        
        return ce

class CashTransferDialogMenuItemTM(BaseCashDialogMenuItemTM):

    def LaunchCallback(self, row, val):
        ct = self.InitCashTransfer(row, val)
        initData = acm.DealCapturing().UX().InitDataFromTemplate(ct.Source().Trade(), 'Cash Transfer')
        acm.StartApplication('Instrument Definition', initData)
        
    def InitCashTransfer(self, row, val):
        instrument = row.Instrument().StorageImage()
        amount = val.Number()
        currency = val.Unit()

        ct = acm.FCashTransfer(instrument)
        ct.Amount(amount)
        ct.Currency(currency)
        
        if not row.Trades().AsArray().First().IsInfant():
            self.SetAttributesFromDictionary(ct.Source(),
                                         TransferInitialSourceAttributeValues(row))
            self.SetAttributesFromDictionary(ct.Destination(),
                                         TransferInitialDestinationAttributeValues(row))
        return ct


class CashFXRateFixingDialogMenuItemTM(BaseCashDialogMenuItemTM):
    
    def LaunchCallback(self, row, val):
        rf = self.InitCashFxRateFixing(row, val)
        initData = acm.DealCapturing().UX().InitDataFromTemplate(rf.Source().Trade(), 'FX Rate Fixing')
        acm.StartApplication('Instrument Definition', initData)
        
    def InitCashFxRateFixing(self, row, val):
        instrument = row.Instrument().StorageImage()
        amount = val.Number()
        sourceCurrency = val.Unit()
        destinationCurrency = acm.UsedAccountingCurrency()

        rf = acm.FCashFxRateFixing(instrument)
        rf.SourceCurrency(sourceCurrency)
        rf.DestinationCurrency(destinationCurrency)
        rf.Amount(amount)
        
        if not row.Trades().AsArray().First().IsInfant():
            self.SetAttributesFromDictionary(rf.Source(),
                                         FXRateFixingInitialSourceAttributeValues(row))
            self.SetAttributesFromDictionary(rf.Destination(),
                                         FXRateFixingInitialDestinationAttributeValues(row))
        return rf
        
