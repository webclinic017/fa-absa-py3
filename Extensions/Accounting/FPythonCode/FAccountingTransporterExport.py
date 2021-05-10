""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingTransporterExport.py"

import acm
import os, urllib, zipfile, time
import FRunScriptGUI
import FAccountingTransporter

from FOperationsIO import GetDefaultPath, IsPathValid, IsFileNameValid
from FBDPCurrentContext import Logme, CreateLog


class OperationsExportGUI(FRunScriptGUI.AelVariablesHandler):

    BOOK_INDEX = 1
    TREATMENT_INDEX = 2
    AI_INDEX = 3

    def __init__(self):
        self.__filteredTreatmentsSet = acm.FSet()
        self.__filteredAccountingInstructionSet = acm.FSet()

        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    def __CreateAelVariables(self):
        dirSelectionExport = FRunScriptGUI.DirectorySelection()

        dirSelectionLogfile = FRunScriptGUI.DirectorySelection()
        dirSelectionLogfile.SelectedDirectory(str(GetDefaultPath()))

        ttLogToCon = ('Whether logging should be done in the Log Console or not.')
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = ('Name of the logfile. Could include the whole path, c:\temp\...')
        ttCompleteExport = ('Complete export of the accounting setup')

        return  [
                 ['basepath', 'Export path', dirSelectionExport, None, dirSelectionExport, 0, 1, 'The default path', None, True],
                 ['books', 'Book name(s)', 'FBook', acm.FBook.Select(""), '', 0, 1, 'Select Books', self.__OnBooksChanged, 1],
                 ['treatments', 'Treatment name(s)', 'FTreatment', self.__filteredTreatmentsSet, '', 0, 1, 'Select Treatments', self.__OnTreatmentsChanged, 1],
                 ['accountinginstructions', 'AccountingInstruction name(s)', 'FAccountingInstruction', self.__filteredAccountingInstructionSet, '', 0, 1, 'Select Accounting Instructions', self.__OnAccountingInstructionsChanged, 1],
                 ['LogToConsole', 'Log to console_Logging', 'int', [1, 0], 1, 1, 0, ttLogToCon],
                 ['LogToFile', 'Log to file_Logging', 'int', [1, 0], 0, 1, 0, ttLogToFile, self.__OnLogToFile],
                 ['LogfilePath', 'Log file path_Logging', dirSelectionLogfile, None, dirSelectionLogfile, 0, 1, 'The default log file path', None,None],
                 ['Logfile', 'Log file_Logging', 'string', None, 'AccountingExport.log', 0, 0, ttLogFile, None, None],
                 ['CompleteExport', 'Complete accounting export', 'bool', ["True", "False"], "False", 1, 0, ttCompleteExport, self.__OnCompleteExport]
                ]


    def __OnLogToFile(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To File to be able to select a Logfile.')
        self.LogfilePath.enable(fieldValues[index])
        return fieldValues

    def __OnCompleteExport(self, index, fieldValues):
        isEnabled = True if fieldValues[index] == "True" else False

        self.books.enable(not isEnabled)
        self.books.set(fieldValues, '')
        self.__OnBooksChanged(index, fieldValues)

        return fieldValues

    def __OnBooksChanged(self, index, fieldValues):
        selectedBooks = self.__ObjectsFromString(index, fieldValues, acm.FBook)

        fieldValues = self.__UpdateTreatments(fieldValues, selectedBooks)
        fieldValues = self.__OnTreatmentsChanged(self.TREATMENT_INDEX, fieldValues)

        return fieldValues

    def __OnTreatmentsChanged(self, index, fieldValues):
        selectedTreatments = self.__ObjectsFromString(index, fieldValues, acm.FTreatment)

        fieldValues = self.__UpdateAccountingInstructions(fieldValues, selectedTreatments)
        fieldValues = self.__OnAccountingInstructionsChanged(self.AI_INDEX, fieldValues)

        return fieldValues

    def __OnAccountingInstructionsChanged(self, index, fieldValues):
        return fieldValues

    def __UpdateTreatments(self, fieldValues, selectedBooks):
        self.__filteredTreatmentsSet.Clear()

        for book in selectedBooks:
            self.__filteredTreatmentsSet.AddAll(book.Treatments())

        sortedList = self.__filteredTreatmentsSet.AsArray().SortByProperty('Name')

        self.treatments.set(fieldValues, (self.__ObjectsToString(sortedList)))
        self.treatments.enable(not self.__filteredTreatmentsSet.IsEmpty())

        return fieldValues

    def __UpdateAccountingInstructions(self, fieldValues, selectedTreatments):
        self.__filteredAccountingInstructionSet.Clear()

        selectedBooks = self.__ObjectsFromString(self.BOOK_INDEX, fieldValues, acm.FBook)
        for treatment in selectedTreatments:
            treatmentLinks = treatment.TreatmentLinks()
            for treatmentLink in treatmentLinks:
                if treatmentLink.Book() in selectedBooks:
                    self.__filteredAccountingInstructionSet.Add(treatmentLink.AccountingInstruction())

        sortedList = self.__filteredAccountingInstructionSet.AsArray().SortByProperty('Name')

        self.accountinginstructions.set(fieldValues, self.__ObjectsToString(sortedList))
        self.accountinginstructions.enable(not self.__filteredAccountingInstructionSet.IsEmpty())

        return fieldValues

    def __ObjectsToString(self, objList):
        return ','.join([obj.Name() for obj in objList])

    def __ObjectsFromString(self, index, fieldValues, objClass):
        list = acm.FArray()

        for name in fieldValues[index].split(','):
            obj = objClass[name]
            if obj:
                list.Add(obj)

        return list

def IsValidInput(logToFile, exportPath, logfilePath, logfileName):
    if not IsPathValid(exportPath):
        acm.Log('Error: Export path does not exist.')
        return False

    if logToFile == 1:
        if not IsPathValid(logfilePath):
            acm.Log('Error: Log file path does not exist.')
            return False
        if not IsFileNameValid(logfileName):
            acm.Log('Error: Log file name contains invalid characters.')
            return False
        if not logfileName:
            acm.Log('Error: No log file name.')
            return False

    return True

def ael_main(params):

    title = 'Accounting Export'
    myPath = "%s" % params['basepath']
    safeChars = ' @.Â‰ˆ¸¯Ê≈ƒ÷‹ÿ∆ﬂ'

    logfilePath = "%s" % params['LogfilePath']
    logfile = "%s" % params['Logfile']
    entirePath = os.path.join(logfilePath, logfile)

    if IsValidInput(params['LogToFile'], myPath, logfilePath, logfile):
        fileExtensionMap = FAccountingTransporter.fileExtensionMap

        CreateLog(title, 1, params['LogToConsole'], params['LogToFile'], entirePath, 0, "", "")

        Logme()('%s started by user %s at %s' % (title, str(acm.UserName()), time.ctime()))
        Logme()('')

        if params['CompleteExport']:
            fileName = "%s.%s" % (myPath + "\\" + urllib.quote('ADS_' + acm.FACMServer().ADSAddress().replace(':', '_'), safeChars), fileExtensionMap[FAccountingTransporter.FileExtensionMapKey.KEY_COMPLETE_EXPORT])

            zipFile = zipfile.ZipFile(fileName, "w", zipfile.ZIP_DEFLATED)
            FAccountingTransporter.ExportBooksOnly(zipFile, acm.FBook.Select(''))
            FAccountingTransporter.ExportTreatmentsOnly(zipFile, acm.FBook.Select(''), acm.FTreatment.Select(''))
            FAccountingTransporter.ExportAccountingInstructionsOnly(zipFile, acm.FTreatment.Select(''), acm.FAccountingInstruction.Select(''))
            FAccountingTransporter.ExportTAccounts(zipFile, acm.FTAccountAllocationLink.Select(''))
            zipFile.close()
        else:
            books = params['books']
            treatments = params['treatments']
            accountingInstructions = params['accountinginstructions']

            for book in books:
                filename = "%s.%s" % (myPath + "\\" + urllib.quote(book.Name(), safeChars), fileExtensionMap[FAccountingTransporter.FileExtensionMapKey.KEY_BOOK])
                myZipFile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
                FAccountingTransporter.ExportBooks(myZipFile, [book], treatments, accountingInstructions)
                myZipFile.close()

        Logme()('')
        Logme()('%s finished at %s.' % (title, time.ctime()))


ael_gui_parameters = {
                      'runButtonLabel' : 'Export',
                      'hideExtraControls' : True,
                      'windowCaption' : 'Accounting Transporter Export',
                      'version' : '%R%'
                      }

ael_variables = OperationsExportGUI()

