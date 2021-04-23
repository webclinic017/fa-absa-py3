""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FScripDivPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FScripDivPerform - Module which process the scrip dividend.

DESCRIPTION
----------------------------------------------------------------------------"""


import sys
import contextlib
import collections
import math
import acm
import FScripDivConst
import FBDPRollback

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


def str_to_class(nameStr):
    return getattr(sys.modules[__name__], nameStr)

def _tradeNumber(trade):
    try:
        trdnbr = trade.trdnbr
    except:
        trdnbr = trade.Oid()
    return trdnbr

def perform(execParam):
    scriptName = ''.join(execParam['ScriptName'].split())
    className = scriptName
    if scriptName == 'ScripDividend' and \
        ('CorporateAction' not in execParam or not
        execParam['CorporateAction']):
        className = scriptName + '_Legacy'
    dividendProcessor = str_to_class('_' + className)

    rollbackParam = execParam.get('Rollback', None)
    rollback = rollbackParam
    if not rollbackParam:
        rollback = FBDPRollback.RollbackWrapper(scriptName,
                    execParam['Testmode'], execParam)

    businessEvt = execParam.get('BusinessEvt', None)
    r = dividendProcessor(rollback, businessEvt)
    r.perform(execParam)
    if not rollbackParam:
        rollback.end()
    del r


_Position = collections.namedtuple('_Position',
        ['portfolio', 'name', 'tradeList'])


@contextlib.contextmanager
def _autoClearTradesWhenExit(acmObject):

    yield acmObject
    acmObject.Trades().Clear()


@contextlib.contextmanager
def _autoClearWhenExit(acmObject):

    yield acmObject
    acmObject.Clear()


def _importModifyScripIssueTradeHook():

    hook = None
    try:
        import FBDPHook
        hook = FBDPHook.modify_scrip_issue_trade
    except (ImportError, AttributeError):
        pass
    return hook


def _importModifyOffsetDividendCashPaymentHook():

    hook = None
    try:
        import FBDPHook
        hook = FBDPHook.modify_offset_dividend_cash_payment
    except (ImportError, AttributeError):
        pass
    return hook


def _importModifyDividendReinvestmentTradeHook():

    hook = None
    try:
        import FBDPHook
        hook = FBDPHook.modify_drip_issue_trade
    except (ImportError, AttributeError):
        pass
    return hook


def _importModifyOffsetDividendReinvestmentCashPaymentHook():

    hook = None
    try:
        import FBDPHook
        hook = FBDPHook.modify_offset_drip_dividend_cash_payment
    except (ImportError, AttributeError):
        pass
    return hook


def _getIsoTradeDate(acmTrade):

    return str(acmTrade.TradeTime())[:10]


def _makeScripIssueTradeTime(strIsoExDivDate):

    return ' '.join([strIsoExDivDate, FScripDivConst.SCRIP_ISSUE_TRADE_TIME])


def _findExDivDividend(acmIns, fromDate, strIsoDateToday):

    if not acmIns:
        return None
    dividendList = sorted([dvd for dvd in acmIns.Dividends()
            if dvd.ExDivDay() <= strIsoDateToday and \
               dvd.ExDivDay() >= fromDate],
            key=lambda dvd: dvd.ExDivDay())
    return dividendList

def _trdProcessedDividend(trade, dividend):

    trdLinks = trade.BusinessEventTradeLinks()
    if not trdLinks:
        return False

    for link in trdLinks:
        trdEvt = link.BusinessEvent()
        payLinks = trdEvt.PaymentLinks()
        if not payLinks:
            continue

        for pL in payLinks:
            pmt = pL.Payment()
            if pmt.Type() != 'Scrip Dividend':
                continue
            #TODO, use DividendLink, not text to link
            #the Scrip Dividend payment with the Dividend
            dividendPayDay = dividend.PayDay()
            pmtPayDay = pmt.PayDay()
            if dividendPayDay == pmtPayDay:
                return True

    return False

def _getProcessingTradeList(candidateTradeList, stockDividend):

    tradeList = []
    for t in candidateTradeList:
        if not _trdProcessedDividend(t, stockDividend):
            tradeList.append(t)
    return tradeList


def _findValidTradeQuantity(tradeList, strTradeBeforeDate, stockDividend):

    candidateTradeList = [trade for trade in tradeList if trade.Oid() > 0 and
            _getIsoTradeDate(trade) < strTradeBeforeDate and
            trade.Status() not in
                    FScripDivConst.TRADE_STATUS_NOT_CONTRIBUTING_QUANTITY]

    validTradeList = _getProcessingTradeList(candidateTradeList, stockDividend)
    return sum(trade.Quantity() for trade in validTradeList), validTradeList


def _setTradeDates(acmIns, trd, pldividendCompareMethod,
        strIsoExDivDate, strIsoRecordDate):

    if (pldividendCompareMethod == 'Trade day vs ex div day' or \
    pldividendCompareMethod == 'Acquire day vs calc record day'):
        tradeTime = _makeScripIssueTradeTime(strIsoExDivDate)
        trd.TradeTime(tradeTime)
        insSpotDate = acmIns.SpotDate(strIsoExDivDate)
        trd.AcquireDay(insSpotDate)
        trd.ValueDay(insSpotDate)
    elif pldividendCompareMethod == 'Acquire day vs record day':
        acquireDate = acm.Time().DateAdjustPeriod(strIsoRecordDate, '1d')
        offsetStr = '-%dd' % (acmIns.SpotBankingDaysOffset())
        tradeDate = acm.Time().DateAdjustPeriod(acquireDate, offsetStr)
        tradeTime = _makeScripIssueTradeTime(tradeDate)

        trd.TradeTime(tradeTime)
        trd.AcquireDay(acquireDate)
        trd.ValueDay(acquireDate)

    return

def _createScripIssueTrade(acmIns, plDividendComparaMethod,
        acmPhysPort, scripIssueQty,
        strIsoExDivDate, strIsoRecordDate, preview):

    trd = acm.FTrade()
    trd.Instrument(acmIns)
    trd.Portfolio(acmPhysPort)
    trd.Quantity(scripIssueQty)
    trd.Currency(acmIns.Currency())
    _setTradeDates(acmIns, trd, plDividendComparaMethod,
        strIsoExDivDate, strIsoRecordDate)
    trd.Acquirer(acm.FParty['FMAINTENANCE'])
    trd.Counterparty(acm.FParty['FMAINTENANCE'])
    trd.Type('Corporate Action')
    status = 'Simulated' if preview else 'FO Confirmed'
    trd.Status(status)
    return trd

def _createOffsetDividendCashPayment(scripIssueTrade, offsetDividendCash,
        dividendCurr, strIsoExDivDate, strIsoPayDate, paymentType):

    pmt = acm.FPayment()
    pmt.Trade(scripIssueTrade)
    pmt.Type(paymentType)
    pmt.Amount(-offsetDividendCash)
    pmt.Currency(dividendCurr)
    pmt.ValidFrom(strIsoExDivDate)
    pmt.PayDay(strIsoPayDate)
    pmt.Party(scripIssueTrade.Counterparty())
    return pmt


def _getTradesInPhysicalPortfolioForInstrument(acmPhysPort, acmIns):

    return [acmTrade for acmTrade in acmPhysPort.TradesIn(acmIns)]


def _getTradesInTradeFilterForInstrument(acmTradeSelection, acmIns):

    return [acmTrade for acmTrade in acmTradeSelection.TradesIn(acmIns)]


def _getUniqueTrades(trades):

    oidToTradeMap = {}
    for trade in trades:
        oidToTradeMap[trade.Oid()] = trade
    return list(oidToTradeMap.values())


def _getBuiltInTradePortfolioGrouper():

    allBuiltInPortfolioGroupers = acm.Risk.GetAllBuiltInPortfolioGroupers()
    tradePortfolioGrouper = allBuiltInPortfolioGroupers.At('Trade Portfolio')
    return tradePortfolioGrouper

def _getPLDividendCompareMethod():
    context = acm.GetDefaultContext()
    extensionName = 'pLDividendComparisonMethod'
    ext = context.GetExtension('FExtensionAttribute',
       'FObject', extensionName)
    attribute = acm.GetCalculatedValue(ext, '', extensionName)
    return attribute.Value()

def _validateMode():
    error = 0
    if acm.ArchivedMode():
        errMsg = 'This script must not be run in the Archived mode.'
        error = 1
        Logme()(errMsg, 'ERROR')
    if acm.IsHistoricalMode():
        errMsg = 'This script must not be run in the Historical mode.'
        error = 1
        Logme()(errMsg, 'ERROR')
    return error

def _logInstrumentDescription(acmIns, acmStockIns):

    if not acmIns:
        return
    Logme()('    Found the specified instrument "{0}" [{1}]'.format(
            acmIns.Name(), acmIns.InsType()), 'INFO')
    Logme()('    The dividend instrument is "{0}" [{1}]'.format(
            acmStockIns.Name(), acmStockIns.InsType()), 'INFO')

def _logStockDividendDescription(acmDividend):

    if not acmDividend:
        return
    Logme()('    The dividend:', 'INFO')
    Logme()('        Amount: {0} {1}'.format(
            acmDividend.Currency().Name(), acmDividend.Amount()), 'INFO')
    Logme()('        Ex-div day: {0}'.format(
            acmDividend.ExDivDay()), 'INFO')
    Logme()('        Record day: {0}'.format(
            acmDividend.RecordDay()), 'INFO')
    Logme()('        Pay day: {0}'.format(acmDividend.PayDay()), 'INFO')


class _DividendProcessingBase(object):
    _RunParam = collections.namedtuple('_RunParam', ['ins',
            'dividendList',
            'positionNumber', 'positionName',
            'positionPortfolio', 'positionTradeList'])

    _InspectionReport = collections.namedtuple(
            '_InspectionReport', ['ins', 'port',
            'positionNumber', 'positionName', 'tradelist',
            'trdQuantity', 'dividend'])

    def AbstractionLogName(self):
        raise NotImplementedError('call to abstract method AbstractionLogName')

    @staticmethod
    def _recordProcessPositionSuccessfully(reinvestmentName,
            inspectionReport, scripIssueTrade, offsetPayment):

        Summary().ok('Position', 'PROCESS', inspectionReport.positionNumber)
        Summary().ok(scripIssueTrade.RecordType(), 'CREATE',
                    scripIssueTrade.Oid())

        Logme()('    {0} issue trade quantity: {1}'.format(
                reinvestmentName, scripIssueTrade.Quantity()), 'INFO')
        Summary().ok(offsetPayment.RecordType(), 'CREATE', offsetPayment.Oid())
        Logme()('    Offset cash dividend payment amount: {0} '
                '{1}'.format(offsetPayment.Currency().Name(),
                offsetPayment.Amount()), 'INFO')

    def __init__(self, rollback, businessEvt=None):

        self._rollbackWrapper = rollback
        self._plDividendCompareMethod = _getPLDividendCompareMethod()
        self._testMode = 0
        self._businessEvent = businessEvt
        self._processedList = []
        self._shortDividendFactor = 1.0
        self._roundingFunc = None
        self._preview = 0
        self._fromDate = 0
        self._issuePerShare = 0
        self._corporateAction = None
        self._modifyIssueTradeHook = None
        self._modifyOffsetDividendCashPaymentHook = None

    def _acquireRunParameterInstrument(self, execParam):

        ins = None
        stockIns = None
        if self._corporateAction:
            caIns = self._corporateAction.Instrument()
            ins, stockIns = self._acquireRunParameterInstrumentValidateInsType(
                caIns)
        return ins, stockIns

    def _acquireRunParameterStockDividend(self, stockIns, fromDate):
        return [self._corporateAction.Dividend()]

    def _acquireRunParameterTrades(self, execParam, acmIns):

        trades = []
        if not acmIns:
            return trades
        allTrades = True
        portfolio = self._corporateAction.Portfolio()
        if portfolio:
            physPortList = [portfolio]
            allTrades = False
            for physPort in physPortList:
                trades.extend(_getTradesInPhysicalPortfolioForInstrument(
                        physPort, acmIns))
        else:
            tradeSelection = self._corporateAction.TradeFilter()
            if tradeSelection:
                tradeFilterList = [tradeSelection]
                allTrades = False
                for tradeFilter in tradeFilterList:
                    trades.extend(_getTradesInTradeFilterForInstrument(
                            tradeFilter, acmIns))
        if allTrades:
            trades = [t for t in acmIns.Trades()]

        return trades

    def acquireRunParameterList(self, execParam):
        error = 0
        try:
            self._testMode = execParam['Testmode']
            self._preview = execParam.get('Preview', 0)
            self._issuePerShare = \
                self._acquireRunParameterIssuePerShare(
                    execParam)
            corporateActions = execParam.get('CorporateAction', None)
            if corporateActions:
                self._corporateAction = corporateActions[0]
            ins, stockIns = self._acquireRunParameterInstrument(execParam)
            _logInstrumentDescription(ins, stockIns)
            self._shortDividendFactor = ins.ShortDividendFactor()
            self._roundingFunc = \
                self._acquireRunParameterRoundingFunc(execParam)
            tradeList = self._acquireRunParameterTrades(execParam, ins)
            positionList = _PositionSplitter(
                    tradeList).splitByCalcSpaceGrouper()
            Logme()('    Found {0} trades in {1} positions.'.format(
                    len(tradeList), len(positionList)), 'INFO')
            runParamList = []
            for positionSequence, position in enumerate(positionList):

                stockDividendList = self._acquireRunParameterStockDividend(
                    stockIns, self._fromDate)
                if not stockDividendList:
                    continue

                runParam = self._RunParam(ins=ins,
                        dividendList=stockDividendList,
                        positionNumber=(positionSequence + 1),
                        positionName=position.name,
                        positionPortfolio=position.portfolio,
                        positionTradeList=position.tradeList
                        )
                runParamList.append(runParam)
            return error, runParamList
        except Exception as e:
            failMsg = ('Unable to generate run parameter {0}'.format(str(e)))
            Logme()(failMsg, 'ERROR')
            error = 1
            return error, []

    def _inspect(self, runParamList):

        inspectionReportList = []
        for runParam in runParamList:
            inspectionReports = self._inspectPosition(runParam)
            if inspectionReports:
                inspectionReportList.extend(inspectionReports)
        return inspectionReportList

    def _inspectPosition(self, runParam):

        Logme()('Inspecting position {0} "{1}"...'.format(
                runParam.positionNumber, runParam.positionName), 'INFO')
        if not runParam.positionTradeList:
            ignMsg = ('There is no trade in position {0} "{1}".  Position '
                    'ignored.'.format(runParam.positionNumber,
                    runParam.positionName))
            Logme()(ignMsg, 'WARNING')
            Summary().ignore('Position', 'INSPECT', [ignMsg],
                        runParam.positionNumber)
            return None

        Summary().ok('Position', 'INSPECT', runParam.positionNumber)
        inspectionReportList = []
        ins = runParam.ins
        insName = ins.Name()
        for stockDividend in runParam.dividendList:
            exDivDate = stockDividend.ExDivDay()
            trdQty, validTradeList = _findValidTradeQuantity(
                runParam.positionTradeList,
                exDivDate, stockDividend)
            if not trdQty:
                ignMsg = ('The valid trade quantity of position {0} '
                        '"{1}" before '
                        'ex-div date is 0.  Position ignored.'.format(
                        runParam.positionNumber, runParam.positionName))
                Logme()(ignMsg, 'WARNING')
                Summary().ignore('Position', 'INSPECT', [ignMsg],
                    runParam.positionNumber)
                continue

            Logme()('    The trade quantity of instrument "{0}" in the '
                'position before ex-div date is {1}'.format(
                insName, int(trdQty)), 'INFO')

            inspectionReport = self._InspectionReport(ins=runParam.ins,
                port=runParam.positionPortfolio,
                positionNumber=runParam.positionNumber,
                positionName=runParam.positionName,
                tradelist=validTradeList,
                trdQuantity=trdQty,
                dividend=stockDividend)
            inspectionReportList.append(inspectionReport)
        return inspectionReportList

    def _isInTestMode(self):
        return self._testMode

    def _addTradeLink(self, trade):
        trdnbr = _tradeNumber(trade)
        tradeLink = acm.FBusinessEventTradeLink()
        tradeLink.Trade(trdnbr)
        tradeLink.BusinessEvent(self._businessEvent)
        self._rollbackWrapper.add(tradeLink)
        Summary().ok(tradeLink, Summary().CREATE, tradeLink.Oid())

    def _addPaymentLink(self, pmt):
        pmtnbr = pmt.Oid()
        pmtLink = acm.FBusinessEventPaymentLink()
        pmtLink.Payment(pmtnbr)
        pmtLink.BusinessEvent(self._businessEvent)
        self._rollbackWrapper.add(pmtLink)
        Summary().ok(pmtLink, Summary().CREATE, pmtLink.Oid())

    def _processPosition(self, inspectionReport):

        if not inspectionReport:
            return

        stockDiv = inspectionReport.dividend
        if not stockDiv:
            return

        ins = inspectionReport.ins
        if not ins:
            return

        if not self._businessEvent:
            self._businessEvent = acm.FBusinessEvent()
            self._rollbackWrapper.add(self._businessEvent)
            Summary().ok(self._businessEvent, Summary().CREATE,
                self._businessEvent.Oid())

        for t in inspectionReport.tradelist:
            if t not in self._processedList:
                self._processedList.append(t)
                self._addTradeLink(t)

        Logme()('Processing position {0} "{1}"'.format(
                inspectionReport.positionNumber,
                inspectionReport.positionName), 'INFO')

        exDivDate = stockDiv.ExDivDay()
        recordDate = stockDiv.RecordDay()
        payDate = stockDiv.PayDay()
        dividendCurr = stockDiv.Currency()

        trdQty = inspectionReport.trdQuantity
        offsetDividendCash = self._calculateDividendCash(ins, stockDiv, trdQty)

        Logme()('    The total cash dividend to offset is {0} '
                '{1}'.format(dividendCurr.Name(), offsetDividendCash),
                'INFO')
        rawScripIssueQty = trdQty * self._issuePerShare
        Logme()('    {0} issue quantity is {1} (raw)'.format(
                self.AbstractionLogName(), rawScripIssueQty), 'INFO')
        scripIssueQty = int(self._roundingFunc(rawScripIssueQty))
        Logme()('    {0} issue quantity is {1} (rounded)'.format(
                self.AbstractionLogName(), scripIssueQty), 'INFO')

        scripIssueTrade = _createScripIssueTrade(inspectionReport.ins,
                self._plDividendCompareMethod,
                inspectionReport.port, scripIssueQty,
                exDivDate, recordDate, self._preview)
        self._rollbackWrapper.add_trade(scripIssueTrade)
        offsetPayment = self._createOffsetDividendCashPayment(scripIssueTrade,
                offsetDividendCash,
                dividendCurr,
                strIsoExDivDate=exDivDate,
                strIsoPayDate=payDate)
        self._modifyOffsetIssueTradeAndOffsetDividendCashPayment(
                scripIssueTrade, offsetPayment)
        if self._isInTestMode():
            self._recordProcessPositionSuccessfully(self.AbstractionLogName(),
                    inspectionReport,
                    scripIssueTrade, offsetPayment)
        else:
            try:
                acm.BeginTransaction()
                scripIssueTrade.Commit()
                offsetPayment.Commit()
                acm.CommitTransaction()

                self._addPaymentLink(offsetPayment)
                self._addTradeLink(scripIssueTrade)
                self._recordProcessPositionSuccessfully(
                        self.AbstractionLogName(),
                        inspectionReport,
                        scripIssueTrade, offsetPayment)
            except Exception as e:
                acm.AbortTransaction()
                failMsg = ('Unable to create scrip issue trade and the '
                        'dividend offset cash payment.  {0}'.format(str(e)))
                Logme()(failMsg, 'ERROR')
                Summary().fail(inspectionReport.port.RecordType(),
                        'PROCESS', [failMsg], inspectionReport.port.Oid())

    def _process(self, inspectionReportList):
        for inspectionReport in inspectionReportList:
            self._processPosition(inspectionReport)

    def perform(self, execParam):

        # VALIDATE phase
        Logme()('Validating environment and parameters...', 'INFO')
        error = _validateMode()
        if error:
            Logme()(Summary().buildErrorsAndWarningsStr(), 'NOTIME')
            return
        # ACQUIRING PARAMETER phase
        Logme()('Acquiring run parameters...', 'INFO')
        error, runParamList = self.acquireRunParameterList(execParam)
        if error:
            Logme()(Summary().buildErrorsAndWarningsStr(), 'NOTIME')
            return
        # INSPECTION phase
        Logme()('Inspecting {0} positions...'.format(
                len(runParamList)), 'INFO')
        inspectionReportList = self._inspect(runParamList)

        # PROCESS phase
        Logme()('Processing {0} positions...'.format(len(
                inspectionReportList)), 'INFO')
        self._process(inspectionReportList)
        # Finalise
        Logme()('Done.', 'INFO')
        Logme()(Summary().buildErrorsAndWarningsStr(), 'NOTIME')
        return

    def _calculateDividendCash(self, ins, stockDiv, trdQty):
        raise NotImplementedError("Not implemented")

    def _createOffsetDividendCashPayment(self, scripIssueTrade,
            offsetDividendCash, dividendCurr, strIsoExDivDate,
            strIsoPayDate):
        raise NotImplementedError("Not implemented")

    def _acquireRunParameterRoundingFunc(self, execParam):
        raise NotImplementedError("Not implemented")

    def _acquireRunParameterIssuePerShare(self, execParam):
        raise NotImplementedError("Not implemented")

    def _acquireRunParameterInstrumentValidateInsType(self, ins):
        raise NotImplementedError("Not implemented")

    def _modifyOffsetIssueTradeAndOffsetDividendCashPayment(self,
            scripIssueTrade, offsetDividendCashPayment):

        if self._modifyIssueTradeHook:
            scripIssueTrade = self._modifyIssueTradeHook(scripIssueTrade)
        if self._modifyOffsetDividendCashPaymentHook:
            offsetDividendCashPayment = (
                    self._modifyOffsetDividendCashPaymentHook(
                    offsetDividendCashPayment))

class _DividendReinvestment(_DividendProcessingBase):

    def __init__(self, rollback, businessEvt=None):
        super(_DividendReinvestment, self).__init__(rollback, businessEvt)
        self._modifyIssueTradeHook = (
                _importModifyDividendReinvestmentTradeHook())
        self._modifyOffsetDividendCashPaymentHook = (
                _importModifyOffsetDividendReinvestmentCashPaymentHook())

    def AbstractionLogName(self):
        return 'Reinvestment'

    def _acquireRunParameterInstrumentValidateInsType(self, ins):

        errorReturnVal = None, None
        if ins.InsType() in FScripDivConst.UNDERLYING_INS_TYPES_ALLOWED:
            stockIns = ins
        elif ins.InsType() in FScripDivConst.DERIVATIVE_INS_TYPES_ALLOWED:
            stockIns = ins.Underlying()
            if not stockIns:
                Logme()('The instrument "{0}" of instrument type "{1}" '
                        'does not have an underlying instrument.  This is '
                        'not allowed.'.format(ins.Name(), ins.InsType()),
                        'ERROR')
                return errorReturnVal
            if (stockIns.InsType() not in
                    FScripDivConst.UNDERLYING_INS_TYPES_ALLOWED):
                Logme()('The instrument "{0}" of instrument type "{1}" '
                        'has an underlying instrument "{2}" of instrument '
                        'type "{3}", which is not an allowed underlying '
                        'instrument type.'.format(ins.Name(), ins.InsType(),
                        stockIns.Name(), stockIns.InsType()), 'ERROR')
                return errorReturnVal
        else:
            Logme()('The instrument "{0}" of instrument type "{1}" is '
                    'not in one of the allowed instrument types "{2}".'.format(
                    ins.Name(), ins.InsType(),
                    FScripDivConst.INS_TYPES_ALLOWED), 'ERROR')
            return errorReturnVal
        return ins, stockIns

    def _acquireRunParameterIssuePerShare(self, execParam):

        try:
            DripIssuePerShare = float(execParam['DripIssuePerShare'])
        except ValueError:
            Logme()('Invalid Scrip issue per share ratio.  Expecting a '
                    'float number, but got {0}'.format(
                    execParam['DripIssuePerShare']), 'ERROR')
            return 0

        if DripIssuePerShare <= 0.0:
            Logme()('Bad scrip issue per share ratio.  Expecting a '
                    'postive number, but got {0}'.format(DripIssuePerShare),
                    'ERROR')
        return DripIssuePerShare

    def _acquireRunParameterRoundingFunc(self, execParam):

        tradeQuantityRounding = execParam['TradeQuantityRounding']
        if tradeQuantityRounding == FScripDivConst.ROUNDING_UP_OR_DOWN:
            roundingFunc = round
        elif tradeQuantityRounding == FScripDivConst.ROUNDING_DOWN_ONLY:
            roundingFunc = math.floor
        else:
            roundingFunc = None
            Logme()('Unrecognised rounding convention "{0}".'.format(
                    tradeQuantityRounding), 'ERROR')
        return roundingFunc

    def _calculateDividendCash(self, ins, stockDiv, trdQty):

        dividendAmountPerShare = stockDiv.Amount()
        dividendFactor = ins.DividendFactor()
        taxFactor = 1
        shortDivFactor = 1.0
        if trdQty < 0:
            shortDivFactor = self._shortDividendFactor

        offsetDividendCash = trdQty * \
            dividendAmountPerShare * taxFactor * \
            dividendFactor * shortDivFactor

        return offsetDividendCash

    def _createOffsetDividendCashPayment(self, scripIssueTrade,
            offsetDividendCash, dividendCurr, strIsoExDivDate,
            strIsoPayDate):
        return _createOffsetDividendCashPayment(scripIssueTrade,
            offsetDividendCash, dividendCurr, strIsoExDivDate,
            strIsoPayDate, 'Dividend Reinvestment')


class _ScripDividend(_DividendProcessingBase):

    def __init__(self, rollback, businessEvt=None):
        super(_ScripDividend, self).__init__(rollback, businessEvt)
        self._modifyIssueTradeHook = _importModifyScripIssueTradeHook()
        self._modifyOffsetDividendCashPaymentHook = (
                _importModifyOffsetDividendCashPaymentHook())

    def AbstractionLogName(self):
        return 'Scrip'

    def _acquireRunParameterInstrumentValidateInsType(self, ins):

        errorReturnVal = None, None
        if ins.InsType() in FScripDivConst.UNDERLYING_INS_TYPES_ALLOWED:
            stockIns = ins
        elif ins.InsType() in FScripDivConst.DERIVATIVE_INS_TYPES_ALLOWED:
            stockIns = ins.Underlying()
            if not stockIns:
                Logme()('The instrument "{0}" of instrument type "{1}" '
                        'does not have an underlying instrument.  This is '
                        'not allowed.'.format(ins.Name(), ins.InsType()),
                        'ERROR')
                return errorReturnVal
            if (stockIns.InsType() not in
                    FScripDivConst.UNDERLYING_INS_TYPES_ALLOWED):
                Logme()('The instrument "{0}" of instrument type "{1}" '
                        'has an underlying instrument "{2}" of instrument '
                        'type "{3}", which is not an allowed underlying '
                        'instrument type.'.format(ins.Name(), ins.InsType(),
                        stockIns.Name(), stockIns.InsType()), 'ERROR')
                return errorReturnVal
        else:
            Logme()('The instrument "{0}" of instrument type "{1}" is '
                    'not in one of the allowed instrument types "{2}".'.format(
                    ins.Name(), ins.InsType(),
                    FScripDivConst.INS_TYPES_ALLOWED), 'ERROR')
            return errorReturnVal
        return ins, stockIns

    def _acquireRunParameterIssuePerShare(self, execParam):

        try:
            scripIssuePerShare = float(execParam['ScripIssuePerShare'])
        except ValueError:
            Logme()('Invalid Scrip issue per share ratio.  Expecting a '
                    'float number, but got {0}'.format(
                    execParam['ScripIssuePerShare']), 'ERROR')
            return 0

        if scripIssuePerShare <= 0.0:
            Logme()('Bad scrip issue per share ratio.  Expecting a '
                    'postive number, but got {0}'.format(scripIssuePerShare),
                    'ERROR')
        return scripIssuePerShare

    def _acquireRunParameterRoundingFunc(self, execParam):

        tradeQuantityRounding = execParam['TradeQuantityRounding']
        if tradeQuantityRounding == FScripDivConst.ROUNDING_UP_OR_DOWN:
            roundingFunc = round
        elif tradeQuantityRounding == FScripDivConst.ROUNDING_DOWN_ONLY:
            roundingFunc = math.floor
        else:
            roundingFunc = None
            Logme()('Unrecognised rounding convention "{0}".'.format(
                    tradeQuantityRounding), 'ERROR')
        return roundingFunc

    def _calculateDividendCash(self, ins, stockDiv, trdQty):

        dividendAmountPerShare = stockDiv.Amount()
        dividendFactor = ins.DividendFactor()
        taxFactor = stockDiv.TaxFactor()
        shortDivFactor = 1.0
        if trdQty < 0:
            shortDivFactor = self._shortDividendFactor

        offsetDividendCash = trdQty * \
            dividendAmountPerShare * taxFactor * \
            dividendFactor * shortDivFactor

        return offsetDividendCash

    def _createOffsetDividendCashPayment(self, scripIssueTrade,
            offsetDividendCash, dividendCurr, strIsoExDivDate,
            strIsoPayDate):
        return _createOffsetDividendCashPayment(scripIssueTrade,
            offsetDividendCash, dividendCurr, strIsoExDivDate,
            strIsoPayDate, 'Scrip Dividend')


class _ScripDividend_Legacy(_ScripDividend):

    def __init__(self, rollback, businessEvt=None):

        super(_ScripDividend_Legacy, self).__init__(rollback, businessEvt)

    def acquireRunParameterList(self, execParam):

        self._fromDate = execParam.get('FromDate', 0)
        return super(_ScripDividend_Legacy, self
                ).acquireRunParameterList(execParam)

    def _acquireRunParameterInstrument(self, execParam):

        insList = execParam['Instrument']
        if len(insList) != 1:
            Logme()('Exactly one instrument should be specified; '
                    'however, we have {0} instrument(s) here.'.format(
                    len(insList)), 'ERROR')
            return None, None
        ins, stockIns = self._acquireRunParameterInstrumentValidateInsType(
                insList[0])
        return ins, stockIns

    def _acquireRunParameterStockDividend(self, stockIns, fromDate):

        if not stockIns:
            return None

        strIsoDateToday = acm.Time.DateToday()
        stockDividends = _findExDivDividend(stockIns, fromDate,
                                            strIsoDateToday)
        if not stockDividends:
            Logme()('No valid dividend found on the instrument '
                    '"{0}".'.format(stockIns.Name()), 'ERROR')

        return stockDividends

    def _acquireRunParameterTrades(self, execParam, acmIns):

        trades = []
        if not acmIns:
            return trades
        tradeFilterList = execParam.get('TradeFilters', ())
        physPortList = execParam.get('Portfolios', ())
        for physPort in physPortList:
            trades.extend(_getTradesInPhysicalPortfolioForInstrument(physPort,
                    acmIns))
        for tradeFilter in tradeFilterList:
            trades.extend(_getTradesInTradeFilterForInstrument(tradeFilter,
                    acmIns))
        return _getUniqueTrades(trades)


class _PositionSplitter(object):

    def __init__(self, tradeList):

        self.__tradeList = tradeList

    def _calcSpaceObtainPositionListFromChildren(self, node):

        child = node.Iterator().FirstChild()
        positionList = []
        while child:
            childNode = child.Tree()
            item = childNode.Item()
            positionName = item.StringKey()
            positionTradeList = [trade for trade in item.Trades()]
            if positionTradeList:
                portfolio = positionTradeList[0].Portfolio()
            else:
                portfolio = None
            positionList.append(_Position(portfolio=portfolio,
                    name=positionName, tradeList=positionTradeList))
            child = child.NextSibling()
        return positionList

    def _calcSpaceSplitTrades(self, tradeList, portfolioGrouper):

        if not tradeList:
            return []
        with _autoClearTradesWhenExit(acm.FAdhocPortfolio()) as tradeUnion:
            tradeUnion.Name('Trade Union')
            for trade in tradeList:
                tradeUnion.Add(trade)
            with _autoClearWhenExit(
                    acm.FCalculationSpace('FPortfolioSheet')) as calcSpace:
                topNode = calcSpace.InsertItem(tradeUnion)
                topNode.ApplyGrouper(portfolioGrouper)
                calcSpace.Refresh()
                positionList = self._calcSpaceObtainPositionListFromChildren(
                        topNode)
        return positionList

    def splitByCalcSpaceGrouper(self):

        portfolioGrouper = _getBuiltInTradePortfolioGrouper()
        positionList = self._calcSpaceSplitTrades(self.__tradeList,
               portfolioGrouper)
        return positionList

    def splitByPhysicalPortfolio(self):

        d = collections.defaultdict(list)
        for trade in self.__tradeList:
            d[trade.Portfolio().Name()].append(trade)
        positionList = []
        for portName, tradeList in d.items():
            positionList.append(
                    _Position(portfolio=acm.FPhysicalPortfolio[portName],
                    name=portName, tradeList=tradeList))
        return positionList
