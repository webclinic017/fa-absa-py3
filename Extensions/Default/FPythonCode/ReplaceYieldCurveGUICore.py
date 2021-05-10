import acm
import FUxUtils

def ShowUI(shell, params):
    parametersDef = 'yieldCurveToReplace, FBenchmarkCurve, Yield Curve to Replace;yieldCurveReplaceWith, FBenchmarkCurve, Replacing Yield Curve;'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )
    

def Execute( parameters):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)

    for namedParameter in namedParameters:
        ycToReplace = namedParameter.Parameter('yieldCurveToReplace')
        ycReplaceWith = namedParameter.Parameter('yieldCurveReplaceWith')	
        ycName = ycToReplace.Name()
   
    ycToReplaceFilter = acm.Filter.SimpleAndQuery(acm.FYieldCurve, ['Name'], None, [ycName]) 
    shiftVector = acm.CreateReplaceShiftVector('benchmark curve', ycToReplaceFilter)
    shiftVector.AddReplaceShiftItem([ycReplaceWith])
    return shiftVector
