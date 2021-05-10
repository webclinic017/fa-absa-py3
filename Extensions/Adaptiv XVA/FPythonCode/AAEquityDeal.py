""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAEquityDeal.py"
import AAUtilFunctions as Util
import AADataUtilFunctions as DataUtil
import AAComposer
import AADealsCreator
import AAParameterDictionary
#import AACfInstrumentDeal
import acm

class AAEquityDeal(object):    
    def __init__(self, equity, positionProjectedPayments, positionTradeQuantities):
        self.equity = equity
        self.projectedPayments = positionProjectedPayments
        self.quantities = positionTradeQuantities

    def createStock(self):
        # Create the class Parameter Dictionary to fill with relevant pricing parameters.
        parameterDict = AAParameterDictionary.ParameterDictionary()

        # Create an array to insert the trade equityDeal strings.
        deals = acm.FArray()

        # Insert the stock in the parameter dictionary and get the AA compatible name
        parameterDict.AddEquityPriceAndGetName(self.equity)

        # Add the expiry date of the option so that the correct amount of projected dividends are generated.
        parameterDict.AddDividendOptionExpiryDateAndGetDate(acm.Time.DateToday())

        # When the price parameters have been fetched, construct the equityDeal string, loop over the number of trades in the instrument.
        for tradeQuantity in self.quantities:
            equityDeal = self.__getEquityDeal(tradeQuantity)
            deals.Add(equityDeal.compose())

        AADealsCreator.AddFixedPaymentDeals(deals, parameterDict, self.projectedPayments)

        AADealsCreator.AddFixedPaymentForDividendDeals(deals, parameterDict, self.projectedPayments)

        # When the equityDeal trade strings have been created create the return dictonary.
        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

    def __getEquityDeal(self, quantity):
        deal = AAComposer.PairList()
        deal["Object"] = "EquityDeal"
        deal["Currency"] = self.equity.Currency().Name()
        deal["Buy_Sell"] = Util.getBuySellFlag(quantity.Value().Number() < 0)
        deal["Units"] =quantity.Value().Number()
        deal["Equity"] = DataUtil.parameterName(self.equity)
        deal["Investment_Horizon"] = Util.createDateString(acm.Time.DateToday())

        return deal