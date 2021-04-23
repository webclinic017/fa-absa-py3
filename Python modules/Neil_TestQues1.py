import ael

#function which calculates all the cashflows associated with the instrument
def sum_cashflows_per_instrument(instrum):
    if instrum:
    	inslegs = instrum.legs()
	count = 0
	for leg in inslegs:
	    count = count + len(leg.cash_flows())
	return count
	
#calls the function to sum the cashflows of an Instrument
i = ael.Instrument['ZAR/R197']
print 'Instrument %s has %d cashflows' %(i.insid, sum_cashflows_per_instrument(i))
