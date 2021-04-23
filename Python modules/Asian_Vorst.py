"""
Valuation of Asian Options using Vorst's method.

Only valid for fixed strike arithmetic average options.

Implementation closely based on Black-Scholes implementation 
contained in FC/Eq/OptDiv. Mathematics provided by Dr Antonie Kotze.

Implementation relies on SEQ package being installed and updated daily i.r.o
average options.

History:
2003-11-12 - Russel Webber - Created
2003-11-24 - Russel Webber - Made changes to return Greeks to Arena, returning list as PV.
2003-11-25 - Russel Webber - Added discounting of pv if pay offset > 0
2003-11-28 - Russel Webber - Added function to return model inputs to ASQLs
"""

import ael, math

if ael.userid() == 'EXTRACT':
    printout = 0
else:
    printout = 1

cached_greeks = {}

def AsianVorst(s, k, Sav, rd, t, divy, sigma, phi, asian_times, mm):
    """AsianVorst(s, k, Sav, rd, t, divy, sigma, phi, asian_times, mm)

    Implementation of Vorst's Asian option valuation method.

    s       (float):	    Spot price
    k       (float):        Strike price
    Sav     (float):	    Average spot price so far
    rd      (float):        Continuous compounded risk-free rate
    t       (float):        Fractional years to expiry
    divy    (float):	    Continuous compounded dividend yield
    sigma   (float):        Continuous compounded volatility
    phi     (int):          Binary variable = 1 for call, -1 for put
    asian_times (list):     List of fractional years between valuation date and
    	    	    	    averaging date.
    mm	    (int):  	    Number of averaging dates passed so far
    returns (tuple):        Tuple of present value, delta and gamma"""
    
    n = len(asian_times)
    
    mm = float(mm)
    n = float(n)
    
    Y = rd - divy - (sigma * sigma * 0.5)
    Sum1 = 0
    
    for i in range(mm, n):
    	Sum1  = Sum1 + (Y * asian_times[i])
    
    BigM = math.log(s) + (Sum1 / (n - mm))
    Sum2 = 0
    
    for i in range(mm, n):
    	for j in range(mm, n):
	    Sum2 = Sum2 + min(asian_times[i], asian_times[j])
    
    V = Sum2 * sigma * sigma /((n - mm) * (n - mm))
    Sum3 = 0
    U1 = math.exp(BigM + (V * 0.5))
    
    for i in range(mm, n):
    	Sum3 = Sum3 + (math.exp((rd - divy) * asian_times[i]))
    
    AA = Sum3 / (n - mm)

    Kstar = n / (n - mm) * (k - mm / n * Sav)
    KK = Kstar - (s * AA - U1)
    if Kstar > 0 and V > 0:
        xx = (BigM - math.log(KK) + V) / math.sqrt(V)
    	yy = xx - math.sqrt(V)
    	pv = (n - mm) / n * math.exp(-rd * t) * phi * (math.exp(BigM + V * 0.5) * \
    	    ael.normal_dist(phi * xx) - KK * ael.normal_dist(phi * yy))
    else:
    	pv = math.exp(-rd * t) * phi * (mm / n * Sav - k + ( n-mm)/n * s * AA)	
    b1 = math.exp(-rd * t) * phi
    b2 = math.exp(BigM + V * 0.5)

    if Kstar > 0 and V > 0:
        delta = (n - mm) / n * b1 * (b2 / s * (ael.normal_dist(phi * xx) - \
    	    ael.normal_dist(phi * yy)) + AA * ael.normal_dist(phi * yy))
	gamma = -phi * (n - mm) / n * b1 * (math.exp(-xx * xx / 2) / math.sqrt(2 * math.pi)) / \
    	    math.sqrt(V) * ((1 - b2) / s + AA / KK) * \
	    (1 / s + (AA - b2 / s) / KK)
    else:
    	delta = math.exp(-rd * t) * phi * ((n-mm) / n * AA)
	gamma = 0

    return (pv, delta, gamma)

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
        
def AsianOption(aelOption, d):
    """AsianOption(aelOption, d)

    Valuation function of asian options

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
    t = ael.date_valueday().days_between(aelOption.exp_day)/365.0
    FairForward = s*math.exp((r-d)*t)
    if printout: print 'FairForward = ', FairForward 
    # Calculate sigma (volatility)
    vs    = aelOption.used_volatility(aelOption.curr)
    # Changed by PG and SM on 12/03/03. Skew is defined in terms of a relative to spot percentange not
    # absolute strike. Changed appropriately.
    if printout: print 'ATM Vol on Expiry = ', vs.volatility(0, aelOption.exp_day)*100
    sigma = vs.volatility((k/FairForward-1)*100, aelOption.exp_day) 

    #Test Values

    #r = nac2ccr(1, 0.08)
    #sigma = 0.2325
    #s= 8990.0
    

    if printout: print 'Volatility = ', sigma*100
    if printout: print 'Moneyednes = ', (k/FairForward-1)*100
    if printout: print 'Expiry = ', aelOption.exp_day
    
    # Determine phi (1 = call, -1 = put)
    if aelOption.call_option:
        phi =  1.0
    else:
        phi = -1.0

    #Need to get ave dates and calc ave spot so far

    ave_dates = []
    ave_spot = 0
    n = 0

    if len(aelOption.time_series()) == 0:
    
    	ael.log('Error - Instrument ' + aelOption.insid + ' has no averaging dates!')
    	return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    for ts in aelOption.time_series():
    	if ts.ts_specnbr.field_name == 'FAveragePrices':
    	    ave_dates.append(ts.day) 

	    if ts.value != -1 and ts.day <= ael.date_valueday():
		ave_spot = ave_spot + ts.value
		n = n + 1

    ave_dates.sort()
    if n > 0: 
    	ave_spot = ave_spot / n
	mTheta = 1
    else:
    	ave_spot = s
	mTheta = 0

    if printout: print '-----------------'
    if printout: print 'Ave s \t= ', ave_spot
    if printout: print 's \t= ', s
    if printout: print 'k \t= ', k
    if printout: print 'r \t= ', r
    if printout: print 'sigma\t= ', sigma
    if printout: print 't \t= ', t
    if printout: print 'd \t= ', d
    if printout: print 'phi\t= ', phi

    if t < 0:
    	return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    elif t == 0:
        return max(0.0, phi*(ave_spot-k)), 0.0, 0.0, 0.0, 0.0, 0.0
    else:

   	#Create list of fractional dates for averaging
    	#Calc m, number of averaging dates passed by value date
	
    	asian_times = []
	m = 0
	
	for ave_date in ave_dates:
	    asian_times.append(ael.date_valueday().days_between(ave_date)/365.0)
    	    if ave_date <= ael.date_valueday():
	    	m = m + 1
	
	#Get pv
	pv, delta, gamma = AsianVorst(s, k, ave_spot, r, t, d, sigma, phi, asian_times, m)
	
	#Calc rho
    	
    	r1 = math.exp(r) - 1
	r1 = r1 + 0.01
	r1 = math.log(1 + r1)
	
	pv1 = AsianVorst(s, k, ave_spot, r1, t, d, sigma, phi, asian_times, m)[0]
	
	rho = pv1 - pv
	
	#Calc vega
	
	sigma1 = sigma + 0.01
	
	pv1 = AsianVorst(s, k, ave_spot, r, t, d, sigma1, phi, asian_times, m)[0]
    	
	vega = pv1 - pv

	#Calc theta
	
	t1 = t - 1.0 / 365.0
	
	if t1 <= 0.00000000001:
	    
	    pv1 = max(0, phi * (ave_spot - k))
	    
	else:
	    
	    asian_times = []
	    
	    for ave_date in ave_dates:
	    	asian_times.append(ael.date_valueday().add_days(1).days_between(ave_date)/365.0)
	    
	    if mTheta: mTheta = m + 1
	    
	    pv1 = AsianVorst(s, k, ave_spot, r, t1, d, sigma, phi, asian_times, mTheta)[0]
	
	theta = pv1 - pv

    	if aelOption.pay_day_offset:
    	    yc = aelOption.used_yield_curve()
	    expiry_date = aelOption.exp_day
	    pay_date = expiry_date.add_banking_day(aelOption.und_insaddr.curr, aelOption.pay_day_offset)

	    df = yc.yc_rate(expiry_date, pay_date, 'None', 'None', 'Discount')
    	
	    pv = pv * df
	
	if printout: print 'Delta ', delta
	if printout: print 'Gamma ', gamma
	if printout: print 'Theta ', theta
	if printout: print 'Rho', rho
	if printout: print 'Vega', vega
	if printout: print 'Present Value', pv
	if printout: print '################################'
	return [pv, delta, gamma, theta, rho, vega]

def pvExp(i, calc=1, ref=0):
    """pvExp(i, calc=1, ref=0)

    Wrapper function for valuation of asian options on dividend equities.
    Explicit dividend yield is retrieved from the underlying"""

    if calc and i.record_type == 'Instrument' and i.instype == 'Option':

	# retrieve d (dividend yield) from additional info (NACA format)
        d = float(i.und_insaddr.add_info('DividendYield'))
        # Convert d from NACA to CCR format
        d = nac2ccr(1, d)

        res = AsianOption(i, d)[0:4]
    		
    else:

    	res = [0.0, None, None, None]

    return [ [ res, i.exp_day, i.curr] ]

def pvImp(i, calc=1, ref=0):
    """pvImp(i, calc=1, ref=0)

    Wrapper function for valuation of asian options on dividend equities.
    Dividend yield is calculated implicitly from underlying's cash dividends"""

    if calc and i.record_type == 'Instrument' and i.instype == 'Option':

	# Calculate implicit yield from cash dividends
        d = DividendYieldFromCash(i)

     	res = AsianOption(i, d)[0:4]
	
    else:
        res = [0.0, None, None, None]

    return [ [ res, i.exp_day, i.curr] ]


def SQL_Greeks(i, greek, *rest):
    
    if i.record_type == 'Instrument' and i.instype == 'Option':
    
	if i not in cached_greeks.keys():

	    # retrieve d (dividend yield) from additional info (NACA format)
            d = float(i.und_insaddr.add_info('DividendYield'))
            # Convert d from NACA to CCR format
            d = nac2ccr(1, d)

    	    res = AsianOption(i, d)

    	    pv  = res[0]
	    delta  = res[1]
	    gamma  = res[2]
	    theta  = res[3]
	    rho  = res[4]
	    vega = res[5]

    	    cached_greeks[i] = [pv, delta, gamma, theta, rho, vega]

    	if greek == 'PV':
	    return cached_greeks[i][0]
	if greek == 'Delta':
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
    d = float(i.und_insaddr.add_info('DividendYield'))
    # Convert d from NACA to CCR format
    d = nac2ccr(1, d)
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
