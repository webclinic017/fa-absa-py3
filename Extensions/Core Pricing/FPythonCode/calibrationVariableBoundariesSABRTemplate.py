import acm
import math

ael_variables = [

['volvolmin', 'Vol Vol min', 'double', None, 0.001, 1, 0, '', None, True],
['volvolmax', 'Vol Vol max', 'double', None, float("inf"), 1, 0, '', None, True],
['alphamin',  'Alpha min', 'double', None, 0.001, 1, 0, '', None, True],
['alphamax',  'Alpha max', 'double', None, float("inf"), 1, 0, '', None, True],
['minrho',    'Rho min', 'double', None, -0.999, 1, 0, '', None, True],
['maxrho',    'Rho max', 'double', None, 0.999, 1, 0, '', None, True]

]

'''SABR default variables boundaries, parameters in order: volvol, rho, alpha'''
def ael_main_ex( parameters, dictExtra ):

    #Unpack SABR volatility parameters
    volvolmin = parameters['volvolmin']
    volvolmax = parameters['volvolmax']
    minrho = parameters['minrho']
    maxrho = parameters['maxrho']
    alphamin = parameters['alphamin']
    alphamax = parameters['alphamax']

    #Unpack extra provided data for variables boundaries    
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    variablesBoundaries = dict.At('variablesBoundaries')
    
    variablesBoundaries.Add( [volvolmin, volvolmax] )
    variablesBoundaries.Add( [minrho, maxrho] )
    variablesBoundaries.Add( [alphamin, alphamax] )
        
    return [variablesBoundaries]
