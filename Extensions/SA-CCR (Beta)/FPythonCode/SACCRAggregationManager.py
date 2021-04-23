
import acm

from SACCRAggregationStrategies import GetAggregationStrategy

class AggregationKeys(object):
    ASSET_CLASS         = "Asset Class"
    HEDGING_SET         = "Hedging Set"
    HEDGING_SUBSET      = "Hedging Subset"
    EFFECTIVE_NOTIONAL  = "Effective Notional"

#------------------------------------------------------------------------
# SA-CCR Aggregation Manager
#------------------------------------------------------------------------
class SACCRAggregationManager(object):
    
    @staticmethod
    def CreateAggregationValue(assetClass, hedgingSet, hedgingSubset, effectiveNotional):
        aggregationValue = acm.FDictionary()
        aggregationValue[AggregationKeys.ASSET_CLASS] = assetClass
        aggregationValue[AggregationKeys.HEDGING_SET] = hedgingSet
        aggregationValue[AggregationKeys.HEDGING_SUBSET] = hedgingSubset
        aggregationValue[AggregationKeys.EFFECTIVE_NOTIONAL] = float(effectiveNotional)
                
        return aggregationValue
    
    #-------------------------------------------------------------------------
    def __init__(self, aggregationValues):
        self._aggregationDict = {}
        self._aggregatedValuesCache = {}
        
        self._CreateAggregationDict(aggregationValues)
        self._AggregateValues()
    
    #-------------------------------------------------------------------------
    def GetAggregatedValue(self, *levels):
        if len(levels) == 0:
            levels = None
        elif len(levels) == 1:
            levels = levels[0]
                
        try:
            return self._aggregatedValuesCache[levels]
        except KeyError as e:
            msg = "Could not find aggregated value based on keys: {}".format(levels)
            raise Exception(msg)

    
    #-------------------------------------------------------------------------
    def AggregationDict(self):
        return self._aggregationDict
    
    #-------------------------------------------------------------------------
    def _AggregateValues(self):
        totalAddOn = 0.0
        
        for assetClass in self._aggregationDict.keys():
            strategy = GetAggregationStrategy(assetClass)
            self._aggregatedValuesCache.update(strategy.Run(self._aggregationDict[assetClass]))
            
            aggregatedValue = self._aggregatedValuesCache[assetClass]
            totalAddOn += aggregatedValue['Add-On']
        
        values = acm.FDictionary()
        values['Add-On'] = totalAddOn
        
        self._aggregatedValuesCache[None] = values
    
    #-------------------------------------------------------------------------
    def _CreateAggregationDict(self, aggregationValues):
        for value in aggregationValues:
            keys = [value[AggregationKeys.ASSET_CLASS], value[AggregationKeys.HEDGING_SET], value[AggregationKeys.HEDGING_SUBSET]]
            keys = [_f for _f in keys if _f]
            
            self._AddValueToAggregationDict(self._aggregationDict, value, *keys)

    #-------------------------------------------------------------------------
    def _AddValueToAggregationDict(self, aggregationDict, value, *levels):
        if len(levels) == 1:
            values = aggregationDict.setdefault(levels[0], list())
            values.append(value[AggregationKeys.EFFECTIVE_NOTIONAL])
        else:
            nextLevel = aggregationDict.setdefault(levels[0], dict())            
            self._AddValueToAggregationDict(nextLevel, value, *levels[1:])
