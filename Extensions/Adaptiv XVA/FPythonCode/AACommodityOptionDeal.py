""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACommodityOptionDeal.py"
import acm

import AAComposer
from AAUtilFunctions import getBuySellFlag, createDateStringFromDateTime, getCallOrPutType, getMtMValue, getSettlementTypeFlag
import AAParameterDictionary
import AADataUtilFunctions as DataUtil


def _getRealizedFXAverage(resets):
    return 0.0


def createCommodityOptionDealString(option, trades, value_date, mtm):
    commodity = option.Underlying()

    
    pricing_parameters = AAParameterDictionary.ParameterDictionary()
    pricing_parameters.AddDiscountCurveAndGetName(commodity.Currency().MappedDiscountLink())
    pricing_parameters.AddFXVolatility(commodity.Currency(), option.Currency())
    
    commodity_name = pricing_parameters.AddCommodityPriceAndGetName(commodity)
    volatilityLink = commodity.MappedVolatilityLink()
    volatility_name = pricing_parameters.AddCommodityVolatilityAndGetName(volatilityLink, commodity)
    curve_name = pricing_parameters.AddDiscountCurveAndGetName(option.MappedDiscountLink())    
        
    
    contact_sz = option.ContractSizeInQuotation()
    deals = acm.FArray()
    for trade in trades:
        deal = AAComposer.PairList()
        deal["Object"] = "CommodityOptionDeal"
        deal["Reference"] = trade.Oid()
        deal["MtM"] = getMtMValue(mtm)
        deal["Currency"] = option.Currency().Name()
        deal["Discount_Rate"] = curve_name
        deal["Buy_Sell"] = getBuySellFlag(trade.Quantity() < 0)
        deal["Expiry_Date"] = createDateStringFromDateTime(option.ExpiryDate())
        deal["Units"] = abs(trade.Quantity() * contact_sz)
        deal["Option_Type"] = getCallOrPutType(option.IsCallOption())
        deal["Strike_Price"] = option.StrikePrice()
        deal["Option_On_Forward"] = 'No'
        deal["Settlement_Style"] = getSettlementTypeFlag(option.SettlementType())
        deal["Commodity"] = commodity_name
        deal["Commodity_Volatility"] = volatility_name
        deal["Payoff_Currency"] = option.Currency().Name()
        deal["Payoff_Type"] = 'Standard'

        deals.Add(deal.compose())

    return AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)
