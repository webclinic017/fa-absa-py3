""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/archive_trades/FCumulativeAggregation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCumulativeAggregation - Archive Trades while preserving P&L values

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)

ScriptName = "CumulativeAggregation"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FArchiveTrades')

ttDeaggregate = "Open up the positions after the aggregation date."
ttDate = ('Specify the aggregation horizon date. Aggregation will be done up '
        'until and not including this date. If the date is today, '
        'aggregation will be done for all historical days.')
ttFilter = 'Specify the tradefilters that you want to process.'
ttGrouper = ('Specify a grouper template. If no grouper is selected, a '
        'default grouping of per portfolio will be used.')
ttTradingCalendar = ('Trading location\'s calendar. Default is '
                'calendar of accounting currency.')


def archiveDearchive_cb(index, fieldValues):
    return fieldValues

agg_days = [acm.Time.DateToday(),
            'Today',
            'First of Month',
            'First of Quarter',
            'First of Year']

ael_variables = FBDPGui.FxAggregationVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['deaggregate',
                'Deaggregate',
                'int', [0, 1], 0,
                0, 0, ttDeaggregate, archiveDearchive_cb],
        ['calendar',
                'Trading location calendar',
                'FCalendar', None, None,
                0, 1, ttTradingCalendar],
        ['date',
                'Aggregation Date',
                'string', agg_days, 'Today',
                1, 0, ttDate],
        ['timeBuckets',
                'Time Bucket Grouper',
                'FStoredTimeBuckets', None, None,
                0, 1, '', None],)


def ael_main(dictionary):
    #Import Front modules
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FFxCommon
    importlib.reload(FFxCommon)
    import FCumulativeAggregationPerform
    importlib.reload(FCumulativeAggregationPerform)
    import FBDPCurrentContext

    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPGui.setPortfolioGrouper(dictionary)
    FBDPCommon.execute_script(FCumulativeAggregationPerform.perform_aggregation,
                              dictionary)
