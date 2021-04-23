from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FCalcUtilTemplate - Module containing a user defined yield curve 
    calibration (bootstrapping) template hook: 
    
    FCalibrateYieldCurve( dates, prices, instruments, yieldCurveName)

DESCRIPTION
    This Python implementation replicates the built-in FRONT ARENA 
    yield curve Calibration Method 'Default', i.e. the algorithms in 
    Numerical Recipes In C chapter 9.6

    To activate the user defined yield curve bootstrapping hook:
    
    1. Re-name the module to FCalcUtil
    
    2. Enter the name of the hook function, FCalibrateYieldCurve,
    in the Estimation choice list in Administration Console. The 
    Estimation list must be included in the MASTER choice list.

    3. The estimate hook is activated by setting the Calibration 
    Method to User Defined in the Yield Curve Definition window. 
    Select FCalibrateYieldCurve from the drop-down choice list 
    in the appearing User Defined combo box field.
    
    (c) Copyright 2011 by SunGard Front Arena. All rights reserved.

----------------------------------------------------------------------------"""

import acm

def getDefaultScenarioConfiguration(irCurveInfo):
    """
    Return the default scenario configuration 
    used in the calibration space.
    """
    
    scen = acm.FExplicitScenario()
    dim = acm.FDirectScenarioDimension()
    calcSpec = acm.FCalculationSpecification()

    # Create scenario members
    m1 = acm.CreateScenarioMember( acm.GetFunction("fixedVariant", 2), ["discountIrCurveInformation"], acm.FObject, irCurveInfo)
    m2 = acm.CreateScenarioMember( acm.GetFunction("fixedVariant", 2), ["forwardIrCurveInformation"], acm.FObject, irCurveInfo)

    # Each scenario member make one dimension
    dim.AddScenarioMember(m1)
    dim.AddScenarioMember(m2)

    # Add dimension to scenario
    scen.AddDimension(dim)
    # Get the configuration
    config = acm.Sheet().Column().ConfigurationFromScenario(scen)
    
    return config

def calcTheoreticalPrice(values, dates, prices, instruments, yieldCurve, irCurve, calcSpace):
    """
    The function calcTheoreticalPrice calculates the non linear 
    function F(x) to be minimzed. 

    The function is defined as 
    F(x) = Theoretical Prices(rates) - Prices
    where rates is the rate vector ('values') and Prices ('prices') 
    is the vector with market price
    """

    # Set the new rate values
    for value, date in zip(values, dates):
        irCurve.AddPoint(value, date)
    
    irCurveInfo = irCurve.IrCurveInformation()
    # Re-calculate Interpolation Coefficients
    irCurveInfo.RecalculateInterpolationCoefficients()
       
    config = getDefaultScenarioConfiguration(irCurveInfo)
       
    # For each instrument, calculate the function values
    result = []
    for instrument, price in zip( instruments, prices):
        calculation = calcSpace.CreateCalculation(instrument, 'Standard Calculations Calibration Curve Theoretical Price', config)
        calcSpace.SimulateValue(instrument, 'Standard Calculations Valuation Date', irCurveInfo.ReferenceDate())
        result.append( calculation.Value().Number() - price )
    irCurveInfo = None
    return result


def usrfun( xp, alpha, beta, m, n, calc_jacobian, dates, prices, instruments, yieldCurve, irCurve, calcSpace):
    """
    The function usrfun calculates the vector of function values 
    and the matrix of cross derivatives (Jacobian). The Jacobian 
    is computed by finite difference approximations.
    """
    if not calc_jacobian:
        funcValues = calcTheoreticalPrice( xp, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
        for i in range(m):
            beta[i] = - funcValues[i]
    else:
        delta = 1.e-6
        for j in range(n):
            x = xp[j]
            xp[j] += delta
            funcValues = calcTheoreticalPrice( xp, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
            for i in range(m):
                diff = funcValues[i] + beta[i]
                alpha[i][j] = diff / delta
            xp[j] = x


def lufactor( LU, ipivot, D, nrows, ztol = 1.0e-12 ):
    """
    The function lufactor computes the LU factorization of the matrix A
    
    detsign = lufactor( LU, ipivot, D, nrows, ztol = 1.0e-12 )

    Input arguments
        LU              matrix to be factored
        ipivot          array of row interchanges made
        D               Work area, array of size nrows
        nrows           number of rows in matrix
        ztol            zero value tolerance

    Output
        detsign         Sign of determinant (0 singular matrix)

    Description
        Splits a square matrix into a lower and an upper triangular 
        matrix L and U, stored in LU, with the row interchanges
        stored in ipivot using implicit scaled partial pivoting.

    Reference
        This routine is based on the FORTRAN 77 routine
        FACTOR of Conte and deBoor.
    """
    # Initialize ipivot, D
    detsign = 1
    for i in range(nrows):
        ipivot[i] = i
        rowmax = max([abs(x) for x in LU[i]])
        if rowmax <= ztol:
            detsign =  0
            rowmax  = 1
        D[i] = rowmax
    if nrows <= 1: 
        return detsign

    # Loop over rows, fatorization matrix
    for k in range(nrows-1):
        # Deterrmine pivot row, the row star
        colmax = abs(LU[k][k]) / D[k]
        istar  = k
        for i in range(k+1, nrows):
            t = abs(LU[i][k]) / D[i]
            if t > colmax:
                colmax = t
                istar  = i
        if colmax <= ztol:
            detsign = 0
        else:
            if istar > k:
                # Make k the pivot row by interchanging it with the chosen row istar
                detsign = -detsign
                ipivot[istar], ipivot[k] = ipivot[k], ipivot[istar]
                D[istar], D[k] = D[k], D[istar]
                for j in range(nrows):
                    LU[istar][j], LU[k][j] = LU[k][j],LU[istar][j]

            # Eliminate elements from rows k+1, .., nrows
            for i in range(k+1, nrows):
                ratio = LU[i][k] = LU[i][k] / LU[k][k]
                for j in range(k+1, nrows):
                    LU[i][j] = LU[i][j] - ratio * LU[k][j]
    if LU[nrows-1][nrows-1] <= ztol:
        detsign = 0

    return detsign


def lusolve( X, LU, ipivot, B, nrows ):
    """
    The function lusolve solves the linear equations system LU x = b
    
    lusolve( X, LU, ipovt, B, nrows )

    Input arguments
        X               unknown solution vector to be solved
        LU              LU decomposition matrix
        ipivot          row interchanges vector
        B               RHS vector of (LU) X = B
        nrows           number of unknowns and rows in matrix

    Description
        Solves the equation (LU) X = B for X.
        Once we have an LU factorization of a matrix A,
        it is very easy to solve for X given any RHS vector B.

    Reference
        This routine is based on the FORTRAN 77 routine
        SUBST of Conte and deBoor.
    """
    if (nrows == 1) :
        X[0] = B[0] / LU[0][0]
        return

    #  Forward substitution
    X[0] = B[ipivot[0]]
    for i in range(1, nrows):
        t = 0.0
        for j in range(i):
            t += (LU[i][j] * X[j])
        X[i] = B[ipivot[i]] - t

    # Back substitution
    X[nrows-1] = X[nrows-1] / LU[nrows-1][nrows-1]
    for i in range(nrows -2 , -1, -1):
        t = sum([LU[i][j] * X[j] for j in range(i+1,  nrows)])
        X[i] = (X[i] - t) / LU[i][i]
    return


def newton_raphson( xp, n, tolx, tolf, ntrial, minx, maxx, dates, prices, instruments, yieldCurve, irCurve, calcSpace):
    """
    The function newton_raphson computes an approximate root to a non-linear
    equation system

    It performs ntrial iterations to compute the root to the non-linear equation 
    system. Iteration stops if either the sum of the magnitudes of the 
    function values is less than some tolerance tolf, or the sum of the absolute 
    values of the corrections to dxi is less than some tolerance tolx. 

    The function newton_raphson calls a user supplied function usrfun which 
    provide the function values F and the Jacobian matrix J. The linear equation 
    system J dx = F is solved using a LU factorization.
    
    The function returns 1 upon success, otherwise 0
    """
    alpha  = [ n * [0.0] for i in range(n) ]
    beta   = [0.0]* n
    ipivot = list(range(n))
    D      = [0.0]* n
    for k in range(ntrial):
        lambd = 1.0
        usrfun( xp, alpha, beta, n, n, False, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
        
        # converged to solution?
        errf = sum( [ abs(x) for x in beta ] )
        if errf <= tolf: 
            return k+1

        usrfun( xp, alpha, beta, n, n, True, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
        
        # LU factorize Jacobian (alpha)
        if not lufactor( alpha, ipivot, D, n):
            print ("Error in Newton-Raphson: Jacobian is singular")
            return 0
            
        # solve LU x = B, solution vector in beta
        lusolve( beta, alpha, ipivot, beta, n )

        # compute step size lambda
        for i in range(n):
            if beta[i] < 0  and minx - xp[i] > lambd * beta[i]:
                lambd = ( minx - xp[i] ) / beta[i]
            elif beta[i] > 0 and maxx - xp[i] < lambd * beta[i]:
                lambd = ( maxx - xp[i] ) / beta[i]
                
        # update solution vector and compute errx
        errx=0.0;
        for i in range(n):
            errx = errx + abs( beta[i] )
            xp[i] = xp[i] + beta[i] * lambd
        
        # converged to solution?
        if errx <= tolx:
            return k+1
        
    return 0
    

def newton_raphson_svd( xp, m, n, tolx, tolf, ntrial, minx, maxx, dates, prices, instruments, yieldCurve, irCurve, calcSpace):
    """
    The function newton_raphson_svd computes an approximate root to a non-linear
    equation system

    It performs ntrial iterations to approximate the root to the non-linear equation 
    system. Iteration stops if either the sum of the magnitudes of the 
    function values is less than some tolerance tolf, or the sum of the absolute 
    values of the corrections is less than some tolerance tolx. 

    The function newton_raphson_svd calls a user supplied function usrfun which 
    provide the function values F and the Jacobian matrix J. The linear equation 
    system J dx = F is solved in least square sense by the singular value
    decomposition.
    
    The function returns 1 upon success, otherwise 0
    """
    if m < n:
        return 0
    try:
        import FSingularValueDecomposition as svd
    except:
        print ("No Singular Value Decomposition module found")
        xp = [0.0] * n
        return 0
        
    alpha  = [ n * [0.0] for i in range(m) ]
    beta   = [0.0] * m
    tmp    = [0.0] * n
    dx     = [0.0] * n
    w      = [0.0] * n
    v      = [ n * [0.0] for i in range(n) ]
    for k in range(ntrial):
        lambd = 1.0
        usrfun( xp, alpha, beta, m, n, False, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
        
        # converged to solution?
        errf = sum( [ abs(x) for x in beta ] )
        if errf <= tolf: 
            return k+1

        usrfun( xp, alpha, beta, m, n, True, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
        
        # svd factorize Jacobian (alpha)
        if not svd.svdcmp( alpha, m, n, w, v, tmp ):
            print ("Singular Value Decomposition failed")
            return 0
            

        # solve LU x = B, solution vector in beta
        svd.svdsolve( alpha, w, v, m, n, beta, dx, tmp)

        # compute step size lambda
        for i in range(n):
            if dx[i] < 0  and minx - xp[i] > lambd * dx[i]:
                lambd = ( minx - xp[i] ) / dx[i]
            elif dx[i] > 0 and maxx - xp[i] < lambd * dx[i]:
                lambd = ( maxx - xp[i] ) / dx[i]
                
        # update solution vector and compute errx
        errx=0.0;
        for i in range(n):
            errx = errx + abs( dx[i] )
            xp[i] = xp[i] + dx[i] * lambd
        
        # converged to solution?
        if errx <= tolx:
            return k+1
        
    return 0


def FCalibrateYieldCurve( dates, prices, instruments, yieldCurveName):
    """
    The function FCalibrateYieldCurve is a Python implementation 
    that replicates the built-in Front Arena yield curve 
    calibration.

    FCalibrateYieldCurve( dates, prices, instruments, yieldCurveName)

    Input arguments
        dates            vector with dates for which rates is to be calculated
        prices            market prices for benchmark instruments
        instruments        vector with benchmark instrument names
        yieldCurveName    name of the yield curve

    Returns a list with the interest rates
    """
    # Number of equations (instruments/prices)
    nbr = len( instruments )
    
    # Number of parameters (dates)
    npars = len( dates )
    
    # Check the problem type...
    if nbr < npars:
        print ("No Unique Solution: Number of equations is less than the number of parameters")
        return [0.0 for i in range(npars)]
    optimize = nbr > npars

    # Get the FYieldCurve, FIrCurveInformation and a calibration object
    yieldCurve = acm.FYieldCurve[ yieldCurveName ].Clone()
    irCurveInfoOriginal = yieldCurve.IrCurveInformation()
    
    # Create a curve building template object to be used as the calibration object.
    irCurve = acm.CurveBuilding.NewTemplate()

    # Copy the yield curve properties to the calibration object.
    # Below is an example of how to set the properties for a curve with type Benchmark
    # and curve format ZC. For a spread curve with curve format ZC, the type would have
    # to be changed to Spread and the underlying curve specified.
    curr = yieldCurve.Currency()
    cal = curr.Calendar()
    irCurve.StorageDayCount(yieldCurve.StorageDayCount())
    irCurve.StorageRateType(yieldCurve.StorageCompoundingType())
    # Calculation Format hard coded in this example to 'Use Storage Format'
    irCurve.InternalCompoundingType(yieldCurve.StorageCompoundingType())
    irCurve.InternalDaycountMethod(yieldCurve.StorageDayCount())
    irCurve.StorageCalcType('Spot Rate')
    irCurve.PayDayMethod(yieldCurve.PayDayMethod())
    irCurve.ReferenceDate(irCurveInfoOriginal.ReferenceDate())
    irCurve.Type('Benchmark')
    irCurve.Format('Zero Coupon Curve')
    irCurve.CalendarInformation(cal.CalendarInformation())
    # UserDefined (or Section) interpolation for zero coupon curves not supported in this example
    irCurve.InterpolationType(yieldCurve.InterpolationType())
    irCurve.ExtrapolationTypeShortEnd(yieldCurve.ExtrapolationTypeShortEnd())
    irCurve.ExtrapolationTypeLongEnd(yieldCurve.ExtrapolationTypeLongEnd())
    # Interpolation Rate Type 'Forward Rate' not supported in this example
    irCurve.InterpolationRateType('Spot Rate')
    # Sequential (/dependent) calibration or Dual Calibration not supported in this example
    irCurve.ForwardPeriod('0d')
    # All the valid FIrCurveTemplate set methods can be viewed in the AEF Browser
    
    
    # Create a Calculation Space for Standard Calculations
    calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
    
    # load the instruments
    instruments = [ acm.FInstrument[ instrument ] for instrument in instruments ]

    # Data for the Newton-Raphson algorithm (note that these are not identical to default Calibration Settings)
    tolx = 1.e-6
    tolf = 1.e-6
    ntrial = 20
    minx = -5
    maxx = 5
    xp = [0.01]* npars
    
    if optimize:
        result = newton_raphson_svd( xp, nbr, npars, tolx, tolf, ntrial, minx, maxx, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
    else:
        result = newton_raphson( xp, npars, tolx, tolf, ntrial, minx, maxx, dates, prices, instruments, yieldCurve, irCurve, calcSpace)
    
    if not result:
        print ("The Newton-Raphson solver failed to find a root to the non-linear equation system")

    return xp

def FCalibrateISDARiskFreeCurve( dates, prices, instruments, yieldCurveName):
    """
    Calibrates the Standard ISDA Risk free curve

    FCalibrateISDARiskFreeCurve( dates, prices, instruments, yieldCurveName)

    Input arguments
        dates            vector with dates for which rates is to be calculated
        prices            market prices for benchmark instruments
        instruments        vector with benchmark instrument names
        yieldCurveName    name of the yield curve

    Returns a list with the interest rates
    """
    
    # Number of equations (instruments/prices)
    nbr = len( instruments )
    # Number of parameters (dates)
    npars = len( dates )
    xp = []
    
    # Problem validation check
    if nbr != npars:
        print ("Calibration failed, number of benchmarks must equal number of points in curve")
        return xp
        
    # Fetch the benchmark instruments
    instruments = [ acm.FInstrument[ instrument ] for instrument in instruments ]
    
    # Load calibration function
    func = acm.GetFunction("isdaCalibrateRiskFreeCurve", 5)
    
    holidayFile = "None"
    if acm.FYieldCurve[yieldCurveName].Currency().Name() == "JPY":
        holidayFile = "TYO"

    try:
        for p in func(dates, instruments, prices, holidayFile, acm.Time().DateToday()):
            xp.append(p)
    except:
        print ("Calibration for risk free curve failed")

    if len(xp) != nbr:
        raise Exception("Calibration for risk free curve failed")
    return xp


