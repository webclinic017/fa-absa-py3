
import acm
import SACCRDateParameters

from SACCREnums import MaturityBuckets

#------------------------------------------------------------------------------
# SA-CCR Interest Rates Classification
#------------------------------------------------------------------------------
def IsInterestRates(instrument):
    if instrument.SACCRIsOption():
        if instrument.IsKindOf(acm.FOption) and instrument.Underlying().IsKindOf(acm.FSwap):
            return IsInterestRates(instrument.Underlying())
            
        if instrument.IsKindOf(acm.FCap) or instrument.IsKindOf(acm.FFloor):
            return ValidCapFloor(instrument)
    else:
        if instrument.IsKindOf(acm.FSwap):
            return ValidSwap(instrument)

        if instrument.IsKindOf(acm.FFra):
            return True

    return False

#------------------------------------------------------------------------------
def HedgingSet(instrument):
    return instrument.Currency()

#------------------------------------------------------------------------------
def HedgingSubset(object):
    endDate = object.SACCREnd()
    
    if endDate <= 1.0:
        return MaturityBuckets.LESS_ONE_YEAR
    elif endDate <= 5.0:
        return MaturityBuckets.ONE_FIVE_YEARS
    else:
        return MaturityBuckets.OVER_FIVE_YEARS
        
#------------------------------------------------------------------------------
def SACCRSubclass( instrument ):
    return ""
    
#------------------------------------------------------------------------------
def ValidSwap(swap):
    if swap.Callable() or swap.Putable():
        return False
    
    # Fixed vs float
    if not swap.IsFixedFloatSwap():
        return False
        
    floatLeg = swap.FirstFloatLeg()
    
    # Not quanto
    if floatLeg.FloatRateReference().Currency() != swap.Currency():
        return False
        
    return True

#------------------------------------------------------------------------------
def ValidCapFloor(instrument):
    leg = instrument.FirstFloatLeg()
    
    # Not quanto
    if leg.FloatRateReference().Currency() != instrument.Currency():
        return False
    
    # Digital
    if leg.Digital():
        return False
    
    # Inflation
    if leg.IsInflationOptionalityLeg():
        return False
    
    if leg.ExoticType() != "None":
        return False
        
    if instrument.NonDeliverable():
        return False
        
    return True
    
#------------------------------------------------------------------------------
# Notional
#------------------------------------------------------------------------------
def AdjustedNotional(instrument, unadjustedNotional):
    return unadjustedNotional * SACCRDateParameters.SACCRSupervisoryDuration(instrument)

#------------------------------------------------------------------------------
# Supervisory Delta
#------------------------------------------------------------------------------
def SupervisoryDeltaAdjustment(instrument, positionQuantity):
    floatLegs = [leg for leg in instrument.Legs() if leg.FloatRateReference()]
    
    assert len(floatLegs) == 1, "Instrument {} has more/less than 1 float leg.".format(instrument.Name())

    floatLeg = floatLegs[0]
    
    if floatLeg.PayLeg():
        return -1 if positionQuantity > 0 else 1
    else:
        return -1 if positionQuantity < 0 else 1
