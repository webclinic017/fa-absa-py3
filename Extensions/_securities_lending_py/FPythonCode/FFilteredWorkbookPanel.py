""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FFilteredWorkbookPanel.py"
from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFilteredWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
from collections import defaultdict
import traceback
from FSecLendCommon import WorkbenchSheet
from FWorkbookPanel import WorkbookPanel
import FGrouperUtils
import acm

class FilteredWorkbookPanel(WorkbookPanel):

    ON_IDLE_FREQ = 0.5

    def __init__(self, application):
        super(FilteredWorkbookPanel, self).__init__(application)
        self._filterColumnsDict = None
        self._filterColumnsSize = None
        self._output = None
        self._sourceObjects = None
        self._filter = None
    def Filter(self, _filter=None):
        if _filter is None:
            return self._filter
        self._filter = _filter

    def ClearFilter(self):
        self._filter = None

    def HasFilterChanged(self, _filter):
        return bool(self.Filter() != _filter)

    def SourceObjects(self, _sourceObjects=None):
        if _sourceObjects is None:
            return self._sourceObjects
        #self._sourceObjects = sorted(_sourceObjects, key=self.SortingKey)
        return self._sourceObjects


    def ApplyGrouperInstanceToSheet(self, sheet, grouper):
        """ Apply grouper to sheet. """
        iterator = sheet.RowTreeIterator(True)
        while iterator.NextUsingDepthFirst():
            if iterator.Tree():
                try:
                    iterator.Tree().ApplyGrouper(grouper)
                except StandardError as stderr:
                    print("Error")

    def createContainer(self, trades, sheet_settings=None):
        adhoc = acm.FAdhocPortfolio()
        adhoc.Name("Filtered Securities")
        for trade in trades:
            adhoc.Add(trade)
        return adhoc

    def InsertObjects(self, sourceObjects=None, sheet_settings=None):
        sourceObjects = sourceObjects if sourceObjects else self.SourceObjects()
        if sheet_settings and sheet_settings.Grouper() and sheet_settings.SheetType():
            grouper = FGrouperUtils.GetGrouper(sheet_settings.Grouper(), sheet_settings.SheetType())
            self.Sheet().LastGrouper(grouper)
        self.Sheet().InsertObject(sourceObjects, pos='IOAP_REPLACE')
        if sheet_settings and sheet_settings.ExpandTreeLevels():
            self.Sheet().ExpandTree(sheet_settings.ExpandTreeLevels())

    @staticmethod
    def SortingKey(obj):
        return obj

    def OnFilterChanged(self, event):
        if self.Filter() is None:
            self.Filter(event.Filter())
        elif self.HasFilterChanged(event.Filter()):
            self.Filter(event.Filter())
            self.InsertObjects()

    def OnFilterRemoved(self, event):
        """ Remove filter, initialize content and update the filter source """
        self.ClearFilter()
        self.InsertObjects()

    def OnFilterRefreshed(self, event):
        self.InsertObjects()

    def FilterColumnsDict(self):
        return dict((c.Attribute().ColumnId(), True)
                for c in self.Filter().Comparator().GetComparators())

    def ObjectsAndValues(self):
        """Objects currently in the sheet"""
        self._output = defaultdict(dict)
        self._filterColumnsDict = self.FilterColumnsDict()
        self._filterColumnsSize = len(self._filterColumnsDict)
        rowIter = self.Sheet().RowTreeIterator(True).FirstChild()
        while rowIter.NextUsingDepthFirst():
            sourceObject = self.SourceObject(rowIter.Tree().Item())
            if sourceObject:
                self.CollectCellValues(rowIter, sourceObject)
        return self._output

    def CollectCellValues(self, rowIter, sourceObject):
        columnsFound = 0
        columnIter = self.Sheet().GridColumnIterator().First()
        while columnIter:
            if columnsFound < self._filterColumnsSize:
                columnId = columnIter.GridColumn().ColumnId()
                if self._filterColumnsDict.get(columnId):
                    cell = self.Sheet().GetCell(rowIter, columnIter)
                    self._output[sourceObject][columnId] = cell.FormattedValue()
                    columnsFound += 1
            else: break
            columnIter = columnIter.Next()

    def DoFilterObjects(self, sheet_settings=None):
        objectsAndValues = self.ObjectsAndValues()
        filteredValues = self.Filter().FilterValues(objectsAndValues)
        if len(filteredValues) != len(objectsAndValues):
            #filteredValues.sort(key=self.SortingKey)
            self.InsertObjects(self.createContainer(filteredValues, sheet_settings), sheet_settings)

    def OnHandleOnIdle(self, *args):
        try:
            if self.Filter() and not self.HasFilterBeenApplied():
                self.DoFilterObjects()
                self._appliedFilter = self._filter
        except Exception as e:
            print("Error printing to delete", traceback.format_exc())

    def HandleDestroy(self):
        self.ClearFilter()
        super(FilteredWorkbookPanel, self).HandleDestroy()

    def SourceObject(self, rowObject):
        pass


class FilteredWorkbenchSheet(WorkbenchSheet):

    ON_IDLE_FREQ = 1

    def __init__(self, workbookPanel, settings):
        super(FilteredWorkbenchSheet, self).__init__(workbookPanel, settings)
        self._filterColumnsDict = None
        self._filterColumnsSize = None
        self._output = None
        self._sourceObjects = None
        self._filter = None
        self._appliedFilter = None
        self._onIdleCallback = None

    def HandleCreate(self):
        super(FilteredWorkbenchSheet, self).HandleCreate()
        self.InitOnIdleCallback()

    def InitOnIdleCallback(self):
        if self._onIdleCallback is None:
            self._onIdleCallback = acm.Time.Timer().CreatePeriodicTimerEvent(
                    self.ON_IDLE_FREQ, self.OnHandleOnIdle, None)

    def RemoveOnIdleCallback(self):
        if self._onIdleCallback is not None:
            acm.Time.Timer().RemoveTimerEvent(self._onIdleCallback)
            self._onIdleCallback = None

    def Filter(self, _filter=None):
        if _filter is None:
            return self._filter
        self._filter = _filter

    def ClearFilter(self):
        self._filter = None
        self._appliedFilter = None

    def HasFilterChanged(self, _filter):
        return bool(self.Filter() != _filter)

    def HasFilterBeenApplied(self):
        return bool(self._appliedFilter == self._filter)

    def SourceObjects(self, _sourceObjects=None):
        if _sourceObjects is None:
            return self._sourceObjects
        # self._sourceObjects = sorted(_sourceObjects, key=self.SortingKey)
        return self._sourceObjects

    def createContainer(self, trades):
        adhoc = acm.FAdhocPortfolio()
        adhoc.Name("Filtered Securities")
        for trade in trades:
            adhoc.Add(trade)
        return adhoc

    def GetSheetContents(self):
        contents = []
        settings = self.Settings()
        if settings.Grouper():
            grouper = FGrouperUtils.GetGrouper(settings.Grouper(), settings.SheetType())
            self.Sheet().LastGrouper(grouper)
        if self.ShowSheetContents():
            query = self._InsertItemQuery() or self.DefaultInsertItemQuery()
            if query:
                folder = acm.FASQLQueryFolder()
                folder.Name(self.QueryFolderLabel())
                folder.AsqlQuery(self.ApplyAdditionalQueryFilters(query))
                contents = folder
        return contents if contents else None

    def InsertObjects(self, sourceObjects=None):
        sourceObjects = sourceObjects if sourceObjects else self.SourceObjects()
        if self._settings.Grouper() and self._settings.SheetType():
            grouper = FGrouperUtils.GetGrouper(self._settings.Grouper(), self._settings.SheetType())
            self.Sheet().LastGrouper(grouper)
        self.Sheet().InsertObject(sourceObjects, pos='IOAP_REPLACE')
        if self._settings.ExpandTreeLevels():
            self.Sheet().ExpandTree(self._settings.ExpandTreeLevels())

    @staticmethod
    def SortingKey(obj):
        return obj

    def OnFilterChanged(self, event):
        if self.Filter() is None:
            self.Filter(event.Filter())
        elif self.HasFilterChanged(event.Filter()):
            self.Filter(event.Filter())
            self._SetSheetContents(self.GetSheetContents())

    def OnFilterRemoved(self, event):
        """ Remove filter, initialize content and update the filter source """
        self.ClearFilter()
        self._SetSheetContents(self.GetSheetContents())

    def OnFilterRefreshed(self, event):
        self._appliedFilter = None #activate filter again
        self.Sheet().InsertObject(self.GetSheetContents())

    def FilterColumnsDict(self):
        return dict((c.Attribute().ColumnId(), True)
                    for c in self.Filter().Comparator().GetComparators())

    def CollectCellValues(self, rowIter, sourceObject):
        columnsFound = 0
        columnIter = self.Sheet().GridColumnIterator().First()
        while columnIter:
            if columnsFound < self._filterColumnsSize:
                columnId = columnIter.GridColumn().ColumnId()
                if self._filterColumnsDict.get(columnId):
                    cell = self.Sheet().GetCell(rowIter, columnIter)
                    self._output[sourceObject][columnId] = cell.FormattedValue()
                    columnsFound += 1
            else:
                break
            columnIter = columnIter.Next()

    def ObjectsAndValues(self):
        """Objects currently in the sheet"""
        self._output = defaultdict(dict)
        self._filterColumnsDict = self.FilterColumnsDict()
        self._filterColumnsSize = len(self._filterColumnsDict)
        rowIter = self.Sheet().RowTreeIterator(True).FirstChild()
        while rowIter.NextUsingDepthFirst():
            sourceObject = self.SourceObject(rowIter.Tree().Item())
            if sourceObject:
                self.CollectCellValues(rowIter, sourceObject)
        return self._output

    def DoFilterObjects(self):
        objectsAndValues = self.ObjectsAndValues()
        filteredValues = self.Filter().FilterValues(objectsAndValues)
        if len(filteredValues) != len(objectsAndValues):
            self.InsertObjects(self.createContainer(filteredValues))

    def OnHandleOnIdle(self, *args):
        if self.Filter() and not self.HasFilterBeenApplied():
            self.DoFilterObjects()
            self._appliedFilter = self._filter

    def HandleDestroy(self):
        self.ClearFilter()
        self.RemoveOnIdleCallback()
        super(FilteredWorkbenchSheet, self).HandleDestroy()

    def SourceObject(self, rowObject):
        pass
