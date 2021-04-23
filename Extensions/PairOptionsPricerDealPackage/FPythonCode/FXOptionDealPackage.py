from __future__ import print_function
import acm
from SinglePairOptionDealPackage import SinglePairOptionDealPackage
from DealPackageDevKit import Settings, List, Action
from DealPackageUtil import DealPackageException
from PairOptionsUtil import SetFXTradeAndInstrumentAttributes, lot 
from FXCalculations import LeftSideFXCalculations, RightSideFXCalculations

SHEET_DEFAULT_COLUMNS = []
@Settings(GraphApplicable=False,
          SheetApplicable=False,
          SheetDefaultColumns=SHEET_DEFAULT_COLUMNS)
class FXOptionDefinition(SinglePairOptionDealPackage):
    
    # -------------------------------------------------------------------------------
    # Composite attributes
    # -------------------------------------------------------------------------------    
                                        
    quoteTradeCalcVal =         LeftSideFXCalculations( sideName='Foreign',
                                        tradeMethodName = 'QuoteTrade',
                                        altTradeMethodName = 'AltQuoteTrade')
                                        
    flippedQuoteTradeCalcVal =  RightSideFXCalculations( sideName='Domestic',
                                        tradeMethodName = 'FlippedQuoteTrade',
                                        altTradeMethodName = 'FlippedAltQuoteTrade')

    # -------------------------------------------------------------------------------
    # DEBUG
    # -------------------------------------------------------------------------------    
    openQuote =                 Action( label='@QuoteLabel',
                                        action='@OpenQuoteTrade')
    openAltQuote =              Action( label='@AltQuoteLabel',
                                        action='@OpenAltQuoteTrade')
    openFlippedQuote =          Action( label='@FlippedQuoteLabel',
                                        action='@OpenFlippedQuoteTrade')
    openFlippedAltQuote =       Action( label='@FlippedAltQuoteLabel',
                                        action='@OpenFlippedAltQuoteTrade')
                                        
    # -------------------------------------------------------------------------------
    # Grid View Model
    # -------------------------------------------------------------------------------    
    gridModelView =       List(     )
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import EmptyRow, Row, BarrierRow, VanillaRow, DigitalEuropeanRow, DigitalAmericanRow, NotDigitalAmericanRow, B2BRow
        from PairOptionsPricerGridViewModel import SingleBarrierRow, DoubleBarrierRow, VannaVolgaRow, NotVannaVolgaRow, AttrLabelPriceLeft, AttrLabelPriceRight, LabelLeft, LabelRight
        from PairOptionsPricerGridViewModel import EmptyCell, Attr, AttrLeft, CurrOrPairAttr, OptionTypeAttr, CurrOrPairAttrLeft, AttrMid, AttrActionBuySell, AttrActionLeft, AttrActionRight, AttrActionForeignCurr, NotDigitalRow
        from PairOptionsPricerGridViewModel import AttrCalc, AttrCalcMarketData, AttrCalcMarketDataLeft, AttrCalcMarketDataLot, AttrCalcLeft, AttrActionDomesticCurr, AttrLeftReadOnly, AttrCalcMarketDataLeftReadOnly
        from PairOptionsPricerGridViewModel import AttrLabelLeft, AttrLabelMarketDataLeft, AttrLabelMarketDataRight, AttrLabelCalcLeft, AttrLabelBoldLeft, AttrLabelRight, AttrLabelCalcRight, AttrLabelBoldRight, Label, LabelParam, LabelCalc, AttrLabelMidBold
        from PairOptionsPricerGridViewModel import CustomCalculationsRows
        return [
                Row([CurrOrPairAttr('foreignInstrument'), AttrActionLeft('foreignOptionType'), AttrMid('instrumentPair'), AttrActionRight('domesticOptionType'), CurrOrPairAttrLeft('domesticCurrency')]),
                Row([Attr('expiryDate'), AttrLabelBoldLeft('expiryDate'), AttrMid('fixingSource'), AttrLabelBoldRight('daysToExpiry'), AttrLeft('daysToExpiry')]),
                Row([Attr('deliveryDate'), AttrLabelBoldLeft('deliveryDate'), Label(''), AttrLabelBoldRight('daysToDelivery'), AttrLeft('daysToDelivery')]),
                Row([OptionTypeAttr('subtypeForeign'), AttrLabelBoldLeft('subtypeForeign'), AttrMid('baseType'), AttrLabelBoldRight('subtypeDomestic'), AttrLeft('subtypeDomestic')]),
                NotDigitalAmericanRow([Attr('strikeDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), Label('Strike'), AttrLabelRight('strikeForeignPerDomestic'), AttrLeft('strikeForeignPerDomestic')]),
                SingleBarrierRow([Attr('barrierDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), AttrLabelMidBold('barrierDomesticPerForeign'), AttrLabelRight('strikeForeignPerDomestic'), AttrLeft('barrierForeignPerDomestic')]),
                DoubleBarrierRow([Attr('doubleBarrierDomesticPerForeign'), AttrLabelLeft('strikeDomesticPerForeign'), AttrLabelMidBold('doubleBarrierDomesticPerForeign'), AttrLabelRight('strikeForeignPerDomestic'), AttrLeft('doubleBarrierForeignPerDomestic')]),
                NotDigitalAmericanRow([AttrCalc('intrinsicFwd'), LabelLeft('Fwd'), AttrLabelMidBold('intrinsicFwd'), LabelRight('Spot'), AttrCalcLeft('intrinsicSpot')]),
                Row([Attr('amountForeign'), AttrActionForeignCurr('setForeignAsSave'), AttrActionBuySell('buySell'), AttrActionDomesticCurr('setDomesticAsSave'), AttrLeft('amountDomestic')]),
                
                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                Row([AttrCalcMarketData('quoteTradeCalcVal_undVal'), AttrLabelMarketDataLeft('quoteTradeCalcVal_undVal'), LabelParam('Spot'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_undVal'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_undVal')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwdPoints'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwdPoints'), LabelParam('Fwd Points'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_fwdPoints'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_fwdPoints')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_fwd'), AttrLabelMarketDataLeft('quoteTradeCalcVal_fwd'), LabelParam('Fwd'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_fwd'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_fwd')]),
                Row([AttrCalcMarketData('quoteTradeCalcVal_interestRate'), AttrLabelMarketDataLeft('quoteTradeCalcVal_interestRate'), LabelParam('Interest Rate'), AttrLabelMarketDataRight('flippedQuoteTradeCalcVal_interestRate'), AttrCalcMarketDataLeft('flippedQuoteTradeCalcVal_interestRate')]),
                NotVannaVolgaRow([AttrCalcMarketDataLot('volatility'), AttrLabelMarketDataLeft('volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                VannaVolgaRow([AttrCalcMarketData('atmVolatility'), AttrLabelMarketDataLeft('quoteTradeCalcVal_volatility'), LabelParam('Volatility'), AttrLabelMarketDataRight('atmVolatility'), AttrCalcMarketDataLeftReadOnly('atmVolatility')]),
                VannaVolgaRow([AttrCalcMarketData('vannaVolgaDelta'), AttrLabelMarketDataLeft('vannaVolgaDelta'), LabelParam('Vanna Volga Adj'), AttrLabelMarketDataRight('vannaVolgaAdjustmentFactor'), AttrCalcMarketDataLeft('vannaVolgaAdjustmentFactor')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),

                Row([AttrCalc('quoteTradeCalcVal_theorPct'), AttrLabelPriceLeft('quoteTradeCalcVal_theorPct'), LabelCalc('Price Foreign'), AttrLabelPriceRight('flippedQuoteTradeCalcVal_theor'), AttrCalcLeft('flippedQuoteTradeCalcVal_theor')]),
                Row([AttrCalc('quoteTradeCalcVal_theor'), AttrLabelPriceLeft('quoteTradeCalcVal_theor'), LabelCalc('Price Domestic'), AttrLabelPriceRight('flippedQuoteTradeCalcVal_theorPct'), AttrCalcLeft('flippedQuoteTradeCalcVal_theorPct')]),
                NotDigitalRow([AttrCalc('quoteTradeCalcVal_breakEvenPrice'), AttrLabelCalcLeft('quoteTradeCalcVal_breakEvenPrice'), LabelCalc('Breakeven'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_breakEvenPrice'), AttrCalcLeft('flippedQuoteTradeCalcVal_breakEvenPrice')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBS'), LabelCalc('Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBS'), AttrCalcLeft('flippedQuoteTradeCalcVal_deltaBS')]),
                Row([AttrCalc('quoteTradeCalcVal_deltaBSAlt'), AttrLabelCalcLeft('quoteTradeCalcVal_deltaBSAlt'), LabelCalc('Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_deltaBSAlt'), AttrCalcLeft('flippedQuoteTradeCalcVal_deltaBSAlt')]),
                Row([AttrCalc('quoteTradeCalcVal_fwdDeltaBS'), AttrLabelCalcLeft('quoteTradeCalcVal_fwdDeltaBS'), LabelCalc('Fwd Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_fwdDeltaBS'), AttrCalcLeft('flippedQuoteTradeCalcVal_fwdDeltaBS')]),
                Row([AttrCalc('quoteTradeCalcVal_delta'), AttrLabelCalcLeft('quoteTradeCalcVal_delta'), LabelCalc('Vol Adj Delta'), AttrLabelCalcRight('flippedQuoteTradeCalcVal_delta'), AttrCalcLeft('flippedQuoteTradeCalcVal_delta')]),

                EmptyRow([EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell(), EmptyCell()]),
                
                CustomCalculationsRows('customCalculations'),

                Row([Label('Trade'), Label(''), Label(''), Label(''), Label('')]),
                Row([AttrCalc('saveTradeCalcVal_theorVal'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal'), Label(''), Label('')]),
                Row([AttrCalc('saveTradeCalcVal_theorValNoPremium'), AttrLeftReadOnly('premiumCurrency'), Label('TheorVal Ins'), Label(''), Label('')]),
                B2BRow([Attr('b2b_b2bPrice'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bPrice'), Label(''), Label('')]),
                B2BRow([Attr('b2b_b2bMargin'), AttrLeftReadOnly('saveTradeQuotation'), AttrLabelMidBold('b2b_b2bMargin'), Label(''), Label('')]),
                Row([AttrCalc('tradePrice'), AttrLeftReadOnly('saveTradeQuotation'), Label('Price'), Label(''), Label('')]),
                Row([AttrCalc('tradePremium'), AttrLeftReadOnly('premiumCurrency'), Label('Premium'), Label(''), Label('')]),
               ]
    
    '''*******************************************************
    * DEBUG
    *******************************************************'''
    def OpenQuoteTrade(self, *args):
        acm.StartApplication('Instrument Definition', self.PricingOptions().QuoteTrade().Trade())
    
    def OpenAltQuoteTrade(self, *args):
        acm.StartApplication('Instrument Definition', self.PricingOptions().AltQuoteTrade().Trade())
    
    def OpenFlippedQuoteTrade(self, *args):
        acm.StartApplication('Instrument Definition', self.PricingOptions().FlippedQuoteTrade().Trade())
    
    def OpenFlippedAltQuoteTrade(self, *args):
        acm.StartApplication('Instrument Definition', self.PricingOptions().FlippedAltQuoteTrade().Trade())

    #*********** END OF DEBUG ***********
    #************************************                                    

    def QuoteLabel(self, *args):
        label = 'Quote'
        if self.PricingOptions().CurrentSaveIsQuoteTrade():
            label = label + ' (S)'
        return label        
                                   
    def AltQuoteLabel(self, *args):
        label = 'AltQuote'
        if self.PricingOptions().CurrentSaveIsAltQuoteTrade():
            label = label + ' (S)'
        return label    
                                    
    def FlippedQuoteLabel(self, *args):
        label = 'Flipped'
        if self.PricingOptions().CurrentSaveIsFlippedQuoteTrade():
            label = label + ' (S)'
        return label    
                                       
    def FlippedAltQuoteLabel(self, *args):
        label = 'FlippedAlt'
        if self.PricingOptions().CurrentSaveIsFlippedAltQuoteTrade():
            label = label + ' (S)'
        return label   
    
    '''*******************************************************
    * Object Access Methods
    *******************************************************'''    
    def Trade(self):
        return self.TradeAt('fxoTrade')

    def Instrument(self):
        return self.InstrumentAt('fxoTrade')
        
    def DeltaHedge(self):
        return self.DeltaHedgeParamsAt('fxoTrade')
        
    def B2B(self): 
        return self.B2BTradeParamsAt('fxoTrade')
        
    def QuoteTrade(self):
        return self.PricingOptions().QuoteTrade()  
        
    def AltQuoteTrade(self):
        return self.PricingOptions().AltQuoteTrade()
        
    def FlippedQuoteTrade(self):
        return self.PricingOptions().FlippedQuoteTrade()    
    
    def FlippedAltQuoteTrade(self):
        return self.PricingOptions().FlippedAltQuoteTrade()    

    def QuoteInstrument(self):
        return self.QuoteTrade().Instrument()    

    def VolatilityObjectsAsLot(self):
        return lot([getattr(self, tradeMethodName)() for tradeMethodName in ['QuoteTrade', 'AltQuoteTrade', 'FlippedQuoteTrade', 'FlippedAltQuoteTrade']])

    '''*******************************************************
    * Overridden base class methods
    *******************************************************'''
    def UpdateConstellationsWithNewSaveTrade(self, newSaveTrade):
        enabled = self.B2BTradeParamsAt('fxoTrade').SalesCoverEnabled()
        if enabled:
            self.SetAttribute('b2b_b2bEnabled', False)
        self.B2BTradeParamsAt('fxoTrade').Trade(newSaveTrade.Trade()) 
        if enabled:
            self.SetAttribute('b2b_b2bEnabled', True)
            
    def FlippedSideChanged(self, attrName, wasFlipped, isFlipped, userInputTraitName):
        if isFlipped and self.IsDigital():
            print ('flipped side changed on digital')
            self.SetForeignAsSaveSide()

    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        super(FXOptionDefinition, self).OnInit()
        self._pricingOptions = acm.FFxOptionsPricer()
        if self.DealPackage().Trades():
            self.PricingOptions().CreatePricingTrades(self.Trade())
        
    def AssemblePackage(self):
        fxoTradeDeco = self.DealPackage().CreateTrade('FX Option', 'fxoTrade')
        fxoTradeDeco.DealPackageTradeLinks().First().IsLead(True)
        SetFXTradeAndInstrumentAttributes(fxoTradeDeco)        
        self.PricingOptions().CreatePricingTrades(self.Trade())

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_FxOptionDealPackage')
        
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

    '''*******************************************************
    * Actions
    *******************************************************'''
    def FlipSaveTradeCalcSimulations(self, attrName, isFlipped, *args):

        for attribute in ['fwdPoints', 'fwd']:
            simulationAttribute = 'saveTradeCalcVal_%s' % attribute
            if self.IsCalculationSimulated(simulationAttribute):
                if isFlipped:
                    newValueAttribute = 'flippedQuoteTradeCalcVal_%s' % attribute
                else:
                    newValueAttribute = 'quoteTradeCalcVal_%s' % attribute
                self.SetAttribute(simulationAttribute, self.GetAttribute(newValueAttribute).Value().Number())
                

