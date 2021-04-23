""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_processes/archive/FArchiveBusinessProcesses.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FArchiveBusinessProcesses - Archive business processes

DESCRIPTION

NOTE

ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FBusinessProcesses
import importlib
importlib.reload(FBusinessProcesses)

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
            1, False, ttDearchive, None, None],
)

# Initialisation block
ael_variables = FBusinessProcesses.init(
    script_name='ArchiveBusinessProcesses',
    ael_variables_to_prepend=ael_variables_to_prepend
)

# Wrapper function for FBusinessProcesses.ael_main execution
def ael_main(params):
    import FArchiveBusinessProcessesPerform
    importlib.reload(FArchiveBusinessProcessesPerform)

    FBusinessProcesses.aelMain(FArchiveBusinessProcessesPerform, params)
