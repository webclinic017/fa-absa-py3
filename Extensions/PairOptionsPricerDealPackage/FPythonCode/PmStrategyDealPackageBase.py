import acm
from StrategyDealPackageBase import StrategyDealPackageBase
from PMCalculations import PMCalculations
from PairOptionsUtil import lot, QuotationLabel
from DealPackageDevKit import CalcVal, List, ParseFloat

class PmStrategyDealPackageBase(StrategyDealPackageBase):

    quoteTradeCalcVal =         PMCalculations( tradeMethodName = 'QuoteTrade', strategyCombinationName = 'QuoteCombinationTrade')
    
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************''' 
    def QuoteTrade(self):
        return self.Trade()  

    def QuoteInstrument(self):
        return self.Instrument()

    def PutPairOptionsPricer(self):
        return self.PricingOptions().PutPairOptionsPricer()

    def CallPairOptionsPricer(self):
        return self.PricingOptions().CallPairOptionsPricer()
    
    def PutQuoteTrade(self):
        return self.PutPairOptionsPricer().QuoteTrade()
    
    def CallQuoteTrade(self):
        return self.CallPairOptionsPricer().QuoteTrade()

    def LeadTrade(self):
        return self.Trade()
    
    def VolatilityObjectsAsLot(self):
        return lot(self.QuoteCombinationTrade().Instrument().InstrumentMaps(acm.Time.DateToday()))
    
    def VolatilityCallObject(self):
        for instrMap in self.QuoteCombinationTrade().Instrument().InstrumentMaps(acm.Time.DateToday()):
            if instrMap.Instrument().IsCall():
                return instrMap

    def VolatilityPutObject(self):
        for instrMap in self.QuoteCombinationTrade().Instrument().InstrumentMaps(acm.Time.DateToday()):
            if not instrMap.Instrument().IsCall():
                return instrMap
    
    def DomesticColumnConfig(self, *attr):
        pass
        
    def CustomCalcLabel(self, *args):
        return QuotationLabel(self.QuoteTrade())
        
    def PremiumQuotedForeignTrade(self):
        return self.QuoteCombinationTrade()
   
    '''*******************************************************
    * On Changed Methods
    *******************************************************'''
    def UpdateDealPackageTrade(self, attr, oldVal, newVal, userInputtedAttr):
        pass
       
    '''*******************************************************
    * Solver Parameter Methods
    *******************************************************'''
    def StrikeParamForPerDom(self, *args):
        return {'minValue': 0, 'maxValue': 0, 'precision' : 0.0001}

    '''*******************************************************
    * Action Methods
    *******************************************************'''        
    def SetForeignAsSaveSide(self, *args):
        pass
        
    def SetDomesticAsSaveSide(self, *args):
        pass

    def FlipPremiumCurrency(self, *args):
        pass
        
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************''' 
    def OnInit(self):
        super(PmStrategyDealPackageBase, self).OnInit()
        self._storedPricingParameters = {'quoteTradeCalcVal_undVal':None,
                                         'quoteTradeCalcVal_interestRateForeign':None,
                                         'quoteTradeCalcVal_interestRateDomestic':None,
                                         'fxSpotRateBidAsk':None,
                                         'fxSpotRate':None} 
                                         #'atmVolatility':None}
        
    def OnNew(self):
        super(PmStrategyDealPackageBase, self).OnNew()
        self.amountForeign = 1000
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_PmStrategyDealPackage')
        
    def SolveDelta(self, attrName, value):
        delta = ParseFloat(value, formatter=self.deltaCall)
        delta = abs(delta)
        
        if "flipped" in attrName.lower():
            callDelta = -delta
        else:
            callDelta = delta
    
        putDelta = -callDelta
                
        callAttr = attrName + "Call"
        putAttr = attrName + "Put"
        
        callStrike = self.Solve(callAttr, 'solverStrike2DomPerFor', callDelta)
        putStrike = self.Solve(putAttr, 'solverStrikeDomPerFor', putDelta)
            
        self.strikeDomesticPerForeign = putStrike
        self.strike2DomesticPerForeign = callStrike
    
        return getattr(self, attrName).FormattedValue()
