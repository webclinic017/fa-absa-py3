""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportPLExplainTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = '_Profit and loss Explain'

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])

class FMarketRiskExportPLExplainTab(FRunScriptGUI.AelVariablesHandler):

    @staticmethod
    def getYieldCurves():
        return sorted([s.Name() for s in acm.FYieldCurve.Select("")])
    @staticmethod
    def getTimeBuckets():
        return sorted([s.Name() for s in acm.FStoredTimeBuckets.Select("")])
        
    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues

    def __init__(self):
        ttFileName = ('Output file name')
        ttTimeBuckets = ('If specified, the timebucket will be used in the '
			' interest rate/benchmark risk factors.')
        ttRiskFactors = ('Selected the sensitivities risk factors to be exported.')
        ttYieldCurves = ('Name of the additional yield curves specified for the '
                         'Interest rate / Benchmark risk factors.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runPLExplainReport',
                    'Run reports{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'PL Explain Report', self._enable, True],
                ["plExplainOutputFile",
                        ttFileName + tab_name,
                        "string", None, 'Sens',
                        0, False, ttFileName, None, False],
                ["riskFactors",
                        "Risk Factors" + tab_name,
                        "string", ["Benchmark", "CommodityPrice", "Credit", "EquityPrice", "FXRate", "Inflation", "InstrumentSpread", "InterestRate", "Volatility"], 'InterestRate',
                        True, True, ttRiskFactors, None, False],
                ["yieldCurve_PLExplain",
                        "Yield Curves" + tab_name,
                        "string", 
                        FMarketRiskExportPLExplainTab.getYieldCurves(),
                        '', False, True,
                        ttYieldCurves,
                        None, False],
                ["timebucket_name_PLExplain",
                        "Time buckets" + tab_name,
                        "string", FMarketRiskExportPLExplainTab.getTimeBuckets(),
                        '', False, False,
                        ttTimeBuckets,
                        None, False],
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)

def getAelVariables():
    outtab = FMarketRiskExportPLExplainTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
