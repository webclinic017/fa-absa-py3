""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pace_runner/etc/FPaceTaskRunner.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import os
import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FTasksSelectItem
import FPaceAelTaskSchedule

# Name of this script used in START, STOP and FINISH messages:
ScriptName = 'PACE Task Runner'

ttTasks = "The tasks to be run" 
default_report_path = os.path.join(FBDPGui.defaultLogDir(),
        "Trade Aggregation")

def contexts():
    contextList = [""]
    for c in acm.Contexts(''):
        contextList.append(c)
    contextList.sort()
    return contextList


def get_default_context():
    contextList = contexts()
    if "Standard" in contextList:
        return "Standard"
    else:
        return contextList[0]

def customDialog(shell, params):
    customDlg = FTasksSelectItem.SelectTasksCustomDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


ael_variables = FBDPGui.LogVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Tasks',
                'Tasks_Task',
                'string', [], '',
                0, 1, ttTasks, None, 1, customDialog],
        )


def ael_main(dictionary):
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FAggregatePerform
    importlib.reload(FAggregatePerform)

    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    taskNames = dictionary['Tasks']
    for n in taskNames:
        s = FPaceAelTaskSchedule.FPaceAelTaskSchedule(n)
        s.CreateTask()
