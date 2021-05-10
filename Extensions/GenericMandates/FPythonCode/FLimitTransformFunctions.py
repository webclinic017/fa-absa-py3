import acm


"""-------------------------------------------------------------------------------------------------------
MODULE
    FLimitTransformFunctions.py

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functions used to transform monitored cell values to a double

-------------------------------------------------------------------------------------------------------"""


def _MapMandates(variant):
    """
    Maps the string equivalent of the mandate column to a double value. This is to make it possible
    to create a limit on a column containing these string values.
    :param variant: FVariantDomain
    :return: double
    """
    mandatesMapping = {"Allowed": 1.0, "Not Allowed": 0.0, "No Mandate Found": -1.0}
    if variant in mandatesMapping:
        return mandatesMapping[variant]
    else:
        return variant


def Mandate(variant):
    variant = _MapMandates(variant)
    try:
        return variant.Number()
    except AttributeError:
        return variant


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
