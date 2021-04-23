""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FRiskCubeDataUpload.py"
"""----------------------------------------------------------------------------
MODULE
    FRiskCubeDataUpload - Run script GUI for uploading data to the Risk Cube

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
----------------------------------------------------------------------------"""


import os


import acm


import FRunScriptGUI
import FLogger
import FRiskCubeDataUploadMain
import FScenarioExportUtils
import FScenarioExportLogSettingsTab


logger = FLogger.FLogger.GetLogger("FRiskCubeDataUpload")


falseTrue = ['False', 'True']
supportedActions = FRiskCubeDataUploadMain.ACTIONS


class RCUpload(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        calendars = acm.FCalendar.Select("")
        accounting_curr = acm.GetFunction("mappedValuationParameters", 0)(
                ).Parameter().AccountingCurrency()
        directorySelection = FRunScriptGUI.DirectorySelection()
        ttReferenceDate = 'The reference date for the report.'
        ttCalendar = 'Calendar used for adjusting relative \'Reference Date\''
        ttMonitor = ('Monitor the progress and status of the upload sessions.')
        ttFilePath = ('The file path to the directory where the risk export '
                'files resides. Environment variables can be specified for '
                'Windows (%VAR%) or Unix ($VAR).')
        ttDateDirectory = ('Use subdirectory with name equal to the given '
                'reference date.')
        ttFileName = ('The name of a specific risk export file to process. '
                'Leave empty to import all files on the specified path.')
        ttFileNamePrefix = ('Only consider files starting with the specified '
                'string')
        ttURL = 'URL to Adaptiv Risk Cube Results Import Service'
        ttPort = 'Port Number to Adaptiv Risk Cube Results Import Service'
        ttCleanUp = ('Run maintenance tasks to summarize, merge and purge '
                'old temporary files to preserve performance.')
        ttCleanUpDate = ('The date with respect to which the '
                'summarization schedule will be applied (i.e., if a data '
                'flow element has AgeToSummarise set to two weeks then '
                'that 2 weeks will be calculated from the refDate value '
                'and anything prior to that point which is currently in '
                'the previous element in the data flow will be summarized).')
        ttIncludeDays = ('This allows restriction of application of the '
                'schedule to the specified number of days with respect to the '
                'ref date. As an example if you had AgeToSummarise specified '
                'as 2 weeks and specified daysToInclude as 10 days then '
                'nothing would get summarized since 10 days is less than 2 '
                'weeks. 0 means include all days.')
        ttDeleteBinaries = ('Delete the unused binary files from which '
                'the data was summarized.')

        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ["Reference Date",
                        "Reference Date",
                        "string", None, acm.Time().DateToday(),
                        1, 0, ttReferenceDate],
                ["Calendar",
                        "Calendar",
                        "FCalendar", calendars, accounting_curr.Calendar(),
                        1, 0, ttCalendar],
                ["Process",
                        "Process",
                        "string", supportedActions, supportedActions[0],
                        1, 0],
                ["Monitor",
                        "Monitor Upload Session Progress",
                        "int", [0, 1], 0,
                        0, 0, ttMonitor],
                # File Input settings tab
                ["File Path",
                        "File Path_file settings",
                        directorySelection, None, directorySelection,
                        0, 1, ttFilePath],
                ["Date Directory",
                        "Use Reference Date subdirectory_file settings",
                        "string", falseTrue, "False",
                        0, 0, ttDateDirectory],
                ["File Name",
                        "File Name_file settings",
                        "string", None, "",
                        0, 0, ttFileName],
                ["File Name Prefix",
                        "File Name Prefix_file settings",
                        "string", None, "",
                        0, 0, ttFileNamePrefix],
                # Results Import Service settings tab
                ["URL",
                        "URL_risk cube settings",
                        "string", None, None,
                        1, 0, ttURL],
                ["Port",
                        "Port_risk cube settings",
                        "int", None, "8080",
                        1, 0, ttPort],
                # Maintenance tasks
                ["cleanUp",
                        "Run Maintenance Tasks_Maintenance",
                        "int", [0, 1], 0,
                        False, 0, ttCleanUp, self._enable, True],
                ["cleanUpDate",
                        "Reference Date_Maintenance",
                        "string", None, acm.Time().DateToday(),
                        True, 0, ttCleanUpDate, None, False],
                ["includeDays",
                        "Days to Include_Maintenance",
                        "int", None, "10",
                        True, 0, ttIncludeDays, None, False],
                ["deleteBinaries",
                        "Delete Binary Files_Maintenance",
                        "int", [0, 1], 1,
                        True, 0, ttDeleteBinaries, None, False],
        ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)
        self.extend(FScenarioExportLogSettingsTab.getAelVariables())

    def _enable(self, index, fieldValues):
        enable = fieldValues[index] == '1'
        for i in range(index+1, index+4):
            self[i].enable(enable)
        return fieldValues


ael_gui_parameters = {"windowCaption": __name__}
ael_variables = RCUpload()
ael_variables.LoadDefaultValues(__name__)


def validate_process(process):

    if not process in supportedActions:
        msg = "Process: '%s' is not supported" % process
        logger.ELOG(msg)
        raise Exception(msg)


def file_paths_in_dir(dir_path, file_name=None, prefix=None):
    """
    Returns a list of paths to all files in dir_path directory
    filtered with prefix.
    Does not follow subdirectories.
    """
    out = []
    if not os.path.isdir(dir_path):
        err_msg = "{0} is not a valid directory path".format(dir_path)
        logger.ELOG(err_msg)
        raise ValueError(err_msg)
    if file_name:
        path = os.path.join(dir_path, file_name)
        if os.path.isfile(path):
            out.append(path)
        else:
            raise ValueError("{0} is not a valid file path".format(path))
    else:
        for it in os.listdir(dir_path):
            path = os.path.join(dir_path, it)
            if os.path.isfile(path):
                if not prefix or os.path.basename(path).startswith(prefix):
                    out.append(path)
    return out


def ael_main(variableDictionary):

    # Initialize the logger, should go _first_ of all initalizations
    FScenarioExportLogSettingsTab.logger_setup(variableDictionary,
            "FRiskCubeDataUpload")

    date = variableDictionary["Reference Date"]
    calendar = variableDictionary["Calendar"]
    reference_date = FScenarioExportUtils.adjust_ref_date(date, calendar)
    process_action = variableDictionary["Process"]
    validate_process(process_action)

    target_files = None
    if not variableDictionary.get('cleanUp', False):
        if process_action in supportedActions[:2]:
            if (not variableDictionary["File Path"] or
                    not variableDictionary["File Path"].AsString()):
                msg = "No File Path"
                logger.ELOG(msg)
                raise ValueError(msg)
            else:
                fpath = variableDictionary["File Path"].AsString()
            fpath = FScenarioExportUtils.get_directory(fpath, reference_date,
                    falseTrue.index(variableDictionary["Date Directory"]))
            file_name = variableDictionary["File Name"]
            prefix = variableDictionary["File Name Prefix"]
            target_files = file_paths_in_dir(fpath, file_name, prefix)
            if not len(target_files):
                msg = ("No files found. File Path: '%s', File Name: '%s', Prefix: "
                        "'%s'" % (fpath, file_name, prefix))
                logger.LOG(msg)
                return

    base_url = variableDictionary["URL"]
    port = variableDictionary["Port"]

    FRiskCubeDataUploadMain.main(process_action, reference_date,
            base_url, port, target_files, **variableDictionary)

