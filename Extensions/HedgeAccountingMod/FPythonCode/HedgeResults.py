'''
===================================================================================================
PURPOSE: This class handles the results of the effectiveness tests. It can read the results from
            the database, or receive a dictionary and convert the data within into the class
            structure. Finally, the class can persist the data to the database.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import math
import datetime
import types

import acm
import FLogger

import HedgeConstants
import HedgeUtils

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


class ResultsBase(object):
    def __init__(self):
        self.result = None
        self.result_id = None                   # Choice list ID


class OverallResult(ResultsBase):
    def __init__(self):
        super(OverallResult, self).__init__()


class CriticalTerms(ResultsBase):
    def __init__(self):
        super(CriticalTerms, self).__init__()


class ValuesBase(ResultsBase):
    def __init__(self):
        self.values = None
        self.data = None
        self.last_value = None
        self.last_value_id = None                # Choice list ID
        super(ValuesBase, self).__init__()


class DollarOffset(ValuesBase):
    def __init__(self):
        super(DollarOffset, self).__init__()


class VariableReduction(ValuesBase):
    def __init__(self):
        super(VariableReduction, self).__init__()


class Regression(ResultsBase):
    def __init__(self):
        super(Regression, self).__init__()
        self.alpha = None
        self.alpha_id = None                    # Choice list ID
        self.beta = None
        self.beta_id = None                     # Choice list ID
        self.correlation = None
        self.correlation_id = None              # Choice list ID
        self.r2 = None
        self.r2_id = None                       # Choice list ID
        self.pValue = None                      # F Statistic
        self.pValue_id = None                   # Choice list ID


class HedgeResults():
    def __init__(self, deal_package_oid):
        self.deal_package_oid = deal_package_oid
        self.pro_dollar_offset = None
        self.ret_dollar_offset = None
        self.regression = None
        self.critical_terms = None
        self.pro_variable_reduction = None
        self.ret_variable_reduction = None
        self.overall_results = None

    def create_result_dict(self):
        ''' Converts result class to result dict
        '''
        self.results = {}

        if self.pro_dollar_offset:
            tmp_result = results['Pro Dollar Offset']
            self.pro_dollar_offset = self.populate_dollar_offset(tmp_result, True)
        if 'Retro Dollar Offset' in results.keys():
            tmp_result = results['Retro Dollar Offset']
            self.ret_dollar_offset = self.populate_dollar_offset(tmp_result, False)
        if 'Regression' in results.keys():
            tmp_result = results['Regression']
            self.regression = self.populate_regression(tmp_result)
        if 'Critical Terms' in results.keys():
            tmp_result = results['Critical Terms']
            self.critical_terms = self.populate_critical_terms(tmp_result)
        if 'Pro Variable Reduction' in results.keys():
            tmp_result = results['Pro Variable Reduction']
            self.pro_variable_reduction = self.populate_variable_reduction(tmp_result, True)
        if 'Retro Variable Reduction' in results.keys():
            tmp_result = results['Retro Variable Reduction']
            self.ret_variable_reduction = self.populate_variable_reduction(tmp_result, False)
        if 'Overall Result' in results.keys():
            tmp_result = results['Overall Result']
            self.overall_results = self.populate_overall_result(tmp_result)

    def populate(self, results):
        ''' This method will receive a dictionary and convert the information held within
            into the class structure
        '''
        self.results = results
        if 'Pro Dollar Offset' in results.keys():
            tmp_result = results['Pro Dollar Offset']
            self.pro_dollar_offset = self.populate_dollar_offset(tmp_result, True)
        if 'Retro Dollar Offset' in results.keys():
            tmp_result = results['Retro Dollar Offset']
            self.ret_dollar_offset = self.populate_dollar_offset(tmp_result, False)
        if 'Regression' in results.keys():
            tmp_result = results['Regression']
            self.regression = self.populate_regression(tmp_result)
        if 'Critical Terms' in results.keys():
            tmp_result = results['Critical Terms']
            self.critical_terms = self.populate_critical_terms(tmp_result)
        if 'Pro Variable Reduction' in results.keys():
            tmp_result = results['Pro Variable Reduction']
            self.pro_variable_reduction = self.populate_variable_reduction(tmp_result, True)
        if 'Retro Variable Reduction' in results.keys():
            tmp_result = results['Retro Variable Reduction']
            self.ret_variable_reduction = self.populate_variable_reduction(tmp_result, False)
        if 'Overall Result' in results.keys():
            tmp_result = results['Overall Result']
            self.overall_results = self.populate_overall_result(tmp_result)

    def populate_overall_result(self, overall_result_string):
        ''' This method will populate the overall result of the test set
        '''
        overall_result = OverallResult()
        overall_result.result = HedgeUtils.get_result_value_from_string(overall_result_string)
        overall_result.result_id = HedgeUtils.get_overall_result_id()
        return overall_result

    def populate_dollar_offset(self, dollar_offset_results, pro_flag):
        ''' This method will populate the dollar offset results for the prospective or
            retrospective. The pro_flag determines whether it is pro- or retro-spective.
        '''

        dollar_offset = None

        if dollar_offset_results:
            dollar_offset = DollarOffset()
            dollar_offset.result = HedgeUtils.get_result_value_from_string(
                dollar_offset_results['result']
            )
            if pro_flag:
                dollar_offset.result_id = HedgeUtils.get_pro_do_result_id()
                dollar_offset.last_value_id = HedgeUtils.get_pro_do_value_id()
            else:
                dollar_offset.result_id = HedgeUtils.get_ret_do_result_id()
                dollar_offset.last_value_id = HedgeUtils.get_ret_do_value_id()

            dollar_offset.data = dollar_offset_results['data']

            if 'do' in dollar_offset_results:
                dollar_offset.values = dollar_offset_results['do']
                dates = sorted(dollar_offset.values.keys())
                dollar_offset.last_value = dollar_offset.values[dates[-1]]

        return dollar_offset

    def populate_regression(self, regression_results):
        ''' This method will populate the regression results
        '''

        if regression_results:

            regression = Regression()

            tmp_result = regression_results['result']

            regression.result = HedgeUtils.get_result_value_from_string(tmp_result)
            regression.result_id = HedgeUtils.get_pro_reg_result_id()

            parameters = ['alpha', 'beta', 'correlation', 'R2', 'PValue']
            if all(par in regression_results for par in parameters):
                regression.alpha = regression_results['alpha']
                regression.alpha_id = HedgeUtils.get_pro_reg_alpha_id()
                regression.beta = regression_results['beta']
                regression.beta_id = HedgeUtils.get_pro_reg_beta_id()
                regression.correlation = regression_results['correlation']
                regression.correlation_id = HedgeUtils.get_pro_reg_corr_id()
                regression.r2 = regression_results['R2']
                regression.r2_id = HedgeUtils.get_pro_reg_r2_id()
                regression.pValue = regression_results['PValue']
                regression.pValue_id = HedgeUtils.get_pro_reg_pvalue_id()

        return regression

    def populate_critical_terms(self, critical_terms_results):
        ''' This method will populate the critical terms/values results
        '''

        critical_terms = None

        if critical_terms_results:
            critical_terms = CriticalTerms()

            tmp_result = critical_terms_results['result']

            critical_terms.result = HedgeUtils.get_result_value_from_string(tmp_result)
            critical_terms.result_id = HedgeUtils.get_pro_cv_result_id()

        return critical_terms

    def populate_variable_reduction(self, variable_reduction_results, pro_flag):
        ''' This method will populate the variable reduction results for the prospective or
            retrospective. The pro_flag determines whether it is pro- or retro-spective.
        '''
        variable_reduction = None

        if variable_reduction_results:
            variable_reduction = VariableReduction()

            tmp_result = variable_reduction_results['result']

            variable_reduction.result = HedgeUtils.get_result_value_from_string(tmp_result)
            if pro_flag:
                variable_reduction.result_id = HedgeUtils.get_pro_vrm_result_id()
                variable_reduction.last_value_id = HedgeUtils.get_pro_vrm_value_id()
            else:
                variable_reduction.result_id = HedgeUtils.get_ret_vrm_result_id()
                variable_reduction.last_value_id = HedgeUtils.get_ret_vrm_value_id()

            variable_reduction.data = variable_reduction_results['data']

            if 'vr' in variable_reduction_results:
                variable_reduction.values = variable_reduction_results['vr']
                dates = sorted(variable_reduction.values.keys())
                variable_reduction.last_value = variable_reduction.values[dates[-1]]

        return variable_reduction

    def save(self):
        ''' This method persists the data that is stored in the class to the database
            The Spec Ids are the values of the choice lists that are used when storing data to the
            time series dv table
        '''

        # The choice list for general results storage
        dp_spec_id = HedgeUtils.get_time_series_spec_id()
        # The choice list for data values calculated
        ts_spec_id = HedgeUtils.get_ts_time_series_spec_id()

        if self.overall_results:
            self.save_overall_result(self.overall_results, dp_spec_id)
        if self.pro_dollar_offset:
            self.save_dollar_offset(self.pro_dollar_offset, dp_spec_id, ts_spec_id, True)
        if self.ret_dollar_offset:
            self.save_dollar_offset(self.ret_dollar_offset, dp_spec_id, ts_spec_id, False)
        if self.critical_terms:
            self.save_critical_terms(self.critical_terms, dp_spec_id)
        if self.regression:
            self.save_regression(self.regression, dp_spec_id)
        if self.pro_variable_reduction:
            self.save_variable_reduction(self.pro_variable_reduction, dp_spec_id, ts_spec_id, True)
        if self.ret_variable_reduction:
            self.save_variable_reduction(self.ret_variable_reduction, dp_spec_id, ts_spec_id, False)

    def save_overall_result(self, overall_results, dp_spec_id):
        ''' Save overall result to DB '''

        return save_time_series_DV(dp_spec_id,
                                   self.deal_package_oid,
                                   overall_results.result_id,
                                   overall_results.result)

    def save_dollar_offset(self, dollar_offset, dp_spec_id, ts_spec_id, pro_flag):
        ''' Save dollar offset results to DB '''
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            dollar_offset.result_id,
                            dollar_offset.result)

        if dollar_offset.last_value is not None:
            if math.isnan(dollar_offset.last_value) is False:
                lastValueTsId = save_time_series_DV(dp_spec_id,
                                                    self.deal_package_oid,
                                                    dollar_offset.last_value_id,
                                                    dollar_offset.last_value)
                self.save_data(dollar_offset.data, dp_spec_id, pro_flag)
                self.save_values(dollar_offset.values, ts_spec_id, lastValueTsId)

    def save_critical_terms(self, critical_terms, dp_spec_id):
        ''' Save critical terms result to DB '''

        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            critical_terms.result_id,
                            critical_terms.result)

    def save_regression(self, regression, dp_spec_id):
        ''' Save regression results to DB '''
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            regression.result_id,
                            regression.result)
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            regression.alpha_id,
                            regression.alpha)
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            regression.beta_id,
                            regression.beta)
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            regression.correlation_id,
                            regression.correlation)
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            regression.r2_id,
                            regression.r2)
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            regression.pValue_id,
                            regression.pValue)

    def save_variable_reduction(self, variable_reduction, dp_spec_id, ts_spec_id, pro_flag):
        ''' Save variable reduction results to DB '''
        save_time_series_DV(dp_spec_id,
                            self.deal_package_oid,
                            variable_reduction.result_id,
                            variable_reduction.result)

        if variable_reduction.last_value is not None and \
           math.isnan(variable_reduction.last_value) is False:
            tsOid = save_time_series_DV(dp_spec_id,
                                        self.deal_package_oid,
                                        variable_reduction.last_value_id,
                                        variable_reduction.last_value)

            self.save_data(variable_reduction.data, dp_spec_id, pro_flag)
            self.save_values(variable_reduction.values, ts_spec_id, tsOid)

    def save_data(self, data, dp_spec_id, pro_flag):
        ''' Stores the raw time series delta values that were used by the test formulae
        '''

        dates = sorted(data.keys())
        if pro_flag:
            tPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_PROTPOINTBASE)
            xPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_PROXPOINTBASE)
            yPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_PROYPOINTBASE)
        else:
            tPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_RETTPOINTBASE)
            xPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_RETXPOINTBASE)
            yPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_RETYPOINTBASE)

        count = 0
        while count < len(dates)-1:
            date_string = dates[count]
            date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
            date_ordinal = datetime.date.toordinal(date)
            save_time_series_DV(dp_spec_id,
                                self.deal_package_oid,
                                tPointIds[count],
                                date_ordinal)
            save_time_series_DV(dp_spec_id,
                                self.deal_package_oid,
                                xPointIds[count],
                                data[date_string]['DOriginal'])
            save_time_series_DV(dp_spec_id,
                                self.deal_package_oid,
                                yPointIds[count],
                                data[date_string]['DExternal'])
            count += 1

    def save_values(self, values, ts_spec_id, tsOid):
        ''' Stores the calculated values that were calculated by the test formulae
            This data series is linked to the last item in the data series
        '''

        dates = sorted(values.keys())
        xPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_XPOINTBASE)
        yPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_YPOINTBASE)

        count = 0

        while count < len(dates)-2:
            date_string = dates[count]
            date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
            date_ordinal = datetime.date.toordinal(date)
            save_time_series_DV(ts_spec_id, tsOid, xPointIds[count], date_ordinal)
            save_time_series_DV(ts_spec_id, tsOid, yPointIds[count], values[date_string])
            count += 1

    def read(self):
        ''' This method will search the DB for result data that is related to the given DealPackage
        '''
        dp_spec_id = HedgeUtils.get_time_series_spec_id()  # Choice list for general results storage
        ts_spec_id = HedgeUtils.get_ts_time_series_spec_id()  # Choice list for data values calc'ed
        self.pro_dollar_offset = self.read_dollar_offset(dp_spec_id, ts_spec_id, True)
        self.ret_dollar_offset = self.read_dollar_offset(dp_spec_id, ts_spec_id, False)
        self.critical_terms = self.read_critical_terms(dp_spec_id, ts_spec_id)
        self.regression = self.read_regression(dp_spec_id, ts_spec_id)
        self.pro_variable_reduction = self.read_variable_reduction(dp_spec_id, ts_spec_id, True)
        self.ret_variable_reduction = self.read_variable_reduction(dp_spec_id, ts_spec_id, False)
        self.overall = self.read_overall_result(dp_spec_id, ts_spec_id)

    def read_overall_result(self, dp_spec_id, ts_spec_id):
        ''' This method will search the DB for the most recent overall result that is
            related to the DealPackage for the class instance
        '''
        overall_result = OverallResult()
        overall_result.result_id = HedgeUtils.get_overall_result_id()
        result = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                     dp_spec_id,
                                                     overall_result.result_id)
        overall_result.result = HedgeUtils.get_result_string_from_value(result)
        return overall_result

    def read_dollar_offset(self, dp_spec_id, ts_spec_id, pro_flag):
        ''' Reads data for dollar offset test
        '''
        dollar_offset = DollarOffset()
        if pro_flag:
            dollar_offset.result_id = HedgeUtils.get_pro_do_result_id()
            dollar_offset.last_value_id = HedgeUtils.get_pro_do_value_id()
        else:
            dollar_offset.result_id = HedgeUtils.get_ret_do_result_id()
            dollar_offset.last_value_id = HedgeUtils.get_ret_do_value_id()
        result = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                     dp_spec_id,
                                                     dollar_offset.result_id)
        if result is None:
            return None
        dollar_offset.result = HedgeUtils.get_result_string_from_value(result)
        # Read the raw time series delta values
        dollar_offset.data = self.read_data(dp_spec_id, pro_flag)
        dollar_offset.last_value = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                                       dp_spec_id,
                                                                       dollar_offset.last_value_id)
        # Get all 'last value' dv time series for DP and test type
        lastValueTimeSeries = HedgeUtils.get_time_series_dv(self.deal_package_oid,
                                                            dp_spec_id,
                                                            dollar_offset.last_value_id)
        # Get the last (most recent) key for the set of test data
        tsOid = lastValueTimeSeries.Last().Oid()
        # Read the calculated values
        dollar_offset.values = self.read_values(ts_spec_id, tsOid)
        return dollar_offset

    def read_critical_terms(self, dp_spec_id, ts_spec_id):
        ''' Reads data for critical terms test
        '''
        critical_terms = CriticalTerms()
        critical_terms.result_id = HedgeUtils.get_pro_cv_result_id()
        result = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                     dp_spec_id,
                                                     critical_terms.result_id)
        if result is None:
            return None
        critical_terms.result = HedgeUtils.get_result_string_from_value(result)
        return critical_terms

    def read_regression(self, dp_spec_id, ts_spec_id):
        ''' Reads data for regression test
        '''
        regression = Regression()
        regression.result_id = HedgeUtils.get_pro_reg_result_id()
        result = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                     dp_spec_id,
                                                     regression.result_id)
        if result is None:
            return None
        # Convert stored value into text
        regression.result = HedgeUtils.get_result_string_from_value(result)
        # Read test results from DB
        regression.alpha_id = HedgeUtils.get_pro_reg_alpha_id()
        regression.alpha = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                               dp_spec_id,
                                                               regression.alpha_id)
        regression.beta_id = HedgeUtils.get_pro_reg_beta_id()
        regression.beta = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                              dp_spec_id,
                                                              regression.beta_id)
        regression.correlation_id = HedgeUtils.get_pro_reg_corr_id()
        regression.correlation = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                                     dp_spec_id,
                                                                     regression.correlation_id)
        regression.r2_id = HedgeUtils.get_pro_reg_r2_id()
        regression.r2 = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                            dp_spec_id,
                                                            regression.r2_id)
        regression.pValue_id = HedgeUtils.get_pro_reg_pvalue_id()
        regression.pValue = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                                dp_spec_id,
                                                                regression.pValue_id)
        return regression

    def read_variable_reduction(self, dp_spec_id, ts_spec_id, pro_flag):
        ''' Reads data for variable reduction methos test
        '''
        variable_reduction = VariableReduction()
        if pro_flag:
            variable_reduction.result_id = HedgeUtils.get_pro_vrm_result_id()
            variable_reduction.last_value_id = HedgeUtils.get_pro_vrm_value_id()
        else:
            variable_reduction.result_id = HedgeUtils.get_ret_vrm_result_id()
            variable_reduction.last_value_id = HedgeUtils.get_ret_vrm_value_id()
        result = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                     dp_spec_id,
                                                     variable_reduction.result_id)
        if result is None:
            return None
        # Convert stored value into text
        variable_reduction.result = HedgeUtils.get_result_string_from_value(result)
        # Read the raw time series delta values
        variable_reduction.data = self.read_data(dp_spec_id, pro_flag)
        variable_reduction.last_value = HedgeUtils.\
            get_time_series_dv_value(self.deal_package_oid,
                                     dp_spec_id,
                                     variable_reduction.last_value_id)
        # Get all 'last value' dv time series for DP and test type
        lastValueTimeSeries = HedgeUtils.get_time_series_dv(self.deal_package_oid,
                                                            dp_spec_id,
                                                            variable_reduction.last_value_id)
        # Get the last (most recent) key for the set of test data
        tsOid = lastValueTimeSeries.Last().Oid()
        # Read the calculated values
        variable_reduction.values = self.read_values(ts_spec_id, tsOid)
        return variable_reduction

    def read_data(self, dp_spec_id, pro_flag):
        if pro_flag:
            tPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_PROTPOINTBASE)
            xPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_PROXPOINTBASE)
            yPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_PROYPOINTBASE)
        else:
            tPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_RETTPOINTBASE)
            xPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_RETXPOINTBASE)
            yPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_RETYPOINTBASE)
        data = {}
        for count in range(1, len(tPointIds)):
            date_ordinal = HedgeUtils.get_time_series_dv_value(self.deal_package_oid,
                                                               dp_spec_id,
                                                               tPointIds[count])
            if not date_ordinal:
                continue
            date_ordinal = int(date_ordinal)
            date = datetime.date.fromordinal(date_ordinal)
            date_string = datetime.datetime.strftime(date, '%Y-%m-%d')
            data[date_string] = {}
            data[date_string]['DOriginal'] = {}
            data[date_string]['DExternal'] = {}
            xTS = HedgeUtils.get_time_series_dv(self.deal_package_oid,
                                                dp_spec_id,
                                                xPointIds[count])
            xDvValue = HedgeUtils.get_tsdv_value_from_TS(xTS)
            xDvCurr = HedgeUtils.get_tsdv_curr_from_TS(xTS)
            xDvDate = HedgeUtils.get_tsdv_date_from_TS(xTS)
            yTS = HedgeUtils.get_time_series_dv(self.deal_package_oid,
                                                dp_spec_id,
                                                yPointIds[count])
            yDvValue = HedgeUtils.get_tsdv_value_from_TS(yTS)
            yDvCurr = HedgeUtils.get_tsdv_curr_from_TS(yTS)
            yDvDate = HedgeUtils.get_tsdv_date_from_TS(yTS)
            if xDvCurr:
                if xDvDate:
                    data[date_string]['DOriginal'] = acm.DenominatedValue(xDvValue,
                                                                          xDvCurr,
                                                                          xDvDate)
                else:
                    data[date_string]['DOriginal'] = acm.DenominatedValue(xDvValue, xDvCurr)
            else:
                if xDvDate:
                    data[date_string]['DOriginal'] = acm.DenominatedValue(xDvValue, None, xDvDate)
                else:
                    data[date_string]['DOriginal'] = xDvValue
            if yDvCurr:
                if yDvDate:
                    data[date_string]['DExternal'] = acm.DenominatedValue(yDvValue,
                                                                          yDvCurr,
                                                                          yDvDate)
                else:
                    data[date_string]['DExternal'] = acm.DenominatedValue(yDvValue, yDvCurr)
            else:
                if yDvDate:
                    data[date_string]['DExternal'] = acm.DenominatedValue(yDvValue, None, yDvDate)
                else:
                    data[date_string]['DExternal'] = yDvValue
        return data

    def read_values(self, ts_spec_id, tsOid):
        xPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_XPOINTBASE)
        yPointIds = HedgeUtils.get_point_ids(HedgeConstants.STR_YPOINTBASE)
        values = {}
        for count in range(1, len(xPointIds)):
            date_oridnal_raw = HedgeUtils.get_time_series_dv_value(tsOid,
                                                                   ts_spec_id,
                                                                   xPointIds[count])
            if date_oridnal_raw is None:
                continue
            date_ordinal = int(date_oridnal_raw)
            date = datetime.date.fromordinal(date_ordinal)
            date_string = datetime.datetime.strftime(date, '%Y-%m-%d')
            ts = HedgeUtils.get_time_series_dv(tsOid, ts_spec_id, yPointIds[count])
            dvValue = HedgeUtils.get_tsdv_value_from_TS(ts)
            dvCurr = HedgeUtils.get_tsdv_curr_from_TS(ts)
            dvDate = HedgeUtils.get_tsdv_date_from_TS(ts)
            if dvCurr:
                if dvDate:
                    values[date_string] = acm.DenominatedValue(dvValue, dvCurr, dvDate)
                else:
                    values[date_string] = acm.DenominatedValue(dvValue, dvCurr)
            else:
                if dvDate:
                    values[date_string] = acm.DenominatedValue(dvValue, None, dvDate)
                else:
                    values[date_string] = dvValue
        return values


def save_time_series_DV(spec_id, rec_add_1, rec_add_2, value):
    '''
        This function will commit the params dictionary to the FTimeSeriesDv table.
        If the Time Series record already exists, it will be updated, else it will be created.
    '''
    if math.isnan(value) is False:
        try:
            storage_date = acm.Time().DateNow()
            query = 'timeSeriesDvSpecification = %s and '\
                    'storageDate = \'%s\' and '\
                    'recordAddress1 = %s and '\
                    'recordAddress2 = %s'\
                    % (spec_id, storage_date, rec_add_1, rec_add_2)

            time_series = acm.FTimeSeriesDv.Select(query)

            if time_series:
                time_series = time_series[0]

            if not time_series:
                time_series = acm.FTimeSeriesDv()
                time_series.TimeSeriesDvSpecification(spec_id)

            if isinstance(value, (types.FloatType, types.IntType)):
                time_series.DvValue(value)
            elif value.IsKindOf(acm.FDenominatedValue):
                try:
                    time_series.DvValue(value.Number())
                    time_series.DvCurrency(value.Unit())
                    time_series.DvDate(value.DateTime())
                except:
                    logger.ELOG('Denominated Value is incorrectly formed')
                    raise Exception('Denominated Value is incorrectly formed')
            else:
                raise TypeError('Value must be of type float, int or Denominated Value')

            time_series.RecordAddress1(rec_add_1)
            time_series.RecordAddress2(rec_add_2)
            time_series.StorageDate(storage_date)

            time_series.Commit()

            return time_series.Oid()

        except Exception, ex:
            logger.ELOG('Unable to commit time series DV - %s' % ex)
            return None
    else:
        logger.ELOG('Unable to commit time series DV - NaN value.')
        return None
