""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FArtiQMarketRiskExportVaRTab.py"
"""----------------------------------------------------------------------------
MODULE
    FMarketRiskExportVaRTab - VaR settings tab

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    that set up VaR calculations.

----------------------------------------------------------------------------"""


import acm

import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection
import FMarketRiskExportColumnSelection

tab_name = "_Value at Risk"

class MarketRiskExportVaRTab(MarketRiskExportColumnSelection):
    
    
    def __init__(self):

        ttVarType = ('Freely defined mandatory text describing the VaR type. '
                'For instance \'Historical\'.')
        ttVaRHistory = ("Comma-separated list of historical periods to "
                "consider in each VaR calculation e.g. '10y,9y,8y'")
        ttBatchSize = ("The number of position rows to write to file before clearing "
                "results, to reduce memory usage during processing.")
        ttMaxPositionCalculationTime = ('Maximum time in seconds to calculate '
                'position value per risk factor.')
        ttStressScenarioFile = ('The name or path to an external scenario '
                'file. If no path is given, the path fallbacks to the '
                'FCS_RISK_DIR environment variable first and then the current '
                'working directory. ')
        ttCreateMarketValue = "Calculate market value and feed into report?"
        ttVaRFileName = ('Name of the file containing the VaR '
                'results.')
        ttScenarioCountFileName = ('Name of the file containing the scenario '
                'count results. if not specified, the file name will be '
                'scenario_count')
        ttScenarioDatesFileName = ('Name of the file containing the scenario '
                'dates. if not specified, the file name will be '
                'scenario_dates')
        ttDecayFactor = ('The value of the decay factor to use for '
                'VaR calculations. If not specified, no decay factor '
                'will be used.')
        ttDecayFactorFileName = ('Name of the file containing the decay '
                'factor value. if not specified, the file name will be '
                'decay_factor')
        ttScenarios = ('The stored scenario applied for calculation.')

        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runVaRReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False, 'Run VaR report',
                    self._enable, True],
                ["var_Scenarios",
                        ("Var stored scenarios"
                            + tab_name),
                        "string",
                        FMarketRiskExportColumnSelection.getStoredScenarios(), "",
                        0, True, ttScenarios, None, False],
                ["var_type",
                        "VaR type" + tab_name,
                        "string", None, "",
                        0, 0, ttVarType, None, False],
                ["vaRHistory",
                        "VaR history" + tab_name,
                        "string", None, "",
                        0, 0, ttVaRHistory, None, False],
                ["batchSize",
                        "Batch size" + tab_name,
                        "int", None, 200,
                        0, 0, ttBatchSize, None, False],
                ["maxCalcTime",
                        "Maximum position calculation time" + tab_name,
                        "float", None, 10,
                        0, 0, ttMaxPositionCalculationTime, None, False],
                ["decay_factor",
                        "Decay factor" + tab_name,
                        "string", None, "",
                        0, 0, ttDecayFactor, None, False],
                ['VaR File Name',
                        'VaR file name' + tab_name,
                        'string', None, 'VaR',
                        0, 0, ttVaRFileName, None, False],
                ['scenario_count_file_name',
                        'Scenario count file name' + tab_name,
                        'string', None, 'scenario_count.csv',
                        0, 0, ttScenarioCountFileName, None, False],
                ['scenario_dates_file_name',
                        'Scenario dates file name' + tab_name,
                        'string', None, 'scenario_dates.csv',
                        0, 0, ttScenarioDatesFileName, None, False],
                ['decay_factor_file_name',
                        'Decay factor file name' + tab_name,
                        'string', None, 'decay_factor.txt',
                        0, 0, ttDecayFactorFileName, None, False]

        ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Theoretical Value')

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():

    outtab = MarketRiskExportVaRTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
