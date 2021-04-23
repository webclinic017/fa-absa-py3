"""----------------------------------------------------------------------------
MODULE
    FFixingEstimateTemplate - Template code for stub fixing 
    interpolation hook FFixingEstimate.interpol_fixing(). 
	
    (c) Copyright 2011 by SunGard Front Arena. All rights reserved.

DESCRIPTION
    The template hook interpol_fixing() returns the interpolated 
    rate for stub fixings. The rate is interpolated between the rate 
    of the index shorter and the rate of the index longer than the
    term of the cashflow period. The indexes must be grouped into 
    families. This is done by entering the family string in the free 
    text field for each rate index (in Misc window). The family, 
    together with the currency will detrmine the set of indexes to use 
    for the interpolation.

    To check: what difference between the cashflow period and the rate 
    index period makes the cashflow applicable for interpolation ? 
    Below, 3 days difference is used.

    To check: How to determine the period length of the rate indexes? 
    Below the lenghth is determined by applying the end period of 
    the rate index from todays date. This might have to be adjusted 
    to any market convention.

RENAME this module to FFixingEstimate to activate the interpolation 
    hook FFixingEstimate.interpol_fixing().

----------------------------------------------------------------------------"""

import acm
import ael
import math

daysBetween = acm.GetFunction( 'days_between', 4)
dateAddDelta = acm.GetFunction('date_add_delta', 6)

calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

def days_between_adjusted_day(leg, startDate, endDate, daycount):
    """
    Function days_between_adjusted_day(leg, startDate, endDate, daycount) 
    returns the number of days between startDate and the adjusted endDate 
    according to the legs reset calendars
    """
    date = endDate
    cals = []
    if leg.ResetCalendar():
        cals.append( leg.ResetCalendar() )
    if leg.Reset2Calendar():
        cals.append( leg.Reset2Calendar() )
    if leg.Reset3Calendar():
        cals.append( leg.Reset3Calendar() )
    if leg.Reset4Calendar():
        cals.append( leg.Reset4Calendar() )
    if leg.Reset5Calendar():
        cals.append( leg.Reset5Calendar() )
    if cals:
        cals.extend( (5-len(cals))*[None] )
        equal = False
        while (equal==False):
            equal = True
            date23 = cals[0].ModifyDate( cals[1], cals[2], date )
            date45 = cals[0].ModifyDate( cals[3], cals[4], date )
            dateDiff = acm.Time().DateDifference( date23, date45 )
            if dateDiff == 0:
                date = date23
            elif dateDiff > 0:
                date = date23
                equal = False
            elif dateDiff < 0:
                date = date45
                equal = False        
    return daysBetween( startDate, date, daycount, None )

def interpol_fixing_dict(cashflow, reset):
    """
    Function interpol_fixing_dict(cashflow, reset) returns a dictionary 
    with interpolation data. 
    The key "interpolation_succeeded" tells if interpolation is needed 
    and possible.
    """
    res_dict = acm.FDictionary()
    res_dict["interpolation_succeeded"] = False
    
    # start date and fixing day
    start_date = acm.Time().DateValueDay()
    try:
        fix_day = reset.Day()
    except:
        fix_day = start_date
    leg = cashflow.Leg()
    daycount = leg.DayCountMethod()
    
    # Length of the cashflow tenor
    cfw_days = daysBetween( cashflow.StartDate(), cashflow.EndDate(), daycount, None )

    # Length of the float rate index tenor
    float_rate = leg.FloatRateReference()
    if not float_rate:
        return res_dict
    try:
        index_leg = float_rate.Legs()[0]
    except:
        return res_dict
    unit = index_leg.EndPeriodUnit()
    count = index_leg.EndPeriodCount()
    end_index = dateAddDelta( start_date, 0, 0, 0, unit, count)
    index_days = daysBetween( start_date, end_index, daycount, None )
    
    # Interpolation needed?
    prev_instr = next_instr = prev_date = next_date = None
    prev_days = 0
    next_days = 10000    
    if abs(cfw_days - index_days) > 3 and leg.ResetType() in ('Single', 'Compound'):
        for ri in acm.FRateIndex.Select(''):
            if ri.FreeText() != "" and ri.FreeText() == float_rate.FreeText() and ri.Currency() == float_rate.Currency():
                ri_leg   = ri.Legs()[0]
                ri_unit  = ri_leg.EndPeriodUnit()
                ri_count = ri_leg.EndPeriodCount()
                ri_end   = dateAddDelta( start_date, 0, 0, 0, ri_unit, ri_count )
                ri_days  = daysBetween( start_date, ri_end, daycount, None )
                if ri_days < cfw_days:
                    if ri_days > prev_days:
                        prev_instr = ri
                        prev_days = ri_days
                        prev_date = ri_end
                if ri_days >= cfw_days:
                    if ri_days < next_days:
                        next_instr = ri
                        next_days = ri_days
                        next_date = ri_end

        # Interpolation needed and succeeded...
        if prev_days > 0 and next_days < 10000:
            prev_rate = prev_instr.Calculation().MarketPrice(calcSpace, fix_day).Value().Number()
            if not acm.Math().IsFinite(prev_rate):
                prev_rate = 0.0
            next_rate = next_instr.Calculation().MarketPrice(calcSpace, fix_day).Value().Number()
            if not acm.Math().IsFinite(next_rate):
                next_rate = 0.0
            prev_days = days_between_adjusted_day(leg, start_date, prev_date, daycount)
            next_days = days_between_adjusted_day(leg, start_date, next_date, daycount)

            res_dict["interpolation_succeeded"] = True
            
            res_dict["cfw_days"] = cfw_days

            res_dict["prev_instr"] = prev_instr.Name()
            res_dict["prev_rate"] = prev_rate
            res_dict["prev_days"] = prev_days

            res_dict["next_instr"] = next_instr.Name()
            res_dict["next_rate"] = next_rate
            res_dict["next_days"] = next_days

    return res_dict
    
def check_arguments(arg):
    """
    Function check_arguments(*arg) checks if argument list is AEL or 
    ACM entities.
    """
    cashflow = None
    reset = None
    if isinstance(arg[0], ael.ael_entity) and arg[0].record_type == 'CashFlow':
        # arg list on format (ael.CashFlow, resnbr)
        cashflow = acm.FCashFlow[ arg[0].cfwnbr ]
        try:
            reset = arg[1]
            if isinstance(reset, type(1)):
                reset = acm.FReset[reset]
            elif isinstance(reset, ael.ael_entity) and reset.record_type == 'Reset':
                reset = acm.FReset[reset.resnbr]
        except:
            pass
    elif arg[0].Class() == acm.FReset:
        reset = arg[0]
        cashflow = reset.CashFlow()
    elif arg[0].Class() == acm.FCashFlow:
        cashflow = arg[0]
        try:
            reset = arg[1]
            if isinstance(reset, type(1)):
                reset = acm.FReset[reset]
        except:
            pass
    return cashflow, reset

def interpol_fixing(*arg):
    res = 0.0
    cashflow, reset = check_arguments(arg)
    if cashflow:
        ipol = interpol_fixing_dict(cashflow, reset)
        if ipol["interpolation_succeeded"]:
            prev_rate = ipol["prev_rate"]
            prev_days = ipol["prev_days"]

            next_rate = ipol["next_rate"]
            next_days = ipol["next_days"]
            
            cfw_days = ipol["cfw_days"]
            
            res = (cfw_days - prev_days) * next_rate + (next_days - cfw_days) * prev_rate
            res = res / (next_days - prev_days)
    return res
