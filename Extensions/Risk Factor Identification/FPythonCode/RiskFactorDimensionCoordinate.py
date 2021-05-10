
import acm

import RiskFactorTimeBuckets
import RiskFactorIdentificationTools

#------------------------------------------------------------------------------
def GetRiskFactorCoordinateCalculation( dim ):
    riskFactorType = acm.RiskFactor().RiskFactorType( dim.RiskFactorCollection().RiskFactorType() )

    if "FX" == riskFactorType.StringKey():
        return FXDimensionCoordinate( dim )
    
    elif not acm.RiskFactor().DimensionUsesVectorItemImplementation( dim ):
        return ConfigDimensionCoordinate( dim )
        
    else:
        return MethodChainDimensionCoordinate( dim )

#------------------------------------------------------------------------------
# RiskFactorDimensionCoordinate
#------------------------------------------------------------------------------
class RiskFactorDimensionCoordinate( object ):

    #------------------------------------------------------------------------------
    def Coordinate( self, obj ):
        raise NotImplementedError("Method Coordinate is not implemented.")

#------------------------------------------------------------------------------
class MethodChainDimensionCoordinate( RiskFactorDimensionCoordinate ):

    #------------------------------------------------------------------------------
    def __init__( self, dim ):
        self.m_dim = dim
        self.m_methodChain = RiskFactorIdentificationTools.MethodChainFromDimension( dim )
        
    #------------------------------------------------------------------------------
    def Coordinate( self, obj ):
        if hasattr(obj, '__iter__'):
            coordinates = [ self.m_methodChain.Call( [item] ) for item in obj ]
        else:
            coordinates = [ self.m_methodChain.Call( [obj] ) ]
        return DimensionCoordinates( self.m_dim.UniqueId(), coordinates )
    
#------------------------------------------------------------------------------
class ConfigDimensionCoordinate( RiskFactorDimensionCoordinate ):

    #------------------------------------------------------------------------------
    def __init__( self, dim ):
        self.m_dim = dim
        self.m_coordinates = None
        
        self._CoordinateSource()
    
    #------------------------------------------------------------------------------
    def Coordinate( self, obj ):
        return DimensionCoordinates( self.m_dim.UniqueId(), self.m_coordinates )
        
    #------------------------------------------------------------------------------
    def _CoordinateSource( self ):
        riskFactorType = acm.RiskFactor().RiskFactorType( self.m_dim.RiskFactorCollection().RiskFactorType() )
        dimensionData = riskFactorType.DimensionData()
        
        domain = dimensionData[self.m_dim.DimensionId()]["Domain"]
        
        if acm.FTimeBucket == domain:
            timeBuckets = RiskFactorTimeBuckets.GetTimeBucketsFromDimensionIfApplicable( self.m_dim )
            coordinates = [tb.Spec() for tb in timeBuckets]
        
        elif acm.FStrikeBucket == domain:
            storedStrikeBuckets = self.m_dim.CoordinatesSource()
            strikeBuckets = acm.Risk.CreateStrikeBuckets( storedStrikeBuckets.StrikeBucketsDefinition() )
            
            coordinates = [sb.Name() for sb in strikeBuckets]
            
        elif domain.IsEnum():
            coordinates = [enum for enum in acm.FEnumeration[domain.StringKey()].Enumerators() if enum != 'None']
            
        else:
            coordinates = [item.StringKey() for item in domain.Select("")]
            
        self.m_coordinates = coordinates
        
#------------------------------------------------------------------------------
class FXDimensionCoordinate( RiskFactorDimensionCoordinate ):

    def __init__( self, dim ):
        self.m_dim = dim
    
    #------------------------------------------------------------------------------
    def Coordinate( self, obj ):
        dimensionId = self.m_dim.DimensionId()
        
        if dimensionId in ['TermCurrency', 'BaseCurrency']:
            return DimensionCoordinates( self.m_dim.UniqueId(), obj[dimensionId].StringKey() )
        else:
            return DimensionCoordinates( self.m_dim.UniqueId(), "" )
        
#------------------------------------------------------------------------------
# Utils
#------------------------------------------------------------------------------
def DimensionCoordinates( dimName, coordinates ):
    coordinates = coordinates if hasattr(coordinates, '__iter__') else [coordinates]
    return [(dimName, coordinate) for coordinate in coordinates]
