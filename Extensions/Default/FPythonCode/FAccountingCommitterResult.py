""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingCommitterResult.py"

# core
from collections import Counter

# operations
from FOperationsResultCounter import ResultCounter


#-------------------------------------------------------------------------
class CounterClass:
    OID                                = 'Oid'
    OBJECT_TYPE                        = 'ObjectType'

#-------------------------------------------------------------------------
class MultipleUpdatesResult(ResultCounter):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(MultipleUpdatesResult, self).__init__()

    #-------------------------------------------------------------------------
    def RE_AddToResult(self, op, obj):
        objectType = obj.JournalCategory() if str(obj.ClassName()) == 'FJournal' else str(obj.ClassName())

        newOid = False

        try:
            self.RE_Result()[CounterClass.OID][obj.OriginalOrSelf().Oid()]

        except KeyError as _:
            self.RE_Result().setdefault(CounterClass.OID, dict())[obj.OriginalOrSelf().Oid()] = (op, objectType)
            newOid = True

        if newOid:
            try:
                self.RE_Result()[CounterClass.OBJECT_TYPE][op][objectType] += 1
            except KeyError as _:
                self.RE_Result().setdefault(CounterClass.OBJECT_TYPE, dict())[op] = Counter({objectType : 1})

    #-------------------------------------------------------------------------
    def RE_Accumulate(self, result):
        resultCountersToAdd = result.RE_Result()

        for oid, counter in resultCountersToAdd.get(CounterClass.OID, dict()).items():

            try:
                self.RE_Result()[CounterClass.OID][oid]

            except KeyError as _:
                op, objectType = resultCountersToAdd[CounterClass.OID][oid]

                self.RE_Result().setdefault(CounterClass.OID, dict())[oid] = (op, objectType)

                self.RE_Result().setdefault(CounterClass.OBJECT_TYPE, dict()).setdefault(op, Counter())
                self.RE_Result()[CounterClass.OBJECT_TYPE][op][objectType] += 1

        self.RE_Exceptions().extend(result.RE_Exceptions())
        self.RE_FailedObjects().extend(result.RE_FailedObjects())

    #-------------------------------------------------------------------------
    def RE_ResultOpAndObjectType(self, op, objectType):
        value = 0

        try:
            value = self.RE_Result()[CounterClass.OBJECT_TYPE][op][objectType]
        except KeyError as _:
            pass

        return value
