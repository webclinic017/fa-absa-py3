""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSLotUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSLotUtils

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

def UnpackLot(lot):
    return [l for l in lot]

def UnpackLotMap(lotMap):
    lot = lotMap.Lot()
    includedElementIndices = lotMap.IncludedElements()
    if includedElementIndices.IsEmpty():
        instruments = UnpackLot(lot)
    else:
        instruments = [lot[i] for i in includedElementIndices]
    return instruments

def Unpack(variant):
    res = list()
    for i in variant:
        if i.IsKindOf(acm.FLotMap):
            res.extend(UnpackLotMap(i))
        elif i.IsKindOf(acm.FLot):
            res.extend(UnpackLot(i))
        else:
            res.append(i)
    return res