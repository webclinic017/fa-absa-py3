import acm
import inspect
import types
from traitlets import AttributeException
from TraitBaseTypes import Str, Float, Int, Object, Date, DatePeriod, Bool, CalcVal, DelegateAttribute, Action, List, Set, Text, Label, Link, Box
from DealPackageUtil import IsFObject, IsIterable, MakeIterable, FUNCTION_DOMAIN_ATTRIBUTE, DealPackageUserException, IsAttributeInListDomain
from DealPackageDialog import DealPackageAttributeDialog
from TraitUtil import CallableMethodChain, CallableMultiMethodChain, CallableMultiCalcConfigurationMethodChain, LogException
import ChoicesExprInstrument
import ChoicesExprTrade

base_type_map = {
    Str:                ('str',        acm.GetDomain('string')),
    Text:               ('text',       acm.GetDomain('string')),
    Float:              ('float',      acm.GetDomain('double')),
    Int:                ('int',        acm.GetDomain('int')),
    Object:             ('FObject',    acm.GetDomain('string')),
    Date:               ('date',       acm.GetDomain('date')),
    DatePeriod:         ('dateperiod', acm.GetDomain('dateperiod')),
    Bool:               ('bool',       acm.GetDomain('bool')),
    CalcVal:            ('str',        acm.GetDomain(acm.FCalculation)),
    List:               ('list',       acm.GetDomain(acm.FIndexedCollection)),
    Set:                ('set',        acm.GetDomain(acm.FSet)),
    DelegateAttribute:  ('delegate',   acm.GetDomain('string')),
    Action:             ('action',     acm.GetDomain(acm.FPythonFunction)),
    Label:              ('label',      acm.GetDomain('string')),
    Link:               ('link',       acm.GetDomain('string')),
    Box:                ('box',        acm.GetDomain('string'))
}
class NoValue(): pass
NO_VALUE = NoValue()
class NoOpinion(object): pass
NoOverride = NoOpinion()
ERROR_COLOR = acm.GetDefaultContext().GetExtension(acm.FColor, acm.FColor, 'SyntaxPythonOperator')

def DoNotCompare(first, second):
    return True # Always return true -> Always equal

def CompareDefinitions(first, second):
    if type(second) == CallbackRunner:
        return first.Definition() == second.Definition()
    else:
        return False

class CallbackRunner(object):
    def __init__(self, cb, isDefault, description, eq, definition):
        self.cb = cb
        self.isDefault = isDefault
        self.description = description
        self.eq = eq
        self.definition = definition
    
    def __call__(self, *args):
        return self.cb(*args)
    
    def __str__(self):
        return self.description
    
    def __eq__(self, other):
        # Equal
        return self.eq(self, other)
    
    def __ne__(self, other): # Has to be implemented along with __eq__
        # Not Equal
        return not self.__eq__(other)
    
    def IsDefault(self):
        return self.isDefault
    
    def Definition(self):
        return self.definition # Same as plain value
    
            
class AttributeMetaData(object):
    callbackPrefix = '@'
    
    def __init__(self, plainMetaValue=None):
        self._dpDef = None
        self._trait = None
        self._attrName = None
        self._plainMetaValue = plainMetaValue
        self._cb = None
        self._cbRunner = None
        self._value = NO_VALUE
        self._previousCallback = None
    
    def DpDef(self):
        return self._dpDef
    
    def SetDpDef(self, dpDef):
        self._dpDef = dpDef
    
    def SetPreviousCallback(self, cb):
        self._previousCallback = cb
    
    def PreviousCallback(self):
        return self._previousCallback
    
    def AttributeName(self):
        return self._attrName
    
    def SetAttributeName(self, attrName):
        self._attrName = attrName
        
    def CallbackPreArgs(self):
        return [self.TraitName()]
    
    def CallbackPostArgs(self):
        return []
    
    def Trait(self):
        return self._trait
    
    def SetTrait(self, trait):
        self._trait = trait
        
    def TraitName(self):
        return self.Trait().get_name()
        
    def DoTransformValue(self, value):
        return value
        
    def DefaultCallback(self, *args):
        return None
        
    def IsAcceptableValue(self):
        return True
    
    def CompareMethod(self, first, second):
        if callable(second):
            return first() == second()
        else:
            return False # first is if type CallbackRunner (callable), second is not callable (not CallbackRunner)
    
    def PostCallbackValidation(self, value):
        return value
        
    def Callback(self):
        if not self._cbRunner:
            self._cb = self.CreateCallback()
            if isinstance(self._cb, CallbackRunner):
                self._cbRunner = self._cb
            else:
                isDefault = self._cb == self.DefaultCallback
                self._cbRunner = CallbackRunner(
                    self._RunCallback, 
                    isDefault,
                    'CallbackRunner: \n attribute = '+ self.TraitName() +'\n isDefault = '+ str(isDefault) + '\n metadataKey = ' + self.AttributeName(),
                    self.CompareMethod,
                    self.Value())
        return self._cbRunner
    
    def Log(self):
        return self.DpDef().Log() 
    
    @LogException(logAs='Error')
    def _RunCallback(self, *args):
        retVal = None
        try:
            value = self._cb( *args )
            if value == NoOverride and self.PreviousCallback():
                retVal = self.PreviousCallback()(*args)
            else:
                retVal = self.PostCallbackValidation(value)
        except DealPackageUserException as e:
            raise type(e), type(e)(str(e))
        except Exception as e:
            self._AppendInfoAndReRaiseException(e)
        return retVal
    
    def _AppendInfoAndReRaiseException(self, e):
        import sys
        msg = self._AppendInfo(e)
        originalStacktrace = sys.exc_info()[2]
        raise type(e), type(e)(msg), originalStacktrace
    
    def _AppendInfoAndLogMessage(self, msg):
        msg = self._AppendInfo(msg)
        self.Log().Warning( msg )
    
    def _AppendInfo(self, msg):
        return 'Failure on attribute "%s" (meta data "%s"): %s' % (self.TraitName(), self.AttributeName(), str(msg))
    
    def Value(self, *args):
        if self._value == NO_VALUE:
            self._value = self.DoTransformValue(self.PlainAttrValue())
        return self._value
    
    def KeyCallbackPair(self):
        return (self.AttributeName(), self.Callback)
    
    def KeyValuePair(self):
        return (self.AttributeName(), self.Value())
        
    def _ShouldDelegate(self):
        return self._plainMetaValue == None
    
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return False
    
    def PlainAttrValue(self):
        if self._plainMetaValue == None and self.DpDef()._GetAttributeMapping(self.TraitName()) and self._ShouldDelegate():
            self._plainMetaValue = self.DpDef()._GetTraitMetaInfoFromAttributeMapping(self.TraitName(), self.AttributeName())
        return self._plainMetaValue
    
    def SetPlainMetaValue(self, plainMetaValue):
        self._plainMetaValue = plainMetaValue
        
    def CreateCallback(self):
        raisedMsg = ""
        try:
            cb = None
            if self._IsValueCallback():
                cb = self.Value()
            elif self._IsValueCallbackSting():
                cb = self._StringToCallBack( self.Value() )
            elif self._IsCallableMultiMethodChain() and self.SupportsCallableMultiMethodChain():
                cb = self._CallableMultiMethodChain( self.Value() )
            elif self.Value() == None:
                cb = self.DefaultCallback
            elif self.IsAcceptableValue():
                cb = self.Value
            return cb
        except Exception as e:
            raisedMsg = str(e)
            
        msg = 'Could not create create callback for attribute %s (%s) using definition: %s. %s' % (self.TraitName(), self.AttributeName(), self.PlainAttrValue(), raisedMsg)
        raise AttributeException(msg)
        
    def _IsCallableMultiMethodChain(self):
        return isinstance(self.Value(), str) and self.Value().startswith( AttributeMetaData.callbackPrefix ) and self.Value().find('|') != -1    
            
    def _IsValueCallbackSting(self):
        return self._IsCallbackString(self.Value())
    
    def _IsCallbackString(self, value):
        return isinstance(value, str) and value.startswith( AttributeMetaData.callbackPrefix ) and value.find('|') == -1

    def _CallableMultiMethodChain(self, aString):
        cb = CallableMultiMethodChain( self.DpDef(), self._RemoveCallbackPrefix(aString), self.CallbackPreArgs(), self.CallbackPostArgs())
        return cb        
        
    def _StringToCallBack(self, aString):
        cb = CallableMethodChain( self.DpDef(), self._RemoveCallbackPrefix(aString), self.CallbackPreArgs(), self.CallbackPostArgs())
        return cb
        
    def _RemoveCallbackPrefix(self, aString):
        return aString.replace(AttributeMetaData.callbackPrefix, "", 1)
    
    def _IsValueCallback(self):
        return callable(self.Value())
 
    def _RefreshDealPackage(self):
        if not self.DpDef()._MinorChange(self.TraitName()) and self.DpDef()._dealPackage and not self.DpDef()._GetAttributeMetaDataCallback(self.TraitName(), "silent")():
            self.DpDef()._UpdateAndRegisterAllObjectMappings(self.TraitName())
            self.DpDef()._RebuildCalculationsIfNeeded(self.TraitName(), 'dummy1', 'dummy2')
            self.DpDef().DealPackage().RefreshNeeded(True)
            
    def _InitAttrib(self, attr):
        attr.SetDpDef( self.DpDef() )
        attr.SetTrait( self.Trait() )
        attr.SetAttributeName( self.AttributeName() )

class UxInteractionAttribute(AttributeMetaData): 
    def PostCallbackValidation(self, value):
        self._RefreshDealPackage()
        return value
    
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return True
        
    def CompareMethod(self, first, second):
        return DoNotCompare(first, second)
        
class UxNonInteractionAttribute(AttributeMetaData): 
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return True
        
    def CompareMethod(self, first, second):
        return DoNotCompare(first, second)

class GetInfoAttribute(AttributeMetaData): 
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return False
        
    def CompareMethod(self, first, second):
        return DoNotCompare(first, second)

class LabelAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return self.TraitName()
    
    def IsAcceptableValue(self):
        if isinstance(self.Value(), str):
            return True
        return False

    def PostCallbackValidation(self, value):
        if self.Trait().AttributeExceptionAccumulator().TraitInErrorState():
            value = str(value) + self.Trait().AttributeExceptionAccumulator().ErrorString()
        mandatory = self.DpDef()._GetAttributeMetaDataCallback(self.TraitName(), "mandatory")()
        if mandatory:
            value = str(value) + '*'
        return value


class ToolTipAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return ''
    
    def IsAcceptableValue(self):
        if isinstance(self.Value(), str):
            return True
        return False

class BoolAttribute(AttributeMetaData):
    def IsAcceptableValue(self):
        if isinstance(self.Value(), bool):
            return True
        return False
    
    def PostCallbackValidation(self, value):
        if bool(value) != value:
            msg = "%s should return boolean, returned '%s'." % (self.PlainAttrValue(), str(value))
            self._AppendInfoAndLogMessage(msg)
        if self.DpDef()._GetAttributeMapping(self.TraitName()) and self._ShouldDelegate():
            delegateValue = self.DpDef()._GetTraitMetaInfoFromAttributeMapping(self.TraitName(), self.AttributeName())
            if delegateValue and delegateValue() == False:
                value = False
                
        return bool(value)

class BoolAttributeTrue(BoolAttribute):
    def DefaultCallback(self, *args):
        return True

class BoolAttributeFalse(BoolAttribute):
    def DefaultCallback(self, *args):
        return False

class EditableAttribute(BoolAttribute):
    def __init__(self, plainMetaValue):
        BoolAttribute.__init__(self, plainMetaValue)
        self._defaultValue = None
    
    def DefaultCallback(self, *args):
        if self._defaultValue is None:
            self._defaultValue = True
            if not IsAttributeInListDomain(self.DpDef(), self.TraitName()):
                objMapping = self.DpDef()._GetObjMapping(self.TraitName())
                for chain in objMapping.split("|") if objMapping else []:
                    obj, methodName = self.DpDef()._GetCallableObjectAndMethodFromChain(chain)
                    try:
                        self._defaultValue = self.__HasMethodSetter(obj, methodName)
                    except AttributeException as e:
                        raise AttributeException("%s: %s" % (traitName, str(e)))
        return self._defaultValue
        
    def __HasMethodSetter(self, obj, methodName):
        toReturn = None
        obj = MakeIterable(obj)
        for objIter in obj:
            if IsFObject(objIter):
                aClass = objIter.Class()
                hasSetter = self.__MethodOnClassHasSetter(aClass, methodName)
            else:
                # Assume python method
                hasSetter = self.__PyMethodHasSetter(objIter, methodName)
            if toReturn is None:
                toReturn = hasSetter
            if not (toReturn == hasSetter):
                raise AttributeException("Inconsistent Object mappings. Some methods does not have setters.")
        return toReturn

    def __MethodOnClassHasSetter(self, aClass, aMethodName):
        if hasattr(aClass, 'GetMethod'):
            return bool(aClass.GetMethod(aMethodName, 1))
        return False
    
    def __PyMethodHasSetter(self, obj, methodName):
        argSpec = inspect.getargspec(getattr(obj, methodName))
        twoArgs = len(argSpec[0]) == 2
        hasVarArgs = len(argSpec[0]) == 1 and bool(argSpec[1])
        return twoArgs or hasVarArgs

class ChoiceListSourceAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        populator = None
        if self.DpDef()._GetAttributeMetaDataCallback(self.TraitName(), "hasChoiceListSource")():
            domain = self.DpDef()._GetDomain(self.TraitName())
            choices = []            
            if domain.IsKindOf(acm.FClass):
                if domain.IncludesBehavior(acm.FChoiceList):
                    msg = "Attribute '%s': objMapping domain FChoiceList requires a choiceListSource" % (self.TraitName())
                    self.Log().Error(msg)
                    choices = []
                elif domain.IsKindOf(acm.FPersistentClass):
                    if domain.IsAbstract():
                        return None
                    else:
                        choices = domain.Select('')
                else:
                    choices = domain.InstancesKindOf()
            elif domain.IsKindOf(acm.FEnumeration):
                choices = domain.Values()
            populator = acm.FChoiceListPopulator()
            populator.SetChoiceListSource(choices)
        return populator
    
    def CompareMethod(self, first, second):
        return DoNotCompare(first, second)
    
    def PopulatorFromCollection(self, coll):
        populator = acm.FChoiceListPopulator()
        populator.SetChoiceListSource(coll)
        return populator
        
    def PostCallbackValidation(self, value):
        if value:
            if hasattr(value, 'IsKindOf') and value.IsKindOf(acm.FCollection):
                value = self.PopulatorFromCollection(value)
            elif isinstance(value, (list, tuple, set)):
                value = self.PopulatorFromCollection(value)
        return value
        
    def IsAcceptableValue(self):
        if isinstance(self.Value(), list) and not isinstance(self.Value(), str):
            return True
        if hasattr(self.Value(), 'IsKindOf') and self.Value().IsKindOf(acm.FCollection):
            return True
        return False

class HasChoiceListSourceAttribute(BoolAttributeFalse):
    def DoTransformValue(self, value):
        hasExplicitChoices = False
        if self.DpDef().trait_metadata(self.TraitName(), 'choiceListSource'):
            hasExplicitChoices = True
        elif self.DpDef()._GetAttributeMapping(self.TraitName()):
            hcsFromDelegate = self.DpDef()._GetTraitMetaInfoFromAttributeMapping(self.TraitName(), 'hasChoiceListSource')
            if hcsFromDelegate:
                hasExplicitChoices = hcsFromDelegate()
        elif self.Trait().__class__ not in [Action, CalcVal, List, Set]:
            domain = self.DpDef()._GetDomain(self.TraitName())
            if domain and not domain.IsSubtype(acm.FCollection):
                hasExplicitChoices = (domain.IsClass() or domain.IsEnum()) and domain != acm.FBoolean
        return hasExplicitChoices
        
class CalcConfigurationAttribute(AttributeMetaData):
    def IsAcceptableValue(self):
        if self._IsValueCallbackSting():
            return True
        return False
    
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return True
    
    def _CallableMultiMethodChain(self, aString):
        cb = CallableMultiCalcConfigurationMethodChain( self.DpDef(), self._RemoveCallbackPrefix(aString), self.CallbackPreArgs(), self.CallbackPostArgs())
        return cb   


class SolverTopValueAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return False
        
    def IsAcceptableValue(self):
        if isinstance(self.Value(), bool):
            return True
        if isinstance(self.Value(), str):
            return True
        return False
        
class SolverParameterAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return False 

class TabToAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return None

class TraitNameAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return self.TraitName()
        
    def IsAcceptableValue(self):
        if isinstance(self.Value(), bool):
            return True
        if isinstance(self.Value(), dict):
            return True
        return False

class OnChangedAttribute(AttributeMetaData):
    def _ShouldDelegate(self):
        return False
    
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return True

    def CallbackPreArgs(self):
        return []
        
    def IsAcceptableValue(self):
        if self._IsValueCallbackSting():
            return True
        return False
    
    def CompareMethod(self, first, second):
        return CompareDefinitions(first, second)

class ValidateAttribute(AttributeMetaData):
    
    @classmethod
    def SupportsCallableMultiMethodChain(self):
        return True
   
    def IsAcceptableValue(self):
        if self._IsValueCallbackSting():
            return True
        return False
        
    def CompareMethod(self, first, second):
        return CompareDefinitions(first, second)
        
class ActionAttribute(AttributeMetaData):
    def IsAcceptableValue(self):
        if self._IsValueCallbackSting():
            return True
        return False
    
    def CompareMethod(self, first, second):
        if type(first) == type(second):
            return DoNotCompare(first, second)
        else:
            return False
    
    def PostCallbackValidation(self, value):
        self._RefreshDealPackage()
        return value

class ActionListAttribute(ActionAttribute):
    def IsAcceptableValue(self):
        if self._IsValueCallbackSting():
            return True
        return False
    
    def CompareMethod(self, first, second):
        if type(first) == type(second):
            return DoNotCompare(first, second)
        else:
            return False

class MandatoryAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return False
        
class TraitTypeAttribute(AttributeMetaData):
    def __init__(self, plainMetaValue):
        AttributeMetaData.__init__(self, plainMetaValue)
        self._defaultValue = None
    
    def DefaultCallback(self, *args):
        if not self._defaultValue:
            trait = self.DpDef().traits()[self.TraitName()]
            typeName = None
            if self.DpDef()._GetAttributeMapping(self.TraitName()):
                typeName = self.DpDef()._GetTraitMetaInfoFromAttributeMapping(self.TraitName(), self.AttributeName())
            else:
                typeName = base_type_map.get(trait.__class__, None)[0]
                if typeName is None:
                    raise AttributeException("Unhandled attribute type: " + str(trait.__class__))
            self._defaultValue = typeName
        return self._defaultValue

class NoDealPackageRefreshOnChangeAttribute(AttributeMetaData):
    def __init__(self, plainMetaValue):
        AttributeMetaData.__init__(self, plainMetaValue)
        self._defaultValue = None
    
    def DefaultCallback(self, *args):
        if self._defaultValue == None:
            noRefreshOnChange = bool(self.Value())
            if isinstance(self.Trait(), (CalcVal)):
                noRefreshOnChange = True
            self._defaultValue = noRefreshOnChange
        return self._defaultValue
        
class TransformAttribute(AttributeMetaData):
    def __init__(self, plainMetaValue):
        AttributeMetaData.__init__(self, plainMetaValue)
        self._defaultValue = None
    
    def _ShouldDelegate(self):
        return False
        
    def CallbackPreArgs(self):
        return [self.TraitName()]
        
    def DefaultCallback(self, value):
        return value
        
    def CompareMethod(self, first, second):
        return DoNotCompare(first, second)

class ColorAttribute(AttributeMetaData):
    def _ParseRGBStringToColor(self, value):
        colorStr = value.upper()
        rgb = [0, 0, 0]
        for elem in colorStr.split(' '):
            if elem.startswith('R'):
                rgb[0] = elem[1:]
            elif elem.startswith('G'):
                rgb[1] = elem[1:]
            elif elem.startswith('B'):
                rgb[2] = elem[1:]
        return acm.UXColors.Create(*rgb)
        
    def _IsRGBString(self, value):
        upper = value.upper()
        colors = upper.split(' ')
        brgCandidate = ''.join(sorted([elem[0] for elem in colors]))
        if brgCandidate == 'BGR':
            return True
        return False
    
    def DoTransformValue(self, value):
        if isinstance(value, str) and not self._IsCallbackString(value):
            color = None
            if self._IsRGBString(value):
                color = self._ParseRGBStringToColor(value)
            if isinstance(value, str):
                extension = acm.GetDefaultContext().GetExtension(acm.FColor, acm.FColor, value)
                if extension is None:
                    raise AttributeException("Could not find an FColor named %s." % (str(value)))
                color = extension.Value()
            value = color
        return value
    
    def PostCallbackValidation(self, value):
        return self.DoTransformValue(value)
    
    def IsAcceptableValue(self):
        return hasattr(self.Value(), 'IsKindOf') and self.Value().IsKindOf(acm.FColor)

class LabelColorAttribute(ColorAttribute):
    def PostCallbackValidation(self, value):
        if self.Trait().AttributeExceptionAccumulator().TraitInErrorState():
            try:
                value = ERROR_COLOR.Value()
            except:
                pass
        else:
            value = super(LabelColorAttribute, self).PostCallbackValidation(value)
        return value

class FontAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return {}
    
    def IsAcceptableValue(self):
        value = self.Value()
        if IsFObject(value, acm.FDictionary) or isinstance(value, dict):
            return True
        return False

class AlignmentAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return 'Left'

    def AcceptableValue(self, val):
        return val in ['Left', 'Center', 'Right']

    def IsAcceptableValue(self):
        val = self.Value()
        if isinstance(val, basestring):
            return self.AcceptableValue(val)
        return False

class AddNewListItemAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return ['Last']

    def AcceptableValue(self, val):
        return val in ['First', 'Last', 'Sorted']

    def IsAcceptableValue(self):
        val = self.Value()
        if isinstance(val, basestring):
            return self.AcceptableValue(val)
        if isinstance(val, list):
            for v in val:
                if not self.AcceptableValue(v):
                    return False
        return True
        

    def DoTransformValue(self, value):
        if isinstance(value, basestring):
            return [value]
        else:
            return value

class WidthAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return -1
        
    def IsAcceptableValue(self):
        return isinstance(self.Value(), (int, long, float))    
    
class FormatterAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        traitDomain = self._dpDef._GetDomain(self.TraitName())
        if traitDomain:
            return traitDomain.DefaultFormatter()        
        return None
    
    def CompareMethod(self, first, second):
        return True # Do not compare
    
    def DoTransformValue(self, value):
        if not self._IsCallbackString(value):
            if isinstance(value, str):
                return acm.Get("formats/" + value)
        return value
    
    def IsAcceptableValue(self):
        isOk = self.Value() == None
        isOk |= hasattr(self.Value(), 'IsKindOf') and self.Value().IsKindOf(acm.FFormatter)
        return isOk

class TickAttribute(AttributeMetaData):
    
    def __init__(self, plainMetaValue):
        AttributeMetaData.__init__(self, plainMetaValue)
        self._tickSize = None
    
    def DefaultTick(self, value, increment):
        # Only intended to work for numerics (not dates)
        if not value:
            value = 0
        if increment:
            value += self._tickSize
        else:
            value -= self._tickSize
        return value
    
    def DoTransformValue(self, value):
        if value and isinstance(value, basestring):
            return value
    
        method = None
        if value == True:
            f = self._dpDef._GetFormatter(self.TraitName())
            if f and hasattr(f, 'Tick') and f.Tick():
                self._tickSize = f.Tick()
                method = self.DefaultTick
        elif isinstance(value, (int, long, float)):
            self._tickSize = value
            method = self.DefaultTick
        return method
    
    def IsAcceptableValue(self):
        isOk = self.Value() == None
        isOk |= isinstance(self.Value(), (int, long, float, bool))    
        return isOk

class NoPreArgsAttribute(AttributeMetaData):
    def CallbackPreArgs(self):
        return []
        
class ColumnsAttribute(AttributeMetaData):
    def DefaultCallback(self, *args):
        return ''
    
class DomainAttributeMetaDataBase(AttributeMetaData):
    def CreateCallback(self):
        return self.Value
        
    def _IsObjMappingWithSimpleTraitType(self, traitName, trait):
        return self.DpDef()._GetTraitTypeName(traitName, trait) != 'FObject' and self.DpDef()._GetObjMapping(traitName)

    def _GetTraitDefaultDomain(self, traitName, trait):
        domain = base_type_map.get(trait.__class__, None)[1]
        if domain is None:
            raise AttributeException("Unhandled attribute domain for attribute: " + str(trait.__class__))
        return domain

    def __ValidDomain(self, domain, methodDomain):
        if domain == None:
            domain = methodDomain
        else:
            if methodDomain.IsSubtype(domain):
                domain = methodDomain
            elif not domain.IncludesBehavior(methodDomain):
                raise AttributeException("Inconsistent Object mapping (mismatching domains)")
        return domain
        
    def __ReduceSymbolToString(self, domain):
        if domain and hasattr(domain, 'IsKindOf') and domain.IsSubtype(acm.FSymbol):
            domain = acm.GetDomain('string')
        return domain
            
    def __GetDomainFromObjectAndMethod(self, obj, methodName, domain):
        obj = MakeIterable(obj)
        for objIter in obj:
            aDomain = self.__GetMethodDomain(objIter, methodName)
            domain = self.__ValidDomain(domain, aDomain)
        return self.__ReduceSymbolToString(domain)
                
    def __GetMethodDomain(self, obj, aMethodName):
        domain = None
        if IsFObject(obj):
            aClass = obj.Class()
            domain = self.__GetMethodDomainFromClass(aClass, aMethodName)
        elif hasattr(getattr(obj, aMethodName), FUNCTION_DOMAIN_ATTRIBUTE):
            # Method is decorated with domain
            domainString = getattr(getattr(obj, aMethodName), FUNCTION_DOMAIN_ATTRIBUTE)
            domain = acm.GetDomain(domainString)
        return domain
    
    def __GetMethodDomainFromClass(self, aClass, aMethodName):
        domain = None
        if hasattr(aClass, 'GetMethod'):
            aMethod = aClass.GetMethod(aMethodName, 0)
            if aMethod:
                domain = aMethod.Domain()
                if domain.IsKindOf(acm.FBusinessLogicDecoratorClass):
                    domain = domain.DecoratedClass()
            else:
                raise AttributeException("'%s' object has no attribute '%s'" %(aClass, aMethodName))
        return domain
    
    def _GetObjMappingDomain(self, traitName, trait):
        domain = None
        attr = self.DpDef()._GetObjMapping(traitName)
        for chain in attr.split("|") if attr else "":
            obj, methodName = self.DpDef()._GetCallableObjectAndMethodFromChain(chain)
            try:
                domain = self.__GetDomainFromObjectAndMethod(obj, methodName, domain)
            except AttributeException as e:
                raise AttributeException("%s: %s" % (traitName, str(e)))
        return domain
    
    def _GetDomainFromStringOrSelf(self, explicitDomain):
        domain = None
        if isinstance(explicitDomain, basestring):
            domain = acm.GetDomain(explicitDomain)
        elif hasattr(explicitDomain, 'IsKindOf') and explicitDomain.IsKindOf(acm.FDomain):
            domain = explicitDomain
        return domain
                    
    def _GetExplicitDomain(self, traitName):
        explicitDomain = self.DpDef().trait_metadata(traitName, 'domain')
        return self._GetDomainFromStringOrSelf(explicitDomain)
    
    def __IsValidElementDomain(self, domain, elementDomain):
        isInvalid = domain.IsSubtype(acm.FString) or elementDomain.IsKindOf(acm.FVoidDomain)
        return not isInvalid
        
    def _ElementDomainFromDomain(self, domain):
        if domain:
            elementDomain = domain.ElementDomain()
            domain = elementDomain if elementDomain and self.__IsValidElementDomain(domain, elementDomain) else None
        return domain
    
    def _FirstNotNone(self, *args):
        return next(iter([a for a in args if a is not None]), None)
        
class ElementDomainAttribute(DomainAttributeMetaDataBase):
        
    def __ObjectMethodElementDomain(self):
        domain = None
        traitName = self.TraitName()
        if self.DpDef()._GetObjMapping(traitName):
            objMappingDomain = self._GetObjMappingDomain(traitName, self.Trait())
            if objMappingDomain:
                domain = self._ElementDomainFromDomain(objMappingDomain)
        return domain
    
    def __ValidateElementDomain(self, domain):
        objectMethodElementDomain = self.__ObjectMethodElementDomain()
        if domain and objectMethodElementDomain:
            if not domain.IsSubtype(objectMethodElementDomain):
                raise AttributeException('Element domain is not subtype of object mapping element domain')
    
    def __GetAttributeMappingElementDomain(self):
        domainCb = None
        if self.DpDef()._GetAttributeMapping(self.TraitName()):
            domainCb = self.DpDef()._GetTraitMetaInfoFromAttributeMapping(self.TraitName(), "elementDomain")
        return domainCb() if domainCb else None
    
    def DoTransformValue(self, value):
        domain = None
        explicitElementDomain = self._GetDomainFromStringOrSelf(value)
        explicitElementDomainFromDomain = self._ElementDomainFromDomain( self._GetExplicitDomain(self.TraitName()) )
        attributeMappingElementDomain = self.__GetAttributeMappingElementDomain()
        objectMethodElementDomain = self.__ObjectMethodElementDomain()
        domain = self._FirstNotNone(explicitElementDomain, explicitElementDomainFromDomain, attributeMappingElementDomain, objectMethodElementDomain)
        self.__ValidateElementDomain(domain)

        return domain
        
class DomainAttribute(DomainAttributeMetaDataBase):

    def __ValidateTraitDomain(self, traitTypeDomain, traitName, trait):
        if self._IsObjMappingWithSimpleTraitType(traitName, trait):
            defaultDomain = self._GetTraitDefaultDomain(traitName, trait)
            if defaultDomain and traitTypeDomain and not traitTypeDomain.IsSubtype(defaultDomain):
                 raise AttributeException('Domain does not match default domain (%s != %s)' % (traitTypeDomain, defaultDomain))
                 
        objMappingDomain = self._GetObjMappingDomain(traitName, trait)
        if objMappingDomain and not traitTypeDomain.IsSubtype(objMappingDomain):
            raise AttributeException('Domain does not match object mapping domain(%s != %s)' % (traitTypeDomain, objMappingDomain))

    def DoTransformValue(self, value):
        return self.__GetTraitDomain(self.TraitName(), self.Trait())
     
    def __GetExplicitElementDomain(self, traitName):
        domainStr = self.DpDef().trait_metadata(self.TraitName(), 'elementDomain')
        return acm.GetDomain(domainStr) if domainStr else None
        
    def __GetCollectionTopDomainName(self, traitName, trait ):
        collectionTopDomain = None
        if self.DpDef()._GetTraitTypeName(traitName, trait) == 'list':
            collectionTopDomain = 'FIndexedCollection'
        elif self.DpDef()._GetTraitTypeName(traitName, trait) == 'set':
            collectionTopDomain = 'FSet'
        return collectionTopDomain
        
    def __GetElementDomain(self, traitName):
        return self.DpDef()._GetAttributeMetaDataCallback(traitName, "elementDomain")()

    def __GetCollectionDomain(self, traitName, trait ):
        domainName = self.__GetCollectionTopDomainName(traitName, trait )        
        elementDomainName = self.__GetElementDomain(traitName)
        if domainName and elementDomainName:
            domainName =  domainName + '(' + elementDomainName.Name() + ')'
        return acm.GetDomain(domainName)
    
    def __SetElementDomain(self, domain):
        if domain and domain.IsSubtype(acm.FCollection):
            elementDomain = self.__GetElementDomain(self.TraitName())
            if elementDomain:
                baseDomainName = domain.BaseDomain().Name()
                elementDomainName = elementDomain.Name()
                domain = acm.GetDomain('%s(%s)' % (baseDomainName, elementDomainName))
        return domain
    
    def __GetAttributeMappingDomain(self):
        domainCb = None
        if self.DpDef()._GetAttributeMapping(self.TraitName()):
            domainCb = self.DpDef()._GetTraitMetaInfoFromAttributeMapping(self.TraitName(), "domain")
        return domainCb() if domainCb else None
    
    def __GetTraitDomain(self, traitName, trait):
        domain = self._GetExplicitDomain(traitName)

        if not domain:
            domain = self._GetObjMappingDomain(traitName, trait)
        if not domain:
            domain = self.__GetAttributeMappingDomain()
        if not domain:
            domain = self._GetTraitDefaultDomain(traitName, trait)
        
        domain = self.__SetElementDomain(domain)
        
        self.__ValidateTraitDomain(domain, traitName, trait)

        return domain

class RecreateCalcSpaceOnChangeAttribute(BoolAttributeTrue):
    def DefaultCallback(self, *args):
        recreateOnChange = False
        domain = self.DpDef()._GetDomain(self.TraitName())
        if self.DpDef()._GetObjMapping(self.TraitName()) and not domain.IsKindOf(acm.FNumericDomain):
            # Recreate calculations when non-numeric object mapping changes since ADFL selects might be affected
            recreateOnChange = True
        return recreateOnChange

class IsCalculationSimulatedAttribute(BoolAttributeTrue):
    def CalculationIsSimulated(self, *args):
        return self.DpDef().IsCalculationSimulated(self.TraitName())
        
    def CreateCallback(self):
        return self.CalculationIsSimulated

class AcquirerChoices(ChoiceListSourceAttribute):
    def AcquirerChoices(self, *args):
        populator = acm.FChoiceListPopulator()
        acquirers = ChoicesExprTrade.getAcquirers()
        populator.SetChoiceListSource(acquirers)
        return populator
    
    def CreateCallback(self):
        return self.AcquirerChoices
        
class CounterpartyChoices(ChoiceListSourceAttribute):
    def CounterpartyChoices(self, *args):
        populator = acm.FChoiceListPopulator()
        counterparties = ChoicesExprTrade.getCounterparties()
        populator.SetChoiceListSource(counterparties)
        return populator
    
    def CreateCallback(self):
        return self.CounterpartyChoices
        
class PortfolioChoices(ChoiceListSourceAttribute):
    def PortfolioChoices(self, *args):
        populator = acm.FChoiceListPopulator()
        portfolios = ChoicesExprTrade.getPhysicalPortfolioChoices()
        populator.SetChoiceListSource(portfolios)
        return populator 
    
    def CreateCallback(self):
        return self.PortfolioChoices
        
class TradeStatusChoices(ChoiceListSourceAttribute):
    def TradeStatusChoices(self, *args):
        leadTrade = self.DpDef().LeadTrade()
        if leadTrade:
            return ChoicesExprTrade.getTradeStatusChoices( leadTrade)
        else:
            raise AttributeException("TradeStatusChoices: LeadTrade is missing.")
    
    def CreateCallback(self):
        return self.TradeStatusChoices
            
class ValGroupChoices(ChoiceListSourceAttribute):
    def ValGroupChoices(self, *args):
        return ChoicesExprInstrument.getValuationGroups()
    
    def CreateCallback(self):
        return self.ValGroupChoices

def AttributeDialog(label, customPanes, btnLabel='Close', dealPackage=None):
    return _AttributeDialog(label, customPanes, btnLabel, dealPackage)

def NoButtonAttributeDialog(label, customPanes, dealPackage=None):
    return _AttributeDialog(label, customPanes, None, dealPackage)

class _AttributeDialog(UxInteractionAttribute):
    def __init__(self, label, customPanes, btnLabel, dealPackage):
        AttributeMetaData.__init__(self, None)
        self._caption = label
        self._customPanes = customPanes
        self._btnLabel = btnLabel
        self._dealPackage = dealPackage
        
    def GetCallBackValue(self, value):
        if self._IsCallbackString(value):
            cb = self._StringToCallBack(value)
            if cb:
                value = cb()
        return value
        
    def AttributeDialog(self):
        if not self._dealPackage:
            self._dealPackage = self.DpDef().DealPackage()
        dealPackage = self.GetCallBackValue(self._dealPackage)
        caption = self.GetCallBackValue(self._caption)
        customPanes = self.GetCallBackValue(self._customPanes)
        btnLabel = self.GetCallBackValue(self._btnLabel)
        return DealPackageAttributeDialog(dealPackage, caption, customPanes, btnLabel)
        
    def CreateCallback(self):
        return self.AttributeDialog
        
    def CompareMethod(self, first, second):
        return DoNotCompare(first, second)

class ContextMenu(UxInteractionAttribute):

    def __init__(self, *args):
        AttributeMetaData.__init__(self, None)
        self._contextMenuCommands = args
        
    def _ValidateCommand(self, cmd):
        if not isinstance(cmd, ContextMenuCommand):
            raise AttributeError('a ContextMenu must be initiated with one or more ContextMenuCommands')
        cmd._ValidateValue()
    
    def ContextMenu(self):
        returnArray = acm.FArray()
        for cmd in self._contextMenuCommands:
            if self._IsCallbackString(cmd):
                cb = self._StringToCallBack(cmd)
                if cb:
                    returnCmd = cb()
            else:
                returnCmd = cmd
            self._ValidateCommand(returnCmd)
            self._InitAttrib(returnCmd)
            returnArray.Add(returnCmd)
        return returnArray
                    
    def CreateCallback(self):
        return self.ContextMenu

class ContextMenuCommand(UxInteractionAttribute):
    
    _callBackAttributes = ('enabled', 'checked', 'invoke', 'applicable',)
    _dialogAttribute = 'dialog'
    
    def __init__(self, **kwargs):
        AttributeMetaData.__init__(self, None)
        self._commandAttributes = kwargs
        
    def _ValidateValue(self):
        if not isinstance(self._commandAttributes.get('commandPath'), str):
            raise AttributeError('Could not find mandatory field "commandPath"')
    
    def ContextMenuCommand(self):
        returnDict = acm.FVariantDictionary()
        for key in self._commandAttributes:
            if key in self._callBackAttributes:
                val = self._commandAttributes[key]
                if self._IsCallbackString(val):
                    returnDict.AtPut(key, self._StringToCallBack(val))
            elif key == self._dialogAttribute:
                dialog = self._commandAttributes[key]
                if self._IsCallbackString(dialog):
                    dialogCb = self._StringToCallBack(dialog)
                    dialog = dialogCb()
                if isinstance(dialog, _AttributeDialog):
                    self._InitAttrib(dialog)
                    returnDict.AtPut(key, dialog.Callback()())
                else:
                    returnDict.AtPut(key, dialog)
            else:
                returnDict.AtPut(key, self._commandAttributes[key])
        return returnDict
        
    def CreateCallback(self):
        return self.ContextMenuCommand
