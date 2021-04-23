""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FUpload.py"
"""--------------------------------------------------------------------------
MODULE
    FUpload

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import FReconciliationDialog
from FUploadEngine import FUploadEngine
import FReconciliationSpecification
import FReconciliationWorkbench
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()

ael_variables = FReconciliationDialog.ReconciliationDialog('Data Upload')
ael_variables.LoadDefaultValues(__name__)
ael_gui_parameters = ael_variables.GUIParams()

def ael_main(params):
    # pylint: disable-msg=E1101,
    logger.info('Initiating data upload processing...')    
    options = FReconciliationDialog.ReconciliationDialog.getParameters(params)
    FAssetManagementUtils.ReinitializeLogger(FReconciliationDialog.ReconciliationDialog.LOG_LEVELS[options.LogLevel])
    if options.Filename:
        forceReRun = (options.ForceReRun == '1')
        displayOperationsManager = (options.DisplayOption == '1')
        try:
            reconSpec = FReconciliationSpecification.FReconciliationSpecification(options.ReconciliationSpecification, upload = True)
        except StandardError as err:
            logger.error('Failed to load data upload specification "%s": %s', options.ReconciliationSpecification, err)
            raise
        
        filename = str(options.Filename.SelectedFile())
        
        try:
            filename = str(options.Filename.SelectedFile())
            if FUploadEngine.IsValidForReconciliation(filename, forceReRun):
                engine = FUploadEngine(filename, reconSpec, options) 
                uploadInstance = engine.Run()
                if uploadInstance:
                    logger.info('Processed and stored %d item(s) for this document', uploadInstance.ReconciliationDocument().ProcessedItemCount())
                    if displayOperationsManager:
                        logger.debug('Displaying loaded reconciliation items in Operations Manager')
                        FReconciliationWorkbench.StartApplication(uploadInstance.ReconciliationDocument(), reconSpec, upload = True)
        except ValueError as err:
            logger.error('Failed to load reconciliation specification "%s": %s', options.ReconciliationSpecification, err)
        except IOError as err:
            logger.error('Failed to load document "%s": %s', options.Filename.SelectedFile(), err)
        logger.info('Data upload processing completed')
