
import acm
import RiskFactorCalculationTools

def configurationForSBAMeasure( path ):
    params = {}
    params[ acm.FSymbol("RiskFactorPathValues") ] = StaticArray( list(path)[::-1] )
    config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(params, None )
    return config
    
def BaseParametersForVectorItemDimension( populator ):
    extParams = {}
    if populator.ShiftType() == "Absolute":
        extParams[ acm.FSymbol("RiskFactorTopOnlyOverride") ] = False
    return extParams
    
def StaticDictionary( dictionary ):
    return acm.FStaticDictionary( dictionary )

def StaticArray( arr ):
    return acm.FStaticArray( arr )
    

class RiskFactorDimensionPopulator(object):

    def __init__( self, rfColls, dimensionInformation, isVectorItem ):
        
        self.m_isVectorItem = isVectorItem
        self.m_dimensionInformation = dimensionInformation
        self.m_commonParams = { RiskFactorCalculationTools.s_riskFactorCollectionSym : rfColls,
                                RiskFactorCalculationTools.s_shiftShapeSym : acm.FSymbol( self.ShiftShape() )
                              }
        
        pe, pc = self.PerimeterInformation()
        
        if pe:
            self.m_commonParams[RiskFactorCalculationTools.s_perimeter] = pe
            self.m_commonParams[RiskFactorCalculationTools.s_perimeterCriteria] = pc

    def ShiftShape( self ):
        assert( 0 )

    def ShiftType( self ):
        assert( 0 )

    def ShiftDivisor( self, shiftSize ):
        assert( 0 )

    def PerimeterInformation( self ):
        assert( 0 )

    def ShiftSize( self ):
        assert( 0 )

    def ShiftSizeAndDivisor( self ):
        shiftSize = self.ShiftSize()
        return ( shiftSize, self.ShiftDivisor( shiftSize ) )

    def PopulateCommon( self ):
        shiftDict = dict( self.m_commonParams )
        shiftSize, shiftDivisor = self.ShiftSizeAndDivisor( )
        if shiftSize:
            shiftDict[RiskFactorCalculationTools.s_shiftSizeSym] = shiftSize
        if shiftDivisor:
            shiftDict[RiskFactorCalculationTools.s_shiftDivisorSym] = shiftDivisor
        shiftDict[ RiskFactorCalculationTools.s_shiftTypeSym] = acm.FSymbol( self.ShiftType() )
        return shiftDict
        
    def Populate(self, path, dimensions, instances, shiftDataTarget):
        points = [self.m_dimensionInformation.InstanceValue( instance ) for instance in instances]
        shifts = []
        labels = []
        pSet = set()
        for point in points:
            if not point in pSet:
                pSet.add( point )
                labels.append(point)
                self.SetPath( self.m_dimensionInformation, point )
                shiftDict = self.PopulateCommon()
                shiftDict[ RiskFactorCalculationTools.s_riskFactorPathValues ] = StaticArray( path[::-1] )
                shiftDict[ RiskFactorCalculationTools.s_riskFactorPathKeys ] = StaticArray( dimensions[::-1] )
                
                if str(self.ShiftType()) == "Absolute":
                    shiftDict[ RiskFactorCalculationTools.s_topOnlyExtensionGroup ] = False
                
                if not self.IsVectorItemPopulator():
                    shiftDict[self.m_dimensionInformation.m_id] = acm.FSymbol( point )
                    shifts.append( [StaticDictionary( shiftDict )] )
                else:
                    shifts.append( StaticDictionary( shiftDict ) )
                    
        shiftDataTarget.AddShiftVector( [acm.FSymbol(i) for i in path], shifts, labels )

    def IsVectorItemPopulator( self ):
        return self.m_isVectorItem

    def SetPath( self, dimensionInformation, item ):
        assert( 0 )


def PopulateShiftDataRecursive( populator, instances, dependentsOn, dimensions, path, shiftData ):
    if len(dependentsOn) == 0:
        populator.Populate( path, dimensions, instances, shiftData )
    else:
        depDim = dependentsOn[0]
        nextDimensions = list(dimensions)
        nextDimensions.append( depDim.AsDictionary() )
        depDimItems = RiskFactorCalculationTools.FilteredInstancesByItemId( depDim, instances )
        for item in depDimItems.keys():
            populator.SetPath( depDim, item )
            newPath = list(path)
            newPath.append( item )
            PopulateShiftDataRecursive( populator, depDimItems[item], dependentsOn[1:], nextDimensions, newPath, shiftData )

