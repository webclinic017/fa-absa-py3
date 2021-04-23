import ael, string

def accrued_interest(t,sday,eday,*rest):

    # Select the instrument associated with the trade
    ins = t.insaddr
    try:
    	sdate = ael.date_from_string(sday)
    except:
#       	print '\n argument1 not in string format\n'
	sdate = sday
	

    try:
    	edate = ael.date_from_string(eday)
    except:
#       	print '\n argument2 not in string format\n'
	edate = eday
    	
	
#    print edate, 'Date Used'
    accint = 0
   
    # Select the legs of the instrument
    legs = ins.legs()
    
    for l in legs:
    	if l.type == 'Fixed':
    	    daycount_method = l.daycount_method
	    ln = len(daycount_method)
	    DaysInYear = float(daycount_method[ln-3:ln])*100
    	    rate = l.fixed_rate
            cashflows = l.cash_flows()
	    for cf in cashflows:
		if (cf.start_day<=edate) and (cf.end_day>edate):
		    if cf.start_day <= sdate:
		    	ddate = sdate
		    else:
		    	ddate = cf.start_day

    	    	    days = cf.start_day.days_between(cf.end_day, daycount_method) + 1
		    Nominal = t.quantity*ins.contr_size*cf.nominal_factor		    
	    	    WholeCashflow = rate*days/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    InterestPerDay = WholeCashflow/days
	    	    AccruedCashflow = rate*(ddate.days_between(edate, daycount_method)+1)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method)


		    if l.payleg == 1:
		    	AccruedCashflow = AccruedCashflow * -1

#		    print
#		    print 'PayLeg ', l.payleg
		    print
    	    	    print 'Nominal ', Nominal
		    print
		    print 'WholeCashflow ', WholeCashflow
		    print
		    print 'InterestPerDay ', InterestPerDay
		    print
		    print 'AccruedCashflow ', AccruedCashflow
#		    print 
#		    print 'DaysInPeriod ', DaysInPeriod
		    
		    accint = accint + AccruedCashflow
		    
    	
    	if l.type == 'Float':
    	    daycount_method = l.daycount_method
	    ln = len(daycount_method)
	    DaysInYear = float(daycount_method[ln-3:ln])*100
	    cashflows = l.cash_flows()
	    for cf in cashflows:
	    	if (cf.start_day<=edate) and (cf.end_day>edate):
		    if cf.start_day <= sdate:
		    	ddate = sdate
		    else:
		    	ddate = cf.start_day		
			
#		    resets = cf.resets()
#		    if resets[0].type == 'Single':
#			rate = resets[0].value + cf.spread
#		    elif resets[0].type == 'Weighted':
#			rate = AVERate(cf,day)      	    #SAIRD_Rates.
#		    elif resets[0].type == 'Weighted 1m Compound':
#			rate = RODRate(t,day)       	    #SAIRD_Rates.
#    	    	    else:
#		    	rate = resets[0].value + cf.spread
		    	
#		    if rate == 0.0:
#		    	rate = cf.period_rate(cf.start_day, cf.end_day)
#			print 'Period Rate AAAAA ', rate
#			#resets[0].value + cf.spread


	    	    rate = (cf.period_rate(cf.start_day, cf.end_day) * cf.float_rate_factor) + cf.float_rate_offset
		    
    	    	    days = cf.start_day.days_between(cf.end_day, daycount_method) + 1
		    Nominal = t.quantity*ins.contr_size*cf.nominal_factor
	    	    WholeCashflow = rate*days/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
	    	    InterestPerDay = WholeCashflow/days
	    	    AccruedCashflow = rate*(ddate.days_between(edate, daycount_method)+1)/DaysInYear*t.quantity*ins.contr_size*cf.nominal_factor
    	    	    DaysInPeriod = cf.start_day.days_between(cf.end_day, daycount_method) 
		    
		    if l.payleg == 1:
		    	AccruedCashflow = AccruedCashflow * -1

#		    print
#		    print 'PayLeg ', l.payleg
#		    print
#   	    	    print 'Nominal ', Nominal
#		    print
#		    print 'WholeCashflow ', WholeCashflow
#		    print
#		    print 'InterestPerDay ', InterestPerDay
#		    print
#		    print 'AccruedCashflow ', AccruedCashflow
#		    print 
#		    print 'DaysInPeriod ', DaysInPeriod
#   		    print 
#		    print 'Rate ', rate

		    accint = accint + AccruedCashflow

    	print '\n\n\n'
    
    return accint

		




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




		
		
	
	
### main ###		
t = ael.Trade[632264]	    	#depo
#[529768]  #swap float/fixed
#[584998]   #FRN


#print
print 'AccInt ', accrued_interest(t, '2005-12-20', '2005-12-21')
#print 'AccInt ', accrued_interest(t, t.value_day, '2006-02-17')
#print 'AccInt ', accrued_interest(t, '2006-10-01', '2005-10-02')

			    	
