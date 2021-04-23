'''----------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2019-03-22  CHG1001539200  Tibor Reiss        Update and refactor to enable PS aggregation
2019-11-19  FAPE-101       Tibor Reiss        New payment type to improve PS aggregation
----------------------------------------------------------------------'''
import acm
from FBDPCurrentContext import Logme, CreateLog, Summary
import FBDPCommon
import FBDPGui
import importlib
importlib.reload(FBDPGui)
from AGGREGATION_PARAMETERS import PARAMETERS, ZAR_CALENDAR
from AGGREGATION_CALC_SPACE import CALC_SPACE
from AGGREGATION_TRADE_FILTER import TRADE_FILTER
from AGGREGATION_TRADE import TRADE_AGGREGATION
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS
import AGGREGATION_CONFIG


agg_days = [acm.Time.DateToday(),
            'Today',
            'First of Month',
            'First of Quarter',
            'First of Year']
counterparties = acm.FParty.Select('').SortByProperty('Name')
internalParties = acm.FParty.Select('type = Intern Dept').SortByProperty('Name')
users = acm.FUser.Select('').SortByProperty('Name')


def disableCounterparty(index, fieldValues):
    counterparty = ael_variables[index + 1]
    counterparty.enable(fieldValues[index])
    return fieldValues


ael_variables = FBDPGui.LogVariables(
                    ['cash_posting_instrument', 'Cash Posting Instrument', acm.FInstrument, acm.FInstrument, None, 1, 0, 'Instrument to be used to post the cash to.', None, 1],
                    ['query_folder', 'Query Folder', acm.FStoredASQLQuery, acm.FStoredASQLQuery, None, 1, 0, 'Query folder containing the trades that should be aggregated.', None, 1],
                    ['date', 'Aggregation Date', 'string', agg_days, 'Today', 1, 0, 'Instruments with an expiry date less than this date will be allegible for aggregation. The trade date, time, vlaue and aquire date will be set to this date as well.', None, 1],
                    ['restrictedPortfolios', 'Restricted Portfolios', acm.FPhysicalPortfolio, acm.FPhysicalPortfolio, 'ERM_IRP', 0, 1, 'Trades in these portfolio or that have mirror trades in these portfolios will be excluded from the aggregation.', None, 1],
                    ['tradeStatus', 'Aggregated Trade Status', 'string', AGGREGATION_CONFIG.TRADE_STATUS_LIST, 'Simulated', 1, 0, 'Trade Status of the aggregated trades.', None, 1],
                    ['grouper', 'Grouper', acm.FStoredPortfolioGrouper, acm.FStoredPortfolioGrouper, None, 1, 0, 'Grouper that should be used to group the selected trades.', None, 1],
                    ['preservePSYearlyTPL', 'Preserve the PS Yearly TPL', 'int', [0, 1], 0, 0, 0, 'Check box indicating whether the PS Yearly TPL should be preserved or not.', None, 1],
                    ['preservePaymentCpty', 'Preserve Payment Counterparty_Advanced', 'int', [0, 1], 0, 0, 0, 'Keep counterparty of addtional trade payments.', None, 1],
                    ['overrideCounterparty', 'Override Counterparty_Advanced', 'int', [0, 1], 0, 0, 0, 'Select a different counterparty for the aggregate trade than the grouper counterparty.', disableCounterparty, 1],
                    ['counterparty', 'Counterparty_Advanced', acm.FParty, counterparties, AGGREGATION_CONFIG.DEFAULT_COUNTERPARTY, 1, 0, 'Counterparty of the aggregate trades.', None, 0],
                    ['acquirer', 'Acquirer_Advanced', acm.FParty, internalParties, AGGREGATION_CONFIG.DEFAULT_ACQUIRER, 1, 0, 'Acquirer of the aggregate trades.', None, 1],
                    ['trader', 'Trader_Advanced', acm.FUser, users, AGGREGATION_CONFIG.DEFAULT_TRADER, 1, 0, 'Trader of the aggregate trades.', None, 1],
                    ['filterYearEndTrades', 'Exclude Year End Cross Over Trades_Advanced', 'int', [0, 1], 0, 0, 0, 'Exclude trades with start date in the previous year and end date in the current year based on aggregation date.', None, 1],
                    ['monthlyBuckets', 'Number of monthly buckets_Advanced', 'int', None, 12, 1, 0, 'The number of monthly buckets which TPL should be retained.', None, 1],
                    ['yearlyBuckets', 'Number of yearly buckets_Advanced', 'int', None, 6, 1, 0, 'The number of (full) yearly buckets which TPL should be retained (extending the monthly buckets).', None, 1]
                )


def ael_main(ael_dict):
    helpers = GENERIC_HELPERS()
    scriptName = __name__
    queryFolder = ael_dict['query_folder']
    
    CreateLog(scriptName,
              ael_dict['Logmode'],
              ael_dict['LogToConsole'],
              ael_dict['LogToFile'],
              ael_dict['Logfile'],
              ael_dict['SendReportByMail'],
              ael_dict['MailList'],
              ael_dict['ReportMessageType'])
    
    Logme()('INFO: STARTING SCRIPT: %s with QUERY FOLDER %s' % (scriptName, queryFolder.Name()), 'INFO')
    
    Logme()('DEBUG: Setting script parameters...', 'DEBUG')
    PARAMETERS.cashPostingInstrument = ael_dict['cash_posting_instrument']
    if ael_dict['overrideCounterparty'] == True:
        PARAMETERS.counterparty = ael_dict['counterparty']
    PARAMETERS.acquirer = ael_dict['acquirer']
    PARAMETERS.trader = ael_dict['trader']
    PARAMETERS.status = ael_dict['tradeStatus']
    dateConvert = ael_dict['date'] and FBDPCommon.toDate(ael_dict['date'])
    if dateConvert != acm.Time.DateToday() and not ZAR_CALENDAR.IsNonBankingDay(None, None, dateConvert):
        PARAMETERS.reportDate = dateConvert
    else:
        PARAMETERS.reportDate = ZAR_CALENDAR.AdjustBankingDays(dateConvert, -1)
    PARAMETERS.queryFolder = queryFolder
    PARAMETERS.grouper = ael_dict['grouper']
    PARAMETERS.preservePSYearlyTPL = ael_dict['preservePSYearlyTPL']
    PARAMETERS.restrictedPortfolios = ael_dict['restrictedPortfolios']
    PARAMETERS.filterYearEndCrossTrades = ael_dict['filterYearEndTrades']
    PARAMETERS.monthlyBuckets = ael_dict['monthlyBuckets']
    PARAMETERS.yearlyBuckets = ael_dict['yearlyBuckets']
    PARAMETERS.summaryDict = {}
    PARAMETERS.preservePaymentCpty = ael_dict['preservePaymentCpty']

    Logme()('DEBUG: Removing Voided trades from the cash posting instrument %s' %
            PARAMETERS.cashPostingInstrument.Name(), 'DEBUG')
    for t in list(PARAMETERS.cashPostingInstrument.Trades()):
        if t.Status() in ('Void') and t.AggregateTrade():
            Logme()('DEBUG: Deleting trade %i' % t.Oid(), 'DEBUG')
            t.Delete()

    Logme()('DEBUG: Initiating the calculation space', 'DEBUG')
    PARAMETERS.calcSpaceClass = CALC_SPACE()
    
    Logme()('DEBUG: Selecting trades and applying grouper', 'DEBUG')
    tradesPerGrouper = PARAMETERS.calcSpaceClass.setTradesPerGrouper()
    
    Logme()('DEBUG: Filter Trades', 'DEBUG')
    tradeFilter = TRADE_FILTER(tradesPerGrouper)
    tradesPerGrouper = tradeFilter.getFilteredTrades()

    nbrOfNodes = len(tradesPerGrouper.keys())
    Logme()('INFO: Number of grouper nodes to aggregate: %i' % nbrOfNodes, 'INFO')
    counter = 0
    
    for key in tradesPerGrouper.keys():
        addInfos = []
        for grouper in PARAMETERS.grouper.Grouper().Groupers():
            if grouper.Method()[0].Text() == 'Trade.Currency':
                if len(tradesPerGrouper[key]) > 0:
                    PARAMETERS.tradeCurrency = tradesPerGrouper[key][0].Currency()
            elif grouper.Method()[0].Text().__contains__('Trade.AdditionalInfo'):
                addInfoPath = grouper.Method()[0].Text().split('.')
                object = tradesPerGrouper[key][0]
                for item in addInfoPath:
                    property = object.GetPropertyObject(item)
                    object = property.Value()
                addInfos.append((grouper.Method()[0].Text(), object))
        PARAMETERS.tradeAdditionalInfos = addInfos
        PARAMETERS.portfolio = 'No Portfolio'
        if len(tradesPerGrouper[key]) > 0:
            if tradesPerGrouper[key][0].Portfolio():
                PARAMETERS.portfolio = tradesPerGrouper[key][0].Portfolio().Name()
            if ael_dict['overrideCounterparty'] == False:
                if tradesPerGrouper[key][0].Counterparty():
                    PARAMETERS.counterparty = ael_dict['counterparty'] = tradesPerGrouper[key][0].Counterparty()
                    
        counter = counter + 1
        Logme()('*' * 150, 'INFO')
        Logme()('')
        grouperCount = 0

        for grouper in PARAMETERS.grouper.Grouper().Groupers():
            Logme()('%-50s\t\t%-50s' % (grouper.Method()[0], key[grouperCount]), 'INFO')
            grouperCount = grouperCount + 1

        Logme()('')
        Logme()('INFO: Progress: %i of %i' % (counter, nbrOfNodes), 'INFO')
        Logme()('')
        Logme()('INFO: Aggregating %i trades.' % len(tradesPerGrouper[key]), 'INFO')
        Logme()('INFO: Trades to be aggregated. %s' % helpers.acmOidToLinstInts(tradesPerGrouper[key]), 'INFO')
        Logme()('')
        Logme()('*' * 150, 'INFO')

        try:
            tradeAggregation = TRADE_AGGREGATION(PARAMETERS.reportDate, tradesPerGrouper[key])
            tradeAggregation.aggregateTrades()
        except Exception, e:
            Logme()('ERROR: Could not aggregate this group of trades. {0}'.format(e), 'ERROR')
                    
        Logme()('INFO: Cleaning of trades complete.', 'INFO')
        
    Summary().log(ael_dict)
    helpers.logSummry()
    Logme()('completed successfully', 'FINISH')
