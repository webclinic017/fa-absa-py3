import ael, string

def accrued_interest(t,day,request,detail,*rest):

    # Select the instrument associated with the trade
    ins = t.insaddr
    date = ael.date_from_string(day).add_days(1)
    print date, 'Date Used'
    # Select the legs of the instrument
    #if request == 'Fixed':
    legs = ins.legs()
    
    for l in legs:
	if request == 'Fixed':
    	    if l.type == 'Fixed':
    	    	daycount_method = l.daycount_method
		ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
    	    	rate = l.fixed_rate
            	cashflows = l.cash_flows()
		for cf in cashflows:
		    if (cf.start_day<date) and (cf.end_day>=date):
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
			    return rate
			elif detail == 'SeqNo':
			    return cf.cfwnbr
		return 0.0
			    	
        elif request == 'Float':
    	    if l.type == 'Float':
	    	daycount_method = l.daycount_method
	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		cashflows = l.cash_flows()
	    	for cf in cashflows:
	    	    if (cf.start_day<date) and (cf.end_day>=date):
		    	resets = cf.resets()
		    	if resets[0].type == 'Single':
			    rate = resets[0].value + cf.spread
			elif resets[0].type == 'Weighted':
			    rate = AVERate(cf, day)  #SAIRD_Rates.
			elif resets[0].type == 'Weighted 1m Compound':
			    rate = RODRate(t, day) #SAIRD_Rates.
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
	elif request == 'Option Fixed':
    	    if l.type == 'Cap':
    	    	daycount_method = l.daycount_method
    	    	ln = len(daycount_method)
		DaysInYear = float(daycount_method[ln-3:ln])*100
		rate = l.strike
		print l.strike
            	cashflows = l.cash_flows()
		for cf in cashflows:
    	    	    
		    if (cf.start_day<date) and (cf.end_day>=date):
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
		print l.strike
            	cashflows = l.cash_flows()
		for cf in cashflows:
    	    	    
		    if (cf.start_day<date) and (cf.end_day>=date):
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
	    	    if (cf.start_day<date) and (cf.end_day>=date):
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
	    	    if (cf.start_day<date) and (cf.end_day>=date):
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
    #trd = ael.Trade.read('trdnbr=%d' % t.trdnbr)
    ins = ael.Instrument.read('insaddr=%d' % t.insaddr.insaddr) #trd.insaddr.insaddr)
    
    lgs = ins.legs()
    print lgs
    for l in lgs:
    	if l.type == 'Float':
    	    leg = l
	    print l

    cshflw = leg.cash_flows()
    if len(cshflw) > 1:
    	print "ERROR: ROD with more than two cashflows!"
    else:
    	#print cshflw[0].resets()
    	resets = cshflw[0].resets()
    	start_day = cshflw[0].start_day
    	end_day = cshflw[0].end_day
    	#print start_day, end_day
    	# last to be set equal to the current Overnight Deposit Rate
    
    	# Create a new list containing all days (weekends included)
    	yc = ael.YieldCurve.read('yield_curve_name=%s' % "ZAR-RODS")
	last = 100*yc.yc_rate(start_day, start_day.add_days(1), 'Simple')
	#print last
	min = start_day
    	sorted = []
	#temp = ael.Instrument.read('insid=%s' % "ZAR-JIBAR-ON-DEP")
	#prc = ael.Price.select('insaddr=%d and day=%s' % (temp.insaddr,date))
	#print prc, "Price"
    	
	
	
	while min != end_day: #len(resets) != len(sorted):
       	    for r in resets:
    	    	if r.day == min:
	    	    #print 'Found'
		    if r.value != 0:
		    	sorted.append((r.day, r.value))
		    	last = r.value
			#print 'No Zero'
		    else:
		    	#last = 100*yc.yc_rate(min,min.add_days(1),'Simple')
			last = 0
			sorted.append((r.day, last))
			#print 'Zero'
		    #print 'HERE HERE HERE', min
		    add = 1
		    
    	    # If reset day is a public holiday or weekend then fill as it will not be found 
	    if add == 0:
	    	#print min, 'ADD ZERO'
		#last = 100*yc.yc_rate(min,min.add_days(1),'Simple')
		sorted.append((min, last))
	    	add = 1
	    min = min.add_days(add)
	    add = 0
    	#print min
    	while min < end_day:
    	    sorted.append((min, last))
    	    min = min.add_days(1)
    	print sorted
    
    
    	# Calculate the sum of rates per month and the number of days
    	sum = [0]
    	days = [0]
    	i = 0
    	for r in sorted:
    	    #print r
    	    if sum[0] == 0:
	    	if r[1] != 0:
		    sum[i] = sum[i] + r[1]
	    	    days[i] = days[i] + 1
	    	    last = r[0]
	    else:
	    	if r[0].day_of_month() > last.day_of_month():
	    	    if r[1] != 0:
		    	sum[i] = sum[i] + r[1]
	    	    	days[i] = days[i] + 1
		    	last = r[0]
	    	else:
	    	    i = i + 1
		    sum.append(0)
		    days.append(0)
		    if r[1] != 0:
		    	print 'Here'
		    	sum[i] = sum[i] + r[1]
		    	days[i] = days[i] + 1
		    	last = r[0]
    	#print sum
    	#print days
    	numdays = 0
    	i = 0
    	average = 1
    	for s in sum:
    	    if days[i] > 0:
	    	numdays = numdays + days[i]
    	    
    	    	st1, st2 = string.split(str(sum[i]/days[i]), '.')
	    	#print str(sum[i]/days[i])
	    	if len(st2)>=4:
	    	    if int(st2[3]) >= 5:
		      	temp = round(sum[i]/days[i]+0.0001, 3)
		    	print temp, days[i]
	    	    else:
		    	temp = round(sum[i]/days[i], 3)
		    	print temp, days[i]
	    	else:
	    	    temp = round(sum[i]/days[i], 3)
		    print days[i]
	    	average = average*(1+temp/36500*days[i])
		i = i + 1
	    	print 'Average', average*100000000
    	print days
	print sum
	return (average-1)*36500/numdays
	


def AVERate(csh,date,*rest):	#t,date,cfwno,*rest):
    #trd = ael.Trade.read('trdnbr=%d' % t.trdnbr)
    ##ins = ael.Instrument.read('insaddr=%d' % t.insaddr.insaddr) #trd.insaddr.insaddr)
    
    ##lgs = ins.legs()
    ##print lgs
    ##for l in lgs:
    ##	if l.type == 'Float':
    ##	    leg = l
	    #print l
    
    ##for cf in leg.cash_flows():
    ##	if cf.cfwnbr == cfwno:
	##    csh = cf
    cshflw = ael.CashFlow.read('cfwnbr=%d'%csh.cfwnbr)
    #print dir(cshflw), 'CASHFLOW'
	     
    #cshflw = leg.cash_flows()
    #print cshflw.resets()
    resets = cshflw.resets()
    start_day = cshflw.start_day
    end_day = cshflw.end_day
    #print start_day, end_day
    # last to be set equal to the current Overnight Deposit Rate
    
    # Create a new list containing all days (weekends included)
    yc = ael.YieldCurve.read('yield_curve_name=%s' % "ZAR-SWAP")
    last = 100*yc.yc_rate(start_day, start_day.add_days(1), 'Simple')
    #print last
    min = start_day
    sorted = []
    #temp = ael.Instrument.read('insid=%s' % "ZAR-JIBAR-ON-DEP")
    #prc = ael.Price.select('insaddr=%d and day=%s' % (temp.insaddr,date))
    #print prc, "Price"
    	
    while min != end_day: #len(resets) != len(sorted):
        for r in resets:
    	    if r.day == min:
	        #print 'Found'
		if r.value != 0:
		    sorted.append((r.day, r.value))
		    last = r.value
		    #print 'No Zero'
		else:
		    #last = 100*yc.yc_rate(min,min.add_days(1),'Simple')
		    last = 0
		    sorted.append((r.day, last))
		    #print 'Zero'
		#print 'HERE HERE HERE', min
		add = 1
		    
    	# If reset day is a public holiday or weekend then fill as it will not be found 
	if add == 0:
	    #print min, 'ADD ZERO'
	    #last = 100*yc.yc_rate(min,min.add_days(1),'Simple')
	    sorted.append((min, last))
	    add = 1
	min = min.add_days(add)
	add = 0
    #print min
    while min < end_day:
        sorted.append((min, last))
        min = min.add_days(1)
    #print sorted
    
    
    # Calculate the sum of rates per month and the number of days
    sum = [0]
    days = [0]
    i = 0
    for r in sorted:
        #print r
        if sum[0] == 0:
	    if r[1] != 0:
	    	sum[i] = sum[i] + r[1]
	    	days[i] = days[i] + 1
	    	last = r[0]
	else:
	    if r[0].day_of_month() > last.day_of_month():
	        if r[1] != 0:
		    sum[i] = sum[i] + r[1]
	            days[i] = days[i] + 1
		    last = r[0]
	    else:
	        i = i + 1
		sum.append(0)
		days.append(0)
		if r[1] != 0:
		    sum[i] = sum[i] + r[1]
		    days[i] = days[i] + 1
		    last = r[0]
    #print sum
    #print days
    numdays = 0
    sumresets = 0
    i = 0
    average = 1
    for s in sum:
        numdays = numdays + days[i]
	sumresets = sumresets + sum[i]
    	#if round(sum[i]/days[i]*10000,0)-sum[i]/days[i]*10000<5:
	#	print sum[i]/days[i]*10000, 'SUMMMMMMMMMM'
    #	temp=  round((sum[i]/days[i]*10000+5)/10000,3)
    #   else:
    #   	temp = round(sum[i]/days[i],3)
        st1, st2 = string.split(str(sum[i]/days[i]), '.')
	if len(st2)>=4:
	    if int(st2[3]) >= 5:
	        temp = round(sum[i]/days[i]+0.0001, 3)
		#print temp
	    else:
	        temp = round(sum[i]/days[i], 3)
		#print temp
	else:
	    temp = round(sum[i]/days[i], 3)
	    #print temp
	average = average*(1+temp/36500*days[i])
	#if sum[i]/days[i]*10000>5:
	#	print round((sum[i]/days[i]*10000+5)/10000,3), 'AAAAAA', sum[i]/days[i]
	i = i + 1
	#print 'Average', average*100000000
    #print (average-1)*365/numdays
    #print numdays
    #print ael.Price.columns()
    #print days
    #return (average-1)*36500/numdays
    return round(sumresets/numdays, 3)
