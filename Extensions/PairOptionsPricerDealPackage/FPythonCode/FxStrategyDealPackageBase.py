import acm
from StrategyDealPackageBase import StrategyDealPackageBase
from PairOptionsUtil import UsePerUnitQuotationImpl, GetFloatFromCalculation, UpdateDealPackageTradeLink, lot
from FXCalculations import LeftSideFXCalculations, RightSideFXCalculations, SaveTradeCalculations
from DealPackageDevKit import Object, Settings, CalcVal, List, ParseFloat

@Settings(GraphApplicable=True,
          SheetApplicable=False,
          ShowGraphInitially=False)
          
class FxStrategyDealPackageBase(StrategyDealPackageBase):
    strategyTypeDisplayName =  ''
    
    quoteTradeCalcVal =         LeftSideFXCalculations( sideName='Foreign',
                                        strategyTradeMethodName = 'QuoteCombinationTrade',
                                        altStrategyTradeMethodName = 'AltQuoteCombinationTrade',
                                        tradeMethodName = 'CallQuoteTrade',
                                        altTradeMethodName = 'CallAltQuoteTrade')
    
    flippedQuoteTradeCalcVal =  RightSideFXCalculations( sideName='Domestic',
                                        strategyTradeMethodName = 'FlippedQuoteCombinationTrade',
                                        altStrategyTradeMethodName = 'FlippedAltQuoteCombinationTrade',
                                        tradeMethodName = 'CallFlippedQuoteTrade',
                                        altTradeMethodName = 'CallFlippedAltQuoteTrade')
                                        
    intrinsicFwd =              CalcVal(label='Fwd',
                                        calcMapping='PutQuoteTrade:FDealSheet:Intrinsic Option Forward Value% FXOStrat',
                                        solverTopValue=True,
                                        tabStop = False)
                                        
    intrinsicSpot =             CalcVal(label='Spot',
                                        calcMapping='PutQuoteTrade:FDealSheet:Intrinsic Option Value % FXOStrat',
                                        solverTopValue=True)
                                        
    saveTradeCalcVal =          SaveTradeCalculations('SaveQuoteCombinationTrade')
    
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************'''                            
    def LeadTradeName(self):
        return 'callTrade'
    
    def LeadTrade(self):
        return self.TradeAt(self.LeadTradeName())
    
    def QuoteTrade(self):
        return self.CallQuoteTrade()
    
    def QuoteInstrument(self):
        return self.QuoteTrade().Instrument()
        
    def CallQuoteTrade(self):
        return self.CallPairOptionsPricer().QuoteTrade()

    def CallAltQuoteTrade(self):
        return self.CallPairOptionsPricer().AltQuoteTrade()

    def CallFlippedQuoteTrade(self):
        return self.CallPairOptionsPricer().FlippedQuoteTrade()
    
    def CallFlippedAltQuoteTrade(self):
        return self.CallPairOptionsPricer().FlippedAltQuoteTrade()
        
    def PutQuoteTrade(self):
        return self.PutPairOptionsPricer().QuoteTrade()

    def PutAltQuoteTrade(self):
        return self.PutPairOptionsPricer().AltQuoteTrade()

    def PutFlippedQuoteTrade(self):
        return self.PutPairOptionsPricer().FlippedQuoteTrade()
    
    def PutFlippedAltQuoteTrade(self):
        return self.PutPairOptionsPricer().FlippedAltQuoteTrade()
        
    def CallPairOptionsPricer(self):
        return self.PricingOptions().CallPairOptionsPricer()
    
    def PutPairOptionsPricer(self):
        return self.PricingOptions().PutPairOptionsPricer()

    def CurrentCallSaveTrade(self):
        return self.CallPairOptionsPricer().CurrentSaveTrades().First()
    
    def CurrentPutSaveTrade(self):
        return self.PutPairOptionsPricer().CurrentSaveTrades().First()
            
    def AltQuoteCombinationTrade(self):
        return self.PricingOptions().AltQuoteCombinationTrade()
                
    def FlippedQuoteCombinationTrade(self):
        return self.PricingOptions().FlippedQuoteCombinationTrade()
            
    def FlippedAltQuoteCombinationTrade(self):
        return self.PricingOptions().FlippedAltQuoteCombinationTrade()
        
    def PremiumQuotedForeignTrade(self):
        return self.AltQuoteCombinationTrade() if self.IsPremiumAdjusted() else self.QuoteCombinationTrade()
        
    def PremiumQuotedDomesticTrade(self):
        return self.FlippedQuoteCombinationTrade() if self.IsPremiumAdjusted() else self.FlippedAltQuoteCombinationTrade()
        
    def SaveQuoteCombinationTrade(self):
        return self.PremiumQuotedDomesticTrade() if self.PricingOptions().CurrentSaveIsFlipped() else self.PremiumQuotedForeignTrade()

    def VolatilityObjectsAsLot(self):
        combInstrMaps = []
        for tradeMethodName in ['QuoteCombinationTrade', 'AltQuoteCombinationTrade', 'FlippedQuoteCombinationTrade', 'FlippedAltQuoteCombinationTrade']:
            combInstrMaps.extend(getattr(self, tradeMethodName)().Instrument().InstrumentMaps(acm.Time.DateToday()))
        return lot(combInstrMaps)
        
    def VolatilityCallObjectsAsLot(self):
        combInstrMaps = []
        for tradeMethodName in ['QuoteCombinationTrade', 'AltQuoteCombinationTrade', 'FlippedQuoteCombinationTrade', 'FlippedAltQuoteCombinationTrade']:
            for instrMap in getattr(self, tradeMethodName)().Instrument().InstrumentMaps(acm.Time.DateToday()):
                if instrMap.Instrument().IsCall() != tradeMethodName.startswith('Flipped'):
                    combInstrMaps.append(instrMap)
        return lot(combInstrMaps)
     
    def VolatilityPutObjectsAsLot(self):
        combInstrMaps = []
        for tradeMethodName in ['QuoteCombinationTrade', 'AltQuoteCombinationTrade', 'FlippedQuoteCombinationTrade', 'FlippedAltQuoteCombinationTrade']:
            for instrMap in getattr(self, tradeMethodName)().Instrument().InstrumentMaps(acm.Time.DateToday()):
                if instrMap.Instrument().IsCall() == tradeMethodName.startswith('Flipped'):
                    combInstrMaps.append(instrMap)
        return lot(combInstrMaps)
        
    def DomesticColumnConfig(self, *attr):
        return self.quoteTradeCalcVal.DomesticColumnConfig(*attr)

    #***************************************                              
    #*********** GRID VIEW MODEL ***********
    gridModelView =       List(     )
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, B2BRow, EmptyRow, EmptyCell, CallPutAmountRow, AmountRow, AttrActionForeignCurr, AttrActionDomesticCurr
        from PairOptionsPricerGridViewModel import Attr, CurrOrPairAttr, CurrOrPairAttrLeft, AttrMid, AttrLeft, AttrActionBuySell, AttrLeftReadOnly, AttrCalcMarketDataLeftReadOnly
        from PairOptionsPricerGridViewModel import AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrCalcMarketDataLot, AttrCalcLeft
        from PairOptionsPricerGridViewModel import AttrLabelLeft, AttrLabelPriceLeft, AttrLabelPriceRight, AttrLabelBoldLeft, AttrLabelRight, AttrLabelBoldRight, AttrLabelMidBold
        from PairOptionsPricerGridViewModel import Label, LabelParam, LabelCalc, LabelWhite, AttrLabelMarketDataRight, AttrLabelMarketDataLeft, AttrLabelCalcLeft, AttrLabelCalcRight
        from PairOptionsPricerGridViewModel import AttrActionForeignCurr, AttrActionDomesticCurr, AttrLeft, AttrLabelMidBold, CustomCalculationsRows
        return  [
                Row([CurrOrPairAttr('foreignInstrument'), Label(''), AttrMid('instrumentPair'), Label(''), CurrOrPairAttrLeft('domesticCurrency')]),
                Row([Attr('expiryDate'), AttrLabelBoldLeft('expiryDate'), AttrMid('fixingSource'), AttrLabelBoldRight('daysToExpiry'), AttrLeft('daysToExpiry')]),
                Row([Attr('deliveryDate'), AttrLabelBoldLeft('deliveryDate'), Label(''), AttrLabelBoldRight('daysToDelivery'), AttrLeft('daysToDelivery')]),
                Row([Attr('exerciseType'), AttrLabelBoldLeft('exerciseType'), LabelWhite(self.strategyTypeDisplayName), AttrLabelBoldRight('exerciseType'), AttrLeft('exerciseType')]),
                Row([Attr('strikeDomesticPerForeign'), AttrLabelLeft('quoteTradeCalcVal_theor'), AttrLabelMidBold('strikeDomesticPerForeign'), AttrLabelRight('flippedQuoteTradeCalcVal_theor'), AttrLeft('strikeForeignPerDomestic')]),
                AmountRow([Attr('amountForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('buySell'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountDomestic')]),
                CallPutAmountRow([Attr('amountPutForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountPutHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountPutDomestic')]),
                CallPutAmountRow([Attr('amountCallForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('amountCallHeader'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountCallDomestic')]),
                
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                Row([AttrCalcMarketData('quoteTradeCalcVal_undVal'), AttrLabelMarketDataLeft('quoteTradeCalcVal_undVal'), LabelParam('Spot'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_undVal'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_undVal')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwdPoints'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwdPoints'), LabelParam('Fwd Points'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_fwdPoints'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_fwdPoints')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwd'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwd'), LabelParam('Fwd'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_fwd'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_fwd')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_interestRate'), AttrLabelMarketDataLeft('quoteTradeCalcVal_interestRate'), LabelParam('Interest Rate'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_interestRate'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_interestRate')]),
                Row([AttrCalcMarketDataLot('volatility'), AttrLabelMarketDataLeft('volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                                
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),

                Row([AttrCalc('quoteTradeCalcVal_theorPct'), AttrLabelPriceLeft('quoteTradeCalcVal_theorPct'), LabelCalc('Price Foreign'), AttrLabelPriceRight('flippedQuoteTradeCalcVal_theor'), AttrCalcLeft('flippedQuoteTradeCalcVal_theor')]),
                Row([AttrCalc('quoteTradeCalcVal_theor'), AttrLabelPriceLeft('quoteTradeCalcVal_theor'), LabelCalc('Price Domestic'), AttrLabelPriceRight('flippedQuoteTradeCalcVal_theorPct'), AttrCalcLeft('flippedQuoteTradeCalcVal_theorPct')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBS'), AttrCalcLeft('flippedQuoteTradeCalcVal_deltaBS')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBSAlt'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBSAlt'), LabelCalc('Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBSAlt'), AttrCalcLeft('flippedQuoteTradeCalcVal_deltaBSAlt')]),
                Row([AttrCalc('quoteTradeCalcVal_fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Fwd Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_fwdDeltaBS'), AttrCalcLeft('flippedQuoteTradeCalcVal_fwdDeltaBS')]),
                Row([AttrCalc('quoteTradeCalcVal_delta'), AttrLabelCalcLeft('quoteTradeCalcVal_delta'), LabelCalc('Vol Adj Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_delta'), AttrCalcLeft('flippedQuoteTradeCalcVal_delta')]),
               
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                CustomCalculationsRows('customCalculations'),
                
                Row([Label('Strategy'), Label(''), Label(''), Label('Put'), Label('Call')]),
                Row([AttrCalc('saveTradeCalcVal_theorVal'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal'), AttrCalc('theorValPutSaveTrade'), AttrCalc('theorValCallSaveTrade')]),
                Row([AttrCalc('saveTradeCalcVal_theorValNoPremium'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal Ins'), AttrCalc('theorValNoPremPutSaveTrade'), AttrCalc('theorValNoPremCallSaveTrade')]),
                B2BRow([Attr('b2b_b2bPrice'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bPrice'), Attr('b2bPut_b2bPrice'), AttrCalc('b2bCall_b2bPrice')]),
                B2BRow([Attr('b2b_b2bMargin'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bMargin'), Attr('b2bPut_b2bMargin'), AttrCalc('b2bCall_b2bMargin')]),
                Row([AttrCalc('tradePrice'), AttrLeftReadOnly('saveTradeQuotation'), Label('Price'), AttrCalc('putTradePrice'), AttrCalc('callTradePrice')]),
                Row([AttrCalc('tradePremium'), AttrLeftReadOnly('premiumCurrency'), Label('Premium'), AttrCalc('putTradePremium'), AttrCalc('callTradePremium')]),
               ]
              
    
    '''*******************************************************
    * Helper Methods
    *******************************************************'''  
    def SetNewSaveTradeOnDealPackage(self):
        UpdateDealPackageTradeLink(self.DealPackage(), self.CurrentCallSaveTrade().Trade(), 'callTrade')
        UpdateDealPackageTradeLink(self.DealPackage(), self.CurrentPutSaveTrade().Trade(), 'putTrade')
       
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************''' 
    def ForeignStrategyOrTradeGreek(self):
        return self.quoteTradeCalcVal.ForeignStrategyOrTradeGreek()
        
    def DomesticStrategyOrTradeGreek(self):
        return self.flippedQuoteTradeCalcVal.DomesticStrategyOrTradeGreek()
    
    def FwdDeltaBSForeignLabel(self):
        return self.quoteTradeCalcVal.ForeignGreekLabel()
        
    def FwdDeltaBSDomesticLabel(self):
        return self.flippedQuoteTradeCalcVal.DomesticGreekLabel()
            
    '''*******************************************************
    * Calculation Configuration
    *******************************************************'''                            
    def UsePerUnitQuotation(self, attrName):
        return UsePerUnitQuotationImpl(attrName)
        
    '''*******************************************************
    * Label methods
    *******************************************************''' 
    def StrikeDomPerForLabel(self, attrName):
        return 'Strike'
    
    '''*******************************************************
    * Solver methods
    *******************************************************'''    
    def UndValParam(self, attrName):
        if attrName.startswith('flipped'):
            undValAttr = 'flippedQuoteTradeCalcVal_undVal'
            strike = self.strikeForeignPerDomestic
        else:
            undValAttr = 'quoteTradeCalcVal_undVal'
            strike = self.strikeDomesticPerForeign
        try:
            undVal = GetFloatFromCalculation(getattr(self, undValAttr))
        except:
            #Will get an exeption on initialization before calculation is created.
            undVal = 1.0
        return [{'minValue':0.3*undVal, 'maxValue':strike, 'precision':0.001},
                {'minValue':strike, 'maxValue':3.0*undVal}]
        
    '''*******************************************************
    * Action methods
    *******************************************************'''     
    def ChangeCallPut(self, *args):
        pass
    
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_FxStrategyDealPackage')
    
    def IsCurrentlyPutOption(self):
        return False

    '''*******************************************************
    * Overridden base class methods
    *******************************************************'''
    def TransformDelta(self, attrName, value):
        delta = ParseFloat(value, formatter=self.deltaCall)
        delta = abs(delta)
        
        callDelta = -delta if attrName.startswith('flipped') else delta
        putDelta = -callDelta
        
        attr = attrName.split('_')[1]
        if attr.endswith('Alt'):
            attr = attr[:-3]
        if attrName.startswith('flipped'):
            attr += 'Flipped'
        if attrName.endswith('Alt'):
            attr += 'Alt'
        callAttr = attr + "Call"
        putAttr = attr + "Put"
        
        if callAttr.endswith('AltCall'):
            callStrike = self.SolveStrikeForPremiumAdjustedDelta('solverStrike2DomPerFor', callAttr, callDelta)
            putStrike = self.SolveStrikeForPremiumAdjustedDelta('solverStrikeDomPerFor', putAttr, putDelta)
        else:
            callStrike = self.Solve(callAttr, 'solverStrike2DomPerFor', callDelta)
            putStrike = self.Solve(putAttr, 'solverStrikeDomPerFor', putDelta)
        
        self.strike2DomesticPerForeign = callStrike
        self.strikeDomesticPerForeign = putStrike
               
        calcCopy = self.GetCalculationsCopy(setBidAsk = False)
        
        return self.GetValueToStore(attrName, calcCopy.Value(attrName).Value())


    def TransformFlippedDelta(self, attrName, value):
         return self.TransformDelta(attrName, value)
         
    def TransformPremiumAdjustedDelta(self, attrName, value):
        return self.TransformDelta(attrName, value)
