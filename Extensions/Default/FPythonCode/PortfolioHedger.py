

import acm

def OnPrepare(self):
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()

def OnPrepared(self):
    if self.HedgeSMART():
        self.TradingUsed=acm.FSmartTradingInterface(self.Trading())
    else:
        self.TradingUsed=self.Trading()

    if None != self.TradingUsed():
        self.TradingSession().AddTradingInterface(self.TradingUsed())
            
def OnCommandError(self, command):
    self.HasErrors = True
    errors = command.Errors()
    message = ''
    for e in errors:
        message = message + e.Message() + '\n'
    self.ConsecutiveErrors = self.ConsecutiveErrors() + 1
    self.ErrorMessage = self.ErrorMessage() + message
    
def CleanUp(self, event):
    self.TradingSession().ClearLimitCommands()
    self.TradingSession().DeleteOrders()
    tag = self.Tag()
    acm.GetCalculatedValueFromString(self.SourceObj(), self.Context(), 'agentPortfolioHedgerActive', tag).RemoveSimulation()

def CreateAndSendAskOrder(self, event):
    order = self.LastOrder()
    
    # If the order was rejected try to resend it    
    if order and order.IsOrderInactive() and not order.IsBuy():
        if self.IsTraceEnabled() and self.Log():
            self.Log().AddStringRecord("Resending order. " + str(self.ConsecutiveErrors()) + " consecutive order modification failures.")
    else:
        order = self.TradingSession().NewOrder(self.TradingUsed())
        order.BuyOrSell('Sell')
        self.AskOrders().Add(order)

    sendPrice = self.TargetPrice()    
    if not self.PriceFeedUsed().IsValidPrice(sendPrice):
        return
        
    if self.HedgeSMART():
        order.TradingStrategy(self.HedgeTradingStrategy())
        order.AlgoTradingInstruction().StartAgent(True)
    order.Account = self.Account()
    order.Reference = self.Reference()
    order.Quantity = self.TradingUsed().NearestRoundLot(self.QtyShortfall())
    order.Price = sendPrice
    order.HedgeOrder(True)
    
    if (self.ActiveAsks().IsEmpty()) or (self.Wp() < sendPrice):
        self.Wp(sendPrice)

    if order.Quantity() < 1:
        print ('bad quantity')
        return
        
    self.LastOrder = order
    order.SendOrder()

def CreateAndSendBidOrder(self, event):
    order = self.LastOrder()

    # If the order was rejected try to resend it    
    if order and order.IsOrderInactive() and order.IsBuy():
        if self.IsTraceEnabled() and self.Log():
            self.Log().AddStringRecord("Resending order. " + str(self.ConsecutiveErrors()) + " consecutive order modification failures.")
    else:
        order = self.TradingSession().NewOrder(self.TradingUsed())
        order.BuyOrSell('Buy')
        self.BidOrders().Add(order)
        
    sendPrice = self.TargetPrice()
    if not self.PriceFeedUsed().IsValidPrice(sendPrice):
        return
        
    if self.HedgeSMART():
        order.TradingStrategy(self.HedgeTradingStrategy())
        order.AlgoTradingInstruction().StartAgent(True)
    order.Account = self.Account()
    order.Reference = self.Reference()
    order.Quantity = self.TradingUsed().NearestRoundLot(self.QtyShortfall())
    order.Price = sendPrice
    order.HedgeOrder(True)
    
    if (self.ActiveBids().IsEmpty()) or (self.Wp() > sendPrice):
        self.Wp(sendPrice)
       
    if order.Quantity() < 1:
        return
    
    self.LastOrder = order
    order.SendOrder()


def DeleteOrders(self, event):
    self.TradingSession().DeleteOrders()
    self.Wp(-1.0)


def ProcessTrade(self, event):
    qty = abs(self.TradeSource().Get().Quantity())
    self.LastFilledQtyOrders = self.LastFilledQtyOrders() + qty


def ReduceHedge (self, event):
    bid = not self.ActiveBids().IsEmpty()
    
    if self.QtyShortfall() > (-abs(self.MinSlice())):
        return
    
    qty = self.QtyShortfall()    
    orders = bid and self.ActiveBids().AsList().SortByProperty("Price", True) or self.ActiveAsks().AsList().SortByProperty("Price", False)
    wp = -1

    for order in orders:
        if qty < 0.0:
            qty = qty + order.Quantity() 
            self.MarkedOrders().Add(order)
            order.DeleteOrder()
        else:
            wp = order.Price().Number()
            break
            
    self.Wp(wp)
    self.ConsecutiveErrors = 0


def ReportOrderSizeBreached(self, event):
    print ('Error: Portfolio Hedger stopped for', self.Trading().StringKey(), ': Kill Agent Order Size has been exceeded')
    log = self.Log()
    if log:
        logString = 'PortfolioHedger Stopped: OrderSizeBreached\n'
        logString += '    killAgentOrderSize = ' + str(self.KillAgentOrderSize()) + '\n'
        logString += '    hedgeQty = ' + str(self.HedgeQuantity()) + '\n'
        log.AddStringRecord(logString);


def SetUp(self, event):
    if self.HedgeSMART():
        self.TradingUsed=acm.FSmartTradingInterface(self.Trading());
    else:
        self.TradingUsed=self.Trading();
    
    self.TradingSession().AddTradingInterface(self.TradingUsed())
    self.LastTrading = self.TradingUsed()
    self.LastMarket = self.TradingUsed().MarketPlace().Name()
    
    self.BidOrders = acm.FDependentArray()
    self.ActiveBids = acm.FFilteredSet()
    self.ActiveBids().AddSource(self.BidOrders())
    activeBidFilter = acm.Filter.SimpleAndQuery(acm.FOrderHandler, ['IsOrderActive', 'IsBuy'], None, [True, True])
    self.ActiveBids().Filter = activeBidFilter
    
    self.AskOrders = acm.FDependentArray()
    self.ActiveAsks = acm.FFilteredSet()
    self.ActiveAsks().AddSource(self.AskOrders())
    activeAskFilter = acm.Filter.SimpleAndQuery(acm.FOrderHandler, ['IsOrderActive', 'IsBuy'], None, [True, False])
    self.ActiveAsks().Filter = activeAskFilter
    
    self.MarkedOrders = acm.FDependentArray()
    self.ActiveMarks = acm.FFilteredSet()
    self.ActiveMarks().AddSource(self.MarkedOrders())
    activeMarksFilter = acm.Filter.SimpleAndQuery(acm.FOrderHandler, ['IsOrderActive'], None, [True])
    self.ActiveMarks().Filter = activeMarksFilter
    
    self.MaxNbrFailedModifications = self.TradingUsed().GetDefaultValueEx("PortfolioHedgerMaxNbrOfFailedModifications", self.Context()) - 1
    if self.MaxNbrFailedModifications() < 0:
        self.MaxNbrFailedModifications = 0
    
    nCommands = self.TradingUsed().GetDefaultValueEx('PortfolioHedgerMaxNbrOfCommands', self.Context())
    nCommandMs = self.TradingUsed().GetDefaultValueEx('PortfolioHedgerMaxCommandsMs', self.Context())
    self.TradingSession().LimitCommands(nCommands, nCommandMs)

def LogPriceBreach(self, BidOrAsk):
    if self.IsTraceEnabled() and self.Log():
        logString = str(BidOrAsk) + " price breached. " + "wp=" + str(self.Wp()) + " PriceType=" + str(self.PriceType()) + " TargetPrice=" + str(self.TargetPrice()) + " PriceOffset=" + str(self.PriceOffset()) + " PriceSlack=" + str(self.PriceSlack())
        self.Log().AddStringRecord(logString)
    

def UpdateAsks (self, event):
    LogPriceBreach(self, "Ask")
    tp = self.TargetPrice()
    po = self.PriceOffset()
    ps = self.PriceSlack()
    wp = -1
    
    cut = ((self.PriceType() == 'Join') and (po > 0.0)) and tp - po + ps or tp + ps
    orders = self.ActiveAsks().AsList().SortByProperty("Price", False)

    for order in orders:
        if order.Price().Number() > cut:
            self.MarkedOrders().Add(order)
            order.DeleteOrder()            
        else:
            wp = order.Price().Number()
            break
            
    self.Wp(wp)
    self.ConsecutiveErrors = 0


def UpdateBids (self, event):
    LogPriceBreach(self, "Bid")
    tp = self.TargetPrice()
    po = self.PriceOffset()
    ps = self.PriceSlack()
    wp = -1
    
    cut = ((self.PriceType() == 'Join') and (po > 0.0)) and tp + po - ps or tp - ps
    orders = self.ActiveBids().AsList().SortByProperty("Price", True)
    
    for order in orders:
        if order.Price().Number() < cut:
            self.MarkedOrders().Add(order)
            order.DeleteOrder()
        else:
            wp = order.Price().Number()
            break
            
    self.Wp(wp)
    self.ConsecutiveErrors = 0


def UpdateMarket(self, event):    
    if self.HedgeSMART():
        self.TradingUsed=acm.FSmartTradingInterface(self.Trading());
    else:
        self.TradingUsed=self.Trading();
    
    self.TradingSession().DeleteOrders()
    self.TradingSession().AddTradingInterface(self.TradingUsed())
    self.LastTrading = self.TradingUsed()
    self.LastMarket = self.Market()
    self.Wp(-1.0)
    self.ConsecutiveErrors = 0


def onAgentActivateClick(row, col, cell, activate, operation):  
    context = col.Context()
    tag = cell.GetEvaluator().Tag()
    hedgeTrading = acm.GetCalculatedValueFromString(row, context, 'agentPortfolioHedgerTrading', tag).Value()
    
    if not hedgeTrading:
        print ('Error: Not allowed to start Portfolio Hedger on current grouping (No hedge order book)!')
        cell.GetEvaluator().RemoveSimulation()

    portfolio = row.Portfolio()
    agentName = 'PortfolioHedger/' + portfolio.Name() + '/' + hedgeTrading.StringKey()
    agent = None

    agents = acm.GetClass('PortfolioHedger').Instances()
    for i in agents:
        if(i.IsRunning() and (i.Trading() == hedgeTrading)):
            agent = i
            break

    if activate:    
        if agent:
            print ('Error: Portfolio Hedger is already running for the selected underlying and portfolio.')
            print ('Only one Portfolio Hedger per underlying and portfolio is allowed!')
            cell.GetEvaluator().RemoveSimulation()
            return
        
        if( acm.GetCalculatedValueFromString(row, context, 'agentPortfolioHedgerKillAgentOrderSize', tag).Value() <= 0.0 ):
            print ('Error: Safety rule Kill Agent Order Size for Portfolio Hedger must be greater than zero!')
            cell.GetEvaluator().RemoveSimulation()
            return
        
        agent = acm.Trading.CreateAgent(agentName, 'PortfolioHedger', context.Name(), tag)

        if agent:
            agent.SourceObj(row)
            agent.Tag(tag)
            agent.Start()
            
    else:
        if agent:
            agent.Stop()

def onSmartActivateClick(row, col, cell, activate, operation):      
    context = col.Context()
    tag = cell.GetEvaluator().Tag()
    hedgeTrading = acm.GetCalculatedValueFromString(row, context, 'agentPortfolioHedgerTrading', tag).Value()
    agent = None

    agents = acm.GetClass('PortfolioHedger').Instances()
    for i in agents:
        if(i.IsRunning() and (i.Trading() == hedgeTrading)):
            agent = i
            break
    if None == agent:
        return
    
    UpdateMarket(agent, None)


def AgentError(self, event):
    maxFailedNbr = self.MaxNbrFailedModifications()
    if self.ConsecutiveErrors() > maxFailedNbr:
        self.ErrorHandler().OnError('Fatal', "Max number of order modification failures reached (" + str(maxFailedNbr + 1) + "), last errors:\n" + self.ErrorMessage())
        return
    
    self.HasErrors = False
