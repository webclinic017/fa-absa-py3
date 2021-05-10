'''NextCashflow: last updated on Fri Oct 29 11:02:08 2004. Extracted by Stowaway on 2004-11-01.'''
#   Date	:   August 2004	    	    	    	    	    	    #
#   Description	:   Finds the next cashflow given the legnbr  		    #
#    	    	    and the report date.  Returns fixed_amount	    	    #
#   	    	    if flag = 0 and pay_day if flag = 1     	    	    #
 
import ael

def NextCF(temp, lnbr, ddate, flag, *rest):
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
#	    print 'Next cashflow pay_day', pay_day
    	    if flag == 0:
		value = (str)(list[count][2])
    	    	return value
	    else:
		value = (str)(list[count][0])
    	        return value		    
	count = count + 1
	
    return value
    
    	
	





#   Date	:   August 2004	    	    	    	    	    	    #
#   Description	:   Finds the previous cashflow given the legnbr  		    #
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
#    	    	    if flag = 0 return fixed_amount 	    	    	    #
#		       flag = 1 returns start_day   	    	    	    #
#		       flag = 2 returns end_day     	    	    	    #
#   	    	       flag = 3 returns sum of all fixed amounts to ddate   #

def CurrentCF(temp, lnbr, ddate, qty, ins, flag, *rest):
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
	else:
	    if notequal == 0:
	    	currentCF = amount
	    notequal = notequal + 1
	    
    	count = count + 1
	

    if ins == 'SD' or ins == 'SL':
#    	print 'CurrentCF', currentCF
    	sum_nom = sum_nom + currentCF
#    	print 'Inc', sum_nom
    
    elif ins == 'Annuity':
    	pass
#	print 'Exc', sum_nom
    
    else:
    	sum_nom = 0
#	print 'None'
	
    return (str)(sum_nom)		    


'''
	    elif flag == 3:
		if ins == 'SD' or ins == 'SL':
		    print 'Inc', sum_nom
		elif ins == 'Annuity':
		    sum_nom = sum_nom - lastamount
		    print 'Exc', sum_nom
		else:
		    sum_nom = 0
		    print 'None'
	        value = (str)(sum_nom)		    
   	        return value		
	    else:
	        return '' 
	else:
	#inclusive
	    if list[count][5] == 'Fixed Amount':
	    	print count, list[count][6]
	    	sum_nom = sum_nom + list[count][6]
		lastamount = list[count][6]
	    	
'''	    


#    return value
    	




#main
#l = 104623
#print PreviousCF(0, l, '2005-01-20', 1)

	 

