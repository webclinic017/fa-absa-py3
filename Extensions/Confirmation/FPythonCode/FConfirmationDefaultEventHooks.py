""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationDefaultEventHooks.py"
import acm
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as HelperFunctions
from FOperationsEnums import InsType, TradeStatus, TradeType


def NewBondTradeEventHook(trade):
    if not trade.IsKindOf(acm.FTrade):
        return False
    return trade.Instrument().InsType() == InsType.BOND

def NewDepositTradeEventHook(trade):
    return trade.Instrument().InsType() == InsType.DEPOSIT

def IsBarrierCrossedEvent(trade):
    if not trade.IsKindOf(acm.FTrade):
        return False
    if not IsBOorBOBOConfirmed(trade):
        return False
    isBarrierCrossed = False
    instrument = trade.Instrument()
    exotics = acm.FExotic.Select("instrument = '%d'" % instrument.Oid())
    if (exotics.Size()
        and exotics.First().BarrierCrossedStatus() == 'Confirmed'):
        crossDate = exotics.First().BarrierCrossDate()
        if crossDate == "":
            crossDate = exotics.First().UpdateTime()
        maxBankingDaysBack = 15
        isBarrierCrossed = HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(crossDate, maxBankingDaysBack)
    return isBarrierCrossed

def GetPosition(trade):
    position = 0
    instrument = trade.Instrument()
    for _trade in instrument.Trades():
        if (_trade.Counterparty() == trade.Counterparty()        and
            _trade.Status()       != TradeStatus.VOID            and
            _trade.Status()       != TradeStatus.CONFIRMED_VOID  and
            _trade.Status()       != TradeStatus.SIMULATED       and
            _trade.Oid() > 0 ):
            position += _trade.Nominal()
    return position

def IsZeroPosition(trade):
    if not trade.IsKindOf(acm.FTrade):
        return False
    return abs(GetPosition(trade)) < 10e-6

def IsBOorBOBOConfirmed(trade):
    return (trade.Status() == TradeStatus.BO_CONFIRMED or trade.Status() == TradeStatus.BO_BO_CONFIRMED)

def IsExerciseEvent(trade):
    if not trade.IsKindOf(acm.FTrade):
        return False
    if not IsBOorBOBOConfirmed(trade):
        return False
    if trade.Type() == TradeType.EXCERCISE:
        maxBankingDaysBack = 15
        return HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), maxBankingDaysBack)
    return False

def IsPartialCloseEvent(trade):
    if not trade.IsKindOf(acm.FTrade):
    	return False
    if trade.DealPackage() and not trade.IsDealPackageLeadTrade():
    	return False
    if not IsBOorBOBOConfirmed(trade):
    	return False
    if (trade.Type() == TradeType.CLOSING and IsZeroPosition(trade) == False):
    	maxBankingDaysBack = 15
    	return HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), maxBankingDaysBack)
    return False

def IsCloseEvent(trade):
    if not trade.IsKindOf(acm.FTrade):
    	return False
    if trade.DealPackage() and not trade.IsDealPackageLeadTrade():
    	return False
    if (trade.Type() == TradeType.CLOSING and IsZeroPosition(trade) == True):
    	maxBankingDaysBack = 15
    	return HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), maxBankingDaysBack)
    return False

def IsDeterminedCashFlow(cashFlow):
    if cashFlow == None:
        return False
    for reset in cashFlow.Resets():
        if not reset.IsFixed():
            return False
    return True

def IsWeightedReset(reset):
    resetType = reset.ResetType()
    return (resetType == 'Weighted' or
            resetType == 'Weighted 1m Compound' or
            resetType == 'Weighted Average Coupon' or
            resetType == 'Compound of Weighted' or
            resetType == 'Total Weighted')

def IsRateFixingEvent(reset):
    if (IsWeightedReset(reset) == False and
            IsDeterminedCashFlow(reset.CashFlow())):
        maxBankingDaysBack = 15
        return HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(reset.ReadTime(), maxBankingDaysBack)
    return False

def GetLatestResetInCashFlowPeriod(cashFlow):
    resets = cashFlow.Resets()
    latestReset = None
    if len(resets):
        for reset in resets:
            if not latestReset:
                latestReset = reset
                continue
            if reset.Day() > latestReset.Day():
                latestReset = reset
    return latestReset

def IsWeightedRateFixingEvent(reset):
    isWeightedRateFixingEvent = False
    if (IsWeightedReset(reset) and
        IsDeterminedCashFlow(reset.CashFlow())):
        latestReset = GetLatestResetInCashFlowPeriod(reset.CashFlow())
        if (latestReset and latestReset == reset):
            maxBankingDaysBack = 15
            isWeightedRateFixingEvent = HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(reset.ReadTime(), maxBankingDaysBack)

    return isWeightedRateFixingEvent

def IsAdjustedOriginalCashFlow(cashFlow):
    return IsOriginalCashFlow(cashFlow) and cashFlow.CreateTime() != cashFlow.UpdateTime()

def IsOriginalCashFlow(cashFlow):
    return abs(cashFlow.CreateTime() - cashFlow.Leg().CreateTime()) <= 1

def IsAdjustDepositEvent(cashFlow):
    isAdjustDepositEvent = False
    leg = cashFlow.Leg()
    instrument = leg.Instrument()
    if (instrument.InsType() == InsType.DEPOSIT and
        cashFlow.CashFlowType()      == 'Fixed Amount'):
        if (IsOriginalCashFlow(cashFlow)         == False or
            IsAdjustedOriginalCashFlow(cashFlow) == True):
            maxBankingDaysBack = 15
            updateTime = acm.Time.DateTimeFromTime(cashFlow.UpdateTime())
            isAdjustDepositEvent = HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(updateTime, maxBankingDaysBack)
    return isAdjustDepositEvent

def IsNewTradeEvent(trade):
    if (trade.Status() == TradeStatus.FO_CONFIRMED or
            trade.Status() == TradeStatus.BO_CONFIRMED or
            trade.Status() == TradeStatus.BO_BO_CONFIRMED):
        if (trade.DealPackage() == None or
            trade.DealPackage().LeadTrade() == None):
            maxBankingDaysBack = 15
            return HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), maxBankingDaysBack)
    return False

def IsNewDealPackageEvent(trade):
    if (trade.Status() == TradeStatus.FO_CONFIRMED or
            trade.Status() == TradeStatus.BO_CONFIRMED or
            trade.Status() == TradeStatus.BO_BO_CONFIRMED):
        if trade.IsDealPackageLeadTrade():
            maxBankingDaysBack = 15
            return HelperFunctions.IsDateWithinMaxBankingDaysBackInterval(trade.ValueDay(), maxBankingDaysBack)
    return False

def IsDepositMaturityEvent(trade):
    isDepositMaturityEvent = False
    instrument = trade.Instrument()
    if (trade.Status() == TradeStatus.FO_CONFIRMED or
            trade.Status() == TradeStatus.BO_CONFIRMED or
            trade.Status() == TradeStatus.BO_BO_CONFIRMED):
        if instrument.InsType() == InsType.DEPOSIT:
            endDate = instrument.EndDate()
            dateToday = acm.Time.DateToday()
            calendar = HelperFunctions.GetDefaultCalendar()
            daysBetween = calendar.BankingDaysBetween(endDate, dateToday)
            if dateToday < endDate:
                if daysBetween == 1:
                    isDepositMaturityEvent = True
            else:
                isDepositMaturityEvent = True
    return isDepositMaturityEvent
