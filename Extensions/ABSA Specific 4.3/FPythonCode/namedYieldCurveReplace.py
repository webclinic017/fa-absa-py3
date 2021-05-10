import acm
import FUxUtils

def shiftNamedYieldCurve(mappingLink, curve, filterCurve):
    if mappingLink.Link().YieldCurveComponent().Name() == filterCurve.Name():
        shiftMappingLink = acm.GetFunction("shiftMappingLink", 2)
        return shiftMappingLink(mappingLink, curve)
    return mappingLink

def ael_custom_dialog_show( shell, params ):
    parametersDef = 'yieldCurve,FYieldCurve,Yield Curve;filterCurve,FYieldCurve,Filter Curve;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )

def ael_custom_dialog_main( parameters, dictExtra ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateShiftVector('shiftNamedYieldCurve', 'yield curve mapped parameter', None)
    for i in namedParameters:
    yieldCurve = i.Parameter('yieldCurve')
    filterCurve = i.Parameter('filterCurve')
    shiftVector.AddShiftItem([yieldCurve, filterCurve])
    return shiftVector
