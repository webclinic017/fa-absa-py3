""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FIssuerExclusionList.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FIssuerExclusionList

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import csv
import FRunScriptGUI

logger = FAssetManagementUtils.logger
logDict = FAssetManagementUtils.logDict

class IssuerExclusionListVariables(FRunScriptGUI.AelVariablesHandler):

    def SubGroupsRecursive(self, exclusionList):
        returnGroups = []
        if exclusionList.Terminal():
            returnGroups.append(exclusionList)
        for subList in exclusionList.SubGroups():
            returnGroups.extend(self.SubGroupsRecursive(subList))
        return returnGroups
        
    def ExclusionListIssuerGroups(self):
        return acm.FPartyGroup.Select('groupType = Issuer Group')
        
    def AelVariables(self):
        filepathTT = 'Filepath to a csv file with an "NAME" column to identify the issuers'
        issuerGroupTT = 'Issuer Group to apply actions to'
        actionTT = 'Choose action to apply to issuer group'
        filter = "CSV Files (*.csv)|*.csv"
        ael_variables = [
            ['FILEPATH', 'Input File', FRunScriptGUI.InputFileSelection(filter), None, FRunScriptGUI.InputFileSelection(filter), 1, 1,
             filepathTT, None, 1],
            ['ISSUER_GROUP', 'Issuer Group', 'FPartyGroup', self.ExclusionListIssuerGroups(), None, 1, 0, issuerGroupTT, None, 1],
            ['ACTION', 'Action', 'string', ["Add Issuers", "Replace Issuers", "Remove Issuers"], "", 1, 0, actionTT, None],
            ['LOG_MODE', 'Logmode_Logging', 'string', sorted(logDict), '1. Normal', 2, 0, log_tip]
        ] 
        return ael_variables
    
    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, self.AelVariables())
        
class ScriptHandler():

    def __init__(self, params, issuers):
        self.issuers = issuers
        self.issuerGroup = params['ISSUER_GROUP']
        self.action = params['ACTION']
        
    def TakeAction(self):
        if self.action == 'Add Issuers':
            self.AddIssuers()
        elif self.action == 'Replace Issuers':
            self.ReplaceIssuers()
        else:
            self.RemoveListedIssuers()
        self.CommitIssuerGroup()
        
    def AddIssuers(self):
        for issuer in self.issuers:
            if self.IssuerInIssuerGroup(issuer):
                continue
            else:
                self.CreateIssuerGroupMap(issuer)
                
    def CreateIssuerGroupMap(self, issuer):
        issuerGroupMap = acm.FPartyGroupLink()
        issuerGroupMap.Party(issuer)
        issuerGroupMap.PartyGroup(self.issuerGroup)
        try:
            issuerGroupMap.Commit()
            logger.LOG('Added issuer "%s" to Issuer Group %s' % (issuer.Name(), self.issuerGroup.Name()))
        except RuntimeError as e:
            logger.WLOG('Failed to create FPartyGroupLink for %s in group %s: %s' %
                        (issuer.Name(), self.issuerGroup.Name(), str(e)))
            
    def ReplaceIssuers(self):
        self.RemoveAllIssuers()
        self.AddIssuers()
        
    def RemoveListedIssuers(self):
        for issuer in self.issuers:
            issuerGroupLink = acm.FPartyGroupLink.Select01("partyGroup='%s' and party='%s'"  % (self.issuerGroup.Name(), issuer.Name()), None)
            if issuerGroupLink:
                issuerGroupLink.Delete()
                logger.LOG('Deleted issuer %s from Exclusion List %s' % (issuer.Name(), self.issuerGroup.Name()))
        
    def RemoveAllIssuers(self):
        for issuer in self.issuerGroup.Parties()[:]:
            logger.LOG('Deleted issuer %s from Exclusion List %s' % (issuer.Name(), self.issuerGroup.Name()))
            issuer.Delete()
            
    def IssuerInIssuerGroup(self, issuer):
        issuerGroupLink = acm.FPartyGroupLink.Select01('party=%s and partyGroup=%s' % (issuer.Oid(), self.issuerGroup.Oid()), None)
        if issuerGroupLink:
            logger.DLOG('The issuerGroupLink already exists for issuer "%s". None is created.' % issuer.Name())
            return True
        else:
            return False
                    
    def CommitIssuerGroup(self):
        imgage = self.issuerGroup.StorageImage()
        imgage.UpdateTime = acm.Time.TimeNow()
        imgage.Commit()


# Run Script GUI Setup
log_tip = 'Logmode 0 shows WARNING and ERROR messages. Logmode 1 shows INFORMATION messages, and also includes the ' \
          'messages from Logmode 0. Logmode 2 shows DEBUG messages and includes all other message types. '

ael_variables = IssuerExclusionListVariables()

def ValidParams(params):
    if params['FILEPATH'] and params['ISSUER_GROUP']:
        return True
    else:
        logger.WLOG('Missing Inputs')
        return False

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
    
def IssuersFromCsv(filepath):
    issuers = []
    try:
        with open(filepath, 'rb') as inputfile:
            exclusionListReader = csv.DictReader(inputfile)
            for row in exclusionListReader:
                issuer = IssuerFromRow(row)
                if issuer:
                    issuers.append(issuer)
        return issuers
    except IOError as e:
        logger.WLOG('Failed to open file %s' % (e))
    except KeyError as e:
         logger.WLOG('Failed to find field %s in input file', e)
    return None
    
def IssuerFromRow(row):
    issuerName = row['NAME'].strip()
    issuer = acm.FParty.Select01('name = {0}'.format(issuerName), None)
    if issuer:
        return issuer
    else:
        logger.WLOG('Failed to find issuer %s' % (row))
        return None

def ael_main(params):
    
    InitLogger(params['LOG_MODE'])
    issuers = IssuersFromCsv(str(params['FILEPATH']))
    
    if ValidParams(params) and issuers:
        scriptHandler = ScriptHandler(params, issuers)
        scriptHandler.TakeAction()