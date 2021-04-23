
#***************************************************************
# 
# Module calculating the settlement amounts
# 
#***************************************************************

import acm
from SP_TrfUtils import BuySellMapping, TrfHasBarrier, TrfExpiryEvent, TrfExpiryEventsSortedByDate
from SP_DealPackageHelper import GetCurrencyPairPointsDomesticPerForeign, GetCurrencyPairPointsForeignPerDomestic

epsilon = 0.000001

def IsDomesticPerForeign(rateDirection):
    if rateDirection not in ('DomesticPerForeign', 'ForeignPerDomestic'):
        raise RuntimeError ('Invalid value for parameter "rateDirection"')
    return rateDirection == 'DomesticPerForeign'

def BuySellAsMultiplier(buySellForeign):
    if buySellForeign == 'SELL':
        return -1.0
    elif buySellForeign == 'BUY':
        return 1.0
    else:
        raise RuntimeError ('Invalid value for parameter "buySellForeign"')

def RateDirectionAsMultiplier(rateDirection):
    return 1.0 if IsDomesticPerForeign(rateDirection) else -1.0

def InverseTargetAsMultiplier(inverseTarget):
    return -1.0 if inverseTarget is True else 1.0

def FxRateValueToUse(rate, inverse, inverseMultiplier = 1.0):
    return inverseMultiplier * (rate if inverse is False or abs(rate) < epsilon else 1.0/rate)

def IntrinsicForAccumulation(strike, fixing, inverseTarget, buySellForeign, rateDirection):
    accumulationStrike = FxRateValueToUse(strike, inverseTarget == IsDomesticPerForeign(rateDirection), -1.0 if inverseTarget else 1.0 )
    accumulationFixing = FxRateValueToUse(fixing, inverseTarget == IsDomesticPerForeign(rateDirection), -1.0 if inverseTarget else 1.0 )
    return IntrinsicValue(accumulationStrike, accumulationFixing, buySellForeign)

def AdjustedStrike(strike, fixing, target, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection):
    if exactTarget is False or target < epsilon:
        return strike
    else:
        accumulation = IntrinsicForAccumulation(strike, fixing, inverseTarget, buySellForeign, rateDirection)
        return strike if accumulation < (target - previousTarget) else AdjustStrikeWithRemainingTarget(fixing, target - previousTarget, inverseTarget, buySellForeign, rateDirection)

def AdjustedStrikeCommodity(strike, fixing, target, previousTarget, exactTarget):
    if exactTarget is False or target < epsilon:
        return strike
    else:
        accumulation = fixing - strike
        if accumulation < (target - previousTarget):
            return strike
        else:
            return fixing - (target - previousTarget)

def AdjustStrikeMultiplier(inverseTarget, buySellForeign):
    return BuySellAsMultiplier(buySellForeign) * InverseTargetAsMultiplier(inverseTarget)

def AdjustStrikeWithRemainingTarget(fixing, remainingTarget, inverseTarget, buySellForeign, rateDirection):
    fixingForAdjustment = FxRateValueToUse(fixing, inverseTarget == IsDomesticPerForeign(rateDirection), 1.0)
    adjustedStrike = fixingForAdjustment - (remainingTarget * AdjustStrikeMultiplier(inverseTarget, buySellForeign))
    return FxRateValueToUse(adjustedStrike, inverseTarget == IsDomesticPerForeign(rateDirection), 1.0)

def IntrinsicValue(strike, fixing, buySellForeign):
    intrinsicValue = fixing - strike
    if buySellForeign != None:
        intrinsicValue *= BuySellAsMultiplier(buySellForeign)
    return intrinsicValue

def IntrinsicValueForPayOff(strike, fixing, buySellForeign, rateDirection):
    if rateDirection == None:
        strikeToUse = strike
        fixingToUse = fixing
    else:
        strikeToUse = FxRateValueToUse(strike, not IsDomesticPerForeign(rateDirection))
        fixingToUse = FxRateValueToUse(fixing, not IsDomesticPerForeign(rateDirection))
    return IntrinsicValue(strikeToUse, fixingToUse, buySellForeign)

def StrikeAdjustedIntrinsicValue(strike, fixing, target, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection):
    adjustedStrike = AdjustedStrike(strike, fixing, target, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection)
    return IntrinsicValueForPayOff(adjustedStrike, fixing, buySellForeign, rateDirection)

def StrikeAdjustedIntrinsicValueCommodity(strike, fixing, target, previousTarget, exactTarget):
    adjustedStrike = AdjustedStrikeCommodity(strike, fixing, target, previousTarget, exactTarget)
    return IntrinsicValueForPayOff(adjustedStrike, fixing, None, None)

def NotionalAtStrike(notional1, notional2, notionalAtStrike, hasBarrier):
    if notionalAtStrike == 'Notional 1':
        return notional1
    elif notionalAtStrike == 'Notional 2' and hasBarrier is False:
        return notional2
    return 0.0

def NotionalAmount(notional1, notional2, strike, fixing, buySellForeign, strikeDirection, hasBarrier, notionalAtStrike = None):
    intrinsic = IntrinsicValueForPayOff(strike, fixing, buySellForeign, strikeDirection)
    if abs(intrinsic) < epsilon:
        return NotionalAtStrike(notional1, notional2, notionalAtStrike, hasBarrier)
    return notional1 if intrinsic > 0.0 else notional2

def CurrencyConversion(fixing, settleInDomesticCurrency, rateDirection):
    return 1.0 if settleInDomesticCurrency is True else FxRateValueToUse(fixing, rateDirection == 'DomesticPerForeign')

def BarrierHit(fixing, barrierLevel, barrierInterpretation, buySellForeign, rateDirection):
    if barrierInterpretation == 'Past':
        return IntrinsicValueForPayOff(barrierLevel, fixing, buySellForeign, rateDirection) < 0
    else:
        return IntrinsicValueForPayOff(barrierLevel, fixing, buySellForeign, rateDirection) <= 0

def BarrierHitOrIgnored(fixing, hasBarrier, barrierLevel, barrierInterpretation, buySellForeign, rateDirection):
    return (not hasBarrier) or BarrierHit(fixing, barrierLevel, barrierInterpretation, buySellForeign, rateDirection)

def BarrierMultiplier(fixing, hasBarrier, barrierLevel, barrierInterpretation, buySellForeign, rateDirection):
    return 1.0 if BarrierHitOrIgnored(fixing, hasBarrier, barrierLevel, barrierInterpretation, buySellForeign, rateDirection) else 0.0

def PhysicalStrikeToUse(strike, fixing, target, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection):
    adjustedStrike = AdjustedStrike(strike, fixing, target, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection)
    return FxRateValueToUse(adjustedStrike, not IsDomesticPerForeign(rateDirection))

def TargetMultiplier(previousTarget, targetLevel):
    return 1.0 if targetLevel < epsilon or (targetLevel - previousTarget) > epsilon else 0.0

def TakeBarrierIntoAccount(hasBarrier, intrinsicValue):
    return hasBarrier and intrinsicValue < -epsilon

def CalculateCashAmount(fixing,
                        strike,
                        rateDirection,
                        targetLevel,
                        inverseTarget,
                        previousTarget,
                        exactTarget,
                        notional1,
                        notional2,
                        settleInDomesticCurrency,
                        buySellForeign,
                        hasBarrier,
                        barrierLevel,
                        barrierInterpretation):
    
    intrinsicValue = StrikeAdjustedIntrinsicValue(strike, fixing, targetLevel, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection)
    notional = NotionalAmount(notional1, notional2, strike, fixing, buySellForeign, rateDirection, hasBarrier)
    currencyConversion = CurrencyConversion(fixing, settleInDomesticCurrency, rateDirection)
    barrierMultiplier = BarrierMultiplier(fixing, TakeBarrierIntoAccount(hasBarrier, intrinsicValue), barrierLevel, barrierInterpretation, buySellForeign, rateDirection)
    targetMultiplier = TargetMultiplier(previousTarget, targetLevel)
        
    return intrinsicValue * notional * currencyConversion * barrierMultiplier * targetMultiplier

def CalculatePhysicalAmounts(fixing,
                             strike,
                             rateDirection,
                             targetLevel,
                             inverseTarget,
                             previousTarget,
                             exactTarget,
                             notional1,
                             notional2,
                             buySellForeign,
                             hasBarrier,
                             barrierLevel,
                             barrierInterpretation,
                             notionalAtStrike):
    
    intrinsicValue = StrikeAdjustedIntrinsicValue(strike, fixing, targetLevel, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection)
    notionalDomestic = NotionalAmount(notional1, notional2, strike, fixing, buySellForeign, rateDirection, hasBarrier, notionalAtStrike)
    strikeToUse = PhysicalStrikeToUse(strike, fixing, targetLevel, previousTarget, inverseTarget, exactTarget, buySellForeign, rateDirection)
    barrierMultiplier = BarrierMultiplier(fixing, TakeBarrierIntoAccount(hasBarrier, intrinsicValue), barrierLevel, barrierInterpretation, buySellForeign, rateDirection)
    targetMultiplier = TargetMultiplier(previousTarget, targetLevel)

    amountDomestic = notionalDomestic * BuySellAsMultiplier(buySellForeign) * barrierMultiplier * targetMultiplier
    amountForeign = -amountDomestic * strikeToUse
    
    return amountDomestic, amountForeign

def CalculateCommodityCashAmount(fixing,
                                 strike,
                                 targetLevel,
                                 previousTarget,
                                 exactTarget,
                                 notional1,
                                 notional2):
    intrinsicValue = StrikeAdjustedIntrinsicValueCommodity(strike, fixing, targetLevel, previousTarget, exactTarget)
    notional = NotionalAmount(notional1, notional2, strike, fixing, None, None, None)
    targetMultiplier = TargetMultiplier(previousTarget, targetLevel)
    return intrinsicValue * notional * targetMultiplier

def GetStrikeDecimals(instrument, rateDirection):
    if not hasattr(instrument, 'DecoratedObject'):
        instrument = acm.FBusinessLogicDecorator.WrapObject(instrument)
    if rateDirection == 'DomesticPerForeign':
        return GetCurrencyPairPointsDomesticPerForeign(instrument.ForeignCurrency(), instrument.DomesticCurrency())
    else:
        return GetCurrencyPairPointsForeignPerDomestic(instrument.ForeignCurrency(), instrument.DomesticCurrency())

def GetFixingValue(instrument, date, rateDirection):
    fixing = TrfExpiryEvent(instrument, date)
    if fixing is not None:
        if acm.Time.DateDifference(date, fixing.Date()) == 0.0:
            if fixing.EventValue() > epsilon:
                if rateDirection == 'ForeignPerDomestic':
                    return 1.0 / fixing.EventValue()
                else:
                    return fixing.EventValue()
            else:
                raise RuntimeError ('No fixing entered for %s' % date)
    raise RuntimeError ('Date %s is not a valid fixing date for %s' % (date, instrument.Name()))
    
def GetPreviousTarget(instrument, date):
    allFixings = TrfExpiryEventsSortedByDate(instrument)
    accumulation = 0.0
    for fixing in allFixings:
        if acm.Time.DateDifference(fixing.Date(), date) >= 0:
            break
        accumulation = fixing.TrfAccTarget()
    return accumulation

def BaseSettlementParameters(instrument, date):
    rateDirection = 'ForeignPerDomestic' if instrument.StrikeQuotation() and instrument.StrikeQuotation().Name() == 'Per Unit Inverse' else 'DomesticPerForeign'
    rateDecimals = GetStrikeDecimals(instrument, rateDirection)
    fixing = round(GetFixingValue(instrument, date, rateDirection), rateDecimals)
    strike = round(instrument.StrikePrice(), rateDecimals)
    barrier = round(instrument.Barrier(), rateDecimals)
    return {
                'fixing'                : fixing,
                'strike'                : strike,
                'rateDirection'         : rateDirection,
                'targetLevel'           : instrument.AdditionalInfo().Sp_TargetLevel(),
                'inverseTarget'         : instrument.AdditionalInfo().Sp_InvertedTarget(),
                'previousTarget'        : GetPreviousTarget(instrument, date),
                'exactTarget'           : instrument.AdditionalInfo().Sp_AdjustedStrike(),
                'notional1'             : instrument.ContractSize(),
                'notional2'             : instrument.AdditionalInfo().Sp_LeverageNotional(),
                'buySellForeign'        : BuySellMapping(instrument, 'Foreign'),
                'hasBarrier'            : TrfHasBarrier(instrument),
                'barrierLevel'          : barrier,
                'barrierInterpretation' : instrument.AdditionalInfo().Sp_BarrierCondition()
            }

def BaseCommoditySettlementParameters(instrument, date):
    return {
                'fixing': GetFixingValue(instrument, date, None),
                'strike': instrument.StrikePrice(),
                'targetLevel': instrument.AdditionalInfo().Sp_TargetLevel(),
                'previousTarget': GetPreviousTarget(instrument, date),
                'exactTarget': instrument.AdditionalInfo().Sp_AdjustedStrike(),
                'notional1': instrument.ContractSizeInQuotation(),
                'notional2': instrument.AdditionalInfo().Sp_LeverageNotional(),
            }
    

def CashSettlementParameters(instrument, date):
    params = BaseSettlementParameters(instrument, date)
    params['settleInDomesticCurrency'] = instrument.AdditionalInfo().Sp_SettleInCurr2()
    return params

def PhysicalSettlementParameters(instrument, date):
    params = BaseSettlementParameters(instrument, date)
    params['notionalAtStrike'] = instrument.AdditionalInfo().Sp_StrikeSettle()
    return params

def CommodityCashSettlementParameters(instrument, date):
    params = BaseCommoditySettlementParameters(instrument, date)
    return params

def CalculateTRFSettlementAmounts(trade, date):
    instrument = trade.Instrument()
    if instrument.AdditionalInfo().StructureType() != 'Target Redemption Forward':
        raise RuntimeError('TRF settlement calculations only implemented for Target Redemption Forward')
    if instrument.SettlementType() == 'Cash':
        return CalculateCashAmount(**CashSettlementParameters(instrument, date))
    else:
        return CalculatePhysicalAmounts(**PhysicalSettlementParameters(instrument, date))

def CalculateCommodityTRFSettlementAmounts(trade, date):
    instrument = trade.Instrument()
    if instrument.AdditionalInfo().StructureType() != 'Target Redemption Forward':
        raise RuntimeError('TRF settlement calculations only implemented for Target Redemption Forward')
    if instrument.SettlementType() == 'Cash':
        return CalculateCommodityCashAmount(**CommodityCashSettlementParameters(instrument, date))
    else:
        raise RuntimeError('TRF settlement calculations only implemented for Cash settlement')

