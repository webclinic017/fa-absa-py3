""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FUploadMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FUploadMenuItem

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import FReuploadEngine
import FReconciliationMenuItem
import FAssetManagementUtils
from FReuploadEngine import FReuploadEngine

logger = FAssetManagementUtils.GetLogger()


class UploadMenuItemBase(FReconciliationMenuItem.FReconciliationMenuItem):


    def __init__(self, extObj):
        super(UploadMenuItemBase, self).__init__(extObj)
        self._resolveBreaks = False
        
    def ResolveBreaks(self):
        return self._resolveBreaks        
        
    @staticmethod
    def _IsInvalidData(businessProcess):
        try:
            return businessProcess.CurrentStep().State().Name() == 'Invalid data'
        except Exception:
            return False           
        
    def Engine(self, reconItem):
        # pylint:disable-msg=W0221
        return FReuploadEngine(reconItem)
    
    def Run(self, reconItem):
        return self.Engine(reconItem).Run(resolveBreaks = self.ResolveBreaks())
        
    def LogSkippedRun(self, bp):
        reconItem = bp.Subject()
        if not self._IsUpload(reconItem, upload = True):
            logger.warn('Reconciliation item %i is not of type upload. Further processing is thus not applicable.' % 
                         reconItem.Oid())                  
        logger.warn('Any further actions will be aborted.')                         
        
class AcceptChangesMenuItem(UploadMenuItemBase):

    def __init__(self, extObj):
        super(AcceptChangesMenuItem, self).__init__(extObj)
        self._resolveBreaks = True

    def IsApplicableForRun(self, bp):
        return self._IsUpload(bp.Subject(), upload = True)
        
    def Enabled(self):
        ''' Only disable for single selections '''
        if len(self.BusinessProcesses()) == 1:
            bp = self.BusinessProcesses()[0]
            return self.IsApplicableForRun(bp)            
        return all([self._IsUpload(bp.Subject(), upload = True) for bp in self.BusinessProcesses()])

class RerunUploadMenuItem(UploadMenuItemBase):

    def __init__(self, extObj):
        super(RerunUploadMenuItem, self).__init__(extObj)        
        
    def IsApplicableForRun(self, bp):
        return self._IsUpload(bp.Subject(), upload = True)
                
    def Enabled(self):
        ''' Only disable for single selections '''
        if len(self.BusinessProcesses()) == 1:
            bp = self.BusinessProcesses()[0]
            return self.IsApplicableForRun(bp)
        return all([self._IsUpload(bp.Subject(), upload = True) for bp in self.BusinessProcesses()])

def CreateRerunUploadMenuItem(eii):
    return RerunUploadMenuItem(eii)

def CreateAcceptChangesMenuItem(eii):
    return AcceptChangesMenuItem(eii)