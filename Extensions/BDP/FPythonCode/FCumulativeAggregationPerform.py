""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/archive_trades/FCumulativeAggregationPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FCumulativeAggregationPerform - Module which executes the archiving of trades

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import os
import os.path
import time
import math

import ael
import acm
import FBDPCommon
import FFxCommon
import FReporting
import FPortfolioComparison

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme

DEFAULTPARTY = acm.FParty['FMAINTENANCE']
BATCH_SIZE = 500
PL_COLUMNS = ['Portfolio Total Profit and Loss',
                'Portfolio Projected Payments Currency Pair']
_SUBDIRS = ('Before', 'After', 'Compare')

DELTA_AGGREGATE = 2
CUMULATIVE_AGGREGATE = 3
SNAPSHOT_AGGREGATE = 4
INACTIVE_CUMULATIVE_AGGREGATE = 5


def perform_aggregation(dictionary):
    Logme()('FCumulativeAggregationPerform 1.0.0')
    day = FBDPCommon.toDate(dictionary['date'])
    Logme()('Aggregation date:%s' % str(day))
    agg = FCumulativeAggregation()
    agg.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')

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


class FCumulativeAggregation(FFxCommon.FxGroupingProcess):
    def _initPLVars(self, args):
        self.diffPL = args.get('diff_test', False)
        self.reports = {}

        if self.diffPL:
            self.reportsDir = _initReportsDir(args.get('report_path', ''))
            if self.reportsDir:
                _initSubDirs(self.reportsDir)
        else:
            self.reportsDir = ''
    
    def validateValuationParams(self):
        return True

    def readArguments(self, args):
        self.date = args['date'] and FBDPCommon.toDate(args['date'])
        if self.date > acm.Time.DateToday():
            raise Exception('Aggregation date cannot be in the future.')

        #self.date = acm.Time.DateAddDelta(self.date, 0, 0, -1)
        self.deagg = args['deaggregate']
        self.tradingObjects = []
        self.Testmode = args['Testmode']
        self._initPLVars(args)

        self.raise_pre = 'AsgardStop1' in args and args['AsgardStop1']
        self.raise_mid1 = 'AsgardStop2' in args and args['AsgardStop2']
        self.raise_mid2 = 'AsgardStop3' in args and args['AsgardStop3']
        self.raise_post = 'AsgardStop4' in args and args['AsgardStop4']
        self.batch_size = BATCH_SIZE
        if 'AsgardBatch' in args:
            self.batch_size = args['AsgardBatch']

        self.prfs = 'TradingPortfolios' in args and args['TradingPortfolios']
        self.openDays = 'openDays' in args and args['openDays']
        self.buckets = 'timeBuckets' in args and args['timeBuckets'][0]
        self.accountingCurrency = acm.ObjectServer().UsedValuationParameters(
                ).AccountingCurrency()
        
        self.calendar = 'calendar' in args and args.get('calendar', None)[0]
        if not self.calendar:
            self.calendar = self.accountingCurrency.Calendar()

        FFxCommon.FxGroupingProcess.readArguments(self, args)

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
    
    def createOrModifyGrouper(self, grouper):

        groupers = acm.FArray()
        instGrouperNeeded = True
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                groupers.Add(g)
                if str(g.Label()) == 'Trade Instrument':
                    instGrouperNeeded = False

        if instGrouperNeeded:
            instGrouper = acm.FAttributeGrouper("Trade.Instrument")
            instGrouper.Label("Trade Instrument")
            groupers.Add(instGrouper)
        grouper = acm.FChainedGrouper(groupers)
        return grouper
    
    def getInstrument(self, nodeTrades):
        return nodeTrades[0].Instrument()
    
    def getArchivedAggregate(self):
        return
        
    def updatePreviousAggs(self, trades, date, agg):
    
        for trade in trades:
            if trade.Aggregate() == CUMULATIVE_AGGREGATE:
                if acm.Time().DateDifference(trade.ValueDay(), date) < 0:
                    trade.Aggregate(INACTIVE_CUMULATIVE_AGGREGATE)
                    trade.AggregateTrade(agg)
                    trade.Commit()       
        acm.PollDbEvents()
        
    def shouldAggregate(self, trades):
        for trade in trades:
            if trade.Aggregate() == 0:
                return True
        
        return False
    
    def getLatestAgg(self, trades, date, type):
        compare_date = '1970-01-01'
        latest_agg = None
        for trade in trades:
            if trade.Aggregate() == type:
                if acm.Time().DateDifference(trade.TradeTime(), compare_date) > 0:
                    compare_date = trade.TradeTime()
                    latest_agg = trade
        return latest_agg
        
    def getPreviousTrades(self, trades, endDate):
        prevTrades = acm.FArray()
        for trade in trades:

            if acm.Time().DateDifference(trade.TradeTime(), endDate) <= 0:
                if trade.Aggregate() != SNAPSHOT_AGGREGATE:
                    prevTrades.Add(trade)
        
        return prevTrades
    
    def shouldCreatePayment(self, start, end, ins):
        dividends = ins.Dividends()
        for dividend in dividends:
            exDivDate = dividend.ExDivDay()
            if exDivDate >= start and exDivDate < end:
                return True
        
        return False
    
    def cumulativeAggregate(self, allTrades, valDate):
        # For the cumulative aggregate, only include historical
        # trades. Otherwise, conversion rates will change P&L over the
        # next n days, where n is the number of spot days.
        instrument = allTrades[0].Instrument()
        spotDays = instrument.SpotBankingDaysOffset()
        endDate = self.calendar.AdjustBankingDays(valDate, -spotDays)
        endDate = endDate + ' 23:59:59'

        trades = self.getPreviousTrades(allTrades, endDate)
        if trades.IsEmpty():
            return
        # dont aggregate if there are only aggregates before this date
        if not self.shouldAggregate(trades):
            return
            
        aggs = acm.AggregateTradeGroup(endDate,
                                        valDate,
                                        1,
                                        CUMULATIVE_AGGREGATE,
                                        1,
                                        [],
                                        trades,
                                        1)
        for agg in aggs:
            print('Aggregated Trade Number:', agg.Oid())
        print('cumulative created')
        acm.PollDbEvents()
        self.updatePreviousAggs(allTrades, endDate, agg)
        acm.PollDbEvents()
    
    def snapshotAggregate(self, allTrades, valDate):
        # For the historical snapshot aggregate, the P&L has to
        # be correct on the snapshot date only, so trade up until
        # valuation date are included
        
        instrument = allTrades[0].Instrument()
        spotDays = instrument.SpotBankingDaysOffset()
        if acm.Time().DateDifference(self.date, valDate) <= spotDays:
            return
            
        trades = self.getPreviousTrades(allTrades, valDate)
        if trades.IsEmpty():
            return
        # dont aggregate if there are only aggregates before this date
        agg = self.getLatestAgg(trades, valDate, SNAPSHOT_AGGREGATE)
        if agg:
            if acm.Time().DateDifference(agg.ValueDay(), valDate) >= 0:
                return
        
        aggs = acm.AggregateTradeGroup(valDate,
                                    valDate,
                                    1,
                                    SNAPSHOT_AGGREGATE,
                                    1,
                                    [],
                                    trades,
                                    1)
        print('snapshot created')
        acm.PollDbEvents()
    
    def aggregateTrades(self, aggDate, historical):
        # Approach: Create a cumulative aggregate that includes all trades
        # which can be aggregated (historical, no forward values)
        # Then create a snapshot aggregate spot days afterwards in 
        # simulated status.
        # The next time aggregation is run, change the status of the snapshot
        # aggregate to FO Confirmed, and mark the previous cumulative with
        # status Simulated
        
        # Cumulative aggregate must have a trade time equal to Spot Days
        # less than the snapshot aggregate
        
        valDate = aggDate
        for obj in self.tradingObjects:
            allTrades = self.getTrades(obj)              
            f = lambda x: (x.Aggregate() != SNAPSHOT_AGGREGATE and
                x.Aggregate() != INACTIVE_CUMULATIVE_AGGREGATE)
            trades = filter(f, allTrades)
            if len(trades) ==0:
                continue
            
            if historical:
                self.snapshotAggregate(trades, valDate)
            else:
                self.cumulativeAggregate(trades, valDate)
                
        return

    def deaggregateTrades(self):
        valDate = self.date
        for obj in self.tradingObjects:
            allTrades = self.getTrades(obj)
            aggTrades = [trade for trade in allTrades
                if (trade.Aggregate() != 0 and
                acm.Time().DateDifference(trade.ValueDay(), valDate) > 0)]
            acm.DeaggregateTradeGroup(aggTrades, 1)
            acm.PollDbEvents()

            agg = self.getLatestAgg(allTrades, self.date, INACTIVE_CUMULATIVE_AGGREGATE)
            if agg:
                agg.Aggregate(CUMULATIVE_AGGREGATE)
                agg.Commit()

    def performProcess(self, args):
        self.readArguments(args)

        if self.requiredAttributesNotSet():
            return

        if isinstance(self.portfolioGrouper, list):
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
        
        if self.deagg:
            self.deaggregateTrades()
            return
            
        buckets = self.buckets.TimeBuckets()
        endDate = '1970-01-01'
        # write the snapshot aggregates first
        # only write snapshots if the aggDate is spot days after
        # the bucket date
        for bucket in buckets:
            endDate = bucket.BucketDate()
            if endDate <= self.date:
                self.aggregateTrades(endDate, True)
        #then write the cumulative aggregate
        self.aggregateTrades(self.date, False)

    def isForwardTrade(self, trade):
        if self.deaggregate and trade.Aggregate():
            return acm.Time().DateDifference(trade.TradeTime(), self.date) <= 0
        
        return acm.Time().DateDifference(trade.TradeTime(), self.date) > 0

    def isLiveTrade(self, trade):
        live = trade.Instrument().ExpiryDate() > self.date
        return live
    
    def isNormalTrade(self, trade):
        return trade.Aggregate() == 0

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
                    if isinstance(tProperty, (int, int)):
                        refFieldId = tProperty
                    elif tProperty.IsKindOf(acm.FTrade):
                        refFieldId = tProperty.Oid()
                if refFieldId == trade.Oid() and t.Oid() != trade.Oid():
                    finalRefTradesSet.Add(t)
        return finalRefTradesSet

    def deaggregate(self, tradeId):
        aelAggTrade = ael.Trade[tradeId]
        trades = aelAggTrade.reference_in(1)
        f = lambda x: (x.record_type == 'Trade' and x.aggregate_trdnbr and
                x.aggregate_trdnbr.trdnbr == tradeId)
        trades = filter(f, trades)
        self.dearchiveTrades(trades)
        if not self.Testmode:
            aelAggTrade.delete()

    def dearchiveTrades(self, trades):
        #ael.begin_transaction()
        self.nrOfArchivedObjects = 0
        try:
            for trade in trades:
                trade = trade.clone()
                trade.archive_status = 0
                trade.aggregate_trdnbr = None
                if not self.Testmode:
                    self.dearchiveAELObjects(trade.additional_infos())
                    self.dearchiveAELObjects(trade.payments())
                    trade.commit()
                #Logme()('Dearchive Trade %s' % trade.trdnbr, 'DEBUG')
                print('Dearchive Trade ', trade.trdnbr)
                Summary().ok(trade, Summary().DEARCHIVE, trade.trdnbr)
                #self.commitIfTransactionSize()
            #self.commitAddedEntities()
        except Exception:
            ael.abort_transaction()

    def dearchiveAELObjects(self, objects):
        for obj in objects:
            obj = obj.clone()
            obj.archive_status = 0
            obj.commit()
            Logme()('Dearchive %s %s' % (obj.record_type, obj.display_id()),
                    'DEBUG')
            Summary().ok(obj, Summary().DEARCHIVE, obj.display_id())

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

    def archiveTradesAndInstruments(self, trades, aggTrade):
        instruments = acm.FSet()
        for trade in trades:
            if not trade.Aggregate():
                self.archiveTradeAndChildren(trade, aggTrade)

    def archiveTradeAndChildren(self, acmtrade, aggTrade):
        trade = FBDPCommon.acm_to_ael(acmtrade).clone()
        trade.archive_status = 1
        trade.aggregate_trdnbr = aggTrade.Oid()
        trade.commit()
        self.archiveAELObjects(trade.additional_infos())
        self.archiveAELObjects(trade.payments())
        Summary().ok(trade, Summary().ARCHIVE, trade.trdnbr)
        Logme()('Archive Trade %s' % trade.trdnbr, 'DEBUG')

    def archiveAELObjects(self, objects):
        for obj in objects:
            obj = obj.clone()
            obj.archive_status = 1
            obj.commit()
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
        except Exception as e:
            ael.abort_transaction()
            raise e
        if continueTransaction:
            ael.begin_transaction()
