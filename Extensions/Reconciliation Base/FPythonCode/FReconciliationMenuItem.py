""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FReconciliationMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationMenuItem

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
import FUxCore
from FReconciliationSpecification import GetReconciliationSpecification
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()

class FReconciliationMenuItem(FUxCore.MenuItem, object):

    def __init__(self, extObj):
        self._extObj = extObj

    def SelectedObjects(self):
        return self._extObj.ActiveSheet().Selection().SelectedRowObjects()
        
    def BusinessProcesses(self):
        return [bp for bp in self.SelectedObjects() if self.IsReconItemBusinessProcess(bp)]
            
    @staticmethod
    def IsReconItemBusinessProcess(obj):
        return (obj.IsKindOf(acm.FBusinessProcess) and
                obj.Subject().IsKindOf(acm.FReconciliationItem))
            
    @staticmethod
    def _ReconciliationSpecification(reconItem, upload):
        ''' Wrapper method for retrieving the reconciliation specification '''
        return GetReconciliationSpecification(reconItem, upload, relaxValidation = True)                   

    @staticmethod
    def _IsDiscrepancy(businessProcess):
        try:
            return businessProcess.CurrentStep().State().Name() == 'Discrepancy'
        except Exception:
            return False

    @classmethod
    def _IsUpload(cls, reconItem, upload = False):
        try:
            reconSpecification = cls._ReconciliationSpecification(reconItem, upload)
            return reconSpecification.Upload() and upload is True
        except Exception:
            return False
            
    @staticmethod
    def _ActionAsString(eii):
        return str(eii.MenuExtension().Name()).lower()

    def __PrivateRun(self, items, bp):
        reconItem = bp.Subject()    
        logger.info('----- For business process %i: -----' % bp.Oid())        
        if self.IsApplicableForRun(bp): 
            logger.info('Processing recon item %i...' % reconItem.Oid())
            success = self.Run(reconItem)
            if success:
                items.append(reconItem)
            else:
                self.LogSkippedRun(bp)
        else:
            self.LogSkippedRun(bp)
        logger.info('----- Finished processing of business process %i. -----' % bp.Oid())            
        
    def __PrivateInvoke(self, child, action):
        self.PrepareSheetItems(child)
        bps = self.BusinessProcesses()        
        logger.info('Attempting %s processing for %i selected item(s)' % (action, len(bps)))        
        items = list()
        for bp in bps:
            self.__PrivateRun(items, bp)
        logger.info('Finished %s processing for %i/%i selected items.' % (action, len(items), len(bps)))             
        
    def Invoke(self, eii):
        # pylint: disable-msg=E0102
        action = self._ActionAsString(eii)        
        logger.info('Preparing %s procedures...' % action)                
        sheet = eii.ExtensionObject().ActiveSheet()
        firstChild = sheet.RowTreeIterator(True).FirstChild()
        self.__PrivateInvoke(firstChild, action)
        logger.info('%s processing completed.' % action.title())            
        
    def Applicable(self):
        return True        
        
    ''' Possibly implement in child class '''
        
    def PrepareSheetItems(self, child):
        ''' Prepare sheet items before an action is invoked '''
        pass        
        
    ''' Implement in child classes '''
        
    def IsApplicableForRun(self, bp):
        ''' Dictate whether the business process is applicable to be 
            used in the engine run method 
        '''    
        raise NotImplementedError

    def Engine(self):
        ''' The engine of the process '''
        raise NotImplementedError        
        
    def Run(self, reconItem):
        ''' The implementation of an action on a given recon item '''
        raise NotImplementedError   
        
    def LogSkippedRun(self, bp):
        ''' Log message to be printed to the console in case a user 
            triggered action is not applicable for some reason 
        '''    
        raise NotImplementedError

    def Enabled(self):
        ''' Dictate whether a selection is enabled or not '''
        raise NotImplementedError    