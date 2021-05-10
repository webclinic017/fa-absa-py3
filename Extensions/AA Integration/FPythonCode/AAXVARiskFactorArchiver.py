""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVARiskFactorArchiver.py"
import acm

import AAXVAGuiCommon
import AAXVAUtility

class Exporter(AAXVAGuiCommon.Exporter):
    NAME = 'FA_RiskFactorArchive'
    OUTPUT_SUFFIX = 'XVA_RiskFactorExport'

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
            info = self._createMarketDataAndGetInfo(
                instrs=instrs, indentation_level=self._indentation_level
            )
            rfas = self._createRiskFactorArchives(
                info=info, indentation_level=self._indentation_level
            )
            return len(rfas) == len(self._calculation_types)
        except Exception as e:
            self._logger.error(indentation + ('Failed: %s' % e))

        return False

    def _createMarketDataAndGetInfo(self, instrs, indentation_level):
        indentation = self._indentation * indentation_level
        msg = 'Writing market data files.'
        self._logger.info(indentation + msg)
        md_paths = {}
        for ct in self._calculation_types:
            key = ct + '_MarketDataFile'
            path = self._getPathParam(key=key, check_path=False)
            acm_date = AAXVAUtility.getACMDate(date=self._ael_date)
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
        return info

    def _createRiskFactorArchives(self, info, indentation_level):
        indentation = self._indentation * indentation_level
        msg = 'Generating risk factor archives.'
        self._logger.info(indentation + msg)
        rfas = AAXVAUtility.createRiskFactorArchives(
            info=info, exe_dir=self._params_helper.getAdaptivPath(),
            logger=self._logger,
            indentation=self._indentation,
            indentation_level=indentation_level + 1
        )
        self._output_filepaths.extend(sorted(rfas))
        msg = 'Finished writing risk factor archives.'
        self._logger.info(indentation + msg)
        return rfas

class ExportBase(AAXVAGuiCommon.Export):
    _EXPORTER = Exporter

    def _getAelVariables(self):
        def callback(name, ael_var, field_values):
            if name == 'DoExport':
                enable = self.cbEnabled(
                    ael_var=ael_var, field_values=field_values
                )
                tt = 'Select export to enable.'
                self.cbEnableVars(
                    callee_var_name=ael_var[0], tt=tt,
                    enable=enable, vars=self._ael_vars
                )

            return field_values

        cb = self.getDoExportCb(callback=callback)
        ttExportCredBal = 'Export market data.'
        ttPrefix = 'Optional prefix for output file names.'
        ttMarketdata = (
            'Select the base market data file. Leave blank to use default paths.'
        )
        market_data_file = self._getInputFileSelector()

        ael_vars = [
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled]
            [self._PREFIX + '_DoExport',
                'Export market data_' + self._PREFIX,
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
        ]
        return ael_vars

def getExports():
    export_classes = AAXVAGuiCommon.createExports(
        base_cls=ExportBase, suffix='Archive'
    )
    return tuple(cls() for cls in export_classes)
