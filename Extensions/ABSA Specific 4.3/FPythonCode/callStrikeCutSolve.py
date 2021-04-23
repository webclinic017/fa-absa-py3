import acm
import ael
import math

target_delta = 0.00005

def getPrice(object, **rest):
    var_swap = object.Instrument()

    estimate1, estimate2 = get_solver_estimates(var_swap) 
    cutoff_strike = secant(find_strike, estimate1, estimate2, var_swap)

    return cutoff_strike

def rational_approximation(t):
    # Abramowitz and Stegun formula 26.2.23.
    # The absolute value of the error should be less than 4.5 e-4.
    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]
    numerator = (c[2]*t + c[1])*t + c[0]
    denominator = ((d[2]*t + d[1])*t + d[0])*t + 1.0
    return t - numerator / denominator

def normal_CDF_inverse(p):
    assert p > 0.0 and p < 1        
    if p < 0.5:
        # F^-1(p) = - G^-1(p)
        return -rational_approximation(math.sqrt(-2.0*math.log(p)))
    else:
        return rational_approximation(math.sqrt(-2.0*math.log(1.0-p)))

def get_underlying_price(ins, calculationSpace):
    calculationSpace.Clear()
    calculation = ins.Calculation()
    return calculation.UnderlyingPrice(calculationSpace).Number()

def get_forward_price(ins, fwd_date, calculationSpace):
    calculationSpace.Clear()
    calculation = ins.Calculation()
    return calculation.ForwardPrice(calculationSpace, fwd_date).Number()

def calculate_strike(fwd_price, vol, time_to_expiry, spot_price, discount_factor, deltacutoff):
    val = fwd_price * math.exp(0.5 * vol**2 * time_to_expiry - \
           normal_CDF_inverse(deltacutoff * spot_price / (fwd_price * discount_factor)) * \
           vol * math.sqrt(time_to_expiry))
    return val

def get_discountfactor(ins, end_date):
    yield_curve = ins.MappedDiscountLink().Link().YieldCurveComponent()
    return yield_curve.IrCurveInformation().Rate(acm.Time().DateToday(), end_date, 'Discount', 'Act/365', 'Discount', None, 0)

def get_distinct_elements(input):
    ''' Return the last two distinct elements from a list.  
        If all elements are the same then increment the one element. 
    '''    
    distinct_items = sorted(list(set(input)))
    
    if len(distinct_items) > 1:
        return distinct_items[len(distinct_items)-1], distinct_items[len(distinct_items)-2] 
    else:
        return distinct_items[0], distinct_items[0] + 100

def get_solver_estimates(var_swap):
    calculationSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    option = acm.FInstrument['OptionDefault']

    expiry_date = var_swap.ExpiryDate()

    option.Simulate()

    option.Underlying(var_swap.Underlying())
    option.ExpiryDate(expiry_date)
    option.Currency(var_swap.Currency())
    option.StrikeCurrency(var_swap.Currency())
    option.IsCallOption(True)
    
    vol_surface = option.MappedVolatilityLink().Link().VolatilityStructure()        
    vol_information = vol_surface.VolatilityInformation(acm.Time().DateToday(), 0.00001)

    fwd_price = get_forward_price(option.Underlying(), expiry_date, calculationSpace)
    spot_price = get_underlying_price(option, calculationSpace)     
    time_to_expiry = acm.Time().DateDifference(expiry_date, acm.Time().DateToday()) / 365.0
    df = get_discountfactor(option, expiry_date)        
    
    option.Unsimulate()    

    K = fwd_price
    strike_estimates = []
    for i in range(5):                
        vol = vol_information.Value(expiry_date, expiry_date, K, True, False)
        K = calculate_strike(fwd_price, vol, time_to_expiry, spot_price, df, target_delta)
        strike_estimates.append(K)   

    estimate1, estimate2 = get_distinct_elements(strike_estimates)
		
    return estimate1, estimate2
    
def secant(func, oldx, x, var_swap, TOL=1e-7):
    calculationSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()  
    option = acm.FInstrument['OptionDefault']        
    option.Simulate()
    option.Underlying(var_swap.Underlying())
    option.ExpiryDate(var_swap.ExpiryDate())
    option.IsCallOption(True)
    option.StrikeCurrency(var_swap.Currency())
    option.Currency(var_swap.Currency())
	
    oldf, f = func(oldx, option, calculationSpace), func(x, option, calculationSpace)
    if (abs(f) > abs(oldf)):        # swap so that f(x) is closer to 0
        oldx, x = x, oldx
        oldf, f = f, oldf
    count = 0
    while True:    
        if (float(f-oldf) == 0):
            option.Unsimulate()
            return 'Optimization did not converge'
        dx = f * (x - oldx) / float(f - oldf)
        if abs(dx) < TOL * (1 + abs(x)):
            option.Unsimulate()		
            return str("%.10f" % (x-dx))
        else:
            if count >= 500:
                option.Unsimulate()
                return 'Optimization did not converge'
        oldx, x = x, x - dx
        oldf, f = f, func(x, option, calculationSpace)
        count = count + 1    

def find_strike(strike, ins_option, calculationSpace):
    ins_option.StrikePrice(strike)
    calculationSpace.Clear()   
    calculation = ins_option.Calculation()    
    delta = calculation.PriceDelta(calculationSpace)
    
    return delta.Number() - target_delta
