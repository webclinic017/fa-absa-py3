""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FIdentifierExclusionList.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FIdentifierExclusionList

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import csv
import FRunScriptGUI

logger = FAssetManagementUtils.logger
logDict = FAssetManagementUtils.logDict

class InstrumentExclusionListVariables(FRunScriptGUI.AelVariablesHandler):

    def IdentifierExclusionLists(self):
        return acm.GetDefaultContext().GetAllExtensions("FExtensionValue", "FObject", True, True, "exclusion list", None, False)
     
    def SetColumnsCallback(self, index, fieldArray):
        ''' If additional fields are added, remember that the index below may change '''
        var = 2
        columns = self.CsvColumns(fieldArray[0])
        if columns:
            self.ael_variables[var][3] = columns
            fieldArray[2] = columns[0]
        return fieldArray
   
    def CsvColumns(self, filePath):
        try:
            if filePath:
                with open(filePath, 'rb') as inputfile:
                    exclusionListReader = csv.DictReader(inputfile)
                    return sorted(list(set([colId for rowItem in exclusionListReader for colId in rowItem.keys()])))
        except IOError as e:
            logger.WLOG('Failed to open file %s' % (e))

    def AelVariables(self):
        filepathTT = 'Filepath to a csv file with the identifiers'
        idListTT = 'Page Group to apply actions to'
        filter = "CSV Files (*.csv)|*.csv"
        columnTT = 'One column from selected csv file'
        idLists = self.IdentifierExclusionLists()
        ael_variables = [
            ['FILEPATH', 'Input File', FRunScriptGUI.InputFileSelection(filter), None, FRunScriptGUI.InputFileSelection(filter), 1, 1,
             filepathTT, self.SetColumnsCallback, 1],
            ['ID_LIST', 'ID List', 'string', idLists, None, 1, 0, idListTT, None, bool(idLists)],
            ['COLUMN',   'Column', 'string',           [],                None,       1, 0, columnTT, None, 1],
            ['LOG_MODE', 'Logmode_Logging', 'string', sorted(logDict), '1. Normal', 1, 0, log_tip]
        ] 
        return ael_variables
    
    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, self.AelVariables())


class ScriptHandler(object):

    def __init__(self, params):
        self.filepath = str(params['FILEPATH'])
        self.idListName = params['ID_LIST']
        self.column = params['COLUMN']

    def Identifiers(self):
        try:
            with open(self.filepath, 'rb') as inputfile:
                exclusionListReader = csv.DictReader(inputfile)
                for row in exclusionListReader:
                    yield row[self.column]
        except IOError as e:
            logger.WLOG('Failed to open file %s' % (e))
        
    def Upload(self):
        self.ImportNewList()
        self.Module().Commit()
        
    def Module(self):
        extension =  acm.GetDefaultContext().GetExtension("FExtensionValue", "FObject", self.idListName)
        if extension:
            return extension.Module()
        else:
            raise ValueError('Could not find extension value %s'%self.idListName)
        
    def Header(self):
        return 'FObject:'+self.idListName
        
    def ImportNewList(self):
        newIdList = self.Header() + '\n'
        for identifier in self.Identifiers():
            if identifier:
                newIdList += identifier + '\n'
        acm.GetDefaultContext().EditImport('FExtensionValue', newIdList, False, self.Module())

# Run Script GUI Setup
log_tip = 'Logmode 0 shows WARNING and ERROR messages. Logmode 1 shows INFORMATION messages, and also includes the ' \
          'messages from Logmode 0. Logmode 2 shows DEBUG messages and includes all other message types. '
ael_variables = InstrumentExclusionListVariables()

def InitLogger(logMode):
    logger.Reinitialize(level=logDict[logMode],
        keep=None,
        logOnce=None,
        logToConsole=1,
        logToPrime=None,
        logToFileAtSpecifiedPath=None,
        filters=None,
        lock=None
    )

def ael_main(params):

    InitLogger(params['LOG_MODE'])
    logger.info('Updating identifier list "%s" from file "%s"..'%(params['ID_LIST'], params['FILEPATH']))
    try:
        scriptHandler = ScriptHandler(params)
        scriptHandler.Upload()
    except Exception as e:
        logger.error('Update of identifier list failed. Reason: %s'%str(e))
    else:
        logger.info('Identifier list update completed')