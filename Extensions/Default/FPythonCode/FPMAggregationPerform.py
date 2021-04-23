""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pm_aggregation/FPMAggregationPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
import importlib
"""----------------------------------------------------------------------------
MODULE
    FPMAggregatePerform - Module which executes the PM aggregation

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

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
from FFxCommon import calcToNum, addDicToDic

DEFAULTPARTY = acm.FParty['FMAINTENANCE']
BATCH_SIZE = 500
COMMODITY_VARIANT_QUANTITY = 'Portfolio Projected Payments'
CURRENCY_AMOUNT = 'Portfolio Projected Payments'


def perform_aggregation(dictionary):
    Logme()('PM Aggregation 4.24.1')
    day = FBDPCommon.toDate(dictionary['date'])
    Logme()('PM Aggregation date:%s' % str(day))
    agg = FPMAggregation()
    agg.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')


def createContainer(trades, filterFn=None):
    unionObject = acm.FAdhocPortfolio()
    for trade in trades:
        unionObject.Add(trade)
    unionObject.Trades()
    if filterFn:
        filterFn(unionObject.Trades())
    return unionObject

class PMAggregationInfo():

    def __init__(self, commodity_variant, commodity_variant_quantity, curr, curr_amount, trades):
        self.commodity_variant = commodity_variant
        self.commodity_variant_quantity = commodity_variant_quantity
        self.curr = curr
        self.curr_amount = curr_amount
        self.trades = trades

    def CurrAmount(self):
        return self.curr_amount

    def CommodityVariant(self):
        return self.commodity_variant
    
    def Quantity(self):
        return self.commodity_variant_quantity
        
    def Currency(self):
        return self.curr

    def CurrAmount(self):
        return self.curr_amount

    def Name(self):
        name = ''
        if self.curr and self.commodity_variant:
            name = self.commodity_variant.Name()
            name += self.curr.Name()
        return name

    def Trades(self):
        return self.trades

    def AddTrade(self, t):
        self.trades.append(t)

class FPMAggregation():

    def readArguments(self, args):
        self.date = args['date'] and FBDPCommon.toDate(args['date'])
        if self.date > acm.Time.DateToday():
            raise Exception('Aggregation date cannot be in the future.')

        self.date = acm.Time.DateAddDelta(self.date, 0, 0, -1)
        self.deaggregate = args['deaggregate']
        self.mergeAggTrades = args.get('mergeAggTrades', 0)
        self.tradingObjects = []
        self.Testmode = args['Testmode']
        self.includeForwardTrades = args.get('includeForwardTrades', 0)
        self.forwardAggregation = False
        self.prfs = 'TradingPortfolios' in args and args['TradingPortfolios']
        self.tradingObjects = self.getTradingObjects(args)
        self.portfolioGrouper = ('PortfolioGrouper' in args and
                args['PortfolioGrouper'])
        self.cashPostingInstrument = ('cp_instrument' in args and args['cp_instrument'])
    
    def getTradingObjects(self, dictionary):

        objects = acm.FArray()
        for field in ['TradeQuery', 'TradeFilter', 'TradingPortfolios']:
            if field in dictionary and dictionary[field]:
                objects.AddAll(dictionary[field])
        return objects
    
    def getTrades(self, obj):
        if obj.IsKindOf(acm.FPortfolio):
            return obj.Trades()
        elif obj.IsKindOf(acm.FStoredASQLQuery) and \
            obj.SubType() == 'FTrade':
            return obj.Query().Select()
        return []

    def createCalcSpace(self, grouper=None):

        self.calcSpace = None
        self.topNode = None
        self.grouping = []
        self.optKeys = {}
        newGroupers = []
        if grouper and grouper.IsKindOf(acm.FChainedGrouper):
            for g in grouper.Groupers():
                self.grouping.append(str(g.Label()))
                newGroupers.append(g)
        self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')
        self.topNode = self.calcSpace.InsertItem(self.container)
        self.topNode.ApplyGrouper(acm.FChainedGrouper(newGroupers))
        self.calcSpace.Refresh()
    
    def performProcess(self, args):

        self.readArguments(args)

        if type(self.portfolioGrouper) == type([]):
            self.portfolioGrouper = self.portfolioGrouper[0]

        if type(self.portfolioGrouper) == type(""):
            self.portfolioGrouper = acm.FChainedGrouper[self.portfolioGrouper]

        if self.portfolioGrouper:
            if self.portfolioGrouper.IsKindOf(acm.FStoredPortfolioGrouper):
                self.portfolioGrouper = self.portfolioGrouper.Grouper()
            elif not self.portfolioGrouper.IsKindOf(acm.FChainedGrouper):
                self.portfolioGrouper = None

        self.aggregate()
    
    def getCalculation(self, node, colName):

        val = self.calcSpace.CreateCalculation(node, colName, None)
        val = calcToNum(val.Value())
        return val

    def getColumnValue(self, node, column, curr):
        return self.getCalculation(node, column)
    
    def getOptKeyObject(self, key, val):
        return acm.FChoiceList.Select("list='%s' AND name=%s" %
                (self.optKeys[key], val))[0]
                
    def extractNodeGrouperMethod(self, grouper):
        method = None
        if grouper.IsKindOf(acm.FAttributeGrouper):
            if str(grouper.Method()) == 'Instrument.Currency':
                method = 'Instrument.Currency'
            else:
                label = grouper.Label()
                method = str(label) if label else str(grouper.Method())
        else:
            method = str(grouper.Label())

        if "Trade " in method:
            method = method.split("Trade ")[1]
        elif "Trade.OptKey" in method:
            return method
        elif method.startswith('Trade.'):
            method = method.split(".")[1]

        return method

    def extractNodeAttribute(self, grouper, item, attrib_out):
        method = self.extractNodeGrouperMethod(grouper)

        if "Trade.OptKey" in method:
            self.buildOptKeysDictionary()
            try:
                attribName = method.split(".")[1]
                attrib_out[attribName] = self.getOptKeyObject(
                        attribName, item.Value()).Name()
            except:
                pass
        else:
            attrib_out[method] = item.StringKey()
    
    def getPositionNodes(self, node=None, attrib_in={}):
        if not node:
            node = self.topNode
        positions = {}
        it = node.Iterator().FirstChild()
        while it:
            tree = it.Tree()
            item = tree.Item()
            trades = item.Trades().AsList()
            if trades.Size() > 0:
                portfolio = (trades and trades[0].Portfolio() or
                        item.Portfolio())
                grouper = item.Grouping().Grouper()
                attrib_out = attrib_in.copy()
                self.extractNodeAttribute(grouper, item, attrib_out)
                if (tree.Depth() - 1 == len(self.grouping)):
                    if portfolio not in positions:
                        positions[portfolio] = []
                    positions[portfolio].append((tree, attrib_out))
                else:
                    addDicToDic(self.getPositionNodes(tree, attrib_out),
                            positions)
            it = it.NextSibling()
        return positions
    
    def getAggInfo(self, node, trades):
        commodity_variant_quantity = self.getColumnValue(node, COMMODITY_VARIANT_QUANTITY, None)[0]
        currency_amount = self.getColumnValue(node, CURRENCY_AMOUNT, None)[1]
        aggInfo = PMAggregationInfo(trades[0].Instrument(), commodity_variant_quantity, trades[0].Currency(), currency_amount, trades)
        print('commodity_variant_quantity', commodity_variant_quantity)
        print('currency_amount', currency_amount)
        return aggInfo

    def aggregate(self):
        for obj in self.tradingObjects:
            trades = self.getTrades(obj)
            self.container = createContainer(trades, self.filterTrades)
            self.createCalcSpace(self.portfolioGrouper)
            positions = self.getPositionNodes()
            
            for portfolio, nodes in positions.iteritems():
                for (node, self.attributes) in nodes:
                    action = 'Deaggregating' if self.deaggregate \
                                else 'Aggregating'
                    print(action, ' trading portfolio:', portfolio.Name())
                    if self.attributes:
                        print(action, ' grouping position: ', self.attributes)
                    trades = node.Item().Trades().AsIndexedCollection()
                    self.aggregateBatch(trades, node)

    def aggregateBatch(self, trades, node):
        Logme()("Process %s trades in this batch" %
            trades.Size(), "DEBUG")
        if self.deaggregate:
            for aggTrade in trades:
                self.deaggregatePosition(aggTrade)
        else:
            aggInfo = self.getAggInfo(node, trades)
            self.aggregatePosition(node, trades[0].Portfolio(), aggInfo)
        acm.PollDbEvents()
        acm.Calculations().ResetEvaluatorBuilders()
        acm.Memory().GcWorldStoppedCollect()

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
        if self.deaggregate:
            #Aggregates need to be included if their date is less than
            #the aggregation date, for de-aggregation to work
            return FBDPCommon.toDate(trade.TradeTime()) <= self.date
        else:
            return FBDPCommon.toDate(trade.TradeTime()) > self.date
    
    def isAggregateTrade(self, trade):
        if self.deaggregate:
            return trade.Aggregate() == 0
        else:
            return trade.Aggregate() != 0

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
        for filterFunc in [self.isForwardTrade,
            self.isFutureTrade,
            self.isAggregateTrade,
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

    def deaggregatePosition(self, aggTrade):
        trades = self.findArchivedTradesFromAggTrade(aggTrade)
        abort = self.dearchiveTrades(trades, aggTrade)
        if not self.Testmode and not abort:
            if aggTrade.Aggregate() != 0:
                aggTrade.Delete()

    def applyPayments(self, aggTrade, aggInfo):
        return
        aggTrade = FBDPCommon.acm_to_ael(aggTrade).clone()
        payment = ael.Payment.new(aggTrade)
        payment.payday = aggTrade.acquire_day
        payment.valid_from = aggTrade.acquire_day
        payment.amount = aggInfo.funding
        payment.curr = FBDPCommon.acm_to_ael(aggInfo.cur)
        payment.ptynbr = aggTrade.counterparty_ptynbr
        payment.type = 'Aggregated Funding'
        payment.commit()

    def createNodeKeyFromAttributes(self, attribs, aggInfo):
        nodeKey = ''.join([str(attribs[key])
                    for key in sorted(attribs.iterkeys())])
        if 'CurrencyPair' in attribs and \
            'No Currency' not in attribs['CurrencyPair']:
            return nodeKey + self.date
        else:
            return nodeKey + aggInfo.Name() + self.date

    def createOrGetAggregateTrade(self, tradingPort, attribs, aggInfo):
        nodeKey = self.createNodeKeyFromAttributes(attribs, aggInfo)
        aggTrade = self.createNewAggTrade(tradingPort, aggInfo)
        Summary().ok(aggTrade, Summary().CREATE, aggTrade.Oid())
        return aggTrade

    def findArchivedTradesFromAggTrade(self, aggTrade):
        aelAggTrade = FBDPCommon.acm_to_ael(aggTrade)
        trades = aelAggTrade.reference_in(1)
        f = lambda x: (x.record_type == 'Trade' and x.aggregate_trdnbr and
                x.aggregate_trdnbr.trdnbr == aggTrade.Oid())
        trades = filter(f, trades)
        return trades

    def aggregatePosition(self, node, tradingPort, aggInfo):
        abort = 0
        newAggregateCreated = False
        inTransaction = False
        trades = aggInfo.Trades()
        try:
            aggTrade = self.createOrGetAggregateTrade(
                        tradingPort, self.attributes, aggInfo)
        except Exception as e:
            message = ('Failed to create new aggregate trade. '
                    'Got an exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            abort = 1
        
        #archive trades
        if not (abort or self.Testmode):
            try:
                ael.begin_transaction()
                inTransaction = True
                # update the empty aggregate's values in the same transaction
                # as archiving occurs
                self.archiveTradesAndInstruments(aggInfo.trades, aggTrade.Oid())
                self.applyPayments(aggTrade, aggInfo)
                #commit any remaining entities
                ael.commit_transaction()
                inTransaction = False
                newAggregateCreated = False
                
            except Exception as e:
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

    def dearchiveTrades(self, trades, aggTrade):
        try:
            for trade in trades:
                tradeClone = trade.clone()
                if tradeClone.aggregate == 0:
                    tradeClone.archive_status = 0
                else:
                    tradeClone.status = 'FO Confirmed'
                tradeClone.aggregate_trdnbr = None
                if not self.Testmode:
                    self.dearchiveAELObjects(trade.additional_infos())
                    self.dearchiveAELObjects(trade.payments())
                    tradeClone.commit()
                Logme()('Dearchive Trade %s' % trade.trdnbr, 'DEBUG')
                Summary().ok(trade, Summary().DEARCHIVE, trade.trdnbr)
            self.commitAddedEntities()
        except Exception as e:
            message = ('Failed to dearchiveTrades. '
                    'Exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            ael.abort_transaction()
            Summary().abortEntries()
            return 1

    def dearchiveAELObjects(self, objects):
        for obj in objects:
            objClone = obj.clone()
            objClone.archive_status = 0
            objClone.commit()
            Logme()('Dearchive %s %s' % (obj.record_type, obj.display_id()),
                    'DEBUG')
            Summary().ok(obj, Summary().DEARCHIVE, obj.display_id())

    def createNewAggTrade(self, tradingPort, aggInfo):
        trade = acm.FTrade()
        trade.Instrument(aggInfo.CommodityVariant())
        trade.Currency(aggInfo.Currency())
        trade.Quantity(aggInfo.Quantity())
        trade.Premium(aggInfo.CurrAmount())
        if math.fabs(aggInfo.Quantity()) > 0.0:
            trade.Price(math.fabs(aggInfo.CurrAmount()/aggInfo.Quantity()))

        # overridden from self.attributes if grouped on acq
        trade.Acquirer(DEFAULTPARTY)
        trade.Counterparty(DEFAULTPARTY)

        trade.Trader(acm.User())
        trade.Type('Aggregate')
        trade.Aggregate(2)
        trade.Status('Internal')

        trade.TradeTime(self.date)
        trade.AcquireDay(self.date)
        trade.ValueDay(self.date)
        self.setTradePropertiesFromGrouper(trade)
        trade.Portfolio(tradingPort)
        if not self.Testmode:
            trade.Commit()
        Logme()('Creating Aggregate Trade %s' % trade.Oid(), 'INFO')
        Logme()('Aggregate Trade Time %s' % trade.TradeTime(), 'INFO')
        return trade

    def setTradePropertiesFromGrouper(self, aggTrade):
        if self.attributes:
            for key, val in self.attributes.iteritems():
                try:
                    if key == 'Currency Split':
                        key = 'Currency'
                    aggTrade.SetProperty(key, val)
                except Exception as e:
                    msg = "Ignored setting {0} on trade as {1}".format(
                            key, str(e))
                    Logme()(msg, "INFO")

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

    def archiveTradesAndInstruments(self, trades, aggregate_trdnbr):
        instruments = acm.FSet()
        for trade in trades:
            self.archiveTradeAndChildren(trade, aggregate_trdnbr)
            if trade.TradeInstrumentType() != 'Curr':
                instruments.Add(trade.Instrument())

        instruments = filter(lambda x: not x.Trades(), instruments.AsList())
        for ins in instruments:
            aelIns = FBDPCommon.acm_to_ael(ins).clone()
            self.set_archive_status_recursive(aelIns)
            Summary().ok(ins, Summary().ARCHIVE, ins.Oid())

    def archiveTradeAndChildren(self, acmtrade, aggregate_trdnbr):
        aelTrade = FBDPCommon.acm_to_ael(acmtrade)
        trade = aelTrade.clone()
        if trade.aggregate == 0:
            trade.archive_status = 1
            self.archiveAELObjects(aelTrade.additional_infos())
            self.archiveAELObjects(aelTrade.payments())
        trade.aggregate_trdnbr = aggregate_trdnbr
        trade.commit()
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

    def commitAddedEntities(self, continueTransaction=0):
        try:
            if self.Testmode:
                ael.abort_transaction()
            else:
                ael.commit_transaction()
            self.nrOfArchivedObjects = 0
        except Exception as e:
            message = ('Failed to commitAddedEntities. '
                    'Got an exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            ael.abort_transaction()
            raise e
        if continueTransaction:
            ael.begin_transaction()

