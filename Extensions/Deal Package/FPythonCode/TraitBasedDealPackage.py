import acm
import TraitBase
import inspect
from TraitBase import IsFObject, TraitBase, Date, DatePeriod, Str, Object, Float, Bool, Box, Int, CalcVal, List, Set, Action, Text, Label, Link, DelegateAttribute, DelegateDealPackage
from DealPackageCalculations import DealPackageCalculations
from TraitDomainAndValueValidator import TraitDomainAndValueValidator
from DealPackageUtil import DealPackageException, IsFObject, IsPublicTrait, StringKeyOrVal, FormatException, ObjMappingSplitter, MergeMetaDataStrings, IsCallable
from TraitUtil import AttributeException, ThrowOrAccumulate
from CompositeAttributeBase import CompositeAttributeBase
from AttributeMetaDataFactory import ValidAttributeMetaDataKeys, MetaDataMergePossible
from traitlets import getmembers, TraitType
from CompositeAttributeBase import CompositeAttributeBase
from collections import OrderedDict
import copy

class NotImplemented():
    pass
    
NOT_IMPLEMENTED = NotImplemented()

def Delegate(*args, **kwargs):
    if 'attributeMapping' in kwargs and len(kwargs['attributeMapping'].split('.')) == 1:
        return DelegateDealPackage(*args, **kwargs)
    else:
        return DelegateAttribute(*args, **kwargs)
    
class ValidationExceptionAccumulator(object):
    def __init__(self):
        self._errors = []
    def __call__(self, error):
        self.ValidationError(error)
    def ValidationError(self, error):
        self._errors.append(error)
    def ValidationResult(self):
        return self._errors if len(self._errors) > 0 else True

class MuteParentDealPackageDelegateUpdates(object):
    def __init__(self, dealPackageBase):
        self._dealPackageBase = dealPackageBase
        self._prev = self._dealPackageBase._muteParentNotifications
    def __enter__(self):
        self._dealPackageBase._muteParentNotifications = True
    def __exit__(self, type, value, traceback):
        self._dealPackageBase._muteParentNotifications = self._prev

class MuteParentDealPackageDelegateUpdatesOnCopyAndOpen(object):
    def __init__(self, dealPackageBase):
        self._dealPackageBase = dealPackageBase
        self._prev = self._dealPackageBase._muteParentNotificationsOnCopyAndOpen
    def __enter__(self):
        self._dealPackageBase._muteParentNotificationsOnCopyAndOpen = True
    def __exit__(self, type, value, traceback):
        self._dealPackageBase._muteParentNotificationsOnCopyAndOpen = self._prev

class MuteNotificationsWithSafeExit(object):
    def __init__(self, dealPackageBase):
        self._dealPackageBase = dealPackageBase
        self._prev = self._dealPackageBase._muteNotifications
    def __enter__(self):
        self._dealPackageBase._muteNotifications = True
    def __exit__(self, type, value, traceback):
        self._dealPackageBase._muteNotifications = self._prev
 
class RegisterAllObjMappingsOnNewWithSafeExit(object):
    def __init__(self, dealPackageBase, newFromInstrumentPackage):
        self._dealPackageBase = dealPackageBase
        self._newFromInstrumentPackage = newFromInstrumentPackage
        self._prev = self._dealPackageBase._registeringAllObjMappingsOnNew
    def __enter__(self):
        self._dealPackageBase._registeringAllObjMappingsOnNew = True
    def __exit__(self, type, value, traceback):
        if type: return False # re-raise exception
        
        self._dealPackageBase._registeringAllObjMappingsOnNew = self._prev
        self._dealPackageBase._RegisterAllCalculations()
        self._dealPackageBase._RegisterAllObjectMappingDefaultValues(self._newFromInstrumentPackage)
        self._dealPackageBase._RegisterAllCalcValSolverDefaultValues()
        self._dealPackageBase._RegisterAllObjectMappings()
        self._dealPackageBase.DealPackage().Refresh()
   
class ApplyTraitChangeAndCallObjMappingSetMethodWithSafeExit(object):
    def __init__(self, dealPackageBase):
        self._dealPackageBase = dealPackageBase
        self._prev = self._dealPackageBase._applyTraitChangeAndCallObjMappingSetMethod
    def __enter__(self):
        self._dealPackageBase._applyTraitChangeAndCallObjMappingSetMethod = False
    def __exit__(self, type, value, traceback):
        self._dealPackageBase._applyTraitChangeAndCallObjMappingSetMethod = self._prev
        
class SetSolverParametersWithSafeExit(object):
    def __init__(self, dealPackageBase, topValue = None, parameter = None, value = None):
        self._dealPackageBase = dealPackageBase
        self._solverTopValue = dealPackageBase.solverTopValue
        self._solverParameter = dealPackageBase.solverParameter
        self._solverValue = dealPackageBase.solverValue
        self._topValue = topValue
        self._parameter = parameter
        self._value = value
    def __enter__(self):
        with MuteNotificationsWithSafeExit(self._dealPackageBase):
            if self._topValue:
                self._dealPackageBase.solverTopValue = self._topValue
            if self._parameter:
                self._dealPackageBase.solverParameter = self._parameter
            if self._value is not None:
                self._dealPackageBase.solverValue = self._value
    def __exit__(self, type, value, traceback):
        with MuteNotificationsWithSafeExit(self._dealPackageBase):
            self._dealPackageBase.solverTopValue = self._solverTopValue
            self._dealPackageBase.solverParameter = self._solverParameter
            self._dealPackageBase.solverValue = self._solverValue
     
class TraitBasedDealPackage(TraitBase):
    
    ONCHANGED_MODE = 1
    
    def __init__(self, dealPackage):
        TraitBase.__init__(self)
        self._dealPackage = dealPackage
        self.on_obj_mapping_trait_change(self.__OnObjectMappingTraitChange)
        self.on_trait_change(self.__OnAnyTraitChange)
        self._validator = TraitDomainAndValueValidator(self)
        self._dealPackageCalculations = None
        self._calculationsRegistered = False
        self._isSolverDealPackage = False
        self._muteParentNotifications = False
        self._muteParentNotificationsOnCopyAndOpen = False
        self._compositeAttributes = OrderedDict()
        self._updatedTraits = {}
        self.OnInit()
        
    def __Validator(self):
        return self._validator
    
    def DealPackage(self):
        return self._dealPackage
        
    def InstrumentPackage(self):
        return self.DealPackage().InstrumentPackage()
    
    def HandleNoDefaultValue(self, attrName):
        if self._GetObjMapping(attrName):
            methodChains = self._GetObjMapping(attrName)
            self._UpdateTraitValuesCache(attrName, methodChains)
        
    '''******************************** 
    CALCULATION SPACE
    ********************************''' 
    def _GetCalcSpace(self, sheetType = "FDealSheet"):
        return self._dealPackageCalculations.CalcSpace(sheetType)
                
    def _GetStdCalcSpace(self):
        return acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
 
    
    '''******************************** 
    METHODS TO EXTRACT DEAL PACKAGE PARTS
    ********************************''' 
    def __DealPackageInstrumentPartImpl(self, dealPackage, name):
        try:
            return dealPackage.InstrumentAt(name)
        except Exception as e:
            raise DealPackageException("Deal Package instrument part " + name + " missing")
            
    def InstrumentAt(self, name):
        return self.__DealPackageInstrumentPartImpl(self.DealPackage(), name)
            
    def __DealPackageTradePartImpl(self, dealPackage, name):
        try:
            return dealPackage.TradeAt(name)
        except Exception as e:
            raise DealPackageException("Deal Package trade part " + name + " missing")
            
    def TradeAt(self, name):
        return self.__DealPackageTradePartImpl(self.DealPackage(), name)
       
    def CombinationMapAt(self, name, combinationKey = None):
        try:
            return self.DealPackage().CombinationMapAt(name, combinationKey)
        except Exception as e:
            raise DealPackageException("Deal Package combination map part " + name + " missing")

    def B2BTradeParamsAt(self, name):
        try:
            b2bParams = self.DealPackage().B2BTradeParamsAt(name)
            b2bParams.Refresh()
            return b2bParams
        except Exception as e:
            raise DealPackageException("Deal Package B2B part " + name + " missing. " + str(e))
            
    def DeltaHedgeParamsAt(self, name):
        try:
            deltaHedgeParams = self.DealPackage().DeltaHedgeParamsAt(name)
            return deltaHedgeParams
        except Exception as e:
            raise DealPackageException("Deal Package Delta Hedge part " + name + " missing")
    
    def PremiumTranslationParamsAt(self, name):
        try:
            premiumTranslationParams = self.DealPackage().PremiumTranslationParamsAt(name)
            return premiumTranslationParams
        except Exception as e:
            raise DealPackageException("Deal Package Premium Translation part " + name + "missing ")
            
    def ChildDealPackageAt(self, name):
        try:
            return self.DealPackage().ChildDealPackageAt(name)
        except Exception as e:
            raise DealPackageException("Deal Package Child part " + name + " missing")

    def Trades(self):
        return self.DealPackage().Trades()
        
    def Instruments(self):
        return self.DealPackage().Instruments()
        
    def Confirmations(self):
        return self.DealPackage().Confirmations()    
        
    def Settlements(self):
        return self.DealPackage().Settlements()    
    
    def ChildDealPackages(self):
        return self.DealPackage().ChildDealPackages()
    
    def LifeCyclePackages(self):
        return self.DealPackage().LifeCyclePackages()
    
    def OpeningDealPackages(self):
        return self.DealPackage().OpeningDealPackages()
        
    def LiveTrades(self):
        return list(filter( self.DealPackage().IsLiveTrade, self.DealPackage().Trades() ))

    '''******************************** 
    TRAIT MAPPINGS (INTERNAL METHODS)
    ********************************'''   
    def __ApplyAttributeMappingChange(self, traitName, newValue):
        traitMethodChain = self._GetAttributeMapping(traitName)
        if traitMethodChain:
            for chain in traitMethodChain.split("|"):
                map = self._GetCallableTraitsFromChain(traitName, chain)
                for object, traitValue, _ in map:
                    if not self._TraitValuesAreEqual(newValue, traitValue):
                        mapTraitName = self.__GetTraitNameFromChain(chain)
                        object.SetAttribute(mapTraitName, newValue)
            if self.ONCHANGED_MODE == 2:
                self.__OnObjectMappingTraitChange(traitName, None, None, None)

    def __GetTraitNameFromChain(self, chain):
        return chain.split(".")[-1]
    
    @ThrowOrAccumulate(None, Exception)
    def _GetAttrValueFromChain(self, traitName, traitMethodChain):
        val = None
        for chain in traitMethodChain.split("|"):
            map = self._GetCallableTraitsFromChain(traitName, chain)
            for object, traitValue, _ in map:
                if not val:
                    val = traitValue
                if not self._TraitValuesAreEqual(val, traitValue):
                    if self.GetAttributeMetaData(traitName, 'validateMapping')():
                        error = "Value cannot be set, diverging values for, "
                        raise AttributeException(error + str(traitName))
                    else:
                        return None #Early exit on mismatch
        return val
        
    @ThrowOrAccumulate(None, Exception)
    def __GetAttrValueFromInstrumentPartOfChain(self, traitName):
        traitMethodChain = self._GetAttributeMapping(traitName)
        insPartOfChain = []
        for chain in traitMethodChain.split("|"):
            map = self._GetCallableTraitsFromChain(traitName, chain, 'objMapping')
            for object, traitValue, objMapping in map:
                objMapping = objMapping()
                if isinstance(objMapping, ObjMappingSplitter) and objMapping._GetInstrumentPart():
                    insPartOfChain.append(objMapping)
        return self._GetAttrValueFromChain('|'.join(insPartOfChain))
    
    def _IsDelegatable(self, traitName, traitMethodChain):
        isDelegatable = True
        if self._GetCalcMapping(traitName):
            count = 0
            for chain in traitMethodChain.split("|"):
                map = self._GetCallableTraitsFromChain(traitName, chain)
                count += len(map)
                if count > 1:
                    return False
            isDelegatable = count == 1
            if isDelegatable:
                val = self._GetAttrValueFromChain(traitName, traitMethodChain)
                if val == None:
                    isDelegatable = False
        return isDelegatable
        
    def _DelegateAttributeMappingDefaultValuesToParent(self):
        with ApplyTraitChangeAndCallObjMappingSetMethodWithSafeExit(self):
            for traitName in self._GetTraitNames():
                traitMethodChain = self._GetAttributeMapping(traitName)
                if traitMethodChain:
                    if self._IsDelegatable(traitName, traitMethodChain):
                        val = self._GetAttrValueFromChain(traitName, traitMethodChain)
                        #Throw if attributes differ
                        self._GetTrait(traitName).AttributeExceptionAccumulator().Raise()
                        self._ApplyValueToTrait(traitName, val, silent=self._GetCalcMapping(traitName))

    def _DelegateAttributeMappingValuesToChildren(self):
        with MuteParentDealPackageDelegateUpdates(self):
            for traitName in self._GetTraitNames():
                traitMethodChain = self._GetAttributeMapping(traitName)
                if traitMethodChain:
                    if not self._GetCalcMapping(traitName):
                        self.__ApplyAttributeMappingChange(traitName, self.get_trait_value(traitName))
                    
    def __RegisterAllAttributeMappings(self):
        self._DelegateAttributeMappingDefaultValuesToParent()
              
    '''******************************** 
    OBJECT MAPPINGS (INTERNAL METHODS)
    ********************************'''            
    def _ApplyValueToTrait(self, traitName, value, silent=False):
        if value != "NoVal":
            self.SetAttribute(traitName, value, silent)
    
    def _ParseValueToCorrectDomainValue(self, traitName, domain, newValue):
        return self.__Validator().GetValueFromParseDomainValue(traitName, domain, newValue)

    def _GetObjectMappingValueAndValidateEqual(self, traitName, methodChains):
        objectValue = "NoVal"
        validationVal = "NoVal"
        for chain in methodChains.split("|"):
            objAndMethods = self.GetCallableMethodsFromChain(chain, traitName)
            for callObject, callableMethod in objAndMethods:
                objectValue = callableMethod()
                domain = self.__Validator().TraitBasedDealPackage()._GetDomain(traitName)
                if domain.IsKindOf(acm.FTimeDomain):
                    objectValue = acm.Time().DateTimeFromTime(objectValue)
                try:
                    validationVal = self.__Validator().ValidateGetTraitValue(traitName, chain, callableMethod, objectValue, validationVal)
                except AttributeException:
                    if self.GetAttributeMetaData(traitName, 'validateMapping')():
                        raise
                    else:
                        return None #Early exit on mismatch
        return objectValue
    
    @ThrowOrAccumulate(True, AttributeException)
    def _UpdateTraitValuesCache(self, traitName, methodChains):
        self._GetTrait(traitName).dirty = False
        objectValue = self._GetObjectMappingValueAndValidateEqual(traitName, methodChains)
        if objectValue != "NoVal":
            self._trait_values[traitName] = objectValue
 
    @ThrowOrAccumulate(["NoVal", None], AttributeException)
    def __TraitValueFromObjMappingIfValueHasChanged(self, traitName, methodChains):
        currentVal = self.get_trait_value(traitName)
        updatedVal = self._GetObjectMappingValueAndValidateEqual(traitName, methodChains)

        if not self._TraitValuesAreEqual(updatedVal, currentVal):
            newVal = updatedVal
        else:
            newVal = "NoVal" # No new value, value has not changed.
        return newVal, currentVal
                
    def __FindAllOtherTraitsAffectedByTheTraitChange(self, userInputTraitName):
        traitsAffectedByChange = {}
        recreateCalcSpaceOnChangeIsCalled = (not self._calculationsRegistered) or self._GetRecreateCalcSpaceOnChange(userInputTraitName)
        #print('PERFORMANCE_UserInput', userInputTraitName, recreateCalcSpaceOnChangeIsCalled)
        for traitName in self._GetTraitNames():
            methodChains = self._GetObjMapping(traitName)
            if methodChains:
                if self.ONCHANGED_MODE == 2 or self.HasOnChanged(traitName) or (not recreateCalcSpaceOnChangeIsCalled and self._GetRecreateCalcSpaceOnChange(traitName)):
                    newTraitValue, oldTraitValue = self.__TraitValueFromObjMappingIfValueHasChanged(traitName, methodChains)
                    #print('PERFORMANCE_CheckIfValuesHaveChanged', traitName)
                    if newTraitValue != "NoVal":
                        traitsAffectedByChange[traitName] = (newTraitValue, oldTraitValue)
                else:
                    self._GetTrait(traitName).set_dirty()
        return traitsAffectedByChange
    
    def _ApplyLatestValueFromObjMapping(self, traitName):
        methodChains = self._GetObjMapping(traitName)
        if methodChains:
            self._UpdateTraitValuesCache(traitName, methodChains)
    
    def _UpdateAndRegisterAllObjectMappings(self, userInputTraitName):
        if self.ONCHANGED_MODE == 0:
            for traitName in self._GetTraitNames():
                methodChains = self._GetObjMapping(traitName)
                if methodChains:
                    self._GetTrait(traitName).set_dirty()
        else:
            if not self._isSolverDealPackage:
                with ApplyTraitChangeAndCallObjMappingSetMethodWithSafeExit(self):
                    self._updatedTraits = self.__FindAllOtherTraitsAffectedByTheTraitChange(userInputTraitName)
                    with MuteNotificationsWithSafeExit(self):
                        for traitName in self._updatedTraits.iterkeys():
                            self._ApplyValueToTrait(traitName, self._updatedTraits.get(traitName)[0])
                self.__SendNotifications(userInputTraitName, self._updatedTraits)
       
    def _ValidateTraits(self, accumulator):
        for traitName in self._GetTraitNames():
            trait = self._GetTrait(traitName)
            trait.TraitIsValid(self, accumulator)
            
    def _RegisterAllObjectMappings(self):
        with ApplyTraitChangeAndCallObjMappingSetMethodWithSafeExit(self):
            for trait in self._GetTraitSeqNbrOrdered():
                traitName = trait.get_name()
                methodChains = self._GetObjMapping(traitName)
                if methodChains:
                    self._UpdateTraitValuesCache(traitName, methodChains)
                    
    def _ValidateAndSetTraitValueToObjMapping(self, traitName, callableMethod, callObject, newValue, doReturnVal):
        objectValue = None
        if self.__Validator().ValidateNewValueInDomainOfCallableMethod(traitName, callObject, newValue):
            try:
                # Todo handle, diverging results 
                callableMethod(newValue)
            except Exception as e:
                raise DealPackageException("'%s' not a valid value for attribute '%s'. %s" % (str(newValue), traitName, str(e)))
        
        if doReturnVal:
            objectValue = callableMethod()
            domain = self.__Validator().TraitBasedDealPackage()._GetDomain(traitName)
            if domain.IsKindOf(acm.FTimeDomain):
                objectValue = acm.Time().DateTimeFromTime(objectValue)
    
        return objectValue
        
    def _AssignValueToObjMappingMethodChain(self, traitName, methodChains, newValue, doReturnVal = True):
        val = "NoVal"
        for chain in methodChains.split("|"):
            methods = self.GetCallableMethodsFromChain(chain, traitName)
            for callObject, callableMethod in methods:
                val = self._ValidateAndSetTraitValueToObjMapping(traitName, callableMethod, callObject, newValue, doReturnVal)
        return val
        
    def __ApplyTraitValueToObjMapping(self, traitName, newValue):
        methodChains = self._GetObjMapping(traitName)
        if methodChains:
            self._AssignValueToObjMappingMethodChain(traitName, methodChains, newValue, False)

    def __GetDefaultValue(self, trait):
        defaultValue = trait.get_default_value()
        defaultValue = trait.transform(self, defaultValue)
        return defaultValue

    def _RegisterObjectMappingDefaultValues(self, traits, newFromInstrumentPackage):
        for trait in traits:
            if trait.has_explicit_default_value():
                try:
                    defaultValue = self.__GetDefaultValue(trait)
                    if self._GetObjMapping(trait.get_name()):
                        self.__SetDefaultOnObjMapping(trait.get_name(), defaultValue, newFromInstrumentPackage)
                    else:
                        if newFromInstrumentPackage and self._GetAttributeMapping(trait.get_name()):
                            insAttrMappingValue = self.__GetAttrValueFromInstrumentPartOfChain(trait.get_name())
                            if insAttrMappingValue != "NoVal":
                                defaultValue = insAttrMappingValue
                        setattr(self, trait.get_name(), defaultValue)
                except Exception as e:
                    msg = "Default value for attribute '%s': '%s'" % (trait.get_name(), e)
                    if self._registeringAllObjMappingsOnNew:
                        self.Log().Verbose(msg)
                    else:
                        self.Log().Error(msg)

    def __SetDefaultOnObjMapping(self, traitName, defaultValue, newFromInstrumentPackage):
        objMapping = self._GetObjMapping(traitName)
        insStringPart = objMapping._GetInstrumentPart() if isinstance(objMapping, ObjMappingSplitter) else None
        if newFromInstrumentPackage and insStringPart:
            val = self._GetObjectMappingValueAndValidateEqual(traitName, insStringPart)
            if objMapping._GetDealPart():
                self._AssignValueToObjMappingMethodChain(traitName, objMapping._GetDealPart(), val, False)
        else:
            if self.__Validator().ValidateNewValueInDomainOfCallableMethod(traitName, self.DealPackage(), defaultValue):
                self.__ApplyTraitValueToObjMapping(traitName, defaultValue)

    def _RegisterDefaultValuesInOtherDomains(self, attributes, newFromInstrumentPackage):
        domains = [acm.GetDomain('date'), acm.GetDomain('datetime'), acm.GetDomain('double')]
        traits = self._GetAttributesExcludeDomains(attributes, domains)
        self._RegisterObjectMappingDefaultValues(traits, newFromInstrumentPackage)
        
    def _RegisterDefaultValuesInDateDomains(self, attributes, newFromInstrumentPackage):
        domains = [acm.GetDomain('date'), acm.GetDomain('datetime')]
        traits = self._GetAttributesInDomains(attributes, domains)
        self._RegisterObjectMappingDefaultValues(traits, newFromInstrumentPackage)

    def _RegisterDefaultValuesInDoubleDomain(self, attributes, newFromInstrumentPackage):
        domains = [acm.GetDomain('double')]
        traits = self._GetAttributesInDomains(attributes, domains)
        self._RegisterObjectMappingDefaultValues(traits, newFromInstrumentPackage)
       
    def _RegisterAllCalcValSolverDefaultValues(self):
        domains = [acm.GetDomain(acm.FCalculation)]
        allAttributes = self._GetTraitSeqNbrOrdered()
        for trait in self._GetAttributesInDomains(allAttributes, domains):
            if trait.has_explicit_default_value() and self._GetSolverTopValue(trait.get_name()):
                try:
                    setattr(self, trait.get_name(), trait.get_default_value())
                except Exception as e:
                    self.Log().Verbose(e)
                    
    def _RegisterAllObjectMappingDefaultValues(self, newFromInstrumentPackage):
        attributes = self._GetTraitSeqNbrOrdered()
        self._RegisterDefaultValues( attributes, newFromInstrumentPackage )
    
    def _RegisterDefaultValues(self, attributes, newFromInstrumentPackage=False):
        #Default Values should be applied to Traits in order:
        #  - Starting with all domains where order is not important
        #  - Date domains default values should be applied after that (to make sure calendars etc are set before)
        #  - At last doubles should be set, these might be dependent on dates (e.g. par rate calculations)
        self._RegisterDefaultValuesInOtherDomains( attributes, newFromInstrumentPackage )
        self._RegisterDefaultValuesInDateDomains( attributes, newFromInstrumentPackage )
        self._RegisterDefaultValuesInDoubleDomain( attributes, newFromInstrumentPackage )
        
    def __RegisterAllActionMethods(self):
        with MuteNotificationsWithSafeExit(self):
            for traitName in self.trait_names():
                trait = self._GetTrait(traitName)
                if trait.__class__ == Action:
                    method = self._GetAction(traitName)
                    trait.SetAction(self, method)
    
    def RestoreDefaultValues(self, *attributeNames):
        attributes = []
        for attr in self._GetTraitSeqNbrOrdered():
            if attr.get_name() in attributeNames:
                attributes.append(attr)
        
        self._RegisterDefaultValues( attributes )
    
    '''******************************** 
    CALCULATION MAPPINGS (EXTERNAL METHODS)
    ********************************'''
    
    def CreateCalculation(self, name, calcInfo, configurationCb = None):
        if name in self.GetAttributes():
            raise DealPackageException("CreateCalculation - The name '%s' is an attribute on the deal package" % name)
        self.__CreateCalculation(name, calcInfo, configurationCb)
    
    def RemoveCalculation(self, name):
        if name in self.GetAttributes():
            raise DealPackageException("RemoveCalculation - The name '%s' is an attribute on the deal package" % name)
        self._dealPackageCalculations.RemoveCalculation(name)
        
    def SimulateCalculation(self, name, newValue):
        self._dealPackageCalculations.SimulateValue(name, newValue)
        
    def IsCalculationSimulated(self, name):
        return self._dealPackageCalculations.IsSimulated(name)
    
    def GetSimulatedCalculationValue(self, name):
        return self._dealPackageCalculations.SimulatedValue(name)
        
    def GetCalculation(self, name):
        return self._dealPackageCalculations.Value(name)
        
    def RemoveAllSimulations(self):
        self._dealPackageCalculations.RemoveAllSimulations()

    '''******************************** 
    CALCULATION MAPPINGS (INTERNAL METHODS)
    ********************************'''
        
    def _GetCalcSpecFromTraitInfo(self, calcInfo):
        calcSpace = None
        columnIdCb = None
        calcObjName, sheetType, columnId = calcInfo.split(":")
        if calcObjName:
            calcObjCb = getattr(self, calcObjName)
        if columnId:
            if IsCallable(self, columnId):
                columnIdCb = getattr(self, columnId)
                columnId = None
        return calcObjCb, columnId, columnIdCb, sheetType   
    
    def __CreateCalculation(self, name, calcInfo, configurationCb):
        calcObjCb, columnId, columnIdCb, sheetType = self._GetCalcSpecFromTraitInfo(calcInfo)
        self._dealPackageCalculations.CreateCalculation(name, calcObjCb, sheetType, columnId, columnIdCb, configurationCb)
    
    def __CreateTraitCalculation(self, traitName, calcInfo):
        trait = self._GetTrait(traitName)
        if not trait.__class__ == CalcVal:
            raise DealPackageException("When using calcMapping, the attribute class should be CalcVal")
        configurationCb = self._GetAttributeMetaDataCallback(traitName, "calcConfiguration")
        self.__CreateCalculation(traitName, calcInfo, configurationCb)
                
    def __UpdateCalculations(self, doCreate):
        for traitName in self._GetTraitNames():
            calcInfo = self.GetAttributeMetaData(traitName, 'calcMapping')()
            if calcInfo and not self.GetAttributeMetaData(traitName, 'attributeMapping')():
                if doCreate:
                    self.__CreateTraitCalculation(traitName, calcInfo)
                value = self.GetCalculation(traitName)
                trait = self._GetTrait(traitName)
                trait.SetCalculation(self, value)

    def _RegisterAllCalculations(self):
        if not self._calculationsRegistered:
            with MuteNotificationsWithSafeExit(self):
                if self._dealPackageCalculations:
                    self._dealPackageCalculations.RegisterCalculations()
                    self.__UpdateCalculations(False)
                else:
                    self._dealPackageCalculations = DealPackageCalculations(self)
                    self.__UpdateCalculations(True)
                self._calculationsRegistered = True
                    
    def __RefreshCalculation(self, traitName):
        refreshNeeded = False
        if self._dealPackageCalculations.RefreshCalculation(traitName):
            refreshNeeded = True
        return refreshNeeded
        
    def _RefreshAllCalculations(self):
        refreshNeeded = False
        for traitName in self._GetTraitNames():
            if self._GetCalcMapping(traitName):
                refreshNeeded |= self.__RefreshCalculation(traitName)
        return refreshNeeded

    '''******************************** 
    COMPOSITE ATTRIBUTES (INTERNAL METHODS)
    ********************************'''
    
    def _CompositeAttributes(self):
        return self._compositeAttributes
    
    def __RegisterCompositeAttributes(self, overrideAccumulator, clsDict = None):
        
        def CreateClassDictImpl(baseClasses, clsDict, classList):
            for cl in baseClasses:
                if cl not in classList:
                    CreateClassDictImpl(cl.__bases__, clsDict, classList)
            for cl in baseClasses:
                if cl not in classList:
                    clsDict.update(cl.__dict__)
                    classList.append(cl)
            
        def CreateClassDict(obj):
            classList = []
            clsDict = OrderedDict()
            CreateClassDictImpl([obj.__class__], clsDict, classList)
            return clsDict
            
        clsDict = CreateClassDict(self)
        instanceCompositeDict = self.__CreateCompositeAttributeInstances(clsDict)
        self._compositeAttributes.update(instanceCompositeDict)
        for attrName, attr in instanceCompositeDict.iteritems():
            setattr(self, attrName, attr)
            clsDict = attr.GetClassDict(overrideAccumulator)                
            self.__AddAttributesToSelf(clsDict)

        # Need to recreate the cached name key
        self._sortedTraitNames = None

    def __CreateCompositeAttributeInstances(self, classAttributeDict):
        instanceCompositeDict = OrderedDict()
        for attrName, attr in classAttributeDict.iteritems():
            if isinstance(attr, CompositeAttributeBase):
                attr = attr.__class__(*attr._PrivateArgs(), **attr._PrivateKwargs())
                instanceCompositeDict[attrName] = attr
                attr.set_name(attrName)
                attr.SetOwner(self)
        return instanceCompositeDict
    
    def __AddAttributesToSelf(self, clsDict):
        for k in clsDict:
            v = clsDict[k]
            if isinstance(v, TraitType):
                setattr(v, 'this_class', self.__class__)
                v.instance_init(self)
                self.UpdateInstanceTraits(k, v)
            if isinstance(v, CompositeAttributeBase):
                self._compositeAttributes[k] = v
            setattr(self, k, v)
    
    def _RegisterOnChangeCallbacks(self):
        traits = self.traits()
        for traitName in traits:
            callback = self._GetOnChanged(traitName)
            if not callback.IsDefault():
                self.on_trait_change(callback, traitName)
    
    def _ValidateTraitsMetaDataKeys(self):
        for trait in self.traits():
            for key in self._GetTrait(trait).get_metadata_keys():
                if not key in ValidAttributeMetaDataKeys() and not key.startswith("_"):
                    msg = "Meta data key '" + key + "' in attribute '" + trait + "' is not defined"
                    self.Log().Error(msg)

    '''******************************** 
    INTERFACE METHODS
    ********************************'''
    def _RefreshCalculations(self):
        refreshNeeded = False
        try:
            if self.get_trait_value("autoRefreshCalc"):
                self._RegisterAllCalculations()
                refreshNeeded = self._RefreshAllCalculations()
        except:
            pass
        return refreshNeeded
        
    def _UpdateDelegations(self):
        for attrName in self.metaData:
            if not self.GetAttributeMetaData(attrName, 'attributeMapping').IsDefault():
                self.metaData[attrName] = {}
    
    def _RebuildCalculations(self):
        self._calculationsRegistered = False
    
    def _RebuildCalculationsNeeded(self):
        return not self._calculationsRegistered

    def _RebuildCalculationsIfNeeded(self, traitName, oldValue, newValue):
        recreateCalcSpaceOnChange = self._GetRecreateCalcSpaceOnChange(traitName)
        if (oldValue != newValue and recreateCalcSpaceOnChange) or (self._dealPackageCalculations and self._dealPackageCalculations.AnyCalcObjectReplaced()):
            self._calculationsRegistered = False
            if not self.get_trait_value("autoRefreshCalc") and traitName not in ['refreshCalcCounter']:
                current = self.get_trait_value("refreshCalcCounter")
                setattr(self, "refreshCalcCounter", current + 1)
        
    def _MinorChange(self, traitName):
        return self._GetNoDealPackageRefreshOnChange(traitName)
    
    def __SetGraphCoordinatesNeedsRefresh(self, traitName, oldValue, newValue):
        refreshNeeded = False
        if not self._MinorChange(traitName):
            if newValue != oldValue and self.get_trait_value('autoRefreshCalc'):
                refreshNeeded = True
        return refreshNeeded
        
    def __SetRefreshGraph(self, traitName, oldValue, newValue):
        if self.__SetGraphCoordinatesNeedsRefresh(traitName, oldValue, newValue):
            self._RecalcGraphCoordinates()
    
    def _RepopulateSheet(self):
        self.SetAttribute("sheetNeedsRefresh", True)
    
    def _RecalcGraphCoordinates(self):
        self.SetAttribute("graphCoordinatesNeedsRefresh", True)
    
    def __CopyTransientValues(self, attributesToCopy):
        if attributesToCopy:
            for name in attributesToCopy:
                if name not in ['solverValue', 'solverParameter', 'solverTopValue']: # Should not be here. See SPR 391246
                    value = attributesToCopy[name]
                    self.SetAttribute(name, value, silent=True)
    
    def __HandleOverrides(self, overrideAccumulator):
        overrides = overrideAccumulator.processed_overrides()
        for attrName, metadata in overrides.iteritems():
            # Make copy of attribute and put on class
            attr = copy.copy(self.traits().get(attrName, None))
            if attr is None:
                raise AttributeError('Failed to override metadata. No attribute named %s.' % attrName)
            # Init attribute
            setattr(attr, 'this_class', self.__class__)
            attr.instance_init(self)
            self.UpdateInstanceTraits(attrName, attr)
            # Set attribute on self
            setattr(self, attrName, attr)
            for mdkey, toMergeList in metadata.iteritems():
                current = attr.get_metadata(mdkey)
                for toMerge in toMergeList:
                    attr.append_metadata(self, mdkey, MergeMetaData(mdkey, current, toMerge))
                    current = attr.get_metadata(mdkey)
                self.metaData.setdefault(attrName, {})[mdkey] = None
        self._ValidateTraitsMetaDataKeys()
    
    def _PrivateOnNew(self, newFromInstrumentPackage = False, optArg = NOT_IMPLEMENTED):
        with RegisterAllObjMappingsOnNewWithSafeExit(self, newFromInstrumentPackage):
            if not newFromInstrumentPackage:
                if isinstance(optArg, NotImplemented) or optArg == None:
                    self.AssemblePackage()
                else:
                    self.AssemblePackage(optArg)
            oa = AttributeOverrideAccumulator(self)
            self.__RegisterCompositeAttributes(oa)
            self.__HandleOverrides(oa)
            self._RegisterOnChangeCallbacks()
            self.__RegisterAllActionMethods()
            self._RegisterAllObjectMappingDefaultValues(newFromInstrumentPackage)
            self._RegisterAllObjectMappings()
            self.DealPackage().Refresh()
            self._RecalcGraphCoordinates()
        self.__CallOnComposites('OnNew')
        self.OnNew()
    
    def _PrivateRefresh(self):
        self.Refresh()
        self.__CallOnComposites('Refresh')
    
    def _DoOpen(self):
        with MuteNotificationsWithSafeExit(self):
            oa = AttributeOverrideAccumulator(self)
            self.__RegisterCompositeAttributes(oa)
            self.__HandleOverrides(oa)
            self._RegisterOnChangeCallbacks()
            self.__RegisterAllActionMethods()
            self._RegisterAllObjectMappings()
            self.__RegisterAllAttributeMappings()
            self._RegisterAllCalculations()
            self._RefreshAllCalculations()
            self._RecalcGraphCoordinates()
    
    def __CallOnComposites(self, methodName):
        for compName in self._CompositeAttributes():
            if hasattr(self, compName):
                comp = getattr(self, compName)
                getattr(comp, methodName)()
    
    def _PrivateOnOpen(self):
        with MuteParentDealPackageDelegateUpdatesOnCopyAndOpen(self):
            self._DoOpen()
            self.__CallOnComposites('OnOpen')
            self.OnOpen()
    
    def _PrivateOnSave(self, config):
        toReturn = None
        try:
            self._SetDealPackageSaveConfiguration(config)
            toReturn = self.OnSave(config)
        except:
            self._SetDealPackageSaveConfiguration(None)
            raise
            
        self._SetDealPackageSaveConfiguration(None)
        return toReturn
    
    def _PrivateOnCopy(self, originalDealPackage, anAspectSymbol, calcDict):
        with MuteParentDealPackageDelegateUpdatesOnCopyAndOpen(self):
            self._DoOpen()
            self._isSolverDealPackage = str(anAspectSymbol) == 'solving'
            self.__CopyTransientValues(calcDict['attributesToCopy'])
            self._SetCalculations(calcDict['calculations'])
            self._SetSimulations(calcDict['simulations'])
            self.OnCopy(originalDealPackage, anAspectSymbol)
    
    def _PrivateIsValid(self, aspect):
        isValid = True
        try:
            accumulator = ValidationExceptionAccumulator()
            self.IsValid(accumulator, aspect)
            self._ValidateTraits(accumulator)
            self.__ValidateCompositeAttributes(accumulator, aspect)
            isValid = accumulator.ValidationResult()
        except Exception as e:
            isValid = [FormatException(e)]
        self.Log().Verbose('IsValid: %s' % isValid)
        return isValid
    
    def __ValidateCompositeAttributes(self, exceptionAccumulator, aspect):
        for member in inspect.getmembers(self):
            if issubclass(member[1].__class__, CompositeAttributeBase):
                getattr(self, member[0]).IsValid(exceptionAccumulator, aspect)
    
    def _PrivateDismantle(self):
        if self._dealPackageCalculations:
            self._dealPackageCalculations.TearDown()
        self.__CallOnComposites('OnDismantle')
        self.OnDismantle()
        self._dealPackage = None
        
    @classmethod
    def _PrivateSetUp(cls, definitionName, gui):
        from DealPackageSetUp import DealPackageSetUp
        definitionSetUp = DealPackageSetUp(definitionName, gui)
        try:
            cls.SetUp( definitionSetUp )
            # Compsite attributes SetUp-methods
            for member in inspect.getmembers(cls):
                if issubclass(member[1].__class__, CompositeAttributeBase):
                    getattr(cls, member[0]).SetUp(definitionSetUp)
            definitionSetUp.SetUp()
        except Exception as e:
            msg = 'Deal Package can not be instantiated: %s' % FormatException(e)
            raise DealPackageException( msg )
            
    def __SetDealPackageRefreshNeeded(self, traitName, oldValue, newValue):
        if not self._MinorChange(traitName):
            self.DealPackage().RefreshNeeded(True)

    def __IsTraitChanging(self, traitName, userInputTraitName):
        return (not userInputTraitName) or (self._traitsChanging and traitName in self._traitsChanging)
            
    def __OnObjectMappingTraitChange(self, traitName, oldValue, newValue, userInputTraitName):
        if self.__IsTraitChanging(traitName, userInputTraitName):
            if self._applyTraitChangeAndCallObjMappingSetMethod:
                if not self._registeringAllObjMappingsOnNew:
                    if not self._IsCalcVal(traitName):
                        self._UpdateAndRegisterAllObjectMappings(traitName)
                        if self.ONCHANGED_MODE > 0:
                            i = 0
                            while len(self._updatedTraits) and i < 5:
                                self._UpdateAndRegisterAllObjectMappings(traitName)
                                i += 1
        
    def __UpdateDelegateTraitOnParentDealPackage(self, traitName, oldValue, newValue, userInputTraitName):
        if (not self._muteParentNotificationsOnCopyAndOpen):
            parent = self.DealPackage().ParentDealPackage() if hasattr(self.DealPackage(), 'ParentDealPackage') else None
            if  parent and (parent.IsStorageImage() or parent.IsInfant()) and self.__IsTraitChanging(traitName, userInputTraitName):
                parent.GetAttribute('updateParentDelegateTraits')()
    
    def __OnAnyTraitChange(self, traitName, oldValue, newValue, userInputTraitName):
        with MuteParentDealPackageDelegateUpdates(self):
            self.__ApplyAttributeMappingChange(traitName, newValue)
            self._RebuildCalculationsIfNeeded(traitName, oldValue, newValue)
            self.__RegisterAllAttributeMappings()
            self.__SetRefreshGraph(traitName, oldValue, newValue)
            self.__SetDealPackageRefreshNeeded(traitName, oldValue, newValue)
            self.__UpdateDelegateTraitOnParentDealPackage(traitName, oldValue, newValue, userInputTraitName)
        
    def _ApplyCalcMappingSimulation(self, traitName, newValue):
        if not self._calculationsRegistered: 
            self._RegisterAllCalculations()   

        if self._GetSolverTopValue(traitName):
            self._SolveForTrait(traitName, newValue)
        else:
            transformCb = self._GetTransform(traitName)
            isSimulated = self._dealPackageCalculations.IsSimulated(traitName)
            oldValue = self.get_trait_value(traitName).Value()
            newValue = transformCb(newValue)
            self.SimulateCalculation(traitName, newValue)
            if isSimulated != self._dealPackageCalculations.IsSimulated(traitName) or oldValue != self.get_trait_value(traitName).Value():
                self.__SendNotification(traitName, oldValue, self.get_trait_value(traitName).Value())
        self._RefreshAllCalculations()
        self._RecalcGraphCoordinates()
    
    def _GetAttributesToCopy(self):
        allAttributeNames = self.trait_names() # including private attributes
        attributesToCopy = {}
        for name in allAttributeNames:
            attr = self._GetTrait(name)
            if attr.__class__ in (Action, Box, CalcVal, DelegateAttribute, Label, Link):
                continue
            elif self._GetObjMapping(name) != None and name != 'uxCallbacks':
                continue
            attributesToCopy[name] = self.GetAttribute(name)
        return attributesToCopy
    
    def _GetSimulations(self):
        simulations = None
        if self._dealPackageCalculations:
            simulations = self._dealPackageCalculations.Simulations()
        return simulations
    
    def _SetSimulations(self, simulations):
        if self._dealPackageCalculations and simulations:
            self._dealPackageCalculations.ApplySimulations(simulations)
    
    def _GetCalculations(self):
        calculations = None
        if self._dealPackageCalculations:
            calculations = self._dealPackageCalculations.Calculations()
        return calculations
        
    def _SetCalculations(self, calculations):
        if self._dealPackageCalculations and calculations:
            self._dealPackageCalculations.CreateMissingCalculations(calculations)
    
    def _SetDealPackageSaveConfiguration(self, config):
        self.m_dealPackageSaveConfiguration = config
        
    def force_apply_obj_mappings(self, traitName):
        return self._muteParentNotificationsOnCopyAndOpen or (traitName in ['solverParameter', 'solverValue', 'solverTopValue']) or self._GetSolverParameter(traitName) or self._GetSolverTopValue(traitName)
        
    '''******************************** 
    IMPLEMENTATION OF DEAL PACKAGE METHODS
       GetAttribute/SetAttribute/GetAttributes/GetAttributeMetaData
    ********************************'''
    def GetAttribute(self, traitName):
        self._GetTrait(traitName).AttributeExceptionAccumulator().Raise()
        return getattr(self, traitName)
        
    def SetAttribute(self, traitName, newValue, silent=False):
        if silent or self.GetAttributeMetaData(traitName, 'silent')():
            with MuteNotificationsWithSafeExit(self):
                setattr(self, traitName, newValue)
        else:
            setattr(self, traitName, newValue)
    
    # DO NOT CALL FROM PY
    def __GetAttributeMetaDataImpl(self, traitName, metaKey=''):
        return self.GetAttributeMetaDataOrThrow(traitName, metaKey)
    
    # DO NOT CALL FROM PY
    def __GetAttributesImpl(self):
        return self.GetAttributesOrThrow()
    
    # DO NOT CALL FROM PY
    def __GetAttributeMetaDataImpl(self, traitName='', metaKey=''):
        if traitName == '' and metaKey == '':
            return self.GetAttributeMetaData
        else:
            return self.GetAttributeMetaDataOrThrow(traitName, metaKey)
    
    # DO NOT CALL FROM PY
    def __GetAttributeFromC(self, traitName=''):
        if traitName == '':
            return self.GetAttribute
        else:
            self._AssertPublicTrait(self, traitName)
            return self.GetAttribute(traitName)
            
    # DO NOT CALL FROM PY
    def __SetAttributeFromC(self, traitName, newValue):
        self._AssertPublicTrait(self, traitName)
        self.SetAttribute(traitName, newValue)
    
    # DO NOT CALL FROM PY
    def __HasAttributeFromC(self, traitName):
        return IsPublicTrait(self, traitName)
    
    # DO NOT CALL FROM PY
    def __CallUserActionFromC(self, traitName):
        self._AssertPublicTrait(self, traitName)
        if self.uxCallbacks:
            dialogCb = self.uxCallbacks['dialog']
            if dialogCb:
                dialogCb(self.DealPackage(), traitName)
                return acm.FSymbol('callUserAction')
        return None

    GetAttributeFromC = __GetAttributeFromC
    SetAttributeFromC = __SetAttributeFromC
    HasAttributeFromC = __HasAttributeFromC
    GetAttributes = __GetAttributesImpl
    GetAttributeMetaData = __GetAttributeMetaDataImpl
    CallUserActionFromC = __CallUserActionFromC
    '''******************************** 
    EO IMPLEMENTATION OF DEAL PACKAGE METHODS
    ********************************'''
    
    __SendNotification = TraitBase._notify_trait
    _TraitValuesAreEqual = TraitBase._trait_values_are_equal
    __SendNotifications = TraitBase._send_notifications
    _GetTraitNames = TraitBase.get_trait_names

# Help methods/classes

class AttributeOverrideAccumulator(object):
    def __init__(self, obj=None):
        self.overrides = {}
        self.name_prefix = ''
        if obj is not None:
            self.get_overrides_from(obj)
        
    def __call__(self, attr_dict):
        for name in attr_dict:
            pf_name = self.get_prefixed_name(name)
            self.overrides.setdefault(pf_name, []).append(attr_dict[name])
    
    def get_overrides_from(self, inst, prefix=''):
        self.name_prefix = prefix
        for klass in type(inst).mro():
            if 'AttributeOverrides' in klass.__dict__:
                klass.AttributeOverrides(inst, self)
        self.name_prefix = ''
    
    def get_prefixed_name(self, name):
        if self.name_prefix:
            if name.startswith('_'):
                return '_' + self.name_prefix + name
            else:
                return self.name_prefix + '_' + name
        else:
            return name
    
    def processed_overrides(self):
        output = {}
        for attrName, overrides in self.overrides.iteritems():
            output[attrName] = {}
            for o in overrides[::-1]: # loop backwards
                for mdkey in o:
                    last = output[attrName].setdefault(mdkey, [])
                    last = last[-1] if last else None
                    output[attrName][mdkey].append( MergeMetaData(mdkey, last, o[mdkey]) )
        return output

def MergeMetaData(metaDataKey, current, toMerge):
    if current is None or current == toMerge:
        return toMerge # Nothing to merge with
    
    if not MetaDataMergePossible(metaDataKey):
        return toMerge # Override instead of merge
    
    validTypes = (basestring, ObjMappingSplitter)
    if not isinstance(current, validTypes):
        raise AttributeException("Current metadata has to be of type string, got %s, type %s"% (str(current), str(type(current))))
    if not isinstance(toMerge, validTypes):
        raise AttributeException("Merging metadata has to be of type string, got %s, type %s"% (str(toMerge), str(type(toMerge))))
    
    if isinstance(current, ObjMappingSplitter) or isinstance(toMerge, ObjMappingSplitter):
        return ObjMappingSplitter.Merge(current, toMerge)
    else:
        return MergeMetaDataStrings(current, toMerge)
