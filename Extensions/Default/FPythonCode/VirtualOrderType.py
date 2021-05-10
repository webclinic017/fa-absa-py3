import acm

def OnPrepare(self):
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()
    
    if self.OrderBook():
        tradingSession.AddTradingInterface(self.OrderBook())
        
    if self.OrderQuantity() == 0:
        self.OrderQuantity(self.TotalQuantity())

def DeleteActiveOrders(self, event):
    orders = self.TradingSession().Orders()
    for order in orders:
        if order.IsOrderActive():
            order.DeleteOrder()
 
def CreateAndSendOrder(self, event):   
    order = self.TradingSession().NewOrder(self.OrderBook())
    order.Account = self.Account()
    order.Reference = self.Reference()
    order.BuyOrSell = self.BuyOrSell()
    order.Quantity = self.UsedOrderQuantity()
    order.Price = self.Price()
    if order.IsModifyAllowed('MarketAccount'):
        order.MarketAccount = self.MarketAccount()
    if order.IsModifyAllowed('ExpirationDateTime'):
        order.ExpirationDateTime = self.ExpirationTime()
    
    self.Order = order
    order.SendOrder()
