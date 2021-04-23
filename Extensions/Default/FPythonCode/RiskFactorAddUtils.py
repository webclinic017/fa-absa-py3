

import numbers

import itertools

import acm
import RiskFactorUtils
import RiskFactorTimeBuckets

from RiskFactorSelection import SelectionCtrl, FixedSelectionCtrl, CompositeSelectionCtrl

#------------------------------------------------------------------------------
def AddRiskFactorToCollection( riskFactor, riskFactorCollection ):
    instance = acm.FRiskFactorInstance()
    instance.RiskFactorCollection(riskFactorCollection)
    instance.RegisterInStorage()

    for uniqueId in riskFactor.Keys():
        coordinate = acm.FRiskFactorCoordinate()
        coordinate.CoordinateValue( riskFactor[uniqueId] )
        coordinate.RiskFactorInstance( instance )
        coordinate.RiskFactorDimensionUniqueId(uniqueId)
        coordinate.RegisterInStorage()
        
#------------------------------------------------------------------------------
# CoreDimensionInformation and dimensionInformation
# DimensionInformation: Each dimension is represented as a dimensionInformation.
# coreDimensionInformation: Each dimension with other dimensions dependent upon it's selection is represented as a coreDimensionInformation. 
#------------------------------------------------------------------------------
class DimensionInformation( object ):
    def __init__(self, dimension, selection, persistentMethodChain, methodChain=None):
        self.m_dimension = dimension
        self.m_selection = selection
        self.m_persistentMethodChain = persistentMethodChain
        self.m_methodChain = methodChain
    
    def GetDimension(self):
        return self.m_dimension
        
    def GetSelection(self):
        return self.m_selection
    
    def SetSelection(self, selection): 
        self.m_selection = selection
        
    def GetPersistentMethodChain(self):
        return self.m_persistentMethodChain
    
    def GetMethodChain(self):
        return self.m_methodChain
    
    def SetMethodChain(self, mChain):
        self.m_methodChain = mChain
    
    def DebugDisplay(self):
        print('- '*10)
        print('Dimension: ', self.m_dimension.DisplayName())
        print('Persistent Method Chain: ', self.m_persistentMethodChain)
        print('Method Chain: ', self.m_methodChain)
        print('/-'*10)
    

class CoreDimensionInformation( object ):
    def __init__(self, id, validationCB, dimInfoList=None):
        self.m_id = id 
        self.m_validationCallBack = validationCB
        self.m_dimInfoList = []
        self.m_domain = None
        self.m_sharedMethodChain = None 
        if dimInfoList:
            for item in dimInfoList:
                self.PushDimInfoList(item)
    
    def PushDimInfoList(self, item):
        assert isinstance(item, DimensionInformation), "Error: Can only insert DimensionInformation type items in CoreDimensionInformation dimInfoList. " 
        self.m_dimInfoList.append(item)
    
    def SetDimInfoList(self, itemsList):
        for item in itemsList:
            self.PushDimInfoList(item)
    
    def GetDimId(self):
        return self.m_id
    
    def GetValidationCB(self):
        return self.m_validationCallBack
    
    def SetValidationCB(self, validCB):
        self.m_validationCallBack = validCB
    
    def GetDimInfoList(self):
        return self.m_dimInfoList
    
    def GetDomain(self):
        return self.m_domain
    
    def SetDomain(self, domain):
        self.m_domain = domain
    
    def GetSharedMethodChain(self):
        return self.m_sharedMethodChain
        
    def SetSharedMethodChain(self, sharedMethdoChain):
        self.m_sharedMethodChain = sharedMethdoChain
        
    def DebugDisplay(self):
        print('-. '*10)
        print('ID: ', self.m_id)
        print('Validation Callback: ', self.m_validationCallBack)
        print('Domain: ', self.m_domain)
        print('Shared Method Chain: ', self.m_sharedMethodChain)
        if len(self.m_dimInfoList) > 0:
            print('DimInfoList: ')
            [item.DebugDisplay() for item in self.m_dimInfoList]
        print('/-.'*10)
    

#------------------------------------------------------------------------------
# Risk Factor Generators
#------------------------------------------------------------------------------
class RiskFactorDetectionGenerator( object ):
    
    #------------------------------------------------------------------------------
    def __init__( self, riskFactorIndentifier, riskFactorCollection ):
        self.m_riskFactorCollection = riskFactorCollection
        self.m_riskFactorIdentifier = riskFactorIndentifier
    
    #------------------------------------------------------------------------------
    def GenerateRiskFactors( self, selectionByDomain ):        
        objects = []
        
        for domain in selectionByDomain.keys():
            objects.extend( selectionByDomain[domain] )
            
        return self.m_riskFactorIdentifier.DetectRiskFactors( self.m_riskFactorCollection, objects )

#------------------------------------------------------------------------------
class RiskFactorCombinationGenerator( object ):
    #------------------------------------------------------------------------------
    def __init__(self, dependentDimensions):
        self.m_dependentDimensions = dependentDimensions
        
    #------------------------------------------------------------------------------
    def GenerateRiskFactors(self, DomainSelection):
        domainDependentDimensions = self.m_dependentDimensions
        
        self.ApplyDimensionMethodChainOnDomainSelection(DomainSelection, domainDependentDimensions)
        
        #structure to get on form {selectionId : [Selection1, ... , SelectionN], ... }
        allDimensionCombinationsList = []
        for domKey in DomainSelection.keys():
            domainToDimensionSelectionDict = {}
            
            for dimInfo in domainDependentDimensions[domKey].GetDimInfoList():
                domainToDimensionSelectionDict[dimInfo.GetDimension().UniqueId()] = dimInfo.GetSelection()

            self.CleanDomainSelections(domainToDimensionSelectionDict)
        
            domainToDimensionSelectionDict = CoordinatesAsStrings(domainToDimensionSelectionDict)
            
            lenghtOfSelections = len(domainToDimensionSelectionDict[list(domainToDimensionSelectionDict)[0]])
            
            #structure the dimensionId tuples-->{ dim1: val1, dim2: val2, ...  }
            dimensionCombinationlist = []
            for selIdx in range(0, lenghtOfSelections):
                dimensionCombination = {}
                for dimensionIdKey in domainToDimensionSelectionDict.keys():
                    dimensionCombination[dimensionIdKey] = domainToDimensionSelectionDict[dimensionIdKey][selIdx]
                dimensionCombinationlist.append(dimensionCombination)
            allDimensionCombinationsList.append(dimensionCombinationlist)
            
        return ComputeCrossProductOfDimensionIdTuples(allDimensionCombinationsList)
        
    #------------------------------------------------------------------------------
    def CleanDomainSelections(self, domainToDimensionSelectionDict):
        #Go through all dimension selections, index of elements to be pop:ed stored.
        popListIndexes = []
        for dimensionIdKey in domainToDimensionSelectionDict.keys():
            idx = 0 
            for item in domainToDimensionSelectionDict[dimensionIdKey]:
                if not self.SelectionControlInvalidItems(item):
                    if not idx in popListIndexes:
                        popListIndexes.append(idx)
                idx = idx + 1
        
        popListIndexes.sort(reverse=True)
        #Pop elements at pop indexes for all dimension selections.
        for dimensionIdKey in domainToDimensionSelectionDict.keys():
            for idx in popListIndexes:
                del domainToDimensionSelectionDict[dimensionIdKey][idx]
                
    #------------------------------------------------------------------------------
    def SelectionControlInvalidItems(self, dimensionAttributeValue):
        if dimensionAttributeValue is None or dimensionAttributeValue == '':
            return False
        return True
        
    #------------------------------------------------------------------------------
    def ApplyDimensionMethodChainOnDomainSelection(self, DomainSelection, domainDependentDimensions):
        #Apply method chain on domain selections --> get dimension selections.  
        for domKey in DomainSelection.keys():
            for depDimensionsKey in domainDependentDimensions.keys():
                if domKey == depDimensionsKey:
                    for depDimension in domainDependentDimensions[depDimensionsKey].GetDimInfoList():
                        mc = depDimension.GetMethodChain()
                        if mc:
                            method = acm.FMethodChain(mc)
                            depDimension.SetSelection( [method.Call([item]) for item in DomainSelection[domKey]] )
                        else:
                            depDimension.SetSelection( list(DomainSelection[domKey]) )
                            
#------------------------------------------------------------------------------
# Risk Factor Selection Init
#------------------------------------------------------------------------------

def ComputeSelectionControlAndDimensionDependances(riskFactorCollection):
    uniqueDimensionIds = CreateDimensionToSelectionUnitDependenceDictionary(riskFactorCollection)
    CompositeSelectionCtrl = CreateAddFromInsertItemsSelection( uniqueDimensionIds )
        
    return CompositeSelectionCtrl, uniqueDimensionIds

#------------------------------------------------------------------------------
def CreateAddFromInsertItemsSelection( uniqueDimensionIds ):
    selections = []
    for dimensionIdKey in uniqueDimensionIds.keys():
        selection = None
        coreDimInfo = uniqueDimensionIds[dimensionIdKey]

        if SoleDependentDimension(coreDimInfo) and IsTimeStrikeOrEnum(coreDimInfo.GetDomain()):
            selection = coreDimInfo.GetDimInfoList()[0].GetSelection()

        else:
            
            mChain = coreDimInfo.GetSharedMethodChain()
            
            delim = ''
            if len(mChain) > 0:
                delim = '.'
            
            validCB = coreDimInfo.GetValidationCB()
            dom = coreDimInfo.GetDomain()
            selection = SelectionCtrl(coreDimInfo.GetDimInfoList()[0].GetDimension().DimensionId() + delim + mChain, dom, True, True, validationCB = validCB, methodChain = None)
            
        selections.append([dimensionIdKey, selection])
            
    return CompositeSelectionCtrl( selections )
    
#------------------------------------------------------------------------------
def CoordinatesAsStrings(coordinateObjectsByDimension ):
    coordinatesByDimension = {}
    
    for uniqueId, objects in coordinateObjectsByDimension.iteritems():
        coordinatesByDimension[uniqueId] = [CoordinateAsString( obj ) for obj in objects]
        
    return coordinatesByDimension

#------------------------------------------------------------------------------
def CoordinateAsString( obj ):
    if isinstance( obj, str ):
        return obj
    elif isinstance(obj, numbers.Number):
        return str(obj)
    elif obj.IsKindOf( acm.FTimeBucket ):
        return obj.Spec()
    else:
        return obj.StringKey()

#------------------------------------------------------------------------------
def ComputeCrossProductOfDimensionIdTuples(allDimensionCombinationsList):
    values = [item for item in allDimensionCombinationsList]
    return [MergeDictTuples(comb) for comb in itertools.product(*values)]
    
#------------------------------------------------------------------------------
def MergeDictTuples(tupleOfDicts):
    dict = {}
    for item in tupleOfDicts:
        dict.update(item)
    return dict
    
#------------------------------------------------------------------------------
def SoleDependentDimension(uniqueDimensionId):
    return len( uniqueDimensionId.GetDimInfoList() ) == 1

#------------------------------------------------------------------------------
def IsTimeStrikeOrEnum(domain):
    return domain.IsEnum() or  \
        domain == acm.FTimeBucket or \
        domain == acm.FStrikeBucket
        
#------------------------------------------------------------------------------
def CreateDimensionToSelectionUnitDependenceDictionary(riskFactorCollection):
    selectionCtrlCreatedList = []
    uniqueDimensionIds = {}
    
    for dimension in riskFactorCollection.RiskFactorDimensions():
        domain, methodChain = RiskFactorUtils.GetPersistentDomainAndRemainingMethodChainFromDimension( dimension )
        persistentMethodChain = None 
        
        if dimension.MethodChain() and methodChain:
            persistentMethodChain = dimension.MethodChain().split( methodChain )[0]
            if persistentMethodChain == '':
                persistentMethodChain = None
            elif persistentMethodChain[-1] == '.': 
                persistentMethodChain = persistentMethodChain[:-1]
        elif dimension.MethodChain():
            persistentMethodChain = dimension.MethodChain()

        selectionId = dimension.UniqueId()
        selection = None
        if domain.IsEnum():
            selection = CreateEnumSelection( dimension, domain ) 
        
        elif acm.FTimeBucket == domain:
            selection = CreateTimeBucketsSelection( dimension, domain )
            
        elif acm.FStrikeBucket == domain:
            selection = CreateStrikeBucketsSelection( dimension, domain )
                
        if not dimension.DimensionId() in uniqueDimensionIds.keys():
            
            uniqueDimensionIds[dimension.DimensionId()] = CoreDimensionInformation(dimension.DimensionId(), None, None) 

        dInf = DimensionInformation(dimension, selection, persistentMethodChain) 
        coreDimInfo = uniqueDimensionIds[dimension.DimensionId()]
        coreDimInfo.PushDimInfoList(dInf)

    uniqueDimensionIds = SplitDimensionIdDictionary(uniqueDimensionIds)
    AdjustDimensionDictionaryInformationPerDimensionId(uniqueDimensionIds, riskFactorCollection)
    return uniqueDimensionIds
    
#------------------------------------------------------------------------------
def SplitDimensionIdDictionary(uniqueDimensionIdDict):
    
    extensionDictionary = {}
    uniqueDimensionIdKeysToDelete = set() 
    
    for dimensionIdKey in uniqueDimensionIdDict.keys():
        breakOutBool = False #used for breaking out to outer loop.
        coreDimInfo = uniqueDimensionIdDict[dimensionIdKey]
        dimInfoList = coreDimInfo.GetDimInfoList()
        if len(dimInfoList) <= 1: #keep original dimensionIdKey- value pair. 
            continue
        
        dependencies = []
        itemsIteratedList = []
        
        for item in dimInfoList:
            itemDependenciesList = []
            
            if item in itemsIteratedList:
                continue
                
            else:
                itemDependenciesList.append(item)
                itemsIteratedList.append(item)

            persChain = item.GetPersistentMethodChain()
            
            
            for item_ in dimInfoList:
            
                if item_ in itemsIteratedList: 
                    continue
                    
                persChain_ = item_.GetPersistentMethodChain()
                
                if persChain is None or persChain_ is None:
                    breakOutBool = True
                    break
                    
                if HaveIncommonSubStringFromBeginningOfStrings(persChain, persChain_):
                    itemDependenciesList.append(item_)
                    itemsIteratedList.append(item_)

            if breakOutBool:
                break
                
            dependencies.append(itemDependenciesList)
    
        idx = 0
        if len(dependencies) > 0: #if dependencies exist between dimensions, split up dimensionIdKey- value pair. 
            for listItem in dependencies:
                key_ = dimensionIdKey + str(idx)
                coreDimInfo_ = CoreDimensionInformation(dimensionIdKey, None, None)
                coreDimInfo_.SetDimInfoList( listItem )
                extensionDictionary[key_] = coreDimInfo_
                idx = idx + 1
            
            uniqueDimensionIdKeysToDelete.add(dimensionIdKey)
    
    for dimensionIdKey in uniqueDimensionIdKeysToDelete:
        uniqueDimensionIdDict.pop(dimensionIdKey)
    
    uniqueDimensionIdDict.update(extensionDictionary)
    
    return uniqueDimensionIdDict
    
#------------------------------------------------------------------------------   
def HaveIncommonSubStringFromBeginningOfStrings(string1, string2):
    if len(string1) > len(string2):
        return string1.startswith( string2 )
    else:
        return string2.startswith( string1 )
    
#------------------------------------------------------------------------------
def AdjustDimensionDictionaryInformationPerDimensionId(uniqueDimensionIds, riskFactorCollection):
    for dimensionIdKey in uniqueDimensionIds.keys():

        coreDimInfo = uniqueDimensionIds[dimensionIdKey]
        dimensionList = []
        for dimInfoTuple in coreDimInfo.GetDimInfoList():
            dimensionList.append(dimInfoTuple.GetDimension())

        sharedMethChain = GetSharedMethodChainFractionFromDimensions(dimensionList)
        rfType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
        dom, remMethodChain = RiskFactorUtils.GetPersistentDomainAndRemainingMethodChain(rfType, coreDimInfo.GetDimId(), sharedMethChain)

        for dimInfoTuple in coreDimInfo.GetDimInfoList():
            mc = dimInfoTuple.GetDimension().MethodChain()
            if remMethodChain:
                mc = remMethodChain
            elif mc and sharedMethChain:
                mc = mc.split(sharedMethChain)[1]
                p = mc.find('.')
                if p == 0:
                    mc = mc[1:]
            
            dimInfoTuple.SetMethodChain( mc )

        coreDimInfo.SetDomain( dom ) 
        coreDimInfo.SetSharedMethodChain(sharedMethChain)
        coreDimInfo.SetValidationCB(CreateValidationCallBack( riskFactorCollection, coreDimInfo.GetDimInfoList()[0].GetDimension(),  sharedMethChain))
    
#------------------------------------------------------------------------------
def GetSharedMethodChainFractionFromDimensions(dimensionList):

    mChainList = []
    for dimension in dimensionList:
        mChainList.append(dimension.MethodChain().split('.'))
    
    if len(mChainList) >= 2:
        incommonSequence = CommonSubstringFromStart(mChainList[0], mChainList[1])
        for itemList in mChainList:
            incommonSequence = CommonSubstringFromStart(incommonSequence, itemList)
        incommonString = '.'.join(incommonSequence)
    else:
        incommonString = '.'.join(mChainList[0])
    
    return incommonString
    
#------------------------------------------------------------------------------
def CommonSubstringFromStart(listOfStrings1, listOfstrings2):
    inCommonElementsList = []
    for item1, item2 in zip(listOfStrings1, listOfstrings2):
        if item1 == item2:
            inCommonElementsList.append(item1)
        else:
            break
            
    return inCommonElementsList

#------------------------------------------------------------------------------
def CreateEnumSelection( dimension, domain ):
    enums = domain.EnumeratorStringsSkipFirst()
    return SelectionCtrl( dimension.DisplayName(), domain, True, True, enums )
    
#------------------------------------------------------------------------------
def CreateTimeBucketsSelection( dimension, domain ):
    timeBuckets = RiskFactorTimeBuckets.GetTimeBucketsFromDimensionIfApplicable( dimension )
    return FixedSelectionCtrl( dimension.DisplayName(), domain, True, timeBuckets )

#------------------------------------------------------------------------------
def CreateStrikeBucketsSelection( dimension, domain ):
    storedStrikeBuckets = dimension.CoordinatesSource()
    
    strikeBucketsDefinition = storedStrikeBuckets.StrikeBucketsDefinition()
    strikeBuckets = acm.Risk.CreateStrikeBuckets( strikeBucketsDefinition )
    
    return FixedSelectionCtrl( dimension.DisplayName(), domain, True, strikeBuckets )
    
#------------------------------------------------------------------------------
def CreateAddFromValuationSelection( startingSelection ):        
    selections = []

    selections.append( ['Portfolios', SelectionCtrl( 'Portfolios', acm.FPhysicalPortfolio, True, False)] )
    selections.append( ['Trade filters', SelectionCtrl( 'Trade filters', acm.FTradeSelection, True, False)] )
    
    tradeQueries = acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
    selections.append(['Trade queries', SelectionCtrl( 'Trade queries', acm.FStoredASQLQuery, True, False, tradeQueries)])
        
    return CompositeSelectionCtrl( selections, startingSelection )

#------------------------------------------------------------------------------
def CreateValidationCallBack( riskFactorCollection, dimension, commonMethodChain = None ):

    riskFactorType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
    
    if commonMethodChain:
        rfType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
        domain, _ = RiskFactorUtils.GetPersistentDomainAndRemainingMethodChain(rfType, dimension.DimensionId(), commonMethodChain)

        coreDomain = riskFactorType.DimensionData().At(dimension.DimensionId()).At('Domain')
        if coreDomain != domain:
           return None  
    
        
    dimensionDefinition = riskFactorType.RiskFactorDimensionDefinition( dimension.DimensionId() )
    
    if dimensionDefinition:
        return CreateValidationCallBackFromDimensionDefinition( dimensionDefinition )
        
    #must be a parameter type
    parameterTypeDefinition = acm.ExtensionTools().GetDefaultContext().GetExtension(acm.FRiskFactorParameterType, acm.FObject, dimension.DimensionId()).Value()
    return CreateValidationCallBackFromDimensionDefinition( parameterTypeDefinition )

#------------------------------------------------------------------------------
def CreateValidationCallBackFromDimensionDefinition( dimDef ):
    additionalConstraint = dimDef['AdditionalConstraint']
    
    return acm.GetFunction( additionalConstraint, 1 ) if additionalConstraint else None
