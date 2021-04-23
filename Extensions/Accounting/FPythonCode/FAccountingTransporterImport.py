""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingTransporterImport.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAccountingTransporterImport

    (c) Copyright 2013 by SunGard Front Arena. All rights reserved.

VERSION
    %R%
DESCRIPTION

MAJOR REVISIONS

    2013-02-05  RL  Initial implementation
    2013-03-12  KA  Revision
-------------------------------------------------------------------------------------------------------"""
import acm
import os, zipfile, time
import FRunScriptGUI
import FAccountingTransporter
from FBDPCurrentContext import Logme, CreateLog
from FAccountingBackup import BookBackup



fileExtensionMap = FAccountingTransporter.fileExtensionMap
updatePathFields = fileExtensionMap.keys()

class OperationsImportGUI(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        dirSelection = FRunScriptGUI.DirectorySelection()

        ttLogToCon = ('Whether logging should be done in the Log Console or not.')
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = ('Name of the logfile. Could include the whole path, c:\temp\...')
        ttBackup = ('Create backup file before import.')

        variables = [
                     ['basepath', 'Import path', dirSelection, None, dirSelection, 0, 1, 'The default path', self.__OnPathChanged, True],
                     ['completeExport', 'Complete accounting export file', 'string', [''], None, 0, 1, 'Select files', None, True],
                     ['book', 'Book name(s)', 'string', [''], None, 0, 1, 'Select book files', None, True],
                     ['LogToConsole', 'Log to console_Logging', 'int', [1, 0], 1, 1, 0, ttLogToCon],
                     ['LogToFile', 'Log to file_Logging', 'int', [1, 0], 0, 1, 0, ttLogToFile, self.__OnLogToFile],
                     ['Logfile', 'Log file_Logging', 'string', None, 'AccountingImport.log', 0, 0, ttLogFile, None, None],
                     ['backupPath', 'Backup file path_Backup', dirSelection, None, dirSelection, 0, 1, ttBackup, None, True]
                    ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    def __OnPathChanged(self, index, fieldvalues):
        path = str(fieldvalues[index])
        for idx, var in enumerate(ael_variables):
            if idx != index and var[0] in updatePathFields:
                self.UpdatePath(path, var[3], fileExtensionMap[var[0]])
        return fieldvalues

    def UpdatePath(self, path, files, extension):
        if isinstance(files, type([])):
            del files[:] # List
        else:
            files.Clear() # FArray

        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith(extension):
                    if isinstance(files, type([])):
                        files.append(filename)
                    else:
                        files.Add(filename)
        elif path.strip() != '':
            pass

    def __OnLogToFile(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To File to be able to select a Logfile.')
        return fieldValues

def ael_main(params):

    title = 'Accounting Import'
    mypath = "%s" % params['basepath']
    backupFilePath = str(params['backupPath'])

    CreateLog(title, 1, params['LogToConsole'], params['LogToFile'], params['Logfile'], 0, "", "")

    Logme()('%s started by user %s at %s' % (title, str(acm.UserName()), time.ctime()))
    Logme()('')

    if mypath and os.path.exists(mypath):
        if backupFilePath and os.path.exists(backupFilePath):
            bookBackup = BookBackup(params['book'], backupFilePath)
            bookBackup.ExportEntities()

        for book in params['book']:
            myZipFile = zipfile.ZipFile(mypath + "\\" + book, "r", zipfile.ZIP_DEFLATED)
            FAccountingTransporter.ImportBooks(myZipFile)
            myZipFile.close()

        for completeExport in params['completeExport']:
            myZipFile = zipfile.ZipFile(mypath + "\\" + completeExport, "r", zipfile.ZIP_DEFLATED)
            FAccountingTransporter.ImportBooks(myZipFile)
            myZipFile.close()

        Logme()('')
        Logme()('%s finished at %s.' % (title, time.ctime()))
    else:
        Logme()("Invalid path")


ael_gui_parameters = {
                      'runButtonLabel' : 'Import',
                      'hideExtraControls' : True,
                      'windowCaption' : 'Accounting Transporter Import',
                      'version' : '%R%'
                      }

ael_variables = OperationsImportGUI()
