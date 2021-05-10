""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportTwistSensitivityTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = '_Twist Sensitivity'

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])


class FMarketRiskExportTwistSensitivityTab(MarketRiskExportColumnSelection):
    yieldCurves = []
    timeBuckets = []
    storedScenarios = []

    ttYieldCurves = ('Names of yield curves to be shifted. The selected '
            'curves will be applied to all sensitivity calculations '
            'available on this tab. Specify "All" to calculate the '
            'sensitivities to shifts in all yield curves at the same time.')
    ttTwistScenarios = ('Names of the stored steepener/flattener scenarios '
            'defining yield curve twists.')
    ttTwistFile = ('Output file name for interest rate delta to yield curve '
            'twist scenarios.')
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
                AELVariable('runTwistReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0,
                    True, False, 'Run Sensitivity twist report',
                    self._enable, True),
                AELVariable('yield_curves_twist', 'Yield curves{0}'.format(
                    tab_name),
                    'string',
                    FMarketRiskExportTwistSensitivityTab.getYieldCurves(),
                    '', 0, True,
                    FMarketRiskExportTwistSensitivityTab.ttYieldCurves,
                    None, False),
                AELVariable('twist_scenarios', 'Twist scenarios{0}'.format(
                    tab_name),
                    'string',
                    FMarketRiskExportTwistSensitivityTab.getStoredScenarios(),
                    '', 0, True,
                    FMarketRiskExportTwistSensitivityTab.ttTwistScenarios,
                    None, False),
                AELVariable("curve_twist_file",
                        'Twist scenarios sensitivity output file{0}'.format(
                            tab_name),
                        'string', None, 'IRDeltaTwists',
                        False, False,
                        FMarketRiskExportTwistSensitivityTab.ttTwistFile,
                        None, False),
                AELVariable("measurement_twist",
                        'Measure{0}'.format(
                            tab_name),
                        'string', ['Delta', 'Gamma', 'Vega'], 'Delta',
                        0, False,
                        FMarketRiskExportTwistSensitivityTab.ttMeasurement,
                        None, False),
                ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Delta Yield')


def getAelVariables():
    outtab = FMarketRiskExportTwistSensitivityTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
