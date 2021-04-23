import acm
from DealPackageDevKit import CalcVal, CompositeAttributeDefinition
from PairOptionsUtil import QuotationLabel, UsePerUnitQuotationImpl, PriceGreekExcludeVolatilityMovement, DomesticColumnConfig, InterestRateLabel, GetSingleValue
from PairOptionsFormatters import TheorPriceFormatterCBImpl

class FXCalculations(CompositeAttributeDefinition):
    def OnInit(self, sideName, tradeMethodName, altTradeMethodName, strategyTradeMethodName = '' , altStrategyTradeMethodName = ''):
        self._sideName = sideName
        self._tradeMethodName = tradeMethodName
        self._altTradeMethodName = altTradeMethodName
        self._strategyTradeMethodName = strategyTradeMethodName
        self._altStrategyTradeMethodName = altStrategyTradeMethodName
        
    def SideName(self):
        return self._sideName

    def TradeName(self):
        return self._tradeMethodName
    
    def StrategyTradeName(self):
        return self._strategyTradeMethodName
       
    def AltTradeName(self):
        return self._altTradeMethodName
    
    def AltStrategyTradeName(self):
        return self._altStrategyTradeMethodName
         
    def Trade(self):
        meth = self.GetMethod(self.TradeName())
        return meth()
    
    def AltTrade(self):
        meth = self.GetMethod(self.AltTradeName())
        return meth()
    
    def StrategyOrTradeName(self):
        return self.StrategyTradeName() or self.TradeName()
        
    def AltStrategyOrTradeName(self):
        return self.AltStrategyTradeName() or self.AltTradeName()
        
    def IsPremiumAdjusted(self):
        pricingOptions = self.GetMethod("PricingOptions")()
        return pricingOptions.CurrentSaveIsFlippedQuoteTrade() or pricingOptions.CurrentSaveIsAltQuoteTrade()
    
    def ForeignStrategyOrTradeGreek(self):
        if self.IsPremiumAdjusted():
            return self.GetMethod(self.AltStrategyOrTradeName())()
        else:
            return self.GetMethod(self.StrategyOrTradeName())()
        
    def DomesticStrategyOrTradeGreek(self):
        if self.IsPremiumAdjusted():
            return self.GetMethod(self.StrategyOrTradeName())()
        else:
            return self.GetMethod(self.AltStrategyOrTradeName())()
        
        
    def CommonAttributes(self):
        return {
                'undVal':      CalcVal( label='@FXRateLabel',
                                         calcMapping=self.TradeName() + ':FDealSheet:Portfolio Underlying Price FXOStrat',
                                         formatter='@FXRateFormatterCB',
                                         transform='@TransformPrice',
                                         onChanged='@ValueSimulated',
                                         calcConfiguration=self.UniqueCallback('@UsePerUnitQuotation'),
                                         _isUserSimulated='@IsCalculationUserSimulated',
                                         _setOppositeSideAsSimulated = True,
                                         solverParameter='@UndValParam'),
                                         
                'fwdPoints':   CalcVal( label='@FXRateLabel',
                                         formatter='@FXPointsFormatterCB',
                                         transform='@TransformBidAsk',
                                         onChanged='@ValueSimulated',
                                         _isUserSimulated='@IsCalculationUserSimulated',
                                         _setOppositeSideAsSimulated = True,
                                         calcMapping=self.TradeName() + ':FDealSheet:Forward Points FXOStrat'),

                'fwd':         CalcVal( label='@FXRateLabel',
                                         formatter='@FXRateFormatterCB',
                                         transform='@TransformPrice',
                                         onChanged='@ValueSimulated',
                                         calcConfiguration=self.UniqueCallback('@UsePerUnitQuotation'),
                                         _isUserSimulated='@IsCalculationUserSimulated',
                                         _setOppositeSideAsSimulated = True,
                                         calcMapping=self.TradeName() + ':FDealSheet:Portfolio Underlying Forward Price FXOStrat'),
                                         
               }

    def TradeQuotationLabel(self):
        return QuotationLabel(self.Trade())
        
    def AltTradeQuotationLabel(self):
        return QuotationLabel(self.AltTrade())
        
    def DeltaBSLabel(self, *args):
        return self.TradeQuotationLabel()
        
    def DeltaBSAltLabel(self, *args):
        return self.AltTradeQuotationLabel()
        
    def ForeignPriceTheorValueLabel(self, *args):
        return self.TradeQuotationLabel()
        
    def DomesticPriceTheorValueLabel(self, *args):
        return self.AltTradeQuotationLabel()
        
    def QuoteInstrument(self):
        return self.QuoteTrade().Instrument()
            
    def IRLabel(self, *args):
        return InterestRateLabel(self.Trade())
        
    def BEPLabel(self, *args):
        return self.TradeQuotationLabel()

    def UsePerUnitQuotation(self, attrName):
        return UsePerUnitQuotationImpl(attrName)

    def PriceGreekExcludeVolatilityMovement(self, attrName):
        return PriceGreekExcludeVolatilityMovement(attrName)

    def DomesticColumnConfig(self, attrName):
        return DomesticColumnConfig(attrName)

    def TheorPriceFormatterCB(self, attrName):
        try:
            value = getattr(self.Owner(), attrName).Value()
            unit = GetSingleValue(value).Unit()
        except:
            unit = None
        return TheorPriceFormatterCBImpl(attrName, unit)
        
    def ForeignGreekLabel(self, *args):
        if self.IsPremiumAdjusted():
            return self.AltTradeQuotationLabel()
        else:
            return self.TradeQuotationLabel()
            
    def DomesticGreekLabel(self, *args):
        if self.IsPremiumAdjusted():
            return self.TradeQuotationLabel()
        else:
            return self.AltTradeQuotationLabel()
        
class LeftSideFXCalculations(FXCalculations):
    def LeftSideAttributes(self):
        return {                                         
                'volatility' :          CalcVal(label = 'Vol %',
                                                calcMapping=self.TradeName() + ':FDealSheet:Portfolio Volatility FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                onChanged='@ValueSimulated',
                                                transform='@TransformVolatility',
                                                solverParameter='@VolatilityParam'),  
                                         
                'volatilityAlt' :       CalcVal(calcMapping=self.AltTradeName() + ':FDealSheet:Portfolio Volatility FXOStrat'),

                'theor' :               CalcVal(label=self.UniqueCallback('@ForeignPriceTheorValueLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Price Theor FXOStrat',
                                                formatter=self.UniqueCallback('@TheorPriceFormatterCB'),
                                                solverTopValue=True),
                
                'theorPct' :            CalcVal(label=self.UniqueCallback('@DomesticPriceTheorValueLabel'),
                                                calcMapping=self.AltStrategyOrTradeName() + ':FDealSheet:Price Theor FXOStrat',
                                                formatter=self.UniqueCallback('@TheorPriceFormatterCB'),
                                                solverTopValue=True),
                                        
                'breakEvenPrice':       CalcVal(label=self.UniqueCallback('@BEPLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Break Even Price FXOStrat',
                                                formatter='@FXRateFormatterCB',
                                                visible='@IsNotDigital',
                                                calcConfiguration=self.UniqueCallback('@UsePerUnitQuotation'),
                                                solverTopValue=True),                        

                'deltaBS' :             CalcVal(label=self.UniqueCallback('@DeltaBSLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformDelta',
                                                solverTopValue=True),
                                         
                'deltaBSAlt' :          CalcVal(label=self.UniqueCallback('@DeltaBSAltLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement'),
                                                calcMapping=self.AltStrategyOrTradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformPremiumAdjustedDelta',
                                                solverTopValue=True),

                'fwdDeltaBS' :          CalcVal(label=self.UniqueCallback('@ForeignGreekLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement'),
                                                calcMapping=self.UniqueCallback('ForeignStrategyOrTradeGreek') + ':FDealSheet:Instrument Forward Delta FXOStrat',
                                                transform='@TransformDelta',
                                                solverTopValue=True),
                                                
                'delta' :               CalcVal(label=self.UniqueCallback('@ForeignGreekLabel'),
                                                calcMapping=self.UniqueCallback('ForeignStrategyOrTradeGreek') + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformDelta',
                                                solverTopValue=True),
                                        
                'interestRate' :        CalcVal(label=self.UniqueCallback('@IRLabel'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Foreign Repo Rate FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                onChanged='@ValueSimulated')
                                                                              
               }
    
    def Attributes(self):
        return dict(self.LeftSideAttributes(), **self.CommonAttributes())  
      
    def GetLayout(self):
        return self.UniqueLayout('''vbox[Calculations;
                                      undVal;
                                      fwd;   
                                      volatility;
                                      interestRate;
                                      theor;
                                      theorPct;
                                      breakEvenPrice;
                                      deltaBS;
                                      deltaBSAlt;
                                      ];
                                 ''')
    
class RightSideFXCalculations(FXCalculations):
    def RightSideAttributes(self):
        return {                                         
                'volatility' :          CalcVal(calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Portfolio Volatility FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                ),
                                        
                'volatilityAlt' :       CalcVal(calcMapping=self.AltStrategyOrTradeName() + ':FDealSheet:Portfolio Volatility FXOStrat'),

                'breakEvenPrice':       CalcVal(label=self.UniqueCallback('@BEPLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Break Even Price FXOStrat',
                                                calcConfiguration=self.UniqueCallback('@UsePerUnitQuotation'),
                                                formatter='@FXRateFormatterCB',
                                                visible='@IsNotDigital',
                                                solverTopValue=True),

                'deltaBS' :             CalcVal(label=self.UniqueCallback('@DeltaBSLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement') + '|' + self.UniqueCallback('DomesticColumnConfig'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformFlippedDelta',
                                                visible='@IsNotDigital',
                                                solverTopValue=True),
                                         
                'deltaBSAlt' :          CalcVal(label=self.UniqueCallback('@DeltaBSAltLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement') + '|' + self.UniqueCallback('DomesticColumnConfig'),
                                                calcMapping=self.AltStrategyOrTradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformPremiumAdjustedDelta',
                                                visible='@IsNotDigital',
                                                solverTopValue=True),

                'fwdDeltaBS' :          CalcVal(label=self.UniqueCallback('@DomesticGreekLabel'),
                                                calcConfiguration=self.UniqueCallback('@PriceGreekExcludeVolatilityMovement') + '|' + self.UniqueCallback('DomesticColumnConfig'),
                                                calcMapping=self.UniqueCallback('DomesticStrategyOrTradeGreek') + ':FDealSheet:Instrument Forward Delta FXOStrat',
                                                transform='@TransformFlippedDelta',
                                                visible='@IsNotDigital',
                                                solverTopValue=True),

                'theorPct' :            CalcVal(label=self.UniqueCallback('@DomesticPriceTheorValueLabel'),
                                                calcMapping=self.AltStrategyOrTradeName() + ':FDealSheet:Price Theor FXOStrat',
                                                formatter=self.UniqueCallback('@TheorPriceFormatterCB'),
                                                solverTopValue=True,
                                                visible='@IsNotDigital'),
                
                'theor' :               CalcVal(label=self.UniqueCallback('@ForeignPriceTheorValueLabel'),
                                                calcMapping=self.StrategyOrTradeName() + ':FDealSheet:Price Theor FXOStrat',
                                                formatter=self.UniqueCallback('@TheorPriceFormatterCB'),
                                                solverTopValue=True,
                                                visible='@IsNotDigital'),
                                                
                'delta' :               CalcVal(label=self.UniqueCallback('@DomesticGreekLabel'),
                                                calcConfiguration=self.UniqueCallback('@DomesticColumnConfig'),
                                                calcMapping=self.UniqueCallback('DomesticStrategyOrTradeGreek') + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformFlippedDelta',
                                                solverTopValue=True,
                                                visible='@IsNotDigital'),

                'interestRate' :        CalcVal(label=self.UniqueCallback('@IRLabel'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Foreign Repo Rate FXOStrat',
                                                _isUserSimulated='@IsCalculationUserSimulated',
                                                onChanged='@ValueSimulated')
                                                                                  
               }
        
    def Attributes(self):
        return dict(self.RightSideAttributes(), **self.CommonAttributes())
        
    def GetLayout(self):
        return self.UniqueLayout('''vbox[Calculations;
                                      undVal;
                                      fwd;
                                      atmVolatility; 
                                      interestRate;
                                      theorPct;
                                      theor;
                                      breakEvenPrice;
                                      deltaBS;
                                      deltaBSAlt;
                                      ];
                                 ''')



class SaveTradeCalculations(CompositeAttributeDefinition):
    def OnInit(self, tradeMethodName = 'Trade', _portfolioMethodName = 'AsPortfolio', enabled = True):
        self._tradeMethodName = tradeMethodName
        self._portfolioMethodName = _portfolioMethodName
        self._enabled = enabled
    
    def TradeName(self):
        return self._tradeMethodName
        
    def Enabled(self):
        return self._enabled

    def PortfolioName(self):
        return self._portfolioMethodName or self._tradeMethodName

    def Trade(self):
        return self.GetMethod(self.TradeName())()
        
    def CalcConfig(self, attrName):
        return PriceGreekExcludeVolatilityMovement(attrName).Merge(DomesticColumnConfig(attrName))

    def DomesticColumnConfig(self, attrName):
        return DomesticColumnConfig(attrName)

    def TheorPriceFormatterCB(self, attrName):
        try:
            value = getattr(self.Owner(), attrName).Value()
            unit = GetSingleValue(value).Unit()
        except:
            unit = None
        return TheorPriceFormatterCBImpl(attrName, unit)
    
    def QuotationLabel(self, attrName):
        return QuotationLabel(self.Trade())

    def UsePerUnitQuotation(self, attrName):
        return UsePerUnitQuotationImpl(attrName)
    
    def Attributes(self):
        return {'theor' :               CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Price Theor FXOStrat',
                                                formatter=self.UniqueCallback('@TheorPriceFormatterCB'),
                                                solverTopValue=self.Enabled(),
                                                enabled=self.Enabled()),
                                                
                'deltaBS' :             CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcConfiguration=self.UniqueCallback('@CalcConfig'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformDelta',
                                                enabled=self.Enabled(),
                                                solverTopValue=self.Enabled()),

                'fwdDeltaBS' :          CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcConfiguration=self.UniqueCallback('@CalcConfig'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Instrument Forward Delta FXOStrat',
                                                transform='@TransformDelta',
                                                enabled=self.Enabled(),
                                                solverTopValue=self.Enabled()),

                'delta' :               CalcVal(label=self.UniqueCallback('@QuotationLabel'),
                                                calcConfiguration=self.UniqueCallback('@DomesticColumnConfig'),
                                                calcMapping=self.TradeName() + ':FDealSheet:Instrument Delta FXOStrat',
                                                transform='@TransformDelta',
                                                enabled=self.Enabled(),
                                                solverTopValue=self.Enabled()),

                'theorVal' :            CalcVal(calcMapping=self.PortfolioName() + ':FPortfolioSheet:Portfolio Theoretical Value FXOStrat',
                                                label='@TheorValSaveTradeLabel',
                                                formatter='@SingleValueFormatterCB',
                                                enabled=self.Enabled(),
                                                solverTopValue=self.Enabled()),
                                            
                'theorValNoPremium':    CalcVal(calcMapping=self.PortfolioName() + ':FPortfolioSheet:Portfolio Theoretical Value No Trade Payments FXOStrat',
                                                label='@TheorValNoPremiumSaveTradeLabel',
                                                formatter='@SingleValueFormatterCB',
                                                enabled=self.Enabled(),
                                                solverTopValue=self.Enabled()),

                'undVal' :      CalcVal( label='@FXRateLabel',
                                         calcMapping=self.TradeName() + ':FDealSheet:Portfolio Underlying Price FXOStrat',
                                         formatter='@FXRateFlipFormatterCB',
                                         transform='@TransformPriceParse',
                                         onChanged='@ValueSimulated',
                                         calcConfiguration=self.UniqueCallback('@UsePerUnitQuotation')),
                                         
                'fwdPoints' :   CalcVal( label='@FXRateLabel',
                                         formatter='@FXPointsFormatterCB',
                                         onChanged='@ValueSimulated',
                                         calcMapping=self.TradeName() + ':FDealSheet:Forward Points FXOStrat'),

                'fwd' :         CalcVal( label='@FXRateLabel',
                                         formatter='@FXRateFlipFormatterCB',
                                         transform='@TransformPriceParse',
                                         onChanged='@ValueSimulated',
                                         calcConfiguration=self.UniqueCallback('@UsePerUnitQuotation'),
                                         calcMapping=self.TradeName() + ':FDealSheet:Portfolio Underlying Forward Price FXOStrat')

               }
