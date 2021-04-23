""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/archive/FArchivePackages.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FArchivePackages - Archive instrument/deal packages

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import FPackagesProcessing
import importlib
importlib.reload(FPackagesProcessing)

glob_vars = FPackagesProcessing.glob_vars
glob_vars['preserve_pl'] = True

# Archive specific input hook
def input_hook(index, field_values):
    assert ael_variables[index][0] == 'Dearchive'
    lookup_archived = bool(int(field_values[index]))
    field_values = FPackagesProcessing.performOnArchivedObjectsCb(
        perform_on_archived_objs=lookup_archived,
        field_values=field_values
    )
    preserve_pl = getattr(ael_variables, 'PreservePL')
    preserve_pl.enable(not lookup_archived, 'Untick Dearchive to enable')
    if lookup_archived:
        glob_vars['preserve_pl'] = field_values[preserve_pl.sequenceNumber]
        field_values[preserve_pl.sequenceNumber] = 0
    else:
        field_values[preserve_pl.sequenceNumber] = glob_vars['preserve_pl']

    return field_values

# Additional AEL variables
ttDearchive = 'Select to dearchive instrument/deal packages.'
ttPreservePL = 'Preserve P/L'
ael_variables_to_prepend = (
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled]
    ['Dearchive',
            'De-archive',
            'int', [0, 1], 0,
            1, False, ttDearchive, input_hook, True],
)
ael_variables_to_append = (
    ['PreservePL',
           ttPreservePL,
           'int', [1, 0], 1,
           0, False, ttPreservePL, None, True],
)

# Initialisation block
ael_variables = FPackagesProcessing.init(
    script_name='ArchivePackages',
    ael_variables_to_prepend=ael_variables_to_prepend,
    ael_variables_to_append=ael_variables_to_append
)

# Wrapper function for FPackagesProcessing.ael_main execution
def ael_main(params):
    import FArchivePackagesPerform
    importlib.reload(FArchivePackagesPerform)

    FPackagesProcessing.aelMain(FArchivePackagesPerform, params)
