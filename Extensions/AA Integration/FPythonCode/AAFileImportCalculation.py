""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAFileImportCalculation.py"
"""----------------------------------------------------------------------------
MODULE
    AAFileImportCalculation - Run script GUI for performing AA calculations
        on CSV import file data.

    (c) Copyright 2016 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import sys

import acm

import FRunScriptGUI

import AAIntegrationUtility
import importlib
importlib.reload(AAIntegrationUtility)
import AAIntegrationGuiCommon
importlib.reload(AAIntegrationGuiCommon)
import AAFileImportCalculationClasses
importlib.reload(AAFileImportCalculationClasses)


CALCULATION_TYPES = ('Main', 'Correction', 'What-if')
# Misc variables
SINKS = AAFileImportCalculationClasses.Manager.SINKS
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

# Tabs
ael_variables = [
    #[VariableName,
    #    DisplayName,
    #    Type, CandidateValues, Default,
    #    Mandatory, Multiple, Description, InputHook, Enabled]
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
    ['FilePath',
        'Import file path',
        directorySelection, None, directorySelection,
        1, 1, ttFile, None, 1],
    ['CalculationType',
        'Calculation type',
        'string', CALCULATION_TYPES, None,
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
ael_variables.extend(AAIntegrationGuiCommon.getLoggingAelVariables(
    sys.modules[__name__], 'aa_saccr.log'
))
ael_variables = FRunScriptGUI.AelVariablesHandler(ael_variables, __name__)

def ael_main(ael_params):
    import AACalculationPerform
    importlib.reload(AACalculationPerform)

    ael_params['AnalysisType'] = 'CSV Import'
    AACalculationPerform.execute_perform(
        name=__name__, ael_params=ael_params,
        calc_manger=AAFileImportCalculationClasses.Manager())
    return
'''
def createCalculationConstructorKwArgs(ael_params):
    get_path = lambda key: AAIntegrationUtility.forwardSlashedPath(
        path=ael_params[key], real=True
    )
    dictionary = ael_params
    ref_date = ael_params['RefDate']
    file_path = get_path(key='FilePath')
    cube_catalog = ael_params['CubeCatalog']
    cube_name = ael_params['CubeName']
    kwargs = {
        'dictionary': dictionary,
        'file_path': file_path,
        'ref_date': ref_date,
        'cube_catalog': cube_catalog,
        'cube_name': cube_name
    }
    return kwargs
'''
