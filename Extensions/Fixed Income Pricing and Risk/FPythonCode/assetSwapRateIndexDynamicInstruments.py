
import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'rateindex,FRateIndex,Rate Index;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)

    rateIndices = []
    for i in namedParameters:
        rateIndex = i.Parameter('rateindex')
        rateIndices.append(rateIndex)            
       
    return rateIndices
