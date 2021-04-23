""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FExportInstallation.py"
# Compiled: 2017-09-21 11:17:58 
from __future__ import print_function

#__src_file__ = "extensions/export/./etc/FExportInstallation.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExportInstallation - 
    This module provides methods to perform basic checks that an export integration
    is correctly set up 

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""
import acm

import FExportUtils
import FTransactionHistoryReader


def CheckTradeStatus():
    # Trade status 'FO Amend' must exist to monitor corrected trades
    customTradeStatus = 'FO Amend'
    try:
        if not acm.FEnumeration['enum(TradeStatus)'].Enumeration(customTradeStatus):
            raise RuntimeError('No enum!')
    except Exception as e:
        assert(False),  "Trade status '%s' does not exist: %s" % (customTradeStatus, e)

def CheckExportStateChart(exportStateChartName):
    # Create the export state chart, if required
    FExportUtils.CreateStandardExportStateChart(exportStateChartName)
    assert(acm.FStateChart[exportStateChartName]), \
        "State chart (%s) for export does not exist" % exportStateChartName
      
def CheckTransactionHistory(integrationId):
    # Check transaction history and subscription functionality is available.
    # This is not strictly required, so only log a warning on failure.
    try:
        subscriber = FTransactionHistoryReader.FTransactionHistorySubscriber(integrationId)
        subscription = subscriber.TransHistSubscription()
        if not subscription:
            print("WARNING: Subscription to transaction history does not exist")
    except Exception as e:
        print("WARNING: Failed to get transaction history subscription:", str(e))
        
def CheckTradeACMQuery(tradeACMQueryPrefix):
    # ACM queries should be setup to select trades to be exported
    queries = FExportUtils.TradeFilterQueriesForIntegration(tradeACMQueryPrefix) 
    assert(len(queries) > 0), \
        "No ACM queries have been defined for '%s', selecting exportable trades." % tradeACMQueryPrefix

def CheckTradingSheetTemplate(tradingSheetName):
    # Check if a trading sheet template has been created
    tradingSheet = acm.FTradingSheetTemplate[tradingSheetName]
    assert(tradingSheet), "Trading sheet template '%s' does not exist" % tradingSheetName

def CheckTradingSheetTemplatePerQuery(tradeACMQueryPrefix):
    # Each query must have a corresponding trading sheet template
    queries = FExportUtils.TradeFilterQueriesForIntegration(tradeACMQueryPrefix)
    for query in queries:
        tradingSheetName = acm.FTradingSheetTemplate[query.Name()]
        assert(tradingSheetName), "Couldn't find sheet template name for ACM query '%s'" % query.Name()
        tradingSheet = acm.FTradingSheetTemplate[tradingSheetName.Name()]
        assert(tradingSheet), "Trading sheet template '%s' (for ACM query '%s') does not exist" \
            % (tradingSheet, query.Name())
