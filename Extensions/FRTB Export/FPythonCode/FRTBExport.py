""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBExport.py"
"""---------------------------------------------------------------------------
MODULE
    BaseExport - Base class for exporting FRTB values + helper GUI methods.

    (c) Copyright 2017 FIS Front Arena. All rights reserved.

DESCRIPTION

---------------------------------------------------------------------------"""
import os
import sys

import acm

import FRTBCommon
import FRTBUtility

import FExportCalculatedValuesMain
import FRunScriptGUI

class Export(object):
    """
    Base class for exporters (should be one per export calculation type).
    Every FRTB contribution exporter script should contain the following
    class signatures:

    class <result collector with any name>(FRTBBaseWriter.ResultsCollector):
        pass
    class <writer with any name>(FRTBBaseWriter.Writer):
        pass
    class <CALC_GROUP><CALC_NAME>Export(FRTBExport.Export):
        RESULTS_COLLECTOR_CLASS = <matching results collector>
        WRITER_CLASSES = (<matching writer1>, etc...)
    """
    # Requires overriding
    RESULTS_COLLECTOR_CLASS = WRITER_CLASSES = None

    # Overriding optional (otherwise automatically set in instance)
    CALC_NAME = CALC_NAME_LONG = None
    REQUIRES_IS_OPTION = False

    # Automatically set
    CALC_GROUP = CALC_CLASS = CALC_CLASS_LONG = None

    def __init__(self):
        for name in ('GROUP', 'CLASS', 'CLASS_LONG', 'NAME', 'NAME_LONG'):
            name = 'CALC_' + name
            assert getattr(self, name, None), \
                'Exporter class attribute \'%s\' must be defined' % name

        assert self.RESULTS_COLLECTOR_CLASS, \
            'Exporter requires attribute \'RESULTS_COLLECTOR_CLASS\''
        assert self.WRITER_CLASSES, \
            'Exporter requires attribute \'WRITER_CLASSES\''
        self._ael_vars = []
        self._additional_writer_kwargs = {}
        self._run_perform = True
        self._ctx = acm.GetDefaultContext()

    def getAelVariables(self):
        self._ael_vars.append(self.getPerformCalculationAelVariable())
        return self._ael_vars

    def getPerformCalculationAelVariable(
        self, calc_name=None, tab_suffix='', tooltip=None
    ):
        calc_name = calc_name or self.CALC_NAME_LONG
        def cb(index, field_values):
            enable = bool(int(field_values[index]))
            return self.enableAelVars(enable, index, field_values, calc_name)

        a_var = getPerformCalculationAelVariable(
            calc_name=self.CALC_NAME, calc_name_long=calc_name,
            tab_suffix=tab_suffix, tooltip=tooltip, callback=cb
        )
        return a_var

    def enableAelVars(
        self, enable=False, ref_idx=None, field_values=None, calc_name=None
    ):
        if enable is None:
            enable = self._run_perform

        calc_name = calc_name or self.CALC_NAME_LONG
        ttDisabled = 'To enable the %s calculation must be enabled' % calc_name
        for idx, a_vars in enumerate(self._ael_vars):
            if a_vars[0].endswith('Enable'):
                continue

            if (idx != ref_idx) and a_vars[0].startswith(self.CALC_NAME):
                a_vars.enable(enable, ttDisabled)

        return field_values

    def isEnabled(self, parameters=None):
        if parameters:
            enabled_key = self.CALC_NAME + 'Enable'
            self._run_perform = self._additional_writer_kwargs[enabled_key] = \
                bool(int(parameters[enabled_key]))

        if not self._run_perform:
            self.enableAelVars()

        return self._run_perform

    def setInternalParameters(self, parameters):
        for k in self._additional_writer_kwargs.keys():
            if k.startswith(self.CALC_NAME):
                del self._additional_writer_kwargs[k]

        self._run_perform = self.isEnabled(parameters=parameters)
        return

    def getAdditionalWriterKwargs(self):
        return self._additional_writer_kwargs.copy()

    def makeColumn(
        self, column_id, column_name=None, config=None,
        params=None, scenario=None, dimension_names=None,
        vector=None
    ):
        column = FExportCalculatedValuesMain.createColumnConfiguration(
            columnID=column_id, extensionContext=self._ctx,
            customName=column_name or column_id,
            scenario=scenario, timebuckets=None,
            vector=vector, parameters=params,
            scenarioDimensionNames=dimension_names,
            vectorConfiguration=config
        )
        return column

    def makeDynamicColumnConfig(self, column_id, params=None):
        config = acm.Risk.CreateDynamicVectorConfiguration(
            self._ctx.Name(), column_id, params or acm.FDictionary()
        )
        return config

    def makeDynamicScenario(self, template_name, scenario_params=None):
        scenario = acm.Risk.CreateDynamicScenario(
            self._ctx, template_name, scenario_params or acm.FDictionary()
        )
        return scenario

    def makeColumns(self, parameters):
        assert self._run_perform, 'Exporter not enabled'
        columns = []
        if self.REQUIRES_IS_OPTION:
            columns.append(
                self.makeColumn(column_id=FRTBCommon.IS_OPTION_COLUMN_ID)
            )

        return columns

    def resetAelVariables(self, ael_variables):
        self._ael_vars = ael_variables
        return

    """
    Uncomment and use the following if each calculation type requires the
    risk factor and/or position spec in it's own tab

    def getRiskFactorSetupAelVariables(
        self, enum_str, setup_only=False, tab_suffix=''
    ):
        a_vars = getRiskFactorAelVariables(
            enum_str=enum_str, setup_only=setup_only, prefix=self.CALC_NAME,
            tab_suffix=tab_suffix or self.CALC_NAME_LONG
        )
        return a_vars

    def getPositionAelVariables(self, tab_suffix=''):
        a_vars = getPositionAelVariables(
            prefix=self.CALC_NAME, tab_suffix=tab_suffix or self.CALC_NAME_LONG
        )
        return a_vars
    """

def getInputFileSelector():
    return FRunScriptGUI.InputFileSelection('All Files (*.*)|*.*||')

def getOutputFileSelector():
    return FRunScriptGUI.OutputFileSelection('All Files (*.*)|*.*||')

def getPerformCalculationAelVariable(
    calc_name, calc_name_long, tab_suffix='', tooltip=None, callback=None
):
    calc_name_long = calc_name_long.lower()
    tooltip = tooltip or 'Select to enable %s calculations' % calc_name_long
    #[VariableName,
    #    DisplayName,
    #    Type, CandidateValues, Default,
    #    Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
    ael_variable = [calc_name + 'Enable',
        'Perform %s calculation%s' % (
            calc_name_long, ('_' + tab_suffix) if tab_suffix else ''
        ),
        'int', [0, 1], 0,
        1, 0, tooltip, callback
    ]
    return ael_variable

def getRiskFactorAelVariables(
    risk_classes, setup_only=False, prefix='', tab_suffix=''
):
    # tool tips
    ttRiskFactorSetup = 'The Risk Factor Setup, repository for the risk factors.'
    ttRiskClassNames = 'Only Risk Factors of this risk class will be shifted.'
    ttHierarchy = 'The hierarchy containing liquidity horizon data.'

    if isinstance(risk_classes, type('')):
        risk_classes = acm.FEnumeration[risk_classes].Values()

    risk_classes = sorted(rc for rc in risk_classes if rc)
    if tab_suffix:
        tab_suffix = '_' + tab_suffix

    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        [prefix + 'riskFactorSetup',
            'Risk factor setup' + tab_suffix,
            acm.FRiskFactorSetup, acm.FRiskFactorSetup.Select(''), None,
            1, 0, ttRiskFactorSetup]
    ]
    if not setup_only:
        ael_variables.extend([
            [prefix + 'riskClassNames',
                'Risk classes' + tab_suffix,
                'string', risk_classes, None,
                1, 1, ttRiskClassNames],
            [prefix + 'hierarchy',
                'Hierarchy' + tab_suffix,
                acm.FHierarchy, None, None,
                1, 0, ttHierarchy],
        ])

    return ael_variables

def getDistributeCalculation(prefix='', tab_suffix=''):

    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        [prefix + 'distributedCalculations',
                 'Use distributed calculations',
                 'int', [0, 1], 0, True, False,
                 'Use distributed calculations for improved performance',
                 None, True],
        ]
    return ael_variables

def getPositionAelVariables(prefix='', tab_suffix=''):
    # tool tips
    ttPositionSpec = (
        'Used to define the positions and specifies which trade attributes '
        'to report.'
    )
    ttPortfolios = 'The physical portfolios to which the trades belong.'
    ttTradeFilters = 'The selection of trade filters.'
    ttTradeQueries = (
        'The stored ASQL queries, queries shown are shared and of type trade.'
    )

    tradeQueries = acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
    if tab_suffix:
        tab_suffix = '_' + tab_suffix

    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        [prefix + 'Position Specification',
            'Position specification' + tab_suffix,
            acm.FPositionSpecification, None, None,
            1, 0, ttPositionSpec],
        [prefix + 'Portfolios',
            'Portfolios' + tab_suffix,
            acm.FPhysicalPortfolio, None, None,
            0, 1, ttPortfolios],
        [prefix + 'Trade Filters',
            'Trade filters' + tab_suffix,
            acm.FTradeSelection, None, None,
            0, 1, ttTradeFilters],
        [prefix + 'Trade Queries',
            'Trade queries' + tab_suffix,
            acm.FStoredASQLQuery, tradeQueries, None,
            0, 1, ttTradeQueries],
    ]
    return ael_variables

def getOutputAelVariables():
    # tool tips
    ttOutputDir = (
        'Path to the directory where the reports should be '
        'created. Environment variables can be used for '
        'Windows (%VAR%) or Unix ($VAR).'
    )
    ttPrefix = 'Optional prefix for output file names.'
    ttExtension = 'Extension used for output file names.'
    ttDateDir = (
        'Create a directory with the todays date as the directory name'
    )
    ttOverwrite = (
        'If a file with the same name and path already exists, overwrite it.'
    )
    ttCalcType = (
        'Based on Calculation Type selection,'
        ' results will be stored in appropriate folder structure.'
    )

    directorySelection = FRunScriptGUI.DirectorySelection()
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['OutputDir',
            'Directory path_Output settings',
            directorySelection, None, directorySelection,
            1, 1, ttOutputDir, None, 1],
        ['Prefix',
            'Output file prefix_Output settings',
            'string', None, '',
            0, 0, ttPrefix],
        ['Extension',
            'Output file extension_Output settings',
            'string', None, '.csv',
            0, 0, ttExtension],
        ['DateDir',
            'Create directory with todays date_Output settings',
            'int', [0, 1], 1,
            1, 0, ttDateDir],
        ['Overwrite',
            'Overwrite if files exist_Output settings',
            'int', [0, 1], 1,
            1, 0, ttOverwrite],
        ['CalcType',
            'Calculation type',
            'string', ['Main', 'Corrections', 'WhatIf'], None,
            2, 0, ttCalcType],
    ]
    return ael_variables

def getLoggingAelVariables(caller, log_filename):
    def logfile_cb(index, fieldValues):
        caller.ael_variables.Logfile.enable(
            fieldValues[index],
            'You have to check Log To File to be able to select a Logfile.'
        )
        return fieldValues

    logFileSelection = getOutputFileSelector()
    logFileSelection.SelectedFile = os.path.join('C:\\', 'temp', log_filename)
    ttLogMode = 'Defines the amount of logging produced.'
    ttLogToCon = (
        'Whether logging should be done in the Log Console or not.'
    )
    ttLogToFile = 'Defines whether logging should be done to file.'
    ttLogFile = (
        'Name of the logfile. Could include the whole path, c:\temp\...'
    )
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['Logmode',
            'Logmode_Logging',
            'int', [1, 2, 3, 4], 1,
            1, 0, ttLogMode],
        ['LogToConsole',
            'Log to console_Logging',
            'int', [0, 1], 1,
            1, 0, ttLogToCon],
        ['LogToFile',
            'Log to file_Logging',
            'int', [0, 1], 1,
            1, 0, ttLogToFile, logfile_cb],
        ['Logfile',
            'Logfile_Logging',
            logFileSelection, None, logFileSelection,
            0, 1, ttLogFile, None, None],
    ]
    return ael_variables

def createAelVariables(ael_vars_list, exporters, log_filename):
    caller = FRTBUtility.getCaller()
    for exporter in exporters:
        ael_vars_list.extend(exporter.getAelVariables())

    ael_vars_list.extend(getOutputAelVariables())
    ael_vars_list.extend(getLoggingAelVariables(
        caller=caller, log_filename=log_filename
    ))
    ael_vars = FRunScriptGUI.AelVariablesHandler(
        ael_vars_list, caller.__name__
    )
    for exporter in exporters:
        exporter.resetAelVariables(ael_variables=ael_vars)

    return ael_vars
