""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryAvailabilityPanels.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendInternalAvailabilityPanels

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Inventory View - Panels displaying availability of lendable instruments.

------------------------------------------------------------------------------------------------"""
import acm
from FEvent import EventCallback
from FSecLendCommon import CommonSheetPanelBase
from FSecLendUtils import (GetDefaultPortfolioForExternalAvailability,
                           GetDefaultPortfolioForInternalAvailability,
                           GetAvailabilityQueryPortfolio)

class SecLendInventoryAvailabilityPanelBase(CommonSheetPanelBase):

    def __init__(self):
        super(SecLendInventoryAvailabilityPanelBase, self).__init__()
        self._instrument = None
        self._portfolio = None
        self._sortColumn = ''
        self._sortAscending = True
        self._rowTreeIsBuilt = True
        
    def SetSheetContents(self, folder):
        self.Sheet().InsertObject(folder, 'IOAP_REPLACE')
        self._rowTreeIsBuilt = self.RowTreeIsBuilt()
        if self._rowTreeIsBuilt:
            self.UpdateSheetContentsRowTree()

    def UpdateSheetContentsRowTree(self):
        self.Sheet().RowTreeIterator(0).Tree().Expand(True, self.Settings().ExpandTreeLevels())
        self.SortBy(self._sortColumn or self.Settings().SortColumn(), self._sortAscending if self._sortColumn else self.Settings().SortAscending())

    def RowTreeIsBuilt(self):
        iterator = self.Sheet().RowTreeIterator(0).NextUsingDepthFirst()
        if iterator.Tree().Item().IsKindOf('FDistributedRow'):
            while iterator.Tree().NumberOfChildren():
                iterator = iterator.NextUsingDepthFirst()
            return iterator.Tree().Item().IsSingleInstrument()
        return True

    def HandleOnIdle(self):
        if not self._rowTreeIsBuilt:
            self._rowTreeIsBuilt = self.RowTreeIsBuilt()
            if self._rowTreeIsBuilt:
                self.UpdateSheetContentsRowTree()
        
    def SortBy(self, columnId, ascending=False, storeValues = False):
        if storeValues:
            self._sortColumn = columnId
            self._sortAscending = ascending
        if columnId:
            columnIter = self.Sheet().GridColumnIterator()
            while columnIter:
                gridColumn = columnIter.GridColumn()
                if gridColumn and gridColumn.ColumnId() == acm.FSymbol(columnId):
                    self.Sheet().SortColumn(columnIter, ascending)
                    break
                columnIter = columnIter.Next()
    
    def InitSheetContents(self):
        super(SecLendInventoryAvailabilityPanelBase, self).InitSheetContents()
        initialContents = self.InitialContents() or acm.FDictionary()
        self._sortColumn = initialContents.At('SortColumn')
        self._sortAscending = initialContents.At('SortAscending')
        self.SortBy(self._sortColumn or self.Settings().SortColumn(), self._sortAscending if self._sortColumn else self.Settings().SortAscending())
    
    def GetContents(self):
        contents = super(SecLendInventoryAvailabilityPanelBase, self).GetContents() or acm.FDictionary()
        contents['SortColumn'] = self._sortColumn
        contents['SortAscending'] = self._sortAscending
        return contents
    
    def UpdateAvailabilitySheetContents(self):
        if self._instrument:
            asqlPortfolio = GetAvailabilityQueryPortfolio(self._portfolio, self._instrument.Name())
            self.SetSheetContents(asqlPortfolio)
        
class SecLendInventoryInternalPanel(SecLendInventoryAvailabilityPanelBase):

    def __init__(self):
        super(SecLendInventoryInternalPanel, self).__init__()
        self._portfolio = GetDefaultPortfolioForInternalAvailability().Name()

    @EventCallback
    def OnInventoryViewInstrumentsSelected(self, event):
        instrument = event.GetUnderlyingOrSelf()
        if self._instrument != instrument:
            self._instrument = instrument
            self.UpdateAvailabilitySheetContents()
            

class SecLendInventoryExternalPanel(SecLendInventoryAvailabilityPanelBase):

    def __init__(self):
        super(SecLendInventoryExternalPanel, self).__init__()
        self._portfolio = GetDefaultPortfolioForExternalAvailability().Name()

    @EventCallback
    def OnInventoryViewInstrumentsSelected(self, event):
        instrument = event.GetUnderlyingOrSelf()
        if self._instrument != instrument:
            self._instrument = instrument
            self.UpdateAvailabilitySheetContents()
