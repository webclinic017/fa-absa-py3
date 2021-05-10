""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACfInstrumentDealSwaption.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import AACfInstrumentDeal
import acm

class CashFlowListEngineSwaption(AACfInstrumentDeal.CashFlowListEngine):
    def __init__(self, tradeAcquireDate):
        self.tradeAcquireDate = tradeAcquireDate
        
    def AddCashFlowIfValid(self, cashFlowListDeal, cfInformation):
        if cfInformation.Type() == cashFlowListDeal.interestCashFlowType:
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, self.tradeAcquireDate):
                cashFlowListDeal.AddInterestCashFlow(cfInformation)
        elif cfInformation.Type() == "Fixed Amount":
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, self.tradeAcquireDate):
                cashFlowListDeal.AddFixedAmountCashFlow(cfInformation)        

    def CalculateNotional(self, cashFlowListDeal, cfInformation, contractSize):
        return abs(cfInformation.NominalFactor() * contractSize * cashFlowListDeal.tradeQuantityDV.Number() * cashFlowListDeal.staticLegInformation.NominalFactor())


class AASwaptionDeal(object):
    def __init__(self, swaption, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
        self.swaption = swaption
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation
        
        self.swap = self.swaption.Underlying()
        self.tradeAcquireDate = self.swap.SpotDateInverted(self.swap.CarryEndDate(self.swap, None, self.swaption.ExpiryDate()), None)

    def getGenericSwapMaturity(self):
        swapMaturityDate = None
        for staticLegInformation in self.staticLegInformations:
            cashFlowEndDates = staticLegInformation.ProjectedNonCouponCashFlows(self.valuationDate, staticLegInformation.AcmLeg().LegInformation(self.valuationDate), None, self.valuationDate)
            for cashFlowEndDate in cashFlowEndDates:
                dateTime = cashFlowEndDate.DateTime()
                if not swapMaturityDate or swapMaturityDate < dateTime:
                    swapMaturityDate = Util.createDateStringFromDateTime(dateTime)
        return swapMaturityDate

    def getAASwaptionDealString(self, parameterDict):
        payLeg = self.swap.PayLeg()
        recLeg = self.swap.RecLeg()
        discountMappingLink = self.swaption.MappedDiscountLink()
        forwardMappingLink = None
        if payLeg.IsFloatLeg():
            forwardMappingLink = payLeg.MappedForwardLink()
        else:
            forwardMappingLink = recLeg.MappedForwardLink()
        volatilityMappingLink = self.swaption.MappedVolatilityLink()

        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()
        deal = AAComposer.PairList()
        deal["Object"] = "SwaptionDeal"
        deal["Reference"] = Util.createAALabel(self.swaption.Name())        
        deal["Currency"] = self.swaption.Currency().Name()
        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(discountMappingLink)
        deal["Forecast_Rate"] = parameterDict.AddDiscountCurveAndGetName(forwardMappingLink)
        deal["Forecast_Rate_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(volatilityMappingLink)
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Payer_Receiver"] = Util.getPayerReceiverFlag(self.swaption.IsPutOption())
        deal["Option_Expiry_Date"] = Util.createDateStringFromDateTime(self.swaption.ExpiryDate())
        deal["Settlement_Date"] = Util.createDateStringFromDateTime(self.swaption.SettlementDate())
        
        if self.swap.Generic():
            deal["Swap_Maturity_Date"] = self.getGenericSwapMaturity()
        else:
            deal["Swap_Maturity_Date"] = Util.createDateStringFromDateTime(self.swap.maturity_date())
        deal["Swap_Effective_Date"] = Util.createDateStringFromDateTime(self.swaption.SettlementDate()) 
        deal["Pay_Frequency"] = payLeg.RollingPeriod()
        deal["Receive_Frequency"] = recLeg.RollingPeriod()
        deal["Swap_Rate"] = self.swaption.AbsoluteStrike()
        deal["Index_Tenor"] = "6M" # Dummy value, not used but needed
        deal["Settlement_Style"] = Util.getSettlementTypeFlag(self.swaption.SettlementType())        
        return deal.compose()
      
    def get(self):
        staticLegInformationCashFlowEngineDict = {}
        strike_rate = self.swaption.AbsoluteStrike() / 100.0
        option_contract_size = self.swaption.ContractSize()
        for staticLegInformation in self.staticLegInformations:
            staticLegInformationCashFlowEngineDict[staticLegInformation] = CashFlowListEngineSwaption(self.tradeAcquireDate)
        (deals, parameterDict) = AADealsCreator.createAnyCashFlowInstrumentDealString(self.portfolioTradeQuantities, self.staticLegInformations, self.valuationDate, self.cfInformation, staticLegInformationCashFlowEngineDict = staticLegInformationCashFlowEngineDict, contractSize = option_contract_size, fixedRate = strike_rate) 
        dealsXML = ''
        for deal in deals:
            dealsXML += '<Deal>' + deal + '</Deal>'
        wholeDealString = "<Properties>" + self.getAASwaptionDealString(parameterDict) + "</Properties><Deals>" + dealsXML + "</Deals>"
        returnDictionary = AAParameterDictionary.createReturnDictionary([wholeDealString], parameterDict)
        return returnDictionary
        
    @staticmethod
    def sameDiscountCurves(swaption):
        swap = swaption.Underlying()
        swaptionDiscountCurveStr = str(swaption.MappedDiscountLink().Link())
        swapDiscountCurveStr = str(swap.MappedDiscountLink().Link())
        return (swaptionDiscountCurveStr == swapDiscountCurveStr)        


class AABermudanSwaptionDeal(AASwaptionDeal):

    def getEvtString(self):
        evts = acm.FArray()
        for e in self.swaption.ExerciseEvents():
            evtString = AAComposer.PairList()
            evtString['Exercise_Date'] = Util.createDateStringFromDateTime(e.Date())
            evtString['Settlement_Date'] = Util.createDateStringFromDateTime(e.SettlementDate())
            evtString['Exercise_Fee'] = 0.0      
            evts.Add([evtString.compose()])
        return str(evts).replace(" ", "")

    def getAASwaptionDealString(self, parameterDict):
    
        payLeg = self.swap.PayLeg()
        recLeg = self.swap.RecLeg()
        discountMappingLink = self.swaption.MappedDiscountLink()
        forwardMappingLink = None
        if payLeg.IsFloatLeg():
            forwardMappingLink = payLeg.MappedForwardLink()
        else:
            forwardMappingLink = recLeg.MappedForwardLink()
        volatilityMappingLink = self.swaption.MappedVolatilityLink()

        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()
        notional = self.staticLegInformations[0].NominalFactor() * tradeQuantity * self.swaption.ContractSize()
        deal = AAComposer.PairList()
        deal["Object"] = "CallableStructuredDeal"
        deal["Reference"] = Util.createAALabel(self.swaption.Name())
        deal["Currency"] = self.swaption.Currency().Name()
        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(discountMappingLink)
        deal["Forecast_Rate"] = parameterDict.AddDiscountCurveAndGetName(forwardMappingLink)
        deal["Forecast_Rate_Swaption_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(volatilityMappingLink)
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Principal"] = notional
        payerReceiver = Util.getPayerReceiverFlag(self.swaption.IsPutOption())
        deal["Option_Type"] = "Put" if payerReceiver == "Receiver" else "Call"
        deal["Settlement_Style"] = Util.getSettlementTypeFlag(self.swaption.SettlementType())
        deal["Exercise_Dates"] = self.getEvtString()
        dealstr = deal.compose()
        return dealstr
        
    def get(self):
        staticLegInformationCashFlowEngineDict = {}
        option_contract_size = self.swaption.ContractSize()
        
        strike_rate = 0.0
        earliestExDay = None
        for e in self.swaption.ExerciseEvents():
            exerciseDate = e.Date()
            if self.valuationDate <= exerciseDate and (not earliestExDay or exerciseDate <= earliestExDay):
                strike_rate = e.Strike() / 100.0
                earliestExDay = exerciseDate
                continue
        
        deals = acm. FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        payerReceiver = Util.getPayerReceiverFlag(self.swaption.IsPutOption())
        for staticLegInformation in self.staticLegInformations:
            buy_sell = 'Sell' if staticLegInformation.LegType() ==  'Fixed' else 'Buy'
            staticLegInformationCashFlowEngineDict[staticLegInformation] = CashFlowListEngineSwaption(earliestExDay)
            AADealsCreator.createLegCashFlowInstrumentDealString(deals, parameterDict, self.portfolioTradeQuantities,
                    staticLegInformation, self.valuationDate, self.cfInformation, 
                    staticLegInformationCashFlowEngineDict = staticLegInformationCashFlowEngineDict, 
                    contractSize = option_contract_size, fixedRate = strike_rate, buySell = buy_sell)
            
        dealsXML = ''
        for deal in deals:
            dealsXML += '<Deal>' + deal + '</Deal>'
            
        wholeDealString = "<Properties>" + self.getAASwaptionDealString(parameterDict) + "</Properties><Deals>" + dealsXML + "</Deals>"
        returnDictionary = AAParameterDictionary.createReturnDictionary([wholeDealString], parameterDict)
        return returnDictionary

class AAXccySwaptionDeal(AASwaptionDeal):

    def getAASwaptionDealString(self, parameterDict):
        payLeg = self.swap.PayLeg()
        recLeg = self.swap.RecLeg()
        discountMappingLink = self.swaption.MappedDiscountLink()
        forwardMappingLink = None
        fixedLeg = None
        floatLeg = None
        if payLeg.IsFloatLeg():
            floatLeg = payLeg
            fixedLeg = recLeg
        else:
            floatLeg = recLeg
            fixedLeg = payLeg
        
        forwardMappingLink = floatLeg.MappedForwardLink()
        volatilityMappingLink = self.swaption.MappedVolatilityLink()
        
        instCurr = self.swaption.Currency().Name()
        
        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()

        fixed_Notional = 0
        float_Notional = 0 
        for staticLegInfo in self.staticLegInformations:
            if staticLegInfo.LegType() == "Fixed":
                fixed_Notional = staticLegInfo.NominalFactor() * tradeQuantity * self.swaption.ContractSize()
            else:
                float_Notional = staticLegInfo.NominalFactor() * tradeQuantity * self.swaption.ContractSize()
 
        deal = AAComposer.PairList()
        deal["Object"] = "SwaptionXccyDeal"
        deal["Reference"] = Util.createAALabel(self.swaption.Name())
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Settlement_Date"] = Util.createDateStringFromDateTime(self.swaption.SettlementDate())
        deal["Option_Expiry_Date"] = Util.createDateStringFromDateTime(self.swaption.ExpiryDate())
        deal["Swap_Maturity_Date"] = Util.createDateStringFromDateTime(self.swap.ExpiryDate())
        
        payerReceiver = Util.getPayerReceiverFlag(self.swaption.IsPutOption())
        deal["Payer_Receiver"] = payerReceiver
        deal["Swap_Rate"] = self.swaption.AbsoluteStrike() #Not Sure, this could be the swap's fixed rate.
        
        deal["Settlement_Style"] = Util.getSettlementTypeFlag(self.swaption.SettlementType())
        deal["Settlement_Currency"] = "Fixed" if fixedLeg.Currency().Name() == instCurr else "Floating"
        
        deal["Principal_Exchange"] = 'No'  #TODO
        deal["Variable_Principal"] = 'Float' #TODO
        deal["Fixed_Principal"] = fixed_Notional
        deal["Fixed_Currency"] = fixedLeg.Currency().Name()
        deal["Fixed_Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(fixedLeg.MappedDiscountLink())
        deal["Fixed_Frequency"] = Util.createDatePeriodString(fixedLeg.RollingPeriod())
        deal["Fixed_Day_Count"] = Util.createDayCountString(fixedLeg.DayCountMethod())
                
        deal["Float_Principal"] = float_Notional
        deal["Float_Currency"] = floatLeg.Currency().Name()
        deal["Float_Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(floatLeg.MappedDiscountLink())
        deal["Float_Frequency"] = Util.createDatePeriodString(floatLeg.RollingPeriod())
        deal["Float_Day_Count"] = Util.createDayCountString(floatLeg.DayCountMethod())
        
        deal["Fixed_Interest_Rate_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(
            self.swaption.MappedVolatilityLink(fixedLeg.Currency(), acm.GetDefaultContext().Oid(), None))
        deal["Float_Interest_Rate_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(
            self.swaption.MappedVolatilityLink(floatLeg.Currency(), acm.GetDefaultContext().Oid(), None))
                
        dealstr = deal.compose()
        return dealstr
    
    def get(self):
        deals = acm.FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        deals.Add(self.getAASwaptionDealString(parameterDict))
        returnDictionary = AAParameterDictionary.createReturnDictionary(deals, parameterDict)
        return returnDictionary    


class AAXccyBermudanSwaptionDeal(AASwaptionDeal):

    def getAASwaptionDealString(self, parameterDict):
        payLeg = self.swap.PayLeg()
        recLeg = self.swap.RecLeg()
        discountMappingLink = self.swaption.MappedDiscountLink()
        forwardMappingLink = None
        fixedLeg = None
        floatLeg = None
        if payLeg.IsFloatLeg():
            floatLeg = payLeg
            fixedLeg = recLeg
        else:
            floatLeg = recLeg
            fixedLeg = payLeg
        
        forwardMappingLink = floatLeg.MappedForwardLink()
        volatilityMappingLink = self.swaption.MappedVolatilityLink()
        
        instCurr = self.swaption.Currency().Name()
        
        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()

        fixed_Notional = 0
        float_Notional = 0 
        for staticLegInfo in self.staticLegInformations:
            if staticLegInfo.LegType() == "Fixed":
                fixed_Notional = staticLegInfo.NominalFactor() * tradeQuantity * self.swaption.ContractSize()
            else:
                float_Notional = staticLegInfo.NominalFactor() * tradeQuantity * self.swaption.ContractSize()
 
        deal = AAComposer.PairList()
        deal["Object"] = "DealSwaptionBermudanXccy"
        deal["Reference"] = Util.createAALabel(self.swaption.Name())
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        payerReceiver = Util.getPayerReceiverFlag(self.swaption.IsPutOption())
        deal["Payer_Receiver"] = payerReceiver
        deal["Settlement_Style"] = Util.getSettlementTypeFlag(self.swaption.SettlementType())
        deal["Settlement_Currency"] = "Fixed" if fixedLeg.Currency().Name() == instCurr else "Floating"
        deal["Fixed_Currency"] = fixedLeg.Currency().Name()
        deal["Float_Currency"] = floatLeg.Currency().Name()
        
        deal["Fixed_Interest_Rate"] = parameterDict.AddDiscountCurveAndGetName(fixedLeg.MappedDiscountLink())
        deal["Float_Interest_Rate"] = parameterDict.AddDiscountCurveAndGetName(floatLeg.MappedDiscountLink())
        
        deal["Fixed_Interest_Rate_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(
            self.swaption.MappedVolatilityLink(fixedLeg.Currency(), acm.GetDefaultContext().Oid(), None))
        deal["Float_Interest_Rate_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(
            self.swaption.MappedVolatilityLink(floatLeg.Currency(), acm.GetDefaultContext().Oid(), None))
        
        deal["Principal_Exchange"] = 'No' #TODO
        deal["Swap_Maturity_Date"] = Util.createDateStringFromDateTime(self.swaption.ExpiryDate())
        deal["Coupon_Frequency"] = Util.createDatePeriodString(fixedLeg.RollingPeriod()) 
        
        deal["Fixed_Day_Count"] = Util.createDayCountString(fixedLeg.DayCountMethod())
        deal["Float_Day_Count"] = Util.createDayCountString(floatLeg.DayCountMethod())
        
        deal["Swap_Rate"] = fixedLeg.FixedRate()
        deal["Variable_Principal"] = 'Float' #TODO
        
        deal["Fixed_Principal"] = fixed_Notional
        deal["Float_Principal"] = float_Notional
        
        firstExerciseDate = None
        lastExerciseDate = None
        for e in self.swaption.ExerciseEvents():
            exerciseDate = e.Date()
            if self.valuationDate <= exerciseDate and (not firstExerciseDate or exerciseDate <= firstExerciseDate):
                firstExerciseDate = exerciseDate
            
            if exerciseDate > lastExerciseDate and \
                Util.createDateStringFromDateTime(exerciseDate) < Util.createDateStringFromDateTime(self.swaption.ExpiryDate()):
                lastExerciseDate = exerciseDate
        
        if not firstExerciseDate: 
            firstExerciseDate = self.valuationDate
        deal["First_Exercise_Date"] = Util.createDateStringFromDateTime(firstExerciseDate)
        deal["Last_Exercise_Date"] = Util.createDateStringFromDateTime(lastExerciseDate)
 
        dealstr = deal.compose()
        return dealstr
    
    def get(self):
        deals = acm.FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        deals.Add(self.getAASwaptionDealString(parameterDict))
        returnDictionary = AAParameterDictionary.createReturnDictionary(deals, parameterDict)
        return returnDictionary    
