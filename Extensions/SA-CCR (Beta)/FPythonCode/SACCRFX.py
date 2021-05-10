
import acm

#------------------------------------------------------------------------------
# SA-CCR FX Classification
#------------------------------------------------------------------------------
def IsFX(instrument):
    return instrument.IsKindOf(acm.FFxRate)

#------------------------------------------------------------------------------
def HedgingSet(instrument):
    return instrument.CurrencyPair(True)

#------------------------------------------------------------------------------
def HedgingSubset(object):
    return ""

#------------------------------------------------------------------------------
def SACCRSubclass( instrument ):
    return ""
    
