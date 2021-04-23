""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_aggregation/FFxAggregation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FXAggregation - Perform aggregation

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)

ScriptName = "FxAggregation"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FxAggregation')

ttDeaggregate = "Open up the positions after the aggregation date."
ttDate = ('Specify the aggregation horizon date. Aggregation will be done up '
        'until and not including this date. If the date is today, '
        'aggregation will be done for all historical days.')
ttFilter = 'Specify the tradefilters that you want to process.'
ttGrouper = ('Specify a grouper template. If no grouper is selected, a '
        'default grouping of per portfolio will be used.')
ttMergeAggregate = ('Aggregate the trades including existing '
                    'aggregate trades into a single aggregate trade.')
ttForwardTrades = 'Include forward trades'
ttYearly = 'The number of yearly periods to retain.'
ttMonthly = 'The number of monthly periods to retain.'
ttDaily = 'The number of daily periods to retain.'
ttMaxTrades = ('The maximum number of trades per aggregate trade.')
ttmultiUpdates = ("Select this check box to perform batch updating "
    "while archiving/de-archiving trades. FValidation and FBDPHook will "
    "not be called. This will reduce the aggregation processing time.")

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
        ['mergeAggTrades',
                'Merge Aggregate Trades',
                'int', [0, 1], 0,
                0, 0, ttMergeAggregate],
        ['date',
                'Aggregation Date',
                'string', agg_days, 'Today',
                1, 0, ttDate],
        ['multiUpdates',
                'Use batch updates',
                'int', [1, 0], 0,
                0, 0, ttmultiUpdates, None, None],
        ['includeForwardTrades',
                'Include Forward Trades_Periodic',
                'int', [0, 1], 0,
                0, 0, ttForwardTrades],
        ['years',
                'Number of yearly aggregates_Periodic',
                'int', [0, 1, 2, 3, 4], 0,
                0, 0, ttYearly],
        ['months',
                'Number of monthly aggregates_Periodic',
                'int', [0, 1, 2, 3, 4], 0,
                0, 0, ttMonthly],
        ['days',
                'Number of daily aggregates_Periodic',
                'int', [0, 1, 2, 3, 4], 0,
                0, 0, ttDaily],
        ['maxTrades',
                'Maximum number of trades per aggregate_Periodic',
                'int', [500, 1000, 10000, 50000, 100000], 100000,
                0, 0, ttMaxTrades],)


def ael_main(dictionary):
    #Import Front modules
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FFxCommon
    importlib.reload(FFxCommon)
    import FFxAggregatePerform
    importlib.reload(FFxAggregatePerform)
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
    FBDPCommon.execute_script(FFxAggregatePerform.perform_aggregation,
                              dictionary)
