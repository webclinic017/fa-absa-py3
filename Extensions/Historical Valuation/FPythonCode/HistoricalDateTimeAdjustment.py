import acm

dateDifferenceFunction = acm.GetFunction('dateDifference', 2)
cutOffDateTimeFunction = acm.GetFunction('historicalCutOffDateTime', 1)
isHistoricalMode = acm.IsHistoricalMode()

def DateIsHistorical(valuationSystemDateTime, dateTimeInput):
    daysBetween = dateDifferenceFunction(valuationSystemDateTime, dateTimeInput)
    return (isHistoricalMode and daysBetween >= 0) or (not isHistoricalMode and daysBetween > 0)

def ValuationBaseDateTimeAdjustment(valuationSystemDateTime, valuationBaseDateTimeInput):
    if DateIsHistorical(valuationSystemDateTime, valuationBaseDateTimeInput):
        return cutOffDateTimeFunction(valuationBaseDateTimeInput)
    return valuationBaseDateTimeInput

def PositionDateTimeAdjustment(valuationSystemDateTime, positionDateTimeInput):
    if DateIsHistorical(valuationSystemDateTime, positionDateTimeInput):
        return cutOffDateTimeFunction(positionDateTimeInput)
    return acm.Time.NotADateTime()
