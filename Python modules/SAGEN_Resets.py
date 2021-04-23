
"""-----------------------------------------------------------------------------
PURPOSE                 :  General Reset Functions
DEPATMENT AND DESK      :  
REQUESTER               :   
DEVELOPER               :  Unknown
CR NUMBER               :  713436
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no   Developer               Description
--------------------------------------------------------------------------------
                        Unknown                 Initial Implementation
2014-02-18  1752210     Rohan vd Walt           Added resetEstimateEnd() for credit desk column
"""

import ael, acm, NamespaceTimeFunctions


def resetEstimateEnd(cashFlowMoneyFlow):
    '''
    Author: vanrohan
    Given FReset, determine "Estimate End" value (seen in cashflow table when looking at floating cashflow)
    '''
    try:
        reset = cashFlowMoneyFlow.Reset()
        rLeg = reset.Leg()
        periodCount = rLeg.ResetPeriodCount()
        periodUnit = rLeg.ResetPeriodUnit()[0]          #Only first character required for DateAddDeltaType function
        if periodCount == 0 and periodUnit == 'D':      #If reset period is the default '0d' value, then use the Rolling Period as per documentation and FA behaviour
            periodCount = rLeg.RollingPeriodCount()
            periodUnit = rLeg.RollingPeriodUnit()[0]
        rCal = rLeg.ResetCalendar().Name()
        rDayMeth = rLeg.ResetDayMethod()
    except Exception as e:
        return ''
    return NamespaceTimeFunctions.DateAddDeltaType(None, reset.StartDate(), periodCount, periodUnit, rCal, rDayMeth)


#   Date	:   September 2005	    	    	    	     	    #
#   Description	:   Finds the current reset given the legnbr  	    	    #
#    	    	    and the report date.    	    	    	    	    #
#    	    	    if flag = 0 returns value	 	    	    	    #
#		       flag = 1 returns start_day   	    	    	    #
#		       flag = 2 returns end_day     	    	    	    #
#   	    	       flag = 3 returns day     	    		    #   	    	    
#   	    	       flag = 4 returns reset no     	    		    #   	    	    

def CurrentReset(temp, lnbr, ddate, flag, *rest):
    l = ael.Leg[lnbr]
    reset  = l.resets()
    list = []
    for r in reset:
    	tup = (r.cfwnbr.start_day, r.cfwnbr.end_day, r.resnbr, r.day)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    if flag == 0:
        value = '0'
    else:
        value = '1900-01-01'
        
    sdate = ael.date_from_string(ddate)
    
    while count < len(list):
    	
	rs = ael.Reset[list[count][2]]
	start_day = list[count][0]
	end_day = list[count][1]
	day = list[count][3]
	val = rs.value
#	fwd_rate = cf.forward_rate()
#	flt_rate_factor = cf.float_rate_factor
	
    	if (start_day <= sdate and end_day > sdate):
	    #print 'Current reset start_day', start_day
    	    if flag == 0:
		value = (str)(val)
    	    	return value
	    elif flag == 1:
	    	if start_day == None:
		    return '1900-01-01'
		else:
		    value = (str)(start_day)
   	            return value		    
	    elif flag == 2:
	    	if end_day == None:
		    return '1900-01-01'
		else:
		    value = (str)(end_day)
   	            return value
    	    elif flag == 3:
    	    	value = (str)(day)
		return value
            elif flag == 4:
                value = (str)(rs.resnbr)
                return value
	    else:
	    	return ''    

    	count = count + 1
	
    return value
    
    
#   A trade is needed for calculations in the Money Flow Sheet even though #
#   no trade is needed for retrieving a fixing estimate in theory.        #

def resetForwardRate( resetNbr, tradeNbr ):
    context    = acm.GetDefaultContext()
    sheetType  = 'FMoneyFlowSheet'
    columnName = 'Cash Analysis Fixing Estimate'
    calcSpace  = acm.Calculations().CreateCalculationSpace( context, sheetType )
    reset      = acm.FReset[ resetNbr ]
    trade      = acm.FTrade[ tradeNbr ]
    resetAndTrades = acm.Risk().CreateResetAndTrades( reset, trade )
    forwardRateDenominatedValue = calcSpace.CalculateValue( resetAndTrades, columnName ).Value()
    try:
        forwardRate = forwardRateDenominatedValue.Number() * 100.0
    except:
        forwardRate = 0.0
    return forwardRate
 
 
#   Date	:   September 2005	    	    	    	     	    #
#   Description	:   Finds the first reset (given the legnbr)  	    	    #
#    	    	    after a given date.    	    	    	    	    #
#    	    	    if flag = 0 returns value	 	    	    	    #
#		       flag = 1 returns start_day   	    	    	    #
#		       flag = 2 returns end_day     	    	    	    #
#   	    	       flag = 3 returns day     	    		    #   	    	    
#   	    	       flag = 4 returns reset no     	    		    #   	    	    
#   	    	       flag = 5 returns reset type     	    		    #   	    	    

def FirstResetAfter(temp, lnbr, ddate, tradeNbr, flag, *rest):
    l = ael.Leg[lnbr]
    reset  = l.resets()
    list = []
    for r in reset:
    	tup = (r.cfwnbr.start_day, r.cfwnbr.end_day, r.resnbr, r.day)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    if flag == 0:
        value = '0'
    else:
        value = '1900-01-01'
    
    try:
    	sdate = ael.date_from_string(ddate)
    except:
	sdate = ddate
	
    while count < len(list):
	rs = ael.Reset[list[count][2]]
	start_day = list[count][0]
	end_day = list[count][1]
	day = list[count][3]
	val = rs.value

#	if l.start_day < sdate:
	if start_day >= sdate:
#	    print 'Reset start_day', start_day
	    if flag == 0:
                value = str(rs.parent().forward_rate())
                #reset.forward_rate() does not work in front 4.3
	    	#value = (str)(rs.forward_rate())
    	    	return value
	    elif flag == 1:
	    	if start_day == None:
		    return '1900-01-01'
		else:
		    value = (str)(start_day)
   	            return value		    
	    elif flag == 2:
	        if end_day == None:
		    return '1900-01-01'
		else:
		    value = (str)(end_day)
   	            return value
    	    elif flag == 3:
    	        value = (str)(day)
		return value
            elif flag == 4:
                value = (str)(rs.resnbr)
                return value	
            elif flag == 5:
                value = (str)(rs.type)
                return value		
	    else:
	        return ''

    	count = count + 1
	
    return value


#   Date	:   December 2005	    	    	    	     	    #
#   Description	:   Finds the requested reset number given the legnbr  	    #
#    	    	    and the report date.    	    	    	    	    #
#    	    	    if flag = 0 returns value	 	    	    	    #
#		       flag = 1 returns start_day   	    	    	    #
#		       flag = 2 returns end_day     	    	    	    #
#   	    	       flag = 3 returns day     	    		    #   	    	    
def ReturnReset(temp, lnbr, ddate, flag, resetnbr, *rest):
    l = ael.Leg[lnbr]
    reset  = l.resets()
    list = []
    for r in reset:
    	tup = (r.start_day, r.end_day, r.resnbr, r.day, r.value)
#	print tup
	list.append(tup)
    	
    list.sort()
#    print list
    
    if resetnbr == 1 or resetnbr == 0:
    	resetnbr = 0
    elif resetnbr > len(list):
    	return ''
    else:
    	resetnbr = resetnbr - 1 


    start_day = list[resetnbr][0]
    end_day = list[resetnbr][1]


    if flag == 0:
    	value = (str)(list[resetnbr][4])
    	return value
    elif flag == 1:
    	if start_day == None:
	    return '0001-01-01'
	else:
	    value = (str)(list[resetnbr][0])
   	    return value		    
    elif flag == 2:
    	if end_day == None:
	    return '0001-01-01'
	else:
	    value = (str)(list[resetnbr][1])
    	    return value
    elif flag == 3:
    	value = (str)(list[resetnbr][3])
#	print resetnbr, value
#	print
	return value
    else:
    	return ''    


#   Date	:   November 2006                                           #
#   Description	:   Fixs a reset given the legnbr, value & report date.     #
#    	    	    if flag = 0 fixes current reset       	    	    #
#		       flag = 1 fixes FirstRestAfter the given date  	    #
def FixReset(temp, i, ddate, value, flag, *rest):

    if flag == 0:
        r = CurrentReset(temp, i.legs()[0].legnbr, ddate, 4)
    else:
        r = FirstResetAfter(temp, i.legs()[0].legnbr, ddate, 4)
            
    res_clone = ael.Reset[(int)(r)].clone()
    res_clone.value = (float)(value)
    
    try:
        res_clone.commit()
        #print 'Fixing of reset successful'
        return 'Success'
    except:
        #print 'Error fixing reset'
        return 'Error'      
    

#   Date	:   November 2007           	    	    	     	      #
#   Description	:   Returns Yes if the cashflow has a reset, else No 	      #

def NoReset(temp,c,*rest):
    
    if c.resets().members() == []:
        return 'No'
    else:
        return 'Yes'
