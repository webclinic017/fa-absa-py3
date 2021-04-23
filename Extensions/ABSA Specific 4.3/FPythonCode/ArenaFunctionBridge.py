"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    ArenaFunctionBridge

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-30      Upgrade2018     Jaysen Naicker                                  Merge customizations with 2018 default code 
-----------------------------------------------------------------------------------------------------------------------------------------
"""

#__src_file__ = "extensions/arena_function_bridge/./ArenaFunctionBridge.py"
from __future__ import print_function
import ael, acm


# ====================== Calc space for Standard Calculations ======

space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()


# ====================== Cashflow functions  =======================

# cf.ex_coupon_date()   
def cashflow_ex_coupon_date(cfwnbr): 
    return acm.FCashFlow[cfwnbr].ExCouponDate()
    
# cf.projected_cf()
def cashflow_projected_cf(cfwnbr): 
    return acm.GetCalculatedValueFromString(acm.FCashFlow[cfwnbr], acm.GetDefaultContext(), "projectedCashFlow", None).Value().Number()

def GetProjectedCashFlow(cashFlow, trade=None):
    if trade is None:
        ins = cashFlow.Leg().Instrument()
        trade = ins.Trades()[0]
    value = ''
    calcValue = cashFlow.Calculation().Projected(space, trade)
    if type(calcValue) == int:
        value = float(calcValue)
    else:
        value = calcValue.Value().Number()
    return value

# ====================== FX functions  =============================

    
# curr1.forward_price(forwardDate, currid2)   
def fx_forward_price(currid1, currid2, forwardDate):
    curr1 = acm.FInstrument[currid1]
    curr2 = acm.FInstrument[currid2]
    currPair = curr1.CurrencyPair(curr2)
    today = acm.Time().DateNow()
    spotDate = currPair.SpotDate(today)
    spotPrice = curr1.Calculation().MarketPrice(space, today, 0, curr2).Value().Number()
    yc1 = curr1.MappedDiscountCurve(0).Parameter().IrCurveInformation()
    yc2 = curr2.MappedDiscountCurve(0).Parameter().IrCurveInformation()
    df1 = yc1.Discount(spotDate, forwardDate)
    df2 = yc2.Discount(spotDate, forwardDate)
    return spotPrice * df1 / df2

# curr1.used_price(date, currid2)   
def fx_rate(currid1, currid2, date):
    curr1 = acm.FInstrument[currid1]
    curr2 = acm.FInstrument[currid2]
    if None == date:
        date = acm.Time().DateNow()
    return curr1.Calculation().MarketPrice(space, date, 0, curr2).Value().Number()
    

# ====================== Instrument functions ====================== 


# ins.interest_accrued(date)
def instrument_accrued_interest(insid, date):
    acc = acm.FInstrument[insid].Calculation().Accrued(space, date, None, None)
    return acc.Value()
    
# ins.dirty_from_yield(date, None, None, quote)
def instrument_dirty_from_yield(insid, quote, date):
    ins = acm.FInstrument[insid]
    fromQuote = ins.DenominatedValue(quote, date)
    fromQuotation = acm.FQuotation['Yield']
    toQuotation = acm.FQuotation['Pct of Nominal']
    return ins.QuoteToQuote(fromQuote, acm.Time().DateNow(), None, fromQuotation, toQuotation).Number()
    
# ins.implied_volat(ump,,,,quote) (ump not defined anymore)
def instrument_implied_volatility(insid, quote):
    expr = "imply(snoop(theoreticalPrice, volatilityRiskFactorNames), theoreticalPrice, "
    expr += str(quote)
    expr += ", 0, 0, 1.5, 50)"
    return  acm.GetCalculatedValueFromString(acm.FInstrument[insid], acm.GetDefaultContext(), expr, None).Value().Number()
    
# ins.implied_volat(ump,Close) (ump not defined anymore)
def instrument_implied_volatility_close(insid):
    quote = acm.GetCalculatedValueFromString(acm.FInstrument[insid], acm.GetDefaultContext(), "adsPriceFeed:marketPriceSettlement", None).Value().Number()
    return instrument_implied_volatility(insid, quote)
    
# ins.mtm_price(date, currid, 1)
def instrument_mtm_price(insid, date, currid): 
    return acm.FInstrument[insid].MtMPrice(date, currid, 0)
    
# ins.nominal_amount(date)
def instrument_nominal_amount(insid, date): 
    #The NominalAtDate has been depracated in Front 2017.1
    # - this override should be removed once the NominalAtDate reference has
    #    been removed from the default module
    #return acm.FInstrument[insid].NominalAtDate(date, None)
    nominalAtDate = 0.0
    
    instrument = acm.FInstrument[insid]
    contractSize = instrument.ContractSize()
    insCalc = instrument.Calculation()
    
    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    
    params = {}
    params['date'] = date
    insNominalFactor = insCalc.InstrumentNominalFactorParams(calcSpace, params)
    
    nominalAtDate = insNominalFactor * contractSize
    return nominalAtDate
    
# ins.position(None, None, None, date, None, None, 1, account, 1)
def instrument_settlement_position(insid, prfnbr, accnbr, day, status):
    pos = 0
    settlements = acm.FInstrument[insid].SecuritySettlements(acm.FPhysicalPortfolio[prfnbr], acm.FAccount[accnbr], status)
    for s in settlements:
        pos += s.Position(day)
    return pos
    
# ins.theor_price()
def instrument_theor_price(insid): 
    return acm.GetCalculatedValueFromString(acm.FInstrument[insid], acm.GetDefaultContext(), "theoreticalPrice", None).Value().Number()

# ins.used_price()
def instrument_used_market_price(insid): 
    return acm.GetCalculatedValueFromString(acm.FInstrument[insid], acm.GetDefaultContext(), "marketPrice", None).Value().Number()
 
# ins.used_price(date, currid, price_find_type)
def instrument_used_price(insid, date, currid = None, price_find_type = 'None', market = None):
    dict = acm.FDictionary()
    if None != date:
        dict['priceDate'] = date
    if None != currid:
        dict['currency'] = acm.FCurrency[currid]
    if price_find_type and price_find_type != 'None':
        if price_find_type == 'Ask' or price_find_type == 'Bid':
            dict['typeOfPrice'] = 'Average'+price_find_type+'Price'
        else:
            dict['typeOfPrice'] = price_find_type+'Price'
    if None != market:
        dict['marketPlace'] = market
 
    ins = acm.FInstrument[insid]
    return ins.Calculation().MarketPriceParams(space, dict).Value().Number()
    
# ins.used_context_parameter(PriceFinding)
def instrument_used_price_finding(insid):
    param = acm.FInstrument[insid].MappedPriceFinding().Parameter()
    if param != None:
        return param.Name()
    return None
 
# ins.used_vol()
def instrument_used_volatility(insid):
    return acm.GetCalculatedValueFromString(acm.FInstrument[insid], acm.GetDefaultContext(), "snoop(theoreticalPrice, volatilityRiskFactorNames)", None).Value()
 
 
# ====================== Leg functions ============================= 


# leg.interest_accrued(date)
def leg_accrued_interest(legnbr, date):
    acc = acm.GetFunction("mappedGlobalAccountingParameters", 0)().Parameter()
    return acm.GetFunction("interestAccrued", 5)(acm.FLeg[legnbr], date, acc, 0, 0).First().Number()
  
# Trade functions

# trade.nominal_amount()
def trade_nominal_amount(trdnbr):
    return acm.FTrade[trdnbr].Nominal()
 
# trade.spot_date(date)
def trade_spot_date(trdnbr, date):
    return acm.FTrade[trdnbr].Instrument().GetSpotDay(date, None)
 
# Yield curve functions

# yc.yc_rate(date1, date2, ratetype, daycont)
def yield_curve_rate(ycname, date1, date2, ratetype, daycount):
    return acm.FYieldCurve[ycname].Rate(date1, date2, ratetype, daycount)
 
 
# ====================== Misc functions ============================ 


# ael.userid()
def current_user(): 
    return acm.User().Name()

# ael.used_acc_curr()
def used_acc_curr():
    return acm.GetFunction("mappedGlobalAccountingParameters", 0)().Parameter().Currency().Name()
    
# ael.used_acc_mtm_market()
def used_acc_mtm_market():
    fMtmMarket = acm.GetFunction("mappedGlobalAccountingParameters", 0)().Parameter().MtmMarket()
    return ael.Party[fMtmMarket.Name()]
  

# ====================== Test code ================================= 


def test():
    aFutureDate = '080808'
    aHistoricalDate = '070101'
    aBond = 'FRD_BOND_AMORT_01'
    aBondYield = 6.3
    anOption = 'MickeBondOption'
    anOptionQuote = 10.5364
    aLeg = 31096
    aTrade = 620081
    aTradeQuote = 98.75
    aCashFlow = 341236
    aYieldCurve = 'FRD_EUR_SWAP'
    
    # Cashflow functions
    print("cashflow_ex_coupon_date: "                   + cashflow_ex_coupon_date(aCashFlow))
    print("cashflow_projected_cf: "                     + str(cashflow_projected_cf(aCashFlow)))
    # FX functions
    print("fx_forward_price: "                          + str(fx_forward_price('EUR', 'USD', aFutureDate)))
    print("fx_rate: "                                   + str(fx_rate('EUR', 'USD', None)))
    # Instrument functions
    print("instrument_accrued_interest: "               + str(instrument_accrued_interest(aBond, aFutureDate)))
    print("instrument_dirty_from_yield: "               + str(instrument_dirty_from_yield(aBond, aBondYield, acm.Time().DateNow()))) 
    print("instrument_implied_volatility: "             + str(instrument_implied_volatility(anOption, anOptionQuote)))
    print("instrument_implied_volatility_close: "       + str(instrument_implied_volatility_close(anOption)))
    print("instrument_mtm_price: "                      + str(instrument_mtm_price(aBond, aHistoricalDate, 'EUR')))
    print("instrument_nominal_amount: "                 + str(instrument_nominal_amount(aBond, aFutureDate)))
    print("instrument_theor_price: "                    + str(instrument_theor_price(anOption)))
    print("instrument_used_market_price: "              + str(instrument_used_market_price(aBond)))
    print("instrument_used_price: "                     + str(instrument_used_price(aBond, aHistoricalDate)))
    print("instrument_used_price2: "                    + str(instrument_used_price(aBond, 0, 'SEK', 'Bid')))
    print("instrument_used_price_finding: "             + str(instrument_used_price_finding(aBond)))
    print("instrument_used_volatility: "                + str(instrument_used_volatility(anOption)))
    # Leg functions
    print("leg_accrued_interest: "                      + str(leg_accrued_interest(aLeg, aFutureDate)))
    # Trade functions
    print("trade_nominal_amount: "                      + str(trade_nominal_amount(aTrade)))
    print("trade_premium_from_quote: "                  + str(trade_premium_from_quote(aTrade, aTradeQuote, acm.Time().DateNow())))
    print("trade_spot_date: "                           + str(trade_spot_date(aTrade, acm.FTrade[aTrade].AcquireDay())))
    # Yield curve functions
    print("yield_curve_rate: "                          + str(yield_curve_rate(aYieldCurve, acm.Time().DateNow(), aFutureDate, 'Annual Comp', 'Act/365')))
    # Misc functions
    print("current_user: "                              + str(current_user()))
    print("used_acc_curr: "                             + str(used_acc_curr()))
    print("used_acc_mtm_market: "                       + str(used_acc_mtm_market().ptyid))
