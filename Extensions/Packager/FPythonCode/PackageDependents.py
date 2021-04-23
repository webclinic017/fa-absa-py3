"""
    PackageDependents
    
    (C)2012-2018 FIS Front Arena
    
    Return dependents
    
    20120522 Richard Ludwig
    
"""
import acm
from Transporter import ACM_INTERNAL_VERSION

def Dependents(object):
    dependents = list()
    if object == None:
        pass

    #elif object.IsKindOf(acm.FInstrument):

    elif object.IsKindOf(acm.FCombination):
        dependents.extend(object.Instruments())

    elif object.IsKindOf(acm.FContext):
        for link in list(object.ContextLinks()):
            if link.Instrument(): 
                dependents.append(link.Instrument())
            if link.Currency():
                dependents.append(link.Currency())
            if link.Portfolio():
                dependents.append(link.Portfolio())
            if str(link.Type()) == 'Accounting Parameter':
                dependents.append(acm.FAccountingParameters[link.Name()])
            elif str(link.Type()) == 'Correlation Matrix':
                dependents.append(acm.FCorrelationMatrix[link.Name()])
            elif str(link.Type()) in ('Repo', 'Risk Free Yield Curve', 'Yield Curve'):
                dependents.append(acm.FYieldCurve[link.Name()])
            elif str(link.Type()) == 'Dividend Stream':
                dependents.append(acm.FDividendStream[link.Name()])
            elif str(link.Type()) == 'Volatility':
                dependents.append(acm.FVolatilityStructure[link.Name()])                
                
    elif object.IsKindOf(acm.FYieldCurve):
        benchmarks = object.Benchmarks()
        if benchmarks:
            dependents.extend(object.Benchmarks())

    return [obj for obj in dependents if obj != None]
    
def Depends(object):
    depends = list()
    if object == None:
        pass

    elif object.IsKindOf(acm.FInstrument):
        if ACM_INTERNAL_VERSION < 4.18:
            pricelink = acm.FPriceDefinition.Select("instrument=%d"%object.Oid())
        else:
            pricelink = acm.FPriceLinkDefinition.Select("instrument=%d"%object.Oid())

        if pricelink:
            depends.extend(pricelink)

    return [obj for obj in depends if obj != None]

