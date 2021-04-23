""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/FSecLendMarkitData.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSecLendMarkitData - Functions for creating dictionary from FCustomTextObject

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""
import acm
import json

MARKIT_CACHE_DICTIONARY = {}

def GetMarkitData(loan, field):
    if loan:
        global MARKIT_CACHE_DICTIONARY
        textObject = acm.FCustomTextObject["Markit Master Text Object"]
        CreateDictionaryFromTextObject(textObject )
        if MARKIT_CACHE_DICTIONARY:
            ins_underlying = loan.Underlying()
            if ins_underlying:
                underlyingMarkitData_dictionary = MARKIT_CACHE_DICTIONARY[textObject.Oid(), textObject.VersionId()].get(ins_underlying.Name())
                if underlyingMarkitData_dictionary: 
                    fieldValue = underlyingMarkitData_dictionary[field]
                    if fieldValue:
                        return str(fieldValue)
    return None
    
def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('latin1') if isinstance(x, str) else x 
    return dict(map(ascii_encode, pair) for pair in data.items())
    
def CreateDictionaryFromTextObject(textObject):
    if textObject:
        global MARKIT_CACHE_DICTIONARY
        if (textObject.Oid(), textObject.VersionId()) not in MARKIT_CACHE_DICTIONARY.keys():
            MARKIT_CACHE_DICTIONARY = {}
            MARKIT_CACHE_DICTIONARY[textObject.Oid(), textObject.VersionId()] = json.loads(textObject.Text(), object_hook=ascii_encode_dict)