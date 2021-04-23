""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitCorporateActions/./etc/FMarkitCorporateActionsImport.py"
import os
import ael, acm
import FRunScriptGUI
reload (FRunScriptGUI)
import FBDPGui
import FBDPRollback
import FBDPCurrentContext
from FOperationsIO import GetDefaultPath
import FCorporateActionsPerformImport
reload(FCorporateActionsPerformImport)
import FBDPPerform

dirSelectionFile = FRunScriptGUI.DirectorySelection()
dirSelectionFile.SelectedDirectory(str(GetDefaultPath()))

defaultFileFilter="Text Files (*.txt)|*.txt|All Files (*.*)|*.*||"
file_selection = FRunScriptGUI.InputFileSelection(defaultFileFilter)
ttOverrideExisting = ("Override existing corporate actions")
ttCreateNew = ("Create new corporate actions")
ttMarkitCAStatuses = ("Only import the corporate actions with the selected MarkitCAStatuses")



ael_variables = FBDPGui.LogVariables(
				# [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['filedir',
                'File Path', dirSelectionFile, None,
                dirSelectionFile, 1, 1, '', None, None],
                ['filename',
                'File name', 'string', None,
                file_selection, 1, 1, '', None, None],
                ['MarkitCAStatuses',
                'Markit CA Statuses', 'string',
                ['Approved', 'Cancelled', 'In conflict', \
                'Incomplete', 'Pending approval', 'Pending cancelled', \
                'Conditionally approved', 'Pending conditionally approved', \
                'Deleted', 'Not Supported'],
                'Approved,Conditionally approved', 1, 1, ttMarkitCAStatuses, None, None],
                ['override_existing',
                'Override existing corporate actions',
                'int', [1, 0], 1,
                1, 0, ttOverrideExisting, 1],
                ['create_new',
                'Create new corporate actions',
                'int', [1, 0], 1,
                1, 0, ttCreateNew, 1])
def ael_main(dictionary):
    """
    Main function
    """
    import FBDPString
    reload(FBDPString)
    import FBDPCommon
    reload(FBDPCommon)
    FBDPCurrentContext.CreateLog('Markit Corporate Actions Import',
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    dictionary['ScriptName'] = 'Markit Corporate Actions Import'
    logme = FBDPString.logme
    if dictionary['override_existing'] or dictionary['create_new']:
        FBDPPerform.execute_perform(FCorporateActionsPerformImport.PerformCorporateActionsImport, dictionary)
    else:
        logme('Markit Corporate Actions Import: Please select an action')
