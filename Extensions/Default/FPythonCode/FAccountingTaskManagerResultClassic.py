""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskManagerResultClassic.py"
from FAccountingTaskManagerResult import AccountingTaskManagerResult

#-------------------------------------------------------------------------
class AccountingTaskManagerResultClassic(AccountingTaskManagerResult):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(AccountingTaskManagerResultClassic, self).__init__()

    #-------------------------------------------------------------------------
    def ATMRC_AddCreated(self, created):
        self._created += created

    #-------------------------------------------------------------------------
    def ATMRC_AddUpdated(self, updated):
        self._updated += updated

    #-------------------------------------------------------------------------
    def ATMRC_AddExceptions(self, exceptions):
        self._exceptions += exceptions

    #-------------------------------------------------------------------------
    def ATMRC_AddFailedObjects(self, failedObjects):
        self._failedObjects.extend(failedObjects)