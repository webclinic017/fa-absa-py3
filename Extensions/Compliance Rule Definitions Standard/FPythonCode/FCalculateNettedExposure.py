""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRuleDefinitionsStandard/./etc/FCalculateNettedExposure.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCalculateNettedExposure

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

singlePosKey = acm.FSymbol("singlePosition")

def UnderlyingRecursive(ins):
    underlying = ins.Underlying()
    if underlying:
        return UnderlyingRecursive(underlying)
    else:
        return ins

#Return underlying or self as neeting key
def GetUnderlyingNettingKey(insaddr):
    try:
        return UnderlyingRecursive(acm.FInstrument[insaddr]).StorageId()
    except Exception:
        return insaddr

#Return underlying or self issuer as netting key, or insaddr if not applicable
def GetIssuerNettingKey(insaddr):
    try:
        return UnderlyingRecursive(acm.FInstrument[insaddr]).Issuer().StorageId()
    except Exception:
        return insaddr

#Return currency as netting key
def GetCurrencyNettingKey(insaddr):
    try:
        return acm.FInstrument[insaddr].Currency().StorageId()
    except Exception:
        return insaddr

def NettingKey(insaddr, nettingSetting):
    nettingKey = insaddr
    if nettingSetting == "Underlying Net":
        nettingKey = GetUnderlyingNettingKey(insaddr)
    elif nettingSetting == "Issuer Net":
        nettingKey = GetIssuerNettingKey(insaddr)
    elif nettingSetting == "Currency Net":
        nettingKey = GetCurrencyNettingKey(insaddr)
    return nettingKey

def PreNettingFilter(value, inclusionSetting):
    if (inclusionSetting == "Long" and float(value) < 0) or (inclusionSetting == "Short" and float(value) > 0):
        return False
    else:
        return True

def PostNettingFilter(value, inclusionSetting):
    if (inclusionSetting == "Net Long" and float(value) < 0) or (inclusionSetting == "Net Short" and float(value) > 0):
        return False
    else:
        return True

def calculateExposure(subResults, nettingSetting, inclusionSetting):
    result = dict()
    singlePosition = False
    for subResult in subResults:
        for key in subResult:
            if key == singlePosKey:
                singlePosition = True
            else:
                nettingKey = NettingKey(key, nettingSetting)
                value = subResult[key]
                if PreNettingFilter(value, inclusionSetting):
                    if result.has_key(nettingKey):
                        result[nettingKey] += value
                    else:
                        result[nettingKey] = value
        
    returnVal = None
    useNetPositions = (nettingSetting == "Net") or (nettingSetting != "Gross" and singlePosition)
    for nettedValue in result.values():
        if PostNettingFilter(nettedValue, inclusionSetting):
            val = nettedValue if useNetPositions else acm.Math.Abs(nettedValue)
            if returnVal is None:
                returnVal = val
            else:
                returnVal += val
    return returnVal or 0.0

