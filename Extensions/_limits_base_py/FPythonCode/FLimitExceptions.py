""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitExceptions.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitExceptions

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Provides functionality for handling errors in the limit framework.
-----------------------------------------------------------------------------"""

class LimitError(Exception):
    """Base class for all limit errors."""
    pass

class EmptyCalculationError(LimitError):
    """Raised when the limit does not have a resulting valid calculation."""
    pass

class MissingLimitTargetError(LimitError):
    """Raised if a limit referencing an invalid or missing limit target (cell)
    is added to the limit engine for monitoring."""
    pass

class CreateCalculationError(LimitError):
    """Raised if CreateCalculation fails when setting up LimitCalculation"""
    pass

class CalculatedValueTypeError(LimitError):
    """Raised if the calculated value is not of supported type"""
    
class TransformFunctionError(LimitError):
    """Raised when limit transform function is invalid"""