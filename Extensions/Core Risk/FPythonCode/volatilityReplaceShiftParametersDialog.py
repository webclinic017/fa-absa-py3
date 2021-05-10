
import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'volatility,FVolatilityStructure;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
            
    shiftVector = acm.CreateShiftVector('shiftMappingLink', 'volatility mapped parameter', None)

    for i in namedParameters:
        volatility = i.Parameter('volatility');
        shiftVector.AddShiftItem(volatility)
    
    return shiftVector
