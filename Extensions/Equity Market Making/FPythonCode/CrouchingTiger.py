
import acm

def OnPrepare(self):    
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()
    if None != self.Trading():
        tradingSession.AddTradingInterface(self.Trading())
        tradingSession.AddTradingInterface(self.Trading().OrderTrading())

def TraceLog(self, message):
    if self.IsTraceEnabled() and self.Log():
        self.Log().AddStringRecord(message)

def RegisterSafetyRules(self):
    errHandler = self.ErrorHandler()             
    errHandler.RegisterCondition('safetyRuleRefPriceCheckOK', 'Information', 'Order price reasonability check failed')   
    errHandler.RegisterCondition('safetyRuleUndPriceMoveOK', 'Information', 'Underlying price move check failed')   
    

def LogBreach(self):
    if self.SafetyRulesNotOK():
        TraceLog(self, "Safety Rules breached...")
    if not self.SafetyRuleRefPriceCheckOK():
        TraceLog(self, "Reference Price set to : " + str(self.RefBasePrice()))
        TraceLog(self, "Reference Price Spread set to :" + str(self.RefPriceSpread()*2.0))
        TraceLog(self, "Reference Price Spreads set to : " + str(self.LowerLimRefPriceCheck()) + " , " + str(self.UpperLimRefPriceCheck()))        
        TraceLog(self, "SafetyRules set to : " + str(self.SafetyRulesNotOK()) + " , " + str(self.SafetyRuleRefPriceCheckOK()) + " , " + str(self.SafetyRuleRefBidPriceCheckOK()) + " , " + str(self.SafetyRuleRefAskPriceCheckOK()))
    if not self.SafetyRuleUndPriceMoveOK():
        TraceLog(self, "Underlying Price Move Exceeeded " +str(self.PriceMoveDifferenceLimit()) + " " + str(self.PriceMoveDifferenceType()))    
     
   
def OnEnterWait(self, event):      
    RegisterSafetyRules(self)

def OnOrderDelete(self, order):
    pass

def CreateBidOrder(self, event):
    bidOrder = self.TradingSession().NewOrder(self.Trading().OrderTrading())
    bidOrder.BuyOrSell = 'Buy'
    bidOrder.OrderType = 'Fill and Kill (IOC)'
    bidOrder.Price = self.SendBidOrderPrice()
    bidOrder.Account = self.CrouchingTigerAccount()
    bidOrder.Reference = self.CrouchingTigerReference()
    bidOrder.Quantity = min(min(self.SendAskOrderVolume(), self.MaxOrderQuantity()), self.MaxPos() - self.Position())
    self.TigerOrder = bidOrder
    bidOrder.SendOrder()


def CreateAskOrder(self, event):
    askOrder = self.TradingSession().NewOrder(self.Trading().OrderTrading())
    askOrder.BuyOrSell = 'Sell'
    askOrder.OrderType = 'Fill and Kill (IOC)'
    askOrder.Price = self.SendAskOrderPrice()
    askOrder.Account = self.CrouchingTigerAccount()
    askOrder.Reference = self.CrouchingTigerReference()
    askOrder.Quantity = min(min(self.SendBidOrderVolume(), self.MaxOrderQuantity()), self.MaxPos() + self.Position())
    self.TigerOrder = askOrder
    askOrder.SendOrder()
    
    
def CleanUp(self, event):
    self.TradingSession().CancelOrders()
    tag = self.Tag()
    
    acm.GetCalculatedValueFromString(self.QuoteController(), self.Context(), 'crouchingTigerActive', tag).RemoveSimulation()
 
def onAgentActivateClick(quoteLevelRow, col, cell, activate, operation):
    quoteController = quoteLevelRow.QuoteController()
    trading = quoteLevelRow.TradingInterface();
    context = col.Context()
    tag = cell.GetEvaluator().Tag()    
    instanceName = 'CrouchingTiger'+ '-' + quoteLevelRow.Instrument().Name()

    agent = getAgent(trading)
    if activate:                
        if agent and (agent.AgentStatus() == 'Running'):
            print (instanceName + ' is already running.')
            return
        agent = acm.Trading.CreateAgent(instanceName, 'CrouchingTiger', context.Name(), tag)
        if not agent:
            return 0
        agent.QuoteController(quoteController)
        agent.Tag(tag)        
        agent.Start()
        eval = acm.GetCalculatedValueFromString(quoteController, context, 'crouchingTigerAgent', tag)
        eval.Simulate(agent, 1)
        eval.Changed()
    else:        
        if agent:            
            agent.Stop()
            acm.GetCalculatedValueFromString(quoteController, context, 'crouchingTigerAgent', tag).RemoveSimulation()
               
def getAgent(trading):    
    agents = acm.GetClass('CrouchingTiger').Instances()
    for agent in agents:
        if(agent.IsRunning() and (agent.Trading() == trading)):
            return agent 
    return None


def OnSafetyBreached(self, event):
    LogBreach(self)
