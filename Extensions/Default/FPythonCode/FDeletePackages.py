""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/delete/FDeletePackages.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDeletePackages - Delete instrument/deal packages

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import FPackagesProcessing
import importlib
importlib.reload(FPackagesProcessing)

# Delete specific input hook
def non_archived_cb(index, field_values):
    assert ael_variables[index][0] == 'NonArchived'
    lookup_archived = not bool(int(field_values[index]))
    field_values = FPackagesProcessing.performOnArchivedObjectsCb(
        perform_on_archived_objs=lookup_archived,
        field_values=field_values
    )
    return field_values

# Additional AEL variables
ttNonArchived = (
    'Delete non-archived instrument/deal packages only if selected. '
    'Otherwise only archived instrument/deal packages will be deleted.'
)
ael_variables_to_prepend = (
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled]
    ['NonArchived',
            'Delete non-archived',
            'int', [0, 1], 0,
            1, False, ttNonArchived, non_archived_cb, True],
)

# Initialisation block
ael_variables = FPackagesProcessing.init(
    script_name='DeletePackages',
    ael_variables_to_prepend=ael_variables_to_prepend
)

# Wrapper function for FPackagesProcessing.ael_main execution
def ael_main(params):
    import FDeletePackagesPerform
    importlib.reload(FDeletePackagesPerform)

    FPackagesProcessing.aelMain(FDeletePackagesPerform, params)
