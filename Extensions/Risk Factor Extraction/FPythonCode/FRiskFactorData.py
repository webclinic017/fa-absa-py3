"""-------------------------------------------------------------------------------------------------------
MODULE
    FRiskFactorExtractor -

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import itertools

import acm
import ael

import FRunScriptGUI

import FRiskFactorScenarioFileGeneration
reload(FRiskFactorScenarioFileGeneration)
import FRiskFactorExtraction
reload (FRiskFactorExtraction)
import FRiskFactorExtractionUtils
reload(FRiskFactorExtractionUtils)
import FRiskFactorGenerationControl
reload(FRiskFactorGenerationControl)

from FRiskFactorVolCorrGeneration import estimation_methods

trueFalse = ['False', 'True']

def getDateFormats():
    return ['%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S', '%y%m%d%H%M%S']

import FLogger
logger = FLogger.FLogger.GetLogger('FARiskFactorExtraction')

class RiskFactorExtractor(FRunScriptGUI.AelVariablesHandler):
       
    def generateScenariosCB(self, index, fieldValues):
        enable = trueFalse.index(fieldValues[index])
        
        """
        if self.generate_volcorr_file == "True" and not enable:
            fieldValues = self.generate_volcorr_file.set(fieldValues, "False")
            if self.generate_volcorr_file.hasCallback:
                fieldValues = self.generate_volcorr_file.callback(fieldValues)
        """
        
        self.scenario_end_day.enable(enable)
        self.scenario_horizon.enable(enable)
        self.scenario_horizon.enable(enable)
        self.scenario_calendar.enable(enable)
        self.nbr_of_scenarios.enable(enable)
        self.overlapping_scenarios.enable(enable)
        self.overwrite_scenario_file.enable(enable)
        self.scenario_file_path.enable(enable)
        self.scenario_file_name.enable(enable)
        return fieldValues
    
    def generateVolCorrCB(self, index, fieldValues):
        enable = trueFalse.index(fieldValues[index])
        
        if self.generate_scenarios != "True" and enable:
            fieldValues = self.generate_scenarios.set(fieldValues, "True")
            if self.generate_scenarios.hasCallback:
                fieldValues = self.generate_scenarios.callback(fieldValues)
        
        self.estimation_method.enable(enable)
        self.decay_factor.enable(enable)
        self.volcorr_file_path.enable(enable)
        self.vol_file_name.enable(enable)
        self.corr_file_name.enable(enable)
        self.overwrite_volcorr_files.enable(enable)
        return fieldValues
 
    def __init__(self):
        headers = acm.FRiskFactorSpecHeader.Select("")
        headers.Sort()
        calendars = acm.FCalendar.Select("")
        file_selection = FRunScriptGUI.InputFileSelection()
        directory_selection = FRunScriptGUI.DirectorySelection()

        vars = [
                 # RISK FACTOR DEPOSITORY
                 ['header', 'Risk Factor Specification_Risk Factor Data', 'FRiskFactorSpecHeader', headers, "", 1, 0, 'Choose a Risk Factor Specification Header', 0, 1],
                 ['File Path', 'File Path_Risk Factor Data', directory_selection, None, directory_selection, 1, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],
                 ['File Name', 'File Name_Risk Factor Data', file_selection, None, file_selection, 1, 1, 'The file name of the output'],
                 ['calendar', 'Calendar_Risk Factor Data', 'FCalendar', calendars, "", 1, 0, 'The calendar used to specify banking days. If none is selected the calendar for the FX Base Currency is used.'],
                 
                 # RISK FACTOR ADD VALUES TAB
                 ['add_values', 'Generate New Data_Risk Factor Extraction', 'string', trueFalse, 'False', 1, 0, 'Generate new risk factor data?', None, 1],

                 # SCENARIO TAB
                 ['generate_scenarios', 'Generate Scenarios_Scenario generator', 'string', trueFalse, 'False', 1, 0, 'TODO', self.generateScenariosCB, 1],
                 ['scenario_end_day', 'Scenario End Day_Scenario generator', 'string', None, "TODAY", 1, 0, 'Last day of scenario generation', None, 1],
                 ['scenario_horizon', 'Scenario Horizon_Scenario generator', 'int', None, 1, 1, 0, 'Scenario horizon in days', None, 1],
                 ['scenario_calendar', 'Calendar_Scenario generator', 'FCalendar', calendars, calendars.First(), 1, 0, 'The calendar used to specify banking days. If none is selected the calendar for the FX Base Currency is used.'],
                 ['nbr_of_scenarios', 'Number of Scenarios_Scenario generator', 'int', None, 0, 1, 0, 'Number of scenarios', None, 1],
                 ['overlapping_scenarios', 'Use Overlapping Scenarios_Scenario generator', 'string', trueFalse, 'False', 1, 0, 'Use daily or sequentially laid out scenarios', None, 1],
                 ['scenario_file_path', 'File Path_Scenario generator', directory_selection, None, directory_selection, 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],
                 ['scenario_file_name', 'File Name_Scenario generator', 'string', None, '', 0, 0, 'The file name of the scenario shift file output'],
                 ['overwrite_scenario_file', 'Overwrite if file exists_Scenario generator', 'string', trueFalse, 'False', 1, 0, 'If an input file is specified, overwrite it?', None, 0],

                 # VOLCORR TAB
                 ['generate_volcorr_file', 'Generate Volatility/Correlation_Vol/Corr generator', 'string', trueFalse, 'False', 1, 0, 'TODO', self.generateVolCorrCB, 1],
                 ['estimation_method', 'Estimation method_Vol/Corr generator', 'string', estimation_methods, 'EWMA', 1, 0, 'TODO', None, 1],
                 ['decay_factor', 'Decay factor_Vol/Corr generator', 'float', None, 0.94, 1, 0, 'Decay factor', None, 1],
                 ['volcorr_file_path', 'File Path_Vol/Corr generator', directory_selection, None, directory_selection, 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],
                 ['vol_file_name', 'Volatility File Name_Vol/Corr generator', 'string', None, '', 0, 0, 'The file name of the volatility shift file output'],
                 ['corr_file_name', 'Correlation File Name_Vol/Corr generator', 'string', None, '', 0, 0, 'The file name of the correlation shift file output'],
                 ['overwrite_volcorr_files', 'Overwrite if files exist_Vol/Corr generator', 'string', trueFalse, 'False', 1, 0, 'If output files are specified, overwrite them if present?', None, 0],
                 
               ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        
ael_gui_parameters = {'windowCaption':__name__}

ael_variables = RiskFactorExtractor()
ael_variables.LoadDefaultValues(__name__)
    
def ael_main(variableDictionary):
    result = FRiskFactorExtraction.get_risk_factor_data(variableDictionary)
    FRiskFactorGenerationControl.\
        do_generation(variableDictionary, result)
