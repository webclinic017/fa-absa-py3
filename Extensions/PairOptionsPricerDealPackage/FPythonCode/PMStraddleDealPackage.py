
import acm
from DealPackageDevKit import Settings, List, CalcVal
from PmStrategyDealPackageBase import PmStrategyDealPackageBase
from PairOptionsUtil import SetPMTradeAndInstrumentAttributes, GetMaxMinBounderiesStrikeSolving, GetFloatFromCalculation


SHEET_DEFAULT_COLUMNS = []
@Settings(GraphApplicable=False,
          SheetApplicable=False,
          SheetDefaultColumns=SHEET_DEFAULT_COLUMNS)

class PMStraddleDefinition(PmStrategyDealPackageBase):
   
    intrinsicFwd =              CalcVal(label='Fwd',
                                        calcMapping='QuoteTrade:FDealSheet:Intrinsic Option Forward Value% FXOStrat',
                                        solverTopValue=True,
                                        tabStop = False)
                                        
    intrinsicSpot =             CalcVal(label='Spot',
                                        calcMapping='QuoteTrade:FDealSheet:Intrinsic Option Value % FXOStrat',
                                        solverTopValue=True)
    # -------------------------------------------------------------------------------
    # Grid View Model
    # -------------------------------------------------------------------------------    
    gridModelView =             List(     )
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, EmptyRow, EmptyCell, B2BRow, Attr, AttrLeft, AttrMid, AttrActionBuySell, AttrActionForeignCurr, AttrActionDomesticCurr, AttrLabelMarketDataRight
        from PairOptionsPricerGridViewModel import AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrCalcMarketDataLot, CurrOrPairAttr, AttrCalcLeft, AttrLeftReadOnly, AttrLabelMarketDataLeft, CustomCalculationsRows
        from PairOptionsPricerGridViewModel import AttrLabelLeft, AttrLabelPriceLeft, AttrLabelBoldLeft, AttrLabelRight, AttrLabelBoldRight, LabelParam, LabelCalc, AttrCalcMarketDataLeftReadOnly
        from PairOptionsPricerGridViewModel import AmountRow, CallPutAmountRow, AttrActionForeignCurr, AttrActionDomesticCurr, AttrLeft, AttrLabelMidBold, Label, LabelWhite, AttrLabelCalcLeft
        
        return [
                Row([CurrOrPairAttr('foreignInstrument'), Label(''), AttrMid('instrumentPair'), Label(''), CurrOrPairAttr('domesticCurrency')]),
                Row([Attr('expiryDate'), AttrLabelBoldLeft('expiryDate'), AttrMid('fixingSource'), AttrLabelBoldRight('daysToExpiry'), AttrLeft('daysToExpiry')]),
                Row([Attr('deliveryDate'), AttrLabelBoldLeft('deliveryDate'), Label(''), AttrLabelBoldRight('daysToDelivery'), AttrLeft('daysToDelivery')]),
                Row([Attr('exerciseType'), AttrLabelBoldLeft('exerciseType'), LabelWhite('Straddle'), Label(''), Label('')]),
                Row([Attr('strikeDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), Label('Strike'), Label(''), Label('')]),
                Row([AttrCalc('intrinsicFwd'), AttrLabelLeft('intrinsicFwd'), Label('Intrinsic %'), AttrLabelRight('intrinsicSpot'), AttrCalcLeft('intrinsicSpot')]),
                AmountRow([Attr('amountForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('buySell'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountDomestic')]),
                CallPutAmountRow([Attr('amountPutForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountPutHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountPutDomestic')]),
                CallPutAmountRow([Attr('amountCallForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountCallHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountCallDomestic')]),
                
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                Row([AttrCalcMarketData('quoteTradeCalcVal_undVal'), AttrLabelMarketDataLeft('quoteTradeCalcVal_undVal'), LabelParam('Spot'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwdPoints'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwdPoints'), LabelParam('Fwd Points'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwd'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwd'), LabelParam('Fwd'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_carryCost'), AttrLabelMarketDataLeft('quoteTradeCalcVal_carryCost'), LabelParam('Carry Cost'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_interestRateForeign'), AttrLabelMarketDataLeft('quoteTradeCalcVal_interestRateForeign'), LabelParam('Interest Rate'), AttrLabelMarketDataRight('quoteTradeCalcVal_interestRateDomestic'), AttrCalcMarketDataLeft('quoteTradeCalcVal_interestRateDomestic')]),
                Row([AttrCalcMarketDataLot('volatility'), AttrLabelMarketDataLeft('volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                Row([AttrCalc('quoteTradeCalcVal_theor'), AttrLabelPriceLeft('quoteTradeCalcVal_theor'), LabelCalc('Price'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Fwd Delta'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_delta'), AttrLabelCalcLeft('quoteTradeCalcVal_delta'), LabelCalc('Vol Adj Delta'), Label(''), Label('')]),
                
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
    * Solver Parameter Methods
    *******************************************************'''
    def GetStrikeParams(self, fwdPrice):
        params = GetMaxMinBounderiesStrikeSolving(fwdPrice)
        paramsUpper = params.copy()
        params["maxValue"] = fwdPrice
        paramsUpper["minValue"] = fwdPrice
        return [params, paramsUpper]    

    def StrikeParamDomPerFor(self, attributeName):
        fwdPrice = GetFloatFromCalculation(self.quoteTradeCalcVal_fwd)
        return self.GetStrikeParams(fwdPrice)
        
    def UndValParam(self, attrName):
        undVal = GetFloatFromCalculation(self.quoteTradeCalcVal_undVal)
        strike = self.strikeDomesticPerForeign
        if attrName.startswith('flipped'):
            undVal = GetFloatFromCalculation(self.flippedQuoteTradeCalcVal_undVal)
            strike = self.strikeForeignPerDomestic
        return [{'minValue':0.3*undVal, 'maxValue':strike, 'precision':0.001},
                {'minValue':strike, 'maxValue':3.0*undVal}]
                
    '''*******************************************************
    * Deal Package Interface Methods
    *******************************************************'''
    def OnInit(self):
        super(PMStraddleDefinition, self).OnInit()
        self._pricingOptions = acm.FPmStraddlePricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreateStraddle(self.DealPackage().TradeAt('callTrade'), self.DealPackage().TradeAt('putTrade'))

    def AssemblePackage(self):
        callTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'callTrade')
        putTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'putTrade')
        SetPMTradeAndInstrumentAttributes(callTradeDeco)        
        SetPMTradeAndInstrumentAttributes(putTradeDeco)        
        callTradeDeco.Instrument().OptionType('Call')
        putTradeDeco.Instrument().OptionType('Put')
        self.PricingOptions().CreateStraddle(callTradeDeco, putTradeDeco)
  
    '''*************************************************************'''
    def SetDefaultStrike(self):
        self.DealPackage().SetAttribute('strikeDomesticPerForeign', '0d')
