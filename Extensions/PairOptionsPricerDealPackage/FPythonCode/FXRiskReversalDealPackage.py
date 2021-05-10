import acm
from FXStrategyDualStrikeDealPackageBase import FXStrategyDualStrikeDealPackageBase
from PairOptionsUtil import SetFXTradeAndInstrumentAttributes
from DealPackageDevKit import CalcVal, Bool

class FXRiskReversalDefinition(FXStrategyDualStrikeDealPackageBase):
    strategyTypeDisplayName =  'Risk Reversal'
    
    volatilitySpread     =     CalcVal( label='Spread %',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Volatility Spread FXOStrat',
                                        enabled=False)

    isFavourCallEnabled  =     Bool(    objMapping = "IsFavourCallEnabled",
                                        enabled = False,
                                        recreateCalcSpaceOnChange = True)
                                    
    callVolatility =           CalcVal( label='@CallVolatilityLabel',
                                        calcMapping='VolatilityCallObjectsAsLot:FDealSheet:Portfolio Volatility FXOStrat',
                                        onChanged='@ValueSimulated|UnsimulateOneVolatility',
                                        transform='@TransformVolatility',
                                        solverParameter='@VolatilityParam')
                                    
    putVolatility =            CalcVal( label='@PutVolatilityLabel',
                                        calcMapping='VolatilityPutObjectsAsLot:FDealSheet:Portfolio Volatility FXOStrat',
                                        onChanged='@ValueSimulated|UnsimulateOneVolatility',
                                        transform='@TransformVolatility',
                                        solverParameter='@VolatilityParam')
            
    deltaBSCall =              CalcVal( label='Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='CallQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                        
    deltaBSAltCall =           CalcVal( label='Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='CallAltQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                        
    deltaBSFlippedCall =       CalcVal( label='Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                        calcMapping='CallFlippedQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                        
    deltaBSFlippedAltCall =    CalcVal( label='Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                        calcMapping='CallFlippedAltQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                        
    deltaBSPut =               CalcVal( label='Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='PutQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
        
    deltaBSAltPut =            CalcVal( label='Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='PutAltQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
                                        
    deltaBSFlippedPut =        CalcVal( label='Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                        calcMapping='PutFlippedQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
                                        
    deltaBSFlippedAltPut =     CalcVal( label='Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                        calcMapping='PutFlippedAltQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
                                                                                    
    fwdDeltaBSCall =           CalcVal( label='Fwd Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='ForeignStrategyOrTradeGreek:FDealSheet:Instrument Forward Delta Call FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                            
    fwdDeltaBSPut =            CalcVal( label='Fwd Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='ForeignStrategyOrTradeGreek:FDealSheet:Instrument Forward Delta Put FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
                                            
    fwdDeltaBSFlippedCall =     CalcVal(label='Fwd Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                        calcMapping='DomesticStrategyOrTradeGreek:FDealSheet:Instrument Forward Delta Call FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                            
    fwdDeltaBSFlippedPut =     CalcVal( label='Fwd Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement|DomesticColumnConfig',
                                        calcMapping='DomesticStrategyOrTradeGreek:FDealSheet:Instrument Forward Delta Put FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')

    #***************************************                              
    #*********** GRID VIEW MODEL ***********
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, Attr, AttrCalcMarketDataLot, AttrCalcMarketDataLotLeft, AttrCalcMarketDataLeftReadOnly
        from PairOptionsPricerGridViewModel import LabelParam, AttrLabelMarketDataLeft, AttrLabelMarketDataRight, AttrCalc
        
        volatilityRow = Row([AttrCalc('volatilitySpread'), AttrLabelMarketDataLeft('volatilitySpread'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')])
        putCallVolRow = Row([AttrCalcMarketDataLot('callVolatility'), AttrLabelMarketDataLeft('callVolatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('putVolatility'), AttrCalcMarketDataLotLeft('putVolatility')])
        
        gridViewModel = super(FXRiskReversalDefinition, self)._gridModelView_default()
        gridViewModel[14] = volatilityRow
        gridViewModel.insert(15, putCallVolRow)
        
        return gridViewModel
        
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************''' 
    def IsFavourCallEnabled(self, notUsed = None):
        currentSaveInstrument = self.CurrentSaveTrade().Instrument()
        volatilityStructure = currentSaveInstrument.MappedVolatilityLink().Link().VolatilityStructure()
        return volatilityStructure.FavourCall()

    
    '''*******************************************************
    * Label methods
    *******************************************************'''
    def CallVolatilityLabel(self, *args):
        callLabel = 'Call'
        if self.isFavourCallEnabled:
            callLabel = callLabel + ' (Favour)'
        return callLabel
        
    def PutVolatilityLabel(self, *args):
        putLabel = 'Put'
        if not self.isFavourCallEnabled:
            putLabel = '(Favour) ' + putLabel
        return putLabel

    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(FXRiskReversalDefinition, self).OnInit()
        self._pricingOptions = acm.FFxRiskReversalPricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateRiskReversal(self.DealPackage().TradeAt('callTrade'), self.DealPackage().TradeAt('putTrade'))
        
    def AssemblePackage(self):
        callTradeDeco = self.DealPackage().CreateTrade('FX Option', 'callTrade')
        putTradeDeco = self.DealPackage().CreateTrade('FX Option', 'putTrade')
        SetFXTradeAndInstrumentAttributes(callTradeDeco)   
        SetFXTradeAndInstrumentAttributes(putTradeDeco)   
        callTradeDeco.Instrument().OptionType('Call')
        putTradeDeco.Instrument().OptionType('Put')
        self.PricingOptions().CreateRiskReversal(callTradeDeco, putTradeDeco)

    '''*************************************************************'''
    def IsVolatilitySimulated(self):
        retVal = False
        for volatility in ['callVolatility', 'putVolatility']:
            if self.GetAttributeMetaData(volatility, 'isCalculationSimulated')():
                retVal = True
        return retVal
    
    '''*******************************************************
    * Overridden base class methods
    *******************************************************'''
    def BuySellHeader(self, *args):
        return self.BuySellLabel() + ' Call'
