
import acm
import SACCRInterestRates, SACCRFX, SACCREquity, SACCRCredit, SACCRCommodity
import SACCRAggregationManager as AM

from SACCREnums import AssetClass

assetClassModuleMap = {AssetClass.INTEREST_RATES : SACCRInterestRates,
                       AssetClass.FX : SACCRFX,
                       AssetClass.EQUITY : SACCREquity,
                       AssetClass.CREDIT : SACCRCredit,
                       AssetClass.COMMODITY : SACCRCommodity}

#------------------------------------------------------------------------------
# Published
#------------------------------------------------------------------------------
def SACCRAssetClass( instrument ):

    if SACCRInterestRates.IsInterestRates(instrument):
        return AssetClass.INTEREST_RATES
    elif SACCRFX.IsFX(instrument):
        return AssetClass.FX
    elif SACCREquity.IsEquity(instrument):
        return AssetClass.EQUITY
    elif SACCRCredit.IsCredit(instrument):
        return AssetClass.CREDIT
    elif SACCRCommodity.IsCommodity(instrument):
        return AssetClass.COMMODITY
    else:
        return AssetClass.UNDEFINED

#------------------------------------------------------------------------------
def SACCRHedgingSet( instrument ):
    assetClass = instrument.SACCRAssetClass()
    return assetClassModuleMap[assetClass].HedgingSet(instrument)

#------------------------------------------------------------------------------
def SACCRHedgingSubset( object, assetClass ):
    return assetClassModuleMap[assetClass].HedgingSubset(object)

#------------------------------------------------------------------------------
def SACCRSubclass( object, assetClass ):
    return assetClassModuleMap[assetClass].SACCRSubclass(object)
    
#------------------------------------------------------------------------------
def SACCRAdjustedNotional(instrument, assetClass, unadjustedNotional):
    return assetClassModuleMap[assetClass].AdjustedNotional(instrument, unadjustedNotional)
        
#-------------------------------------------------------------------------
def SACCRSupervisoryDeltaAdjustment(instrument, positionQuantity, assetClass):
    return assetClassModuleMap[assetClass].SupervisoryDeltaAdjustment(instrument, positionQuantity)

#-------------------------------------------------------------------------
def SACCRAggregationValue(assetClass, hedgingSet, hedgingSubset, effectiveNotional):
    return AM.SACCRAggregationManager.CreateAggregationValue(assetClass, hedgingSet, hedgingSubset, effectiveNotional)
    
#-------------------------------------------------------------------------
def SACCRAddOnsAssetClass(effectiveNotionals):
    am = AM.SACCRAggregationManager(effectiveNotionals)
    
    assetClassAddOns = acm.FDictionary()
    
    for assetClass in list(am.AggregationDict().keys()):
        aggregatedValues = am.GetAggregatedValue(assetClass)
        assetClassAddOns[assetClass] = aggregatedValues['Add-On']
    
    return assetClassAddOns

