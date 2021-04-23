""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pl_processing/etc/FPLSweep_Perform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPLSweep_Perform - Module which performs FPLSweep.

    Requirements:

    For the time from our tomorrow to next spot date after our tomorrow
    inclusive ('Spot next') or the time from our today to next spot date
    inclusive ('Spot'), iterate over each FX trading portfolio, over each
    currency, over each calendar date. If there is a cashflow on that day,
    create a plsweep trade in the trading portfolio to net the position
    to zero, and create a mirror of the plsweep trade (i.e. a funding trade)
    in the funding portfolio. The purpose is to present the trader with
    a zero position in each currency pair at the beginning of each day.

DESCRIPTION
    This module performs the PL Sweep procedure based on the
    parameters passed from the script FPLSweep.

----------------------------------------------------------------------------"""


import math
import traceback
from collections import namedtuple

import acm
import FFxCommon
import FBDPCommon
import FBDPRollback
import FBDPValidation
import FPLSweep_Columns

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


USE_MTM_PRICE_TODAY_NO = 0
USE_MTM_PRICE_TODAY_FALLBACK = 1
USE_MTM_PRICE_TODAY_ONLY = 2
PROJ_PL = "Portfolio Points Profit And Loss"
THEO_PL = 'Portfolio Theoretical Total Profit and Loss'


# PL instrument, and sweep and PL currencies.
_NodeCurrencies = namedtuple('_NodeCurrencies', ('instr', 'sweep', 'pAndL'))


def perform_sweep(execParam):
    FPLSweep_Columns.Apply()
    r = Sweep(execParam)
    r.perform(execParam)
    FPLSweep_Columns.Remove()
    r.end()


def _getRollbackName(execParam):
    rollbackName = execParam.get('RollbackID', '')
    if not rollbackName:
        rollbackName = 'PLSweep'
    if len(rollbackName) > FBDPRollback.Rollback.NAME_MAX_LEN:
        rollbackName = rollbackName[:FBDPRollback.Rollback.NAME_MAX_LEN]
        Logme()('The rollback identifier allows up to {0} characters. '
                'The name \'{1}\' will be used.'.format(
                FBDPRollback.Rollback.NAME_MAX_LEN, rollbackName), 'WARNING')
    return rollbackName


def _getSweepCurrencies(plCurrencies, tradingPort):
    # Build currency list for projected payment
    excludedCurrencies = []

    instrument, sweepCurrency, currency = plCurrencies
    if instrument.InsType() == 'Curr':
        excludedCurrencies.append(instrument)
    excludedCurrencies.append(sweepCurrency)
    excludedCurrencies.append(currency)

    portCurrencyPair = tradingPort.CurrencyPair()
    if portCurrencyPair:
        excludedCurrencies.append(portCurrencyPair.Currency1())
        excludedCurrencies.append(portCurrencyPair.Currency2())

    allCurrencies = acm.FCurrency.Select('')
    allCurrenciesList = [curr for curr in allCurrencies]
    return ([curr for curr in allCurrenciesList
        if curr not in excludedCurrencies])


class Sweep(FBDPRollback.RollbackWrapper, FFxCommon.FxPortfolioProcess):
    def __init__(self, execParam):
        FBDPRollback.RollbackWrapper.__init__(self,
                rollbackName=_getRollbackName(execParam), Testmode=0,
                param=execParam)
        FFxCommon.FxPortfolioProcess.__init__(self)

    def getTrades(self, obj):
        allTrades = FFxCommon.TimeOrPorfolioSheet.getTrades(self, obj)
        if self.retainPL:
            return [t for t in allTrades if t.Type() != 'PL Sweep']
        else:
            return allTrades

    def getCurrObjects(self, currPair):
        if currPair:
            query = "name <> '%s' and name <> '%s'" % (
                    currPair.Currency1().Name(), currPair.Currency2().Name())
        else:
            query = "name <> '%s'" % self.plCurr.Name()
        return acm.FCurrency.Select(query)

    def perform(self, args):
        self.performProcess(args)

    def readArguments(self, args):
        FFxCommon.FxPortfolioProcess.readArguments(self, args)
        self.fxBaseCurrency = acm.ObjectServer().UsedValuationParameters(
                ).FxBaseCurrency()
        self.accountingCurrency = acm.ObjectServer().UsedValuationParameters(
                ).AccountingCurrency()
        self.tradingCalendar = self.accountingCurrency.Calendar()
        if args['TradingCalendar']:
            self.tradingCalendar = args['TradingCalendar'][0]

        today = acm.Time.DateToday()
        self.sweepPLToday = args.get('SweepPLToday', 0)
        if not self.sweepPLToday:
            self.nextTradingDate = args['NextTradingDate']
            if self.nextTradingDate == 'Tom next':
                self.nextTradingDate = today
            elif self.nextTradingDate == 'Spot next':
                self.nextTradingDate = self.tradingCalendar.AdjustBankingDays(
                        today, 1)
            else:
                self.nextTradingDate = FBDPCommon.toDate(self.nextTradingDate)
            if self.tradingCalendar.CalendarInformation(
                        ).IsNonBankingDay(self.nextTradingDate):
                self.nextTradingDate = self.tradingCalendar.AdjustBankingDays(
                        self.nextTradingDate, 1)
        else:
            self.nextTradingDate = today

        self.plPortfolio = args['PLPortfolio'][0]
        self.PLAcquirer = self.plPortfolio.PortfolioOwner()
        if args['PLAcquirer']:
            self.PLAcquirer = args['PLAcquirer'][0]
        self.plCurr = args['PLCurrency']

        self.mappedInstrument = args.get('MappedInstrument', {})
        self.mappedFundingInstruments = args.get('MappedFundingInstruments',
                {})
        self.plExtractionTrades = []
        self.useMtMforCalc = args.get('UseMtMforCalc', 0)
        self.useMtMforConv = args.get('UseMtMforConv', 0)
        self.spotForwardPLValue = args.get('SpotForwardPLValue', THEO_PL)
        self.sweepPLCurrencyIfInPair = args.get('SweepPLCurrencyIfInPair', 1)
        self.sweepAccountingCurrencyIfInPair = args.get(
            'AccountingCurrencyIfInPair', 1)
        self.sweepFXBaseCurrencyIfInPair = args.get(
            'SweepFXBaseCurrencyIfInPair', 0)
        self.retainPL = args.get('RetainPL', 0)
        self.mtmMarket = None
        if self.useMtMforConv:
            if 'MtMMarket' in args and args['MtMMarket']:
                self.mtmMarket = args['MtMMarket'][0]
        self.usePayment = args.get('UsePayments', 1)
        self.convert = args.get('ConvertInTradingPortfolio', 0)

        Logme()('Using PL Portfolio:  "%s".' % (self.plPortfolio.Name()))
        Logme()('Using PL Currency:  "%s".' % (self.plCurr.Name()))

    def requiredSubAttributesNotSet(self):
        msg = ''
        if not self.PLAcquirer:
            msg += 'PLAcquirer or PortfolioOwner of the PLPortfolio ' + \
                    'must be set'
        if self.useMtMforConv and not self.mtmMarket:
            msg += "No MtM market specified for funding rates."
        if not self.defaultAcquirer:
            if not self.portfolioGrouper:
                msg += 'You must either specify a default acquirer' + \
                    ' or an acquirer grouper'
            elif isinstance(self.portfolioGrouper, type(list())):
                if self.portfolioGrouper[0].IsKindOf(acm.FChainedGrouper):
                    for g in self.portfolioGrouper[0].Groupers():
                        method = g.Method()
                        if method.AsString().find("Acquirer"):
                            return msg
                    msg += 'You must either specify a default acquirer' + \
                        ' or an acquirer grouper'
            elif self.portfolioGrouper.IsKindOf(acm.FArray):
                if self.portfolioGrouper.IsEmpty():
                    msg += 'You must either specify a default acquirer' + \
                        ' or an acquirer grouper'
            elif self.portfolioGrouper.IsKindOf(acm.FChainedGrouper):
                for g in self.portfolioGrouper.Groupers():
                    method = g.Method()
                    if method.AsString().find("Acquirer"):
                        return msg
                msg += 'You must either specify a default acquirer' + \
                    ' or an acquirer grouper'
        return msg

    def validateMode(self):
        if acm.ArchivedMode():
            errMsg = 'This script must not be run in Archived mode.'
            raise RuntimeError(errMsg)
        if acm.IsHistoricalMode():
            errMsg = 'This script must not be run in Historical mode.'
            raise RuntimeError(errMsg)
        return True

    def validateValuationParams(self):
        FBDPValidation.FBDPValidate.validateValuationParams(self)
        return True

    def _getSpecifiedFXRate(self, payDate, toCurr, fromCurr, fundInstr,
            bidAsk=''):
        """
        Returns either the latest or the mark-to-market rate for the specified
        payDate discounted from the (latest or mark-to-market) spot FX using
        the forward points on the swap funding instrument passed in.
        """
        currPair = FFxCommon.currencyPair(toCurr, fromCurr)
        spotDate = currPair.SpotDate(self.nextTradingDate)
        points = 0.

        if self.useMtMforConv:
            quotedRate = FFxCommon.getMtMFXRate(currPair.Currency1(),
                    currPair.Currency2(), self.mtmMarket, spotDate)
            if payDate != spotDate:
                points = FFxCommon.getMtMSwapPoints(currPair, fundInstr,
                        payDate, spotDate, self.mtmMarket, bidAsk)
        else:
            quotedRate = FFxCommon.getFxRate(spotDate, currPair.Currency1(),
                    currPair.Currency2())
            if payDate != spotDate:
                points = FFxCommon.getLatestSwapPoints(currPair, fundInstr,
                        payDate, spotDate, bidAsk)

        if toCurr == currPair.Currency1():
            fxRate = quotedRate - points
        else:
            fxRate = 1. / (quotedRate - points)
        return fxRate

    def _getImpliedFXRate(self, payDate, toCurr, fromCurr):
        """
        Returns either the latest or marked-to-market FX rate for the requested
        date, as calculated by the CalcSpace based on yield curves set up by
        the user.
        """
        if self.useMtMforConv:
            return FFxCommon.getMtMFXRate(toCurr, fromCurr, self.mtmMarket)
        return FFxCommon.getFxRate(payDate, toCurr, fromCurr)

    def _getValidFXRate(self, payDate, toCurr, fromCurr, bidAsk=''):
        if toCurr == fromCurr:
            return 1.0

        currPair = FFxCommon.currencyPair(toCurr, fromCurr)
        fundInstr = self.getMappedFundingInstrument(currPair)

        if not (fundInstr and fundInstr.InsType() == 'FxSwap'):
            fxRate = self._getImpliedFXRate(payDate, toCurr, fromCurr)
        else:
            fxRate = self._getSpecifiedFXRate(payDate, toCurr, fromCurr,
                    fundInstr, bidAsk)

        if any([not fxRate, math.isinf(fxRate), math.isnan(fxRate)]):
            Logme()('Neither {0}/{1} nor {1}/{0} valid Fx rate is available.'.
                    format(toCurr.Name(), fromCurr.Name()), 'DEBUG')
            return None
        return fxRate

    def _getSweepCurrencyFromCurrencyPair(self, currPair):
        curr1, curr2 = currPair.Currency1(), currPair.Currency2()
        sweepCurrency = None

        if (self.fxBaseCurrency in (curr1, curr2)
                and self.sweepFXBaseCurrencyIfInPair):
            sweepCurrency = self.fxBaseCurrency

        if (self.accountingCurrency in (curr1, curr2)
                and self.sweepAccountingCurrencyIfInPair):
            sweepCurrency = self.accountingCurrency

        if self.plCurr in (curr1, curr2) and self.sweepPLCurrencyIfInPair:
            sweepCurrency = self.plCurr

        if not sweepCurrency:
            sweepCurrency = currPair.SweepCurrency()
            if not sweepCurrency:
                sweepCurrency = curr2
        return sweepCurrency

    def _byCurrencySplitGroup(self):
        currencySplit = acm.FCurrency[self.attributes['Currency Split']]
        return _NodeCurrencies(currencySplit, currencySplit, currencySplit)

    def _byInstrumentTypeGroup(self, node):
        attributes = self.attributes
        Logme()('Getting PL instrument and sweep currency from Instrument '
                'Type grouping.', 'DEBUG')
        insType = attributes['Instrument Type']
        insCurr = None
        if 'Instrument.Currency' in attributes:
            insCurr = attributes['Instrument.Currency']
        trade = self.tradeAtNode(node)

        # Instrument Currency exists
        if insCurr:
            insTypeCurr = str(insType) + '/' + str(insCurr)
            if insTypeCurr in self.mappedInstrument:
                return _NodeCurrencies(
                        acm.FInstrument[self.mappedInstrument[insTypeCurr]],
                        acm.FCurrency[insCurr],
                        acm.FInstrument[self.mappedInstrument[
                                insTypeCurr]].Currency())

            instrument = self.instrumentAtNode(node)
            if not instrument:
                Logme()('Could not find representative instrument for '
                        '{0}.'.format(insTypeCurr), 'ERROR')
                return _NodeCurrencies(None, None, None)
            curr = instrument.Currency()
            if insType == 'Fx Rate':
                return _NodeCurrencies(trade.Instrument(), curr,
                        trade.Currency())
            return _NodeCurrencies(instrument, curr, curr)
        else:
            # Use PL currency
            insTypeCurr = str(insType) + '/' + self.plCurr.Name()
            if insTypeCurr in self.mappedInstrument:
                return _NodeCurrencies(
                        acm.FInstrument[self.mappedInstrument[insTypeCurr]],
                        self.plCurr,
                        acm.FInstrument[self.mappedInstrument[
                                insTypeCurr]].Currency())
            instrument = self.instrumentAtNode(node)
            if not instrument:
                return _NodeCurrencies(None, None, None)
            if insType == 'Fx Rate':
                currPair = FFxCommon.currencyPair(trade.Instrument(),
                        trade.Currency())
                return _NodeCurrencies(currPair.Currency1(), self.plCurr,
                        currPair.Currency2())
            return _NodeCurrencies(instrument, self.plCurr,
                    instrument.Currency())

    def _byInstrumentGroup(self):
        Logme()('Getting PL instrument and sweep currency from Instrument '
                'grouping.', 'DEBUG')
        ins = self.attributes['Instrument.Instrument']
        currPair = acm.FCurrencyPair[ins]
        if currPair:
            sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
            return _NodeCurrencies(currPair.Currency1(), sweepCurrency,
                    currPair.Currency2())

        instrument = acm.FInstrument[ins]
        if instrument:
            return _NodeCurrencies(acm.FInstrument[ins],
                        acm.FInstrument[ins].Currency(),
                        acm.FInstrument[ins].Currency())
        if '/' in ins:
            curr1Name, curr2Name = ins.split("/")
            curr1 = acm.FCurrency[curr1Name]
            curr2 = acm.FCurrency[curr2Name]
            if curr1 and curr2:
                cpair = FFxCommon.currencyPair(curr2, curr1)
                if cpair:
                    sweepCurrency = self._getSweepCurrencyFromCurrencyPair(
                        cpair)
                    return _NodeCurrencies(curr1, sweepCurrency, curr2)
                return _NodeCurrencies(None, None, None)
        return _NodeCurrencies(None, None, None)

    def _byCurrencyGroup(self, insCurr):
        Logme()('Getting PL instrument and sweep currency from Instrument '
                'Currency grouping.', 'DEBUG')
        return _NodeCurrencies(acm.FCurrency[insCurr],
                acm.FCurrency[insCurr],
                acm.FCurrency[insCurr])

    def _byPortfolioCurrencies(self, portfolio):
        currPair = portfolio.CurrencyPair()
        if currPair:
            sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
            return _NodeCurrencies(currPair.Currency1(), sweepCurrency,
                    currPair.Currency2())
        portCurr = portfolio.Currency()
        return _NodeCurrencies(portCurr, portCurr, portCurr)

    def _byAccountingandSweepCurr(self, portfolio):
        currPair = portfolio.CurrencyPair()
        if currPair:
            sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        else:
            sweepCurrency = portfolio.Currency()
        return _NodeCurrencies(self.plCurr, sweepCurrency, self.plCurr)

    def _byInstrumentCurrency(self, currPair, pairPosition):
        curr1 = currPair.Currency1()
        curr2 = currPair.Currency2()
        sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        icPosition = self._positionInChain('Instrument.Currency')
        insCurr = acm.FCurrency[self.attributes['Instrument.Currency']]
        if icPosition > pairPosition:
            if curr1 == insCurr:
                return _NodeCurrencies(curr2, insCurr, curr1)
            return _NodeCurrencies(curr1, insCurr, curr2)

        if curr1 == insCurr:
            return _NodeCurrencies(curr2, sweepCurrency, curr1)
        return _NodeCurrencies(curr1, sweepCurrency, curr2)

    def _byCurrencyInstrument(self, currPair):
        attrInsIns = self.attributes['Instrument.Instrument']
        curr1 = currPair.Currency1()
        curr2 = currPair.Currency2()
        curr1Name, _curr2Name = attrInsIns.split("/")
        sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        if acm.FCurrency[curr1Name] == curr1:
            return _NodeCurrencies(curr1, sweepCurrency, curr2)
        return _NodeCurrencies(curr2, sweepCurrency, curr1)

    def _byUnderlyingCurrency(self, currPair, pairPosition):
        undPosition = self._positionInChain('Underlying')
        und = acm.FCurrency[self.attributes['Underlying']]
        curr1 = currPair.Currency1()
        curr2 = currPair.Currency2()
        sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        if undPosition > pairPosition:
            if curr2 == und:
                return _NodeCurrencies(curr2, und, curr1)
            return _NodeCurrencies(curr1, und, curr2)
        if curr2 == und:
            return _NodeCurrencies(curr2, sweepCurrency, curr1)
        return _NodeCurrencies(curr1, sweepCurrency, curr2)

    def _byCurrencyPairGroup(self):
        Logme()('Getting PL instrument and sweep currency from Currency Pair '
                'grouping.', 'DEBUG')

        attributes = self.attributes
        cpName = attributes[FFxCommon.CURRENCY_PAIR]
        currPair = acm.FCurrencyPair[cpName]
        pairPosition = self._positionInChain(FFxCommon.CURRENCY_PAIR)

        if 'Instrument.Currency' in attributes:
            return self._byInstrumentCurrency(currPair, pairPosition)
        elif 'Instrument.Instrument' in attributes:
            return self._byCurrencyInstrument(currPair)
        elif 'Underlying' in attributes:
            return self._byUnderlyingCurrency(currPair, pairPosition)

        sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        return _NodeCurrencies(currPair.Currency1(), sweepCurrency,
                currPair.Currency2())

    def _byUnderlyingGroup(self, portfolio, node):
        Logme()('Getting PL instrument and sweep currency from Underlying '
                'grouping.', 'DEBUG')

        repTrade = self.tradeAtNode(node)
        if (repTrade.Instrument().InsType() == 'Curr' and
                repTrade.Instrument() != repTrade.Currency()):
            plIns = FFxCommon.currencyPair(repTrade.Instrument(),
                    repTrade.Currency())
        elif repTrade.Instrument().InsType() == 'Commodity Variant':
            plIns = repTrade.Instrument()
        else:
            plIns = repTrade.Instrument().Underlying().Instrument()

        insCurr = self.attributes.get('Instrument.Currency', None)
        if insCurr:
            return _NodeCurrencies(plIns, acm.FCurrency[insCurr],
                    plIns.Currency())
        return _NodeCurrencies(plIns, portfolio.Currency(), plIns.Currency())

    def _byPositionOrCurrencyPairGroup(self):
        Logme()('Getting PL instrument and sweep currency from '
                'Position Or Currency Pair grouping.', 'DEBUG')

        attributes = self.attributes
        cpName = attributes['PositionOrCurrencyPair']
        currPair = acm.FCurrencyPair[cpName]

        sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        return _NodeCurrencies(currPair.Currency1(), sweepCurrency,
                currPair.Currency2())

    def _byPositionOrInstrumentPairGroup(self):
        Logme()('Getting PL instrument and sweep currency from '
                'Position Or Currency Pair grouping.', 'DEBUG')

        attributes = self.attributes
        cpName = attributes['PositionOrInstrumentPair']
        currPair = acm.FCurrencyPair[cpName]

        sweepCurrency = self._getSweepCurrencyFromCurrencyPair(currPair)
        return _NodeCurrencies(currPair.Currency1(), sweepCurrency,
                currPair.Currency2())

    def _getPLInstrumentAndSweepCurrency(self, portfolio, node):
        attributes = self.attributes
        #Currency Split in the grouper
        if 'Currency Split' in attributes:
            return self._byCurrencySplitGroup()

        #Currency Pair in the grouper
        if (FFxCommon.CURRENCY_PAIR in attributes and
                attributes[FFxCommon.CURRENCY_PAIR] != 'No Currency Pair'):
            return self._byCurrencyPairGroup()

        #PositionOrCurrencyPair in the grouper
        if ('PositionOrCurrencyPair' in attributes and
                attributes['PositionOrCurrencyPair'] !=
                    'No Trade: PositionOrCurrencyPair'):
            return self._byPositionOrCurrencyPairGroup()

        #PositionOrInstrumentPair in the grouper
        if ('PositionOrInstrumentPair' in attributes and
                attributes['PositionOrInstrumentPair'] !=
                    'No Trade: PositionOrInstrumentPair'):
            return self._byPositionOrInstrumentPairGroup()

        #Instrument in the grouper
        if 'Instrument.Instrument' in attributes:
            return self._byInstrumentGroup()

        #Instrument Type in the grouper
        if 'Instrument Type' in attributes:
            return self._byInstrumentTypeGroup(node)

        #Instrument Underlying.
        if 'Underlying' in attributes:
            return self._byUnderlyingGroup(portfolio, node)

        #Other grouper and no grouper cases.
        if 'Instrument.Currency' in attributes:
            return self._byCurrencyGroup(attributes['Instrument.Currency'])

        if self.convert:
            return self._byAccountingandSweepCurr(portfolio)

        return self._byPortfolioCurrencies(portfolio)

    def _getCurrenciesForNode(self, tradingPort, topNode):
        plCurrencies = self._getPLInstrumentAndSweepCurrency(tradingPort,
                topNode)
        if all(plCurrencies):
            for s, c in zip(("Sweep currency", "PL currency", "PL instrument"),
                    (plCurrencies.sweep, self.plCurr, plCurrencies.instr)):
                Logme()("{0} {1} spot date for next trading date {2}: "
                        "{3}".format(s, c.Name(), self.nextTradingDate,
                            c.SpotDate(self.nextTradingDate)), "DEBUG")
        else:
            Summary().fail(tradingPort, Summary().SWEEP, 'Could not '
                    'find PL Instrument, Sweep currency or currency '
                    'for the position', tradingPort.Name())
        return plCurrencies

    def _createZeroNominalTrade(self, instrument, currency, portfolio,
            acquirer, counterparty, date, price, tradetype, trade_process):
        #Create Zero trade
        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(currency)
        # overridden from self.attributes if grouped on acq
        trade.Acquirer(acquirer)
        trade.Counterparty(counterparty)
        trade.Trader(acm.User())
        trade.Type(tradetype)
        trade.Status('Internal')
        trade.Price(price)
        trade.ReferencePrice(price)
        trade.Quantity(0)
        trade.Premium(0)
        tradeTime = acm.Time.DateNow()
        if acm.Time().DateDifference(tradeTime, date) > 0:
            tradeTime = date
        trade.TradeTime(tradeTime)
        trade.AcquireDay(date)
        trade.ValueDay(date)
        trade.TradeProcess(trade_process)
        trade.Portfolio(portfolio)
        return trade

    def setTradePropertiesFromGrouperInPLPort(self, trade,
                    excludedAttributes=()):
        if self.attributes:
            for key, val in self.attributes.iteritems():
                if key not in excludedAttributes:
                    try:
                        if 'OptKey' in key:
                            val = self.getOptKeyObject(key, val)
                        if ('PositionOrCurrencyPair' in key or
                            'PositionOrInstrumentPair' in key):
                            key = 'PositionPair'
                        if key == 'Acquirer':
                            key = 'Counterparty'
                        elif key == 'Counterparty':
                            key = 'Acquirer'
                        elif key == 'MasterTrade':
                            key = 'Acquirer'
                        trade.SetProperty(key, val)
                    except Exception as e:
                        msg = "Ignored setting {0} on trade as {1}".format(
                                key, str(e))
                        Logme()(msg, "DEBUG")

    def setTraderonMirrorSweepTrade(self, sweepTrade):
        mirrorTrade = sweepTrade.MirrorTrade()  # Attempt to set the
        mirrorTrade.Trader(sweepTrade.Trader())  # Trader
        self.beginTransaction()
        self.add_trade(mirrorTrade)
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return FFxCommon.RESULT_FAIL, mirrorTrade

    def _createZeroPLTrade(self, instrument, currency, portfolio, acquirer,
            date, price, tradetype="Normal", trade_process=4096):
        trade = self._createZeroNominalTrade(instrument, currency, portfolio,
                acquirer, self.defaultAcquirer, date, price, tradetype,
                trade_process)
        self.setTradePropertiesFromGrouperInPLPort(trade, ('Portfolio'))
        return trade

    def _createPLPaymentTrade(self, instrument, currency, portfolio, acquirer,
            date, price, pl, sweepCurrency, tradetype="Normal",
            trade_process=4096):
        trade = self._createZeroNominalTrade(instrument, currency, portfolio,
                acquirer, self.defaultAcquirer, date, price, tradetype,
                trade_process)
        #Create cash payment in sweep currency for the zero trade
        payment = self._createTradePayment(trade, date, pl, sweepCurrency)
        self.setTradePropertiesFromGrouperInPLPort(trade, ('Portfolio'))
        return trade, payment

    def _createPLTrade(self, instrument, currency, portfolio, acquirer,
            date, price, pl, sweepCurrency, tradetype="Normal",
            trade_process=4096):
        #Create zero nominal PL trade
        trade = self._createZeroNominalTrade(instrument, currency, portfolio,
                acquirer, self.defaultAcquirer, date, price, tradetype,
                trade_process)
        #Update PL in quantity or premium, the if statement order
        #make sure the quantity is set on cash payment trade
        if sweepCurrency == instrument:
            trade.Quantity(pl)
        elif currency == sweepCurrency:
            trade.Premium(pl)
        else:
            fxRate = self._getValidFXRate(self.spotDate,
                                        sweepCurrency, instrument)
            trade.Quantity(pl * fxRate)
        #Update grouping attribute
        self.setTradePropertiesFromGrouperInPLPort(trade, ('Portfolio'))
        return trade

    def _createMirrorPayment(self, trade, payment):
        mirrorTrade = trade.MirrorTrade()
        mirrorPayment = acm.FPayment()
        mirrorPayment.Trade(mirrorTrade)
        mirrorPayment.Type('Cash')
        mirrorPayment.Amount(-payment.Amount())
        mirrorPayment.Currency(payment.Currency())
        mirrorPayment.ValidFrom(payment.ValidFrom())
        mirrorPayment.PayDay(payment.PayDay())
        mirrorPayment.Party(mirrorTrade.Acquirer())
        return mirrorPayment

    def _createTradePayment(self, trade, valueDay, pl, sweepCurrency):
        payment = self._createPayment(valueDay, pl, sweepCurrency)
        payment.Trade(trade)
        payment.Party(trade.Acquirer())
        return payment

    def _createPayment(self, valueDay, pl, sweepCurrency):
        payment = acm.FPayment()
        payment.Type('Cash')
        payment.Currency(sweepCurrency)
        roundingForCurrency = self.getPremiumRounding(sweepCurrency)
        payment.Amount(FBDPCommon.roundValueForInstrument(pl,
                roundingForCurrency))
        payment.ValidFrom(acm.Time.DateToday())
        payment.PayDay(valueDay)
        return payment

    def _sellCashflow(self, instrument, currency, tradingPort, payments):
        assert payments, "_sellCashflow() called with no payments"

        self.printPL()
        paymentCurrList = [p.Currency() for p in payments]
        self.printCashBalance(paymentCurrList)

        # build zero trade
        value_day = self.nextTradingDate
        sweepTrade = self._createZeroPLTrade(instrument, currency,
                self.plPortfolio,
                self.PLAcquirer, value_day, 0, 'Normal')
        self.callAdjustTradeHook(sweepTrade, 'PL Sweep')

        # Commit the Zero trade and its mirror first if sweep trade is
        # newly created
        self.beginTransaction()
        sweepTrade.MirrorPortfolio(tradingPort)
        self.add_trade(sweepTrade)
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return FFxCommon.RESULT_FAIL, None

        self.beginTransaction()
        for payment in payments:
            payment.Trade(sweepTrade)
            payment.Party(sweepTrade.Counterparty())
            mirrorPayment = self._createMirrorPayment(sweepTrade, payment)
            self.add(payment)
            self.add(mirrorPayment)
            Logme()("Moving cashflow %s %s on %s to pl portfolio %s." % (
                    payment.Amount(),
                    payment.Currency().Name(), payment.PayDay(),
                    self.plPortfolio.Name()),
                    'DEBUG')
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return FFxCommon.RESULT_FAIL, None

        sweepTradeMirror = sweepTrade.MirrorTrade()
        self.container.Trades().Add(sweepTradeMirror)
        self.plExtractionTrades.append(sweepTrade)
        self.logCreatedMirrorTrade(sweepTrade)
        self.calcSpace.Refresh()

        self.printCashBalance(paymentCurrList)
        self.printPL()
        return FFxCommon.RESULT_SUCCESS, sweepTrade

    def _sellPLByTrades(self, pl, instrument, currency, value_day,
            tradingPort, sweepCurrency):

        #check if the PL can be ignored
        roundingForCurrency = self.getPremiumRounding(sweepCurrency)
        if math.fabs(FBDPCommon.roundValueForInstrument(pl,
                roundingForCurrency)) < 0.000001:
            return FFxCommon.RESULT_IGNORED, None

        #Create PL extraction trade
        sweepTrade = self._createPLTrade(instrument,
                    currency, self.plPortfolio, self.PLAcquirer,
                    value_day, 0, pl,
                    sweepCurrency, 'Normal')
        self.callAdjustTradeHook(sweepTrade, 'PL Sweep')
        self.beginTransaction()
        sweepTrade.MirrorPortfolio(tradingPort)
        self.add_trade(sweepTrade)
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return FFxCommon.RESULT_FAIL, None

        self.setTraderonMirrorSweepTrade(sweepTrade)
        sweepTradeMirror = sweepTrade.MirrorTrade()
        self.container.Trades().Add(sweepTradeMirror)
        self.plExtractionTrades.append(sweepTrade)
        self.logCreatedMirrorTrade(sweepTrade)
        self.calcSpace.Refresh()
        self.printPL(sweepCurrency)

        return FFxCommon.RESULT_SUCCESS, None

    def _sellPLByPayments(self, pl, instrument, currency, value_day,
            tradingPort, sweepCurrency, plExtractionTrade):

        # Create payment, and trade if there isn't one
        sweepTrade = None
        payment = None
        if not plExtractionTrade:
            sweepTrade, payment = self._createPLPaymentTrade(instrument,
                    currency, self.plPortfolio, self.PLAcquirer,
                    value_day, 0, pl,
                    sweepCurrency, 'Normal')
            self.callAdjustTradeHook(sweepTrade, 'PL Sweep')
        else:
            payment = self._createTradePayment(plExtractionTrade,
                    value_day, pl, sweepCurrency)

        # Ignore very small pl
        if math.fabs(payment.Amount()) < 0.000001:
            return FFxCommon.RESULT_IGNORED, plExtractionTrade

        # Commit the Zero trade and its mirror first if sweep trade is
        # newly created
        if sweepTrade:
            self.beginTransaction()
            sweepTrade.MirrorPortfolio(tradingPort)
            self.add_trade(sweepTrade)
            try:
                self.commitTransaction()
            except Exception:
                self.abortTransaction()
                Summary().abortEntries()
                traceback.print_exc()
                return FFxCommon.RESULT_FAIL, plExtractionTrade

            self.setTraderonMirrorSweepTrade(sweepTrade)
        # Commit payment and its mirror payment
        if sweepTrade:
            mirrorPayment = self._createMirrorPayment(sweepTrade, payment)
        else:
            mirrorPayment = self._createMirrorPayment(plExtractionTrade,
                    payment)
        self.beginTransaction()
        self.add(payment)
        self.add(mirrorPayment)
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return FFxCommon.RESULT_FAIL, plExtractionTrade

        if sweepTrade:
            sweepTradeMirror = sweepTrade.MirrorTrade()
            self.container.Trades().Add(sweepTradeMirror)
            self.plExtractionTrades.append(sweepTrade)
            self.logCreatedMirrorTrade(sweepTrade)
            plExtractionTrade = sweepTrade
        else:
            ts = self.container.Trades().AsIndexedCollection()
            size = self.container.Trades().AsIndexedCollection().Size()
            for i in range(size):
                if ts[i].Oid() == plExtractionTrade.MirrorTrade().Oid():
                    ts.RemoveAt(i)
                    break
            self.container.Trades().Add(plExtractionTrade.MirrorTrade())

        self.calcSpace.Refresh()
        self.printPL(sweepCurrency)

        return FFxCommon.RESULT_SUCCESS, plExtractionTrade

    def _sellPL(self, pl, instrument, currency, value_day, tradingPort,
            sweepCurrency, plExtractionTrade):
        if pl is None:
            return FFxCommon.RESULT_IGNORED, plExtractionTrade

        if math.isinf(pl) or math.isnan(pl):
            return FFxCommon.RESULT_FAIL, plExtractionTrade

        self.printPL(sweepCurrency)
        Logme()("Moving %s %s on %s to pl portfolio %s." % (pl,
                sweepCurrency.Name(), value_day, self.plPortfolio.Name()),
                'DEBUG')

        if self.convert:
            return self._sellPLByTrades(pl, instrument, currency, value_day,
                tradingPort, sweepCurrency)
        elif self.usePayment or (sweepCurrency != instrument
                and sweepCurrency != currency):
            return self._sellPLByPayments(pl, instrument, currency, value_day,
                tradingPort, sweepCurrency, plExtractionTrade)
        else:
            return self._sellPLByTrades(pl, instrument, currency, value_day,
                tradingPort, sweepCurrency)

    def _createSplitTrades(self, sweepDate, fromCurr, toCurr, splitCurr,
                amount, sweepPort, sweepAcquirer):

        # The sweep portfolio for the split trade from trading to split
        # currency will always be specified in terms of fromCurr/splitCurr
        splitPair = FFxCommon.currencyPair(fromCurr, splitCurr)
        splitPort, splitAcquirer = self.getPortfolioAndAcquirer(splitPair)

        if not splitPort:
            errMsg = ('Could not get sweep portfolio for '
                    'currency pair {0}.'.format(splitPair.Name()))
            Summary().fail(self.plPortfolio, Summary().SWEEP, errMsg,
                    self.plPortfolio.Name())
            return []

        # Create the split trade in the trade currency-PL currency sweep
        # portfolio and mirror it in the split currency-PL currency sweep
        # portfolio.
        sweepTrade = self._createFXTrade(splitCurr, fromCurr, sweepPort,
                sweepAcquirer, splitAcquirer, sweepDate, amount)
        if not sweepTrade:
            return []
        sweepTrade.MirrorPortfolio(splitPort)

        # Create a temporary split trade to get the PL currency amount, which
        # you then use to get the final amount converted from trading to PL
        # currency.
        splitAmount = sweepTrade.Quantity() * splitCurr.ContractSize()
        splitTrade = self._createFXTrade(toCurr, splitCurr, sweepPort,
                sweepAcquirer, splitAcquirer, sweepDate, splitAmount)
        if not splitTrade:
            return []
        plAmount = splitTrade.Quantity() * toCurr.ContractSize()
        plPair = FFxCommon.currencyPair(fromCurr, toCurr)
        _plPort, plAcquirer = self.getPortfolioAndAcquirer(plPair)
        plTrade = self._createFXTrade(fromCurr, toCurr, self.plPortfolio,
                self.PLAcquirer, plAcquirer, sweepDate, -1.0 * plAmount)
        if not plTrade:
            return []

        self._setConversionTradeProperties(plTrade, (not splitAcquirer))

        plTrade.MirrorPortfolio(sweepPort)

        return [sweepTrade, plTrade]

    def _createConversionTrades(self, sweep_date, fromCurr,
                                    toCurr, amount, portfolio=None):
        sweepPair = FFxCommon.currencyPair(fromCurr, toCurr)
        mirrorPort, conversionAcquirer = self.getPortfolioAndAcquirer(
                                            sweepPair)
        if self.convert:
            conversionPort = mirrorPort
            mirrorPort = portfolio
        else:
            conversionPort = self.plPortfolio
        # the conversion acquirer may be null
        if not mirrorPort:
            errMsg = ('Could not get conversion portfolio for '
                    'currency pair {0}.'.format(sweepPair.Name()))
            Summary().fail(self.plPortfolio, Summary().SWEEP, errMsg,
                    self.plPortfolio.Name())
            return []

        # You must explicitly map a portfolio, other than your default sweep
        # portfolio, to your currency pair if you want to split. See for
        # instance ZKB's use case PLSweepSetDefaultSweepPortAsTradingPort.xls.
        self.mappedPositionPairs.pop(self.defaultPortfolio.Name(), None)
        if mirrorPort != self.defaultPortfolio and not self.convert:
            splitCurr = self.getSplittingCurrency(fromCurr, toCurr,
                                                mirrorPort)
            if splitCurr:
                return self._createSplitTrades(sweep_date, fromCurr, toCurr,
                        splitCurr, amount, mirrorPort, conversionAcquirer)

        conversionTrade = self._createFXTrade(toCurr, fromCurr,
                conversionPort, self.PLAcquirer, conversionAcquirer,
                sweep_date, amount)
        if not conversionTrade:
            return []

        self._setConversionTradeProperties(conversionTrade,
            (not conversionAcquirer))

        conversionTrade.MirrorPortfolio(mirrorPort)
        return [conversionTrade]

    def _setConversionTradeProperties(self, trade, updateAcquirer):
        # Overrides properties based on grouping criteria
        if self.attributes:
            for key, val in self.attributes.items():
                # Note: The acquirer of the PL Conversion trades is actually
                # the counterparty of the mirrored trade, so we set the
                # counterparty so that the mirrored trade has the correct
                # acquirer
                try:
                    if key == 'Acquirer' and updateAcquirer:
                        trade.SetProperty('Counterparty', val)
                    elif key == 'Counterparty' and updateAcquirer:
                        trade.SetProperty('Acquirer', val)
                    if key not in ['Portfolio', 'CounterParty', 'Acquirer',
                                'Instrument']:
                        if 'OptKey' in key:
                            val = self.getOptKeyObject(key, val)
                        trade.SetProperty(key, val)
                except:
                    Logme()("Ignored setting %s on trade." %
                            key, 'DEBUG')

    def _createFXTrade(self, toCurr, fromCurr, portfolio, acquirer,
            counterparty, acquireDate, amount):
        """
        Returns amount converted from trading currency (fromCurr) to PL
        currency (toCurr).
        """
        # amount is in fromCurr.
        if FFxCommon.currencyPair(fromCurr, toCurr).Currency1() == fromCurr:
            bidAsk, ignore = FFxCommon.getBidAsk(amount)
        else:
            bidAsk, ignore = FFxCommon.getBidAsk(-amount)
        fxRate = self._getValidFXRate(acquireDate, toCurr, fromCurr, bidAsk)
        if not fxRate:
            message = 'Could not get fx rate'
            Summary().fail(fromCurr, 'sweep "%s"' % (fromCurr.Name()), message,
                    self.plPortfolio.Name())
            return None

        Logme()("Selling {0} {1} for PL currency {2} using rate {3} on value "
                "date {4}.".format(amount, fromCurr.Name(), toCurr.Name(),
                fxRate, acquireDate), 'DEBUG')
        quantity = -amount / fxRate / toCurr.ContractSize()
        price = fxRate
        premium = amount

        trade = self.createFxTrade(toCurr, fromCurr, portfolio, acquirer,
                counterparty, acquireDate, price, quantity, premium,
                'PL Sweep', 4096)
        self.callAdjustTradeHook(trade, 'PL Sweep')
        return trade

    def _sweepInPL(self, sweepInTrade, fromCurr, toCurr, payDate, amount):
        sweepInMirrorTrade = sweepInTrade.MirrorTrade()
        fxRate = self._getValidFXRate(self.spotDate, toCurr, fromCurr)
        if not fxRate:
            message = 'Could not get fx rate'
            Summary().fail(fromCurr, 'sweep "%s"' % (fromCurr.Name()),
                    message, trade.Portfolio().Name())
            return False

        Logme()('Selling %s %s on date %s using rate %s.' % (amount,
                fromCurr.Name(), payDate, fxRate), 'DEBUG')
        quantity = amount / fxRate / toCurr.ContractSize()
        newPayment = self._createTradePayment(sweepInTrade, payDate,
                quantity, toCurr)
        self.add(newPayment)
        mirrorPayment = self._createTradePayment(sweepInMirrorTrade,
                payDate, -quantity, toCurr)
        self.add(mirrorPayment)
        return True

    def _removeFXRisk(self, trade, toCurr):
        #Create zero sweep in trades
        sweepInTrade = self._createZeroNominalTrade(trade.Instrument(),
                trade.Currency(), self.plPortfolio, trade.Counterparty(),
                trade.Acquirer(), trade.ValueDay(), trade.Price(), 'PL Sweep',
                trade_process=4096)
        if not sweepInTrade:
            return False
        self.setTradePropertiesFromGrouper(sweepInTrade,
            ('Portfolio', 'Acquirer', 'Counterparty'))
        self.callAdjustTradeHook(sweepInTrade, 'PL Sweep')

        # Commit the Zero trade and its mirror first if sweep trade is
        # newly created
        sweepInTrade.MirrorPortfolio(trade.Portfolio())
        self.beginTransaction()
        self.add_trade(sweepInTrade)
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return False
        self.logCreatedMirrorTrade(sweepInTrade)

        # Check if PL in quantity or premium
        self.beginTransaction()
        if trade.Quantity() or trade.Premium():
            fromCurr, amount, payDate = self._getConversionTradeInfo(trade)
            if fromCurr == toCurr:
                aelClone = FBDPCommon.acm_to_ael(sweepInTrade).clone()
                aelClone.quantity = amount
                self.add(aelClone, ['quantity'])
            else:
                if not self._sweepInPL(sweepInTrade, fromCurr,
                        toCurr, payDate, amount):
                    self.abortTransaction()
                    Summary().abortEntries()
                    return False

        # Check if PL in payments
        for p in trade.Payments():
            payDate = p.PayDay()
            fromCurr = p.Currency()
            amount = p.Amount()
            if not self._sweepInPL(sweepInTrade, fromCurr,
                    toCurr, payDate, amount):
                self.abortTransaction()
                Summary().abortEntries()
                return False

        # Commit Payments to sweep in PL
        try:
            self.commitTransaction()
        except Exception:
            self.abortTransaction()
            Summary().abortEntries()
            traceback.print_exc()
            return False

        return True

    def _createAndCommitConversionTrades(self, sweep_date, fromCurr,
                toCurr, amount, portfolio=None):
        #create and commit sweep trades
        if fromCurr and fromCurr != toCurr:
            sweepFxTrades = self._createConversionTrades(sweep_date, fromCurr,
                    toCurr, amount, portfolio)
            if not sweepFxTrades:
                return False

            tradesAdded = []
            self.beginTransaction()
            for trd in sweepFxTrades:
                if trd.Quantity() != 0:
                    self.add_trade(trd)
                    tradesAdded.append(trd)

            try:
                self.commitTransaction()
            except Exception:
                self.abortTransaction()
                Summary().abortEntries()
                traceback.print_exc()
                return False

            for trd in tradesAdded:
                self.logCreatedMirrorTrade(trd)
        return True

    def _getConversionTradeInfo(self, trade):
        fromCurr = None
        if trade.Quantity() and trade.Instrument().IsKindOf(acm.FCurrency):
            fromCurr = trade.Instrument()
            amount = trade.Quantity()
        elif trade.Premium():
            fromCurr = trade.Currency()
            amount = trade.Premium()
        valueDay = trade.ValueDay()
        return fromCurr, amount, valueDay

    def _toPLCurrency(self, trade, toCurr):
        # for the case which premium or quantity contains PL
        if trade.Premium() or trade.Quantity():
            fromCurr, amount, sweep_date = self._getConversionTradeInfo(trade)
            result = self._createAndCommitConversionTrades(sweep_date,
                    fromCurr, toCurr, amount, trade.Portfolio())
            if not result:
                return result

        # for the case which payments contains PL
        for p in trade.Payments():
            fromCurr = p.Currency()
            sweep_date = p.PayDay()
            amount = p.Amount()
            result = self._createAndCommitConversionTrades(sweep_date,
                    fromCurr, toCurr, amount)
            if not result:
                return result
        return True

    def _positionInChain(self, method):
        for i in range(len(self.grouping)):
            if method == self.grouping[i]:
                return i
        return -1

    def _lowestGroupInstrument(self):
        for i in range(len(self.grouping) - 1, -1, -1):
            attrKey = self.grouping[i]
            if '.OptKey' in attrKey:
                attrKey = attrKey.split(".")[1]
            attr = self.attributes.get(attrKey, None)
            if attr is None:
                continue
            if acm.FCurrency[attr]:
                return acm.FCurrency[attr]
            if acm.FCurrencyPair[attr]:
                return acm.FCurrencyPair[attr]
            if acm.FInstrument[attr]:
                if '/' in attr:
                    insParts = attr.split("/")
                    if len(insParts) == 2:
                        curr1, curr2 = attr.split("/")
                        if all([curr1, curr2, acm.FCurrency[curr2],
                            acm.FCurrency[curr1]]):
                            return FFxCommon.currencyPair(acm.FCurrency[curr2],
                                    acm.FCurrency[curr1])
                    else:
                        return acm.FInstrument[attr].Currency()
                else:
                    return acm.FInstrument[attr].Currency()
        return None

    def _setSpotDate(self, tradingPort):
        insForSweepday = self._lowestGroupInstrument()
        if not insForSweepday:
            portCurrencyPair = tradingPort.CurrencyPair()
            if portCurrencyPair:
                insForSweepday = portCurrencyPair
            else:
                insForSweepday = tradingPort.Currency()

        self.spotDate = insForSweepday.SpotDate(self.nextTradingDate)
        valparams = acm.ObjectServer().UsedValuationParameters()
        reportDate = valparams.ReportDate()
        if reportDate == 'Today' or self.sweepPLToday:
            self.spotDate = self.nextTradingDate
        Logme()("Instrument for Sweep date {0} spot date for next "
                "trading date {2}: {1}".format(insForSweepday.Name(),
                self.spotDate, self.nextTradingDate), "DEBUG")

    def _getProjectedPayments(self, topNode, currObjects):
        # Build projected payments
        projPayments = []
        for currObj in currObjects:
            if not self.hasCashBalance(topNode, currObj):
                continue
            sweep_to = self.spotDate
            sweep_date = self.nextTradingDate
            while sweep_date <= sweep_to:
                cashflow = self.getCashflow(topNode, sweep_date, currObj)
                if cashflow:
                    payment = self._createPayment(sweep_date, cashflow,
                            currObj)
                    if math.fabs(payment.Amount()) > 0.000001:
                        projPayments.append(payment)
                    Summary().commitEntries()
                sweep_date = acm.Time.DateAddDelta(sweep_date, 0, 0, 1)
        return projPayments

    def _sweepCashBalances(self, topNode, plCurrencies, tradingPort):
        currObjs = _getSweepCurrencies(plCurrencies, tradingPort)
        projPayments = self._getProjectedPayments(topNode, currObjs)
        if not projPayments:
            return FFxCommon.RESULT_SUCCESS, None
        return self._sellCashflow(plCurrencies.instr, plCurrencies.pAndL,
                tradingPort, projPayments)

    def processPortfolio(self, tradingPort, nodes):
        FFxCommon.printEmp('Sweeping trading portfolio: "%s".' %
                (tradingPort and tradingPort.Name()), '*')

        resultOk = True
        try:
            for (topNode, self.attributes) in nodes:
                self.plExtractionTrades = []
                self.node = topNode
                if self.attributes:
                    FFxCommon.printEmp('Sweeping grouping position: %s' %
                            (self.attributes), '=')

                plCurrencies = self._getCurrenciesForNode(tradingPort, topNode)
                if not all(plCurrencies):
                    return False

                self._setSpotDate(tradingPort)

                plTrade = None
                if (not self.sweepPLToday and self.attributes and
                        'Currency Split' not in self.attributes):
                    Logme()("", "NOTIME_DEBUG")
                    Logme()("### Sweep Cashflows to PL portfolio ###", "DEBUG")

                    result, plTrade = self._sweepCashBalances(topNode,
                            plCurrencies, tradingPort)
                    if result == FFxCommon.RESULT_FAIL:
                        Summary().fail(tradingPort, Summary().SWEEP,
                                'All positions not swept', tradingPort.Name())
                        return False

                instrument, sweepCurrency, currency = plCurrencies
                if sweepCurrency == self.plCurr and self.retainPL:
                    continue

                today = acm.Time.DateToday()
                if self.nextTradingDate != today:
                    Logme()("### Spot Next Sweep, setting Valuation Date to "
                            "tomorrow ###", "DEBUG")
                    self.calcSpace.SimulateGlobalValue('Valuation Date',
                            self.nextTradingDate)

                if self.useMtMforCalc:
                    Logme()("### Using MtM prices for calculation ###",
                            "DEBUG")
                    self.calcSpace.SimulateGlobalValue(
                            'Portfolio Profit Loss Use MtM Today',
                            USE_MTM_PRICE_TODAY_ONLY)

                if not self.sweepPLToday:
                    #Sell Daily PL
                    Logme()("", "NOTIME_DEBUG")
                    Logme()("### Sweep daily PL to PL portfolio ###", "DEBUG")

                    sweep_date = self.nextTradingDate
                    while sweep_date < self.spotDate:
                        pl = self._getPL(topNode, PROJ_PL, sweep_date,
                                sweepCurrency.Name())
                        result, plTrade = self._sellPL(pl, instrument,
                                currency, sweep_date, tradingPort,
                                sweepCurrency, plTrade)
                        Summary().commitEntries()
                        if result == FFxCommon.RESULT_FAIL:
                            Summary().fail(tradingPort, Summary().SWEEP,
                                    'All positions not swept',
                                    tradingPort.Name())
                            return False

                        sweep_date = acm.Time.DateAddDelta(sweep_date, 0, 0, 1)

                #sell NPV
                Logme()("", "NOTIME_DEBUG")
                Logme()("### Sweep NetPL to PL Portfolio ###", "DEBUG")

                if sweepCurrency == self.plCurr and self.retainPL:
                    continue

                npv = self._getPL(topNode, self.spotForwardPLValue, None,
                        sweepCurrency.Name())
                if self.nextTradingDate != today:
                    self.calcSpace.RemoveGlobalSimulation('Valuation Date')
                result, plTrade = self._sellPL(npv, instrument, currency,
                        self.spotDate, tradingPort, sweepCurrency, plTrade)
                Summary().commitEntries()

                if result == FFxCommon.RESULT_FAIL:
                    Summary().fail(tradingPort, Summary().SWEEP,
                            'All positions not swept', tradingPort.Name())
                    return False
                if not self.sweepPLToday:
                    Logme()("### Convert PL to PL Currency ###", "DEBUG")
                    if self.plExtractionTrades:
                        for i in self.plExtractionTrades:
                            if self.convert:
                                result = self._toPLCurrency(i.MirrorTrade(),
                                    sweepCurrency)
                            else:
                                result = self._toPLCurrency(i.MirrorTrade(),
                                    self.plCurr)
                            if not result:
                                resultOk = False
                            Summary().commitEntries()
                    else:
                        Summary().warning(tradingPort, Summary().SWEEP,
                            'There is no P/L to be swept', tradingPort.Name())

                    if self.retainPL and self.plExtractionTrades:
                        for i in self.plExtractionTrades:
                            result = self._removeFXRisk(i.MirrorTrade(),
                                    self.plCurr)
                            if not result:
                                resultOk = False
                            Summary().commitEntries()
                else:
                    if self.retainPL and self.plExtractionTrades:
                        for t in self.plExtractionTrades:
                            result = self._sweepInNetPL(t)
                            if not result:
                                resultOk = False
                            Summary().commitEntries()

        except Exception:
            resultOk = False
            Logme()(FBDPCommon.get_exception(), 'ERROR')

        if resultOk:
            Summary().ok(tradingPort, Summary().SWEEP)
        else:
            Summary().fail(tradingPort, Summary().SWEEP,
                    'All positions not swept', tradingPort.Name())
        Summary().commitEntries()
        return False

    def _sweepInNetPL(self, trade):
        if trade.Premium() or trade.Quantity():
            sweepCurr, amount, sweep_date = self._getConversionTradeInfo(trade)
            sweepInPair = FFxCommon.currencyPair(self.plCurr, sweepCurr)
            sweepTrade = self._createSweepInNetPLTrade(
                                        sweepInPair.Currency1(),
                                        sweepInPair.Currency2(),
                                        trade.Portfolio(),
                                        trade.Acquirer(),
                                        trade.Counterparty(),
                                        sweep_date,
                                        0,
                                        (-1.0) * amount,
                                        sweepCurr,
                                        "PL Sweep")
            self.callAdjustTradeHook(sweepTrade, 'PL Sweep')
            self.beginTransaction()
            sweepTrade.MirrorPortfolio(trade.MirrorTrade().Portfolio())
            self.add_trade(sweepTrade)
            try:
                self.commitTransaction()
            except Exception:
                self.abortTransaction()
                Summary().abortEntries()
                traceback.print_exc()
                return False

            sweepTradeMirror = sweepTrade.MirrorTrade()
            self.container.Trades().Add(sweepTradeMirror)
            self.logCreatedMirrorTrade(sweepTrade)
            self.calcSpace.Refresh()
            self.printPL(sweepCurr)
            return True
        return True

    def _createSweepInNetPLTrade(self, instrument, currency, portfolio,
            acquirer, counterparty, date, price, pl, sweepCurrency,
            tradetype="Normal", trade_process=4096):

        trade = self._createZeroNominalTrade(instrument, currency, portfolio,
                acquirer, self.defaultAcquirer, date, price, tradetype,
                trade_process)

        if sweepCurrency == instrument:
            trade.Quantity(pl)
        elif currency == sweepCurrency:
            trade.Premium(pl)
        self.setTradePropertiesFromGrouperInPLPort(trade,
            ('Portfolio', 'PositionOrCurrencyPair',
            'PositionOrInstrumentPair'))
        return trade

    def _getPL(self, topNode, column, date, curr=None):
        nodeDate = topNode.Item().StringKey()
        if date == nodeDate or date == None:
            if curr:
                self.calcSpace.SimulateValue(topNode, "Portfolio Currency",
                        curr)
            val = self.getCalculation(topNode, column)
            return val

        if topNode.Iterator().HasChildren():
            child = topNode.Iterator().FirstChild()
            while child:
                val = self._getPL(child.Tree(), column, date, curr)
                if val:
                    return val
                child = child.NextSibling()
        return None

    def printPL(self, curr=None):
        cols = ["Portfolio Points Profit And Loss",
                "Portfolio Theoretical Total Profit and Loss"]
        self.printTree(self.node, cols, currencies=curr)

    def printCashBalance(self, curr=None):
        cols = ["Portfolio Projected Payments"]
        self.printTree(self.node, cols, currencies=curr)
