""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAFRADeal.py"
import acm
import re
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary

class AAFRADeal(object):
    def __init__(self, fra, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation, mtm):
        self.fra = fra
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation
        self.mtm = mtm
        
    def getAAFRADealString(self, staticLegInformation, tradeQuantity, parameterDict):
        leg = staticLegInformation.AcmLeg()
        discountMappingLink = leg.MappedDiscountLink()
        forwardMappingLink = leg.MappedForwardLink()
        notional = abs(staticLegInformation.NominalFactor() * tradeQuantity * self.fra.ContractSize())
        deal = AAComposer.PairList()
        deal["Object"] = "FRADeal"
        deal["Reference"] = Util.createAALabel(staticLegInformation.InstrumentId())
        deal["MtM"] = Util.getMtMValue(self.mtm)       
        deal["Currency"] = staticLegInformation.CurrencySymbol().AsString()
        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(discountMappingLink)
        deal["Interest_Rate"] = parameterDict.AddForwardCurveAndGetName(forwardMappingLink)
        deal["Principal"] = notional
        deal["Borrower_Lender"] = 'Lender' if tradeQuantity < 0 else 'Borrower'
        deal["FRA_Rate"] = str(leg.FixedRate())
        deal["Day_Count"] = Util.createDayCountString(leg.DayCountMethod())
        deal['Effective_Date'] = Util.createDateStringFromDateTime(self.fra.StartDate())
        deal['Maturity_Date'] = Util.createDateStringFromDateTime(self.fra.EndDate())
        return deal.compose()

    def get(self):
    
        deals = acm.FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        for staticLegInformation in self.staticLegInformations:
            for tradeDV in self.portfolioTradeQuantities:
                deals.Add(self.getAAFRADealString(staticLegInformation, tradeDV.Number(), parameterDict))
        returnDictionary = AAParameterDictionary.createReturnDictionary(deals, parameterDict)
        return returnDictionary
