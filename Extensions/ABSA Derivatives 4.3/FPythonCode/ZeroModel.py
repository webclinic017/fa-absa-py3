
import acm

def theor(valuationDate, instrumentCurrency, undprice ):
    res = acm.DenominatedValue(0, instrumentCurrency, valuationDate)
    return {'result':res}
