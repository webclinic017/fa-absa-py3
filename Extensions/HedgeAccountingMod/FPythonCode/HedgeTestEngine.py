'''
===================================================================================================
PURPOSE: The HedgeTestengine manages the hedge effectiveness testing procedure and also contain the
            test specific algorithms and logic. The testing algorithms are:
                - Regression test
                - Variable Reduction test
                - Dollar offset test
                - Critical terms test
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''
import sys

import acm
import FLogger

import HedgeConstants
import HedgeResults
import HedgePriceSeriesBuilder

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE, HedgeConstants.LOG_VERBOSITY)

try:
    sys.path.insert(-1, HedgeConstants.STR_NumPySciPyLocalLoadPath)
    sys.path.insert(-1, HedgeConstants.STR_NumPySciPyServerLoadPath)

    from scipy import stats
except ImportError, e:
    logger.WLOG('There was an error importing the scipy library. '
                'Regression testing will not work. Exception: %s'% e)
    stats = None

context = acm.GetDefaultContext()
sheet_type = HedgeConstants.STR_TRADE_SHEET
calcSpace = acm.Calculations().CreateCalculationSpace(context, sheet_type)


def compare(comparator, terms):
    if comparator == 'Equal':
        value = None
        for term in terms:
            if not value:
                value = term
            if term != value:
                return False

    elif comparator == 'Absolute':
        value = None
        for term in terms:
            if not value:
                value = term
            if abs(value) != abs(term):
                return False

    elif comparator == 'N/A':
        return True

    else:
        logger.WLOG('Comparator not defined')
        return False

    return True


def print_dictionary(m_dict):
    overal_comparison = True

    for key in m_dict:
        dict2 = m_dict[key]
        columns = dict2.keys()
        columns.sort()
        terms = []
        for column in columns:
            if column == 'Compare':
                continue
            value = dict2[column]
            terms.append(value)

        # Compute Result
        comparator = dict2['Compare']
        comparison = compare(comparator, terms)
        dict2['Result'] = comparison
        m_dict[key] = dict2
        if not comparison:
            pass
        overal_comparison = (overal_comparison and comparison)
    return m_dict


def get_critical_terms(trade, m_dict):

    def addToDict(term, value, comparator='Equal'):
        if term not in m_dict:
            m_dict[term] = {'Compare': comparator}
        dict2 = m_dict[term]

        dict2[trade.Oid()] = value
        m_dict[term] = dict2
        return m_dict

    instrument = trade.Instrument()
    fixed_leg = instrument.FirstFixedLeg()

    fixed_leg_fixed_rate = None
    fixed_leg_fixed_rolling_period = None
    fixed_leg_fixed_day_count = None

    if fixed_leg:
        fixed_leg_fixed_rate = fixed_leg.FixedRate()
        fixed_leg_fixed_rolling_period = fixed_leg.RollingPeriod()
        fixed_leg_fixed_day_count = fixed_leg.DayCountMethod()

    addToDict('Expiry Date', instrument.ExpiryDate())
    addToDict('Start Date', instrument.StartDate())
    addToDict('Value Date', instrument.ExpiryDateOnly())
    addToDict('Nominal Amount', trade.Nominal(), 'Absolute')
    addToDict('Interest Rate', fixed_leg_fixed_rate)
    addToDict('Rolling Period', fixed_leg_fixed_rolling_period)
    addToDict('Currency', instrument.Currency().Name())
    addToDict('Spot Days', instrument.SpotBankingDaysOffset())
    addToDict('Day Count Method', fixed_leg_fixed_day_count)

    return m_dict


def run_critical_terms_comparison(trades):
    m_dict = {}
    for trade in trades:
        m_dict = get_critical_terms(trade, m_dict)
    return print_dictionary(m_dict)


def remove_column_simulations(trade):
    # Remove possible simulations that were done earlier
    try:
        calcSpace.RemoveSimulation(trade, 'Valuation Date')
        calcSpace.RemoveSimulation(trade, 'Fixed Rate')
        calcSpace.RemoveSimulation(trade, 'Hedge Accounting Start Date')
        calcSpace.RemoveSimulation(trade, 'Hedge Accounting End Date')
        calcSpace.RemoveSimulation(trade, 'Hedge Accounting Parameter Date')
    except:
        pass


def run_variable_reduction(series_a, series_b, dates):
    '''Variable Reduction Method

    Input: Two lists of values (same length)
    Output: Variable reduction percentage.

    VR = 1-[sum(a+b)^2/sum(b)^2]

    The sign of a differs from that of b in an effective hedge.

    For more information, refer to the paper by Finnerty and Grant entitled
        "TESTING HEDGE EFFECTIVENESS UNDER SFAS 133"
    '''

    results = {}

    if len(series_a) != len(series_b):
        logger.WLOG('Unable to perform variable reduction analysis'
                    ' - the two series are of different lengths.')
        return results

    if not series_a:
        logger.WLOG('Unable to perform variable reduction analysis - no input.')
        return results

    if len(series_a) != len(dates) - 1:
        logger.WLOG('Unable to perform the variable reduction analysis'
                    ' - %s dates have been submitted, but %s data points.'
                    % (len(dates), len(series_a)))
        return results

    epsilon = 1e-6
    sum_a_plus_b_squared = 0
    sum_b_squared = 0
    vr = {}

    dateIndex = 0
    while dateIndex < len(dates):
        date = dates[dateIndex]
        if dateIndex == 0:
            vr[date] = 0
            dateIndex += 1
            continue
        a_plus_b_squared = (series_a[date] + series_b[date])**2
        b_squared = series_b[date]**2
        sum_a_plus_b_squared += a_plus_b_squared
        sum_b_squared += b_squared

        if sum_b_squared < epsilon:
            logger.WLOG('The cumulative change in the value of the hedged item on %s is less than '
                        '%s, \n\t causing the variable reduction percentage to tend towards '
                        'negative infinity.' % (date, epsilon))
            vr[date] = 0
        else:
            vr[date] = (1 - (sum_a_plus_b_squared / float(sum_b_squared)))
        dateIndex += 1

    results['vr'] = vr
    return results


def run_regression(series1, series2):
    '''
        Implements the actual regression calculation using scipy

        Input: Two lists of values (same length)
        Output: Dictionary with regression output variables
    '''

    results = {}

    if len(series1) != len(series2):
        logger.WLOG('Two series for regression are of different length. '
                    'Unable to perform regression analysis.')
        return results

    if not series1:
        logger.WLOG('No input for the regression. Unable to perform regression analysis.')
        return results

    if len(series1) < 2:
        logger.WLOG('Not enough input for the regression (n < 2). '
                    'Unable to perform regression analysis.')
        return results

    try:
        beta, alpha, correlation, p_value, std_err = stats.linregress(series1, series2)
        results['alpha'] = alpha
        results['beta'] = beta
        results['correlation'] = correlation
        results['R2'] = correlation**2
        results['PValue'] = p_value
        results['Std_Err'] = std_err
    except Exception, e:
        logger.ELOG('There was an error with the regression: %s' % e)
    return results


def run_dollar_offset(series1, series2, dates):

    results = {}

    if len(series1) != len(series2):
        logger.WLOG('Unable to execute the dollar offset method'
                    ' - the two series are of different lengths.')
        return results

    if not series1:
        logger.WLOG('Unable to perform variable reduction analysis - no input.')
        return results

    x_cum = 0
    y_cum = 0
    epsilon = 1e-6
    do = {}

    dateIndex = 0
    while dateIndex < len(dates):
        date = dates[dateIndex]
        if dateIndex == 0:
            do[date] = 0
            dateIndex += 1
            continue
        x = series1[date]
        y = series2[date]
        x_cum += x
        y_cum += y
        dateIndex += 1

        if abs(x_cum) < epsilon:
            logger.WLOG('The cumulative change in the value of the hedged item on %s is less '
                        'than %s,\n\t causing the dollar offset percentage to tend towards '
                        'infinity. 1e6 returned.' % (date, epsilon))
            # If both the numerator and denominator are < epsilon, the hedge is effective,
            #   even though the DO calculation might return a contradictory result.
            if abs(y_cum) < epsilon:
                do[date] = 1
            # The choice of numerator and denomnitor is arbitrary, so the ratio may be reversed
            #   for this special case, which will fail.
            else:
                do[date] = 0
        else:
            do[date] = -y_cum/float(x_cum)

    results['do'] = do
    return results


def get_trades_numbers(h, m_type):
    returnTrades = []
    trades = h.get_trades()
    for trdnbr in trades:
        hedgetype, _, _ = trades[trdnbr]
        if m_type == hedgetype:
            returnTrades.append(trdnbr)
    return returnTrades


def is_valid_hedge_relation(hedge_relation):
    ''' Check if Hedge Relation is valid to perform tests:
        * At least 1 "Hypo" trade
        * At least 1 "External" trade
    '''

    trades = hedge_relation.get_trades()
    hedges = []
    hypos = []
    for trade in trades.keys():
        if trades[trade][0] == 'Hypo':
            hypos.append(trade)
        if trades[trade][0] == 'External':
            hedges.append(trade)

    if len(hedges) < 1 or len(hypos) < 1:
        logger.WLOG('Not enough Hypo or External trades specified.')
        return False
    return True


def run_tests(hedge_relation, m_type=None, test_date=acm.Time().DateNow()):
    results = {}
    test_settings = hedge_relation.get_test_settings()
    if not is_valid_hedge_relation(hedge_relation):
        logger.WLOG('Hedge Relation not valid for testing')
        return results

    overall_result = 'Fail'
    active_test_count = 0
    tests_passed_count = 0

    if test_settings:
        # Calculate the time series once, as the same data are used for all tests.
        test_settings = hedge_relation.get_test_settings()
        timeBucketSettingsItem = test_settings['TimeBuckets']
        timeBucketName = ''
        if timeBucketSettingsItem:
            timeBucketName = timeBucketSettingsItem['TimeBuckets']

        retro_price_builder = HedgePriceSeriesBuilder.price_delta_builder(hedge_relation)
        retro_price_builder.build_retrospective_price_series(timeBucketName, test_date)

        pro_price_builder = HedgePriceSeriesBuilder.price_delta_builder(hedge_relation)
        pro_price_builder.build_simulated_price_series(timeBucketName, test_date)

        # always run all tests:

        # run Prospective Dollar Offset tests
        pro_dollar_offset_result = run_test_pro_dollar_offset(hedge_relation, pro_price_builder)
        results['Pro Dollar Offset'] = pro_dollar_offset_result

        # run Retrospective Dollar Offset tests
        retro_dollar_offset_result = run_test_retro_dollar_offset(hedge_relation,
                                                                  retro_price_builder)
        results['Retro Dollar Offset'] = retro_dollar_offset_result

        # run Regression tests
        regression_result = run_test_regression(hedge_relation, pro_price_builder)
        results['Regression'] = regression_result

        # run Prospective Variable Reduction tests
        pro_variable_reduction_result = run_test_pro_variable_reduction(hedge_relation,
                                                                        pro_price_builder)
        results['Pro Variable Reduction'] = pro_variable_reduction_result

        # run Retrospective Variable Reduction tests
        retro_variable_reduction_result = run_test_retro_variable_reduction(hedge_relation,
                                                                            retro_price_builder)
        results['Retro Variable Reduction'] = retro_variable_reduction_result

        # run Critical Terms tests
        critical_terms_result = run_test_critical_terms(hedge_relation)
        results['Critical Terms'] = critical_terms_result

        # Apply overall Pass/Fail rule when the designation date is on today
        # - Rule: Only look at prospective test results since no retrospective
        #               data will exist for child trades on designation date.
        designation_date = hedge_relation.get_start_date()
        if designation_date[:10] == acm.Time().DateNow()[:10]:
            if test_settings['ProDollarOffset']['Enabled'] == 'True':
                if (pro_dollar_offset_result['result'] == 'Pass')or\
                   (pro_dollar_offset_result['result'] == 'Warning'):
                    overall_result = 'Pass'

            if test_settings['ProVRM']['Enabled'] == 'True':
                if (pro_variable_reduction_result['result'] == 'Pass')or\
                   (pro_variable_reduction_result['result'] == 'Warning'):
                    overall_result = 'Pass'

            if test_settings['Regression']['Enabled'] == 'True':
                if (regression_result['result'] == 'Pass')or\
                   (regression_result['result'] == 'Warning'):
                    overall_result = 'Pass'

        else:
            # Apply overall Pass/Fail rule when the designation date not on today:
            # - Rule: If the regression test pass, the overall test will pass,
            #           otherwise all other tests should pass.
            if test_settings['Regression']['Enabled'] == 'True':
                if (regression_result['result'] == 'Pass')or\
                   (regression_result['result'] == 'Warning'):
                    overall_result = 'Pass'

            elif test_settings['ProVRM']['Enabled'] == 'True':
                # JS (2017-12-11): Add Exception to the overall pass/fail
                # criteria as requested by James Moodie.
                # Rule: if prospective VRM pass, overall result should pass
                #   regardless of the retrospective result.
                if (pro_variable_reduction_result['result'] == 'Pass')or\
                   (pro_variable_reduction_result['result'] == 'Warning'):
                    overall_result = 'Pass'
            else:
                if test_settings['ProDollarOffset']['Enabled'] == 'True':
                    active_test_count += 1
                    if (pro_dollar_offset_result['result'] == 'Pass')or\
                       (pro_dollar_offset_result['result'] == 'Warning'):
                        tests_passed_count += 1

                if test_settings['RetroDollarOffset']['Enabled'] == 'True':
                    active_test_count += 1
                    if (retro_dollar_offset_result['result'] == 'Pass')or\
                       (retro_dollar_offset_result['result'] == 'Warning'):
                        tests_passed_count += 1

                if test_settings['ProVRM']['Enabled'] == 'True':
                    active_test_count += 1
                    if (pro_variable_reduction_result['result'] == 'Pass')or\
                       (pro_variable_reduction_result['result'] == 'Warning'):
                        tests_passed_count += 1

                if test_settings['RetroVRM']['Enabled'] == 'True':
                    active_test_count += 1
                    if (retro_variable_reduction_result['result'] == 'Pass')or\
                       (retro_variable_reduction_result['result'] == 'Warning'):
                        tests_passed_count += 1

                if test_settings['CriticalTerms']['Enabled'] == 'True':
                    active_test_count += 1
                    if (critical_terms_result['result'] == 'Pass')or\
                       (critical_terms_result['result'] == 'Warning'):
                        tests_passed_count += 1

                # set overall result
                if active_test_count > 0 and active_test_count == tests_passed_count:
                    overall_result = 'Pass'
                else:
                    overall_result = 'Fail'

        results['Overall Result'] = overall_result

        # Save Test History
        _, deal_package_name = hedge_relation.get_deal_package()
        deal_package_oid = acm.FDealPackage[deal_package_name].Oid()

        results_class = HedgeResults.HedgeResults(deal_package_oid)
        results_class.populate(results)
        results_class.save()
    return results


def run_test_pro_variable_reduction(hedgeRelation, priceBuilder):
    # Get results from Test Engine
    # Then test if it is within limits, decide "Pass" or "Fail" or "Warning"
    results = run_test_pro_variable_reduction_logic(hedgeRelation, priceBuilder)

    if not results:
        return results

    dates = sorted(results['vr'].keys())
    value = results['vr'][dates[-1]]  # check to see that this is the last item....

    testsettings = hedgeRelation.get_test_settings()
    limit = float(testsettings['ProVRM']['Limit'])
    warning = float(testsettings['ProVRM']['Warning'])

    result = 'Fail'
    if value >= warning:
        result = 'Pass'
    if value < warning and value >= limit:
        result = 'Warning'
    if value < limit:
        result = 'Fail'

    results['result'] = result

    return results


def run_test_retro_variable_reduction(hedgeRelation, priceBuilder):
    # Get results from Test Engine
    # Then test if it is within limits, decide "Pass" or "Fail" or "Warning"
    results = run_test_retro_variable_reduction_logic(hedgeRelation, priceBuilder)

    if not results or ('vr' in results) is False:
        results['result'] = 'Fail'
        return results

    dates = sorted(results['vr'].keys())
    value = results['vr'][dates[-1]]  # check to see that this is the last item....

    testsettings = hedgeRelation.get_test_settings()

    limit = float(testsettings['RetroVRM']['Limit'])
    warning = float(testsettings['RetroVRM']['Warning'])

    result = 'Fail'
    if value >= warning:
        result = 'Pass'
    if value < warning and value >= limit:
        result = 'Warning'
    if value < limit:
        result = 'Fail'

    results['result'] = result
    return results


def run_test_critical_terms(hedgeRelation):
    result = run_test_critical_terms_logic(hedgeRelation)
    return result


def run_test_pro_dollar_offset(hedgeRelation, priceBuilder):
    # Get results from Test Engine
    # Then test if it is within limits, decide "Pass" or "Fail" or "Warning"
    results = run_test_pro_dollar_offset_logic(hedgeRelation, priceBuilder)

    if not results:
        return results

    testsettings = hedgeRelation.get_test_settings()
    loLimit = float(testsettings['ProDollarOffset']['LoLimit'])
    hiLimit = float(testsettings['ProDollarOffset']['HiLimit'])
    loWarning = float(testsettings['ProDollarOffset']['LoWarning'])
    hiWarning = float(testsettings['ProDollarOffset']['HiWarning'])

    dates = sorted(results['do'].keys())
    value = results['do'][dates[-1]]

    result = 'Fail'
    if value >= loWarning and value <= hiWarning:
        result = 'Pass'
    elif (value < loWarning and value >= loLimit) or\
            (value > hiWarning and value <= hiLimit):
        result = 'Warning'
    elif value < loLimit or value > hiLimit:
        result = 'Fail'

    results['result'] = result
    return results


def run_test_retro_dollar_offset(hedgeRelation, priceBuilder):
    # Get results from Test Engine
    # Then test if it is within limits, decide "Pass" or "Fail" or "Warning"
    results = run_test_retro_dollar_offset_logic(hedgeRelation, priceBuilder)

    if not results or 'do' not in results:
        results['result'] = 'Fail'
        return results

    testsettings = hedgeRelation.get_test_settings()
    loLimit = float(testsettings['RetroDollarOffset']['LoLimit'])
    hiLimit = float(testsettings['RetroDollarOffset']['HiLimit'])
    loWarning = float(testsettings['RetroDollarOffset']['LoWarning'])
    hiWarning = float(testsettings['RetroDollarOffset']['HiWarning'])

    dates = sorted(results['do'].keys())
    value = results['do'][dates[-1]]

    result = 'Fail'
    if value >= loWarning and value <= hiWarning:
        result = 'Pass'
    elif (value < loWarning and value >= loLimit) or\
            (value > hiWarning and value <= hiLimit):
        result = 'Warning'
    elif value < loLimit or value > hiLimit:
        result = 'Fail'

    results['result'] = result
    return results


def run_test_regression(hedgeRelation, priceBuilder):

    results = run_test_regression_logic(hedgeRelation, priceBuilder)

    if not results:
        return results

    testsettings = hedgeRelation.get_test_settings()

    beta = results['beta']
    R2 = results['R2']
    PValue = results['PValue']

    hiBetaLimit = float(testsettings['Regression']['HiBetaLimit'])
    loBetaLimit = float(testsettings['Regression']['LoBetaLimit'])
    hiBetaWarning = float(testsettings['Regression']['HiBetaWarning'])
    loBetaWarning = float(testsettings['Regression']['LoBetaWarning'])
    R2Limit = float(testsettings['Regression']['R2Limit'])
    R2Warning = float(testsettings['Regression']['R2Warning'])
    PValueLimit = float(testsettings['Regression']['PValueLimit'])
    PValueWarning = float(testsettings['Regression']['PValueWarning'])

    resultTotal = 'Fail'
    resultBeta = 'Fail'
    resultR2 = 'Fail'
    resultPValue = 'Fail'

    if beta >= loBetaWarning and beta <= hiBetaWarning:
        resultBeta = 'Pass'
    elif (beta < loBetaWarning and beta > hiBetaWarning) and\
            (beta >= loBetaLimit and beta <= hiBetaLimit):
        resultBeta = 'Warning'
    elif beta < loBetaLimit or beta > hiBetaLimit:
        resultBeta = 'Fail'

    if R2 >= R2Warning and R2 >= R2Limit:
        resultR2 = 'Pass'
    elif R2 < R2Warning and R2 >= R2Limit:
        resultR2 = 'Warning'
    elif R2 < R2Limit:
        resultR2 = 'Fail'

    if PValue <= PValueWarning and PValue <= PValueLimit:
        resultPValue = 'Pass'
    elif PValue > PValueWarning and PValue <= PValueLimit:
        resultPValue = 'Warning'
    elif PValue > PValueLimit:
        resultPValue = 'Fail'

    if resultBeta == 'Fail' or resultR2 == 'Fail' or resultPValue == 'Fail':
        resultTotal = 'Fail'
    elif resultBeta == 'Warning' or resultR2 == 'Warning' or resultPValue == 'Warning':
        resultTotal = 'Warning'
    else:
        resultTotal = 'Pass'

    results['result'] = resultTotal
    results['resultBeta'] = resultBeta
    results['resultR2'] = resultR2
    results['resultPValue'] = resultPValue

    return results


def run_test_pro_variable_reduction_logic(hedgeRelation, priceBuilder):
    # get the appropriate time series to be used in the test
    seriesOrig = priceBuilder.marketValueSeries_Original
    seriesExt = priceBuilder.marketValueSeries_External
    seriesDOrig = priceBuilder.marketValueDeltaSeries_Original
    seriesDExt = priceBuilder.marketValueDeltaSeries_External

    dates = priceBuilder.get_sorted_date_range()

    results = run_variable_reduction(seriesDExt, seriesDOrig, dates)

    if not results:
        results = {}

    i = 0
    results['data'] = {}
    for date in dates:
        results['data'][date] = {}
        results['data'][date]['Original'] = seriesOrig[date]
        results['data'][date]['External'] = seriesExt[date]
        if i == 0:
            results['data'][date]['DOriginal'] = 0
            results['data'][date]['DExternal'] = 0
        else:
            results['data'][date]['DOriginal'] = seriesDOrig[date]
            results['data'][date]['DExternal'] = seriesDExt[date]
        i += 1

    results['original'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.Hypo)
    results['external'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.External)

    return results


def run_test_retro_variable_reduction_logic(hedgeRelation, priceBuilder):
    # get the appropriate time series to be used in the test
    seriesOrig = priceBuilder.marketValueSeries_Original
    seriesExt = priceBuilder.marketValueSeries_External
    seriesDOrig = priceBuilder.marketValueDeltaSeries_Original
    seriesDExt = priceBuilder.marketValueDeltaSeries_External

    dates = priceBuilder.get_sorted_date_range()

    results = run_variable_reduction(seriesDExt, seriesDOrig, dates)

    if not results:
        results = {}

    i = 0
    results['data'] = {}
    for date in dates:
        results['data'][date] = {}
        results['data'][date]['Original'] = seriesOrig[date]
        results['data'][date]['External'] = seriesExt[date]
        if i == 0:
            results['data'][date]['DOriginal'] = 0
            results['data'][date]['DExternal'] = 0
        else:
            results['data'][date]['DOriginal'] = seriesDOrig[date]
            results['data'][date]['DExternal'] = seriesDExt[date]
        i += 1

    results['original'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.Hypo)
    results['external'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.External)

    return results


def run_test_pro_dollar_offset_logic(hedgeRelation, priceBuilder):
    # get the appropriate time series to be used in the test
    seriesOrig = priceBuilder.marketValueSeries_Original
    seriesExt = priceBuilder.marketValueSeries_External
    seriesDOrig = priceBuilder.marketValueDeltaSeries_Original
    seriesDExt = priceBuilder.marketValueDeltaSeries_External

    dates = priceBuilder.get_sorted_date_range()

    results = run_dollar_offset(seriesDOrig, seriesDExt, dates)

    if not results:
        results = {}

    i = 0
    results['data'] = {}
    for date in dates:
        results['data'][date] = {}
        results['data'][date]['Original'] = seriesOrig[date]
        results['data'][date]['External'] = seriesExt[date]
        if i == 0:
            results['data'][date]['DOriginal'] = 0
            results['data'][date]['DExternal'] = 0
        else:
            results['data'][date]['DOriginal'] = seriesDOrig[date]
            results['data'][date]['DExternal'] = seriesDExt[date]
        i += 1

    results['original'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.Hypo)
    results['external'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.External)

    return results


def run_test_retro_dollar_offset_logic(hedgeRelation, priceBuilder):
    # get the appropriate time series to be used in the test
    seriesOrig = priceBuilder.marketValueSeries_Original
    seriesExt = priceBuilder.marketValueSeries_External
    seriesDOrig = priceBuilder.marketValueDeltaSeries_Original
    seriesDExt = priceBuilder.marketValueDeltaSeries_External

    dates = priceBuilder.get_sorted_date_range()

    results = run_dollar_offset(seriesDOrig, seriesDExt, dates)

    if not results:
        results = {}

    i = 0
    results['data'] = {}
    for date in dates:
        results['data'][date] = {}
        results['data'][date]['Original'] = seriesOrig[date]
        results['data'][date]['External'] = seriesExt[date]
        if i == 0:
            results['data'][date]['DOriginal'] = 0
            results['data'][date]['DExternal'] = 0
        else:
            results['data'][date]['DOriginal'] = seriesDOrig[date]
            results['data'][date]['DExternal'] = seriesDExt[date]
        i += 1

    results['original'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.Hypo)
    results['external'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.External)

    return results


def run_test_regression_logic(hedgeRelation, priceBuilder):
    # get the appropriate time series to be used in the test
    seriesOrig = priceBuilder.marketValueSeries_Original
    seriesExt = priceBuilder.marketValueSeries_External
    seriesDOrig = priceBuilder.marketValueDeltaSeries_Original
    seriesDExt = priceBuilder.marketValueDeltaSeries_External

    dates = priceBuilder.get_sorted_date_range()

    results = run_regression(seriesDExt.values(), seriesDOrig.values())

    if not results:
        results = {}

    i = 0
    results['data'] = {}
    for date in dates:
        results['data'][date] = {}
        results['data'][date]['Original'] = seriesOrig[date]
        results['data'][date]['External'] = seriesExt[date]
        if i == 0:
            results['data'][date]['DOriginal'] = 0
            results['data'][date]['DExternal'] = 0
        else:
            results['data'][date]['DOriginal'] = seriesDOrig[date]
            results['data'][date]['DExternal'] = seriesDExt[date]
        i += 1

    results['original'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.Hypo)
    results['external'] = get_trades_numbers(hedgeRelation,
                                             HedgeConstants.Hedge_Trade_Types.External)

    return results


def run_test_critical_terms_logic(hedgeRelation):
    trade_list = []

    tradesDict = hedgeRelation.get_trades()
    for tradeOid in tradesDict:
        m_type, _, childTradeId = tradesDict[tradeOid]

        if m_type == HedgeConstants.Hedge_Trade_Types.External:
            trade_list.append(acm.FTrade[childTradeId])
        elif m_type == HedgeConstants.Hedge_Trade_Types.Hypo:
            trade_list.append(acm.FTrade[tradeOid])

    total = 'Pass'
    m_dict = run_critical_terms_comparison(trade_list)

    for key in m_dict:
        results = m_dict[key]
        for result in results:
            if not results[result]:
                total = 'Fail'

    results = {}
    results['result'] = total
    results['info'] = m_dict
    return results
