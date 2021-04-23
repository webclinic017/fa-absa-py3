import ael
def getCF(i,date,* rest):
    legs = i.legs()
    for l in legs: 
    	if l.type == 'Fixed':
	    cfs = l.cash_flows()
	    for cs in cfs:
	    	
		if date == cs.start_day:
		    if cs.type == 'Fixed Rate':
		    	print(cs.nominal_amount())
		    	return cs.nominal_amount()
			
		    

