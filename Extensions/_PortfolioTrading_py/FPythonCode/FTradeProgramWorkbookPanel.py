""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramWorkbookPanel.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramWorkbookPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FSheetUtils
import FTradeProgramColumns
from FWorkbookPanel import WorkbookPanel
from FTradeProgramEvents import OnMainSheetSelected
from FIntegratedWorkbenchLogging import logger
from FTradeProgramAction import Action
from FEvent import EventCallback

class TradeProgramWorkbookPanel(WorkbookPanel):

    def __init__(self, application):
        super(TradeProgramWorkbookPanel, self).__init__(application)
        self._lastColumn = None
        self._lastColumnOldBackground = None

    @EventCallback
    def OnTradeProgramActionCleared(self, event):
        FTradeProgramColumns.ClearInputColumns(self.Sheet(), self.Application())

    @EventCallback
    def OnOrdersSuccessfullyCreated(self, event):
        FTradeProgramColumns.ClearInputColumns(self.Sheet(), self.Application())
        
    @EventCallback
    def OnMainSheetSelected(self, event):
        self._HighlightTargetColumn(event.Selection())

    def _HighlightTargetColumn(self, selection):
        selectedCell = selection.SelectedCell()
        if selectedCell:
            self._SetColumnBackground(self._lastColumn, self._lastColumnOldBackground)
            self._lastColumn = None
            self._lastColumnOldBackground = None
            targetColumnID = self._FindTargetColumnID(selectedCell.Column())
            if targetColumnID:
                targetColumn = self._FindColumnInSheet(targetColumnID)
                if targetColumn:
                    self._lastColumn = targetColumn
                    self._lastColumnOldBackground = targetColumn.ColumnAppearance().Background()
                    fcolor = self._GetColor("BkgUserEdited")
                    self._SetColumnBackground(targetColumn, fcolor)
                else:
                    logger.debug("The target column '%s' is missing from sheet."%targetColumnID)

    def _FindTargetColumnID(self, selCol):
        colParams = FSheetUtils.ColumnParameters(selCol)
        return colParams.At('TargetColumnParameters') if colParams else None

    def _FindColumnInSheet(self, columnId):
        columnIter = self.Sheet().GridColumnIterator()
        while columnIter:
            gridColumn = columnIter.GridColumn()
            if gridColumn and str(gridColumn.ColumnId()) == columnId:
                return columnIter.GridColumn()
            columnIter = columnIter.Next()

    @staticmethod
    def _GetColor(name):
        return acm.GetDefaultContext().GetExtension(
            acm.FColor, acm.FObject, name).Value()

    @staticmethod
    def _SetColumnBackground(column, background):
        if column:
            app = column.ColumnAppearance()
            app.Background(background)
            column.ColumnAppearance(app)

    def SelectionChanged(self, selection):
        self.SendEvent(OnMainSheetSelected(self, selection))

