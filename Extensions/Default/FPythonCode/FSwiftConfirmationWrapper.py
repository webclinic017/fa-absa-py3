""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftConfirmationWrapper.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftConfirmation - Module that provides a wrapper class for the ACM entity
    Confirmation


    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

from FOperationsEnums import InsType

class FSwiftConfirmation(object):

    def __init__(self, boEntity):
        self.boEntity = boEntity
        self.instrument = boEntity.Trade().Instrument()

    def __getattr__(self, attr):
        return getattr(self.boEntity, attr)

    def GetInsType(self):
        return self.instrument.InsType()

    def GetUnderlyingInstrType(self):
        return self.instrument.UnderlyingType()

    def GetExoticType(self):
        return self.instrument.ExoticType()

    def GetDigital(self):
        return self.instrument.Digital()

    def GetExerciseType(self):
        if self.instrument.InsType() == InsType.OPTION:
            return self.instrument.ExerciseType()
        return ''

    def GetOpenEnd(self):
        return self.instrument.OpenEnd()

    def GetProductTypeChlItem(self):
        return self.instrument.ProductTypeChlItem()

