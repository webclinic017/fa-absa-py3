""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FReconciliationWorkbench.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationWorkbench

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved. 

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FBusinessProcessUtils
import FOperationsManagerWorkbench
import FReconciliationColumnCreator
import FReconciliationSpecification
import FReconciliationGUI
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


def OnCreate(eii):
    """Callback from OperationsManager frame for workbench creation."""
    eii.ExtensionObject().CreateCustomDockWindow(
        FReconciliationGUI.ReconciliationWorkflowPanel(), 
        'ReconciliationWorkflowPanel', 'Reconciliation Workflow', 'Right', '', False, False)
    eii.ExtensionObject().CreateCustomDockWindow(
        FReconciliationGUI.ReconciliationItemPanel(), 
        'ReconciliationItemPanel', 'Reconciliation Item Details', 'Bottom', '', False, False)

def OnSelectionChanged(eii, _rest):
    """Callback from OperationsManager frame when selection on sheet is changed."""
    FOperationsManagerWorkbench.OnBusinessProcessPanelSelectionChanged(eii,
        [('ReconciliationWorkflowPanel', FReconciliationGUI.ReconciliationWorkflowPanel), 
         ('ReconciliationItemPanel', FReconciliationGUI.ReconciliationItemPanel)])

def StartApplication(reconDocument, reconSpecification=None, upload = False):
    """Start a reconciliation workbench for the passed reconciliation document.

    This function will start the Operations Manager application, initialise all
    reconciliation workbench panels and add the reconciliation document to the sheet
    for further processing and management.

    """

    logger.info('Launching Operations Manager...')
    eventClosed = None
    try:
        import FReconciliationWorkflow
    except:
        pass
    else:
        eventClosed = FReconciliationWorkflow.FReconciliationWorkflow.EVENT_CLOSED
    
    try:
        import FUploadWorkflow
    except:
        pass
    else:
        eventClosed = FUploadWorkflow.FUploadWorkflow.EVENT_CLOSED
    
    if not reconSpecification:
        try:
            reconItem = reconDocument.ReconciliationItems()[0]
            reconSpecification = FReconciliationSpecification.GetReconciliationSpecification(reconItem, upload)
        except IndexError:
            raise ValueError('Could not load reconciliation specification for document "%s"' % reconDocument.StringKey())
    sheetTemplate = None
    try:
        sheetTemplate = reconSpecification.BusinessProcessSheetTemplate()
        assert(sheetTemplate)
    except AssertionError:
        name = reconSpecification.BusinessProcessSheetTemplateName()
        if name:
            logger.error('Failed to load business process sheet template "%s"' % name)

    additionalColumns = _GetAdditionalColumnIds(reconSpecification) if not sheetTemplate else [] 
    FOperationsManagerWorkbench.StartOperationsManagerWorkbench(
            defaultObjects=[_GetSheetInsertableReconciliationDocument(reconDocument, reconSpecification), ],
            sheetTemplate=sheetTemplate,
            additionalColumnIds=additionalColumns,
            grouperName='Current State',
            expandAllRows=True,
            expandedRowFilter=[eventClosed, ])

def _GetExternalValueColumnIds(reconSpecification):
    columnMap = reconSpecification.DataTypeMapping()
    columnNamespace = reconSpecification.Name()
    return [FReconciliationColumnCreator.MakeColumnId(col, columnNamespace) for 
            col in sorted(columnMap.Keys())]

def _GetAdditionalColumnIds(reconSpecification):
    columns = FReconciliationGUI.GetComparisonColumnIds(reconSpecification)
    columns.extend(_GetExternalValueColumnIds(reconSpecification))
    columnExtensions = FReconciliationColumnCreator.ColumnExtensions('businessprocesssheet')
    return [c for c in columns if c in columnExtensions]

def _GetSheetInsertableReconciliationDocument(reconDocument, reconSpecification):
    ''' Until the BP sheet supports direct insertion of FReconciliationDocuments (properly), 
        insert the recon document as a query of the contained business processes
    '''
    queryFolder = acm.FASQLQueryFolder()
    queryFolder.Name(reconSpecification.Name())
    query = acm.CreateFASQLQuery('FBusinessProcess', 'OR')
    
    for reconciliationItem in reconDocument.ReconciliationItems():
        bp = FBusinessProcessUtils.GetBusinessProcessWithCache(reconciliationItem, reconSpecification.StateChartName())
        if bp:
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', bp.Oid())
    if not reconDocument.ReconciliationItems():
        query.AddAttrNode('Oid', 'EQUAL', 0)    
        
    queryFolder.AsqlQuery(query)
    return queryFolder
