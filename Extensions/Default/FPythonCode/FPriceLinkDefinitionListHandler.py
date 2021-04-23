""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkDefinitionListHandler.py"
from __future__ import print_function
import operator
import acm


from FPriceLinkApplicationStates import MandatoryColumns
from FPriceLinkApplicationStates import CurrentColumns
import FPriceLinkSpecificationUtils as Utils

class PriceLinkDefinitionListHandler(object):
    def p1(self, pld):
        return pld.Instrument().Name()

    def p2(self, pld):
        return pld.Instrument().InsType()

    def p3(self, pld):
        return pld.Currency().Name()

    def p4(self, pld):
        market = ""
        if pld.Market():
            market = pld.Market().Name()
        return market

    def p5(self, pld):
        return pld.IdpCode()

    def p6(self, pld):
        return pld.PriceDistributor()

    def p7(self, pld):
        return Utils.NegativeToBlank(pld.UpdateInterval())

    def p8(self, pld):
        return Utils.ZeroToBlank(pld.AdditionAddend())

    def p9(self, pld):
        return Utils.OneToBlank(pld.MultiplicationFactor())

    def p10(self, pld):
        return pld.LastFollowInterval()

    def p11(self, pld):
        return Utils.NoneToBlank(pld.DiscardZeroPrice())

    def p12(self, pld):
        return Utils.NoneToBlank(pld.DiscardZeroQuantity())

    def p13(self, pld):
        return Utils.NoneToBlank(pld.DiscardNegativePrice())

    def p14(self, pld):
        return Utils.NoneToBlank(pld.ForceUpdate())

    def p15(self, pld):
        return pld.ErrorMessage()

    def p16(self, pld):
        return pld.Service()

    def p17(self, pld):
        return pld.SemanticSeqNbr()

    def p18(self, pld):
        startTime = pld.StartTime()
        if Utils.NegativeToBlank(startTime) or Utils.ZeroToBlank(startTime):
            time_hm_start = Utils.IntToTime(startTime)
            return time_hm_start
        else:
            return ""

    def p19(self, pld):
        stopTime = pld.StopTime()
        if Utils.NegativeToBlank(stopTime) or Utils.ZeroToBlank(stopTime):
            time_hm_stop = Utils.IntToTime(stopTime)
            return time_hm_stop
        else:
            return ""

    def p20(self, pld):
        return pld.DonotResetFields()

    def p21(self, pld):
        return pld.XmlData()
        
    def p22(self, pld):
        return Utils.NoneToBlank(pld.IsDelayed())
       
    def p23(self, pld):
        return Utils.NoneToBlank(pld.IgnoreClearPrice())
 
    def __init__(self, listControl):
        self.pldList = listControl
        self.rowsModified = 0
        self.countCol = 0
        self.myDict={
        "Instrument": self.p1,
        "Ins Type": self.p2,
        "Currency": self.p3,
        "Market": self.p4,
        "Market Code(Ticker/RIC/Alpha Code)": self.p5,
        "Price Distributor": self.p6,
        "Update Interval": self.p7,
        "Addition Addend": self.p8,
        "Multiplication Factor": self.p9,
        "Last Follow Interval": self.p10,
        "Discard Zero Price": self.p11,
        "Discard Zero Quantity": self.p12,
        "Discard Negative Price": self.p13,
        "Force Update": self.p14,
        "Error Message": self.p15,
        "Service": self.p16,
        "Semantic": self.p17,
        "Start Time": self.p18,
        "Stop Time": self.p19,
        "Do Not Reset Fields": self.p20,
        "XML Data": self.p21,
        "Is Delayed": self.p22,
        "Ignore Clear Price": self.p23
        }

    def Initialize(self):
        """Initialize Price link definition Grid"""
        self.pldList.EnableMultiSelect()
        self.pldList.ShowGridLines()
        self.pldList.ShowColumnHeaders()

        for column in MandatoryColumns:
            self.pldList.AddColumn(column, -1, column)

        for column in CurrentColumns:
            self.pldList.AddColumn(column, -1, column)

        self.countCol = len(MandatoryColumns) + len(CurrentColumns) + 1
        self.AdjustColumnWidth()






    def SelectAllItems(self, value):
        self.pldList.SelectAllItems(value)

    def _Sort(self, rows, sortBy = 'Instrument', descending = False):
        #                           0          1            2            3           4          5          6
        #row structure is ['Status', 'Inactive', 'Instrument', 'Ins Type', 'Currency', 'Market', 'Market Code', 'Price Distributor']

        # Start of new sortPriority dictionary creation code
        sortPriority1 = {}
        tupleSortPriority = list()

        priorityListForStatus = []

        priorityListForStatus.append(0)
        lastElem = len(CurrentColumns)+3
        idx = 2
        while idx < lastElem:
            priorityListForStatus.append(idx)
            idx = idx + 1
        priorityListForStatus.append(1)

        tupleSortPriority = tuple(priorityListForStatus)
        sortPriority1['Status'] = tupleSortPriority

        priorityListForInactive = []

        priorityListForInactive.append(1)
        lastElem = len(CurrentColumns)+3
        idx = 2
        while idx < lastElem:
            priorityListForInactive.append(idx)
            idx = idx + 1
        priorityListForInactive.append(0)

        tupleSortPriority = tuple(priorityListForStatus)
        sortPriority1['Inactive'] = tupleSortPriority


        priorityListForInstrument = []

        priorityListForInstrument.append(2)
        lastElem = len(CurrentColumns)+3
        idx = 3
        while idx < lastElem:
            priorityListForInstrument.append(idx)
            idx = idx + 1
        priorityListForInstrument.append(0)
        priorityListForInstrument.append(1)

        tupleSortPriority = tuple(priorityListForStatus)
        sortPriority1['Instrument'] = tupleSortPriority

        for index, column in enumerate(CurrentColumns):
            lastElem = len(CurrentColumns)+3
            priorityList = []
            pos = index+3
            priorityList.append(pos)
            idx = 2
            while idx < lastElem:
                if idx != pos:
                    priorityList.append(idx)
                idx = idx + 1
            priorityList.append(0)
            priorityList.append(1)

            tupleSortPriority = tuple(priorityList)
            sortPriority1[column] = tupleSortPriority

        return sorted(rows, key=operator.itemgetter(*sortPriority1[sortBy]), reverse=descending)

    def Sort(self, sortBy, descending):
        rows = self.GetRows()
        sortedRows = self._Sort(rows, sortBy, descending)
        self.pldList.Clear()
        self._Populate(sortedRows)

    def GetRows(self):
        rows = []
        root = self.pldList.GetRootItem()
        for child in root.Children():
            rows.append(child.GetData())
        return rows

    def _Populate(self, rows):
        rootItem = self.pldList.GetRootItem()
        for aRow in rows:
            child = rootItem.AddChild()
            for index, item in enumerate(aRow):
                child.Label(item, index)
            child.SetData(aRow)

    def Populate(self, pldList):
        rows = self.MakeRows(pldList)
        sortedRows = self._Sort(rows)
        self._Populate(sortedRows)
        self.AdjustColumnWidth()
        self.rowsModified = 0

    def AdjustColumnWidth(self):
        for count in range(0, self.countCol):
            self.pldList.AdjustColumnWidthToFitItems(count)

    def MakeRows(self, pldList):
        rows = []
        status = ''
        for pld in pldList:
            aRow = self.MakeRow(pld, status)
            rows.append(aRow)
        return rows

    def MakeRow(self, pld, status):

        inactive = ""
        if pld.IsKindOf('FPriceLinkDefinition'):
            if not status:
                distributor = pld.PriceDistributor()
                if distributor.ErrorMessage():
                    status = "DistErr"
                elif pld.ErrorMessage():
                    status = "E"
            if pld.NotActive():
                inactive = "X"

        marketName = ""
        if pld.Market():
            marketName = pld.Market().Name()

        ConfCol = acm.FArray()

        for column in MandatoryColumns:
            ConfCol.Add(column)

        for column in CurrentColumns:
            ConfCol.Add(column)

        listCol = []
        listCol.append(status)
        listCol.append(inactive)

        for item in ConfCol:
            if item in self.myDict:
                functionToCall = self.myDict[item]
                listCol.append(functionToCall(pld))

        listCol.append(pld)
        self.countCol = len(listCol)
        tupleCol = tuple(listCol)

        row = tupleCol
        return row

    def SetCountCol(self, count):
        self.countCol = count

    def Update(self, status, pld, child):
        row = self.MakeRow(pld, status)
        for index, item in enumerate(row):
            child.Label(item, index)
        child.SetData(row)
        self.AdjustColumnWidth()
        if status:
            self.rowsModified += 1

    def Add(self, pld):
        rootItem = self.pldList.GetRootItem()
        newRow = rootItem.AddChild()
        self.Update('A', pld, newRow)
        newRow.Select()
        newRow.EnsureVisible()
        self.AdjustColumnWidth()

    def RevertAll(self):
        root = self.pldList.GetRootItem()
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
            pld = self.GetPLDObject(row)
            originalPLD = self.GetOriginalPLDObject(pld)
            self.Update('', originalPLD, row)

        elif opType == 'A':
            self.pldList.SelectAllItems(False)
            row.Select()
            self.pldList.RemoveAllSelectedItems(True)

    def Remove(self):
        rows = self.GetSelectedRows()
        for aRow in rows:
            opType = self.GetOperationType(aRow)
            if opType == 'A':
                continue
            pld = self.GetPLDObject(aRow)
            self.Update('R', pld, aRow)

    def SaveAll(self):
        root = self.pldList.GetRootItem()
        for child in root.Children():
            self._Save(child)
        self.rowsModified = 0

    def Save(self):
        rows = self.GetSelectedRows()
        for aRow in rows:
            if self.IsModified(aRow):
                opType = self.GetOperationType(aRow)
                try:
                    self._Save(aRow)
                    self.rowsModified -= 1
                except RuntimeError as e:
                    if opType == 'U':
                        pld = self.GetPLDObject(aRow)
                        clone = pld.Clone()
                        operation = "U"
                        self.Update(operation, clone, aRow)
                        aRow.EnsureVisible()

    def _Save(self, row):
        opType = self.GetOperationType(row)
        pld = self.GetPLDObject(row)

        if opType == 'R':
            self._Delete(pld, row)

        elif opType == 'U':
            originalPLD = self.GetOriginalPLDObject(pld)
            originalPLD.Apply(pld)
            self.Commit(originalPLD, row)

        elif opType == 'A':
            message = "WARNING: Instrument [ " + pld.Instrument().Name() + " ] does not have - "
            if not pld.PriceDistributor():
                message = message + "<Distributor>"
            if not pld.IdpCode():
                message = message + " <Market Code>"
            if not pld.Market():
                message = message + " <Market>"

            message = message + " associated. Unable to create Price Link."

            if pld.PriceDistributor() and pld.IdpCode() and pld.Market():
                self.Commit(pld, row)
            else:
                print(message)


    def _Delete(self, pld, row):
        try:
            self.pldList.SelectAllItems(False)
            row.Select()
            originalPLD = self.GetOriginalPLDObject(pld)
            originalPLD.Delete()
            self.pldList.RemoveAllSelectedItems(True)
        except RuntimeError as e:
            print("Failed to delete PriceLinkDefinition '%s'. Refer Prime log for details." % pld.Oid())

    def Commit(self, pld, row):
        try:
            pld.Commit()
            status = ''
            self.Update(status, pld,  row)
        except RuntimeError as e:
            print("Failed to save PriceLinkDefinition '%s'. Refer Prime log for details." % pld.Oid())
            print(str(e))
            raise

    def HandleServerUpdate(self, param):
        matched = False
        root = self.pldList.GetRootItem()
        for child in root.Children():
            pld = self.GetPLDObject(child)
            if pld.Oid() == param.Oid():
                self.Update('', pld, child)
                matched = True
                break

    def HandleServerUpdateDist(self, param):
        root = self.pldList.GetRootItem()
        for child in root.Children():
            pld = self.GetPLDObject(child)
            self.Update('', pld, child)
                       
    def HandleServerRemove(self, param):
        root = self.pldList.GetRootItem()
        for child in root.Children():
            pld = self.GetPLDObject(child)
            if pld.Oid() == param.Oid():
               child.Remove()
               break

    def GetSelectedRow(self):
        return self.pldList.GetSelectedItem()

    def GetSelectedRows(self):
        return self.pldList.GetSelectedItems()

    def GetSelectedPLDs(self):
        selectedPLDs = []
        for row in self.GetSelectedRows():
            pld = self.GetPLDObject(row)
            selectedPLDs.append(pld)
        return selectedPLDs

    def GetSelectedPLD(self):
        retVal = None
        row = self.GetSelectedRow()
        if row != None:
            retVal = self.GetPLDObject(row)
        return retVal

    def GetPLDObject(self, row):
        data = row.GetData()
        return data[self.countCol-1]

    def GetOriginalPLDObject(self, pld):
        return acm.FPriceLinkDefinition[pld.Oid()]

    def GetOperationType(self, row):
        data = row.GetData()
        return data[0]

    def IsMultiSelect(self):
        return self.pldList.SelectedCount() > 1

    def IsModified(self, row):
        opType = self.GetOperationType(row)
        if opType in ('U', 'R', 'A'):
            return True
        return False