
import acm
import math
from StrikeBucketsDefinition import StrikeBucketsDefinition
from StrikeBucketsDefinition import DeltaStrikeBucketsDefinition
from StrikeBucketsDefinition import StrikeBucketDefinition
from StrikeBucketsDefinition import ATMDeltaStrikeBucketDefinition

DEFAULT_MAX_COUNT = 10

def GenerateMALZDeltaStrikeBuckets( malzStructure, params ):
    bucketsDef = DeltaStrikeBucketsDefinition()
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Delta', -0.01, "1P" ) )
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Delta', -0.1, "10P") )
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Delta', -0.25, "25P" ) )
    bucketsDef.AddDefinition( ATMDeltaStrikeBucketDefinition( "ATM" ) )
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Delta', 0.25, "25C" ) )
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Delta', 0.1, "10C" ) )
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Delta', 0.01, "1C" ) )
    return bucketsDef.GenerateStrikeBuckets()
    
def GenerateEQParametricStrikeBuckets( eqParamStructure, params ):
    bucketsDef = StrikeBucketsDefinition()
    bucketsDef.AddDefinition( StrikeBucketDefinition( 'Rel Frw', 0, "ATM" ) )
    return bucketsDef.GenerateStrikeBuckets()  
    
def GenerateStrikeBucketsFromVolatilityStructure( volStructure, params ):
    maxCount = params and params['maxCount'] or DEFAULT_MAX_COUNT
    pointStrikes = set()
    for p in volStructure.Points():
        if p.Benchmark() and p.Benchmark().StoredStrikeType() == volStructure.StrikeType():
            pointStrikes.add( p.Benchmark().StrikePrice() )
        else:
            pointStrikes.add( p.Strike() )

    points = sorted( list(pointStrikes) )
    if len(points) > maxCount:
        denominator = math.ceil( (len(points))/float(maxCount))
        count = math.ceil( (len(points)) / float( denominator ) )
        points = [points[ n * int(denominator) ] for n in range(int(count)) ]
    bucketsDef = StrikeBucketsDefinition()
    for p in points:
        name = volStructure.StrikeType() != 'Absolute' and volStructure.StrikeType() + " " + str(p) or str(p)
        bucketsDef.AddDefinition( StrikeBucketDefinition( volStructure.StrikeType(), p, name ) )
    return bucketsDef.GenerateStrikeBuckets()
    
    
def GenerateStrikeBuckets( volSurface, params ):
    if volSurface.StructureType() == 'Malz':
        return GenerateMALZDeltaStrikeBuckets( volSurface, params )
    elif volSurface.IsEqParametricStructure():
        return GenerateEQParametricStrikeBuckets( volSurface, params )
    else:
        return GenerateStrikeBucketsFromVolatilityStructure( volSurface, params )
