
import acm


def CreditIssuerRiskFactors( creditCurves, issuers ):
    out = []
    func = acm.GetFunction( 'creditCurveFilter', 6 )
    for curve in creditCurves:
        for issuer in issuers:
            criteria = func( ["Issuer"], issuer.Name() )
            if criteria.IsSatisfiedBy( curve ):
                out.append( issuer )
    return out
