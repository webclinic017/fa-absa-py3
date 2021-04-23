""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AASACCRCalculation.py"
"""----------------------------------------------------------------------------
MODULE
    AASACCRCalculation - Run script GUI for performing AA calculations
        on SA-CCR data.

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
import AASACCRCalculationClasses
importlib.reload(AASACCRCalculationClasses)

# Misc variables
SINKS = AASACCRCalculationClasses.Manager.SINKS
marketDataFileSelector = AAIntegrationGuiCommon.getPathSelector(is_dir=False, is_input=True)
dealsFileSelector = AAIntegrationGuiCommon.getPathSelector(is_dir=False, is_input=True)
rateFixingsFileSelector = AAIntegrationGuiCommon.getPathSelector(is_dir=False, is_input=True)

# Tooltips
ttSink= 'The calculation results sink.'
ttCurrency = 'The reference date for the report.'
ttReferenceDate = 'The reporting currency.'
ttMarketData = 'Path to the file containing the market data.'
ttDeals = 'Path to the file containing the deals.'
ttRateFixings = 'Path to the file containing rate fixings.'

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
    ['MarketDataPath',
        'Path to market data file',
        marketDataFileSelector, None, marketDataFileSelector,
        1, 1, ttMarketData, None, 1],
    ['DealsPath',
        'Path to deals file',
        dealsFileSelector, None, dealsFileSelector,
        1, 1, ttDeals, None, 1],
    ['RateFixingsPath',
        'Path to rate fixings file',
        rateFixingsFileSelector, None, rateFixingsFileSelector,
        1, 1, ttRateFixings, None, 1],
]
ael_variables.extend(AAIntegrationGuiCommon.getLoggingAelVariables(
    sys.modules[__name__], 'aa_saccr.log'
))
ael_variables = FRunScriptGUI.AelVariablesHandler(ael_variables, __name__)

def ael_main(ael_params):
    import AACalculationPerform
    importlib.reload(AACalculationPerform)

    ael_params['AnalysisType'] = 'SA-CCR'
    AACalculationPerform.execute_perform(
        name=__name__, ael_params=ael_params,
        calc_manger=AASACCRCalculationClasses.Manager()
    )
    return
