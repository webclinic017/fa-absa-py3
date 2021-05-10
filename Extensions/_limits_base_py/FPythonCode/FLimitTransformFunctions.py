""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitTransformFunctions.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FLimitTransformFunctions

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functions used to transform monitored cell values to a double

-------------------------------------------------------------------------------------------------------"""
import acm

def Value(variant):
    try:
        return variant.Number()
    except AttributeError:
        return variant
        
def AbsoluteValue(variant):
    try:
        return abs(Value(variant))
    except TypeError:
        return variant
        
def ValueSize(variant):
    if not variant:
        return 0
    if variant.IsKindOf(acm.FException):
        return variant
    try:
        return variant.Size()
    except AttributeError:
        return int(bool(variant))