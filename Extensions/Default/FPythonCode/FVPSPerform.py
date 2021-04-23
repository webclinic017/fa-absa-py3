""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FVPSPerform - Called from FVPSDelete and FVPSExecute

DESCRIPTION
    Main module for deleting valuation parameters. Reload the module
    to execute the storage procedure.


----------------------------------------------------------------------------"""


import collections


import ael


import FBDPCommon
import FVPSYieldCurve
import FVPSVolatility
import FVPSCorrelationMatrix
import FVPSDividendStream


# Used to shuffle arguments into FVPSx-modules
class Params(object):
    pass


_DateExcludeParam = collections.namedtuple('_DateExcludeParam',
        'foy foq fom fow')


def _isDateExcluded(world, aelCal, aelDate, dateExcludeParam):
    """
    Given the date and calendar, check if the date is excluded as dictated by
    the dateExcludeParam. Dates excluded are:
    * Any date before 1999-01-01
    * First banking day of the year (if selected to be excluded)
    * First banking day of the quarter (if selected to be excluded)
    * First banking day of the month (if selected to be excluded)
    * First banking day of the week (if selected to be excluded)
    """
    aelOldDate = ael.date('1999-01-01')
    if aelDate.days_between(aelOldDate) > 0:
        world.logDebug('    Exclude date {0} (reason: before '
                '1999-01-01)'.format(aelDate.to_string()))
        return True
    if dateExcludeParam.foy:
        foyDate = aelDate.first_day_of_year().adjust_to_banking_day(aelCal)
        if foyDate == aelDate:
            world.logDebug('    Exclude date {0} (reason: first banking day '
                    'of the year)'.format(aelDate.to_string()))
            return True
    if dateExcludeParam.foq:
        foqDate = aelDate.first_day_of_quarter().adjust_to_banking_day(aelCal)
        if foqDate == aelDate:
            world.logDebug('    Exclude date {0} (reason: first banking day '
                    'of the quarter)'.format(aelDate.to_string()))
            return True
    if dateExcludeParam.fom:
        fomDate = aelDate.first_day_of_month().adjust_to_banking_day(aelCal)
        if fomDate == aelDate:
            world.logDebug('    Exclude date {0} (reason: first banking day '
                    'of the month)'.format(aelDate.to_string()))
            return True
    if dateExcludeParam.fow:
        fowDate = aelDate.first_day_of_week().adjust_to_banking_day(aelCal)
        if fowDate == aelDate:
            world.logDebug('    Exclude date {0} (reason: first banking day '
                    'of the week)'.format(aelDate.to_string()))
            return True
    return False


def _splitPeriodToDelete(world, aelCal, aelStartDate, aelEndDate,
        dateExcludeParam, excludeDate=_isDateExcluded):
    """
    Given a period specified between the start date (inclusive) and end date
    (inclusive) and a calendar, split the period up if the following dates are
    selected to be excluded in the dateExcludeParam.
    * First banking day of the year
    * First banking day of the quarter
    * First banking day of the month
    * First banking day of the week
    """
    splittedPeriods = []
    world.logDebug('    Splitting period [{0}, {1}]'.format(
            aelStartDate.to_string(), aelEndDate.to_string()))
    periodFirstDay = aelStartDate
    periodLastDay = None
    d = aelStartDate
    isNewlySplittedPeriod = not excludeDate(world, aelCal, d,
            dateExcludeParam)
    while d.days_between(aelEndDate) >= 0:
        periodLastDay = d
        d = d.add_days(1)
        if excludeDate(world, aelCal, d, dateExcludeParam):
            if isNewlySplittedPeriod:
                if periodLastDay > periodFirstDay:
                    splittedPeriods.append((periodFirstDay, periodLastDay))
                isNewlySplittedPeriod = False
        else:
            if not isNewlySplittedPeriod:
                periodFirstDay = d
                isNewlySplittedPeriod = True
    if isNewlySplittedPeriod:
        if aelEndDate > periodFirstDay:
                splittedPeriods.append((periodFirstDay, aelEndDate))
    return splittedPeriods


def _calculateDatesAndPeriodsToDelete(world, isPeriod, aelCal, aelStartDate,
        aelEndDate, aelDate, dateExcludeParam):

    datesToDelete = []
    periodsToDelete = []
    if isPeriod:
        world.logInfo('Finding dates.')
        d = aelStartDate
        while d.days_between(aelEndDate) >= 0:
            if not _isDateExcluded(world, aelCal, d, dateExcludeParam):
                datesToDelete.append(d)
            d = d.add_days(1)
        world.logInfo('Found {0} dates'.format(len(datesToDelete)))
        world.logInfo('Finding periods.')
        if (not dateExcludeParam.foy and not dateExcludeParam.foq and
                not dateExcludeParam.fom and not dateExcludeParam.fow):
            world.logDebug('    No date to exclude.')
            periodsToDelete.append([aelStartDate, aelEndDate])
        else:
            periodsToDelete = _splitPeriodToDelete(world, aelCal, aelStartDate,
                    aelEndDate, dateExcludeParam)
        world.logInfo('Found {0} periods'.format(len(periodsToDelete)))
    else:
        world.logInfo('Finding dates.')
        if not _isDateExcluded(world, aelCal, aelDate, dateExcludeParam):
            datesToDelete.append(aelDate)
        world.logInfo('Found {0} dates'.format(len(datesToDelete)))
    return datesToDelete, periodsToDelete


def _getSingleDate(dt, keep):
    if dt in keep:
        return []
    return [dt]


def _getDeleteDates(start, end, keep, log):
    """
    Generate list of dates and periods to delete between start and end dates,
    excluding dates to keep.
    """
    log.logInfo('Getting dates.')
    diff = start.days_between(end)
    datesBetween = [start.add_days(i) for i in range(diff + 1)]
    assert datesBetween[-1] == end, "Off by 1: {0} != {1}".format(end,
            datesBetween[-1])
    deleteDates = []
    for d in datesBetween:
        if d not in keep:
            deleteDates.append(d)
    log.logInfo('Found {0} dates'.format(len(deleteDates)))

    log.logInfo('Getting periods.')
    periods = _splitPeriodToDelete(log, keep, start, end, None,
            excludeDate=lambda x, keep, dt, y: dt in keep)
    log.logInfo('Found {0} periods'.format(len(periods)))

    return deleteDates, periods


def perform_vps_delete(world, execParam):

    p = Params()

    _filterParamFilters(world, execParam, 'delete')
    p.yield_curve_base = execParam.get('yield_curve_base') == 1
    p.yield_curves_incl = execParam.get('yield_curves_incl')
    p.yield_curves_excl = execParam.get('yield_curves_excl')
    p.volatility_base = execParam.get('volatility_base') == 1
    p.volatilities_incl = execParam.get('volatilities_incl')
    p.volatilities_excl = execParam.get('volatilities_excl')
    p.corr_matrices_base = execParam.get('corr_matrices_base') == 1
    p.corr_matrices_incl = execParam.get('corr_matrices_incl')
    p.corr_matrices_excl = execParam.get('corr_matrices_excl')
    p.dividend_streams_base = execParam.get('dividend_streams_base') == 1
    p.dividend_streams_incl = execParam.get('dividend_streams_incl')
    p.dividend_streams_excl = execParam.get('dividend_streams_excl')
    # Find the calendar
    calName = execParam.get('calendar')
    aelCal = ael.Calendar[calName]
    assert aelCal, 'No calendar \'{0}\' found.'.format(aelCal)
    # Find the dates
    aelStartDate = None
    aelEndDate = None
    aelDate = None
    isPeriod = execParam.get('day_or_period') == 'Period'
    if isPeriod:
        strStartDate = execParam.get('start_date')
        strEndDate = execParam.get('end_date')
        aelStartDate = FBDPCommon.toDateAEL(strStartDate, aelCal)
        aelEndDate = FBDPCommon.toDateAEL(strEndDate, aelCal)
        assert aelStartDate, ('\'{0}\' is not a proper start date.'.format(
                strStartDate))
        assert aelEndDate, ('\'{0}\' is not a proper start date.'.format(
                strEndDate))
        assert aelStartDate.days_between(aelEndDate) >= 0, ('Start date '
                '\'{0}\' must be on or before end date {1}'.format(
                strStartDate, strEndDate))
    else:
        strDate = execParam.get('date')
        aelDate = FBDPCommon.toDateAEL(strDate, aelCal)
        assert aelDate, '\'{0}\' is not a proper date.'.format(strDate)

    datesToDelete = []
    periodsToDelete = []
    buckets = execParam.get('timeBuckets', None)
    if buckets:
        keep = [ael.date(tb.BucketDate()) for tb in buckets[0].TimeBuckets()]
        if isPeriod:
            datesToDelete, periodsToDelete = _getDeleteDates(aelStartDate,
                    aelEndDate, keep, world)
        else:
            assert aelDate, "Must specify date if not using periods."
            datesToDelete = _getSingleDate(aelDate, keep)
            world.logInfo("Found {0} date(s)".format(len(datesToDelete)))
    else:
        # Default keep dates in the old GUI, for backwards compatibility, were
        # first of year, quarter, month.
        dateExcludeParam = _DateExcludeParam(
                foy=bool(execParam.get('first_of_year', 1)),
                foq=bool(execParam.get('first_of_quarter', 1)),
                fom=bool(execParam.get('first_of_month', 1)),
                fow=bool(execParam.get('first_of_week', 0)))
        # Generate dates and periods to delete
        datesToDelete, periodsToDelete = _calculateDatesAndPeriodsToDelete(
                world, isPeriod, aelCal, aelStartDate, aelEndDate, aelDate,
                dateExcludeParam)

    # Yield curves
    if (p.yield_curve_base or p.yield_curves_incl):
        world.logInfo('[VPS Delete - Yield Curves]')
        for aelDelDate in datesToDelete:
            FVPSYieldCurve.delete_all_yc_of_a_day(world, aelDelDate, p)
    # Volatilities
    if (p.volatility_base or p.volatilities_incl):
        world.logInfo('[VPS Delete - Volatilities]')
        for aelDelDate in datesToDelete:
            FVPSVolatility.delete_all_vol_of_a_day(world, aelDelDate, p)
    # Correlation matrices
    if (p.corr_matrices_base or p.corr_matrices_incl):
        world.logInfo('[VPS Delete - Correlation Matrices]')
        for (aelPeriodFirstDay, aelPeriodLastDay) in periodsToDelete:
            FVPSCorrelationMatrix.delete_all_cm_in_period(world,
                    aelPeriodFirstDay, aelPeriodLastDay, p)
    # Dividend streams
    if (p.dividend_streams_base or p.dividend_streams_incl):
        world.logInfo('[VPS Delete - Dividend Streams]')
        for (aelPeriodFirstDay, aelPeriodLastDay) in periodsToDelete:
            FVPSDividendStream.delete_all_ds_in_period(world,
                    aelPeriodFirstDay, aelPeriodLastDay, p)


def perform_vps_execute(world, execParam):

    p = Params()

    _filterParamFilters(world, execParam, 'execute')
    p.yield_curve_base = execParam.get('yield_curve_base') == 1
    p.yield_curves_incl = execParam.get('yield_curves_incl')
    p.yield_curves_excl = execParam.get('yield_curves_excl')
    p.volatility_base = execParam.get('volatility_base') == 1
    p.volatilities_incl = execParam.get('volatilities_incl')
    p.volatilities_excl = execParam.get('volatilities_excl')
    p.correlation_base = execParam.get('correlation_base') == 1
    p.correlations_incl = execParam.get('correlations_incl')
    p.correlations_excl = execParam.get('correlations_excl')
    p.stream_base = execParam.get('stream_base') == 1
    p.streams_incl = execParam.get('stream_incl')
    p.streams_excl = execParam.get('stream_excl')
    p.calculate = execParam.get('calculate') == 1
    p.iso_date = execParam.get('iso_date', 0)
    p.yc_realtimeupdatedunchanged = execParam.get(
        'RealTimeUpdatedUnchanged') == 1

    date = str(ael.date_today())
    if p.iso_date:
        date = ael.date(date).to_string(ael.DATE_ISO)

    # Yield curves
    if (p.yield_curve_base or p.yield_curves_incl):
        world.logInfo('[VPS Execute - Yield Curves]')
        FVPSYieldCurve.update_all_yield_curves(world, p, date)
    # Volatilities
    if (p.volatility_base or p.volatilities_incl):
        world.logInfo('[VPS Execute - Volatilities]')
        FVPSVolatility.update_all_vol(world, p, date)
    # Correlation matrices
    if (p.correlation_base or p.correlations_incl):
        world.logInfo('[VPS Execute - Correlation Matrices]')
        FVPSCorrelationMatrix.update_all_cm(world, p, date)
    # Dividend streams
    if (p.stream_base or p.streams_incl):
        world.logInfo('[VPS Execute - Dividend Streams]')
        FVPSDividendStream.update_all_ds(world, p, date)

def _filterParamFilters(world, execParam, op):
    missing = []
    for key, values in execParam.items():
        if key.endswith('_excl') or key.endswith('_incl'):
            values = values or []
            filtered_values = []
            for value in values:
                if not value:
                    continue

                if not isinstance(value, str):
                    value = value.Name()

                filtered_values.append(value)

            if len(filtered_values) != len(values):
                missing.append(key)

            execParam[key] = filtered_values

    if missing:
        world.logWarning((
            '[VPS %s - Some entities missing from the following filters: %s]'
            % (op.lower().capitalize(), ', '.join(sorted(missing)))))

    return
