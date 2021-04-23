
import acm
import SACCRParameters
import SACCRTools

from SACCREnums import MaturityBuckets, AssetClass

#-------------------------------------------------------------------------
def AggregatedValues(effectiveNotional, addOn):
    values = acm.FDictionary()
    values['Effective Notional'] = effectiveNotional
    values['Add-On'] = addOn
    return values

#-------------------------------------------------------------------------
# Get Aggregation Strategy
#-------------------------------------------------------------------------
def GetAggregationStrategy(assetClass):
    if AssetClass.COMMODITY == assetClass:
        return CommodityAggregation()
    elif AssetClass.CREDIT == assetClass:
        return CreditAggregation()
    elif AssetClass.EQUITY == assetClass:
        return EquityAggregation()
    elif AssetClass.FX == assetClass:
        return FXAggregation()
    else:
        return InterestRatesAggregation()

#-------------------------------------------------------------------------
# SA-CCCR Aggregation Strategies
#-------------------------------------------------------------------------
class SACCRAggregationStrategy(object):
    
    def __init__(self):
        self._aggregatedValues = {}
    
    def Run(self, values):
        pass

#-------------------------------------------------------------------------
# FX Aggregation Strategy
#-------------------------------------------------------------------------
class FXAggregation(SACCRAggregationStrategy):
    
    def Run(self, values):
        addOn = sum(self._AggregateHedgingSet(hedgingSet, effectiveNotionals) \
                    for hedgingSet, effectiveNotionals in values.items())

        self._aggregatedValues[AssetClass.FX] = AggregatedValues(None, addOn)
        return self._aggregatedValues
    
    #-------------------------------------------------------------------------
    def _AggregateHedgingSet(self, hedgingSet, values):
        effectiveNotional = sum(values)
        
        supervisoryFactor = SACCRParameters.GetSupervisoryFactor(AssetClass.FX)
        addOn = supervisoryFactor * acm.Math.Abs(effectiveNotional)
        
        self._aggregatedValues[(AssetClass.FX, hedgingSet)] = AggregatedValues(effectiveNotional, addOn)
        
        return addOn

#-------------------------------------------------------------------------
# Equity Aggregation Strategy
#-------------------------------------------------------------------------
class EquityAggregation(SACCRAggregationStrategy):

    def Run(self, values):
        systematicAddOn, idiosyncraticAddOn = 0.0, 0.0
        
        for hedgingSubset, effectiveNotionals in values.items():
            subclass = SACCRTools.SACCRSubclass(hedgingSubset, AssetClass.EQUITY)
            
            addOn = self._AggregateHedgingSubset(hedgingSubset, subclass, effectiveNotionals)
            correlation = SACCRParameters.GetCorrelation(AssetClass.EQUITY, subclass)
            
            systematicAddOn += correlation * addOn
            idiosyncraticAddOn += (1 - correlation * correlation) * addOn * addOn
            
        assetClassAddOn = acm.Math.Sqrt(systematicAddOn * systematicAddOn + idiosyncraticAddOn)
        self._aggregatedValues[AssetClass.EQUITY] = AggregatedValues(None, assetClassAddOn)
        
        return self._aggregatedValues
        
    #-------------------------------------------------------------------------
    def _AggregateHedgingSubset(self, hedgingSubset, subclass, values):
        effectiveNotional = sum(values)
        
        supervisoryFactor = SACCRParameters.GetSupervisoryFactor(AssetClass.EQUITY, subclass)
        addOn = supervisoryFactor * effectiveNotional
        
        self._aggregatedValues[(AssetClass.EQUITY, hedgingSubset)] = AggregatedValues(effectiveNotional, addOn)
        
        return addOn
        
#-------------------------------------------------------------------------
# Credit Aggregation Strategy
#-------------------------------------------------------------------------
class CreditAggregation(SACCRAggregationStrategy):

    def Run(self, values):
        systematicAddOn, idiosyncraticAddOn = 0.0, 0.0
        
        for hedgingSubset, effectiveNotionals in values.items():
            subclass = SACCRTools.SACCRSubclass(hedgingSubset, AssetClass.CREDIT)
        
            addOn = self._AggregateHedgingSubset(hedgingSubset, subclass, effectiveNotionals)
            correlation = SACCRParameters.GetCorrelation(AssetClass.CREDIT, subclass)
            
            systematicAddOn += correlation * addOn
            idiosyncraticAddOn += (1 - correlation * correlation) * addOn * addOn
            
        assetClassAddOn = acm.Math.Sqrt(systematicAddOn * systematicAddOn + idiosyncraticAddOn)
        self._aggregatedValues[AssetClass.CREDIT] = AggregatedValues(None, assetClassAddOn)
        
        return self._aggregatedValues
        
    #-------------------------------------------------------------------------
    def _AggregateHedgingSubset(self, hedgingSubset, subclass, values):
        effectiveNotional = sum(values)
        
        supervisoryFactor = SACCRParameters.GetSupervisoryFactor(AssetClass.CREDIT, subclass)
        addOn = supervisoryFactor * effectiveNotional
        
        self._aggregatedValues[(AssetClass.CREDIT, hedgingSubset)] = AggregatedValues(effectiveNotional, addOn)
        
        return addOn

#-------------------------------------------------------------------------
# Interest Rates Aggregation Strategy
#-------------------------------------------------------------------------
class InterestRatesAggregation(SACCRAggregationStrategy):
    
    def Run(self, values):
        addOn = sum(self._AggregateHedgingSet(hedgingSet, maturityBuckets) \
                     for hedgingSet, maturityBuckets in values.items())

        self._aggregatedValues[AssetClass.INTEREST_RATES] = AggregatedValues(None, addOn)
        
        return self._aggregatedValues

    #-------------------------------------------------------------------------
    def _AggregateHedgingSet(self, hedgingSet, maturityBuckets):
        effectiveNotional = self._AggregateMaturityBuckets(hedgingSet, maturityBuckets)
        
        supervisoryFactor = SACCRParameters.GetSupervisoryFactor(AssetClass.INTEREST_RATES)
        addOn = supervisoryFactor * effectiveNotional
        
        self._aggregatedValues[(AssetClass.INTEREST_RATES, hedgingSet)] = AggregatedValues(effectiveNotional, addOn)
        
        return addOn
        
    #-------------------------------------------------------------------------
    def _AggregateMaturityBuckets(self, hedgingSet, maturityBuckets):
        d1 = self._AggregateMaturityBucket(hedgingSet, maturityBuckets, MaturityBuckets.LESS_ONE_YEAR)
        d2 = self._AggregateMaturityBucket(hedgingSet, maturityBuckets, MaturityBuckets.ONE_FIVE_YEARS)
        d3 = self._AggregateMaturityBucket(hedgingSet, maturityBuckets, MaturityBuckets.OVER_FIVE_YEARS)
        
        return acm.Math.Sqrt(d1 * d1 + d2 * d2 + d3 * d3 + 1.4 *d1 * d2 + 1.4 * d2 * d3 + 0.6 * d1 * d3)
    
    #-------------------------------------------------------------------------
    def _AggregateMaturityBucket(self, hedgingSet, maturityBuckets, bucket):
        values = maturityBuckets.get(bucket, [])
        effectiveNotional = sum(values)
        
        self._aggregatedValues[(AssetClass.INTEREST_RATES, hedgingSet, bucket)] = AggregatedValues(effectiveNotional, None)
        
        return effectiveNotional
        
#-------------------------------------------------------------------------
# Commodity Aggregation Strategy
#-------------------------------------------------------------------------
class CommodityAggregation(SACCRAggregationStrategy):
    
    def Run(self, values):
        addOn = sum(self._AggregateHedgingSet(hedgingSet, commodityTypes) \
                     for hedgingSet, commodityTypes in values.items())

        self._aggregatedValues[AssetClass.COMMODITY] = AggregatedValues(None, addOn)
        
        return self._aggregatedValues
        
    #-------------------------------------------------------------------------
    def _AggregateHedgingSet(self, hedgingSet, commodityTypes):
        systematicAddOn, idiosyncraticAddOn = 0.0, 0.0
        
        for commodityType, effectiveNotionals in commodityTypes.items():
            subclass = SACCRTools.SACCRSubclass(commodityType, AssetClass.COMMODITY)
            
            addOn = self._AggregateCommodityType(hedgingSet, commodityType, subclass, effectiveNotionals)
            correlation = SACCRParameters.GetCorrelation(AssetClass.COMMODITY, subclass)
            
            systematicAddOn += correlation * addOn
            idiosyncraticAddOn += (1 - correlation * correlation) * addOn * addOn
            
        hedgingSetAddOn = acm.Math.Sqrt(systematicAddOn * systematicAddOn + idiosyncraticAddOn)
        self._aggregatedValues[(AssetClass.COMMODITY, hedgingSet)] = AggregatedValues(None, hedgingSetAddOn)
        
        return hedgingSetAddOn

    #-------------------------------------------------------------------------
    def _AggregateCommodityType(self, hedgingSet, commodityType, subclass, values):
        effectiveNotional = sum(values)
        
        supervisoryFactor = SACCRParameters.GetSupervisoryFactor(AssetClass.COMMODITY, subclass)
        
        addOn = supervisoryFactor * effectiveNotional
        
        self._aggregatedValues[(AssetClass.COMMODITY, hedgingSet, commodityType)] = AggregatedValues(effectiveNotional, addOn)
        
        return addOn
