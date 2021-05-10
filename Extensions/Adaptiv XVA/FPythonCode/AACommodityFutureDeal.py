""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACommodityFutureDeal.py"
import acm
import AAComposer
import AAUtilFunctions
import AAParameterDictionary

class FloatingEnergyDeal:
    def __init__(self, commodity):
        self.commodity = commodity
        self.sample_type = None
        self.commodity_name = None
        self.curve_name = None 

    def setCommodityParameters(self, pricing_parameters):
        commodity = self.commodity
        pricing_parameters.AddDiscountCurveAndGetName(commodity.Currency())
        volatilityLink = commodity.MappedVolatilityLink()
        
        self.commodity_name = pricing_parameters.AddCommodityPriceAndGetName(commodity)
        self.sample_type = commodity.Currency().Name().upper()
        
    def setTradeParameters(self, pricing_parameters, currency, discount_link):
        """
        The currency could change for commodity spot trades, so we need to 
        re-add currency parameters for every trade. 
        """
        pricing_parameters.AddDiscountCurveAndGetName(currency)
        if discount_link:
            pricing_parameters.AddDiscountCurveAndGetName(discount_link)

        link = self.commodity.MappedDiscountLink(currency, False, None)
        self.curve_name = pricing_parameters.AddDiscountCurveAndGetName(link)

    def _generatePayments(self, trade, settle_date, contract_sz):
        items = AAComposer.CashFlowDataDictionary()
        flows = AAComposer.CashFlowList()
    
        end_date = AAUtilFunctions.createDateStringFromDateTime(settle_date)
    
        r = AAComposer.CashFlowDataDictionary()
        r["Payment_Date"] = end_date
        r["Period_Start"] = end_date
        r["Period_End"] = end_date
        r["Volume"] = abs(trade.Quantity() * contract_sz)
        r["Fixed_Basis"] = trade.Price()
        r["Price_Multiplier"] = "1"
        r["Realized_Average_Date"] = ""
        r["Realized_Average"] = "0"
        r["FX_Period_Start"] = ""
        r["FX_Period_End"] = ""
        r["FX_Realized_Average"] = "0"

        flows.append(r)
        items["Items"] = flows
        
        return items

    def addDeal(self, deals, trade, currency, settle_date, mtm, contract_sz):
        deal = AAComposer.PairList()
        deal["Object"] = "FloatingEnergyDeal"
        deal["Reference"] = trade.Oid()
        deal["MtM"] = AAUtilFunctions.getMtMValue(mtm)
        deal["Currency"] = currency.Name()
        deal["Discount_Rate"] = self.curve_name
        deal["Sampling_Type"] = self.sample_type
        deal["FX_Sampling_Type"] = self.sample_type
        deal["Payer_Receiver"] = "Payer" if trade.Quantity() < 0.0 else "Receiver"
        deal["Average_FX"] = "No"
        deal["Payments"] = self._generatePayments(trade, settle_date, contract_sz)
        deal["Reference_Type"] = self.commodity_name
        deal["Reference_Volatility"] = self.commodity_name
        deal["Payoff_Currency"] = trade.Currency().Name()
        deals.Add(deal.compose())

def createCommodityFutureDealString(future, trades, value_date, mtm):
    deals = acm.FArray()
    pricing_parameters = AAParameterDictionary.ParameterDictionary() 

    currency = future.Currency()
    settle_date = future.ExpiryDate()
    contractSz =future.ContractSizeInQuotation()

    fwd_model = FloatingEnergyDeal(future.Underlying())
    fwd_model.setCommodityParameters(pricing_parameters)
    fwd_model.setTradeParameters(pricing_parameters, currency, future.MappedDiscountLink())
    
    for trade in trades:
        fwd_model.addDeal(deals, trade, currency, settle_date, mtm, contractSz)

    return AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)


def createCommodityDealString(commodity, trades, value_date, mtm):
    deals = acm.FArray()
    pricing_parameters = AAParameterDictionary.ParameterDictionary() 

    fwd_model = FloatingEnergyDeal(commodity)
    fwd_model.setCommodityParameters(pricing_parameters)
    contractSz =commodity.ContractSizeInQuotation()
    for trade in trades:
        fwd_model.setTradeParameters(pricing_parameters, trade.Currency(), None)
        fwd_model.addDeal(deals, trade, trade.Currency(), value_date, mtm, contractSz)

    return AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)
