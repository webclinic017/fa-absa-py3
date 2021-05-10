
import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'useMarkToMarketPriceToday, EnumMtMTodayChoice, Use Mark to Market Price Today;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateReplaceShiftVector('Use Mark to Market Price Today', None)
    
    for i in namedParameters:
        useMarkToMarketPriceToday = i.Parameter('useMarkToMarketPriceToday')
        enumValue = acm.FEnumeration['EnumMtMTodayChoice'].Enumeration(useMarkToMarketPriceToday)

        shiftVector.AddReplaceShiftItem(enumValue, useMarkToMarketPriceToday)
       
    return shiftVector
