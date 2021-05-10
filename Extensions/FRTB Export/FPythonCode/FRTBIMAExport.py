""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBIMAExport.py"
import FRTBIMAHierarchy

import FRTBCommon
import FRTBExport

ael_variables = FRTBExport.getDistributeCalculation()
exporters = FRTBCommon.getExporters(group_name='ima')
ael_variables.extend(FRTBExport.getRiskFactorAelVariables(
    # In the future, use the commented out line
    #risk_classes='enum(cl_FRTB_IMA_Risk_Class)'
    risk_classes=FRTBIMAHierarchy.RiskClassNames()))

ael_variables.extend([
    #[VariableName,
    #    DisplayName,
    #    Type, CandidateValues, Default,
    #    Mandatory, Multiple, Description, InputHook, Enabled]
    ['liquidityHorizons',
        'Liquidity horizons',
        'int', [10, 20, 40, 60, 120], None,
        0, 1, (
            'Specify the liquidity horizons that should be reported. '
            'If none specified, the liquidity horizons will be taken '
            'from the hierarchy.'
        )
    ],
    ['scenarioCalendar',
        'Scenario calendar',
        'FCalendar', None, FRTBCommon.ACCOUNTING_CURRENCY_CALENDAR,
        1, 0, 'Calendar used to generate scenario file(s).'
    ],
])
ael_variables.extend(FRTBExport.getPositionAelVariables())
ael_variables = FRTBExport.createAelVariables(
    ael_vars_list=ael_variables, exporters=exporters,
    log_filename='frtb_ima_export.log'
)

def ael_main(parameters):
    return FRTBCommon.aelMain(parameters, exporters)
