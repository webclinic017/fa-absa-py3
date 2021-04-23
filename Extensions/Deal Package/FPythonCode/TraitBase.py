import traitlets
import acm
from TraitBaseTypes import Str, Float, Int, Object, Date, DatePeriod, Bool, Box, CalcVal, DelegateAttribute, DelegateDealPackage, Action, List, Set, Text, Label, Link
from traitlets import AttributeException
import inspect
from functools import partial
from DealPackageUtil import IsFObject, IsPublicTrait, IsIterable
from AttributeMetaData import base_type_map
from AttributeMetaDataFactory import AttributeMetaDataFactory, AttributeMetaDataKeys
from TraitUtil import AttributeLog, ThrowOrAccumulate

'''******************************** 
TRAIT BASE
********************************''' 

class TraitBase(traitlets.HasTraits):
    """Traits enabled object that exposes metadata and get/setters to acm"""
        
    def __init__(self):        
        traitlets.HasTraits.__init__(self)
        self._log = AttributeLog(self._LogMode())
        self.metaDataFullyInitialized = {}
        self.metaData = {}
        self._metaDataFactory = AttributeMetaDataFactory( self )
        self.InitTraits()
        self._sortedTraitNames = None
    
    @classmethod
    def _LogMode(cls):
        return 'Error'
    
    def Log(self):
        return self._log
    
    def InitTraits(self):
        self.traits()
    
    '''******************************** 
    Meta-Data Access Methods
    ********************************'''
    def _GetOnChanged(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "onChanged")    
    
    def _GetDomain(self, traitName):
        try:
            return self.domainDict[traitName]
        except KeyError:
            domain = self._GetAttributeMetaDataCallback(traitName, "domain")()
            self.domainDict[traitName] = domain
            return domain
        
    def _GetFormatter(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "formatter")()

    def _GetObjMapping(self, traitName):
        return self.trait_metadata(traitName, "objMapping")
    
    def _GetCalcMapping(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "calcMapping")()
        
    def _GetAttributeMapping(self, traitName):
        return self.trait_metadata(traitName, "attributeMapping")
       
    def _GetSolverTopValue(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "solverTopValue")()
    
    def _GetSolverParameter(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "solverParameter")()
    
    def _GetTransform(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "transform")
    
    def _GetLabel(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "label")()
    
    def _GetCalcConfiguration(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "calcConfiguration")()
    
    def _GetRecreateCalcSpaceOnChange(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "recreateCalcSpaceOnChange")()
    
    def _GetNoDealPackageRefreshOnChange(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "noDealPackageRefreshOnChange")()
        
    def _GetAction(self, traitName):
        return self._GetAttributeMetaDataCallback(traitName, "action")
    
    def _GetTrait(self, traitName):
        return self.traits()[traitName]
        
    def _GetExceptionAccumulator(self, traitName):
        return self._GetTrait(traitName).AttributeExceptionAccumulator()
        
    
    '''******************************** 
    UTIL FOR TYPE CHECK
    ********************************'''
    
    def __IsClass(self, traitName, aClass):
        isClass = False
        try:
            trait = self._GetTrait(traitName)
            isClass = trait.__class__ == aClass
        except:
            pass
        return isClass
    
    def _IsCalcVal(self, traitName):
        return self.__IsClass(traitName, CalcVal)
    
    '''******************************** 
    UTIL FOR PARSING METHOD CHAINS
    ********************************'''
    
    def GetCallableMethodsFromChain(self, methodChain, traitName):
        try:
            obj, callableMethod = self._GetCallableObjectAndMethodFromChain(methodChain)
            return self.__GetCallableMethods(obj, callableMethod)
        except AttributeError as e:
            raise AttributeException("%s, %s. Problem in method chain '%s'" % (traitName, str(e), methodChain))
            
    def _GetCallableTraitsFromChain(self, traitName, methodChain, metaName=None):
        try:
            obj, childTraitName = self._GetCallableObjectAndMethodFromChain(methodChain)
            return self.__GetCallableTraits(obj, traitName, childTraitName, metaName)
        except AttributeError as e:
            raise AttributeException("%s, %s. Problem in method chain '%s'" % (traitName, str(e), methodChain))
 
    def __GetObjFromMethod(self, obj, method):
        objects = []
        if IsIterable(obj):
            for objIter in obj:
                objIter = getattr(objIter, method)()
                objects.append(objIter)
            obj = objects
        else:        
            obj = getattr(obj, method)()
        return obj
        
    def __GetCallableMethods(self, obj, callable):
        methods = []
        if IsIterable(obj):
            for objIter in obj:
                map = objIter, getattr(objIter, callable)
                methods.append(map)
        else:
            map = obj, getattr(obj, callable)
            methods.append(map)
        return methods
    
    @ThrowOrAccumulate(None, Exception)
    def __GetAttributeFromChild(self, parentTraitName, childTraitName, childDealPackage):
        # parentTraitName is used by the decorator to log errors
        return childDealPackage.GetAttribute(childTraitName)
    
    def __GetCallableTraits(self, obj, traitName, childTraitName, metaName=None):
        methods = []
        
        def add_methods(obj):
            childHasAttr = obj.HasAttribute(childTraitName)
            if childHasAttr:
                value = self.__GetAttributeFromChild(traitName, childTraitName, obj)
            else:
                self.Log().Verbose("VERBOSE: Delegation failed. Child %s does not contain attribute '%s', and will be ignored." % (str(obj), childTraitName))
                return # Exit
            
            metaCallback = obj.GetAttributeMetaData(childTraitName, metaName) if metaName else None
            map = obj, value, metaCallback
            methods.append(map)
    
        if IsIterable(obj):
            for objIter in obj:
                add_methods(objIter)
        else:
            add_methods(obj)
        return methods
        
    def _GetCallableObjectAndMethodFromChain(self, methodChain):
        obj = self
        chainAsList = methodChain.split(".")
        callableMethod = chainAsList.pop()
        for method in chainAsList:
            obj = self.__GetObjFromMethod(obj, method)
        return obj, callableMethod
        
    '''******************************** 
    MISC - REWRITE
    ********************************'''    
    
    def __IsHiddenTrait(self, traitName):
        return traitName.startswith('_') or\
               self.trait_metadata(traitName, 'noDealPackageRefreshOnChange') or\
               traitName == 'refreshCalcCounter'
    
    def create_sorted_trait_name_list(self):
        """Get sorted list with names of public traits for an obj

        Return [name1, name2 ...]
        """
        return sorted(name for name in self.trait_names()
                      if not self.__IsHiddenTrait(name))    
                      
    def get_trait_names(self):
        if not self._sortedTraitNames:
            self._sortedTraitNames = self.create_sorted_trait_name_list()
        return self._sortedTraitNames
    
    def _GetAttributesInDomains(self, attributes, domains):
        traits = []
        for trait in attributes:
            if self._GetDomain(trait.get_name()) in domains:
                traits.append(trait)
        return traits
        
    def _GetAttributesExcludeDomains(self, attributes, domains):
        traits = []
        for trait in attributes:
            if self._GetDomain(trait.get_name()) not in domains:
                traits.append(trait)
        return traits
        
    def _GetTraitSeqNbrOrdered(self):
        allTraits = self.traits().values()
        allTraits.sort(key=lambda x: x.creation_seqnbr)
        return allTraits
        
    def _GetTraitMetaInfoFromAttributeMapping(self, traitName, metaName):
        typeName = None
        methodChains = self._GetAttributeMapping(traitName)
        validateMapping = True
        if metaName != 'validateMapping':
            validateMapping = self._GetAttributeMetaDataCallback(traitName, 'validateMapping')()
        for chain in methodChains.split("|"):
            map = self._GetCallableTraitsFromChain(traitName, chain, metaName)
            for object, _, traitMetaData in map:
                type = traitMetaData
                if not typeName:
                    typeName = type
                if validateMapping and typeName != type:
                    raise AttributeException("Get attributeMapping metadata failed, diverging values for, " + str(traitName) + ' ' + str(metaName))
        return typeName
    
    def _GetTraitTypeName(self, traitName, trait):
        type_name = None
        if self._GetAttributeMapping(traitName):
            type_name = self._GetTraitMetaInfoFromAttributeMapping(traitName, "type")
        else:
            type_name = base_type_map.get(trait.__class__, None)[0]
            if type_name is None:
                raise AttributeException("Unhandled attribute type: " + str(trait.__class__))
        return type_name
    
    def _AssertPublicTrait(self, obj, traitName):
        if not IsPublicTrait(obj, traitName):
            msg = "%s: Attribute is not a public attribute on %s"
            raise AttributeException(msg % (str(traitName), str(obj)))
    
    def _GetAttributeMetaDataCallback(self, traitName, attrName):
        traitMetaData = self.metaData.setdefault(traitName, {})
        if not traitMetaData.get(attrName, None):
            trait = self._GetTrait(traitName)
            traitMetaData[attrName] = self._metaDataFactory.CreateMetaData(trait, attrName).Callback()
        return traitMetaData[attrName]
        
    def GetAttributeMetaDataKeys(self):
        return AttributeMetaDataKeys()

    def get_trait_value(self, traitName):
        """Get value of a public trait"""
        traitName = str(traitName)
        # We avoid checking type of object for performance reasons, if it doesn't
        # inherit from HasTraits subsequent calls will fail anyway
        
        return getattr(self, traitName)
    
    def GetAttributeOrThrow(self, traitName):
        self._GetTrait(traitName).AttributeExceptionAccumulator().Raise()
        return self.get_trait_value(traitName)
            
    def GetAttributesOrThrow(self):
        return self.get_trait_names()
        
    def GetAttributeMetaDataOrThrow(self, traitName, metaKey):
        return self._GetAttributeMetaDataCallback(traitName, metaKey)
