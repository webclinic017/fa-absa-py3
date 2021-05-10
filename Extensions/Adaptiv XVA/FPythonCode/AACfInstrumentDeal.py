""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACfInstrumentDeal.py"
import AACashFlowCreator
import AAComposer
import AADataUtilFunctions as DataUtil
import AAUtilFunctions as Util
import acm

class CashFlowListDeal(object):
    # Abstract class
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, singleCfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None):
        mappingLink = staticLegInformation.AcmLeg().MappedDiscountLink()
        discountCurveName = parameterDict.AddDiscountCurveAndGetName(mappingLink)
        self.staticLegInformation = staticLegInformation
        self.legInformation = staticLegInformation.AcmLeg().LegInformation(valuationDate)
        self.valuationDate = valuationDate
        self.discountCurve = discountCurveName
        self.tradeQuantityDV = tradeQuantity
        self.singleCfInformation = singleCfInformation
        self.interestCashFlowList = AAComposer.CashFlowList()
        self.fixedCashFlowList = AAComposer.CashFlowList()
        self.cashFlowListEngine = cashFlowEngine
        self.buySell = buy_sell
        if contractSize:
            self.contractSize = contractSize # This parametrization is for the swaption implementation
        else:
            self.contractSize = staticLegInformation.ContractSize()
     
    def AppendToDealsArray(self, deals):
        self.FillCashFlowLists()
        if self.HasInterestCashFlows():
            interestDealDictionary = self.CreateInterestDealDictionary()
            deals.Add(interestDealDictionary.compose())
        if self.CreateSeperateDealForFixedAmounts() and self.HasFixedAmountCashFlows():
            fixedAmountDealDictionary = self.CreateFixedAmountDealDictionary()
            deals.Add(fixedAmountDealDictionary.compose())
    
    def CreateSeperateDealForFixedAmounts(self):
        return True
    
    def HasFixedAmountCashFlows(self):
        return (not self.fixedCashFlowList.is_empty())
        
    def HasInterestCashFlows(self):
        return (not self.interestCashFlowList.is_empty())
    
    def FillCashFlowLists(self):
        if self.singleCfInformation:
            self.cashFlowListEngine.AddCashFlowIfValid(self, self.singleCfInformation)
        else:
            cashFlowInformations = self.staticLegInformation.CashFlowInformations()
            for cashFlowInformation in cashFlowInformations:
                self.cashFlowListEngine.AddCashFlowIfValid(self, cashFlowInformation)

    def AddFixedAmountCashFlow(self, cfInformation):
        fixedAmountCfDictionary = AACashFlowCreator.createFixedAmountCashFlowDictionary(self.staticLegInformation, cfInformation, self.tradeQuantityDV)
        self.fixedCashFlowList.append(fixedAmountCfDictionary)
    
    def CreateFixedAmountCashFlowsListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Items"] = self.fixedCashFlowList
        return cashFlowsDictionary
    
    def CreateFixedAmountDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "CFFixedListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Buy_Sell"] = self.buySell if self.buySell else Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Cashflows"] = self.CreateFixedAmountCashFlowsListDictionary()
        return deal
    
    def CreateInterestDealDictionary(self):
        raise NotImplementedError("Not implemented")
    
    def AddInterestCashFlow(self, cfInformation):
        raise NotImplementedError("Not implemented")
            
            
class CashFlowListEngine(object):
    def AddCashFlowIfValid(self, cashFlowListDeal, cfInformation):
        if cfInformation.Type() == cashFlowListDeal.interestCashFlowType:
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, cashFlowListDeal.tradeQuantityDV.DateTime()):
                cashFlowListDeal.AddInterestCashFlow(cfInformation)
        elif cfInformation.Type() == "Fixed Amount":
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, cashFlowListDeal.tradeQuantityDV.DateTime()):
                cashFlowListDeal.AddFixedAmountCashFlow(cfInformation)
    
    def CalculateNotional(self, cashFlowListDeal, cfInformation, contractSize):
        return cfInformation.NominalFactor() * contractSize * cashFlowListDeal.tradeQuantityDV.Number() * cashFlowListDeal.staticLegInformation.NominalFactor()                  
    
    def AppendInterestCashFlow(self, interestCashFlowList, cashFlowDictionary, cfInformation, valuationDate):
        interestCashFlowList.append(cashFlowDictionary)


class FixedInterestDeal(CashFlowListDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, fixedRate, buy_sell = None):
        super(FixedInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        self.interestCashFlowType = "Fixed Rate"
        self.fixedRate = fixedRate # This parametrization is for the swaption implementation

    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Compounding"] = "No"
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary
    
    def CreateInterestDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "CFFixedInterestListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Buy_Sell"] = self.buySell if self.buySell else Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Cashflows"] = self.CreateInterestCashFlowListDictionary()
        return deal
    
    def AddInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        accrual_year_fraction = str(cfInformation.Period())
        fixed_rate = self.fixedRate if self.fixedRate else cfInformation.FixedRate()
        fixedRateCashFlowDictionary = AACashFlowCreator.createFixedRateCashFlowDictionary(cfInformation.PayDate(), notional, cfInformation.StartDate(), cfInformation.EndDate(), accrual_year_fraction, fixed_rate)
        self.cashFlowListEngine.AppendInterestCashFlow(self.interestCashFlowList, fixedRateCashFlowDictionary, cfInformation, self.valuationDate)

        
class CompoundingFixedInterestDeal(FixedInterestDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None):
        super(CompoundingFixedInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        self.interestCashFlowType = "Zero Coupon Fixed"
    
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Compounding"] = "Yes"
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary
    
    def AddInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        for startDate, endDate in zip(cfInformation.FixingStartDays(), cfInformation.FixingEndDays()):
            accrual_year_fraction = self.staticLegInformation.CalendarInformation().YearsBetween(startDate, endDate, self.staticLegInformation.DaycountMethod())
            fixedRateCashFlowDictionary = AACashFlowCreator.createFixedRateCashFlowDictionary(cfInformation.PayDate(), notional, acm.Time.DateFromTime(startDate), acm.Time.DateFromTime(endDate), accrual_year_fraction, cfInformation.FixedRate())
            self.cashFlowListEngine.AppendInterestCashFlow(self.interestCashFlowList, fixedRateCashFlowDictionary, cfInformation, self.valuationDate)            

class FixedAccretiveInterestDeal(FixedInterestDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None):
        super(FixedAccretiveInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        self.interestCashFlowType = "Fixed Rate Accretive"
    
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Compounding"] = "Yes"
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary
    
class FloatInterestDeal(CashFlowListDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None):
        super(FloatInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        mappingLink = staticLegInformation.AcmLeg().MappedForwardLink()
        self.forwardCurve = parameterDict.AddForwardCurveAndGetName(mappingLink)
        self.floatReferenceCalendar = self.staticLegInformation.FixingInformations()[0].CalendarInformation()
        self.interestCashFlowType = "Float Rate"
    
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        if self.staticLegInformation.ResetType() == "Single":
            cashFlowsDictionary["Compounding_Method"]   = "None"
        elif self.staticLegInformation.ResetType() == "Unweighted":
            cashFlowsDictionary["Compounding_Method"]   = "None"  
            cashFlowsDictionary["Averaging_Method"]     = "Average_Interest"
        elif self.staticLegInformation.ResetType() == "Weighted":
            cashFlowsDictionary["Compounding_Method"]   = "None"  
            cashFlowsDictionary["Averaging_Method"]     = "Average_Rate"
        elif self.staticLegInformation.ResetType() == "Compound":
            cashFlowsDictionary["Compounding_Method"]   = "Include_Margin"
            cashFlowsDictionary["Averaging_Method"]     = "Average_Rate"
        else:
            raise AssertionError("reset type %s not implemented" %str(self.staticLegInformation.ResetType()))
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary

    def CreateInterestDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "CFFloatingInterestListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Buy_Sell"] = self.buySell if self.buySell else Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Cashflows"] = self.CreateInterestCashFlowListDictionary()
        deal["Forecast_Rate"] = self.forwardCurve
        return deal

    def AddSingleResetInterestCashFlow(self, cfInformation):

        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        accrual_year_fraction = str(cfInformation.Period())
        reset_accrual_year_fraction = self.floatReferenceCalendar.YearsBetween(cfInformation.RateStartDay(0), cfInformation.RateEndDay(0), self.staticLegInformation.FixingDaycountMethod())
        fixedValue = 0.0 if str(cfInformation.FixingValues(self.legInformation)[0]).lower() == 'nan' else cfInformation.FixingValues(self.legInformation)[0]
        reset_list = "[" + AACashFlowCreator.createResetList(cfInformation.FixingDays()[0], cfInformation.RateStartDay(0), cfInformation.RateEndDay(0), reset_accrual_year_fraction, self.staticLegInformation.FixingEndPeriod(0), self.staticLegInformation.FixingDaycountMethod(), self.staticLegInformation.FixingRollingPeriod(0), fixedValue, cfInformation.FixingIsFixed(self.valuationDate)[0], fixedValue * 100) + "]"
        floatRateCashFlowDictionary = AACashFlowCreator.createFloatRateCashFlowDictionary(cfInformation.PayDate(), notional, cfInformation.StartDate(), cfInformation.EndDate(), accrual_year_fraction, reset_list, cfInformation.Spread())  
        self.cashFlowListEngine.AppendInterestCashFlow(self.interestCashFlowList, floatRateCashFlowDictionary, cfInformation, self.valuationDate)
        

    def AddWeightedResetInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        fixingRateStartDates = [cfInformation.RateStartDay(i) for i in range(0, cfInformation.FixingDays().Size())]
        fixingRateEndDates = [cfInformation.RateEndDay(i) for i in range(0, cfInformation.FixingDays().Size())]
        
        for startDate, endDate, estimateStartDate, estimateEndDate, date, value, fixing_is_fixed in zip(cfInformation.FixingStartDays(), cfInformation.FixingEndDays(), fixingRateStartDates, \
                fixingRateEndDates, cfInformation.FixingDays(), cfInformation.FixingValues(self.legInformation), cfInformation.FixingIsFixed(self.valuationDate)):
            reset_accrual_year_fraction = self.floatReferenceCalendar.YearsBetween(acm.Time.DateFromTime(estimateStartDate), acm.Time.DateFromTime(estimateEndDate), self.staticLegInformation.FixingDaycountMethod())
            accrual_year_fraction = self.staticLegInformation.CalendarInformation().YearsBetween(acm.Time.DateFromTime(startDate), acm.Time.DateFromTime(endDate), self.staticLegInformation.DaycountMethod())
            fixedValue = 0.0 if str(value).lower() == 'nan' else value
            reset_list = "[" + AACashFlowCreator.createResetList(acm.Time.DateFromTime(date), acm.Time.DateFromTime(estimateStartDate), acm.Time.DateFromTime(estimateEndDate), reset_accrual_year_fraction, self.staticLegInformation.FixingEndPeriod(0), self.staticLegInformation.FixingDaycountMethod(), self.staticLegInformation.FixingRollingPeriod(0), fixedValue, fixing_is_fixed, fixedValue * 100) + "]"
            floatRateCashFlowDictionary = AACashFlowCreator.createFloatRateCashFlowDictionary(acm.Time.DateFromTime(cfInformation.PayDate()), notional, acm.Time.DateFromTime(startDate), acm.Time.DateFromTime(endDate), \
                accrual_year_fraction, reset_list, cfInformation.Spread())
            self.cashFlowListEngine.AppendInterestCashFlow(self.interestCashFlowList, floatRateCashFlowDictionary, cfInformation, self.valuationDate)        
            
    def AddUnweightedResetInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        accrual_year_fraction = str(cfInformation.Period())
        reset_list = AAComposer.ResetList()
        fixingRateStartDates = [cfInformation.RateStartDay(i) for i in range(0, cfInformation.FixingDays().Size())]
        fixingRateEndDates = [cfInformation.RateEndDay(i) for i in range(0, cfInformation.FixingDays().Size())]

        for estimateStartDate, estimateEndDate, date, value, fixing_is_fixed in zip(fixingRateStartDates, \
                fixingRateEndDates, cfInformation.FixingDays(), cfInformation.FixingValues(self.legInformation), cfInformation.FixingIsFixed(self.valuationDate)):
            reset_accrual_year_fraction = self.floatReferenceCalendar.YearsBetween(acm.Time.DateFromTime(estimateStartDate), acm.Time.DateFromTime(estimateEndDate), self.staticLegInformation.FixingDaycountMethod())
            fixedValue = 0.0 if str(value).lower() == 'nan' else value
            single_reset = AACashFlowCreator.createResetList(acm.Time.DateFromTime(date), acm.Time.DateFromTime(estimateStartDate), acm.Time.DateFromTime(estimateEndDate), reset_accrual_year_fraction, self.staticLegInformation.FixingEndPeriod(0), self.staticLegInformation.FixingDaycountMethod(), self.staticLegInformation.FixingRollingPeriod(0), fixedValue, fixing_is_fixed, fixedValue * 100)
            reset_list.append(single_reset)
        floatRateCashFlowDictionary = AACashFlowCreator.createFloatRateCashFlowDictionary(cfInformation.PayDate(), notional, cfInformation.StartDate(), cfInformation.EndDate(), accrual_year_fraction, reset_list, cfInformation.Spread())  
        self.cashFlowListEngine.AppendInterestCashFlow(self.interestCashFlowList, floatRateCashFlowDictionary, cfInformation, self.valuationDate)
        
    def AddInterestCashFlow(self, cfInformation):
        if self.staticLegInformation.ResetType() == "Single":
            self.AddSingleResetInterestCashFlow(cfInformation)
        elif self.staticLegInformation.ResetType() == "Weighted" or self.staticLegInformation.ResetType() == "Compound":
            self.AddWeightedResetInterestCashFlow(cfInformation)
        elif self.staticLegInformation.ResetType() == "Unweighted":
            self.AddUnweightedResetInterestCashFlow(cfInformation)
        else:
            raise AssertionError("reset type %s not implemented" %str(self.staticLegInformation.ResetType()))

class CMSFloatInterestDeal(FloatInterestDeal):
    
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize): 
        super(CMSFloatInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize)
        volitilityLink = self.staticLegInformation.AcmLeg().MappedVolatilityLink()
        self.volitiliyCurve = parameterDict.AddInterestRateVolatilityAndGetName(volitilityLink)
        
        
    def CreateInterestDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "CFFloatingInterestListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Buy_Sell"] = Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Cashflows"] = self.CreateInterestCashFlowListDictionary()
        deal["Forecast_Rate"] = self.forwardCurve
        
        deal["Discount_Rate_Swaption_Volatility"] = self.volitiliyCurve
        deal["Forecast_Rate_Swaption_Volatility"] = self.volitiliyCurve
        return deal


class IndexLinkedInterestDeal(CashFlowListDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None): 
        super(IndexLinkedInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        self.interestCashFlowType = "Fixed Rate"
        self.compounding = None
        self.baseReferenceValue = staticLegInformation.InflationBaseValue()
        inflationLeg = staticLegInformation.AcmLeg()
        parameterDict.AddInflationLegAndGetName(inflationLeg)
        priceIndex = inflationLeg.InflationScalingRef()
        inflationMappingLink = priceIndex.MappedRepoLink(priceIndex.Currency())
        ycComponent = inflationMappingLink.Link().YieldCurveComponent()
        if ycComponent.IsKindOf("FSeasonalityCurve"):
            self.indexName = DataUtil.parameterName(ycComponent.UnderlyingCurve()) # TODO: Remove this dependency
        else:
            self.indexName = DataUtil.parameterName(ycComponent) # TODO: Remove this dependency
    
    def CreateSeperateDealForFixedAmounts(self):
        return False
    
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary
        
    def CreateInterestDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "YieldInflationCashflowListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Cashflows"] = self.CreateInterestCashFlowListDictionary()
        deal["Buy_Sell"] = self.buySell if self.buySell else Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Index"] = self.indexName
        return deal
       
    def AddInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        finalRefDate = cfInformation.InflationScalingDays()[0]
        finalRefValue = 0
        if cfInformation.InflationScalingsAreFixed(self.valuationDate):
            finalRefValue = cfInformation.InflationScalingValues(self.legInformation, self.valuationDate)[0].Number()
        accrual_start_date = cfInformation.StartDate()
        accrual_end_date = cfInformation.EndDate()
        accrual_year_fraction = cfInformation.Period()
        rate = cfInformation.FixedRate()
        margin = cfInformation.Spread()
        payment_date = cfInformation.PayDate()
        indexLinkedCashFlowDictionary = AACashFlowCreator.createIndexLinkedCashFlowDictionary(notional, self.baseReferenceValue, finalRefDate, finalRefValue, accrual_start_date, accrual_end_date, accrual_year_fraction, rate, margin, True, payment_date)
        self.interestCashFlowList.append(indexLinkedCashFlowDictionary)
         
    def AddFixedAmountCashFlow(self, cfInformation):
        notional = cfInformation.FixedAmount() * self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        finalRefDate = cfInformation.InflationScalingDays()[0]
        finalRefValue = 0
        if cfInformation.InflationScalingsAreFixed(self.valuationDate):
            finalRefValue = cfInformation.InflationScalingValues(self.legInformation, self.valuationDate)[0].Number()
        payment_date = cfInformation.PayDate()
        indexLinkedCashFlowDictionary = AACashFlowCreator.createIndexLinkedCashFlowDictionary(notional, self.baseReferenceValue, finalRefDate, finalRefValue, None, None, 1, 1.0, 0, False, payment_date)
        self.interestCashFlowList.append(indexLinkedCashFlowDictionary)

class FixedAccretiveIndexLinkedInterestDeal(IndexLinkedInterestDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None):
        super(FixedAccretiveIndexLinkedInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        self.interestCashFlowType = "Fixed Rate Accretive"
    
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary


class CapFloorBaseInterestDeal(CashFlowListDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(CapFloorBaseInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        fowardLink = staticLegInformation.AcmLeg().MappedForwardLink()
        self.forwardCurve = parameterDict.AddForwardCurveAndGetName(fowardLink)
        
        discountLink = staticLegInformation.AcmLeg().MappedDiscountLink()
        self.discountCurve = parameterDict.AddDiscountCurveAndGetName(discountLink)
        
        volitilityLink = staticLegInformation.AcmLeg().MappedVolatilityLink()
        self.volitiliyCurve = parameterDict.AddInterestRateVolatilityAndGetName(volitilityLink)
        
        self.floatReferenceCalendar = self.staticLegInformation.FixingInformations()[0].CalendarInformation()
        self.cflProperites = AAComposer.CashFlowList()
        self.stepStrike = stepStrike
        self.isCMS = False
        self.spread = staticLegInformation.Spread()
    
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        if self.staticLegInformation.ResetType() == "Single":
            cashFlowsDictionary["Compounding_Method"]   = "None"
        else:
            raise AssertionError("reset type %s not implemented" %str(self.staticLegInformation.ResetType()))
        
        cashFlowPropDictionary = self.CreatCashflowPropertiesDictionary()
        self.cflProperites.append(cashFlowPropDictionary)

        cashFlowsDictionary["Properties"] = self.cflProperites
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary

    def CreateInterestDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "CFFloatingInterestListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Buy_Sell"] = self.buySell if self.buySell else Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Cashflows"] = self.CreateInterestCashFlowListDictionary()
        deal["Discount_Rate"] = self.discountCurve
        deal["Forecast_Rate"] = self.forwardCurve
        if self.isCMS:
            deal["Discount_Rate_Swaption_Volatility"] = self.volitiliyCurve
            deal["Forecast_Rate_Swaption_Volatility"] = self.volitiliyCurve
        else:
            deal["Discount_Rate_Cap_Volatility"] = self.volitiliyCurve
            deal["Forecast_Rate_Cap_Volatility"] = self.volitiliyCurve
        return deal

    def CreatCashflowPropertiesDictionary(self):
        raise AssertionError("CreatCashflowPropertiesDictionary in base class not implemented")
    
    def AddSingleResetInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        accrual_year_fraction = str(cfInformation.Period())
        reset_accrual_year_fraction = self.floatReferenceCalendar.YearsBetween(cfInformation.RateStartDay(0), cfInformation.RateEndDay(0), self.staticLegInformation.FixingDaycountMethod())
        fixedValue = 0.0 if str(cfInformation.FixingValues(self.legInformation)[0]).lower() == 'nan' else cfInformation.FixingValues(self.legInformation)[0]
        reset_list = "[" + AACashFlowCreator.createResetList(cfInformation.FixingDays()[0], cfInformation.RateStartDay(0), cfInformation.RateEndDay(0), reset_accrual_year_fraction, self.staticLegInformation.FixingEndPeriod(0), self.staticLegInformation.FixingDaycountMethod(), self.staticLegInformation.FixingRollingPeriod(0), fixedValue, cfInformation.FixingIsFixed(self.valuationDate)[0], fixedValue * 100) + "]"
        floatRateCashFlowDictionary = AACashFlowCreator.createFloatRateCashFlowDictionary(cfInformation.PayDate(), notional, cfInformation.StartDate(), cfInformation.EndDate(), accrual_year_fraction, reset_list, 0)
        self.cashFlowListEngine.AppendInterestCashFlow(self.interestCashFlowList, floatRateCashFlowDictionary, cfInformation, self.valuationDate)
        
    def AddInterestCashFlow(self, cfInformation):
        if not cfInformation.IsCapFloorCashFlow():
            return
        if self.staticLegInformation.ResetType() == "Single":
            self.AddSingleResetInterestCashFlow(cfInformation)
        else:
            raise AssertionError("reset type %s not implemented" %str(self.staticLegInformation.ResetType()))

class CapInterestDealBase(CapFloorBaseInterestDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(CapInterestDealBase, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike, buy_sell)
        self.interestCashFlowType = "Caplet"
        self.strike = staticLegInformation.AcmLeg().Strike()
            
    def CreatCashflowPropertiesDictionary(self):
        props = AAComposer.CashFlowDataDictionary()
        strike = self.stepStrike if self.stepStrike else self.strike 
        strikeStr = (strike - self.spread) / 100.0
        props["Cap_Multiplier"] = "1"
        props["Cap_Strike"] = strikeStr
        
        props["Rate_Multiplier"] = 1
        props["Swap_Multiplier"] = 0
        props["Exponential_Multiplier"] = "100%"
        
        return props

class FloorInterestDealBase(CapFloorBaseInterestDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(FloorInterestDealBase, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike, buy_sell)
        self.interestCashFlowType = "Floorlet"
        floorStrike = staticLegInformation.AcmLeg().Strike2 ( ) 
        self.strike = floorStrike if floorStrike else staticLegInformation.AcmLeg(). Strike()
            

    def CreatCashflowPropertiesDictionary(self):
        props = AAComposer.CashFlowDataDictionary()
        strike = self.stepStrike if self.stepStrike else self.strike 
        strikeStr = (strike - self.spread) / 100.0      

        props["Floor_Multiplier"] = "1"
        props["Floor_Strike"] = strikeStr
        
        props["Rate_Multiplier"] = 1
        props["Swap_Multiplier"] = 0
        props["Exponential_Multiplier"] = "100%"
        
        return props

class CapInterestDeal(CapInterestDealBase):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(CapInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike, buy_sell)
        

class FloorInterestDeal(FloorInterestDealBase):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(FloorInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike, buy_sell)

class CMSCapInterestDeal(CapInterestDealBase):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(CMSCapInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike, buy_sell)
        self.isCMS = True
        

class CMSFloorInterestDeal(FloorInterestDealBase):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike = 0.0, buy_sell = None):
        super(CMSFloorInterestDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, stepStrike, buy_sell)
        self.isCMS = True


class EquitySwapletListDeal(CashFlowListDeal):
    def __init__(self, tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell = None): 
        super(EquitySwapletListDeal, self).__init__(tradeQuantity, staticLegInformation, valuationDate, cfInformation, parameterDict, cashFlowEngine, contractSize, buy_sell)
        self.interestCashFlowType = "Total Return"
        self.equity = parameterDict.AddEquityWithRepoCurveAndGetName(staticLegInformation.AcmLeg().FloatRateReference())
        
    def CreateInterestCashFlowListDictionary(self):
        cashFlowsDictionary = AAComposer.CashFlowDataDictionary()
        cashFlowsDictionary["Items"] = self.interestCashFlowList
        return cashFlowsDictionary
        
    def CreateInterestDealDictionary(self):
        deal = AAComposer.PairList()
        deal["Object"] = "EquitySwapletListDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformation.InstrumentId())
        deal["Equity"] = self.equity
        deal["Equity_Currency"] = self.staticLegInformation.AcmLeg().FloatRateReference().Currency().Name()
        deal["Currency"] = self.staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = self.discountCurve
        deal["Buy_Sell"] = self.buySell if self.buySell else Util.getBuySellFlag(self.staticLegInformation.PayLeg()) 
        deal["Cashflows"] = self.CreateInterestCashFlowListDictionary()
        return deal
       
    def AddInterestCashFlow(self, cfInformation):
        notional = self.cashFlowListEngine.CalculateNotional(self, cfInformation, self.contractSize)
        start_date = cfInformation.StartDate()
        end_date = cfInformation.EndDate()
        payment_date = cfInformation.PayDate()
        if end_date > payment_date:
            end_date = payment_date
            
        cfl = cashFlow = acm.FCashFlow[cfInformation.CashFlowNbr()]
        knownStartPrice = 0
        knownEndPrice = 0
        for reset in cashFlow.Resets():
            if reset.ResetType() != "Return":
                continue

            fixingValue = reset.FixingValue()
            if fixingValue == 0:
                continue
            day = reset.Day()

            if day < self.valuationDate and day <= start_date:
                knownStartPrice = fixingValue
                
            if day < self.valuationDate and day > start_date and day <= end_date:
                knownEndPrice = fixingValue
            
        trsCashFlowDictionary = AACashFlowCreator.createEquitySwapletCashFlowDictionary(notional, start_date, end_date, payment_date, knownStartPrice, knownEndPrice)
        self.interestCashFlowList.append(trsCashFlowDictionary)
