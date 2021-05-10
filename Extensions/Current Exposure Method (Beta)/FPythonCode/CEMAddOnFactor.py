import acm
import CEMCustomOverrides

hierarchy = acm.FHierarchy['CEM Parameters']
hierarchyTree = acm.FHierarchyTree()
hierarchyTree.Hierarchy(hierarchy)

#-------------------------------------------------------------------------
def CEMAddOnFactor(assetClass, maturity, rating):
    factor = 0.0
    
    levelType = rating if rating else maturity
    
    assetClassNode = hierarchyTree.FindChildByName01(assetClass, hierarchyTree.RootNode())
    if assetClassNode:
        factorNode = hierarchyTree.FindChildByName01(levelType, assetClassNode)
        if factorNode:
            dataValue = hierarchyTree.DataValueFromColumnName(factorNode, 'Factor')
            if dataValue:
                factor = dataValue.DataValueVA()

    return factor

#-------------------------------------------------------------------------
def CEMAssetClass(instrument):
    """ Get asset class """
    assetClass = CEMCustomOverrides.Custom_CEMAssetClass(instrument)
    if assetClass:
        return assetClass
    else:
        return CEMAssetClassDefault(instrument)

#-------------------------------------------------------------------------
def CEMRating(instrument):
    """ Get asset class """
    rating = CEMCustomOverrides.Custom_CEMRating(instrument)
    if rating:
        return rating
    else:
        return CEMRatingDefault(instrument)
        
#-------------------------------------------------------------------------
def CEMAssetClassDefault(instrument):
    if instrument.Class() == acm.FCreditDefaultSwap or instrument.Class() == acm.FTotalReturnSwap:
        return "Credit"
    if instrument.IsBasedOnEquity():
        return "Equities"
    elif instrument.IsPreciousMetal() or instrument.IsPreciousMetalSwap(): # and not IsBasedOnGold
        return "Precious Metals Except Gold"
    elif instrument.InsType() in ["Curr", "Fx Rate", "CurrSwap"]:
        return "FX and Gold"
    elif instrument.IsCashFlowInstrument():
        return "Interest Rates"
    elif instrument.IsDerivative():
        return CEMAssetClassDefault(instrument.Underlying())
    else:
        return "Other Commodities"

#-------------------------------------------------------------------------
def CEMRatingDefault(instrument):
    return "Non-Qualifying Reference Obligation"

#-------------------------------------------------------------------------
def CEMTimeToMaturityBucket(cemTimeToMaturity):    
    if cemTimeToMaturity <= 1.0:
        return "One Year or Less"
    elif cemTimeToMaturity <= 5.0:
        return "Over One Year to Five Years"
    else:
        return "Over Five Years"

#-------------------------------------------------------------------------
def CEMMaturity(maturityDate):
    dateToday = acm.Time.DateToday()
    dateDifference = float(acm.Time().DateDifference(maturityDate, dateToday)) / 365
    
    return max(dateDifference, 0.0)    

#-------------------------------------------------------------------------
def CEMFxAddOnsFromNotionals(denominatedValues):
    values = acm.FArray()
    
    for value in denominatedValues:
        cemTimeToMaturity = CEMMaturity(acm.Time.AsDate(value.DateTime()))
        values.Add(value * CEMAddOnFactor("FX and Gold", CEMTimeToMaturityBucket(cemTimeToMaturity), None))
            
    return values
