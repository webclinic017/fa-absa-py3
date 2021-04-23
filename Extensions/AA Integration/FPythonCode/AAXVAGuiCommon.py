""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVAGuiCommon.py"
import os
import sys

import acm

import FRunScriptGUI

import AAIntegrationGuiCommon
import AAIntegrationUtility
import AAXVAUtility
import importlib

DATES = AAXVAUtility.DATES
INSTRUMENTS = AAXVAUtility.INSTRUMENTS

class Export(object):
    _EXPORTER = None
    _PREFIX = None

    def __init__(self):
        self._ael_vars = []

    def resetAelVariables(self, ael_variables):
        self._ael_vars = ael_variables

    def addTab(self):
        self._ael_vars.extend(self._getAelVariables())
        return self._ael_vars

    def shouldPerform(self, ael_params):
        return bool(int(ael_params[self._PREFIX + '_DoExport']))

    def doExportCb(self, index, field_values, callback):
        for var in self._ael_vars:
            name = var[0]
            if not name.startswith(self._PREFIX):
                continue

            name = name.split('_')[1]
            field_values = callback(
                name=name, ael_var=var, field_values=field_values
            )

        return field_values

    def getDoExportCb(self, callback):
        cb = lambda index, field_values: self.doExportCb(
            index=index, field_values=field_values, callback=callback
        )
        return cb

    def cbEnabled(self, ael_var, field_values):
        if ael_var.isEnabled():
            return bool(int(field_values[ael_var.sequenceNumber]))

        return False

    def cbEnableVar(self, name, enable, tt):
        getattr(self._ael_vars, name).enable(enable, tt)
        return

    def cbEnableVars(self, callee_var_name, tt, enable, vars):
        for var in vars:
            name = var[0]
            if (name != callee_var_name) and name.startswith(self._PREFIX):
                self.cbEnableVar(name=name, enable=enable, tt=tt)

        return

    def _getInputFileSelector(self):
        selector = AAIntegrationGuiCommon.getPathSelector(
            is_dir=False, is_input=True
        )
        return selector

    def _getAelVariables(self):
        raise NotImplementedError

class Exporter(object):
    NAME = None

    def __init__(self):
        assert self.NAME, 'NAME not set'

        self._output_dir = None
        self._overwrite = None
        self._ael_date = None
        self._logger = None
        self._indentation = None
        self._indentation_level = None
        self._ael_params = None
        self._output_filepaths = None
        self._calculation_types = []
        self._params_helper = None

    def getOutputDir(self):
        assert self._output_dir, 'No output directory specified'
        return self._output_dir

    def init(self, ael_params, logger, indentation, indentation_level):
        self._logger = logger
        self._ael_params = ael_params.copy()
        self._ael_date = AAXVAUtility.getAELDate(date=self._ael_params['Date'])
        self._overwrite = self._ael_params['Overwrite']
        self._output_dir = self._getOutputDir()
        self._indentation = indentation
        self._indentation_level = indentation_level
        self._output_filepaths = list()
        self._params_helper = AAXVAUtility.getAdaptivXVAParamsHelper()
        indentation = self._indentation * self._indentation_level
        msg = '%s exporter initialised.' % self.NAME
        self._logger.debug(indentation + msg)
        return

    def perform(self):
        result = AAXVAUtility.executeWithRedirectedLogger(
            func=lambda: self.performImplementation(),
            logger=self._logger
        )
        return bool(result)

    def getFilepaths(self):
        return tuple(self._output_filepaths)

    def _addCalculationType(self, calculation_type):
        if calculation_type not in self._calculation_types:
            self._calculation_types.append(calculation_type)

        return

    def _getMarketDataFilePath(self, prefix):
        path = self._getPathParam(key=prefix + '_MarketDataFile', check_path=False)
        if not path:
            date = AAXVAUtility.getACMDate(date=self._ael_params['Date'])
            path = AAXVAUtility.getMarketDataFilePath(prefix=prefix, date=date)

        assert os.path.isfile(path), param_key + ' base market data file not found'
        return AAIntegrationUtility.forwardSlashedPath(path=path)

    def _getOutputDir(self):
        dir_path = self._getPathParam(key='OutputDir', check_path=False)
        dir_path = os.path.join(dir_path, self.NAME)
        if self._ael_params['DateDir']:
            dir_path = os.path.join(dir_path, acm.Time().DateToday())

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return AAIntegrationUtility.forwardSlashedPath(path=dir_path)

    def _getOutputFilepath(self, filename, prefix):
        filepath = getOutputFilepath(
            dir_path=self._output_dir, filename=filename,
            prefix=prefix, overwrite=self._overwrite
        )
        return AAIntegrationUtility.forwardSlashedPath(path=filepath)

    def _getPathParam(self, key, check_path):
        path = AAIntegrationUtility.forwardSlashedPath(
            path=self._ael_params[key], real=False, check=check_path
        )
        return path

    def performImplementation(self):
        raise NotImplementedError

    def _setResults(self):
        raise NotImplementedError

def createExports(base_cls, suffix='Export'):
    def factory(name):
        def __init__(self):
            base_cls.__init__(self)

        new_cls = type(name, (base_cls,), {'__init__': __init__})
        return new_cls

    exports = []
    for calc_type in AAXVAUtility.CALCULATIONS_TYPES:
        export = factory(name=calc_type + suffix)
        export._PREFIX = calc_type
        exports.append(export)

    return tuple(exports)

def getOutputFilepath(dir_path, filename, prefix, overwrite, max_files=256):
    filename, ext = filename.rsplit('.', 1)
    if prefix:
        filename = '{0}_{1}'.format(prefix, filename)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    filepath = os.path.join(dir_path, filename) + '.' + ext
    if overwrite or not os.path.exists(filepath):
        return filepath

    for i in range(1, max_files + 1):
        filepath = os.path.join(
            dir_path, '{0}{1}.{2}'.format(filename, i, ext)
        )
        if not os.path.exists(filepath):
            return filepath

    msg = (
        'Maximum no. of %s files found in %s. Please clear '
        'out directory or allow overwrites.'
    ) % (filename, dir_path)
    raise Exception(msg)

def getAelVariables(name, exports, log_filename):
    ttDistributedCalculations = (
        'Use distributed calculations for improved performance.'
    )
    ttDate = 'Date to use as calculation valuation date.'
    ttSelectedInstrs = (
        'Credit Balance instruments for which to perform task.'
    )

    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['UseDistributedCalcs',
            'Use distributed calculations',
            'int', [0, 1], 0,
            1, 0, ttDistributedCalculations, None, 1],
        ['Date',
            'Valuation date',
            'string', DATES, None,
            1, 0, ttDate, None, None],
        ['Instruments',
            'Credit balance instruments',
            acm.FCreditBalance, None, INSTRUMENTS,
            1, 1, ttSelectedInstrs, None, 1],
    ]
    for export in exports:
        export.resetAelVariables(ael_variables=ael_variables)
        export.addTab()

    ael_variables.extend(_getOutputAelVariables())
    ael_variables.extend(AAIntegrationGuiCommon.getLoggingAelVariables(
        caller=sys.modules[name], log_filename=log_filename
    ))
    ael_variables = FRunScriptGUI.AelVariablesHandler(ael_variables, name)
    for export in exports:
        export.resetAelVariables(ael_variables=ael_variables)

    return ael_variables

def aelMain(name, exports, parameters):
    importlib.reload(AAXVAUtility)
    AAXVAUtility.reloadModules(ignore_gui=True)
    import AAXVAPerform

    exporters = _getExporters(
        exports=exports, ael_params=parameters
    )
    AAXVAPerform.perform(
        name=name, parameters=parameters, exporters=exporters
    )
    return

def _getOutputAelVariables():
    # tool tips
    ttOutputDir = (
        'Path to the directory where the reports should be '
        'created. Environment variables can be used for '
        'Windows (%VAR%) or Unix ($VAR).'
    )
    ttDateDir = (
        'Create a directory with the todays date as the directory name'
    )
    ttOverwrite = (
        'If a file with the same name and path already exists, overwrite it.'
    )

    directorySelection = AAIntegrationGuiCommon.getPathSelector(
        is_dir=True, is_input=False
    )
    ael_variables = [
        #[VariableName,
        #    DisplayName,
        #    Type, CandidateValues, Default,
        #    Mandatory, Multiple, Description, InputHook, Enabled]
        ['OutputDir',
            'Directory path_Output settings',
            directorySelection, None, directorySelection,
            1, 1, ttOutputDir, None, 1],
        ['DateDir',
            'Create directory with todays date_Output settings',
            'int', [0, 1], 1,
            1, 0, ttDateDir],
        ['Overwrite',
            'Overwrite if files exist_Output settings',
            'int', [0, 1], 1,
            1, 0, ttOverwrite],
    ]
    return ael_variables

def _getExporters(exports, ael_params):
    exporters = {}
    for export in exports:
        if export.shouldPerform(ael_params):
            e = export._EXPORTER
            exporter = exporters.get(e.__name__)
            if not exporter:
                exporter = exporters[e.__name__] = e()

            exporter._addCalculationType(export._PREFIX)

    return exporters.values()
