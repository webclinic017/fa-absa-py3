import ael

########################################################################################
#This AEL works with an ASQL query, that uses the AEL. The purpose of 
#the AEL script is to provide an accurate price for Prime NCDs. 
#The trader will key the price returned by the ASQL into the price field in the
#trade window. 
########################################################################################

def pncd(i,nominal,traded_factor,current_prime,date,*rest):

    i_years = i.years_to_maturity()
# There is only one leg for the FRN, so get the 'first' leg
    ffleg = i.legs()[0]
# Because at the leg level the float factor only accepts 3dp, the user must update each cashflow's
# float factor. So, let's get the first cashflow's float factor as they will all be the same
    ffcashflow=ffleg.cash_flows()[0]
    float_factor = ffcashflow.float_rate_factor
#    print float_factor
    rolling_period=ffleg.rolling_period
# The rolling period of the instrument determines the coupon frequency
    if rolling_period == '1m':
	i_cpn_freq = 12
    elif rolling_period == '3m':
	    i_cpn_freq = 4
    elif rolling_period == '6m':
	    i_cpn_freq = 2
    elif rolling_period == '12m':
	    i_cpn_freq = 1
    else: return 0
    current_prime = float(current_prime)	
    traded_factor = float(traded_factor)	
# Calculate the cashflow effect over the life of the instrument
    cashflow_effect = nominal*((float_factor-traded_factor)*current_prime)/i_cpn_freq
#    print cashflow_effect
    legs = i.legs()[0]
    cfs = legs.cash_flows()
    pv = 0
# We need the last cashflow's end day to determine if it is a broken period
    cf_end_day=cfs[0].end_day
    for cf_last in cfs:
    	if cf_last.end_day > cf_end_day:
	    cf_end_day = cf_last.end_day
#    print cf_end_day, 'cfed'
    for c in cfs:
# determine days in period for discounting
	if c.end_day: 
	    if c.end_day==cf_end_day:
# If the last period is a broken period, calculate the proportion of the cashflow effect
#	    	print c.start_day.days_between(c.end_day)
	    	cashflow_effect = cashflow_effect/(float(365)/float(12))*c.start_day.days_between(c.end_day)
#		print cashflow_effect
	    else: cashflow_effect = nominal*((float_factor-traded_factor)*current_prime)/i_cpn_freq
	    if date == ael.date_today():
	    	days = ael.date_today().days_between(c.end_day)
	    else:
		days = ael.date_from_string(date).days_between(c.end_day)
	    if days > 0:
		df = ((1 + current_prime)**(float(days)/float(365)))**-1
# aggregate the total PV effect of the cashflow effect
#    	    	print df*cashflow_effect, 'cashflow effect pvd'
		pv = pv - df*cashflow_effect
#		print pv, 'pv'
# calculate the clean consideration (or premium)
#    print pv
    diff = nominal-pv
#    print diff
# express as clean price for entry into trade window
    pncd_price = diff/nominal * 100
#    print pncd_price 
    return pncd_price

def cfff(i,*rest):

    cfff= i.legs()[0].cash_flows()[0].float_rate_factor
    return cfff
