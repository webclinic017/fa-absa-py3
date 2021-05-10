import acm

def OnPrepare(self):
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()
    if None != self.OrderBook():
        tradingSession.AddTradingInterface(self.OrderBook())
    self.FilledQuantity(0)


def OnOrderDelete(self, order):
    pass


def CreateOrder(self, event):
    order = self.TradingSession().NewOrder(self.OrderBook())
    order.Account = self.Account()
    order.Reference = self.Reference()
    order.BuyOrSell = self.BuyOrSell()
    self.Order = order


def SendOrder(self, event):
    order = self.Order()
    order.Quantity = min( self.OrderQuantity(), self.TargetQuantity() - self.FilledQuantity() )
    
    sendPrice = 0
    priceType = self.OrderPriceType()
    
    if priceType == 'Own Price':
        sendPrice = self.OrderBook().PriceFeed().RoundTickUpDown(not order.IsBuy(), self.OwnPrice())
    elif priceType == 'Last':
        sendPrice = order.GetPrice(priceType)
    elif priceType == 'Middle':
        sendPrice = self.OrderBook().PriceFeed().RoundTickUpDown(not order.IsBuy(), order.GetPrice(priceType))
    elif priceType == 'Match' or priceType == 'Match All':
        sendPrice = order.GetPrice(priceType)
        order.OrderType = 'Fill and Kill (IOC)'

    if sendPrice == 0:
        self.ErrorHandler().OnError('Fatal', 'Order price is 0')
        return
    
    order.Price = sendPrice    
    order.SendOrder()

def CleanUp(self, event):
    self.TradingSession().DeleteOrders()
