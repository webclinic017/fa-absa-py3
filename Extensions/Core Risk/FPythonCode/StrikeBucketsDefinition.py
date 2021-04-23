
import acm

class StrikeBucketsDefinition:
    
    def __init__( self ):
        self.m_definitions = []
        
    def AddDefinition( self, definition ):
        self.m_definitions.append( definition )
    
    def GenerateStrikeBucketsImpl( self, start, end ):
        buckets = []
        for idx, bucketDef in enumerate( self.m_definitions ):
            actEnd = end
            if idx <= len( self.m_definitions ) - 2:
                nextBucketDef = self.m_definitions[ idx + 1 ]
                actEnd = nextBucketDef.Point()
            bucket = acm.FStrikeBucket()
            bucket.StrikeType( bucketDef.StrikeType() )
            bucket.StrikeStart( start )
            bucket.StrikeMid( bucketDef.Point() )
            bucket.StrikeEnd( actEnd )
            bucket.Name( bucketDef.Name() )
            buckets.append( bucket )
            start = bucketDef.Point()
        return buckets       
    
    def GenerateStrikeBuckets( self ):
        self.m_definitions.sort( key = lambda StrikeBucketDefinition: StrikeBucketDefinition.Point() )
        return self.GenerateStrikeBucketsImpl( -float("inf"), float("inf") )

class DeltaStrikeBucketsDefinition( StrikeBucketsDefinition ):
    
    def GenerateStrikeBuckets( self ):
        return self.GenerateStrikeBucketsImpl( -0.00000001, 0.00000001 )


class StrikeBucketDefinition:
    
    def __init__( self, strikeType, point, name ):
        self.m_strikeType = strikeType
        self.m_point = point
        self.m_name = name
    
    def StrikeType(self):
        return self.m_strikeType
        
    def Point( self ):
        return self.m_point

    def Name( self ):
        return self.m_name


class ATMDeltaStrikeBucketDefinition(StrikeBucketDefinition):

    def __init__( self, name ):
        self.m_strikeType = 'Delta'
        self.m_point = 0.0
        self.m_name = name    
