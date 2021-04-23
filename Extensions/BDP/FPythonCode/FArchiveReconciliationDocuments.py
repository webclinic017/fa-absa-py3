""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/reconciliation_documents/archive/FArchiveReconciliationDocuments.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FArchiveReconciliationDocuments - Archive business processes

DESCRIPTION

NOTE

ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FReconciliationDocuments
import importlib
importlib.reload(FReconciliationDocuments)

def archiveStatusCb(index, field_values):
    FReconciliationDocuments.ael_vars.src_archive_status = \
        int(field_values[index])
    field_values = FReconciliationDocuments.ael_vars.changeDialog(
        field_values=field_values
    )
    return field_values

# Additional AEL variables
ttDearchive = 'Select to dearchive business process'
ael_variables_to_prepend = (
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled]
    ['Dearchive',
            'De-archive',
            'int', [0, 1], 0,
            1, False, ttDearchive, archiveStatusCb, None],
)

# Initialisation block
ael_variables = FReconciliationDocuments.init(
    script_name='ArchiveReconciliationDocuments',
    ael_variables_to_prepend=ael_variables_to_prepend
)

# Wrapper function for FReconciliationDocuments.ael_main execution
def ael_main(params):
    import FArchiveReconciliationDocumentsPerform
    importlib.reload(FArchiveReconciliationDocumentsPerform)

    FReconciliationDocuments.aelMain(
        FArchiveReconciliationDocumentsPerform, params
    )
