""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/FFxSpotRolloverPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFxSpotRolloverPerform - Module which performs FFxSpotRollover MM- and
    Swap- Funding.

DESCRIPTION
    This module performs (1) FX spot rollover swap funding procedure (based on
    the parameters passed from the script FFxSpotRolloverSwapFunding), and also
    (2) FX spot rollover money-market funding procedure (based on parameters
    passed from the script FFxSpotRolloverMMFunding).
----------------------------------------------------------------------------"""


import math

import acm
import ael

import FFxCommon
import FBDPRollback
import FBDPCommon
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


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


def perform_mm_rollover(args):
    r = MMRollover('FxSpotRolloverMMFunding', args['Testmode'], args)
    r.perform(args)
    r.end()


def perform_swap_rollover(args):
    r = SwapRollover('FxSpotRolloverSwapFunding', args['Testmode'], args)
    r.perform(args)
    r.end()


class Rollover(FBDPRollback.RollbackWrapper, FFxCommon.FxPortfolioProcess):
    class IgnoreCashflow(Exception):
        pass

    def cashflowShouldBeIgnored(self, cashflow):
        return True if math.fabs(cashflow) < 0.0001 else False

    def getCurrObjects(self, currPair):
        if currPair:
            return [currPair]
        else:
            query = ""
        return acm.FCurrency.Select(query)

    def perform(self, args):
        self.performProcess(args)

    def performCalculation(self):
        self.rollDate = self.nextTradingDate
        for n in range(0, 3):
            if (n == 1):
                self.refreshCalcSpace = True

            positions = self.getPositionNodes()
            for portfolio, nodes in positions.iteritems():
                currencies = None
                pair = portfolio.CurrencyPair()
                if pair:
                    currencies = [pair.Currency1(), pair.Currency2()]
                for n in nodes:
                    if FFxCommon.POSITION_PAIR in n[1]:
                        message = 'PositionPair grouper is not supported. \
Please use PositionOrCurrencyPair grouper instead.'
                        Summary().fail(portfolio, Summary().ROLL, message,
                            portfolio.Name())
                        return False
                    self.printTree(n[0], currencies=currencies)
                self.processPortfolio(portfolio, nodes)
            self.cleanAndRecreateCalcSpace()
            self.rollDate = self.tradingCalendar.AdjustBankingDays(
                    self.rollDate, 1)

    def requiredSubAttributesNotSet(self):
        if self.useMtM and not self.mtmMarket:
            return "No MtM market specified for funding rates."
        return ''

    def readArguments(self, args):
        FFxCommon.FxPortfolioProcess.readArguments(self, args)
        calcvalparm = acm.ObjectServer().UsedValuationParameters()
        Logme()('Using valuation parameters: "%s".   Forward start PL: %i' %
                (calcvalparm.Name(), calcvalparm.ForwardStartPL()), 'DEBUG')
        self.accCurr = calcvalparm.AccountingCurrency()

        self.tradingCalendar = self.accCurr.Calendar()
        if 'TradingCalendar' in args and args['TradingCalendar']:
            self.tradingCalendar = args['TradingCalendar'][0]

        today = acm.Time.DateToday()
        self.mtmDate = today
        self.nextTradingDate = args['NextTradingDate']
        if self.nextTradingDate == 'Tom next':
            self.nextTradingDate = today
        elif self.nextTradingDate == 'Tom':
            self.nextTradingDate = today
        elif self.nextTradingDate == 'Spot next':
            self.nextTradingDate = self.tradingCalendar.AdjustBankingDays(
                    today, 1)
        else:
            self.nextTradingDate = FBDPCommon.toDate(self.nextTradingDate)

        self.mappedFundingInstruments = (args['MappedFundingInstruments']
                if 'MappedFundingInstruments' in args else {})
        self.fundingInstruments = (args['FundingInstruments']
                if 'FundingInstruments' in args else None)
        self.useMtM = args.get('UseMtM', 0)
        self.mtmMarket = None
        self.setFundingRate = self._setSpotRate
        self.useFXSwapTrades = (args['UseFXSwapTrades']
                if 'UseFXSwapTrades' in args else 0)
        if self.useMtM:
            if 'MtMMarket' in args and args['MtMMarket']:
                self.mtmMarket = args['MtMMarket'][0]
                self.setFundingRate = self._setMtMRate

    def processPortfolio(self, tradingPortfolio, nodes):
        FFxCommon.printEmp('Rolling trading portfolio: "%s".' %
                (tradingPortfolio.Name()), '*')
        resultOk = True
        groupingByCurrPair = True
        curr = tradingPortfolio.Currency()
        currPair = tradingPortfolio.CurrencyPair()

        for (topNode, self.attributes) in nodes:
            FFxCommon.printEmp('Rolling grouping position: %s' %
                        (self.attributes), '=')

            if FFxCommon.CURRENCY_PAIR in self.attributes:
                groupingByCurrPair = True
                val = self.attributes[FFxCommon.CURRENCY_PAIR]
                currPair = acm.FCurrencyPair[val]
            if 'PositionOrCurrencyPair' in self.attributes:
                groupingByCurrPair = True
                val = self.attributes['PositionOrCurrencyPair']
                currPair = acm.FCurrencyPair[val]

            try:
                if currPair is None:
                    message = ('Portfolio %s has no currency pair or'
                              'PositionOrCurrencyPair groupers.' %
                              (tradingPortfolio.Name()))
                    Logme()(message, 'INFO')
                    # If currpair is None, then we don't have a
                    # currency pair on the portfolios or grouper,
                    # so we should use the currency of the portfolio
                    # or the currency of the group (if specified).
                    currency = curr
                    if 'Trade.Currency' in self.attributes:
                        Logme()('Using trade currency', 'DEBUG')
                        currency = self.attributes['Trade.Currency']
                    elif 'Instrument.Currency' in self.attributes:
                        Logme()('Using instrument currency', 'DEBUG')
                        currency = self.attributes['Instrument.Currency']
                    else:
                        Logme()('Using portfolio currency', 'DEBUG')

                    currencyInfos = self.createCurrInfos([currency])
                else:
                    # Don't split yet, preserve original trading
                    # currency pair and split only in funding
                    # portfolio in rollCashflow().
                    currencyInfos = self.getTradingCurrencyPairs([currPair])

            except Exception, ex:
                Summary().fail(tradingPortfolio, Summary().ROLL, str(ex),
                        tradingPortfolio.Name())
                return False

            resultOk = self.processGroup(topNode, currencyInfos,
                        tradingPortfolio, groupingByCurrPair)

        if resultOk:
            Summary().ok(tradingPortfolio, Summary().ROLL)
        else:
            Summary().fail(tradingPortfolio, Summary().ROLL,
                    'All positions not rolled', tradingPortfolio.Name())
        Summary().commitEntries()
        return False

    def processGroup(self, topNode, currencyInfos, tradingPortfolio,
                    groupingByCurrPair):
        resultOk = True
        for currInfo in currencyInfos:
            Logme()('Max roll to: %s.' % (currInfo.maxRollTo), 'DEBUG')
            Logme()('Roll date: %s.' % (currInfo.rollDate), 'DEBUG')
            Logme()('Roll currency: %s.' %
            (currInfo.rollCurr.Name()), 'DEBUG')

            if acm.Time().DateDifference(currInfo.maxRollTo,
                currInfo.rollDate) <= 0:
                return True
            if acm.Time().DateDifference(currInfo.rollDate,
                currInfo.rollTo) >= 0:
                return True
            try:
                cashflow = self.getCashflow(topNode,
                        day=currInfo.rollDate,
                        configCurr=currInfo.rollCurr)

                cashflowInCounterCur = self.getCashflow(topNode,
                        currInfo.rollDate, currInfo.counterCurr)
                nextCashflow = 0.0
                if not cashflow:
                    continue

                result = self.rollCashflow(currInfo, cashflow,
                        currInfo.rollDate, tradingPortfolio,
                        nextCashflow, cashflowInCounterCur,
                        groupingByCurrPair)
                self.refreshCalcSpace = True

                if not result:
                    resultOk = False

            except Rollover.IgnoreCashflow:
                pass
            finally:
                currInfo.rollDate = self.tradingCalendar.AdjustBankingDays(
                                    currInfo.rollDate, 1)
                currInfo.rollTo = self.tradingCalendar.AdjustBankingDays(
                                    currInfo.rollDate, 1)
        return resultOk

    def createCurrInfos(self, currObjects):
        raise NotImplementedError('Must override createCurrInfos function')

    def getTradingCurrencyPairs(self, currObjects):
        raise NotImplementedError('Must override getTradingCurrencyPairs '
                'function')

    def rollCashflow(self, currInfo, cashflow, fromDate, tradingPortfolio,
            farAmount=None, cashflowCounterCur=None, groupByCurrPair=False):
        raise NotImplementedError('Must override rollCashflow function')

    def getTradeAcquirer(self, tradingPortfolio):
        acquirer = tradingPortfolio.PortfolioOwner()
        if not acquirer:
            acquirer = self.defaultAcquirer
            if not self.attributes or 'Acquirer' not in self.attributes:
                message = ('No owner specified for trading portfolio %s.' %
                       tradingPortfolio.Name())
                raise Exception(message)
        return acquirer


class MMRollover(Rollover):

    FXProcessType = "FxSpotRolloverMMFunding"

    def readArguments(self, args):
        self._nextTradingDateInput = args['NextTradingDate']
        return super(MMRollover, self).readArguments(args)

    def _getMaxRollTo(self, currObj, calendar, today, is_tom_only):
        if is_tom_only:
            return calendar.AdjustBankingDays(today, 1)

        return currObj.SpotDate(self.nextTradingDate)

    def createCurrInfos(self, currObjects):
        is_tom_only = self._nextTradingDateInput == 'Tom'
        today = acm.Time.DateToday()
        currInfoList = []
        for currObj in currObjects:
            if currObj.IsKindOf(acm.FCurrencyPair):
                rollTo = currObj.Currency1().Calendar().AdjustBankingDays(
                    self.rollDate, 1)
                maxRollTo = self._getMaxRollTo(currObj,
                    currObj.Currency1().Calendar(), today, is_tom_only)
                currInfoList.append(CurrInfo(currObj.Currency1(), rollTo,
                        mtmDate=self.mtmDate, maxRollTo=maxRollTo,
                        rollDate=self.rollDate,
                        nextTradingDate=self.nextTradingDate))
                rollTo = currObj.Currency2().Calendar().AdjustBankingDays(
                    self.rollDate, 1)
                maxRollTo = self._getMaxRollTo(currObj,
                    currObj.Currency2().Calendar(), today, is_tom_only)
                currInfoList.append(CurrInfo(currObj.Currency2(), rollTo,
                        mtmDate=self.mtmDate, maxRollTo=maxRollTo,
                        rollDate=self.rollDate,
                        nextTradingDate=self.nextTradingDate))
            else:
                rollTo = currObj.Calendar().AdjustBankingDays(
                    self.rollDate, 1)
                maxRollTo = self._getMaxRollTo(currObj,
                    currObj.Calendar(), today, is_tom_only)
                currInfo = CurrInfo(currObj, rollTo, mtmDate=self.mtmDate,
                        maxRollTo=maxRollTo, rollDate=self.rollDate,
                        nextTradingDate=self.nextTradingDate)
                currInfoList.append(currInfo)

        for currInfo in currInfoList:
            currInfo.fundPort, currInfo.fundAcq = \
                        self.getPortfolioAndAcquirer(currInfo.rollCurr)
            currInfo.mappedFundingInst = \
                        self.getFundingInstrument(currInfo)

        return currInfoList

    def getTradingCurrencyPairs(self, currObjects):
        return self.createCurrInfos(currObjects)

    def _setSpotRate(self, currInfo):
        currInfo.getInterestRate = currInfo._getSpotRate

    def _setMtMRate(self, currInfo):
        currInfo.getInterestRate = currInfo._getMtMRate

    def _getEndCash(self, ins, currInfo, cashflow, fromDate, tradingPortfolio):
        """
        Return the end cash by create a temporary deposit trade.
        """
        ins.Commit()
        try:
            rolloverTrade = self.createRolloverTrade(ins,
                    currInfo.rollCurr, cashflow, tradingPortfolio,
                    currInfo.fundAcq, fromDate)
        except Exception, e:
            Logme()("Could not create Rollover Trade as %s" % str(e))
            return None
        rolloverTrade.Status('Simulated')
        rolloverTrade.Commit()
        endCash = rolloverTrade.EndCash()
        rolloverTrade.Delete()
        ins.Delete()
        return endCash

    def _rollByDepositTrade(self, ins, currInfo, cashflow,
                    fromDate, tradingPortfolio):
        with FBDPRollback.RollbackAutoTransaction(self):
            self.add(ins)
            try:
                rolloverTrade = self.createRolloverTrade(ins,
                        currInfo.rollCurr, cashflow, tradingPortfolio,
                        currInfo.fundAcq, fromDate)
            except Exception, e:
                Logme()("Could not create Rollover Trade as %s" % str(e))
                return False
            self.callAdjustTradeHook(rolloverTrade, 'Roll')
            if self.cashflowShouldBeIgnored(rolloverTrade.Premium()):
                raise Rollover.IgnoreCashflow()

            rolloverTrade.MirrorPortfolio(currInfo.fundPort)
            self.add_trade(rolloverTrade)
            try:
                self.commitTransaction()
            except Exception, e:
                Logme()("Could not commit transaction. %s" % str(e))
                Summary().abortEntries()
                return False
        self.logCreatedMirrorTrade(rolloverTrade)
        return True

    def _rollByFXTrades(self, ins, currPair, currInfo,
                        cashflow, fromDate, toDate, tradingPortfolio):
        endCash = self._getEndCash(ins, currInfo, cashflow,
                    fromDate, tradingPortfolio)
        if endCash is None:
            return False

        #Get the first currency for the FX trade
        if currPair.Currency1() == currInfo.rollCurr:
            curr = currPair.Currency2()
        else:
            curr = currPair.Currency1()

        with FBDPRollback.RollbackAutoTransaction(self):
            try:
                rolloverTradeStart = self.createRolloverTrade(curr,
                        currInfo.rollCurr, cashflow, tradingPortfolio,
                        currInfo.fundAcq, fromDate)
                rolloverTradeEnd = self.createRolloverTrade(curr,
                        currInfo.rollCurr, -endCash, tradingPortfolio,
                        currInfo.fundAcq, toDate)
            except Exception, e:
                Logme()("Could not create Rollover Trade as %s" % str(e))
                return False
            rolloverTradeStart.Quantity(0)
            rolloverTradeEnd.Quantity(0)
            self.callAdjustTradeHook(rolloverTradeStart, 'Roll')
            self.callAdjustTradeHook(rolloverTradeEnd, 'Roll')
            if self.cashflowShouldBeIgnored(rolloverTradeStart.Premium()) or \
                    self.cashflowShouldBeIgnored(rolloverTradeEnd.Premium()):
                raise Rollover.IgnoreCashflow()
            rolloverTradeStart.MirrorPortfolio(currInfo.fundPort)
            rolloverTradeEnd.MirrorPortfolio(currInfo.fundPort)
            self.add_trade(rolloverTradeStart)
            self.add_trade(rolloverTradeEnd)
            try:
                self.commitTransaction()
            except Exception, e:
                Logme()("Could not commit transaction. %s" % str(e))
                Summary().abortEntries()
                return False
        self.logCreatedMirrorTrade(rolloverTradeStart)
        self.logCreatedMirrorTrade(rolloverTradeEnd)
        return True

    def rollCashflow(self, currInfo, cashflow, fromDate, tradingPortfolio,
            farAmount=None, cashflowCounterCur=None, groupByCurrPair=False):
        toDate = currInfo.rollTo
        self.setFundingRate(currInfo)
        if cashflow < 0.0:
            rate, timeInYears = currInfo.getEffectiveRate(currInfo.rollCurr,
                    'Ask', fromDate, toDate, self.mtmMarket)
        else:
            rate, timeInYears = currInfo.getEffectiveRate(currInfo.rollCurr,
                    'Bid', fromDate, toDate, self.mtmMarket)
        if rate == None:
            Logme()('Could not get rate for %s' % currInfo.rollCurr.Name(),
                    'ERROR')
            return False

        Logme()('Roll %s from %s to %s for cashflow % 18.4f.'
              % (currInfo.rollCurr.Name(), fromDate, toDate, cashflow), 'INFO')

        #Create instrument but not commit
        insName = self.buildInstrumentName(currInfo.rollCurr, fromDate,
                toDate, tradingPortfolio)
        insContractSize = math.fabs(cashflow)
        ins = self.createInstrument(insName, currInfo.rollCurr,
                insContractSize, rate, fromDate, toDate)

        #Try to get currency pair in the groupers
        currPair = None
        if FFxCommon.CURRENCY_PAIR in self.attributes:
            val = self.attributes[FFxCommon.CURRENCY_PAIR]
            currPair = acm.FCurrencyPair[val]

        if FFxCommon.POSITIONORCURRENCY_PAIR in self.attributes:
            val = self.attributes[FFxCommon.POSITIONORCURRENCY_PAIR]
            currPair = acm.FCurrencyPair[val]

        result = False
        if not self.useFXSwapTrades or not currPair:
            #Roll by creating deposit trade
            result = self._rollByDepositTrade(ins, currInfo,
                cashflow, fromDate, tradingPortfolio)
        else:
            #Create two one-sided FX trade for from and to date
            result = self._rollByFXTrades(ins, currPair, currInfo,
                    cashflow, fromDate, toDate, tradingPortfolio)
        return result

    def createInstrument(self, name, currency, contractSize, rate, fromDate,
                         toDate):
        """
        Return an newly created deposit instrument with the given parameters.
        """

        ins = acm.FDeposit()
        ins.Name(name)
        ins.Currency(currency)
        ins.QuoteType('Pct of Nominal')
        ins.Quotation('Pct of Nominal')
        ins.ContractSize(contractSize)

        # Create the receive leg
        receiveLeg = ins.CreateLeg(False)
        receiveLeg.LegType('Fixed')
        receiveLeg.Currency(currency)
        receiveLeg.ResetType('None')
        receiveLeg.StartDate(fromDate)
        receiveLeg.AmortStartDay(fromDate)
        receiveLeg.RollingPeriodBase(fromDate)
        receiveLeg.EndDate(toDate)
        receiveLeg.AmortEndDay(toDate)
        receiveLeg.FixedRate(rate)

        # The new deposit instrument's rounding specification should be that of
        # the default deposit instrument.  If it is not defined, use that of
        # the currency's
        roundingSpec = None
        depositDefaultIns = acm.FDeposit['DepositDefault']
        if depositDefaultIns is not None:
            roundingSpec = depositDefaultIns.RoundingSpecification()
        if roundingSpec is None:
            roundingSpec = currency.RoundingSpecification()
        if roundingSpec is not None:
            ins.RoundingSpecification(roundingSpec)

        return ins

    def buildInstrumentName(self, currency, fromDate, toDate,
            tradingPortfolio):
        name = ('%s/DEP/%s-%s-%d' % (currency.Name(),
                ael.date(fromDate).to_string(ael.DATE_Quick),
                ael.date(toDate).to_string(ael.DATE_Quick),
                tradingPortfolio.Oid()))
        for si in range(1000):  # Domain, avoid dupe suffix.
            namesi = name + '/%s' % (si)
            inst = acm.FInstrument[namesi]
            if inst == None:
                return namesi
        return None

    def createRolloverTrade(self, instrument, currency, amount,
            tradingPortfolio, counterparty, date):
        tradePremium = -amount
        tradeQuantity = amount / instrument.ContractSize()
        acquirer = self.getTradeAcquirer(tradingPortfolio)
        trade = self.createFxTrade(instrument, currency, tradingPortfolio,
                acquirer, counterparty, date, 100, tradeQuantity, tradePremium,
                tradetype="Spot Roll", trade_process=4096)
        self.setTradePropertiesFromGrouper(trade,
                (FFxCommon.CURRENCY_PAIR, 'Currency Split'))
        return trade

    def getFundingInstrument(self, currencyInfo):
        if not self.fundingInstruments:
            return None
        for fundingInstrument in self.fundingInstruments:
            if fundingInstrument.Currency() == currencyInfo.rollCurr:
                if fundingInstrument.ExpiryPeriod_count() == \
                currencyInfo.getRollPeriod():
                    return fundingInstrument


class SwapRollover(Rollover):

    FXProcessType = "FxSpotRolloverSwapFunding"

    def getTradingCurrencyPairs(self, currObjects):
        currInfoList = []
        for currObj in currObjects:
            maxRollTo = currObj.SpotDate(self.nextTradingDate)
            rollTo = self.tradingCalendar.AdjustBankingDays(
                    self.rollDate, 1)
            if currObj.IsKindOf(acm.FCurrencyPair):
                cc = self.getCounterCurrencyOfCurrPair(currObj)
                rc = currObj.Currency1()
                if rc == cc:
                    rc = currObj.Currency2()

                currInfo = CurrInfo(rc, rollTo, cc, currObj,
                        mtmDate=self.mtmDate, maxRollTo=maxRollTo,
                        rollDate=self.rollDate,
                        nextTradingDate=self.nextTradingDate)
                fundPort, fundAcq = \
                    self.getMappedPortfolioAndAcquirer(currInfo.currPair)
                currInfo.fundPort = fundPort
                currInfo.fundAcq = fundAcq
                if not currInfo.fundPort:
                    currInfo.fundPort = self.getDefaultPortfolio()
                currInfo.splitCurr = self.getSplittingCurrency(
                    currInfo.rollCurr, currInfo.counterCurr, currInfo.fundPort)

                if not currInfo.fundAcq:
                    currInfo.fundAcq = self.getDefaultAcquirer()
                if not self.fundingInstruments:
                    currInfo.mappedFundingInst = \
                        self.getMappedFundingInstrument(currInfo.currPair)
                else:
                    currInfo.mappedFundingInst = \
                        self.getFundingInstrument(currInfo)
                    currInfo.pointsPerDay = False
                currInfoList.append(currInfo)

        return currInfoList

    def getSplitPortfolioAndAcquirer(self, lookupCurrencyPair, currInfo):
        splitFundPort, splitFundAcq = self.getMappedPortfolioAndAcquirer(
            lookupCurrencyPair)
        # Allow the script to specify the mapped portfolio and acquirer
        # explicitly or implicitly. This allows users to specify either
        # Roll/Split: port or Roll/Counter: port
        if not splitFundPort:
            splitFundPort = currInfo.fundPort
        if not splitFundAcq:
            splitFundAcq = currInfo.fundAcq

        if not splitFundPort:
            splitFundPort = self.getDefaultPortfolio()
        if not splitFundAcq:
            splitFundAcq = self.getDefaultAcquirer()

        return splitFundPort, splitFundAcq

    def createSplitCurrencyInfo(self, currInfo, rollCurr, splitCurr):
        splitCurrInfo = CurrInfo(rollCurr, currInfo.rollTo, splitCurr,
                mtmDate=self.mtmDate, rollDate=self.rollDate,
                maxRollTo=currInfo.maxRollTo,
                nextTradingDate=self.nextTradingDate)
        splitCurrInfo.splitting = True
        lookupCurrencyPair = FFxCommon.currencyPair(rollCurr, splitCurr)
        if lookupCurrencyPair is None:
            message = ('Currency Pair for %s/%s does not exist.' %
                    (rollCurr.Name(), splitCurr.Name()))
            raise Exception(message)

        splitCurrInfo.currPair = lookupCurrencyPair
        splitCurrInfo.mappedFundingInst = self.getMappedFundingInstrument(
                lookupCurrencyPair)
        splitFundPort, splitFundAcq = self.getSplitPortfolioAndAcquirer(
                lookupCurrencyPair, currInfo)

        if (not splitFundPort.CurrencyPair() or
                self.currPairIncludes(splitFundPort.CurrencyPair(), splitCurr,
                        currInfo.counterCurr)):
            splitCurrInfo.fundPort = splitFundPort
            splitCurrInfo.fundAcq = splitFundAcq
        else:
            if self.currPairIncludes(splitFundPort.CurrencyPair(), rollCurr,
                    splitCurr):
                splitCurrInfo.fundPort = currInfo.fundPort
                splitCurrInfo.fundAcq = splitFundAcq
                currInfo.fundPort = splitFundPort
                currInfo.fundAcq = splitFundAcq
            else:
                message = ('Funding portfolio {0} for splitting currency {1} '
                        'has mismatching CurrencyPair: {2} != {3}/{4}'.format(
                        splitFundPort.Name(), splitCurr.Name(),
                        splitFundPort.CurrencyPair().Name(), rollCurr.Name(),
                        splitCurr.Name()))
                raise Exception(message)
        self.setFundingRate(splitCurrInfo)
        return splitCurrInfo

    def createCurrInfos(self, currObjects):
        currInfoList = self.getTradingCurrencyPairs(currObjects)
        splitCurrInfoList = []
        for currInfo in currInfoList:
            splitCurr = currInfo.getSplittingCurrency()
            if not splitCurr:
                continue

            splitCurrInfo = self.createSplitCurrencyInfo(currInfo,
                    currInfo.rollCurr, splitCurr)
            splitCurrInfoList.insert(0, splitCurrInfo)

            #now update the currInfo object for the split roll
            currInfo.rollCurr = splitCurr
            currInfo.splitting = True
            lookupCurrencyPair = FFxCommon.currencyPair(currInfo.counterCurr,
                    splitCurr)
            if lookupCurrencyPair is None:
                message = ('Currency Pair for %s/%s does not exist.' %
                        (currInfo.counterCurr.Name(), splitCurr.Name()))
                raise Exception(message)

            currInfo.currPair = lookupCurrencyPair
            currInfo.mappedFundingInst = self.getMappedFundingInstrument(
                    lookupCurrencyPair)
            fundPort, fundAcq = self.getPortfolioAndAcquirer(
                    lookupCurrencyPair)
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

    def _setSpotRate(self, currInfo):
        currInfo.getFxRate = currInfo._getSpotFX
        currInfo.getInterestRate = currInfo._getSpotRate
        currInfo.getSwapPoints = currInfo._getSpotPoints

    def _setMtMRate(self, currInfo):
        currInfo.getFxRate = currInfo._getHistoricalFX
        currInfo.getInterestRate = currInfo._getMtMRate
        currInfo.getSwapPoints = currInfo._getMtMRate

    def _createSplitTrades(self, currInfo, splitCurr, fromDate, toDate,
            cashflow, bidAsk, counterBidAsk):
        # The roll currency amount will be rolled "as is", the counter currency
        # amount will be derived from what you get when swapping from the split
        # currency.
        splitCurrInfo = self.createSplitCurrencyInfo(currInfo,
                currInfo.rollCurr, splitCurr)

        splitPort, splitAcq = self.getSplitPortfolioAndAcquirer(
                splitCurrInfo.currPair, splitCurrInfo)
        Logme()('Using splitting portfolio %s for currency pair %s' %
                    (splitPort.Name(), splitCurrInfo.currPair.Name()), 'INFO')

        spotFXRate = splitCurrInfo.getFxRate(self.mtmMarket)
        farPrice = self.getPrice(spotFXRate, splitCurrInfo, toDate,
                toDate, counterBidAsk, bidAsk, self.mtmMarket)
        nearPrice = self.getPrice(spotFXRate, splitCurrInfo, fromDate,
                toDate, bidAsk, counterBidAsk, self.mtmMarket)

        rollCurrNear = self.createNearTrade(currInfo.rollCurr, splitCurr,
                cashflow, nearPrice, splitPort, splitAcq, fromDate)
        rollCurrFar = self.createFarTrade(rollCurrNear, farPrice, toDate, 0.)
        rollCurrFar.ConnectedTrade(rollCurrNear)

        for t in (rollCurrNear, rollCurrFar):
            # This gets overwritten in createTrade()'s, so you need to set it
            # again.
            t.Portfolio(splitPort)
            self.add_trade(t)

        # Amounts in the split currency you now want to convert back to
        # the counter currency.
        nearQuantity, farQuantity = [t.Premium() for t in
                (rollCurrNear, rollCurrFar)]

        splitCurrInfo = self.createSplitCurrencyInfo(currInfo, splitCurr,
                    currInfo.counterCurr)
        splitPort, splitAcq = self.getSplitPortfolioAndAcquirer(
                splitCurrInfo.currPair, splitCurrInfo)
        Logme()('Using splitting portfolio %s for currency pair %s' %
                    (splitPort.Name(), splitCurrInfo.currPair.Name()), 'INFO')

        spotFXRate = splitCurrInfo.getFxRate(self.mtmMarket)
        farPrice = self.getPrice(spotFXRate, splitCurrInfo, toDate,
                toDate, counterBidAsk, bidAsk, self.mtmMarket)
        nearPrice = self.getPrice(spotFXRate, splitCurrInfo, fromDate,
                toDate, bidAsk, counterBidAsk, self.mtmMarket)
        counterCurrNear = self.createNearTrade(splitCurr, currInfo.counterCurr,
                nearQuantity, nearPrice, splitPort, splitAcq, fromDate)
        farPremium = farQuantity * farPrice
        counterCurrFar = self.createFxTrade(splitCurr, currInfo.counterCurr,
                splitPort, counterCurrNear.Acquirer(),
                counterCurrNear.Counterparty(), toDate, farPrice,
                (-1. * farQuantity), farPremium, tradetype="Spot Roll",
                trade_process=32768)
        self.setTradePropertiesFromGrouper(counterCurrFar,
                (FFxCommon.CURRENCY_PAIR, 'Currency Split'))
        counterCurrFar.ConnectedTrade(counterCurrNear)
        for t in (counterCurrNear, counterCurrFar):
            t.Portfolio(splitPort)
            self.add_trade(t)

        return counterCurrNear, counterCurrFar

    def rollCashflow(self, currInfo, cashflow, fromDate, tradingPortfolio,
            farAmount=None, cashflowCounterCur=None, groupByCurrPair=False):
        if not cashflow:
            return True

        if self.cashflowShouldBeIgnored(cashflow):
            if self.cashflowShouldBeIgnored(cashflow):
                raise Rollover.IgnoreCashflow()

        toDate = currInfo.rollTo
        cc = currInfo.counterCurr.Name() if currInfo.counterCurr else ''
        Logme()('Roll %s against %s from %s to %s for cashflow % 18.4f.' % (
                currInfo.rollCurr.Name(), cc, fromDate, toDate, cashflow),
                'INFO')

        bidAsk, counterBidAsk = FFxCommon.getBidAsk(cashflow)
        if cashflowCounterCur:
            counterBidAsk, _ignore = FFxCommon.getBidAsk(cashflowCounterCur)

        self.setFundingRate(currInfo)
        spotFXRate = currInfo.getFxRate(self.mtmMarket)
        if not spotFXRate:
            return False

        farPrice = self.getPrice(spotFXRate, currInfo, toDate, toDate,
                counterBidAsk, bidAsk, self.mtmMarket)
        nearPrice = self.getPrice(spotFXRate, currInfo, fromDate, toDate,
                bidAsk, counterBidAsk, self.mtmMarket)
        if nearPrice == None:
            Logme()('Could not get the near price for %s' %
                    currInfo.rollCurr.Name(), 'ERROR')
            return False

        with FBDPRollback.RollbackAutoTransaction(self):
            try:
                # Creating Swap trade Near Leg
                rolloverTrade = self.createNearTrade(currInfo.rollCurr,
                        currInfo.counterCurr, cashflow, nearPrice,
                        tradingPortfolio, currInfo.fundAcq, fromDate)
            except Exception, e:
                Logme()("Could not create Near Trade as %s" % str(e))
                return False
            rolloverTrade.MirrorPortfolio(currInfo.fundPort)

            # Creating Swap trade Far Leg
            farRolloverTrade = self.createFarTrade(rolloverTrade, farPrice,
                    toDate, farAmount)
            farRolloverTrade.ConnectedTrade(rolloverTrade)
            farRolloverTrade.MirrorPortfolio(currInfo.fundPort)

            # If grouping by currency pair and splitting, the splitting will
            # occur in the funding, rather than the trading, portfolio.
            splitCurr = currInfo.getSplittingCurrency()
            if groupByCurrPair and splitCurr:
                nearSplitTrade, farSplitTrade = self._createSplitTrades(
                        currInfo, splitCurr, fromDate, toDate, cashflow,
                        bidAsk, counterBidAsk)
                # Set the premiums on the original trades to split premiums and
                # infer the price accordingly.

                for orgTrade, splitTrade in zip((rolloverTrade,
                        farRolloverTrade), (nearSplitTrade, farSplitTrade)):
                    orgTrade.Premium(splitTrade.Premium())
                    if orgTrade.Quantity():
                        orgTrade.Price(orgTrade.Premium() /
                                        orgTrade.Quantity())

            self.callAdjustTradeHook(rolloverTrade, 'Roll')
            self.callAdjustTradeHook(farRolloverTrade, 'Roll')

            if self.cashflowShouldBeIgnored(rolloverTrade.Premium()):
                if self.cashflowShouldBeIgnored(farRolloverTrade.Premium()):
                    raise Rollover.IgnoreCashflow()

            self.add_trade(rolloverTrade)
            self.add_trade(farRolloverTrade)
            try:
                self.commitTransaction()
            except Exception, e:
                Logme()("Could not commit transaction. %s" % str(e))
                Summary().abortEntries()
                return False
        self.logCreatedMirrorTrade(rolloverTrade)
        self.logCreatedMirrorTrade(farRolloverTrade)

        return True

    def getPrice(self, farPrice, currInfo, fromDate, toDate, bidAsk,
            counterBidAsk, mtmMarket=None):
        if (currInfo.mappedFundingInst and
                currInfo.mappedFundingInst.InsType() == 'FxSwap'):
            if (currInfo.rollCurr.Name() ==
                    currInfo.mappedFundingInst.Currency().Name()):
                return 1.0 / (1.0 / farPrice -
                        currInfo.getTotalPointsOnFundInst(fromDate,
                        bidAsk, counterBidAsk, mtmMarket))
            price = farPrice - currInfo.getTotalPointsOnFundInst(fromDate,
                    bidAsk, counterBidAsk, mtmMarket)
            return math.fabs(price)
        else:
            discountFactor = currInfo.getDiscountFactor(fromDate,
                    toDate, bidAsk, counterBidAsk, mtmMarket)
            if discountFactor == None:
                Logme()('Could not get funding for %s' %
                        currInfo.rollCurr.Name(), 'ERROR')
                return None
            price = farPrice * discountFactor
            return math.fabs(price)

    def createNearTrade(self, instrument, currency, amount, price,
            tradingPortfolio, counterparty, date):
        acquirer = self.getTradeAcquirer(tradingPortfolio)
        trade = self.createFxTrade(instrument, currency, tradingPortfolio,
                acquirer, counterparty, date, price, -amount, amount * price,
                tradetype="Spot Roll", trade_process=16384)
        self.setTradePropertiesFromGrouper(trade,
                (FFxCommon.CURRENCY_PAIR, 'Currency Split'))
        return trade

    def createFarTrade(self, trade, farPrice, date, farAmount):
        portfolio = trade.Portfolio()
        tradeInstrument = trade.Instrument()
        currencyPair = portfolio.CurrencyPair()
        curr1 = None
        curr2 = None
        if currencyPair != None:
            curr1 = currencyPair.Currency1()
            curr2 = currencyPair.Currency2()

        if (farAmount != 0.0 and tradeInstrument != curr1 and
                tradeInstrument != curr2 and curr1 != None and curr2 != None):
            farQuantity = -1.0 * farAmount
        else:
            farQuantity = -1.0 * trade.Quantity()

        farPremium = -1.0 * farQuantity * farPrice
        farTrade = self.createFxTrade(tradeInstrument, trade.Currency(),
                portfolio, trade.Acquirer(), trade.Counterparty(), date,
                farPrice, farQuantity, farPremium, tradetype="Spot Roll",
                trade_process=32768)
        if self.attributes['Portfolio']:
            trade.SetProperty('Portfolio', self.attributes['Portfolio'])
        self.setTradePropertiesFromGrouper(farTrade,
                (FFxCommon.CURRENCY_PAIR, 'Currency Split'))
        return farTrade

    def getFundingInstrument(self, currencyInfo):
        for fundingInstrument in self.fundingInstruments:
            if fundingInstrument.Legs()[0].Currency() == \
            currencyInfo.rollCurr and \
            fundingInstrument.Legs()[1].Currency() == \
            currencyInfo.counterCurr:
                if fundingInstrument.ExpiryPeriod_count() == \
                currencyInfo.getRollPeriod():
                    return fundingInstrument

            elif fundingInstrument.Legs()[1].Currency() == \
            currencyInfo.rollCurr and \
            fundingInstrument.Legs()[0].Currency() == \
            currencyInfo.counterCurr:
                if fundingInstrument.ExpiryPeriod_count() == \
                currencyInfo.getRollPeriod():
                    return fundingInstrument


class CurrInfo(object):
    def __init__(self, rollCurr, rollTo, counterCurr=None, currPair=None,
            mtmDate=acm.Time.DateToday(), maxRollTo=None, rollDate=None,
            nextTradingDate=acm.Time.DateToday()):
        self.colName = "Portfolio Projected Payments"
        self.rollCurr = rollCurr
        self.counterCurr = counterCurr
        self.rollTo = rollTo
        self.maxRollTo = maxRollTo
        self.currPair = currPair
        self.config = None
        self.fundPort = None
        self.splitCurr = None
        self.fundAcq = None
        self.yearsBetween = acm.GetFunction('yearsBetween', 4)
        self.splitting = False
        self.mappedFundingInst = None
        self.mtmDate = mtmDate
        self.rollDate = rollDate
        self.nextTradingDate = nextTradingDate
        # Compatibility with previous tasks
        self.pointsPerDay = True
        self.calendar = None
        if currPair:
            self.calendar = currPair.SpotCalendar()
        if not self.calendar:
            if self.rollCurr:
                self.calendar = self.rollCurr.Calendar()

    def getRollPeriod(self):
        today = self.nextTradingDate
        tomorrow = self.calendar.AdjustBankingDays(self.nextTradingDate, 1)
        if self.currPair:
            spot = self.currPair.SpotDate(self.nextTradingDate)
        else:
            spot = self.rollCurr.SpotDate(self.nextTradingDate)
        spotNext = self.calendar.AdjustBankingDays(spot, 1)
        if (self.rollDate == today) and (self.rollTo == tomorrow):
            return 1
        elif (self.rollDate == tomorrow) and (self.rollTo == spot):
            return 2
        elif (self.rollDate == spot) and (self.rollTo == spotNext):
            return 3
        else:
            raise Exception('Unrecognised Roll Period')

    def getSplittingCurrency(self):
        return self.splitCurr

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

    def _getSpotFX(self, mtmMarket=None):
        spotDate = self.rollCurr.CurrencyPair(self.counterCurr).SpotDate(
                acm.Time().DateNow())
        rate = FFxCommon.getFxRate(spotDate, self.rollCurr, self.counterCurr)
        if rate:
            msgType = 'DEBUG'
        else:
            msgType = 'ERROR'
        message = 'Latest {0}-{1} rate for spot delivery on {2}: {3}.'.format(
                self.rollCurr.Name(), self.counterCurr.Name(), spotDate, rate)
        Logme()(message, msgType)
        return rate

    # Today's mark-to-market FX rate for spot delivery.
    def _getHistoricalFX(self, mtmMarket):
        rate = self._getMtMRate(self.rollCurr, self.mtmDate, self.counterCurr,
                '', mtmMarket)
        if not rate:
            Logme()('Trying inverse rate {0}-{1}...'.format(
                    self.counterCurr.Name(), self.rollCurr.Name(), 'INFO'))
            inverse = self._getMtMRate(self.counterCurr, self.mtmDate,
                    self.rollCurr, '', mtmMarket)
            if inverse:
                rate = 1. / inverse
        if rate:
            msgType = 'DEBUG'
        else:
            msgType = 'ERROR'
        message = 'MtM {0}-{1} rate on {2} for spot delivery: {3}.'.format(
                self.rollCurr.Name(), self.counterCurr.Name(), self.mtmDate,
                rate)
        Logme()(message, msgType)
        return rate

    def getDiscountFactor(self, fromDate, toDate, bidAsk, counterBidAsk,
            mtmMarket=None):
        rollRate, rollTimeInYears = self.getEffectiveRate(self.rollCurr,
                bidAsk, fromDate, toDate, mtmMarket)
        counterRate, counterTimeInYears = self.getEffectiveRate(
                self.counterCurr, counterBidAsk, fromDate, toDate, mtmMarket)
        return self.calcDiscountFactor(rollRate, counterRate, rollTimeInYears,
                counterTimeInYears)

    def _getSpotPoints(self, instr, fromDate, curr, bidAsk, mtmMarket=None):
        calcValue = instr.Calculation().MarketPrice(FFxCommon.space, fromDate,
                0, curr, 1, None, 0, 'Average' + bidAsk + 'Price', 1).Value()
        if not self.checkDenominatedValue(calcValue):
            message = ('Invalid spot points found for swap funding instrument '
                    '{0} ({1}) on {2}'.format(self.mappedFundingInst.Name(),
                    curr.Name(), fromDate))
            Logme()(message, 'ERROR')
            return 0.0

        points = calcValue.Number()
        Logme()("Spot {0} points for {1} ({2}) on {3}: {4}.".format(
                bidAsk.lower(), self.mappedFundingInst.Name(), curr.Name(),
                fromDate, points, 'DEBUG'))
        return points

    def getPointsOnFundInst(self, rollCurr, date, bidAsk, counterBidAsk,
            mtmMarket=None):
        curr = self.mappedFundingInst.Currency()
        if curr.Name() == rollCurr.Name():
            useBidAsk = bidAsk
        else:
            useBidAsk = counterBidAsk

        points = self.getSwapPoints(self.mappedFundingInst, date, curr,
                useBidAsk, mtmMarket)
        if not points:
            message = ('Using {3} swap points of zero for {0} ({1}) on '
                    '{2}.'.format(self.mappedFundingInst.Name(), curr.Name(),
                    date, useBidAsk.lower()))
            Logme()(message, 'WARNING')
        return points

    def getTotalPointsOnFundInst(self, date, bidAsk, counterBidAsk,
            mtmMarket=None):
        totalPoints = 0.0
        if not self.mappedFundingInst:
            raise Exception('No mapped funding instrument')
        totalPoints = self.getPoints(self.mtmDate, bidAsk, counterBidAsk,
                        mtmMarket)
        if self.pointsPerDay == True:
            days = acm.Time().DateDifference(self.maxRollTo, date)
            totalPoints = totalPoints * days
            message = ('for {0} days. Total points: {1}'.format(days,
            totalPoints))
            Logme()(message, 'DEBUG')

        return totalPoints

    def getPoints(self, date, bidAsk, counterBidAsk, mtmMarket=None):
        points = self.getPointsOnFundInst(self.rollCurr, date, bidAsk,
                counterBidAsk, mtmMarket)
        if not self.currPair:
            msg = 'Currency Pair in curInfo ({0}, {1}) does not exist.'.format(
                    self.rollCurr.Name(), self.counterCurr.Name())
            raise Exception(msg)
        pointValue = self.currPair.PointValue()
        totalPoints = points * pointValue
        message = ('Points for {0} = {1} = {2} points * {3} per '
                'point'.format(date, totalPoints, points, pointValue))
        Logme()(message, 'DEBUG')
        return totalPoints

    def calcDiscountFactor(self, rollRate, counterRate, rollTimeInYears,
            counterTimeInYears):
        if None in (rollRate, counterRate):
            return None
        rollDiscount = 1 + rollRate / 100.0 * rollTimeInYears
        counterDiscount = 1 + counterRate / 100.0 * counterTimeInYears
        if counterDiscount != 0.0:
            return rollDiscount / counterDiscount
        return None

    def getEffectiveRate(self, curr, bidAsk, fromDate, toDate, mtmMarket=None):
        """
        This returns the funding instrument rate as a simple rate.
        """
        rate, dayCountMethod, fundingType = self.getRate(curr, bidAsk, toDate,
                mtmMarket)
        rate, timeInYears = self.convertToSimpleRate(rate, fundingType,
                fromDate, toDate, dayCountMethod, curr.Calendar())
        return rate, timeInYears

    def _getSpotRate(self, fundingRate, date, curr, bidAsk, mtmMarket=None):
        calcValue = fundingRate.Calculation().MarketPrice(FFxCommon.space,
                date, 0, curr, 1, None, 0, 'Average' + bidAsk + 'Price',
                1).Value()
        if not self.checkDenominatedValue(calcValue):
            message = "Invalid spot rate found for {0} ({1}).".format(
                    fundingRate.Name(), curr.Name())
            Logme()(message, 'ERROR')
            return 0.0

        rate = calcValue.Number()
        Logme()("Latest {0} ({1}) {2} rate: {3}.".format(
            fundingRate.Name(), curr.Name(), bidAsk.lower(), rate, 'DEBUG'))
        return rate

    def _getMtMRate(self, instr, date, curr, bidAsk, mtmMarket):
        if (bidAsk != 'Bid') and (bidAsk != 'Ask'):
            bidAsk = 'Settle'

        rate = FFxCommon.getMtMRate(instr, curr, bidAsk, mtmMarket,
            self.mtmDate)
        return rate

    def getRate(self, curr, bidAsk, date, mtmMarket=None):
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
        if self.mappedFundingInst:
            fundingRate = self.mappedFundingInst

        if not fundingRate:
            Logme()('Missing funding rate instrument. Using zero funding.',
                    'ERROR')
            return (0.0, defaultDayCountMethod, defaultFundingType)

        rate = self.getInterestRate(fundingRate, date, curr, bidAsk, mtmMarket)
        if not rate:
            message = ("Using zero funding rate for {0} on spot date "
                    "{1}.".format(curr.Name(), date))
            Logme()(message, 'ERROR')
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
            totalR = math.exp(rate / 100.0 * timeInYears) - 1.0
            return (100.0 * (totalR / timeInYears), timeInYears)
        elif fundingType == HistoricalFinancing_DailyCompounding:
            daysInYear = acm.Time.YearLength(dayCountMethod)
            timeInDays = daysInYear * timeInYears
            totalR = ((1.0 + rate / 100.0 / daysInYear) ** timeInDays) - 1.0
            return (100.0 * (totalR / timeInYears), timeInYears)
        elif fundingType == HistoricalFinancing_Simple:
            return (rate, timeInYears)
        else:
            raise TypeError("Parameter 'fundingType' is not a supported "
                    "value " + fundingType)
