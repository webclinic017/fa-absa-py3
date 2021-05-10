""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACfInstrumentDealCapFloor.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import AACfInstrumentDeal
import acm

class CashFlowListEngineCapFloor(AACfInstrumentDeal.CashFlowListEngine):
    def AddCashFlowIfValid(self, cashFlowListDeal, cfInformation):
        if cfInformation.Type() not in ['Floorlet', 'Caplet']:
            return

        cflStrike = cfInformation.StrikePrice() * 100.0
        dealStrike =  cashFlowListDeal.strike
        if cflStrike != dealStrike:
            return
        if cfInformation.Type() == cashFlowListDeal.interestCashFlowType:
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, cashFlowListDeal.tradeQuantityDV.DateTime()):
                cashFlowListDeal.AddInterestCashFlow(cfInformation)
    
    def AppendInterestCashFlow(self, interestCashFlowList, cashFlowDictionary, cfInformation, valuationDate):
        interestCashFlowList.append(cashFlowDictionary)

class AACapFloorDeal(object):
    def __init__(self, capfloor, portfolioTradeQuantities, positionProjectedPayments, staticLegInformations, valuationDate, cfInformation, mtm):
        self.capfloor = capfloor
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.positionProjectedPayments = positionProjectedPayments
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation
        self.mtm = mtm
        self.is_cap = True if self.staticLegInformations[0].LegType() == 'Cap' else False
        
        
    def getAACapFloorDealString(self, parameterDict):
        leg = self.staticLegInformations[0].AcmLeg()
        discountMappingLink = leg.MappedDiscountLink()
        forwardMappingLink = leg.MappedForwardLink()
        volatilityMappingLink = leg.MappedVolatilityLink()
        
        tradeQuantity = self.portfolioTradeQuantities.At(0).Number()
        deal = AAComposer.PairList()
        deal["Object"] = "CapDeal" if self.is_cap else "FloorDeal"
        deal["Reference"] = Util.createAALabel(self.staticLegInformations[0].InstrumentId())
        deal["MtM"] = Util.getMtMValue(self.mtm)       
        deal["Currency"] = self.staticLegInformations[0].CurrencySymbol().AsString()
        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(discountMappingLink)
        deal["Forecast_Rate"] = parameterDict.AddDiscountCurveAndGetName(forwardMappingLink)
        deal["Forecast_Rate_Volatility"] = parameterDict.AddInterestRateVolatilityAndGetName(volatilityMappingLink)
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Effective_Date"] = Util.createDateStringFromDateTime(self.capfloor.StartDate())
        deal["Maturity_Date"] = Util.createDateStringFromDateTime(self.capfloor.ExpiryDate())
        deal["Payment_Interval"] = str(leg.RollingPeriod()).upper()
        deal["Reset_Frequency"] = str(leg.ResetPeriod()).upper()
        deal["Payment_Timing"] = "End"
        deal["Accrual_Day_Count"] = Util.createDayCountString(leg.DayCountMethod())
        deal["Index_Day_Count"] = Util.createDayCountString(leg.DayCountMethod())
                
        if self.is_cap:
            deal["Cap_Rate"] = leg.Strike()
        else:
            deal["Floor_Rate"] = leg.Strike()
                        
        deal["Index_Tenor"] = "6M" # Dummy value, not used but needed
        
        return deal.compose()
    
    def get(self):
        staticLegInformationCashFlowEngineDict = {}
        strike_rate = self.capfloor.AbsoluteStrike() / 100.0
        contract_size = self.capfloor.ContractSize()
        for staticLegInformation in self.staticLegInformations:
            staticLegInformationCashFlowEngineDict[staticLegInformation] = CashFlowListEngineCapFloor()
        (deals, parameterDict) = AADealsCreator.createAnyCashFlowInstrumentDealString(self.portfolioTradeQuantities, self.staticLegInformations, self.valuationDate, self.cfInformation, staticLegInformationCashFlowEngineDict = staticLegInformationCashFlowEngineDict, contractSize = contract_size, fixedRate = strike_rate)
        AADealsCreator.AddFixedPaymentDeals(deals, parameterDict, self.positionProjectedPayments)

        dealsXML = ''
        for deal in deals:
            dealsXML += '<Deal>' + deal + '</Deal>'
        wholeDealString = "<Properties>" + self.getAACapFloorDealString(parameterDict) + "</Properties><Deals>" + dealsXML + "</Deals>"
        returnDictionary = AAParameterDictionary.createReturnDictionary([wholeDealString], parameterDict)
        return returnDictionary
