import acm
import FRTBSATools
import FRTBSAHierarchy
import RiskFactorCalculationTools

from RiskFactorDimensionPopulator import RiskFactorDimensionPopulator
from RiskFactorDimensionPopulator import PopulateShiftDataRecursive
from RiskFactorDimensionPopulator import configurationForSBAMeasure
from RiskFactorDimensionPopulator import StaticArray
from RiskFactorDimensionPopulator import BaseParametersForVectorItemDimension


ael_variables = [
['riskClass', 'Risk Class', 'string', acm.FEnumeration['enum(cl_FRTB_SA_Risk_Class)'].Enumerators(), None, 1, 0, '', None],
['measureType', 'Measure Type', 'string', acm.FEnumeration['EnumFRTBMeasureType'].Enumerators(), None, 1, 0, '', None],
['rfsetup', 'Risk Factor Setup', 'string', acm.FRiskFactorSetup.Select(""), None, 1, 0, '', None],
['hierarchy', 'Hierarchy', 'string', acm.FHierarchy.Select(''), None, 1, 0, '', None],
['positionExpiryTimeBuckets', 'Position Expiry Time Buckets', acm.FStoredTimeBuckets, None, None, 1, 0, '', None]
]


def MeasureTypeIsCurvature( measureType ):
    return measureType in ['Curvature Up', 'Curvature Down']

def MeasureTypeIsPriceOrRate( measureType ):
    return MeasureTypeIsCurvature( measureType ) or measureType == "Delta"
    
class Populator(RiskFactorDimensionPopulator):

    def __init__(self, measureType, riskClass, rfColls, dimensionInformation, isVectorItem, commonCurrency, hierarchyName):
        self.m_measureType = measureType
        self.m_riskClass = riskClass
        self.m_hierarchy = FRTBSAHierarchy.GetSAHierarchy(hierarchyName)
        
        pe, pc = self.PerimeterInformation()
        self.m_bucket = None
        self.m_subTypeSet = False
        self.m_subType = None
        
        self.m_currency = None
        self.m_commonCurrency = commonCurrency
        RiskFactorDimensionPopulator.__init__( self, rfColls, dimensionInformation, isVectorItem )

    def ShiftShape( self ):
        if self.m_riskClass in ['GIRR', 'CSR (NS)', 'CSR (S-C)'] and MeasureTypeIsPriceOrRate( self.m_measureType ):
            return acm.Valuation().MappedValuationParameters().Parameter().IrShiftType()
        elif 'Vega' == self.m_measureType:
            return acm.Valuation().MappedValuationParameters().Parameter().VolShiftType()
        return 'Triangle'

    def ShiftType( self ):
        shiftType = None
        if ( 'Vega' == self.m_measureType ) or ( self.m_riskClass in ['Commodity', 'Equity', 'FX'] and self.m_subType != 'Repo Rate'):
            shiftType = 'Relative'
        else:
            shiftType = 'Absolute'
        return shiftType

    def GetHierarchyColumValue( self, columnName ):
        value = None

        subType = self.SubTypeForHierarchyGet()
        currencyPair = self.CurrencyPairForHiearchyGet(False)

        value = self.m_hierarchy.ColumnValue( self.m_riskClass, self.m_bucket, subType, currencyPair, columnName )

        if not value:
            if 'FX' == self.m_riskClass:
                value = self.m_hierarchy.ColumnValue( self.m_riskClass, self.m_bucket, subType, self.CurrencyPairForHiearchyGet(True), columnName )
                if not value:
                    value = self.m_hierarchy.ColumnValue( self.m_riskClass, self.m_bucket, subType, 'Other Currency Pair', columnName )
            elif 'GIRR' == self.m_riskClass:
                value = self.m_hierarchy.ColumnValue( self.m_riskClass, 'Other Currency', subType, currencyPair, columnName )
        return value

    def CurvatureShiftSize( self ):
        shiftSize = None
        if self.m_riskClass and self.m_bucket and self.SubTypeSetIfNeeded() and self.CurrencyPairSetIfNeeded():
            shiftSize = self.GetHierarchyColumValue( "Delta Risk Weight" )
            if 'Curvature Down' == self.m_measureType and shiftSize:
                shiftSize = -shiftSize
        return shiftSize

    def ShiftDivisor( self, shiftSize ):
        return MeasureTypeIsCurvature( self.m_measureType ) and 1.0 or shiftSize

    def PerimeterInformation( self ):
        if self.m_measureType in ['Vega']:
            return None, None
        elif self.m_riskClass in ['CSR (NS)', 'CSR (S-C)']:
            return FRTBSATools.FRTBPerimeterEntities( self.m_riskClass ), FRTBSATools.FRTBPerimeterCriteria( self.m_riskClass )
        return None, None

    def SubTypeForHierarchyGet(self):
        return None if self.m_riskClass in ["CSR (NS)", "CSR (S-C)", "FX", "Commodity"] else self.m_subType
    
    def SubTypeSetIfNeeded(self):
        if self.m_riskClass in ["CSR (NS)", "CSR (S-C)", "FX", "Commodity"]:
            return True
        return self.m_subTypeSet
        
    def CurrencyPairSetIfNeeded( self ):
        if self.m_riskClass == "FX":
            return self.m_commonCurrency and self.m_currency
        return True
        
    def CurrencyPairForHiearchyGet(self, reversed):
        if self.m_riskClass == "FX":
            return reversed and self.m_commonCurrency + "/" + self.m_currency or self.m_currency + "/" + self.m_commonCurrency
        return None
        
    def ShiftSize( self ):
        shiftSize = None
        if 'Vega' == self.m_measureType:
            shiftSize = 0.01
        elif self.m_riskClass and self.m_bucket and self.SubTypeSetIfNeeded() and self.CurrencyPairSetIfNeeded():
            shiftSize = self.GetHierarchyColumValue("Delta Shift Size")
        return shiftSize

    def ShiftSizeAndDivisor( self ):
        shiftSize = None
        if MeasureTypeIsCurvature( self.m_measureType ):
            shiftSize = self.CurvatureShiftSize()
        else:
            shiftSize = self.ShiftSize()
        return ( shiftSize, self.ShiftDivisor( shiftSize ) )

    def SetPath( self, dimensionInformation, item ):
        if item is not None:
            item = str(item)
        if str(dimensionInformation.m_id) == "Subtype":
            self.m_subType = item
            self.m_subTypeSet = True
        elif str(dimensionInformation.m_id) == "Bucket":
            self.m_bucket = item
        elif str(dimensionInformation.m_id) == "Currency":
            self.m_currency = item
    
def OrderedDimensionInformations( riskFactorCollections, riskClass, measureType, positionExpiryTimeBuckets ):
    usedDimensionIDs = set()
    vDims = []
    
    dimensionInformations = []
    dimInfo = RiskFactorCalculationTools.DimensionInformation("Bucket", True, "FRTB_SA_Bucket", False)
    dimensionInformations.append( (dimInfo, "VectorItem") )
    dimInfo = RiskFactorCalculationTools.DimensionInformation("Risk Class", False, "FRTB_SA_Risk_Class", True)
    dimensionInformations.append( (dimInfo, "VectorItem") )

    if not (riskClass in ["Commodity", "FX"]):
        if not (MeasureTypeIsCurvature( measureType ) and riskClass in ["CSR (NS)", "CSR (S-C)"]):
            dimInfo = RiskFactorCalculationTools.DimensionInformation("Subtype", False, "FRTB_SA_Subtype", False)
            dimensionInformations.append( (dimInfo, "VectorItem") )
        
    for idx, riskFactorCollection in enumerate(riskFactorCollections):
        dimensions = riskFactorCollection.RiskFactorDimensions()
        for dimension in dimensions:
            if MeasureTypeIsCurvature( measureType ) and dimension.DimensionId() == 'Time':
                continue
            if riskClass == 'Commodity' and measureType == 'Delta' and dimension.DimensionId() == 'Time':
                #Time dimension is handled differently, ( for old setups )
                continue
            dimensionID = RiskFactorCalculationTools.DimensionIdFromDimension( dimension )
            if idx == 0:
                usedDimensionIDs.add( dimensionID )
                if acm.RiskFactor.DimensionUsesVectorItemImplementation( dimension ):
                    dimInfo = RiskFactorCalculationTools.DimensionInformation(dimensionID, False, None, False)
                    dimensionInformations.append( (dimInfo, "VectorItem") )
                else:
                    dimInfo = RiskFactorCalculationTools.DimensionInformation(dimensionID, False, None, False)
                    vDims.append( (dimInfo, "Vector") )
            else:
                if 'Time' != dimension.DimensionId():
                    assert( dimensionID in usedDimensionIDs )
                else:
                    if not dimensionID in usedDimensionIDs:
                        usedDimensionIDs.add( dimensionID )
                        
                        dimInfo = RiskFactorCalculationTools.DimensionInformation(dimensionID, False, None, False)
                        vDims.append( (dimInfo, "Vector") )
                        
    dimensionInformations.extend( vDims )
    
    if riskClass == 'Commodity' and measureType == 'Delta' and positionExpiryTimeBuckets:
        dimensionID = RiskFactorCalculationTools.DimensionId( "Position Expiry", positionExpiryTimeBuckets )
        dimInfo = RiskFactorCalculationTools.DimensionInformation( dimensionID, False, None, False )
        dimensionInformations.append( (dimInfo, "PositionExpiry") )
        
    return dimensionInformations

def CollectionIsValid( riskFactorCollection, riskClass, measureType ):
    if riskFactorCollection.AdditionalInfo().FRTB_SA_Risk_Class() == riskClass:
        if measureType == "Vega" and riskFactorCollection.RiskFactorType() in ["Volatility", "Benchmark Volatility"]:
            return True
        elif MeasureTypeIsCurvature( measureType ):
            if not riskFactorCollection.RiskFactorType() in ["Volatility", "Benchmark Volatility"] and not riskFactorCollection.AdditionalInfo().FRTB_SA_Subtype() in ["Inflation", "Cross Currency Basis", "Repo Rate"]:
                return True
        elif measureType == "Delta":
            if not riskFactorCollection.RiskFactorType() in ["Volatility", "Benchmark Volatility"]:
                return True
    return False

def RiskFactorCollections( parameters ):
    return [rfColl for rfColl in acm.FRiskFactorSetup[parameters.At('rfsetup')].RiskFactorCollections() if CollectionIsValid( rfColl, parameters.At("riskClass"), parameters.At("measureType") )]
                
def TermCurrencyDimension( riskFactorCollection ):
    for dimension in riskFactorCollection.RiskFactorDimensions():
        if dimension.DimensionId() == "TermCurrency":
            return dimension
    return None
    
def GetPositionExpiryTimeBuckets( parametersAsACMDict ):
    riskFactorCollections = RiskFactorCollections( parametersAsACMDict )
    positionExpiryTimeBuckets = parametersAsACMDict.At("positionExpiryTimeBuckets")
    if positionExpiryTimeBuckets is None:
        for rfColl in riskFactorCollections:
            for dimension in rfColl.RiskFactorDimensions():
                if 'Time' == dimension.DimensionId():
                    positionExpiryTimeBuckets = dimension.CoordinatesSource()
    return positionExpiryTimeBuckets
    
def ael_main_ex(parameters, unused):
    dims = []
    context = acm.ExtensionTools().GetDefaultContext()
    parametersAsACMDict = acm.FDictionary()
    parametersAsACMDict.AddAll( parameters )
    riskClass = parametersAsACMDict.At("riskClass")
    measureType = parametersAsACMDict.At("measureType")
    hierarchy = parametersAsACMDict.At("hierarchy")
    positionExpiryTimeBuckets = GetPositionExpiryTimeBuckets( parametersAsACMDict )
    
    riskFactorCollections = RiskFactorCollections( parametersAsACMDict )
    if len( riskFactorCollections ) == 0:
        return dims

    orderedDimensionInformations = OrderedDimensionInformations(
        riskFactorCollections,
        riskClass,
        measureType,
        positionExpiryTimeBuckets
    )
    
    dependentsOn = []
    vCount = 0
    
    riskFactorInstances = []
    for riskFactorCollection in riskFactorCollections:
        riskFactorInstances.extend( riskFactorCollection.RiskFactorInstances() )

    commonCurrency = None
    if riskClass == "FX" and MeasureTypeIsPriceOrRate( measureType ) and len(riskFactorInstances) > 0:
        commonCurrency = riskFactorInstances[0].CoordinateValue( TermCurrencyDimension( riskFactorInstances[0].RiskFactorCollection() ) )
    for dimensionInformation, implementationType in orderedDimensionInformations:
        config = None
        if implementationType == "PositionExpiry":
            dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'Risk Factor Position Expiry').Value()
            shiftData = acm.FVectorShiftData()
            shiftData.SetShiftVector( positionExpiryTimeBuckets.TimeBuckets() )
            shiftData.SetLabels( [tb.Spec() for tb in positionExpiryTimeBuckets.TimeBuckets()] )
            
            dim = acm.Risk().CreateVectorDimension( dimensionInformation.m_id, dimDef, shiftData, config, None, [] )
        else:
            isVectorItem = implementationType == "VectorItem"
            if isVectorItem:
                dependentsOn.append( dimensionInformation )

            shiftData = acm.FPathDependentVectorShiftData( [d.m_id for d in dependentsOn] )
            populator = Populator( measureType, riskClass, riskFactorCollections, dimensionInformation, isVectorItem, commonCurrency, hierarchy)
            PopulateShiftDataRecursive( populator, riskFactorInstances, dependentsOn, [], [], shiftData )
            
            if isVectorItem:
                dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, 'Risk Factor Targets').Value()
                extParams = BaseParametersForVectorItemDimension( populator )
                if MeasureTypeIsCurvature( measureType ):
                    extParams[acm.FSymbol("RiskFactorTargetsInclusionHook")] = acm.FSymbol( "frtbIsOption" )
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

    orderedDimensionInformations = OrderedDimensionInformations(
        riskFactorCollections,
        parametersAsACMDict.At('riskClass'),
        parametersAsACMDict.At('measureType'),
        GetPositionExpiryTimeBuckets( parametersAsACMDict )
    )

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
        
    positionExpiryTimeBuckets = GetPositionExpiryTimeBuckets( parametersAsACMDict )
    if dimensionIdToMatch == RiskFactorCalculationTools.DimensionId( "Position Expiry", positionExpiryTimeBuckets ):
        return positionExpiryTimeBuckets.TimeBuckets()
        
    for riskFactorCollection in riskFactorCollections:
        for dimension in riskFactorCollection.RiskFactorDimensions():
            if RiskFactorCalculationTools.DimensionIdFromDimension( dimension ) == dimensionIdToMatch:
                source = dimension.CoordinatesSource()
                if source and source.IsKindOf(acm.FStoredTimeBuckets):
                    return source.TimeBuckets()
                return source
    return None
