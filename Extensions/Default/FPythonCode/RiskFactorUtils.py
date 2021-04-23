

import acm
import RiskFactorTimeBuckets

class FilterValues :
    def __init__(self, filterByDimension = {}, filterByAddInfoSpec = {}) :
        self.m_filterByDimension = filterByDimension
        self.m_filterByAddInfoSpec = filterByAddInfoSpec

class FilterControlCollection(object):
    def __init__(self, dimensions, addInfoSpecs, sortingFunctions = {}):
        self.m_dimensions = dimensions
        self.m_addInfoSpecs = addInfoSpecs
        self.m_sortingFunctions = sortingFunctions
        
        self.m_ctrls = {}
        
    def GetFilterValues(self):
        dimensionValues = {}
        addInfoValues = {}

        for dimension in self.m_dimensions:
            dimensionValues[dimension.UniqueId()] = self.m_ctrls[dimension.UniqueId()].GetData()

        for addInfoSpec in self.m_addInfoSpecs:
            addInfoValues[addInfoSpec] = self.m_ctrls[addInfoSpec].GetData()

        return FilterValues(dimensionValues, addInfoValues)
        
    def GetKeys(self):
        return self.m_dimensions

    def PopulateControl(self, ctrl, filters) :
        changed = False
        selection = ctrl.GetData()

        ctrl.Clear()
        ctrl.AddItem('')


        for filter in filters :
            ctrl.AddItem( filter )


        if selection in filters :
            ctrl.SetData(selection)
        elif selection:
            changed = True

        return changed

    def SortFilters(self, dimension, filters):
        sortingFunction = self.m_sortingFunctions.get(dimension.UniqueId(), None)
        filters.sort(key=sortingFunction)

    def PopulateByDimension(self, filterByDimension):
        changed = False
        for dimension, filters in filterByDimension.iteritems() :
            ctrl = self.m_ctrls[dimension.UniqueId()]

            self.SortFilters(dimension, filters)

            if self.PopulateControl(ctrl, filters):
                changed = True
        
        return changed

    def PopulateByAddInfoSpec(self, filterByAddinfoSpec):
        changed = False
        for addInfoSpec, filters in filterByAddinfoSpec.iteritems() :
            ctrl = self.m_ctrls[addInfoSpec]
            if self.PopulateControl(ctrl, filters):
                changed = True

        return changed
        
    def Populate( self, filterByDimension, filterByAddinfoSpec):
        changed = False
        if self.PopulateByDimension(filterByDimension) :
            changed = True
        if self.PopulateByAddInfoSpec(filterByAddinfoSpec) :
            changed = True

        return changed
        
    def HandleCreate( self, layout ):
        dimensionCtrlCount = len(self.m_dimensions)

        for index, dimension in enumerate(self.m_dimensions):
            self.m_ctrls[dimension.UniqueId()] = layout.GetControl( self.GetCtrlName(index) )

        if self.m_addInfoSpecs :
            for index, addInfoSpec in enumerate(self.m_addInfoSpecs) :
                self.m_ctrls[addInfoSpec] = layout.GetControl(self.GetCtrlName(index + dimensionCtrlCount))

    def AddFilterCallback( self, cb ):
        for dimension in self.m_dimensions:
            self.m_ctrls[dimension.UniqueId()].AddCallback('Changed', cb, dimension.UniqueId())

        for addInfoSpec in self.m_addInfoSpecs:
            self.m_ctrls[addInfoSpec].AddCallback('Changed', cb, addInfoSpec)

    def GetCtrlName(self, index) :
        return  'filterCtrl' + str(index)

    def BuildLayout( self, b ):
        dimensionCtrlCount = len(self.m_dimensions)

        b.BeginVertBox()
        b.  BeginHorzBox()

        first = True
        for index, dimension in enumerate(self.m_dimensions):
            if not first :
                b.AddSpace(10)
            first = False
            b.AddOption(self.GetCtrlName(index), dimension.DisplayName(), -1, -1, 'Vertical' )
        if self.m_addInfoSpecs :
            for index, addInfoSpec in enumerate(self.m_addInfoSpecs) :
                b.AddSpace(10)
                b.AddOption(self.GetCtrlName(index + dimensionCtrlCount), addInfoSpec.Name(), -1, -1, 'Vertical')
        b.  EndBox()
        b.  AddSpace(10)
        b.EndBox()


def ValueMapsAsDictionary(riskFactorDimensionSplit):
    valueMapDictionary = None

    if riskFactorDimensionSplit:
        valueMaps = riskFactorDimensionSplit.ValueMaps()
        valueMapDictionary = {}

        for valueMap in valueMaps :
            valueMapDictionary[valueMap.SingleDimensionValue()] = valueMap

    return valueMapDictionary

def clearAddInfo(spec, parent) :
    if spec != None :
        addInfo = spec.AddInfo(parent)
        if addInfo:
            if addInfo.IsClone() :
                addInfo.Unsimulate()
            else:
                addInfo.Delete()


def setAddInfo(spec, parent, value) :
    if spec != None :
        value = acm.DataConversion.VariantToString(spec.DataDomain(), value)
        addInf = spec.AddInfo(parent)

        if addInf:
            addInf.FieldValue(value)
        else:
            addInf = acm.FAdditionalInfo()
            addInf.AddInf(spec)
            addInf.Parent(parent)
            addInf.FieldValue(value)
            addInf.RegisterInStorage()

def FormatAddInfoValue(domain, value) :
    if value != None:
        if str(domain.Name()) == 'bool' :
            if value == True or value == 'Yes' or value == 'true' :
                value = 'Yes'
            else:
                value = 'No'

    return value

def getAddInfo(spec, parent) :
    value = None
    description = None
    
    if spec != None :
        addInf = spec.AddInfo(parent)
        
        if addInf != None :
            value = addInf.FieldValue()
            description = spec.Description()
        
    try:
        value = acm.DataConversion.VariantFromString(spec.DataDomain(), value)
    except RuntimeError as e:
        print ('Failed to get additional info value on field: ' + spec.FieldName())
        value = None
        description = None

    return value, description     

def SetTextSelection(ctrl, startPos, endPos):
    if hasattr(ctrl, 'SetTextSelection') :
        ctrl.SetTextSelection(startPos, endPos)


def OnButtonClicked(self, ad):
    result = acm.UX().Dialogs().SelectStoredASQLQuery(self.m_parent.Shell(), self.m_domain, None)
    if result:
        self.m_items  = result.Query().Select()
        self.m_itemsText.SetData( result.Name()  )
        if self.m_extraCB:
            self.m_extraCB(self)


def DimensionDomainFromRiskFactorType(riskFactorType, dimensionId, methodChain) :
    dimensionData = riskFactorType.DimensionData().At(dimensionId)
    dimensionDomain = None

    if dimensionData :
        dimensionDomain = dimensionData.At(acm.FSymbol('Domain'))
        
    if not dimensionDomain:
        dimensionDomain = riskFactorType.CoordinateNamesAndDomains()[ dimensionId ]

    dimensionDomain= GetMethodDomain(dimensionDomain, methodChain)

    return dimensionDomain


def GetDimensionDomain(dimension):
    riskFactorCollection = dimension.RiskFactorCollection()
    riskFactorType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
        
    return DimensionDomainFromRiskFactorType(riskFactorType, acm.FSymbol(dimension.DimensionId()), dimension.MethodChain())


def GetMethodDomain( dimensionDomain, methodChain ):
    if methodChain:
        resultDomain = None
        pos = methodChain.find('.')
        methodName = methodChain
        if pos != -1:
            methodName = methodChain[:pos]
        
        '''
        If the domain is a set of a persistent class, we want to have the set elements. 
        otherwise the method may not be found.
        '''
        if dimensionDomain.ElementDomain().Name() != acm.FSymbol('void'):
            dimensionDomain = dimensionDomain.ElementDomain()

        method = dimensionDomain.GetMethod( methodName, 0 )
        if method:
            if pos != -1:
                resultDomain = GetMethodDomain( method.Domain(), methodChain[pos + 1:])
            else:
                resultDomain = method.Domain()
        else:
            for subClass in dimensionDomain.Subclasses():
                resultDomain = GetMethodDomain( subClass, methodChain[pos + 1:])
                if resultDomain:
                    break
            #print ('No method ' + methodName + ' on domain ' + dimensionDomain.Name())
    else:
        resultDomain = dimensionDomain
    return resultDomain 


def GetPersistentDomainAndRemainingMethodChainFromDimension(dimension):
    riskFactorCollection = dimension.RiskFactorCollection()
    riskFactorType = acm.RiskFactor().RiskFactorType( riskFactorCollection.RiskFactorType() )
        
    return GetPersistentDomainAndRemainingMethodChain(riskFactorType, acm.FSymbol(dimension.DimensionId()), dimension.MethodChain())


def GetPersistentDomainAndRemainingMethodChain(riskFactorType, dimensionId, methodChain):
    dimensionData = riskFactorType.DimensionData().At(dimensionId)
    dimensionDomain = None

    if dimensionData :
        dimensionDomain = dimensionData.At(acm.FSymbol('Domain'))
        
    if not dimensionDomain:
        dimensionDomain = riskFactorType.CoordinateNamesAndDomains()[ dimensionId ]
    
    resultChain = None
    resultChain = methodChain
    mChain = ''
    prevDom = dimensionDomain 
    delimitor = '.'
    i = 0 
    
    while i < len(methodChain.split('.')):
        pos = resultChain.find('.')
        
        if len(mChain) > 0:
            delimitor = '.'
        else:
            delimitor = ''
        
        if pos != -1:
            mChain = mChain + delimitor + resultChain[:pos]
            resultChain = resultChain[pos+1:]
        else:
            mChain = mChain + delimitor + resultChain

        retDom = GetMethodDomain(dimensionDomain, mChain)

        if not ( isinstance(retDom, type(acm.FPersistentClass)) or (retDom and retDom.IsEnum()) ):
            if isinstance(prevDom, type(acm.FAdditionalInfoProxy)):
                #Backup two steps in methodChain, extend resultChain accordingly.
                splitMChain = mChain.split('.')
                mChain = '.'.join(splitMChain[:-2])
                resultChain = '.'.join(splitMChain[-2:])
                retDom = GetMethodDomain(dimensionDomain, mChain)
                break
            retDom = prevDom
            break 
        else: 
            prevDom = retDom
            if pos == -1:
                if resultChain == mChain[mChain.rfind('.')+1:]:
                    resultChain = None 
                break
        i = i + 1
    return retDom, resultChain 
    

def IsAddInfoSpecDomain(addInfoSpec, domainName) :
    return addInfoSpec.DataDomain().Name() == acm.FSymbol(domainName)

def GetAddInfoSpecs(riskFactorCollection, addInfoRecType, onlyBool) :
    addInfoSpecs = []

    if riskFactorCollection :
        riskFactorSetup = riskFactorCollection.RiskFactorSetup()
        addInfoSpecs = GetAddInfoSpecsFromRiskFactorSetup(riskFactorSetup, addInfoRecType, onlyBool)

    return addInfoSpecs

def GetAddInfoSpecsFromRiskFactorSetup(riskFactorSetup, addInfoRecType, onlyBool) :
    addInfoSpecs = []
    allAddInfoSpecs = acm.FAdditionalInfoSpec.Select('recType=' + addInfoRecType)

    for addInfoSpec in allAddInfoSpecs:
        if addInfoSpec.Mandatory() :
            if IsAddInfoSpecDomain(addInfoSpec, 'bool') or not onlyBool:
                addInfoSpecs.append(addInfoSpec)

    if riskFactorSetup :
        riskFactorPropertySpecifications = riskFactorSetup.RiskFactorPropertySpecifications()

        for index, riskFactorPropertySpecification in enumerate(riskFactorPropertySpecifications) :
            addInfoSpec = riskFactorPropertySpecification.AdditionalInfoSpec()
            if addInfoSpec.RecType() == addInfoRecType :
                if  IsAddInfoSpecDomain(addInfoSpec, 'bool') or not onlyBool:
                    if addInfoSpec not in addInfoSpecs :
                        addInfoSpecs.append(addInfoSpec)

    return addInfoSpecs

def GetRiskFactorInstanceKey(instance) :
    key = ''

    riskFactorCollection = instance.RiskFactorCollection()

    if riskFactorCollection :
        key = riskFactorCollection.RiskFactorType()
        
        riskFactorDimension = riskFactorCollection.RiskFactorDimensions()

        for dimension in riskFactorDimension :
            key += instance.CoordinateValue( dimension )

    return key
    
def GetRiskFactorInstanceKeyFromDict( riskFactorCollection, riskFactorDict ):
    key = riskFactorCollection.RiskFactorType()
    
    riskFactorDimension = riskFactorCollection.RiskFactorDimensions()

    for dimension in riskFactorDimension:
        key += riskFactorDict[dimension.UniqueId()]

    return key

def GetEnumValueAsString(dataGroupName, dataEnumValue) :
    enumerator = None
    
    if dataGroupName == 'Standard' :
        enumerator = acm.FEnumeration['enum(B92StandardType)']
    elif dataGroupName == 'Enum' :
        enumerator = acm.FEnumeration['enum(B92EnumType)']
    elif dataGroupName == 'RecordRef' :
        enumerator = acm.FEnumeration['enum(B92RecordType)']

    enumName = None
    if enumerator :
        enumName = enumerator.Enumerator(dataEnumValue)

    return enumName

#------------------------------------------------------------------------------
# Supported Risk Factors
#------------------------------------------------------------------------------
s_supportedRiskFactorMappingTypes = [ 'Dividend', 'Commodity', 'Volatility', 'Zero Coupon', 'FX', 'Equity', 'Par CDS Rate', 'Stored Instrument Spread', 'Benchmark Volatility', 'Volatility Skew Parameters (SVI)', 'Equity Repo Rate', 'Benchmark Price', 'Inflation Benchmark Price', 'Inflation Rate']


#------------------------------------------------------------------------------
# Risk Factor Domain Sorting
#------------------------------------------------------------------------------
def CreateSortersForCollection( riskFactorCollection ):
    sorterByDimension = {}

    for dimension in riskFactorCollection.RiskFactorDimensions():
        domain = GetDimensionDomain( dimension )
    
        if acm.FTimeBucket == domain:
            sorterByDimension[dimension.UniqueId()] = TimeBucketSorter( dimension )
        elif acm.FStrikeBucket == domain:
            sorterByDimension[dimension.UniqueId()] = StrikeBucketSorter()
    
    return sorterByDimension

#------------------------------------------------------------------------------
# Time Bucket sorter
#------------------------------------------------------------------------------
class TimeBucketSorter( object ):
    
    def __init__( self, dimension ):
        timeBuckets = RiskFactorTimeBuckets.GetTimeBucketsFromDimensionIfApplicable( dimension )
        
        self.m_indexByTimeBucketName = RiskFactorTimeBuckets.GetIndexByTimeBuckets( timeBuckets )
        
    def __call__( self, timeBucketName ):
        return self.m_indexByTimeBucketName[timeBucketName]

#------------------------------------------------------------------------------
# Strike Bucket sorter
#------------------------------------------------------------------------------
class StrikeBucketSorter( object ):
    
    def __call__( self, strikeBucketValue ):
        return float( strikeBucketValue )
