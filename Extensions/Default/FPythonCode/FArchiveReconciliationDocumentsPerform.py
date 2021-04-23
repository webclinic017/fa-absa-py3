""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/reconciliation_documents/archive/FArchiveReconciliationDocumentsPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FArchiveReconciliationDocumentsPerform -
        Module to archive business processes

DESCRIPTION


ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FReconciliationDocumentsPerform
import importlib
importlib.reload(FReconciliationDocumentsPerform)
from FBDPCurrentContext import Summary

def perform(params):
    dearchive = bool(params['Dearchive'])
    params['other_params'] = {
        'task': 'de-archiving' if dearchive else 'archiving',
        'src_archive_status': 1 if dearchive else 0,
        'action': Summary().DEARCHIVE if dearchive else Summary().ARCHIVE,
    }
    FReconciliationDocumentsPerform.perform(
        params, ArchiveReconciliationDocuments
    )
    return

class ArchiveReconciliationDocuments(
    FReconciliationDocumentsPerform.ReconciliationDocumentsPerform
):
    # constructor
    def __init__(self, testmode, baseParams, otherParams):
        super(ArchiveReconciliationDocuments, self).__init__(
            testmode, baseParams, otherParams
        )
        self.new_archive_status = int(not bool(self._src_archive_status))

    # override
    def processObj(self, obj):
        if not self.testmode:
            obj = obj.clone()
            obj.archive_status = self.new_archive_status
            obj.commit()

        return obj
