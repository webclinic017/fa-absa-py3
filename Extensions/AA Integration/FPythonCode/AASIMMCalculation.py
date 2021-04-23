""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASIMMCalculation.py"
"""----------------------------------------------------------------------------
MODULE
    AASIMMCalculation - Run script GUI for performing AA SIMM calculations.

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
import AASIMMCalculationClasses
importlib.reload(AASIMMCalculationClasses)


marketdataFileFilter="Dat Files (*.dat)|*.dat|All Files (*.*)|*.*||"
market_data = FRunScriptGUI.InputFileSelection(marketdataFileFilter)
staticDataFileSelector = AAIntegrationGuiCommon.getPathSelector(is_dir=False, is_input=True)

CALCULATION_TYPES = ('Main', 'Correction', 'What-if')
# Misc variables
SINKS = AASIMMCalculationClasses.Manager.SINKS
directorySelection = FRunScriptGUI.DirectorySelection()

# Tooltips
ttSink= 'The calculation results sink.'
ttReferenceDate = 'The reference date.'
ttCurrency = 'The reporting currency.'
ttFile = 'Path to the CRIF file.'
ttCubeCatalog = 'Name of the cube catalog.'
ttCubeName = 'Name of the cube.'
ttAppendReferenceDate = 'Append reference date to the selected file folder.'
ttCalculationType = 'The calculation type: Main, Correction, What-if.'
ttDirPath = 'The path to the directory containing the data files to upload.'
ttStaticData = 'Path to the file containing static data.'
ttHorizon ='Calculation horizon'
ttIsCounterParty = 'CounterParty\'s sensitivities file or not.'
ttCounterParty = 'Counter party'
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
    ['Currency',
        'Reporting currency',
        'FCurrency', None, None,
        1, 0, ttCurrency],
    ['AppendReferenceDate',
        'Append Reference date to the selected file folder',
        'int', [1, 0], 1,
        0, 0, ttAppendReferenceDate],
    ['MarketDataPath',
        'Market Data file',
        market_data, None, market_data,
        1, 1, ttDirPath],
    ['CRIFFilePath',
        'Sensitivities file path',
        directorySelection, None, directorySelection,
        1, 1, ttFile, None, 1],
    ['StaticDataPath',
        'Path to static data file',
        staticDataFileSelector, None, staticDataFileSelector,
        1, 1, ttStaticData, None, 1],
    ['CalculationType',
        'Calculation type',
        'string', CALCULATION_TYPES, None,
        1, 0, ttCalculationType, None],
    ['Horizon',
        'Horizon',
        'string', '10d', '10d',
        1, 0, ttHorizon, None],
    ['IsCounterParty',
        'Counterparty CRIF file',
        'int', [1, 0], 0,
        1, 0, ttIsCounterParty, None],
    ['CounterParty',
        'Counter Party',
        'string', None, '',
        0, 0, ttCounterParty, None],
    ['CubeCatalog',
        'Destination Catalog',
        'string', None, 'Credit Risk',
        1, 1, ttCubeCatalog, None, 1],
    ['CubeName',
        'Destination Cube',
        'string', None, 'Default',
        1, 1, ttCubeName, None, 1],
]
ael_variables.extend(AAIntegrationGuiCommon.getLoggingAelVariables(
    sys.modules[__name__], 'aa_simm.log'))
ael_variables = FRunScriptGUI.AelVariablesHandler(ael_variables, __name__)

def ael_main(ael_params):
    import AACalculationPerform
    importlib.reload(AACalculationPerform)

    ael_params['AnalysisType'] =  'SIMM'
    AACalculationPerform.execute_perform(
        name=__name__, ael_params=ael_params,
        calc_manger=AASIMMCalculationClasses.Manager())
    return
