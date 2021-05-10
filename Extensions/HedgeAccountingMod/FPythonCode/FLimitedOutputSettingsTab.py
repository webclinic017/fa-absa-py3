"""------------------------------------------------------------------------------------------------
MODULE
    FOutputSettingsTab - General output settings

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FWorksheetReport GUI which contains settings
    which are changed frequently, e.g. name of the report.

---------------------------------------------------------------------------------------------------
"""

import FRunScriptGUI

trueFalse = ['False', 'True']


def getDateFormats():
    return ['%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S', '%y%m%d%H%M%S']


def getListFromExtensions(extensions):
    extensionListString = extensions.AsString().replace(']', '').replace('[', '').replace(' ', '')
    extensions_list = extensionListString.split(',')
    extensions_list.sort()
    return extensions_list


class LimitedOutputSettingsTab(FRunScriptGUI.AelVariablesHandler):
    def xmlToFileCB(self, index, field_values):
        self.FilePath.enable(trueFalse.index(field_values[index]))
        self.FileDateFormat.enable(trueFalse.index(field_values[index]))
        self.FileDateBeginning.enable(0)
        self.CreateDirectoryWithDate.enable(trueFalse.index(field_values[index]))
        self.DateFormat.enable(0)
        self.OverwriteIfFileExists.enable(trueFalse.index(field_values[index]))
        return field_values

    def appendDateToFileNameCB(self, index, field_values):
        self.FileDateBeginning.enable(field_values[index] != '')
        return field_values

    def createDirectoryWithDatesCB(self, index, field_values):
        self.DateFormat.enable(trueFalse.index(field_values[index]))
        return field_values

    def __init__(self):
        directorySelection = FRunScriptGUI.DirectorySelection()
        ael_vars = [
            ['XMLtoFile', 'XML to File_Output settings', 'string', trueFalse, 'True', 1, 0,
             'Save XML to file?', self.xmlToFileCB, 1],
            ['FilePath', 'File Path_Output settings', directorySelection, None, directorySelection,
             0, 1, 'The file path to the directory where the report should be put. Environment '
             'variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],
            ['FileDateFormat', 'Format of Date Added to File Name_Output settings', 'string',
             getDateFormats(), '', 0, 0, 'Format of the date added to the file name. No date is '
             'added to the file name if this field is empty. As default, it is appended at the '
             'end of the file name. Toggle checkbox Date at Beginning of File Name to insert the '
             'date at the beginning of the file name.', self.appendDateToFileNameCB, 1],
            ['FileDateBeginning', 'Date at Beginning of File Name_Output settings', 'string',
             trueFalse, 'False', 1, 0, 'Append date at beginning of file name'],
            ['CreateDirectoryWithDate', 'Create Directory with Date_Output settings', 'string',
             trueFalse, 'True', 1, 0, 'Create a directory with the date included in the directory '
             'name', self.createDirectoryWithDatesCB, 1],
            ['DateFormat', 'Directory Date Format_Output settings', 'string', getDateFormats(),
             '%d%m%y', 0, 0, 'Date format', None, 1],
            ['OverwriteIfFileExists', 'Overwrite if File Exists_Output settings', 'string',
             trueFalse, 'True', 1, 0, 'If a file with the same name and path already exist, '
             'overwrite it?']
        ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, ael_vars, __name__)


def getAelVariables():
    outtab = LimitedOutputSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
