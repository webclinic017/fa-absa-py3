""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AACalculationLoader.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAACalculationLoader - Run Script GUI

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import sys
import FRunScriptGUI
import AAIntegrationGuiCommon
import AAIntegrationUtility
import FAACalculationLoaderGeneralTab
import FAACalculationLoaderLoggingTab
import FAACalcSensitivityBasedPLTab
import FAACalcSensitivityTab
import FAACalcFileImportTab
import FAACalcPLRatesTab

import AAFileImportCalculationClasses
import AASensitivitiesCalculationClasses
import AASensitivitiesPLCalculationClasses
import AAPLRatesCalculationClasses

import AACalculationPerform

ScriptName = "AACalculationLoader"
class AACalculationLoader(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, [])
        #add other tabs
        self.extend(FAACalculationLoaderGeneralTab.getAelVariables())
        self.extend(FAACalcFileImportTab.getAelVariables())
        self.extend(FAACalcPLRatesTab.getAelVariables())
        self.extend(FAACalcSensitivityTab.getAelVariables())
        self.extend(FAACalcSensitivityBasedPLTab.getAelVariables())
        self.extend(FAACalculationLoaderLoggingTab.getAelVariables())
        
ael_gui_parameters = {"windowCaption":__name__}
ael_variables = AACalculationLoader()
ael_variables.LoadDefaultValues(__name__)

funcdict = {
  'AAFileImportCalculationClasses': AAFileImportCalculationClasses.Manager,
  'AASensitivitiesCalculationClasses' : AASensitivitiesCalculationClasses.Manager,
  'AASensitivitiesPLCalculationClasses' : AASensitivitiesPLCalculationClasses.Manager,
  'AAPLRatesCalculationClasses': AAPLRatesCalculationClasses.Manager
}


def ael_main(ael_params):
    # Initialize the logger, should go _first_ of all initalizations
    logger = AAIntegrationUtility.getLogger(ScriptName, ael_params)
    logger.info('Initialised %s logger.' % logger.Name())
    logger.info('Starting %s.' % ScriptName)
    
    calcs= (('runCalcCVAImport', 'CSV Import', 'AAFileImportCalculationClasses'),
            ('runCalcSen', 'Sensitivities', 'AASensitivitiesCalculationClasses'),
            ('runCalcSenPL', 'SensitivitiesPL', 'AASensitivitiesPLCalculationClasses'),
            ('runCalcPLRates', 'PLRates', 'AAPLRatesCalculationClasses')
            )
 
    for runCalc, name, calcManager in calcs:
        if ael_params[runCalc]:
            ael_params['AnalysisType'] = name
            AACalculationPerform.execute_perform(
                name=__name__, ael_params=ael_params,
                calc_manger=funcdict[calcManager]())
    logger.info('Finished %s.' % ScriptName)
    return
