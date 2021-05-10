
import acm

def CupomInflationModel(inflationValue, currencySymbol, forwardDate):
    out = {}
    out['result'] = acm.DenominatedValue(inflationValue.Number(), currencySymbol, forwardDate)
    return out
