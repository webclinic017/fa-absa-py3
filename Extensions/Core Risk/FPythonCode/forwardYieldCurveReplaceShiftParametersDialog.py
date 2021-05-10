
import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'yieldCurve,FYieldCurve;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)

    shiftVector = acm.CreateShiftVector('shiftMappingLink', 'forward yield curve link', None)
    
    for i in namedParameters:
        yieldCurve = i.Parameter('yieldCurve')
        shiftVector.AddShiftItem(yieldCurve)            
       
    return shiftVector
