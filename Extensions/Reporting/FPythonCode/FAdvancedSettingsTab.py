"""-------------------------------------------------------------------------------------------------------
MODULE
    FAdvancedSettingsTab - Avanced settings, not changed frequently

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FWorksheetReport GUI which contains settings which are
    not changed frequently or not used by most users.

-------------------------------------------------------------------------------------------------------"""

import FRunScriptGUI

trueFalse = ['False', 'True']

perf_strategy_gc = "Periodic full GC to save memory"
perf_strategy_speed = "No extra GC"
performance_strategies = [perf_strategy_gc, perf_strategy_speed]
performance_strategy_default = perf_strategy_gc

class AdvancedSettingsTab(FRunScriptGUI.AelVariablesHandler):
    def xmlToAmbCB(self, index, fieldValues):
        for i in (1, 2, 3, 4):
            if (self.ael_variables) and (len(self.ael_variables) >= index+i):
                self.ael_variables[index + i][FRunScriptGUI.Controls.ENABLED] = (fieldValues[index] == 'True')
        return fieldValues
        
    def __init__(self):
        """ Get ael_variables that need to be suplied to produceOutput, scripts outputing
        reports should extend their ael_variables with this list
        """
        tab_name = '_Advanced settings'
        vars =[
                ['Include Raw Data', 'Include Raw Data' + tab_name, 'string', trueFalse, 'True', 1, 0, 'Is the raw data needed in the report?'],
                ['Include Full Data', 'Include Full Data' + tab_name, 'string', trueFalse, 'False', 1, 0, 'Is the full data needed in the report?'],
                ['Include Formatted Data', 'Include Formatted Data' + tab_name, 'string', trueFalse, 'True', 1, 0, 'Is the formatted data needed in the report? Must be checked when using FStandardTemplate.'],
                ['Include Default Data', 'Include Default Data' + tab_name, 'string', trueFalse, 'False', 1, 0, 'Is the default data needed in the report? Must be checked when using FStandardTemplate.'],
                ['Include Color Information', 'Include Color Information' + tab_name, 'string', trueFalse, 'True', 1, 0, 'Include the color information for each cell in the report.'],
                ['Wait for Remote Work', 'Wait for Remote Work' + tab_name, 'string', trueFalse, 'False', 1, 0, 'Wait with generating output until all remote work (including market transactions) results have been received. Memory consumption will increase.'],
                ['XML to File', 'XML to File' + tab_name, 'string', trueFalse, 'False', 1, 0, 'Is the XML wanted on file?'],
                ['Compress Output', 'Compress XML output (.zip)' + tab_name, 'string', trueFalse, 'False', 1, 0, 'Compress the .xml output with zip', None, 1],
                ['Send XML File to AMB', 'Send XML File to AMB' + tab_name, 'string', trueFalse, 'False', 1, 0, 'Send XML File to ARENA Message Broker?', self.xmlToAmbCB, 1],
                ['AMB XML Message', 'AMB XML Message' + tab_name, 'string', trueFalse, 'True', 0, 0, 'XML Message or Front Arena internal format?', None, 1],
                ['AMB Address', 'AMB Address' + tab_name, 'string', '', '', 0, 0, 'Address to ARENA Message Broker on format host:port', None, 0],
                ['AMB Sender Name', 'AMB Sender Name' + tab_name, 'string', '', '', 0, 0, 'Name on Sender to ARENA Message Broker (Must exist in AMB system table!)', None, 0],
                ['AMB Subject', 'AMB Subject' + tab_name, 'string', '', '', 0, 0, 'Subject on Messages Sent to ARENA Message Broker', None, 0],
                ['Performance Strategy', 'Performance Strategy' + tab_name, 'string', performance_strategies, performance_strategy_default, 0, 0, 'Strategy for optimizing between memory and performance', None, 1]
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars, __name__)

def getAelVariables():
    advtab=AdvancedSettingsTab()
    advtab.LoadDefaultValues(__name__)
    return advtab
