""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    FDivYield - Calculate and store implied dividend yields for equity indexes.
        
    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module calculates dividend yield for the nearest at-the-money
    synthetical future. The call and put nearest the current index value
    with market prices are used. The dividend yield curve is updated automatically 
    so the the implied volatilities of the neaest at-the-money options are equal.
    
    Two types of indexes are handled.
    
    1. Dividend adjusted indexes. (Dividend Factor < 0.5) e.g. DAX
    
    A "dividend" yield spread is added on the yield curve. The spread is derived 
    from the put-call parity: 
    
    	Call + DiscountFactor*Strike = Put + ATM

	IRR = (Pow(Strike/(IndexATM - Call + Put),1/time_to_maturity) - 1) * 100
    
    	Div yield = IRR - Yield
	
	where Yield is taken from the Yield Curve mapped to the index.
	

    2. Non dividend adjusted indexes.  (Dividend Factor >= 0.5) e.g. EUROSTOXX50
    
    The divided yield is derived from the put-call parity:
    
    	Call + DiscountFactor*Strike = Put + DiscoutDividendFactor*ATM

    	Div yield = - 100 * Log(IndexATM/(Call - Put + Strike * disc)) / time_to_maturity 
    	
	where disc = Pow(1 + Yield/100.0, - time_to_maturity) 
 
    The dividend yield is scaled from continuous to annual terms. 

 
    The dividend yields are stored in the yield curve that is the underlying
    spread curve to the repo curve mapped to the index.
    
    The module can be called both from ASQL queries and AEL modules, e.g. 
    mark-to-market procedures.

DATA-PREP       
    Define a page where all the underlying indexes are entered. or list? 
    
    Define a Benchmark Spread yield curve that is mapped as Repo curve
    of the equity index.
    
    Important!
    For dividend adjusted indexes, map also the YC to this Benchmark Spread yield curve
    to all INDEX OPTIONS e.g. via a Valgroup.
    
    For non adjusted indexes, map the YC of the index options to the underlying curve 
    of the Benchmark spread curve. Normaly done automatically.
    
    
    
    

EXTERNAL DEPENDENCIES
    .App/DividendYieldWatch            ASQL query calling these routines.
     
----------------------------------------------------------------------------"""

import ael
import math
print 'Inside FDivYield.'

Verb = 1
def log(level, s):
    """Log me."""
    if Verb >= level: print s


# 3. Build all synthetical futures, look for the nearest to at-the-money
# and calculate the dividend yield.

def divy(u, exp, calls, puts):
    
    synt = []
    for i in range(len(calls)):
    	for j in range(len(puts)):
	    # Check if Call Strike = Put Strike and Call exp_day = exp
	    # and Put exp_day = exp:
	    if calls[i][1] == puts[j][1] and calls[i][0] == exp \
	    	and puts[j][0] == exp:
	    	synt.append((calls[i][1], calls[i][2], puts[j][2]))
    synt.sort()
    if synt != []:
    	log(1, '\nMatched Call and Put (strike and used_prices): %s'
    	    % synt)
    
    atm = u.used_price()
    diff = 99999999999999.0
    istr = -1
    for i in range(len(synt)):
    	if abs(atm - synt[i][0]) < diff:
	    istr = i
	    diff = abs(atm - synt[i][0])
    if istr >= 0:

	strike = synt[istr][0]
	call = synt[istr][1]
	put = synt[istr][2]

	today = ael.date_today()
	t = today.years_between(exp)

    	try:
	    yld = syntyield(u, exp)
	except TypeError:
	    return None #0.0	
	
	
	if u.dividend_factor < 0.5:
	    fact = strike/(atm - call + put)
	    irr = (pow(fact, 1/t) - 1) * 100

	    log(1, '''IRR = 100 *(pow (Strike %f /(Und %f - Call %f + Put %f), 1/t 1/%f) - 1)  = %f ''' \
% (strike, atm, call, put, t, irr))

	    res = irr - yld
	    
	    log(1, '''Result = IRR %f - yld %f = %f (Annual)''' % (irr, yld, res))	
	    	
	else:
	    disc = pow(1 + yld/100.0, -t)   # discount factor from annual yield
	    divcont = 100 * math.log(atm/(call - put + strike * disc)) / t      # Continuous 

	    log(1, '''Div Yield (continous) = 100*log(Und %f /(Call %f - Put %f + Strike %f * disc %f) /\
 TimeToMaturity %f = %f''' % (atm, call, put, strike, disc, t, divcont))	

	    yieldcont = math.log(pow(1+yld/100.0, t)) / t * 100.0  # Continuous yield

	    log(1, '''Yield (continous) =  %f''' % (yieldcont))	

    	    # spread curve is calculated using continuous  yield in ATLAS, transform spread to annual
	    irrtot = (pow(math.exp(-t*(yieldcont - divcont)/100.0), -1/t) - 1 ) * 100.0 

	    log(1, '''Yield - Div yield (Continuous) = %f -->  Yield - Div yield (Annual comp) =  %f''' % (yieldcont - divcont, irrtot))	
	    
	    res = irrtot - yld 
	    
	    log(1, '''Result = (Yield - Div yield)(Annual) %f - yield(Annual) %f = %f''' % (irrtot, yld, res))	

    	return res

    else:
    	return None #0.0


# 4. If exp = 'All'
# Commit. This function is called per exp, so it is only necessary to find 
# the right point to update (if yield != 0) or create a new point.

def updy(u, exp, yld):

    rc = u.used_repo_curve()
    log(2, 'Update Yield Curve: %s' % rc.ir_name)
    yc = ael.YieldCurve[rc.ir_name]
    ycclone = yc.clone()
    createnew = 1

    for y in ycclone.points():
    	log(3, "YieldCurvePoint value, date, period:%f, %s, %s" %\
	    (y.value, str(y.date), str(y.date_period)))
	if y.date == exp:
	    
	    if yld == 0:
	    	y.delete()
	    else:	
		y.value = yld / 100.0
		log(1, 'Assigned DivYield to point %f, %s' % (yld, str(exp)))
	    createnew = 0
	    break
    	elif y.date < ael.date_today(): # ael.date_today() is the time the 
	    	    	    	    	# application is started with with 
					# the -date argument.
	    y.delete() 
	    yld = -1  
	    createnew = 0
    
    if createnew == 1 and yld != 0:
    
	newyp = ael.YieldCurvePoint.new(ycclone)

	newyp.value = yld / 100.0
	log(1, 'Created new point for date: %s' % str(exp))
	newyp.date = exp   	

    ycclone.commit()
    log(4, '%s' % ycclone.pp())
    ycclone.simulate()
    return yld	


# 2. Search all option of the underlying index and look for all expiration dates.

def syntdivyield(u, exp, inslist, *rest):
    log(2, '\nFor instrument with expiry: %s, %s' % (u.insid, exp))

    calls = []
    puts = []
    dy = 0.0

    opt = ael.Instrument.select('und_insaddr=' + str(u.insaddr))
    for o in opt:
    	#print 'start opt, include = 0', o.insid
    	include = 0
	#print 'If inslist = None, include = 1', inslist
	if inslist == None:
	    include = 1
	    #print include
	else:
	    #print 'include should still be 0', include
    	    try:
		for i in range(len(inslist)):
		    #print 'Und in inslist',inslist[i][0].insid
		    #print 'Und of opt', o.und_insaddr.insid
	    	    if o.und_insaddr == inslist[i][0]:
		    	#print 'YES! same und, include', include
			include = 1
			log(3, 'Alias: %s, %s, %s' % (o.und_insaddr.insid, 
		    	    inslist[i][0].insid, o.insid))
	    except TypeError:
		for i in inslist:
	    	    if o.und_insaddr == i:
			include = 1
			log(3, 'Dist: %s, %s, %s' % (o.und_insaddr.insid, 
		    	    i.insid, o.insid))
    	
	if o.instype == 'Option' and o.exp_day > ael.date_today():
	    log(3, "Found derivative: %s, %s, %f, %s" %  (o.insid, 
	    	o.instype, o.used_price(), str(o.exp_day)))
    	if include == 1 and o.instype == 'Option' and o.used_price() > 0 \
	    and o.exp_day > ael.date_today():
	    log(2, "Selected derivative: %s, %s, %f, %s" %  (o.insid, 
	    	o.instype, o.used_price(), str(o.exp_day)))
	    if o.call_option == 1:
	    	calls.append((o.exp_day, o.strike_price, o.used_price()))
	    else:
	    	puts.append((o.exp_day, o.strike_price, o.used_price()))	

    calls.sort()

    if exp == 'All':

    	expdict = {}
    	yieldvec = []
	for i in range(len(calls)):
	    e = calls[i][0]
	    expdict[str(e)] = e
	for i in range(len(puts)):
    	    e = puts[i][0]
	    expdict[str(e)] = e

	val = expdict.values()

	for e in range(len(val)):
    	    
	    dy = divy(u, val[e], calls, puts)
	    log(3, "IRR synth if 'All': %s, %s" % (str(dy), str(val[e])))
	    if dy != None: #0.0:
	    	log(1, 'DivYield will be saved.')
	    	updy(u, val[e], dy)

    	return dy

    else:
    	dy = divy(u, exp, calls, puts)
	log(3, "IRR synth if NOT 'All': %s, %s" % (str(dy), str(exp)))
	if dy != None: #0.0:
    	    log(1, 'DivYield will be saved.')
	    updy(u, exp, dy)

	return dy
    	#return divy(u, exp, calls, puts)


# 5. Look for the yield from the underlying yield curve

def syntyield(u, exp, *rest):
    rc = u.used_repo_curve()

    if rc.und_ir_name == '':
    	print 'WARNING! A Spread curve for the underlying must be defined.'
	yc = None
	#yc = rc
    else:
	yc = ael.YieldCurve[rc.und_ir_name]
    
    try:
    	rate = 100.0 * yc.yc_rate(ael.date_today(), exp, 'Annual Comp', 
	    'Act/365')
    	log(1, 'Used Yield %f' % rate)
    except AttributeError:
    	rate = None
    return rate


# 1. Update the new dividend yield in the mapped spread curve or
# delete expired or zero yield curve points or
# add new points for new expiration dates.

def update_yc(u, exp, inslist, *rest):
    yld = syntdivyield(u, exp, inslist) # exp = expiry date(s) or 'All'
    log(1, 'DivYield = IRR Synth - Yield = %s' % str(yld))
    return yld
    #return updy(u, exp, yld) # Already done this!

# Test code:
#u = ael.Instrument['DAX']
#exp = ael.date('2003-11-03')
#exp = 'All'
#update_yc(u, exp)
# Update all dividend yield curve points    
#syntdivyield(ael.Instrument['SMI'],'All')
# Update one point
#print syntdivyield(ael.Instrument['DAX'],ael.date('2002-11-15'),None)
#print syntdivyield(ael.Instrument['EuroSTOXX50E'],ael.date('2002-11-15'),None)
