""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitViewer.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitViewer

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    The Trading Manager limit viewer docked-in panel.

-----------------------------------------------------------------------------"""
import itertools

import acm
import FUxCore
import FLimitSettings
import FLimitUtils
from FLimitTreeSpecification import LimitTreeSpecification

LIMIT_UTILITY_VIEW_KEY = 'LimitViewer'


def OnCreateMenuItem(extObj):
    return ViewLimitsMenuItem(extObj)
    
def OnSelectionChanged(eii, _rest):
    frame = eii.ExtensionObject()
    activeSheet = frame.ActiveSheet()
    if activeSheet and FLimitUtils.IsSupportedSheetClass(activeSheet.SheetClass()):
        UpdateLimitUtilityView(frame)

def CreateLimitUtilityView(frame):
    # pylint: disable-msg=E1101
    sheet = frame.ShowBuiltInUtilityView(LIMIT_UTILITY_VIEW_KEY)
    assert(sheet)
    context = acm.GetDefaultContext()
    defaultColumns = acm.GetColumnCreators(FLimitSettings.DefaultDisplayColumns(), context)
    columns = sheet.ColumnCreators()
    columns.Clear()
    for i in range(defaultColumns.Size()):
        columns.Add(defaultColumns.At(i))
    UpdateLimitUtilityView(frame)

def IsLimitUtilityViewVisible(frame):
    # Guard against crash getting a utility view that has been created and later closed (SPR 348156)
    try:
        if not frame.IsDockWindowVisible(LIMIT_UTILITY_VIEW_KEY):
            return False
    except RuntimeError:
        return False
    return bool(frame.GetUtilityView(LIMIT_UTILITY_VIEW_KEY))

def UpdateLimitUtilityView(frame):
    if not IsLimitUtilityViewVisible(frame):
        return
    limitSheet = frame.GetUtilityView(LIMIT_UTILITY_VIEW_KEY)
    if limitSheet:
        limits = []
        activeSheet = frame.ActiveSheet()
        activeSheetClass = activeSheet.SheetClass()
        if FLimitUtils.IsSupportedSheetClass(activeSheetClass):
            limits = _GetLimits(activeSheet.Selection().SelectedCells())
        if activeSheetClass != acm.FLimitSheet:
            _DisplayLimits(limitSheet, limits)

def _DisplayLimits(sheet, limits):
    assert(sheet.SheetClass() == acm.FLimitSheet)
    if set(limits) == set(sheet.GetAllOfType(acm.FLimit)):
        return
    sheet.RemoveAllRows()
    limitOriginObject = lambda l: FLimitUtils.OriginObjectName(l)   # pylint: disable-msg=W0108
    for originObject, limits in itertools.groupby(limits, limitOriginObject):
        folder = _GetLimitsAsFolder(originObject, limits)
        sheet.InsertObject(folder, 'IOAP_LAST')
    sheet.RowTreeIterator(0).Tree().Expand(True, 1000)

def _GetLimits(selectedCells):
    supportedCells = [cell for cell in selectedCells if FLimitUtils.IsSupportedCell(cell)]
    treeSpecs = _RemoveDuplicatesFromList((
        LimitTreeSpecification(cell).TreeSpecification()
        for cell in supportedCells))
    limits = itertools.chain.from_iterable((acm.Limits.FindByTreeSpecification(ts) for ts in treeSpecs))
    return _RemoveDuplicatesFromList(limits)

def _GetLimitsAsFolder(label, limits):
    folder = acm.FASQLQueryFolder()
    folder.Name(label)
    query = acm.CreateFASQLQuery('FLimit', 'OR')
    for limit in limits:
        query.AddOpNode('OR')
        query.AddAttrNode('Oid', 'EQUAL', limit.Oid())
    folder.AsqlQuery(query)
    return folder

def _RemoveDuplicatesFromList(orderedList):
    # Remove duplicate and null elements whilst maintaining list order
    seen = set()
    return [i for i in orderedList if i and i not in seen and not seen.add(i)]


class ViewLimitsMenuItem(FUxCore.MenuItem):
    
    def __init__(self, extObj):
        self._frame = extObj

    def Applicable(self):
        try:
            if not self._frame.IsKindOf(acm.FManagerBaseFrame):
                raise AttributeError('CreateUtilityView')
            activeSheet = FLimitUtils.ActiveSheet(self._frame)
            if activeSheet:
                return FLimitUtils.IsSupportedSheetClass(activeSheet.SheetClass())
            return True
        except AttributeError:
            return False

    def Invoke(self, _eii):
        if IsLimitUtilityViewVisible(self._frame):
            self._frame.ShowDockWindow(LIMIT_UTILITY_VIEW_KEY, False)
        else:
            CreateLimitUtilityView(self._frame)
        
    def Checked(self):
        return IsLimitUtilityViewVisible(self._frame)
