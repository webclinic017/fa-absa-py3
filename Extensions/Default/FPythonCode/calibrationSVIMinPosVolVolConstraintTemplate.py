import acm
import math

ael_variables = [

['sviminvol', 'Minimum Volatility Value in %', 'double', None, 0.0, 1, 0, 'Minimum allowed SVI volatility value for volatility', None, True]

]

def Value(dict):

    #Unpack Constraint parameters       
    parameters = dict.At(acm.FSymbol('parameters'))
    sviminvol = parameters['sviminvol'] / 100.0
    
    variables = dict.At(acm.FSymbol("variables"))
    jacobianRow = dict.At(acm.FSymbol("jacobianRow"))
    jacobianDesired = dict.At(acm.FSymbol("jacobianDesired"))
    
    # unpack variables, to svi-parameters
    l = variables[0]
    r = variables[1]
    a = variables[2]
    m = variables[3]
    s = variables[4]
    
    # Constraint Value
    jacobianRow[0] = 0.0
    jacobianRow[1] = 0.0
    jacobianRow[2] = 0.0
    jacobianRow[3] = 0.0
    jacobianRow[4] = 0.0  

    constraintValue = a + s*math.sqrt(r*l)
    constraintLowValue = sviminvol * sviminvol
    
    if a < 0.0 and l > 0.0 and r > 0.0:
    
        if jacobianDesired:
        
            jacobianRow[0] = s*s*r
            jacobianRow[1] = s*s*l
            jacobianRow[2] = -2.0*a
            jacobianRow[4] = 2*s*l*r
            
    elif a < 0.0 and l <= 0.0 and r <= 0.0:
                
        constraintValue = a*a
                
        if jacobianDesired:
        
            jacobianRow[2] = 2.0*a
              
    if jacobianDesired:
    
        dict.AtPut(acm.FSymbol("jacobianCalculated"), True)   
    
    # Put back Result
    constraintedBreached = constraintValue < constraintLowValue;
    
    dict.AtPut(acm.FSymbol("constraintBreached"), constraintedBreached)
    
    return 0.0

def ael_main_ex( parameters, dictExtra ):       

    # Unpack InputData
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()   
    calibrationConstraintsFunctions = dict.At('calibrationConstraintsFunctions')
    
    calibrationConstraintsFunctions.Add([Value, parameters])
    
    return  calibrationConstraintsFunctions;

'''Register SVI-Consraints'''
def RegisterConstraintsFunctions(constraintsFunctions):

    constraintsFunctions.Add(acm.FSymbol("VolVol_Square_Positive"))
    
