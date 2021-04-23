


import acm
import RiskFactorUtils

class TimeBucketMap( object ):

    def __init__( self, riskFactorCollection ):
        self.m_timeBucketDataBySpec = {}
        self.m_timeBucketDataByName = {}
        
        for dim in riskFactorCollection.RiskFactorDimensions():
            timeBuckets = GetTimeBucketsFromDimensionIfApplicable( dim )
            
            if timeBuckets:
                self.MapTimeBuckets( dim.UniqueId(), timeBuckets )
    
    def TimeBucketNameFromSpec( self, uniqueId, spec ):
        try:
            return self.m_timeBucketDataBySpec[uniqueId][spec][0]
        except KeyError as e:
            return None
            
    def TimeBucketIndexFromSpec( self, uniqueId, spec ):
        try:
            return self.m_timeBucketDataBySpec[uniqueId][spec][1]
        except KeyError as e:
            return None

    def TimeBucketIndexFromName( self, uniqueId, name ):
        try:
            return self.m_timeBucketDataByName[uniqueId][name][1]
        except KeyError as e:
            return None
    
    def MapTimeBuckets( self, uniqueId, timeBuckets ):
        self.m_timeBucketDataBySpec[uniqueId] = {}
        self.m_timeBucketDataByName[uniqueId] = {}
        
        for sortingIdx, timeBucket in enumerate( timeBuckets ):
            self.m_timeBucketDataBySpec[uniqueId][timeBucket.Spec()] = ( timeBucket.Name(), sortingIdx )
            self.m_timeBucketDataByName[uniqueId][timeBucket.Name()] = ( timeBucket.Spec(), sortingIdx )

def GetCoordinateDisplayValue( timeBucketMap, uniqueId, coordinate ):
    timeBucketDisplayName = timeBucketMap.TimeBucketNameFromSpec( uniqueId, coordinate )
    return timeBucketDisplayName if timeBucketDisplayName else coordinate

def IsTimeBucketDomain( dimension ):
    domain = RiskFactorUtils.GetDimensionDomain( dimension )
    return acm.FTimeBucket == domain

def GetTimeBucketsFromDimensionIfApplicable(dimension) :
    storedTimeBucket = dimension.CoordinatesSource()
    items = []

    if storedTimeBucket and storedTimeBucket.IsKindOf( acm.FStoredTimeBuckets ):
        timeBuckets = storedTimeBucket.TimeBuckets()

        if timeBuckets:
            for timeBucket in timeBuckets:
                items.append( timeBucket )
    
    return items

def GetIndexByTimeBuckets(items) :
    indexByTimeBuckets = {}

    if items:
        for index, item in enumerate(items) :
            indexByTimeBuckets[item.StringKey()] = index

    return indexByTimeBuckets
    
