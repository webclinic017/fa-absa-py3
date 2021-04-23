'''
-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2018-02-26                      Gavin Brennan       Nico Louw          Use the reset period as the forecast period for floating rate.

'''


import ael, acm, string, RollingPeriod, SAGEN_str_functions


def EagleTradeTTSProductType(temp, t, *rest):
    acmLegs = acm.FTrade[t.trdnbr].Instrument().Legs()
    isZeroCoupon = False
    
    for leg in acmLegs:
        if leg.LegType() == 'Zero Coupon Fixed':
            isZeroCoupon = True
    
    if isZeroCoupon:
        return 'ZERO_SWP'
    else:
        return 'IR_SWP'
    
    
def EagleAssetInterestTerm(temp, l, *rest):
    acmLeg = acm.FLeg[l.legnbr]
    if acmLeg.FloatRateReference():
        period = ExtractPeriodFromName(l)
        if period != 'Index out of range' and period != 'ON':
            return period
        else:
            fr = acmLeg.FloatRateReference().ExpiryPeriod()
            return string.upper(fr)
    else:
        return RollingPeriod.RPUpper(None, l)


def ExtractPeriodFromName(l):
    if (SAGEN_str_functions.split_string(1, l.float_rate.insid, '-', 3)) == 'Index out of range' :
        return SAGEN_str_functions.split_string(1, l.float_rate.insid, '-', 2)
    else:
        return SAGEN_str_functions.split_string(1, l.float_rate.insid, '-', 3)
