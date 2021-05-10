""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportBucketShiftSensitivityTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = '_Bucket Shift Sensitivity'

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])


class FMarketRiskExportBucketShiftSensitivityTab(MarketRiskExportColumnSelection):
    yieldCurves = []
    timeBuckets = []
    storedScenarios = []

    ttYieldCurves = ('Names of yield curves to be shifted. The selected '
            'curves will be applied to all sensitivity calculations '
            'available on this tab. Specify "All" to calculate the '
            'sensitivities to shifts in all yield curves at the same time.')
    ttTimeBuckets = ('Define the grid into which the yield curve will be '
            'split up for independent shifts of each time bucket.')
    ttBucketShiftFile = ('Output file name for sensitivitity calculations to '
                            'shifts of individual time buckets.')
    ttStressNameTimeBucket = ('Specify stress name for Sensitivity to '
                            'shifts of individual time buckets.')
    ttMeasurement =("The measure of the calculation.")

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
        variables = [
                AELVariable('runBucketShiftReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0,
                    True, False, 'Run interest rate delta report',
                    self._enable, True),
                AELVariable("stress_name_timebucket",
                    'Stress name for time bucket shift{0}'.format(
                        tab_name),
                    'string', None, 'Time Bucket Shift',
                    False, False,
                    FMarketRiskExportBucketShiftSensitivityTab.ttStressNameTimeBucket,
                    None, False),
                AELVariable('yield_curves_timebucket', 'Yield curves{0}'.format(
                    tab_name),
                    'string',
                    FMarketRiskExportBucketShiftSensitivityTab.getYieldCurves(),
                    '', 0, True,
                    FMarketRiskExportBucketShiftSensitivityTab.ttYieldCurves,
                    None, False),
                AELVariable('time_buckets', 'Time buckets{0}'.format(
                    tab_name),
                    'string',
                    FMarketRiskExportBucketShiftSensitivityTab.getTimeBuckets(),
                    '', 0, True,
                    FMarketRiskExportBucketShiftSensitivityTab.ttTimeBuckets,
                    None, False),
                AELVariable("bucket_shift_file",
                        'Bucket shift delta output file{0}'.format(
                            tab_name),
                        'string', None, 'IRDeltaBuckets',
                        False, False,
                        FMarketRiskExportBucketShiftSensitivityTab.ttBucketShiftFile,
                        None, False),
                AELVariable("measurement_timebucket",
                        'Measure{0}'.format(
                            tab_name),
                        'string', ['Delta', 'Gamma', 'Vega'], 'Delta',
                        0, False,
                        FMarketRiskExportBucketShiftSensitivityTab.ttMeasurement,
                        None, False),
                ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Interest Rate Yield Delta Bucket')


def getAelVariables():
    outtab = FMarketRiskExportBucketShiftSensitivityTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
