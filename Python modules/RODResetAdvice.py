import ael, string

def RODRate(t,date,request,*rest):
    
    # Select Instrument related to the trade for determining resets
    ins = ael.Instrument.read('insaddr=%d' % t.insaddr.insaddr) #trd.insaddr.insaddr)
    
    # Set Nominal Amount for trade to compute revised notional amount
    nominal_amount = t.quantity*ins.contr_size
    
    # Select legs associated with the instrument
    lgs = ins.legs()
    
    # Convert date
    
    day_used = ael.date_from_string(date)
    
    # Select the floating leg
    
    for l in lgs:
    	if l.type == 'Float':
    	    leg = l

    # Select the cashflow associated with the floating leg for the Rand Overnight Deposit
    
    cshflw = leg.cash_flows()
    if len(cshflw) > 1:
    	print "ERROR: ROD with more than two cashflows!"
    else:
    
    	resets = cshflw[0].resets()
    	start_day = cshflw[0].start_day
    	end_day = cshflw[0].end_day

    	# Create a new list containing all days (weekends included)
    	yc = ael.YieldCurve.read('yield_curve_name=%s' % "ZAR-RODS")
	
	min = start_day
    	sorted = []
	while min != end_day: #len(resets) != len(sorted):
       	    for r in resets:
    	    	if r.day == min:
	    	    if r.value != 0:
		    	sorted.append((r.day, r.value))
		    	last = r.value
		    else:
		    	last = 0
			sorted.append((r.day, last))
		    add = 1
		    
    	    # If reset day is a public holiday or weekend then fill as it will not be found 
	    if add == 0:
	    	sorted.append((min, last))
	    	add = 1
	    min = min.add_days(add)
	    add = 0
    	while min < end_day:
    	    sorted.append((min, last))
    	    min = min.add_days(1)
    
    	# Calculate the sum of rates per month and the number of days
    	sum = [0]
    	days = [0]
	dates1 = [sorted[0][0]]
    	i = 0
    	for r in sorted:
    	    if sum[0] == 0:
	    	if r[1] != 0 and r[0] < day_used:
		    sum[i] = sum[i] + r[1]
	    	    days[i] = days[i] + 1
	    	    last = r[0]
	    else:
	    	if r[0].day_of_month() > last.day_of_month():
	    	    if r[1] != 0 and r[0] < day_used:
		    	sum[i] = sum[i] + r[1]
	    	    	days[i] = days[i] + 1
		    	last = r[0]
	    	else:
	    	    i = i + 1
		    sum.append(0)
		    days.append(0)
		    dates1.append(r[0])
		    if r[1] != 0 and r[0] < day_used:
		    	sum[i] = sum[i] + r[1]
		    	days[i] = days[i] + 1
		    	last = r[0]
    	numdays = 0
    	i = 0
    	average = 1
    	for s in sum:
    	    if days[i] > 0:
	    	numdays = numdays + days[i]
    	    
    	    	st1, st2 = string.split(str(sum[i]/days[i]), '.')
	    	if len(st2)>=4:
	    	    if int(st2[3]) >= 5:
		      	temp = round(sum[i]/days[i]+0.0001, 3)
	    	    else:
		    	temp = round(sum[i]/days[i], 3)
	    	else:
	    	    temp = round(sum[i]/days[i], 3)
	    	if dates1[i].first_day_of_month() == ael.date_from_string(date).first_day_of_month():
		    if request == 'AverageRate':
		    	return temp
		    elif request == 'OldNotional':
		    	return average*nominal_amount
		    elif request == 'RevisedNotional':
		    	return average*(1+temp/36500*days[i])*nominal_amount
		average = average*(1+temp/36500*days[i])
		i = i + 1
	return (average-1)*36500/numdays
	


def AVERate(csh,date,*rest):
    
    cshflw = ael.CashFlow.read('cfwnbr=%d'%csh.cfwnbr)
    day_used = ael.date_from_string(date)	     
    resets = cshflw.resets()
    start_day = cshflw.start_day
    end_day = cshflw.end_day
    # last to be set equal to the current Overnight Deposit Rate
    
    # Create a new list containing all days (weekends included)
    yc = ael.YieldCurve.read('yield_curve_name=%s' % "ZAR-SWAP")
    min = start_day
    sorted = []
    	
    while min != end_day: #len(resets) != len(sorted):
        for r in resets:
    	    if r.day == min:
	        if r.value != 0:
		    sorted.append((r.day, r.value))
		    last = r.value
		else:
		    last = 0
		    sorted.append((r.day, last))
		add = 1
		    
    	# If reset day is a public holiday or weekend then fill as it will not be found 
	if add == 0:
	    sorted.append((min, last))
	    add = 1
	min = min.add_days(add)
	add = 0
    while min < end_day:
        sorted.append((min, last))
        min = min.add_days(1)
    
    # Calculate the sum of rates per month and the number of days
    sum = [0]
    days = [0]
    i = 0
    for r in sorted:
        if sum[0] == 0:
	    if r[1] != 0 and r[0] < day_used:
	    	sum[i] = sum[i] + r[1]
	    	days[i] = days[i] + 1
	    	last = r[0]
	else:
	    if r[0].day_of_month() > last.day_of_month():
	        if r[1] != 0 and r[0] < day_used:
		    sum[i] = sum[i] + r[1]
	            days[i] = days[i] + 1
		    last = r[0]
	    else:
	        i = i + 1
		sum.append(0)
		days.append(0)
		if r[1] != 0 and r[0] < day_used:
		    sum[i] = sum[i] + r[1]
		    days[i] = days[i] + 1
		    last = r[0]
    numdays = 0
    sumresets = 0
    i = 0
    average = 1
    for s in sum:
        numdays = numdays + days[i]
	sumresets = sumresets + sum[i]
 
        st1, st2 = string.split(str(sum[i]/days[i]), '.')
	if len(st2)>=4:
	    if int(st2[3]) >= 5:
	        temp = round(sum[i]/days[i]+0.0001, 3)
	    else:
	        temp = round(sum[i]/days[i], 3)
	else:
	    temp = round(sum[i]/days[i], 3)
	average = average*(1+temp/36500*days[i])
	
	i = i + 1
    
    return round(sumresets/numdays, 3)
    
t = ael.Trade.read('trdnbr=%d' % 183255)
#print RODRate(t,'2002-09-15')
