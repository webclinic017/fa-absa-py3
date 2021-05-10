""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACustomDealsCreator.py"
import AAParameterDictionary
import AAComposer
import acm
import AAUtilFunctions as Util

#the customer could define their own custom deal model if they need to
def CustomDealModelCall(instrument):
    return ''

def createEVOConstantModelCall(instrument, amount, portfolioTradeQuantities):

    # Create an array to insert the trade deal strings.
    deals = acm.FArray()
    
    evoAddOnAmount = 0.0
    try:
        evoAddAmount = instrument.AdditionalInfo().EVOAddOnAmount()
    except:
        evoAddAmount = 0.0

    parameterDict = AAParameterDictionary.ParameterDictionary()

    for tradeQuantity in portfolioTradeQuantities:
        # The AAComposer.PairList is a class which makes it easy to work with a deal in a form that resembles the AA studio deal properties window.
        deal = AAComposer.PairList()
        deal["Object"] = "DealEVOConstant"
        #deal["MtM"]=
        #deal["Tags"]=
        #deal["Description"]=
        deal["Amount"] = amount + evoAddAmount
        deal["Currency"] = instrument.Currency().Name()
        deal["Maturity_Date"] = Util.createDateStringFromDateTime(instrument.ExpiryDate())
        deals.Add(deal.compose())
    
    # When the deal trade strings have been created create the return dictonary.
    return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

    
# Create the custom marketdata string.
def createCustomMarketDataString(customPriceFactors):

# Create the price factor string according to the definition in Adaptiv Analytics, the empty string means no custom price factors have been supplied.
    return ''
