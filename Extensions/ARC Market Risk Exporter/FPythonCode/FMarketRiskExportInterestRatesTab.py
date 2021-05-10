""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportInterestRatesTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = '_Delta'

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])


class MarketRiskExportInterestRatesTab(MarketRiskExportColumnSelection):
    yieldCurves = []
    timeBuckets = []
    storedScenarios = []

    ttYieldCurves = ('Names of yield curves to be shifted. The selected '
            'curves will be applied to all sensitivity calculations '
            'available on this tab. Specify "All" to calculate the '
            'sensitivities to shifts in all yield curves at the same time.')
    ttTimeBuckets = ('Define the grid into which the yield curve will be '
            'split up for independent shifts of each time bucket.')
    ttTwistScenarios = ('Names of the stored steepener/flattener scenarios '
            'defining yield curve twists.')
    ttParallelShiftFile = ('Output file name for interest rate delta to '
            'parallel shifts of entire curves.')
    ttBucketShiftFile = ('Output file name for interest rate delta to '
            'shifts of individual time buckets.')
    ttTwistFile = ('Output file name for interest rate delta to yield curve '
            'twist scenarios.')
    ttStressNameParallel = ('Specify stress name for parallel shift.')
    ttStressNameTimeBucket = ('Specify stress name for interest rate delta to '
                            'shifts of individual time buckets.')

    @staticmethod
    def getYieldCurves():
        return sorted([s.Name() for s in acm.FYieldCurve.Select("")])

    @staticmethod
    def getTimeBuckets():
        return sorted([s.Name() for s in acm.FStoredTimeBuckets.Select("")])

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
                AELVariable('runIRReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0,
                    True, False, 'Run interest rate delta report',
                    self._enable, True),
                AELVariable("stress_name_parallel",
                    'Stress name for parallel shift{0}'.format(
                        tab_name),
                    'string', None, 'Parallel Shift',
                    False, False,
                    MarketRiskExportInterestRatesTab.ttStressNameParallel,
                    None, False),
                AELVariable("stress_name_timebucket",
                    'Stress name for time bucket shift{0}'.format(
                        tab_name),
                    'string', None, 'Time Bucket Shift',
                    False, False,
                    MarketRiskExportInterestRatesTab.ttStressNameTimeBucket,
                    None, False),
                AELVariable('yield_curves', 'Yield curves{0}'.format(
                    tab_name),
                    'string',
                    MarketRiskExportInterestRatesTab.getYieldCurves(),
                    '', False, True,
                    MarketRiskExportInterestRatesTab.ttYieldCurves,
                    None, False),
                AELVariable('time_buckets', 'Time buckets{0}'.format(
                    tab_name),
                    'string',
                    MarketRiskExportInterestRatesTab.getTimeBuckets(),
                    '', False, True,
                    MarketRiskExportInterestRatesTab.ttTimeBuckets,
                    None, False),
                AELVariable('twist_scenarios', 'Twist scenarios{0}'.format(
                    tab_name),
                    'string',
                    MarketRiskExportInterestRatesTab.getStoredScenarios(),
                    '', False, True,
                    MarketRiskExportInterestRatesTab.ttTwistScenarios,
                    None, False),
                AELVariable("parallel_shift_file",
                        'Parallel shift delta output file{0}'.format(
                            tab_name),
                        'string', None, 'IRDeltaParallel',
                        False, False,
                        MarketRiskExportInterestRatesTab.ttParallelShiftFile,
                        None, False),
                AELVariable("bucket_shift_file",
                        'Bucket shift delta output file{0}'.format(
                            tab_name),
                        'string', None, 'IRDeltaBuckets',
                        False, False,
                        MarketRiskExportInterestRatesTab.ttBucketShiftFile,
                        None, False),
                AELVariable("curve_twist_file",
                        'Twist scenarios delta output file{0}'.format(
                            tab_name),
                        'string', None, 'IRDeltaTwists',
                        False, False,
                        MarketRiskExportInterestRatesTab.ttTwistFile,
                        None, False),
                ]
        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Delta Yield')


def getAelVariables():
    outtab = MarketRiskExportInterestRatesTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
