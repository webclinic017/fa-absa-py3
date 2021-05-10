""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAFxOptionDeal.py"
import acm

from AAComposer import PairList 
from AAUtilFunctions import getBuySellFlag, createDateStringFromDateTime, getCallOrPutType, createAALabel, getMtMValue
import AAParameterDictionary 
from AADataUtilFunctions import getMappedFXDiscountLinkFromPair
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

DIRECTION_UP = 1
DIRECTION_DOWN = -1
DIRECTION_DOUBLE = 0

class AABarrier():
    def __init__(self, exotic):
        self._exotic = exotic
        self._crossed = False
        self._direction = DIRECTION_UP
        self._knock_in = True
        self._digital = False
        
        if str(exotic.BarrierCrossedStatus()) != "None":
            self._crossed = True
            
        if str(exotic.DigitalBarrierType()) != "None":
            self._digital = True

        barrier_type = str(exotic.BarrierOptionType())
        if barrier_type.startswith("Down"):
            self._direction = DIRECTION_DOWN
        elif barrier_type.startswith("Double"):
            self._direction = DIRECTION_DOUBLE
            
        if barrier_type.endswith("Out"):
            self._knock_in = False
    
    def isKnockedOut(self):
        if self._crossed:
            if not self._knock_in:
                return True
            
            if self._digital:
                return True
        
        return False
    
    def isKnockedIn(self):
        if self._crossed and self._knock_in:
            return True
        
        return False

    def isDigital(self):
        return self._digital
    
    def getAAType(self, invert_direction=False):
        barrier_type = "In" if self._knock_in else "Out"
        
        direction = "Up"
        if invert_direction:
            if self._direction == DIRECTION_UP:
                direction = "Down"
        else: 
            if self._direction == DIRECTION_DOWN:
                direction = "Down"
        
        if self._direction == DIRECTION_DOUBLE:
            return "Knock_%s" % (barrier_type)          

        if self.isDigital():
            return direction
        
        return "%s_And_%s" % (direction, barrier_type)      

    def doubleBarrier(self):
         return self._exotic.DoubleBarrier()
     
    
def isOptionKnockedOut(barrier):
    return barrier.isKnockedOut()

def isOptionDigital(barrier):
    return barrier.isDigital()
    
def isOptionDoubleBarriers(barriers):
    return barrier.isDouble()
    
def getAABarriers(option):
    barriers = []
    for exotic in option.Exotics():
        barrierType = str(exotic.BarrierOptionType())
        if barrierType not in ["None", "Custom"]:
            barrier = AABarrier(exotic)
            barriers.append(barrier)
        else:
            acm.Log("Barrier type %s on Instrument %s "
"currently is not supported." % (barrierType, option.Name()))
            logger.LOG("Barrier type %s on Instrument %s "
"currently is not supported." % (barrierType, option.Name()))

    if len(barriers) > 1:
        acm.Log("Instrument %s has more than one barrier. "
"Only one barrier is currently supported." % option.Name())
        logger.LOG("Instrument %s has more than one barrier. "
"Only one barrier is currently supported." % option.Name())

    return barriers

class FxOptionDeal(object):
    def __init__(self, option, portfolioTradeQuantities, valuationDate, mtm):
        self.option = option
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.valuationDate = valuationDate
        self.mtm = mtm
        
        underlying = self.option.Underlying()
        self.ccy = self.option.StrikeCurrency()
        self.fxBaseCurrencyDiscountCurveMappingLink = getMappedFXDiscountLinkFromPair(underlying, self.option.StrikeCurrency())
        self.strike = 1/self.option.StrikePrice() if self.option.StrikeQuotation().Name() == 'Per Unit Inverse' else self.option.StrikePrice()
        
    def get(self):
        barriers = getAABarriers(self.option)
        if barriers:
            if self.option.IsDoubleBarrier():
                return self.createDoubleBarrierFXOption(barriers[0])
    
            return self.createBarrierFXOption(barriers[0])
        else:
            return self.createVanillaFXOption()

   
    def createVanillaFXOption(self):
        underlying = self.option.Underlying()
        name = self.option.Name()
        pricing_parameters = AAParameterDictionary.ParameterDictionary()
        deals = acm.FArray()
        curve_name = pricing_parameters.AddDiscountCurveAndGetName(self.fxBaseCurrencyDiscountCurveMappingLink)
        
        volatility_name = pricing_parameters.AddFXOptionVolatility(self.option)
        pricing_parameters.AddDiscountCurveAndGetName(underlying.MappedDiscountLink())
                
        for quantityDV in self.portfolioTradeQuantities:
            quantity =  quantityDV.Number()      
            deal = PairList()
            deal["Object"] = "FXOptionDeal"
            deal["Reference"] = createAALabel(name)
            deal["MtM"] = getMtMValue(self.mtm)
            deal["Tags"] = ""
            deal["Currency"] = self.ccy.Name()
            deal["Underlying_Currency"] = underlying.Name()
            deal["Discount_Rate"] = curve_name
            deal["Buy_Sell"] = getBuySellFlag(quantity < 0)
            deal["Expiry_Date"] = createDateStringFromDateTime(self.option.ExpiryDate())
            deal["Underlying_Amount"] = abs(quantity)
            deal["Option_Type"] = getCallOrPutType(self.option.IsCallOption())
            deal["Strike_Price"] = self.strike 
            deal["Option_On_Forward"] = "No"
            deal["Settlement_Style"] = "Cash"
            deal["Option_Style"] = self.option.ExerciseType()
            deal["FX_Volatility"] = volatility_name

            deals.Add(deal.compose())
        return AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)

    def createBarrierFXOption(self, barrier):
        underlying = self.option.Underlying()
        #ccy = self.option.StrikeCurrency()
        name = self.option.Name()
        pricing_parameters = AAParameterDictionary.ParameterDictionary()
        deals = acm.FArray()
        curve_name = pricing_parameters.AddDiscountCurveAndGetName(self.fxBaseCurrencyDiscountCurveMappingLink)
        volatility_name = pricing_parameters.AddFXOptionVolatility(self.option)

        pricing_parameters.AddDiscountCurveAndGetName(underlying.MappedDiscountLink())
                
        for quantityDV in self.portfolioTradeQuantities:
            quantity =  quantityDV.Number()      
            deal = PairList()
            deal["Object"] = "FXBarrierOption"
            deal["Reference"] = createAALabel(name)
            deal["MtM"] = getMtMValue(self.mtm)
            deal["Tags"] = ""
            deal["Currency"] = self.ccy.Name()
            deal["Underlying_Currency"] = underlying.Name()
            deal["Discount_Rate"] = curve_name
            deal["Buy_Sell"] = getBuySellFlag(quantity < 0)
            deal["Expiry_Date"] = createDateStringFromDateTime(self.option.ExpiryDate())
            deal["Underlying_Amount"] = abs(quantity)
            deal["Option_Type"] = getCallOrPutType(self.option.IsCallOption())
            deal["Strike_Price"] = self.strike
            deal["FX_Volatility"] = volatility_name

            deal["Barrier_Type"] = barrier.getAAType()
            deal["Barrier_Price"] = self.option.Barrier()
            deal["Cash_Rebate"] = self.option.Rebate()
            deal["Payoff_Currency"] = "Currency"
            deal["Barrier_Monitoring_Frequency"] = "0M"  # Continuous

            deals.Add(deal.compose())

        return AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)
        

    def createDoubleBarrierFXOption(self, barrier):
        underlying = self.option.Underlying()
        #ccy = self.option.StrikeCurrency()
        name = self.option.Name()
        pricing_parameters = AAParameterDictionary.ParameterDictionary()
        deals = acm.FArray()
        curve_name = pricing_parameters.AddDiscountCurveAndGetName(self.fxBaseCurrencyDiscountCurveMappingLink)
        volatility_name = pricing_parameters.AddFXOptionVolatility(self.option)

        pricing_parameters.AddDiscountCurveAndGetName(underlying.MappedDiscountLink())
                
        for quantityDV in self.portfolioTradeQuantities:
            quantity =  quantityDV.Number()      
            deal = PairList()
            deal["Object"] = "FXDoubleBarrierOption"
            deal["Reference"] = createAALabel(name)
            deal["MtM"] = getMtMValue(self.mtm)
            deal["Tags"] = ""
            deal["Currency"] = self.ccy.Name()
            deal["Underlying_Currency"] = underlying.Name()
            deal["Discount_Rate"] = curve_name
            deal["Buy_Sell"] = getBuySellFlag(quantity < 0)
            deal["Expiry_Date"] = createDateStringFromDateTime(self.option.ExpiryDate())
            deal["Underlying_Amount"] = abs(quantity)
            deal["Option_Type"] = getCallOrPutType(self.option.IsCallOption())
            deal["Strike_Price"] = self.strike
            deal["FX_Volatility"] = volatility_name

            deal["Barrier_Type"] = barrier.getAAType()
            deal["Upper_Barrier"] = self.option.Barrier()
            deal["Lower_Barrier"] = barrier.doubleBarrier()
            deal["Cash_Rebate"] = self.option.Rebate()
            deal["Payoff_Currency"] = "Currency"
            deal["Barrier_Monitoring_Frequency"] = "0M"  # Continuous

            deals.Add(deal.compose())

        return AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)

def createFXOptionDealString(option, portfolioTradeQuantities, valuationDate, mtm):
    deal = FxOptionDeal(option, portfolioTradeQuantities, valuationDate, mtm)
    return deal.get()
