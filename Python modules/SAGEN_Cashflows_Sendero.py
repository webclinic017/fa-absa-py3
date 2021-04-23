'''NextCashflow: last updated on Fri Oct 29 11:02:08 2004. Extracted by Stowaway on 2004-11-01.'''
#   Date	:   August 2004	    	    	    	    	    	    #
#   Description	:   Finds the next cashflow given the legnbr  		    #
#    	    	    and the report date.  Returns fixed_amount	    	    #
#   	    	    if flag = 0 and pay_day if flag = 1     	    	    #
#   	    	    if flag = 2 return a string of all next paydays    	    #
#  Changes 
#
#  Developer : Jaysen Naicker,=
#  Purpose   : [Change rate, average balance and interest calcualtions to be more accurate]
#  Date      : 07-07-2011
#  Department and Desk : PCG Fixed income (NLD)]
#  Requester           : Haroon Mansoor
#  CR Number           : 705440

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
    value = ''
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):
    	pay_day = list[count][0]
	if pay_day > sdate:
#	    print 'Next cashflow pay_day', pay_day
    	    if flag == 0:
		value = (str)(list[count][2])
    	    	return value
	    elif flag == 1:
		value = (str)(list[count][0])
    	        return value		    
            elif flag == 2:
                if value == '':
                    value = (str)(list[count][0])
                else:
                    if value.find((str)(list[count][0])) == -1:
                        value = value + ',' + (str)(list[count][0])
                    else: value = value
    	        #return value		    
            else:
                return value
	count = count + 1
	
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
            if c.type <> 'Fixed Amount':
                tup = (c.start_day, c.end_day, c.cfwnbr)
    #	print tup
                list.append(tup)
            
        list.sort()
        
        count = 0
        if flag in (0, 3, 4, 5, 6, 8, 9):
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
            amount = cf.fixed_amount * 1.00
            fwd_rate = cf.forward_rate()* 1.00
            flt_rate_factor = cf.float_rate_factor * 1.00
            period_rate = cf.period_rate(start_day, end_day) * 1.00
            pay_day = cf.pay_day
            if l.payleg:
                nom = -1.0 * cf.nominal_amount()  #should be multiplied by (t.quantity/i.index_factor) in the calling function
            else:
                nom = cf.nominal_amount()
            
            if (start_day < sdate and end_day <= sdate):

    #	    print 'Current cashflow start_day', start_day
                if flag == 0:
                    value = (str)(amount)
                    
                elif flag == 1:
                    if start_day == None:
                        value =  '0001-01-01'
                    else:
                        value = (str)(start_day)
          		    
                elif flag == 2:
                    if end_day == None:
                        value =  '0001-01-01'
                    else:
                        value = (str)(end_day)
  
                elif flag == 3:
                    value = (str)(fwd_rate * flt_rate_factor)
    
                elif flag == 4:
                    if start_day == None:
                        start_day = l.start_day
                    if end_day == None:
                        end_day = l.insaddr.exp_day    
                    value = (str)(start_day.days_between(end_day, 'Act/365'))

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







#   Date	:   August 2006 	    	    	    	     	    #
#   Description	:   Counts the number of future cashflows given the legnbr  #
#    	    	    and the report date.    	    	    	    	    #
#    	    	    if flag = 1 returns count of all cashflows 	    	    #
#		       flag = 2 returns count of Fixed cashflows     	    #
#		       flag = 3 returns count of Float cashflows    	    #
#		       flag = 4 returns count of Other cashflows    	    #

def CountCF(temp, lnbr, ddate, flag, *rest):
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    
    CountFixed = 0
    CountFloat = 0
    CountOther = 0
    
    
    for c in cashf:
    	if c.type == 'Fixed Rate':
	    CountFixed = CountFixed + 1
        elif c.type == 'Float Rate':
            CountFloat = CountFloat + 1
        else:
            CountOther = CountOther + 1
            
    if flag == 1:
	return (str)(CountFixed + CountFloat + CountOther)
    elif flag == 2:
    	return (str)(CountFixed)
    elif flag == 3:
        return (str)(CountFloat)
    elif flag == 4:
        return (str)(CountOther)
    else:
    	return (str)(CountFixed + CountFloat + CountOther)    
    
    






#   Date	:   April 2006		    	    	    	     	      #
#   Description	:   Calls one of the cashflow functions given  	    	      #
#   	    	    the instrument and date and flag and name of function (f) #
#    	    	    Calls for all legs and gets the max.    	    	      #
#    	    	    Flag is dependend on the cashflow function called.        #

def GetCashflow_Ins(temp, i, ddate, flag, f, *rest):
    legs = i.legs()
    count = 1
    mindate = '0001-01-01'
    for l in legs:
    	if f == 'NextCF':
	    d1 = NextCF(0, l.legnbr, ddate, flag)
	elif f == 'CurrentCF':
	    d1 = CurrentCF(0, l.legnbr, ddate, flag)	    

	if count == 1:
	    mindate = d1
	elif d1 <= mindate:
	    mindate = d1
	count = count + 1
	
    return mindate


#   Date	:   November 2007           	    	    	     	      #
#   Description	:   Returns Yes if the leg has a cashflow, else No 	      #

def NoCfwnbr(temp,l,*rest):
    
    if l.cash_flows().members() == []:
        return 'No'
    else:
        return 'Yes'


import acm
        
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def interestRateOnDate(trdnbr, date):
    '''
    InterestRateOnDate is calculated as the SUM of all Call Fixed Rate Adjustable reset value's where "date >= cf.StartDate AND date < cd.EndDate"
    '''

    t = acm.FTrade[trdnbr]
    ins = t.Instrument()

    result = 0
    out = ('0001-01-01', '0001-01-01', 0.0, 0.0)
    
    for l in ins.Legs():
        for cf in l.CashFlows():
            if  date >= cf.StartDate() and date < cf.EndDate():
                if l.LegType() == 'Float':
                    for r in cf.Resets():
                        if r.StartDate() and r.EndDate():
                            if date >= r.StartDate() and date < r.EndDate():
                                result = r.FixingValue()
                                calc = cf.Calculation()
                                nom =  float(calc.Nominal(cs, t).Value().Number())
                                out = (cf.StartDate(), cf.EndDate(), result, nom)
                        else:
                            if date >= cf.StartDate() and date < cf.EndDate():
                                result = r.FixingValue()
                                calc = cf.Calculation()
                                nom =  float(calc.Nominal(cs, t).Value().Number())
                                out = (cf.StartDate(), cf.EndDate(), result, nom)
                            
                else:
                    if cf.CashFlowType()  <> 'Fixed Amount':
                        calc = cf.Calculation()
                        nom =  float(calc.Nominal(cs, t).Value().Number())
                        out = (cf.StartDate(), cf.EndDate(), l.FixedRate(), nom)

    return out
    
def Get_MostCommonRateData(temp, trdnbr, start, end, flag , *rest):
    '''
    Calculates the Interest rate for each day in the period, then returns average rate per day
    '''
    
    try:
        if flag in (3, 4) :
            default = 0.0
        else:
            default = '0001-01-01'
            
        out = default    
        #ins = acm.FInstrument[ins]
        
        nsTime = acm.Time()
        sdate = nsTime.AsDate(start)
        date =  nsTime.AsDate(start)
        end = nsTime.AsDate(end)
  
        
        currSDate, currEDate, currIR, nom = interestRateOnDate(trdnbr, date)
   
        cnt = 1
        if  date < end:
            dailyRate = {}
            while date < end:
                ir_data = interestRateOnDate(trdnbr, date)    
     
                dr_amount = ir_data[2]
                if dr_amount <> 0:
                    if dr_amount <> currIR or currSDate <> ir_data[0] or currEDate <> ir_data[1]:
                       currSDate, currEDate, currIR, nom = ir_data
                       cnt = 1
                    dailyRate[ir_data] = cnt
                    cnt = cnt + 1
                date = nsTime.DateAddDelta(date, 0, 0, 1)
            cnt = 0
            d_rate = 0.0
            
            if flag <> 4:
                for entry in dailyRate:
                    if dailyRate[entry] > cnt:
                        cnt = dailyRate[entry]
                        out = entry[flag-1]
            else:
                for entry in dailyRate:
                    cnt = dailyRate[entry]
                    out = out + entry[3]/abs(acm.Time.DateDifference(sdate, end)) * cnt
            
            return out
        else:
            return default
    except:
        return default



#main
#l = 93261

#temp, lnbr, ddate, qty, ins, flag, *rest
#i = ael.Trade[758816].insaddr
#print GetCashflow_Ins(0, i, '2006-06-30', 4, 'CurrentCF')
#l = 176021
#print CurrentCF(0, l, '2006-06-22', 4)
