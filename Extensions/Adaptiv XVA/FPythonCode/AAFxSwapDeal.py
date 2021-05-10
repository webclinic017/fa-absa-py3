""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAFxSwapDeal.py"
import AAComposer
import AAUtilFunctions as Util
import acm

class FxSwapDeal(object):    
    def __init__(self, trade, parameterDict):
        self.farTrade = trade
        self.parameterDict = parameterDict
        self.trade = trade.ConnectedTrade()
       
    def CreateDealDictionary(self):
        deal = AAComposer.PairList()
        discType                        = self.trade.DiscountingTypeForValuation()
        buyMappingLink                  = self.trade.Instrument().MappedMoneyMarketLink( discType, False )
        sellMappingLink                 = self.trade.Currency().MappedMoneyMarketLink( discType, False )
        buyDiscCurveName                = self.parameterDict.AddDiscountCurveAndGetName(buyMappingLink)
        sellDiscCurveName               = self.parameterDict.AddDiscountCurveAndGetName(sellMappingLink)
        deal["Object"]                  = "FXSwapDeal"
        deal["Reference"]               = str(self.trade.Oid())
        deal["Near_Buy_Far_Sell_Ccy"] = self.trade.Instrument().Name()
        deal["Near_Buy_Far_Sell_Discount_Rate"]       = buyDiscCurveName
        deal["Near_Sell_Far_Buy_Ccy"] = self.trade.Currency().Name()
        deal["Near_Sell_Far_Buy_Discount_Rate"]      = sellDiscCurveName
        deal["Near_Buy_Amount"]              = str(self.trade.Quantity())
        deal["Near_Sell_Amount"]             = str(-1.0 * self.trade.Premium())
        deal["Far_Buy_Amount"]              = str(self.farTrade.Premium())
        deal["Far_Sell_Amount"]             = str(-1.0 * self.farTrade.Quantity())
        deal["Near_Settlement_Date"]         = Util.createDateString(self.trade.AcquireDay())
        deal["Far_Settlement_Date"]         = Util.createDateString(self.farTrade.AcquireDay())
        return deal
    
    def CreateZeroDealDictionary(self):
        deal = AAComposer.PairList()
        trades = acm.FTrade.Select('connectedTrdnbr = ' + str(self.trade.Oid()))
        for trade in trades:
            if trade.Oid() != self.trade.Oid():
                self.trade = trade
        
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
        deal["Buy_Amount"]              = str(0.0)
        deal["Sell_Amount"]             = str(0.0)
        deal["Settlement_Date"]         = Util.createDateString(self.trade.AcquireDay())
        return deal

def createFxSwapDealDictionary(trade, parameterDict):
    fxSwap = FxSwapDeal(trade, parameterDict)
    return fxSwap.CreateDealDictionary()

def createZeroDealDictionary(trade, parameterDict):
    fxSwap = FxSwapDeal(trade, parameterDict)
    return fxSwap.CreateZeroDealDictionary()
