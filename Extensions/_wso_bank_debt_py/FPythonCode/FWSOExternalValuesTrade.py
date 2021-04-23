""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOExternalValuesTrade.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOExternalValuesTrade

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

from FWSOCustomMappingsTrade import WSOCustomMappings
from FWSODictToTradeDict import WsoDictToTradeDict

class ExternalValuesReplacer(object):
    
    def __init__(self, evDict):
        self.evDict = evDict
    
    def _DefaultAttributesDict(self):
        wsoDictToTradeDict = WsoDictToTradeDict(self.evDict)
        
        ''' Set default attributes for trade upload '''
        attributesDict = {
            'FA_AcquireDay': wsoDictToTradeDict.AcquireDay(),
            'FA_Currency': wsoDictToTradeDict.CurrencyName(),
            'FA_Instrument': wsoDictToTradeDict.Instrument(),
            'FA_OptionalKey': wsoDictToTradeDict.OptionalKey(),
            'FA_Premium': wsoDictToTradeDict.Premium(),
            'FA_Trader': wsoDictToTradeDict.Trader(),
            'FA_TradeStatus': wsoDictToTradeDict.TradeStatus(),
            'FA_TradeTime': wsoDictToTradeDict.TradeTime(),
            'FA_ValueDay': wsoDictToTradeDict.ValueDay(),
        }
        return attributesDict
    
    def _CustomAttributesDict(self):
        ''' Additional custom key-value pair mappings (defined in WSOCustomMappings) '''
        attributesDict = dict()
        customMappings = WSOCustomMappings(self.evDict)
        for methodName in dir(WSOCustomMappings):
            if methodName.startswith('__'):
                continue
            method = getattr(customMappings, methodName)
            value = method()
            attributesDict[methodName] = value
        return attributesDict
    
    def _InsertDictIntoExternalValues(self, replacingDict):
        ''' Replaces key-value pairs in external values dict with pairs from replacingDict '''
        for key, value in list(replacingDict.items()):
            self.evDict[key] = value

    def ModifyExternalValues(self):
        defaultAttributes = self._DefaultAttributesDict()
        self._InsertDictIntoExternalValues(defaultAttributes)
        
        customAttributes = self._CustomAttributesDict()
        self._InsertDictIntoExternalValues(customAttributes)
        
        return self.evDict


def ExternalValues(evDict):
    ''' Returns a modified version of the external values dictionary '''
    replacer = ExternalValuesReplacer(evDict)
    evDict = replacer.ModifyExternalValues()
    return evDict
