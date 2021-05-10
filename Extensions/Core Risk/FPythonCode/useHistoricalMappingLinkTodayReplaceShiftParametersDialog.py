
import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'useHistoricalMappingLinkToday, FBoolean, Use Historical Mapping Link Today;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateReplaceShiftVector('Use Historical Mapping Link Today', None)
    
    for i in namedParameters:
        useHistoricalMappingLinkToday = i.Parameter('useHistoricalMappingLinkToday')
        shiftVector.AddReplaceShiftItem(useHistoricalMappingLinkToday, useHistoricalMappingLinkToday)
       
    return shiftVector
