import acm

def OnPrepare(self):
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()
    if None != self.OrderBook():
        tradingSession.AddTradingInterface(self.OrderBook())

def CreateOrder(self, event):
    order = self.TradingSession().NewOrder(self.OrderBook())
    order.Account = self.Account()
    order.Reference = self.Reference()
    order.BuyOrSell = self.BuyOrSell()
    order.Price = self.OrderPrice()
    order.Quantity = self.OrderQuantity()
    self.Order = order

def SendOrder(self, event):
    self.Order().SendOrder()  

def CleanUp(self, event):
    self.TradingSession().DeleteOrders()

