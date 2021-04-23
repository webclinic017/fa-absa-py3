
import acm
import time
import FUxCore

class TimePassed(object):
    def __init__(self):
        self._time = 0
        
    def SetNow(self):
        self._time = time.time()

    def TimePassed(self):
        return time.time() - self._time
        
class QuoteRequestReplyList(object):
    def __init__(self, quoteControllers, selectionChangedCB):
        self._quoteControllers = None
        self._fuxControl = None
        self._selectionChangedCB = selectionChangedCB
        self._timePassed = TimePassed()
        self.m_timeSpanFormatter = acm.Get('formats/SecondsSpan')
        self._quoteControllerToFuxItemMap = acm.FDictionary()
        self.SetQuoteControllerList(quoteControllers)
        
    def SetQuoteControllerList(self, quoteControllers):
        self._quoteControllers = quoteControllers
        self._quoteControllers.AddDependent(self)
        
    def QuoteControllers(self):
        return self._quoteControllers
        
    def TimePassed(self):
        timePassed = False
        if self._timePassed.TimePassed() > 0.75:
            self._timePassed.SetNow() 
            timePassed = True
        return timePassed
             
    def FuxControl(self):
        return self._fuxControl
        
    def SetListAttributes(self):
        self.FuxControl().ShowColumnHeaders(True)
        self.FuxControl().ShowGridLines(True)
        self.FuxControl().EnableHeaderSorting(False)
        self.FuxControl().EnableMultiSelect(False)
        self.FuxControl().ShowCheckboxes(False)
        
    def AdjustColumnWidth(self):
        for i in range(self.FuxControl().ColumnCount()):
            self.FuxControl().AdjustColumnWidthToFitItems(i)
            
    def AssignCallbacks(self):
        self.FuxControl().AddCallback('SelectionChanged', self.OnSelectionChanged, self )
    
    def AddColumnsToList(self):
        self.FuxControl().AddColumn('Time Left')
        self.FuxControl().AddColumn('Req Status')
        self.FuxControl().AddColumn('Order Book')
        self.FuxControl().AddColumn('Quote Status')
        self.FuxControl().AddColumn('Counterparty')
        self.FuxControl().AddColumn('Side')
        self.FuxControl().AddColumn('Quote Quantity')
        
    def OnInitControl(self):
        self.SetListAttributes()
        self.AddColumnsToList()
        self.AssignCallbacks()

    @FUxCore.aux_cb
    def OnSelectionChanged(self, *args):
        self._selectionChangedCB(self.FuxControl().GetData())
    
    def BuildLayout(self):
        fUxLayoutBuilder = acm.FUxLayoutBuilder()
        fUxLayoutBuilder.BeginHorzBox()
        fUxLayoutBuilder.AddList('replyHandlerList')
        fUxLayoutBuilder.EndBox()
        return fUxLayoutBuilder
        
    def Update(self):
        if self.TimePassed():
            self.UpdateList()
        
    def InitControls(self, fuxLayout):
        self._fuxControl = fuxLayout.GetControl('replyHandlerList')
        self.OnInitControl()
        for quoteController in self.QuoteControllers():
            self.AddToListControl(quoteController)
        self.AdjustColumnWidth()
    
    def SetColumnValuesToListItem(self, fuxItem, quoteController):
        fuxItem.Label(self.m_timeSpanFormatter.Format(quoteController.QuoteRequestReply().TimeoutCountdown()), 0)
        fuxItem.Label(quoteController.QuoteRequestReply().RequestStatus(), 1)
        fuxItem.Label(quoteController.TradingInterface(), 2)
        fuxItem.Label(quoteController.QuoteRequestReply().Status(), 3)
        fuxItem.Label(quoteController.QuoteRequestReply().CounterpartyId(), 4)
        fuxItem.Label(quoteController.QuoteRequestReply().BidOrAsk(), 5)
        fuxItem.Label(quoteController.QuoteRequestReply().RequestedQuantity(), 6)
      
    def RemoveFromListControl(self, quoteController):
        fuxItem = self._quoteControllerToFuxItemMap.RemoveKey(quoteController)
        quoteController.RemoveDependent(self)
        fuxItem.Remove()

    def AddToListControl(self, quoteController):
        fuxItem = self._quoteControllerToFuxItemMap.At(quoteController)
        if not fuxItem:
            rootItem = self.FuxControl().GetRootItem()
            fuxItem = rootItem.AddChild(True)
            fuxItem.SetData(quoteController)
            icon = quoteController.Icon()
            fuxItem.Icon(icon, icon)
            self._quoteControllerToFuxItemMap.AtPut(quoteController, fuxItem)
        self.SetColumnValuesToListItem(fuxItem, quoteController)

    def RemoveAllItemsFromList(self, quoteController):
        self.FuxControl().RemoveAllItems()
        self._quoteControllerToFuxItemMap = acm.FDictionary()
        
    def UpdateListControlItem(self, quoteController):
        fuxItem = self._quoteControllerToFuxItemMap.At(quoteController)
        if fuxItem:
            self.SetColumnValuesToListItem(fuxItem, quoteController)
        
    def UpdateList(self):
        for quoteController in self.QuoteControllers():
            self.UpdateListControlItem(quoteController)

    def UpdateSelected(self, quoteController):
        fuxItem = self._quoteControllerToFuxItemMap.At(quoteController)
        fuxItem.Select(True)
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        try: 
            if sender == self.QuoteControllers():
                if str(aspectSymbol) == 'remove':
                    self.RemoveFromListControl(parameter)
                elif str(aspectSymbol) == 'insert':
                    self.AddToListControl(parameter)
                elif str(aspectSymbol) == 'clear':
                    self.RemoveAllItemsFromList()
        except Exception as e:
            print ('ReplyHandlerList ServerUpdate failed: ' + str(e))
                    
