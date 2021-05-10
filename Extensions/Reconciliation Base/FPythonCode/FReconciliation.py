""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FReconciliation.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliation

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import FReconciliationDialog
from FReconciliationEngine import FReconciliationEngine
import FReconciliationSpecification
import FReconciliationWorkbench
import FAssetManagementUtils
from datetime import datetime

logger = FAssetManagementUtils.GetLogger()

ael_variables = FReconciliationDialog.ReconciliationDialog('Reconciliation')
ael_variables.LoadDefaultValues(__name__)
ael_gui_parameters = ael_variables.GUIParams()


def ael_main(params):
    options = FReconciliationDialog.ReconciliationDialog.getParameters(params)
    reconInstance = RunReconciliation(options)
    return reconInstance

def setDateFormats(fileName, utc):
    directives = ('%%', '%a', '%A', '%w', 
                  '%b', '%B', '%m', '%y', 
                  '%Y', '%H', '%I', '%p', 
                  '%M', '%S', '%f', '%z', 
                  '%Z', '%j', '%U', '%W', 
                  '%c', '%x', '%X', '%d')
    now = datetime.utcnow() if utc is True else datetime.now()
    for d in directives:
        fileName = fileName.replace(d, now.strftime(d))
    return fileName

def RunReconciliation(options):
    logger.info('Initiating reconciliation processing...')
    FAssetManagementUtils.ReinitializeLogger(FReconciliationDialog.ReconciliationDialog.LOG_LEVELS[options.LogLevel])
    if options.Filename:
        forceReRun = (options.ForceReRun == '1')
        displayOperationsManager = (options.DisplayOption == '1')
        try:
            reconSpec = FReconciliationSpecification.FReconciliationSpecification(options.ReconciliationSpecification)
            fileName = str(options.Filename if isinstance(options.Filename, str) else options.Filename.SelectedFile())
            if options.FormatDateTime:
                fileName = setDateFormats(fileName, options.FormatDateTimeUTC)
            logger.info('Processing document: %s', fileName)
            reconInstance = None
            if FReconciliationEngine.IsValidForReconciliation(fileName, forceReRun):
                engine = FReconciliationEngine(fileName, reconSpec, options) 
                reconInstance = engine.Run()
                if reconInstance:
                    logger.info('Processed %d item(s) for this document', reconInstance.ReconciliationDocument().ProcessedItemCount())
                    if displayOperationsManager:
                        logger.debug('Displaying loaded reconciliation items in Operations Manager')
                        if not reconInstance.NbrOfReconciliationItems():
                            logger.info('There are no reconciliation items to display. A total of %i successfully reconciled items have been removed.' % 
                                        reconInstance.NbrOfRemovedClosedItems())
                        FReconciliationWorkbench.StartApplication(reconInstance.ReconciliationDocument(), reconSpec, upload = False)
                    return reconInstance
            logger.info('Reconciliation processing completed')
        except ValueError as error:
            logger.error('Failed to load reconciliation specification "%s": %s', \
                    options.ReconciliationSpecification, error)
        except IOError as error:
            logger.error('Failed to load file "%s": %s', fileName, error)
        finally:
            # Avoid further logging in the Operations Manager workbench
            logger.Reinitialize(level=4)