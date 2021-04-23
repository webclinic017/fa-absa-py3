
import acm
import FCalculatedValueXMLWriter
import FExportCalculatedValuesPublisher

import RiskFactorValueCalculator

import FReportAPI
import FReportUtils
import FRunScriptGUI
import FOutputSettingsTab
import FAdvancedSettingsTab

class RiskFactorValueXMLReport( FRunScriptGUI.AelVariablesHandler ):
    
    def __init__(self):

        ttRiskFactorSetup = ""

        vars = [
                #[VariableName,
                #    DisplayName,
                #    Type, CandidateValues, Default,
                #    Mandatory, Multiple, Description, InputHook, Enabled]

                ['Risk Factor Setups',
                    'Risk Factor Setups',
                    acm.FRiskFactorSetup, None, None,
                    1, 1, ttRiskFactorSetup]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        self.extend(FOutputSettingsTab.getAelVariables())
        advancedSettings = FAdvancedSettingsTab.getAelVariables()
        for var in advancedSettings:
            if var[0] in ['Include Raw Data', 'Include Full Data', 'Include Default Data', 'Include Formatted Data']:
                # Might need to add some entries to be able to set the 9:th.
                while len(var) < FRunScriptGUI.Controls.ENABLED + 1:
                    var.append(None)            
            
                # only data of one type is written
                if var[FRunScriptGUI.Controls.NAME] == 'Include Raw Data':
                    var[FRunScriptGUI.Controls.DEFAULT] = 'True'
                else:
                    var[FRunScriptGUI.Controls.DEFAULT] = 'False'
                
                # disable data type checkboxes
                var[FRunScriptGUI.Controls.ENABLED] = 0
        
        self.extend(advancedSettings)

ael_gui_parameters = {'windowCaption':'FRiskFactorValueXMLReport'}
ael_variables=RiskFactorValueXMLReport()

       
def perform_report( params ):

    riskFactorSetups = params['Risk Factor Setups']
    
    writer = FCalculatedValueXMLWriter.CalculatedValueXMLWriter("TEST_REPORT")
    
    
    publisher = FExportCalculatedValuesPublisher.Publisher(contentProvider = RiskFactorValueCalculator.RiskFactorValueCalculator(riskFactorSetups),
                              writers = [writer],
                              logger = None,
                              testMode = False)
    publisher.publish()


    xmltext = writer.XmlText()

    report = FReportAPI.FWorksheetReportApiParameters()
    report.snapshot = True
    FReportAPI.init_from_output_settings_tab(report, params)
    FReportAPI.init_from_advanced_settings_tab(report, params)
    report.CreateReportByXml(xmltext)
    

def ael_main( params ):
    params=FReportUtils.adjust_parameters(params)
    
    perform_report( params )
    
