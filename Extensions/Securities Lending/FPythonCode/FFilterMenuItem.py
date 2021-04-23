""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FFilterMenuItem.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFilterMenuItem

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import traceback
import FFilter
import FEvent
from collections import namedtuple
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FSecLendEvents import OnFilterCreated, OnFilterCleared, OnFilterActive, OnFilterRefreshed
from FSecLendUtils import logger
import FSheetFilterApplication

def ActiveSheet(eii):
    extObj = eii.ExtensionObject()
    if extObj.IsKindOf(acm.FUiTrdMgrFrame):
        return extObj.ActiveSheet()


def ColumnIds(eii):
    try:
        creators = ActiveSheet(eii).ColumnCreators()
        return [creators.At(i).ColumnId() for i in range(creators.Size())]
    except AttributeError:
        return []

class FFilterMenuItem(IntegratedWorkbenchMenuItem):
    DEFAULT_COMPARATOR = FFilter.FBetweenOperator().OperatorSymbol()
    DEFAULT_OPERATOR = FFilter.FAndOperator().OperatorSymbol()

    def __init__(self, extObj):
        super(FFilterMenuItem, self).__init__(extObj, view='SecLendPortfolioView')

    def SendEvent(self, event):
        self._Dispatcher().Update(event)

    def ApplicableOnNoWorkbench(self):
        return False

    def ActiveFilter(self):
        try:
            return self.CurrentActiveFilter().ActiveFilter()
        except Exception:
            return None

    def Filter(self):
        try:
            return self.CurrentActiveFilter().Filter()
        except Exception:
            return None

    def Invoke(self, eii):
        try:
            self.SendEvent(self.CreateEvent(eii))
        except Exception:
            pass

    def CreateEvent(self, _eii):
        raise NotImplementedError

    def IsSecLendPortfolioView(self):
        return bool(self.View().Name() == 'SecLendPortfolioView')

    def CurrentActiveFilter(self):
        try:
            return self._Handler("CurrentActiveWatchlistFilter")
        except Exception:
            return None

class FCreateFilterMenuItem(FFilterMenuItem):

    CONTROLS = ['attr', 'comparisonOp', 'minValue', 'maxValue', 'logicalOp']

    def __init__(self, extObj):
        FFilterMenuItem.__init__(self, extObj)
        self.Comparator = namedtuple('Comparator', self.CONTROLS)

    def InputValues(self):
        if self.Filter():
            return self.FilterDlgInputValues()
        return self.DefaultDlgInputValues()

    def CreateEvent(self, eii):
        try:
            columnIds = ColumnIds(eii)
            content = [self.InputValues(), columnIds, self]
            FSheetFilterApplication.StartFilterApplicationModal(content)
        except Exception as e:
            logger.error('CreateFilterMenuItem.CreateEvent: {}'.format(traceback.format_exc()))

    def DoSendEvent(self, dlgOutput):
        # Comparator
        if dlgOutput:
            eventFilter = FFilter.FFilter.CreateFromComparator(
                *FFilter.FFilter.ComparatorParts(dlgOutput))
            self.SendEvent(FEvent.CreateEvent('OnWatchlistFilterCreated', OnFilterCreated, self, eventFilter))

    def UniqueColumnIds(self):
        return set(c.Column().ColumnId()
                   for c in self._frame.ActiveSheet().Selection().SelectedCells()
                   if c.Column().ColumnId())

    def DefaultDlgInputValues(self):
        try:
            return (self.Comparator(
                columnId,
                self.DEFAULT_COMPARATOR,
                '',
                '',
                self.DEFAULT_OPERATOR
            )
                    for columnId in self.UniqueColumnIds())
        except AttributeError:
            pass
        return ()

    def FilterDlgInputValues(self):
        try:
            activeFilter = self.Filter()
            if activeFilter:
                return (self.Comparator(
                    acm.FSymbol(cmp.Attribute().ColumnId()),
                    cmp.OperatorSymbol(),
                    cmp.LeftValue(),
                    self.RightValue(cmp),
                    acm.FSymbol(op)
                )
                        for cmp, op in self.Pairwise(activeFilter.Comparator().Arguments()))
        except AttributeError:
            pass
        return ()

    def Checked(self):
        return bool(self.Filter())

    @staticmethod
    def Pairwise(iterable):
        for i in range(0, len(iterable), 2):
            try:
                yield iterable[i], iterable[i + 1]
            except IndexError:
                yield iterable[i], None

    @staticmethod
    def RightValue(cmpr):
        if cmpr.OperatorSymbol().Text() != 'BETWEEN':
            return cmpr.RightValue() or cmpr.LeftValue()
        return cmpr.RightValue()

class FClearFilterMenuItem(FFilterMenuItem):
    def CreateEvent(self, eii):
        return FEvent.CreateEvent('OnWatchlistFilterCleared', OnFilterCleared, self)

    def Enabled(self):
        return bool(self.Filter())

class FApplyFilterMenuItem(FFilterMenuItem):

    def CreateEvent(self, eii):
        if self.CurrentActiveFilter().Filter():
            active = not self.CurrentActiveFilter().FilterActive()
            return FEvent.CreateEvent('OnWatchlistFilterActive', OnFilterActive, self, active)
        else:
            try:
                createFilter = FCreateFilterMenuItem(eii.ExtensionObject())
                createFilter.Invoke(eii)
            except Exception:
                pass

    def Checked(self):
        """Should the menu item be checked for this extension object?
           Return True if it should be checked otherwise return False"""
        if self.CurrentActiveFilter():
            return self.CurrentActiveFilter().FilterActive()
        else:
            return False

    def Enabled(self):
        return bool(self.Filter())

class FRefreshFilterMenuItem(FFilterMenuItem):
    def CreateEvent(self, eii):
        return FEvent.CreateEvent('OnWatchlistFilterRefreshed', OnFilterRefreshed, self)

    def Enabled(self):
        return bool(self.Filter())

def CreateFilterMenuItem(eii):
    return FCreateFilterMenuItem(eii)

def ClearFilterMenuItem(eii):
    return FClearFilterMenuItem(eii)

def RefreshFilterMenuItem(eii):
    return FRefreshFilterMenuItem(eii)

def ApplyFilterMenuItem(eii):
    return FApplyFilterMenuItem(eii)