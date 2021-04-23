""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOExternalValuesFacility.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOExternalValuesFacility

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

from FWSOCustomMappingsFacility import WSOCustomMappingsFacility as CustomMappings
from FWSODictToCombinationDict import WsoDictToCombinationDict


class ExternalValuesReplacer(object):
    
    def __init__(self, evDict):
        self.evDict = evDict
        
    def _EvDict(self):
        return self.evDict
        
    def _CustomMappedMethods(self):
        methodNames = list()
        for methodName in dir(CustomMappings):
            if methodName.startswith('__'):
                continue
            methodNames.append(methodName)
        return methodNames
        
    def _SetAttribute(self, customMappings, methodName, customAttributesDict):
        method = getattr(customMappings, methodName)
        value = method()
        customAttributesDict[methodName] = value
    
    def _DefaultAttributesDict(self):                
        ''' Set default attributes for facility upload. '''
        wsoDictToCombDict = WsoDictToCombinationDict(self._EvDict()) 
        defaultAttrDict = wsoDictToCombDict.CombinationDict()
        return defaultAttrDict
    
    def _CustomAttributesDict(self):
        ''' Additional custom key-value pair mappings (defined in WSOCustomMappingsFacility) '''
        customAttributesDict = dict()
        customMappings = CustomMappings(self._EvDict())
        for methodName in self._CustomMappedMethods():
            self._SetAttribute(customMappings, methodName, customAttributesDict)
        return customAttributesDict
    
    def _InsertDictIntoExternalValues(self, replacingDict):
        ''' Replaces key-value pairs in external values dict with pairs from replacingDict '''
        for key, value in list(replacingDict.items()):
            self._EvDict()[key] = value

    def ModifyExternalValues(self):
        defaultAttributes = self._DefaultAttributesDict()
        self._InsertDictIntoExternalValues(defaultAttributes)
        customAttributes = self._CustomAttributesDict()
        self._InsertDictIntoExternalValues(customAttributes)
        return self._EvDict()


def ExternalValues(evDict):
    ''' Returns a modified version of the external values facility dictionary. '''
    replacer = ExternalValuesReplacer(evDict)
    evDict = replacer.ModifyExternalValues()
    return evDict