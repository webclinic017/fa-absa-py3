'''
===================================================================================================
PURPOSE: A single module to contain all classes used in the Hedge Effectiveness Testing Package
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import acm
import FLogger

import HedgeConstants

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


class TestResultBase(object):
    """A Class containing the basic parameters of a test result
    """
    def __init__(self, name, perspective):
        self.name = name
        self.perspective = perspective
        self.value = 0.0
        self.result = HedgeConstants.STR_NO_RESULT
        self.date = acm.Time().DateNow()
        self.dealPackage = None
        self.pointsX = []
        self.pointsY = []

    def storeResults(self):

        if not self.dealPackage:
            logger.WLOG('The results cannot be saved as no deal package has been assigned to the '
                        'test results')

        str_chlValue = testResult.perspective + '_' + testResult.name + '_Value'
        str_chlResult = testResult.perspective + '_' + testResult.name + '_Result'

        saveTimeSeriesValue(testResult.dealPackage, str_chlValue, testResult.value)
        saveTimeSeriesValue(testResult.dealPackage, str_chlResult, testResult.result)

        i = 1
        old_len = 0
        padding = len(str(len(testResult.pointsX)))
        str_chlStart = 'Prospective_Point X_'
        for point in testResult.pointsX:
            if len(str(i)) > old_len:
                zero_padding = '0'*(padding-len(str(i)))
                old_len = len(str(i))
            str_chlPoint = str_chlStart+zero_padding+str(i)
            saveTimeSeriesValue(testResult.dealPackage, str_chlPoint, point)
            i += 1

        i = 1
        old_len = 0
        padding = len(str(len(testResult.pointsY)))
        str_chlStart = 'Prospective_Point Y_'
        for point in testResult.pointsY:
            if len(str(i)) > old_len:
                zero_padding = '0'*(padding-len(str(i)))
                old_len = len(str(i))
            str_chlPoint = str_chlStart+zero_padding+str(i)
            saveTimeSeriesValue(testResult.dealPackage, str_chlPoint, point)
            i += 1


class TestResultRegression(TestResultBase):
    """A Class which inherits from 'TestResultBase' and has extra
        parameters relevant to the Linear Regression test
    """
    def __init__(self):
        TestResultBase.__init__(self, HedgeConstants.STR_REGRESSION, HedgeConstants.STR_PROSPECTIVE)
        self.alpha = 0.0
        self.beta = 0.0
        self.p_value = 0.0
        self.correlation = 0.0
        self.f_statistic = 0.0

    def storeResults(self):

        if not self.dealPackage:
            logger.WLOG('The results cannot be saved as no deal package has been assigned to the '
                        'test results')

        str_chlAlpha = testResult.perspective + '_' + testResult.name + '_alpha'
        str_chlBeta = testResult.perspective + '_' + testResult.name + '_beta'
        str_chlPVal = testResult.perspective + '_' + testResult.name + '_p-value'
        str_chlCorr = testResult.perspective + '_' + testResult.name + '_correlation'
        str_chlFStat = testResult.perspective + '_' + testResult.name + '_Fstatistic'

        saveTimeSeriesValue(testResult.dealPackage, str_chlAlpha, testResult.alpha)
        saveTimeSeriesValue(testResult.dealPackage, str_chlBeta, testResult.beta)
        saveTimeSeriesValue(testResult.dealPackage, str_chlPVal, testResult.p_value)
        saveTimeSeriesValue(testResult.dealPackage, str_chlCorr, testResult.correlation)
        saveTimeSeriesValue(testResult.dealPackage, str_chlFStat, testResult.f_statistic)

        super(TestResultRegression, self).storeResults()
