import ael

def AveResetAmount(o,t, d, *rest):
    trd = ael.Trade[t]
    day = ael.date_from_string(d)
        
    fdom = day.first_day_of_month()
    ldom = fdom.add_days(fdom.days_in_month()-1)
    
    list = []
    prevDict = {}
    prelist = []
    ins = ael.Instrument[trd.insaddr.insaddr]
    legs = ins.legs()
    for l in legs:
    	if l.type == 'Float':
	    if fdom <= l.start_day:
	    	fdom = l.start_day

	    if ldom >= l.end_day:
	    	ldom = l.end_day
		
	    num = 0
	    daylist = []
	    daysInMonth = fdom.days_between(ldom, 'Act/365') + 1 
	    while num < daysInMonth:
	    	daylist.append(fdom.add_days(num))
		num = num + 1
		
	    cf = l.cash_flows()
    	    resets = cf[0].resets()
    	    #print 'Last day of month:',ldom
	    prevday = fdom.add_months(-1)
	    for r in resets:
	    	if (r.day >= fdom) and (r.day <= ldom):
	    	    list.append([r.day, r.value])
		if (r.day > prevday) and (r.day < fdom):
		    prevDict['%s' %(r.day)] = r.value
    for p in prevDict.keys():
       	prelist.append(ael.date_from_string(p))
    prelist.sort()
       	

#    list.sort()
#    print list
#    return
    temp = 0
    sum = 0
    for i in daylist:
       	for l in list:
	    if l[0] == i:
	    	sum = sum + l[1]
	    	temp = l[1]
		#print i, l[1]
		break
	else:
	    if temp == 0:
	    	temp = prevDict['%s' %(prelist[len(prelist)-1])]
	    #print i, temp
	    sum = sum + temp
    #print 'Sum ', sum
    #print 'Days ', daysInMonth
    return round((sum/daysInMonth), 3)
    return


#main
print AveResetAmount(1, 215480, '2004-08-31')
