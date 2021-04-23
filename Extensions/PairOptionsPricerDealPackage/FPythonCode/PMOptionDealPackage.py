
import acm
from DealPackageDevKit import Settings, List
from SinglePairOptionDealPackage import SinglePairOptionDealPackage
from PairOptionsUtil import SetPMTradeAndInstrumentAttributes, QuotationLabel
from PMCalculations import PMCalculations

SHEET_DEFAULT_COLUMNS = []
@Settings(GraphApplicable=False,
          SheetApplicable=False,
          SheetDefaultColumns=SHEET_DEFAULT_COLUMNS)
          
class PMOptionDefinition(SinglePairOptionDealPackage):
    quoteTradeCalcVal =         PMCalculations( tradeMethodName = 'QuoteTrade')
   
    # -------------------------------------------------------------------------------
    # Grid View Model
    # -------------------------------------------------------------------------------    
    gridModelView =             List(     )
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import Row, EmptyRow, EmptyCell, BarrierRow, VanillaRow, DigitalEuropeanRow, DigitalAmericanRow, NotDigitalAmericanRow, B2BRow, AttrActionBuySell
        from PairOptionsPricerGridViewModel import SingleBarrierRow, DoubleBarrierRow, VannaVolgaRow, NotVannaVolgaRow, AttrLabelMarketDataRight, AttrLabelMarketDataLeft, AttrCalcMarketDataLeftReadOnly
        from PairOptionsPricerGridViewModel import Attr, AttrLeft, CurrOrPairAttr, OptionTypeAttr, CurrOrPairAttrLeft, AttrMid, AttrActionLeft, AttrActionRight, AttrActionForeignCurr, AttrLabelCalcLeft
        from PairOptionsPricerGridViewModel import AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrCalcLeft, AttrLabelPriceLeft, AttrActionDomesticCurr, AttrLeftReadOnly, CustomCalculationsRows
        from PairOptionsPricerGridViewModel import AttrLabelLeft, AttrLabelBoldLeft, AttrLabelRight, AttrLabelBoldRight, Label, LabelParam, LabelCalc, AttrLabelMidBold, NotDigitalRow
        return [
                Row([CurrOrPairAttr('foreignInstrument'), AttrActionLeft('foreignOptionType'), AttrMid('instrumentPair'), AttrActionRight('domesticOptionType'), CurrOrPairAttrLeft('domesticCurrency')]),
                Row([Attr('expiryDate'), AttrLabelBoldLeft('expiryDate'), AttrMid('fixingSource'), AttrLabelBoldRight('daysToExpiry'), AttrLeft('daysToExpiry')]),
                Row([Attr('deliveryDate'), AttrLabelBoldLeft('deliveryDate'), Label(''), AttrLabelBoldRight('daysToDelivery'), AttrLeft('daysToDelivery')]),
                VanillaRow([OptionTypeAttr('exerciseType'), AttrLabelBoldLeft('exerciseType'), AttrMid('baseType'), Label(''), Label('')]),
                BarrierRow([OptionTypeAttr('barrierTypeForeign'), AttrLabelBoldLeft('barrierTypeForeign'), AttrMid('baseType'), Label(''), Label('')]),
                DigitalEuropeanRow([OptionTypeAttr('digitalEuropeanTypeForeign'), AttrLabelBoldLeft('digitalEuropeanTypeForeign'), AttrMid('baseType'), Label(''), Label('')]),
                DigitalAmericanRow([OptionTypeAttr('digitalAmericanTypeForeign'), AttrLabelBoldLeft('digitalAmericanTypeForeign'), AttrMid('baseType'), Label(''), Label('')]),
                NotDigitalAmericanRow([Attr('strikeDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), Label('Strike'), Label(''), Label('')]),
                SingleBarrierRow([Attr('barrierDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), AttrLabelMidBold('barrierDomesticPerForeign'), Label(''), Label('')]),
                DoubleBarrierRow([Attr('doubleBarrierDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), AttrLabelMidBold('doubleBarrierDomesticPerForeign'), Label(''), Label('')]),
                Row([AttrCalc('intrinsicFwd'), AttrLabelLeft('intrinsicFwd'), Label('Intrinsic %'), AttrLabelRight('intrinsicSpot'), AttrCalcLeft('intrinsicSpot')]),
                Row([Attr('amountForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('buySell'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountDomestic')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                Row([AttrCalcMarketData('quoteTradeCalcVal_undVal'), AttrLabelMarketDataLeft('quoteTradeCalcVal_undVal'), LabelParam('Spot'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwdPoints'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwdPoints'), LabelParam('Fwd Points'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwd'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwd'), LabelParam('Fwd'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_carryCost'), AttrLabelMarketDataLeft('quoteTradeCalcVal_carryCost'), LabelParam('Carry Cost'), Label(''), Label('')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_interestRateForeign'), AttrLabelMarketDataLeft('quoteTradeCalcVal_interestRateForeign'), LabelParam('Interest Rate'), AttrLabelMarketDataRight('quoteTradeCalcVal_interestRateDomestic'), AttrCalcMarketDataLeft('quoteTradeCalcVal_interestRateDomestic')]),
                NotVannaVolgaRow([AttrCalcMarketData('volatility'), AttrLabelMarketDataLeft('volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                VannaVolgaRow([AttrCalcMarketData('atmVolatility'), AttrLabelMarketDataLeft('volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                VannaVolgaRow([AttrCalcMarketData('vannaVolgaDelta'), AttrLabelMarketDataLeft('vannaVolgaDelta'), LabelParam('Vanna Volga Adj'), AttrLabelMarketDataRight('vannaVolgaAdjustmentFactor'), AttrCalcMarketDataLeft('vannaVolgaAdjustmentFactor')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                Row([AttrCalc('quoteTradeCalcVal_theor'), AttrLabelPriceLeft('quoteTradeCalcVal_theor'), LabelCalc('Price'), Label(''), Label('')]),
                NotDigitalRow([AttrCalc('quoteTradeCalcVal_breakEvenPrice'), AttrLabelCalcLeft('quoteTradeCalcVal_breakEvenPrice'), LabelCalc('Breakeven'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Fwd Delta'), Label(''), Label('')]),
                Row([AttrCalc('quoteTradeCalcVal_delta'), AttrLabelCalcLeft('quoteTradeCalcVal_delta'), LabelCalc('Vol Adj Delta'), Label(''), Label('')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                CustomCalculationsRows('customCalculations', False),

                Row([Label('Trade'), Label(''), Label(''), Label(''), Label('')]),
                Row([AttrCalc('saveTradeCalcVal_theorVal'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal'), Label(''), Label('')]),
                Row([AttrCalc('saveTradeCalcVal_theorValNoPremium'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal Ins'), Label(''), Label('')]),
                B2BRow([Attr('b2b_b2bPrice'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bPrice'), Label(''), Label('')]),
                B2BRow([Attr('b2b_b2bMargin'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bMargin'), Label(''), Label('')]),
                Row([AttrCalc('tradePrice'), AttrLeftReadOnly('saveTradeQuotation'), Label('Price'), Label(''), Label('')]),
                Row([AttrCalc('tradePremium'), AttrLeftReadOnly('premiumCurrency'), Label('Premium'), Label(''), Label('')]),
               ]

    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************'''                            
    def Trade(self):
        return self.TradeAt('pmoTrade')

    def Instrument(self):
        return self.InstrumentAt('pmoTrade')
        
    def DeltaHedge(self):
        return self.DeltaHedgeParamsAt('pmoTrade')

    def B2B(self):
        return self.B2BTradeParamsAt('pmoTrade')

    def QuoteTrade(self):
        return self.PricingOptions().QuoteTrade()  

    def QuoteInstrument(self):
        return self.QuoteTrade().Instrument()    

    def LeadTrade(self):
        return self.Trade()
    
    def VolatilityObjectsAsLot(self):
        return self.QuoteTrade()
   
    '''*******************************************************
    * On Changed Methods
    *******************************************************'''
    def UpdateDealPackageTrade(self, attr, oldVal, newVal, userInputtedAttr):
        pass
        
    '''*******************************************************
    * Enabled methods
    *******************************************************''' 
    def AmountFieldDisabled(self, currency):
        if self.payoutCurrency:
            return self.IsDigital() and self.payoutCurrency != currency
        else:
            return self.IsDigital() and self.foreignInstrument != currency
        
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
    * Solver Parameter Methods
    *******************************************************'''
    def StrikeParamForPerDom(self, *args):
        return {'minValue': 0, 'maxValue': 0, 'precision' : 0.0001}

    '''*******************************************************
    * Overridden base class methods
    *******************************************************'''
    def UpdateConstellationsWithNewSaveTrade(self, newSaveTrade):
        self.B2BTradeParamsAt('pmoTrade').Trade(newSaveTrade)  
        #self.DeltaHedgeParamsAt('pmoTrade').Trade(newSaveTrade) # TODO: Needed? (Tomas)
    
    def CustomCalcLabel(self, *args):
        return QuotationLabel(self.Trade())

    '''*******************************************************
    * Deal Package Interface Methods
    *******************************************************'''
    def OnInit(self):
        super(PMOptionDefinition, self).OnInit()
        self._storedPricingParameters = {'quoteTradeCalcVal_undVal':None,
                                         'quoteTradeCalcVal_interestRateForeign':None,
                                         'quoteTradeCalcVal_interestRateDomestic':None,
                                         'fxSpotRateBidAsk':None,
                                         'fxSpotRate':None}
                                         #'atmVolatility':None}

        self._pricingOptions = acm.FPmOptionsPricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreatePricingTrades(self.Trade())
        
    def AssemblePackage(self):
        pmoTradeDeco = self.DealPackage().CreateTrade('Precious Metal Option', 'pmoTrade')
        SetPMTradeAndInstrumentAttributes(pmoTradeDeco)        
        self.PricingOptions().CreatePricingTrades(self.Trade())
        
    def OnNew(self):
        super(PMOptionDefinition, self).OnNew()
        self.amountForeign = 1000
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_PmOptionDealPackage')
        
    @classmethod
    def SetUp(cls, definitionSetUp):
        from DealPackageSetUp import  AddInfoSetUp
        definitionSetUp.AddSetupItems(
                            AddInfoSetUp( recordType='DealPackage',
                                          fieldName='MemoString',
                                          dataType='String',
                                          description='Options description',
                                          dataTypeGroup='Standard',
                                          subTypes=[],
                                          defaultValue='',
                                          mandatory=False))
