import acm
from PairOptionsDealPackageBase import PairOptionsDealPackageBase
from FXStrategyDualStrikeDealPackageBase import FXStrategyDualStrikeDealPackageBase
from PairOptionsUtil import SetFXTradeAndInstrumentAttributes, UpdateDealPackageTradeLink, lot
from PairOptionsOneVolatility import OneVolVolatility
from DealPackageDevKit import Action


class FXCallPutSpreadDefinition(FXStrategyDualStrikeDealPackageBase):
    strategyTypeDisplayName =  'Spread'
    
    foreignOptionType =         Action( label='@ForeignCurrencyLabel',
                                        action='@ChangeCallPut',
                                        recreateCalcSpaceOnChange = True)
    
    domesticOptionType =        Action( label='@DomesticCurrencyLabel',
                                        action='@ChangeCallPut',
                                        recreateCalcSpaceOnChange = True)
    
    oneVol =          OneVolVolatility( quoteTradeName='QuoteCombinationTrade',
                                        callVolObjectsName='VolatilityCallObjectsAsLot',
                                        putVolObjectsName='VolatilityPutObjectsAsLot')
                                                
    deltaCall = None
    deltaFlippedCall =  None
    deltaPut =  None              
    deltaFlippedPut = None
    
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************''' 
    def LeadTradeName(self):
        return 'long'
    
    def Trade(self):
        return self.TradeAt('long')

    def CallTrade(self):
        return self.TradeAt('long')
        
    def PutTrade(self):
        return self.TradeAt('short')

    def Instrument(self):
        return self.InstrumentAt('long')
        
    def B2B(self):
        return [self.B2BTradeParamsAt('long'), self.B2BTradeParamsAt('short')]

    def B2BCall(self):
        return self.B2BTradeParamsAt('long')

    def B2BPut(self):
        return self.B2BTradeParamsAt('short')

    
    #***************************************                              
    #*********** GRID VIEW MODEL ***********
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, Label, AttrActionLeft, AttrActionRight
        from PairOptionsPricerGridViewModel import AttrCalcMarketData, AttrLabelMarketDataLeft, LabelParam, AttrLabelMarketDataRight, AttrCalcMarketDataLeftReadOnly, AttrCalcMarketDataLot, AttrCalcMarketDataLotLeft
        
        volatilityRow = Row([AttrCalcMarketData('oneVol_volatility'), AttrLabelMarketDataLeft('oneVol_volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')])
        putCallVolRow = Row([AttrCalcMarketDataLot('oneVol_callVolatility'), AttrLabelMarketDataLeft('oneVol_callVolatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('oneVol_putVolatility'), AttrCalcMarketDataLotLeft('oneVol_putVolatility')])        
        
        gridViewModel = super(FXCallPutSpreadDefinition, self)._gridModelView_default()
        gridViewModel[0].RowItems()[1] = AttrActionLeft('foreignOptionType')
        gridViewModel[0].RowItems()[3] = AttrActionRight('domesticOptionType')
        gridViewModel[4:6] = gridViewModel[4:6][::-1] #Swap Long/short stike rows
        gridViewModel[7:9] = gridViewModel[7:9][::-1] #Swap Long/short amount rows
        gridViewModel[14] = volatilityRow
        gridViewModel.insert(15, putCallVolRow)
        gridViewModel[25] = Row([Label('Strategy'), Label(''), Label(''), Label('Short'), Label('Long')])
        return gridViewModel

    
    '''*******************************************************
    * Label methods
    *******************************************************'''  
    def AmountCallHeader(self, *args):
        buySell = 'Buy' if self.AmountCallForeignSign() > 0 else 'Sell'
        return "%s %s" % (buySell, 'Long')

    def AmountPutHeader(self, *args):
        buySell = 'Buy' if self.AmountPutForeignSign() > 0 else 'Sell'
        return "%s %s" % (buySell, 'Short')
        
    def CallVolatilityLabel(self, *args):
        return 'Long'
        
    def PutVolatilityLabel(self, *args):
        return 'Short'
        
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(FXCallPutSpreadDefinition, self).OnInit()
        self._pricingOptions = acm.FFxSpreadPricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateCallPutSpread(self.DealPackage().TradeAt('long'), self.DealPackage().TradeAt('short'))
        
    def AssemblePackage(self):
        longTradeDeco = self.DealPackage().CreateTrade('FX Option', 'long')
        shortTradeDeco = self.DealPackage().CreateTrade('FX Option', 'short')
        SetFXTradeAndInstrumentAttributes(longTradeDeco)   
        SetFXTradeAndInstrumentAttributes(shortTradeDeco)   
        self.PricingOptions().CreateCallPutSpread(longTradeDeco, shortTradeDeco)

    '''*******************************************************
    * Helper Methods
    *******************************************************'''  
    def SetNewSaveTradeOnDealPackage(self):
        UpdateDealPackageTradeLink(self.DealPackage(), self.CurrentCallSaveTrade().Trade(), 'long')
        UpdateDealPackageTradeLink(self.DealPackage(), self.CurrentPutSaveTrade().Trade(), 'short')

    '''*************************************************************'''
    def SetDefaultStrike(self):
        self.solverParameter = 'solverStrike2DomPerFor'
        self.DealPackage().SetAttribute('strikeDomesticPerForeign', '-5pf')
        self.DealPackage().SetAttribute('strike2DomesticPerForeign', '0pf')
        
    def VolatilityCallObjectsAsLot(self):
        combInstrMaps = []
        for tradeMethodName in ['QuoteCombinationTrade', 'AltQuoteCombinationTrade', 'FlippedQuoteCombinationTrade', 'FlippedAltQuoteCombinationTrade']:
            combInstrMaps.append(getattr(self, tradeMethodName)().Instrument().InstrumentMaps(acm.Time.DateToday()).First())
        return lot(combInstrMaps)
     
    def VolatilityPutObjectsAsLot(self):
        combInstrMaps = []
        for tradeMethodName in ['QuoteCombinationTrade', 'AltQuoteCombinationTrade', 'FlippedQuoteCombinationTrade', 'FlippedAltQuoteCombinationTrade']:
            combInstrMaps.append(getattr(self, tradeMethodName)().Instrument().InstrumentMaps(acm.Time.DateToday()).Last())
        return lot(combInstrMaps)

    def ChangeCallPut(self, *args):
        PairOptionsDealPackageBase.ChangeCallPut(self, *args)
    
    def TransformDelta(self, name, newDelta):
        return PairOptionsDealPackageBase.TransformDelta(self, name, newDelta)
        
    def TransformFlippedDelta(self, name, newDelta):
        return PairOptionsDealPackageBase.TransformFlippedDelta(self, name, newDelta)
    
    def StrikeDomPerForLabel(self, attrName):
        return 'Long Strike' if attrName == 'strike2DomesticPerForeign' else 'Short Strike'
    
    def IsVolatilitySimulated(self):
        retVal = False
        for volatility in ['oneVol_callVolatility', 'oneVol_putVolatility', 'oneVol_volatility']:
            if self.GetAttributeMetaData(volatility, 'isCalculationSimulated')():
                retVal = True
        return retVal
        
    
    '''*******************************************************
    * Overridden base class methods
    *******************************************************'''
    def TransformVolatility(self, attrName, value):
        if attrName is not "volatility":
            if value in ('', None):
                self.bidAskModeVol = self.bidAskMode
            elif isinstance(value, str) and len(value.split('/')) == 2:
                self.bidAskModeVol = True
            else:
                self.bidAskModeVol = False
        return self.TransformBidAskSplit(attrName, value)
    
