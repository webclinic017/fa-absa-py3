import acm
import math

ael_variables = [

['lmin', 'l min', 'double', None, 0.0, 1, 0, 'l minimum value', None, True],
['lmax', 'l max', 'double', None, None, 0, 0, 'l maximum value. If left blank, calculated to two divided by the expiry time of the applicable volatility skew.', None, True],
['rmin', 'r min', 'double', None, 0.0, 1, 0, 'r minimum value. ', None, True],
['rmax', 'r max', 'double', None, None, 0, 0, 'r maximum value. If left blank, calculated to two divided by the expiry time of the applicable volatility skew.', None, True],
['amin', 'a min', 'double', None, 0.00, 1, 0, 'a minimum value', None, True],
['amax', 'a max', 'double', None, float("inf"), 1, 0, 'a maximum value', None, True],
['mmin', 'm min', 'double', None, None, 0, 0, 'm minimum value. If left blank, calculated to the minimum log-moneyness of none-filtered benchmarks for the applicable volatility skew.', None, True],
['mmax', 'm max', 'double', None, None, 0, 0, 'm maximum value. If left blank, calculated to the maximum log-moneyness of none-filtered benchmarks for the applicable volatility skew', None, True],
['smin', 's min', 'double', None, 0.01, 1, 0, 's minimum value', None, True],
['smax', 's max', 'double', None, float("inf"), 1, 0, 's maximum value', None, True]

]

'''SVI default variables boundaries, parameters in order: l, r, a, m, s'''
def ael_main_ex( parameters, dictExtra ):

    #Unpack SVI volatility parameters
    lmin = parameters['lmin']
    lmax = parameters['lmax']
    rmin = parameters['rmin']
    rmax = parameters['rmax']
    amin = parameters['amin']
    amax = parameters['amax']
    mmin = parameters['mmin']
    mmax = parameters['mmax']
    smin = parameters['smin']
    smax = parameters['smax']
    
    #Unpack extra provided data for variables boundaries    
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    variablesBoundaries = dict.At('variablesBoundaries')
    
    infinity = float("inf")
    timeToExpiry = calibrationRowObjects.First().Calculation("Time to Expiry").Value() / 365.0

    # Calculate parameter lmax, Only if user not supplied a specific value
    if not lmax:

        lmax = 2.0 / timeToExpiry
        
    # Calculate parameter rmax, Only if user not supplied a specific value
    if not rmax:

        rmax = 2.0 / timeToExpiry

    # Calculate parameter m boundaries, only if user not supplied specific values
    # Parameter m, [minLogMoneyness, maxLogMoneyness]
    # of none filtered calibration row objects
    if not mmin and not mmax:
        moneyness = []
        calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()    
        for calibrationRowObject in calibrationRowObjects:
            calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())
            if not calibrationCostFunctionResult.Filtered():
                #Column has inverted definition of log moneyness
                logMoneyness = calibrationRowObject.Calculation("Standard Calculations Option Log Moneyness").Value()
                moneyness.append(-logMoneyness)
        moneyness.sort()
        mmin = moneyness[0]
        mmax = moneyness[-1]
    variablesBoundaries.Add( [lmin, lmax] )
    variablesBoundaries.Add( [rmin, rmax] )
    variablesBoundaries.Add( [amin, amax] )
    variablesBoundaries.Add( [mmin, mmax] )
    variablesBoundaries.Add( [smin, smax] )
    
    return [variablesBoundaries]
