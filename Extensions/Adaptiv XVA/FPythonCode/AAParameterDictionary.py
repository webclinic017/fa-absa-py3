""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAParameterDictionary.py"
import acm 
import AADataUtilFunctions as DataUtil
import AAUtilFunctions as Util

TYPE_FX_VOLATILITY = "FXVol"

TYPE_IR_VOLATILITY = "IRVolatility"

dealStringKey = acm.FSymbol('DealString')

parametersKey = acm.FSymbol('Parameters')

interestRateKey = acm.FSymbol('InterestRate')
equityKey = acm.FSymbol('Equity')
commodityKey = acm.FSymbol('Commodity')
inflationKey = acm.FSymbol('Inflation')

marketPriceKey = acm.FSymbol('MarketPrice')
volatilityKey = acm.FSymbol('Volatility')
# Interest Rate specific
curvesKey = acm.FSymbol('Curves')
discountCurveKey = acm.FSymbol('DiscountCurve')
forwardCurveKey = acm.FSymbol('ForwardCurve')
repoCurveKey = acm.FSymbol('RepoCurve')

dividendKey = acm.FSymbol('Dividend')

# Inflation specific
inflationLegKey = acm.FSymbol('InflationLeg')

customDataKey = acm.FSymbol('Custom')

class ParameterDictionary():
    def __init__(self, dict = None):
    
        if dict:
            self.dict = dict
        else:
            dict = {}    
            dict[interestRateKey] = {}
            dict[interestRateKey][curvesKey] = {}
            dict[interestRateKey][curvesKey][discountCurveKey] = acm.FSet()
            dict[interestRateKey][curvesKey][forwardCurveKey] = acm.FSet()
            dict[interestRateKey][curvesKey][repoCurveKey] = acm.FSet()
            dict[interestRateKey][volatilityKey] = acm.FSet()
            dict[equityKey] = {}
            dict[equityKey][marketPriceKey] = {}
            dict[equityKey][marketPriceKey][discountCurveKey] = {}
            dict[equityKey][marketPriceKey][repoCurveKey] = {}
            dict[commodityKey] = {}
            dict[inflationKey] = {}
            self.dict = dict
        
    def AddForwardCurveAndGetName(self, forwardCurve):
        self.dict[interestRateKey][curvesKey][forwardCurveKey].Add(forwardCurve)
        return DataUtil.getPriceFactorName(forwardCurve)
        
    def AddDiscountCurveAndGetName(self, discountCurve):
        self.dict[interestRateKey][curvesKey][discountCurveKey].Add(discountCurve)
        return DataUtil.getPriceFactorName(discountCurve)

    def AddRepoCurveAndGetName(self, repoCurve):
        self.dict[interestRateKey][curvesKey][repoCurveKey].Add(repoCurve)
        return DataUtil.getPriceFactorName(repoCurve)
        
    def AddInterestRateVolatilityAndGetName(self, IRvolatility):
        self.dict[interestRateKey][volatilityKey].Add(IRvolatility)
        return DataUtil.getPriceFactorName(IRvolatility)
    
    def AddEquityVolatilityAndGetName(self, equityVolatility, equity):
        self.dict[equityKey][volatilityKey] = equityVolatility
        return DataUtil.parameterName(equity)
        
    def AddCommodityVolatilityAndGetName(self, commodityVolatility, commodity): 
        self.dict[commodityKey][volatilityKey] = commodityVolatility
        return DataUtil.parameterName(commodity)
        
    def AddEquityPriceAndGetName(self, equityPrice):
        self.AddDiscountCurveAndGetName(equityPrice.MappedDiscountLink())
        self.dict[equityKey][marketPriceKey][discountCurveKey] = equityPrice
        return DataUtil.parameterName(equityPrice)

    def AddEquityWithRepoCurveAndGetName(self, equityObject):
        repoCurve = self.AddForwardCurveAndGetName(equityObject.MappedRepoLink(equityObject.Currency()))
        self.dict[equityKey][marketPriceKey][repoCurveKey] = equityObject
        return DataUtil.parameterName(equityObject)
    
    def AddCommodityPriceAndGetName(self, commodityPrice):
        self.AddDiscountCurveAndGetName(commodityPrice.MappedDiscountLink())
        self.dict[commodityKey][marketPriceKey] = commodityPrice
        return DataUtil.getPriceFactorName(commodityPrice)
        
    def AddInflationLegAndGetName(self, inflationLeg):
        self.dict[inflationKey][inflationLegKey] = inflationLeg
        return DataUtil.getPriceFactorName(inflationLeg)
    
    def AddDividendOptionExpiryDateAndGetDate(self, date):
        self.dict[dividendKey] = date
        return Util.createDateStringFromDateTime(date)
        
    def AddCustomMarketData(self, customMarketData):
        self.dict[customDataKey] = customMarketData

    def AddFXVolatility(self, ccy1, ccy2):
        # This is the rule that is built into Adaptiv.
        if ccy2.Name() < ccy1.Name():
            ccy_temp = ccy1
            ccy1 = ccy2
            ccy2 = ccy_temp

        name = "%s.%s" % (ccy1.Name(), ccy2.Name())        
                
        return name

    def AddFXOptionVolatility(self, fx_option):
        ccy1 = fx_option.StrikeCurrency()
        ccy2 = fx_option.Underlying()
        return self.AddFXVolatility(ccy1, ccy2)
        
    def GetDictionary(self):
        return self.dict

def createReturnDictionary(dealString, parameterDictionary):
    dict = {}
    dict[dealStringKey] = dealString
    dict[parametersKey] = parameterDictionary.GetDictionary()
    return dict
