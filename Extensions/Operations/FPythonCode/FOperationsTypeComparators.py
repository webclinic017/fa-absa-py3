""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTypeComparators.py"
import acm, types
from FOperationsTypeComparator import TypeComparator

#-------------------------------------------------------------------------
# PrimitiveTypeComparator - Can check for primitive python types
#-------------------------------------------------------------------------
class PrimitiveTypeComparator(TypeComparator):

    #-------------------------------------------------------------------------
    def __init__(self, primitiveType):
        super(PrimitiveTypeComparator, self).__init__()
        self.__primitiveType = primitiveType

    #-------------------------------------------------------------------------
    def IsCorrectType(self, value):
        return isinstance(value, self.__primitiveType)

    #-------------------------------------------------------------------------
    def GetExpectedType(self):
        return self.__primitiveType

#-------------------------------------------------------------------------
# AcmTypeComparator - Can check for acm class types
#-------------------------------------------------------------------------
class AcmTypeComparator(TypeComparator):

    #-------------------------------------------------------------------------
    def __init__(self, acmType):
        super(AcmTypeComparator, self).__init__()
        self.__acmType = acmType

    #-------------------------------------------------------------------------
    def IsCorrectType(self, value):
        return isinstance(value, acm._pyClass(self.__acmType))

    #-------------------------------------------------------------------------
    def GetExpectedType(self):
        return acm._pyClass(self.__acmType)

#-------------------------------------------------------------------------
# DateTypeComparator - Can check for correct date format
#-------------------------------------------------------------------------
class DateTypeComparator(TypeComparator):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(DateTypeComparator, self).__init__()

    #-------------------------------------------------------------------------
    def IsCorrectType(self, value):
        if isinstance(value, bytes):
            try:
                date = acm.Time.FromDate(value) 
            except Exception as _:
                return False
            return date != acm.Time.FromDate('0') #Since strings unable to parse will parse to date 'zero'
        else:
            return False

    #-------------------------------------------------------------------------
    def GetExpectedType(self):
        return "Date"

#-------------------------------------------------------------------------
# SWIFTMessageTypeComparator - Can check for valid SWIFT message types
#-------------------------------------------------------------------------
class SWIFTMessageTypeComparator(TypeComparator):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(SWIFTMessageTypeComparator, self).__init__()

    #-------------------------------------------------------------------------
    def IsCorrectType(self, value):
        if isinstance(value, bytes):
            try:
                intValue = int(value)
            except Exception as _:
                return False
            return intValue >= 0
        return False
    #-------------------------------------------------------------------------
    def GetExpectedType(self):
        return "SWIFT Message Type"

#-------------------------------------------------------------------------
# DummyTypeComparator - Always returns False
#-------------------------------------------------------------------------
class DummyTypeComparator(TypeComparator):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(DummyTypeComparator, self).__init__()

    #-------------------------------------------------------------------------
    def IsCorrectType(self, value):
        return False