import acm
from PairOptionsDealPackageBase import PairOptionsDealPackageBase
from DealPackageDevKit import Object, List, Str, CalcVal, Action, Float, DealPackageChoiceListSource, TradeStatusChoices
from DealPackageDevKit import CounterpartyChoices, AcquirerChoices, PortfolioChoices
from PairOptionsUtil import QuotationLabel, GetInitialBarrierLevel, GetInitialDoubleBarrierLevel, IsDoubleBarrier
from PairOptionsUtil import CurrencyNameFromCurrency, Flipped, CurrencyLabel, DeltaNoSurfaceDelta
from PairOptionsUtil import GetSingleValue, IsOfTypeFLot, UpdateDealPackageTradeLink
from PairOptionsFormatters import GetFXSpotForwardFormatter, StrikeFormatter
from PairOptionsDeltaHedge import DeltaHedgeCompositeAttribute
from PairOptionsB2B import B2BCompositeAttribute

class SinglePairOptionDealPackage(PairOptionsDealPackageBase):

    foreignOptionType =         Action( label='@ForeignCurrencyLabel',
                                        action='@ChangeCallPut',
                                        recreateCalcSpaceOnChange = True)
                                        
    optionType =                Object( label = 'Call/Put',
                                        objMapping='OptionType',
                                        choiceListSource=['Call', 'Put'])         

    domesticOptionType =        Action( label='@DomesticCurrencyLabel',
                                        action='@ChangeCallPut',
                                        recreateCalcSpaceOnChange = True)                        
   
    tradePrice =                Object( label='@TradePriceLabel',
                                        objMapping='CurrentSaveTrade.Price')
                                        
    tradePremium =              Float( label='@TradePremiumLabel',
                                        objMapping='TradePremium',
                                        onChanged='@TradePremiumChanged')


    # -------------------------------------------------------------------------------
    # Calculation attributes not fit for the Calculations composite class
    # -------------------------------------------------------------------------------  
    intrinsicFwd =              CalcVal(label='Intrinsic %',
                                        calcMapping='QuoteTrade:FDealSheet:Intrinsic Option Forward Value% FXOStrat',
                                        solverTopValue=True,
                                        tabStop = False)
                                        
    intrinsicSpot =             CalcVal(label='Intrinsic %',
                                        calcMapping='QuoteTrade:FDealSheet:Intrinsic Option Value % FXOStrat',
                                        solverTopValue=True)
    
    # -------------------------------------------------------------------------------
    # Delta hedge calculations (not shown in grid)
    # -------------------------------------------------------------------------------    
    positionSpotDelta =         CalcVal(calcMapping='CurrentSaveTrade:FDealSheet:Portfolio Delta',
                                        label='Position Delta Spot',
                                        calcConfiguration=DeltaNoSurfaceDelta)
                                        
    positionForwardDelta =      CalcVal(calcMapping='CurrentSaveTrade:FDealSheet:Portfolio Delta Forward Hedge',
                                        label='Position Delta Forward',
                                        calcConfiguration=DeltaNoSurfaceDelta) 


    # -------------------------------------------------------------------------------
    # Composite attributes
    # -------------------------------------------------------------------------------    
    deltaHedge =                DeltaHedgeCompositeAttribute(deltaHedgeName='DeltaHedge')

    b2b =                       B2BCompositeAttribute(b2bName='B2B')    

    # -------------------------------------------------------------------------------
    # Exotic type mappings
    # -------------------------------------------------------------------------------
    baseType =                    Object( label='Base Type',
                                          objMapping='PricingOptions.BaseType',
                                          choiceListSource=['Vanilla', 'Barrier', 'Digital European', 'Digital American'],
                                          onChanged='@InitBarriers|UpdateDealPackageTrade|OverrideValuationGroupOnChanged')   
    
    barrierTypeForeign =          Object( label='Type',
                                          objMapping='PricingOptions.BarrierTypeForeign',
                                          visible='@HasBaseTypeBarrier',
                                          choiceListSource='@BarrierTypeChoiceList',
                                          onChanged='@OnBarrierTypeChanged',
                                          recreateCalcSpaceOnChange = True)

    barrierTypeDomestic =         Object( label='Type',
                                          objMapping='PricingOptions.BarrierTypeDomestic',
                                          visible='@HasBaseTypeBarrier',
                                          choiceListSource='@BarrierTypeChoiceList',
                                          recreateCalcSpaceOnChange = True)
                                        
    digitalEuropeanTypeForeign =  Object( label='Type',
                                          objMapping='PricingOptions.DigitalEuropeanTypeForeign',
                                          visible='@HasBaseTypeDigitalEuropean',
                                          choiceListSource='@DigitalEuropeanTypeChoiceList',
                                          onChanged='@OnBarrierTypeChanged',
                                          recreateCalcSpaceOnChange = True)

    digitalEuropeanTypeDomestic = Object( label='Type',
                                          objMapping='PricingOptions.DigitalEuropeanTypeDomestic',
                                          visible='@HasBaseTypeDigitalEuropean',
                                          choiceListSource='@DigitalEuropeanTypeChoiceList',
                                          recreateCalcSpaceOnChange = True)
                                        
    digitalAmericanTypeForeign =  Object( label='Type',
                                          objMapping='PricingOptions.DigitalAmericanTypeForeign',
                                          visible='@HasBaseTypeDigitalAmerican',
                                          choiceListSource='@DigitalAmericanTypeChoiceList',
                                          onChanged='@OnBarrierTypeChanged',
                                          recreateCalcSpaceOnChange = True)

    digitalAmericanTypeDomestic = Object( label='Type',
                                          objMapping='PricingOptions.DigitalAmericanTypeDomestic',
                                          visible='@HasBaseTypeDigitalAmerican',
                                          choiceListSource='@DigitalAmericanTypeChoiceList',
                                          recreateCalcSpaceOnChange = True)

    subtypeForeign =              Object( label = '@SubtypeLabel',
                                          objMapping='SubtypeForeign',
                                          transform='@TransformToOptionType',
                                          domain = 'FObject',
                                          choiceListSource='@SubtypeChoiceList')
                                            
    subtypeDomestic =             Object( label = '@SubtypeLabel',
                                          objMapping='SubtypeDomestic',
                                          choiceListSource='@SubtypeChoiceList')

    payoutCurrency =              Object( label='Payout Currency',
                                          objMapping='PricingOptions.PayoutCurrency',
                                          visible='@IsDigital',
                                          choiceListSource='@PremiumCurrencyChoices') # TODO: Recreate calcspace?
                                     
    payAtExpiry =                 Object( label='Rebate Type',
                                          objMapping='PricingOptions.PayAtExpiry',
                                          visible='@IsDigitalAmerican')


    # -------------------------------------------------------------------------------
    # Exotic barrier mappings
    # -------------------------------------------------------------------------------                                        
    barrierDomesticPerForeign = Object( label='@BarrierLabel',
                                        objMapping='PricingOptions.BarrierDomesticPerForeign',
                                        visible='@HasBaseTypeBarrierOrDigitalBarrierType',
                                        formatter='@FXRateFormatterCB',
                                        solverParameter='@StrikeParamDomPerFor',
                                        recreateCalcSpaceOnChange = True)

    barrierForeignPerDomestic = Object( label='@BarrierLabel',
                                        objMapping='PricingOptions.BarrierForeignPerDomestic',
                                        visible='@HasBaseTypeBarrierOrDigitalBarrierType',
                                        formatter='@FXRateFormatterCB',
                                        solverParameter='@StrikeParamForPerDom',
                                        recreateCalcSpaceOnChange = True)        

    doubleBarrierDomesticPerForeign = Object( label='@DoubleBarrierLabel',
                                        objMapping='PricingOptions.DoubleBarrierDomesticPerForeign',
                                        visible='@HasBaseTypeBarrierAndBarrierTypeDouble',
                                        formatter='@FXRateFormatterCB',
                                        solverParameter='@StrikeParamDomPerFor',
                                        recreateCalcSpaceOnChange = True)

    doubleBarrierForeignPerDomestic = Object( label='@DoubleBarrierLabel',
                                        objMapping='PricingOptions.DoubleBarrierForeignPerDomestic',
                                        visible='@HasBaseTypeBarrierAndBarrierTypeDouble',
                                        formatter='@FXRateFormatterCB',
                                        solverParameter='@StrikeParamForPerDom',
                                        recreateCalcSpaceOnChange = True)


    # -------------------------------------------------------------------------------
    # Barrier monitoring mappings
    # -------------------------------------------------------------------------------      
    barrierMonitoring =                 Object( label='Monitoring:',
                                                objMapping='PricingInstruments.Exotic.BarrierMonitoring',
                                                visible='@HasBaseTypeBarrierOrDigitalBarrierType',
                                                enabled=False)
    
    barrierCrossedStatus =              Object( label='Crossed:',
                                                objMapping='PricingInstruments.Exotic.BarrierCrossedStatus',
                                                visible='@HasBaseTypeBarrierOrDigitalBarrierType')
    
    barrierCrossDate =                  Object( label='Cross Date:',
                                                objMapping='PricingInstruments.Exotic.BarrierCrossDate',
                                                visible='@HasBaseTypeBarrierOrDigitalBarrierType',
                                                transform='@TransformBarrierCrossPeriodToDate',
                                                enabled='@IsCrossedStatusSelected')                                       

 
    # -------------------------------------------------------------------------------
    # Vanna Volga Add On
    # -------------------------------------------------------------------------------      
   
    vannaVolgaDelta =                   CalcVal(calcMapping='CurrentSaveTrade:FDealSheet:Vanna Volga Delta FXO',
                                                label='Vol Delta')
 
    vannaVolgaAdjustmentFactor =        CalcVal(calcMapping='CurrentSaveTrade:FDealSheet:Vanna Volga Adjustment Factor FXO',
                                                label='Factor %') 
                                                
    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************'''                                
    def LeadTrade(self):
        return self.Trade()
            
    '''*******************************************************
    * Transform methods
    *******************************************************'''  
    def TransformBarrierCrossPeriodToDate(self, name, newDate):
        periodAsDate = acm.Time().PeriodSymbolToDate(newDate)
        if periodAsDate:
            newDate = periodAsDate
        return newDate

    '''*******************************************************
    * Choices methods
    *******************************************************'''   
    def DigitalEuropeanTypeChoiceList(self, *args):
        return ['Vanilla', 'Down & In', 'Down & Out', 'Up & In', 'Up & Out', 'Double In', 'Double Out']
        
    def BarrierTypeChoiceList(self, *args):
        return ['Down & In', 'Down & Out', 'Up & In', 'Up & Out', 'Double In', 'Double Out']
        
    def DigitalAmericanTypeChoiceList(self, *args):
        return ['Double No Touch', 'Double One Touch', 'No Touch', 'One Touch']
        
    def SubtypeChoiceList(self, traitName, *args):
        subtypeTrait = self.SubtypeTrait(traitName.replace('subtype', ''))
        return self.GetAttributeMetaData(subtypeTrait, "choiceListSource")()
        
    '''*******************************************************
    * OnChange methods
    *******************************************************'''  
    def SetNewSaveTradeOnDealPackage(self):
        if UpdateDealPackageTradeLink(self.DealPackage(), self.CurrentSaveTrade().Trade(), 'fxoTrade'):
            self.UpdateConstellationsWithNewSaveTrade(self.CurrentSaveTrade().Trade())   

    def UpdateConstellationsWithNewSaveTrade(self, newSaveTrade):
        ''' Implemented in derived classes '''
        pass

    def InitBarriers(self, *args):
        if self.baseType != 'Vanilla':
            self.barrierMonitoring = 'Continuous'
            self.barrierCrossedStatus = 'None'
            self.barrierCrossDate = None
        
        if self.HasBaseTypeBarrier() or self.HasDigitalEuropeanBarrierType() or self.HasBaseTypeDigitalAmerican():
            fwdPrice = GetSingleValue(self.quoteTradeCalcVal_fwd.Value(), self.BuySellLabel()).Number()
            self.barrierDomesticPerForeign = GetInitialBarrierLevel(fwdPrice, self.barrierTypeForeign)
            if IsDoubleBarrier(self.barrierTypeForeign):
                self.doubleBarrierDomesticPerForeign = GetInitialDoubleBarrierLevel(fwdPrice)
            
    def OnBarrierTypeChanged(self, *args):
        self.InitBarriers()
        
    def OnHedgeTypeChanged(self, attributeName, old, new, userInputAttributeName):
        self.SetDeltaHedgePriceToSpotOrForward(new)
        self.SetDeltaHedgeDelta(new)
        self.SetDeltaHedgeValueDay(new)

    def TradePremiumChanged(self, attributeName, old, new, userInputAttributeName):
        if userInputAttributeName == 'payType' and new == 0.0:
            self.tradePremium = old
    
    def OverrideValuationGroupOnChanged(self, attributeName, oldBaseType, newBaseType, userInputAttributeName):
        self.OverrideValuationGroup(newBaseType)

        
    '''*******************************************************
    * Base Class Methods
    *******************************************************'''    
    def ChangeSignOnDeltaBasedOnCallPut(self, delta, isFlippedDelta):
        trade = self.FlippedQuoteTrade() if isFlippedDelta else self.QuoteTrade()
        if delta > 0 and not trade.Instrument().IsCall():
            delta *= -1
        return delta
        
    '''*******************************************************
    * Visible methods
    *******************************************************'''            
    def HasBaseTypeBarrier(self, *args):
        return self.baseType == 'Barrier'                            # TODO: compare against proper enum?
        
    def HasBaseTypeDigitalEuropean(self, *args):
        return self.baseType == 'Digital European'
        
    def HasBaseTypeDigitalAmerican(self, *args):
        return self.baseType == 'Digital American'
        
    def IsDigital(self, *args):
        return self.HasBaseTypeDigitalEuropean() or self.HasBaseTypeDigitalAmerican()
        
    def IsDigitalAmerican(self, *args):
        return self.HasBaseTypeDigitalAmerican()
       
    def HasBaseTypeBarrierAndBarrierTypeDouble(self, *args):
        if self.HasBaseTypeBarrier():
            return IsDoubleBarrier(self.barrierTypeForeign)
        elif self.HasBaseTypeDigitalEuropean():
            return IsDoubleBarrier(self.digitalEuropeanTypeForeign)
        elif self.HasBaseTypeDigitalAmerican():
            return IsDoubleBarrier(self.digitalAmericanTypeForeign)
 
    def HasDigitalEuropeanBarrierType(self):
        return self.PricingOptions().DigitalEuropeanTypeForeign() in ['Down & Out', 'Down & In', 'Up & Out', 'Up & In', 'Double In', 'Double Out']
 
    def HasBaseTypeBarrierOrDigitalBarrierType(self, *args):
        return self.HasBaseTypeBarrier() or self.HasDigitalEuropeanBarrierType() or self.HasBaseTypeDigitalAmerican()
        
    def IsCrossedStatusSelected(self, attributeName):
        return self.barrierCrossedStatus != 'None'
                
    '''*******************************************************
    * Label methods
    *******************************************************'''
    def BarrierLabel(self, *args):
        if self.HasBaseTypeBarrier():
            if self.PricingOptions().BarrierTypeForeign().startswith('Double'):
                return '1:st Barrier'
            else:
                return 'Barrier'
        elif self.HasBaseTypeDigitalEuropean():
            if self.PricingOptions().DigitalEuropeanTypeForeign().startswith('Double'):
                return '1:st Trigger'
            else:
                return 'Trigger'
        elif self.HasBaseTypeDigitalAmerican():
            if self.PricingOptions().DigitalAmericanTypeForeign().startswith('Double'):
                return '1:st Trigger'
            else:
                return 'Trigger'
    
    def DoubleBarrierLabel(self, *args):
        if self.HasBaseTypeBarrier():
            return '2:nd Barrier'
        elif self.HasBaseTypeDigitalEuropean() or self.HasBaseTypeDigitalAmerican():
            return '2:nd Trigger'
    
    def TradePriceLabel(self, *args):
        return 'Price ' + QuotationLabel(self.CurrentSaveTrade())
        
    def TradePremiumLabel(self, *args):
        return 'Premium ' + CurrencyNameFromCurrency(self.premiumCurrency)
        
    def DomesticCurrencyLabel(self, *args):
        label = ''
        if self.HasBaseTypeDigitalAmerican():
            label = CurrencyLabel(True, self.IsQuoteCallOption(), put='Down', call='Up')
        else:
            label = CurrencyLabel(True, self.IsQuoteCallOption())
        return label
        
    def ForeignCurrencyLabel(self, *args):
        label = ''
        if self.HasBaseTypeDigitalAmerican():
            label = CurrencyLabel(False, self.IsQuoteCallOption(), put='Down', call='Up')
        else:
            label = CurrencyLabel(False, self.IsQuoteCallOption())
        return label
        
    def SubtypeLabel(self, traitName, *args):
        subtypeTrait = self.SubtypeTrait(traitName.replace('subtype', ''))
        return self.GetAttributeMetaData(subtypeTrait, "label")()    
    '''*******************************************************
    * Delta Hedge methods
    *******************************************************'''
    def DeltaHedgeIsEnabled(self):
        return self.deltaHedge_type != 'None'
    
    def DeltaHedgeUpdatePrice(self, *args):
        self.SetDeltaHedgePriceToSpotOrForward(self.GetAttribute('deltaHedge_type'))

    def DeltaHedgeUpdateDelta(self, *args):
        self.SetDeltaHedgeDelta(self.GetAttribute('deltaHedge_type'))
    
    def SetDeltaHedgePriceToSpotOrForward(self, deltaHedgeType):
        price = None
        if deltaHedgeType == 'Spot':
            price = self.GetDeltaHedgeValueFromAttribute('quoteTradeCalcVal_undVal')
        elif deltaHedgeType == 'Forward':
            price = self.GetDeltaHedgeValueFromAttribute('quoteTradeCalcVal_fwd')
        if price:
            self.SetAttribute('deltaHedge_price', price)    
            
    def SetDeltaHedgeDelta(self, deltaHedgeType):
        delta = None
        contractSize = self.foreignInstrument.ContractSize()
        contractSizeInQuotation = self.foreignInstrument.ContractSizeInQuotation()
        
        if self.foreignInstrument.IsKindOf('FCommodityVariant'):
            conversionRatio = self.foreignInstrument.ConversionRatio()
        else:
            conversionRatio = 1.0
        
        if deltaHedgeType == 'Spot':
            delta = self.GetDeltaHedgeValueFromAttribute('positionSpotDelta')
        elif deltaHedgeType == 'Forward':
            delta = self.GetDeltaHedgeValueFromAttribute('positionForwardDelta')
        if delta and contractSize and conversionRatio:
            self.SetAttribute('deltaHedge_delta', round(delta / contractSize / conversionRatio))
        
    def SetDeltaHedgeValueDay(self, deltaHedgeType):
        valueDay = None
        if deltaHedgeType == 'Spot':
            valueDay = self.CurrentSaveTrade().ValueDay()
        elif deltaHedgeType == 'Forward':
            valueDay = self.GetAttribute('deliveryDate')
        if valueDay:
            self.SetAttribute('deltaHedge_valueDay', valueDay)

    '''*******************************************************
    * Object Mapping methods
    *******************************************************'''  
    def TradePremium(self, premium = 'ValueNotSet'):
        premiumType = "Premium" if self.payType != "Forward" else "ForwardPremium"
        premiumMethod = getattr(self.CurrentSaveTrade(), premiumType)
        if premium == 'ValueNotSet':
            return premiumMethod()
        else:
            premiumMethod(premium)

    def OptionType(self, value = "ValueNotSet"):
        currentOptionType = self.CurrentSaveTrade().Instrument().OptionType()
        if value == 'ValueNotSet':
            return currentOptionType
        else:
            if self.OptionTypeShouldBeFlipped(value):
                # Use the action to switch option type to make sure that
                # all four pricing options are updated.
                self.foreignOptionType()
    
    def SubtypeTrait(self, side = 'Foreign'):
        basetype = self.baseType.replace(' ', '').replace(self.baseType[0], self.baseType[0].lower(), 1)
        return "exerciseType" if basetype == "vanilla" else "%sType%s" % (basetype, side)
    
    def Subtype(self, value = "ValueNotSet", side = 'Foreign'):
        subtypeTrait = self.SubtypeTrait(side)
        if value == 'ValueNotSet':
            return getattr(self, subtypeTrait)
        else:
            if hasattr(value, 'IsKindOf') and value.IsKindOf('FDictionary'):
                for traitName in value:
                    setattr(self, traitName, value[traitName])
            else:   
                setattr(self, subtypeTrait, value)
    
    def SubtypeForeign(self, value = "ValueNotSet"):
        return self.Subtype(value, "Foreign")

    def SubtypeDomestic(self, value = "ValueNotSet"):
        return self.Subtype(value, "Domestic")

    '''*******************************************************
    * Util methods
    *******************************************************'''  
    def OptionTypeShouldBeFlipped(self, value):
        return (value.upper() in ['PUT', 'CALL'] and 
                value.upper() != self.CurrentSaveTrade().Instrument().OptionType().upper())

