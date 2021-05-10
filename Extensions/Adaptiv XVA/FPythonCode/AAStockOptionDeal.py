""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAStockOptionDeal.py"
import AAParameterDictionary
import AAComposer
import AADealsCreator
import acm
import time
import AAUtilFunctions as Util

class AAStockOption(object):
    
    def __init__(self, option, positionProjectedPayments, positionTradeQuantities):
        self.option = option
        self.projectedPayments = positionProjectedPayments
        self.quantities = positionTradeQuantities
        
    def _getEquityOptionDeal(self, parameterDict, quantity):
        underlying = self.option.Underlying()
        discountLink = self.option.MappedDiscountLink()
        volatilityLink = self.option.MappedVolatilityLink()
        
        deal = AAComposer.PairList()
        deal["Object"] = "EquityOptionDeal"
        deal["Currency"] = self.option.Currency().Name()
        deal["Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(discountLink)
        deal["Buy_Sell"] = Util.getBuySellFlag(quantity.Value().Number() < 0)
        deal["Expiry_Date"] = Util.createDateStringFromDateTime(self.option.ExpiryDate())
        deal["Units"] =quantity.Value().Number() * self.option.ContractSize()
        deal["Option_Type"] = Util.getCallOrPutType(self.option.IsCallOption())
        deal["Strike_Price"] = self.option.StrikePrice()
        deal["Option_On_Forward"] = 'No'
        deal["Settlement_Style"] = 'Cash'
        deal["Option_Style"] = 'European'
        deal["Payoff_Currency"] = self.option.Currency().Name()
        deal["Payoff_Type"] = 'Standard'
        
        deal["Equity"] = parameterDict.AddEquityPriceAndGetName(underlying)
        deal["Equity_Volatility"] = \
            parameterDict.AddEquityVolatilityAndGetName(volatilityLink, underlying) \
            + "." + self.option.Currency().Name()
        return deal

    def createStockOption(self):
        # Create the class Parameter Dictionary to fill with relevant pricing parameters.
        parameterDict = AAParameterDictionary.ParameterDictionary()
        
        # Create an array to insert the trade equityOptionDeal strings.
        deals = acm.FArray()
        
        # Get the underlying of the option.
        underlying = self.option.Underlying()
        
        # repo curve for calculating forward price of the stock
        parameterDict.AddEquityWithRepoCurveAndGetName(underlying)
        
        # Add the expiry date of the option so that the correct amount of projected dividends are generated.
        expiryDate = parameterDict.AddDividendOptionExpiryDateAndGetDate(self.option.ExpiryDate())
        
        for tradeQuantity in self.quantities:
            equityOptionDeal = self._getEquityOptionDeal(parameterDict, tradeQuantity)
            deals.Add(equityOptionDeal.compose())

        AADealsCreator.AddFixedPaymentDeals(deals, parameterDict, self.projectedPayments)
        
        # When the equityOptionDeal trade strings have been created create the return dictonary.
        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)
