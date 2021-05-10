import acm
import FUxUtils
import YieldCurveShiftParCDSRatePointsGUICore

def ael_custom_dialog_show(shell, params):
    return YieldCurveShiftParCDSRatePointsGUICore.ShowUI(shell, params )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    return YieldCurveShiftParCDSRatePointsGUICore.Execute(parameters, 'Replace', 'Shift Par CDS Points Replace' )
