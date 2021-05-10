

import acm

def df(today, undSpotDaysOffset, etfSpotDaysOffset, ins):
    
    
    
    cal = ins.Currency().Calendar().Name()
    
    cs = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

    FIrCurveInformation = ins.Calculation().MappedDiscountCurve(cs)
      
    d1 = acm.FCalendar[cal].AdjustBankingDays(today, undSpotDaysOffset)

    d2 = acm.FCalendar[cal].AdjustBankingDays(today, etfSpotDaysOffset)
    
    df = FIrCurveInformation.Discount(d1, d2)
    
    return df
    
  
    
    
    


