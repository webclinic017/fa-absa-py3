import acm
from DealPackageBase import *
from DealPackageUtil import SetNewWithoutClearingIdentifiers, SetSave

@Settings(GraphApplicable=False,
          MultiTradingEnabled=True)
class DealBase(DealPackageBase):
    
    def __init__(self, dealPackage):
        DealPackageBase.__init__(self, dealPackage)
        
    def AssemblePackage(self, optArg=None):
        type = None
        trade = None
        if optArg and hasattr(optArg, 'IsKindOf') and optArg.IsKindOf(acm.FDictionary):
            contents = optArg['contents']
            type = optArg['type']
            if contents:
                if contents.IsKindOf(acm.FInstrument):
                    trade = acm.DealCapturing().CreateNewTrade(contents)
                elif contents.IsKindOf(acm.FTrade):
                    trade = contents
        
        if type and not trade:
            trade = acm.DealCapturing().CreateNewCustomTrade(type)
    
        if not trade:
            raise DealPackageException('Could not assemble deal')
        self.DealPackage().AddTrade(trade, "Trade")
    
    def Instrument(self):
        return self.Instruments().First()
        
    def InstrumentRegulatoryInfo(self):
        return self.Instrument().GetOrCreateRegulatoryInfo()
        
    def Leg(self):
        return self.Instrument().FirstStartDayLeg()
        
    def PayLeg(self):
        return self.Instrument().FirstPayLeg()
        
    def ReceiveLeg(self):
        return self.Instrument().FirstReceiveLeg()
        
    def Trade(self):
        return self.Trades().First()
        
    def LeadTrade(self):
        return self.Trade()

    def TradeRegulatoryInfo(self):
        return self.Trade().GetOrCreateRegulatoryInfo()
        
    def IsShowModeInstrumentDetail(self, *args):    
        return self.IsShowModeDetail()
        
    def IsShowModeTradeDetail(self, *args):
        return self.IsShowModeDetail2()
        
    def InstrumentPanes(self):
        return None
        
    def TradePanes(self):
        return None
    
    def CustomPanes(self):
        customPanes = []
        instrumentPanes = self.InstrumentPanes()
        if instrumentPanes:
            insTabs = self.GetCustomPanesFromExtValue(instrumentPanes)
            customPanes.append({'Instrument':insTabs})
        tradePanes = self.TradePanes()
        if tradePanes:
            tradeTabs = self.GetCustomPanesFromExtValue(tradePanes)
            customPanes.append({'Trade':tradeTabs})
        
        return customPanes
    
    def OnQuotationChanged(self, attributeName, oldValue, newValue, *args):
        self.Trade().UpdatePremium(True)
        self._UpdateAndRegisterAllObjectMappings(attributeName)
        
    def OnInstrumentCurrencyChanged(self, attributeName, oldValue, newValue, *args):
        self.Trade().Currency(newValue)
        self._UpdateAndRegisterAllObjectMappings(attributeName)
    
    def OnInstrumentStartDateChanged(self, attributeName, oldValue, newValue, *args):
        self.Trade().UpdateDays()
        self._UpdateAndRegisterAllObjectMappings(attributeName)
        
    def OnInstrumentSpotDaysChanged(self, attributeName, oldValue, newValue, *args):
        self.Trade().UpdateDays()
        self._UpdateAndRegisterAllObjectMappings(attributeName)

    def OnInterestPaymentTimeChanged(self, attributeName, oldValue, newValue, *args):
        self.Trade().UpdateDays()
        self._UpdateAndRegisterAllObjectMappings(attributeName)

    def OnSave(self, saveConfig):
        saveTrades = []
        saveInstruments = []
        saveDealPackages = []
        saveInstrumentPackages = []
        saveAsNewTrades = []
        saveAsNewInstruments = []
        saveAsNewDealPackages = []
        saveAsNewInstrumentPackages = []
        
        if saveConfig.InstrumentPackage() == "SaveNew":
            saveAsNewInstruments = self.Instruments()
            saveAsNewInstrumentPackages = self.DealPackage().InstrumentPackage().ChildInstrumentPackages()
        elif saveConfig.InstrumentPackage() == "Save":
            saveInstruments = self.Instruments()
            saveInstrumentPackages = self.DealPackage().InstrumentPackage().ChildInstrumentPackages()
        if saveConfig.DealPackage() == "SaveNew" or saveConfig.InstrumentPackage() == "SaveNew":
            saveAsNewTrades = self.Trades()
            saveAsNewDealPackages = self.ChildDealPackages()
        elif saveConfig.DealPackage() == "Save":
            saveTrades = self.Trades()
            saveDealPackages = self.ChildDealPackages()
            
        SetSave( 
            saveTrades,
            saveInstruments,
            saveDealPackages,
            saveInstrumentPackages)
        
        SetNewWithoutClearingIdentifiers( 
            saveAsNewTrades,
            saveAsNewInstruments,
            saveAsNewDealPackages,
            saveAsNewInstrumentPackages)

        if saveConfig.InstrumentPackage() == 'Save' and self.DealPackage().HasAttribute('ins_askBeforeSave'):
            return self.ins_askBeforeSave(saveConfig)
    
    def IsLiveTrade(self, trade):
        return True
    
    def OpenAfterSave(self, config):
        return self.DealPackage()
    
    def SuggestName(self):
        pass
        
    def Refresh(self):
        pass
    
    
