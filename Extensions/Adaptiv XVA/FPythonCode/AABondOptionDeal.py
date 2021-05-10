""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AABondOptionDeal.py"
import AAParamsAndSettingsHelper
import AAComposer
import AAParameterDictionary
import acm

import AAUtilFunctions as Util


logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def bondYieldVolatilityName(bondName):
    undName = bondName.replace(' ', '_')
    rightLen = len(undName)
    if rightLen > 10:
        rightLen = 10
    return undName[:rightLen].upper()
    

def createBondOptionVolatilityString(option, modifiedDuration, volatility):
    underlying = option.Underlying()
    priceFactorName = bondYieldVolatilityName(underlying.Name())
    retVal = 'InterestYieldVol.{0},Property_Aliases=,Distribution_Type=Normal,Surface=[3,Flat,(0,0,0,{1})]'
    return retVal.format(priceFactorName, volatility / modifiedDuration)


class AABondOptionDeal(object):    
    def __init__(self, bondOption, positionProjectedPayments, positionTradeQuantities, valuationDate, cfInformation):
        self.bondOption = bondOption
        self.projectedPayments = positionProjectedPayments
        self.quantities = positionTradeQuantities
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation
        self.bond = bondOption.Underlying() if bondOption != None else None

    def __getBondOptionDeal(
            self, parameterDict, tradeQuantity, 
            discountCurveName, repoCurveKey, yieldVolName):
        
        buyNotSell = tradeQuantity.Value().Number() < 0
        bondLeg = self.bond.Legs()[0]
        bondMat = self.bond.maturity_date()
        dayCount = bondLeg.DayCountMethod()
        coupon1 = bondLeg.CashFlows()[0].PayDate()
        bondIssue = bondLeg.StartDate()
        expiryDate = self.bondOption.ExpiryDate()
        rollingPeriod = str(bondLeg.RollingPeriod()).upper()
        if (rollingPeriod == '12M' or rollingPeriod == '0D'):
            rollingPeriod = '1Y'

        deal = AAComposer.PairList()
        deal["Object"] = "BondOptionDeal"
        deal["Currency"] = self.bondOption.Currency().Name()
        deal["Discount_Rate"] = discountCurveName
        deal["Repo_Rate"] = repoCurveKey
        deal["Buy_Sell"] = Util.getBuySellFlag(buyNotSell)
        deal["Issue_Date"] = Util.createDateStringFromDateTime(bondIssue)
        deal["Bond_Maturity_Date"] = Util.createDateStringFromDateTime(bondMat)
        deal['Notional'] = self.bondOption.ContractSize() * tradeQuantity.Number()
        deal['Coupon_Interval'] = rollingPeriod
        deal['Coupon_Rate'] = str(bondLeg.FixedRate())
        deal['Accrual_Day_Count'] = Util.createDayCountString(dayCount)
        deal['First_Coupon_Date'] = Util.createDateStringFromDateTime(coupon1)
        if self.bond.Issuer():
            deal['Issuer'] = str(self.bond.Issuer().Name())
        deal['Option_Type'] = self.bondOption.OptionType()
        deal['Yield_Volatility'] = yieldVolName
        deal['Strike_Price'] = self.bondOption.StrikePrice()
        deal['Strike_Is_Clean'] = 'No'
        deal['Expiry_Date'] = Util.createDateStringFromDateTime(expiryDate)
        return deal


    def get(self):
        discountLink = self.bondOption.MappedDiscountLink()
        repoLink = self.bondOption.MappedRepoLink(self.bondOption.Currency())
        bondVolLink = self.bondOption.MappedVolatilityLink();
        
        parameterDict = AAParameterDictionary.ParameterDictionary()
        discountCurveName = parameterDict.AddDiscountCurveAndGetName(discountLink)
        repoCurveName = parameterDict.AddRepoCurveAndGetName(repoLink)
        parameterDict.AddEquityVolatilityAndGetName(bondVolLink, self.bondOption)
        
        yieldVolName = bondYieldVolatilityName(self.bond.Name())

        deals = acm.FArray()

        for tradeQuantity in self.quantities:
            bondOptionDeal = self.__getBondOptionDeal(
                parameterDict, tradeQuantity, discountCurveName, repoCurveName, yieldVolName)
            deals.Add(bondOptionDeal.compose())

        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

