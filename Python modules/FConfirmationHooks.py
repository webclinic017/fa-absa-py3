"""---------------------------------------------------------------------------------------------------------------------
MODULE                  :       FConfirmationHooks
PURPOSE                 :       In this hook override functions and custom confirmation event functions
                                can be defined. It is activated when a trade meets any of the defined methods.

                                These methods are linked to the event hooks defined in FConfirmationParameters called
                                confirmationEvents.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2014-05-19      #########       Sanele Macanda          Adaptiv Requirements    Created CONF_NEW_TRADE_EVEN
                                                                                CONF_NEW_TRADE_EVENT_CALL
                                                                                CONF_ISPLEDGE_FROZEN
                                                                                CONF_ISNOVATED
                                                                                CONF_MATURITY_NOTICE
                                                                                CONF_NOTICE_TO_DISREGARD
                                                                                CONF_PROLONG_DEPOSIT
2016-03-18                      Willie van der Bank                             Amended CONF_MATURITY_NOTICE to only
                                                                                generate expirations
                                                                                1 day in advance
2016-07-20      CHNG0003821295  Willie van der Bank                             Updated IsAdjustDepositEvent to take
                                                                                cash flow pay date
                                                                                into consideration as well
2016-11-03      CHNG0004066766  Willie van der Bank                             Changed maxBankingDaysBack to 15
2017-03-14      CHNG0004391406  Willie van der Bank                             Updated CONF_PROLONG_DEPOSIT to include
                                                                                a counterparty check
2017-12-07      CHNG0005210529  Willie van der Bank                             Changed maxBankingDaysBack to 30
2017-12-11      CHNG0005220511  Manan Ghosh                                     Block "New Trade" confirmations for DIS
                                                                                trades
2018-08-28                      Stuart Wilson           Capital Markets         Block new trade event for broker note
                                                                                trades
2019-04-30      FAOPS-461       Cuen Edwards            Letitia Carboni         Block Rate Fixing Call event for non-
                                                                                call accounts.
2019-05-17      FAOPS-453       Hugo Decloedt           Wandile Sithole         Updated check for maturity notice.
2020-02-10      FAOPS-725       Cuen Edwards            Kgomotso Gumbo          Minor refactoring.
2020-09-23      FAOPS-933       Ntokozo Skosana         Kgommotso Gumbo         Allowing the generation of 'New trade'
                                                                                confirmations for trades of instrument
                                                                                type 'Deposit' & 'Option'
------------------------------------------------------------------------------------------------------------------------
"""

import acm
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as helper
from Adaptiv_XML_Functions import is_valid_status
from at_time import to_date
from FConfirmationDefaultEventHooks import IsWeightedReset, IsDeterminedCashFlow, GetLatestResetInCashFlowPeriod, IsZeroPosition, IsOriginalCashFlow, IsAdjustedOriginalCashFlow
from BrokerNoteGeneral import is_broker_note_trade
from ASUSNewTradeConfirmationEventHooks import ASUS_NEW_TRADE_EVENT


"""
ABITFA-4473
The maximum allowed days for back-dating is maxBankingDaysBack - FConfirmationHooksTemplate.GetExpiryDayCount
If maxBankingDaysBack = FConfirmationHooksTemplate then confirmations will Cancel for back-dated trades
See FCA2105
"""
MAX_BANKING_DAYS_BACK = 30


def CONF_PROLONG_DEPOSIT(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION
        This function checks if a term deposit trade has been rolled over on its maturity date.
    ----------------------------------------------------------------------------"""
    if trade:
        ins = trade.Instrument()
        if ins.InsType() == 'Deposit' and not ins.IsCallAccount():
            if trade.Contract() and trade.Contract() != trade.Oid():
                original_trade = trade.Contract()
                if trade.Counterparty() == original_trade.Counterparty():
                    if trade.Instrument().StartDate() == original_trade.Instrument().EndDate():
                        return helper.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), MAX_BANKING_DAYS_BACK)
    return False


def CONF_NEW_TRADE_EVENT(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION:
        This function creates a confirmation whenever a new trade has been created.
        The creation of New Trade confirmations is limited to trades of instrument
        types: 'Deposit' & 'Option'
    ----------------------------------------------------------------------------"""

    if trade:
        instrument = trade.Instrument()
        if instrument.InsType() not in ['Deposit', 'Option']:
            return False

        if trade.Status() in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed') and \
                not trade.Instrument().IsCallAccount():
            if trade.Type() not in ('Novated', 'Novated Assigned', 'Closing'):
                if not CONF_PROLONG_DEPOSIT(trade):
                    return helper.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), MAX_BANKING_DAYS_BACK)
    return False


def CONF_NEW_TRADE_EVENT_CALL(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION:
        This function creates a confirmation whenever a new call account trade has been created
    ----------------------------------------------------------------------------"""
    if trade:
        if trade.Status() in ('FO Confirmed', 'BO Confirmed') and trade.Instrument().IsCallAccount():
            if trade.Type() not in ('Novated', 'Closing'):
                return helper.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), MAX_BANKING_DAYS_BACK)
    return False


def CONF_CALL_RATE_FIXING(reset):
    """----------------------------------------------------------------------------
    DESCRIPTION:
        This function creates a rate fixing whenever the rate on a call account trade is amended
    ----------------------------------------------------------------------------"""
    if not reset.Leg().Instrument().IsCallAccount():
        return False
    isWeightedRateFixingEvent = False
    if IsWeightedReset(reset) and IsDeterminedCashFlow(reset.CashFlow()):
        latestReset = GetLatestResetInCashFlowPeriod(reset.CashFlow())
        if latestReset and latestReset == reset:
            if len(reset.CashFlow().Resets()) > 1:
                if reset.FixingValue() != reset.CashFlow().Resets()[0].FixingValue():
                    if to_date(reset.Day()) == to_date('today'):
                        maxBankingDaysBack = 15
                        isWeightedRateFixingEvent = helper.IsDateWithinMaxBankingDaysBackInterval(reset.ReadTime(),
                                                                                                  maxBankingDaysBack)
    return isWeightedRateFixingEvent


def CONF_ISPLEDGE_FROZEN(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION
        This function creates a confirmation whenever a trade has been ceded.
    ----------------------------------------------------------------------------"""
    if trade:
        ins = trade.Instrument()
        if trade.Type() not in ('Novated Assigned', 'Novated', 'Closing'):
            if is_valid_status(trade) and ins.InsType() == 'Deposit':
                if trade.AdditionalInfo().MM_Ceded_Amount():
                    if trade.AdditionalInfo().MM_Ceded_Amount() != '':
                        return True
    return False


def CONF_ISNOVATED(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION
        This function creates a "Novated" confirmation event for fixed term deposits expiring 30 days from today.
        It is executed indirectly as part of the FConfirmationEOD.
    ----------------------------------------------------------------------------"""
    if trade:
        if is_valid_status(trade) and trade.Type() == 'Novated Assigned':
            return helper.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), MAX_BANKING_DAYS_BACK)
    return False


def CONF_MATURITY_NOTICE(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION
        This function creates a "Maturity Notice" confirmation event for fixed term deposits expiring today days from
        today.
        It is executed indirectly as part of the FConfirmationEOD.
    ----------------------------------------------------------------------------"""

    dateToday = acm.Time.DateToday()
    calendar = helper.GetDefaultCalendar()

    if trade and trade.Status() in ('BO Confirmed', 'BO-BO Confirmed'):
        ins = trade.Instrument()
        if ins.InsType() == 'Deposit' and not ins.IsCallAccount():
            expiryDate = acm.Time().DateFromTime(ins.ExpiryDate())
            if expiryDate < dateToday:
                return False
            if calendar.BankingDaysBetween(expiryDate, dateToday) <= 1:
                return True
    return False


def IsPartialCloseEvent(trade):
    """----------------------------------------------------------------------------
    DESCRIPTION
        This function checks for a partial close.
    ----------------------------------------------------------------------------"""
    if not trade.IsKindOf(acm.FTrade):
        return False
    if trade.Status() not in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
        return False
    if trade.Type() == 'Closing' and IsZeroPosition(trade) is False:
        maxBankingDaysBack = 15
        return helper.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), maxBankingDaysBack)
    return False


def IsAdjustDepositEvent(cashFlow):
    """----------------------------------------------------------------------------
    DESCRIPTION
        This function checks for an adjust deposit event.
    ----------------------------------------------------------------------------"""
    isAdjustDepositEvent = False
    leg = cashFlow.Leg()
    instrument = leg.Instrument()
    if instrument.InsType() == 'Deposit' and cashFlow.CashFlowType() == 'Fixed Amount':
        if IsOriginalCashFlow(cashFlow) is False or IsAdjustedOriginalCashFlow(cashFlow) is True:
            maxBankingDaysBack = 15
            updateTime = acm.Time.DateTimeFromTime(cashFlow.UpdateTime())
            payDate = cashFlow.PayDate()
            isAdjustDepositEvent = helper.IsDateWithinMaxBankingDaysBackInterval(updateTime, maxBankingDaysBack) and \
                                   helper.IsDateWithinMaxBankingDaysBackInterval(payDate, maxBankingDaysBack)
    return isAdjustDepositEvent

