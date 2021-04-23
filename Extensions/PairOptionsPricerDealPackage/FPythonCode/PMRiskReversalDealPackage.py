
import acm
from PmStrategyDealPackageBase import PmStrategyDealPackageBase
from PairOptionsUtil import SetPMTradeAndInstrumentAttributes
from DealPackageDevKit import Settings, Object, CalcVal, Bool, List

SHEET_DEFAULT_COLUMNS = []
@Settings(GraphApplicable=False,
          SheetApplicable=False,
          SheetDefaultColumns=SHEET_DEFAULT_COLUMNS)

class PMRiskReversalDefinition(PmStrategyDealPackageBase):
    strategyTypeDisplayName =  'Risk Reversal'
    
    strike2DomesticPerForeign = Object( defaultValue='atmf',
                                        label='@StrikeDomPerForLabel',
                                        objMapping='PricingOptions.Strike2DomesticPerForeign',
                                        transform='@TransformStrikePrice',
                                        formatter='@StrikeFormatterCB',
                                        recreateCalcSpaceOnChange=True)
    
    solverStrike2DomPerFor =    Object( label='@StrikeDomPerForLabel',
                                        objMapping='PricingOptions.Strike2DomesticPerForeignNoInputFormatter',
                                        solverParameter='@StrikeParamDomPerFor',
                                        onChanged='@SolverStrikeChanged')
    
    volatilitySpread     =     CalcVal( label='Spread %',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Volatility Spread FXOStrat')

    isFavourCallEnabled  =        Bool( objMapping = "IsFavourCallEnabled",
                                        enabled = False,
                                        recreateCalcSpaceOnChange = True)
                                        
    callVolatility =           CalcVal( label='@CallVolatilityLabel',
                                        calcMapping='VolatilityCallObject:FDealSheet:Portfolio Volatility FXOStrat',
                                        onChanged='@ValueSimulated',
                                        transform='@TransformVolatility',
                                        solverParameter='@VolatilityParam')
                                    
    putVolatility =            CalcVal( label='@PutVolatilityLabel',
                                        calcMapping='VolatilityPutObject:FDealSheet:Portfolio Volatility FXOStrat',
                                        onChanged='@ValueSimulated',
                                        transform='@TransformVolatility',
                                        solverParameter='@VolatilityParam')
    
    deltaBS =                  CalcVal( label='Delta BS',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Delta FXOStrat',
                                        transform='@SolveDelta',
                                        solverTopValue=True)
    
    deltaBSCall =              CalcVal( label='Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='CallQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                   
    deltaBSPut =              CalcVal(  label='Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='PutQuoteTrade:FDealSheet:Instrument Delta FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')
                                        
    fwdDeltaBS =               CalcVal( label='Fwd Delta BS',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Forward Delta FXOStrat',
                                        transform='@SolveDelta',
                                        solverTopValue=True)
                                        
    fwdDeltaBSCall =           CalcVal( label='Fwd Delta BS Call',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Forward Delta Call FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')
                                           
    fwdDeltaBSPut =            CalcVal( label='Fwd Delta BS Put',
                                        calcConfiguration='@PriceGreekExcludeVolatilityMovement',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Forward Delta Put FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')

    delta =                    CalcVal( label='Delta',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Delta FXOStrat',
                                        transform='@SolveDelta',
                                        solverTopValue=True)
                                        
    deltaCall =                CalcVal( label='Delta Call',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Delta Call FXOStrat',
                                        solverTopValue='solverStrike2DomPerFor')                                   
                                    
    deltaPut =                 CalcVal( label='Delta Put',
                                        calcMapping='QuoteCombinationTrade:FDealSheet:Instrument Delta Put FXOStrat',
                                        solverTopValue='solverStrikeDomPerFor')

    intrinsicFwd =             CalcVal( label='Fwd',
                                        calcMapping='PutQuoteTrade:FDealSheet:Intrinsic Option Forward Value% FXOStrat',
                                        solverTopValue=True,
                                        tabStop = False)
                                        
    intrinsicSpot =            CalcVal( label='Spot',
                                        calcMapping='PutQuoteTrade:FDealSheet:Intrinsic Option Value % FXOStrat',
                                        solverTopValue=True)
                                        
    intrinsic2Fwd =            CalcVal( label='Fwd',
                                        calcMapping='CallQuoteTrade:FDealSheet:Intrinsic Option Forward Value% FXOStrat',
                                        solverTopValue=True)
                                        
    intrinsic2Spot =           CalcVal( label='Spot',
                                        calcMapping='CallQuoteTrade:FDealSheet:Intrinsic Option Value % FXOStrat',
                                        solverTopValue=True)
                                        
                                        
    
    
    # -------------------------------------------------------------------------------
    # Grid View Model
    # -------------------------------------------------------------------------------    
    gridModelView =             List(     )
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, EmptyRow, EmptyCell, B2BRow, Attr, AttrLeft, AttrMid, AttrActionBuySell, AttrActionForeignCurr, AttrActionDomesticCurr, AttrLabelMarketDataLeft
        from PairOptionsPricerGridViewModel import AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrLeftReadOnly, AttrLabelMarketDataRight, AttrCalcMarketDataLeftReadOnly, CustomCalculationsRows
        from PairOptionsPricerGridViewModel import AttrLabelLeft, AttrLabelPriceLeft, AttrLabelBoldLeft, AttrLabelBoldRight, Label, LabelParam, AttrLabelMidBold, LabelWhite, AttrLabelCalcLeft
        from PairOptionsPricerGridViewModel import AmountRow, CallPutAmountRow, AttrActionForeignCurr, AttrActionDomesticCurr, AttrLeft, AttrLabelMidBold, LabelCalc, CurrOrPairAttr
        return [
                Row([CurrOrPairAttr('foreignInstrument'), Label(''), AttrMid('instrumentPair'), Label(''), CurrOrPairAttr('domesticCurrency')]),
                Row([Attr('expiryDate'), AttrLabelBoldLeft('expiryDate'), AttrMid('fixingSource'), AttrLabelBoldRight('daysToExpiry'), AttrLeft('daysToExpiry')]),
                Row([Attr('deliveryDate'), AttrLabelBoldLeft('deliveryDate'), Label(''), AttrLabelBoldRight('daysToDelivery'), AttrLeft('daysToDelivery')]),
                Row([Attr('exerciseType'), AttrLabelBoldLeft('exerciseType'), LabelWhite(self.strategyTypeDisplayName), Label(''), Label('')]),
                Row([Attr('strikeDomesticPerForeign'), AttrLabelLeft('quoteTradeCalcVal_theor'), AttrLabelMidBold('strikeDomesticPerForeign'), Label(''), Label('')]),
                Row([Attr('strike2DomesticPerForeign'), AttrLabelLeft('quoteTradeCalcVal_theor'), AttrLabelMidBold('strike2DomesticPerForeign'), Label(''), Label('')]),
                AmountRow([Attr('amountForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('buySell'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountDomestic')]),
                CallPutAmountRow([Attr('amountPutForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountPutHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountPutDomestic')]),
                CallPutAmountRow([Attr('amountCallForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountCallHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountCallDomestic')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
              
                Row([AttrCalcMarketData('quoteTradeCalcVal_undVal'), AttrLabelMarketDataLeft('quoteTradeCalcVal_undVal'), LabelParam('Spot'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwdPoints'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwdPoints'), LabelParam('Fwd Points'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwd'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwd'), LabelParam('Fwd'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_carryCost'), AttrLabelMarketDataLeft('quoteTradeCalcVal_carryCost'), LabelParam('Carry Cost'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_interestRateForeign'), AttrLabelMarketDataLeft('quoteTradeCalcVal_interestRateForeign'), LabelParam('Interest Rate'), AttrLabelMarketDataRight('quoteTradeCalcVal_interestRateDomestic'), AttrCalcMarketDataLeft('quoteTradeCalcVal_interestRateDomestic')]),                
                Row([AttrCalcMarketData('volatilitySpread'), AttrLabelMarketDataLeft('volatilitySpread'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                Row([AttrCalcMarketData('callVolatility'), AttrLabelMarketDataLeft('callVolatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('putVolatility'), AttrCalcMarketDataLeft('putVolatility')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
              
                Row([AttrCalc('quoteTradeCalcVal_theor'), AttrLabelPriceLeft('quoteTradeCalcVal_theor'), LabelCalc('Price'), Label(''), Label('')]),
                Row([AttrCalc('deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta'), Label(''), Label('')]),
                Row([AttrCalc('fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Fwd Delta'), Label(''), Label('')]),
                Row([AttrCalc('delta'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Vol Adj Delta'), Label(''), Label('')]),
                
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                CustomCalculationsRows('customCalculations', False),

                Row([Label('Strategy'), Label(''), Label(''), Label('Put'), Label('Call')]),
                Row([AttrCalc('saveTradeCalcVal_theorVal'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal'), AttrCalc('theorValPutSaveTrade'), AttrCalc('theorValCallSaveTrade')]),
                Row([AttrCalc('saveTradeCalcVal_theorValNoPremium'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal Ins'), AttrCalc('theorValNoPremPutSaveTrade'), AttrCalc('theorValNoPremCallSaveTrade')]),
                B2BRow([Attr('b2b_b2bPrice'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bPrice'), Attr('b2bPut_b2bPrice'), AttrCalc('b2bCall_b2bPrice')]),
                B2BRow([Attr('b2b_b2bMargin'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bMargin'), Attr('b2bPut_b2bMargin'), AttrCalc('b2bCall_b2bMargin')]),
                Row([AttrCalc('tradePrice'), AttrLeftReadOnly('saveTradeQuotation'), Label('Price'), AttrCalc('putTradePrice'), AttrCalc('callTradePrice')]),
                Row([AttrCalc('tradePremium'), AttrLeftReadOnly('premiumCurrency'), Label('Premium'), AttrCalc('putTradePremium'), AttrCalc('callTradePremium')]),
               ]
                               
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
        
    def StrikeDomPerForLabel(self, attrName):
        if attrName == 'strike2DomesticPerForeign':
            return 'Call Strike'
        else:
            return 'Put Strike'
            
    def BuySellHeader(self, *args):
        return self.BuySellLabel() + ' Call'
        
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(PMRiskReversalDefinition, self).OnInit()
        self._pricingOptions = acm.FPmRiskReversalPricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateRiskReversal(self.DealPackage().TradeAt('callTrade'), self.DealPackage().TradeAt('putTrade'))
        
    def AssemblePackage(self):
        callTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'callTrade')
        putTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'putTrade')
        SetPMTradeAndInstrumentAttributes(callTradeDeco)   
        SetPMTradeAndInstrumentAttributes(putTradeDeco)   
        callTradeDeco.Instrument().OptionType('Call')
        putTradeDeco.Instrument().OptionType('Put')
        self.PricingOptions().CreateRiskReversal(callTradeDeco, putTradeDeco)
    
    '''*************************************************************'''
    def SetDefaultStrike(self):
        self.DealPackage().SetAttribute('strikeDomesticPerForeign', '-2p')
        self.DealPackage().SetAttribute('strike2DomesticPerForeign', '-2p')
        
    def GetDeltaTraitsList(self):
        return ['deltaCall', 'deltaPut']
        
    def IsVolatilitySimulated(self):
        retVal = False
        for volatility in ['callVolatility', 'putVolatility']:
            if self.GetAttributeMetaData(volatility, 'isCalculationSimulated')():
                retVal = True
        return retVal
