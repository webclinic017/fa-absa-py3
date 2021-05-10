""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AABondFutureDeal.py"
import AAParamsAndSettingsHelper
import AAComposer
import AAParameterDictionary
import acm

import AAUtilFunctions as Util
import AADealsCreator

logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

class AABondFutureDeal(object):    
    def __init__(self, bondFuture, positionProjectedPayments, trades, valuationDate):
        self.bondFuture = bondFuture
        self.projectedPayments = positionProjectedPayments
        self.bond = bondFuture.Underlying() if bondFuture != None else None
        self.trades = trades
        self.valuationDate = valuationDate
        
    def __getBondFutureDeal(
            self, parameterDict, trade, 
            discountCurveName, repoCurveKey):

        tradeQuantity = trade.Quantity()
        buyNotSell = tradeQuantity < 0
        expiryDate = self.bondFuture.ExpiryDate()
        settleDate = self.bondFuture.SettlementDate()
        
        deal = AAComposer.PairList()
        deal["Object"] = "BondFuture"
        deal["Currency"] = self.bondFuture.Currency().Name()
        deal["Buy_Sell"] = Util.getBuySellFlag(buyNotSell)
        deal["Units"] = self.bondFuture.ContractSize()
        deal["Expiry_Date"] = Util.createDateStringFromDateTime(expiryDate)
        deal["Settlement_Date"] = Util.createDateStringFromDateTime(settleDate)
        deal["Contract"] = self.bondFuture.Name()
        deal["Contract_Size"] = tradeQuantity
        deal["Price"] = trade.Price()
        deal["Discount_Rate"] = discountCurveName
        deal["Repo_Rate"] = repoCurveKey
        if self.bond.Issuer():
            deal['Issuer'] = str(self.bond.Issuer().Name())
        return deal


    def get(self):
        discountLink = self.bondFuture.MappedDiscountLink()
        repoLink = self.bondFuture.MappedRepoLink(self.bondFuture.Currency())
        bondVolLink = self.bondFuture.MappedVolatilityLink();
        
        parameterDict = AAParameterDictionary.ParameterDictionary()
        discountCurveName = parameterDict.AddDiscountCurveAndGetName(discountLink)
        repoCurveName = parameterDict.AddRepoCurveAndGetName(repoLink)
        parameterDict.AddEquityVolatilityAndGetName(bondVolLink, self.bondFuture)
        
        deals = acm.FArray()

        for trade in self.trades:
            bondFutureDeal = self.__getBondFutureDeal(
                parameterDict, trade, discountCurveName, repoCurveName)
            deals.Add(bondFutureDeal.compose())
        
        AADealsCreator.AddFixedPaymentDeals(deals, parameterDict, self.projectedPayments)
        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)
