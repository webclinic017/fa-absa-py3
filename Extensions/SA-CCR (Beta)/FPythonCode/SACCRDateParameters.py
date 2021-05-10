
import acm
import SACCRInterestRates
import SACCRCredit

from CreditRiskTools import DateDifferenceInYears

BUSINESS_DAYS_FLOOR = 10.0 / 250

#-------------------------------------------------------------------------
# Published - FCashFlow SA-CCR date methods
#-------------------------------------------------------------------------
def SACCRMaturityCashFlow(cashFlow):
    return DateDifferenceInYears(cashFlow.PayDate(), acm.Time.DateToday())

#-------------------------------------------------------------------------
def SACCRStartCashFlow(cashFlow):
    if SACCRInterestRates.IsInterestRates(cashFlow.Instrument()):
        return DateDifferenceInYears(cashFlow.StartDate(), acm.Time.DateToday())
    else:
        return 0.0
    
#-------------------------------------------------------------------------
def SACCREndCashFlow(cashFlow):
    if SACCRInterestRates.IsInterestRates(cashFlow.Instrument()):
        return DateDifferenceInYears(cashFlow.EndDate(), acm.Time.DateToday())
    else:
        return 0.0
    
#-------------------------------------------------------------------------
def SACCRLatestExerciseCashFlow(cashFlow):
    if cashFlow.Instrument().SACCRIsOption():
        return DateDifferenceInYears(cashFlow.StartDate(), acm.Time.DateToday())
    else:
        return 0.0

#-------------------------------------------------------------------------
# Published - FInstrument SA-CCR date methods
#-------------------------------------------------------------------------
def SACCRMaturityInstrument(instrument):
    if instrument.IsDerivative() and PhysicallySettledIntoUnderlyingContract(instrument):
        return SACCRMaturityInstrument(instrument.Underlying())
    
    return DateDifferenceInYears(instrument.LastPayDay(), acm.Time.DateToday())
    
#-------------------------------------------------------------------------
def SACCRStartInstrument(instrument, startDate = ""):
    if SACCRInterestRates.IsInterestRates(instrument) or \
       SACCRCredit.IsCredit(instrument):
        startDate = SACCRStartDate(instrument)
        
        return DateDifferenceInYears(startDate, acm.Time.DateToday())
    
    return 0.0

#-------------------------------------------------------------------------
def SACCREndInstrument(instrument):
    if SACCRInterestRates.IsInterestRates(instrument) or \
       SACCRCredit.IsCredit(instrument):
        endDate = SACCREndDate(instrument)
        
        return DateDifferenceInYears(endDate, acm.Time.DateToday())
        
    return 0.0

#-------------------------------------------------------------------------
def SACCRLatestExerciseInstrument(instrument):
    if instrument.SACCRIsOption():
        latestExercise = GetLatestExerciseDate(instrument)
        
        return DateDifferenceInYears(latestExercise, acm.Time.DateToday())
    
    return 0.0

#-------------------------------------------------------------------------
# Published functions
#-------------------------------------------------------------------------
def SACCRSupervisoryDuration(object):
    startDate = object.SACCRStart()
    endDate = object.SACCREnd()
    
    if endDate:
        endDate = max(endDate - startDate, BUSINESS_DAYS_FLOOR) + startDate
    
    return (acm.Math.Exp(-0.05 * startDate) - acm.Math.Exp(-0.05 * endDate)) / 0.05

#-------------------------------------------------------------------------
def SACCRMaturityFactor(timeToMaturity):
    return acm.Math.Sqrt( min( max(BUSINESS_DAYS_FLOOR, timeToMaturity), 1 ) )
    
#-------------------------------------------------------------------------
# Not published
#-------------------------------------------------------------------------
def SACCRStartDate(instrument, startDate = ""):
    if instrument.IsDerivative():
        startDate = GetEarliestExerciseDate(instrument) if instrument.IsKindOf(acm.FOption) else instrument.ExpiryDate()
        return SACCRStartDate(instrument.Underlying(), startDate)
    
    if not startDate:
        startDate = acm.Time.DateToday()
        
    return max(instrument.StartDate(), startDate)

#-------------------------------------------------------------------------
def SACCREndDate(instrument):
    if instrument.IsDerivative():
        return SACCREndDate(instrument.Underlying())
        
    return instrument.ExpiryDate()
    
#-------------------------------------------------------------------------    
# SA-CCR Optionality
#-------------------------------------------------------------------------    
def GetLatestExerciseDate(instrument):
    exerciseEvents = instrument.ExerciseEvents().SortByProperty("Date", False)
    
    return exerciseEvents.First().Date() if exerciseEvents.Size() > 0 else instrument.ExpiryDate()
    
#-------------------------------------------------------------------------    
def GetEarliestExerciseDate(instrument):
    exerciseEvents = instrument.ExerciseEvents().SortByProperty("Date", True)
    
    return exerciseEvents.First().Date() if exerciseEvents.Size() > 0 else instrument.ExpiryDate()
    
#-------------------------------------------------------------------------    
def PhysicallySettledIntoUnderlyingContract(instrument):
    if instrument.SettlementType() == "Physical Delivery":
        underlying = instrument.Underlying()
        if underlying and not (underlying.IsKindOf(acm.FIndex) or underlying.IsSecurity()):
            return True
            
    return False
