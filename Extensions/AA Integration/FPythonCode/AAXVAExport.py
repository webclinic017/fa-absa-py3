""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVAExport.py"
import AAXVAUtility
import importlib
importlib.reload(AAXVAUtility)
AAXVAUtility.reloadModules()
import AAXVAAAJCreator
import AAXVAGuiCommon

exports = AAXVAAAJCreator.getExports()
ael_variables = AAXVAGuiCommon.getAelVariables(
    name=__name__, exports=exports, log_filename='aa_xva_export.log'
)

def ael_main(parameters):
    rv = AAXVAGuiCommon.aelMain(
        name=__name__, exports=exports, parameters=parameters
    )
    return rv
