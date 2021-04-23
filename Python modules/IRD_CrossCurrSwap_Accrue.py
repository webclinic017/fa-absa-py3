import ael, string

def accrued_interest(t,sday,eday, request,reqCurr, *rest):

#works for cross currency swaps - ie two float legs. the last parameter sent(reqCurr) is teh currency of the leg whose accr int will be returned

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
    FloatAccInt = 0
    FixedAccInt = 0
    AccruedCashflow = 0
    InterestPerDay = 0
    FloatInterestPerDay = 0
    FixedInterestPerDay = 0
    FDIFixedAccInt = 0
    FDI_Nominal = 0
    FDI_days = 0
    FDI_cf = 0
    FDI_SUMCF = 0
   
    # Select the legs of the instrument
    legs = ins.legs()
    
    for l in legs:
  
    	  
    	if l.type == 'Float' and l.curr.insid == reqCurr :
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
                    rate = (cf.period_rate(cf.start_day, edate)) + cf.float_rate_offset    #sday
                    
		    
		    
    	    	    days = cf.start_day.days_between(cf.end_day, daycount_method) + 1
		    Nominal = l.nominal_amount() 
	    	    WholeCashflow = -rate*days/DaysInYear*l.nominal_amount() 
	    	    InterestPerDay = WholeCashflow/days
	    	    AccruedCashflow = -rate*(ddate.days_between(edate, daycount_method)+1)/DaysInYear* l.nominal_amount() 
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
#		    print 'InterestPerDay Float ', InterestPerDay
#		    print
#		    print 'AccruedCashflow ', AccruedCashflow
#		    print 
#		    print 'DaysInPeriod ', DaysInPeriod
#   		    print 
#		    print 'Rate ', rate

		    accint = accint + AccruedCashflow

                    FloatInterestPerDay = FloatInterestPerDay + InterestPerDay
                    InterestPerDay = 0

	FloatAccInt = FloatAccInt + accint
        accint = 0    

#   print '\n\n\n'
    if request == 'IntON':
    	return FloatInterestPerDay
    elif request == 'Float':
    	return FloatAccInt
    elif request == 'Nominal':
    	return Nominal
    else:
    	return FloatAccInt
#    	return accint
	
def legs_curr(t,lnbr, *rest):
    #displays a trade's legs' currencies.
    return t.insaddr.legs()[lnbr-1].curr.insid
    
