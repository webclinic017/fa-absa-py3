""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceSemanticListHandler.py"
from __future__ import print_function
import operator
import acm

class FPriceSemanticListHandler(object):
    def __init__(self, listControl):
        self.semanticList = listControl
        self.rowsModified = 0

    def Initialize(self):
        """Initialize Price link definition Grid"""
        self.semanticList.EnableMultiSelect()
        self.semanticList.ShowGridLines()
        self.semanticList.ShowColumnHeaders()
        self.semanticList.EnableHeaderSorting()

        self.semanticList.AddColumn(' ', -1, "Status")
        self.semanticList.AddColumn('ADM Field', -1, "ADM Field name to which the IDP field will be mapped")
        self.semanticList.AddColumn('IDP Field', -1, "Field from Reuters/Bloomberg/MarketMap")
        self.semanticList.AddColumn('Field Comment', -1, "Comments about the IDP Field")
        
        for count in range(0, self.semanticList.ColumnCount()):
            self.semanticList.AdjustColumnWidthToFitItems(count)
        

    def SelectAllItems(self, value):
        self.semanticList.SelectAllItems(value)

    def _Sort(self, rows, sortBy = 'ADM Field   ', descending = False):
        #                       0            1            2
        #row structure is ['ADM Field', 'IDP Field', 'Field Comment']
        sortPriority = {
            'ADM Field   ': (0, 1, 2),
            'IDP Field   ': (1, 0, 2),
            'Field Comment': (2, 0, 1),
            }

        return sorted(rows, key=operator.itemgetter(*sortPriority[sortBy]), reverse=descending)

    def Sort(self, sortBy, descending):
        rows = self.GetRows()
        sortedRows = self._Sort(rows, sortBy, descending)
        self.semanticList.Clear()
        self._Populate(sortedRows)

    def GetRows(self):
        rows = []
        root = self.semanticList.GetRootItem()
        for child in root.Children():
            rows.append(child.GetData())
        return rows

    def _Populate(self, rows):
        rootItem = self.semanticList.GetRootItem()
        for aRow in rows:
            child = rootItem.AddChild()
            for index, item in enumerate(aRow):
                child.Label(item, index)
            child.SetData(aRow)

    def Populate(self, semanticList, newPriceSemanticName):
        rows = self.MakeRows(semanticList)
        selectedFieldMappings = self.GetSelectedfieldMappings()
        self.semanticList.Clear()
        if selectedFieldMappings:
            for fieldMapping in selectedFieldMappings:
                row = acm.FPriceSemanticRow()
                row.SemanticSeqNbr(newPriceSemanticName)
                row.AdmName(fieldMapping.AdmName())
                row.IdpName(fieldMapping.IdpName())
                row.Comment(fieldMapping.Comment())
                self.Add(row)
                
        sortedRows = self._Sort(rows)        
        self._Populate(sortedRows)
        self.AdjustColumnWidth()
        self.rowsModified = 0

    def AdjustColumnWidth(self):
        for i in [0, 1, 2]:
            self.semanticList.AdjustColumnWidthToFitItems(i)

    def MakeRows(self, semanticList):
        rows = []
        status = ''
        for fieldMapping in semanticList:
            aRow = self.MakeRow(fieldMapping, status)
            rows.append(aRow)
        return rows

    def MakeRow(self, fieldMapping, status):
        row = (status, fieldMapping.AdmName(), fieldMapping.IdpName(), fieldMapping.Comment(), fieldMapping)
        return row

    def Update(self, status, fieldMapping, child):
        row = self.MakeRow(fieldMapping, status)
        for index, item in enumerate(row):
            child.Label(item, index)
        child.SetData(row)
        self.AdjustColumnWidth()
        if status:
            self.rowsModified += 1

    def Add(self, fieldMapping):
        rootItem = self.semanticList.GetRootItem()
        newRow = rootItem.AddChild()
        self.Update('A', fieldMapping, newRow)
        newRow.Select()
        newRow.EnsureVisible()
        self.AdjustColumnWidth()

    def RevertAll(self):
        root = self.semanticList.GetRootItem()
        for child in root.Children():
            self._Revert(child)
        self.rowsModified = 0

    def Revert(self):
        rows = self.GetSelectedRows()
        for aRow in rows:
            if self.IsModified(aRow):
                self._Revert(aRow)
                self.rowsModified -= 1

    def _Revert(self, row):
        opType = self.GetOperationType(row)
        if opType in ('U', 'R'):
            fieldMapping = self.GetfieldMappingObject(row)
            originalfieldMapping = self.GetOriginalfieldMappingObject(fieldMapping)
            self.Update('', originalfieldMapping, row)

        elif opType == 'A':
            self.semanticList.SelectAllItems(False)
            row.Select()
            self.semanticList.RemoveAllSelectedItems(True)

    def Remove(self):
        rows = self.GetSelectedRows()
        for aRow in rows:
            opType = self.GetOperationType(aRow)
            if opType == 'A':
                continue
            fieldMapping = self.GetfieldMappingObject(aRow)
            self.Update('R', fieldMapping, aRow)

    def SaveAll(self):
        root = self.semanticList.GetRootItem()
        for child in root.Children():
            self._Save(child)
        self.rowsModified = 0

    def Save(self):
        rows = self.GetSelectedRows()
        for aRow in rows:
            if self.IsModified(aRow):
                self._Save(aRow)
                self.rowsModified -= 1

    def _Save(self, row):
        opType = self.GetOperationType(row)
        fieldMapping = self.GetfieldMappingObject(row)

        if opType == 'R':
            self._Delete(fieldMapping, row)

        elif opType == 'U':
            originalfieldMapping = self.GetOriginalfieldMappingObject(fieldMapping)
            originalfieldMapping.Apply(fieldMapping)
            self.Commit(originalfieldMapping, row)

        elif opType == 'A':
            self.Commit(fieldMapping, row)

    def _Delete(self, fieldMapping, row):
        try:
            self.semanticList.SelectAllItems(False)
            row.Select()
            originalfieldMapping = self.GetOriginalfieldMappingObject(fieldMapping)
            originalfieldMapping.Delete()
            self.semanticList.RemoveAllSelectedItems(True)
        except RuntimeError as e:
            print("Failed to delete PriceSemanticRow '%s'. Refer Prime log for details." % fieldMapping.Oid())

    def Commit(self, fieldMapping, row):
        try:
            fieldMapping.Commit()
            status = ''
            self.Update(status, fieldMapping,  row)
        except RuntimeError as e:
            print("Failed to save PriceSemanticRow '%s'. Refer Prime log for details." % fieldMapping.Oid())
            print(str(e))

    def HandleServerUpdate(self, param):
        matched = False
        root = self.semanticList.GetRootItem()
        for child in root.Children():
            fieldMapping = self.GetfieldMappingObject(child)
            if fieldMapping.Oid() == param.Oid():
                self.Update('', fieldMapping, child)
                matched = True
                break

        if matched == False:
            rootItem = self.semanticList.GetRootItem()
            newRow = rootItem.AddChild()
            self.Update('', param, newRow)

    def HandleServerRemove(self, param):
        root = self.semanticList.GetRootItem()
        for child in root.Children():
            fieldMapping = self.GetfieldMappingObject(child)
            if fieldMapping.Oid() == param.Oid():
                child.Remove()
                break

    def GetSelectedRow(self):
        return self.semanticList.GetSelectedItem()

    def GetSelectedRows(self):
        return self.semanticList.GetSelectedItems()

    def GetSelectedfieldMappings(self):
        selectedfieldMappings = []
        for row in self.GetSelectedRows():
            fieldMapping = self.GetfieldMappingObject(row)
            selectedfieldMappings.append(fieldMapping)
        return selectedfieldMappings

    def GetSelectedfieldMapping(self):
        row = self.GetSelectedRow()
        return self.GetfieldMappingObject(row)

    def GetfieldMappingObject(self, row):
        data = row.GetData()
        return data[4]
        
    def GetSelectedSemantics(self):
        selectedSemantics = []
        for row in self.GetSelectedRows():
            sem = self.GetSemanticObject(row)
            selectedSemantics.append(sem)
        return selectedSemantics

    def GetSelectedSemantic(self):
        retVal = None
        row = self.GetSelectedRow()
        if row != None:
            retVal = self.GetSemanticObject(row)
        return retVal

    def GetSemanticObject(self, row):
        data = row.GetData()
        return data[self.semanticList.ColumnCount()]

    def GetOriginalfieldMappingObject(self, fieldMapping):
        return acm.FPriceSemanticRow[fieldMapping.Oid()]

    def GetOperationType(self, row):
        data = row.GetData()
        return data[0]

    def IsMultiSelect(self):
        return self.semanticList.SelectedCount() > 1

    def IsModified(self, row):
        opType = self.GetOperationType(row)
        if opType in ('U', 'R', 'A'):
            return True
        return False