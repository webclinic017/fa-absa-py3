""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskRunnerResult.py"
from FOperationsTaskRunnerResult import TaskRunnerResult

#-------------------------------------------------------------------------
class AccountingTaskRunnerResult(TaskRunnerResult):

    #-------------------------------------------------------------------------
    def __init__(self):

        self._created = 0
        self._updated = 0
        self._exceptions = 0

        self._failedObjects = dict()

    #-------------------------------------------------------------------------
    def TRR_AddResult(self, tmID, result):
        self._created += result.ATMR_Created()
        self._updated += result.ATMR_Updated()
        self._exceptions += result.ATMR_Exceptions()

        self._failedObjects[tmID] = list(result.ATMR_FailedObjects())

    #-------------------------------------------------------------------------
    def TRR_ContainsFailedData(self):
        return any([len(objects) > 0 for _, objects in self._failedObjects.items()])

    #-------------------------------------------------------------------------
    def TRR_FailedData(self):
        return self._failedObjects

    #-------------------------------------------------------------------------
    def TRR_Clear(self):
        self._created = 0
        self._updated = 0
        self._exceptions = 0
        self._failedObjects.clear()

    #-------------------------------------------------------------------------
    def ATRR_Created(self):
        return self._created

    #-------------------------------------------------------------------------
    def ATRR_Updated(self):
        return self._updated

    #-------------------------------------------------------------------------
    def ATRR_Exceptions(self):
        return self._exceptions