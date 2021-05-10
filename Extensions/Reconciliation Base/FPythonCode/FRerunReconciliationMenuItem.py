""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FRerunReconciliationMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FRerunReconciliationMenuItem

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import FReconciliationMenuItem
from FRerunReconciliationEngine import FRerunReconciliationEngine
from FReconciliationGUI import ReconciliationPositionRetriever
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


class RerunReconciliationMenuItem(FReconciliationMenuItem.FReconciliationMenuItem):          
                 
    @staticmethod
    def _IsMissingDataValues(reconItem):
        return reconItem.ExternalValues().IsEmpty() and reconItem.InternalValues().IsEmpty()
        
    def _GetInfantStoredPosQueryForItem(self, reconItem):
        assert reconItem
        positionRetriever = ReconciliationPositionRetriever(reconItem, 
                                                            self._ReconciliationSpecification(reconItem, False), 
                                                            allowIncompletePositions = False)
        infantStoredPositionQuery = positionRetriever.RetrieveDynamicStoredPositionQuery()
        return infantStoredPositionQuery
        
    @staticmethod
    def _EnsureMissingSubject(reconItem):
        reconItem.Subject(None)

    def PrepareSheetItems(self, child):
        ''' Position recon items need preparation to be applicable for redo action '''
        while child:
            bp = child.Tree().Item()
            if bp and self.IsReconItemBusinessProcess(bp):
                reconItem = bp.Subject()
                if reconItem.ReconciliationDocument().ObjectType() == 'Position':
                    try:
                        infantStoredPositionQuery = self._GetInfantStoredPosQueryForItem(reconItem)
                        if infantStoredPositionQuery:
                            self._EnsureMissingSubject(reconItem)
                            reconItem.Subject(infantStoredPositionQuery)
                    except:
                        pass
            child = child.NextUsingDepthFirst()
        
    def IsApplicableForRun(self, bp):
        reconItem = bp.Subject()
        return not self._IsMissingDataValues(reconItem) and \
               not bool(self._IsUpload(bp.Subject(), upload = True))    
            
    def Engine(self, reconItem):
        #pylint: disable-msg=W0221
        return FRerunReconciliationEngine(reconItem)
        
    def Run(self, reconItem):
        return self.Engine(reconItem).Run()
        
    def LogSkippedRun(self, bp):
        reconItem = bp.Subject()
        if self._IsUpload(reconItem, upload = True):
            logger.warn('Reconciliation item %i is of type upload. Reconciliation redo procedures is thus not applicable.' % 
                         reconItem.Oid())
        if self._IsMissingDataValues(reconItem):
            logger.warn('External values data found missing for reconciliation item %i. \n' % 
                         reconItem.Oid())        
        logger.warn('Aborting redo processing.')           

    def Enabled(self):
        ''' Only disable for single selections '''
        if len(self.BusinessProcesses()) == 1:
            bp = self.BusinessProcesses()[0]        
            return self.IsApplicableForRun(bp)
        return not any([self._IsUpload(bp.Subject(), upload = True) for bp in self.BusinessProcesses()])

def CreateRerunReconciliationMenuItem(eii):
    return RerunReconciliationMenuItem(eii)
