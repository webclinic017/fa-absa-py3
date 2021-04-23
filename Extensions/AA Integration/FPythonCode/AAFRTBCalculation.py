""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAFRTBCalculation.py"
"""----------------------------------------------------------------------------
MODULE
    AAFRTBCalculation - Run script GUI for performing AA calculation on FRTB data.

    (c) Copyright 2016 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import os
import sys

import acm

import FRunScriptGUI
import FScenarioExportUtils

import AAIntegrationUtility
import importlib
importlib.reload(AAIntegrationUtility)
import AAIntegrationGuiCommon
importlib.reload(AAIntegrationGuiCommon)
import AAFRTBCalculationClasses
importlib.reload(AAFRTBCalculationClasses)

# Misc variables
MANAGER = AAFRTBCalculationClasses.Manager
ANALYSIS_TYPES = ('SA SBA', 'SA DRC', 'SA RRAO', 'IMA ES',
        'IMA Hypothetical_PL', 'IMA Risk_Theoretical_PL',
        'IMA SES', 'IMA DRC', 'FRTB All')
CALCULATION_TYPES = ('Main', 'Correction', 'What-if')
SINKS = MANAGER.SINKS

marketdataFileFilter="Dat Files (*.dat)|*.dat|All Files (*.*)|*.*||"
resultsFileFilter=".csv Files (*.csv)|*.csv|All Files (*.*)|*.*||"
market_data = FRunScriptGUI.InputFileSelection(marketdataFileFilter)
results_data = FRunScriptGUI.InputFileSelection(resultsFileFilter)
directorySelection = FRunScriptGUI.DirectorySelection()

# Tooltips
ttSink= 'The calculation results sink.'
ttAnalysisType = 'The type of analysis to perform.'
ttCalculationType = 'The calculation type: Main, Correction, What-if.'
ttReferenceDate = 'The reference date for the report.'
ttDateDirectory = 'Use subdirectory with name equal to the given reference date.'
ttFilePath = 'The path to the data file to upload.'
ttDirPath = 'The path to the directory containing the data files to upload.'
ttFileNameSuffix = 'Only consider files ending with the specified string.'
ttAppendReferenceDate = 'Append reference date to the selected file folders.'

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
        1, 0, ttSink],
    ['AnalysisType',
        'Analysis type',
        'string', ANALYSIS_TYPES, None,
        1, 0, ttAnalysisType, None],
    ['CalculationType',
        'Calculation type',
        'string', CALCULATION_TYPES, None,
        1, 0, ttCalculationType, None],
    ['RefDate',
        'Reference date',
        'string', reference_day, acm.Time.DateToday(),
        1, 0, ttReferenceDate],
    ['AppendReferenceDate',
        'Append Reference date to the selected file folders',
        'int', [1, 0], 1,
        0, 0, ttAppendReferenceDate],
    ['SASBASensitivities',
        'SA SBA Sensitivities',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['SADRCDeals',
        'SA DRC Deals',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['SARRAODeals',
        'SA RRAO Deals',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['IMAESValuations',
        'IMA ES Valuations',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['IMASESValuations',
        'IMA SES Valuations',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['IMADRCDeals',
        'IMA DRC Deals',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['IMAHypotheticalPL',
        'IMA Hypothetical PL',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['IMARiskTheoPL',
        'IMA Risk Theoretical PL',
        directorySelection, None, directorySelection,
        0, 1, ttDirPath],
    ['MarketData',
        'IMA DRC Market Data file',
        market_data, None, market_data,
        0, 1, ttDirPath],
    ['Extension',
        'File name extension',
        'string', None, '.csv',
        0, 0, ttFileNameSuffix],
]
'''
  <Property name="Static Data" value="" />
  <Property name="Trade Tags" value="" />
    <Property name="IMA DRC Deals" value="" />
    <Property name="Book Tags" value="" />
    <Property name="SA DRC Static Data" value="" />
    <Property name="IMA DRC Scenarios" value="10000" />
    <Property name="Factor Grouping Data" value="" />
    <Property name="SA RRAO Static Data" value="" />
    <Property name="IMA DRC Risk Factor Archive" value="" />
    <Property name="Adjust To External MtM" value="Yes" />
    <Property name="Rate Fixings" value="" />
    <Property name="Reporting Currency" value="" />
    <Property name="Base Date" value="" />
    <Property name="Issue Data" value="" />
    <Property name="SA RRAO External Trade Data" value="" />
    <Property name="Destination Cube" value="Default" />
    <Property name="IMA ES External Data" value="" />
    <Property name="IMA ES Scenario Data" value="" />
    <Property name="IMA NMRF External Data" value="" />
    <Property name="Destination Catalog" value="Market Risk" />
    <Property name="Market Data" value="" />
    <Property name="SA DRC External Trade Data" value="" />
    <Property name="Calendar Data" value="" />
    <Property name="SA SBA External Sensitivities" value="" />
    <Property name="Proxying Rules" value="" />
    <Property name="IMA DRC Seed" value="1" />
    <Property name="SA SBA Static Data" value="" />
'''
ael_variables.extend(AAIntegrationGuiCommon.getLoggingAelVariables(
    sys.modules[__name__], 'aa_frtb.log'
))
ael_variables = FRunScriptGUI.AelVariablesHandler(ael_variables, __name__)

def ael_main(ael_params):
    import AACalculationPerform
    importlib.reload(AACalculationPerform)

    #ael_params['DirPath'] = str(ael_params['DirPath'])
    #if ael_params['UseDateDir'] and not ael_params['RefDate']:
    #    raise AssertionError('Reference required')

    analysis_type = ael_params['AnalysisType'] = str(ael_params['AnalysisType']).strip()
    if analysis_type not in ANALYSIS_TYPES:
        msg = 'Invalid analysis type, select from:', ANALYSIS_TYPES
        raise AssertionError(msg)

    AACalculationPerform.execute_perform(
        name=__name__, ael_params=ael_params,
        calc_manger=MANAGER())
    return
