""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FPFEExport.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPFEExport - Module which export the PFE XML column on the instrument.

DESCRIPTION
    This is the start-script for the Export PFE XML procedure. It mainly
    contains the parameter GUI. The script FPFEExportPerform then takes
    over the execution of the procedure.
----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',)


qInstruments = FBDPGui.insertInstruments(generic=None)
qStoredFolder = FBDPGui.insertInstrumentStoredFolder()

def disable_variables(variables, enable=0, disabledTooltip=None):
    for i in variables:
        getattr(ael_variables, i).enable(enable, disabledTooltip)

def cbCollateral(index, fieldValues):
    if fieldValues[index] == '0':
        disable_variables(('GenerateCollateralProfile', 'CollateralProfilePartitionByDeal'), fieldValues[index],
            'Include collateral in calculation must be enabled.')
        fieldValues[getattr(ael_variables, 'GenerateCollateralProfile').sequenceNumber] = 'No'
        fieldValues[getattr(ael_variables, 'CollateralProfilePartitionByDeal').sequenceNumber] = 'No'
    else:
        disable_variables(('GenerateCollateralProfile', ), fieldValues[index],
            'Include collateral in calculation must be enabled.')
    return fieldValues
    
def cbCollateralProfile(index, fieldValues):
    disable_variables(('CollateralProfilePartitionByDeal',), fieldValues[index] != 'No',
            'Need to generate collateral profile to be able to partition by deal.')
    if fieldValues[index] == 'No':
        fieldValues[getattr(ael_variables, 'CollateralProfilePartitionByDeal').sequenceNumber] = 'No'
    return fieldValues
    
def cbCashflowProfile(index, fieldValues):
    disable_variables(('CashflowProfileCurrencyOptions', ), fieldValues[index] != 'No',
            'Need to generate cashflow profile to be able to specify this option.')
    return fieldValues
    
def cbInputDataExportPath(index, fieldValues):
    disable_variables(('InputExportPath',), fieldValues[index], )
    disable_variables(('AppendDateToInputDataDir',), fieldValues[index], )
    return fieldValues

def cbOutputDataExportPath(index, fieldValues):
    disable_variables(('OutputExportPath', ), fieldValues[index], )
    disable_variables(('AppendDateToOutputDataDir',), fieldValues[index], )
    return fieldValues

def cbInputIns(index, fieldValues):
    for i in ('Instruments', 'InstrumentsQuery'):
        if index != getattr(ael_variables, i).sequenceNumber:
            disable_variables((i, ), (not fieldValues[index]),
                'You can only select Instruments or InstrumentsQuery.')
    return fieldValues

# ## Tool Tip


ttSelIns = 'Save PFE XML for these instruments filtered by instrument filter.'
ttSelQuery = 'Save PFE XML for these instruments filtered by stored folder.'
ttInputExportPath = 'Input data export path'
ttAppendDateToInputFolderName = 'Append date to input export directory'
ttOutputExportPath = 'Output data export path'
ttAppendDateToOutputFolderName = 'Append date to output export directory'
ttGenerateOutputData = 'Generate output data'
ttGenerateInputData = 'Generate output data'
ttIncludeCollateralInCalculations = 'Should Collateral be included in the calculation'
ttGenerateCollateralProfile = 'Generate Collateral profile'
ttCollateralProfilePartitionByDeal = 'Should partition by deal be applied'
ttGenerateCashflowProfile = 'Generate Collateral profile'
ttCashflowProfileCurrencyOptions = 'Currency options for cashflow profiles'
ttPercentiles = ('Specify PFE percentiles. When not specified, PFE percentile value '
                'set in valuation parameter will be used')
ttDistributedCalculations = ('Use distributed calculations for improved performance')


CASHFLOW_PROFILE_CURRENCY_OPTIONS            = ['Cashflow_And_Consolidated', 'Cashflow_Currency', 'Consolidated_To_Base']
CASHFLOW_PROFILE_CURRENCY_OPTIONS_DEFAULT    = 'Cashflow_And_Consolidated'
COLLATERAL_PROFILE_PARTITION_BY_DEAL         = ['No', 'Yes']
COLLATERAL_PROFILE_PARTITION_BY_DEAL_DEFAULT = 'No'

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['distributedCalculations',
                 'Use distributed calculations',
                 'int', [0, 1], 0,
                 True, False, ttDistributedCalculations, None, True],
        ['Instruments',
                'Instruments',
                'FInstrument', None, qInstruments,
                None, 1, ttSelIns, cbInputIns, None],
        ['InstrumentsQuery',
                'Stored Folder',
                'FStoredASQLQuery', None, qStoredFolder,
                None, 1, ttSelQuery, cbInputIns, None],
        ['GenerateInputData',
                'Generate AA input data_Output settings',
                'int', ['0', '1'], None,
                0, 0, ttGenerateInputData, cbInputDataExportPath, None],
        ['AppendDateToInputDataDir',
                'Append date to folder name_Output settings',
                'int', ['0', '1'], 1,
                0, 0, ttAppendDateToInputFolderName, None, None],
        ['InputExportPath',
                'Input data export path_Output settings',
                'string', None, None,
                0, 0, ttInputExportPath, None, None],
        ['GenerateOutputData',
                'Generate AA output data_Output settings',
                'int', ['0', '1'], None,
                0, 0, ttGenerateOutputData, cbOutputDataExportPath, None],
        ['AppendDateToOutputDataDir',
                'Append date to folder name_Output settings',
                'int', ['0', '1'], 1,
                0, 0, ttAppendDateToOutputFolderName, None, None],
        ['OutputExportPath',
                'Output data export path_Output settings',
                'string', None, None,
                0, 0, ttOutputExportPath, None, None],
        ['IncludeCollateralInCalculations',
                'Include Collateral_Calculation Settings',
                'int', ['0', '1'], '1',
                0, 0, ttIncludeCollateralInCalculations, cbCollateral, None],
        ['Percentiles',
                'Percentiles_Calculation Settings',
                'string', None, None,
                0, 0, ttPercentiles, None, None],
        ['GenerateCollateralProfile',
                'Generate Collateral profile_Collateral Profile Settings',
                'string', ['No', 'Yes'], None,
                0, 0, ttGenerateCollateralProfile, cbCollateralProfile, None],
        ['CollateralProfilePartitionByDeal',
                'Partition by deal_Collateral Profile Settings',
                'string', COLLATERAL_PROFILE_PARTITION_BY_DEAL, COLLATERAL_PROFILE_PARTITION_BY_DEAL_DEFAULT,
                0, 0, ttCollateralProfilePartitionByDeal, None, None],
        ['GenerateCashflowProfile',
                'Generate Cashflow profile_Cashflow Profile Settings',
                'string', ['No', 'Yes'], None,
                0, 0, ttGenerateCashflowProfile, cbCashflowProfile, None],
        ['CashflowProfileCurrencyOptions',
                'Cashflow profile currency options_Cashflow Profile Settings',
                'string', CASHFLOW_PROFILE_CURRENCY_OPTIONS, CASHFLOW_PROFILE_CURRENCY_OPTIONS_DEFAULT,
                0, 0, ttCashflowProfileCurrencyOptions, None, None],
)


def ael_main(execParam):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPPerform
    importlib.reload(FBDPPerform)
    import FPFEExportPerform
    importlib.reload(FPFEExportPerform)

    execParam['ScriptName'] = 'Export PFE XML'
    FBDPPerform.execute_perform(FPFEExportPerform.perform, execParam)
