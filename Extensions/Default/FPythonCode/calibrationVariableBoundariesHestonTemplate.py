import acm
import math

ael_variables = [

['kappamin',      'Kappa min', 'double', None, 0.1, 1, 0, 'Minimum value of Kappa (Speed of Mean Reversion)', None, True],
['kappamax',      'Kappa max', 'double', None, 4.0, 1, 0, 'Maximum value of Kappa (Speed of Mean Reversion)', None, True],
['initialvolsquaredmin', 'Initial Vol Squared min', 'double', None, 0.0025, 1, 0, 'Minimum value of the square of Initial Vol', None, True],
['initialvolsquaredmax', 'Initial Vol Squared max', 'double', None, 2.25, 1, 0, 'Maximum value of the square of Initial Vol', None, True],
['thetasquaredmin',      'Theta Squared min', 'double', None, 0.0025, 1, 0, 'Minumum value of the square of Theta (Long Term Mean Volatility)', None, True],
['thetasquaredmax',      'Theta Squared max', 'double', None, 2.25, 1, 0, 'Maximum value of the square of Theta (Long Term Mean Volatility)', None, True],
['volvolmin',     'Vol Vol min', 'double', None, 0.1, 1, 0, 'Minimum value of Vol Vol', None, True],
['volvolmax',     'Vol Vol max', 'double', None, 2.0, 1, 0, 'Maximum value of Vol Vol', None, True],
['rhomin',        'Rho min', 'double', None, -0.95, 1, 0, 'Minimum value of Rho (Correlation)', None, True],
['rhomax',        'Rho max', 'double', None, 0.95, 1, 0, 'Maximum value of Rho (Correlation)', None, True]

]

'''Heston default variables boundaries, parameters in order: kappa, initialVolSquared, thetaSquared, volvol, rho'''
def ael_main_ex( parameters, dictExtra ):

    #Unpack Heston parameters to variables
    kappamin = parameters['kappamin']
    kappamax = parameters['kappamax']
    initialvolsquaredmin = parameters['initialvolsquaredmin']
    initialvolsquaredmax = parameters['initialvolsquaredmax']
    thetasquaredmin = parameters['thetasquaredmin']
    thetasquaredmax = parameters['thetasquaredmax']
    volvolmin = parameters['volvolmin']
    volvolmax = parameters['volvolmax']
    rhomin = parameters['rhomin']
    rhomax = parameters['rhomax']
    
    #Unpack extra provided data for variables boundaries
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    variablesBoundaries = dict.At('variablesBoundaries')
    
    variablesBoundaries.Add( [kappamin, kappamax] )
    variablesBoundaries.Add( [initialvolsquaredmin, initialvolsquaredmax] )
    variablesBoundaries.Add( [thetasquaredmin, thetasquaredmax] )
    variablesBoundaries.Add( [volvolmin, volvolmax] )
    variablesBoundaries.Add( [rhomin, rhomax] )    
        
    return [variablesBoundaries]
