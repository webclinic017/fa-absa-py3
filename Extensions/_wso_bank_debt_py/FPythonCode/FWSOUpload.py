""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOUpload.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOUpload

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Input example:
        params = {
            'StartDate': 'Inception', 
            'EndDate': 'Now', 
            'ReconciliationSpecification': 'WSO Upload Facility', 
            'LogLevel': '1. Normal', 
            'ForceReRun': '0', 
            'DisplayOption': '0', 
            'CustomStartDate': '', 
            'CustomEndDate': '', 
        }

-----------------------------------------------------------------------------"""

import os

import FWSODictAccessor
import FWSOUploadDialog
import FReconciliationSpecification
import FReconciliationWorkbench
import FAssetManagementUtils

from FUploadEngine import FUploadEngine
from FWSOPostUpload import CombLinkMaintainer, PostUploadContract

logger = FAssetManagementUtils.GetLogger()


class UploadInstance(object):
    
    def __init__(self, options):
        FAssetManagementUtils.ReinitializeLogger(FWSOUploadDialog.WSOUploadDialog.LOG_LEVELS[options.LogLevel])
        self.options = options
        self.forceReRun = (options.ForceReRun == '1')
        self.displayOperationsManager = (options.DisplayOption == '1')
        self.reconSpecName = options.ReconciliationSpecification
        self.reconSpec = None
        self.reconInstance = None
        self.filePath = None

    def SetReconSpecName(self, reconSpecName):
        self.reconSpecName = reconSpecName

    def _UploadType(self):
        ''' Determine what is being uploaded (Facility, Contract or Trade) '''
        objectType = self.reconSpec.ReconciliationObjectType()
        subType = self.reconSpec.ReconciliationSubType()
        if (objectType, subType) == ('Instrument', 'Combination'):
            return 'Facility'
        if (objectType, subType) == ('Instrument', 'FRN'):
            return 'Contract'
        if (objectType, subType) in [('Trade', None), ('Trade', '')]:
            return 'Trade'
        raise Exception('Unknown upload type pair: (%s [%s], %s [%s]).' % (objectType, type(objectType), subType, type(subType)))

    def _FilePath(self, uploadType):
        ''' Determine the path to the file defined by uploadType
            (Facility, Contract, Trade).
        '''
        wsoDirToWSODict = FWSODictAccessor.GetWSODictsCache()
        dirPath = wsoDirToWSODict.WSODirPath()
        wsoFilesInDir = wsoDirToWSODict.WSOFilesInDir()
        fileName = wsoFilesInDir.get(uploadType)
        if not fileName:
            raise Exception('No file path for the upload type %s was found.' % uploadType)
        filePath = os.path.join(dirPath, fileName)
        return filePath

    def _LoadDataUploadSpecification(self):
        try:
            self.reconSpec = FReconciliationSpecification.FReconciliationSpecification(self.reconSpecName, upload = True)
        except StandardError as error:
            logger.error('Failed to load data upload specification "%s": %s', \
                    self.options.ReconciliationSpecification, error)
            raise
        return self.reconSpec

    def _UpdateCombLinks(self):
        # Update combination links of uploaded combinations or FRNs
        linkMaintainer = CombLinkMaintainer()
        if self._UploadType() == 'Facility':
            # Remove redundant links (after Facility upload)
            linkMaintainer.RemoveOldCombLinksInReconInstance(self.ReconInstance())
        elif self._UploadType() == 'Contract':
            # Insert new links (after Contract upload)
            linkMaintainer.AddNewCombLinksInReconInstance(self.ReconInstance())
            
    def _PostUploadHandler(self):
        # Post upload contract initiator
        if self._UploadType() == 'Contract':
            reconInstance = self.ReconInstance()
            PostUploadContract.PostUploadContractInitiator(reconInstance)

    # Check whether this method can be removed (not used anywhere?)
    def RemoveOldCombLinksInReconInstance(self, reconInstance):
        ''' Removes comb links not in the current Contract XML '''
        if not reconInstance:
            return None
        reconItems = reconInstance.ReconciliationItems()
        for reconItem in reconItems:
            frn = reconItem.Subject()
            if not frn:
                continue
            try:
                linkRemover = OldCombinationLinkRemover()
                linkRemover.RemoveOldLinks(combination)
            except StandardError as e:
                logger.error(e)
                continue

    def _ExecuteDefaultPostUploadActions(self):
        self._UpdateCombLinks()
        self._PostUploadHandler()
        
    def _ExecutePostUploadHookIfAny(self):
        uploadType = self._UploadType()
        try:
            import FWSOCustomHooks
            if uploadType == 'Facility':
                result = FWSOCustomHooks.PostUploadFacility(self.reconInstance)
            elif uploadType == 'Contract':
                result = FWSOCustomHooks.PostUploadContract(self.reconInstance)
            elif uploadType == 'Trade':
                result = FWSOCustomHooks.PostUploadTrade(self.reconInstance)
            return result
        except ImportError:
            pass
        except AttributeError:
            pass

    def PerformUpload(self):
        self.reconSpec = self._LoadDataUploadSpecification()
        self.uploadType = self._UploadType()
        self.filePath = self._FilePath(self.uploadType)
        engine = FUploadEngine(self.filePath, self.reconSpec, self.options) 
        uploadInstance = engine.Run()
        self.reconInstance = uploadInstance
        self._ExecuteDefaultPostUploadActions()
        self._ExecutePostUploadHookIfAny()

    def ReconInstance(self):
        return self.reconInstance

    def LaunchOperationsManager(self):
        if self.reconInstance:
            logger.info('Processed %d item(s) for this file', self.reconInstance.ReconciliationDocument().ProcessedItemCount())
            if self.displayOperationsManager and self.reconInstance.ReconciliationItems():
                logger.debug('Displaying loaded reconciliation items in Operations Manager')
                FReconciliationWorkbench.StartApplication(self.reconInstance.ReconciliationDocument(), self.reconSpec)
                
    def UploadAndLaunchOperationsManager(self):
        self.PerformUpload()
        self.LaunchOperationsManager()


def ClearCache():
    wsoDirToWSODict = FWSODictAccessor.GetWSODictsCache()
    wsoDirToWSODict.ClearCache()

def RunUploadBasedOnParams(params):
    ClearCache()
    options = FWSOUploadDialog.WSOUploadDialog.getParameters(params)
    
    reconSpecName = options.ReconciliationSpecification
    uploadInstance = UploadInstance(options)
    uploadInstance.SetReconSpecName(reconSpecName)
    uploadInstance.UploadAndLaunchOperationsManager()
    
    logger.info('Data upload processing complete')


ael_variables = FWSOUploadDialog.WSOUploadDialog('Data Upload')
ael_variables.LoadDefaultValues(__name__)

def ael_main(params):
    RunUploadBasedOnParams(params)