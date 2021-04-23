
"""----------------------------------------------------------------------------
MODULE
    CSACurveFromXCCY - Module containing python Composite Function call (and 
    corresponding 'FCustomFunction'):
    
    CSACurveFromXCCY(constituentCurves, constituentCurveLinkTypes, compositeCurve, 
    valuationDate)

DESCRIPTION
    The built-in extension manager Module 'Composite Curve Examples' contains
    custom code examples needed for using the yield curve type 'Composite'.
    
    In order to apply this example the following four steps should be taken:
    
    1. Add choice list entry 'CSACurveFromXCCY' to choice list 'Composite Function'.
    
    2. Add the following choice list entries to choice list 'Composite Link Type':
    
    'CollCurrDomestic' - The default ("non-FX implied") OIS/CSA curve in the 
    collateral currency.
    'CompCurrFromBaseCurr' - The CSA discount curve in the composite curve currency 
    implied (via FX forwards/basis swaps) from the base currency (typically USD).
    'CollCurrFromBaseCurr' - The CSA discount curve in the collateral currency 
    implied (via FX forwards/basis swaps) from the base currency (typically USD).
    
    3. Create a new composite yield curve with 'Composite Function' set to 
    'CSACurveFromXCCY' and link the appropriate zero coupon Benchmark or Spread 
    curve to each Link Type entry.
    
    4. Add Period and/or Date points to the curve or (recommended) let the code below
    generate points identical to those used in the curve corresponding to Link Type
    'CompCurrFromBaseCurr' (or any of the two other Link Types if preferred).
    
    The curve constructed below is meant to be used for (CSA/OIS) discounting when 
    collateral currency is different from trade/ins currency and there are no
    quoted FX forwards/basis swaps available between these two currencies. The 
    currency of the composite curve should be equal to the trade/ins currency.
    
    The interpolation behavior below is; discount factors are asked for from each
    constituent curve at the Used Dates in the Composite Curve in order to calculate
    the discount factors in the latter at the same dates. The composite curve 
    discount factors are converted to spot rates in the curve Calculation Format. 
    If the composite curve is asked for a rate between the Used Dates in the 
    composite curve interpolation is made (between the now known spot rates) 
    according to composite curve Interpolation/Extrapolation settings.
    
    Refer to PRIME help for further details about Composite yield curves.
    
    (c) Copyright 2017 by FIS Front Arena. All rights reserved.

----------------------------------------------------------------------------"""

import acm

    # Help function for calculating the discount factors in the composite curve
def DiscountFactor(valuationDate, pointDate, CollCurrDomesticYC, CompCurrYCFromBaseCurr, CollCurrYCFromBaseCurr):
    df1 = CollCurrDomesticYC.Discount(valuationDate, pointDate)
    df2 = CompCurrYCFromBaseCurr.Discount(valuationDate, pointDate)
    df3 = CollCurrYCFromBaseCurr.Discount(valuationDate, pointDate)
    return df1 * df2 / df3
    
    
    # The main python function taking the parameters specified by the FCustomFunction
def CSACurveFromXCCY(constituentCurves, constituentCurveLinkTypes, compositeCurve, valuationDate):

    # The FIrCurveInformation is the transient calculation object created below
    # and returned from the function as the curve to use in ADFL
    
    # The FIrCurveTemplate is an object from which the properties for a curve can se set arbitrary. The 
    # wanted FIrCurveInformation object is later created from this object. 
    
    curve = acm.CurveBuilding.NewTemplate()

    CollCurrDomesticYC = None
    CompCurrYCFromBaseCurr = None
    CollCurrYCFromBaseCurr = None

    if (len(constituentCurves) != 3):
        raise Exception("Selected Composite Function requires exactly 3 Composite Links.")
        return curve

    for i in range(len(constituentCurveLinkTypes)):
        choiceList = constituentCurveLinkTypes[i]
        if choiceList:
            if choiceList.Name() == 'CollCurrDomestic':
                CollCurrDomesticYC = constituentCurves[i]
            if choiceList.Name() == 'CompCurrFromBaseCurr':
                CompCurrYCFromBaseCurr = constituentCurves[i]
            if choiceList.Name() == 'CollCurrFromBaseCurr':
                CollCurrYCFromBaseCurr = constituentCurves[i]

    if CollCurrDomesticYC == None or CompCurrYCFromBaseCurr == None or CollCurrYCFromBaseCurr == None:
        raise Exception("Selected Composite Function requires that Link Types 'CollCurrDomestic', 'CompCurrFromBaseCurr' and 'CollCurrFromBaseCurr' are defined.")
        return curve
        
    curr = compositeCurve.Currency()
    cal = curr.Calendar()
    # If internal spot rate Day Count/Rate Type is taken from curve settings
    # as per below care must be taken such that calculation formats are not
    # mixed (for example within one curve hierarchy). Below this is not an 
    # issue as only discount factors are used.
    curve.StorageDayCount(compositeCurve.StorageDayCount())
    curve.StorageRateType(compositeCurve.StorageCompoundingType())
    curve.InternalCompoundingType(compositeCurve.StorageCompoundingType())
    curve.InternalDaycountMethod(compositeCurve.StorageDayCount())
    curve.StorageCalcType('Spot Rate')
    curve.PayDayMethod(compositeCurve.PayDayMethod())
    curve.ReferenceDate(valuationDate)
    # Curve type 'Spread' (with curve format ZC) is also supported for the composite 
    # curve, if used a Base Curve must also be specified.
    curve.Type('Benchmark')
    curve.Format('Zero Coupon Curve')
    curve.CalendarInformation(cal.CalendarInformation())
    curve.InterpolationType(compositeCurve.InterpolationType())
    curve.ExtrapolationTypeShortEnd(compositeCurve.ExtrapolationTypeShortEnd())
    curve.ExtrapolationTypeLongEnd(compositeCurve.ExtrapolationTypeLongEnd())
    # All the valid FIrCurveInformation set/get methods can be viewed in the AEF Browser
                
    if compositeCurve.Points().Size() == 0:
        for pointDate in CompCurrYCFromBaseCurr.OriginalCurve().PointDates():
            curve.AddPoint(0.0, pointDate)
    else:
        for point in compositeCurve.Points():
            curve.AddPoint(0.0, point.ActualDate(valuationDate))
    
    discountFactorDays = []
    discountFactors = []

    for pointDate in curve.PointDates():
        discountFactorDays.append(pointDate)
        discFactor = DiscountFactor(valuationDate, pointDate, CollCurrDomesticYC, CompCurrYCFromBaseCurr, CollCurrYCFromBaseCurr)
        discountFactors.append(discFactor)
    
    # Create the FIrCurveInformation object from the template. 
    irCurveInformation = curve.IrCurveInformation()
    curve = None
    
    # 'RecalculateCurve' makes sure the calculation type Spot Rates matches the incoming 
    # discount factor vector (the first argument).
    # Only spot rates can be inserted to the curve object (and interpolation is applied 
    # on these spot rates).
    irCurveInformation.RecalculateCurve(discountFactors, discountFactorDays, valuationDate, 'None', 'None', 'Discount', '0d', 0)
    # 2nd argument is the vector of dates specifying dates for the spot rates
    # 3rd argument is the normal ADFL valuation date (which can be shifted)
    # 4th and 5th argument is 'Rate Type' and 'Day Count' (not applicable in this example 
    # as discount factors are used)
    # 6th argument is the 'Calculation Type' of the incoming values 
    # 7th argument is the Tenor if forward rates are sent to the function (not applicable 
    # in this example as discount factors are used)
    # Last argument is applicable if curve type 'Spread' is set on the FIrCurveInformation 
    # object, in this case '1' means that the incoming values to the 'RecalculateCurve' 
    # function should match only the top curve. '0' means that the whole curve hierarchy 
    # should be matched.
    
    # If 'RecalculateCurve' is not used (if for example fixed values are inserted to the 
    # curve) one must use 'curve.RecalculateInterpolationCoefficients()' if interpolation 
    # method is non-linear (used to for example calculate the splines).
    
    return irCurveInformation
