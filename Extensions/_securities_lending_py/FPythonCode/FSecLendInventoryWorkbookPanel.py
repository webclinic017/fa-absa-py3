""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryWorkbookPanel.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendInventoryWorkbookPanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Inventory View - Main workbook panel.

------------------------------------------------------------------------------------------------"""
import acm
from FEvent import EventCallback
from FSecLendEvents import OnInventoryViewInstrumentsSelected, OnInventoryViewInstrumentDoubleClick, OnPositionSelection
from FSecLendCommon import ExtendedWorkbookPanel, WorkbenchSheet
from FSecLendUtils import ASQLPortfolioProvider
import FSecLendUtils
from FSecLendHooks import DefaultPortfolio

class SecLendInventoryWorkbookPanel(ExtendedWorkbookPanel):
    pass
    
class SecLendInventorySheet(WorkbenchSheet):

    def __init__(self, workbookPanel, settings):
        super(SecLendInventorySheet, self).__init__(workbookPanel, settings)
        self._inventoryQuery = None
        self._instrument = None
        self._rowTreeIsBuilt = True
    
    def HandleCreate(self):
        super(SecLendInventorySheet, self).HandleCreate()
        self.InitOnIdleCallback()

    def ShowSheetContents(self):
        return bool(self._inventoryQuery)

    def QueryFolderLabel(self):
        return self.Settings().InsertItemFolderLabel() or self.Settings().Caption()

    def RowSelectionChanged(self, selection):
        if selection.SelectedRowObjects():
            rowObject = selection.SelectedRowObjects().First()
            if rowObject.Class() == acm.FMultiInstrumentAndTrades:
                instruments = rowObject.Instruments()
                if instruments:
                    underlyings = instruments.Transform("UnderlyingOrSelf", "FSet", [])
                    if underlyings.Size() != 1:
                        return
                    instrument = underlyings.AsList().First()
                    if self._instrument != instrument:
                        self._instrument = instrument
                        self.SendEvent(OnInventoryViewInstrumentsSelected(self, instrument))
        # Event for Rerate Panel
        self.SendEvent(OnPositionSelection(self, selection.SelectedRowObjects()))
                    
    def UpdateInventorySheetContents(self):
        if self._inventoryQuery:
            folder = acm.FASQLQueryFolder()
            folder.Name(self.QueryFolderLabel())
            folder.AsqlQuery(self._inventoryQuery)
            asqlPortfolio = ASQLPortfolioProvider().GetOrCreateFromQuery(folder)
            self.Sheet().InsertObject(asqlPortfolio, 'IOAP_REPLACE')
            self._rowTreeIsBuilt = self.RowTreeIsBuilt()
            if self._rowTreeIsBuilt:
                self.UpdateSheetContentsRowTree()

    def UpdateSheetContentsRowTree(self):
        self.Sheet().ExpandTree(self.Settings().ExpandTreeLevels())
            
    def RowTreeIsBuilt(self):
        iterator = self.Sheet().RowTreeIterator(0).NextUsingDepthFirst()
        if iterator.Tree().Item().IsKindOf('FDistributedRow'):
            while iterator.Tree().NumberOfChildren():
                iterator = iterator.NextUsingDepthFirst()
            return iterator.Tree().Item().IsSingleInstrument()
        return True

    def OnHandleOnIdle(self, *args):
        if not self._rowTreeIsBuilt:
            self._rowTreeIsBuilt = self.RowTreeIsBuilt()
            if self._rowTreeIsBuilt:
                self.UpdateSheetContentsRowTree()        

    @EventCallback
    def OnInventoryViewInventoryChangedFromOrderCapture(self, event):
        self.UpdateInventoryView(event)
        
    @EventCallback
    def OnInventoryViewInventoryChanged(self, event):
        self.UpdateInventoryView(event)

    def UpdateInventoryView(self, event):
        instrument = event.Instrument()
        if instrument and self._instrument != instrument:
            self._instrument = instrument
            self._inventoryQuery = self.CreateInventoryQuery()
            self.UpdateInventorySheetContents()

    def SelectionDoubleClick(self, selection):
        rowObject = selection.SelectedCell().RowObject()
        if rowObject.IsKindOf(acm.FInstrumentAndTrades):
            loan = rowObject.Instrument()
            self.SendEvent(OnInventoryViewInstrumentDoubleClick(self, loan))

    def CreateInventoryQuery(self):
        inventory_query = self._InsertItemQuery() or self.DefaultInsertItemQuery()
        if inventory_query:
            inventory_query.AddAttrNodeString('Instrument.Underlying.Name', self._instrument.Name(), 'EQUAL')
            return inventory_query

    def DefaultInsertItemQuery(self):
        query = FSecLendUtils.ActiveLoansBaseQuery()
        conf_portfolios = [DefaultPortfolio(), FSecLendUtils.GetDefaultPortfolioForExternalAvailability(),
                           FSecLendUtils.GetDefaultPortfolioForInternalAvailability()]
        if conf_portfolios:
            orNodePort = query.AddOpNode('OR')
            for port in conf_portfolios:
                for p in port.AllPhysicalPortfolios() if port.IsKindOf(acm.FCompoundPortfolio) else [port]:
                    orNodePort.AddAttrNode('Portfolio.Name', 'EQUAL', p.Name())
        return query


