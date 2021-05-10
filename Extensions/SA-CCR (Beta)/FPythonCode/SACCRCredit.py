
import string

import acm

import SACCRDateParameters

#------------------------------------------------------------------------------
# SA-CCR Credit Classification
#------------------------------------------------------------------------------
def IsCredit( instrument ):
    if instrument.IsCredit():
        if instrument.IsKindOf( acm.FCreditDefaultSwap ):
            return ValidCDS( instrument )
                
    if instrument.IsKindOf( acm.FOption ):
        return IsCredit( instrument.Underlying() )
    
    return False

#------------------------------------------------------------------------------
def ValidCDS( cds ):
    floatLeg = cds.FirstFloatLeg()
    
    if floatLeg:
        return False
        
    if cds.CreditBasketExoticType() in ["Loss Protection", "Nth-To-Default"]:
        return False
    
    if cds.Underlying().Class() not in [acm.FBond, acm.FCreditIndex]:
        return False
    
    return True

#------------------------------------------------------------------------------
def HedgingSet( instrument ):
    return ""

#------------------------------------------------------------------------------
def HedgingSubset( instrument ):
    underlying = instrument.Underlying()
    
    if underlying:
        return HedgingSubset( underlying )
    else:
        if instrument.IsKindOf( acm.FCreditIndex ):
            return instrument
        else:
            return instrument.Issuer()

#------------------------------------------------------------------------------
def SACCRSubclass( object ):
    return CreditRating( object )
    
#------------------------------------------------------------------------------
# Credit Rating methods
#------------------------------------------------------------------------------
def CreditRating( object ):
    if object.IsKindOf( acm.FCreditIndex ):
        return IndexCreditRating( object )
    elif object.IsKindOf( acm.FIssuer ):
        return IssuerCreditRating( object )
    else:
        ratingEntity = HedgingSubset( object )
        return CreditRating( ratingEntity )

#------------------------------------------------------------------------------
def IssuerCreditRating( issuer ):
    ratingString = ""
    rating = issuer.Rating1()
    
    if not rating:
        rating = issuer.Rating2()
    if not rating:
        rating = issuer.Rating3()
    if rating:
        ratingString = rating.Name()
        ratingString = ratingString.replace( "a", ratingString[0] ).strip( string.digits ).strip( string.punctuation )
    
    if ratingString not in ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC']:
        msg = "Could not find matching credit rating for issuer {}.".format( issuer.Name() )
        acm.Log( msg )
        raise Exception( msg )
        
    return ratingString
    
#------------------------------------------------------------------------------
def IndexCreditRating( creditIndex ):
    category = creditIndex.CategoryChlItem()

    if (not category) or (category.Name() not in ['IG', 'SG']):
        msg = "Credit rating must be specified in Category field for {}.".format( creditIndex.Name() )
        acm.Log( msg )
        raise Exception( msg )
        
    return category.Name()

#------------------------------------------------------------------------------
# Notional
#------------------------------------------------------------------------------
def AdjustedNotional( instrument, unadjustedNotional ):
    return unadjustedNotional * SACCRDateParameters.SACCRSupervisoryDuration( instrument )

#------------------------------------------------------------------------------
# Supervisory Delta
#------------------------------------------------------------------------------ 
def SupervisoryDeltaAdjustment( instrument, positionQuantity ):
    creditLegs = [leg for leg in instrument.Legs() if leg.LegType() == "Credit Default"]
    
    assert len( creditLegs ) == 1, "Instrument {} has more/less than 1 credit default leg.".format( instrument.Name() )
    
    creditLeg = creditLegs[0]
    
    if not creditLeg.PayLeg():
        return 1 if positionQuantity > 0 else -1
    else:
        return 1 if positionQuantity < 0 else -1
