""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FFilteredWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFilteredWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


from collections import defaultdict
from FWorkbookPanel import WorkbookPanel


class FilteredWorkbookPanel(WorkbookPanel):

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

    def InsertObjects(self, sourceObjects=None):
        if sourceObjects is not None:
            self._sourceObjects = sorted(sourceObjects, key=self.SortingKey)
        self.Sheet().InsertObject(self._sourceObjects, pos='IOAP_REPLACE')

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
        self.ClearFilter()
        self.InsertObjects()

    def OnFilterRefreshed(self, event):
        self.InsertObjects()

    def FilterColumnsDict(self):
        return dict((c.Attribute().ColumnId(), True)
                for c in self.Filter().Comparator().GetComparators())

    def ObjectsAndValues(self):
        self._output = defaultdict(dict)
        self._filterColumnsDict = self.FilterColumnsDict()
        self._filterColumnsSize = len(self._filterColumnsDict)
        rowIter = self.Sheet().RowTreeIterator(0).FirstChild()
        while rowIter:
            sourceObject = self.SourceObject(rowIter.Tree().Item())
            if sourceObject:
                self.CollectCellValues(rowIter, sourceObject)
            rowIter = rowIter.NextSibling()
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

    def DoFilterObjects(self):
        objectsAndValues = self.ObjectsAndValues()
        filteredValues = self.Filter().FilterValues(objectsAndValues)
        if len(filteredValues) != len(objectsAndValues):
            filteredValues.sort(key=self.SortingKey)
            self.Sheet().InsertObject(filteredValues, 'IOAP_REPLACE')

    def OnHandleOnIdle(self, *args):
        if self.Filter():
            self.DoFilterObjects()

    def SourceObject(self, rowObject):
        pass
