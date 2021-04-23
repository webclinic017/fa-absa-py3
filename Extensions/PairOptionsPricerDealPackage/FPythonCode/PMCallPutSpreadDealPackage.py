
import acm
from PmStrategyDealPackageBase import PmStrategyDealPackageBase
from PairOptionsUtil import SetPMTradeAndInstrumentAttributes
from PairOptionsOneVolatility import OneVolVolatility
from DealPackageDevKit import Settings, Object, List, CalcVal, Action

SHEET_DEFAULT_COLUMNS = []
@Settings(GraphApplicable=False,
          SheetApplicable=False,
          SheetDefaultColumns=SHEET_DEFAULT_COLUMNS)

class PMCallPutSpreadDefinition(PmStrategyDealPackageBase):
    strategyTypeDisplayName =  'Spread'
        
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
    
    foreignOptionType =         Action( label='@ForeignCurrencyLabel',
                                        action='@ChangeCallPut',
                                        recreateCalcSpaceOnChange = True)
    
    domesticOptionType =        Action( label='@DomesticCurrencyLabel',
                                        action='@ChangeCallPut',
                                        recreateCalcSpaceOnChange = True)
    
                                        
    oneVol =          OneVolVolatility( quoteTradeName='QuoteCombinationTrade',
                                        callVolObjectsName='VolatilityCallObject',
                                        putVolObjectsName='VolatilityPutObject')
                                        
    

    # -------------------------------------------------------------------------------
    # Grid View Model
    # -------------------------------------------------------------------------------    
    gridModelView =             List(     )
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, EmptyRow, EmptyCell, B2BRow, Attr, AttrLeft, AttrMid, AttrActionBuySell, AttrActionForeignCurr, AttrActionDomesticCurr
        from PairOptionsPricerGridViewModel import AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrLeftReadOnly, AttrLabelMidBold, LabelWhite, AttrLabelCalcLeft, CustomCalculationsRows
        from PairOptionsPricerGridViewModel import AttrLabelLeft, AttrLabelPriceLeft, AttrLabelBoldLeft, AttrLabelBoldRight, Label, LabelParam, LabelCalc, CurrOrPairAttr, AttrActionLeft
        from PairOptionsPricerGridViewModel import AmountRow, CallPutAmountRow, AttrLeft, AttrLabelMarketDataLeft, AttrLabelMarketDataRight, AttrCalcMarketDataLeftReadOnly, AttrActionRight
        return [
                Row([CurrOrPairAttr('foreignInstrument'), AttrActionLeft('foreignOptionType'), AttrMid('instrumentPair'), AttrActionRight('domesticOptionType'), CurrOrPairAttr('domesticCurrency')]),
                Row([Attr('expiryDate'), AttrLabelBoldLeft('expiryDate'), AttrMid('fixingSource'), AttrLabelBoldRight('daysToExpiry'), AttrLeft('daysToExpiry')]),
                Row([Attr('deliveryDate'), AttrLabelBoldLeft('deliveryDate'), Label(''), AttrLabelBoldRight('daysToDelivery'), AttrLeft('daysToDelivery')]),
                Row([Attr('exerciseType'), AttrLabelBoldLeft('exerciseType'), LabelWhite(self.strategyTypeDisplayName), Label(''), Label('')]),
                Row([Attr('strike2DomesticPerForeign'), AttrLabelLeft('quoteTradeCalcVal_theor'), AttrLabelMidBold('strike2DomesticPerForeign'), Label(''), Label('')]),
                Row([Attr('strikeDomesticPerForeign'), AttrLabelLeft('quoteTradeCalcVal_theor'), AttrLabelMidBold('strikeDomesticPerForeign'), Label(''), Label('')]),
                AmountRow([Attr('amountForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('buySell'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountDomestic')]),
                CallPutAmountRow([Attr('amountCallForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountCallHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountCallDomestic')]),
                CallPutAmountRow([Attr('amountPutForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountPutHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountPutDomestic')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
              
                Row([AttrCalcMarketData('quoteTradeCalcVal_undVal'), AttrLabelMarketDataLeft('quoteTradeCalcVal_undVal'), LabelParam('Spot'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwdPoints'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwdPoints'), LabelParam('Fwd Points'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwd'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwd'), LabelParam('Fwd'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_carryCost'), AttrLabelMarketDataLeft('quoteTradeCalcVal_carryCost'), LabelParam('Carry Cost'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_interestRateForeign'), AttrLabelMarketDataLeft('quoteTradeCalcVal_interestRateForeign'), LabelParam('Interest Rate'), AttrLabelMarketDataRight('quoteTradeCalcVal_interestRateDomestic'), AttrCalcMarketDataLeft('quoteTradeCalcVal_interestRateDomestic')]),                
                Row([AttrCalcMarketData('oneVol_volatility'), AttrLabelMarketDataLeft('oneVol_volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                Row([AttrCalcMarketData('oneVol_callVolatility'), AttrLabelMarketDataLeft('oneVol_callVolatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('oneVol_putVolatility'), AttrCalcMarketDataLeft('oneVol_putVolatility')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
              
                Row([AttrCalc('quoteTradeCalcVal_theor'), AttrLabelPriceLeft('quoteTradeCalcVal_theor'), LabelCalc('Price'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Fwd Delta'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_delta'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Vol Adj Delta'), Label(''), Label('')]),
                
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                CustomCalculationsRows('customCalculations', False),

                Row([Label('Strategy'), Label(''), Label(''), Label('Short'), Label('Long')]),
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
        
    def StrikeDomPerForLabel(self, attrName):
        return 'Long Strike' if attrName == 'strike2DomesticPerForeign' else 'Short Strike'
                
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(PMCallPutSpreadDefinition, self).OnInit()
        self._pricingOptions = acm.FPmSpreadPricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateCallPutSpread(self.DealPackage().TradeAt('long'), self.DealPackage().TradeAt('short'))
            
    def AssemblePackage(self):
        longTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'long')
        shortTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'short')
        SetPMTradeAndInstrumentAttributes(longTradeDeco)
        SetPMTradeAndInstrumentAttributes(shortTradeDeco)
        self.PricingOptions().CreateCallPutSpread(longTradeDeco, shortTradeDeco)
        
        
    '''*************************************************************'''
    def VolatilityCallObject(self):
        for instrMap in self.QuoteCombinationTrade().Instrument().InstrumentMaps(acm.Time.DateToday()):
            if instrMap.Weight() > 0:       # Check weight instead of IsCall flag
                return instrMap

    def VolatilityPutObject(self):
        for instrMap in self.QuoteCombinationTrade().Instrument().InstrumentMaps(acm.Time.DateToday()):
            if instrMap.Weight() < 0:       #  Check weight instead of IsCall flag
                return instrMap
    
    def SetDefaultStrike(self):
        self.solverParameter = 'solverStrike2DomPerFor'
        self.DealPackage().SetAttribute('strikeDomesticPerForeign', '-5pf')
        self.DealPackage().SetAttribute('strike2DomesticPerForeign', '0pf')
        
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
