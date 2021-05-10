""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBSAExport.py"
import FRTBCommon
import FRTBExport

ael_variables = FRTBExport.getDistributeCalculation()
exporters = FRTBCommon.getExporters(group_name='sa')
ael_variables.extend(FRTBExport.getRiskFactorAelVariables(
    risk_classes='enum(cl_FRTB_SA_Risk_Class)')
)

ael_variables.extend(FRTBExport.getPositionAelVariables())
ael_variables = FRTBExport.createAelVariables(
    ael_vars_list=ael_variables, exporters=exporters,
    log_filename='frtb_sa_export.log'
)

def ael_main(parameters):
    return FRTBCommon.aelMain(parameters, exporters)
