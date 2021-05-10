"""-----------------------------------------------------------------------------
PURPOSE                 :  Converts the forward rate for a leg's cashflows to a 
                           NACM rate for the proprietary valuation of Swaps.
DEPATMENT AND DESK      :  IRD, PCG
REQUESTER               :  Dirk Strauss
DEVELOPER               :  Francois Truter
CR NUMBER               :  549193
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer           Description
--------------------------------------------------------------------------------
2011-01-20 549193    Francois Truter     Initial implementation
                                        
"""

import acm

def ConvertToNacm(value, calendar, date, datePeriod):
    if not value or value != value:
        return value
    if hasattr(value, 'IsKindOf') and value.IsKindOf(acm.FDenominatedValue):
        value = value.Number()
    isPercentage = False
    if value < 1:
        isPercentage = True
        value = value * 100

    date2 = acm.Time().DateAdjustPeriod(date, datePeriod)
    if calendar.IsNonBankingDay(None, None, date2):
        date2 = calendar.AdjustBankingDays(date2, 1)

    days = acm.Time().DateDifference(date2, date)
    nacm = (pow(1.0 + (value * float(days) / (365.0 * 100.0)), 365.0 / (12.0 * float(days))) - 1.0) * 12.0 * 100.0
    if isPercentage:
        return nacm / 100
    else:
        return nacm

def NacmPV(staticLegInformations, instrumentSpotDate, riskFreeDiscountCurves, valuationDate):
    out = {}
    cashFlows = []
    cashFlowsPVs = []
    spotValue = 0.0
    calculationSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FMoneyFlowSheet')
    nacmColumn = 'Cash Analysis NACM Forward Rate'
    
    legIndex = 0
    for staticLegInfo in staticLegInformations:
        instrument = acm.FInstrument[staticLegInfo.InstrumentId()]
        if staticLegInfo.IsPayLeg():
            leg = instrument.PayLeg()
            nominal = - staticLegInfo.NominalFactor()
        else:
            leg = instrument.RecLeg()
            nominal = staticLegInfo.NominalFactor()

        currency = staticLegInfo.CurrencySymbol()
        riskFreeDiscountCurve = riskFreeDiscountCurves[legIndex]
        cashFlowInformations = staticLegInfo.CashFlowInformations()
        counter = 0
        for cashFlowInfo in cashFlowInformations.SortByProperty('StartDate'):
            cashFlow = acm.FCashFlow[cashFlowInfo.Id().Text()]
            newRate = calculationSpace.CalculateValue(cashFlow, nacmColumn)
                
            projected = nominal * newRate / 100 * cashFlowInfo.Period()
            pv = projected * riskFreeDiscountCurve.Discount(instrumentSpotDate, cashFlowInfo.PayDate())
            
            cashFlows.append(acm.DenominatedValue(projected, currency, cashFlowInfo.Id(), cashFlowInfo.PayDate()))
            cashFlowsPVs.append(acm.DenominatedValue(pv, currency, cashFlowInfo.Id(), instrumentSpotDate))
            spotValue += pv
        
        legIndex += 1
    
    out['result'] = acm.DenominatedValue(spotValue, currency, instrumentSpotDate)
    out['cashFlowProjected'] = cashFlows
    out['cashFlowResult'] = cashFlowsPVs
    return out
