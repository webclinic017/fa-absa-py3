""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FReconciliationColumns.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationColumns

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FUxCore

import FReconciliationIdentification
from FReconciliationValueMapping import GetCalculationParamsColumnId, GetCalculator, GetSheetInsertableACMObject
from FReconciliationSpecification import GetReconciliationSpecification, FReconciliationSpecification
from FReconciliationContainer import FReconciliationInstance
from FReconciliationGUI import ReconciliationPositionRetriever


def GetStateChartFromDocument(reconDoc):
    return FReconciliationSpecification(reconDoc).StateChart()

def GetReconciliationItemFromRowObject(rowObject):
    if rowObject.IsKindOf(acm.FBusinessProcess):
        subject = rowObject.Subject()
        if subject.IsKindOf(acm.FReconciliationItem):
            return subject
    elif rowObject.IsKindOf(acm.FTradeRow):
        subject = rowObject.OriginalSourceObject()
        reconciliationItems = acm.ReconciliationItem.FindBySubject(subject)
        if reconciliationItems:
            # Assume we are working with the latest reconciliation item
            return reconciliationItems.SortByProperty('CreateTime')[-1]
    elif rowObject.IsKindOf(acm.FInstrumentAndTrades):
        ''' Position objects - stored as ASQL queries - change type when inserted in to
            the sheet such that the reconciliation item cannot be located based on its subject.
            Instead, use the portfolio naming convention to locate the corresponding
            reconciliation item manually.
         '''
        oid = int(rowObject.Portfolio().Name()[len('Reconciliation Item_'):])
        return acm.FReconciliationItem[oid]
    else:
        subject = rowObject
        reconciliationItems = acm.ReconciliationItem.FindBySubject(subject)
        if reconciliationItems:
            # Assume we are working with the latest reconciliation item
            return reconciliationItems.SortByProperty('CreateTime')[-1]
    return None

def GetAttributeFromExternalValues(rowObject, attribute):
    value = None
    reconciliationItem = GetReconciliationItemFromRowObject(rowObject)
    externalValues = reconciliationItem.ExternalValues()
    if externalValues:
        value = externalValues.At(attribute)
    return value

def GetCalculationParams(reconDocument):
    keys = GetCalculationParamsColumnId().keys()
    return dict((key, getattr(reconDocument, key)()) for key in keys)

def GetAttributeFromCalcSpace(rowObject, sheetType, columnId):
    reconItem = rowObject.Subject()
    itemSubject = reconItem.Subject()
    reconSpec = GetReconciliationSpecification(reconItem, upload=False, relaxValidation=True)
    if not itemSubject:
        # Case: Position reconciliation - retrieve item subject
        positionRetriever = ReconciliationPositionRetriever(reconItem,
                                                            reconSpec,
                                                            allowIncompletePositions=True)
        itemSubject = positionRetriever.RetrieveDynamicStoredPositionQuery()
        reconItem.Subject(itemSubject)
    if itemSubject:
        reconInstance = FReconciliationInstance(reconSpec)
        reconDocument = reconItem.ReconciliationDocument()
        reconInstance.ReconciliationDocument(reconDocument)
        calculationParams = GetCalculationParams(reconDocument)
        reconInstance.CalculationParams(calculationParams)
        calculator = GetCalculator(reconInstance, sheetType)
        insertableObject = GetSheetInsertableACMObject(
                itemSubject, reconSpec.IsFXReconciliation(), reconItem)
        calculator.InsertItem(insertableObject)
        return calculator.CalculateValue(columnId)
    return None

def ReconciliationItemReport(eii):
    for reconItem in eii.ExtensionObject():
        if reconItem.IsKindOf(acm.FReconciliationItem):
            FReconciliationIdentification.PrintIdentificationReport(reconItem)

def CreateReconciliationItemReportMenuItem(extObj):
    return ReconciliationItemReportMenuItem(extObj)

class ReconciliationItemReportMenuItem(FUxCore.MenuItem):

    def __init__(self, mgrFrame):
        self._mgrFrame = mgrFrame
        self._reconItems = self._ReconciliationItems()

    def Invoke(self, _eii):
        for reconItem in self._reconItems:
            FReconciliationIdentification.PrintIdentificationReport(reconItem)

    def Applicable(self):
        return bool(self._reconItems)

    def _ReconciliationItems(self):
        reconItems = []
        if self._mgrFrame and self._mgrFrame.IsKindOf(acm.FBackOfficeManagerFrame):
            for rowObject in self._mgrFrame.ActiveSheet().Selection().SelectedRowObjects():
                if rowObject.IsKindOf(acm.FBusinessProcess):
                    subject = rowObject.Subject()
                    if subject and subject.IsKindOf(acm.FReconciliationItem):
                        reconItems.append(subject)
        return reconItems

def HasNotes(bp):
    return bool(bp.Diary().GetEntry(bp, bp.CurrentStep()).Notes().Size() > 0)

def NewDiaryBusinessProcessPair(bp):
    pair = acm.FPair()
    pair.First(bp.Diary())
    pair.Second(bp)
    return pair

def LastUpdatedDiaryAndProcess(businessProcesses, diariesSorted):
    diariesAndProcesses = dict(list(zip((b.Diary() for b in businessProcesses), businessProcesses)))
    for diary in diariesSorted:
        bp = diariesAndProcesses[diary]
        if HasNotes(bp):
            return NewDiaryBusinessProcessPair(bp)