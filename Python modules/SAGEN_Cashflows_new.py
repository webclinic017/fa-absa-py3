'''NextCashflow: last updated on Fri Oct 29 11:02:08 2004. Extracted by Stowaway on 2004-11-01.'''
#   Date	:   August 2004	    	    	    	    	    	    #
#   Description	:   Finds the next cashflow given the legnbr  		    #
#    	    	    and the report date.  Returns fixed_amount	    	    #
#   	    	    if flag = 0 and pay_day if flag = 1       	    	    #
#   	    	    and if flag = 2 return cf.start_day     	    	    #
 
import ael

def NextCF(temp, lnbr, ddate, flag, *rest):
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    list = []
    for c in cashf:
    	tup = (c.pay_day, c.cfwnbr, c.fixed_amount, c.start_day)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    value = '0'
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):
    	pay_day = list[count][0]
	count = count + 1
	if pay_day > sdate:
#	    print 'Next cashflow pay_day', pay_day
    	    if count == len(list):
	    	return 'last cashflow'
	    elif flag == 0:
		value = (str)(list[count][2])
    	    	return value
	    elif flag == 1:
		value = (str)(list[count][0])
    	        return value		    
    	    elif flag == 2:
	    	value = (str)(list[count][3])
		return value	    
	    else:
		value = (str)(0)
    	        return value
#	count = count + 1		    
	
	
    return value
    
	
	





#   Date	:   August 2004	    	    	    	    	    	    #
#   Description	:   Finds the previous cashflow given the legnbr  	    #
#    	    	    and the report date.  Returns fixed_amount	    	    #
#   	    	    if flag = 0 and pay_day if flag = 1     	    	    #
 
def PreviousCF(temp, lnbr, ddate, flag, *rest):
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    list = []
    for c in cashf:
    	tup = (c.pay_day, c.cfwnbr, c.fixed_amount)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    value = '0'
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):
    	pay_day = list[count][0]
	if pay_day > sdate:
#	    print 'Previous cashflow pay_day', list[count-1][0]
    	    if flag == 0:
		value = (str)(list[count-1][2])
    	    	return value
	    else:
		value = (str)(list[count-1][0])
    	        return value		    
	count = count + 1
	
    return value







#   Date	:   October 2004	    	    	    	     	    #
#   Description	:   Finds the current cashflow given the legnbr  	    #
#    	    	    and the report date.    	    	    	    	    #
#    	    	    if flag = 0 returns fixed_amount 	    	    	    #
#		       flag = 1 returns start_day   	    	    	    #
#		       flag = 2 returns end_day     	    	    	    #
#   	    	       flag = 3 returns rate (forward rate * float factor   #
#   	    	    	      for PNCD of FRN    	    		    #   	    	    
#   	    	       flag = 4 returns the days in the cf period   	    #		
#   	    	       flag = 5 returns the forward_rate for current cf     #
#   	    	       flag = 6 returns the cfwnbr  	    	    	    #	
#   	    	       flag = 7 returns the current cashflows reset value   #

def CurrentCF(temp, lnbr, ddate, flag, *rest):
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    list = []
    for c in cashf:
    	tup = (c.start_day, c.end_day, c.cfwnbr)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    value = ''
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):
       	
	cf = ael.CashFlow[list[count][2]]
	start_day = list[count][0]
	end_day = list[count][1]
	amount = cf.fixed_amount
	fwd_rate = cf.forward_rate()
	flt_rate_factor = cf.float_rate_factor
	
    	if (start_day <= sdate and end_day > sdate):
#	    print 'Current cashflow start_day', start_day
    	    if flag == 0:
		value = (str)(amount)
    	    	return value
	    elif flag == 1:
	    	if start_day == None:
		    return '0001-01-01'
		else:
		    value = (str)(start_day)
   	            return value		    
	    elif flag == 2:
	    	if end_day == None:
		    return '0001-01-01'
		else:
		    value = (str)(end_day)
   	            return value
    	    elif flag == 3:
    	    	value = (str)(fwd_rate * flt_rate_factor)
		return value
	    elif flag == 4:
	    	if start_day == None:
		    start_day = l.start_day
		if end_day == None:
		    end_day = l.insaddr.exp_day    
	    	value = (str)(start_day.days_between(end_day, 'Act/365'))
		return value
	    elif flag == 5:
	    	value = (str)(cf.forward_rate())
		return value
    	    elif flag == 6:
	    	value = (str)(cf.cfwnbr)
		return value
	    elif flag == 7:
    	    	resets = cf.resets()
		for r in resets:
		    value = (str)(r.value)
		return value

	    else:
	    	return ''    

    	count = count + 1
	
    return value
    
    
    



#   Date	:   October 2004	    	    	    	     	    #
#   Description	:   Finds the current cashflow given the legnbr  	    #
#    	    	    and the report date.    	    	    	    	    #
#    	    	    if flag = 3 returns sum of all fixed amounts to ddate   #

def CurrentAnnuityCF(temp, lnbr, ddate, qty, ins, flag, *rest):
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    list = []
    for c in cashf:
    	if c.type == 'Fixed Amount':
	    tup = (c.pay_day, c.cfwnbr, c.fixed_amount, c.projected_cf() * qty)
#	    print tup
	    list.append(tup)
	
    list.sort()

    sum_nom = 0
    count = 0
    notequal = 0
    value = '0'
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):

	pay_day = list[count][0]    	
    	start_day = list[count][1]
	end_day = list[count][2]
	amount = list[count][3]

	if pay_day < sdate:
#	    print count, pay_day, amount
    	    sum_nom = sum_nom + amount
	    end = end_day
	else:
	    if notequal == 0:
	    	currentCF = amount
	    notequal = notequal + 1
	    
    	count = count + 1
	

    if ins == 'SD' or ins == 'SL' or ins == 'SFLI':
#    	print 'CurrentCF', currentCF
    	sum_nom = sum_nom + currentCF
#    	print 'Inc', sum_nom
    
    elif ins == 'Annuity' or ins == 'RDL' or ins == 'FDI':
    	pass
#	print 'Exc', sum_nom
    
    else:
    	sum_nom = 0
#	print 'None'
	
	

    if flag == 3:
	return (str)(sum_nom)

    elif flag == 2:
    	if end_day == None:
	    return '0001-01-01'
	else:
	    value = (str)(end_day)
   	    return value
    else:
    	return ''    





#main
#   	    	    if flag = 0 and pay_day if flag = 1       	    	    #
#   	    	    and if flag = 2 return cf.start_day     	    	    #
 

#l = 99175
#print NextCF(0, l, '2005-04-05', 2)
#print
#print CurrentCF(0, l, '2005-04-05', 1)
#temp, lnbr, ddate, qty, ins, flag, *rest

	 

