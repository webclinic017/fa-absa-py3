"""----------------------------------------------------------------------------
MODULE
    CSACurveCTD - Module containing python Composite Function call (and 
    corresponding 'FCustomFunction').

DESCRIPTION
    Cheapest-To-Deliver (CTD) curve example, buckets are only generated from 
    the 'FwdTenorGenerator' curve (as opposed to Union of all curves Used
    Dates, or other approaches).
    
    In order to apply this example the following three steps should be taken:
    
    1. Add choice list entry 'CSACurveCTD' to choice list 'Composite Function'.
    
    2. Add the following choice list entry to choice list 'Composite Link Type':
    
    'FwdTenorGenerator' - The curve used to generate buckets used for forward
    rate comparison and for generating buckets in the CTD curve.
    
    3. Create a new composite yield curve with 'Composite Function' set to 
    'CSACurveCTD' and link the appropriate zero coupon Benchmark or Spread 
    OIS curves. For one of these curves also set the Link Type to 'FwdTenorGenerator'.
    
    The curve constructed below is meant to be used for (CSA/OIS) discounting when 
    cash collateral currency can be selected among a given set of currencies. The 
    currency of the composite curve itself should be equal to the trade/ins 
    currency. Note that this valuation approach does not include any optionality
    adjustment for the fact that the collateral currency can be changed.
    
    The calculation of the final composite curve is performed as follows:
    1. For all linked constituent curves (one per possible collateral currency)
    the daily forward rates will be read for each bucket.
    2. Spot rates are then for each composite curve bucket sourced from the
    constituent curve which has the highest daily forward rate in each bucket.
    
    Refer to PRIME help for further details about Composite yield curves.
    
    (c) Copyright 2017 by FIS Front Arena. All rights reserved.    

----------------------------------------------------------------------------"""

import acm
import time

def SpotRates(constituentCurves, curveDates, valuationDate):
    actRates         = []
    timeToGetRate    = 0
    timeToGetIndex   = 0
    for date in curveDates:
        rates     = []
        endDate   = acm.Time.DateAddDelta(date, 0, 0, 1)
        for c in constituentCurves:
            fwdRate = c.Rate(date, endDate, 'Simple', 'Act/365', 'Forward Rate')
            rates.append(fwdRate)
            
        useCurve  = constituentCurves[rates.index(max(rates))]
        actualRate     = useCurve.Rate(valuationDate, date, 'Annual Comp', 'Act/365', 'Spot Rate')
        actRates.append(actualRate)

    return actRates
    
def CSACurveCTD(constituentCurves, constituentCurveLinkTypes, compositeCurve, valuationDate):
    curve = acm.CurveBuilding.NewTemplate()
    tenorCurve = None

    for i in range(len(constituentCurveLinkTypes)):
        choiceList = constituentCurveLinkTypes[i]
        if choiceList:
            if choiceList.Name() == 'FwdTenorGenerator':
                tenorCurve = constituentCurves[i]
                
    if not tenorCurve:
        raise Exception("Selected Composite Function requires that Link Type 'FwdTenorGenerator' is defined.")
        return curve
        
    curveDates  = tenorCurve.OriginalCurve().PointDates()
    actrates    = SpotRates(constituentCurves, curveDates, valuationDate)
    curr = compositeCurve.Currency()
    cal = curr.Calendar()
    curve.StorageDayCount(compositeCurve.StorageDayCount())
    curve.StorageRateType(compositeCurve.StorageCompoundingType())
    curve.InternalCompoundingType(compositeCurve.StorageCompoundingType())
    curve.InternalDaycountMethod(compositeCurve.StorageDayCount())
    curve.StorageCalcType('Spot Rate')
    curve.PayDayMethod(compositeCurve.PayDayMethod())
    curve.ReferenceDate(valuationDate)
    curve.Type('Benchmark')
    curve.Format('Zero Coupon Curve')
    curve.CalendarInformation(cal.CalendarInformation())
    curve.InterpolationType(compositeCurve.InterpolationType())
    curve.ExtrapolationTypeShortEnd(compositeCurve.ExtrapolationTypeShortEnd())
    curve.ExtrapolationTypeLongEnd(compositeCurve.ExtrapolationTypeLongEnd())
    irCurveInformation = curve.IrCurveInformation()
    curve = None
    irCurveInformation.RecalculateCurve(actrates, curveDates, valuationDate, 'Annual Comp', 'Act/365', 'Spot Rate', '0d', 0)
    return irCurveInformation
