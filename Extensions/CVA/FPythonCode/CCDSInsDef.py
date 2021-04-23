
from __future__ import print_function
import acm
import FUxCore

def StartCCDS(eii):
    acm.StartApplication("Instrument Definition", acm.FSymbol("CCDS"))
    return
        
def PrintAddInfoError(type, name):
    message ="Additional Info Spec missing. Please create an Additional Info Spec for Instrument (CreditBalance) of type '"
    message += type
    message += "' called '"
    message += name
    message += "' and restart system."
    print (message)
    
def GetCCDSUnderlyingTrade(instrument):
    try:
        if instrument.IsCCDS():
            return instrument.AdditionalInfo().CCDSUnderlyingTrade()
    except:
        PrintAddInfoError("Trade", "CCDSUnderlyingTrade")
        return None

def SetCCDSUnderlyingTrade(instrument, trade):
    creditBalance = GetUniqueCreditBalance(trade)
    if not creditBalance:
        error = "Trade ", trade.Name(), " is not included in any valid Credit Balance instrument."
        raise Exception(error)
        return
        
    try:
        if instrument.IsCCDS():
            instrument.AdditionalInfo().CCDSUnderlyingTrade(trade)
            instrument.Issuer = creditBalance.Issuer()
            instrument.AdditionalInfo().CVADocument = creditBalance.AdditionalInfo().CVADocument()
            instrument.ValuationGrpChlItem = creditBalance.ValuationGrpChlItem()
            instrument.Currency = creditBalance.Currency()
    except:
        PrintAddInfoError("Trade", "CCDSUnderlyingTrade")
       
def GetCCDSBalancePortfolio(instrument):
    portfolio = acm.FAdhocPortfolio()
    try:
        trade = instrument.CCDSUnderlyingTrade()
        if trade:
            portfolio.Add(trade)
    except:
        PrintAddInfoError("Trade", "CCDSUnderlyingTrade")
        
    return portfolio
        
def GetIsCCDS(instrument):
    return instrument.Suspended()
    
def SetIsCCDS(instrument, isCCDS):
    instrument.Suspended = isCCDS
    
def UpdateDefaultInstrument(instrument):
    instrument.IsCCDS = True
    
def UpdateDefaultTrade(trade):
    trade.Currency = acm.UsedValuationParameters().AccountingCurrency()
    trade.Quantity = 1

def GetUniqueCreditBalance(trade):
    creditBalance = None
    try:
        creditBalance = trade.CreditBalance()
    except:
        return None
    
    return creditBalance
    
def MakeCCDS(shell, trade):
    creditBalance = GetUniqueCreditBalance(trade)
    if creditBalance:
        ccds = acm.DealCapturing.CreateNewInstrument("CCDS")
        ccds.CCDSUnderlyingTrade = trade
        ccdsTrade = acm.DealCapturing().CreateNewTrade(ccds)
        acm.StartApplication("Instrument Defintion", ccdsTrade)
    else:
        print ("The trade is not part of a Credit Balance instrument.")
    
    
'''*******************************************************************
*******************************************************************'''
class MakeCCDSMenuItemInsDef(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def IsMenuEnabled(self, extObj):
        enabled = False
        trade = extObj.OriginalTrade()
        if trade:
            if GetUniqueCreditBalance(trade):
                enabled = True
        return enabled
        
    def Invoke(self, eii):
        extObj = eii.ExtensionObject()
        if self.IsMenuEnabled(extObj):
            trade = extObj.OriginalTrade()
            shell = eii.ExtensionObject().Shell()
            MakeCCDS( shell, trade )
        
    def Enabled(self):
        return self.IsMenuEnabled(self.m_extObj)
        
    def Applicable(self):
        return self.IsMenuEnabled(self.m_extObj)
        
def CreateMakeCCDSMenuItemInsDef(extObj):
    return MakeCCDSMenuItemInsDef(extObj)
    
