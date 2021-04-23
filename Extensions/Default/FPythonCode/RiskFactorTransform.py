
import acm
import RiskFactorDimensionCoordinate

#------------------------------------------------------------------------------
# RiskFactorTransform
#------------------------------------------------------------------------------
class RiskFactorTransform( object ):
    
    #------------------------------------------------------------------------------
    def __init__( self, riskFactorCollection, riskFactor ):
        self.m_riskFactorType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
        
        self.m_riskFactor = riskFactor
        
        self.m_transformedByDimensionId = {}
        
        if self.m_riskFactorType.ParameterTransform():
            self._TransformRiskFactor( riskFactorCollection.RiskFactorDimensions() )
    
    #------------------------------------------------------------------------------
    def TransformedObjectForDimension( self, dim ):
        if self.m_riskFactorType.ParameterTransform():
            if dim.DimensionId() in self.m_transformedByDimensionId:
                return self.m_transformedByDimensionId[ dim.DimensionId() ]
            return None
        else:
            return self.m_riskFactor
 
    #------------------------------------------------------------------------------
    def _TransformRiskFactor( self, dims ):
        riskFactorTransform  = acm.GetClass( self.m_riskFactorType.ParameterTransform() )()
        
        dimensionIdSet = set()
        for dim in dims:
            if dim.DimensionId() in dimensionIdSet:
                continue

            coordinate = riskFactorTransform.GetCoordinate( dim.DimensionId(), self.m_riskFactor )
            #self._ValidateDomain( dim, coordinate )
            self.m_transformedByDimensionId[ dim.DimensionId() ] = coordinate
        
    #------------------------------------------------------------------------------
    def _ValidateDomain( self, dim, transformedObject ):
        dimData = self.m_riskFactorType.DimensionData().At( dim.DimensionId() )
        domain = dimData["Domain"]
        
        if not transformedObject:
            raise Exception( "Could not transform risk factor for dimension {}.".format( dim.DisplayName() ) )
    
        if not transformedObject.IsKindOf( domain ):
            raise Exception( "{} is not of domain {}.".format( transformedObject.StringKey(), domain.StringKey() ) )
