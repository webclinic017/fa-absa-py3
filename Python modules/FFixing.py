""" Standard_Queries:1.0.0 """

import ael
import math

# This function returns the interpolated rate for stub fixings. The rate is interpolated 
# between the rate of the index shorter and the rate of the index longer than the
# term of the cashflow period. The indexes must be grouped into families. This is done
# by entering the family string in the free text field for each rate index (in Misc window).
# The family, together with the currency will detrmine the set of indexes to use for 
# the interpolation.

# To check: what difference between the cashflow period and the rate index period
# makes the cashflow applicable for interpolation ? Below, 3 days difference is used.
# To check: How to determine the period length of the rate indexes? Below the lenghth
# is determined by applying the end period of the rate index from todays date. This might
# have to be adjusted to any market convention.

def interpol_fixing(c, *rest):

    printing = 0
    prev_days = 0
    prev_rate = 0
    prev_ref = ""
    next_days = 10000
    next_rate = 0
    next_ref = ""
    daycount_method = c.legnbr.daycount_method
    days = c.start_day.days_between(c.end_day, daycount_method)
    start_date = ael.date_today()

    try:
    	resnbr = int(rest[0])
	r = ael.Reset[resnbr]
	fix_day = r.day
    except:
    	fix_day = ael.date_today()


    for frl in c.legnbr.float_rate.legs():
	  index_days = start_date.days_between(start_date.add_period(frl.end_period), daycount_method)
    if abs(days - index_days) > 3 and c.legnbr.reset_type in ('Single', 'Compound'):
	for i in ael.Instrument.select('instype="RateIndex"'):
	    if i.free_text != "" and i.free_text == c.legnbr.float_rate.free_text and i.curr == c.legnbr.float_rate.curr:
		for l in i.legs():
    		    ri_days = start_date.days_between(start_date.add_period(l.end_period), daycount_method)
                    if ri_days <= days:
                        if ri_days > prev_days:
                            prev_rate = i.used_price(fix_day)
                            prev_days = ri_days
                            prev_ref = i.insid
                    if ri_days > days:
                        if ri_days < next_days:
                            next_rate = i.used_price(fix_day)
                            next_days = ri_days
                            next_ref = i.insid

	if prev_days > 0 and next_days < 10000:
	    res = (days - prev_days) * next_rate + (next_days - days) * prev_rate
	    res = res / (next_days - prev_days)
    	    if printing:
	    	print ""
		print "Cashflow period", days
    		print "Shorters Index", prev_ref, prev_days, prev_rate
    		print "Longer Index  ", next_ref, next_days, next_rate
    		print "Interpolated Rate", res
	else:
	    res = 0.0
    	    if printing:
		print "Cashflow period", days
    		print "Shorters Index", prev_ref, prev_days, prev_rate
    		print "Longer Index  ", next_ref, next_days, next_rate
	    	print "Interpol unsuccessfull"
    else:
    	res = 0.0
    	if printing:
    	    print "Interpol not needed"
    return res
