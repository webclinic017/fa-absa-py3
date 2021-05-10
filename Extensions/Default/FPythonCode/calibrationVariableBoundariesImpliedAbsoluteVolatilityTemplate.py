import acm
import math

ael_variables = [

['impliedvolatilitymin', 'Implied Volatility min', 'double', None, 0.0, 1, 0, '', None, True],
['impliedvolatilitymax', 'Implied Volatility max', 'double', None, 10.0, 1, 0, '', None, True],

]

''' Implied volatility, parameters in order: impliedvolatility '''
def ael_main_ex( parameters, dictExtra ):

    #Unpack Implied volatility parameters
    impliedvolatilitymin = parameters['impliedvolatilitymin']
    impliedvolatilitymax = parameters['impliedvolatilitymax']
    
    #Unpack extra provided data for variables boundaries
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    variablesBoundaries = dict.At('variablesBoundaries')
    
    variablesBoundaries.Add( [impliedvolatilitymin, impliedvolatilitymax] )
    
    return [variablesBoundaries]
