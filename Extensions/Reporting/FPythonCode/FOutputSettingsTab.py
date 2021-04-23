"""-------------------------------------------------------------------------------------------------------
MODULE
    FOutputSettingsTab - General output settings

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FWorksheetReport GUI which contains settings
    which are changed frequently, e.g. name of the report.

-------------------------------------------------------------------------------------------------------"""
import acm
import FRunScriptGUI
import FReportSettings

trueFalse = ['False', 'True']

def getDateFormats():
    return ['%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S', '%y%m%d%H%M%S']

def getListFromExtensions(extensions):
    str = extensions.AsString().replace(']', '').replace('[', '').replace(' ', '')
    extensionsList = str.split(',')
    extensionsList.sort()
    return extensionsList

def getPrintTemplateNames():
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'print templates')
    return getListFromExtensions(extensions)

def getSecondaryTemplateNames(ext = ''):
    if ext != '':
        ext = ' ' + ext.replace('.', '')
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'secondary templates' + ext)
    return getListFromExtensions(extensions)

def getCSSNames():
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'style sheets')
    return getListFromExtensions(extensions)

class OutputSettingsTab(FRunScriptGUI.AelVariablesHandler):

    def appendDateToFileNameCB(self, index, fieldValues):
        self.File_date_beginning.enable( fieldValues[index] != '' )
        return fieldValues

    def createDirectoryWithDatesCB(self, index, fieldValues):
        self.Date_format.enable(trueFalse.index(fieldValues[index]))
        return fieldValues

    def htmlToFileCB(self, index, fieldValues):
        self.HTML_to_File.enable(fieldValues[index] != 'True')
        if fieldValues[index] == 'True':
            fieldValues[index - 1] = 'True'
        return fieldValues

    def secondaryOutputCB(self, index, fieldValues):
        for i in (1, 2, 3):
            if (self.ael_variables) and (len(self.ael_variables) >= index+i):
                self.ael_variables[index + i][FRunScriptGUI.Controls.ENABLED] = (fieldValues[index] == 'True')
        return fieldValues
        
    def addHeadImageCB(self, index, fieldValues):
        if (self.ael_variables) and (len(self.ael_variables) >= index+1):
            self.ael_variables[index + 1][FRunScriptGUI.Controls.ENABLED] = (fieldValues[index] == 'True')
        return fieldValues

    def setFileExtensionCB(self, index, fieldValues):
        """ Set file extension depending on which group the template belongs to """
        secTempl = fieldValues[index]

        for ext in FReportSettings.FILE_EXTENSIONS:
            list = getSecondaryTemplateNames(ext)
            if secTempl in list:
                fieldValues[index+1] = ext
        return fieldValues
    
    def __init__(self):
        directorySelection=FRunScriptGUI.DirectorySelection()
        file_selection = FRunScriptGUI.InputFileSelection()
        vars =[
                ['HTML to File', 'HTML to File_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the HTML wanted on file?', None, 1],
                ['HTML to Screen', 'HTML to Screen_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the HTML wanted on screen in a browser?', self.htmlToFileCB, 1],
                ['HTML to Printer', 'HTML to Printer_Output settings', 'string', trueFalse, 'False', 1, 0, 'Is printing of the HTML wanted?', None, 0],                
                ['File Path', 'File Path_Output settings', directorySelection, None, directorySelection, 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],
                ['File Name', 'File Name_Output settings', 'string', None, '', 0, 0, 'The file name of the output'],
                ['File date format', 'Format of Date Added to File Name_Output settings', 'string', getDateFormats(), '', 0, 0, 'Format of the date added to the file name. No date is added to the file name if this field is empty. As default, it is appended at the end of the file name. Toggle checkbox Date at Beginning of File Name to insert the date at the beginning of the file name.', self.appendDateToFileNameCB, 1],
                ['Year with century', 'Year with century_Output settings', 'string', trueFalse, 'False', 1, 0, 'When using dates for filename and directory, year will be with or without century'],
                ['File date beginning', 'Date at Beginning of File Name_Output settings', 'string', trueFalse, 'False', 1, 0, 'Append date at beginning of file name'],
                ['Create directory with date', 'Create Directory with Date_Output settings', 'string', trueFalse, 'True', 1, 0, 'Create a directory with the date included in the directory name', self.createDirectoryWithDatesCB, 1],
                ['Date format', 'Directory Date Format_Output settings', 'string', getDateFormats(), '%d%m%y', 0, 0, 'Date format', None, 1],
                ['Overwrite if file exists', 'Overwrite if File Exists_Output settings', 'string', trueFalse, 'True', 1, 0, 'If a file with the same name and path already exist, overwrite it?'],
                ['Print template (XSL)', 'HTML Template (XSL)_Output settings', 'string', getPrintTemplateNames(), 'FStandardTemplate', 0, 0, 'Choose which XSL template to use in the transformation from XML. Templates must be added to group aef reporting/print templates to be visible here.'],
                ['Print style sheet (CSS)', 'HTML Style Sheet (CSS)_Output settings', 'string', getCSSNames(), 'FStandardCSS', 0, 0, 'If wanted, choose a Cascading Style Sheet'],
                ['Include header image', 'Add Header Image to HTML_Output settings', 'string', trueFalse, 'False', 1, 0, 'If wanted, choose a header image to add to HTML output', self.addHeadImageCB, 1],
                ['Header image path', 'Header Image Path_Output settings', 'FFileSelection', None, None, 0, 1, 'The file path to the header image. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 0],
                ['Secondary output', 'Secondary Output_Output settings', 'string', trueFalse, 'False', 1, 0, 'Is a secondary output wanted?', self.secondaryOutputCB, 1],
                ['Secondary template', 'Secondary Template_Output settings', 'string', getSecondaryTemplateNames(), 'FTABTemplate', 0, 0, 'Choose a secondary output template. Templates must be added to group aef reporting/secondary templates [ext] to be visible here.', self.setFileExtensionCB, 0],
                ['Secondary file extension', 'Secondary File Extension_Output settings', 'string', FReportSettings.FILE_EXTENSIONS, '.xls', 0, 0, 'Which file extension should the secondary output have?', None, 0],
                ['Utf8 BOM', 'Enforce UTF-8 encoded output_Output settings', 'string', trueFalse, 'False', 0, 0, 'Add a Byte Order Mark to UTF-8 encoded output files. Some application, such as Excel, need the Byte Order Mark to be able to open the file correctly. Only applicable for templates with UTF-8 encoding.', None, 0],
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars, __name__)

def getAelVariables():
    outtab=OutputSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
