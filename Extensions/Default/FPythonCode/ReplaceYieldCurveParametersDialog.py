
import acm
import FUxUtils
import ReplaceYieldCurveGUICore

def ael_custom_dialog_show(shell, params):
    return ReplaceYieldCurveGUICore.ShowUI(shell, params )
    
def ael_custom_dialog_main( parameters, dictExtra ):
    return ReplaceYieldCurveGUICore.Execute(parameters)
