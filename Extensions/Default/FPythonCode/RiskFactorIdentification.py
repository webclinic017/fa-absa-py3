
import itertools

import acm

from RiskFactorTransform import RiskFactorTransform
from RiskFactorDimensionCoordinate import GetRiskFactorCoordinateCalculation as GetCoordCalc

#------------------------------------------------------------------------------
# RiskFactorIdentifier
#------------------------------------------------------------------------------
class RiskFactorIdentifier( object ):

    #------------------------------------------------------------------------------
    def __init__( self, columnId = 'Risk Factors In Theoretical Value' ):
        self.m_calcSpace = acm.Calculations().CreateCalculationSpaceCollection().GetSpace( acm.FPortfolioSheet, acm.GetDefaultContext() )
        self.m_columnId = columnId
        self.m_coordCalcByDimension = {}
        
        self.m_generatedRiskFactors = set()
    
    #------------------------------------------------------------------------------
    def DetectRiskFactors( self, riskFactorCollection, objects ):
        detectedRiskFactors = []
        
        for obj in objects:
            snoopedRiskFactors = self._SnoopedRiskFactors( riskFactorCollection, obj )

            for riskFactor in snoopedRiskFactors:
                try:
                    coordinatesPerDimension = self._CoordinatesPerDimensions( riskFactor, riskFactorCollection )
                    riskFactors = [dict(p) for p in itertools.product( *coordinatesPerDimension ) ]
                    
                    for riskFactor in riskFactors:
                        if self._UniqueRiskFactor( riskFactor ):
                            detectedRiskFactors.append( riskFactor )
                    
                except Exception, e:
                    pass

        self.m_generatedRiskFactors.clear()

        return detectedRiskFactors
    
    #------------------------------------------------------------------------------
    def _SnoopedRiskFactors( self, riskFactorCollection, obj ):
        params = {'RiskFactorCollection' : riskFactorCollection}
        config = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues( params )
        
        return self.m_calcSpace.CalculateValue( obj, self.m_columnId, config )
        
    #------------------------------------------------------------------------------
    def _CoordinatesPerDimensions( self, value, riskFactorCollection ):
        coordinates = []
    
        riskFactorTransform = RiskFactorTransform( riskFactorCollection, value )
    
        for dim in riskFactorCollection.RiskFactorDimensions():
            transformedObject = riskFactorTransform.TransformedObjectForDimension( dim )
            
            if dim not in self.m_coordCalcByDimension:
                self.m_coordCalcByDimension[dim] = GetCoordCalc( dim )
            
            coords = self.m_coordCalcByDimension[dim].Coordinate( transformedObject )
            self._ValidateCoordinates( coords )
            
            coordinates.append( coords )
        
        return coordinates
    
    #------------------------------------------------------------------------------
    def _UniqueRiskFactor( self, riskFactor ):
        key = '-'.join( [coordinate for _, coordinate in riskFactor.iteritems()] )
        
        if key not in self.m_generatedRiskFactors:
            self.m_generatedRiskFactors.add( key )
            return True
        else:
            return False
    
    #------------------------------------------------------------------------------
    def _ValidateCoordinates( self, coordinates ):
        incompleteCoordinates = any(not coordinate for _, coordinate in coordinates)
        
        if incompleteCoordinates:
            raise Exception( "Incomplete risk factor coordinates: {}".format( coordinates ) )
    
