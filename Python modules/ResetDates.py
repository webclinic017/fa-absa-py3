'''ResetDates: last updated on Fri Oct 22 16:01:57 2004. Extracted by Stowaway on 2004-11-01.'''
#   Created by 	:   Aaeda Salejee   	    	    	    	    	    	    #
#   Date	:   April 2004	    	    	    	    	    	    	    #
#   Description	:   Finds the previous and next reset dates from the CF payday	    #
#    	    	    given the relevant instrument, cf.pay_day and   	    	    #
#    	    	    flag = 0 for the previous reset date    	    	    	    #
#		    flag = 1 for the next reset date     	    	    	    #


 
import ael

def ResetDay(temp, i, cf_date, flag, *rest):
    
    #initialize previous and next dates
    prevday = ael.date_from_string('1900-01-01', '%Y-%m-%d')
    nextday = ael.date_from_string('9999-12-31', '%Y-%m-%d')
    legs = i.legs()
    for l in legs:
    	if l.type in ('Float', 'Cap', 'Floor'):
    	    resets = l.resets()
	    #print resets
	    for r in resets:
	    	#print dir(r)
	    	if (r.day < cf_date and r.day > prevday):
		    prevday = r.day
		else:
		    if (r.day >= cf_date and r.day < nextday):
		    	nextday = r.day
			
			if r.day > ael.date_today():
			    nextamount = 0.0
			else:
			    nextamount = r.value
			    
		    
	    if flag == 0:
	    	return prevday
	    else:
	    	if nextday == ael.date_from_string('9999-12-31', '%Y-%m-%d'):
	    	    return 
		else:
		    #print nextday
		    return nextday






#   Date    	:   October 2004    	    	    	    	    	    #
#   Description :   Returns the current reset date (flag = 0) or	    #
#   	    	    the current reset amount (flag = 1)     	    	    #

def CurrentResetDay(temp, cashf, flag, *rest):

    tdy = ael.date_today()
    list = []
    rday = ''
    rvalue = 0.0
    rtype = 0
    
    resets = cashf.resets()
#    print cashf.cfwnbr
    if len(resets) == 1:
#       print '1', resets[0].day, resets[0].value
	rday = resets[0].day
	rvalue = resets[0].value
	list.append([rday, rvalue])
    else:
        for r in resets:
	    if r.type == 'Weighted':
	        rtype = 1   	
	    if ((r.start_day <= tdy and r.end_day > tdy) or (r.day <= tdy and r.end_day == r.day)):
#	    if ((r.start_day <= tdy and r.end_day > tdy) or r.day <= tdy):
	        #print '2', r.day, r.value
	        rday = r.day
		rvalue = r.value
		list.append([rday, rvalue])
		break
	    else:
	        list.append([r.day, 0.0])
	    
	    
	    
    if cashf.start_day > tdy and rday >= cashf.start_day:
        list.sort()
	try:
	    rday = list[0][0]
	except:
	    rday = '0001-01-01'
	rvalue = 0.0
	
    if flag == 0:
    	if rtype:
    	    return cashf.end_day
    	else:
       	    return rday
    else:
    	if rtype:
    	    if cashf.end_day > tdy:
    	    	return 0.0
    	    else:
    	    	return cashf.period_rate()
    	else:
    	    return rvalue
    	    
    
        
    
    
    
#   Date    	:   October 2004    	    	    	    	    	    #
#   Description :   Returns the reset value calling the above function	    #

def CurrentResetValue(temp, cashf, flag, *rest):
    amount = CurrentResetDay('', cashf, flag)
    return amount    


#   Date    	:   December 2009    	    	    	    	    	    #
#   Description :   Returns the Single reset value for Floating Rate cashflows   #
def getResetValue(temp, cashf, flag, *rest):
    if cashf.type == 'Float Rate':
        for r in cashf.resets():
            if r.type == 'Single':
                return r.value
    else:
        return CurrentResetValue(temp, cashf, flag, *rest)


#   Date	:   July 2004	    	    	    	    	    	    #
#   Description	:   Returns a 0 if found      	    	    	    	    #
def ApartCFDays(temp, i, d_date, *rest):

    legs = i.legs()
    for l in legs:
    	if l.type in ('Float', 'Cap', 'Floor'):
    	    list = []
    	    cashflows = l.cash_flows()
	    for c in cashflows:
	    	tup = (c.pay_day, c.cfwnbr, c.start_day, c.end_day)
		list.append(tup)
	    list.sort()
    	    
	    count = 0 
    	    for t in list:
	    	seqno = t[1]
		cf = ael.CashFlow[seqno]
		if count == 0:
		    prev_end_day = cf.end_day
#		    print 'a', count, cf.cfwnbr, prev_end_day, cf.start_day, cf.end_day
	    	    count = count + 1
		else:
	    	    if cf.start_day != prev_end_day:
		    	#print 'NOT EQUAL'
			d = ael.date_from_string(d_date)
			#print d
			if ((d > prev_end_day) and (d < cf.start_day)):
			    #print seqno
			    return 0
#			print 'b',count, cf.cfwnbr, prev_end_day, cf.start_day, cf.end_day
#		    else:
#		    	print 'EQUAL'
#    	    	    	print 'c', count, cf.cfwnbr, prev_end_day, cf.start_day, cf.end_day
		    prev_end_day = cf.end_day
		    count = count + 1

    return 1

#Brings the latest nominal scaling reset through 
def nominal_Scale(t,*rest):
    list = []
    ins = t.insaddr
    for l in ins.legs():
    	for r in l.resets():
	    if (r.value != 0.0 and r.type == 'Nominal Scaling'):
	    	list.append((r.day, r.value))
    list.sort()
    last = len(list)
    if last == 0:
    	return 0.0
    else:	
    	return list[last-1][1]


#main
#i = ael.Instrument['10yALCO']
#['CASHADJ/EUR/ZAR-EUR/CS']
#i = ael.Instrument['ZAR/IRS/F-JI/030226-050228/11.22']
#c = ael.CashFlow[105682]
#print CurrentResetDay('', c, 0)
#print ApartCFDays('x', i, '2004-11-15')


