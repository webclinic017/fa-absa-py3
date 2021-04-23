""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/archive_trades/FCashAggregationPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FCashAggregatePerform - Module which executes the cash aggregation

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import os
import os.path
import ael
import acm
import FBDPCommon

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
from FFxCommon import calcToNum, addDicToDic

DEFAULTPARTY = ael.Party['FMAINTENANCE']
DEFAULTSTATUS = 'FO Confirmed'
PAYMENT_ZERO_AMOUNT_TOLERANCE = 0.01

ACM_TO_AEL = {'Acquirer':'acquirer_ptynbr',
         'Broker':'broker_ptynbr',
         'Counterparty':'counterparty_ptynbr',
         'Trader':'trader_usrnbr',
         'Market':'market_ptynbr',
         'Currency':'curr',
         'Instrument':'insaddr',
         'OptKey1':'optkey1_chlnbr',
         'OptKey2':'optkey2_chlnbr',
         'OptKey3':'optkey3_chlnbr',
         'OptKey4':'optkey4_chlnbr'}

COL_CASH = 'Portfolio Accumulated Cash'
COL_VAL = 'Portfolio Value'
COL_FUNDING = 'Portfolio Funding'
COL_DIVIDENDS = 'Portfolio Dividends'
COL_PAYMENTS = 'Portfolio PL Period Payments'

COL_YTD_CASH = 'Portfolio Accumulated Cash Yearly'
COL_YTD_VAL = 'Portfolio Value Yearly'
COL_YTD_FUNDING = 'Portfolio Carry Yearly'
COL_YTD_DIVIDENDS = 'Portfolio Dividends Yearly'
COL_YTD_PAYMENTS = 'Portfolio PL Payments Yearly'

PL_COLUMNS = [COL_CASH, COL_FUNDING, COL_DIVIDENDS]

def perform(dictionary):
    Logme()('Cash Aggregation 4.24.1')
    day = FBDPCommon.toDate(dictionary['date'])
    Logme()('Cash Aggregation date:%s' % str(day))
    agg = FCashAggregation()
    agg.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')

def createContainer(trades, filterFn=None):
    unionObject = acm.FAdhocPortfolio()
    for trade in trades:
        if FBDPCommon.is_acm_object(trade):
            unionObject.Add(trade)
        else:
            acmTrade = FBDPCommon.ael_to_acm(trade)
            unionObject.Add(acmTrade)
    if filterFn:
        filterFn(unionObject.Trades())
    return unionObject

def createChainedGrouper(groupingNames):
    """
    Given the grouperNames, return a representing grouper for the default
    or built-in groupers specified in the list.
    """

    # Transform grouping name list into grouper list
    grouperList = []
    for g in groupingNames:
        if hasattr(g, 'IsKindOf') and g.IsKindOf(acm.FCurrencySplitGrouper):
            grouperList.append(g)
        else:
            attribute_grouper = acm.FAttributeGrouper(g)
            if attribute_grouper:
                grouperList.append(attribute_grouper)
            else:
                raise ValueError('Unable to construct attribute grouper for %s in %s' % (g, groupingNames))

    # Return the only grouper or the synthesised chained grouper from the list.
    if len(grouperList) == 1:
        return grouperList[0]
    return acm.CreateWithParameter('FChainedGrouper', grouperList)

def getAttributeFromMethodChain(acmObj, methodChain):
        methodChain = methodChain.split('.')
        getAtt = methodChain.pop()
        
        for m in methodChain:
            acmObj = acmObj.GetProperty(m)
            
        attr = acmObj.GetProperty(getAtt)
        if attr:
            return attr.Name()
        else:
            return None

def setAttributeFromMethodChain(aelObj, methodChain, attrValue):
        methodChain = methodChain.split('.')
        setAtt = methodChain.pop()
        setattr(aelObj, ACM_TO_AEL[setAtt], attrValue)
        return aelObj

class CashAggregationInfo():
    def __init__(self, bucket_date, cur, cash, val, dividends, funding, payments, trades, portfolio, attributes):
        self.bucket_date = bucket_date
        self.cur = cur
        self.cash = cash
        self.val = val
        self.dividends = dividends
        self.funding = funding
        self.payments = payments
        self.trades = trades
        self.portfolio = portfolio
        self.attributes = attributes

    def Cash(self):
        return self.cash
    
    def VAL(self):
        return self.val

    def Dividends(self):
        return self.dividends
        
    def Funding(self):
        return self.funding

    def Payments(self):
        return self.payments

    def Cur(self):
        return self.cur

    def Name(self):
        if self.cur:
            return self.cur.Name()
        return ''

    def Trades(self):
        return self.trades

    def AddTrade(self, t):
        self.trades.append(t)
    
    def Portfolio(self):
        return self.portfolio
        
    def Acquirer(self):
        return self.acquirer
        
    def Attributes(self):
        return self.attributes

class FCashAggregation():

    class TradeAttributeKeyChain(object):
        def __init__(self, trade, key_chain_attributes, key_currency=None, include_instrument=True):        
            self.key_currency = key_currency
            self.trade = trade
            self.key_chain_attributes = key_chain_attributes
            self.include_instrument = include_instrument
        
        @property
        def currency(self):
            return self.key_currency
    
        @property
        def attributes(self):
            return dict([(attr, getAttributeFromMethodChain(self.trade, attr)) for attr in self.key_chain_attributes])
    
        @property
        def key(self):
            curr_split_list = [self.key_currency] if self.key_currency else []
            ins_grouper = [self.trade.Instrument()] if self.include_instrument else []
            return tuple([self.trade.Portfolio().Name()] + [getAttributeFromMethodChain(self.trade, method_chain) for method_chain in self.key_chain_attributes] + ins_grouper + curr_split_list)

    def readArguments(self, args):
        param_date = FBDPCommon.toDate(args.get('date', acm.Time.DateToday()))
        if param_date > acm.Time.DateToday():
            raise Exception('Aggregation date cannot be in the future.')

        self.date = acm.Time.DateAddDelta(param_date, 0, 0, -1)
        self.deaggregate = args.get('deaggregate', 0)
        self.tradingObjects = []
        self.Testmode = args.get('Testmode', 1)
        self.tradingObjects = self.getTradingObjects(args)
        self.portfolioGrouperAttributes = args.get('PortfolioGrouperNativeAttributes', [])
        self.consolidate_cash = args.get('ConsolidateCash', False)
        #The preserve year end PnL function is disabled as the columns aren't built-in columns
        self.preserve_ytd_pnl = False
        self.date_eoy = acm.Time.DateAddDelta(acm.Time.FirstDayOfYear(param_date), 0, 0, -1)
        #print 'EOY DATE IS:', self.date_eoy
        self.preservePaymentTypes = args.get('PreservePaymentTypes', [])

    def getTradingObjects(self, dictionary):
        objects = acm.FArray()
        for field in ['TradeQuery', 'TradeFilter', 'TradingPortfolios']:
            objects.AddAll(dictionary.get(field, []))
        return objects

    def getTrades(self, obj):
        if obj.IsKindOf(acm.FPortfolio):
            return obj.Trades()
        elif obj.IsKindOf(acm.FStoredASQLQuery) and \
            obj.SubType() == 'FTrade':
            return obj.Query().Select()
        return []

    #returns a list of all instruments with zero positions in a given portfolio
    def getOpenPositions(self, portfolio):
        self.createCalcSpace(self.portfolioGrouper)
        return self.getPosition(self.topNode)
    
    def getPosition(self, node, attrs=[]):
        it = node.Iterator().FirstChild()
        openPositions = []
        while it:
            tree = it.Tree()
            item = tree.Item()
            if it.HasChildren():
                openPositions.extend(self.getPosition(tree, attrs[:] + [item]))
            else:                
                trades = item.Trades().AsList()
                pos = 0
                if trades.Size() > 0:
                    for trade in trades:
                        pos += trade.Quantity()
                if pos != 0:
                    takc = self.TradeAttributeKeyChain(trade, self.portfolioGrouperAttributes)
                    openPositions.append(takc.key)                    
                    #print 'open pos @ ', str(takc)
            it = it.NextSibling()
        return openPositions

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
        
    def _createCurrSplitGrouper(self):
        currSplitGrouper = acm.FCurrencySplitGrouper()
        currSplitGrouper.Label("Currency Split")        
        self.portfolioCurrSplitGrouper = createChainedGrouper(['Trade.Portfolio'] + self.portfolioGrouperAttributes + self.ins_grouper + [currSplitGrouper])
    
    def performProcess(self, args):
        # Read GUI parameter selection
        self.readArguments(args)                
        
        # Basic position grouper, based on trade attributes.  Used to find candidate zero positions
        self.portfolioGrouper = createChainedGrouper(['Trade.Portfolio'] + self.portfolioGrouperAttributes + ['Trade.Instrument'])
        
        # create the currency split grouper to preserve cash per currency
        # Instrument grouper to be bypassed if consolidating cash postings
        self.ins_grouper = [] if self.consolidate_cash else ['Trade.Instrument']        
        self._createCurrSplitGrouper()
                    
        # Perform the cash aggregation
        self.aggregate()

    def getCalculation(self, node, colName):
        val = self.calcSpace.CreateCalculation(node, colName)
        val = calcToNum(val.Value())
        return val

    def getColumnValue(self, node, column, curr):
        return self.getCalculation(node, column)
    
    def getParameterisedColumnValue(self, node, column, parameter):
        config = acm.Sheet().Column().ConfigurationFromVectorItem(parameter)
        return self.calcSpace.CalculateValue(node, column, config)

    def getPositionNodes(self, node, currency, positions, key_string):
        if not node:
            node = self.topNode
        it = node.Iterator().FirstChild()
        while it:
            tree = it.Tree()
            item = tree.Item()
            grouper = item.Grouping().Grouper()
            if grouper.IsKindOf(acm.FCurrencySplitGrouper):
                currency = item.StringKey()
                trades = item.Trades().AsList()
                if trades.Size() > 0:
                    include_instrument = False if self.consolidate_cash else True
                    takc = self.TradeAttributeKeyChain(trades[0], self.portfolioGrouperAttributes, currency, include_instrument)
                    portfolio = trades[0].Portfolio()
                    instrument = None if self.consolidate_cash else trades[0].Instrument()
                    positions.setdefault((portfolio, instrument), []).append((takc, tree))
            elif it.HasChildren():
                #print 'Iterate:', key_string + '|' + item.StringKey()
                self.getPositionNodes(tree, currency, positions, key_string + '|' + item.StringKey())
            it = it.NextSibling()
        return positions
    
    def getAggInfo(self, node, takc, trades, yearly=False):
        portfolio = trades[0].Portfolio()
        acquirer = trades[0].Acquirer()
        if yearly:
            cash = self.getColumnValue(node, COL_YTD_CASH, None)
            val = self.getColumnValue(node, COL_YTD_VAL, None)
            funding = self.getColumnValue(node, COL_YTD_FUNDING, None)
            dividends = self.getColumnValue(node, COL_YTD_DIVIDENDS, None)
        else:
            cash = self.getColumnValue(node, COL_CASH, None)
            val = self.getColumnValue(node, COL_VAL, None)
            funding = self.getColumnValue(node, COL_FUNDING, None)
            dividends = self.getColumnValue(node, COL_DIVIDENDS, None)
        
        # Preserve certain payment types
        payments = {}
        for payment_type in self.preservePaymentTypes:
            payment_type_param = acm.FNamedParameters()
            payment_type_enum = acm.EnumFromString('PaymentType', payment_type)
            payment_type_param.AddParameter('paymentType', payment_type_enum)
            if yearly:
                _payment = self.getParameterisedColumnValue(node, COL_YTD_PAYMENTS, payment_type_param)
            else:
                _payment = self.getParameterisedColumnValue(node, COL_PAYMENTS, payment_type_param)
            payment_amount = calcToNum(_payment.Value())
            payments[payment_type] = payment_amount
            cash -= payment_amount
        
        bucket_date = self.date_eoy if self.preserve_ytd_pnl and not yearly else self.date
        aggInfo = CashAggregationInfo(bucket_date, takc.currency, cash, val,
                                    dividends, funding, payments, trades, portfolio, takc.attributes)
        return aggInfo

    def aggregate(self):
        for obj in self.tradingObjects:
            trades = self.getTrades(obj)
            self.openPositions = None
            self.container = createContainer(trades, self.filterTrades)            
            self.openPositions = self.getOpenPositions(self.container) #obj
            self.container = createContainer(trades, self.filterTrades)
            self.createCalcSpace(self.portfolioCurrSplitGrouper)
            positions = self.getPositionNodes(None, None, {}, '')
            self.printCashBalance(positions)
            aggTrades = []
            # Gather all the calculated values and attributes
            # for the positions using a constant snapshot.            
            for address, posinfo in positions.items():
                portfolio, instrument = address
                # Cash (de-)aggregation should be transactional per portfolio per instrument
                if not posinfo:
                    continue
                    
                aggInfos = []
                for trade_attribute_key_chain, node in posinfo:
                    print('trade_attribute_key_chain', trade_attribute_key_chain.key)
                    action = 'Deaggregating' if self.deaggregate else 'Aggregating'
                    trades = node.Item().Trades().AsIndexedCollection()
                    if self.deaggregate:
                        for aggTrade in trades: 
                            self.deaggregatePosition(aggTrade)
                    else:
                        aggInfo = self.getAggInfo(node, trade_attribute_key_chain, trades)
                        if self.preserve_ytd_pnl:
                            aggInfoYTD = self.getAggInfo(node, trade_attribute_key_chain, trades, yearly=True)
                        else:
                            aggInfoYTD = None
                        
                        aggInfos.append((aggInfo, aggInfoYTD))
                
                if not self.deaggregate:
                    try:
                        ael.begin_transaction()
                        # Perform the aggregation and archiving on the snapshot
                        for aggInfo, aggInfoYTD in aggInfos:
                            aggTrade = self.createOrGetAggregateTrade(aggInfo)
                            self.aggregatePosition(aggInfo, aggInfoYTD, aggTrade)
                            aggTrades.append(aggTrade)
                        ael.commit_transaction()
                    except Exception as e:                    
                        message = ('Failed to aggregate trades. '
                                'Exception: {0}'.format(e))
                        Logme()(message, 'ERROR')
                        Logme()("Aborting transaction.", "ERROR")
                        ael.abort_transaction()
                        Summary().abortEntries()

            acm.PollDbEvents()
            ael.poll()
            #report pl before archiving
            self.container = createContainer(aggTrades, None)
            self.createCalcSpace(self.portfolioCurrSplitGrouper)
            positions = self.getPositionNodes(None, None, {}, '')
            self.printCashBalance(positions)

    def isAggregate(self, trade):
        if self.deaggregate:
            # if de-aggregating, we only consider type 2, Cash posting trades
            if trade.Aggregate() == 2 and trade.Type() == "Cash Posting":
                return True
            else:
                return False
        else:
            #if aggregating, we only consider type 2, and those that aren't cash postings
            if trade.Aggregate() == 2 and trade.Type() != "Cash Posting":
                return True
            else:
                return False
    
    def isNotAggregate(self, trade):
        return not self.isAggregate(trade)
    
    def isInactiveAggregate(self, trade):
        if trade.Aggregate() == 5:
            return True
        else:
            return False

    def isAggregateTradeWithForwardPayment(self, trade):
        if self.isAggregate(trade) and (trade.AcquireDay() <= self.date):
            for p in trade.Payments():
                if p.PayDay() > self.date:
                    print('*** Aggregate trade {0} excluded because it has forward payments'.format(trade.Oid()))
                    return True
        return False

    def isForwardTrade(self, trade):
        #compares value date
        if self.deaggregate:
            #Aggregates need to be included if their date is less than
            #the aggregation date, for de-aggregation to work
            return trade.Aggregate() != 5 and trade.AcquireDay() <= self.date
        else:
            return trade.AcquireDay() > self.date

    def isFutureTrade(self, trade):
        #compares trade time
        if self.deaggregate:
            #Aggregates need to be included if their date is less than
            #the aggregation date, for de-aggregation to work
            return trade.Aggregate() != 5 and FBDPCommon.toDate(trade.TradeTime()) <= self.date
        else:
            return FBDPCommon.toDate(trade.TradeTime()) > self.date
    
    def isInOpenPosition(self, trade):
        retval = True
        if self.deaggregate:
            if trade.Aggregate() == 0 and trade.Type() == "Cash Posting":
                retval = False
        if self.openPositions:
            takc = self.TradeAttributeKeyChain(trade, self.portfolioGrouperAttributes)
            if takc.key in self.openPositions:
                retval = True
            else:
                retval = False
        else:
            retval = False
        return retval

    def filterTrades(self, trades):
        hook = None
        totalrefs = acm.FIdentitySet()
        for filterFunc in [self.isForwardTrade,
            self.isFutureTrade, 
            self.isInactiveAggregate,
            self.isInOpenPosition,
            self.isNotAggregate,
            self.isAggregateTradeWithForwardPayment,
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
            aggTrade.Delete()

    def applyPayments(self, aggTrade, aggInfo, aggInfoYTD):
        #aggTrade = aggTrade.clone()
        funding_deduct = 0.0
        dividends_deduct = 0.0
        cash_deduct = 0.0
        payment_deduct = {}
        # YTD payments
        if aggInfoYTD:
            funding_deduct = aggInfoYTD.funding            
            if abs(aggInfoYTD.funding) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
                payment = ael.Payment.new(aggTrade)
                payment.payday = ael.date(aggInfoYTD.bucket_date)
                payment.valid_from = ael.date(aggInfoYTD.bucket_date)
                payment.amount = aggInfoYTD.funding
                payment.curr = ael.Instrument[aggInfoYTD.cur]
                payment.ptynbr = aggTrade.counterparty_ptynbr
                payment.type = 'Funding'
                payment.commit()
                    
            dividends_deduct = aggInfoYTD.dividends
            if abs(aggInfo.dividends) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
                payment2 = ael.Payment.new(aggTrade)
                payment2.payday = ael.date(aggInfoYTD.bucket_date)
                payment2.valid_from = ael.date(aggInfoYTD.bucket_date)
                payment2.amount = aggInfoYTD.dividends
                payment2.curr = ael.Instrument[aggInfoYTD.cur]
                payment2.ptynbr = aggTrade.counterparty_ptynbr
                payment2.type = 'Aggregated Dividends'
                payment2.commit()
            
            cash_amount_ytd = aggInfoYTD.cash - (aggInfoYTD.dividends + aggInfoYTD.funding) + aggInfoYTD.val
            cash_deduct = cash_amount_ytd
            if abs(cash_amount_ytd) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
                payment3 = ael.Payment.new(aggTrade)
                payment3.payday = ael.date(aggInfoYTD.bucket_date)
                payment3.valid_from = ael.date(aggInfoYTD.bucket_date)
                payment3.amount = cash_amount_ytd
                payment3.curr = ael.Instrument[aggInfoYTD.cur]
                payment3.ptynbr = aggTrade.counterparty_ptynbr
                payment3.type = 'Cash'
                payment3.commit()
            
            for payment_type, payment_amount in aggInfoYTD.Payments().items():
                payment_deduct[payment_type] = payment_amount
                if abs(payment_amount) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
                    agg_payment = ael.Payment.new(aggTrade)
                    agg_payment.payday = ael.date(aggInfoYTD.bucket_date)
                    agg_payment.valid_from = ael.date(aggInfoYTD.bucket_date)
                    agg_payment.amount = payment_amount                    
                    agg_payment.curr = ael.Instrument[aggInfoYTD.cur]
                    agg_payment.ptynbr = aggTrade.counterparty_ptynbr
                    agg_payment.type = payment_type
                    agg_payment.commit()
                
        # Main payments
        if abs(aggInfo.funding) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
            payment = ael.Payment.new(aggTrade)
            payment.payday = ael.date(aggInfo.bucket_date)
            payment.valid_from = ael.date(aggInfo.bucket_date)
            payment.amount = aggInfo.funding - funding_deduct
            payment.curr = ael.Instrument[aggInfo.cur]
            payment.ptynbr = aggTrade.counterparty_ptynbr
            payment.type = 'Aggregated Funding'
            payment.commit()
        
        if abs(aggInfo.dividends) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
            payment2 = ael.Payment.new(aggTrade)
            payment2.payday = ael.date(aggInfo.bucket_date)
            payment2.valid_from = ael.date(aggInfo.bucket_date)
            payment2.amount = aggInfo.dividends - dividends_deduct
            payment2.curr = ael.Instrument[aggInfo.cur]
            payment2.ptynbr = aggTrade.counterparty_ptynbr
            payment2.type = 'Aggregated Dividends'
            payment2.commit()

        cash_amount = aggInfo.cash - (aggInfo.dividends + aggInfo.funding) + aggInfo.val
        if abs(cash_amount) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
            payment3 = ael.Payment.new(aggTrade)
            payment3.payday = ael.date(aggInfo.bucket_date)
            payment3.valid_from = ael.date(aggInfo.bucket_date)
            payment3.amount = cash_amount - cash_deduct
            payment3.curr = ael.Instrument[aggInfo.cur]
            payment3.ptynbr = aggTrade.counterparty_ptynbr
            payment3.type = 'Cash'
            payment3.commit()

        for payment_type, payment_amount in aggInfo.Payments().items():
            net_payment_amount = payment_amount - payment_deduct.get(payment_type, 0.0)
            if abs(net_payment_amount) >= PAYMENT_ZERO_AMOUNT_TOLERANCE:
                agg_payment = ael.Payment.new(aggTrade)
                agg_payment.payday = ael.date(aggInfo.bucket_date)
                agg_payment.valid_from = ael.date(aggInfo.bucket_date)
                agg_payment.amount = net_payment_amount
                agg_payment.curr = ael.Instrument[aggInfo.cur]
                agg_payment.ptynbr = aggTrade.counterparty_ptynbr
                agg_payment.type = payment_type
                agg_payment.commit()

    def createOrGetAggregateTrade(self, aggInfo):
        aggTrade = self.createNewAggTrade(aggInfo)
        Summary().ok(aggTrade, Summary().CREATE, aggTrade.trdnbr)
        return aggTrade

    def findArchivedTradesFromAggTrade(self, aggTrade):
        aelAggTrade = FBDPCommon.acm_to_ael(aggTrade)
        trades = aelAggTrade.reference_in(1)
        f = lambda x: (x.record_type == 'Trade' and x.aggregate_trdnbr and
                x.aggregate_trdnbr.trdnbr == aggTrade.Oid())
        trades = filter(f, trades)
        return trades

    def aggregatePosition(self, aggInfo, aggInfoYTD, aggTrade):
        #archive trades
        if not self.Testmode:
            # update the empty aggregate's values in the same transaction
            # as archiving occurs                
            self.archiveTradesAndInstruments(aggInfo.trades, aggTrade.trdnbr)
            self.applyPayments(aggTrade, aggInfo, aggInfoYTD)

    def dearchiveTrades(self, trades, aggTrade):
        try:
            ael.begin_transaction()
            for trade in trades:
                tradeClone = trade.clone()
                if tradeClone.aggregate == 0:
                    tradeClone.archive_status = 0
                elif tradeClone.aggregate == 5:
                    tradeClone.aggregate = 2
                elif tradeClone.aggregate == 2 and tradeClone.status == 'Void': 
                    tradeClone.status = 'FO Confirmed'
                tradeClone.aggregate_trdnbr = None
                if not self.Testmode:
                    self.dearchiveAELObjects(trade.additional_infos())
                    self.dearchiveAELObjects(trade.payments())
                    tradeClone.commit()
                Logme()('Dearchive Trade %s' % trade.trdnbr, 'DEBUG')
                Summary().ok(trade, Summary().DEARCHIVE, trade.trdnbr)
            self.commitAddedEntities()
            return 0
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
    
    def createNewAggTrade(self, aggInfo):
        #use ael to commit inside the transaction
        curr = ael.Instrument[aggInfo.cur]
        trade = ael.Trade.new(curr)
        trade.curr = curr

        # overridden from aggInfo.attributes if grouped on acq or cpty
        #trade.Acquirer(aggInfo.Acquirer())
        trade.counterparty_ptynbr = ael.Party['FMAINTENANCE']
        trade.acquirer_ptynbr = ael.Party['FMAINTENANCE']
        trade.trader_usrnbr = ael.userid()
        trade.type = 'Cash Posting'
        trade.quantity = 0
        trade.aggregate = 2
        trade.status = DEFAULTSTATUS
        date = ael.date(aggInfo.bucket_date)
        time = date.to_time()
        trade.time = time
        trade.acquire_day = date
        trade.value_day = date
        trade.prfnbr = aggInfo.Portfolio().Oid()
        
        for methodChain, value in aggInfo.Attributes().items():
            setAttributeFromMethodChain(trade, methodChain, value)
                
        if not self.Testmode:
            trade.commit()
        Logme()('Creating Aggregate Trade %s' % trade.trdnbr, 'INFO')
        Logme()('Aggregate Trade Time %s' % trade.time, 'INFO')
        return trade

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
            Logme()('Archive Trade %s' % aelTrade.trdnbr, 'DEBUG')
        else:
            trade.aggregate = 5
            Logme()('Marked Aggregate Trade %s as inactive.' % aelTrade.trdnbr, 'DEBUG')
        trade.aggregate_trdnbr = aggregate_trdnbr
        trade.commit()
        Summary().ok(trade, Summary().ARCHIVE, aelTrade.trdnbr)

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
                    'Exception: {0}'.format(e))
            Logme()(message, 'ERROR')
            ael.abort_transaction()
            raise e
        if continueTransaction:
            ael.begin_transaction()
    
    def printCashBalance(self, positions):
        cols = PL_COLUMNS
        print('printCashBalance')
        for address, posinfo in positions.items():
            for trade_attribute_key_chain, node in posinfo:
                print(trade_attribute_key_chain.key)
                self.printTree(node, cols, currencies=trade_attribute_key_chain.currency)

    def printTree(self, node, colNames=["Portfolio Projected Payments"],
            max_depth=0, start_depth=0, currencies=None):
        if Logme().LogMode < 2:
            return
        if not start_depth:
            start_depth = node.Depth()
        if type(currencies) == type(acm.FCurrency()):
            currencies = [currencies]
        elif not currencies:
            currencies = [acm.ObjectServer().UsedValuationParameters(
                    ).AccountingCurrency()]

        values = []
        for name in colNames:
            #self.setColumnConfig(currencies)
            val = self.getCalculation(node, name)
            values.append(val)

        Logme()("%s (Node Level %s) %s => %s : %s " %
                (" " * (node.Depth() - start_depth) * 5, node.Depth(),
                node.Item().StringKey(), str(colNames), str(values)), "DEBUG")

        if (node.Iterator().HasChildren() and
                (not max_depth or node.Depth() <= max_depth)):
            child = node.Iterator().FirstChild()
            while child:
                self.printTree(child.Tree(), colNames, max_depth, start_depth,
                        currencies)
                child = child.NextSibling()
