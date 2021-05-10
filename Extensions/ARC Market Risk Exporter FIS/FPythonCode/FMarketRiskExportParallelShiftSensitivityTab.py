""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportParallelShiftSensitivityTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = '_Parallel Shift Sensitivity'

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])


class FMarketRiskExportParallelShiftSensitivityTab(MarketRiskExportColumnSelection):
    yieldCurves = []
    storedScenarios = []

    ttYieldCurves = ('Names of yield curves to be shifted. The selected '
            'curves will be applied to all sensitivity calculations '
            'available on this tab. Specify "All" to calculate the '
            'sensitivities to shifts in all yield curves at the same time.')
    ttParallelShiftFile = ('Output file name for sensitivity calculation to '
            'parallel shifts of entire curves.')
    ttStressNameParallel = ('Specify stress name for parallel shift.')
    ttMeasurement =("The measure of the calculation.")
     
    @staticmethod
    def getYieldCurves():
        return sorted([s.Name() for s in acm.FYieldCurve.Select("")])

    @staticmethod
    def getStoredScenarios():
        return sorted([s.Name() for s in acm.FStoredScenario.Select("")])

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues

    def __init__(self):
        variables = [
                AELVariable('runParallelShiftReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0,
                    True, False, 'Run Parallel shift sensitivity report',
                    self._enable, True),
                AELVariable("stress_name_parallel",
                    'Stress name for parallel shift{0}'.format(
                        tab_name),
                    'string', None, 'Parallel Shift',
                    0, False,
                    FMarketRiskExportParallelShiftSensitivityTab.ttStressNameParallel,
                    None, False),
                AELVariable('yield_curves_parallel', 'Yield curves{0}'.format(
                    tab_name),
                    'string',
                    FMarketRiskExportParallelShiftSensitivityTab.getYieldCurves(),
                    '', 0, True,
                    FMarketRiskExportParallelShiftSensitivityTab.ttYieldCurves,
                    None, False),
                AELVariable("parallel_shift_file",
                    'Parallel shift delta output file{0}'.format(
                    tab_name),
                    'string', None, 'IRDeltaParallel',
                    False, False,
                    FMarketRiskExportParallelShiftSensitivityTab.ttParallelShiftFile,
                    None, False),
                AELVariable("measurement_parallel_shift",
                        'Measure{0}'.format(
                            tab_name),
                        'string', ['Delta', 'Gamma', 'Vega'], 'Delta',
                        0, False,
                        FMarketRiskExportParallelShiftSensitivityTab.ttMeasurement,
                        None, False),
                ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Delta Yield')


def getAelVariables():
    outtab = FMarketRiskExportParallelShiftSensitivityTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
