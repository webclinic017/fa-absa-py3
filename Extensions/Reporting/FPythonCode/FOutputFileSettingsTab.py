"""-------------------------------------------------------------------------------------------------------
MODULE
    FOutputFileSettingsTab - General file output settings

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FRunScript GUI which contains settings
    that sets up output to a file.

-------------------------------------------------------------------------------------------------------"""
import acm

import FFileUtils
import FRunScriptGUI

trueFalse = ['False', 'True']

def getDateFormats():
    return ['' '%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S', '%y%m%d%H%M%S']

def getListFromExtensions(extensions):
    str = extensions.AsString().replace(']', '').replace('[', '').replace(' ', '')
    extensionsList = str.split(',')
    extensionsList.sort()
    return extensionsList

class OutputFileSettingsTab(FRunScriptGUI.AelVariablesHandler):

    def appendDateToFileNameCB(self, index, fieldValues):
        self.fileDateBeginning.enable(fieldValues[index] != '')
        return fieldValues

    def createDirectoryCB(self, index, fieldValues):
        self.fileDirName.enable(trueFalse.index(fieldValues[index]))
        self.fileDirDateFormat.enable(trueFalse.index(fieldValues[index]))
        return fieldValues
        
    def overwriteCB(self, index, fieldValues):
        self.fileMaxNrOfFilesInDir.enable(not trueFalse.index(fieldValues[index]))
        return fieldValues
        
    def enableFileOutputCB (self, index, fieldValues):
        enabled = fieldValues[index] == 'True'
        self.filePath.enable(enabled)
        self.fileName.enable(enabled)
        self.fileDateFormat.enable(enabled)
        self.fileCreateDirectory.enable(enabled)
        self.fileOverwriteIfFileExists.enable(enabled)
        
        if enabled:
            # enable dependent controls according to "parent" control status or content
            offset = index - self.fileOutput.sequenceNumber
            self.appendDateToFileNameCB(self.fileDateFormat.sequenceNumber + offset, fieldValues)
            self.createDirectoryCB(self.fileCreateDirectory.sequenceNumber + offset, fieldValues)
            self.overwriteCB(self.fileOverwriteIfFileExists.sequenceNumber + offset, fieldValues)
        else:
            # disable all dependent controls as well
            self.fileDateBeginning.enable(False)
            self.fileDirName.enable(False)
            self.fileDirDateFormat.enable(False)
            self.fileMaxNrOfFilesInDir.enable(False)
        
        return fieldValues
        

    def __init__(self):
        directorySelection=FRunScriptGUI.DirectorySelection()
        vars =[
                ['fileOutput', 'Enable File Output_Output settings', 'string', trueFalse, 'False', 1, 0, 'Enables write to file options', self.enableFileOutputCB, 1],
                ['filePath', 'File Path_Output settings', directorySelection, None, directorySelection, 0, 1, 'The file path to the directory where the file should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],
                ['fileName', 'File Name_Output settings', 'string', None, '', 0, 0, 'The file name of the output', None, 1],
                ['fileDateFormat', 'Format of Date Added to File Name_Output settings', 'string', getDateFormats(), '', 0, 0, 'Format of the date added to the file name. No date is added to the file name if this field is empty. As default, it is appended at the end of the file name. Toggle checkbox Date at Beginning of File Name to insert the date at the beginning of the file name.', self.appendDateToFileNameCB, 1],
                ['fileDateBeginning', 'Date at Beginning of File Name_Output settings', 'string', trueFalse, 'False', 1, 0, 'Append date at beginning of file name', None, 1],
                ['fileCreateDirectory', 'Create Directory_Output settings', 'string', trueFalse, 'False', 1, 0, 'Create a directory', self.createDirectoryCB, 1],
                ['fileDirName', 'Directory Name_Output settings', 'string', None, '', 0, 0, 'Name for created directory', None, 1],
                ['fileDirDateFormat', 'Directory Date Format_Output settings', 'string', getDateFormats(), '', 0, 0, 'Date format for the date appended to the directory name', None, 1],
                ['fileOverwriteIfFileExists', 'Overwrite if File Exists_Output settings', 'string', trueFalse, 'True', 1, 0, 'If a file with the same name and path already exist, overwrite it?', self.overwriteCB, 1],
                ['fileMaxNrOfFilesInDir', 'Maximum Number of Files in Directory_Output settings', 'int', [], '256', 0, 0, 'Maximum number of files with the same name, disregarding appended number, allowed in a directory', None, 1],
                ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars, __name__)

def getAelVariables():
    outtab=OutputFileSettingsTab()
    outtab.LoadDefaultValues(__name__)
    return outtab

def validateVariables(aelParams):
    if trueFalse.index(aelParams['fileOutput']):
        if aelParams['fileName'] == '':
            raise Exception("File name must be specified")
        if aelParams['filePath'] == '':
            raise Exception("File path must be specified")
        if trueFalse.index(aelParams['fileCreateDirectory']):
            if aelParams['fileDirName'] == '' and aelParams['fileDirDateFormat'] == '':
                raise Exception("Directory name or date format must be specified to create directory")
        if trueFalse.index(aelParams['fileCreateDirectory']):
            if aelParams['fileDirName'] == '' and aelParams['fileDirDateFormat'] == '':
                raise Exception("Directory name or date format must be specified")
    return True

def getNewFilePath(aelParams, outputDir, ext):
    if trueFalse.index(aelParams['fileOutput']) and validateVariables(aelParams):
        return FFileUtils.getFilePath(outputDir, aelParams['fileName'], ext, \
                                      aelParams['fileDateFormat'], \
                                      trueFalse.index(aelParams['fileDateBeginning']), \
                                      trueFalse.index(aelParams['fileOverwriteIfFileExists']), \
                                      aelParams['fileMaxNrOfFilesInDir'])
    return None

def createOutputDir(aelParams):
    if trueFalse.index(aelParams['fileOutput']) and validateVariables(aelParams):
        return FFileUtils.createDirectory(aelParams['filePath'], aelParams['fileDirName'], aelParams['fileDirDateFormat'])
    return None


      
