""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FInstrumentExclusionList.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FInstrumentExclusionList

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

    def SubGroupsRecursive(self, exclusionList):
        returnGroups = []
        if exclusionList.Terminal():
            returnGroups.append(exclusionList)
        for subList in exclusionList.SubGroups():
            returnGroups.extend(self.SubGroupsRecursive(subList))
        return returnGroups
        
    def ExclusionListPageGroups(self):
        topItem = acm.FPageGroup['ExclusionList']
        if topItem:
            leafSubgroups = self.SubGroupsRecursive(topItem)
            return leafSubgroups
        else:
            return []
        
    def AelVariables(self):
        filepathTT = 'Filepath to a csv file with an "ISIN" column to identify the instruments'
        pageGroupTT = 'Page Group to apply actions to'
        actionTT = 'Choose action to apply to page group'
        filter = "CSV Files (*.csv)|*.csv"
        pageGroups = self.ExclusionListPageGroups()
        ael_variables = [
            ['FILEPATH', 'Input File', FRunScriptGUI.InputFileSelection(filter), None, FRunScriptGUI.InputFileSelection(filter), 1, 1,
             filepathTT, None, 1],
            ['PAGE_GROUP', 'Page Group', 'FPageGroup', pageGroups, None, 1, 0, pageGroupTT, None, bool(pageGroups)],
            ['ACTION', 'Action', 'string', ["Add Instruments", "Replace Instruments", "Remove Instruments"], "", 1, 0, actionTT, None],
            ['LOG_MODE', 'Logmode_Logging', 'string', sorted(logDict), '1. Normal', 1, 0, log_tip]
        ] 
        return ael_variables
    
    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, self.AelVariables())


class ScriptHandler():

    def __init__(self, params, instruments):
        self.filepath = str(params['FILEPATH'])
        self.pageGroup = params['PAGE_GROUP']
        self.action = params['ACTION']
        self.instruments = instruments
        
    def TakeAction(self):
        if self.action == 'Add Instruments':
            self.AddInstrumentsToPageGroup()
        elif self.action == 'Replace Instruments':
            self.ReplaceInstruments()
        else:
            self.RemoveListedInstruments()
        self.CommitPageGroup(self.pageGroup)
        
    def ReplaceInstruments(self):
        self.RemoveAllInstruments()
        self.AddInstrumentsToPageGroup()
            
    def AddInstrumentsToPageGroup(self):
        for instrument in self.instruments:
            if self.instrumentInExclusionList(instrument):
                continue
            else:
               self.CreateInstrGroupMap(instrument)

    def CreateInstrGroupMap(self, instrument):
        instrGroupMap = acm.FInstrGroupMap()
        instrGroupMap.Instrument(instrument)
        instrGroupMap.Group(self.pageGroup)
        try:
            instrGroupMap.Commit()
            logger.LOG('Added instrument with ISIN "%s" to Exclusion List %s' % (instrument.Isin(), self.pageGroup.Name()))
        except RuntimeError as e:
            logger.WLOG('Failed to create FInstrGroupMap for ISIN "%s" in group %s: %s' %
                        (instrument.Isin(), self.pageGroup.Name(), str(e)))
        
    def RemoveAllInstruments(self):
        instruments = self.pageGroup.InstrumentsRecursively()
        for instrument in instruments:
            acm.FInstrGroupMap.Select01('instrument=%s and group=%s' % (instrument.Oid(), self.pageGroup.Oid()), None).Delete()
            logger.WLOG('Deleted instrument with ISIN "%s" from Exclusion List %s' % (instrument.Isin(), self.pageGroup.Name()))
            
    def RemoveListedInstruments(self):
        for instrument in self.instruments:
            instrGroup = acm.FInstrGroupMap.Select01('instrument=%s and group=%s' % (instrument.Oid(), self.pageGroup.Oid()), None)
            if instrGroup:
                instrGroup.Delete()
                logger.WLOG('Deleted instrument with ISIN "%s" from Exclusion List %s' % (instrument.Isin(), self.pageGroup.Name()))
        
    def instrumentInExclusionList(self, instrument):
        instrGroupMap = acm.FInstrGroupMap.Select01('instrument=%s and group=%s' % (instrument.Oid(), self.pageGroup.Oid()), None)
        if instrGroupMap:
            logger.DLOG('The InstrGroupMap with ISIN "%s" already exists. None is created.' % instrument.Isin())
            return True
        else:
            return False
    
    def CommitPageGroup(self, pageGroup):
        imgage = pageGroup.StorageImage()
        imgage.UpdateTime = acm.Time.TimeNow()
        imgage.Commit()
        if pageGroup.SuperGroup():
            self.CommitPageGroup(pageGroup.SuperGroup())
        

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

def ValidParams(params):
    if params['FILEPATH'] and params['PAGE_GROUP']:
        return True
    else:
        logger.WLOG('Missing Inputs')
        return False

def InstrumentsFromCsv(filepath):
    try:
        instruments = []
        with open(filepath, 'rb') as inputfile:
            exclusionListReader = csv.DictReader(inputfile)
            for row in exclusionListReader:
                instrument = InstrumentFromRow(row)
                if instrument:
                    instruments.append(instrument)
        return instruments
    except IOError as e:
        logger.WLOG('Failed to open file %s' % (e))
    except KeyError as e:
        logger.WLOG('Failed find field %s in file' % (e))
    return None
        
def InstrumentFromRow(row):
    isin = row['ISIN'].strip()
    if isin:
        instrument = acm.FInstrument.Select01('isin = {0}'.format(isin), None)
        if instrument:
            return instrument
        else:
            logger.WLOG('Failed to find instrument %s' % (row))
            return None

def ael_main(params):

    InitLogger(params['LOG_MODE'])

    if params['PAGE_GROUP']:
        instruments = InstrumentsFromCsv(str(params['FILEPATH']))
        if ValidParams(params) and instruments:
            scriptHandler = ScriptHandler(params, instruments)
            scriptHandler.TakeAction()
    else:
        logger.LOG('No page group found')
        raise IOError('No page group found. Create a page definition folder called ExclusionList and store your page groups there.')
