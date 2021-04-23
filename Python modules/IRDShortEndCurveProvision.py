"""
-------------------------------------------------------------------------------
MODULE
    IRDShortEndCurveProvision

DESCRIPTION
    Date                : 2014-07-01
    Purpose             : Helper module for provision calculations
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002084118

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
05/08/2014  2036323     Jakub Tomaga    market_rate_instruments added for
                                        ShortEndDelta + ael date handling
02/10/2014  2325358     Jakub Tomaga    Support for price testing added.
21/10/2014  2374912     Jakub Tomaga    ASQL version of function fixed. 
-------------------------------------------------------------------------------
"""

import ael
import acm


def _get_default_instrument_list(currency_name):
    """List of instruments used for market rate calculation."""
    instrument_list = []
    if currency_name == 'ZAR':
        for k in range(1, 10):
            instrument_list.append(ael.Instrument['ZAR/FRA/JI/{0}X{1}'.format(
                k, k + 3)])
    elif currency_name == 'USD':
        for k in range(1, 10):
            instrument_list.append(ael.Instrument['USD/FRA/LI/{0}X{1}'.format(
                k, k + 3)])

    return instrument_list


class ProvisionError(Exception):
    """General provision error."""


def linear_interpolation(x, y, val):
    """Return linear interpolated value.

    Parameters:
        x - market dates (list)
        y - market rates (list)
        val - value to interpolate (reset date)

    """
    if  val <= x[0]:
        return y[0]

    for k in range(1, len(x)):
        if x[k] > val:
            n = x[k - 1].days_between(x[k]) * 1.0
            n1 = x[k - 1].days_between(val) * 1.0
            n2 = n - n1
            return n1 / n * y[k] + n2 / n * y[k - 1]

    return y[len(y) - 1]


def get_mpc_dates(currency):
    """Return dates of MPC events from time series for currency."""
    time_series_name = 'MO_MPC_{0}'.format(currency)
    time_series_spec = acm.FTimeSeriesSpec[time_series_name]
    if not time_series_spec:
        message = 'Unknown time series: {0}'.format(time_series_name)
        raise ProvisionError(message)

    date_list = []
    for ts in time_series_spec.TimeSeries():
        date_list.append(ts.Day())

    if not date_list:
        message = "ERROR: Data problem. Time series {0} has no dates.".format(
            time_series_name)
        raise ProvisionError(message)

    time = acm.Time()
    date_list.sort(lambda x, y: cmp(time.AsDate(x), time.AsDate(y)))
    return date_list


def get_mpc_dates_asql(params):
    """ASQL version of get_mpc_dates()."""
    try:
        currency = params[0][0]
    except Exception as ex:
        message = 'Error while parsing input parameters: {0}'.format(ex)
        raise ProvisionError(message)

    return get_mpc_dates(currency)


def get_future_mpc_dates(date, currency):
    """Return future dates of MPC events from time series for currency."""
    time_series_name = 'MO_MPC_{0}'.format(currency)
    time_series_spec = acm.FTimeSeriesSpec[time_series_name]
    if not time_series_spec:
        message = 'Unknown time series: {0}'.format(time_series_name)
        raise ProvisionError(message)

    date_list = []
    time = acm.Time()
    for ts in time_series_spec.TimeSeries():
        if time.AsDate(ts.Day()) > time.AsDate(date):
            date_list.append(ts.Day())

    if not date_list:
        message = "ERROR: Data problem. Time series {0} has no future dates."
        raise ProvisionError(message)

    date_list.sort(lambda x, y: cmp(time.AsDate(x), time.AsDate(y)))
    return date_list


def get_future_mpc_dates_asql(params):
    """ASQL version of get_future_mpc_dates()."""
    try:
        date = ael.date_from_string(params[0][0])
        currency = params[0][1]
    except Exception as ex:
        message = 'Error while parsing input parameters: {0}'.format(ex)
        raise ProvisionError(message)

    return get_future_mpc_dates(date, currency)


def get_next_mpc_date(date, currency):
    """Return date of next MPC event (after the give date)."""
    return get_future_mpc_dates(date, currency)[0]


def get_next_mpc_date_asql(params):
    """ASQL version of get_next_mpc_date()."""
    try:
        date = ael.date_from_string(params[0][0])
        currency = params[0][1]
    except Exception as ex:
        message = 'Error while parsing input parameters: {0}'.format(ex)
        raise ProvisionError(message)

    return get_next_mpc_date(date, currency)


def market_rate_asql(params):
    """ASQL version of market_rate()."""
    try:
        reset_date = ael.date_from_string(params[0][0])
        start_date = ael.date_from_string(params[0][1])
        currency = params[0][2]
    except Exception as ex:
        message = 'Error while parsing input parameters: {0}'.format(ex)
        raise ProvisionError(message)

    return market_rate(reset_date, start_date, currency, None)


def market_rate_zar_data(start_date, instrument_list):
    """Return ZAR market rate data without interpolation.

    Data can be used when final rates are interpolated over many  dates.
    In that case this data is calculated once and interpolated in the loop
    over the known set of dates.

    """
    currency = ael.Instrument['ZAR']

    mpc_list = get_future_mpc_dates(start_date, 'ZAR')

    market_date_list = []
    market_rate_list = []

    market_date_list.append(start_date)
    market_rate_list.append(ael.Instrument['ZAR-JIBAR-3M'].used_price())

    failed = []

    for k, instrument in enumerate(instrument_list):
        date = start_date.add_months(k + 1).adjust_to_banking_day(currency)
        rate = instrument.used_price()

        if mpc_list and date > ael.date(mpc_list[0]):
            mpc_date = ael.date(mpc_list[0])
            mpc_string = mpc_date.to_string('%b%y').upper()

            instrument_name = "ZAR/FRA/JI/PRE_{0}_MPC".format(mpc_string)
            try:
                pre_instrument = ael.Instrument[instrument_name]
                if pre_instrument:
                    market_rate_list.append(pre_instrument.used_price())
                    market_date_list.append(mpc_date)

            except Exception as ex:
                failed.append((instrument_name, ex))

            instrument_name = "ZAR/FRA/JI/POST_{0}_MPC".format(mpc_string)
            try:
                post_instrument = ael.Instrument[instrument_name]
                if post_instrument:
                    market_rate_list.append(post_instrument.used_price())
                    market_date_list.append(mpc_date.add_days(
                        1).adjust_to_banking_day(currency))
            except Exception as ex:
                failed.append((instrument_name, ex))
            del mpc_list[0]

        market_date_list.append(date)
        market_rate_list.append(rate)

    if failed:
        message = "Error occurred while calculating market rate."
        print(message)
        for (instrument_name, ex) in failed:
            print("{0}: {1}".format(instrument_name, ex))
        raise ProvisionError(message)

    return market_date_list, market_rate_list


def market_rate(reset_date, start_date, currency_name, instrument_list):
    """Return market rate based on currency.

    Function returns interpolated market rate needed for the short end
    provision calculation as performed by IRD desk.

    Rate is interpolated in the series of market rates:
        - 3M JIBAR
        - 1X4 through 9X12 FRA rates

    Parameters:
        - reset_date - value date for interpolated reset rate
        - start_date - report date
        - currency_name - currency for which market rate should be returned

    """

    if not instrument_list:
        instrument_list = _get_default_instrument_list(currency_name)

    market_date_list, market_rate_list = market_rate_data(start_date,
        currency_name, instrument_list)
    return linear_interpolation(market_date_list, market_rate_list, reset_date)


def market_rate_data(start_date, currency, instrument_list):
    """Return market rate data based on given currency."""
    if currency == 'ZAR':
        return market_rate_zar_data(start_date, instrument_list)
    elif currency == 'USD':
        return market_rate_usd_data(start_date, instrument_list)
    else:
        message = 'Unknown currency for market rate: {0}'.format(currency)
        raise ProvisionError(message)


def market_rate_usd_data(start_date, instrument_list):
    """Return USD market rate data without interpolation.

    Data can be used when final rates are interpolated over many  dates.
    In that case this data is calculated once and interpolated in the loop
    over the known set of dates.

    """
    currency = ael.Instrument['USD']
    mpc_list = get_future_mpc_dates(start_date, 'USD')

    market_date_list = []
    market_rate_list = []

    market_date_list.append(start_date)
    market_rate_list.append(ael.Instrument['USD-LIBOR-3M'].used_price())

    mpc_done = False
    for k, instrument in enumerate(instrument_list):
        date = start_date.add_months(k + 1).adjust_to_banking_day(currency)
        rate = instrument.used_price()

        mpc_date = mpc_list[0]
        if not mpc_done and date > mpc_date:
            market_date_list.append(mpc_date)
            market_rate_list.append(market_rate_list[-1])

            market_date_list.append(mpc_date.add_days(1))
            market_rate_list.append(rate)

            mpc_done = True

        market_date_list.append(date)
        market_rate_list.append(rate)

    return market_date_list, market_rate_list


def market_rate_instruments(start_date, currency_name):
    """Return list of instruments used in ShortEndDelta report."""
    instrument_list = []
    mpc_list = get_future_mpc_dates(start_date, currency_name)
    if currency_name == 'ZAR':
        instrument_list.append('ZAR-JIBAR-ON-DEP')
        instrument_list.append('ZAR-JIBAR-1M')
        instrument_list.append('ZAR-JIBAR-3M')

        currency = ael.Instrument[currency_name]
        for k in range(1, 10):
            date = start_date.add_months(k).adjust_to_banking_day(currency)
            if mpc_list and ael.date(date) > ael.date(mpc_list[0]):
                mpc_date = ael.date(mpc_list[0])
                mpc_string = mpc_date.to_string('%b%y').upper()
                instrument_list.append('ZAR/FRA/JI/PRE_{0}_MPC'.format(
                    mpc_string))
                instrument_list.append('ZAR/FRA/JI/POST_{0}_MPC'.format(
                    mpc_string))

                del mpc_list[0]

            instrument_list.append('ZAR/FRA/JI/{0}X{1}'.format(k, k + 3))
    elif currency_name == 'USD':
        instrument_list.append('USD-LIBOR-ON-DEP')
        instrument_list.append('USD-LIBOR-1M')
        instrument_list.append('USD-LIBOR-3M')

        currency = ael.Instrument[currency_name]
        for k in range(1, 10):
            instrument_list.append('USD/FRA/LI/{0}X{1}'.format(k, k + 3))

    return instrument_list
