""" Compiled: 2017-11-06 12:31:15 """

#__src_file__ = "extensions/ConvertiblePricingAndRisk/etc/FInstrumentSpreadFunctions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FInstrumentSpreadFunctions -

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from math import isnan, isinf

def IsValidSpread(spread):
    return not (isnan(spread) or isinf(spread))

def CloneWithNewSpread(spread, newSpread):
    newInstrumentSpread = spread.Clone()
    if IsValidSpread(newSpread):
        newInstrumentSpread.Spread(newSpread)
    return newInstrumentSpread
