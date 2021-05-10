import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'includeReservedTrades, FBoolean, Include Reserved Trades;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateReplaceShiftVector('Include Reserved Trades', None)
    
    for i in namedParameters:
        includeReservedTrades = i.Parameter('includeReservedTrades')
        shiftVector.AddReplaceShiftItem(includeReservedTrades, i.Name())
       
    return shiftVector
