import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'includeSimulatedTrades, FBoolean, Include Simulated Trades;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateReplaceShiftVector('Include Simulated Trades', None)
    
    for i in namedParameters:
        includeSimulatedTrades = i.Parameter('includeSimulatedTrades')
        shiftVector.AddReplaceShiftItem(includeSimulatedTrades, i.Name())
       
    return shiftVector
