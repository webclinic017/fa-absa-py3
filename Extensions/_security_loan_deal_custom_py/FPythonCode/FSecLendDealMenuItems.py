""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecurityLoanDealCustom/etc/FSecLendDealMenuItems.py"
import acm
import FUxCore
import DealUx
import TransactionHistory

class SecLendDealMenuItem(FUxCore.MenuItem, object):
    
    def __init__(self, frame, enabledFunc = None, invokeFunc = None):
        self.frame = frame
        self.enabledFunc = enabledFunc
        self.invokeFunc = invokeFunc
        
    def Enabled(self):
        if self.enabledFunc is None:
            return True
        else:
            trade = self.frame.CustomLayoutApplication().DealPackage().Trades().First()
            return self.enabledFunc(trade)

    def Invoke(self, eii):
        if self.invokeFunc is None:
            pass
        else:
            self.invokeFunc(self.frame.CustomLayoutApplication().DealPackage().Trades().First())     
   
    def Applicable(self):
        try:
            definitionName = self.frame.CustomLayoutApplication().DealPackage().DefinitionDisplayName()
            if definitionName in ('Security Loan', 'Master Security Loan'):
                return True
        except Exception as e:
            pass
        return False



def Transhist(frame):
    return SecLendDealMenuItem(frame, 
                    enabledFunc = lambda trade: IsPersistent(trade), 
                    invokeFunc  = lambda trade: OpenTranshist(frame.Shell(), trade))

def DividendEstimation(frame):    
    return SecLendDealMenuItem(frame, 
                    enabledFunc = lambda trade: HasUnderlying(trade), 
                    invokeFunc  = lambda trade: OpenDividendEstimate(frame.Shell(), trade))
    
def PriceEntry(frame):
    return SecLendDealMenuItem(frame, 
                    enabledFunc = lambda trade: True, 
                    invokeFunc  = lambda trade: OpenPriceEntry(frame.Shell(), trade))
    
def Underlying(frame):
    return SecLendDealMenuItem(frame, 
                    enabledFunc = lambda trade: HasUnderlying(trade), 
                    invokeFunc  = lambda trade: OpenUnderlying(frame.Shell(), trade))
    
def Counterparty(frame):
    return SecLendDealMenuItem(frame, 
                    enabledFunc = lambda trade: HasCounterparty(trade), 
                    invokeFunc  = lambda trade: OpenCounterparty(frame.Shell(), trade))

def ContractTrade(frame):
    return SecLendDealMenuItem(frame, 
                    enabledFunc = lambda trade: HasOtherContractTrade(trade), 
                    invokeFunc  = lambda trade: OpenContractTrade(frame.Shell(), trade))
                    
# Enabled callbacks
def IsPersistent(trade):
    return trade.Originator().IsInfant() == False

def HasUnderlying(trade):
    return trade.Instrument().Underlying() != None
    
def HasCounterparty(trade):
    return trade.Counterparty() != None
    
def HasOtherContractTrade(trade):
    return trade.Contract() and trade.Contract() != trade.Originator()
    
#Invokation callbacks
def OpenTranshist(shell, trade):
    TransactionHistory.ShowTransactionHistoryForInstrumentAndTradesPrivate(trade.Instrument().Originator(), 
                trade.Originator(), 
                shell,
                trade.Originator().StringKey() + ' Transaction History')

def OpenDividendEstimate(shell, trade):
    security = trade.Instrument().Underlying()
    divStream = security.MappedDividendStream().Parameter()
    acm.StartApplication("Dividend Estimation", divStream)
    
def OpenPriceEntry(shell, trade):
    instrument = trade.Instrument().Originator()
    if instrument.IsInfant():
        instrument = None
    acm.StartApplication('Price Entry', instrument)
    
def OpenUnderlying(shell, trade):
    security = trade.Instrument().Underlying()
    acm.StartApplication("Instrument Definition", security)

def OpenCounterparty(shell, trade):
    acm.StartApplication("Party Definition", trade.Counterparty())

def OpenContractTrade(shell, trade):
    acm.StartApplication("Instrument Definition", trade.Contract())
