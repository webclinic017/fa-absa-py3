""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportCreditTab.py"
import acm
import FRunScriptGUI


tab_name = "_Credit "


class MarketRiskExportCreditTab(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        dayCounts = acm.FEnumeration["enum(DaycountMethod)"].Values()
        rateTypes = acm.FEnumeration["enum(IrCalcType)"].Values()
        frequencies = acm.FEnumeration["enum(IrRateType)"].Values()

        ttDayCount = 'Day count convention'
        ttRateType = 'Credit rate type'
        ttFrequency = 'Compounding frequency'
        ttFileName = 'Output file name'

        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runCreditReport',
                    'Run reports{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'Run Credit Delta Report', self._enable, True],
                ["creditOutputFile",
                        ttFileName + tab_name,
                        "string", None, 'CreditDelta',
                        0, False, ttFileName, None, False],
                ["creditDayCount",
                        ttDayCount + tab_name,
                        "enum(DaycountMethod)", dayCounts, None,
                        True, False, ttDayCount, None, False],
                ["creditRateType",
                        "Rate type" + tab_name,
                        "enum(IrCalcType)", rateTypes, None,
                        True, False, ttRateType, None, False],
                ["creditFrequency",
                        ttFrequency + tab_name,
                        "enum(IrRateType)", frequencies, None,
                        True, False, ttFrequency, None, False],
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():
    outtab = MarketRiskExportCreditTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
