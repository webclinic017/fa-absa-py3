""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAFxForwardDeal.py"
import AAComposer
import AAUtilFunctions as Util
import acm

class ForwardDateBasisFxDeal(object):    
    # TODO: Is it worth putting this in a class hierarchy with ForwardFxDeal?
    def __init__(self, trade, fxBaseCurrencyDiscountCurveMappingLink, parameterDict):
        self.trade = trade
        self.fxBaseCurrencyDiscountCurveMappingLink = fxBaseCurrencyDiscountCurveMappingLink
        self.parameterDict = parameterDict
    
    def CreateDealDictionary(self):
        deal = AAComposer.PairList()
        settlementDiscountCurveName     = self.parameterDict.AddDiscountCurveAndGetName(self.fxBaseCurrencyDiscountCurveMappingLink)
        settlementCurrency              = str(self.fxBaseCurrencyDiscountCurveMappingLink.Link().YieldCurveComponent().Currency().Name())
        deal["Object"]                  = "FXNonDeliverableForward"
        deal["Reference"]               = str(self.trade.Oid())
        deal["Buy_Currency"]            = self.trade.Instrument().Name()
        deal["Sell_Currency"]           = self.trade.Currency().Name()
        deal["Buy_Amount"]              = str(self.trade.Quantity())
        deal["Sell_Amount"]             = str(-1.0 * self.trade.Premium())
        deal["Settlement_Date"]         = Util.createDateString(self.trade.AcquireDay())
        deal["Settlement_Currency"]     = settlementCurrency
        deal["Discount_Rate"]           = settlementDiscountCurveName
        return deal

class ForwardFxDeal(object):    
    def __init__(self, trade, parameterDict):
        self.trade = trade
        self.parameterDict = parameterDict
    
    def CreateDealDictionary(self):
        deal = AAComposer.PairList()
        discType                        = self.trade.DiscountingTypeForValuation()
        buyMappingLink                  = self.trade.Instrument().MappedMoneyMarketLink( discType, False )
        sellMappingLink                 = self.trade.Currency().MappedMoneyMarketLink( discType, False )
        buyDiscCurveName                = self.parameterDict.AddDiscountCurveAndGetName(buyMappingLink)
        sellDiscCurveName               = self.parameterDict.AddDiscountCurveAndGetName(sellMappingLink)
        deal["Object"]                  = "FXForwardDeal"
        deal["Reference"]               = str(self.trade.Oid())
        deal["Buy_Currency"]            = self.trade.Instrument().Name()
        deal["Buy_Discount_Rate"]       = buyDiscCurveName
        deal["Sell_Currency"]           = self.trade.Currency().Name()
        deal["Sell_Discount_Rate"]      = sellDiscCurveName
        deal["Buy_Amount"]              = str(self.trade.Quantity())
        deal["Sell_Amount"]             = str(-1.0 * self.trade.Premium())
        deal["Settlement_Date"]         = Util.createDateString(self.trade.AcquireDay())
        return deal
    
def createFxForwardDateBasisDealDictionary(trade, fxBaseCurrencyDiscountCurveMappingLink, parameterDict):
    fxForward = ForwardDateBasisFxDeal(trade, fxBaseCurrencyDiscountCurveMappingLink, parameterDict)
    return fxForward.CreateDealDictionary()

def createFxForwardDealDictionary(trade, parameterDict):
    fxForward = ForwardFxDeal(trade, parameterDict)
    return fxForward.CreateDealDictionary()
