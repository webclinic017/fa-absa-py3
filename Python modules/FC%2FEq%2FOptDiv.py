
"""Module: FC/Eq/OptDiv

 Valuation of options on dividend equities using modified B&S

 When                 Who             What
 -----------------------------------------------------------------------------
 May        2002      Martin Boberg   Created
 August     2002      Martin Boberg   Changed date_today to date_valueday
                                      Changed yield to simpleYield
 November   2003      Russel Webber   Added calcs for rho and vega
    	    	    	    	      Extended module to allow calling from ASQL
				      	    and returning of greeks.
				      Added discounting of pv if pay offset > 0
    	    	    	    	      Added function to return model inputs to ASQLs
January     2003    H kan Norekrans   Error handling when reading dividend yield added
January     2003    H kan Norekrans   Correction of Theta 1d on the last day before expiration
January     2003    H kan Norekrans   Theta should be returned in years, theta = theta/365
January     2003    H kan Norekrans   Handling of sigma = 0				      
				      
 Other AEL Modules and Functions dependencies
 -----------------------------------------------------------------------------
 None

 Other External dependencies
 -----------------------------------------------------------------------------
 None

 ASQL Query
 -----------------------------------------------------------------------------
 None

 References
 -----------------------------------------------------------------------------
 Dr A. A. Kotze, 'Derivatives on equities and equity futures in the 
                  South African market', July 2001 """


import ael
import math
import sys

if ael.userid() == 'EXTRACT':
    printout = 0
else:
    printout = 1

cached_greeks = {}

def nac2ccr(m, r):
    """nac2ccr(m, r)

    Converts notional amount compounded annually/semi-annually etc
    to continuous compounded format.

    m       (int):         Number of compounds per annum (1 for annually)
    r       (float):       Interest rate per annum
    returns (float):       Continuous compounded yield"""

    try:
        m = float(m)
        r = float(r)
    except:
        print 'Arguments must be numeric values'
        sys.exit()
    if m == 0.0:
    	return m
    else:
    	return m * math.log(1 + r/m)


def sim2nac(m, simpleYield, t):
    """sim2nac(m, simpleYield, t)

    Converts simple yield to notional amount compounded

    m           (int):         Number of compounds per annum (1 for annually)
    simpleYield (float):       Simple yield
    t           (float):       Time in years
    returns     (float):       Yield in NAC format"""

    try:
        m           = float(m)
        simpleYield = float(simpleYield)
        t           = float(t)
    except:
        print 'Arguments must be numeric values'
        sys.exit()

    return ((1 + simpleYield*t)**(1/(m*t)) - 1)*m


def DividendYieldFromCash(aelOption):
    """DividendYieldFromCash(aelOption)

    Calculates the dividend yield from the underlying's cash dividends

    aelOption               An Instrument entity of type Option
    returns                 The dividend yield in CCR format"""

    aelUnderlying = aelOption.und_insaddr
    selDivs = aelUnderlying.dividends(aelOption.exp_day)

    SDate = ael.date_valueday()
    EDate = aelOption.exp_day

    # Calculate the risk free rate in CCR format
    ycrf = aelOption.used_yield_curve(aelOption.curr)
    rd   = ycrf.yc_rate(SDate,
                        EDate,
                        'Continuous',
                        ael.YieldCurve[ycrf.ir_name].storage_daycount,
                        'Spot Rate',
                        0) 

    # Get the spot price for the underlying
    Spot = aelOption.used_und_price()

    DivsPv = 0.0

    for div in selDivs:
        LDRDate   = div.day        # Record day
        payDate   = div.pay_day    
        cashValue = div.dividend

        if SDate <= LDRDate and EDate >= LDRDate:
            t = SDate.days_between(payDate)/365.0
            DivsPv  = DivsPv + cashValue*math.exp(-rd*t)

    t = SDate.days_between(EDate)
    simpleYield = DivsPv / (Spot * t)

    dyNacs = sim2nac(2, simpleYield, t)
    dyCCR  = nac2ccr(2, dyNacs)

    return dyCCR


def EuropeanOption(aelOption, d):
    """EuropeanOption(aelOption, d)

    Valuation function of european options

    aelOption  An instrument entity of type Option
    d          Dividend yield in CCR format"""


    # Retrieve s (current spot market price of the underlying) from ADS
    s = aelOption.used_und_price()
    # Retrieve k (strike price) from ADS
    k = aelOption.strike_price
    # Retrieve r (risk free rate) from ADS
    ycrf = aelOption.used_yield_curve(aelOption.curr)
    r = ycrf.yc_rate(ael.date_valueday(),
                     aelOption.exp_day,
                     'Continuous',
                     ael.YieldCurve[ycrf.ir_name].storage_daycount,
                     'Spot Rate',
                     0) 
    
    # Calculate sigma (volatility)
    # For ATLAS 3.2.8 and later
    # sigma = aelOption.get_vol(k, aelOption.exp_day)
    # Added below before vs.
    t = ael.date_valueday().days_between(aelOption.exp_day)/365.0
    FairForward = s*math.exp((r-d)*t)
    #FairForward = FairForwardDates(aelOption.exp_day)
    if printout: print 'FairForward = ', FairForward 
    vs    = aelOption.used_volatility(aelOption.curr)
    # Changed by PG and SM on 12/03/03. Skew is defined in terms of a relative to spot percentange not
    # absolute strike. Changed appropriately.
    if printout: print 'ATM Vol on Expiry = ', vs.volatility(0, aelOption.exp_day)*100
    sigma = 0
    if aelOption.instype == 'Warrant':
    	volt = ael.Volatility[vs.vol_name]
    	for v in volt.points():
    	    if v.insaddr == aelOption:
    	    	sigma = v.volatility
    else:
    	sigma = vs.volatility((k/FairForward-1)*100, aelOption.exp_day) #(k/s-1)*100, aelOption.exp_day)
    if printout: print 'Volatility = ', sigma*100
    if printout: print 'Moneyednes = ', (k/FairForward-1)*100
    if printout: print 'Expiry = ', aelOption.exp_day

    
    # Calculate t (annualised time to expiry)
    t = ael.date_valueday().days_between(aelOption.exp_day)/365.0

    # Determine phi (1 = call, -1 = put)
    if aelOption.call_option:
        phi =  1
    else:
        phi = -1

    if printout: print '-----------------'
    if printout: print 's \t= ', s
    if printout: print 'k \t= ', k
    if printout: print 'r \t= ', r
    if printout: print 'sigma\t= ', sigma
    if printout: print 't \t= ', t
    if printout: print 'd \t= ', d
    if printout: print 'phi\t= ', phi

    
    # HN 2004-01-16 Handle sigma = 0
    if sigma == 0:
    	sigma = 0.000001


    if t < 0:
        return 0.0
    elif t == 0:
        return max(0.0, phi*(s-k))
    else:
        x = (math.log(s/k) + (r - d + sigma*sigma/2)*t)/(sigma*math.sqrt(t))
        y = x - sigma*math.sqrt(t)

	delta = phi*math.exp(-d*t)*ael.normal_dist(phi*x)
	gamma = 1/(math.sqrt(2*3.14159265358979))*math.exp(-(x*x)/2)*math.exp(-d*t)/(s*sigma*math.sqrt(t))
	theta = -(s*1/(math.sqrt(2*3.14159265358979))*math.exp(-(x*x)/2)*sigma*math.exp(-d*t))/(math.sqrt(t)*2) + phi*(d*s*ael.normal_dist(phi*x)*math.exp(-d*t)- \
	    	r*k*math.exp(-r*t)*ael.normal_dist(phi*y))
    	
	# HN 2004-01-16 Theta should be returned per day 
    	theta = theta/365
    	
    	if printout: print 'Theta per day', theta/365
	
	p0 = phi*(math.exp(-d*t)*s*ael.normal_dist(phi*x) - \
                    k*ael.normal_dist(phi*y)*math.exp(-r*t))
	
	# HN 2004-01-16 Error on last day before expiration
	if t > 1.0/365.0:
	
	    t1 = t - 1.0/365.0
	    x1 = (math.log(s/k) + (r - d + sigma*sigma/2)*t1)/(sigma*math.sqrt(t1))
	
	    y1 = x1 - sigma*math.sqrt(t1)
	
	    p1 = phi*(math.exp(-d*t1)*s*ael.normal_dist(phi*x1) - \
                    k*ael.normal_dist(phi*y1)*math.exp(-r*t1))
    	else:
	    p1 = 0
	    

    	pv = phi*(math.exp(-d*t)*s*ael.normal_dist(phi*x) - \
                    k*ael.normal_dist(phi*y)*math.exp(-r*t))
		    
	rho = -t * k * math.exp(-r * t) * ael.normal_dist(phi * y) / 100.0
	vega = math.exp(-d * t) * s * math.sqrt(t) * (0.39894228 * math.exp(-0.5 * x * x)) / 100.0

    	if aelOption.pay_day_offset:
    	    yc = aelOption.used_yield_curve()
	    expiry_date = aelOption.exp_day
	    pay_date = expiry_date.add_banking_day(aelOption.und_insaddr.curr, aelOption.pay_day_offset)

	    df = yc.yc_rate(expiry_date, pay_date, 'None', 'None', 'Discount')
    	
	    pv = pv * df
		    
	if printout: print 'Delta ', delta
	if printout: print 'Gamma ', gamma
	if printout: print 'Theta ', theta
	if printout: print 'Theta 1d ', (p1 - p0)/(-1.0/365.0)
	if printout: print 'Rho ', rho
	if printout: print 'Vega ', vega
	if printout: print 'Present Value', pv
	if printout: print '################################'
	return [pv, delta, gamma, theta, rho, vega]


def pvExp(i, calc=1, ref=0):
    """pvExp(i, calc=1, ref=0)

    Wrapper function for valuation of european options on dividend equities.
    Explicit dividend yield is retrieved from the underlying"""
    if calc:
        
	# H kan N 2004-01-16 Error handling included
	
	# retrieve d (dividend yield) from additional info (NACA format)
        try:
	    d = float(i.und_insaddr.add_info('DividendYield'))
	except:
	    d = 0.0
        # Convert d from NACA to CCR format
        d = nac2ccr(1, d)
	try:
	    res = EuropeanOption(i, d)[0:4]
	except:
	    res= 0.0
    else:
        res = 0.0

    return [ [ res, i.exp_day, i.curr] ]

def pvImp(i, calc=1, ref=0):
    """pvImp(i, calc=1, ref=0)

    Wrapper function for valuation of european options on dividend equities.
    Dividend yield is calculated implicitly from underlying's cash dividends"""
    if calc:
        # Calculate implicit yield from cash dividends
        d = DividendYieldFromCash(i)
        res = EuropeanOption(i, d)[0:4]
    else:
        res = 0.0

    return [ [ res, i.exp_day, i.curr] ]
    
def FairForwardDates(date,*rest):
    Options = ael.Instrument.select('und_insaddr.insid = %s' % 'ZAR/ALSI')
    SAFEXFuturesOptions = []
    SAFEXDates = []
    SAFEXPrices = []
    for o in Options:
    	if o.otc == 0:
    	    SAFEXFuturesOptions.append(o)
    	    #SAFEXDates.append(o.exp_day)
	    prices = ael.Price.select('insaddr=%s' % o.insaddr)
	    if prices:
	    	LatestPrice = prices[0].settle
	    	LatestDate = prices[0].day
	    	for p in prices:
	    	    if p.day > LatestDate:
	    	    	LatestDate = p.day
		    	LatestPrice = p.settle
	    	SAFEXDates.append([o.exp_day, LatestPrice])
	    	SAFEXPrices.append(LatestPrice)
    
    FinalPrices = []
    length = len(SAFEXDates)
    for i in range(length):
    	min = SAFEXDates[0][0]
    	minprice = SAFEXDates[0][1]
    	for d in SAFEXDates:
	    if d[0] < min:
	    	min = d[0]
	    	minprice = d[1]
    	FinalPrices.append([min, minprice])
    	#print [min,minprice]
    	SAFEXDates.remove([min, minprice])
    #print 'FinalPrices', FinalPrices
    
    before = 0
    length = len(FinalPrices)
    for i in range(length-1):
    	if (date >= FinalPrices[i][0] and date < FinalPrices[i+1][0]):
	    before = FinalPrices[i][1]
	    beforedate = FinalPrices[i][0]
	    after = FinalPrices[i+1][1]
	    afterdate = FinalPrices[i+1][0]
	    #print before,after
	#print 'Inputted', date
    if before == 0:
    	before = FinalPrices[length-2][1]
	#print before
	beforedate = FinalPrices[length-2][0]
	after = FinalPrices[length-1][1]
	afterdate = FinalPrices[length-1][0]
    leg1 = beforedate.days_between(date)
    leg2 = date.days_between(afterdate)
    total = beforedate.days_between(afterdate)
    #print leg1,leg2,total,before,after
    return round(float(leg2)/float(total)*float(before) + float(leg1)/float(total)*float(after), 0)

def SQL_Greeks(i, greek, *rest):
    # Function to be called from ASQL
    # i = Instrument object of the instrument that the greek value is required
    # greek = The name of the greek that is requested
    # Retruns the requested greek for a specific instrument
    
    if (i.record_type == 'Instrument' and (i.instype == 'Option' or i.instype == 'Warrant')):
    
	if i not in cached_greeks.keys():
    	    
	    # retrieve d (dividend yield) from additional info (NACA format)
            try:
	    	d = float(i.und_insaddr.add_info('DividendYield'))
	    except:
	    	print 'No Dividend'
		d = 0.0
            # Convert d from NACA to CCR format
            d = nac2ccr(1, d)
    	    if i.instype == 'Option' and i.und_instype == 'Future/Forward' and i.otc == 0:
    	    	d = 0.0
    	    res = EuropeanOption(i, d)

    	    pv  = res[0]
	    delta  = res[1]
	    gamma  = res[2]
	    theta  = res[3]
	    rho  = res[4]
	    vega = res[5]

    	    cached_greeks[i] = [pv, delta, gamma, theta, rho, vega]

    	if greek == 'PV':
	    return cached_greeks[i][0]
	elif greek == 'Delta':
    	    return cached_greeks[i][1]
	elif greek == 'Gamma':
    	    return cached_greeks[i][2]
	elif greek == 'Theta':
    	    return cached_greeks[i][3]
	elif greek == 'Rho':
    	    return cached_greeks[i][4]
	elif greek == 'Vega':
    	    return cached_greeks[i][5]
	    
    else:
    
    	return 0.0

def SQL_ModelInputs(i, input, *rest):

    # retrieve d (dividend yield) from additional info (NACA format)
    try:
    	d = float(i.und_insaddr.add_info('DividendYield'))
    except:
    	print 'No dividend'
	d = 0.0
    # Convert d from NACA to CCR format
    d = nac2ccr(1, d)
    if i.instype == 'Option' and i.und_instype == 'Future/Forward' and i.otc == 0:
    	d = 0.0
    # Retrieve s (current spot market price of the underlying) from ADS
    s = i.used_und_price()
    # Retrieve k (strike price) from ADS
    k = i.strike_price
    # Retrieve r (risk free rate) from ADS
    ycrf = i.used_yield_curve(i.curr)
    r = ycrf.yc_rate(ael.date_valueday(),
                     i.exp_day,
                     'Continuous',
                     ael.YieldCurve[ycrf.ir_name].storage_daycount,
                     'Spot Rate',
                     0) 
    t = ael.date_valueday().days_between(i.exp_day)/365.0
    FairForward = s*math.exp((r-d)*t)
    # Calculate sigma (volatility)
    vs    = i.used_volatility(i.curr)
    # Changed by PG and SM on 12/03/03. Skew is defined in terms of a relative to spot percentange not
    # absolute strike. Changed appropriately.
    sigma = 0.0
    if i.instype == 'Warrant':
    	volt = ael.Volatility[vs.vol_name]
    	for v in volt.points():
    	    if v.insaddr == i:
    	    	sigma = v.volatility
    else:		
    	sigma = vs.volatility((k/FairForward-1)*100, i.exp_day) 
   
    # Determine phi (1 = call, -1 = put)
    if i.call_option:
        phi =  1.0
    else:
        phi = -1.0
	
    if input == 'd':
    	return d
    elif input == 's':
    	return s
    elif input == 'k':
    	return k
    elif input == 'r':
    	return r
    elif input == 't':
    	return t
    elif input == 'FairForward':
    	return FairForward
    elif input == 'sigma':
    	return sigma
    elif input == 'phi':
    	return phi
    else:
    	return 0.0


def divYield(aelOption):
 
    d = float(aelOption.und_insaddr.add_info('DividendYield'))
    # Convert d from NACA to CCR format
    d = nac2ccr(1, d) 
    return d
