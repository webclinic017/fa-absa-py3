from FHandler import Handler
from FEvent import EventCallback
from StiwEvents import OnTradeSelectionChanged, OnQuoteRequestSelectionChanged, OnSalesOrderSelectionChanged, OnUnderlyingChanged

class StiwHandler(Handler):

    def __init__(self, dispatcher):
        super(StiwHandler, self).__init__(dispatcher)
        self.client = None
        self.underlying = None
        self.selectedTrade = None
        self.selectedQuoteRequest = None
        self.selectedSalesOrder = None

    def ResetSelections(self):
        self.SendEvent(OnTradeSelectionChanged(None))
        self.SendEvent(OnQuoteRequestSelectionChanged(None))
        self.SendEvent(OnSalesOrderSelectionChanged(None))

    # ---------------------------------------------------------------
    # Client
    # ---------------------------------------------------------------
    @EventCallback
    def OnClientChanged(self, event):
        self.client = event.Parameters()
        self.ResetSelections()

    def Client(self):
        return self.client

    # ---------------------------------------------------------------
    # Underlying
    # ---------------------------------------------------------------
    @EventCallback
    def OnUnderlyingChanged(self, event):
        self.underlying = event.Parameters()
        self.ResetSelections()

    def Underlying(self):
        return self.underlying

    # ---------------------------------------------------------------
    # Trade Selection
    # ---------------------------------------------------------------
    @EventCallback
    def OnTradeSelectionChanged(self, event):
        self.selectedTrade = event.Parameters()
        
    def SelectedTrade(self):
        return self.selectedTrade

    # ---------------------------------------------------------------
    # Quote Request Selection
    # ---------------------------------------------------------------
    @EventCallback
    def OnQuoteRequestSelectionChanged(self, event):
        self.selectedQuoteRequest = event.Parameters()
        
    def SelectedQuoteRequest(self):
        return self.selectedQuoteRequest

    # ---------------------------------------------------------------
    # Sales Order Selection
    # ---------------------------------------------------------------
    @EventCallback
    def OnSalesOrderSelectionChanged(self, event):
        self.selectedSalesOrder = event.Parameters()
        
    def SelectedSalesOrder(self):
        return self.selectedSalesOrder
