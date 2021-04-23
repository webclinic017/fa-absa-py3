import re
import acm
from collections import OrderedDict

class IsToken(object): pass
IS_ATTRIBUTE = IsToken()
IS_COMPOSITE = IsToken()

class CompositeAttributeBase(object):
    
    def __getattribute__(self, name):
        obj = super(CompositeAttributeBase, self).__getattribute__(name)
        if obj == IS_ATTRIBUTE:
            return self.GetAttribute(name)
        elif obj == IS_COMPOSITE:
            return self._owner._CompositeAttributes()[self.PrefixedName(name)]
        else:
            return obj
    
    def __setattr__(self, name, value):
        obj = name in self.__dict__ and super(CompositeAttributeBase, self).__getattribute__(name)
        if obj == IS_ATTRIBUTE:
            self.SetAttribute(name, value)
        else:
            self.__dict__[name] = value
            
    def __init__(self, *args, **kwargs):
        self._owner = None
        self._attr_name = None
        self._functions = []
        self._attributeNames = []
        self.__args = args 
        self.__kwargs = kwargs 
        self.OnInit(*args, **kwargs)
        
    def get_name(self):
        return self._attr_name
    
    def set_name(self, name):
        self._attr_name = name
    
    def _PrivateArgs(self):
        return self.__args
    
    def _PrivateKwargs(self):
        return self.__kwargs
        
    def OnInit(self, *args, **kwargs):
        pass
    
    def OnNew(self):
        pass
    
    def OnOpen(self):
        pass
    
    def OnDismantle(self):
        pass
    
    def Attributes(self):
        return {}
    
    def Owner(self):
        return self._owner
    
    def Refresh(self):
        pass
    
    def SetOwner(self, owner):
        self._owner = owner
    
    def GetClassDict(self, overrideAccumulator):
        overrideAccumulator.get_overrides_from(self, self.get_name())
        composite_attribute_dict = OrderedDict()
        for attrName, attr in self.Attributes().iteritems():
            self._attributeNames.append(attrName)
            attr.set_name( self.PrefixedName(attrName) )
            composite_attribute_dict[attr.get_name()] = attr
            if isinstance(attr, CompositeAttributeBase):
                attr.SetOwner(self._owner)
                clsDict = attr.GetClassDict(overrideAccumulator)
                composite_attribute_dict.update(clsDict)
        for attrName in composite_attribute_dict:
            self.__MarkAsAttributeOrComposite(attrName, composite_attribute_dict[attrName])
        for methodName in set(self._functions):
            combMethodName = self.PrefixedName(methodName)
            composite_attribute_dict[combMethodName] = getattr(self, methodName)
        return composite_attribute_dict

    def __MarkAsAttributeOrComposite(self, attrName, attr):
        cleanName = attrName
        if cleanName.startswith('_'):
            cleanName = cleanName[1:]
        cleanName = cleanName[len(self.get_name())+1:]
        if isinstance(attr, CompositeAttributeBase):
            self.__dict__[cleanName] = IS_COMPOSITE
        else:
            self.__dict__[cleanName] = IS_ATTRIBUTE

    def PrefixedName(self, name):
        if name.startswith('_'):
            return '_' + self.get_name() + name
        else:
            return self.get_name() + '_' + name
    
    def UniqueCallback(self, name):
        name = name.strip()
        prefix = ''
        if name.startswith('@'):
            name = name.translate(None, '@')
            prefix = '@'
        names = name.split('|')
        to_return = []
        for n in names:
            n = n.strip()
            self._functions.append(n)
            to_return.append(self.PrefixedName(n))
        return prefix + '|'.join(to_return)
    
    def SetAttribute(self, name, value, silent=False):
        self._owner.SetAttribute(self.PrefixedName(name), value, silent)
    
    def GetAttribute(self, name):
        return self._owner.GetAttribute(self.PrefixedName(name))
        
    def GetAttributeMetaData(self, attrName, metaKey):
        return self._owner.GetAttributeMetaData(self.PrefixedName(attrName), metaKey)
        
    def GetAttributeMetaDataKeys(self, attrName):
        return self._owner.GetAttributeMetaDataKeys()
        
    def UniqueLayout(self, layoutString):
        if not self._attributeNames:
            return layoutString
        replacement = [self.PrefixedName(attr) for attr in self._attributeNames]
        rep = dict(list(zip(self._attributeNames, replacement)))
        
        p = r'(?:\b)(%s)(?=\b|_)' % '|'.join(rep.keys())
        pattern = re.compile(p)
        return pattern.sub(lambda m: rep[m.group(0)], layoutString)

    def GetMethod(self, methodName):
        return getattr(self._owner, methodName)
        
    def HasMethod(self, methodName):
        return hasattr(self._owner, methodName)
    
    def GetLayout(self):
        return self.UniqueLayout(';'.join(self._attributeNames))
        
    def IsShowModeDetail(self, *args):
        return self._owner.IsShowModeDetail()
    
    def IsShowModeDetail2(self, *args):
        return self._owner.IsShowModeDetail2()

    def CloseDialog(self):
        return self._owner.CloseDialog()
