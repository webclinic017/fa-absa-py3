
import acm
from sets import Set

def quotations(quotationArray):
    perUnitQuotation = acm.FQuotation["Per Unit"]
    typeStr = "('" + "', '".join(quotationArray) + "')"
    # for backwards compatibility when using an older ADM version. See SPR 381087.
    if perUnitQuotation.MetricSpaceType() == 'None':
        queryStr = "quotationType"
    else:
        queryStr = "metricSpaceType"
    
    quotations = acm.FQuotation.Select("%s in %s" % (queryStr, typeStr)).AsArray()
    quotations.Add(perUnitQuotation)
    return quotations
    

def instrumentsForProjectedPayments():

    projectedPaymentInstruments = []
    commodities = Set([])
    for comVar in acm.FCommodityVariant.Select(""):
        if comVar.IsInstrumentPairInstrument():
            projectedPaymentInstruments.append(comVar)
            commodities.add(comVar.Underlying())

    projectedPaymentInstruments.extend(acm.FCurrency.Select(""))
    projectedPaymentInstruments.extend(commodities)
    return projectedPaymentInstruments
    
    
def defaultNamedParameterForProjectedPayments():
    namedPar = acm.FNamedParameters()
    namedPar.Name("defaultInstrumentsSetExternally")
    namedPar.AddParameter("currency", acm.FCurrency())
    namedPar.AddParameter("quotation", acm.FQuotation())
    return namedPar
