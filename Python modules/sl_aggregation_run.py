"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Aggregates Security Loan Trades and Instruments
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  567248

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2010-04-22 378175    Francois Truter    Added automatic before and after P/L
                                        report comparison.
2010-08-05 389878    Francois Truter    Added option for WEEKLY aggregation
2011-02-04 567248    Francois Truter    Added LAST_FRIDAY_TWO_MONTHS_AGO
2011-11-25 ######    Paul Jacot-Guillarmod    Defined a new aggregation rule, so that we aggregate more frequently.
2012-11-08 587024    Peter Fabian        Added option for setting the aggregation date 10 business days ago
-----------------------------------------------------------------------------"""

import acm
import sl_aggregation
import FRunScriptGUI
from sl_aggregation_report_compare import SLAggregationComparisonReport
import string

nsTime = acm.Time()
calendar = acm.FCalendar['ZAR Johannesburg']

def _enumDayOfWeek(dayStr):
    if dayStr == 'Monday':
        return 1
    elif dayStr == 'Tuesday':
        return 2
    elif dayStr == 'Wednesday':
        return 3
    elif dayStr == 'Thursday':
        return 4
    elif dayStr == 'Friday':
        return 5
    elif dayStr == 'Saturday':
        return 6
    elif dayStr == 'Sunday':
        return 7
    else:
        raise Exception('Unknown day: %s' % dayStr)

def _tenDayAggregationRule(date):
    ''' Once ten business days have passed in the current month we aggregate up to the last day of the
        previous month, otherwise we aggregate up to the last day of the month, two months ago.
    '''
    lastDayOfPreviousMonth = _lastDayOfPreviousMonth(date)
    businessDaysPassedInMonth = calendar.BankingDaysBetween(lastDayOfPreviousMonth, date)
    if businessDaysPassedInMonth > 10:
        return lastDayOfPreviousMonth
    else:
        return _lastDayOfPreviousMonth(lastDayOfPreviousMonth)

def _previousFriday(date):
    days = _enumDayOfWeek('Friday') - _enumDayOfWeek(acm.Time().DayOfWeek(date))
    if days > 0:
        days -= 7
    return acm.Time().DateAddDelta(date, 0, 0, days)

def _lastDayOfPreviousMonth(date):
    return acm.Time().DateAddDelta(acm.Time().FirstDayOfMonth(date), 0, 0, -1)

def enableCustomAggregationDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == CUSTOM_DATE)
    return fieldValues

TODAY = acm.Time().DateNow()
CUSTOM_DATE = 'Custom Date'
END_OF_LAST_MONTH_STR = 'End of Last Month'
END_OF_LAST_MONTH_DATE = nsTime.DateAddDelta(nsTime.FirstDayOfMonth(nsTime.DateNow()), 0, 0, -1)
FRIDAY_TWO_WEEKS_AGO_STR = 'Friday 2 Weeks Ago'
FRIDAY_TWO_WEEKS_AGO_DATE = _previousFriday(acm.Time().DateAddDelta(TODAY, 0, 0, -14))
LAST_FRIDAY_TWO_MONTHS_AGO_STR = 'Last Friday 2 Months Ago'
LAST_FRIDAY_TWO_MONTHS_AGO_DATE = _previousFriday(_lastDayOfPreviousMonth(acm.Time().DateAddDelta(TODAY, 0, -1, 0)))
TEN_DAY_AGGREGATION_RULE_STR = 'Ten Day Aggregation Rule'
TEN_DAY_AGGREGATION_RULE = _tenDayAggregationRule(TODAY)
TEN_BUSINESS_DAYS_AGO_STR = "10 Business Days Ago"
TEN_BUSINESS_DAYS_AGO = calendar.AdjustBankingDays(TODAY, -10)

MONTHLY = 'Monthly'
WEEKLY = 'Weekly'

aggregateDateKey = 'AggregateDate'
customAggregateDateKey = 'CustomAggregateDate'
reportDirectoryKey = 'OutputDirectory'
aggregationPeriodKey = 'AggregationPeriod'
tradeFilterKey = 'TradeFilter'
reportTradeFilterKey = 'ReportTradeFilter'

AggregationDateDict = {CUSTOM_DATE: None,
                       END_OF_LAST_MONTH_STR: END_OF_LAST_MONTH_DATE,
                       FRIDAY_TWO_WEEKS_AGO_STR: FRIDAY_TWO_WEEKS_AGO_DATE,
                       LAST_FRIDAY_TWO_MONTHS_AGO_STR: LAST_FRIDAY_TWO_MONTHS_AGO_DATE,
                       TEN_DAY_AGGREGATION_RULE_STR: TEN_DAY_AGGREGATION_RULE,
                       TEN_BUSINESS_DAYS_AGO_STR: TEN_BUSINESS_DAYS_AGO,
                       }
AggregationDateDisplay = AggregationDateDict.keys()
AggregationDateDisplay.sort()

directorySelection=FRunScriptGUI.DirectorySelection()
defaultTradeFilter = acm.FTradeSelection['sl_swept_trades']
defaultReportTradeFilter = acm.FTradeSelection['sl_all_security_loans']

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [aggregateDateKey, 'Aggregation Date', 'string', AggregationDateDisplay, FRIDAY_TWO_WEEKS_AGO_STR, 1, 0, 'Trades expiring on or before this date will be aggregated.', enableCustomAggregationDate, 1],
    [customAggregateDateKey, 'Custom Aggregation Date', 'date', None, None, 0, 0, 'Date used when Custom Date is selected for Aggregation Date.', None, 0],
    [aggregationPeriodKey, 'Aggregation Period', 'string', [MONTHLY, WEEKLY], WEEKLY, 1, 0, 'How often should aggregate positions be created.', None, 1],
    [tradeFilterKey, 'Trade Filter', 'FTradeSelection', None, defaultTradeFilter, 1, 1, 'The Trade Filter that returns trades to be considered for aggregation.', None, 1],
    [reportDirectoryKey, 'Report Directory', directorySelection, None, directorySelection, 0, 1, 'The directory where the report(s) will be generated.', None, 1],
    [reportTradeFilterKey, 'Report Trade Filter', 'FTradeSelection', None, defaultReportTradeFilter, 1, 1, 'The Trade Filter used for the P/L report comparison.', None, 1]
]

def ael_main(parameters):
    aggregateDateStr = parameters[aggregateDateKey]
    if aggregateDateStr == CUSTOM_DATE:
        aggregateDate = parameters[customAggregateDateKey]
        if not nsTime.IsValidDateTime(aggregateDate):
            raise Exception('Please enter a valid date for Custom Aggregation Date.')
        else:
            aggregateDate = sl_aggregation.ToAcmDate(aggregateDate)
    elif aggregateDateStr in AggregationDateDict:
        aggregateDate = AggregationDateDict[aggregateDateStr]
    else:
        raise Exception('Unknown date: ' + aggregateDateStr)
        
    aggregationPeriodStr = parameters[aggregationPeriodKey]
    tradeFilter = parameters[tradeFilterKey][0]
    reportDirectory = parameters[reportDirectoryKey]
    reportTradeFilter = parameters[reportTradeFilterKey][0]
    
    if aggregationPeriodStr == 'Monthly':
        aggregationPeriod = sl_aggregation.PeriodType.Monthly
    elif aggregationPeriodStr == 'Weekly':
        aggregationPeriod = sl_aggregation.PeriodType.Weekly
    else:
        raise Exception('Unknown aggregation period: ' + aggregationPeriodStr)
    
    print 'Aggregating %(period)s positions of trade filter [%(tradeFilter)s] expiring on or before %(date)s' % \
        {'period': string.lower(aggregationPeriodStr), 'tradeFilter': tradeFilter.Name(), 'date': aggregateDate}
    report = SLAggregationComparisonReport(reportDirectory.SelectedDirectory().Text(), reportTradeFilter.Name())
    report.CreateReportBeforeAggregation()
    
    print 'Loading trades to be aggregated...'
    trades = tradeFilter.Trades()
    print '%i trades selected for aggregation' % len(trades)
    
    aggregator = sl_aggregation.AggregatorCollection(trades, aggregationPeriod, aggregateDate)
    aggregator.Aggregate()
    
    report.CreateReportAfterAggregation()
    report.Compare()
