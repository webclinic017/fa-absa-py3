
import acm

#------------------------------------------------------------------------------
# SA-CCR Equity Classification
#------------------------------------------------------------------------------
def IsEquity( instrument ):
    if instrument.IsDerivative():
        if instrument.Underlying().Class() in [acm.FStock, acm.FEquityIndex]:
            if instrument.IsKindOf( acm.FOption ):
                if not (instrument.IsQuanto() or instrument.IsExotic() or instrument.Digital()):
                    return True
                    
            elif instrument.IsKindOf( acm.FFuture ):
                if instrument.PayType() == "Forward":
                    if instrument.Currency() == instrument.Underlying().Currency():
                        return True
                    
    return False

#------------------------------------------------------------------------------
def HedgingSet( instrument ):
    return ""
    
#------------------------------------------------------------------------------
def HedgingSubset( instrument ):
    underlying = instrument.Underlying()
    
    if underlying.IsKindOf( acm.FEquityIndex ):
        return underlying
    else:
        return underlying.Issuer()

#------------------------------------------------------------------------------
def SACCRSubclass( object ):
    if object.IsKindOf( acm.FEquityIndex ):
        return "Index"
    elif object.IsKindOf( acm.FIssuer ):
        return "Single Name"
    else:
        hedgingSubset = HedgingSubset( object )
        return SACCRSubclass( hedgingSubset )


#------------------------------------------------------------------------------
# Supervisory Delta
#------------------------------------------------------------------------------
def SupervisoryDeltaAdjustment( instrument, positionQuantity ):
    return 1 if positionQuantity > 0 else -1

