""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FReuploadEngine.py"
"""--------------------------------------------------------------------------
MODULE
    FReuploadEngine

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
import FExternalDataImportEngine
import FUploadWorkflow
import FReconciliationContainer as RC
import FReconciliationSpecification

import FAssetManagementUtils
logger = FAssetManagementUtils.GetLogger()


class FReuploadEngine(FExternalDataImportEngine.FExternalDataImportEngine):

    REDO_EVENT_NAME = 'Redo'

    def __init__(self, reconItem):
        self._reconItem = reconItem
        reconciliationSpecification = self._GetReconciliationSpecification()
        # On a rerun, ReconciliationItems should never be removed
        reconciliationSpecification.StoreReconciledItems(True)
        super(FReuploadEngine, self).__init__(reconciliationSpecification, None)
        
    def ReconciliationItem(self):
        return self._reconItem
        
    def _GetReconciliationSpecification(self):
        ''' Returns the FReconciliationSpecification instance for a stored reconciliation item object.
            Use this (helper) method when accessing the specification during recon processing. 
        '''
        reconciliationName = self.ReconciliationItem().ReconciliationDocument().ReconciliationName()
        try:
            return FReconciliationSpecification.FReconciliationSpecification(reconciliationName, upload = True)
        except ValueError as e:
            logger.error('Failed to load reconciliation specification "%s" for reconciliation item %d: %s',
                          reconciliationName, self.ReconciliationItem().Oid(), e)
            raise
        return None
                 
    def HandleBusinessObjects(self, resolveBreaks):
        for wf in self.ReconciliationInstance().Workflows():
            try:
                if not wf.IsIdentified():
                    wf.CreateBusinessObject()
                elif not wf.IsBreak():
                    wf.CreateBusinessObject()
                elif resolveBreaks and wf.IsBreak():
                    wf.CreateBusinessObject()
                    wf.IsBreak(False)
            except Exception as err:
                wf.ErrorMessage(str(err))
                continue

            if wf.BusinessDataCreator() != None:
                wf.CommitBusinessObject()
                
    def ParametersForReRun(self):
        # Return a tuple (redo event name, notes, params) of input parameters for redo
        return ( self.REDO_EVENT_NAME, 
                 ['Manually triggered redo event by user %s' % acm.User().Name(), ], 
                 acm.FDictionary() )   

    def __PrivatePrepareForRun(self): 
        # pylint: disable-msg=W0221
        reconDocument = self._reconItem.ReconciliationDocument()
        self.ReconciliationInstance(RC.FReconciliationInstance(self.ReconciliationSpecification(),
                                                               fileName = None, 
                                                               forceReRun = False, 
                                                               reconDocument=reconDocument))
        try:
            workflow = FUploadWorkflow.FUploadWorkflow(self.ReconciliationInstance(),
                                                       None,
                                                       self._reconItem)
                                                       
            bpw = self.ReinitializeBusinessProcess(self.ReconciliationItem(), 
                                                   self.ReconciliationSpecification(), 
                                                   self.ParametersForReRun())
            if bpw and bpw.IsReinitialized(): 
                workflow.BusinessProcess(bpw.BusinessProcess())
                self.AddWorkflow(workflow)
            else:
                return None
        except (ValueError, TypeError, AttributeError) as err:
            workflow = FUploadWorkflow.FUploadWorkflow(self.ReconciliationInstance(), {})
            workflow.ErrorMessage('Error on workflow creation: %s'%(str(err)))
            self.AddWorkflow(workflow) 
        return bpw.IsReinitialized()
            
    def __PrivateRun(self, resolveBreaks):
        self.RunIdentification()
        self.RunComparison()
        self.ReconciliationInstance().Commit()
        self.HandleBusinessObjects(resolveBreaks)
        self.CommitWorkflows()    
             
    def Run(self, resolveBreaks=False):
        # pylint: disable-msg=W0221
        logger.debug('Redoing upload process for recon item %i' % self.ReconciliationItem().Oid())    
        isPrepared = self.__PrivatePrepareForRun()
        if isPrepared:
            self.__PrivateRun(resolveBreaks)
            return self.ReconciliationInstance()