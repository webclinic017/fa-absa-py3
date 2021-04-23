import ael



#   Date	:   August 2004	    	    	    	    	    	    #
#   Description	:   Finds the next cashflow given the legnbr  		    #
#    	    	    and the report date.  Returns fixed_amount	    	    #
#   	    	    if flag = 0 and pay_day if flag = 1     	    	    #

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
#                      flag = 6 returns the period rate of the current cf   #
#   	    	       flag = 7 returns the pay day of the current cashflow #
#                      flag = 8 returns the period rate of the current cf   #
#                      flag = 9 returns the nominal of the current cf       #

def CurrentCF(temp, lnbr, ddate, flag, *rest):
    if lnbr == None:
        return '0.00'
    else:
        l = ael.Leg[lnbr]
        cashf = l.cash_flows()
        list = []
        for c in cashf:
            if c.type != 'Fixed Amount':
                tup = (c.start_day, c.end_day, c.cfwnbr)
        	#print tup
                list.append(tup)
            
        list.sort()
    
        count = 0
        if flag in (8, 9):
            value = '0.00'
        else:
            value = '0001-01-01'
        
        try:
            sdate = ael.date_from_string(ddate)
        except:
    #       	print '\n argument1 not in string format\n'
            sdate = ddate
        
    
        while count < len(list):
            
            cf = ael.CashFlow[list[count][2]]
            start_day = list[count][0]
            end_day = list[count][1]
            amount = cf.fixed_amount
            fwd_rate = cf.forward_rate()
            flt_rate_factor = cf.float_rate_factor
            period_rate = cf.period_rate(start_day, end_day)
            pay_day = cf.pay_day
            if l.payleg:
                nom = -1.0 * cf.nominal_amount()  #should be multiplied by (t.quantity/i.index_factor) in the calling function
            else:
                nom = cf.nominal_amount()
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
                    value = (str)(period_rate)
                    return value
                elif flag == 7:
                    value = (str)(pay_day)
                    return value		
                elif flag == 8:
                    value = (str)(period_rate)
                    return value		
                elif flag == 9:
                    value = (str)(nom)
                    return value		
                else:
                    return ''    
    
            count = count + 1
            
        return value
    
    return '0.00'   
    	




#main
#l = 39436
#print CurrentCF(0, l, '2004-10-29', 0)

	 


