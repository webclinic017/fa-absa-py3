"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2019-03-22  CHG1001539200  Tibor Reiss        Update and refactor to enable PS aggregation
2019-04-12  CHG1001622197  Tibor Reiss        Fix bonds which have aggregated payment types (e.g.
                                              Aggregated Accrued): retain every payment type by
                                              using generalised function for determining if it
                                              is part of cash or not
2019-04-17  CHG1001639975  Tibor Reiss        Clear calc space when calculating time buckets for cash
2019-11-19  FAPE-101       Tibor Reiss        New payment type to improve PS aggregation
-----------------------------------------------------------------------------"""
from collections import defaultdict

import acm, ael
from FBDPCurrentContext import Logme
from FBDPCommon import ael_to_acm

from AGGREGATION_TRADE_FILTER import PV_TOLERANCE
from AGGREGATION_CASH_POSTING import CASH_POSTING
from AGGREGATION_PARAMETERS import PARAMETERS, ZAR_CALENDAR
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS
from AGGREGATION_SQL_HELPERS import TRADE_SQL_HELPERS


PAYMENT_TYPES_RETAINED_SEPARATELY = []
CALC_SPACE_IN_CASH = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), "FTradeSheet")
CALC_SPACE_YEARLY_TPL = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), "FPortfolioSheet")
FIRST_DAY_OF_YEAR = acm.Time.FirstDayOfYear(acm.Time.DateToday())


def isIncludedInCash(acmTrade):
    inCash = {}
    CALC_SPACE_IN_CASH.Clear()
    col = 'Portfolio Cash Vector'
    aelTrade = ael.Trade[acmTrade.Oid()].clone()
    for aelPayment in aelTrade.payments():
        paymentNumber = aelPayment.paynbr
        currName = aelPayment.curr.insid
        vector = acm.FArray()
        param = acm.FNamedParameters()
        param.AddParameter('currency', acm.FCurrency[currName])
        vector.Add(param)
        currVector = acm.Sheet.Column().ConfigurationFromVector(vector)
        aelTradeClone = aelTrade.clone()
        for aelPayment2 in aelTradeClone.payments():
            if aelPayment2.paynbr == aelPayment.paynbr:
                aelPayment2.amount = 0.0
                break
        calc_with = CALC_SPACE_IN_CASH.CreateCalculation(ael_to_acm(aelTrade), col, currVector).Value().Number()
        calc_without = CALC_SPACE_IN_CASH.CreateCalculation(ael_to_acm(aelTradeClone), col, currVector).Value().Number()
        if abs(calc_with - calc_without) > PV_TOLERANCE:
            inCash[paymentNumber] = True
        else:
            inCash[paymentNumber] = False
        Logme()("DEBUG: Included in cash: {} {} {} {} {}".format(aelPayment.type, inCash[paymentNumber],
                                                                calc_with, calc_without,
                                                                calc_with - calc_without), 'DEBUG')
    return inCash


class TradeAggregationError(Exception):
    pass


class TRADE_AGGREGATION():
    def __init__(self, reportDate, trades):
        self.__trades = trades
        self.__reportDate = reportDate
        self.__archivingSuccess = False
        self.__paymentsIncludedInCash = defaultdict(float)
        self.__payments = defaultdict(float)
        self.__cashBuckets = defaultdict(float)
        self.__initializeTimeBuckets(reportDate)
        self.__calculateSpecifiedPayments()
        self.__calculateCashBuckets()
        self.__psYearlyTPL = self.__preservePSYearlyTPL()
        self.__consolidateCashBuckets()
        self.__cashPostingTrade = None

    def getPayments(self):
        return self.__payments

    def __preservePSYearlyTPL(self):
        """
        This is specifically for Prime Services. But the function will be executed if preservePSYearlyTPL == True
        is defined.
        Explanation based on an example: a swap has two trades, both are terminated and available for aggregation. If
        the first trade was executed before beginning of current year, and the second trade was made in the current
        year, the val (Portfolio Value) will be non-zero on the first day of the current year - and this val is part
        of the yearly TPL (PS Yearly TPL). During aggregation though only cash is preserved, thus the yearly TPL would
        be broken.
        For this reason, the total yearly TPL is calculated for the group of trades. A payment of type
        PS_YearlyTPLAdjustment will be booked in the first time bucket of the present year, and another one with an
        opposite sign to the last time bucket of the previous year. This preserves the PS yearly TPL, and also the
        overall cash. Valuation will be broken between the time bucket end dates - but this is not a problem because
        the aggregation-candidate trades are old (this is also the reason why we don't have to worry about the
        PS monthly TPL).
        """
        if PARAMETERS.preservePSYearlyTPL:
            Logme()('DEBUG: Calculating PS Yearly TPL...', 'DEBUG')
            tempVirtualPf = acm.FAdhocPortfolio()
            for trade in self.__trades:
                tempVirtualPf.Add(trade)
            CALC_SPACE_YEARLY_TPL.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
            CALC_SPACE_YEARLY_TPL.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', FIRST_DAY_OF_YEAR)
            topNode = CALC_SPACE_YEARLY_TPL.InsertItem(tempVirtualPf)
            CALC_SPACE_YEARLY_TPL.Refresh()
            psYearlyTPL = CALC_SPACE_YEARLY_TPL.CreateCalculation(topNode, "PS Yearly TPL").Value().Number()
            psYearlyFunding = CALC_SPACE_YEARLY_TPL.CreateCalculation(topNode, "Yearly Funding").Value().Number()
            CALC_SPACE_YEARLY_TPL.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
            CALC_SPACE_YEARLY_TPL.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
            CALC_SPACE_YEARLY_TPL.Clear()
            Logme()('DEBUG: PS Yearly TPL = {}, PS Yearly Funding = {}.'.format(psYearlyTPL, psYearlyFunding), 'DEBUG')
            return psYearlyTPL - psYearlyFunding
        return None

    def aggregateTrades(self):
        Logme()('DEBUG: Creating Cash Posting Trade', 'DEBUG')
        self.__createCashPostingTrade()
        Logme()('DEBUG: Archive Trades', 'DEBUG')
        self.__setArchiveStatusAggregateTrdnbnrAggregate()
        if self.__archivingSuccess == True:
            Logme()('DEBUG: Updating Aggregate trades', 'DEBUG')
            self.__updateCashPostingTradeStatus()

    def __initializeTimeBuckets(self, reportDate):
        # Contains: end of previous year + end of all past months in this year + reportDate
        timeBuckets = []
        timeBuckets.append(reportDate)
        firstDayOfMonth = acm.Time.FirstDayOfMonth(reportDate)
        for _ in range(PARAMETERS.monthlyBuckets):
            lastDayOfPreviousMonth = ZAR_CALENDAR.AdjustBankingDays(firstDayOfMonth, -1)
            firstDayOfMonth = acm.Time.FirstDayOfMonth(lastDayOfPreviousMonth)
            if lastDayOfPreviousMonth not in timeBuckets:
                timeBuckets.append(lastDayOfPreviousMonth)
        firstDayOfYearForYearlyBuckets = FIRST_DAY_OF_YEAR
        for _ in range(PARAMETERS.yearlyBuckets):
            lastBusinessDayOfPreviousYear = ZAR_CALENDAR.AdjustBankingDays(firstDayOfYearForYearlyBuckets, -1)
            firstDayOfYearForYearlyBuckets = acm.Time.FirstDayOfYear(lastBusinessDayOfPreviousYear)
            if lastBusinessDayOfPreviousYear not in timeBuckets:
                timeBuckets.append(lastBusinessDayOfPreviousYear)
        self.__timeBuckets = sorted(timeBuckets)

    def __getTimeBucket(self, date):
        for tb in self.__timeBuckets:
            if date <= tb:
                return tb
        return None

    def __calculateSpecifiedPayments(self):
        """
        1) Payments not part of cash need to be retained.
        2) Payments part of cash but in the list PAYMENT_TYPES_RETAINED_SEPARATELY
           need to be deducted from the cash buckets and retained separately. If the
           list is empty, retain all payment types.
        """
        preserve_cpty = PARAMETERS.preservePaymentCpty
        for trade in self.__trades:
            inCash = isIncludedInCash(trade)
            for payment in trade.Payments():
                paymentType = payment.Type()
                paymentCurrency = payment.Currency().Name()
                paymentDay = payment.PayDay()
                bucket = self.__getTimeBucket(paymentDay)
                if not bucket:
                    error_msg = ("Payment {} for trade {} is after last time bucket "
                                 "(report date)!".format(payment.Oid(), trade.Oid()))
                    Logme()('ERROR: {}'.format(error_msg), 'ERROR')
                    raise TradeAggregationError(error_msg)
                party = payment.Party() if preserve_cpty else None
                if not inCash[payment.Oid()]:
                    self.__payments[(paymentType, paymentCurrency, bucket, party)] += payment.Amount()
                elif not PAYMENT_TYPES_RETAINED_SEPARATELY \
                     or paymentType in PAYMENT_TYPES_RETAINED_SEPARATELY:
                    self.__paymentsIncludedInCash[(paymentType, paymentCurrency, bucket)] += payment.Amount()
                    self.__payments[(paymentType, paymentCurrency, bucket, party)] += payment.Amount()

    def __calculateCashBuckets(self):
        PARAMETERS.calcSpaceClass.addTradesToVirtualPortfolio(self.__trades)
        self.__checkCashAfterReportDate()
        start_date = None
        for tb in self.__timeBuckets:
            PARAMETERS.calcSpace.Clear()
            PARAMETERS.calcSpaceClass.ApplyGlobalDateSimulations(start_date, tb)
            PARAMETERS.calcSpace.Refresh()
            cash = PARAMETERS.calcSpaceClass.calculateCashPerCurrency()
            for item in cash.Value():
                if item.Value().Number():
                    self.__cashBuckets[(str(item.Unit()), tb)] = item.Value().Number()
            start_date = tb

    def __checkCashAfterReportDate(self):
        PARAMETERS.calcSpaceClass.ApplyGlobalDateSimulations(start_date=self.__reportDate)
        cash = PARAMETERS.calcSpaceClass.calculateCashPerCurrency()
        for item in cash.Value():
            if abs(item.Value().Number()) >= PV_TOLERANCE:
                raise TradeAggregationError("Non-zero cash available after report date!")

    def __consolidateCashBuckets(self):
        cashCurrentYear = 0.0
        for (payType, payCurr, payDate), value in self.__paymentsIncludedInCash.iteritems():
            self.__cashBuckets[(payCurr, payDate)] -= value
            if payDate >= FIRST_DAY_OF_YEAR:
                cashCurrentYear += value
        for (payCurr, payDate), value in self.__cashBuckets.iteritems():
            if abs(value) >= PV_TOLERANCE:
                self.__payments[("Cash", payCurr, payDate, None)] += value
                if payDate >= FIRST_DAY_OF_YEAR:
                    cashCurrentYear += value
        if self.__psYearlyTPL is not None:
            # Funding is transferred to the CASH_PAYMENT instrument in a separate task, thus it must be deduced.
            Logme()('DEBUG: Current year cash in ZAR = {}'.format(cashCurrentYear), 'DEBUG')
            lastBusinessDayOfPreviousYear = ZAR_CALENDAR.AdjustBankingDays(FIRST_DAY_OF_YEAR, -1)
            firstBusinessDayOfCurrentYear = ZAR_CALENDAR.AdjustBankingDays(lastBusinessDayOfPreviousYear, +1)
            amount = self.__psYearlyTPL - cashCurrentYear
            self.__payments[("PS_YearlyTPLAdjustmentWithoutFunding", "ZAR",
                             self.__getTimeBucket(firstBusinessDayOfCurrentYear), None)] = amount
            self.__payments[("PS_YearlyTPLAdjustmentWithoutFunding", "ZAR",
                             self.__getTimeBucket(lastBusinessDayOfPreviousYear), None)] = -1.0 * amount

    def __createCashPostingTrade(self):
        """
        Create one trade with multiple payments. Payment types: cash, payment types excluded in FA from cash, payment
        types explicitly specified which need to be retained. Additionally, use time buckets, i.e. one payment per
        time bucket.
        """
        try:
            earliestPayDay = self.__reportDate
            for (_, _, payDay, _) in self.__payments:
                if payDay <= earliestPayDay:
                    earliestPayDay = payDay
            self.__cashPostingTrade = CASH_POSTING(PARAMETERS.cashPostingInstrument, PARAMETERS.counterparty,
                                                   PARAMETERS.acquirer, PARAMETERS.trader,
                                                   PARAMETERS.portfolio, "Simulated",
                                                   earliestPayDay, PARAMETERS.tradeCurrency)
            self.__cashPostingTrade.createTrade()
            for (payType, payCurr, payDay, party), payAmount in self.__payments.iteritems():
                if abs(payAmount) >= PV_TOLERANCE:
                    Logme()('DEBUG: Creating payment %s with value %s %s for date %s' %
                            (payType, payAmount, payCurr, payDay), 'DEBUG')
                    self.__cashPostingTrade.createPayment(payType, payAmount, payCurr, payDay, party)
            self.__cashPostingTrade.commit()
        except Exception as e:
            error_msg = "Could not create cash posting trade."
            Logme()('ERROR: {0} {1}'.format(error_msg, e), 'ERROR')
            raise TradeAggregationError(error_msg)
    
    def __setArchiveStatusAggregateTrdnbnrAggregate(self):
        helpers = GENERIC_HELPERS()
        trdNbrList = helpers.acmOidToLinstInts(self.__trades)
        sqlHelpers = TRADE_SQL_HELPERS()
        try:
            sqlHelpers.setArchiveStatusAggregateTrdnbnrAggregate(
                trdnbrs=trdNbrList,
                archiveFlag=1,
                aggTradeId=self.__cashPostingTrade.getCashPostingTrade().Oid(),
                aggregate=0,
                selectionAttribute='trdnbr')
            self.__archivingSuccess = True
        except Exception as e:
            self.__archivingSuccess = False
    
    def __updateCashPostingTradeStatus(self):
        updateTrdInfo = {}
        updateTrdInfo['Status'] = PARAMETERS.status
        self.__cashPostingTrade.updateTrade(updateTrdInfo)
