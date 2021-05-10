import acm
import FSheetPanel
import FSheetUtils
import StiwUtils
from StiwCustomization import Filters
from StiwEvents import OnTradeSelectionChanged, OnQuoteRequestSelectionChanged, OnSalesOrderSelectionChanged
from FEvent import EventCallback

class StiwSheetBase(FSheetPanel.SheetPanel):
    def __init__(self, *args, **kwargs):
        super(StiwSheetBase, self).__init__(*args, **kwargs)
        self._lastGrouper = None
        self._client = None
        
    def InitControls(self, layout):
        super(StiwSheetBase, self).InitControls(layout)
        self.Sheet().ShowGroupLabels(False)
    
    def InitSheetContents(self):
        initialContents = self.InitialContents() or acm.FDictionary()
        sheetContents = initialContents.At('sheetContents')
        if sheetContents:
            # In order to not store the rows when saving a workspace.
            rows = acm.FSymbol('rows')
            noRows = self.Sheet().Sheet().SheetContents().At(rows)
            sheetContents.AtPut(rows, noRows)
            self.Sheet().Sheet().SheetContents(sheetContents)
        self._lastGrouper = initialContents.At('grouper')
    
    def GetContents(self):
        # Serialize additional data
        contents = super(StiwSheetBase, self).GetContents() or acm.FDictionary()
        contents['grouper'] = self.GetGrouper()
        return contents
    
    # -------------------------------------------------------------
    # Events
    # -------------------------------------------------------------  
    @EventCallback
    def OnClientChanged(self, event=None):
        self._client = event.Parameters()
        filter = self.GetFilter(self._client, None)
        self.RepopulateSheet(filter)
        
    @EventCallback
    def OnUnderlyingChanged(self, event=None):
        underlying = event.Parameters()
        filter = self.GetFilter(self._client, underlying)
        self.RepopulateSheet(filter)
    
    # -------------------------------------------------------------
    # Utils
    # -------------------------------------------------------------
    def GetGrouper(self):
        if self.Sheet():
            return FSheetUtils.GetGrouperFromSheet(self.Sheet())
    
    def SetGrouper(self, grouper):
        if grouper:
            FSheetUtils.ApplyGrouperToSheet(self.Sheet(), grouper)
        elif self._lastGrouper:
            FSheetUtils.ApplyGrouperToSheet(self.Sheet(), self._lastGrouper)
            self._lastGrouper = None
    
    def RepopulateSheet(self, filter):
        grouper = self.GetGrouper()
        self.Sheet().RemoveAllRows()
        if filter:
            self.Sheet().Sheet().InsertObject(filter, 'IOAP_REPLACE')
        else:
            self._lastGrouper = grouper
        FSheetUtils.ExpandTree(self.Sheet())
        self.SetGrouper(grouper)
    
    
'''********************************************************************
* Trade History
********************************************************************'''
class StiwTradeHistorySheet(StiwSheetBase):
        
    def GetFilter(self, client, underlying):
        return Filters.TradeSheet(client, underlying)
    
    def SelectionChanged(self, selection):
        selected = None
        selection = selection and selection.SelectedTrades()
        if selection and len(selection) == 1:
            selected = selection[0]
        self.SendEvent(OnTradeSelectionChanged(self, selected))


'''********************************************************************
* Portfolio History
********************************************************************'''
class StiwPortfolioHistorySheet(StiwSheetBase):
    
    def GetFilter(self, client, underlying):
        return Filters.PortfolioSheet(client, underlying)
        
    def SelectionChanged(self, selection):
        pass


'''********************************************************************
* Quote Requests
********************************************************************'''
class StiwQuoteRequestHistorySheet(StiwSheetBase):
    
    def GetFilter(self, client, underlying):
        return Filters.QuoteRequestPricingSheet(client, underlying)

    def SelectionChanged(self, selection):
        selected = None
        selection = selection and selection.SelectedRowObjects()
        if selection and len(selection) == 1:
            candidate = selection[0]
            if candidate.IsKindOf(acm.FSingleQuoteRequestRow):
                selected = candidate.QuoteRequestInfo()
        self.SendEvent(OnQuoteRequestSelectionChanged(self, selected))


'''********************************************************************
* Orders
********************************************************************'''
class StiwOrderHistorySheet(StiwSheetBase):
    
    def GetFilter(self, client, underlying):
        return Filters.OrderSheet(client, underlying)
    
    def SelectionChanged(self, selection):
        selected = None
        selection = selection and selection.SelectedRowObjects()
        if selection and len(selection) == 1:
            candidate = selection[0]
            if candidate.IsKindOf(acm.FSalesOrder):
                selected = candidate
        self.SendEvent(OnSalesOrderSelectionChanged(self, selected))

