import acm
import ExecutionAlgo

def OnPrepare(self):
    ExecutionAlgo.OnPrepare(self)

def PrepareManualOrder(self, order):
    pass

def AdjustQuantityDueToExternalVolume(self, event):
    self.ExternalDealDetected(False)
    
    order = None
    if self.CurrentOrder():
        order = self.CurrentOrder()
    filledQty = 0
    if order:
        filledQty = order.FilledQuantity("Order")
    
    qtyLeftForAgent = self.ExecutionPlan().RemainingQuantity();
    qtyLeftInSlice  =   self.Slice().RemainingQuantity() - filledQty
    
    TraceLog(self, 'QtyLeftForAgent: '+str(qtyLeftForAgent))
    TraceLog(self, 'QtyLeftInSlice: '+str(qtyLeftInSlice))
        
    if (qtyLeftForAgent < qtyLeftInSlice):
        self.ExecutionPlan().UpdateSliceQuantity(qtyLeftForAgent);
        TraceLog(self, 'Adjustment due to external deal for slice: '+str(self.Slice()))
        TraceLog(self, 'Remaining quantity: ' + str(self.Slice().RemainingQuantity()))

def ReoptimizeAfterPhaseChange(self, event):
    pass
 
def GetUpdatedAuctionQuantity(self, event):
    UpdateAuctionQuantity(self, event)
    
    return self.AuctionSliceQuantity()
    

def UpdateAuctionOrder(self, event):
    order = self.CurrentOrder()

    if order and order.IsOrderActive():
        updatedQty = GetUpdatedAuctionQuantity(self, event)          
        if updatedQty > 0 :
            order.Quantity(updatedQty)
            self.CurrentOrderQty(updatedQty)
            self.PendingCommand(order.SendOrder())
            ExecutionAlgo.UpdateAuctionOrderStatus(self, False)

def UpdateAuctionSliceQuantity(self, event):
    if self.Slice():
        currentSliceQty = self.Slice().Quantity()
        if ( (currentSliceQty != self.AuctionSliceQuantity()) and (not self.Slice().IsFinished()) ):
            self.ExecutionPlan().UpdateSliceQuantity(self.AuctionSliceQuantity())

    

def SetInitialAuctionSliceQuantity(self, event):
    averageTradeQty = self.TradingInterface().PrevRoundLot( self.PeriodAverageTradeSize() )
    qty = min(averageTradeQty, self.ExecutionPlan().RemainingQuantity())
    self.AuctionSliceQuantity(qty)

def UpdateAuctionQuantity(self, event):
    qty = self.LimVolumeParticipationAuctionQty()
    TraceLog(self, 'Participation limited order quantity: ' + str(qty))
    TraceLog(self, 'Max participation quantity: ' + str(self.AuctionMaxParticipationAuctionQuantity()))
    TraceLog(self, 'Max participation rate: ' + str(self.AuctionMaxParticipationRate()))
    TraceLog(self, 'Auction Surplus: ' + str(self.AuctionSurplus()))
    TraceLog(self, 'Auction Equilibirum Quantity: ' + str(self.AuctionEquilibriumQuantity()))
    
    if qty > 0 :
        self.AuctionSliceQuantity(qty)
    else: 
        TraceLog(self, 'Invalid modify quantity for auction (limited order qty):' + str(qty))
    
    self.ModifyAuctionOrderTimer(acm.Time.Timer().CreateTimerEvent(self.ModifyAuctionOrderDelayLength(), None, None))

def TraceLog(self, message):
    if self.IsTraceEnabled() and self.Log():
        self.Log().AddStringRecord(message)

def UpdateQuantity(self, event):
    order = self.CurrentOrder()
    slice = self.Slice()
    if order and order.IsOrderActive() and slice:
        filledQty = order.FilledQuantity("Order")
        if (slice.RemainingQuantity() - filledQty) > 0:
            order.Quantity(slice.RemainingQuantity() - filledQty)
            self.PendingCommand(order.SendOrder())
        else:
            self.PendingCommand(self.TradingSession().DeleteOrders(True))
