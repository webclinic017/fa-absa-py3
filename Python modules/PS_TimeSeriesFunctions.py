'''----------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)


History:
Date       CR Number Who                    What

2011-06-17 685737    Herman Hoon            Amended GetMarginRequirement function to use the time series name as parameter.
2012-12-11 620455    Peter Fabian           Added function UpdateTimeSeriesValueForce
2013-02-18 C809119   Peter Kutnik           Updates for Voice fees on Equities
2014-11-20 C2450799  Peter Fabian           Fixing errors and exception handling
----------------------------------------------------------------------'''
import acm

import at_logging
LOGGER = at_logging.getLogger()

''' Values like the short overnight funding rate and execution premium are stored on additional-infos on the portfolio swap or
    underlying portfolio.  These additional-infos are subject to change over time so a history is stored in a time series. The 
    time series will only store the values when the additional-info changes.  

    This module contains functions to create, update and retrieve values from these time-series.
'''

def GetTimeSeries(timeSeriesName, entity):
    ''' Return the time-series spec of a given time-series mapped to the given entity.
    '''
    timeSeriesSpec = acm.FTimeSeriesSpec[timeSeriesName]
    if timeSeriesSpec:
        timeSeries = acm.FTimeSeries.Select('recaddr=%i and timeSeriesSpec=%i' % (entity.Oid(), timeSeriesSpec.Oid()))
        return timeSeries
    else:
        return None

def GetTimeSeriesPoint(timeSeries, date):
    ''' Get the latest point from the timeSeries with day less than or equal to the given date.
    '''

    # The list is scanned through in reverse order (by day) as we're more likely to need more recent values.
    timeSeriesData = sorted(timeSeries, key=lambda value: value.Day(), reverse=True)
    for point in timeSeriesData:
        if date >= point.Day():
            return point
    return point

def GetTimeSeriesValue(addInfoName, timeSeriesName, entity, date):
    ''' If the date is in the past then the value is read off the mapped time-series.  If there 
        are no historical values or the value is todays value then the current additional-info
        value is used.
        
        If the lookup date is before the earliest time-series entry then the earliest entry is
        returned.
    '''
    value = entity.add_info(addInfoName)
    if value:
        value = float(value)
    else:
        value = 0.0

    if date < acm.Time().DateToday():
        timeSeries = GetTimeSeries(timeSeriesName, entity)
        if timeSeries:
            timeSeriesPoint = GetTimeSeriesPoint(timeSeries, date)
            if timeSeriesPoint:
                # Front Upgrade 2013.3 -- amended Value() to TimeValue(), it changed semantics between versions
                value = timeSeriesPoint.TimeValue()
    return value

def SetTimeSeriesValue(timeSeriesName, entity, value, date):
    ''' Create a new time-series entry.
    '''
    timeSeriesSpec = acm.FTimeSeriesSpec[timeSeriesName]
    if timeSeriesSpec:

        timeSeries = acm.FTimeSeries()
        timeSeries.Day(date)
        timeSeries.TimeSeriesSpec(timeSeriesSpec)
        # Front Upgrade 2013.3 -- Value() to TimeValue()
        timeSeries.TimeValue(value)
        timeSeries.Recaddr(entity.Oid())
        try:
            timeSeries.Commit()
        except Exception, err:
            LOGGER.exception('ERROR: Timeseries %s not commited: %s' % (timeSeriesName, err))
            raise
    else:
        print(timeSeriesName + ' has not been defined.')

def UpdateTimeSeriesValue(timeSeriesName, entity, value, date):
    ''' Update the time-series with the additional-info value. A new entry 
        is only added to the time-series if the value has changed since 
        the previous time-series entry.
    '''
    if value:
        value = float(value)
        timeSeries = GetTimeSeries(timeSeriesName, entity)
        if timeSeries:
            timeSeriesPoint = GetTimeSeriesPoint(timeSeries, date)
            if timeSeriesPoint:
                # Front Upgrade 2013.3 -- Value() to TimeValue()
                pointValue = timeSeriesPoint.TimeValue()
                pointDay = timeSeriesPoint.Day()
                # If the time-series point exists for the date and has changed then update the existing entry.
                if abs(value - pointValue) > 0.00001 and pointDay == date:
                    # Front Upgrade 2013.3 -- Value() to TimeValue()
                    timeSeriesPoint.TimeValue(value)
                    try:
                        timeSeriesPoint.Commit()
                    except Exception as err:
                        LOGGER.exception('ERROR: Timeseries %s not commited: %s' % (timeSeriesName, err))
                        raise
                # If the time-series value has changed then insert a new point
                elif abs(value - pointValue) > 0.00001 and pointDay != date:
                    SetTimeSeriesValue(timeSeriesName, entity, value, date)
            else:
                SetTimeSeriesValue(timeSeriesName, entity, value, date)
        else:
            SetTimeSeriesValue(timeSeriesName, entity, value, date)

def UpdateTimeSeriesValueForce(timeSeriesName, entity, value, date):
    ''' Update the time-series for entity with specified value. 
        This function ignores the difference between the previous
        value and new value and can write 0 as value to the time series.
    '''
    try:
        value = float(value)
    except ValueError as e:
        LOGGER.exception("ERROR: Value {0} can't be converted to float".format(value))
        return
    timeSeries = GetTimeSeries(timeSeriesName, entity)
    if timeSeries:
        timeSeriesPoint = GetTimeSeriesPoint(timeSeries, date)
        if timeSeriesPoint:
            pointDay = timeSeriesPoint.Day()
            # If the time-series point exists for the date and has changed then update the existing entry.
            if pointDay == date:
                # Front Upgrade 2013.3 -- Value() to TimeValue()
                timeSeriesPoint.TimeValue(value)
                try:
                    timeSeriesPoint.Commit()
                except Exception, err:
                    LOGGER.exception('ERROR: Timeseries %s not commited: %s' % (timeSeriesName, err))
            # If the time-series value has changed then insert a new point
            else:
                SetTimeSeriesValue(timeSeriesName, entity, value, date)
        else:
            SetTimeSeriesValue(timeSeriesName, entity, value, date)
    else:
        SetTimeSeriesValue(timeSeriesName, entity, value, date)


def UpdateTimeSeries(addInfoName, timeSeriesName, entity, date):
    ''' Update the time-series with the additional-info value. A new entry 
        is only added to the time-series if the value has changed since 
        the previous time-series entry.
    '''
    value = entity.add_info(addInfoName)
    if value:
        value = float(value)
        timeSeries = GetTimeSeries(timeSeriesName, entity)
        if timeSeries:
            timeSeriesPoint = GetTimeSeriesPoint(timeSeries, date)
            if timeSeriesPoint:
                # Front Upgrade 2013.3 -- Value() to TimeValue()
                pointValue = timeSeriesPoint.TimeValue()
                pointDay = timeSeriesPoint.Day()
                # If the time-series point exists for the date and has changed then update the existing entry.
                if abs(value - pointValue) > 0.00001 and pointDay == date:
                    # Front Upgrade 2013.3 -- Value() to TimeValue()
                    timeSeriesPoint.TimeValue(value)
                    timeSeriesPoint.Commit()
                # If the time-series value has changed then insert a new point
                elif abs(value - pointValue) > 0.00001 and pointDay != date:
                    SetTimeSeriesValue(timeSeriesName, entity, value, date)
            else:
                SetTimeSeriesValue(timeSeriesName, entity, value, date)
        else:
            SetTimeSeriesValue(timeSeriesName, entity, value, date)

def GetShortPremiumRate(portfolioSwap, date):
    ''' Return the short rate for a given portfolio swap for a given date
    '''
    shortRate = GetTimeSeriesValue('PSShortPremRate', 'PSShortPremRate', portfolioSwap, date)
    return shortRate

def GetWarehousingRate(portfolio, date):
    ''' Return the warehousing rate for a given portfolio for a given date
    '''
    warehousingRate = GetTimeSeriesValue('PS_Warehousing', 'PS_Warehousing', portfolio, date)
    return warehousingRate

def GetExecutionPremiumRate(portfolio, date, executionType=None):
    ''' Return the execution premium for a given portfolioswap on a given date.
    '''
    if executionType and executionType == 'Non-DMA':
        executionPremium = GetTimeSeriesValue('PSExtExecPremNonDMA', 'PSExtExecPremNonDMA', portfolio, date)
    elif executionType and executionType == 'Voice':
        executionPremium = GetTimeSeriesValue('PSExtExecPremVoice', 'PSExtExecPremVoice', portfolio, date)
    else:
        executionPremium = GetTimeSeriesValue('PSExtExecPremRate', 'PSExtExecPremRate', portfolio, date)
    return executionPremium

def GetMarginRequirement(timeSeriesName, callAccount, date):
    ''' The margin requirement for the date is stored in a time-series attached to the portfolio swaps call-account.
        The time-series will store a value for each date, so does not implement logic to only update the value when
        the margin changes.
    '''
    timeSeries = GetTimeSeries(timeSeriesName, callAccount)
    if timeSeries:
        for point in timeSeries:
            if point.Day() == date:
                return point.TimeValue()
    return 0.0

def GetCollateral(timeSeriesName, callAccount, date):
    ''' The collateral for the date is stored in a time-series attached to the portfolio swaps call-account.
    '''
    timeSeries = GetTimeSeries(timeSeriesName, callAccount)
    if timeSeries:
        for point in timeSeries:
            if point.Day() == date:
                return point.TimeValue()
    return 0.0

def test1():
    from PS_Functions import DateGenerator
    portfolioSwap = acm.FInstrument['pjg/ps_test2']
    startDate = acm.Time().DateFromYMD(2010, 11, 10)
    endDate = acm.Time().DateFromYMD(2010, 11, 23)
    today = acm.Time().DateToday()
    # UpdateTimeSeries('PSShortPremRate', 'PSShortPremRate', portfolioSwap, startDate)
    for date in DateGenerator(startDate, endDate):
        print(date, GetShortPremiumRate(portfolioSwap, date))

    # print today, GetShortPremiumRate(portfolioSwap, today)

def test2():
    from PS_Functions import DateGenerator
    callAccount = acm.FInstrument['pjg/margin_account2']
    startDate = acm.Time().DateFromYMD(2010, 11, 10)
    endDate = acm.Time().DateFromYMD(2010, 11, 30)
    for date in DateGenerator(startDate, endDate):
        print(date, GetMarginRequirement(callAccount, date))

