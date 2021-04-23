""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/reconciliation_documents/delete/FDeleteReconciliationDocumentsPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FDeleteReconciliationDocumentsPerform - Module to delete business processes

DESCRIPTION


ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FReconciliationDocumentsPerform
import importlib
importlib.reload(FReconciliationDocumentsPerform)
from FBDPCurrentContext import Summary

def perform(params):
    params['other_params'] = {
        'task': 'deleting',
        'src_archive_status': int(not params['NonArchived']),
        'action': Summary().DELETE,
    }
    FReconciliationDocumentsPerform.perform(
        params, DeleteReconciliationDocuments
    )
    return

class DeleteReconciliationDocuments(
    FReconciliationDocumentsPerform.ReconciliationDocumentsPerform
):
    # override
    def processObj(self, obj):
        if (not self.testmode and
            obj.record_type != 'ReconciliationItem'):
            obj.delete()

        return
