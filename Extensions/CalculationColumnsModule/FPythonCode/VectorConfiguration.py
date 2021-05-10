
import acm
import string

_s_DependenciesSym = acm.FSymbol("Dependencies")
_s_ImplementationTypeSym = acm.FSymbol("ImplementationType")
_s_ModuleSym = acm.FSymbol( 'Module' )

def ael_custom_dialog_show():
    pass
    
def DependentDimensionDefinitionNames( dependentsString ):
    if dependentsString:
        return [acm.FSymbol( item ) for item in string.split( str(dependentsString), ";" )]
    return None
    
def DependentDimensionsAndCallbackCreator( dimensionId, dimDef, dimDefByLogicalName, logicalNameByDimDefName ):
    dependentDimDefNames = DependentDimensionDefinitionNames( dimDef[ _s_DependenciesSym ] )
    isVectorItem = dimDef[ _s_ImplementationTypeSym ] == acm.FSymbol( "VectorItem" )
    
    dependentOnDimensionIds = None
    callbackCreator = None
    if dependentDimDefNames and dimDefByLogicalName:
        dependentOnDimensionDefinitions = []
        dependentOnDimensionIds = []
        for dependentDimDefName in dependentDimDefNames:
            dependentLogicalName = logicalNameByDimDefName[ dependentDimDefName ]
            if dependentLogicalName:
                dependentDimDef = dimDefByLogicalName[ dependentLogicalName ]
                dependentOnDimensionDefinitions.append( dependentDimDef )
                dependentOnDimensionIds.append( acm.FSymbol( dependentLogicalName ) )
        if isVectorItem:
            dependentOnDimensionIds.append( acm.FSymbol( dimensionId ) )
        callbackCreatorModule = __import__( str(dimDef[ _s_ModuleSym ]) )
        callbackCreator = callbackCreatorModule.Create( dependentOnDimensionDefinitions )
        
    return dependentOnDimensionIds, callbackCreator
    
def Dimensions( parameters ):
    dims = []
    dimensionsData = parameters["dimensions"]
    if dimensionsData:
        dimDefByLogicalName = acm.FDictionary()
        logicalNameByDimDefName = acm.FDictionary()
        context = acm.ExtensionTools().GetDefaultContext()
        for dimensionData in dimensionsData:
            dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, dimensionData['dimDefName']).Value()
            externalId = acm.FSymbol( dimensionData["externalId"] )
            dimDefByLogicalName[externalId] = dimDef
            logicalNameByDimDefName[dimDef.Name()] = externalId
        
        for dimensionData in dimensionsData:
            dimDef = context.GetExtension(acm.FColumnDimensionDefinition, acm.FObject, dimensionData['dimDefName']).Value()
            dimensionId = acm.FSymbol( dimensionData["externalId"] )
            
            dependentOnDimensionIds, callbackCreator = DependentDimensionsAndCallbackCreator( dimensionId, dimDef, dimDefByLogicalName, logicalNameByDimDefName )
        
            isVectorItem = dimDef[ _s_ImplementationTypeSym ] == acm.FSymbol( "VectorItem" )
            imdrDimensionId = str(dimensionId)
            
            configCreateCallback = None
            shiftData = None
            
            if isVectorItem:
                shiftData = acm.FVectorShiftData()
                if callbackCreator:
                    configCreateCallback = callbackCreator.CreateConfig
            else:
                if callbackCreator:
                    shiftData = acm.FDynamicVectorShiftData()
                    shiftData.SetFunctions( callbackCreator.Vector, callbackCreator.Labels )
                else:
                    shiftData = acm.FVectorShiftData()
                    if dimensionData["coordinatesParams"]:
                        if dimensionData["coordinatesParams"].IsKindOf( acm.FStoredTimeBuckets ):
                            imdrDimensionId += ": " + dimensionData["coordinatesParams"].Name()
                            timeBuckets = dimensionData["coordinatesParams"].TimeBuckets()
                            shiftData.SetShiftVector( timeBuckets )
                            shiftData.SetLabels( [tb.Spec() for tb in timeBuckets] )
                        elif dimensionData["coordinatesParams"].IsKindOf( acm.FIndexedCollection ):
                            shiftData.SetShiftVector( dimensionData["coordinatesParams"] )
                            shiftData.SetLabels( dimensionData["coordinatesParams"] )
                        else:
                            assert(0)
                    
            dimension = acm.Risk().CreateVectorDimension( imdrDimensionId, dimDef, shiftData, None, configCreateCallback, dependentOnDimensionIds, dimensionData["receivers"] )
            dims.append( dimension )           

    return dims
    
def ael_custom_dialog_main(parameters, unused):
    return Dimensions( parameters )
    
def ael_coordinates_source( parameters, dictExtra ):
    dimensions = Dimensions( parameters )
    dimensionIdToMatch = acm.FSymbol( dictExtra.At('customData').ExtensionObject() )
    for dim in dimensions:
        if dim.DimensionId() == dimensionIdToMatch:
            return dim.ShiftVector()
    return None
    
