
import string

import acm
import RiskFactorCalculationTools

import FRunScriptGUI
from RiskFactorDimensionPopulator import RiskFactorDimensionPopulator
from RiskFactorDimensionPopulator import PopulateShiftDataRecursive
from RiskFactorDimensionPopulator import configurationForSBAMeasure
from RiskFactorDimensionPopulator import StaticArray
from RiskFactorDimensionPopulator import BaseParametersForVectorItemDimension

class AELVariables(FRunScriptGUI.AelVariablesHandler):

    def RiskFactorTypesForSetup( self, setupName ):
        setup = acm.FRiskFactorSetup[setupName]
        types = set()
        for collection in setup.RiskFactorCollections():
            types.add( collection.RiskFactorType() )
        return types
        
    def Dimensions( self, setupName, rfType ):
        dimensions = set()
        if setupName != "":
            setup = acm.FRiskFactorSetup[setupName]
            propertySpecs = setup.RiskFactorPropertySpecifications()
            for propertySpec in propertySpecs:
                addInfoSpec = propertySpec.AdditionalInfoSpec()
                if addInfoSpec.ExtendedClass() == acm.FRiskFactorInstance:
                    dimensions.add( "i." + str(addInfoSpec.MethodName()) )
                else:
                    dimensions.add( "c." + str(addInfoSpec.MethodName()) )
            for collection in setup.RiskFactorCollections():
                if collection.RiskFactorType() == rfType:
                    for dim in collection.RiskFactorDimensions():
                        dimensions.add( str(dim.DisplayName()) )
        return dimensions
        
    def OnSetupChanged( self, index, fieldvalues):
        setupName = fieldvalues[2]
        if setupName != "":
            rfTypes = self.RiskFactorTypesForSetup( setupName )
            self.ael_variables[3][3] = list(rfTypes)
        rftype = fieldvalues[3]
        if rftype != "":
            validDimensions = self.Dimensions( setupName, rftype )
            self.ael_variables[4][3] = list(validDimensions)
        return fieldvalues
        
    def __init__(self):

        vars = [
                ['shiftType', 'Shift Type', 'string', ['Relative', 'Absolute'], None, 1, 0, '', None],
                ['shiftUnit', 'Shift Unut', 'string', acm.GetDomain('enum(RiskFactorValueUnit)').EnumeratorStringsSkipFirst(), None, 1, 0, '', None],
                ['shiftSize', 'Shift Size', 'float', None, 1.0, 1, 0, '', None],
                ['scaleFactor', 'Scale Factor', 'float', None, 1.0, 1, 0, '', None],
                ['rfsetup', 'Risk Factor Setup', 'string', acm.FRiskFactorSetup.Select(""), None, 1, 0, '', self.OnSetupChanged],
                ['riskFactorType', 'Risk Factor Type', 'string', [], None, 1, 0, '', self.OnSetupChanged],
                ['dimensions', 'Dimensions', 'string', [], None, 1, 1, '', None]
               ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)

ael_variables = AELVariables()

class Populator(RiskFactorDimensionPopulator):

    def __init__(self, rfColls, dimensionInformation, isVectorItem, riskFactorType, shiftSize, shiftType, shiftUnit, scaleFactor):
        self.m_riskFactorType = riskFactorType
        self.m_shiftSize = shiftSize
        self.m_shiftType = shiftType
        self.m_shiftUnit = shiftUnit
        self.m_scaleFactor = scaleFactor
        RiskFactorDimensionPopulator.__init__( self, rfColls, dimensionInformation, isVectorItem )

    def ShiftShape( self ):
        if self.m_riskFactorType in ['Zero Coupon']:
            return acm.Valuation().MappedValuationParameters().Parameter().IrShiftType()
        elif self.m_riskFactorType in ['Volatility', 'Benchmark Volatility']:
            return acm.Valuation().MappedValuationParameters().Parameter().VolShiftType()
        return 'Triangle'

    def ShiftType( self ):
        return self.m_shiftType

    def ShiftDivisor( self, shiftSize ):
        return self.m_scaleFactor

    def PerimeterInformation( self ):
        return None, None

    def ShiftSize( self ):
        shiftSize = self.m_shiftSize
        if self.m_shiftUnit == 'Basis Point':
            shiftSize *= 0.0001
        elif self.m_shiftUnit == 'Percent':
            shiftSize *= 0.01
        return shiftSize * self.m_scaleFactor

    def SetPath( self, dimensionInformation, item ):
        pass
    
def OrderedDimensionInformations( riskFactorCollections, dimensions ):
    vDims = []
    
    dimensionInformations = []
    for dimension in dimensions:
        cc = string.split( dimension, "." )
        if len(cc) > 1:
            if cc[0] == 'c':
                dimInfo = RiskFactorCalculationTools.DimensionInformation(cc[1], False, cc[1], False)
            elif cc[0] == 'i':
                dimInfo = RiskFactorCalculationTools.DimensionInformation(cc[1], True, cc[1], False)
            dimensionInformations.append( (dimInfo, True) )
        else:
            fDimension = riskFactorCollections[0].RiskFactorDimension( dimension )
            dimensionID = RiskFactorCalculationTools.DimensionIdFromDimension( fDimension )
            dimInfo = RiskFactorCalculationTools.DimensionInformation(dimensionID, False, None, False)
            if acm.RiskFactor.DimensionUsesVectorItemImplementation( fDimension ):
                dimensionInformations.append( (dimInfo, True) )
            else:
                vDims.append( (dimInfo, False) )
    dimensionInformations.extend( vDims )
    return dimensionInformations

def CollectionIsValid( riskFactorCollection, riskFactorType ):
    if riskFactorCollection.RiskFactorType() == riskFactorType:
        return True
    return False

def RiskFactorCollections( parameters ):
    return [rfColl for rfColl in acm.FRiskFactorSetup[parameters.At('rfsetup')].RiskFactorCollections() if CollectionIsValid( rfColl, parameters.At("riskFactorType"))]
    
def ael_main_ex(parameters, apa):
    dims = []
    context = acm.ExtensionTools().GetDefaultContext()
    parametersAsACMDict = acm.FDictionary()
    parametersAsACMDict.AddAll( parameters )

    riskFactorCollections = RiskFactorCollections( parametersAsACMDict )
    if len( riskFactorCollections ) == 0:
        return dims

    orderedDimensionInformations = OrderedDimensionInformations( riskFactorCollections, parametersAsACMDict.At('dimensions') )
    dependentsOn = []
    vCount = 0
    
    riskFactorInstances = []
    for riskFactorCollection in riskFactorCollections:
        riskFactorInstances.extend( riskFactorCollection.RiskFactorInstances() )

    for dimensionInformation, isVectorItem in orderedDimensionInformations:
        config = None
        if isVectorItem:
            dependentsOn.append( dimensionInformation )

        shiftData = acm.FPathDependentVectorShiftData( [d.m_id for d in dependentsOn] )
        populator = Populator( riskFactorCollections, dimensionInformation, isVectorItem, parametersAsACMDict.At('riskFactorType'), parametersAsACMDict.At('shiftSize'), parametersAsACMDict.At('shiftType'), parametersAsACMDict.At('shiftUnit'), parametersAsACMDict.At('scaleFactor'))
        PopulateShiftDataRecursive( populator, riskFactorInstances, dependentsOn, [], [], shiftData )

        if isVectorItem:
            dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'Risk Factor Targets').Value()
                
            extParams = BaseParametersForVectorItemDimension( populator )
            extParams[acm.FSymbol("RiskFactorCollections")] = riskFactorCollections
            extParams[acm.FSymbol("RiskFactorDimension")] = dimensionInformation.AsDictionary()
            extParams[acm.FSymbol("RiskFactorPathKeys")] = StaticArray( [dimInfo.AsDictionary() for dimInfo in dependentsOn[:-1][::-1]] )
            
            config = acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues(extParams, None )
        else:
            dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'Risk Factor Dimension ' + str(vCount)).Value()
            vCount += 1

        dim = acm.Risk().CreateVectorDimension( dimensionInformation.m_id, dimDef, shiftData, config, configurationForSBAMeasure, [d.m_id for d in dependentsOn] )
        dims.append( dim )
    return dims

def ael_dimension_ids( parameters, unused ):
    dimIds = []
    parametersAsACMDict = acm.FDictionary()
    parametersAsACMDict.AddAll( parameters )
    riskFactorCollections = RiskFactorCollections( parametersAsACMDict )
    if len( riskFactorCollections ) == 0:
        return dimIds

    orderedDimensionInformations = OrderedDimensionInformations( riskFactorCollections, parametersAsACMDict.At('dimensions') )

    for dimensionInformation, _ in orderedDimensionInformations:
        dimIds.append( dimensionInformation.m_id )
    return dimIds

def ael_coordinates_source( parameters, dictExtra ):
    dimensionIdToMatch = acm.FSymbol( dictExtra.At('customData').ExtensionObject() )
    parametersAsACMDict = acm.FDictionary()
    parametersAsACMDict.AddAll( parameters )
    riskFactorCollections = RiskFactorCollections( parametersAsACMDict )
    if len( riskFactorCollections ) == 0:
        return None
           
    for riskFactorCollection in riskFactorCollections:
        for dimension in riskFactorCollection.RiskFactorDimensions():
            if RiskFactorCalculationTools.DimensionIdFromDimension( dimension ) == dimensionIdToMatch:
                source = dimension.CoordinatesSource()
                if source and source.IsKindOf(acm.FStoredTimeBuckets):
                    return source.TimeBuckets()
                return source
    return None
