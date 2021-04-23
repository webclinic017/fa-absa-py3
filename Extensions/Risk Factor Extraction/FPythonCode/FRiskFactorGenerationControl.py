
import os
import itertools

import acm

import FRiskFactorScenarioFileGeneration
import FRiskFactorFileProcessing
import FRiskFactorVolCorrGeneration
import FRiskFactorFileProcessing
import FRiskFactorExtractionUtils

from FRiskFactorExtractionUtils import get_output_filename_simple
from FRiskFactorExtractionUtils import RiskFactorDynamicsEnum
from FRiskFactorScenarioFileGeneration import DATE_ORDER_LAST_TO_FIRST

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

class GeneratorParameters(object):
    def __init__(self, ael_variables, raw_data):
        self.raw_data = raw_data
    
        self.spec_header = ael_variables["header"]
        self.delimiter = self.spec_header.DelimiterChar()
        self.comment_char = self.spec_header.CommentChar()
        self.cross_delimiter = self.spec_header.CorrelationIdDelimChar()
        self.corr_delimiter = self.spec_header.DelimiterChar()
        self.vol_delimiter = self.spec_header.DelimiterChar()
        
        labels_token = FRiskFactorFileProcessing.labels_token(
            self.comment_char)
        self.ext_ids = list(itertools.filterfalse(
            (lambda it: it == labels_token),
                raw_data.keys()))
        
        self.generate_scenarios = \
            ael_variables['generate_scenarios'] == "True"

        self.scenario_calendar = ael_variables['scenario_calendar']
        if not self.scenario_calendar and self.generate_scenarios:
            fx_base_curr = acm.UsedValuationParameters().FxBaseCurrency()
            if not fx_base_curr:
                fx_base_curr = \
                    acm.UsedValuationParameters().AccountingCurrency()
            self.scenario_calendar = fx_base_curr.Calendar()
        if ael_variables["scenario_end_day"] and self.scenario_calendar:
            self.scenario_end_day = \
                FRiskFactorExtractionUtils.adjust_date(
                    ael_variables["scenario_end_day"],
                    acm.Time().DateToday(), self.scenario_calendar, "Preceding")
        else:
            self.scenario_end_day = None

        self.horizon = ael_variables['scenario_horizon']
        
        self.nbr_of_scenarios = ael_variables['nbr_of_scenarios']
        self.overlapping_scenarios = \
            ael_variables['overlapping_scenarios'] == "True"
            
        self.overwrite_scenario_file = \
            ael_variables['overwrite_scenario_file'] == "True"
            
        if ael_variables['scenario_file_path'] and \
            ael_variables['scenario_file_name']:
            self.scenario_file_path = get_output_filename_simple(
                ael_variables['scenario_file_path'],
                ael_variables['scenario_file_name'],
                self.overwrite_scenario_file, "")
        else:
            self.scenario_file_path = None
        
        self.generate_volcorr_file = \
            ael_variables['generate_volcorr_file'] == "True"
        self.estimation_method = ael_variables['estimation_method']
        self.dec_factor = ael_variables['decay_factor']
        
        self.overwrite_volcorr_files = \
            ael_variables['overwrite_volcorr_files'] == "True"
        
        if ael_variables['volcorr_file_path'] and \
            ael_variables['vol_file_name']:
            self.vol_file_path = get_output_filename_simple(
                ael_variables['volcorr_file_path'],
                ael_variables['vol_file_name'],
                self.overwrite_volcorr_files, "")
        else:
            self.vol_file_path = None

        if ael_variables['volcorr_file_path'] and \
            ael_variables['corr_file_name']:
            self.corr_file_path = get_output_filename_simple(
                ael_variables['volcorr_file_path'],
                ael_variables['corr_file_name'],
                self.overwrite_volcorr_files, "")
        else:
            self.corr_file_path = None
            
        self.ext_id_infos = self.get_ext_id_infos()
            
    def validate_and_open_file(self, path, overwrite):
        if not overwrite and os.path.isfile(path):
            raise IOError("File already exists at '%s'" % path)
        logger.LOG("Opening file at '%s'" % path)
        return open(path, "w")
            
    def get_scenario_file(self):
        if not self.scenario_file_path:
            return None
        return self.validate_and_open_file(self.scenario_file_path,
            self.overwrite_scenario_file)
        
    def get_volatility_file(self):
        if not self.vol_file_path:
            return None
        return self.validate_and_open_file(self.vol_file_path,
            self.overwrite_volcorr_files)

    def get_correlation_file(self):
        if not self.corr_file_path:
            return None
        return self.validate_and_open_file(self.corr_file_path,
            self.overwrite_volcorr_files)
        
    def decay_factor(self):
        if self.estimation_method == "SMA":
            return None
        else:
            return self.dec_factor
            
    def get_ext_id_infos(self):
        rf_dyn = FRiskFactorExtractionUtils.risk_factor_dynamics_from_ext_id
        ext_id_infos = \
            [(ext_id, rf_dyn(ext_id, self.spec_header)) \
             for ext_id in self.ext_ids]
        return ext_id_infos
    
def do_generation(ael_variables, result):
    if not ael_variables['generate_scenarios'] == "True":
        return
    generator_parameters = GeneratorParameters(ael_variables, result)
    
    scenario_ostream = None
    vol_ostream = None
    corr_ostream = None
    
    if generator_parameters.generate_scenarios or \
        generator_parameters.generate_volcorr_file:
        try:
            scenario_ostream = generator_parameters.get_scenario_file()
            rel_returns = FRiskFactorScenarioFileGeneration.hist_scenario(
                generator_parameters.raw_data,
                generator_parameters.ext_id_infos,
                generator_parameters.spec_header,
                generator_parameters.scenario_calendar,
                generator_parameters.horizon,
                generator_parameters.scenario_end_day,
                generator_parameters.nbr_of_scenarios,
                generator_parameters.overlapping_scenarios,
                generator_parameters.delimiter,
                generator_parameters.comment_char,
                DATE_ORDER_LAST_TO_FIRST,
                scenario_ostream)
        except Exception as msg:
            logger.ELOG("Failed to generate historical scenario: %s" % msg)
            raise
        finally:
            if scenario_ostream:
                scenario_ostream.close()
        
    if generator_parameters.generate_volcorr_file:
        try:
            vol_ostream = generator_parameters.get_volatility_file()
            corr_ostream = generator_parameters.get_correlation_file()
            FRiskFactorVolCorrGeneration.write_vol_corr_file(rel_returns,
                generator_parameters.ext_id_infos,
                generator_parameters.decay_factor(),
                vol_ostream,
                corr_ostream,
                generator_parameters.vol_delimiter,
                generator_parameters.cross_delimiter,
                generator_parameters.corr_delimiter)
        except Exception as msg:
            logger.ELOG("Failed to generate vol/corr files: %s" % msg)
            raise
        finally:
            if vol_ostream:
                vol_ostream.close()
            if corr_ostream:
                corr_ostream.close()
