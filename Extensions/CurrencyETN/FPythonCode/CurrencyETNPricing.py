"""----------------------------------------------------------------------------
PROJECT                 :   ETN Pricing
PURPOSE                 :   New version of ETN pricing
DEPATMENT AND DESK      :   Prime Services, Commodities
REQUESTER               :   Byron Woods, Floyd Malatji
DEVELOPER               :   Ondrej Bahounek
CR NUMBER               :   CHG1000488229

This is a new version of ETN pricing solution in Front Arena.
Previous version didn't work properly since FA Upgrade 2013,
but instead of fixing it, completely new solution was requested by business.

More info: https://confluence.barcapint.com/display/ABCAPFA/Commodities+-+ETN+solution

HISTORY
===============================================================================
Date        Change no      Developer        Description
-------------------------------------------------------------------------------
2018-08-07  CHG1000488229  Ondrej Bahounek  Initial Implementation
2018-12-14  CHG1001218211  Ondrej Bahounek  Pass FX rate as parameter.
----------------------------------------------------------------------------"""

import math
import acm
import ael
from at_timeSeries import add_time_series_value, get_time_series_values
from at_logging import getLogger


TODAY = acm.Time.DateToday()
LOGGER = getLogger()
CALENDAR = acm.FInstrument['ZAR'].Calendar()
SPACE = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
PRICE_MARKETS_ORDERS = ('SPOT', 'internal')

# time serie saved on FRN instruments as this value is more related to FRN than ETN
TS_ACC_PIP_NAME = 'ETN_AccMktPips'

FRIDAY_DIST = {
    'Monday': -3,
    'Tuesday': 3,
    'Wednesday': 2,
    'Thursday': 1,
    'Friday': 0,
    'Saturday': -1,
    'Sunday': -2
    }

    
def used_price(ins, for_date, curr=None, price_find_type=None, market=None, space=SPACE):
    """
    USD/ZAR rate = # used_price('USD', '2018-05-14', 'ZAR')
    
    market:
        you should use SPOT for any historical date and None for date today
    """
    if isinstance(ins, str):
        ins = acm.FInstrument[ins]
    dict = acm.FDictionary()
    if for_date:
        dict['priceDate'] = for_date
    if curr:
        dict['currency'] = curr
    if price_find_type and price_find_type != 'None':
        if price_find_type == 'Ask' or price_find_type == 'Bid':
            dict['typeOfPrice'] = 'Average' + price_find_type + 'Price'
        else:
            dict['typeOfPrice'] = price_find_type + 'Price'
    if market:
        dict['marketPlace'] = market
        dict['useSpecificMarketPlace'] = True
    return ins.Calculation().MarketPriceParams(space, dict).Value().Number()


def get_price(ins, for_date, curr=None):
    if for_date == TODAY:
        price = used_price(ins, for_date, curr)
        if price == price:
            return price
    
    for market in PRICE_MARKETS_ORDERS:
        price = used_price(ins, for_date, curr, market=market)
        if price == price:
            return price
    return float('nan')


def FXRate(curr1, date, curr2):
    if isinstance(curr1, str):
        curr1 = acm.FCurrency[curr1]
    if isinstance(curr2, str):
        curr2 = acm.FCurrency[curr2]
    base_curr = acm.FCurrency['USD']
    if curr1.Name() != base_curr.Name():
        try:
            fx_rate_curr1 = get_price(curr1, date, base_curr)
        except:
            fx_rate_curr1 = 0.0
    else:
        fx_rate_curr1 = 1
    if curr2.Name() != base_curr.Name():
        try:
            fx_rate_curr2 = get_price(base_curr, date, curr2)
        except:
            fx_rate_curr2 = 0.0
    else:
        fx_rate_curr2 = 1
    fx_rate = fx_rate_curr1 * fx_rate_curr2
    return fx_rate


def get_libor(curr_name, for_date):
    '''
    Current LIBORs:
        JPY-LIBOR-ON-DEP,
        USD-LIBOR-ON-DEP,
        GBP-LIBOR-ON-DEP,
        CAD-LIBOR-ON-DEP,
        CHF-LIBOR-ON-DEP,
        EUR-LIBOR-ON-DEP,
        AUD-LIBOR-ON-DEP,
        NZD-LIBOR-ON-DEP,
        BRL-LIBOR-ON-DEP,
        THB-LIBOR-ON-DEP
    '''
    libor_name = "%s-LIBOR-ON-DEP" % curr_name
    libor_ins = acm.FInstrument[libor_name]
    if not libor_ins:
        msg = "LIBOR instrument for '%s' not found" % curr_name
        LOGGER.error(msg)
        raise RuntimeError(msg)
    return get_price(libor_ins, for_date)


def get_underlying_frn(etn):
    if etn is None or etn.InsType() != 'ETF':
        msg = "Unexpected Currency-linked ETN instrument"
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    und = etn.Underlying()
    comb_maps = und.InstrumentMaps()
    if len(comb_maps) != 1:
        msg = "Currency-linked ETN underlying index does not have a single constituent"
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    frn = comb_maps[0].Instrument()
    if frn.InsType() != 'FRN':
        msg = "Currency-linked ETN underlying index does not have a single FRN constituent"
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    return frn


def calc_acc_pip_from_multiplier(multiplier, fx_rate):
    acc_pip = (multiplier * fx_rate - fx_rate) * 10000
    return acc_pip


def check_previous_ts_value(frn, for_date):
    previous_day = acm.Time.DateAddDelta(for_date, 0, 0, -1)
    tsval = get_time_series_values(TS_ACC_PIP_NAME, frn.Oid(), previous_day)
    if len(tsval) == 0:
        raise RuntimeError("'%s' Time Serie value for previous day (%s) on '%s' is missing"
                            % (TS_ACC_PIP_NAME, previous_day, frn.Name()))


def save_to_timeserie(frn, value, for_date):
    """Save new value to time series.
    
    Don't save new value if previous day value is missing.
    """
    check_previous_ts_value(frn, for_date)
    LOGGER.info("Storing TS: '{0}' on '{1}' for '{2}': {3}".format(
            TS_ACC_PIP_NAME, frn.Name(), for_date, value))
    add_time_series_value(TS_ACC_PIP_NAME, frn.Oid(), value, for_date, 0, True)


def get_last_acc_pip(frn, for_date):
    """Get last time serie value BEFORE given day"""
    time_series = acm.FTimeSeries.Select('recaddr=%i and timeSeriesSpec="%s" and day<"%s"'
                                         % (frn.Oid(), TS_ACC_PIP_NAME, for_date))
    ts_sorted = sorted(time_series, key=lambda ts: ts.Day(), reverse=True)
    for point in ts_sorted:
        if for_date >= point.Day():
            return point.TimeValue()


def calc_mkt_mid(etn_curr, frn, for_date, fx_rate=None):
    frn_curr = frn.Currency()
    if CALENDAR.IsNonBankingDay(None, None, for_date):
        # previous business day
        for_date = CALENDAR.AdjustBankingDays(for_date, -1)
    if fx_rate is None or math.isnan(fx_rate):
        fx_rate = FXRate(frn_curr, for_date, etn_curr)
    
    libor = get_libor(frn_curr.Name(), for_date)
    leg = frn.Legs()[0]
    spread = leg.Spread() * 100
    investor_earns = libor - spread
    day_count = int(leg.DayCountMethod()[-3:])
    mtk_mid = fx_rate / day_count * investor_earns * 100
    return mtk_mid


def calc_acc_pip(etn_curr, frn, for_date):
    # always calculate calc_mkt_mid for current day
    # as FX rate changes during the day
    mkt_mid = calc_mkt_mid(etn_curr, frn, for_date)
    if mkt_mid < 0:
        mkt_mid = 0
    last_acc = get_last_acc_pip(frn, for_date)
    if last_acc is None:
        LOGGER.warning("Last accumulated value for '%s' before '%s' not found",
                       frn.Name(), for_date)
        return mkt_mid
    return last_acc + mkt_mid


def get_frn_theor(frn, val_date, cal_curr):
    mkt_val = calc_acc_pip(cal_curr, frn, val_date)
    return mkt_val


def CurrencyETNTheor(etn, val_date=TODAY, fx_rate=None):
    frn = get_underlying_frn(etn)
    if frn is None:
        msg = "Missing underlying on '%s'" % etn.Name()
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    roll_date = get_etn_roll_date(etn, val_date)
    
    if roll_date == val_date:
        frn_theor = 0
    else:
        frn_theor = get_frn_theor(frn, val_date, etn.Currency())
    
    if fx_rate is None or math.isnan(fx_rate):
        fx_rate = FXRate(frn.Currency(), val_date, etn.Currency())
    
    etn_theor = frn_theor / 10000 + fx_rate
    yc = ael.Instrument[etn.Name()].used_yield_curve()
    ael_date = ael.date_from_string(val_date)
    etn_curr = ael.Instrument[etn.Name()].curr
    day_offset = etn.SpotBankingDaysOffset()
    discount_factor = yc.yc_rate(ael_date,
                                 ael_date.add_banking_day(etn_curr, day_offset),
                                 'Discount',
                                 yc.storage_daycount,
                                 'Discount')
    etn_theor = discount_factor * etn_theor
    
    return {"result":acm.DenominatedValue(etn_theor, etn.Currency().Name(), val_date)}


def store_accumulated_mkt(etn, val_date):
    frn = get_underlying_frn(etn)
    roll_date = get_etn_roll_date(etn, val_date)
    if roll_date == val_date:
        mkt_val = 0
    else:
        mkt_val = calc_acc_pip(etn.Currency(), frn, val_date)
    save_to_timeserie(frn, mkt_val, val_date)


def CurrencyETNLinkedEquivalent(etn, val_date=TODAY):
    frn = get_underlying_frn(etn)
    cal = etn.Currency().Calendar()
    if cal.IsNonBankingDay(None, None, val_date):
        val_date = cal.AdjustBankingDays(val_date, 1)
    frn_theor = get_frn_theor(frn, val_date, etn.Currency())
    return acm.DenominatedValue(frn_theor, frn.Currency().Name(), val_date)


def closest_friday(tdate):
    """Closest Friday to given date."""
    day = acm.Time.DayOfWeek(tdate)
    adjustment = FRIDAY_DIST[day]
    friday = acm.Time.DateAddDelta(tdate, 0, 0, adjustment)
    return friday


def get_next_roll_date(frn, val_date, cal_curr):
    """Get closest roll date.
    
    Can also return current day.
    """
    cal = cal_curr.Calendar()
    leg = frn.Legs()[0]
    roll_date = leg.RollingPeriodBase()
    roll_period = leg.RollingPeriod()
    if roll_date > val_date:
        while acm.Time.DateAdjustPeriod(roll_date, '-%s' % roll_period) > val_date:
            roll_date = acm.Time.DateAdjustPeriod(roll_date, '-%s' % roll_period)
    else:
        while roll_date < val_date:
            roll_date = acm.Time.DateAdjustPeriod(roll_date, roll_period)
    roll_date = max(roll_date, leg.StartDate())
    roll_date = closest_friday(roll_date)
    if cal.IsNonBankingDay(None, None, roll_date):
        roll_date = cal.AdjustBankingDays(roll_date, -1)
    roll_date = max(roll_date, leg.StartDate())
    return roll_date


def get_etn_roll_date(etn, for_date):
    if etn.FreeText():
        roll_date = acm.Time.AsDate(etn.FreeText())
    else:
        frn = get_underlying_frn(etn)
        roll_date = get_next_roll_date(frn, for_date, etn.Currency())
    return roll_date


def is_etn_reset_date(etn, for_date):
    roll_date = get_etn_roll_date(etn, for_date)
    frn = get_underlying_frn(etn)
    start_day = frn.StartDate()
    return start_day < for_date and roll_date == for_date


def is_etn_reset_coming(etn, for_date, bus_days_diff=2):
    roll_date = get_etn_roll_date(etn, for_date)
    cal = etn.Currency().Calendar()
    return cal.BankingDaysBetween(for_date, roll_date) <= bus_days_diff


def print_all():
    """For testing purposes."""
    asql_result = ael.asql("""select i.insaddr 
from Instrument i, Instrument u, Instrument frn, CombinationLink cl, ChoiceList c 
where i.instype = 'ETF' 
    and c.seqnbr = i.product_chlnbr
    and i.und_insaddr = u.insaddr 
    and u.instype = 'EquityIndex' 
    and frn.instype = 'FRN' 
    and frn.insaddr = cl.member_insaddr 
    and u.insaddr = cl.owner_insaddr 
    and (i.curr < frn.curr or i.curr > frn.curr) 
    and c.entry = 'CurrencyETN'""")[1][0]

    etns = [ael.Instrument[x[0]] for x in asql_result]
    for etn in etns:
        frn = getUnderlyingFRN(etn)
        print('ETN:', etn.insid, 'curr:', etn.curr.insid)
        print('FRN:', frn.insid, 'curr:', frn.curr.insid)
        frn_curr = acm.FInstrument[frn.curr.insid]
        etn_curr = acm.FInstrument[etn.curr.insid]
        print(get_price(frn_curr, '2018-04-13', etn_curr))

#print_all()
