import ael
try:
    import math
except:
    print 'Error! AEL Module FC_SAFEX_VAL unable to import Math module'

def SafexCulmulativeNormal(d):
    a  =  0.2316419
    b1 =  0.31938153
    b2 = -0.356563782
    b3 =  1.781477937
    b4 = -1.821255978
    b5 =  1.330274429
    
    factor = 0.3989422804014330 # = (2.0 * PI)^-0.5
    
    z = abs(d)
    
    k = 1.0/(1.0 + a * z)
    k2 =  k * k
    k3 = k2 * k
    k4 = k3 * k
    k5 = k4 * k
    
    Nz = 1 - factor * math.exp(z * z/-2.0) * (b1*k + b2*k2 + b3*k3 + b4 * k4 + b5 * k5)
    
    if d > 0:
    	Nd = Nz
    elif d == 0.0:
    	Nd = 0.5
    else:
    	Nd = 1.0 - Nz
    
    return Nd

def SafexBlack(u_price, strike, vol, tenor, call_option):
    try:
	if tenor<=0:
    	    C = max(u_price - strike, 0.0)
	else:
    	    factor = vol * math.sqrt(tenor)
    	    d1 = (math.log(u_price/strike) + vol * vol * tenor / 2.0)/factor
	    d2 = d1 - factor
	    C = u_price * SafexCulmulativeNormal(d1) - strike * SafexCulmulativeNormal(d2)

	if call_option:
    	    V = max(C, u_price - strike)
	    print V
	else:
    	    V = max(C - u_price + strike, strike - u_price)
	    print V
    	return V
	#return round(V,4)
    except:
    	return 0.0
	

def pv_BS(i, calc, ref):
    
    try:
    	trace_level = int(i.add_info('AEL Trace Level'))
    except:
    	trace_level = 0
    
    result = [ [ 0.0, i.exp_day, i.curr, 'Fixed' ] ]

    if not(calc): return result
    
    if i.instype != 'Option':
    	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_BS()"' %(i.insid)
	print 'This function is only valid for Safex Futures Options, but this instrument is a "%s"' %(i.instype) 
    	return result

    underlying = i.und_insaddr
    
    if underlying.instype != 'Future/Forward':
       	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_BS()"' %(i.insid)
	print 'This function is only valid if the underlying is a Future or Forward, but this underlying is a "%s"' %(underlying.instype)
	return result
	
    if  i.digital or i.barrier:
    	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_BS()"' %(i.insid)
	print 'This function is only valid for plain vanilla options that can be valued in a Black&Scholes framework.'
	return result

    #Get our parameters' values ---------------------------------------------------------------------------
    u_price     = i.used_und_price(i.undprice_type())
    print  u_price
    #tenor       = i.years_to_maturity() This method isn't adequate as it doesn't allow ATLAS to calc Theta
    tenor       = ael.date_valueday().days_between(i.exp_day, 'Act/365') / 365.0
    vol         = i.used_vol() / 100.0
    risk_free   = i.used_discount_rate() / 100.0
    coc         = 0   #underlying is a future or forward, so the "spot" price is already a forward price
    strike      = i.strike_price
    call_option = i.call_option
    american    = (i.exercise_type == 'American')
    dividends   = []
    model       = 'BlackScholes'
    steps       = 2000
    pay_offset  = i.pay_day_offset
    #------------------------------------------------------------------------------------------------------
    
    if trace_level >= 2: print '\n\nSafex Option Val: ---------------------------------------------'
    if trace_level: print 'Instrument     = %s' %(i.insid)
    if trace_level >= 2:
    	print 'Underlying     = %s\nUnd Spot Price = %f\nTenor/yrs      = %f\nRaw Vol        = %f\nRisk Free      = %f\nCoC            = %f\nStrike         = %f' %(underlying.insid, u_price, tenor, vol, risk_free, coc, strike)
    	print 'Call Option    = %i\nAmerican       = %i' %(call_option, american)
    	print 'Dividends      =', dividends
    	print 'Model          = %s\nSteps          = %i' %(model, steps)
    
    #------ Round Volatility to 4 decimal places in accordance with Safex rules ----
    vol = round(vol, 4)
    #-------------------------------------------------------------------------------
    
    if trace_level >=2: print 'Rounded Vol    = %f' %vol

    pv = ael.eq_option(u_price, tenor, vol, risk_free, 0.0, strike, call_option, american, dividends, model, steps)
    
    if pay_offset:
    	yc = i.used_yield_curve()
	expiry_date = i.exp_day
	pay_date = expiry_date.add_banking_day(underlying.curr, pay_offset)

	df = yc.yc_rate(expiry_date, pay_date, 'None', 'None', 'Discount')
    	
	if trace_level >=2:
	    print 'Pay Day Offset = %i\nYield Curve    = %s\nAdjust Factor  = %f' %(pay_offset, yc.ir_name, df)
	
	pv = pv * df

    if trace_level: print 'PV             = %f' %pv
    if trace_level >=2: print '---------------------------------------------------------------'

    return [ [ pv, i.exp_day, i.curr, 'Fixed' ] ]


def pv_Blk(i, calc, ref):
    
    try:
    	trace_level = int(i.add_info('AEL Trace Level'))
    except:
    	trace_level = 0
    
    result = [ [ 0.0, i.exp_day, i.curr, 'Fixed' ] ]

    if not(calc): return result
    
    if i.instype != 'Option':
    	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_Blk()"' %(i.insid)
	print 'This function is only valid for Safex Futures Options, but this instrument is a "%s"' %(i.instype) 
    	return result

    underlying = i.und_insaddr
    
    if underlying.instype != 'Future/Forward':
       	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_Blk()"' %(i.insid)
	print 'This function is only valid if the underlying is a Future or Forward, but this underlying is a "%s"' %(underlying.instype)
	return result
	
    if i.digital or i.barrier:
    	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_Blk()"' %(i.insid)
	print 'This function is only valid for plain vanilla options that can be valued in a Black&Scholes framework.'
	return result
    
    if (i.pay_day_offset != 0):
    	print 'Valuation Function Mapping Error!\nInstrument "%s" has been mapped to AEL Valuation Function "FC_SAFEX_Val.pv_Blk()"' %(i.insid)
	print 'This function is only valid for options that pay out on their exercise day. But this instrument has a pay day offset of %i day(s)' %(i.pay_day_offset)
	return result
    
    #Get our parameters' values ---------------------------------------------------------------------------
    u_price     = i.used_und_price(i.undprice_type())
    print  'Underlying price', round(u_price, 0)
    tenor       = ael.date_valueday().days_between(i.exp_day, 'Act/365') / 365.0
    vol         = i.used_vol() / 100.0
    strike      = i.strike_price
    call_option = i.call_option
    #------------------------------------------------------------------------------------------------------
        
    if trace_level >= 2: print '\n\nSafex Option Val: ---------------------------------------------'
    if trace_level: print 'Instrument     = %s' %(i.insid)
    if trace_level >= 2:
    	print 'Underlying     = %s\nUnd Spot Price = %f\nTenor/yrs      = %f\nRaw Vol        = %f\nStrike         = %f' %(underlying.insid, u_price, tenor, vol, strike)
    	print 'Call Option    = %i' %(call_option)
	print 'Model          = Safex Black'
    
    #------ Round Volatility to 4 decimal places in accordance with Safex rules and constrain it ----
    MaxVol, MinVol = 0.0, 0.0
    VolStruct = ael.Volatility[i.used_volatility().vol_name]
    try:
        MaxVol = float(VolStruct.add_info('Max Vol'))
    except:
    	MaxVol = 0
    try:
        MinVol = float(VolStruct.add_info('Min Vol'))
    except:
    	MinVol = 0
    if trace_level >= 2: print 'MaxVol         = %f\nMinVol         = %f' %(MaxVol, MinVol)
    
    if MaxVol: vol = min(vol, MaxVol)
    if MinVol: vol = max(vol, MinVol)
    vol = round(vol, 4)
    
    #------------------------------------------------------------------------------------------------
    
    if trace_level >=2: print 'Rounded Vol    = %f' %vol

    pv = SafexBlack(u_price, strike, vol, tenor, call_option) #rounding added on 29/08/2003 SafexBlack(round(u_price,0), strike, vol, tenor, call_option)
    pv = (i.contr_size*pv)/i.contr_size	# Rounding added on 6Feb2003 round(i.contr_size*pv,0)/i.contr_size
    #pv = (i.contr_size*pv)/i.contr_size	
    if trace_level: print 'PV             = %f' %pv
    if trace_level >=2: print '---------------------------------------------------------------'
    

    

    return [ [ pv, i.exp_day, i.curr, 'Fixed' ] ]




