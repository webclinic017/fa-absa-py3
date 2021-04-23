""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FManualExercise.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FManualExercise - Module to perform manual ExerciseAssign.

DESCRIPTION
    This module executes the Exercise/Assign procedure based on the
    parameters passed from FManualExerciseHook.

----------------------------------------------------------------------------"""
import sys
import traceback

import ael
import acm
import FBDPGui
import importlib

# FManualExerciseHook is running this module, so FManualExerciseHook has already been imported
# and its AEL variables have already been defined, therefore we can grab them.

pricingHook = sys.modules['FManualExerciseHook']
ael_variables = pricingHook.ael_variables

ael_gui_parameters = {'windowCaption': 'Exercise/Abandon', 'hideExtraControls': True}

def ael_main(dictionary):
    import FBDPString
    importlib.reload(FBDPString)
    
    ScriptName = "Manual Exercise Assign"
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'], 
                      dictionary['MailList'], 
                      dictionary['ReportMessageType'])    
    

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPInstrument
    importlib.reload(FBDPInstrument)
    import FExeAssPerform
    importlib.reload(FExeAssPerform)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    import FBDPCalculatePosition
    importlib.reload(FBDPCalculatePosition)
    

    dictionary['Positions'] = dictionary['trades'] = FBDPCommon.convertEntityList(dictionary['trades'], dictionary)

    if not 'actions_for_trades' in dictionary:
        dictionary['actions_for_trades'] = '{}'
    FBDPGui.setPortfolioGrouper(dictionary)
    FBDPCommon.execute_script(FExeAssPerform.perform_exercise_assign, dictionary)
