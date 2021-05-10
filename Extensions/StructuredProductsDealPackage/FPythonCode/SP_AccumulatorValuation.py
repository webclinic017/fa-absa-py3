
# Setup needed:
#       - Additional Info field: AccumulatorLeverage
#       - ValGroup: AccDec
#       - Valuation Extension: accDecModelDesc
#       - Context Mapping: Valuation Extension accDecModelDesc mapped to val group AccDec


# Use price fixing exotic event to fix underlying prices
# Can we use the expiry time field on the exercise events?

import acm

# ####################################################################################
# NOTE: using an array of arrays does not work for barrier monitoring dates
#       Workaround is to use the "last" array for all options as this will contain
#       all possible dates.
# ####################################################################################
def FiniteDifferenceModelFullYieldCurves(paramDict, isCall):
    valFunc = acm.GetFunction("finiteDifferenceModelFullYieldCurves", 37)
    
    return valFunc( paramDict.At('underlyingValue'),
                    paramDict.At('volatility'),
                    paramDict.At('strikeValue'),
                    paramDict.At('discountCurve'),
                    paramDict.At('carryCostCurvePos'),
                    paramDict.At('carryCostCurveNeg'),
                    isCall,
                    paramDict.At('timeToExpiry'),
                    paramDict.At('timeToCarry'),
                    paramDict.At('timeToDiscount'),
                    paramDict.At('dividends'),
                    paramDict.At('valuationTime'),
                    paramDict.At('spotDate'),
                    paramDict.At('isAmerican'),
                    paramDict.At('isKnockIn'),
                    paramDict.At('isLowerBarrier'),
                    paramDict.At('isUpperBarrier'),
                    paramDict.At('barrier'),
                    paramDict.At('barrier2'),
                    paramDict.At('rebate'),
                    paramDict.At('payRebateOnExpiry'),
                    paramDict.At('pDESettings'),
                    paramDict.At('supressGreek'),
                    paramDict.At('isCrossed'),
                    paramDict.At('isCashSettled'),
                    paramDict.At('isDigital'),
                    paramDict.At('digitalBarrierType'),
                    paramDict.At('barrierMonitoring'),
                    paramDict.At('barrierDiscreteMonitoringDates')[-1] if paramDict.At('barrierDiscreteMonitoringDates').Size() > 0 else paramDict.At('barrierDiscreteMonitoringDates'),
                    paramDict.At('barrierWindowMonitoringDates')[-1] if paramDict.At('barrierWindowMonitoringDates').Size() > 0 else paramDict.At('barrierWindowMonitoringDates'),
                    paramDict.At('vFxQuanto'),
                    paramDict.At('vFlatDriftQuanto'),
                    paramDict.At('corrQuanto'),
                    paramDict.At('settlementDate'),
                    paramDict.At('instrumentSpotDate'),
                    paramDict.At('underlyingSpotDate'),
                    paramDict.At('expiryPlusUndSpotDays')
                    )

def BarrierContinuousAnalytic(paramDict, isCall):
    valFunc = acm.GetFunction("barrierContinuousAnalytic", 22)

    return valFunc( paramDict.At('forwardValueProvider'),
                    paramDict.At('forwardValueDate'),
                    paramDict.At('underlyingStartDate'),
                    paramDict.At('volatility'),
                    paramDict.At('strikePrice'),
                    paramDict.At('discountRate'),
                    isCall,
                    paramDict.At('valuationDateTime'),
                    paramDict.At('timeToExpiry'),
                    paramDict.At('timeToDiscount'),
                    paramDict.At('isKnockIn'),
                    paramDict.At('isDigital'),
                    paramDict.At('isLowerBarrier'),
                    paramDict.At('isUpperBarrier'),
                    paramDict.At('barrier'),
                    paramDict.At('barrier2'),
                    paramDict.At('rebate'),
                    paramDict.At('payRebateOnExpiry'),
                    paramDict.At('isCrossed'),
                    paramDict.At('crossedDate'),
                    paramDict.At('isCashSettled'),
                    paramDict.At('quantoCarryAdjustment'))

def FiniteDifferenceModel(paramDict, isCall):
    valFunc = acm.GetFunction("finiteDifferenceModel", 33)
    
    return valFunc( paramDict.At('underlyingValue'),
                    paramDict.At('volatility'),
                    paramDict.At('strikeValue'),
                    paramDict.At('discountRate'),
                    paramDict.At('carryCost'),
                    paramDict.At('carryCostIsDivYield'),
                    isCall,
                    paramDict.At('timeToExpiry'),
                    paramDict.At('timeToCarry'),
                    paramDict.At('timeToDiscount'),
                    paramDict.At('dividends'),
                    paramDict.At('valuationTime'),
                    paramDict.At('spotDate'),
                    paramDict.At('isAmerican'),
                    paramDict.At('isKnockIn'),
                    paramDict.At('isLowerBarrier'),
                    paramDict.At('isUpperBarrier'),
                    paramDict.At('barrier'),
                    paramDict.At('barrier2'),
                    paramDict.At('rebate'),
                    paramDict.At('payRebateOnExpiry'),
                    paramDict.At('pDESettings'),
                    paramDict.At('supressGreek'),
                    paramDict.At('isCrossed'),
                    paramDict.At('isCashSettled'),
                    paramDict.At('isDigital'),
                    paramDict.At('digitalBarrierType'),
                    paramDict.At('barrierMonitoring'),
                    paramDict.At('barrierDiscreteMonitoringDates')[-1] if paramDict.At('barrierDiscreteMonitoringDates').Size() > 0 else paramDict.At('barrierDiscreteMonitoringDates'),
                    paramDict.At('barrierWindowMonitoringDates')[-1] if paramDict.At('barrierWindowMonitoringDates').Size() > 0 else paramDict.At('barrierWindowMonitoringDates'),
                    paramDict.At('vFxQuanto'),
                    paramDict.At('vFlatDriftQuanto'),
                    paramDict.At('corrQuanto')
                    )

def FiniteDifferenceLocalVolatilityModel(paramDict, isCall):
    valFunc = acm.GetFunction("finiteDifferenceLocalVolatilityModel", 35)
    
    return valFunc( paramDict.At('underlyingValue'),
                    paramDict.At('volatility'),
                    paramDict.At('volatilityProvider'),
                    paramDict.At('unshiftedVolatilityProvider'),
                    paramDict.At('strikeValue'),
                    paramDict.At('discountRate'),
                    paramDict.At('carryCost'),
                    paramDict.At('carryCostIsDivYield'),
                    isCall,
                    paramDict.At('timeToExpiry'),
                    paramDict.At('timeToCarry'),
                    paramDict.At('timeToDiscount'),
                    paramDict.At('dividends'),
                    paramDict.At('valuationTime'),
                    paramDict.At('spotDate'),
                    paramDict.At('isAmerican'),
                    paramDict.At('isKnockIn'),
                    paramDict.At('isLowerBarrier'),
                    paramDict.At('isUpperBarrier'),
                    paramDict.At('barrier'),
                    paramDict.At('barrier2'),
                    paramDict.At('rebate'),
                    paramDict.At('payRebateOnExpiry'),
                    paramDict.At('pDESettings'),
                    paramDict.At('supressGreek'),
                    paramDict.At('isCrossed'),
                    paramDict.At('isCashSettled'),
                    paramDict.At('isDigital'),
                    paramDict.At('digitalBarrierType'),
                    paramDict.At('barrierMonitoring'),
                    paramDict.At('barrierDiscreteMonitoringDates')[-1] if paramDict.At('barrierDiscreteMonitoringDates').Size() > 0 else paramDict.At('barrierDiscreteMonitoringDates'),
                    paramDict.At('barrierWindowMonitoringDates')[-1] if paramDict.At('barrierWindowMonitoringDates').Size() > 0 else paramDict.At('barrierWindowMonitoringDates'),
                    paramDict.At('vFxQuanto'),
                    paramDict.At('vFlatDriftQuanto'),
                    paramDict.At('corrQuanto')
                    )

def GetPriceFixing(fixingDate, priceFixings, undSpot, valuationDateTime):
    for pf in priceFixings:
        if (pf.Date() == fixingDate) and (pf.EventValue() > 0.0):
            return pf.EventValue()
    
    if fixingDate == acm.Time().DateFromTime(valuationDateTime):
        return undSpot.Number()
    
    raise RuntimeError ( 'Missing price fixing for %s' % (str(fixingDate)) )

def ApplyLeverage( fixing, strike, accDecFactor):
    return ((strike - fixing) * accDecFactor > 0)

def CalculateHistoricalStrike(ee, historicalDividends):
    if not historicalDividends:
        return ee.Strike()

    historicalStrike = ee.Strike()
    for div in historicalDividends:
        if acm.Time().DateDifference(ee.ExpiryDate(), div.DateTime()) >= 0:
            historicalStrike -= div.Number()
    return historicalStrike

def PeriodIsExercised(ee):
    return ee.FreeText() == 'Exercised'

def SpotOrLastPeriodFixing(periodEndDate, valuationDateTime, priceFixings, undSpot):
    if acm.Time().DateDifference(periodEndDate, acm.Time().DateFromTime(valuationDateTime)) == 0:
        return GetPriceFixing(periodEndDate, priceFixings, undSpot, valuationDateTime)
    else:
        return undSpot.Number()

def PastDayValue( exerciseEvents, priceFixings, leverageFactor, 
                  accDec, valuationDateTime, undSpot, 
                  isIntradayExpired, crossedStatus, crossedDate,
                  currentStrike, historicalDividends):

    pastDayValue = 0.0
    accDecFactor = 1.0 if accDec else -1.0

    for ee in exerciseEvents:

        if acm.Time().DateDifference(ee.NoticeDate(), acm.Time().DateFromTime(valuationDateTime)) < 0:
            # Event is from closed period
            continue

        if ( crossedStatus == 'Confirmed' and crossedDate and
             acm.Time().DateFromTime(crossedDate) <= ee.ExpiryDate() ):
            continue

        # If period is closing today and we are past intraday expiry we will include the
        # value until exercise is booked
        if ( acm.Time().DateDifference(ee.NoticeDate(), acm.Time().DateFromTime(valuationDateTime)) == 0 and
             isIntradayExpired):
            if PeriodIsExercised(ee):
                continue
    
        # Change to expiry time method if possible
        if ( ee.ExpiryDate() < acm.Time().DateFromTime(valuationDateTime)
             or
             ( ee.ExpiryDate() == acm.Time().DateFromTime(valuationDateTime) and isIntradayExpired )):
            # We are past observation date but period is still open
            fixing = GetPriceFixing(ee.ExpiryDate(), priceFixings, undSpot, valuationDateTime)
            historicalStrike = CalculateHistoricalStrike(ee, historicalDividends)
            leverageFactorToUse = leverageFactor if ApplyLeverage(fixing, historicalStrike, accDecFactor) else 1.0
            undValueForPayoff = SpotOrLastPeriodFixing(ee.NoticeDate(), valuationDateTime, priceFixings, undSpot)
            pastDayValue += ((undValueForPayoff - currentStrike) * accDecFactor * leverageFactorToUse)

    return pastDayValue

def OptionSeries(paramDict, isCall):

    if paramDict.At('valuationMethod') == "barrierContinuousAnalytic":
        return BarrierContinuousAnalytic(paramDict.At('standardValParams'), isCall)
        
    elif paramDict.At('valuationMethod') == "finiteDifferenceModelFullYieldCurves":
        return FiniteDifferenceModelFullYieldCurves(paramDict.At('standardValParams'), isCall)
    
    elif paramDict.At('valuationMethod') == "finiteDifferenceModel":
        return FiniteDifferenceModel(paramDict.At('standardValParams'), isCall)
    
    elif paramDict.At('valuationMethod') == "finiteDifferenceLocalVolatilityModel":
        return FiniteDifferenceLocalVolatilityModel(paramDict.At('standardValParams'), isCall)
    
    else:
        raise Exception("valuationMethod '%s' not recognized/handled" % paramDict.At('valuationMethod'))

def CreateFArrayWithValue(value):
    newArray = acm.FArray()
    newArray.Add(value)
    return newArray

def GetvalueAsDenomiatedValue(value):
    if value.IsKindOf('FVariantDictionary'):
        return value.At("result")
    else:
        return value

def SumOfOptionSeries(seriesValuesAll, leverage, isIntradayExpired):
    # On expiry day the valuation funcrion will have been called with
    # just one value and no array will have been returned.
    if (hasattr(seriesValuesAll, 'IsKindOf') and
        (seriesValuesAll.IsKindOf('FDictionary') or seriesValuesAll.IsKindOf('FDenominatedValue'))):
        seriesValuesAll = CreateFArrayWithValue(seriesValuesAll)
    
    if isIntradayExpired:
        # If past todays expiry time we will still get an exercise event
        # with todays date but valuation will fail (or should not be taken into account)
        seriesValues = seriesValuesAll[1:]
    else:
        seriesValues = seriesValuesAll
    
    if seriesValues:
        total = GetvalueAsDenomiatedValue(seriesValues[0]) * leverage
        for item in seriesValues[1:]:
            total += (GetvalueAsDenomiatedValue(item) * leverage)
        return total
    return 0.0

def IsCompletelyExpired(endDate, isIntradayExpired):
    if acm.Time().DateDifference(acm.Time.DateToday(), endDate) > 0:
        return True
    if (acm.Time().DateDifference(acm.Time.DateToday(), endDate) == 0 and 
        isIntradayExpired):
        return True
    else:
        return False

def MoveValueToValuationDate(value, discount, repo, curveToUse, valuationDateTime):
    if curveToUse == 'Discount':
        return discount.DiscountValues(value, valuationDateTime)
    if curveToUse == 'Repo':
        return repo.DiscountValues(value, valuationDateTime)
    else:
        return value

def TheoreticalPrice(paramDict):

    # Only make a call to the actual valuation functions as long 
    # as there is at least one live expiry left. Otherwise there will
    # be an exception thrown.
    if not IsCompletelyExpired( paramDict.At ('endDate'),
                                paramDict.At ('isIntradayExpired') ):

        # is there leverage and on which side
        putLeverage  = -paramDict.At('leverageFactor') if paramDict.At('isCall') else 1.0
        callLeverage = 1.0 if paramDict.At('isCall') else -paramDict.At('leverageFactor')
        
        # 1) Calculate value of all put options
        putSeries  = OptionSeries(paramDict, False)
        totalPutSide = SumOfOptionSeries(putSeries, putLeverage, paramDict.At('isIntradayExpired'))

        # 2) Calculate value of all call options
        callSeries = OptionSeries(paramDict, True)
        totalCallSide = SumOfOptionSeries(callSeries, callLeverage, paramDict.At('isIntradayExpired'))

        totalFutureValue = MoveValueToValuationDate(totalCallSide + totalPutSide, 
                                                    paramDict.At('discountCurve'), 
                                                    paramDict.At('repoCurve'), 
                                                    paramDict.At('moveValue'),
                                                    paramDict.At('valuationDateTime') )

        

    else:
        totalFutureValue = acm.DenominatedValue(0.0, paramDict.At('currency'), paramDict.At('valuationDateTime') )

    # 3) Calculate the value of past observation dates that have not yet accumulated
    pastDayValue = PastDayValue( paramDict.At('exerciseEvents'), paramDict.At('priceFixings'), 
                                 paramDict.At('leverageFactor'), paramDict.At('isCall'),
                                 paramDict.At('valuationDateTime'), paramDict.At('underlyingSpot'),
                                 paramDict.At('isIntradayExpired'), paramDict.At('crossedStatus'),
                                 paramDict.At('crossedDate'), paramDict.At('currentStrike'),
                                 paramDict.At('historicalDividends') )

    pastDayValueDenom = acm.DenominatedValue(pastDayValue, totalFutureValue.Unit(), totalFutureValue.DateTime())

    theorPrice = totalFutureValue + pastDayValueDenom
    
    result = acm.FVariantDictionary()
    result.AtPut('result', theorPrice)

    return result
