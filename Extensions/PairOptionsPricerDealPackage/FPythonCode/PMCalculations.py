import acm
from DealPackageDevKit import CalcVal, CompositeAttributeDefinition
from PairOptionsUtil import QuotationLabel, UsePerUnitQuotationImpl, PriceGreekExcludeVolatilityMovement, InterestRateLabel, GetSingleValue
from PairOptionsFormatters import TheorPriceFormatterCBImpl

class PMCalculations(CompositeAttributeDefinition):
    def OnInit(self, tradeMethodName, strategyCombinationName = None):
        self._tradeMethodName = tradeMethodName
        self._strategyCombinationName = strategyCombinationName

    def TradeName(self):
        return self._tradeMethodName
    
    def StrategyCombinationName(self):
        return self._strategyCombinationName
        
    def StrategyOrTradeName(self):
        return self.StrategyCombinationName() if self.StrategyCombinationName() else self.TradeName()
        
    def Trade(self):
        meth = self.GetMethod(self.TradeName())
        return meth()
 
    def Attributes(self):
        return {
                'undVal' :              CalcVal(label='@FXRateLabel',
                                                calcMapping=self.TradeName() + ':FDealSheet:Portfolio Underlying Price FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                formatter='@FXRateFormatterCB',
                                                solverParameter='@UndValParam',
                                                transform='@TransformPrice',
                                                onChanged='@ValueSimulated'),
           
                'fwdPoints' :           CalcVal(label='@FXRateLabel',
                                                formatter='@FXPointsFormatterCB',
                                                transform='@TransformBidAsk',
                                                calcMapping=self.TradeName() + ':FDealSheet:Forward Points FXOStrat',
                                                onChanged='@ValueSimulated'),

                'carryCost' :           CalcVal(label='@FXRateLabel',
                                                calcMapping=self.TradeName() + ':FDealSheet:Portfolio Carry Cost',
                                                formatter='PercentIncreasedPrecision',
                                                transform='@TransformBidAsk',
                                                onChanged='@ValueSimulated'),

                'fwd' :                 CalcVal(label='@FXRateLabel',
                                                formatter='@FXRateFormatterCB',
                                                transform='@TransformPrice',
                                                calcMapping=self.TradeName() + ':FDealSheet:Portfolio Underlying Forward Price FXOStrat',
                                                onChanged='@ValueSimulated'),
                                             
                'interestRateForeign' : CalcVal(label=self.UniqueCallback('@ForeignIRLabel'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Foreign Repo Rate FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                onChanged='@ValueSimulated'),
                         
                
                'interestRateDomestic' :CalcVal(label=self.UniqueCallback('@DomesticIRLabel'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Domestic Repo Rate FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                onChanged='@ValueSimulated'),
                      
                'theor' :               CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Price Theor FXOStrat',
                                                formatter=self.UniqueCallback('@TheorPriceFormatterCB'),
                                                solverTopValue=True),
                                                
                'breakEvenPrice':       CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Break Even Price FXOStrat',
                                                formatter='@FXRateFormatterCB',
                                                visible='@IsNotDigital',
                                                solverTopValue=True),                        
                
                'deltaBS' :             CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformDelta',
                                                solverTopValue=True),
                                                
                'fwdDeltaBS' :          CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Instrument Forward Delta FXOStrat',
                                                transform='@TransformDelta',
                                                solverTopValue=True),
                                                
                'delta' :               CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformDelta',
                                                solverTopValue=True)
               }

    def UsePerUnitQuotation(self, attrName):
        return UsePerUnitQuotationImpl(attrName)

    def ForeignIRLabel(self, *args):
        return InterestRateLabel(self.Trade())
    
    def DomesticIRLabel(self, *args):
        return 'Domestic' # TODO: Pick up the domestic/flipped currency
        
    def QuotationLabel(self, *args):
        return QuotationLabel(self.Trade())
                
    def TheorPriceFormatterCB(self, attrName):
        value = getattr(self.Owner(), attrName).Value()
        unit = GetSingleValue(value).Unit()
        return TheorPriceFormatterCBImpl(attrName, unit)
        
    def PriceGreekExcludeVolatilityMovement(self, attrName):
        return PriceGreekExcludeVolatilityMovement(attrName)
        
    def GetLayout(self):
        return self.UniqueLayout('''vbox[Calculations;
                                      undVal;
                                      fwdPoints;
                                      fwd; 
                                      volatility;
                                      atmVolatility;
                                      ];
                                 ''')
