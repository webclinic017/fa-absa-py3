import acm
import traitlets
import re
from DealPackageUtil import IsFObject, FormatException, UnpackPaneInfo
from TraitUtil import AttributeException
from traitlets import Bytes
from traitlets import Float as BaseFloat
from traitlets import Int as BaseInt
from traitlets import Bool as BaseBool
from traitlets import Any as BaseAny
from traitlets import Set as BaseSet
from CompositeAttributeDevKit import CompositeAttributeDefinition

class NotSet():
    pass

ArrayCast = acm.GetFunction('array', 1)

'''*************************
TraitValidationBase
*************************'''
class TraitValidationBase():

    def TransformTrait(self, obj, name, value):
        def parseValueToDouble(obj, traitName, value):
            if obj.GetAttributeMetaData(traitName, 'attributeMapping').IsDefault() and isinstance(value, basestring) and obj._GetDomain(traitName) in [acm.GetDomain('double'), acm.GetDomain('int')]:
                parsed = obj._GetFormatter(traitName).Parse(value)
                if parsed is not None:
                    value = parsed
                if not value and parsed is None:
                    value = None
            return value
        value = obj._GetAttributeMetaDataCallback(name, 'transform')(value)
        value = parseValueToDouble(obj, name, value)
        return obj._ParseValueToCorrectDomainValue(name, obj._GetDomain(name), value)
        
    def ApplyObjMapping(self, obj, name, value):
        chain = obj._GetObjMapping(name)
        if chain:
            value = obj._AssignValueToObjMappingMethodChain(name, chain, value, True)
        return value
        
    def ValidateTrait(self, obj, name, value):
        validateCb = obj.GetAttributeMetaData(name, 'validate')
        if validateCb:
            validateCb(value)
        return self.ValidateTraitValue(obj, value)
             
    def __TraitValidateCB(self, obj, accumulator):
        try:
            self._validate(obj, self.get_value( obj ) )
        except AttributeException as e:
            accumulator(FormatException(e))
            
    def __MandatoryValueMissing(self, obj):
        valueMissing = False
        if obj._GetAttributeMetaDataCallback(self._attr_name, "mandatory")():
            value = self.get_value( obj )
            if not isinstance(value, bool):
                valueMissing = True if not value else False
        return valueMissing
        
    def __TraitIsMandatory(self, obj, accumulator):
        if self.__MandatoryValueMissing(obj):
            label = obj._GetAttributeMetaDataCallback(self._attr_name, "label")()[:-1]
            accumulator("%s is mandatory" % (label))

    def __ValidateObjectMapping(self, obj, accumulator):
        methodChains = obj._GetObjMapping(self._attr_name)
        if methodChains:
            try:
                obj._GetObjectMappingValueAndValidateEqual(self._attr_name, methodChains)
            except AttributeException as e:
                accumulator(FormatException(e))

    def __ValidateAttributeMapping(self, obj, accumulator):
        methodChains = obj._GetAttributeMapping(self._attr_name)
        if methodChains:
            try:
                obj._GetAttrValueFromChain(self._attr_name, methodChains)
            except AttributeException as e:
                accumulator(FormatException(e))

    def TraitIsValid(self, obj, accumulator):
        self.__ValidateObjectMapping(obj, accumulator)
        self.__ValidateAttributeMapping(obj, accumulator)
        self.__TraitValidateCB(obj, accumulator)
        self.__TraitIsMandatory(obj, accumulator)

'''*************************
BaseStr Trait Type
*************************'''
class BaseStr(Bytes):
    pass
    
'''*************************
Date Trait Type
*************************'''
class Date(BaseStr, TraitValidationBase):

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)
        
    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)
    
    def ValidateTraitValue(self, obj, value):
        result = value
        if value is not None and value != '':
            result = acm.Time().PeriodSymbolToDate(value)
            if not result:
                result = acm.GetDomain('date').ParseValue(value)
            if None == result:
                raise Exception('Not a valid date format.')
        return result

'''*************************
DatePeriod Trait Type
*************************'''
class DatePeriod(BaseStr, TraitValidationBase):

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)
               
    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)
        
    def ValidateTraitValue(self, obj, value):
        result = value
        if value != None:
            result = acm.GetDomain('dateperiod').ParseValue(value)
        return result
        
'''*************************
Object Trait Type
*************************'''
class Object(BaseAny, TraitValidationBase): 
    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)
        
    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)

    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)    

    def ValidateTraitValue(self, obj, value):
        if value == "":
            value = None
        return value
    
'''*************************
Bool Trait Type
*************************'''
class Bool(BaseBool, TraitValidationBase):

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)

    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)
        
    def ValidateTraitValue(self, obj, value):
        return acm.GetDomain('bool').ParseValue(value)
        
'''*************************
Action Trait Type
*************************'''   
class Action(BaseAny, TraitValidationBase):
    def do_set(self, obj, new_value, old_value):
        from DealPackageUtil import DealPackageException
        raise DealPackageException("Action attributes cannot be changed")
    
    def SetAction(self, obj, val):
        BaseAny.do_set(self, obj, val, NotSet())
            

'''*************************
Float Trait Type
*************************'''
class Float(BaseFloat, TraitValidationBase):

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)

    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)    

    def ValidateTraitValue(self, obj, value):
        if value == None:
            return 0.0
        return acm.GetDomain('double').ParseValue(value)

'''*************************
Int Trait Type
*************************'''
class Int(BaseInt, TraitValidationBase):
 
    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)
 
    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)
      
    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)    

    def ValidateTraitValue(self, obj, value):
        if value == None:
            return 0.0
        return acm.GetDomain('int').ParseValue(value)

'''*************************
Str Trait Type
*************************'''
class Str(BaseStr, TraitValidationBase):
    
    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)
           
    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)    

    def ValidateTraitValue(self, obj, value):
        if value == None:
            value = ""
        return value
        
'''*************************
Str Trait Type
*************************'''    
class Text(Str, TraitValidationBase):
    pass
    
'''*************************
Calc Val Trait Type
*************************'''
class CalcVal(BaseAny, TraitValidationBase):
    def do_set(self, obj, new_value, old_value):
        if (not obj._muteNotifications):
            obj._ApplyCalcMappingSimulation(self._attr_name, new_value)
            obj.DealPackage().RefreshNeeded(True)
        else:
            BaseAny.do_set(self, obj, new_value, old_value)
        
    def SetCalculation(self, obj, val):
        BaseAny.do_set(self, obj, val, NotSet())

    def validate(self, obj, value):
        return value
        
'''*************************
DelegateAttribute Trait Type
*************************'''
class DelegateAttribute(BaseAny, TraitValidationBase):

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)
      
    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)
    
    def ValidateTraitValue(self, obj, value):
        return value


'''*************************
DelegateDealPackage Composite Attribute Type
*************************'''
class DelegateDealPackage(CompositeAttributeDefinition):
    
    def OnInit(self, attributeMapping, customPanes=None, **kwargs):
        self._dp = attributeMapping
        self._rawLayout = customPanes
        self._layout = ""
        self._kwargs = kwargs
        
    def Attributes(self):
        attributes = {}
        if self.DP():
            self.InitLayout()
            for attrName in self.DP().GetAttributes():
                attributes[attrName] = DelegateAttribute( attributeMapping=self._dp+"."+attrName, **self._kwargs)
        return attributes
        
    def DP(self):
        return self.GetMethod(self._dp)()
    
    def GetLayout(self):
        layout = []
        if isinstance(self._layout, basestring):
            layout = self.UniqueLayout(self._layout)
        else:
            for tabInfo in self._layout:
                tabCtrlName, tabCtrlLayout = UnpackPaneInfo(tabInfo)
                newTabCtrlLayout = []
                for paneInfo in tabCtrlLayout:
                    paneName, paneLayout = UnpackPaneInfo(paneInfo)
                    newTabCtrlLayout.append({paneName: self.UniqueLayout(paneLayout)})
                layout.append({tabCtrlName: newTabCtrlLayout})
        return layout
    
    def InitLayout(self):
        if isinstance(self._rawLayout, basestring):
            layoutCbName = self._rawLayout.strip().translate(None, '@')
            layout = self.DP().GetAttribute('transformLayout')(self.GetMethod(layoutCbName)())
        elif not self._rawLayout:
            layout = ArrayCast(self.DP().GetAttribute('customPanes'))
        else:
            layout = ArrayCast(self._rawLayout)
        self._layout = layout

'''*************************
List Trait Type
*************************'''
class List(BaseAny, TraitValidationBase):
    def get_default_value(self):
        '''Create a new instance of the default value.'''
        if self.default_value == None:
            self.default_value = acm.FArray()
        return self.ValidateValue(self.default_value)

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)

    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)
        
    def ValidateTraitValue(self, obj, value):
        try:
            return self.ValidateValue(value)
        except ValueError:
            raise Exception("The '%s' attribute of %s instance must be a FIndexedCollection or a subclass of FIndexedCollection, but a value of %s was specified."
                            % (self._attr_name, traitlets.class_of(obj), traitlets.repr_type(value)) )
        
    def ValidateValue(self, value):
        if isinstance(value, (list, tuple)):
            array = acm.FArray()
            for v in value: array.Add(v)
            value = array
        if not IsFObject(value) or not value.IsKindOf(acm.FIndexedCollection):
            raise ValueError("Class has to be list, tuple or subclass to FIndexedCollection")
        return value      


'''*************************
Set Trait Type
*************************'''

class Set(BaseSet, TraitValidationBase):   

    def transform(self, obj, value):
        return self.TransformTrait(obj, self._attr_name, value)

    def applyObjMapping(self, obj, value):
        return self.ApplyObjMapping(obj, self._attr_name, value)

    def validate(self, obj, value):
        return self.ValidateTrait(obj, self._attr_name, value)
        
    def ValidateTraitValue(self, obj, value):        
        if IsFObject(value):        
            if value.IsKindOf(acm.FSet):
                return value
            else:
                raise Exception("The '%s' attribute of %s instance must be a FSet or a subclass of FSet, but a value of %s was specified."
                                % (self._attr_name, traitlets.class_of(obj), traitlets.repr_type(value)) )
        else:
            return BaseSet.validate(self, obj, value)        

'''*************************
Label Trait Type
*************************'''
class Label(BaseAny, TraitValidationBase):
    def set_value(self, obj, new_value):
        raise Exception("The '%s' attribute of %s instance can't be set, but a value of %s was specified."
                        % (self._attr_name, traitlets.class_of(obj), traitlets.repr_type(new_value)) )
                        
    def get_value(self, obj):
        value = None
        cb = obj.GetAttributeMetaData(self._attr_name, 'label')
        if cb:
            value = cb()
        return value
        
    def validate(self, obj, value):
        return value
        
'''*************************
Link Trait Type
*************************'''
class Link(Label, TraitValidationBase):
    pass
    

'''*************************
Box Trait Type
*************************'''   
class Box(BaseAny, TraitValidationBase):
    def do_set(self, obj, new_value, old_value):
        from DealPackageUtil import DealPackageException
        raise DealPackageException("Box attributes cannot be changed")
