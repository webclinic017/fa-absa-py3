'''
    Date                : 2010-05-21; 2010-09-21
    Purpose             : * Used to calculate breakeven credit spread for CLN deals
                          * Fixed secant algorithm to stop if it doesn't converge
    Department and Desk : FO Credit; Prime Services Collateral Management
    Requester           : Parbhoo-Kanjee, Trusha; Nhlapo, Mduduzi
    Developer           : Rohan van der Walt
    CR Number           : 319427, 444702
'''

import acm, ael

context = acm.GetDefaultContext()
sheet_type = 'FPortfolioSheet'
calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )

def myFunc(shift, **rest):
    """
    Gets a dictionary in rest containg the CDS ins
    apply shift to CDS 
    calculate new value of combination
    return difference between nominal supplied and loss/gain in combination value
    """
    Trade = rest['trade']
    Ins = Trade.Instrument()
    if Ins.InsType() == 'CreditDefaultSwap':
        #1. Create a scenario object.
        scenario = acm.FExplicitScenario()
        #2. Create the individual shifts and store them in a shift vector object.
        #Only shift credit curve, and store in shift vector
        shiftVector = acm.CreateShiftVector('shiftCurveParCDSRateAbs', 'Credit Yield Curve', None)
        shiftVector.AddShiftItem([shift])
        #3. Apply the shift vector to the scenario object.
        scenario.AddShiftVector(shiftVector)
        #4. Call the Standard Calculation with the scenario as a parameter
        aspect = acm.FScenarioAspect()
        colCreatorConf = acm.Sheet.Column().ConfigurationFromScenario( scenario, aspect )
        column_id = 'Portfolio Net Asset Value'
        value = rest['calc_space'].CreateCalculation( Trade, column_id, colCreatorConf ).Value().Number()
        return value - rest['nominal']
    else:
        return 0

def simulate(t, *rest):
    if t.insaddr.instype == 'CreditDefaultSwap':
        t = acm.FTrade[t.trdnbr]
        target = -t.FaceValue()/2
        x0 = +5
        x1 = +10
        return secant(myFunc, x0, x1, calc_space = calc_space, trade=t, nominal=target)
    else:
        return 0
    
def secant(func, oldx, x, TOL=1e-6, **rest):    # f(x)=func(x)
    """
    Similar to Newton's method, but the derivative is estimated by line through 2 starting points.
    http://en.wikipedia.org/wiki/Secant_method
    """

    oldf, f = func(oldx, **rest), func(x, **rest)
    if (abs(f) > abs(oldf)):        # swap so that f(x) is closer to 0
        oldx, x = x, oldx
        oldf, f = f, oldf
    count = 0
    while True:
        dx = f * (x - oldx) / float(f - oldf)
        if abs(dx) < TOL * (1 + abs(x)): 
            return str("%.3f" % (x-dx))
        else:
            if count >= 500:
                return 'COULD NOT FIND BREAKEVEN TRIGGER'
        oldx, x = x, x - dx
        oldf, f = f, func(x, **rest)
        count = count + 1
