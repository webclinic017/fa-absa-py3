import acm
import FUxUtils

def ShowUI(shell, params):
    parametersDef = 'dateVal,date,Point Date;value,double,Point Shift'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )

def Execute( parameters, shiftType, displayName ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    shiftVector = acm.CreateShiftVector('shiftCurvePoints', 'credit yield curve', None )
    vector = acm.FArray()
    
    for namedParameter in namedParameters:
        date = namedParameter.Parameter('dateVal')
        shift = namedParameter.Parameter('value')
        vector.Add(acm.DenominatedValue(TransformShift(shift, shiftType), None, None, date) )
       
    shiftVector.AddShiftItem( [vector, shiftType, None], displayName )
    return shiftVector

def TransformShift( shift, shiftType ):
    if 'Relative' == shiftType:
        return 1.0 + 0.01 * shift
    if 'Absolute' == shiftType:
        return 0.0001 * shift
    if 'Replace' == shiftType:
        return 0.01 * shift
