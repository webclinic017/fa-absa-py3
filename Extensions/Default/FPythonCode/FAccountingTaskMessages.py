""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/distribution/FAccountingTaskMessages.py"

import uuid

import FAccountingTaskTraits

# operations
from FOperationsTaskManager import TaskManager

#-------------------------------------------------------------------------
class AccountingTaskMessage(TaskManager.MessageCreator):

    #-------------------------------------------------------------------------
    @staticmethod
    def MC_CreateMessage(params, objIds):

        definition = FAccountingTaskTraits.Definition()
        definition.objIds.extend(objIds)
        definition.targetClass = params['targetClass']
        definition.startDate = params['startDate']
        definition.endDate = params['endDate']
        definition.endOfDayDate = params['endOfDayDate']
        definition.processDate = params['processDate']
        definition.bookIds.extend([book.Oid() for book in params['bookIds']])
        definition.treatmentIds.extend([treatment.Oid() for treatment in params['treatmentIds']])
        definition.aiIds.extend([ai.Oid() for ai in  params['aiIds']])
        definition.testMode = params['testMode']
        definition.guid = str(uuid.uuid1())
        return definition