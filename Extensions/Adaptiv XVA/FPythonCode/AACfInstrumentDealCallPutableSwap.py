""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACfInstrumentDealCallPutableSwap.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import AACfInstrumentDeal
import acm
import AACfInstrumentDealCMSSwap

class AACfInstrumentDealCallPutableSwap(object):

    def __init__(self, swap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
        self.swap = swap
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation
        self.isCallOption = self.swap.Callable()
        self.isCMS = False
        for l in self.swap.Legs():
            if l.FloatRateReference() and l.FloatRateReference().IsKindOf("FSwap"):
                self.isCMS = True
        events = self.swap.ExerciseEvents()
        self.breakEvts = [e for e in events if e.Type() in ['Break', 'MandatoryBreak']]
        self.exerciseEvts = [e for e in events if e.Type() not in ['Break', 'MandatoryBreak']]
        
    def getBreakEvtString(self):
        if not self.breakEvts:
            return ""
        evts = []
        for e in self.breakEvts:
            evt = []
            evt.append(Util.createDateStringFromDateTime(e.Date()))
            evt.append(Util.createDateStringFromDateTime(e.SettlementDate()))
            evt.append(str(e.Strike()))
            evt.append("0")
            evt.append("")
            evt.append("Mutal")
            evtStr = "=".join(evt)+"\\"
            evts.append(evtStr)
        return "".join(evts)

    def getExerciseEvtString(self):
        if not self.exerciseEvts:
            return ""
        evts = acm.FArray()
        for e in self.exerciseEvts:
            evtString = AAComposer.PairList()
            evtString['Exercise_Date'] = Util.createDateStringFromDateTime(e.Date())
            evtString['Settlement_Date'] = Util.createDateStringFromDateTime(e.SettlementDate())
            evtString['Exercise_Fee'] = 0.0 
            evts.Add([evtString.compose()])
        return str(evts).replace(" ", "")

    def getAABreakClauseSwapDealString(self, parameterDict):
        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()
        deal = AAComposer.PairList()
        deal["Object"] = "StructuredDealBreakClause"
        deal["Reference"] = Util.createAALabel(self.swap.Name())        
        deal["Currency"] = self.swap.Currency().Name()
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Net_Cashflows"] = "No"
        deal["Break_Clause"] = self.getBreakEvtString()
        dealstr  = deal.compose()
        return dealstr 
        
    def getAACallPutableSwapDealString(self, parameterDict):
        payLeg = self.swap.PayLeg()
        recLeg = self.swap.RecLeg()
        discountMappingLink = self.swap.MappedDiscountLink()
        forwardMappingLink = None
        if payLeg.IsFloatLeg():
            forwardMappingLink = payLeg.MappedForwardLink()
        else:
            forwardMappingLink = recLeg.MappedForwardLink()
        volatilityMappingLink  = self.swap.MappedVolatilityLink( )

        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()
        deal = AAComposer.PairList()
        deal["Object"] = "CallableStructuredDeal"
        deal["Reference"] = Util.createAALabel(self.swap.Name())        
        deal["Currency"] = self.swap.Currency().Name()
        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(discountMappingLink)
        deal["Forecast_Rate"] = parameterDict.AddDiscountCurveAndGetName(forwardMappingLink)
        deal["Forecast_Rate_Swaption_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(volatilityMappingLink)
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Principal"] = self. swap. ContractSize( )
        deal["Option_Type"] = "Call" if self.isCallOption else "Put" 
        deal["Settlement_Style"] = "Embedded" 
        deal["Exercise_Dates"] = self.getExerciseEvtString()
        dealstr  = deal.compose()
        return dealstr 
        
    def get(self):
        staticLegInformationCashFlowEngineDict = {}
        option_contract_size = self.swap.ContractSize()
        
        deals = acm.FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        if self.isCMS:
            cmsSwap = AACfInstrumentDealCMSSwap.AACMSSwapDeal(self.swap, self.portfolioTradeQuantities, self.staticLegInformations, self.valuationDate, self.cfInformation) 
            for staticLegInformation in self.staticLegInformations:
                leg = staticLegInformation.AcmLeg()
                if leg.FloatRateReference() and leg.FloatRateReference().IsKindOf("FSwap"):
                    cmsSwap.createCMSLegDealString(deals, parameterDict, staticLegInformation)
                else:
                    AADealsCreator.createLegCashFlowInstrumentDealString(deals, parameterDict, self.portfolioTradeQuantities,
                        staticLegInformation, self.valuationDate, self.cfInformation)
        else:
            (deals, parameterDict) = AADealsCreator.createAnyCashFlowInstrumentDealString(self.portfolioTradeQuantities, self.staticLegInformations, self.valuationDate, self.cfInformation, contractSize = option_contract_size) 
            
        dealsXML = ''
        for deal in deals : 
            dealsXML += '<Deal>' + deal + '</Deal>'    
        
        wholeDealString = ''
        if self.breakEvts and self.exerciseEvts :
            breakStructureDealStr = self.getAABreakClauseSwapDealString(parameterDict)
            callableStructureDealStr = self.getAACallPutableSwapDealString(parameterDict)
            wholeDealString = "<Properties>" + breakStructureDealStr + "</Properties><Deals><Deal>" + callableStructureDealStr + "<Deals>" + dealsXML + "</Deals></Deal></Deals>"

        elif self.breakEvts or self.exerciseEvts:
            structureDealStr = ""
            if self.breakEvts:
                structureDealStr = self.getAABreakClauseSwapDealString(parameterDict)
            elif self.exerciseEvts: 
                structureDealStr = self.getAACallPutableSwapDealString(parameterDict)
            wholeDealString = "<Properties>" + structureDealStr + "</Properties><Deals>" + dealsXML + "</Deals>"

        returnDictionary = AAParameterDictionary.createReturnDictionary([wholeDealString], parameterDict)
        return returnDictionary
