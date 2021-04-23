""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FPositionTasksGenerator.py"
import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FTasksSelectItem
import FPositionInstancesGenerator 


# Name of this script used in START, STOP and FINISH messages:
ScriptName = 'Position Tasks Generator'

ttTasks = "The master task to be run"
ttPositionSpecification = "position specification"

def customDialog(shell, params):
    params['supportedModules'] = ['FMarketRiskExport']
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
                1, 1, ttTasks, None, 1, customDialog],
        ['PositionSpecification',
                'Position Specification_Task',
                'FPositionSpecification', None, None,
                1, 0, ttPositionSpecification, None, 1],
        )


def ael_main(dictionary):
    
    import FBDPCommon
    import FBDPCurrentContext
    import FBDPPerform
    
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPPerform.execute_perform(FPositionInstancesGenerator.perform, dictionary)
