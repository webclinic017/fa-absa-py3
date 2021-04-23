
import acm
import RiskFactorExtensions
import FLogger

logger = FLogger.FLogger.GetLogger('FARiskFactorCalculations')

def SymbolOrNone( s ):
    if s is not None:
        return acm.FSymbol( s )
    return None

def DimensionId( dimensionName, coordinatesSource ):
    id = dimensionName
    if coordinatesSource:
        id += " : " + coordinatesSource.Name()
    return SymbolOrNone( id )
    
def DimensionIdFromDimension( dimension ):
    return DimensionId( 
        dimension.DisplayName(),
        dimension.CoordinatesSource()
    )
    
class DimensionInformation:

    def __init__(self, id, isInstanceProperty, propertyMethodName, isImplicitDimension):
        self.m_id = SymbolOrNone( id )
        self.m_isInstanceProperty = isInstanceProperty
        self.m_propertyMethodName = propertyMethodName
        self.m_isImplicitDimension = isImplicitDimension
        
        #mutable
        self.m_dimensionByCollection = None
        
    def GetDimension( self, collection ):
        if not self.m_dimensionByCollection:
            self.m_dimensionByCollection = {}
        dimension = self.m_dimensionByCollection.get( collection )
        if not dimension:
            for dim in collection.RiskFactorDimensions():
                if DimensionIdFromDimension(dim) == self.m_id:
                    dimension = dim
                    self.m_dimensionByCollection[ collection ] = dimension
                    break
        return dimension
        
    def InstanceValue( self, riskFactorInstance ):
        value = None
        if self.m_propertyMethodName:
            if self.m_isInstanceProperty:
                value = riskFactorInstance.AdditionalInfo().PerformWith( self.m_propertyMethodName, [] )
            else:
                value = riskFactorInstance.RiskFactorCollection().AdditionalInfo().PerformWith( self.m_propertyMethodName, [] )
        else:
            dimension = self.GetDimension( riskFactorInstance.RiskFactorCollection() )
            if dimension:
                value = riskFactorInstance.CoordinateValue( dimension )
        return SymbolOrNone( value )
    
    def IsImplicit( self ):
        return self.m_isImplicitDimension
        
    def AsDictionary( self ):
        return acm.FStaticDictionary( {acm.FSymbol("id") : SymbolOrNone(self.m_id),
                acm.FSymbol("isInstanceProperty") : self.m_isInstanceProperty,
                acm.FSymbol("propertyMethodName") : SymbolOrNone( self.m_propertyMethodName ),
                acm.FSymbol("isImplicitDimension") : self.m_isImplicitDimension} )
                
    @staticmethod
    def FromDictionary( dimensionInformationDictionary ):
        dimensionInformation = DimensionInformation(
            dimensionInformationDictionary[acm.FSymbol("id")],
            dimensionInformationDictionary[acm.FSymbol("isInstanceProperty")],
            dimensionInformationDictionary[acm.FSymbol("propertyMethodName")],
            dimensionInformationDictionary[acm.FSymbol("isImplicitDimension")]
        )
        return dimensionInformation
                


s_riskFactorCollectionSym = acm.FSymbol( "riskFactorCollection" )
s_shiftTypeSym = acm.FSymbol( "shiftType" )    #Relative, Absolute, etc...
s_shiftShapeSym = acm.FSymbol( "shiftShape" )  #eg. Triangle
s_perimeter = acm.FSymbol( "perimeter" )
s_perimeterCriteria = acm.FSymbol( "perimeterCriteria" )
s_shiftSizeSym = acm.FSymbol( "shiftSize" )
s_shiftDivisorSym = acm.FSymbol( "shiftDivisor" )
s_riskFactorPathValues = acm.FSymbol( "riskFactorPathValues" )
s_riskFactorPathKeys = acm.FSymbol( "riskFactorPathKeys" )
s_referenceDateSym = acm.FSymbol( "referenceDate" )
s_topOnlyExtensionGroup = acm.FSymbol("topOnlyExtensionGroup")


#PUBLISHED
def FilteredInstancesByItemIdFromDictionary( dimensionInformationDictionary, sourceInstances ):
    dimensionInformation = DimensionInformation.FromDictionary( dimensionInformationDictionary )
    return FilteredInstancesByItemId( dimensionInformation, sourceInstances )

def FilteredInstancesByItemId( dimensionInformation, sourceInstances ):
    filteredInstances = {}
    if dimensionInformation.IsImplicit():
        item = dimensionInformation.InstanceValue( sourceInstances[0])
        return {item : sourceInstances}
    for instance in sourceInstances:
        instanceValue = dimensionInformation.InstanceValue( instance )
        if instanceValue in filteredInstances:
            filteredInstances[ instanceValue ].append( instance )
        else:
            filteredInstances[ instanceValue ] = [ instance ]
    return filteredInstances
    

#PUBLISHED
def RiskFactorDeltaParameters( referenceDate ):
    return { s_referenceDateSym : referenceDate }

#PUBLISHED
def ShiftRiskFactorDeltaParameters( parametersDict, newParametersDict ):
    merged = None
    if parametersDict:
        merged = acm.FDictionary()
        merged.AddAll( parametersDict )
    if newParametersDict:
        merged.AddAll( newParametersDict )
    return merged

#PUBLISHED
def RiskFactorDeltaShiftParameters( riskFactorCreatorCache, parametersDict, riskFactorCollection, riskFactorInstances ):
    
    riskFactorDescr, shiftConfig = RiskFactorFromParameters( riskFactorCreatorCache, parametersDict, riskFactorCollection, riskFactorInstances )
    params = []
    params.append( RiskFactorExtensions.RiskFactorDeltaParameters(
        riskFactorDescr,
        shiftConfig,
        None, 
        1,
        parametersDict[ s_shiftSizeSym ] ) )
    return params

def GetCoordinateString( parametersDict, dimension ):
    coordinateString = parametersDict[ DimensionIdFromDimension( dimension ) ]
    if not coordinateString:
        for dimensionDictionary, value in zip( parametersDict[s_riskFactorPathKeys], parametersDict[s_riskFactorPathValues] ):
            if acm.FSymbol(dimension.DisplayName()) == dimensionDictionary[ acm.FSymbol("id") ]:
                coordinateString = str( value )
    return coordinateString
    
def RiskFactorFromParameters( riskFactorCreatorCache, parametersDict, riskFactorCollection, riskFactorInstances ):
    type = acm.RiskFactor.RiskFactorType( riskFactorCollection.RiskFactorType() )

    shiftConfig = None
    if acm.FSymbol('ShiftType') in type.ShiftFormatNames():
        shiftShape = parametersDict[ s_shiftShapeSym ]
        if shiftShape:
            shiftConfig = type.ShiftConfiguration( 'ShiftType', shiftShape, shiftConfig )
    if acm.FSymbol('DifferenceType') in type.ShiftFormatNames():
        shiftType = parametersDict[ s_shiftTypeSym ]
        if shiftType:
            shiftConfig = type.ShiftConfiguration( 'DifferenceType', shiftType, shiftConfig )

    vConf = None
    valueParams = riskFactorCollection.RiskFactorValueParameters()
    if valueParams and len(valueParams) > 0:
        for valueParam in riskFactorCollection.RiskFactorValueParameters():
            vConf = type.ValueConfiguration( valueParam.ParameterKey(), valueParam.ParameterValue(), vConf )

    vConf = type.ValueConfiguration( 'ValueUnit', 'Unit', vConf )

    coordinateByDimension = {}
    for dimension in riskFactorCollection.RiskFactorDimensions():
        if acm.RiskFactor().DimensionIsPartOfArguments( dimension ):
            coordinateString = GetCoordinateString( parametersDict, dimension )
            if coordinateString:
                coordinateByDimension[ dimension ] = str( coordinateString )

    if len(coordinateByDimension) > 0:
        riskFactor = None
        for instance in riskFactorInstances:
            if instance.RiskFactorCollection() == riskFactorCollection:
                match = True
                for dimension in coordinateByDimension:
                    if instance.CoordinateValue( dimension ) != coordinateByDimension[dimension]:
                        match = False
                        break
                if match:
                    riskFactor = acm.RiskFactor().RiskFactorFromRiskFactorInstance( instance, "", riskFactorCreatorCache, parametersDict[s_referenceDateSym] )
                    return riskFactor.RiskFactorDescription().RiskFactorType().CreateRiskFactorDescription(
                        riskFactor.RiskFactorDescription().CoordinateConfiguration(), vConf ), shiftConfig
        assert( False )
    else:
        return type.CreateRiskFactorDescription( None, vConf ), shiftConfig


#PUBLISHED
def DimensionItems( riskFactorInstances, dimension, scenarioBuilder, riskFactorCreatorCache ):
    itemCriterias = []
    if not riskFactorInstances or len(riskFactorInstances) == 0:
        return itemCriterias

    if dimension[acm.FSymbol("isImplicitDimension")]:
        dimensionInformation = DimensionInformation.FromDictionary( dimension )
        item = dimensionInformation.InstanceValue( riskFactorInstances[0])
        return [[item]]
    byItem = FilteredInstancesByItemIdFromDictionary( dimension, riskFactorInstances )
    for item in byItem.keys():
        itemCriterias.append( [item, CriteriaFromInstances(byItem[item], scenarioBuilder, riskFactorCreatorCache)] )
    return itemCriterias

__s_criteriaFunction = acm.GetFunction( 'riskFactorCompositeCriteriaIsSatisfiedBy', 2 )

def CriteriaFromInstances( riskFactorInstances, scenarioBuilder, riskFactorCreatorCache ):
    crit = scenarioBuilder.CreateCriteriaFromRiskFactor(
        acm.RiskFactor().RiskFactorFromRiskFactorInstance( riskFactorInstances, "", riskFactorCreatorCache, acm.Time().DateToday() ),
        True
    )
    
    if isinstance(crit, str) or crit.IsKindOf(acm.FString):
        crit = [crit]
    
    if hasattr(crit, '__iter__'):
        criterias = acm.FIdentitySet()
        for criteria in crit:
            try:
                if isinstance(criteria, str):
                    raise Exception('Criteria: {} is not created correctly, please control related risk factor instances.'.format(str(criteria)) )
            except Exception as e:
                logger.WLOG(str(e))
            criterias.Add( criteria )
        return __s_criteriaFunction.CreateCall( [None, criterias] )
    return crit

#PUBLISHED
def RiskFactorCollectionTopOnly( riskFactorCollection, topOnlyOverride ):
    if topOnlyOverride is None:
        valueParameter = riskFactorCollection.RiskFactorValueParameter( 'TotalOrTopSpread' )
        if valueParameter:
            return valueParameter.ParameterValue() == "Top Spread"
    return topOnlyOverride
    
#PUBLISHED
def RiskFactorScenarioAxis( context, scenarioBuilder, riskFactorCreatorCache, riskFactorCollections, riskFactorInstances, shiftParamNodes, topOnlyOverride ):
    scenarioAxis = acm.FScenarioAxis()
    riskFactorInstancesSet = set(riskFactorInstances)
    for riskFactorCollection, shiftParams in zip(riskFactorCollections, shiftParamNodes):
        instances = []
        for instance in riskFactorCollection.RiskFactorInstances():
            if instance in riskFactorInstancesSet:
                instances.append( instance )
        rfType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
        topOnly = RiskFactorCollectionTopOnly( riskFactorCollection, topOnlyOverride )
        entities = context.MemberNames("FExtensionAttribute", "risk factors", rfType.ExtensionAttributeGroupItem( topOnly ));
        criteria = CriteriaFromInstances(instances, scenarioBuilder, riskFactorCreatorCache)
        function = acm.GetFunction(rfType.ShiftFunctionName(), 6 )
        scenarioAxis.AddMember( entities, criteria, function, shiftParams, acm.FObject, True )
    return scenarioAxis

#PUBLISHED  
def UsedDimensionItems( dimensionInformation, itemsAndCriteria, evaluator ):
    usedItems = acm.FArray()
    if dimensionInformation[acm.FSymbol("isImplicitDimension")]:
        for iAndA in itemsAndCriteria:
            usedItems.Add(acm.FSymbol( iAndA[0] ))
            break
    else:
        for iAndA in itemsAndCriteria:
            criteria = iAndA[1]
            item = iAndA[0]
            if criteria.IsSatisfiedBy( evaluator ):
                usedItems.Add( acm.FSymbol( item ) )
            else:
                prop = evaluator.Proprietor()
                if prop and criteria.IsSatisfiedBy( prop ):
                    usedItems.Add( acm.FSymbol( item ) )
    return usedItems


#PUBLISHED
def RiskFactorCompositeCriteriaIsSatisfiedBy( anObject, subCriterias ):
    for subCriteria in subCriterias:
        try:
            if subCriteria.IsSatisfiedBy( anObject ):
                return True
        except Exception as e:
            logger.WLOG('Processing sub-criteria: {}. \'{}\''.format(str(subCriteria), str(e)))
    return False
    
