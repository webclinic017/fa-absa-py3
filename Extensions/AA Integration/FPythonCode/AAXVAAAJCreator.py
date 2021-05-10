""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVAAAJCreator.py"
import acm
import ael

import AAXVAGuiCommon
import AAXVAUtility

class Exporter(AAXVAGuiCommon.Exporter):
    NAME = 'FA_AAJs'
    OUTPUT_SUFFIX = 'XVA_Export'

    def performImplementation(self):
        # CVA_DoExport already checked by shouldPerform
        instrs = sorted(
            ins for ins in set(self._ael_params['Instruments']) if ins
        )
        if not instrs:
            indentation = self._indentation * self._indentation_level
            msg = 'No valid credit balance instruments selected.'
            self._logger.info(indentation + msg)
            return

        assert all((ins.IsKindOf(acm.FCreditBalance) for ins in instrs)), \
            'Not all instruments were of type \'FCreditBalance\''
        # validate params
        AAXVAUtility.validateCVAModule()
        AAXVAUtility.validateAAJDirectory(path=self._output_dir)

        # perform export
        return self._export(instrs=instrs)

    def _export(self, instrs):
        indentation = self._indentation * self._indentation_level
        msg = 'Performing the following exports: %s' % (
            ', '.join(sorted(self._calculation_types))
        )
        self._logger.info(indentation + msg)

        msg = 'Found %d distinct credit balance instruments' % len(instrs)
        self._logger.info(indentation + msg)
        msg = 'Performing export for the following instruments:\n  %s' % (
            '\n  '.join(ins.Name() for ins in instrs)
        )
        self._logger.debug(indentation + msg)
        try:
            aajs = self._createAAJs(
                instrs=instrs, indentation_level=self._indentation_level + 1
            )
            #self._writeAAJs(aajs=aajs)
            return bool(aajs)
        except Exception as e:
            self._logger.error(indentation + ('Failed: %s' % e))

        return False

    def _createAAJs(self, instrs, indentation_level):
        acm_date = AAXVAUtility.getACMDate(date=self._ael_params['Date'])
        iso_date = None if self._ael_params['DateDir'] else \
            self._ael_date.to_string(ael.DATE_ISO)
        aajs = None
        md_paths = self._getMarketData(
            instrs=instrs, acm_date=acm_date,
            indentation_level=indentation_level
        )
        aajs = bool(md_paths)
        # To be fixed in subsequent SPRs
        """
        aajs = AAXVAUtility.getAAJWriteDetails(
            aajs=aajs, iso_date=iso_date, suffix=self.OUTPUT_SUFFIX,
            prefixes=prefixes, getOutputFilepathCb=self._getOutputFilepath
        )
        """
        return aajs

    def _getMarketData(self, instrs, acm_date, indentation_level):
        indentation = self._indentation * indentation_level
        md_paths = {}
        for ct in self._calculation_types:
            key = ct + '_MarketDataFile'
            path = self._getPathParam(key=key, check_path=False)
            md_paths[ct] = AAXVAUtility.getMarketDataFilePath(
                path=path, calc_type=ct, date=acm_date
            )

        distributed = bool(self._ael_params['UseDistributedCalcs'])
        calc_query = AAXVAUtility.getCalculationQuery(instrs=instrs)
        info = AAXVAUtility.getMarketDataInfo(
            distributed=distributed, calc_types=self._calculation_types,
            calc_query=calc_query, output_dir=self._output_dir
        )
        mds = AAXVAUtility.createMarketData(
            distributed=distributed, calc_types=self._calculation_types,
            calc_query=calc_query, market_data_paths=md_paths,
            calc_infos=info, logger=self._logger,
            indentation=self._indentation,
            indentation_level=indentation_level + 1
        )
        self._output_filepaths.extend(mds)
        msg = 'Finished writing market data files.'
        self._logger.info(indentation + msg)
        return mds

    # To be fixed in subsequent SPRs
    """
    def _writeAAJs(self, aajs):
        if aajs:
            for column_name, filepath, aaj in aajs:
                msg = 'Writing %s to %s' % (column_name, filepath)
                self._logger.debug(self._base_indentation + '  ' + msg)
                with open(filepath, 'w') as fout:
                    fout.write(aaj)

                self._output_filepaths.append(filepath)
        else:
            msg = self._base_indentation + \
                '  Nothing to write for any instrument.'
            self._logger.debug(msg)

        return
    """

class ExportBase(AAXVAGuiCommon.Export):
    _EXPORTER = Exporter

    def _getAelVariables(self):
        def enabled(ael_var, field_values):
            if ael_var.isEnabled():
                return bool(int(field_values[ael_var.sequenceNumber]))

            return False

        def enableVar(name, enable, tt):
            getattr(self._ael_vars, name).enable(enable, tt)
            return

        def enableVars(callee_var_name, tt, enable, vars):
            for var in vars:
                name = var[0]
                if (name != callee_var_name) and name.startswith(self._PREFIX):
                    enableVar(name=name, enable=enable, tt=tt)

            return

        def cb(index, field_values):
            for var in self._ael_vars:
                name = var[0]
                if not name.startswith(self._PREFIX):
                    continue

                name = name.split('_')[1]
                if name == 'DoExport':
                    enable = enabled(ael_var=var, field_values=field_values)
                    tt = 'Select export to enable.'
                    enableVars(
                        callee_var_name=var[0], tt=tt, enable=enable, vars=self._ael_vars
                    )
                elif name == 'DeterministicScenarios':
                    enable = enabled(ael_var=var, field_values=field_values)
                    tt = 'Select use deterministic scenarios to enable.'
                    enableVar(
                        name=self._PREFIX + '_ScenariosFromFile', enable=enable, tt=tt
                    )
                elif name == 'ScenariosFromFile':
                    enable = enabled(ael_var=var, field_values=field_values)
                    tt = 'Select use archived scenario file to enable.'
                    enableVar(
                        name=self._PREFIX + '_ScenarioFile', enable=enable, tt=tt
                    )
                    dep_var = getattr(self._ael_vars, self._PREFIX + '_ScenarioFile')

            return field_values

        ttExportCredBal = (
            'Export Credit Balance instruments AAJ file (create AAJ file).'
        )
        ttPrefix = 'Optional prefix for output file names.'
        ttMarketdata = (
            'Select the base market data file. Leave blank to use default paths.'
        )
        ttDeterministicScenarios = (
            'Select to use deterministic scenarios. Enable will '
            'allow for either writing scenarios used in calculation to file, '
            'or reading in archived scenarios to use in calculation.'
        )
        ttScenariosFromFile = (
            'Select to specify an achived scenario file, otherwise a new '
            'file will be written to the output directory.'
        )
        ttArchivedScenarioFile = 'Select the archived scenario file.'
        market_data_file = self._getInputFileSelector()
        scenario_file = self._getInputFileSelector()

        ael_vars = [
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled]
            [self._PREFIX + '_DoExport',
                'Export Credit Balance instruments AAJ file_' + self._PREFIX,
                'int', [1, 0], 0,
                1, 0, ttExportCredBal, cb, 1],
            [self._PREFIX + '_Prefix',
                'Output file prefix_' + self._PREFIX,
                'string', None, self._PREFIX,
                0, 0, ttPrefix, None, 0],
            [self._PREFIX + '_MarketDataFile',
                'Base market data file_' + self._PREFIX,
                market_data_file, None, market_data_file,
                0, 1, ttMarketdata, None, 0],
            [self._PREFIX + '_DeterministicScenarios',
                'Use deterministic scenarios_' + self._PREFIX,
                'int', [1, 0], 0,
                1, 0, ttDeterministicScenarios, cb, 0],
            [self._PREFIX + '_ScenariosFromFile',
                'Use archived scenario file_' + self._PREFIX,
                'int', [1, 0], 0,
                1, 0, ttScenariosFromFile, cb, 0],
            [self._PREFIX + '_ScenarioFile',
                'Archived scenario file_' + self._PREFIX,
                scenario_file, None, scenario_file,
                0, 1, ttArchivedScenarioFile, None, 0],
        ]
        return ael_vars

def getExports():
    export_classes = AAXVAGuiCommon.createExports(base_cls=ExportBase)
    return tuple(cls() for cls in export_classes)
