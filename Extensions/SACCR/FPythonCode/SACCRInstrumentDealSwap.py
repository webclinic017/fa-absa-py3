""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRInstrumentDealSwap.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import acm

class SACCRSwapDeal(object):
    def __init__(self, swap, portfolioTradeQuantities, staticLegInformations, valuationDate, mtm, creditBalance, collateralAgreement):
        self.swap = swap
        self.name = self.swap.Name()
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.mtm = mtm
        self.payLeg = self.swap.PayLeg()
        self.recLeg = self.swap.RecLeg()
        self.creditbalance = creditBalance
        self.collateralAgreement = collateralAgreement
        
        self.fixedLeg = None
        self.floatLeg = None
        if self.payLeg.IsFloatLeg():
            self.floatLeg = self.payLeg
            self.fixedLeg = self.recLeg
        else:
            self.floatLeg = self.recLeg
            self.fixedLeg = self.payLeg
        
        self.forwardMappingLink = None
        if self.payLeg.IsFloatLeg():
            self.forwardMappingLink = self.payLeg.MappedForwardLink()
        else:
            self.forwardMappingLink = self.recLeg.MappedForwardLink()
        self.discountMappingLink = self.swap.MappedDiscountLink()
        
    
    def getSACCRSwapDealString(self, tradeQuantity, parameterDict):
        deal = AAComposer.PairList()
        deal["Object"] = "SwapInterestDeal"
        deal["Reference"] = Util.createAALabel(self.name)
        deal["MtM"] = Util.getMtMValue(self.mtm)
        if self.collateralAgreement:
            tags = self.creditbalance.Name() + ',0,Interest Rate,' + self.payLeg.Currency().Name() + ":" + self.recLeg.Currency().Name() + ",Swap,False"
        else:
            tags = '&lt;NONE&gt;,0,Interest Rate,' + self.payLeg.Currency().Name() + ":" + self.recLeg.Currency().Name() + ",Swap,False"
        deal["Tags"] = "[" + tags + "]"
        deal["Currency"] = self.swap.Currency().Name()
        deal["Effective_Date"] = Util.createDateString(self.swap.StartDate())
        deal["Maturity_Date"] = Util.createDateString(self.swap.EndDate())
        deal["Principal"] = self.payLeg.NominalFactor() * abs(tradeQuantity) * self.swap.ContractSize()
        deal["Pay_Rate_Type"] = Util.getLegType(self.payLeg.LegType())
        deal["Pay_Frequency"] = self.payLeg.RollingPeriod()
        deal["Pay_Timing"] = "End" if self.staticLegInformations[0].IsResetInArrear() else "Begin"
        deal["Pay_Day_Count"] = Util.createDayCountString(self.payLeg.DayCountMethod())
        deal["Pay_Roll_Direction"] = "Backward" if self.staticLegInformations[0].IsResetInArrear() else "Forward"
        deal["Receive_Frequency"] = self.recLeg.RollingPeriod()
        deal["Receive_Timing"] = "End" if self.staticLegInformations[1].IsResetInArrear() else "Begin"
        deal["Receive_Day_Count"] = Util.createDayCountString(self.recLeg.DayCountMethod())
        deal["Receive_Roll_Direction"] = "Backward" if self.staticLegInformations[1].IsResetInArrear() else "Forward"
        deal["Reset_Type"] = "Standard"
        deal["Index_Offset"] = "2"
        deal["Index_Day_Count"] = Util.createDayCountString(self.payLeg.DayCountMethod())
        deal["Swap_Rate"] = str(self.fixedLeg.FixedRate())
        deal["Index_Tenor"] = Util.createDatePeriodString(self.floatLeg.RollingPeriod()) 
        deal["Rate_Constant"] = "0%"
        deal["Compounding_Method"] = "None"

        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(self.discountMappingLink)
        deal["Interest_Rate"] = parameterDict.AddForwardCurveAndGetName(self.forwardMappingLink)
        
        return deal.compose()
        
    def getSACCRStructuredDealString(self, tradeQuantity):
        deal = AAComposer.PairList()
        deal["Object"] = "StructuredDeal"
        deal["Reference"] = Util.createAALabel(self.name)
        deal["MtM"] = Util.getMtMValue(self.mtm)
        if self.collateralAgreement:
            tags = self.creditbalance.Name() + ",0,Interest Rate," +  self.payLeg.Currency().Name() + ":" + self.recLeg.Currency().Name() + ",Swap,False"
        else:
            tags = "&lt;NONE&gt;,0,Interest Rate," +  self.payLeg.Currency().Name() + ":" + self.recLeg.Currency().Name() + ",Swap,False"
        deal["Tags"] = "[" + tags +"]"
        deal["Description"] = "Structured Deal" 
        deal["Currency"] = self.swap.Currency().Name()
        deal["Buy_Sell"] = Util.getBuySellFlag(tradeQuantity < 0)
        deal["Net_Cashflows"] = 'No'
        return deal.compose()
         
    def get(self):
        deals = acm.FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        for quantityDV in self.portfolioTradeQuantities:
            structuredSwap = "<Properties>" + self.getSACCRStructuredDealString(quantityDV.Number()) + "</Properties><Deals>" + \
               "<Deal><Properties>" + self.getSACCRStructuredDealString(quantityDV.Number()) + "</Properties><Deals><Deal>" + \
               self.getSACCRSwapDealString(quantityDV.Number(), parameterDict) + "</Deal></Deals></Deal></Deals>"
            deals.Add(structuredSwap)
        
        returnDictionary = AAParameterDictionary.createReturnDictionary(deals, parameterDict)
        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)
