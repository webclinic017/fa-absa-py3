""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_aggregation/FFxAggregatePerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFXAggregatePerform - Module which executes the FX aggregation

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import os
import os.path
import time

import ael
import acm
import FBDPCommon
import FFxCommon
import FReporting

from collections import Counter
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import importlib

DEFAULTPARTY = acm.FParty['FMAINTENANCE']
BATCH_SIZE = 400
INCEPTION_DATE = '1970-01-01'
PL_COLUMNS = ['Portfolio Total Profit and Loss',
                'Portfolio Projected Payments Currency Pair']
_SUBDIRS = ('Before', 'After', 'Compare')


def perform_aggregation(dictionary):
    Logme()('FXAggregation 2.1.5')
    day = FBDPCommon.toDate(dictionary['date'])
    Logme()('FX Aggregation date:%s' % str(day))
    agg = FxAggregation()
    agg.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')


def createContainer(trades, filterFn=None):
    unionObject = acm.FAdhocPortfolio()
    for trade in trades:
        unionObject.Add(trade)
    if filterFn:
        filterFn(unionObject.Trades())
    return unionObject


def createCalculationSpaceAndNodeTree(trades):
    container = createContainer(trades)
    calcSpace = acm.Calculations().CreateCalculationSpace(
            acm.GetDefaultContext(), 'FPortfolioSheet')
    calcSpace.Clear()
    topNode = calcSpace.InsertItem(container)
    calcSpace.Refresh()

    node = topNode.Iterator().FirstChild()
    if not node:
        raise acm.FException("Could not get Asian Option instrument "
                "fields from the CalculationSpace.")
    nodeTree = node.Tree()
    return calcSpace, nodeTree


def getColumnValue(calcSpace, nodeTree, column, curr):
    try:
        c = FFxCommon.setColumnConfig(curr)
        calcObj = calcSpace.CreateCalculation(nodeTree, column, c)
        if not calcObj:
            Logme()('Could not get {0} for {1}. Returning 0.'.format(column,
                curr.Name()), 'WARNING')
            return 0.
        val = FFxCommon.calcToNum(calcObj.Value())
        return val
    except Exception as e:
        Logme()('Invalid {0} found for {1}: {2}. Returning 0.'.format(column,
            curr.Name(), e), 'WARNING')
    return 0.


class Batcher(object):
    def __init__(self, trades, batch_size):
        self.batch = int(batch_size)
        self.fr = 0
        self.to = int(self.batch)
        self.trades = trades

    def getTradeBatch(self):
        if not self.trades:
            return None

        if self.fr >= len(self.trades):
            return None

        if self.to > len(self.trades):
            self.to = len(self.trades)
        batch = self.trades[self.fr:self.to]
        self.fr = self.fr + self.batch
        self.to = self.to + self.batch
        if not batch:
            return None
        return batch


def _initReportsDir(path):
    if not path:
        Logme()("No P&L report directory specified.", 'ERROR')
        return ''

    dirname = os.path.join(path, "ProfitAndLoss{0}".format(time.strftime(
        '%Y%m%d')))
    if os.path.exists(dirname):
        if os.path.isdir(dirname):
            return dirname
        Logme()("P&L report path {0} must be a directory.".format(dirname),
                'ERROR')
        return ''

    try:
        # makedirs will make a directory out of the input path as long as it
        # doesn't exist, even if it looks like a filename e.g. 'blah.txt'.
        os.makedirs(dirname)
        Logme()('Created P&L report directory: {0}'.format(dirname), 'DEBUG')
        return dirname
    except Exception as ex:
        Logme()('Could not create P&L report directory {0}: {1}'.format(
            dirname, ex), 'ERROR')
        return ''


def _initSubDirs(dirname):
    assert os.path.exists(dirname) and os.path.isdir(dirname), ("argument "
            "must be an existing directory")
    for subdir in _SUBDIRS:
        path = os.path.join(dirname, subdir)
        if not os.path.exists(path):
            os.mkdir(path)

class CashAggregationInfo():

    def __init__(self, currPair, cur, cash1, cash2, trades):
        self.currPair = currPair
        self.cur = cur
        self.cash1 = cash1
        self.cash2 = cash2
        self.trades = trades

    def CurrencyPair(self):
        return self.currPair

    def Cash1(self):
        return self.cash1

    def Cash2(self):
        return self.cash2

    def Cur(self):
        return self.cur

    def Name(self):
        if self.currPair:
            return self.currPair.Name()
        elif self.cur:
            return self.cur.Name()
        return ''

    def Trades(self):
        return self.trades

    def AddTrade(self, t):
        self.trades.append(t)

class FxAggregation(FFxCommon.FxGroupingProcess):
    def _initPLVars(self, args):
        self.diffPL = args.get('diff_test', False)
        self.reports = {}

        if self.diffPL:
            self.reportsDir = _initReportsDir(args.get('report_path', ''))
            if self.reportsDir:
                _initSubDirs(self.reportsDir)
        else:
            self.reportsDir = ''

    def readArguments(self, args):
        self.date = args['date'] and FBDPCommon.toDate(args['date'])
        if self.date > acm.Time.DateToday():
            raise Exception('FX Aggregation date cannot be in the future.')

        self.date = acm.Time.DateAddDelta(self.date, 0, 0, -1)
        self.deaggregate = args['deaggregate']
        self.mergeAggTrades = args.get('mergeAggTrades', 0)
        self.tradingObjects = []
        self.Testmode = args['Testmode']
        self._initPLVars(args)
        self.includeForwardTrades = args.get('includeForwardTrades', 0)
        self.forwardAggregation = False
        self.years = args.get('years', 0)
        self.months = args.get('months', 0)
        self.days = args.get('days', 0)
        self.maxTrades = args.get('maxTrades', 100000)

        self.raise_pre = 'AsgardStop1' in args and args['AsgardStop1']
        self.raise_mid1 = 'AsgardStop2' in args and args['AsgardStop2']
        self.raise_mid2 = 'AsgardStop3' in args and args['AsgardStop3']
        self.raise_post = 'AsgardStop4' in args and args['AsgardStop4']
        self.batch_size = BATCH_SIZE
        if 'AsgardBatch' in args:
            self.batch_size = args['AsgardBatch']
        self.multiUpdates = args.get('multiUpdates', 0)
        self.resultDict = {}

        self.prfs = 'TradingPortfolios' in args and args['TradingPortfolios']
        self.positionAggTrade = {}
        FFxCommon.FxGroupingProcess.readArguments(self, args)

    def calculateAggregationDates(self):
        aggdates = []
        #self.date is the aggregation date.
        #starting on date, move back self.years
        i = self.years
        while i > 0:
            year = acm.Time.DateAddDelta(self.date, -i + 1, 0, 1)
            firstOfYear = acm.Time.FirstDayOfYear(year)
            aggDate = acm.Time.DateAddDelta(firstOfYear, 0, 0, -1)
            aggdates.append(aggDate)
            i -= 1
        j = self.months
        while j > 0:
            month = acm.Time.DateAddDelta(self.date, 0, -j + 1, 1)
            firstOfMonth = acm.Time.FirstDayOfMonth(month)
            aggDate = acm.Time.DateAddDelta(firstOfMonth, 0, 0, -1)
            aggdates.append(aggDate)
            j -= 1
        k = self.days
        while k > 0:
            aggDate = acm.Time.DateAddDelta(self.date, 0, 0, -k)
            aggdates.append(aggDate)
            k -= 1
        aggdates.append(self.date)
        return aggdates

    def createCalcSpace(self, trades, grouper=None, timeBucketGrouper=None,
            filterTrades=None):

        self.config = None
        self.portfolio = None
        self.calcSpace = None
        self.topNode = None
        self.grouping = []
        self.container = None
        self.optKeys = {}
        newGroupers = []
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                self.grouping.append(str(g.Label()))
                newGroupers.append(g)
        if self.forwardAggregation:
            valueDayGrouper = acm.FAttributeGrouper("Trade.ValueDay")
            valueDayGrouper.Label("Trade ValueDay")
            self.grouping.append(str(valueDayGrouper.Label()))
            newGroupers.append(valueDayGrouper)
            acquireDayGrouper = acm.FAttributeGrouper("Trade.AcquireDay")
            acquireDayGrouper.Label("Trade AcquireDay")
            self.grouping.append(str(acquireDayGrouper.Label()))
            newGroupers.append(acquireDayGrouper)

        if (timeBucketGrouper and
                timeBucketGrouper.IsKindOf(acm.FTimeBucketGrouper)):
            config = acm.Report().CreatePortfolioSheetGridConfiguration(
                    timeBucketGrouper.TimeBuckets())
            csc = acm.Calculations().CreateCalculationSpaceCollection()
            self.calcSpace = csc.GetSpace('FPortfolioSheet', 'Standard',
                    config)
        else:
            self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')

        container = createContainer(trades, filterTrades)
        self.topNode = self.calcSpace.InsertItem(container)

        self.topNode.ApplyGrouper(acm.FChainedGrouper(newGroupers))
        self.calcSpace.Refresh()

    # tradingObj can be a portfolio, stored folder or trade filter.
    def _reportPL(self, tradingObj, subdir='Before'):
        reportsDir = os.path.join(self.reportsDir, subdir)
        assert os.path.exists(reportsDir) and os.path.isdir(reportsDir), (
                "Report directory {0} should have been created "
                "already.".format(reportsDir))
        filename = tradingObj.Name()
        sheetname = 'FXAggregation'
        FReporting.createPortfolioReport(PL_COLUMNS, [tradingObj],
                # Contrary to the parameter name, it's actually asking for the
                # FChainedGrouper object...
                grouperNames=[self.portfolioGrouper],
                filePath=reportsDir,
                fileName=filename,
                name=sheetname,
                createDateDirectory=False,
                includeExpired=True,
                xmlToFile=True,
                htmlToFile=True,
                snapshot=True,
                matchPerPortfolio=True)
        self.reports[tradingObj] = filename

    def _comparePL(self, tradingObj):
        filename = self.reports.get(tradingObj, '')
        if not filename:
            Logme()("No PL comparison report generated for {0}.".format(
                tradingObj.Name()), "WARNING")
            return False
        filename = '{0}.xml'.format(filename)
        reports = [os.path.join(self.reportsDir, subdir, filename)
                for subdir in _SUBDIRS]

        import FPortfolioComparison
        try:
            diffs = FPortfolioComparison.diff(reports[0], reports[1],
                    reports[2].strip('.xml'), self.portfolioGrouper)
            if not diffs:
                Logme()("{0}: No differences in P&L before and after "
                        "aggregation.".format(tradingObj.Name()), "DEBUG")
                return
            Logme()(("{0}: Different P&L before and after aggregation. "
                "Details in {1}.".format(tradingObj.Name(),
                    reports[2].replace('xml', 'html'))), "WARNING")
        except FPortfolioComparison.PCTException as ex:
            Logme()("{0}: Error comparing P&L - {1}".format(tradingObj.Name(),
                ex), "ERROR")

    def aggregate(self):
        if self.diffPL and self.reportsDir:
            reportPL = self._reportPL
            diffPL = self._comparePL
        else:
            reportPL = lambda x, y: None
            diffPL = lambda x: True
        for obj in self.tradingObjects:
            reportPL(obj, 'Before')
            # check for cash outside the grouped currency pair
            self.createCalcSpace(self.getTrades(obj), self.portfolioGrouper,
                    None, self.filterTrades)
            positions = self.getPositionNodes()
            self.calcSpace.Clear()
            for portfolio, nodes in positions.iteritems():
                for (node, self.attributes) in nodes:
                    if 'PositionPair' in self.attributes:
                        Logme()('PositionOrCurrencyPair should be used '
                                'instead of PositionPair grouper', 'ERROR')
                        return
                    currPair = portfolio.CurrencyPair()
                    if not currPair and \
                        'CurrencyPair' not in self.attributes and \
                        'PositionOrCurrencyPair' not in self.attributes:
                        Logme()('FX Aggregation requires a currency pair '
                                'defined on the portfolio {0} or a portfolio '
                                'grouper containing a grouping by currency '
                                'pair or PositionOrCurrencyPair '
                                'to be defined in the Run Script - '
                                'FFxAggregation application.'.format(
                                    portfolio.Name()), 'ERROR')
                        return
                    pair = None
                    if 'CurrencyPair' in self.attributes:
                        pair = acm.FCurrencyPair[
                                self.attributes['CurrencyPair']]
                    elif 'PositionOrCurrencyPair' in self.attributes:
                        pair = acm.FCurrencyPair[
                                self.attributes['PositionOrCurrencyPair']]
                    if pair:
                        currPair = pair

                    action = 'Deaggregating' if self.deaggregate \
                                else 'Aggregating'
                    FFxCommon.printEmp('%s trading portfolio: "%s".' % (
                            action, portfolio.Name()), '*')
                    if self.attributes:
                        FFxCommon.printEmp('%s grouping position: %s' % (
                                    action, self.attributes), '=')

                    currPairName = 'No Currency Pair'
                    if currPair:
                        currPairName = currPair.Name()

                    Logme()("Grouped currency pair: %s" % currPairName,
                            "DEBUG")

                    nodeTrades = node.Item().Trades().AsIndexedCollection()
                    nodeTrades.SortByProperty("TradeTime")
                    batch_size = self.batch_size
                    if self.deaggregate or self.mergeAggTrades:
                        batch_size = 1
                    tradeList = [t for t in nodeTrades]
                    self.batcher = Batcher(tradeList, batch_size)
                    trades = self.batcher.getTradeBatch()
                    self.aggregateBatch(trades, currPair)
            diffPL(obj)

            self.calcSpace.Clear()
            acm.Calculations().ResetEvaluatorBuilders()
            acm.Memory().GcWorldStoppedCollect()

    def aggregateBatch(self, trades, currPair):
        while trades is not None:
            Logme()("Process %s trades in this batch" %
                len(trades), "DEBUG")
            if self.deaggregate:
                for aggTrade in trades:
                    if aggTrade.Instrument() == aggTrade.Currency():
                        self.otherCurrObjects = self.getCurrObjects(
                                    [aggTrade.Currency()])
                    else:
                        self.otherCurrObjects = self.getCurrObjects(
                            [aggTrade.Instrument(), aggTrade.Currency()])

                    self.deaggregatePosition(aggTrade)
            else:
                if trades[0].Aggregate() == 0:
                    self.createCalcSpace(trades,
                            self.portfolioGrouper,
                            None, None)
                    positions = self.getPositionNodes()

                    for portfolio, nodes in positions.iteritems():
                        self.processPortfolio(portfolio,
                                nodes, trades, currPair)
                    self.calcSpace.Clear()
                else:
                    if currPair:
                        self.otherCurrObjects = self.getCurrObjects(
                                [currPair.Currency1(), currPair.Currency2()])
                        self.mergePosition(trades, currPair)
            acm.PollDbEvents()
            trades = self.batcher.getTradeBatch()
            acm.Calculations().ResetEvaluatorBuilders()
            acm.Memory().GcWorldStoppedCollect()

    def performProcess(self, args):
        self.readArguments(args)

        if self.requiredAttributesNotSet():
            return

        if isinstance(self.portfolioGrouper, list) and \
                        self.portfolioGrouper:
            self.portfolioGrouper = self.portfolioGrouper[0]

        if isinstance(self.portfolioGrouper, str):
            self.portfolioGrouper = acm.FChainedGrouper[self.portfolioGrouper]

        if self.portfolioGrouper:
            if self.portfolioGrouper.IsKindOf(acm.FStoredPortfolioGrouper):
                self.portfolioGrouper = self.portfolioGrouper.Grouper()
            elif not self.portfolioGrouper.IsKindOf(acm.FChainedGrouper):
                self.portfolioGrouper = None

        self.portfolioGrouper = self.createOrModifyGrouper(
                self.portfolioGrouper)
        if not self.tradingObjects:
            return

        self.aggDates = self.calculateAggregationDates()
        for self.date in self.aggDates:
            self.aggregate()
            if self.includeForwardTrades:
                self.forwardAggregation = True
                self.aggregate()
                self.forwardAggregation = False
        if self.multiUpdates:
            self.show_result(self.resultDict)

    def isTradeInExcludedPeriod(self, tradeDate):
        aggIndex = self.aggDates.index(self.date)
        if aggIndex > 0:
            previousAggDate = self.aggDates[aggIndex - 1]
        else:
            previousAggDate = INCEPTION_DATE
        return (tradeDate <= previousAggDate or tradeDate > self.date)

    def isAggregateTrade(self, trade):
        # removes either aggregate trades or normal trades
        # depending on self.deaggregate and self.mergeAggTrades
        if self.deaggregate or self.mergeAggTrades:
            return trade.Aggregate() == 0
        return trade.Aggregate() != 0

    def isForwardTrade(self, trade):
        #compares value date
        if self.deaggregate:
            #Aggregates need to be included if their date is less than
            #the aggregation date, for de-aggregation to work
            return trade.AcquireDay() <= self.date
        else:
            if self.includeForwardTrades and self.forwardAggregation:
                return trade.AcquireDay() > acm.Time.DateToday()
            return trade.AcquireDay() > self.date

    def isFutureTrade(self, trade):
        #compares trade time
        tradeDate = FBDPCommon.toDate(trade.TradeTime())
        if self.deaggregate:
            #Aggregates need to be included if their date is less than
            #the aggregation date, for de-aggregation to work
            return tradeDate <= self.date
        elif self.mergeAggTrades:
            return self.isTradeInExcludedPeriod(tradeDate)
        else:
            return tradeDate > self.date

    def isLiveTrade(self, trade):
        live = trade.Instrument().ExpiryDate() > self.date
        return live

    def hasFuturePayments(self, trade):

        if trade.Aggregate() != 0:
            return False

        payments = trade.Payments()
        for p in payments:
            if p.PayDay() > self.date:
                return True
        return False

    def filterTrades(self, trades):
        hook = None
        try:
            import FBDPHook
            importlib.reload(FBDPHook)
            hook = FBDPHook.fx_aggregation_exclude_trade
            if trades:
                hook(trades[0])
        except Exception:
            hook = None
        totalrefs = acm.FIdentitySet()
        for filterFunc in [self.isAggregateTrade,
                            self.isForwardTrade,
                            self.isLiveTrade, self.isFutureTrade,
                            self.hasFuturePayments,
                            hook]:
            if not filterFunc:
                continue
            remove = acm.FArray()
            remove.AddAll(filter(filterFunc, trades))
            totalrefs.AddAll(remove)
            for t in remove:
                self.findReferenceTrades(t, totalrefs)
        removed = trades.Intersection(totalrefs).AsArray().Sort()
        trades.RemoveAll(removed)

    def findReferenceTrades(self, trade, removed):
        trades = self.getRefIn(trade).AddAll(self.getRefOut(trade))
        trades.RemoveAll(removed)
        removed.AddAll(trades)
        tradeList = trades.AsArray()
        for t in tradeList:
            self.findReferenceTrades(t, removed)

    def getRefOut(self, trade):
        trades = acm.FArray()
        refAttribs = ['ConnectedTrdnbr', 'GroupTrdnbr', 'MirrorTrade',
                'TrxTrade']
        for attr in refAttribs:
            t = trade.GetProperty(attr)
            if t:
                if type(t) == type(1):
                    #check if this is our trade id
                    if t != trade.Oid():
                        trades.Add(acm.FTrade[t])
        return trades

    def getRefIn(self, trade):
        finalRefTradesSet = acm.FIdentitySet()
        refAttribs = [('connectedTrdnbr', 'ConnectedTrdnbr'),
                ('groupTrdnbr', 'GroupTrdnbr'),
                ('mirrorTrade', 'MirrorTrade'),
                ('trxTrade', 'TrxTrade')]
        for attr1, attr2 in refAttribs:
            allRefTrades = acm.FTrade.Select('%s = %s' % (attr1, trade.Oid()))
            for t in allRefTrades:
                refFieldId = None
                tProperty = t.GetProperty(attr2)
                if tProperty:
                    if isinstance(tProperty, (long, int)):
                        refFieldId = tProperty
                    elif tProperty.IsKindOf(acm.FTrade):
                        refFieldId = tProperty.Oid()
                if refFieldId == trade.Oid() and t.Oid() != trade.Oid():
                    finalRefTradesSet.Add(t)
        return finalRefTradesSet

    def getCurrObjects(self, currList):
        query = ''
        for curr in currList:
            if query:
                query += ' and '
            query += "name <> '%s'" % (curr.Name())
        return acm.FCurrency.Select(query)

    def getCashAggregationInfoObjects(self, node, trades, currPair):
        curPair = ''
        if 'CurrencyPair' in self.attributes:
            curPair = self.attributes['CurrencyPair']
        elif 'PositionOrCurrencyPair' in self.attributes:
            curPair = self.attributes['PositionOrCurrencyPair']

        noCurrPair = ['No Currency Pair', 'No CurrencyPair',
            'No Trade: CurrencyPair', 'No Trade: PositionOrCurrencyPair']
        if any(n in curPair for n in noCurrPair):
            aggInfoDic = {}
            for t in trades:
                curr = t.Currency()
                if curr.Name() in aggInfoDic.keys():
                    aggInfoDic[curr.Name()].AddTrade(t)
                    continue
                else:
                    cash = self.getCashflow(node, None, curr)
                    aggInfo = CashAggregationInfo(None, curr, cash, 0.0, [])
                    aggInfo.AddTrade(t)
                    aggInfoDic[curr.Name()] = aggInfo
            return aggInfoDic.values()
        else:
            cash1 = self.getCashflow(node, None, currPair.Currency1())
            cash2 = self.getCashflow(node, None, currPair.Currency2())
            aggInfo = CashAggregationInfo(currPair, None, cash1, cash2, trades)
            return [aggInfo]

    def processPortfolio(self, tradingPort, nodes, trades, currPair):
        for (node, self.attributes) in nodes:
            aggInfoList = self.getCashAggregationInfoObjects(node,
                              trades, currPair)

            if len(aggInfoList) == 1 and aggInfoList[0].CurrencyPair():
                currList = [aggInfoList[0].CurrencyPair().Currency1(),
                            aggInfoList[0].CurrencyPair().Currency2()]
            else:
                currList = [aggInfo.Cur() for aggInfo in aggInfoList]
            self.otherCurrObjects = self.getCurrObjects(currList)
            self.otherCurrObjectsProcessed = 0
            for aggInfo in aggInfoList:
                self.aggregatePosition(node, tradingPort, aggInfo)

    def deaggregatePosition(self, aggTrade):
        trades = self.findArchivedTradesFromAggTrade(aggTrade)
        if self.multiUpdates and not self.Testmode:
            abort = self.multiDearchiveTrades(trades, aggTrade)
        else:
            abort = self.dearchiveTrades(trades, aggTrade)
        if not self.Testmode and not abort:
            aggTrade.Delete()

    def applyPayments(self, aggTrade, node):

        if aggTrade.insaddr == aggTrade.curr and \
                self.otherCurrObjectsProcessed == 1:
            return

        for curr in self.otherCurrObjects:
            cash = self.getCashflow(node, None, curr)
            if not cash:
                continue

            payments = ael.Payment.select('trdnbr=%d' % (aggTrade.trdnbr))
            existingPayment = None
            for p in payments:
                if p.curr == FBDPCommon.acm_to_ael(curr):
                    existingPayment = p
                    break

            if existingPayment:
                existingPaymentClone = existingPayment.clone()
                existingPaymentClone.amount += cash
                existingPaymentClone.commit()
            else:
                payment = ael.Payment.new(aggTrade)
                payment.payday = aggTrade.acquire_day
                payment.valid_from = aggTrade.acquire_day
                payment.amount = cash
                payment.curr = FBDPCommon.acm_to_ael(curr)
                payment.ptynbr = aggTrade.counterparty_ptynbr
                payment.commit()

        if aggTrade.insaddr == aggTrade.curr:
            self.otherCurrObjectsProcessed = 1

    def createSimulatePayments(self, aggTrade, node):

        if aggTrade.Instrument() == aggTrade.Currency() and \
                self.otherCurrObjectsProcessed == 1:
            return []

        simulatePayments = []
        for curr in self.otherCurrObjects:
            cash = self.getCashflow(node, None, curr)
            if not cash:
                continue
            paymentCurrs = [p.Currency() for p in aggTrade.Payments()]
            if curr not in paymentCurrs:
                targetPayment = self.fillPayment(curr, 0, aggTrade)
                targetPayment.Trade(aggTrade)
                targetPayment.Commit()

            simulatePayment = self.fillPayment(curr,
                                        cash, aggTrade)
            simulatePayments.append(simulatePayment)

        if aggTrade.Instrument() == aggTrade.Currency():
            self.otherCurrObjectsProcessed = 1

        return simulatePayments

    def createNodeKeyFromAttributes(self, attribs, aggInfo):
        nodeKey = ''.join([str(attribs[key])
                    for key in sorted(attribs.iterkeys())])
        if (('CurrencyPair' in attribs and
           'No Currency' not in attribs['CurrencyPair'] and
           'No Trade: CurrencyPair' not in attribs['CurrencyPair']) or
           ('PositionOrCurrencyPair' in attribs and
           'No Trade: PositionOrCurrencyPair' not in
            attribs['PositionOrCurrencyPair'])):
            return nodeKey + self.date
        else:
            return nodeKey + aggInfo.Name() + self.date

    def createOrGetAggregateTrade(self, tradingPort, attribs, aggInfo):
        nodeKey = self.createNodeKeyFromAttributes(attribs, aggInfo)
        newAggregateCreated = False
        if nodeKey not in self.positionAggTrade:
            aggTrade = self.createNewAggTrade(tradingPort, aggInfo)
            self.positionAggTrade[nodeKey] = aggTrade
            newAggregateCreated = True
            Summary().ok(aggTrade, Summary().CREATE, aggTrade.Oid())
        elif self.shouldCreate(self.positionAggTrade[nodeKey]):
            aggTrade = self.createNewAggTrade(tradingPort, aggInfo)
            self.positionAggTrade[nodeKey] = aggTrade
            newAggregateCreated = True
            Summary().ok(aggTrade, Summary().CREATE, aggTrade.Oid())
        return self.positionAggTrade[nodeKey], newAggregateCreated

    def reuseExistingAggregateTrade(self, trade):
        trade.TradeTime(self.date)
        trade.AcquireDay(self.date)
        trade.ValueDay(self.date)
        self.setTradePropertiesFromGrouper(trade)
        if not self.Testmode:
            trade.Commit()
        Logme()('Updating Aggregate Trade %s' % trade.Oid(), 'INFO')
        return trade

    def findArchivedTradesFromAggTrade(self, aggTrade):
        aelAggTrade = FBDPCommon.acm_to_ael(aggTrade)
        trades = aelAggTrade.reference_in(1)
        f = lambda x: (x.record_type == 'Trade' and x.aggregate_trdnbr and
                x.aggregate_trdnbr.trdnbr == aggTrade.Oid())
        trades = filter(f, trades)
        return trades

    def shouldCreate(self, aggTrade):
        nSource = len(self.findArchivedTradesFromAggTrade(aggTrade))
        if nSource >= self.maxTrades:
            return True
        else:
            return False

    def shouldMerge(self, sourceAgg, targetAgg, nodeKey):
        sourceTrades = self.findArchivedTradesFromAggTrade(sourceAgg)
        targetTrades = self.findArchivedTradesFromAggTrade(targetAgg)
        if targetAgg is None:
            return True, sourceTrades, targetTrades
        nSource = len(sourceTrades)
        nTarget = len(targetTrades)
        if nSource + nTarget > self.maxTrades:
            if nSource < nTarget:
                self.reuseExistingAggregateTrade(sourceAgg)
                self.positionAggTrade[nodeKey] = sourceAgg
            return False, sourceTrades, targetTrades
        else:
            return True, sourceTrades, targetTrades

    def mergePosition(self, trades, currPair):
        abort = 0
        try:
            nodeKey = self.createNodeKeyFromAttributes(
                    self.attributes, currPair)
            if nodeKey not in self.positionAggTrade:
                self.reuseExistingAggregateTrade(trades[0])
                self.positionAggTrade[nodeKey] = trades[0]
                return
        except Exception, e:
            message = ('Failed to reuse the existing aggregate trade. '
                    'Got an exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            abort = 1
        if not abort:
            targetAggTrade = self.positionAggTrade[nodeKey]
            sourceAggTrade = trades[0]
            merge, sourceTrades, targetTrades = self.shouldMerge(
                                        sourceAggTrade, targetAggTrade,
                                        nodeKey)
            if not merge:
                return

            # only proceed if the total number of trades
            # will be less than maxtrades
            paymentCurrs = [p.Currency() for p in targetAggTrade.Payments()]
            for payment in sourceAggTrade.Payments():
                if payment.Currency() not in paymentCurrs:
                    targetPayment = self.fillPayment(payment.Currency(),
                                                    0, targetAggTrade)
                    targetPayment.Trade(targetAggTrade)
                    targetPayment.Commit()
            self.updatePositionAggregateTrades(targetAggTrade, sourceAggTrade,
                                            sourceTrades)

    def updatePositionAggregateTrades(self, targetAggTrade,
                                        sourceAggTrade, trades):
        if not self.Testmode and self.multiUpdates:
            abort = self.moveArchivedTrades(trades,
                                    sourceAggTrade, targetAggTrade)
        else:
            abort = self.updateArchiveTrades(trades,
                                sourceAggTrade, targetAggTrade)
        if not self.Testmode and not abort:
            sourceAggTrade.Delete()

    def BuildUpdateInfo(self, batchTrades, sourceAggTrade):
        simulateTradeList = []
        for t in batchTrades:
            td = FBDPCommon.ael_to_acm(t)
            simulateTradeList.append(td)
        calcSpace, nodeTree = createCalculationSpaceAndNodeTree(
                        simulateTradeList)

        simulateTrade, simulatePayments = \
                self.simulateTradesAndPayments(calcSpace, sourceAggTrade,
                                    nodeTree,
                                    'Portfolio Projected Payments')
        tradeIds = [t.Oid() for t in simulateTradeList]
        updateInfo = {'aggTrade': simulateTrade,
                    'payments': simulatePayments}
        return tradeIds, updateInfo

    def moveArchivedTrades(self, trades, sourceAggTrade, targetAggTrade):
        batcher = Batcher(trades, self.batch_size)
        batchTrades = batcher.getTradeBatch()
        while batchTrades is not None:
            tradeIds, updateInfo = self.BuildUpdateInfo(batchTrades,
                                                    sourceAggTrade)
            results = acm.Aggregation.MergeAggregates(
                        tradeIds, targetAggTrade.Oid(),
                        sourceAggTrade.Oid(), updateInfo)
            self.collectResults(results)
            batchTrades = batcher.getTradeBatch()
        return 0

    def updateArchiveTrades(self, trades, sourceAggTrade, targetAggTrade):
        batcher = Batcher(trades, self.batch_size)
        batchTrades = batcher.getTradeBatch()
        while batchTrades is not None:
            ael.begin_transaction()
            try:
                for trade in batchTrades:
                    tradeClone = trade.clone()
                    tradeClone.aggregate_trdnbr = targetAggTrade.Oid()
                    if not self.Testmode:
                        tradeClone.commit()
                    Logme()('Move archive trade %s to Aggregate trade %s' %
                            (trade.trdnbr, targetAggTrade.Oid()), 'DEBUG')
                if not self.Testmode:
                    simulateTradeList = []
                    for t in batchTrades:
                        td = FBDPCommon.ael_to_acm(t)
                        #td.ArchiveStatus(0)
                        #td.Simulate()
                        simulateTradeList.append(td)
                    calcSpace, nodeTree = createCalculationSpaceAndNodeTree(
                                    simulateTradeList)
                    self.UpdateSourceAndTargetAggregateTrade(calcSpace,
                                        sourceAggTrade,
                                        targetAggTrade,
                                        nodeTree,
                                        'Portfolio Projected Payments')
                    #for t in simulateTradeList:
                    #    t.Unsimulate()
                self.commitAddedEntities()
            except Exception, e:
                message = ('Failed to move and update trades. '
                        'Got an exception: {0}'.format(e))
                Logme()(message, 'ERROR')
                ael.abort_transaction()
                Summary().abortEntries()
                return 1
            batchTrades = batcher.getTradeBatch()
        return 0

    def UpdateSourceAndTargetAggregateTrade(self, calcSpace, sourceAggTrade,
                                    targetAggTrade, nodeTree, column):
        aelSourceAggTrade = FBDPCommon.acm_to_ael(sourceAggTrade)
        aelTargetAggTrade = FBDPCommon.acm_to_ael(targetAggTrade)
        aelAggTradeClone = aelSourceAggTrade.clone()
        aelTargetAggTradeClone = aelTargetAggTrade.clone()
        ins = sourceAggTrade.Instrument()
        curr = sourceAggTrade.Currency()
        quantity = getColumnValue(calcSpace, nodeTree, column, ins)
        aelAggTradeClone.quantity -= quantity
        aelTargetAggTradeClone.quantity += quantity
        premium = getColumnValue(calcSpace, nodeTree, column, curr)
        aelAggTradeClone.premium -= premium
        aelTargetAggTradeClone.premium += premium
        if aelTargetAggTradeClone.quantity != 0:
            aelTargetAggTradeClone.price = \
                        abs(float(-aelTargetAggTradeClone.premium) /
                        aelTargetAggTradeClone.quantity)
        if aelAggTradeClone.quantity != 0:
            aelAggTradeClone.price = abs(float(-aelAggTradeClone.premium) /
                                    aelAggTradeClone.quantity)
        aelAggTradeClone.commit()
        aelTargetAggTradeClone.commit()

        for curr in self.otherCurrObjects:
            paymentAmount = getColumnValue(calcSpace, nodeTree, column, curr)
            if paymentAmount:
                payments = aelSourceAggTrade.payments()
                for p in payments:
                    if p.curr.insid == curr.Name():
                        paymentClone = p.clone()
                        paymentClone.amount -= paymentAmount
                        paymentClone.commit()
                        break
                payments = aelTargetAggTrade.payments()
                for p in payments:
                    if p.curr.insid == curr.Name():
                        paymentClone = p.clone()
                        paymentClone.amount += paymentAmount
                        paymentClone.commit()
                        break

    def collectResults(self, results):
        tempDict = {}
        operation = 0
        for key in results.Keys():
            if key != 'Operation':
                tempDict[key] = results.At(key)
            else:
                operation = results.At(key)
        if not self.resultDict or operation not in self.resultDict:
            self.resultDict[operation] = Counter(tempDict)
        else:
            self.resultDict[operation] += Counter(tempDict)

    def aggregatePosition(self, node, tradingPort, aggInfo):
        abort = 0
        newAggregateCreated = False
        inTransaction = False
        trades = aggInfo.Trades()
        try:
            aggTrade, newAggregateCreated = self.createOrGetAggregateTrade(
                        tradingPort, self.attributes, aggInfo)
        except Exception as e:
            message = ('Failed to create new aggregate trade. '
                    'Got an exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            abort = 1

        if not (abort):
            if not self.Testmode:
                if self.multiUpdates:
                    simulateTrade = self.createSimulateTrade(tradingPort,
                                                            aggInfo)
                    simulatePayments = self.createSimulatePayments(aggTrade,
                                                                node)
                    updateInfo = {'aggTrade': simulateTrade,
                                'payments': simulatePayments}

                    tradeIds = [t.Oid() for t in trades]
                    results = acm.Aggregation.Aggregate(
                                tradeIds, aggTrade.Oid(), updateInfo)
                    self.collectResults(results)
                    return
                else:
                    aggTrade = self.fillAggregateTrade(
                            FBDPCommon.acm_to_ael(aggTrade).clone(),
                                            tradingPort, aggInfo)
            else:
                aggTrade = self.fillAggregateTrade_acm(aggTrade.Clone(),
                        tradingPort, aggInfo)

        #archive trades
        if not (abort or self.Testmode):
            try:
                if self.raise_pre:
                    raise Exception('ASGARD test generated exception '
                            '(before transaction).')
                ael.begin_transaction()
                inTransaction = True
                # update the empty aggregate's values in the same transaction
                # as archiving occurs
                aggTrade.commit()
                self.applyPayments(aggTrade, node)
                if self.raise_mid1:
                    raise Exception('ASGARD test generated exception '
                            '(during transaction).')
                for trade in trades:
                    self.archiveTradeAndChildren(trade, aggTrade)

                if self.raise_mid2:
                    raise Exception('ASGARD test generated exception '
                            '(during transaction).')
                #commit any remaining entities
                ael.commit_transaction()
                inTransaction = False
                newAggregateCreated = False
                if self.raise_post:
                    raise Exception('ASGARD test generated exception '
                            '(after transaction).')
            except Exception, e:
                message = ('Failed to aggregate trades. '
                        'Got an exception: {0}'.format(e))
                Logme()(message, 'ERROR')
                if inTransaction == True:
                    Logme()("Aborting transaction.", "ERROR")
                    ael.abort_transaction()
                if newAggregateCreated and not self.Testmode:
                    Logme()("Deleting aggregate trade.", "ERROR")
                    aggTrade.delete()
                Summary().abortEntries()

    def UpdateAggregateTrade(self, calcSpace, aggTrade, nodeTree,
                            column):
        aelAggTrade = FBDPCommon.acm_to_ael(aggTrade)
        aelAggTradeClone = aelAggTrade.clone()
        ins = aggTrade.Instrument()
        curr = aggTrade.Currency()
        quantity = getColumnValue(calcSpace, nodeTree, column, ins)
        aelAggTradeClone.quantity -= quantity
        premium = getColumnValue(calcSpace, nodeTree, column, curr)
        aelAggTradeClone.premium -= premium
        aelAggTradeClone.commit()

        for curr in self.otherCurrObjects:
            paymentAmount = getColumnValue(calcSpace, nodeTree, column, curr)
            if paymentAmount:
                payments = aelAggTrade.payments()
                for p in payments:
                    if p.curr.insid == curr.Name():
                        paymentClone = p.clone()
                        paymentClone.amount -= paymentAmount
                        paymentClone.commit()
                        break

    def dearchiveTrades(self, trades, aggTrade):
        batcher = Batcher(trades, self.batch_size)
        batchTrades = batcher.getTradeBatch()
        while batchTrades is not None:
            ael.begin_transaction()
            try:
                for trade in batchTrades:
                    tradeClone = trade.clone()
                    tradeClone.archive_status = 0
                    tradeClone.aggregate_trdnbr = None
                    if not self.Testmode:
                        self.dearchiveAELObjects(trade.additional_infos())
                        self.dearchiveAELObjects(trade.payments())
                        tradeClone.commit()
                    Logme()('Dearchive Trade %s' % trade.trdnbr, 'DEBUG')
                    Summary().ok(trade, Summary().DEARCHIVE, trade.trdnbr)
                if not self.Testmode:
                    simulateTradeList = []
                    for t in batchTrades:
                        td = FBDPCommon.ael_to_acm(t)
                        td.ArchiveStatus(0)
                        td.Simulate()
                        simulateTradeList.append(td)
                    calcSpace, nodeTree = createCalculationSpaceAndNodeTree(
                                    simulateTradeList)
                    self.UpdateAggregateTrade(calcSpace, aggTrade,
                                        nodeTree,
                                        'Portfolio Projected Payments')
                    for t in simulateTradeList:
                        t.Unsimulate()
                self.commitAddedEntities()
            except Exception as e:
                message = ('Failed to dearchiveTrades. '
                        'Got an exception: {0}'.format(e))
                Logme()(message, 'ERROR')
                ael.abort_transaction()
                Summary().abortEntries()
                return 1
            batchTrades = batcher.getTradeBatch()
        return 0

    def fillPayment(self, curr, paymentAmount, aggTrade):
        simulatePayment = acm.FPayment()
        simulatePayment.Amount(paymentAmount)
        simulatePayment.Type('Cash')
        simulatePayment.ValidFrom(aggTrade.AcquireDay())
        simulatePayment.Party(aggTrade.Counterparty())
        simulatePayment.PayDay(aggTrade.AcquireDay())
        simulatePayment.Currency(curr)
        return simulatePayment

    def simulateTradesAndPayments(self, calcSpace, aggTrade, nodeTree,
                            column):
        ins = aggTrade.Instrument()
        curr = aggTrade.Currency()
        quantity = getColumnValue(calcSpace, nodeTree, column, ins)
        premium = getColumnValue(calcSpace, nodeTree, column, curr)
        aggInfo = CashAggregationInfo(None, None, -quantity, -premium, [])
        simulateTrade = self.createSimulateTrade(None, aggInfo)
        simulatePayments = []
        for curr in self.otherCurrObjects:
            paymentAmount = getColumnValue(calcSpace, nodeTree, column, curr)
            if paymentAmount:
                simulatePayment = self.fillPayment(curr,
                                    -paymentAmount, aggTrade)
                simulatePayments.append(simulatePayment)
        return simulateTrade, simulatePayments

    def multiDearchiveTrades(self, trades, aggTrade):
        batcher = Batcher(trades, self.batch_size)
        batchTrades = batcher.getTradeBatch()
        while batchTrades is not None:
            tradeIds, updateInfo = self.BuildUpdateInfo(batchTrades,
                                                    aggTrade)
            results = acm.Aggregation.DeAggregate(
                        tradeIds, aggTrade.Oid(), updateInfo)
            self.collectResults(results)
            batchTrades = batcher.getTradeBatch()
        return 0

    def dearchiveAELObjects(self, objects):
        for obj in objects:
            objClone = obj.clone()
            objClone.archive_status = 0
            objClone.commit()
            Logme()('Dearchive %s %s' % (obj.record_type, obj.display_id()),
                    'DEBUG')
            Summary().ok(obj, Summary().DEARCHIVE, obj.display_id())

    def setTrdAdditionalInfo(self, trade, aggInfo):
        trades = aggInfo.Trades()
        if len(trades) == 0:
            return

        addinfoGroupers = []
        grouper = self.portfolioGrouper
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                if not g.IsKindOf(acm.FAttributeGrouper):
                    continue
                gpMethodStr = g.Method().Text()
                if "Trade.AdditionalInfo." not in gpMethodStr:
                    continue
                addinfoGroupers.append(
                    gpMethodStr.replace("Trade.AdditionalInfo.", "").lower())

        origTrd = trades[0]
        addinfo = origTrd.AdditionalInfo()
        Props = addinfo.Properties().split(',')
        trdInfoSpecNames = [i.AddInf().AttributeName().Text().lower()
                        for i in origTrd.AddInfos()]
        for info in trdInfoSpecNames:
            if info not in addinfoGroupers:
                continue

            for p in Props:
                if p.lower() == info:
                    v = addinfo.ReadProperty(p)
                    setattr(trade.AdditionalInfo(), p, v)
                    break
        return

    def createNewAggTrade(self, tradingPort, aggInfo):
        trade = acm.FTrade()
        currPair = aggInfo.CurrencyPair()
        if currPair:
            trade.Instrument(currPair.Currency1())
            trade.Currency(currPair.Currency2())
        else:
            trade.Instrument(aggInfo.Cur())
            trade.Currency(aggInfo.Cur())

        # overridden from self.attributes if grouped on acq
        trade.Acquirer(DEFAULTPARTY)
        trade.Counterparty(DEFAULTPARTY)

        trade.Trader(acm.User())
        trade.Type('FX Aggregate')
        trade.Aggregate(2)
        trade.Status('Internal')

        trade.TradeTime(self.date)
        trade.AcquireDay(self.date)
        trade.ValueDay(self.date)

        for key, val in self.attributes.iteritems():
            if 'AdditionalInfo' in key:
                self.setTrdAdditionalInfo(trade, aggInfo)
                break

        self.setTradePropertiesFromGrouper(trade)
        trade.Portfolio(tradingPort)
        if not self.Testmode:
            trade.Commit()
        Logme()('Creating Aggregate Trade %s' % trade.Oid(), 'INFO')
        Logme()('Aggregate Trade Time %s' % trade.TradeTime(), 'INFO')
        return trade

    def fillAggregateTrade(self, aggTrade, tradingPort, aggInfo):
        price = 0
        aggTrade.quantity += aggInfo.Cash1()
        aggTrade.premium += aggInfo.Cash2()
        if aggTrade.quantity:
            price = -1.0 * aggTrade.premium / aggTrade.quantity
        aggTrade.price = price
        return aggTrade

    def createSimulateTrade(self, tradingPort, aggInfo):
        aggTradeSimulate = acm.FTrade()
        aggTradeSimulate.Quantity(aggInfo.Cash1())
        aggTradeSimulate.Premium(aggInfo.Cash2())
        return aggTradeSimulate

    def fillAggregateTrade_acm(self, aggTrade, tradingPort, aggInfo):
        quantity = aggTrade.Quantity() + aggInfo.Cash1()
        premium = aggTrade.Premium() + aggInfo.Cash2()
        price = 0
        if quantity:
            price = -1.0 * premium / quantity

        aggTrade.Price(price)
        aggTrade.Quantity(quantity)
        aggTrade.Premium(premium)
        return aggTrade

    def set_archive_status_recursive(self, clone, archive_status=1):
        a_status = (FBDPCommon.is_acm_object(clone) and 'ArchiveStatus' or
                'archive_status')
        agg = FBDPCommon.is_acm_object(clone) and 'Aggregate' or 'aggregate'
        if FBDPCommon.has_attr(clone, a_status):
            if FBDPCommon.record_type(clone) == "Settlement":
                return 0
            elif (FBDPCommon.record_type(clone) == "Trade" and
                    FBDPCommon.get_attr(clone, agg) and archive_status == 1):
                if self.Testmode:
                    return 1
                else:
                    raise RuntimeError("Not able to deaggregate the position.")
            if FBDPCommon.get_attr(clone, a_status) != archive_status:
                FBDPCommon.set_attr(clone, a_status, archive_status)
            Summary().ok(clone, (archive_status and Summary().ARCHIVE or
                    Summary().DEARCHIVE), FBDPCommon.display_id(clone))
            clone_ael = eval('ael.%s[%s]' % (FBDPCommon.record_type(clone),
                    FBDPCommon.getPrimaryKey(clone))).clone()
            for child in clone_ael.children():
                c = child
                if FBDPCommon.is_acm_object(clone):
                    c = FBDPCommon.ael_to_acm(child)
                self.set_archive_status_recursive(c, archive_status)
            return 1
        else:
            return 0

    def archiveTradeAndChildren(self, acmtrade, aggTrade):
        aelTrade = FBDPCommon.acm_to_ael(acmtrade)
        trade = aelTrade.clone()
        trade.archive_status = 1
        trade.aggregate_trdnbr = aggTrade.trdnbr
        trade.commit()
        self.archiveAELObjects(aelTrade.additional_infos())
        self.archiveAELObjects(aelTrade.payments())
        self.archiveAELObjects(aelTrade.regulatory_infos())
        self.archiveAELObjects(aelTrade.business_evt_trd_links())
        self.archiveAELObjects(aelTrade.trade_account_links())
        self.archiveAELObjects(aelTrade.aliases())
        Summary().ok(trade, Summary().ARCHIVE, aelTrade.trdnbr)
        Logme()('Archive Trade %s' % aelTrade.trdnbr, 'DEBUG')

    def archiveAELObjects(self, objects):
        for obj in objects:
            objClone = obj.clone()
            objClone.archive_status = 1
            objClone.commit()
            Logme()('Archive %s %s' % (obj.record_type, obj.display_id()),
                    'DEBUG')
            Summary().ok(obj, Summary().ARCHIVE, obj.display_id())

    def commitIfTransactionSize(self):
        self.nrOfArchivedObjects += 1
        if self.nrOfArchivedObjects > self.MAX_IN_TRANSACTION:
            self.commitAddedEntities("continueTransaction")

    def commitAddedEntities(self, continueTransaction=0):
        try:
            if self.Testmode:
                ael.abort_transaction()
            else:
                ael.commit_transaction()
            self.nrOfArchivedObjects = 0
        except Exception, e:
            message = ('Failed to commitAddedEntities. '
                    'Got an exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            ael.abort_transaction()
            raise e
        if continueTransaction:
            ael.begin_transaction()

    def validatePLValues(self, aggTrade, val):
        if Logme().LogMode != 2 or self.Testmode:
            return True

        newGroupers = []
        curr = val.Value().Unit()
        grouper = self.portfolioGrouper
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                newGroupers.append(g)

        calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        unionObject = acm.FAdhocPortfolio()
        unionObject.Name("Trade Union")
        unionObject.Trades().Add(aggTrade)
        calcSpace.SimulateValue(unionObject, 'Portfolio Currency', curr)
        topNode = calcSpace.InsertItem(unionObject)

        topNode.ApplyGrouper(acm.FChainedGrouper(newGroupers))
        calcSpace.Refresh()
        column = "Portfolio Theoretical Total Profit and Loss"

        plBefore = self.calcToNum(val.Value())
        Logme()('TPL Before: %s' % plBefore, 'DEBUG')
        val = calcSpace.CreateCalculation(topNode, column, self.config)
        plAfter = self.calcToNum(val.Value())
        Logme()('TPL After: %s' % plAfter, 'DEBUG')

        if abs(plBefore - plAfter) > 1:
            return False
        else:
            return True

    def show_result(self, resDics):
        for operation, resDic in resDics.iteritems():
            if 'error' in resDic and resDic['error']:
                Logme()('Failed to aggregate: %s' % resDic['error'], 'ERROR')
            else:
                class DummyAgg:
                    def RecordType(self):
                        return "Aggregate"

                class DummyPayment:
                    def RecordType(self):
                        return "Payment"

                class DummyAdditionalInfo:
                    def RecordType(self):
                        return "AdditionalInfo"

                class DummyTrade:
                    def RecordType(self):
                        return "Trade"

                class DummyBusinessTradeLink:
                    def RecordType(self):
                        return "Business Trade Link"

                class DummyTradeAccountLink:
                    def RecordType(self):
                        return "Trade Account Link"

                class DummyTradeAliasLink:
                    def RecordType(self):
                        return "Trade Alias Link"

                ad = DummyAdditionalInfo()
                a = DummyAgg()
                t = DummyTrade()
                p = DummyPayment()
                btl = DummyBusinessTradeLink()
                tal = DummyTradeAccountLink()
                tradeAlias = DummyTradeAliasLink()

                summaryOp = eval('Summary().' + operation)
                if "NbrOfAddInfosUpdated" in resDic:
                    Summary().ok(ad, summaryOp, None,
                            resDic["NbrOfAddInfosUpdated"])
                if "NbrOfPaymentsUpdated" in resDic:
                    Summary().ok(p, summaryOp, None,
                            resDic["NbrOfPaymentsUpdated"])
                if "NbrOfTradesUpdated" in resDic:
                    Summary().ok(t, summaryOp, None,
                            resDic["NbrOfTradesUpdated"])
                if "NbrOfTradeAliasLinksUpdated" in resDic:
                    Summary().ok(tradeAlias, summaryOp, None,
                            resDic["NbrOfTradeAliasLinksUpdated"])
                if "NbrOfTradeAccountLinksUpdated" in resDic:
                    Summary().ok(tal, summaryOp, None,
                            resDic["NbrOfTradeAccountLinksUpdated"])
                if "NbrOfBTLsUpdated" in resDic:
                    Summary().ok(btl, summaryOp, None,
                            resDic["NbrOfBTLsUpdated"])
