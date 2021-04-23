import acm
from RFQUtils import Direction, PriceAndMarginConversions, Misc
from DealPackageUtil import SalesTradingInteraction, SalesTradingInfo, UnDecorate
from TradeCreationUtil import TABTradeCreationSetting, TradeCreationUtil
from SalesTradingCustomizations import OrderBookCreation
from SalesTradingCustomizations import PriceAndMarginConversions as ConversionCustomizations

MAIN_TRADING_QR_NAME = SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME

class TradeCreator(object):
    def __init__(self, hookArgument):
        self._dealPackage = None
        self._artifactsToCommit = acm.FArray()
        self._isFromSalesOrder = hookArgument.IsFromSalesOrder()
        self._extendedDataDict = hookArgument.ExtendedDataDict()
        self._clientTrades = hookArgument.ClientTrades()
        self._internalTrades = hookArgument.InternalTrades()
        self._log = hookArgument.LogObject()
        self._logicGUI = acm.FBusinessLogicGUIDefault()
        self.SavePrices()
        
    def SavePrices(self):
        self._allInPrice = self.ClientQuoteTrade().Price()
        self._traderPrices = self.CreateTraderPriceDict()
    
    def CreateTraderPriceDict(self):
        traderPrices = acm.FDictionary()
        for componentName, trades in self.InternalTrades().items():
            traderPrices.AtPut(componentName, trades['ORDER'].Price())
        return traderPrices
    
    def STISettings(self):
        stiSettings = None
        if self.DealPackage():
            stiSettings = self.DealPackage().GetAttribute('salesTradingInteraction')
        return stiSettings
    
    def ArtifactsToCommit(self):
        return self._artifactsToCommit

    def LogicGUI(self):
        return self._logicGUI

    def IsFromSalesOrder(self):
        return self._isFromSalesOrder

    def ExtendedDataDict(self):
        return self._extendedDataDict
    
    def IsMultipleTradingQuoteRequests(self):
        return len(self.InternalTrades()) > 1
    
    def IsSingleQuoteRequest(self):
        return len(self.InternalTrades()) == 0

    def ClientInstrument(self):
        return self.ClientOrderTrade().Instrument()

    def ClientTrades(self):
        return self._clientTrades

    def InternalTrades(self):
        return self._internalTrades

    def ClientQuoteTrade(self):
        return self.ClientTrades()['QUOTE']

    def ClientQuoteTradeDecorator(self):
        return acm.FBusinessLogicDecorator.WrapObject(self.ClientQuoteTrade(), self.LogicGUI())

    def ClientOrderTrade(self):
        return self.ClientTrades()['ORDER']

    def InternalQuoteTrade(self, quoteRequestName):
        return self.InternalTrades()[quoteRequestName]['QUOTE']
    
    def AllInPrice(self):
        return self._allInPrice
    
    def TraderPrice(self, quoteRequestName):
        return self._traderPrices[quoteRequestName]
    
    def SalesObject(self):
        salesObjectDict = self.ExtendedDataDict().At(SalesTradingInteraction.SALES_NAME).At('objectToQuote')
        return SalesTradingInfo.ObjectToQuoteFromDict(salesObjectDict)
        
    def DealPackage(self):    
        if not self._dealPackage:
            if self.SalesObject().IsKindOf(acm.FDealPackage):
                self._dealPackage = acm.FBusinessLogicDecorator.WrapObject(self.SalesObject()).Edit()
            elif self.SalesObject().IsKindOf(acm.FInstrumentPackage):
                self._dealPackage = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(self.SalesObject())
        return self._dealPackage
    
    def Trade(self):
        trade = None
        if self.SalesObject() and self.SalesObject().IsKindOf('FTrade'):
            trade = self.SalesObject()
        return trade

    def TabTradeCreationRule(self):
        return self.ExtendedDataDict().At(SalesTradingInteraction.SALES_NAME).At('tabTradeCreationSetting')
    
    def MultipleTradingQuoteRequests(self):
        return len(self.InternalTrades()) > 1
        
    def Warning(self, text):
        self._log.warning(text)

    def Error(self, text):
        raise Exception(text)
    
    def IsRebateSecurityLoan(self, instrument):
        prodType = instrument.ProductTypeChlItem()
        if (prodType is not None) and (prodType.StringKey() == 'Rebate Security Loan'):
            return True
        else:
            return False
    
    def IsNonFixedSecurityLoan(self, instrument):
        isNonFixedSecurityLoan = False
        leg = instrument.FirstReceiveLeg() if self.IsRebateSecurityLoan(instrument) else instrument.FirstPayLeg()
        if instrument.InsType() == 'SecurityLoan' and leg.NominalScaling() != 'None':
            isNonFixedSecurityLoan = True
        return isNonFixedSecurityLoan
    
    def ApplyPriceToSpreadReset(self, leg):
        leg.FixedRate(0.0)
        leg.GenerateCashFlows(0.0)
        cf = leg.CashFlows().First() if leg.CashFlows() else None
        if cf:
            for reset in cf.Resets():
                if reset.ResetType() == 'Spread':
                    reset.FixFixingValue(self.AllInPrice())
    
    def ApplyPriceToInstrument(self, instrument):
        instrument = instrument.StorageImage()
        if self.IsNonFixedSecurityLoan(instrument):
            leg = instrument.FirstReceiveLeg() if self.IsRebateSecurityLoan(instrument) else instrument.FirstPayLeg()
            self.ApplyPriceToSpreadReset(leg)
        elif PriceAndMarginConversions.PriceAsSpread(instrument, None):
            leg = instrument.PayLeg() if instrument.IsSwap() else instrument.FirstFloatLeg()
            leg.Spread(self.AllInPrice())
            name = instrument.SuggestName()
            instrument.Name(name)
            leg.GenerateCashFlows(0.0)
        elif PriceAndMarginConversions.PriceAsFixedRate(instrument, None):
            leg = instrument.FirstFloatLeg() if instrument.InsType() == 'FRA' else instrument.FirstFixedLeg()
            leg.FixedRate(self.AllInPrice())
            name = instrument.SuggestName()
            instrument.Name(name)
            leg.GenerateCashFlows(self.AllInPrice())
        else:
            self.Error("Cannot handle non-price based instrument '%s'" % instrument.Name())  
            
        instrument.Commit()
    
    def ApplyPrice(self, trade):
        instrument = trade.Trade().Instrument()
        if OrderBookCreation.IsPriceBased(instrument):
            trade.Price(self.AllInPrice())
        else:
            trade.Price(0.0)
            self.ApplyPriceToInstrument(instrument)

    def SetTrader(self):
        if not self.ClientQuoteTrade().Trader():
            self.ClientQuoteTrade().Trader(self.ClientOrderTrade().Trader())

    def SalesMargin(self, quoteRequestName):
        direction = Direction.FromQuantity(self.ClientOrderTrade().Quantity(), self.ClientInstrument())
        margin = PriceAndMarginConversions.Spread(self.TraderPrice(quoteRequestName), self.AllInPrice(), direction == Direction.ask, None, self.ClientInstrument())
        priceDiff = ConversionCustomizations.PriceDifferenceFromMargin(margin, None, self.ClientInstrument())
        if self.ClientInstrument().IsSpreadInBasisPoints():
            margin = priceDiff * 100.0
        else:
            margin = priceDiff
        return margin

    def TraderPortfolio(self, quoteRequestName):
        return self.InternalQuoteTrade(quoteRequestName).Portfolio()

    def TraderAcquirer(self, quoteRequestName):
        return self.InternalQuoteTrade(quoteRequestName).Acquirer()

    def SetRegulatoryInfo(self, trade):
        regInfo = trade.RegulatoryInfo()
        regInfo.TheirOrganisation(self.ClientQuoteTrade().RegulatoryInfo().TheirOrganisation())
        regInfo.TheirInvestmentDecider(self.ClientQuoteTrade().RegulatoryInfo().TheirInvestmentDecider())

    def SetDealPackageTradeQuantities(self, dp):
        clientQuoteTrade = self.ClientQuoteTrade()
        stiSettings = self.STISettings()
        amountInfo = stiSettings.At('amountInfo')
        if amountInfo and dp.GetAttribute(amountInfo['amountAttr']) is not None:
            dp.SetAttribute(amountInfo['amountAttr'], clientQuoteTrade.Quantity())
        else:
            for trdDeco in dp.Trades():
                trdDeco.Quantity(trdDeco.Quantity() if self.ClientQuoteTrade().Quantity() > 0 else -trdDeco.Quantity())

    def SetRegulatoryInfos(self, dp):
        for trdDeco in dp.Trades():
            self.SetRegulatoryInfo(trdDeco.Trade())
    
    def SetTags(self, dp):
        addInfoName = 'SalesOrderId' if self.IsFromSalesOrder() else 'QuoteRequestId'
        if hasattr(self.ClientQuoteTrade().AdditionalInfo(), addInfoName):
            addInfoValue = getattr(self.ClientQuoteTrade().AdditionalInfo(), addInfoName)()
        TradeCreationUtil.SetAddInfoOnTrades(dp.Trades(), addInfoName, addInfoValue)
            
    def SaveDealPackage(self, dp):
        acm.PollAllDbEvents()
        config = acm.FDealPackageSaveConfiguration()
        config.InstrumentPackage('Exclude')
        config.DealPackage('Save')
        dp = dp.Save(config).First()
    
    def SetGeneralAttrs(self, dp):
        clientQuoteTrade = self.ClientQuoteTrade()
        stiSettings = self.STISettings()
        if stiSettings.At('statusAttr'):
            dp.SetAttribute(stiSettings.At('statusAttr'), stiSettings.At('status'))
        if stiSettings.At('clientAttr'):
            dp.SetAttribute(stiSettings.At('clientAttr'), clientQuoteTrade.Counterparty())
        if stiSettings.At('acquirerAttr'):
            dp.SetAttribute(stiSettings.At('acquirerAttr'), clientQuoteTrade.Acquirer())
        if stiSettings.At('portfolioAttr'):
            dp.SetAttribute(stiSettings.At('portfolioAttr'), clientQuoteTrade.Portfolio())
        if stiSettings.At('tradeTimeAttr'):
            dp.SetAttribute(stiSettings.At('tradeTimeAttr'), clientQuoteTrade.TradeTime())
        Misc.GetTradeFromDealPackage(dp).OptionalKey(clientQuoteTrade.OptionalKey())
        self.SetDealPackageTradeQuantities(dp)
        self.SetRegulatoryInfos(dp)
        self.SetTags(dp)
    
    def SetComponentAttrs(self, dp):
        componentAttrs = self.STISettings().At('componentAttrs')
        if componentAttrs:
            for componentName, componentDict in componentAttrs.items():
                if componentDict.get('priceAttr'):
                    dp.SetAttribute(componentDict.get('priceAttr'), self.TraderPrice(componentName))
                if componentDict.get('traderPrfAttr'):
                    dp.SetAttribute(componentDict.get('traderPrfAttr'), self.TraderPortfolio(componentName))
                if componentDict.get('traderAcqAttr'):
                    dp.SetAttribute(componentDict.get('traderAcqAttr'), self.TraderAcquirer(componentName))
    
    def SetAllInPrice(self, dp):
        if self.STISettings().At('allInPriceAttr'):
            dp.SetAttribute(self.STISettings().At('allInPriceAttr'), self.AllInPrice())

    def UpdateDealPackageAndSave(self):
        rfqTrade = self.ClientQuoteTrade()
        dp = self.DealPackage()
        dp = dp.Edit() if dp.StorageId() > 0 else dp
        self.SetGeneralAttrs(dp)
        self.SetComponentAttrs(dp)
        self.SetAllInPrice(dp)
        self.SaveDealPackage(dp)

    def UpdateExistingTrade(self, trade):
        rfqTrade = self.ClientQuoteTrade()
        trdDeco = acm.FBusinessLogicDecorator.WrapObject(trade)
        trdDeco.Portfolio(rfqTrade.Portfolio())
        trdDeco.Counterparty(rfqTrade.Counterparty())
        trdDeco.Trader(rfqTrade.Trader())
        trdDeco.TradeTime(rfqTrade.TradeTime())
        self.ApplyPrice(trdDeco)
        trdDeco.Status(rfqTrade.Status())
        trdDeco.Quantity(rfqTrade.Quantity())
        if not trdDeco.Acquirer():
            trdDeco.Acquirer(rfqTrade.Acquirer())
        self.SetRegulatoryInfo(trdDeco)
        trdDeco.OptionalKey(rfqTrade.OptionalKey())
        return trade

    def UpdateB2BParameters(self, b2bParams):
        b2bParams.SalesMargin(self.SalesMargin(MAIN_TRADING_QR_NAME))
        b2bParams.SalesCoverEnabled(True)
        b2bParams.TraderPortfolio(self.TraderPortfolio(MAIN_TRADING_QR_NAME))
        b2bParams.TraderAcquirer(self.TraderAcquirer(MAIN_TRADING_QR_NAME))

    def CreateAndUpdateB2BParameters(self, trade):
        b2bparams = acm.FB2BSalesCoverConstellationParameters(trade)
        b2bDeco = acm.FBusinessLogicDecorator.WrapObject(b2bparams, self.LogicGUI())
        self.UpdateB2BParameters(b2bDeco)
        return b2bDeco

    def ManualHandling(self):
        if self.DealPackage():
            trade = Misc.GetTradeFromDealPackage(dealPackage)
        elif self.Trade():
            trade = self.Trade()
        if trade:
            trade = trade.StorageImage()
            trade.OptionalKey(self.ClientQuoteTrade().OptionalKey())
            self.ArtifactsToCommit().Add(trade)

    def UpdateExisting(self):
        if self.DealPackage():
            self.UpdateDealPackageAndSave()
        elif self.Trade():
            trade = self.Trade()
            trade = trade.StorageImage()
            if self.InstrumentSupportsB2B() and not self.IsSingleQuoteRequest():
                b2bDeco = self.CreateAndUpdateB2BParameters(trade)
                trade = self.UpdateExistingTrade(trade)
                b2bDeco.Refresh()
                b2bResult = b2bDeco.AllocateRisk()
                self.ArtifactsToCommit().AddAll([trade, b2bResult])
            else:
                trade = self.UpdateExistingTrade(trade)
                self.ArtifactsToCommit().Add(trade)
            
    def InstrumentSupportsB2B(self):
        return self.ClientQuoteTrade().Instrument().InsType() not in ['SecurityLoan', 'Repo/Reverse', 'BasketRepo/Reverse', 'BasketSecurityLoan']
        
    def CreateNew(self):
        if self.DealPackage():
            self.UpdateDealPackageAndSave()
        else:
            self.SetTrader()
            self.ApplyPrice(self.ClientQuoteTradeDecorator())
            if self.InstrumentSupportsB2B() and not self.IsSingleQuoteRequest():
                b2bDeco = self.CreateAndUpdateB2BParameters(self.ClientQuoteTrade())
                b2bResult = b2bDeco.AllocateRisk()
                self.ArtifactsToCommit().AddAll([self.ClientQuoteTrade(), b2bResult])
            else:
                self.ArtifactsToCommit().AddAll([self.ClientQuoteTrade()])

    def CreateOrUpdateTrades(self):
        if self.TabTradeCreationRule() == TABTradeCreationSetting.manualTradeHanling:
            self.ManualHandling()
        elif self.TabTradeCreationRule() == TABTradeCreationSetting.updateExistingTrade:
            self.UpdateExisting()       
        elif self.TabTradeCreationRule() == TABTradeCreationSetting.createNewTrade:
            self.CreateNew()
        return self.ArtifactsToCommit() 
  
def TradeCreationTemplate(hookArgument, *args):
    extendedDataDict = hookArgument.ExtendedDataDict()
    clientTrades = hookArgument.ClientTrades()
    internalTrades = hookArgument.InternalTrades()
    tradeCreator = TradeCreator(hookArgument)
    artifactsToCommit = tradeCreator.CreateOrUpdateTrades()
    return artifactsToCommit
