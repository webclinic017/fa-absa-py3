import ael, string

def accrued_interest(t,day,request,detail,*rest):

    # Select the instrument associated with the trade
    ins = t.insaddr
    # Create date variable to be used for reporting
    date = ael.date_from_string(day) #.add_days(1)
    
    # Select the legs of the instrument
    
    legs = ins.legs()
    
    for l in legs:
	if request == 'Fixed':
    	    if l.type == 'Fixed':
    	    	daycount_method = l.daycount_method
		ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
    	    	rate = l.fixed_rate
            	cashflows = l.cash_flows()
		#1
		WholeCashflow = 0
		InterestPerDay = 0
		AccruedCashflow = 0
		cfwnbr = 0
		#
		for cf in cashflows:
		    #print cf.cfwnbr, 'Here', date
		    if (cf.start_day<date) and (cf.pay_day>=date):
			
			Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    	#2
			WholeCashflow = WholeCashflow + rate*cf.start_day.days_between(cf.end_day, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    	InterestPerDay = InterestPerDay + WholeCashflow/cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	AccruedCashflow = AccruedCashflow + rate*min(cf.start_day.days_between(date, daycount_method), cf.start_day.days_between(cf.end_day, daycount_method))/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    	#
			DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)
    	    	    	cfwnbr = cf.cfwnbr
			#print t.trdnbr, WholeCashflow, cf.cfwnbr, AccruedCashflow, 'Fixed Side',cf.start_day.days_between(date,daycount_method)
		    	#print min(0,1)
		if detail == 'Fixed':
	    	    return -WholeCashflow
		elif detail == 'PerDay':
		    return -InterestPerDay
		elif detail == 'Accrued':
		    return -AccruedCashflow
		elif detail == 'Rate':
		    return rate
		elif detail == 'SeqNo':
		    return cfwnbr
		return 0.0
			    	
        elif request == 'Float':
    	    if l.type == 'Float':
	    	daycount_method = l.daycount_method
	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		cashflows = l.cash_flows()
	    	#1
		WholeCashflow = 0
		InterestPerDay = 0
		AccruedCashflow = 0
		rate = 0
		cfwnbr = 0
		#
		for cf in cashflows:
	    	    if (cf.start_day<date) and (cf.pay_day>=date):
		    	resets = cf.resets()
		    	if resets[0].type == 'Single':
			    rate = resets[0].value + cf.spread
			elif resets[0].type == 'Weighted':
			    rate = AVERate(cf, day)  #SAIRD_Rates.
			elif resets[0].type == 'Weighted 1m Compound':
			    rate = RODRate(t, day) #SAIRD_Rates.
		    	Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    	#2
			WholeCashflow = WholeCashflow + rate*cf.start_day.days_between(cf.end_day, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    	InterestPerDay = InterestPerDay + WholeCashflow/cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	AccruedCashflow = AccruedCashflow + rate*cf.start_day.days_between(date, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    	#
			DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)
			cfwnbr = cf.cfwnbr
	    	    	
    	    	if detail == 'Float':
		    return WholeCashflow
		elif detail == 'PerDay':
		    return InterestPerDay
		elif detail == 'Accrued':
		    return AccruedCashflow
		elif detail == 'Rate':
		    return rate
		elif detail == 'SeqNo':
		    return cfwnbr
		return 0.0
	elif request == 'Option Fixed':
    	    if l.type == 'Cap':
    	    	daycount_method = l.daycount_method
    	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		rate = l.strike
		#print l.strike
            	cashflows = l.cash_flows()
		for cf in cashflows:
    	    	    
		    if (cf.start_day<date) and (cf.pay_day>=date):
			Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    	WholeCashflow = rate*cf.start_day.days_between(cf.end_day, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    	InterestPerDay = WholeCashflow/cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	AccruedCashflow = rate*cf.start_day.days_between(date, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    	DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	
		    	if detail == 'Fixed':
	    		    return -WholeCashflow
			elif detail == 'PerDay':
			    return -InterestPerDay
			elif detail == 'Accrued':
			    return -AccruedCashflow
			elif detail == 'Rate':
			    print 'Rate', rate
			    return rate
			elif detail == 'SeqNo':
			    return cf.cfwnbr
		return 0.0
	    elif l.type == 'Floor':
    	    	daycount_method = l.daycount_method
    	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		rate = l.strike
		#print l.strike
            	cashflows = l.cash_flows()
		for cf in cashflows:
    	    	    
		    if (cf.start_day<date) and (cf.pay_day>=date):
			Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    	WholeCashflow = rate*cf.start_day.days_between(cf.end_day, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    	InterestPerDay = WholeCashflow/cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	AccruedCashflow = rate*cf.start_day.days_between(date, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    	DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)
	    	    
		    	if detail == 'Fixed':
			    return WholeCashflow
			elif detail == 'PerDay':
			    return InterestPerDay
			elif detail == 'Accrued':
			    return AccruedCashflow
			elif detail == 'Rate':
			    return rate
			elif detail == 'SeqNo':
			    return cf.cfwnbr
		return 0.0
        elif request == 'Option Float':
    	    if l.type == 'Cap':
		daycount_method = l.daycount_method
	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		cashflows = l.cash_flows()
	    	for cf in cashflows:
	    	    if (cf.start_day<date) and (cf.pay_day>=date):
		    	resets = cf.resets()
		    	rate = resets[0].value + cf.spread
		    	Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    	WholeCashflow = rate*cf.start_day.days_between(cf.end_day, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    	InterestPerDay = WholeCashflow/cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	AccruedCashflow = rate*cf.start_day.days_between(date, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    	DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	
		    	if detail == 'Float':
			    return WholeCashflow
			elif detail == 'PerDay':
			    return InterestPerDay
			elif detail == 'Accrued':
			    return AccruedCashflow
			elif detail == 'Rate':
			    return rate
			elif detail == 'SeqNo':
			    return cf.cfwnbr
		return 0.0
	    elif l.type == 'Floor':
		daycount_method = l.daycount_method
	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		cashflows = l.cash_flows()
	    	for cf in cashflows:
	    	    if (cf.start_day<date) and (cf.pay_day>=date):
		    	resets = cf.resets()
		    	rate = resets[0].value + cf.spread
		    	Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    	WholeCashflow = rate*cf.start_day.days_between(cf.end_day, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    	InterestPerDay = WholeCashflow/cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	AccruedCashflow = rate*cf.start_day.days_between(date, daycount_method)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    	DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)
	    	    	
		    	if detail == 'Float':
			    return -WholeCashflow
			elif detail == 'PerDay':
			    return -InterestPerDay
			elif detail == 'Accrued':
			    return -AccruedCashflow
			elif detail == 'Rate':
			    return rate
			elif detail == 'SeqNo':
			    return cf.cfwnbr
		return 0.0





def RODRate(t,date,*rest):
    
    # Select Instrument related to the trade for determining resets
    ins = ael.Instrument.read('insaddr=%d' % t.insaddr.insaddr) #trd.insaddr.insaddr)
    
    # Select legs associated with the instrument
    lgs = ins.legs()
    
    # Convert date
    
    day_used = ael.date_from_string(date)
    
    # Select the floating leg
    
    for l in lgs:
    	if l.type == 'Float':
    	    leg = l
	    print l

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
    	#print sorted
    
    
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
	    	average = average*(1+temp/36500*days[i])
		i = i + 1
	return (average-1)*36500/numdays
	


def AVERate(csh,date,*rest):
    
    cshflw = ael.CashFlow.read('cfwnbr=%d'%csh.cfwnbr)
    day_used = ael.date_from_string(date)	     
    resets = cshflw.resets()
    start_day = cshflw.start_day
    end_day = cshflw.end_day
    
    # Create a new list containing all days (weekends included)
    yc = ael.YieldCurve.read('yield_curve_name=%s' % "ZAR-SWAP")
    
    min = start_day
    sorted = []
    	
    while min != end_day:
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
    #print sorted
    
    
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
