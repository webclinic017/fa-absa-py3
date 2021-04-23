""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/BuySide/FFxSpotRolloverPerformBuySide.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFxSpotRolloverPerformBuySide

DESCRIPTION

----------------------------------------------------------------------------"""

#Import builtin modules
import math

#Import Front modules
import acm
import ael

import FFxCommonBuySide
import FBDPString
import FBDPRollback
import FBDPCommon
import FBDPCustomPairDlg

Summary = FBDPCommon.Summary
logme = FBDPString.logme

CurrencyPair = 'CurrencyPair'

HistoricalFinancing_None = 'None'
HistoricalFinancing_Simple = 'Simple'
HistoricalFinancing_Continuous = 'Continuous'
HistoricalFinancing_NotSet = 'Not Set'
HistoricalFinancing_DailyCompounding = 'Daily Compounding'
HistoricalFinancingEnum = (HistoricalFinancing_None,
        HistoricalFinancing_Simple,
        HistoricalFinancing_Continuous,
        HistoricalFinancing_NotSet,
        HistoricalFinancing_DailyCompounding)
HistoricalFinancingInstrumentName = 'HISTORICAL_FINANCING'


def perform_swap_rollover(args):
    r = SwapRollover('FxSpotRolloverSwapFunding', args['Testmode'], args)
    r.perform(args)
    r.end()


class Rollover(FBDPRollback.RollbackWrapper,
        FFxCommonBuySide.FxPortfolioProcess):

    def getCurrObjects(self, currPair):

        if currPair:
            return [currPair]
        else:
            query = ""
        return acm.FCurrency.Select(query)

    def perform(self, args):

        self.performProcess(args)

    def getRatesAndDates(self, args=[]):
        res = FBDPCustomPairDlg.FX_TABLE
        if res:
            return res
        if args:
            return args.get('BrokerRates', [])
        return []

    def maxOfNearDates(self):
        try:
            date = max([row[5] for row in self.brokerRates])
            return FBDPCommon.toDate(date)
        except:
            return acm.Time.DateValueDay()

    def readArguments(self, args):

        calcvalparm = acm.UsedValuationParameters()
        logme('Using valuation parameters: "%s".   Forward start PL: %i' % (
                calcvalparm.Name(), calcvalparm.ForwardStartPL()), 'DEBUG')
        self.accCurr = calcvalparm.AccountingCurrency()
        self.tradingCalendar = self.accCurr.Calendar()
        if 'TradingCalendar' in args and args['TradingCalendar']:
            self.tradingCalendar = args['TradingCalendar'][0]
        self.tradingObjects = self.getTradingObjects(args)
        self.brokerRates = self.getRatesAndDates(args)
        self.nextTradingDate = self.maxOfNearDates()
        self.portfolioGrouper = ('PortfolioGrouper' in args and
                args['PortfolioGrouper'])
        self.defaultPortfolio = args['DefaultPortfolio'][0]
        self.defaultAcquirer = args['DefaultAcquirer'][0]
        self.counterparty = args['Counterparty'][0]
        self.rollNotNeeded = args['RollNotNeeded']

    def getBroker(self):

        try:
            return self.attributes['Broker']
        except KeyError:
            return None

    def getCounterparty(self):

        return self.counterparty

    def getNearDatePerBrokerAndPair(self, currPair, broker):

        try:
            pairname = currPair.Name()
            for row in self.brokerRates:
                if row[0] == pairname and row[1] == broker:
                    return FBDPCommon.toDate(row[5])
        except IndexError:
            return None

    def aggregate(self, _dict, key, value, grouper_size, i, currInfo=None,
            rollDate=None):

        _dict.setdefault(key, value)
        while i < grouper_size:
            try:
                self.aggregate(_dict[self.attributes[self.grouper_values[i]]],
                        self.attributes[self.grouper_values[i + 1]], {},
                        grouper_size, i + 1, currInfo, rollDate)
                return
            except IndexError:
                if rollDate:
                    if (not isinstance(_dict[self.attributes[self.grouper_values[i]]], type([]))):
                        _dict[self.attributes[self.grouper_values[i]]] = [0,
                                rollDate, currInfo]
                i += 1
            except KeyError:
                self.aggregate(_dict[currInfo.currPair.Name()],
                        self.attributes[self.grouper_values[i + 1]], {},
                        grouper_size, i + 1, currInfo, rollDate)
                return

    def update_attributes(self):

        i = len(self.grouping_values_list) - 1
        for v in reversed(self.grouper_values[1:]):
            if i >= 0:
                self.attributes[v] = self.grouping_values_list[i]
                i -= 1
            else:
                break

    def update_market_attributes(self, pair, broker):

        try:
            self.attributes['CurrencyPair'] = pair
        except KeyError:
            pass
        try:
            self.attributes['Broker'] = broker
        except KeyError:
            pass

    def rollCashflowAggregated(self, _dict, tradingPortfolio, market=None):

        for key in _dict:
            self.grouping_values_list.append(key)
            if isinstance(_dict[key], type({})):
                self.rollCashflowAggregated(_dict[key], tradingPortfolio,
                        market)
            else:
                cashflow = _dict[key][0]
                rollDate = _dict[key][1]
                currInfo = _dict[key][2]
                self.update_attributes()
                if cashflow and math.fabs(cashflow) > 0.0001:
                    if not market:
                        result = self.rollCashflow(currInfo, cashflow,
                                rollDate, tradingPortfolio)
                    else:
                        result = self.rollCashflow(currInfo, cashflow,
                                rollDate, tradingPortfolio, market)
                    if not result:
                        self.resultNotOk.append(0)
                    acm.PollDbEvents()
                del self.grouping_values_list[:]

    def rollMarketCashflow(self, aggregated_market_prf, tradingPortfolio):

        for pair in aggregated_market_prf:
            for broker in aggregated_market_prf[pair]:
                for cparty in aggregated_market_prf[pair][broker]:
                    cashflow = aggregated_market_prf[pair][broker][cparty][0]
                    rollDate = aggregated_market_prf[pair][broker][cparty][1]
                    currInfo = aggregated_market_prf[pair][broker][cparty][2]
                    self.update_market_attributes(pair, broker)
                    if cashflow and math.fabs(cashflow) > 0.0001:
                        result = self.rollCashflow(currInfo, cashflow,
                                rollDate, tradingPortfolio, 1)
                        if not result:
                            self.resultNotOk.append(0)
                        acm.PollDbEvents()

    def processPortfolio(self, tradingPortfolio, nodes, aggregated_market_prf,
            counter, size):

        FFxCommonBuySide.printEmp('Rolling trading portfolio: "%s".' % (
                tradingPortfolio.Name()), '*')
        needToReprocess = False
        changed = False
        today = acm.Time.DateValueDay()
        grouper_size = len(self.grouper_values)
        self.resultNotOk = []
        aggregated_result_prf = {}
        aggregated_result_prf_test = {}
        for (topNode, self.attributes) in nodes:
            if self.attributes:
                FFxCommonBuySide.printEmp('Rolling grouping position: %s' %
                        (self.attributes), '=')
            rollDate = self.tradingCalendar.AdjustBankingDays(today, 1)
            currPairs = []
            if CurrencyPair in self.attributes:
                val = self.attributes[CurrencyPair]
                currPair = acm.FCurrencyPair[val]
                if currPair is not None:
                    if currPair not in currPairs:
                        currPairs.append(currPair)
            currPair = tradingPortfolio.CurrencyPair()
            currObjects = []
            if currPair is not None:
                currObjects.append(currPair)
            for currPair in currPairs:
                if currPair is not None:
                    if currPair not in currObjects:
                        currObjects.append(currPair)
            if len(currObjects) == 0:
                currObjects = self.getCurrObjects(currPair)
                message = ('Portfolio %s has no currency pair or currency '
                        'pair groupers.' % (tradingPortfolio.Name()))
                logme(message, 'WARNING')
                message = ('Portfolio "%s" rolling by individual currencies.' %
                        (tradingPortfolio.Name()))
                logme(message, 'INFO')
            if 'currInfoList' not in dir(self):
                self.currInfoList = []
            try:
                self.currInfoList = self.createCurrInfos(currObjects,
                        tradingPortfolio)
            except Exception, ex:
                Summary().fail(tradingPortfolio, Summary().ROLL, str(ex),
                        tradingPortfolio.Name())
                return False
            if 'procList' not in dir(self):
                self.procList = []
            for currInfo in self.currInfoList:
                broker = self.getBroker()
                if (self.rollNotNeeded == 'True' and
                        not self.getNearRatePerBrokerAndPair(currInfo,
                        broker)):
                    message = ('No FX rate is specified for the currency pair'
                            ' "{0}" and broker "{1}". The position will not '
                            'be rolled.'.format(currInfo.currPair.Name(),
                            broker))
                    logme(message, 'INFO')
                    continue
                cparty = self.getCounterpartyPerBrokerAndPair(
                        currInfo.currPair, broker)
                if not cparty:
                    cparty = broker
                rollDate = self.getNearDatePerBrokerAndPair(currInfo.currPair,
                        broker)
                if not rollDate:
                    if 'CAD' in currInfo.currencies():
                        rollDate = today
                    else:
                        rollDate = self.tradingCalendar.AdjustBankingDays(
                               today, 1)
                changed = False
                processedKey = self.attributes.copy()
                if currInfo.currPair is not None:
                    processedKey['CurrencyPair'] = currInfo.currPair.Name()
                else:
                    processedKey['Currency'] = currInfo.rollCurr.Name()
                acm.PollDbEvents()
                cashflow = self.getCashflow(topNode, day=rollDate,
                        configCurr=currInfo.rollCurr)
                if cashflow and math.fabs(cashflow) > 0.0001:
                    #trader prf ditionary
                    self.aggregate(aggregated_result_prf,
                            currInfo.currPair.Name(), {}, grouper_size, 1,
                            currInfo, rollDate)
                    aggregated_result_prf_temp = aggregated_result_prf
                    aggregated_result_prf_temp = aggregated_result_prf_temp[
                            currInfo.currPair.Name()]
                    for i in self.grouper_values[2:]:
                        aggregated_result_prf_temp = (
                                aggregated_result_prf_temp[self.attributes[i]])
                    if aggregated_result_prf_temp:
                        aggregated_result_prf_temp[0] += cashflow
                    #market prf dictionary
                    aggregated_market_prf.setdefault(currInfo.currPair.Name(),
                            {}).setdefault(broker, {}).setdefault(cparty, [0,
                            rollDate, currInfo])
                    aggregated_market_prf[currInfo.currPair.Name()][broker][
                            cparty][0] += cashflow
        self.grouping_values_list = []
        self.rollCashflowAggregated(aggregated_result_prf, tradingPortfolio)
        if counter == size:
            self.rollMarketCashflow(aggregated_market_prf, tradingPortfolio)
        self.calcSpace.Refresh()
        if not self.resultNotOk:
            Summary().ok(tradingPortfolio, Summary().ROLL)
        else:
            Summary().fail(tradingPortfolio, Summary().ROLL,
                    'All positions not rolled', tradingPortfolio.Name())
        Summary().commitEntries()
        return needToReprocess

    def createCurrInfos(self, currObjects, tradingPortfolio):

        raise 'Must override createCurrInfos function'

    def rollCashflow(self, currInfo, cashflow, fromDate, tradingPortfolio,
            market=None):

        raise 'Must override rollCashflow function'

    def getTradeAcquirer(self, tradingPortfolio):
        acquirer = tradingPortfolio.PortfolioOwner()
        if not acquirer:
            acquirer = self.defaultAcquirer
            logme('No owner specified for trading portfolio %s.' %
                    tradingPortfolio.Name(), 'INFO')
            logme('Using default funding acquirer %s as the acquirer for the '
                    'trade.' % acquirer.Name(), 'INFO')
        return acquirer


class SwapRollover(Rollover):

    FXProcessType = "FxSpotRolloverSwapFunding"

    def createCurrInfos(self, currObjects, tradingPortfolio):

        currInfoList = []
        for currObj in currObjects:
            if currObj.IsKindOf(acm.FCurrencyPair):
                cc = self.getCounterCurrencyOfCurrPair(currObj)
                rc = currObj.Currency1()
                if rc == cc:
                    rc = currObj.Currency2()
                currInfo = CurrInfo(rc, cc, currObj)
                currInfoList.append(currInfo)
        splitCurrInfoList = []
        for currInfo in currInfoList:
            fundPort, fundAcq = self.getPortfolioAndAcquirer()
            currInfo.fundPort = fundPort
            currInfo.fundAcq = fundAcq
            if not currInfo.fundPort:
                currInfo.fundPort = self.getDefaultPortfolio()
            if not currInfo.fundAcq:
                currInfo.fundAcq = self.getDefaultAcquirer()
            splitCurr = currInfo.getSplittingCurrency()
            if splitCurr:
                splitCurrInfo = CurrInfo(currInfo.counterCurr, splitCurr)
                splitCurrInfoList.insert(0, splitCurrInfo)
                lookupCurrencyPair = FFxCommonBuySide.currencyPair(
                        currInfo.rollCurr, splitCurr)
                if lookupCurrencyPair is None:
                    message = 'Currency Pair for %s/%s does not exist.' % (
                            currInfo.rollCurr.Name(), splitCurr.Name())
                    raise Exception(message)
                splitCurrInfo.currPair = lookupCurrencyPair
                splitCurrInfo.rollCurr = currInfo.rollCurr
                splitFundPort = self.getDefaultPortfolio()
                splitFundAcq = self.getDefaultAcquirer()
                if (not splitFundPort.CurrencyPair() or self.currPairIncludes(
                        splitFundPort.CurrencyPair(), splitCurr,
                        currInfo.counterCurr)):
                    splitCurrInfo.fundPort = splitFundPort
                    splitCurrInfo.fundAcq = splitFundAcq
                else:
                    if self.currPairIncludes(splitFundPort.CurrencyPair(),
                            currInfo.rollCurr, splitCurr):
                        splitCurrInfo.fundPort = currInfo.fundPort
                        splitCurrInfo.fundAcq = splitFundAcq
                        currInfo.fundPort = splitFundPort
                        currInfo.fundAcq = splitFundAcq
                    else:
                        message = ('Funding portfolio %s for splitting '
                                'currency %s has mismatching CurrencyPair' % (
                                splitFundPort.Name(), splitCurr.Name()))
                        raise Exception(message)
                #now update the currInfo object for the split roll
                lookupCurrencyPair = FFxCommonBuySide.currencyPair(
                        currInfo.counterCurr, splitCurr)
                if lookupCurrencyPair is None:
                    message = ('Currency Pair for %s/%s does not exist.' %
                            (currInfo.counterCurr.Name(), splitCurr.Name()))
                    raise Exception(message)

                currInfo.rollCurr = currInfo.counterCurr
                currInfo.counterCurr = splitCurr
                currInfo.currPair = lookupCurrencyPair
                fundPort, fundAcq = self.getPortfolioAndAcquirer()
                #update the funding portfolio for the new ccy pair
                currInfo.fundPort = fundPort
                currInfo.fundAcq = fundAcq
        currInfoList = splitCurrInfoList.__add__(currInfoList)
        return currInfoList

    def currPairIncludes(self, currPair, curr1, curr2):
        if currPair.Currency1() == curr1 and currPair.Currency2() == curr2:
            return True
        if currPair.Currency1() == curr2 and currPair.Currency2() == curr1:
            return True
        return False

    def getNearRatePerBrokerAndPair(self, currInfo, broker):
        try:
            pairname = currInfo.currPair.Name()
            for row in self.brokerRates:
                if row[0] == pairname and row[1] == broker:
                    return float(row[3])
        except:
            return None

    def getFarRatePerBrokerAndPair(self, currInfo, broker):
        try:
            pairname = currInfo.currPair.Name()
            for row in self.brokerRates:
                if row[0] == pairname and row[1] == broker:
                    return float(row[4])
        except:
            return None

    def getFarDatePerBrokerAndPair(self, currPair, broker):

        try:
            pairname = currPair.Name()
            for row in self.brokerRates:
                if row[0] == pairname and row[1] == broker:
                    return FBDPCommon.toDate(row[6])
        except IndexError:
            return None

    def getCounterpartyPerBrokerAndPair(self, currPair, broker):

        try:
            pairname = currPair.Name()
            for row in self.brokerRates:
                if row[0] == pairname and row[1] == broker:
                    return row[2]
        except IndexError:
            return None

    def rollCashflow(self, currInfo, cashflow, fromDate, tradingPortfolio,
            market=None):

        nearPrice = None
        farPrice = None
        cparty = None
        toDate = None
        broker = self.getBroker()
        counterparty = self.getCounterparty()
        if self.brokerRates:
            nearPrice = self.getNearRatePerBrokerAndPair(currInfo, broker)
            farPrice = self.getFarRatePerBrokerAndPair(currInfo, broker)
            toDate = self.getFarDatePerBrokerAndPair(currInfo.currPair, broker)
            cparty = self.getCounterpartyPerBrokerAndPair(currInfo.currPair,
                    broker)
        if not toDate:
            #currInfo.currPair.SpotDate(fromDate)
            toDate = self.tradingCalendar.AdjustBankingDays(fromDate, 1)
        logme('Roll %s from %s to %s for cashflow % 18.4f.' %
                (currInfo.rollCurr.Name(), fromDate, toDate, cashflow), 'INFO')
        if not farPrice:
            farPrice = currInfo.getFxRate()
            if not farPrice:
                logme('Could not get fx rate for %s' %
                        currInfo.rollCurr.Name(), 'ERROR')
                return False
            if cashflow < 0.0:
                discountFactor = currInfo.getDiscountFactor(fromDate, toDate,
                        'Ask')
            else:
                discountFactor = currInfo.getDiscountFactor(fromDate, toDate,
                        'Bid')
            if discountFactor == None:
                logme('Could not get funding for %s' %
                        currInfo.rollCurr.Name(), 'ERROR')
                return False
            nearPrice = farPrice * discountFactor
        self.beginTransaction()
        curr1 = currInfo.currPair.Currency1()
        curr2 = currInfo.currPair.Currency2()
        if not market:
            # Creating Swap trade Near Leg
            rolloverTrade = self.createNearTrade(curr1, curr2, cashflow,
                    nearPrice, tradingPortfolio, currInfo.fundPort,
                    counterparty, fromDate, currInfo.rollCurr)
            #rolloverTrade.MirrorPortfolio(currInfo.fundPort)
            rolloverMirrorTrade = self.createMirrorTrade(rolloverTrade,
                    currInfo.fundPort)
            # Creating Swap trade Far Leg
            farRolloverTrade = self.createFarTrade(rolloverTrade, farPrice,
                    toDate, currInfo.rollCurr)
            farRolloverTrade.ConnectedTrade(rolloverTrade)
            #farRolloverTrade.MirrorPortfolio(currInfo.fundPort)
            farRolloverMirrorTrade = self.createMirrorTrade(farRolloverTrade,
                    currInfo.fundPort)
            farRolloverMirrorTrade.ConnectedTrade(rolloverMirrorTrade)
            self.callAdjustTradeHook(rolloverTrade, 'Roll')
            self.callAdjustTradeHook(farRolloverTrade, 'Roll')
            self.add_trade(rolloverTrade)
            self.add_trade(farRolloverTrade)
            self.add_trade(rolloverMirrorTrade)
            self.add_trade(farRolloverMirrorTrade)
            #self.logCreatedMirrorTrade(rolloverTrade)
            #self.logCreatedMirrorTrade(farRolloverTrade)
        else:
            if not cparty:
                cparty = counterparty
            # Creating Swap trade market Near Leg
            rolloverTradeMarket = self.createNearTradeMarket(curr1, curr2,
                    cashflow, nearPrice, currInfo.fundPort, currInfo.fundPort,
                    cparty, fromDate, currInfo.rollCurr)
            # Creating Swap trade market Far Leg
            farRolloverTradeMarket = self.createFarTradeMarket(
                    rolloverTradeMarket, farPrice, toDate, currInfo.rollCurr)
            farRolloverTradeMarket.ConnectedTrade(rolloverTradeMarket)
            # Sending market trades to BDP hook
            self.callAdjustTradeHook(rolloverTradeMarket, 'Market')
            self.callAdjustTradeHook(farRolloverTradeMarket, 'Market')
            self.add_trade(rolloverTradeMarket)
            self.add_trade(farRolloverTradeMarket)
        try:
            self.commitTransaction()
        except Exception, e:
            self.abortTransaction()
            logme("Could not commit transaction. %s" % str(e))
            Summary().abortEntries()
            return False
        return True

    def setMarketTradeStrategy(self, trade, instrument, currency):

        insid = instrument.Name()
        value = currency.Name() if insid in ('USD') else insid
        strategy = acm.FChoiceList.Select01('list="%s" and name="%s"' %
                ('Strategy', value), None)
        if strategy:
            trade.OptKey2(strategy)

    def createNearTradeMarket(self, instrument, currency, amount, price,
            tradingPortfolio, fundingPortfolio, counterparty, date, rollCurr):

        acquirer = self.getTradeAcquirer(tradingPortfolio)
        if rollCurr == instrument:
            trade = self.createFxTrade(instrument, currency, tradingPortfolio,
                    acquirer, counterparty, date, price, -amount,
                    amount * price, type="Spot Roll", trade_process=16384)
        else:
            trade = self.createFxTrade(instrument, currency, tradingPortfolio,
                    acquirer, counterparty, date, price, amount / price,
                    -amount, type="Spot Roll", trade_process=16384)
        if self.attributes:
            for key, val in self.attributes.iteritems():
                if key in ('Broker'):
                    try:
                        trade.SetProperty(key, val)
                    except (TypeError, AttributeError):
                        pass
        self.setMarketTradeStrategy(trade, instrument, currency)
        return trade

    def createFarTradeMarket(self, trade, farPrice, date, rollCurr):
        instrument = trade.Instrument()
        if rollCurr == instrument:
            farQuantity = -1.0 * trade.Quantity()
            farPremium = -1.0 * farQuantity * farPrice
        else:
            farPremium = -1.0 * trade.Premium()
            farQuantity = -1.0 * farPremium / farPrice
        farTrade = self.createFxTrade(instrument, trade.Currency(),
                trade.Portfolio(), trade.Acquirer(), trade.Counterparty(),
                date, farPrice, farQuantity, farPremium, type="Spot Roll",
                trade_process=32768)
        if self.attributes:
            for key, val in self.attributes.iteritems():
                if key in ('Broker'):
                    try:
                        farTrade.SetProperty(key, val)
                    except (TypeError, AttributeError):
                        pass
        self.setMarketTradeStrategy(farTrade, instrument, trade.Currency())
        return farTrade

    def createNearTrade(self, instrument, currency, amount, price,
            tradingPortfolio, fundingPortfolio, counterparty, date, rollCurr):
        acquirer = self.getTradeAcquirer(tradingPortfolio)
        if rollCurr == instrument:
            trade = self.createFxTrade(instrument, currency, tradingPortfolio,
                    acquirer, counterparty, date, price, -amount,
                    amount * price, type="Spot Roll", trade_process=16384)
        else:
            trade = self.createFxTrade(instrument, currency, tradingPortfolio,
                    acquirer, counterparty, date, price, amount / price,
                    -amount, type="Spot Roll", trade_process=16384)
        if self.attributes:
            for key, val in self.attributes.iteritems():
                if 'OptKey' in key:
                    key = key.split(".Name")[0]
                    num = int(key[-1])
                    trade_keys = acm.FChoiceList.Select01(
                            'list="%s" and name="%s"' %
                            ('MASTER', 'Trade Keys'), None)
                    if trade_keys:
                        choices = trade_keys.Choices()
                        try:
                            val = acm.FChoiceList.Select01(
                                   'list="%s" and name="%s"' %
                                   (choices.At(num - 1).Name(), val), None)
                        except:
                            continue
                    else:
                        continue
                if key not in ['CurrencyPair', 'Portfolio']:
                    try:
                        trade.SetProperty(key, val)
                    except (TypeError, AttributeError):
                        pass
        return trade

    def createFarTrade(self, trade, farPrice, date, rollCurr):

        instrument = trade.Instrument()
        if rollCurr == instrument:
            farQuantity = -1.0 * trade.Quantity()
            farPremium = -1.0 * farQuantity * farPrice
        else:
            farPremium = -1.0 * trade.Premium()
            farQuantity = -1.0 * farPremium / farPrice
        farTrade = self.createFxTrade(instrument, trade.Currency(),
                trade.Portfolio(), trade.Acquirer(), trade.Counterparty(),
                date, farPrice, farQuantity, farPremium, type="Spot Roll",
                trade_process=32768)
        if self.attributes:
            for key, val in self.attributes.iteritems():
                if 'OptKey' in key:
                    key = key.split(".Name")[0]
                    num = int(key[-1])
                    trade_keys = acm.FChoiceList.Select01(
                            'list="%s" and name="%s"' %
                            ('MASTER', 'Trade Keys'), None)
                    if trade_keys:
                        choices = trade_keys.Choices()
                        try:
                            val = acm.FChoiceList.Select01(
                                    'list="%s" and name="%s"' %
                                    (choices.At(num - 1).Name(), val), None)
                        except:
                            continue
                    else:
                        continue
                if key not in ['CurrencyPair', 'Portfolio']:
                    try:
                        farTrade.SetProperty(key, val)
                    except (TypeError, AttributeError):
                        pass
        return farTrade


class CurrInfo(object):

    def __init__(self, rollCurr, counterCurr=None, currPair=None):

        self.colName = "Portfolio Projected Payments"
        self.rollCurr = rollCurr
        self.counterCurr = counterCurr
        self.currPair = currPair
        self.config = None
        self.fundPort = None
        self.fundAcq = None
        self.yearsBetween = acm.GetFunction('yearsBetween', 4)

    def getAccountingCurrency(self):

        valParams = acm.UsedValuationParameters()
        return valParams.AccountingCurrency()

    def getSplittingCurrencyBuySide(self):

        ac = self.getAccountingCurrency()
        try:
            acname = ac.StringKey()
            if acname in self.currencies():
                return None
            return ac
        except AttributeError, err:
            raise err

    def getSplittingCurrency(self):

        if not self.fundPort.CurrencyPair():
            #override for BuySide
            return self.getSplittingCurrencyBuySide()
        fundCurr1 = self.fundPort.CurrencyPair().Currency1()
        fundCurr2 = self.fundPort.CurrencyPair().Currency2()
        if fundCurr1 == self.rollCurr:
            if fundCurr2 != self.counterCurr:
                return fundCurr2
        if fundCurr1 == self.counterCurr:
            if fundCurr2 != self.rollCurr:
                return fundCurr2
        if fundCurr2 == self.rollCurr:
            if fundCurr1 != self.counterCurr:
                return fundCurr1
        if fundCurr2 == self.counterCurr:
            if fundCurr1 != self.rollCurr:
                return fundCurr1
        return None

    def checkDenominatedValue(self, value):

        try:
            if value.Type() and value.Type().Text() == 'InvalidPrice':
                return False
            if str(value.Number()) in ('Infinity', '-Infinity', '1.#INF',
                    '-1.#INF', '1.#IND', '-1.#IND', 'NaN', '-NaN', '1.#QNAN',
                    '-1.#QNAN'):
                return False
            if not value.Number() >= 0.0 and not value.Number() < 0.0:
                return False
        except Exception:
            return False
        return True

    def getFxRate(self):
        spotDate = self.currPair.SpotDate(acm.Time().DateNow())
        curr1 = self.currPair.Currency1()
        curr2 = self.currPair.Currency2()
        rate = FFxCommonBuySide.getFxRate(spotDate, curr1, curr2)
        logme('FX rate: %s between %s and %s at %s' % (rate, curr1.Name(),
                curr2.Name(), spotDate), 'DEBUG')
        return rate

    def getDiscountFactor(self, fromDate, toDate, bidAsk):

        rollRate, rollTimeInYears = self.getEffectiveRate(self.rollCurr,
                bidAsk, fromDate, toDate)
        counterRate, counterTimeInYears = self.getEffectiveRate(
                self.counterCurr, bidAsk, fromDate, toDate)
        return self.calcDiscountFactor(rollRate, counterRate, rollTimeInYears,
                counterTimeInYears)

    def calcDiscountFactor(self, rollRate, counterRate, rollTimeInYears,
            counterTimeInYears):

        if None in (rollRate, counterRate):
            return None
        rollDiscount = 1 + rollRate / 100.0 * rollTimeInYears
        counterDiscount = 1 + counterRate / 100.0 * counterTimeInYears
        if counterDiscount != 0.0:
            return rollDiscount / counterDiscount
        return None

    def getEffectiveRate(self, curr, bidAsk, fromDate, toDate):
        """
        This returns the funding instrument rate as a simple rate.
        """
        rate, dayCountMethod, fundingType = self.getRate(curr, bidAsk, toDate)
        rate, timeInYears = self.convertToSimpleRate(rate, fundingType,
                fromDate, toDate, dayCountMethod, curr.Calendar())
        return rate, timeInYears

    def getRate(self, curr, bidAsk, date):
        """
        This returns a tuple of the rate, DayCountMethod and FundingType from
        the funding instrument.  The rate type returned will be whichever type
        has been configured for the funding rate.
        """
        if not isinstance(bidAsk, type('')):
            raise TypeError("Parameter 'bidAsk' should be of type string")
        if bidAsk not in ('Bid', 'Ask'):
            raise KeyError("Parameter 'bidAsk' should is not a valid value " +
                    bidAsk)
        defaultDayCountMethod = 'Act/360'
        defaultFundingType = HistoricalFinancing_Simple
        fundingRate = acm.FInstrument[HistoricalFinancingInstrumentName]
        fundingPar = curr.MappedFundingParameter().Parameter()
        if fundingPar:
            fundingRate = fundingPar.FundingRates()
            fundingType = fundingPar.FundingType()
        if not fundingRate:
            logme('Missing funding rate instrument. Using zero funding.',
                  'ERROR')
            return (0.0, defaultDayCountMethod, defaultFundingType)

        calcValue = fundingRate.Calculation().MarketPrice(
                FFxCommonBuySide.space, date, 0, curr, 1, None, 0,
                'Average' + bidAsk + 'Price', 1).Value()
        rate = calcValue and calcValue.Number()

        logme('%s rate: %s for %s at %s' % (bidAsk, rate, curr.Name(), date),
                'DEBUG')
        if not self.checkDenominatedValue(calcValue):
            message = ('Rate error on historical financing instrument in %s '
                    'at %s. Using zero funding.' % (curr.Name(), date))
            logme(message, 'ERROR')
            return (0.0, defaultDayCountMethod, defaultFundingType)
        dayCountMethod = fundingRate.DayCountMethod()
        if dayCountMethod == 'None':
            dayCountMethod = defaultDayCountMethod
        return (rate, dayCountMethod, fundingType)

    def convertToSimpleRate(self, rate, fundingType, fromDate, toDate,
            dayCountMethod, calendar):

        if not isinstance(rate, float):
            raise TypeError("Parameter 'rate' should be of type float")
        if not isinstance(fundingType, type('')):
            raise TypeError("Parameter 'fundingType' should be of type string")
        if not isinstance(fromDate, type('')):
            raise TypeError("Parameter 'fromDate' should be of type string")
        if not isinstance(toDate, type('')):
            raise TypeError("Parameter 'toDate' should be of type string")
        if fundingType not in HistoricalFinancingEnum:
            raise TypeError("Parameter 'fundingType' is not a valid value")
        if not isinstance(calendar, type(acm.FCalendar())):
            raise TypeError("Parameter 'calendar' should be of type FCalendar")
        timeInYears = self.yearsBetween(fromDate, toDate, dayCountMethod,
                calendar)
        if fundingType == HistoricalFinancing_Continuous:
            return (100.0 * ((math.exp(rate / 100.0 * timeInYears) - 1.0) /
                    timeInYears), timeInYears)
        elif fundingType == HistoricalFinancing_DailyCompounding:
            daysInYear = acm.Time.YearLength(dayCountMethod)
            return (100.0 * ((((1.0 + rate / 100.0 / daysInYear) ** (
                    daysInYear * timeInYears)) - 1.0) / timeInYears),
                    timeInYears)
        elif fundingType == HistoricalFinancing_Simple:
            return (rate, timeInYears)
        else:
            raise TypeError("Parameter 'fundingType' is not a supported "
                    "value " + fundingType)

    def currencies(self):

        for i in range(1, 3):
            curr = getattr(self.currPair, 'Currency%s' % str(i))()
            yield curr.Name()
