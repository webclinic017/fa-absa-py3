""" Compiled: 2020-01-21 09:44:05 """

#__src_file__ = "extensions/aa_integration/./etc/AAFileImportCalculation.py"
"""----------------------------------------------------------------------------
MODULE
    AAFileImportCalculation - Run script GUI for performing AA calculations
        on CSV import file data.

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

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

trdTagfileFilter=".aap Files (*.aap)|*.aap|All Files (*.*)|*.*||"
trdTag_file = FRunScriptGUI.InputFileSelection(trdTagfileFilter)
csvFilter=".csv Files (*.csv)|*.csv|All Files (*.*)|*.*||"
csv_file = FRunScriptGUI.InputFileSelection(csvFilter)
ttDirPath = 'The path to the directory containing the data files to upload.'

reference_day = [acm.Time.DateToday(),
            'Today',
            'Yesterday',
            '-1d']

def _enable(index, fieldValues):
    enable = len(fieldValues[index]) == 0
    if index == ael_variables.FilePath.sequenceNumber:
        ael_variables.FileName.enable(enable, \
            "Either FileName or FilePath could be selected.")
    elif index == ael_variables.FileName.sequenceNumber:
        ael_variables.FilePath.enable(enable, \
            "Either FileName or FilePath could be selected.")
    return fieldValues

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
        0, 1, ttFile, _enable, 1],
    ['FileName',
        'CSV Files',
        csv_file, None, csv_file,
        0, 1, ttDirPath, _enable, 1],
    ['TradeTags',
        'Trade Tags File',
        trdTag_file, None, trdTag_file,
        0, 1, ttDirPath],
    ['BookTags',
        'Book Tags File',
        csv_file, None, csv_file,
        0, 1, ttDirPath],
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
