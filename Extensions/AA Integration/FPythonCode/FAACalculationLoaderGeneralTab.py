""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/FAACalculationLoaderGeneralTab.py"
"""----------------------------------------------------------------------------
MODULE
    FAACalculationLoaderGeneralTab - General setting.

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    
----------------------------------------------------------------------------"""


import acm
import FRunScriptGUI

CALCULATION_TYPES = ('Main', 'Correction', 'What-if')
# Misc variables
SINKS = ('artiQ', 'artiQ Store')
directorySelection = FRunScriptGUI.DirectorySelection()

# Tooltips
ttSink= 'The calculation results sink.'
ttReferenceDate = 'The reporting currency.'
ttFile = 'Path to the CSV import file.'
ttCubeCatalog = 'Name of the cube catalog.'
ttCubeName = 'Name of the cube.'
ttAppendReferenceDate = 'Append reference date to the selected file folder.'
ttCalculationType = 'The calculation type: Main, Correction, What-if.'

reference_day = [acm.Time.DateToday(),
            'Today',
            'Yesterday',
            '-1d']

class AACalculationLoaderGeneralTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                # ExportCalculatedValues expects these to be strings for now.
                ['Sink',
                    'AA results sink',
                    'string', SINKS, SINKS[0],
                    1, 0, ttSink, None],
                ['RefDate',
                    'Reference date',
                    'string', reference_day, acm.Time().DateToday(),
                    1, 0, ttReferenceDate],
                ['AppendReferenceDate',
                    'Append Reference date to the selected file folder',
                    'int', [1, 0], 1,
                    0, 0, ttAppendReferenceDate],
                ['CalculationType',
                    'Calculation type',
                    'string', CALCULATION_TYPES, 'Main',
                    1, 0, ttCalculationType, None],        
                ['CubeCatalog',
                    'Destination Catalog',
                    'string', None, 'Market Risk',
                    1, 1, ttCubeCatalog, None, 1],
                ['CubeName',
                    'Destination Cube',
                    'string', None, 'Default',
                    1, 1, ttCubeName, None, 1],
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    ael_vars = AACalculationLoaderGeneralTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars
