"""-------------------------------------------------------------------------------------------------------
MODULE
    FPostProcessingTab - General post processing

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FWorksheetReport GUI which contains post processing settings

-------------------------------------------------------------------------------------------------------"""
import FRunScriptGUI

def getAelVariables():
    tab_name = '_Processing'
    tooltipPreProcess = 'Python function for processing of XML before transformation. Fill in module_name.function_name'
    tooltipFunction = 'Python function to call after the script has terminated. Fill in module_name.function_name'
    tooltipParam = 'Optional parameter to pass to the function.'

    vars=[['preProcessXml', 'Pre process XML' + tab_name, 'string', '', None, 0, 0, tooltipPreProcess, None, 1],
          ['function', 'Post process' + tab_name, 'string', '', None, 0, 0, tooltipFunction, None, 1],
          ['param', 'Parameter' + tab_name, 'string', '', None, 0, 0, tooltipParam, None, 1],
         ]
    ael_vars = FRunScriptGUI.AelVariablesHandler(vars, __name__)
    ael_vars.LoadDefaultValues(__name__)
    return ael_vars
