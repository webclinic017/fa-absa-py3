import ael
import string
import time
import acm
from datetime import date, timedelta
from at_time import date_today


#Date           Who                     What                                    CR Number
#2008-04-29     Heinrich Cornje         Added functions FirstDayOfMonth and     2701
#2009-11-03     Anwar Banoo             Method getYCName was returning blank for discount curves - was missing the return
#                                       FirstBusinessDay
#2010-02-11     Jaysen Naicker          to Function ASQL_log   log path changed to Y:\\Jhb\Arena\log\log43 instead of \\\\v036syb004001\log\Prime C225315
#2013-08-01     Dusan Fasko             BankingDaysCount function added.        CHNG0001229133
#2014-08-07     Sanele Macanda          prev_weekday function                   CHNG0002184135

global calcSpace
global collect
global collectLimit
calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
collect = 0
collectLimit = 100000

def SACDPrintNCDs(t,request,*rest):
    ins = ael.Instrument.read('insaddr=%d' %t.insaddr.insaddr)
    legs = ins.legs()
    if request == 'margin':
	min = 100
	for l in legs:
	    if l.type == 'Fixed':
	    	cfws = l.cash_flows()
		for cf in cfws:
		    if cf.type == 'Fixed Rate':
		    	if cf.rate < min:
		    	    min = cf.rate
	if min:
	    #print min
	    return str(min)
	else:
	    return ''
    elif request == 'Float':  	
	for l in legs:
	    if l.type == 'Float':
		return l.float_rate.insid
	return ''
    elif request == 'resetrate' or request == 'resetdate':
	for l in legs:
	    if l.type == 'Float':
		resets = l.resets()
		minreset = resets[0].day
		sorted_resets = []
		dict = {}
		n1 = 0
		for rs in resets:
		    dict[str(rs.day)] = n1
		    n1 = n1 + 1
		    if rs.day < minreset:
		    	minreset = rs.day
		
		for n2 in range(len(resets)):
		    sorted_resets.append(minreset)
		    
		    del dict[str(minreset)]
		    
		    if dict.keys():
		    	minreset = dict.keys()[0]
		    	
		    	for e in dict.keys():
		    	
			    if ael.date_from_string(e) < minreset:
			    	minreset = ael.date_from_string(e)
		Output = ''   	    	
		flag = 0
		for dates in sorted_resets[1:len(sorted_resets)]:
		    if flag == 0:
		    	Output = Output + str(dates)
			flag = 1
		    else:
		    	Output = Output + ';' + str(dates)
		#print Output
		    		
		
		
		
		max = 0
		baseday = ael.date_today().add_years(-10)
		for r in resets:
		    if r.day > baseday and r.value != 0:
		    	baseday = r.day
			max = r.value
			#print r.day,r.value
		if request == 'resetrate':
		    return str(max)
		else:
		    return Output 
		    #str(baseday)
	return ''
		    
    else:	    
    	return 'Error'
	
def CashflowNumber(l,number,*rest):
    cfs = l.cash_flows()
    mincash = cfs[0].cfwnbr
    for i in cfs:
    	if i.cfwnbr < mincash:
	    mincash = i.cfwnbr
    #print len(cfs)
    #print number
    return (number - mincash) + 1
    
def ExchangeCurr(i,curr,*rest):
    legs = i.legs()
    for l in legs:
    	if l.curr.insid != curr:
	    return l.curr.insid
	    
"""
def CommitExchange(r,sys_rate,*rest):
    
    new = r.clone()
    
    new.value = sys_rate
    new.commit()
    return 'Updated'	
    """



def CashFlowCount(i,*rest):
    lgs = i.legs()
    NumOfCshflws = 0
    for l in lgs:
    	cshflws = l.cash_flows()
    	NumOfCshflws = NumOfCshflws + len(cshflws)
    return NumOfCshflws

def MinFloorCF(l,*rest):
    cfs = l.cash_flows()
    mincash = cfs[0].cfwnbr
    for i in cfs:
    	if i.cfwnbr < mincash:
	    mincash = i.cfwnbr
	    date = i.start_day
    
    return date


def PBADate(c,*rest):
    b = 0
    cfs=c.resets()
    for r in cfs:
    	if r.start_day==c.start_day:
	    b=c.start_day
	
    #print b
    
    return b


def res_advice(i,MVal,*rest):
    
    if MVal == 'TradeNo':
    	trd = ael.Trade.read('trdnbr= %d' % t.trdnbr)
    	return (trd)
	
	
def ResetDay(r,*rest):
    	
    Month = r.day.to_string('%B')
    Year = r.day.to_string('%Y')
    #print Month + ' ' + Year
    output = Month + ' ' + Year
	
    return output	
    
def FDofMonth(r,*rest):
    	
    
    FirstDay = r.start_day.first_day_of_month()
    #print Test
    output = FirstDay
	
    return output       
 
 
 
def DinMonths(r,*rest):

    Days = r.start_day.days_in_month()
    output = Days
    
    return output

def LDofMonth(r,*rest):

    FirstDay = r.start_day.first_day_of_month()
    Days = r.start_day.days_in_month()
    
    LastDay = FirstDay.add_days(Days)
    
    output = LastDay
    
    return output
    
    
def DayofYear(temp, dat, *rest):

    try:
    	d = ael.date_from_string(dat)
    except:
        try:
            d = ael.date_from_string(dat, '%Y/%m/%d')
        except:
            d = dat
	    
    try:
        return d.day_of_year()
    except:
        return 0
        
    '''
    if date:
    	d = ael.date_from_string(date)
    	return d.day_of_year()
    else:
    	return 0
    '''
    

def Kim2(l,*rest):
    b=0
    # print "In"
    lastreset = l.resets()
    mindate=(l.start_day.add_delta(l.reset_day_offset, 0, 0))
    # mindate = lastreset[0].start_day
    #print mindate
    for r in lastreset:
    	if r.start_day >= mindate:  
	    if r.day<=ael.date_today(): 
	    	if r.read_time!=0:
		    if r.value!=0:
		    	# print "C"
			mindate = r.start_day
			b=r.value
			# print b	
    	    	    else: 
		    	break
    #print b
    	 
    return b

def BreakEventLD(i,*rest):
    
    ExEvents = ael.ExerciseEvent.select('insaddr= %d' % i.insaddr) 
    
    if len(ExEvents) == 0:
    	Output = ''
        return (Output)
	       
    lastdate = ExEvents[0].day
    #print len(ExEvents)
    for a in ExEvents:
    	#print a.seqnbr
    	if a.day > lastdate:
            lastdate = a.day
	    #print a.day
    return lastdate.to_string()

def BreakEventFD(i,*rest): 

    ExEvents = ael.ExerciseEvent.select('insaddr= %d' % i.insaddr) 
    
    if len(ExEvents) == 0:
    	Output = ''
        return (Output)
	
    firstdate = ExEvents[0].day
    #print len(ExEvents)
    for b in ExEvents:
    	#print b.seqnbr
    	if b.day < firstdate:
            firstdate = b.day
	    #print b.day
    return firstdate.to_string()
    
def InsStart(i,*rest):
    lgs = i.legs()
    
    for l in lgs:
    	#Date = l.start_day
    	#print Date
	#NewDate = Date.to_ymd()
	#y, m, d = NewDate
	#NewYr = y
	#NewMn = m
	#print str(NewYr), str(NewMn)
	#output = str(NewYr)
	
	#print output
	
	Month = l.start_day.to_string('%B')
	Day = l.start_day.to_string('%d')
	#print Month, Day
	output = Day + ' ' + Month
	
    return output    
    
def Kim3(cf,*rest):
    b = 0
    cfs=cf.resets()
    for r in cfs:
    	if r.start_day==cf.start_day:
	    b=r.value
	
    #print b
    
    return b 
    
def Kim(l,test,*rest):
    lastreset = l.resets()
    mindate = lastreset[0].start_day
    for r in lastreset:
    	if r.start_day > mindate:
	    mindate = r.start_day
    	# print mindate  
    return mindate
    
def Kim4(l,test,*rest):
    b=0
    # print "In"
    lastreset = l.resets()
    mindate=l.start_day
    # mindate = lastreset[0].start_day
    # print mindate
    for r in lastreset:
    	#print r.value
	if r.start_day >= mindate:  
	    if r.day<=ael.date_today: 
		if r.read_time!=0:
		    if r.value!=0:
		    	# print "C"
			mindate = r.start_day
	    	    	b=mindate
			# print b	
    	    	    else: 
		    	break
    
    
    #print b
    	 
    return b
    
    
    
def Kim5(l, *rest):
    #returns the rate of the current cashflow
    cashflows = l.cash_flows()
    for cfs in cashflows:
    	if cfs.start_day <= ael.date_today():
	    if ael.date_today() <= cfs.end_day:
	    	return cfs.rate
		
    return 0.0

    
    

def AutoFax(p,*rest):
    FNbr = p.fax
    A = '[FAX:'
    B = ']'
    Output = A + str(FNbr) + B
    return Output

def ResetCount(c,*rest):
    
    cfs=c.resets()
    
    for r in cfs:
    	if r.type == 'Nominal Scaling':
	    output = 1
	else:
	    output = 0
    return output
    
def Date2MonthYear(i,date,*rest):
    try:
    	AelDate = date #ael.date_from_string(date)
    	month = {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}
    	y, m, d = AelDate.to_ymd()
    	if len(str(y-2000)) == 1:
    	    return month[m] + '0' + str(y-2000)
    	else:
    	    return month[m] + str(y-2000)
    except:
    	return ''
	
	
def ReturnVolatility(v,strike,exp_day,putcall,*rest):
#Hardus Jacobs Added Code for option of a Call or Put layer
    if putcall == 'PUT':
    	val = 0
    else:
    	val = 1
    return v.vol_get(strike, exp_day, exp_day, val)

#Returns the volatility name against the instrument
def ReturnVolatility_Name(I,*rest):
    Vol_Name = I.used_volatility(I.curr)   
    return Vol_Name.vol_name




def ReturnVolatility_test(v,strike,exp_day,putcall,*rest):
#Hardus Jacobs Added Code for option of a Call or Put layer
    if putcall == 'PUT':
    	val = 0
        strike = strike * -1
    else:
    	val = 1
       	
    return v.vol_get(strike, exp_day, exp_day, val)
    
    

def CapMinCF(l,*rest):
    cfs = l.cash_flows()
    mincash = cfs[0].start_day
    for i in cfs:
    	if i.start_day < mincash:
	    mincash = i.start_day
	    
    date = mincash
	    
    
    return date
    
def freq(i,*rest):
    for l in i.legs():
    	if l.rolling_period=='3m':
	    f='QURT'
	elif l.rolling_period=='91d':
	    f='QURT'
	elif l.rolling_period=='6m':
	    f='SEMI'
	elif l.rolling_period=='1m':
	    f='MON'
	elif l.rolling_period=='1y':
	    f='ANNU'
	elif l.rolling_period=='12m':
	    f='ANNU'    
	
	else:
	    f='unknown'    	
    return f    

    
def myfreq(l,*rest):
    rolper = l.rolling_period
    return rolper
    
    
def myfreqname(l,*rest):
    if l.rolling_period=='3m':
	f='QURT'
    elif l.rolling_period=='91d':
	f='QURT'
    elif l.rolling_period=='6m':
	f='SEMI'
    elif l.rolling_period=='1m':
	f='MON'
    elif l.rolling_period=='1y':
	f='ANNU'
    elif l.rolling_period=='12m':
	f='ANNU'    
	
    else:
	f=l.rolling_period
    return f 
    
    
def CreateBondConfoName(e, insid, coupon, expiry, *rest):
    """
    	Returns a string for use in bond confirmations.
	
	Parameters:
	    e 	    - table ref     - ignored
	    insid   - string	    - the bonds instrument id
	    coupon  - float 	    - the bonds coupon rate
	    expiry  - date  	    - the bonds expiry date
	
	Function returns a string containing a concatenation of the inputs.
	 
	History:
    	2003/10/28 - Russel Webber - Created
    """
    s = '%s %2.3f%% %s' % (insid[4:], coupon, str(expiry.to_ymd()[0]))
    return s

def last_res(l,*rest):
    b=0
    lastreset = l.resets()
    mindate=l.start_day
    today = ael.date_today
    for r in lastreset:
	if r.day >= mindate:  
	    if r.day<=today: 
		if r.read_time!=0:
		    if r.value!=0:
			mindate = r.cfwnbr.start_day
	    	    	b=r.resnbr
    	    	    else: 
		    	break
    if b == 0:
    	mindate = lastreset[0].day
	b = r.resnbr
	for r in lastreset:
	    if r.day <= mindate:
	    	mindate = r.day
		b = r.resnbr
    return b

def myfreq(l,*rest):
    rolper = l.rolling_period
    return rolper
    
def concat_endperiod(l, *rest):
    endper = l.end_period
    return endper
    
def updte_yc():
    list = []
    for y in ael.YieldCurve:
    	ya = y.additional_infos()
    	if ya:
    	    if ya[0].value == 'Yes':
    	    	list.append(y.yield_curve_name)
	    
    YieldCurves = list
#    print list
    for ycname in YieldCurves:
        yc = ael.YieldCurve[ycname].clone()
    	try:
	    yc.calculate()
            yc.commit()
	except:
	    print 'Unable to calculate YC: ', ycname
    #ael.poll()
    return 'calculated'
    
def getYCName2(i,*rest):
    if i.used_yield_curve():
        return i.used_yield_curve().ir_name
    return None

def getYCName3(i,*rest):
    yc = i.used_yield_curve()
    print yc.ir_name
    name = ''
    
    if yc.ir_name:
        return yc.ir_name
    else:
        for uyc in i.used_yield_curves():
            if uyc[0] == 'Discount':
                name = uyc[1]
        return name

def getYCName4(i,*rest):
    instrument = acm.FInstrument[i.insid]
    global calcSpace
    global collectLimit
    global collect
    if instrument:
        if collect == collectLimit:
            for eb in acm.FCache.Select01('.StringKey = "evaluator builders"', "").Contents():
                eb.Reset()
            calcSpace.Clear()
            acm.Memory().GcWorldStoppedCollect()
            collect = 0
        component = instrument.Calculation().DiscountYieldCurveComponent(calcSpace)
        collect = collect + 1
        'What if more than one???'
        if component:
            if component.IsKindOf('FYieldCurve'):
                return component.Name()
            if component.IsKindOf('FInstrumentSpread') or component.IsKindOf('FYCAttribute'):
                return component.Curve().Name()
    return ''
    
def getYCName(i,*rest):
    instrument = acm.FInstrument[i.insaddr]
    if instrument:
        discountLink = instrument.MappedDiscountLink()
        if discountLink:
            discountYieldCurveHierarchy = discountLink.Link()
            if discountYieldCurveHierarchy:
                discountYieldCurveComponent = discountYieldCurveHierarchy.YieldCurveComponent()
                if discountYieldCurveComponent:
                    if discountYieldCurveComponent.IsKindOf('FYieldCurve'):
                        return discountYieldCurveComponent.Name()
                    if discountYieldCurveComponent.IsKindOf('FInstrumentSpread') or discountYieldCurveComponent.IsKindOf('FYCAttribute'):
                        return discountYieldCurveComponent.Curve().Name()
    return ''
    
def get_repo_depo_rate(i,pick,*rest):
    curve = i.used_yield_curves()[pick - 1][2]
    ycrate = curve.yc_rate(ael.date_today(), ael.date_today(), 'Continuous', 'Act/365', 'Spot Rate')
    return ycrate

def get_discountcurve(t,i,ptype,*rest):
    paycur = i.curr.insaddr
    receivecur = i.curr.insaddr
    for l in i.legs():
    	if l.payleg:
	    paycur = l.curr.insaddr
	else:
    	    receivecur = l.curr.insaddr
    	    
    if ptype == 'Pay':
        cur = paycur
    else:
        cur = receivecur

    for c in ael.ContextLink.select('group_chlnbr=%d' % i.product_chlnbr.seqnbr):
    	if c.context_seqnbr.name == 'ACMB Global' and c.type == 'Yield Curve' and c.curr.insaddr==cur:
    	    return c.name

    for c in ael.ContextLink.select('insaddr=%d'% i.curr.insaddr):
        if c.context_seqnbr.name == 'ACMB Global' and c.type == 'Yield Curve' and c.curr.insaddr==cur:
            return c.name

    return ' '


def ASQL_log(e,*ASQL_NAME):
    import os, sys, acm
    deffile=''
    #print ASQL_NAME[0],ael.date_from_time(e.updat_time)
    d = ael.date_today().to_string('%Y-%m-%d')
    fname = "AUTO_PROD_ASQLs_" + str(ael.date_today().to_string('%Y-%m')) + ".log"
    UPDATE=ASQL_NAME[0] + '; Executed by: ;' + str(ael.userid()) + '; Last Executed:  ;' + d + '; Server: ;' + acm.ADSAddress() 
    nbr=1
    if os.name == 'nt':
    	#ael.log(os.name)
    	#deffile=os.path.join('\\\\atlasprd\log\prime','PROD_ASQLs.log')
        #deffile=os.path.join('\\\\v036syb004001\log\Prime',fname)
        deffile=os.path.join('Y:\\Jhb\Arena\log\log43', fname)
	#ael.log(deffile)
    else:
    	#ael.log(os.name)
    	#deffile=os.path.join('/services/front/scripts/log/',fname)
	deffile=os.path.join('/front/arena/apps/log/', fname)
    #ael.log(deffile)    
    #ael.log("PROD_ASQLs.log file error.")
    ael.log(UPDATE)
    try:
    	f=open(deffile, 'a')
    except:
	ael.log("PROD_ASQLs.log file error.")
	return nbr
    f.write(UPDATE)
    f.write('\n')
    f.close()
    return nbr

def LastDayOfMonth(temp, date, *rest):
#  Function returns last day of month given a date in "date" or "string" format #

    try:
    	sdate = ael.date_from_string(date)
    except:
       	#print '\n argument1 not in string format\n'
	sdate = date

    FirstDay = sdate.first_day_of_month()
    Days = sdate.days_in_month() - 1
    
    LastDay = FirstDay.add_days(Days)
    
    #output = LastDay.to_string('%B')
    
    return LastDay
    #output
   

def LastBusinessDay(temp, date, *rest):
#  Function returns last business day of month given a date in "date" or "string" format #    
    ld = LastDayOfMonth(temp, date)
    lbd = ld.adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding')
    
    return lbd

def FirstDayOfMonth(temp, date, *rest):
#  Function returns first day of month given a date in "date" or "string" format #

    try:
    	sdate = ael.date_from_string(date)
    except:
	sdate = date
	
    FirstDay = sdate.first_day_of_month()
    
    return FirstDay

def FirstBusinessDay(temp, date, *rest):
#  Function returns first business day of month given a date in "date" or "string" format #
    fd = FirstDayOfMonth(temp, date)
    fbd = fd.adjust_to_banking_day(ael.Instrument['ZAR'], 'Following')
    
    return fbd
    
def getSwiftCode(temp, accnbr, *rest):
    a = ael.Account[accnbr]
    if a.correspondent_bank_ptynbr:
        cor_bank = a.correspondent_bank_ptynbr
        if cor_bank.aliases():
            for x in cor_bank.aliases():
                if x.type.alias_type_name == 'SWIFT':
                    return x.alias
    return 'Not Found'


#def getExpiryDate(temp, i, date, *rest):
    #print i.generic 


#Returns if a date is a banking day or not
def isBankingDay (Date,Curr,*rest):

    ReportingDate = ael.date(Date)

    CurrentDate = ReportingDate.adjust_to_banking_day(ael.Instrument[Curr], 'Following')
    
    if CurrentDate == ReportingDate:
        value = 1
    else:
        value = 0
    
    return value


#used in LA Stock file to include agg trades after a weekend.
def CheckFirstofWeek(temp, date, *rest):
    try:
        repday = ael.date_from_string(date)
    except:
        repday = date
        
    if isBankingDay(repday.first_day_of_week(), 'ZAR'):
        if repday == repday.first_day_of_week():
            return 'YES'  #repday.add_delta(
        else:
            return 'NO'
     
    return 'NO'
    
    
#Returns the previous banking day    
def previousBankingDay (Date,Curr,*rest):

    ReportingDate = ael.date(Date)

    PreviousDate = ReportingDate.add_days(-1).adjust_to_banking_day(ael.Instrument[Curr], 'Preceding')
    
    return PreviousDate

#Returns the next banking day    
def nextBankingDay (Date,Curr,*rest):

    ReportingDate = ael.date(Date)

    NextDate = ReportingDate.add_days(1).adjust_to_banking_day(ael.Instrument[Curr], 'Following')
    
    return NextDate

#Returns the day before next banking day    
def dayBeforeNextBankingDay (Date,Curr,*rest):

    ReportingDate = ael.date(Date)

    NextDate = nextBankingDay(ReportingDate, 'ZAR')
    
    dayBefore = NextDate.add_days(-1)
    
    return dayBefore


def getInstype(trd, instype, *rest):
    if instype == 'FRN':
        ai = trd.add_info('MM_Instype')
        if ai == 'NCC':
            return ai
        else:
            return 'FRN'
            
    ai = trd.add_info('Funding Instype')
    if ai != '':
        return ai
    
    ai = trd.add_info('MM_Instype')
    if ai != '':
        return ai
    
    return trd.add_info('Instype')

def get_discountcurve2(t,i,ptype,*rest):
    a = get_discountcurve(t, i, ptype)
    if a == ' ':
        return 'No Discount Curve Allocated'
    return a

# SANLD FX OPTIONS

def ReturnVolatility_Name_new(i, *rest):
    ins = acm.FInstrument[i.insid]  
    return ins.MappedVolatilityStructure().Parameter().Name()
    
def get_discountcurve_new(i, *rest):
    ins = acm.FInstrument[i.insid]    
    curr = ins.StrikeCurrency()
    att = ins.MappedDiscountLink().Link().YieldCurveComponent()
    if att.RecordType() == 'YieldCurve':
        return att.Name()
    else:
        return att.Curve().Name()

def get_mirror_trade(temp, trdnbr, *rest):
    t = ael.Trade[trdnbr]
    m = t.get_mirror_trade()
    if m:
        return m.trdnbr
    else:
        return 0

def prev_weekday(date):
    date -= timedelta(days=1)
    while date.weekday() > 4: # Mon-Fri are 0-4
        date -= timedelta(days=1)
    return date


#print get_mirror_trade(1, 18716524)


def BankingDaysCount(i, date_from, date_to, currency, *rest):

    return acm.FInstrument[int(currency)].Calendar().BankingDaysBetween(date_from, date_to)

