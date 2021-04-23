""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_processes/delete/FDeleteBusinessProcesses.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FDeleteBusinessProcesses - Delete business processes

DESCRIPTION

NOTE

ENDDESCRIPTION
---------------------------------------------------------------------------"""

import FBusinessProcesses
import importlib
importlib.reload(FBusinessProcesses)

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
            1, False, ttNonArchived, None, None],
)

# Initialisation block
ael_variables = FBusinessProcesses.init(
    script_name='DeleteBusinessProcesses',
    ael_variables_to_prepend=ael_variables_to_prepend
)

# Wrapper function for FBusinessProcesses.ael_main execution
def ael_main(params):
    import FDeleteBusinessProcessesPerform
    importlib.reload(FDeleteBusinessProcessesPerform)

    FBusinessProcesses.aelMain(FDeleteBusinessProcessesPerform, params)
