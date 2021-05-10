
import acm
import string
import math
import FRTBCustomOverrides

def JTDScalingFactor( remainingMaturity ):
    if not math.isnan( remainingMaturity ):
        return max(0.25, min( 1.0, remainingMaturity ))
    return 1.0
    
def DRCIssuerType( party ):
    customIssuerType = FRTBCustomOverrides.Custom_DRCIssuerType( party )
    if customIssuerType:
        return customIssuerType
    issuerType = ""
    return issuerType
    
def DRCRemainingMaturity(instrument):
    customRemainingMaturity = FRTBCustomOverrides.Custom_DRCRemainingMaturity( instrument )
    if customRemainingMaturity:
        return customRemainingMaturity
    return 1.0
    
def DRCCreditQuality( party ):
    customRating = FRTBCustomOverrides.Custom_DRCCreditQuality( party )
    if customRating:
        return customRating
    
    ratingString = "Unrated"
    rating = party.Rating1()
    if not rating:
        rating = party.Rating2()
    if not rating:
        rating = party.Rating3()
    if rating:
        ratingString = rating.Name()
        ratingString = ratingString.replace("a", ratingString[0] ).strip( string.digits ).strip( string.punctuation )
        if ratingString[0] == "D" or ( ratingString[0] == "C" and len(ratingString) < 3 ):
            ratingString = "Defaulted"
    return ratingString

def DRCSeniority( instrument ):
    while instrument.Underlying():
        instrument = instrument.Underlying()

    customSeniority = FRTBCustomOverrides.Custom_DRCSeniority( instrument )
    if customSeniority:
        if "Equity/Non-Senior Debt" == customSeniority:
            customSeniority = "Equity"
        return customSeniority

    seniority = 'Other'
    return seniority

def FrtbDRCInclusionCriteriaFunction( instrumentOrRiskFactor, seniorities, issuer ):
    if instrumentOrRiskFactor.IsKindOf( acm.FPriceRiskReference ):
        instrument = instrumentOrRiskFactor.Instrument()
    else:
        instrument = instrumentOrRiskFactor
    if not instrument.IsKindOf( acm.FInstrument ):
        return False
    if issuer:
        if instrument.CreditReferenceIssuerOrIssuer() != issuer:
            return False
    return str(instrument.DRCSeniority()) in seniorities

def ToSADRCSeniority( seniority ):
    if str(seniority) in ["Equity", "Non-Senior Debt"]:
        return "Equity/Non-Senior Debt"
    return seniority
    
def IsLongCreditExposureInstrument( instrument ):
    if instrument.IsKindOf(acm.FDerivative):
        if instrument.IsCall():
            return IsLongCreditExposureInstrument( instrument.Underlying() )
        else:
            return not IsLongCreditExposureInstrument( instrument.Underlying() )
    else:
        legs = instrument.Legs()
        if legs:
            exposure = 0.0
            for leg in legs:
                payFactor = 1.0
                if leg.PayLeg():
                    payFactor = -1.0
                if leg.LegType() in ["Credit Default", "Total Return", "Position Total Return"]:
                    exposure -= payFactor * leg.NominalFactor()
                elif leg.NominalAtEnd():
                    exposure += payFactor * leg.NominalFactor()
            return exposure >= 0 and True or False
        else:
            return True

def IsLongCreditExposure( instrument, tradeQuantities ):
    
    q = 0.0
    for tq in tradeQuantities:
        q += tq.Number()
    if q >= 0:
        return IsLongCreditExposureInstrument( instrument )
    else:
        return not IsLongCreditExposureInstrument( instrument )
