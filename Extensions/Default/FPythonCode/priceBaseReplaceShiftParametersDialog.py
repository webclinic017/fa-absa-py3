
import acm
import FUxUtils

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'priceBase, enum(PriceBase), Price Base;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateReplaceShiftVector('price base', None)
    
    for i in namedParameters:
        priceBase = i.Parameter('priceBase')
        shiftVector.AddReplaceShiftItem(priceBase, priceBase)            
       
    return shiftVector
