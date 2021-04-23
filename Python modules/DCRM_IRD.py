"""----------------------------------------------------------------------------
MODULE
    DCRM_IRD

DESCRIPTION
    This module is called by the DCRM_IRD ASQL query to calculate
    benchmark delta for a specific benchmark instrument
    on a specific portfolio.

    Department and Desk : Credit Desk
    Requester           : De Clercq Wentzel
    Developer           : Herman Hoon

    History:
    When:         CR Number:  Who:             What:
    2010-05-24    203010      Herman Hoon      Created.
    2010-11-04    475569      Herman Hoon      Added start_date to get
                                               the stat date
                                               for generic instruments.
    2012-05-23    209921      Anwar Banoo      Amended bm_delta
                                               to use trade filter
                                               rather than physical portfolio.
    2012-06-04    241538      Nidheesh Sharma  Amended basis_delta
                                               to use trade filter
                                               rather than physical portfolio.
    2013-11-04    None        Peter Basista    Replaced the yield curve
                                               calculation in ael with
                                               the same code in acm.
    2015-02-11  FA-Upgrade-2014 Peter Basista  Fix a change in FInstrument.
                                               MappedDiscountLink API

END DESCRIPTION
----------------------------------------------------------------------------"""

import datetime
import time

import acm

import dirk_utils

debug = 0

def getDiscountCurve(i, curr_name, *rest):
    """
    Returns the discount curve for a specific instrument and currency.
    """
    ins = acm.FInstrument[i.insid]
    curr = acm.FCurrency[curr_name]
    discount_link = ins.MappedDiscountLink(curr, False, None).Link()
    discount_curve_name = str(discount_link.AsString()).\
        split(',')[0].strip("'")
    return discount_curve_name

def getUnderlyingCurve(i, curr_name, *rest):
    """
    Returns the underlying curve for attribute spread curves.
    """
    ins = acm.FInstrument[i.insid]
    curr = acm.FCurrency[curr_name]
    und = ins.MappedDiscountLink(curr, False, None).Link().UnderlyingComponent()
    if und:
        return und.YieldCurveComponent().Name()
    else:
        return ''

def bm_maturity(ins, *rest):
    """
    Returns the expiry day for generic instruments.
    """
    currency = acm.FCurrency[ins.curr.insid]
    calendar = currency.Calendar()
    date = acm.Time().DateToday()
    adjusted_date = acm.Time().DateAdjustPeriod(date, ins.exp_period)
    # If the adjusted_date is not a business day,
    # use the following business day instead.
    previous_business_day = calendar.AdjustBankingDays(adjusted_date, -1)
    return calendar.AdjustBankingDays(previous_business_day, 1)

def bm_delta(ins, tfn, ycn, shiftsize, *rest):
    """
    Returns the benchmark delta for a specific benchmark instrument
    on a specific tradefilter.
    """
    t0 = time.time()
    columnId = 'Present Value'
    sheetType = 'FPortfolioSheet'
    calcSpace = acm.Calculations().CreateCalculationSpace('Standard',
        sheetType)

    tf = acm.FTradeSelection[tfn]
    if tf == None:
        print(("TradeFilter '{0}' does not exist. "
            "Please note that the names of trade filters "
            "are case sensitive.").format(tfn))
        return -99999999999.0

    topnode = calcSpace.InsertItem(tf)
    calculation = calcSpace.CreateCalculation(topnode, columnId)

    pv0 = calculation.Value().Number()

    yc = acm.FYieldCurve[ycn]

    changed_pcs = []
    for p in ins.prices():
        if dirk_utils.mightBeUsedPrice(p):
            pc = p.clone()
            pc.settle = p.settle + shiftsize
            pc.last = p.last + shiftsize
            pc.bid = p.bid + shiftsize
            pc.ask = p.ask + shiftsize
            pc.apply()
            changed_pcs.append(pc)
            if debug == 1:
                print("Cloned point:\n{0}".format(pc.pp()))

    ycc = yc.Clone()
    ycc.Calculate()
    yc.Apply(ycc)

    pv1 = calculation.Value().Number()

    pv01 = pv1 - pv0
    if debug == 1:
        print("{0}: pv0: {1}, pv1: {2}, diff: {3}".format(ins.insid,
            pv0, pv1, pv01))

    for pc in changed_pcs:
        pc.revert_apply()

    if debug == 1:
        print("{0:f} seconds to calculate benchmark delta for {1}.".format(
            time.time() - t0, ins.insid))

    return pv01

def bm_delta_trade(ins, trdnbr, ycn, shiftsize, *rest):
    """
    Returns the benchmark delta for a specific benchmark instrument
    on a specific trade.
    """
    t0 = time.time()
    columnId = 'Present Value'
    sheetType = 'FPortfolioSheet'
    calcSpace = acm.Calculations().CreateCalculationSpace('Standard',
        sheetType)

    t = acm.FTrade[trdnbr]

    calculation = calcSpace.CreateCalculation(t, columnId)

    pv0 = calculation.Value().Number()

    yc = acm.FYieldCurve[ycn]

    changed_pcs = []
    for p in ins.prices():
        if dirk_utils.mightBeUsedPrice(p):
            pc = p.clone()
            pc.settle = p.settle + shiftsize
            pc.last = p.last + shiftsize
            pc.bid = p.bid + shiftsize
            pc.ask = p.ask + shiftsize
            pc.apply()
            changed_pcs.append(pc)
            if debug == 1:
                print("Cloned point:\n{0}".format(pc.pp()))

    ycc = yc.Clone()
    ycc.Calculate()
    yc.Apply(ycc)

    pv1 = calculation.Value().Number()

    pv01 = pv1 - pv0
    if debug == 1:
        print("{0}: pv0: {1}, pv1: {2}, diff: {3}".format(ins.insid,
            pv0, pv1, pv01))

    for pc in changed_pcs:
        pc.revert_apply()

    if debug == 1:
        print(("{0:f} seconds to calculate benchmark delta "
            "for trade {1}.").format(time.time() - t0, trdnbr))

    return pv01

def basis_delta(sprd, tfn, ycn, shiftsize, *rest):
    """
    Returns the basis delta for a specific spread and tradefilter.
    """
    # Front Upgrade 2013: ael transformed to acm,
    # yc.calculate() crashes Front Arena for some yield curves.
    t0 = time.time()
    columnId = 'Present Value'
    sheetType = 'FPortfolioSheet'
    calcSpace = acm.Calculations().CreateCalculationSpace('Standard',
        sheetType)

    tf = acm.FTradeSelection[tfn]
    if tf == None:
        print(("TradeFilter '{0}' does not exist. "
            "Please note that the names of trade filters "
            "are case sensitive.").format(tfn))
        return -99999999999.0

    topnode = calcSpace.InsertItem(tf)
    calculation = calcSpace.CreateCalculation(topnode, columnId)

    pv0 = calculation.Value().Number()

    ycb = acm.FYieldCurve[ycn]
    yc = ycb.UnderlyingCurve()

    sc = sprd.clone()
    sc.spread = sprd.spread + shiftsize
    sc.apply()

    ycc = yc.Clone()
    ycc.Calculate()
    yc.Apply(ycc)

    pv1 = calculation.Value().Number()
    pv01 = pv1 - pv0

    sc.revert_apply()

    if debug == 1:
        print("{0:f} seconds to calculate basis delta for {1}.".format(
            time.time() - t0, sprd.point_seqnbr.date_period))

    return pv01
 
def getCurveStrip(ycp, *rest):
    """
    Return a string representing the date_period of the provided yield curve.
    """
    return str(ycp.date_period).upper()

def getExpPeriod(ins, *rest):
    """
    Returns the expiry period in upper case.
    """
    i = acm.FInstrument[ins.insid]

    daysOffset = i.SpotBankingDaysOffset()
    unit = i.ExpiryPeriod_unit()
    count = i.ExpiryPeriod_count()
    if unit == 'Days':
        count = count + daysOffset
        if count < 30:
            return str(count) + 'D'
        elif count <= 360:
            return str(int(round(count/30))) + 'M'
        else:
            return str(int(round(count/365))) + 'Y'

    expiry_period = str(ins.exp_period).upper()
    return expiry_period

def start_date(ins, *rest):
    """
    Returns the start day for generic instruments.
    """
    currency = acm.FCurrency[ins.curr.insid]
    calendar = currency.Calendar()
    date = acm.Time().DateToday()
    leg = ins.legs()[0]
    adjusted_date = acm.Time().DateAdjustPeriod(date, leg.start_period)
    # If the adjusted_date is not a business day,
    # use the following business day instead.
    previous_business_day = calendar.AdjustBankingDays(adjusted_date, -1)
    start_date = calendar.AdjustBankingDays(previous_business_day, 1)
    pydate = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    str_date = pydate.strftime("%d-%b-%y")
    return str_date
