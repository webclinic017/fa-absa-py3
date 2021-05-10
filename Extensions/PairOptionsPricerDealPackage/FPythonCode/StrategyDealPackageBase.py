import acm
from PairOptionsDealPackageBase import PairOptionsDealPackageBase
from PairOptionsUtil import QuotationLabel, CurrencyNameFromCurrency, GetSingleValue, RoundPremium
from DealPackageDevKit import Object, CalcVal, Float, ParseFloat, Action
from DealPackageUtil import DealPackageException
from PairOptionsB2B import B2BCompositeAttribute

class ValueNotSet():
    pass

class StrategyDealPackageBase(PairOptionsDealPackageBase):
    
    amountCallForeign =         Object( label='@ForeignAmountLabel',
                                        objMapping='PricingOptions.AmountCallForeign',
                                        transform='@AmountTransform',
                                        onChanged='@UpdateDealPackageTrade',
                                        formatter='@ForeignAmountFormatterCB',
                                        enabled='@ForeignAmountEnabled',
                                        visible='@CallPutAmountsVisible',
                                        recreateCalcSpaceOnChange=True)

    amountCallDomestic =        Object( label='@DomesticAmountLabel',
                                        objMapping='PricingOptions.AmountCallDomestic',
                                        transform='@AmountTransform',
                                        onChanged='@UpdateDealPackageTrade',
                                        formatter='@DomesticAmountFormatterCB',
                                        enabled='@DomesticAmountEnabled',
                                        visible='@CallPutAmountsVisible',
                                        recreateCalcSpaceOnChange=True)
                                        
    amountPutForeign =          Object( label='@ForeignAmountLabel',
                                        objMapping='PricingOptions.AmountPutForeign',
                                        transform='@AmountTransform',
                                        onChanged='@UpdateDealPackageTrade',
                                        formatter='@ForeignAmountFormatterCB',
                                        enabled='@ForeignAmountEnabled',
                                        visible='@CallPutAmountsVisible',
                                        recreateCalcSpaceOnChange=True)   
                                        
    amountPutDomestic =         Object( label='@DomesticAmountLabel',
                                        objMapping='PricingOptions.AmountPutDomestic',
                                        transform='@AmountTransform',
                                        onChanged='@UpdateDealPackageTrade',
                                        formatter='@DomesticAmountFormatterCB',
                                        enabled='@DomesticAmountEnabled',
                                        visible='@CallPutAmountsVisible',
                                        recreateCalcSpaceOnChange=True)
                                        
    theorValCallSaveTrade =    CalcVal(calcMapping='CallTrade:FDealSheet:Portfolio Theoretical Value FXOStrat',
                                        label='@TheorValSaveTradeLabel',
                                        formatter='@SingleValueFormatterCB',
                                        solverTopValue=True)

    theorValNoPremCallSaveTrade=CalcVal(calcMapping='CallTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments FXOStrat',
                                        label='@TheorValNoPremiumSaveTradeLabel',
                                        formatter='@SingleValueFormatterCB',
                                        solverTopValue=True)
                                        
    theorValPutSaveTrade =     CalcVal(calcMapping='PutTrade:FDealSheet:Portfolio Theoretical Value FXOStrat',
                                        label='@TheorValSaveTradeLabel',
                                        formatter='@SingleValueFormatterCB',
                                        solverTopValue=True)

    theorValNoPremPutSaveTrade =CalcVal(calcMapping='PutTrade:FDealSheet:Portfolio Theoretical Value No Trade Payments FXOStrat',
                                        label='@TheorValNoPremiumSaveTradeLabel',
                                        formatter='@SingleValueFormatterCB',
                                        solverTopValue=True)
                                        
    tradePrice =                Float(  label='@TradePriceLabel',
                                        objMapping='StrategyPrice')
                                        
    tradePremium =              Float(  label='@TradePremiumLabel',
                                        objMapping='StrategyPremium')
    
    callTradePrice =            Object( label='@TradePriceLabel',
                                        objMapping='CallTrade.Price')
                                        
    callTradePremium =          Object( label='@TradePremiumLabel',
                                        objMapping='CallTrade.Premium')

    putTradePrice =             Object( label='@TradePriceLabel',
                                        objMapping='PutTrade.Price')
                                        
    putTradePremium =           Object( label='@TradePremiumLabel',
                                        objMapping='PutTrade.Premium')
                                        
    amountCallHeader =          Action( label='@AmountCallHeader',
                                        action='@UpdateBuySell')
    
    amountPutHeader =           Action( label='@AmountPutHeader',
                                        action='@UpdateBuySell')
    
    
                                        
    # -------------------------------------------------------------------------------
    # Composite attributes
    # ------------------------------------------------------------------------------- 
    b2b =                       B2BCompositeAttribute(b2bName='B2B')
    b2bCall =                   B2BCompositeAttribute(b2bName='B2BCall')
    b2bPut =                    B2BCompositeAttribute(b2bName='B2BPut')
    
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************'''                            
    def Trade(self):
        return self.TradeAt('callTrade')

    def CallTrade(self):
        return self.TradeAt('callTrade')
        
    def PutTrade(self):
        return self.TradeAt('putTrade')

    def Instrument(self):
        return self.InstrumentAt('callTrade')
        
    def B2B(self):
        return [self.B2BTradeParamsAt('callTrade'), self.B2BTradeParamsAt('putTrade')]

    def B2BCall(self):
        return self.B2BTradeParamsAt('callTrade')

    def B2BPut(self):
        return self.B2BTradeParamsAt('putTrade')
        
    def QuoteCombinationTrade(self):
        return self.PricingOptions().QuoteCombinationTrade()

    def CallStrike(self):
        return self.strikeDomesticPerForeign
    
    def PutStrike(self):
        return self.strikeDomesticPerForeign
        
    '''*******************************************************
    * Label methods
    *******************************************************'''  
    def TradePriceLabel(self, *args):
        return 'Price ' + QuotationLabel(self.LeadTrade())
        
    def TradePremiumLabel(self, *args):
        return 'Premium ' + CurrencyNameFromCurrency(self.premiumCurrency)
        
    def CallVolatilityLabel(self, *args):
        return 'Call'
        
    def PutVolatilityLabel(self, *args):
        return 'Put'
        
    def AmountCallHeader(self, *args):
        return 'Buy Call' if self.AmountCallForeignSign() > 0 else 'Sell Call'
     
    def AmountPutHeader(self, *args):
        return 'Buy Put' if self.AmountPutForeignSign() > 0 else 'Sell Put'
        
    '''*******************************************************
    * OnChanged methods
    *******************************************************'''  
    def SimulateVolatility(self, attributeName, old, new, userInputAttributeName):
        if new == 'ValueWillNotBeSet':
            self.SimulateCalculation(attributeName, None)
        else:
            self.volatility = self.GetSimulatedCalculationValue(attributeName)

    '''*******************************************************
    * Action methods
    *******************************************************'''   
    def UpdateBuySell(self, *args):
        if self.PricingOptions().CurrentSaveIsFlipped():
            self.amountCallDomestic = -self.amountCallDomestic
        else:
            self.amountCallForeign = -self.amountCallForeign

    '''*******************************************************
    * Visible methods
    *******************************************************'''     
    def CallPutAmountsVisible(self, *args):
        visibile = False
        if self.saveIsFlippedSide:
            visible = abs(self.amountCallDomestic) != abs(self.amountPutDomestic) or self.IsShowModeDetail()
        else:
            visible = abs(self.amountCallForeign) != abs(self.amountPutForeign) or self.IsShowModeDetail()
        return visible
    
    '''*******************************************************
    * Choices methods
    *******************************************************'''   
    def ExerciseTypeChoiceList(self, *args):
        return ['European']
        
    '''*******************************************************
    * Object mapping methods
    *******************************************************'''
    def StrategyPrice(self, price = ValueNotSet()):
        if isinstance(price, ValueNotSet):
            if self.PricingOptions().CurrentSaveIsFlipped():
                return (self.amountCallDomestic * self.callTradePrice + self.amountPutDomestic * self.putTradePrice) / self.amountDomestic if self.amountDomestic else 0.0
            else:
                return (self.amountCallForeign * self.callTradePrice + self.amountPutForeign * self.putTradePrice) / self.amountForeign if self.amountForeign else 0.0
        else:
            thVal = GetSingleValue(self.saveTradeCalcVal_theorValNoPremium.Value(), "Buy")
            if not (thVal and thVal.Number()):
                raise DealPackageException('No theoretical value for the strategy, you have to set the price on the components individually')
            
            thValCall = GetSingleValue(self.theorValNoPremCallSaveTrade.Value(), "Buy")
            thValPut = GetSingleValue(self.theorValNoPremPutSaveTrade.Value(), "Buy")
            
            callStrike = self.CallStrike()
            putStrike = self.PutStrike()
            
            thValCall = thValCall.Number()
            thValPut = thValPut.Number()
            thVal = thValCall + thValPut
            
            if self.PricingOptions().CurrentSaveIsFlipped():
                self.callTradePrice = price * thValCall / thVal * self.amountDomestic / self.amountCallDomestic
                self.putTradePrice = price * thValPut / thVal * self.amountDomestic / self.amountPutDomestic
            else:
                self.callTradePrice = price * thValCall / thVal * self.amountForeign / self.amountCallForeign
                self.putTradePrice = price * thValPut / thVal * self.amountForeign / self.amountPutForeign
                
        
    def StrategyPremium(self, premium = ValueNotSet()):
        if isinstance(premium, ValueNotSet):
            return self.callTradePremium + self.putTradePremium
        else:
            thVal = GetSingleValue(self.saveTradeCalcVal_theorValNoPremium.Value(), "Buy")
            if not (thVal and thVal.Number()):
                raise DealPackageException('No theoretical value for the strategy, you have to set the premium on the components individually')
            thValCall = GetSingleValue(self.theorValNoPremCallSaveTrade.Value(), "Buy")
            callPremium = RoundPremium(self.premiumCurrency, premium * thValCall.Number() / thVal.Number())
            self.callTradePremium = callPremium
            self.putTradePremium = RoundPremium(self.premiumCurrency, premium) - callPremium

    def UnsimulateOneVolatility(self, attrName, oldVal, newVal, *args):
        if self.IsCalculationSimulated('oneVolatility'):
            self.UnsimulateAttributeValue('oneVolatility')
            self.SetAttribute(attrName, newVal * 100)
    
    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def PriceGreekExcludeVolatilityMovement(self, *attr):
        return self.quoteTradeCalcVal.PriceGreekExcludeVolatilityMovement(*attr)
    
    def GetIntrinsicAttribute(self, name, isFwd):
        attr = 'intrinsic'
        attr += '2' if name.startswith('strike2') else ''
        attr +=  'Fwd' if isFwd else 'Spot'
        return attr
        
    def AmountCallForeignSign(self):
        return 1 if self.amountCallForeign > 0 else -1
        
    def AmountPutForeignSign(self):
        return 1 if self.amountPutForeign > 0 else -1
    
    def AmountCallDomesticSign(self):
        return 1 if (self.amountCallDomestic > 0) else -1
        
    def AmountPutDomesticSign(self):
        return 1 if (self.amountPutDomestic > 0) else -1
            
    '''*******************************************************
    * Object mapping methods
    *******************************************************'''    
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
