""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsResultCounter.py"

from collections import Counter

from FOperationsResult import Result

#-------------------------------------------------------------------------
class ResultCounter(Result):

    #-------------------------------------------------------------------------
    def __init__(self):
        self.__resultCounters = dict()
        self.__exceptions = list()
        self.__failedObjects = list()

    #-------------------------------------------------------------------------
    def RE_Clear(self):
        self.__resultCounters.clear()
        del self.__exceptions[:]
        del self.__failedObjects[:]

    #-------------------------------------------------------------------------
    def RE_Result(self):
        return self.__resultCounters

    #-------------------------------------------------------------------------
    def RE_Exceptions(self):
        return self.__exceptions
    
    #-------------------------------------------------------------------------
    def RE_FailedObjects(self):
        return self.__failedObjects

    #-------------------------------------------------------------------------
    def RE_Accumulate(self, result):
        resultCountersToAdd = result.RE_Result()

        for op, counter in resultCountersToAdd.items():
            if op in self.__resultCounters:
                self.__resultCounters[op] += counter
            else:
                self.__resultCounters[op] = counter

        self.__exceptions.extend(result.RE_Exceptions())
        self.__failedObjects.extend(result.RE_FailedObjects())

    #-------------------------------------------------------------------------
    def RE_AddToResult(self, op, obj):
        className = str(obj.ClassName())

        try:
            self.__resultCounters[op][className] += 1
        except KeyError as _:
            self.__resultCounters[op] = Counter({className : 1})

    #-------------------------------------------------------------------------
    def RE_AddException(self, exception):
        self.__exceptions.append(exception)

    #-------------------------------------------------------------------------
    def RE_AddFailedObject(self, failedObject):
        self.__failedObjects.append(failedObject)

    #-------------------------------------------------------------------------
    def RE_ResultOpAndObjectType(self, op, objectType):
        value = 0
        try:
            value = self.__resultCounters[op][objectType]
        except KeyError as _:
            pass
        return value
