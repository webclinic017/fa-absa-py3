""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/reconciliation_documents/delete/FDeleteReconciliationDocuments.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FDeleteReconciliationDocuments - Delete business processes

DESCRIPTION

NOTE

ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FReconciliationDocuments
import importlib
importlib.reload(FReconciliationDocuments)

def archiveStatusCb(index, field_values):
    FReconciliationDocuments.ael_vars.src_archive_status = \
        1 - int(field_values[index])
    field_values = FReconciliationDocuments.ael_vars.changeDialog(
        field_values=field_values
    )
    return field_values

# Additional AEL variables
ttNonArchived = (
    'Delete non-archived business processes only if selected. '
    'Otherwise only archived business process will be deleted.'
)
ael_variables_to_prepend = (
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled]
    ['NonArchived',
            'Delete non-archived',
            'int', [0, 1], 0,
            1, False, ttNonArchived, archiveStatusCb, None],
)

# Initialisation block
ael_variables = FReconciliationDocuments.init(
    script_name='DeleteReconciliationDocuments',
    ael_variables_to_prepend=ael_variables_to_prepend
)

# Wrapper function for FReconciliationDocuments.ael_main execution
def ael_main(params):
    import FDeleteReconciliationDocumentsPerform
    importlib.reload(FDeleteReconciliationDocumentsPerform)

    FReconciliationDocuments.aelMain(
        FDeleteReconciliationDocumentsPerform, params
    )
