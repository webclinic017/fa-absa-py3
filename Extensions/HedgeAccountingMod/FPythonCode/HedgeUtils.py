'''
===================================================================================================
PURPOSE: A collection a helper functions used throughout the Hedge Effectiveness Testing solution.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import types
from datetime import datetime

import acm
import FLogger

import HedgeConstants
import HedgeRelation
import HedgeAccountingStorage


LOGGER = FLogger.FLogger(__name__)

denominatedvalue = acm.GetFunction('denominatedvalue', 4)


def convert_currencies(value, valuationDate, fromCurrency, toCurrency):
    '''Convert between currencies, taking into account the valuation date and the discounting
        required to account for spot days.
    '''
    if fromCurrency.Name() == toCurrency.Name():
        return denominatedvalue(value, toCurrency, '', '')
    else:
        currPair = fromCurrency.CurrencyPair(toCurrency)
        curr1 = currPair.Currency1()
        curr2 = currPair.Currency2()
        space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        spotDate = currPair.SpotDate(valuationDate)
        spotPrice = curr1.Calculation().MarketPrice(space,
                                                    valuationDate,
                                                    0,
                                                    curr2).Value().Number()

        yc1 = curr1.Calculation().HistoricalDiscountCurve(space, valuationDate, True)
        yc2 = curr2.Calculation().HistoricalDiscountCurve(space, valuationDate, True)

        df1 = yc1.Discount(spotDate, valuationDate)
        df2 = yc2.Discount(spotDate, valuationDate)
        df3 = df2 / df1

        if curr1.Name() != fromCurrency.Name():
            try:
                discountedHistoricalSpotRate = spotPrice * df3
                return denominatedvalue(value / discountedHistoricalSpotRate, toCurrency, '', '')
            except Exception:
                LOGGER.LOG('%s: Error converting to ZAR.' % valuationDate)
                return denominatedvalue(0, toCurrency, '', '')
        else:
            try:
                discountedHistoricalSpotRate = spotPrice / df3
                return denominatedvalue(value * discountedHistoricalSpotRate, toCurrency, '', '')
            except Exception:
                LOGGER.LOG('%s: Error converting to ZAR. Check that rate != 0' % valuationDate)
                return denominatedvalue(0, toCurrency, '', '')


def get_additional_info(spec, record):
    ai = acm.FAdditionalInfo.Select('addInf="%s" and recaddr=%i' % (spec.Oid(), record.Oid()))
    if len(ai) == 1:
        return ai.First()
    return None


def save_additional_info(spec, record, value):
    ai = get_additional_info(spec, record)
    if not ai:
        ai = acm.FAdditionalInfo()
        ai.Recaddr(record.Oid())
        ai.AddInf(spec)
    ai.FieldValue(value)
    ai.Commit()


def get_allocated_percent(external_oid):
    portfolio = HedgeConstants.STR_CHILD_TRADE_PORTFOLIO
    query = "portfolio = '%s' and trxTrade = %i" % (portfolio, external_oid)

    trades = acm.FTrade.Select(query)
    utilisation_percent = 0.00
    for trade in trades:
        deal_package = trade.DealPackage()
        if not deal_package:
            continue
        hedge_relationship = get_hedge_from_dealpackage(deal_package)
        if (not hedge_relationship) or \
           (hedge_relationship.get_status() == HedgeConstants.Hedge_Relation_Status.DeDesignated):
            continue
        hedge_trades = hedge_relationship.get_trades()
        _, percent, _ = hedge_trades[str(external_oid)]
        utilisation_percent += float(percent)
    return utilisation_percent


def get_exclusive_alocated_percent(external_oid, requesting_hedge_relationship):
    portfolio = HedgeConstants.STR_CHILD_TRADE_PORTFOLIO
    query = "portfolio = '%s' and trxTrade = %i" % (portfolio, external_oid)

    HRs_with_trades = []
    trades = acm.FTrade.Select(query)
    utilisation_percent = 0.00

    for trade in trades:
        deal_package = trade.DealPackage()
        hedge_relationship = get_hedge_from_dealpackage(deal_package)
        if (not hedge_relationship) or\
           (hedge_relationship.get_file_name() == requesting_hedge_relationship.get_file_name()) or\
           (hedge_relationship.get_status() == HedgeConstants.Hedge_Relation_Status.DeDesignated):
            continue
        hedge_trades = hedge_relationship.get_trades()
        _, percent, _ = hedge_trades[str(external_oid)]
        utilisation_percent += float(percent)
        HRs_with_trades.append(hedge_relationship.get_file_name())
    return utilisation_percent, HRs_with_trades


def get_spread(start_date, base_curve_name, attr_curve_name):
    # Check if start_date is not today and add the date extension to pull historic curve
    date_extension = ''
    if start_date != acm.Time().DateNow():
        date = datetime.strptime(start_date, '%Y-%m-%d')
        date_extension = datetime.strftime(date, '_%Y-%m-%d')

    # Get Curves
    base_curve = acm.FYieldCurve[base_curve_name + date_extension]
    attr_curve = acm.FYieldCurve[attr_curve_name + date_extension]

    # Check if the curves exist
    if not base_curve:
        return -99999999998
    if not attr_curve:
        return -99999999999

    # Get 1d simple act/365 rate from both curves
    end_date = acm.Time.DateAddDelta(start_date, 0, 0, 1)
    base_curve_rate = base_curve.Rate(start_date, end_date, 2, 2)  # Annual Comp, Act/365
    attr_curve_rate = attr_curve.Rate(start_date, end_date, 2, 2)  # Annual Comp, Act/365

    # Return calculated value
    return attr_curve_rate - base_curve_rate


def get_test_dates(deal_package_name):
    deal_package = acm.FDealPackage[deal_package_name]
    if not deal_package:
        return None
    time_series_array = get_dealpackage_time_series_array(deal_package.Oid(),
                                                          get_time_series_spec_id())
    date_set = set()
    for time_series in time_series_array:
        date_set.add(time_series.StorageDate())
    date_list = []
    for date in date_set:
        date_list.append(date)
    return sorted(date_list)


def get_hedge_from_dealpackage(deal_package):
    if not deal_package:
        return None
    name = deal_package.OptionalId()
    index = name.split('/')
    if len(index) > 1:
        deal_package_name = '/'.join(index[0:2])  # Assumes dpname "HR/xxxxx/x" & hrname "HR/xxxxx"
    else:
        deal_package_name = name
    hedge_relationship = HedgeRelation.HedgeRelation(deal_package_name)
    found = hedge_relationship.read()
    if not found:
        return None
    return hedge_relationship


def get_text_object_from_dealpackage(deal_package):
    if not deal_package:
        return None
    name = deal_package.OptionalId()
    index = name.split('/')
    if len(index) > 1:
        deal_package_name = '/'.join(index[0:2])  # Assumes dpname "HR/xxxxx/x" & hrname "HR/xxxxx"
    else:
        deal_package_name = name
    return HedgeAccountingStorage.TextObjectManager.get_acm_textobject(deal_package_name,
                                                                       'Customizable')


def get_result_string_from_value(result_value):
    if not isinstance(result_value, int):
        return ''
    if result_value == 1:
        return 'Pass'
    if result_value == 0:
        return 'Fail'
    if result_value == 2:
        return 'Warning'
    return ''


def get_result_value_from_string(result_string):
    if not isinstance(result_string, (str,)):
        return -1
    if result_string == 'Pass':
        return 1
    if result_string == 'Fail':
        return 0
    if result_string == 'Warning':
        return 2
    if result_string == '':
        return -1
    return -1


def get_time_series_dv(recAdd1, specId, recAdd2):
    query = 'timeSeriesDvSpecification = %s and recordAddress1 = %s and recordAddress2 = %s' % \
        (int(specId), int(recAdd1), int(recAdd2))
    timeSeries = acm.FTimeSeriesDv.Select(query)
    return timeSeries


def get_time_series_dv_date(recAdd1, specId, recAdd2, date):
    query = "timeSeriesDvSpecification = %s and recordAddress1 = %s and " % (specId, recAdd1) + \
        "recordAddress2 = %s and storageDate = '%s'" % (recAdd2, date)
    timeSeries = acm.FTimeSeriesDv.Select(query)
    return timeSeries


def get_dealpackage_time_series_array(recAdd1, specId):
    query = 'timeSeriesDvSpecification = %s and recordAddress1 = %s' % (specId, recAdd1)
    timeSeries = acm.FTimeSeriesDv.Select(query)
    return timeSeries


def get_time_series_dv_value(recAdd1, specId, recAdd2):
    timeSeries = get_time_series_dv(recAdd1, specId, recAdd2)
    result = get_tsdv_value_from_TS(timeSeries)
    return result


def get_time_series_dv_value_date(recAdd1, specId, recAdd2, date):
    timeSeries = get_time_series_dv_date(recAdd1, specId, recAdd2, date)
    return get_tsdv_value_from_TS(timeSeries)


def get_time_series_dv_value_from_dp(dealPackage, specId, recAdd2):
    return get_time_series_dv_value(dealPackage.Oid(), specId, recAdd2)


def get_tsdv_value_from_TS(timeSeries):
    if not timeSeries:
        return
    timeSeries = timeSeries.SortByProperty('StorageDate')
    return timeSeries.Last().DvValue()


def get_tsdv_curr_from_TS(timeSeries):
    if not timeSeries:
        return
    timeSeries = timeSeries.SortByProperty('StorageDate')
    return timeSeries.Last().DvCurrency()


def get_tsdv_date_from_TS(timeSeries):
    if not timeSeries:
        return
    timeSeries = timeSeries.SortByProperty('StorageDate')
    return timeSeries.Last().DvDate()


def get_time_series_spec_id():
    return acm.FTimeSeriesDvSpec[HedgeConstants.STR_TIMESERIESSPECNAME].Oid()


def get_ts_time_series_spec_id():
    return acm.FTimeSeriesDvSpec[HedgeConstants.STR_TSTIMESERIESSPECNAME].Oid()


def get_point_ids(baseString):
    m_list = []
    for cnt in range(1, 40):
        chl = acm.FChoiceList[baseString + '%02d' % cnt]
        if chl:
            m_list.append(chl.Oid())
    return m_list


def get_overall_result_id():
    return acm.FChoiceList[HedgeConstants.STR_OVERALLRESULT].Oid()  # MS


def get_pro_cv_value_id():
    return acm.FChoiceList[HedgeConstants.STR_PROCVVALUENAME].Oid()


def get_pro_cv_result_id():
    return acm.FChoiceList[HedgeConstants.STR_PROCVRESULTNAME].Oid()


def get_pro_do_value_id():
    return acm.FChoiceList[HedgeConstants.STR_PRODOVALUENAME].Oid()


def get_pro_do_result_id():
    return acm.FChoiceList[HedgeConstants.STR_PRODORESULTNAME].Oid()


def get_pro_reg_value_id():
    return acm.FChoiceList[HedgeConstants.STR_PROREGVALUENAME].Oid()


def get_pro_reg_alpha_id():
    return acm.FChoiceList[HedgeConstants.STR_PROREGALPHA].Oid()


def get_pro_reg_beta_id():
    return acm.FChoiceList[HedgeConstants.STR_PROREGBETA].Oid()


def get_pro_reg_corr_id():
    return acm.FChoiceList[HedgeConstants.STR_PROREGCORRELATION].Oid()


def get_pro_reg_r2_id():
    return acm.FChoiceList[HedgeConstants.STR_PROREGR2].Oid()


def get_pro_reg_pvalue_id():  # F Statistic
    return acm.FChoiceList[HedgeConstants.STR_PROREGPVALUE].Oid()


def get_pro_vrm_value_id():
    return acm.FChoiceList[HedgeConstants.STR_PROVRMVALUENAME].Oid()


def get_pro_vrm_result_id():
    return acm.FChoiceList[HedgeConstants.STR_PROVRMRESULTNAME].Oid()


def get_pro_vrm_par_coupon_id():
    return acm.FChoiceList[HedgeConstants.STR_PROVRMPARCOUPONNAME].Oid()


def get_pro_reg_result_id():
    return acm.FChoiceList[HedgeConstants.STR_PROREGRESULTNAME].Oid()


def get_ret_do_value_id():
    return acm.FChoiceList[HedgeConstants.STR_RETDOVALUENAME].Oid()


def get_ret_do_result_id():
    return acm.FChoiceList[HedgeConstants.STR_RETDORESULTNAME].Oid()


def get_ret_vrm_value_id():
    return acm.FChoiceList[HedgeConstants.STR_RETVRMVALUENAME].Oid()


def get_ret_vrm_result_id():
    return acm.FChoiceList[HedgeConstants.STR_RETVRMRESULTNAME].Oid()


def get_ret_vrm_par_coupon_id():
    return acm.FChoiceList[HedgeConstants.STR_RETVRMPARCOUPONNAME].Oid()


def get_value_for_calculation(calcSpace, trade, column_id):
    calculation = calcSpace.CreateCalculation(trade, column_id)
    try:
        return calculation.Value().Number()
    except:
        try:
            return calculation.Value()
        except:
            return None


def get_hedge_types():
    query = "list = '%s'" % HedgeConstants.STR_HEDGE_TYPES
    choice_lists = acm.FChoiceList.Select(query)
    hedge_types = []
    for choice_list_item in choice_lists.SortByProperty('Name'):
        hedge_types.append(choice_list_item)
    return hedge_types


def get_hedge_sub_types():
    query = "list = '%s'" % HedgeConstants.STR_HEDGE_SUB_TYPES
    choice_lists = acm.FChoiceList.Select(query)
    hedge_types = []
    for choice_list_item in choice_lists.SortByProperty('Name'):
        hedge_types.append(choice_list_item)
    return hedge_types


def get_risk_types():
    query = "list = '%s'" % HedgeConstants.STR_HEDGE_RISK_TYPES
    choice_lists = acm.FChoiceList.Select(query)
    hedge_types = []
    for choice_list_item in choice_lists.SortByProperty('Name'):
        hedge_types.append(choice_list_item)
    return hedge_types


def openApplication(eii):
    selection = eii.ExtensionObject().ActiveSheet().Selection()
    selected_rows = selection.SelectedRowObjects()
    deal_package_found = False
    item = selected_rows[0]
    deal_package = None
    while not deal_package_found:
        try:
            deal_package = item.Trade().DealPackage()
            deal_package_found = True
        except:
            try:
                item = item.Children().First()
            except:
                return
    text_object = get_text_object_from_dealpackage(deal_package)
    if text_object:
        acm.StartApplication('Hedge Effectiveness Test Suite', text_object)
