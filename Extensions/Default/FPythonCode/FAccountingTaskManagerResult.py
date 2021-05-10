""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskManagerResult.py"
from FOperationsTaskManagerResult import TaskManagerResult

#-------------------------------------------------------------------------
class AccountingTaskManagerResult(TaskManagerResult):

    #-------------------------------------------------------------------------
    def __init__(self):

        self._created = 0
        self._updated = 0
        self._exceptions = 0

        self._failedObjects = list()

    #-------------------------------------------------------------------------
    def TMR_AddResult(self, result):

        self._created += result.result.created
        self._updated += result.result.updated
        self._exceptions += result.result.exceptions

        self._failedObjects.extend(result.result.objIds)

    #-------------------------------------------------------------------------
    def TMR_Clear(self):
        self._created = 0
        self._updated = 0
        self._exceptions = 0

        del self._failedObjects[:]

    #-------------------------------------------------------------------------
    def ATMR_Created(self):
        return self._created

    #-------------------------------------------------------------------------
    def ATMR_Updated(self):
        return self._updated

    #-------------------------------------------------------------------------
    def ATMR_Exceptions(self):
        return self._exceptions

    #-------------------------------------------------------------------------
    def ATMR_FailedObjects(self):
        return self._failedObjects