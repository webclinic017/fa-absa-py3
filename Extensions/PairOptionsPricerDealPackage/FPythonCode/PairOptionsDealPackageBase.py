from __future__ import print_function
import acm
import types
from DealPackageDevKit import DealPackageDefinition, Object, Action, Str, Bool, CalcVal, List, CounterpartyChoices, AcquirerChoices
from DealPackageDevKit import PortfolioChoices, TradeStatusChoices, DealPackageChoiceListSource, DealPackageException, ParseFloat
from PairOptionsFormatters import GetFXSpotForwardFormatter, AmountFormatter, FXRateFormatter, FXRateInverseFormatter, FXPointsFormatter, SingleValueFormatter
from PairOptionsUtil import GetMaxMinBounderiesStrikeSolving, GuiAttributeToSolverAttributeName, GetOppositeAttributeName
from PairOptionsUtil import IsOfTypeFLot, IsFxOption, IsValidBidAskVolatilitySurfaces
from PairOptionsUtil import QuotationLabel, CurrencyLabel, GetFloatFromCalculation, GetFixingSourceChoices, GetValGroupChoices, Inverse
from PairOptionsUtil import ValuationAddOnModelIsUsed, ValuesAreEqual, PriceGreekExcludeVolatilityMovement, DomesticColumnConfig
from PairOptionsUtil import Flipped, IsBidAskValue, IsIterable, TransformDecimalPoints, TransformMagnitude
from PairOptionsUtil import CurrencyStrFromDV, UsePerUnitQuotationImpl
from PairOptionsUtil import FixingSourceFromString, ValGroupFromString
from InstrumentPairFromStrUtil import InstrumentFromStr, InstrumentPairFromStr, CallPutFromInstrumentPairFromStr, GetInstrumentPairFromInput
from DateFromStrUtil import TransformExpiryInputStrToDate
from OptionTypeFromStrUtil import TransformToOptionTypeFromStr
from DealPackageCalculations import DealPackageCalculations
from FXOptionPricerExtensionPoint import TurnOffRealTimeUpdatesOnSimulation, PreciousMetalChoiceList
from FXOptionPricerExtensionPoint import ValuationGroupOverride, CustomerAdditionalAttributes
from TraitBasedDealPackage import SetSolverParametersWithSafeExit
from FXCalculations import SaveTradeCalculations
        

class PairOptionsDealPackageBase(DealPackageDefinition):
    expiryDate =                Object( label='Expiry',
                                        objMapping='PricingInstruments.FxoExpiryDate',
                                        onChanged='@UnsimulateVolatility',
                                        transform='@TransformExpiryDate')
    
    daysToExpiry =              Object( label='Exp Days',
                                        objMapping='PricingOptions.DaysToExpiry',
                                        enabled=False)
                                        
    deliveryDate =              Object( label = 'Delivery',
                                        objMapping = 'PricingInstruments.DeliveryDate',
                                        onChanged='@UnsimulateVolatility',
                                        transform='@DeliveryDateFromPeriod',
                                        tabStop = False)  
    
    daysToDelivery =            Object( label='Del Days',
                                        objMapping='PricingOptions.DaysToDelivery',
                                        enabled=False)
                 
    payType =                   Object( label = 'Pay Type',
                                        objMapping = 'PricingInstruments.PayType',
                                        choiceListSource = ['Spot', 'Forward'],
                                        recreateCalcSpaceOnChange = True)
                                        
    settlementType =            Object( label = 'Settlement Type',
                                        objMapping = 'PricingOptions.SettlementType',
                                        choiceListSource = ['Physical', 'Cash'],
                                        visible='@ShowSettlementType')

    exerciseType =              Object( label='Exercise',
                                        objMapping='PricingInstruments.ExerciseType',
                                        transform='@TransformToOptionType',
                                        visible='@HasBaseTypeVanilla',
                                        choiceListSource='@ExerciseTypeChoiceList',
                                        recreateCalcSpaceOnChange = True)
                       
    tradeTime =                 Object( defaultValue = acm.Time.DateToday(),
                                        label='Trade Time',
                                        objMapping='PricingTrades.TradeTime',
                                        transform='@TradeTimeFromPeriod')
                                        
    valueDay =                  Object( label='Value Day',
                                        objMapping='PricingTrades.ValueDay',
                                        transform='@ValueDayFromPeriod')  
                                
    tradeStatus =               Object( label = 'Status',
                                        objMapping = 'PricingTrades.Status',
                                        choiceListSource=TradeStatusChoices())  

    portfolio =                 Object( label = 'Portfolio',
                                        objMapping = 'PricingTrades.Portfolio',
                                        choiceListSource=PortfolioChoices(),
                                        mandatory='@PortfolioIsMandatory')
                                        
    acquirer  =                 Object( label = 'Acquirer',
                                        objMapping = 'PricingTrades.Acquirer',
                                        choiceListSource=AcquirerChoices(),
                                        mandatory='@AcquirerIsMandatory')
                        
    counterparty =              Object( label='Counterparty',
                                        objMapping='PricingTrades.Counterparty',
                                        choiceListSource=CounterpartyChoices(),
                                        mandatory='@TradeIsConfirmed',
                                        onChanged='@UpdateMirrorPortfolioChoices')
                                        
    counterpartyPortfolio =     Object( label='Cpty Portfolio',
                                        objMapping='CounterpartyPortfolio',
                                        visible='@MirrorPortfolioVisible',
                                        domain=acm.FPhysicalPortfolio,
                                        choiceListSource='@MirrorPortfolioChoices')
                                        
    trader =                    Object( label='Trader',
                                        objMapping='PricingTrades.Trader',
                                        mandatory='@TraderIsMandatory')                      
                                        
    broker =                    Object( label='Broker',
                                        objMapping='PricingTrades.Broker')
                            
    memo =                      Object( defaultValue='',
                                        label='Memo',
                                        objMapping='DealPackage.AdditionalInfo.MemoString')

    instrumentPair =            Str(    label = 'Currency Pair',
                                        objMapping='InstrumentPair',
                                        transform='@TransformToInstrumentPair',
                                        onChanged='@OnInstrumentPairChanged|UpdateInstrumentChoices|UpdatePremiumCurrencyChoices')
                                
    foreignInstrument =         Object( label='@ForeignCurrencyLabel',
                                        objMapping='PricingOptions.ForeignInstrument',
                                        transform='@TransformToForeignInstrument',
                                        choiceListSource='@ForeignCurrencyChoices',
                                        onChanged='@OnInstrumentPairChanged|UpdateInstrumentChoices|UpdatePremiumCurrencyChoices')
                                
    domesticCurrency =          Object( label='@DomesticCurrencyLabel',
                                        objMapping='PricingOptions.DomesticCurrency',
                                        transform='@TransformToDomesticCurrency',
                                        choiceListSource='@DomesticCurrencyChoices',
                                        onChanged='@OnInstrumentPairChanged|UpdateInstrumentChoices|UpdatePremiumCurrencyChoices')
                                
    strikeDomesticPerForeign =  Object( label='@StrikeDomPerForLabel',
                                        objMapping='PricingOptions.StrikeDomesticPerForeign',
                                        transform='@TransformStrikePrice',
                                        formatter='@StrikeFormatterCB',
                                        visible = '@IsNotDigitalAmerican',
                                        recreateCalcSpaceOnChange=True)
    
    strikeForeignPerDomestic =  Object( label='@StrikeForPerDomLabel',
                                        objMapping='PricingOptions.StrikeForeignPerDomestic',
                                        transform='@TransformStrikePrice',
                                        formatter='@StrikeFormatterInverseCB',
                                        visible = '@IsNotDigitalAmerican',
                                        recreateCalcSpaceOnChange=True)
    
    solverStrikeDomPerFor =     Object( label='@StrikeDomPerForLabel',
                                        objMapping='PricingOptions.StrikeDomesticPerForeignNoInputFormatter',
                                        transform='@TransformStrikePrice',
                                        solverParameter='@StrikeParamDomPerFor',
                                        onChanged='@SolverStrikeChanged')
                                 
    solverStrikeForPerDom =     Object( label='@StrikeForPerDomLabel',
                                        objMapping='PricingOptions.StrikeForeignPerDomesticNoInputFormatter',
                                        solverParameter='@StrikeParamForPerDom',
                                        onChanged='@SolverStrikeChanged')
                                        
    amountForeign =             Object( defaultValue=1000000,
                                        label='@ForeignAmountLabel',
                                        objMapping='PricingOptions.AmountForeign',
                                        transform='@AmountTransform',
                                        onChanged='@UpdateDealPackageTrade',
                                        formatter='@ForeignAmountFormatterCB',
                                        enabled='@ForeignAmountEnabled',
                                        recreateCalcSpaceOnChange=True)
            
                                        
    amountDomestic =            Object( label='@DomesticAmountLabel',
                                        objMapping='PricingOptions.AmountDomestic',
                                        transform='@AmountTransform',
                                        onChanged='@UpdateDealPackageTrade',
                                        formatter='@DomesticAmountFormatterCB',
                                        enabled='@DomesticAmountEnabled',
                                        recreateCalcSpaceOnChange=True)        
    
    premiumCurrency =           Object( label='Premium Curr',
                                        objMapping='PricingOptions.PremiumCurrency',
                                        domain=acm.FCurrency,
                                        choiceListSource='@PremiumCurrencyChoices',
                                        onChanged='@UpdateDealPackageTrade|SetRoundingSpecification',
                                        transform='@TransformToValidCurrency')
          
    fixingSource =              Object( label='Fixing Source',
                                        objMapping='PricingInstruments.FixingSource',
                                        choiceListSource='@FixingSourceChoices',
                                        transform='@TransformToValidFixingSource')
                                        
    valGroup =                  Object( label='Val Group',
                                        objMapping='PricingInstruments.ValuationGrpChlItem',
                                        choiceListSource='@ValGroupChoices',
                                        recreateCalcSpaceOnChange=True,
                                        transform='@TransformToValidValGroup')

    saveIsFlippedSide =         Object( objMapping='PricingOptions.CurrentSaveIsFlipped',
                                        onChanged='@FlippedSideChanged')
    
    isQuoteCallOption =         Bool(   objMapping='IsQuoteCallOption')

    setForeignAsSave =          Action( label='@ForeignAmountLabel',
                                        action='@SetForeignAsSaveSide',
                                        recreateCalcSpaceOnChange=True,
                                        enabled='@IsNotDigital')
                                        
    setDomesticAsSave =         Action( label='@DomesticAmountLabel',
                                        action='@SetDomesticAsSaveSide',
                                        recreateCalcSpaceOnChange=True)

    buySell =                   Action( label='@BuySellHeader',
                                        action='@UpdateBuySell')
                                        
    removeSimulations =         Action( action='@RemoveSimulations')

    setSolverParameterAction =  Action( label='Set solverParameter',
                                        action='@SetSolverParameter')
                                        
    updateTradePriceFromTheor = Action( label='Update Trd Price',
                                        action='@UpdateTradePriceFromTheor')
                                        
    flipBidAskMode =            Action( label='Flip bid/ask mode',
                                        action='@FlipBidAskMode')

    flipPremiumCurrency =       Action( label='Flip Premium Currency',
                                        action='@FlipPremiumCurrency')
                                        
    refreshMarketDataPerAttr =  Action( label='Refresh Market Data Per Attribute',
                                        action='@RefreshMarketDataAttr')

    getStoredPricingParameters= Action(action='@GetStoredPricingParameters',
                                        noDealPackageRefreshOnChange=True)

    marketValuesLocked =        Bool(   objMapping = 'MarketValuesLocked')

    saveTradeQuotation =        Str(    label='Quotation',
                                        objMapping='SaveTradeQuotation',
                                        enabled=False)

    valuationModel =            Str(    label='Model',
                                        objMapping='ValuationModel')
                                        
    valuationAddOnModel =       Str(    label='Add On',
                                        objMapping='ValuationAddOnModel',
                                        visible='@ValuationAddOnModelUsed')

    bidAskMode =                Bool(   objMapping='BidAskMode')

    bidAskModeVol =             Bool(   objMapping='BidAskModeVol')
    
    volatility =                CalcVal(label = 'Vol %',
                                        calcMapping='VolatilityObjectsAsLot:FDealSheet:Portfolio Volatility FXOStrat',
                                        onChanged='@ValueSimulated|ReaplySimulation',
                                        transform='@TransformVolatility',
                                        solverParameter='@VolatilityParam')

    atmVolatility =             CalcVal(label = 'ATM Vol %',
                                        calcMapping='QuoteTrade:FDealSheet:ATM Volatility',
                                        onChanged='@ValueSimulated',
                                        _isUserSimulated='@IsCalculationUserSimulated',
                                        transform='@TransformVolatility',
                                        solverParameter='@VolatilityParam',
                                        enabled='@AtmVolatilityEnabled')
                                        
  
    undVal =                    CalcVal( calcMapping='CurrentSaveTrade:FDealSheet:Portfolio Underlying Price FXOStrat',
                                         formatter='@FXRateFlipFormatterCB',
                                         transform='@TransformPriceParse',
                                         onChanged='@ValueSimulated',
                                         calcConfiguration='@UsePerUnitQuotation',
                                         _isUserSimulated='@IsCalculationUserSimulated',
                                         solverParameter='@UndValParam')

    customCalculations =        List(   label='@CustomCalcLabel',
                                        action='@GetCustomCalculation',
                                        visible=True,
                                        enabled=False,
                                        noDealPackageRefreshOnChange=True)
                                        
    saveTradeCalcVal =          SaveTradeCalculations()
                                        
    customerAttributes =        CustomerAdditionalAttributes(tradeNames = 'PricingTrades')
                        
    # -------------------------------------------------------------------------------
    # Action to use when flipping a strip of options to flip simulations
    # -------------------------------------------------------------------------------    
    flipSaveTradeSimulations =  Action( action = '@FlipSaveTradeCalcSimulations' )

    '''*******************************************************
    * Trade/Instrument Get methods
    *******************************************************'''         
    def PricingOptions(self):
        return self._pricingOptions
    
    def PricingTrades(self):
        return self.PricingOptions().Trades()
    
    def PricingInstruments(self):
        return self.PricingOptions().Instruments()
 
    def CurrentSaveTrade(self):
        return self.PricingOptions().CurrentSaveTrades().First()
        
    def FXRatesToLock(self):
        if self.foreignInstrument.IsKindOf('FCommodityVariant'):
            cmdCurr = self.foreignInstrument.Underlying().Currency()
            tradeCurr = self.domesticCurrency
            if cmdCurr != tradeCurr:
                fxRate = acm.GetFunction('CreateFxRate', 2)
                return acm.FLot([fxRate(cmdCurr, tradeCurr), fxRate(tradeCurr, cmdCurr)])

    def AsPortfolio(self):
        return self.DealPackage().AsPortfolio()
        
    '''*******************************************************
    * Helper Methods
    *******************************************************'''  
    def GetUnderlyingValue(self, name):
        value = None
        if name in ['strikeDomesticPerForeign', 'solverStrikeDomPerFor', 'strike2DomesticPerForeign', 'solverStrike2DomPerFor']:
            value = self.quoteTradeCalcVal_undVal
        elif name in ['strikeForeignPerDomestic', 'solverStrikeForPerDom', 'strike2ForeignPerDomestic', 'solverStrike2ForPerDom']:
            value = self.flippedQuoteTradeCalcVal_undVal
        #Used to keep old logic, should be removed
        buySell = ('Buy' if self.BuySellLabel() == 'Sell' else 'Sell') if self.IsPutOptionForSide(name) else self.BuySellLabel()
        return GetFloatFromCalculation(value, buySell)
        
    def GetForwardValue(self, name):
        value = None
        if name in ['strikeDomesticPerForeign', 'solverStrikeDomPerFor', 'strike2DomesticPerForeign', 'solverStrike2DomPerFor']:
            value = self.quoteTradeCalcVal_fwd
        elif name in ['strikeForeignPerDomestic', 'solverStrikeForPerDom', 'strike2ForeignPerDomestic', 'solverStrike2ForPerDom']:
            value = self.flippedQuoteTradeCalcVal_fwd
        #Used to keep old logic, should be removed
        buySell = ('Buy' if self.BuySellLabel() == 'Sell' else 'Sell') if self.IsPutOptionForSide(name) else self.BuySellLabel()
        return GetFloatFromCalculation(value, buySell)
     
    def SetNewSaveTradeOnDealPackage(self):
        # Overridden in sub class
        pass
        
    def GetDeltaHedgeValueFromAttribute(self, attributeName):
        retVal = self.GetAttribute(attributeName).Value()
        if IsOfTypeFLot(retVal):
            if self.CurrentSaveTrade().Quantity() > 0:
                retVal = retVal[0].Number()
            else:
                retVal = retVal[1].Number()
        else:
            retVal = retVal.Number()
        return retVal      
        
    def IsFxOption(self):
        return IsFxOption(self.QuoteInstrument())
  
    def IsPmOption(self):
        return not IsFxOption(self.QuoteInstrument())
        
    def ParentIsStrip(self):
        isStrip = False
        if self.DealPackage().ParentDealPackage():
            isStrip = str(self.DealPackage().ParentDealPackage().DefinitionName()) == 'FXStripDealPackage'
        return isStrip
        
    def SetAttributeOnStrip(self, attrName, val):
        if self.ParentIsStrip():
            self.DealPackage().ParentDealPackage().SetAttribute(attrName, val)
            self.DealPackage().ParentDealPackage().Refresh()
        else:
            raise DealPackageException("Parent is not a Strip")
            
    def StoreMarketValues(self, attributeToStore = None):
        try:
            attributesToStore = [attributeToStore] if attributeToStore else self._storedPricingParameters.keys()
            calcCopy = self.GetCalculationsCopy(copySimulations = False)
            for attribute in list(attributesToStore):
                if not self.GetCalculation(attribute):
                    if self.FXRatesToLock():
                        self.CreateCalculation(attribute, 'FXRatesToLock:FDealSheet:%s' % attribute)
                        calcCopy.CreateMissingCalculations(acm.GetFunction('createDictionary', 2)(attribute, self._dealPackageCalculations.Calculation(attribute)))
                    else:
                        attributesToStore.remove(attribute)
                        continue
                self._storedPricingParameters[attribute] = [self.GetValueToStore(attribute, calcCopy.Value(attribute).Value()), None]
            calcCopy.SimulateValue('useBidOrAskPrice', ['Bid', 'Ask'])
            calcCopy.SimulateValue('alternativeContext', ["Bid", "Ask"])
            for attribute in attributesToStore:
                self._storedPricingParameters[attribute][1] = self.GetValueToStore(attribute, calcCopy.Value(attribute).Value())
            calcCopy.TearDown()
        except Exception as e:
            self.Log().Error('Failed to store market values. %s' % e)
            if not attributeToStore:
                for attribute in self._storedPricingParameters:
                    self._storedPricingParameters[attribute] = None
                    if not hasattr(self, attribute):
                        self.RemoveCalculation(attribute)
                    
    def LockMarketValues(self, lockSimulatedValues = False):
        if self.MarketValuesLocked():
            for attribute, storedValue in sorted(self._storedPricingParameters.items()):
                #Using sorted because fxSpotRate has to be locked before quoteTradeCalcVal_undVal.
                #UndVal is using fxSpotRate in column transform
                if not storedValue:
                    continue
                bidAskMode = self.BidAskModeVol() if attribute.lower().find('volatility') != -1 else self.BidAskMode()
                if lockSimulatedValues or not self.IsCalculationUserSimulated(attribute):
                    value = storedValue[1] if bidAskMode else storedValue[0]
                    if hasattr(self, attribute):
                        setattr(self, attribute, value)
                    else:
                        self.SimulateCalculation(attribute, value)
    
    def RefreshLockedValue(self, attribute):
        if self._storedPricingParameters.get(attribute):
            self.StoreMarketValues(attribute)
        self.UnsimulateAttributeValue(attribute)
        
    def GetCalculationsCopy(self, copyCalculations = True, copySimulations = True, setBidAsk = None):
        calcCopy = DealPackageCalculations(self, 1)
        for traitName in self._GetTraitNames():
            calcInfo = self.trait_metadata(traitName, "calcMapping")
            if calcInfo and self._GetTrait(traitName).__class__ == CalcVal:
                configurationCb = self._GetAttributeMetaDataCallback(traitName, "calcConfiguration")
                calcObjCb, columnId, columnIdCb, sheetType = self._GetCalcSpecFromTraitInfo(calcInfo)
                calcCopy.CreateCalculation(traitName, calcObjCb, sheetType, columnId, columnIdCb, configurationCb)
        if copyCalculations:
            calcCopy.CreateMissingCalculations(self._GetCalculations())
        if copySimulations:
            calcCopy.ApplySimulations(self._GetSimulations())
        if setBidAsk == True:
            calcCopy.SimulateValue('useBidOrAskPrice', ['Bid', 'Ask'])
            calcCopy.SimulateValue('alternativeContext', ["Bid", "Ask"])
        elif setBidAsk == False:
            calcCopy.SimulateValue('useBidOrAskPrice', '')
            calcCopy.SimulateValue('alternativeContext', '')
            simulations = calcCopy.Simulations()
            for attribute in simulations:
                simulatedValue = simulations[attribute]
                if IsBidAskValue(simulatedValue):
                    #Simulated value is bid ask but not in bid ask mode, use mid
                    calcCopy.SimulateValue(attribute, sum(map(ParseFloat, simulatedValue)) / len(simulatedValue))
        return calcCopy  
    
    def GetValueToStore(self, attribute, value = None):
        calc = self.GetCalculation(attribute)
        if IsIterable(calc) and hasattr(self, attribute):
            calc = calc[0]
        if value is None:
            try:
                value = calc.Value()
            except Exception as e:
                self.Log().Error('Failed to get value for %s. [%s]' % (attribute, e))
                return
        if value and hasattr(self, attribute):
            value /= calc.Parse(1.0) #Assume calculation formatting is only inverse scaling of parse
            if IsBidAskValue(value):
                if value[0] == value[-1]:
                    value = value[0]
                else:
                    value = [v for v in value]
        return value
    
    def GetColumnFormatter(self, attributeName):
        return self._DealPackageBase__ColumnFormatter(attributeName)
    
    '''*******************************************************
    * Action methods
    *******************************************************'''   
    def UpdateBuySell(self, *args):
        if self.PricingOptions().CurrentSaveIsFlipped():
            self.amountDomestic = -self.amountDomestic
        else:
            self.amountForeign = -self.amountForeign

    def SetCurrentSaveToQuote(self):
        self.PricingOptions().SetCurrentSaveToQuote()
        self.SetNewSaveTradeOnDealPackage()
    
    def SetCurrentSaveToFlipped(self):
        self.PricingOptions().SetCurrentSaveToFlipped()
        self.SetNewSaveTradeOnDealPackage()
        
    def SetForeignAsSaveSide(self, *args):
        if self.IsDigital():
            self.payoutCurrency = self.foreignInstrument
        self.SetCurrentSaveToQuote()        
        
    def SetDomesticAsSaveSide(self, *args):
        if self.IsDigital():
            self.payoutCurrency = self.domesticCurrency
        else:
            self.SetCurrentSaveToFlipped()            
  
    def RemoveSimulations(self, *args):
        bidAskMode = self.bidAskMode
        self.RemoveAllSimulations()
        self.BidAskMode(bidAskMode)
        self.LockMarketValues(True)

    def TransformStrikeSolverAttr(self, guiAttr):
        return GuiAttributeToSolverAttributeName(guiAttr)

    def ValidateSolverParameter(self, newSolverParameter):
        return self.GetAttributeMetaData(newSolverParameter, 'solverParameter')()
        
    def SetSolverParameter(self, attrName, newSolverParameter):
        newSolverParameter = self.TransformStrikeSolverAttr(newSolverParameter)  
        if self.ValidateSolverParameter(newSolverParameter):
            self.solverParameter = newSolverParameter
            
    def GetTheorPrcForCurrentSaveTrade(self):
        theorPrc = None
        if self.PricingOptions().CurrentSaveIsQuoteTrade():
            theorPrc = self.quoteTradeCalcVal_theor
        elif self.PricingOptions().CurrentSaveIsAltQuoteTrade():
            theorPrc = self.quoteTradeCalcVal_theorPct
        elif self.PricingOptions().CurrentSaveIsFlippedQuoteTrade():
            theorPrc = self.flippedQuoteTradeCalcVal_theor
        elif self.PricingOptions().CurrentSaveIsFlippedAltQuoteTrade():
            theorPrc = self.flippedQuoteTradeCalcVal_theorPct
        return theorPrc
        
    def UpdateTradePriceFromTheor(self, *args):
        try:
            self.tradePrice = GetFloatFromCalculation(self.GetTheorPrcForCurrentSaveTrade(), self.BuySellLabel())
        except Exception as e:
            # Can't trust the theor to always be OK
            pass
            
    def FlipBidAskMode(self, *args):
        self.bidAskMode = not self.bidAskMode
    
    def RefreshMarketDataAttr(self, attrName, updateValueForAttrName):
        if self._storedPricingParameters.get(updateValueForAttrName):
            self.RefreshLockedValue(updateValueForAttrName)
        else:
            setattr(self, updateValueForAttrName, None)
    
    def UsePerUnitQuotation(self, attrName):
        return UsePerUnitQuotationImpl(attrName)

    def IsCalculationUserSimulatedImpl(self, attributeName):    
        if self.IsCalculationSimulated(attributeName):
            storedValue = self._storedPricingParameters.get(attributeName)
            if storedValue:
                #storedValue = storedValue[-1] if self.bidAskMode else storedValue[0]
                attributeValue = self.GetValueToStore(attributeName)
                if ValuesAreEqual(storedValue[0], attributeValue) or ValuesAreEqual(storedValue[-1], attributeValue):
                    #Comparing with both to get correct behavior when changing bid/ask mode
                    return False
            return True
        return False
        
    def GetOppositeSimulationAttribute(self, attributeName):
        try:
            if self.GetAttributeMetaData(attributeName, '_setOppositeSideAsSimulated')():        
                oppositeAttributeName = GetOppositeAttributeName(attributeName)
                if oppositeAttributeName in self.DealPackage().GetAttributes():
                    return oppositeAttributeName
        except:
            #Will fail if you call the method with a caluclation which isn't an attribute
            pass

    def IsCalculationUserSimulated(self, attributeName):
        if not self.IsCalculationUserSimulatedImpl(attributeName):
            oppositeAttributeName = self.GetOppositeSimulationAttribute(attributeName)
            if oppositeAttributeName:
                return self.IsCalculationUserSimulatedImpl(oppositeAttributeName)
            return False
        return True
  
    def ChangeCallPut(self, *args):
        self.PricingOptions().ChangeCallPut()
        
    def DeltaHedgeIsEnabled(self):
        pass
        
    def TradeIsConfirmed(self, *args):
        return not self.tradeStatus in ('Simulated', 'Reserved', 'Void')
        
    def AcquirerIsMandatory(self, *args):
        return self.TradeIsConfirmed() or self.DeltaHedgeIsEnabled()
    
    def TraderIsMandatory(self, *args):
        installData  = acm.FInstallationData.Instances().First() 
        return self.TradeIsConfirmed() and installData.TraderMandatory()
    
    def PortfolioIsMandatory(self, *args):
        installData  = acm.FInstallationData.Instances().First()
        portfolioMandatory = installData.PhysicalPortfolioMandatory()
        return (self.TradeIsConfirmed() and portfolioMandatory) or self.DeltaHedgeIsEnabled()

    def FlipSaveTradeCalcSimulations(self, attrName, isFlipped, *args):
        # Override in sub classes
        pass

    def FlipPremiumCurrency(self, *args):
        if self.foreignInstrument == self.premiumCurrency:
            self.premiumCurrency = self.domesticCurrency
        else:
            self.premiumCurrency = self.foreignInstrument
            
    '''*******************************************************
    * Object Mapping methods
    *******************************************************'''  
    def ValuationModel(self, notUsed = None):
        if notUsed:
            pass
        return self.CurrentSaveTrade().Instrument().ValuationModel()
        
    def ValuationAddOnModel(self, notUsed = None):
        if notUsed:
            pass
        return self.CurrentSaveTrade().Instrument().ValuationAddOnModel()
                
    def IsQuoteCallOption(self, notUsed = None):
        if notUsed:
            pass
        return self.QuoteTrade().Instrument().IsCall()
                
    def InstrumentPair(self, instrPair = None):
        if not instrPair:
            return self.PricingOptions().InstrumentPair().Name()
        else:
            self.PricingOptions().InstrumentPair(instrPair)
            
    def SaveTradeQuotation(self, notUsed = None):
        if notUsed:
            pass
        return QuotationLabel(self.CurrentSaveTrade())
   
    def VolatilityObjectsAsLot(self, notUsed = None):
        #Not implemented in base class
        raise NotImplementedError()
   
    def BidAskMode(self, setBidAskMode = None):
        if not self._dealPackageCalculations:
            return False
        if not self.GetCalculation('useBidOrAskPrice'):
            self.CreateCalculation('useBidOrAskPrice', 'Trade:FDealSheet:useBidOrAskPrice')
        bidAskMode = IsBidAskValue(self.GetCalculation('useBidOrAskPrice').Value())
        if setBidAskMode == None:
            return bidAskMode
        elif setBidAskMode == bidAskMode:
            self.BidAskModeVol(setBidAskMode)
            return
        self.SimulateCalculation('useBidOrAskPrice', ['Bid', 'Ask'] if setBidAskMode else "")
        if self.BidAskModeVol(setBidAskMode) is None:
            self.LockMarketValues()
        if not setBidAskMode:
            for attribute in self._GetSimulations():
                simulatedValue = self._GetSimulations()[attribute]
                if IsBidAskValue(simulatedValue) and hasattr(self, attribute):
                    #Simulated value is bid ask but not in bid ask mode, use mid
                    setattr(self, attribute, sum(map(ParseFloat, simulatedValue)) / len(simulatedValue))

    def BidAskModeVol(self, setBidAskMode = None):
        if not self._dealPackageCalculations:
            return False
        if not self.GetCalculation('alternativeContext'):
            self.CreateCalculation('alternativeContext', 'Trade:FDealSheet:alternativeContext')
        bidAskMode = IsBidAskValue(self.GetCalculation('alternativeContext').Value())
        if setBidAskMode == None:
            return bidAskMode
        elif bidAskMode != setBidAskMode:
            if setBidAskMode and not IsValidBidAskVolatilitySurfaces(self.PricingInstruments().First().Instrument()):
                return bidAskMode
            self.SimulateCalculation('alternativeContext', ['Bid', 'Ask'] if setBidAskMode else "")
            self.LockMarketValues()
            return setBidAskMode

    def MarketValuesLocked(self, lockOrUnlockValues = None):
        if lockOrUnlockValues == None:
            for value in self._storedPricingParameters.values():
                if value != None:
                    return True
            return False
        elif lockOrUnlockValues == True:
            self.StoreMarketValues()
            self.LockMarketValues()
        elif lockOrUnlockValues == False:
            for attribute in self._storedPricingParameters:
                if not hasattr(self, attribute):
                    self.RemoveCalculation(attribute)
                elif not self.IsCalculationUserSimulated(attribute):
                    self.SimulateCalculation(attribute, "") #Remove simulation
                self._storedPricingParameters[attribute] = None

    '''*******************************************************
    * OnChanged methods
    *******************************************************'''          
    def ValueSimulated(self, attributeName, old, new, userInputAttributeName):
        if self.IsCalculationSimulated(attributeName):
            if TurnOffRealTimeUpdatesOnSimulation() and not self.MarketValuesLocked():
                if self.ParentIsStrip():
                    self.SetAttributeOnStrip('marketValuesLocked', True)
                else:
                    self.marketValuesLocked = True
                self.ReaplySimulation(attributeName, old, new, userInputAttributeName)
        else:
            self.UnsimulateAttributeValue(attributeName)
            
    def ReaplySimulation(self, attributeName, old, new, userInputAttributeName):
        simulatedValue = self.GetSimulatedCalculationValue(attributeName)
        self.SimulateCalculation(attributeName, '')
        self.SimulateCalculation(attributeName, simulatedValue)
        
    def UnsimulateVolatility(self, attributeName, old, new, userInputAttributeName):
        self.UnsimulateAttributeValue('volatility')
        #self.RefreshLockedValue('atmVolatility')
    
    def SetRoundingSpecification(self, attributeName, old, new, userInputAttributeName):
        roundingSpec = self.premiumCurrency.RoundingSpecification()
        for instrument in self.PricingInstruments():
            for ins in instrument.Instruments() if instrument.IsKindOf('FCombination') else [instrument]:
                ins.RoundingSpecification(roundingSpec)
    
    def SetDefaultStrike(self):
        self.DealPackage().SetAttribute('solverStrikeDomPerFor', 'atmf')
        
    def Refresh(self):
        try:
            if self._updateDefaultStrike: 
                self.SetDefaultStrike() 
                self.tradePrice = 0
        except Exception as e:
            print (e)
        finally:
            self._updateDefaultStrike = False 

   
    def OnInstrumentPairChanged(self, attr, oldVal, newVal, userInputTraitName):
        if userInputTraitName == None:   
            self.MarketValuesLocked(False)
            self.GetAttribute('removeSimulations')()
            self.solverParameter = 'solverStrikeDomPerFor'
            self._updateDefaultStrike = True
        
    def UpdatePremiumCurrencyChoices(self, *args):
        self._premiumCurrencyChoices.Clear()
        if self.IsFxOption():
            self._premiumCurrencyChoices.AddAll([self.foreignInstrument, self.domesticCurrency])            
        else:
            self._premiumCurrencyChoices.AddAll([self.domesticCurrency])            

    def UpdateDealPackageTrade(self, attr, oldVal, newVal, userInputtedAttr):
        if oldVal and newVal and not userInputtedAttr:
            self.SetNewSaveTradeOnDealPackage()

    def FlippedSideChanged(self, *args):
        # Overridden in sub class
        pass
    
    '''*******************************************************
    * Choices methods
    *******************************************************'''   
    def PremiumCurrencyChoices(self, *args):
        if self._premiumCurrencyChoices.IsEmpty():
            self.UpdatePremiumCurrencyChoices()
        return self._premiumCurrencyChoices
     
    def ExerciseTypeChoiceList(self, *args):
        return ['European', 'American']
        
    def FixingSourceChoices(self, *args):
        return GetFixingSourceChoices()
        
    def ValGroupChoices(self, *args):
        return GetValGroupChoices()
        
    def UpdateInstrumentChoices(self, *args):
        self._foreignInstrumentChoices.Clear()
        self._domesticCurrencyChoices.Clear()
        if self.IsFxOption():
            self._foreignInstrumentChoices.AddAll(list(self.QuoteInstrument().DefaultForeignCurrencies()))
            self._domesticCurrencyChoices.AddAll(list(self.QuoteInstrument().DefaultDomesticCurrencies()))  
        else:
            self._foreignInstrumentChoices.AddAll(list(PreciousMetalChoiceList(self.QuoteInstrument())))
            self._domesticCurrencyChoices.AddAll(list(self.QuoteInstrument().DefaultPreciousMetalCurrencies()))  

    def ForeignCurrencyChoices(self, *args):
        if self._foreignInstrumentChoices.IsEmpty():
            self.UpdateInstrumentChoices()
        return self._foreignInstrumentChoices
        
    def DomesticCurrencyChoices(self, *args):
        if self._domesticCurrencyChoices.IsEmpty():
            self.UpdateInstrumentChoices()
        return self._domesticCurrencyChoices
   
    '''*******************************************************
    * Visible methods
    *******************************************************'''  
    def ValuationAddOnModelUsed(self, *args):
        return ValuationAddOnModelIsUsed(self.CurrentSaveTrade().Instrument())
        
    def IsDigital(self):
        # Overridden in sub class
        return False

    def IsDigitalAmerican(self):
        # Overridden in sub class
        return False
        
    def ShowSettlementType(self, *args):
        if self.IsFxOption():
            return self.IsNotDigital(args)
        else:
            return True
            
    def IsNotDigital(self, *args):
        return not self.IsDigital()
        
    def IsNotDigitalAmerican(self, *args):
        return not self.IsDigitalAmerican()
    
    def HasBaseTypeVanilla(self, *args):
        # Overridden in sub class
        if not hasattr(self, 'baseType'):
            return True
        return self.baseType == 'Vanilla' 
        
    '''*******************************************************
    * Transform methods
    *******************************************************'''  
    def TransformDelta(self, name, newDelta):
        delta = self.ChangeSignOnDeltaBasedOnCallPut(ParseFloat(newDelta), False)
        return str(delta)
        
    def TransformFlippedDelta(self, name, newDelta):
        delta = self.ChangeSignOnDeltaBasedOnCallPut(ParseFloat(newDelta), True)
        return str(delta)
        
    
    def SolveStrikeForPremiumAdjustedDelta(self, solverParameter, attributeName, delta):
        precision = 0.0001
        maxIterations = 100
        
        # Possible attributeName values:
        #       1) quoteTradeCalcVal_deltaBSAlt
        #       2) flippedQuoteTradeCalcVal_deltaBSAlt
        #       3) deltaBSAltCall
        #       4) deltaBSFlippedAltCall
        
        isSolverValueQuote = False if 'flipped' in attributeName.lower() else True
        isSolverParameterQuote = solverParameter.endswith('For')
        
        #if isSolverParameterQuote:
        #    fwdPrice = GetFloatFromCalculation(self.quoteTradeCalcVal_fwd, self.BuySellLabel()) if self.quoteTradeCalcVal_fwd else 1.0
        #else:
        #    fwdPrice = GetFloatFromCalculation(self.flippedQuoteTradeCalcVal_fwd, self.BuySellLabel()) if self.flippedQuoteTradeCalcVal_fwd else 1.0
        
        fwdPrice = GetFloatFromCalculation(self.quoteTradeCalcVal_fwd, self.BuySellLabel()) if self.quoteTradeCalcVal_fwd else 1.0
        
        maxStrike = self.DealPackage().Solve(solverParameter, attributeName.replace('Alt', ''), delta, fwdPrice/3, fwdPrice*3, precision, maxIterations)
        minStrike = maxStrike * 0.9
        
        # Increase maxStrike boundary by 10% when solving
        # strike for flipped premium adjusted delta.
        if isSolverValueQuote != isSolverParameterQuote:
            maxStrike = maxStrike * 1.1
        
        with SetSolverParametersWithSafeExit(self, attributeName, solverParameter, delta):
            strike = self.DealPackage().Solve(solverParameter, attributeName, delta, minStrike, maxStrike, precision, maxIterations)
        
        isFinite = acm.Math.IsFinite(strike)
        if isFinite:
            return strike
        else:
            raise DealPackageException("No solution found for '%s' that gives expected '%s' of %s. "
                                "(Using boundary conditions min = %f, max = %f, precision = %f, max iterations = %d)."
                                %(solverParameter, attributeName, delta, minStrike, maxStrike, precision, maxIterations))
        
    
    def TransformPremiumAdjustedDelta(self, attributeName, delta):
        # Since the premium adjusted call delta is not strictly
        # monotone vs strike, we need to obtain valid strike 
        # boundaries. The right limit (maxStrike) is chosen as 
        # the strike corresponding to the non-premium adjusted 
        # delta, since the premium adjusted delta for strike
        # K is always smaller than the non-premium adjusted delta 
        # corresponding to the same strike. The left limit (minStrike)
        # is chosen to be 10% smaller than maxStrike.
        
        validSolverParameters = ['solverStrikeDomPerFor', 'solverStrikeForPerDom', 'solverStrike2DomPerFor', 'solverStrike2ForPerDom']
        
        if self.solverParameter in validSolverParameters:
            if attributeName.startswith('flipped'):
                delta = self.TransformFlippedDelta(attributeName, delta)
            else:
                delta = self.TransformDelta(attributeName, delta)
                
            form = self.GetColumnFormatter(attributeName)
            delta = ParseFloat(delta, formatter=form)
            
            isCallOption = self.IsCallOptionForSide(attributeName)
            if isCallOption:
                strike = self.SolveStrikeForPremiumAdjustedDelta(self.solverParameter, attributeName, delta)
                setattr(self, self.solverParameter, strike)
                delta = self.GetValueToStore(attributeName)
                
        return delta
        
    def DeliveryDateFromPeriod(self, name, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            decoNoGUI = acm.FBusinessLogicDecorator.WrapObject(self.Instrument().Instrument())
            date = decoNoGUI.DeliveryDateFromPeriod(newDate)
        return date  
        
    def TransformExpiryDate(self, name, newDate):
        return TransformExpiryInputStrToDate(newDate, name)

    def TradeTimeFromPeriod(self, name, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate= acm.Time().PeriodSymbolToDate(newDate)
        return newDate
        
    def ValueDayFromPeriod(self, name, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            startDate = self.CurrentSaveTrade().Instrument().SpotDate(self.tradeTime)
            newDate = acm.Time().PeriodSymbolToRebasedDate(newDate, startDate)
        return newDate
            
    def TransformToOptionType(self, name, value):
        return TransformToOptionTypeFromStr(value)
            
    def TransformToInstrumentPair(self, name, value):
        instrPairName = InstrumentPairFromStr(value, self.instrumentPair, self.IsFxOption())        
        userEnteredInverseQuote = CallPutFromInstrumentPairFromStr(self.instrumentPair, instrPairName, value)
        if userEnteredInverseQuote is not None:
            if not self.IsQuoteCallOption() == userEnteredInverseQuote: # Put + inverse -> call, call + not inverse -> put
                self.ChangeCallPut()
        return instrPairName

    def FindInstrumentOrPairFromString(self, inputStr, isForeign, isFxOption): 
        value = inputStr
        if inputStr:
            value = InstrumentFromStr(inputStr, isFxOption if isForeign else True)
            if not value:
                value = self.TransformToInstrumentPair(None, inputStr)
        return value
        
    def FindCurrOrPairFromStr(self, currentInstr, otherInstr, inputStr, isForeign, isFxOption):
        currOrPairStr = None
        try:
            instrOrPairFromInputStr = self.FindInstrumentOrPairFromString(inputStr, isForeign, isFxOption)
            if instrOrPairFromInputStr and acm.FInstrument[instrOrPairFromInputStr]:
                otherInstrStr = otherInstr.Name() if otherInstr else None
                instrPair = GetInstrumentPairFromInput(str(instrOrPairFromInputStr+'/'+otherInstrStr), isFxOption)
                compareWithCurr = instrPair.Instrument1().Name() if isForeign else instrPair.Instrument2().Name()
                currOrPairStr = instrOrPairFromInputStr if compareWithCurr == instrOrPairFromInputStr else instrPair.Name()
            else:
                currOrPairStr = instrOrPairFromInputStr
        except Exception as e:
            currOrPairStr = self.TransformToInstrumentPair(None, inputStr)
                
        if not currOrPairStr:
            currOrPairStr = currentInstr.Name() if currentInstr else None
        return currOrPairStr
    
    def TransformToForeignInstrument(self, name, inputStr):
        return self.FindCurrOrPairFromStr(self.foreignInstrument, self.domesticCurrency, inputStr, True, self.IsFxOption())
        
    def TransformToDomesticCurrency(self, name, inputStr):
        return self.FindCurrOrPairFromStr(self.domesticCurrency, self.foreignInstrument, inputStr, False, self.IsFxOption())
        
    def ChangeSignOnDeltaBasedOnCallPut(self, delta, isFlippedDelta = False):
        return delta
            
    def GetSolvedStrikeFromDelta(self, name, value): 
        value = value[:-1]
        if name in ['strikeDomesticPerForeign', 'solverStrikeDomPerFor', 'strike2DomesticPerForeign', 'solverStrike2DomPerFor']:
            topValue = 'quoteTradeCalcVal_deltaBSAlt' if self.PricingOptions().CurrentSaveIsAltQuoteTrade() else 'quoteTradeCalcVal_deltaBS'
        elif name in ['strikeForeignPerDomestic', 'solverStrikeForPerDom', 'strike2ForeignPerDomestic', 'solverStrike2ForPerDom']:
            topValue = 'flippedQuoteTradeCalcVal_deltaBSAlt' if self.PricingOptions().CurrentSaveIsFlippedAltQuoteTrade() else 'flippedQuoteTradeCalcVal_deltaBS'
        else:
            return getattr(self, name)
           
        solverParameter = GuiAttributeToSolverAttributeName(name)
        delta = ParseFloat(value, formatter=getattr(self, topValue))
        delta = self.ChangeSignOnDeltaBasedOnCallPut(delta, topValue.startswith('flipped'))

        solvedStrike = None
        if topValue in ['quoteTradeCalcVal_deltaBSAlt', 'flippedQuoteTradeCalcVal_deltaBSAlt']:
            solvedStrike = self.SolveStrikeForPremiumAdjustedDelta(solverParameter, topValue, delta)
        else:
            solvedStrike = self.Solve(topValue, solverParameter, delta)
            
        return solvedStrike
        
    
    def GetIntrinsicAttribute(self, name, isFwd):
        return 'intrinsicFwd' if isFwd else 'intrinsicSpot'
    
    def GetSolvedStrikeFromIntrinsic(self, name, value):
        intrinsicAttribute = self.GetIntrinsicAttribute(name, value[-1] == 'f')
        intrinsic = ParseFloat(value, formatter=getattr(self, intrinsicAttribute))
        if getattr(self, intrinsicAttribute) == None:
            return
        return self.Solve(intrinsicAttribute, GuiAttributeToSolverAttributeName(name), intrinsic)

    def IsPutOptionForSide(self, attrName):
        if Flipped(attrName):
            return self.IsQuoteCallOption()
        else:
            return not self.IsQuoteCallOption()
            
    def IsCallOptionForSide(self, attrName):
        return not self.IsPutOptionForSide(attrName)

    def TransformStrikePrice(self, name, value):
    
        if isinstance(value, str):
            value = value.lower()
            
        if value in ['atm', '*', 'atms', 's']:
            value = self.GetUnderlyingValue(name)
        elif value in ['atmf', 'f']:
            value = self.GetForwardValue(name)
        elif isinstance(value, str) and value.endswith('d'):
            value = self.GetSolvedStrikeFromDelta(name, value)
        elif isinstance(value, str) and (value.endswith('p') or value.endswith('pf')):
            value = self.GetSolvedStrikeFromIntrinsic(name, value)
        if not value:
            # Fallback
            value = self.CurrentSaveTrade().Instrument().StrikePrice()
        
        return value
        
    def UnsimulateAttributeValueImpl(self, attrName):
        value = self._storedPricingParameters.get(attrName)
        if value != None:
            bidAskMode = self.BidAskModeVol() if attrName.lower().find('volatility') != -1 else self.BidAskMode()
            value = value[0] if not bidAskMode else value[1]
            value = self._GetTransform(attrName)(value)
        self.SimulateCalculation(attrName, value)

    def UnsimulateAttributeValue(self, attrName):
        oppositeAttrName = self.GetOppositeSimulationAttribute(attrName)
        if oppositeAttrName:
            if oppositeAttrName in self._storedPricingParameters:
                self.UnsimulateAttributeValueImpl(attrName)
                attrName = oppositeAttrName
            else:
                self.UnsimulateAttributeValueImpl(oppositeAttrName)
        self.UnsimulateAttributeValueImpl(attrName)

    def TransformBidAskSplit(self, attrName, value):
        if isinstance(value, str):
            valueSplit = value.split('/')
            if len(valueSplit) == 2:
                v0 = valueSplit[0].replace(' ', '')
                v1 = valueSplit[1].replace(' ', '')
                if not v0:
                    self.RefreshLockedValue(attrName)
                    if not v1:
                        #Use unsimulated bid/ask value
                        value = 'ValueWillNotBeSet'
                    else:
                        val = self.GetValueToStore(attrName)
                        if IsBidAskValue(val):
                            val = val[0]
                        value = [val.Number() if hasattr(val, 'Number') else val, v1]
                elif not v1:
                    self.RefreshLockedValue(attrName)
                    val = self.GetValueToStore(attrName)
                    if IsBidAskValue(val):
                        val = val[1]
                    value = [v0, val.Number() if hasattr(val, 'Number') else val]
                else:
                    value = TransformDecimalPoints([v0, v1])
        return value
        
    def TransformBidAsk(self, attrName, value):
        if isinstance(value, str) and len(value.split('/')) == 2:
            self.bidAskMode = True
        if value in [None, ''] and not self.IsCalculationSimulated(attrName):
            oppositeAttrName = self.GetOppositeSimulationAttribute(attrName)
            if oppositeAttrName and self.IsCalculationSimulated(oppositeAttrName):
                self.UnsimulateAttributeValue(oppositeAttrName)
        return self.TransformBidAskSplit(attrName, value)
        
    def TransformPrice(self, attrName, value):
        value = self.TransformBidAsk(attrName, value)
        if not self._isSolverDealPackage and value != 'ValueWillNotBeSet':
            currentValue = GetFloatFromCalculation(getattr(self, attrName))
            value = TransformMagnitude(value, currentValue)
        return value
    
    def TransformPriceParse(self, attrName, value):
        value = self.TransformPrice(attrName, value)
        formatter = self.GetAttributeMetaData(attrName, 'formatter')()
        if formatter and hasattr(formatter, 'Parse'):
            value = formatter.Parse(value)
        return value
    
    def TransformVolatility(self, attrName, value):
        if value in ('', None):
            self.bidAskModeVol = self.bidAskMode
        elif isinstance(value, str) and len(value.split('/')) == 2:
            self.bidAskModeVol = True
        else:
            self.bidAskModeVol = False
        return self.TransformBidAskSplit(attrName, value)

    def AmountTransform(self, attrName, value):
        if not isinstance(value, basestring):
            return value
            
        if value.startswith( ('+', '-') ):
            sign = {'+':1, '-':-1}[value[0]]
        else:
            sign = -1 if getattr(self, attrName) < 0 else 1
            
        formatter = self.GetAttributeMetaData(attrName, 'formatter')()
        parsedValue = formatter.Parse(value)
            
        return sign * abs(parsedValue) if parsedValue else value

    def TransformToValidCurrency(self, attrName, value, *rest):
        if type(value) == types.StringType:
            curr = InstrumentFromStr(value, True)
            if curr != None:
                return curr
            else:
                return getattr(self, attrName)
        return value

    def TransformToValidFixingSource(self, attrName, value, *rest):
        if type(value) == types.StringType:
            source = FixingSourceFromString(value)
            if source != None:
                return source
            else:
                return getattr(self, attrName)
        return value

    def TransformToValidValGroup(self, attrName, value, *rest):
        if type(value) == types.StringType:
            valGroup = ValGroupFromString(value)
            if valGroup != None:
                return valGroup
            else:
                return getattr(self, attrName)
        return value
    
    '''*******************************************************
    * Formatter methods
    *******************************************************'''                    
    def StrikeFormatterCB(self, *args):
        return GetFXSpotForwardFormatter(self.foreignInstrument, self.domesticCurrency, False)
    
    def FXRateFormatterCB(self, attrName):
        return FXRateFormatter(self.foreignInstrument, self.domesticCurrency, Flipped(attrName))

    def FXRateFlipFormatterCB(self, attrName):
        formatter = FXRateInverseFormatter if self.IsDigital() else FXRateFormatter
        return formatter(self.foreignInstrument, self.domesticCurrency, self.saveTradeQuotation.endswith(self.domesticCurrency.Name()))

    def FXPointsFormatterCB(self, attrName):
        return FXPointsFormatter(self.foreignInstrument, self.domesticCurrency, Flipped(attrName))     
           
    def StrikeFormatterInverseCB(self, *args):
        return GetFXSpotForwardFormatter(self.foreignInstrument, self.domesticCurrency, True)
        
    def ForeignAmountFormatterCB(self, *args):
        return AmountFormatter(self.foreignInstrument)
        
    def DomesticAmountFormatterCB(self, *args):
        return AmountFormatter(self.domesticCurrency) 
    
    def SingleValueFormatterCB(self, *args):
        return SingleValueFormatter("Buy")

    '''*******************************************************
    * Label methods
    *******************************************************'''  
    def BuySellLabel(self, *args):
        return self.CurrentSaveTrade().BoughtAsString()
        
    def BuySellHeader(self, *args):
        return self.BuySellLabel()
        
    def QuoteQuotationPriceLabel(self, *args):
        '''
        IsDigital() due to avoid having labels in %curr notation for prices/strikes/etc.
        '''
        return QuotationLabel(self.QuoteTrade(), self.IsDigital())
  
    def DomesticCurrencyLabel(self, *args):
        return CurrencyLabel(True, self.IsQuoteCallOption())
       
    def ForeignCurrencyLabel(self, *args):
        return CurrencyLabel(False, self.IsQuoteCallOption())

    def StrikeDomPerForLabel(self, *args):
        return self.QuoteQuotationPriceLabel()
        
    def ForeignAmountLabel(self, *args):
        return self.QuoteTrade().Instrument().Underlying().Name()
        
    def DomesticAmountLabel(self, *args):
        return self.QuoteTrade().Instrument().StrikeCurrency().Name()
    
    def InverseQuoteQuotationLabel(self):
        return Inverse(self.QuoteQuotationPriceLabel()) if self.IsFxOption() else ""
    
    def StrikeForPerDomLabel(self, *args):
        return self.InverseQuoteQuotationLabel()
    
    def FXRateLabel(self, attrName):
        quote = self.InverseQuoteQuotationLabel() if Flipped(attrName) else self.QuoteQuotationPriceLabel()
        return quote
    
    def TheorValSaveTradeLabel(self, *args):
        return 'TheorVal' + CurrencyStrFromDV(self.saveTradeCalcVal_theorVal)
        
    def TheorValNoPremiumSaveTradeLabel(self, *args):
        return 'TheorVal Ins' + CurrencyStrFromDV(self.saveTradeCalcVal_theorVal)

    '''*******************************************************
    * Custom calculations methods
    *******************************************************''' 
    def IsPremiumAdjusted(self):
        return self.PricingOptions().CurrentSaveIsFlippedQuoteTrade() or self.PricingOptions().CurrentSaveIsAltQuoteTrade()
    
    def PremiumQuotedForeignTrade(self):
        return self.AltQuoteTrade() if self.IsPremiumAdjusted() else self.QuoteTrade()
        
    def PremiumQuotedDomesticTrade(self):
        return self.FlippedQuoteTrade() if self.IsPremiumAdjusted() else self.FlippedAltQuoteTrade()
        
    def CustomCalcLabel(self, *args):
        return '%s;%s' % (QuotationLabel(self.PremiumQuotedForeignTrade()), QuotationLabel(self.PremiumQuotedDomesticTrade()))
    
    def CustomCalcConfig(self, *args):
        return PriceGreekExcludeVolatilityMovement(None)
    
    def CustomCalcConfigFlipped(self, *args):
        return PriceGreekExcludeVolatilityMovement(None).Merge(DomesticColumnConfig(None))
        
    def GetCustomCalculation(self, attrName, columnName, flipped = None):
        if not columnName in self.customCalculations:
            raise DealPackageException('%s is not a valid custom calculation' % columnName)
        calcName = str(columnName).replace(' ', '_') + ('Flipped' if flipped else '')
        calc = self.GetCalculation(calcName)
        if not calc:
            calcObj = 'PremiumQuotedDomesticTrade' if flipped else 'PremiumQuotedForeignTrade'
            calcConfig = self.CustomCalcConfigFlipped if flipped else self.CustomCalcConfig
            self.CreateCalculation(calcName, '%s:FDealSheet:%s' % (calcObj, columnName), calcConfig)
            calc = self.GetCalculation(calcName)
        return calc   

    '''*******************************************************
    * Enabled methods
    *******************************************************''' 
    def AmountFieldDisabled(self, currency):
        return self.IsDigital() and self.payoutCurrency != currency
    
    def ForeignAmountEnabled(self, *args):
        return not self.AmountFieldDisabled(self.foreignInstrument)
        
    def DomesticAmountEnabled(self, *args):
        return not self.AmountFieldDisabled(self.domesticCurrency)
        
    def AtmVolatilityEnabled(self, *args):
        return self.valuationAddOnModel == 'Vanna Volga Pricing'

    '''*******************************************************
    * Solver methods
    *******************************************************'''    
    def VolatilityParam(self, *args):
        return {'minValue':1e-10, 'maxValue':1000, 'precision':0.0001}

    def StrikeParamDomPerFor(self, attributeName):
        # TODO: Create new BarrierParam where barrier boundery is not above/below strike depending on Down/Up (Tomas)
        fwdPrice = GetFloatFromCalculation(self.quoteTradeCalcVal_fwd, self.BuySellLabel()) if self.quoteTradeCalcVal_fwd else 1.0
        return GetMaxMinBounderiesStrikeSolving(fwdPrice)
        
    def StrikeParamForPerDom(self, attributeName):
        fwdPrice = GetFloatFromCalculation(self.flippedQuoteTradeCalcVal_fwd, self.BuySellLabel()) if self.flippedQuoteTradeCalcVal_fwd else 1.0
        return GetMaxMinBounderiesStrikeSolving(fwdPrice)
        
    def UndValParam(self, attrName):
        if attrName.startswith('flipped'):
            undValAttr = 'flippedQuoteTradeCalcVal_undVal'
        else:
            undValAttr = 'quoteTradeCalcVal_undVal'
        undVal = GetFloatFromCalculation(getattr(self, undValAttr), self.BuySellLabel()) or 1
        return {'minValue':0.3*undVal, 'maxValue':3.0*undVal, 'precision':0.001}

    '''*******************************************************
    * Deal Package Interface methods
    *******************************************************'''
    def OnInit(self):
        self._premiumCurrencyChoices = DealPackageChoiceListSource()
        self._foreignInstrumentChoices = DealPackageChoiceListSource()
        self._domesticCurrencyChoices = DealPackageChoiceListSource()
        self._mirrorPortfolioChoices = DealPackageChoiceListSource()
        self._counterpartyPrfSet = 'NoInput'
        self._updateDefaultStrike = False
        self._storedPricingParameters = {'quoteTradeCalcVal_undVal':None}#,
                                         #'quoteTradeCalcVal_interestRate':None,
                                         #'flippedQuoteTradeCalcVal_interestRate':None} 
                                         #'atmVolatility':None}
                                         
    def GetStoredPricingParameters(self, *args):
        return self._storedPricingParameters
    
    def OnSave(self, saveConfig):
        super(PairOptionsDealPackageBase, self).OnSave(saveConfig)
        if saveConfig.InstrumentPackage() == 'SaveNew':
            self.InstrumentPackage().Name('')
    
    def OnNew(self):
        self.SetSolverParameter(None, 'strikeDomesticPerForeign')
        self.SetDefaultStrike()
        self.SetRoundingSpecification(None, None, None, None)
        self.OverrideValuationGroup('Vanilla')

    def OnOpen(self):
        for t in self.DealPackage().Trades():
            if t.Trade().MirrorTrade() and t.MirrorPortfolio() != t.Trade().MirrorTrade().Portfolio():
                t.MirrorPortfolio(t.Trade().MirrorTrade().Portfolio())
            
        self.SetSolverParameter(None, 'strikeDomesticPerForeign')

    def OnCopy(self, originalDealPackage, anAspectSymbol):
        storedPricingParameters = originalDealPackage.GetAttribute('getStoredPricingParameters')()
        for attribute in self._storedPricingParameters:
            self._storedPricingParameters[attribute] = storedPricingParameters[attribute]
        self._RegisterAllObjectMappings()
        if str(anAspectSymbol) == 'solving':
            self.bidAskMode = False
        self.gridModelView = self._gridModelView_default()
        if str(anAspectSymbol) != 'solving':
            self.SetSolverParameter(None, 'strikeDomesticPerForeign')
            
        tradeTime = originalDealPackage.Trades().First().TradeTime()
        for t in self.PricingOptions().Trades():
            t.TradeTime(tradeTime)

    
    def GetDeltaTraitsList(self):
        return ['quoteTradeCalcVal_delta', 'flippedQuoteTradeCalcVal_delta']
    
    def IsVolatilitySimulated(self):
        return self.GetAttributeMetaData('volatility', 'isCalculationSimulated')()
    
    def SolverStrikeChanged(self, attribute, old, new, userInputTraitName):
        deltaTraits = self.GetDeltaTraitsList()
        if self.IsVolatilitySimulated() and self._isSolverDealPackage and self.solverTopValue in deltaTraits:
            self._calculationsRegistered = False
            self._RegisterAllCalculations()

    def OverrideValuationGroup(self, baseType):
        valuationGroupOverride = ValuationGroupOverride(baseType)
        if valuationGroupOverride:
            try:
                self.valGroup = valuationGroupOverride.ValuationGroup()
            except Exception as e:
                print ('Cannot set the Valuation Group Override', e)

    def MirrorPortfolioVisible(self, attributeName):
        counterparty = self.CurrentSaveTrade().Counterparty()
        return self.IsShowModeDetail() or self.Trade().MirrorPortfolio() or (counterparty and counterparty.OwnedPortfolios().Size())
        
    def MirrorPortfolioChoices(self, attributeName):
        if self._mirrorPortfolioChoices.IsEmpty():
            self.UpdateMirrorPortfolioChoices()
        return self._mirrorPortfolioChoices
        
    def UpdateMirrorPortfolioChoices(self, *args):
        self._mirrorPortfolioChoices.Clear()
        counterparty = self.CurrentSaveTrade().Counterparty()
        if counterparty:
            self._mirrorPortfolioChoices.AddAll(counterparty.OwnedPortfolios())
            
    def CounterpartyPortfolio(self, val = 'NoInput'):
        if val == 'NoInput':
            t = self.CurrentSaveTrade()
            if t.IsInfant():
                cptyPrf = t.MirrorPortfolio()
            if self._counterpartyPrfSet == 'NoInput':
                cptyPrf = t.MirrorTrade().Portfolio() if t.MirrorTrade() else None
            else:
                cptyPrf = self._counterpartyPrfSet
            return cptyPrf
        else:
            for t in self.PricingTrades():
                t.MirrorPortfolio(val)
            self._counterpartyPrfSet = val
