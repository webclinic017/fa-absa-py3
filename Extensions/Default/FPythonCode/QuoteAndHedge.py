import acm
import FAgent

def OnPrepare(self):
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()
    
    if None != self.QuoteLegTradingStrategy(): 
        self.QuoteLegUsedOrderBook=acm.FSmartTradingInterface(self.QuoteLegOrderBook());
    else:
        self.QuoteLegUsedOrderBook=self.QuoteLegOrderBook();
    
    if None != self.HedgeLegTradingStrategy(): 
         self.HedgeLegUsedOrderBook=acm.FSmartTradingInterface(self.HedgeLegOrderBook());
    else:
         self.HedgeLegUsedOrderBook=self.HedgeLegOrderBook();
        
    if None != self.QuoteLegUsedOrderBook():
        tradingSession.AddTradingInterface(self.QuoteLegUsedOrderBook())
    if None != self.HedgeLegUsedOrderBook():
        tradingSession.AddTradingInterface(self.HedgeLegUsedOrderBook(), True)
    if None == self.HedgeOrders():
        self.HedgeOrders = acm.FDependentArray()
        self.DoneHedgeOrders = acm.FFilteredSet()
        self.DoneHedgeOrders().AddSource(self.HedgeOrders())
        doneFilter = acm.Filter.SimpleAndQuery(acm.FOrderHandler, ['IsOrderDone'], None, [True])
        self.DoneHedgeOrders().Filter = doneFilter
        self.DeletedHedgeOrders = acm.FFilteredSet()
        self.DeletedHedgeOrders().AddSource(self.HedgeOrders())
        deletedFilter = acm.Filter.SimpleAndQuery(acm.FOrderHandler, ['IsOrderDeleted'], None, [True])
        self.DeletedHedgeOrders().Filter = deletedFilter
    
    if self.Status() == 'Stopped':
        self.QuoteOrder = None
        self.QuoteOrderPrice = 0
        self.QuoteOrderQuantity = 0
        self.QuoteLegFilledQuantity = 0
        self.QuoteLegFilledQuantityPreviously = 0
        self.HedgeOrders().Clear()
        self.HedgeOrderPrice = 0
        self.HedgeOrderQuantity = 0
        self.HedgeLegFilledQuantity = 0


    errHandler = self.ErrorHandler()
    errHandler.Clear()
    errHandler.RegisterCondition('infoRuleQuoteOrderPriceIsSafe', 'Information', 'Quote price is unsafe')
    errHandler.RegisterCondition('infoRuleQuoteLegPriceAndQuantityIsRational', 'Information', 'Quote order is not rational')
    errHandler.RegisterCondition('infoRuleHedgeLegOrderBookIsNotMatching', 'Information', 'Hedge order book has crossing prices')
    errHandler.RegisterCondition('infoRuleQuoteLegOrderBookIsConnected', 'Information', 'Quote order book is not connected')
    errHandler.RegisterCondition('infoRuleHedgeLegOrderBookIsTradeable', 'Information', 'Hedge order book is not tradable')
    errHandler.RegisterCondition('infoRuleHedgeLegOrderBookIsNotEmpty', 'Information', 'Hedge order book is empty')
    errHandler.RegisterCondition('infoRuleQuoteLegCalculatedQuantityOverMinimum', 'Information', 'Calculated quote quantity below minimum quote limit')
    errHandler.RegisterCondition('infoRuleQuoteLegInternalOrderBookPresent', 'Information', 'Quote order book must have a corresponding order book on the internal market for SMART to work.')
    errHandler.RegisterCondition('infoRuleHedgeLegInternalOrderBookPresent', 'Information', 'Hedge order book must have a corresponding order book on the internal market for SMART to work.')
    
def OnOrderDelete(self, order):
    if order.OrderType() == 'Fill and Kill (IOC)':
        pass
    else:
        FAgent.OnOrderDelete(self, order)

def PrepareManualOrder(self, order):
    trading = order.TradingInterface()
    if trading == self.HedgeLegUsedOrderBook():
        order.Account = self.HedgeOrderAccount()
        order.Reference = self.HedgeOrderReference()
        order.BuyOrSell = self.HedgeLegBuyOrSell()
        order.Quantity = abs(self.HedgeLegResidual())
        price = order.GetPrice('Match All')
        if not trading.PriceFeed().IsValidPrice(price):
            price = float(trading.PriceFeed().LastPrice().Get())
        order.Price = price
    else:
        raise Exception('Manual orders only allowed for hedge leg!')
    
def CreateQuoteOrder(self, event):
    quoteOrder = self.TradingSession().NewOrder(self.QuoteLegUsedOrderBook())
    if self.QuoteLegTradingStrategy()!=None:
        quoteOrder.TradingStrategy(self.QuoteLegTradingStrategy())
    quoteOrder.RemoveOnBrokenSession=True
    quoteOrder.Account = self.QuoteOrderAccount()
    quoteOrder.Reference = self.QuoteOrderReference()
    quoteOrder.BuyOrSell = self.QuoteLegBuyOrSell()
    #Set previously filled quantity with the total filled quantity when creating a new quote order
    self.QuoteLegFilledQuantityPreviously = self.QuoteLegFilledQuantity()
    self.QuoteOrder = quoteOrder

def SetAndSendQuoteOrder(self, event):
    quoteOrder = self.QuoteOrder()
    if self.QuoteLegTradingStrategy()!=None:
        quoteOrder.AlgoTradingInstruction().StartAgent(True)
    quoteOrder.Price = self.QuoteOrderPrice()
    quoteOrder.Quantity = self.QuoteOrderQuantity()
    quoteOrder.SendOrder()

def CreateAndSendHedgeOrder(self, event):
    hedgeOrder = self.TradingSession().NewOrder(self.HedgeLegUsedOrderBook())
    if self.SendHedgeOrders() is False:
        hedgeOrder.Release()
    if self.HedgeLegTradingStrategy()!=None:
        hedgeOrder.TradingStrategy(self.HedgeLegTradingStrategy())
    hedgeOrder.RemoveOnBrokenSession=True
    hedgeOrder.Account = self.HedgeOrderAccount()
    hedgeOrder.Reference = self.HedgeOrderReference()
    hedgeOrder.BuyOrSell = self.HedgeLegBuyOrSell()
    hedgeOrder.IsIndependentModifyEnabled(True)
    hedgeOrder.HedgeOrder(True)
    
    if self.HedgeLegTradingStrategy()!=None:
        hedgeOrder.AlgoTradingInstruction().StartAgent(True)
    hedgeOrder.Price = self.HedgeOrderPrice()
    hedgeOrder.Quantity = self.HedgeOrderQuantity()
    hedgeOrder.LoadOrder()
    if self.SendHedgeOrders() is True:
        hedgeOrder.SendOrder()
        self.HedgeOrders().Add(hedgeOrder)

def DeleteQuoteOrder(self, event):
    self.QuoteOrder().DeleteOrder()

def HandleDoneHedgeOrders(self, event):
    hedgeOrders = self.HedgeOrders()
    removeHedgeOrders = []

    for hedgeOrder in hedgeOrders:
        if hedgeOrder.IsOrderDone():
            removeHedgeOrders.append(hedgeOrder)
            self.HedgeLegFilledQuantity = self.HedgeLegFilledQuantity() + hedgeOrder.FilledQuantity("Order")

    for hedgeOrder in removeHedgeOrders:
        hedgeOrders.Remove(hedgeOrder)

        
def HandleDeletedHedgeOrders(self, event):
    hedgeOrders = self.HedgeOrders()
    removeHedgeOrders = []

    for hedgeOrder in hedgeOrders:
        if hedgeOrder.IsOrderDeleted():
            removeHedgeOrders.append(hedgeOrder)

    for hedgeOrder in removeHedgeOrders:
        hedgeOrders.Remove(hedgeOrder)

def HandleDoneResidualOrder(self, event):
    residualOrder = self.ResidualOrder()
    if residualOrder:
        self.HedgeLegResidual = self.HedgeLegResidual() - residualOrder.FilledQuantity('Order')
    
def WithdrawActiveOrdersAndReport(self, event):
    self.TradingSession().DeleteOrders()
    log = self.Log()
    if log:
        logString = 'Agent Stopped\n'
        logString += 'Done Quote Quantity = ' + str(self.QuoteLegFilledQuantity()) + '\n'
        logString += 'Done Hedge Quantity = ' + str(self.HedgeLegFilledQuantity()) + '\n'
        log.AddStringRecord(logString);

"""
    Button actions
"""
def isQuoteAndHedgeAgent(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    rowObject = cell.RowObject()
    if rowObject.IsKindOf('FAgentRow'):
        agent = rowObject.AgentProxy()
        return agent and agent.IsKindOf('LocalAgent.QuoteAndHedgeProxy')
    return rowObject and rowObject.IsKindOf('QuoteAndHedge')

def showMoveButton(invokationInfo):
    return isQuoteAndHedgeAgent(invokationInfo)

def showRemoveButton(invokationInfo):
    return isQuoteAndHedgeAgent(invokationInfo)
    
def onMatchButton(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")  
    if button:
        rowObject = button.RowObject()        
        agent = rowObject.Agent()
        hedgeOrders = agent.HedgeOrders()
        
        for o in hedgeOrders :
            if o.IsOrderActive():
                MarketPrice = acm.GetFunction('marketPrice', 0)
                if o.TradingInterface().PriceFeed().IsValidPrice(MarketPrice()):
                    o.OrderType('Fill and Kill (IOC)')
                    o.Price = MarketPrice()
                else: 
                    o.Price = o.GetPrice('Match All')
                    
                o.SendOrder()

def onBestButton(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")  
    if button:
        rowObject = button.RowObject()
        agent = rowObject.Agent()
        hedgeOrders = agent.HedgeOrders()
        
        for o in hedgeOrders :
            if o.IsOrderActive():
                Price = o.GetPrice('Best')
                if o.TradingInterface().PriceFeed().IsValidPrice(Price):
                    o.Price = Price
                    o.SendOrder()
                else:
                    log = self.Log()
                    if log:
                        logString = 'Best price not found, not moving Hedge order(s)\n'
                        log.AddStringRecord(logString);

def onJoinButton(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")  
    if button:
        rowObject = button.RowObject()
        agent = rowObject.Agent()
        hedgeOrders = agent.HedgeOrders()
        
        for o in hedgeOrders :
            if o.IsOrderActive():
                Price = o.GetPrice('Join')
                if o.TradingInterface().PriceFeed().IsValidPrice(Price):
                    o.Price = Price
                    o.SendOrder()
                else:
                    log = self.Log()
                    if log:
                        logString = 'Join price not found, not moving Hedge order(s)\n'
                        log.AddStringRecord(logString);

def onRemoveButton(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")  
    if button:
        rowObject = button.RowObject()
        agent = rowObject.Agent()
        hedgeOrders = agent.HedgeOrders()
        
        for o in hedgeOrders :
            if o.IsOrderActive():
                o.DeleteOrder()
                
