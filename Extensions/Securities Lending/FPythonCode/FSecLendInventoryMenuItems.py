""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendInventoryMenuItems.py"
""" --------------------------------------------------------------------------
MODULE
    FSecLendInventoryMenuItems

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Menu items used in the Inventory workbench. 

---------------------------------------------------------------------------"""
import acm
from FSecLendMenuItem import SecLendMenuItemBase
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FParameterSettings import ParameterSettingsCreator
import FSheetUtils


class SaveQuoteMenuItem(SecLendMenuItemBase):
    """ The menu item for saving quotes, based on the selection in the view. """
    
    def ActiveWorkbookSheet(self):
        if self._frame.IsKindOf(acm.FManagerBaseFrame):
            return self._frame.ActiveSheet()
        return None
    
    def WorkbookSheetSelection(self):
        try:
            return self.ActiveWorkbookSheet().Selection().SelectedRowObjects()
        except Exception:
            return acm.FArray()
    
    def EnabledFunction(self):
        selectedRows = self.WorkbookSheetSelection()
        if (self._ViewName() == 'SecLendInventoryView' and selectedRows.Size() == 1 
                and selectedRows.First().IsKindOf(acm.FPriceLevelRow)):
            return True
        return False
    
    def InvokeAsynch(self, eii):
        selectedItem = self.WorkbookSheetSelection().First() #Type is FPriceLevelRow
        # Call method for saving the selected instrument row. 


class OpenInstrumentInNewSheetMenuItem(IntegratedWorkbenchMenuItem):
    
    def __init__(self, extObj):
        super(self.__class__, self).__init__(extObj, view='SecLendInventoryView')
        self._frame = extObj
        self._settings = ParameterSettingsCreator.FromRootParameter('SecLendInventorySheet')
    
    def SheetSetup(self, rows):
        setup = FSheetUtils.SheetContents(self._settings).SheetSetup()
        setup.SheetTitle(','.join(row.StringKey() for row in rows[:3]))
        return setup
    
    def Invoke(self, eii):
        workbook = self._frame.ActiveWorkbook()
        rows = workbook.ActiveSheet().Selection().SelectedRowObjects()
        setup = self.SheetSetup(rows)
        newSheet = workbook.NewSheet('PortfolioSheet', self._settings.Columns(), setup)
        newSheet.InsertObject(rows, 'IOAP_FIRST')

def SaveQuoteItem(eii):
    return SaveQuoteMenuItem(eii)

def OpenInstrumentInNewSheet(eii):
    return OpenInstrumentInNewSheetMenuItem(eii)