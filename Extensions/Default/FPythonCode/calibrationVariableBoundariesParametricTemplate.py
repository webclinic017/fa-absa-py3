import acm
import math

'''Variable boundaries for the parametric (benchmark skew) surface'''

ael_variables = [

['atmvolmin',             'Atm Vol min', 'double', None, 0.0, 1, 0, 'ATM forward volatility minimum value', None, True],
['atmvolmax',             'Atm Vol max', 'double', None, float("inf"), 1, 0, 'ATM forward volatility maximum value', None, True],
['slopemin',              'Slope min', 'double', None, float("-inf"), 1, 0, 'Slope minimum value', None, True],
['slopemax',              'Slope max', 'double', None, float("inf"), 1, 0, 'Slope maximum value', None, True],
['leftcurvaturemin',      'Left Curvature min', 'double', None, float("-inf"), 1, 0, 'Left curvature minimum value', None, True],
['leftcurvaturemax',      'Left Curvature max', 'double',  None, float("inf"), 1, 0, 'Left curvature maximum value', None, True],
['rightcurvaturemin',     'Right Curvature min', 'double', None, float("-inf"), 1, 0, 'Right curvature minimum value', None, True],
['rightcurvaturemax',     'Right Curvature max', 'double', None, float("inf"), 1, 0, 'Right curvature maximum value', None, True],
['leftcutoffmin',         'Left Cut-Off min', 'double', None, None, 0, 0, 'Left cut-off minimum value. If left blank, calculated to minimum log-moneyness of none-filtered benchmarks.', None, True],
['leftcutoffmax',         'Left Cut-Off max', 'double', None, -0.001, 1, 0, 'Left cut-off maximum value', None, True],
['rightcutoffmin',        'Right Cut-Off min', 'double', None, 0.001, 1, 0, 'Right cut-off minimum value', None, True],
['rightcutoffmax',        'Right Cut-Off max', 'double', None, None, 0, 0, 'Right cut-off maximum value. If left blank, calculated to maximum log-moneyness of none filtered benchmarks.', None, True],
['leftwingmin',           'Left Wing min', 'double', None, 0.0, 1, 0, 'Left wing minimum value', None, True],
['leftwingmax',           'Left Wing max', 'double', None, 1.0, 1, 0, 'Left wing maximum value', None, True],
['rightwingmin',          'Right Wing min', 'double', None, 0.0, 1, 0, 'Right wing minimum value', None, True],
['rightwingmax',          'Right Wing max', 'double', None, 1.0, 1, 0, 'Right wing maximum value', None, True],


]

'''Default variable boundaries, parameters in order according to above'''
def ael_main_ex( parameters, dictExtra ):

    #Unpack parameters to variables
    atmvolmin = parameters['atmvolmin']
    atmvolmax = parameters['atmvolmax']
    slopemin = parameters['slopemin']
    slopemax = parameters['slopemax']
    leftcurvaturemin = parameters['leftcurvaturemin']
    leftcurvaturemax = parameters['leftcurvaturemax']
    rightcurvaturemin = parameters['rightcurvaturemin']
    rightcurvaturemax = parameters['rightcurvaturemax']
    leftcutoffmin = parameters['leftcutoffmin']
    leftcutoffmax = parameters['leftcutoffmax']
    rightcutoffmin = parameters['rightcutoffmin']
    rightcutoffmax = parameters['rightcutoffmax']
    leftwingmin = parameters['leftwingmin']
    leftwingmax = parameters['leftwingmax']
    rightwingmin = parameters['rightwingmin']
    rightwingmax = parameters['rightwingmax']

    #Unpack extra provided data for variables boundaries
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    variablesBoundaries = dict.At('variablesBoundaries')
    
    # Calculate boundaries for parameters leftcutoffmin and rightcutoffmax if user has not supplied specific values
    # Use only none filtered calibration row objects
    moneyness = []
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()    
    for calibrationRowObject in calibrationRowObjects:
        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())
        if not calibrationCostFunctionResult.Filtered():
            #Column has inverted definition of log moneyness
            logMoneyness = calibrationRowObject.Calculation("Standard Calculations Option Log Moneyness").Value()
            moneyness.append(-logMoneyness)
    moneyness.sort()
    
    if not leftcutoffmin:
    
        leftcutoffmin = moneyness[0]
        
        if leftcutoffmin > 0.0:
        
            leftcutoffmin = -leftcutoffmin
            
        elif leftcutoffmin == 0.0:
        
            leftcutoffmin = -0.3
        
    if not rightcutoffmax:
    
        rightcutoffmax = moneyness[-1]
        
        if rightcutoffmax < 0.0:
        
            rightcutoffmax = -rightcutoffmax
            
        elif rightcutoffmax == 0.0:
        
            rightcutoffmax = 0.3
            
            
    variablesBoundaries.Add( [atmvolmin, atmvolmax] )
    variablesBoundaries.Add( [slopemin, slopemax] )
    variablesBoundaries.Add( [leftcurvaturemin, leftcurvaturemax] )
    variablesBoundaries.Add( [rightcurvaturemin, rightcurvaturemax] )
    variablesBoundaries.Add( [leftcutoffmin, leftcutoffmax] )    
    variablesBoundaries.Add( [rightcutoffmin, rightcutoffmax] )
    variablesBoundaries.Add( [leftwingmin, leftwingmax] )
    variablesBoundaries.Add( [rightwingmin, rightwingmax] )    
        
    return [variablesBoundaries]
