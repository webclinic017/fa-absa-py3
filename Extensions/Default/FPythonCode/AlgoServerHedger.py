
import acm
import FAgent

def OnPrepare(self):
    FAgent.OnPrepare(self)

def OnEnterStart(self, event):
    self.ServerAgent(None)
    self.CurrentTheoreticalPrices(None)
    self.CurrentUnderlyingPrices(None)
    
    if self.ReferencePrice() == 'Market' or self.ReferencePrice() == 'Manual':
        self.ErrorHandler().OnError('Fatal', 'Failed to create server agent: Price type cannot be Manual or Market')
        print ('Failed to create server agent: Price type cannot be Manual or Market')
        self.AgentCanBeStarted(False)
        
def OnEnterStop(self, event):
    if self.ServerAgent():
        self.ServerAgent().Delete()

def OnServerAgentError(self, event):
    self.ErrorHandler().AddError('Fatal', 'Server error')

def OnStartServerAgentFailed(self, event):
    msg = 'Failed to start server agent'
    errors = self.CommandCompletion().Errors()
    separator = ': '
    for e in errors:
        msg = msg + separator + e.StringKey()
        separator = ', '

    self.ErrorHandler().OnError('Fatal', msg)

def CreateAlgoServerAgent(self, event):
    agent = self.AlgoServer().NewAgent(self.AlgoServerStrategy())
    agent.OrderbookId(self.Trading())
    agent.ExclusiveOwnerSession(True)
    agent.RemoveOnBrokenSession(True)
    self.ServerAgent(agent)
    try:
        self.UpdateParameters(event)
        agent.Start()
    except Exception as e:
        self.ErrorHandler().OnError('Fatal', 'Failed to create server agent: ' + str(e))

def UpdateCurrentVectors(self, event):
    theoreticalPrices = self.PendingTheoreticalPrices()
    underlyingPrices = self.PendingUnderlyingPrices()
    if theoreticalPrices and underlyingPrices:
        self.CurrentTheoreticalPrices(theoreticalPrices)
        self.CurrentUnderlyingPrices(underlyingPrices)
    self.PendingTheoreticalPrices(None)
    self.PendingUnderlyingPrices(None)
   
def UpdateParameters(self, event):
    try:
        agent = self.ServerAgent()
        agent.AccountId(self.HedgeAccount())
        agent.Reference(self.HedgeReference())
        agent.MinimumQuantity(self.MinimumQuantity())
        agent.CalculationType(self.CalculationType())
        agent.Aggressive_Order_Part(self.AggressivePart())
        agent.SMARTTradingStrategy(self.SmartTradingStrategy())
        agent.ReferencePrice(self.ReferencePrice())
        agent.TickOffset(self.TickOffset())
        agent.Underlying_OrderbookId(self.HedgeOrderBook())
        self.UpdateVectors(event)
        if event.StringKey() == 'updateServerParameters':
            agent.Commit()
    except Exception as e:
        if self.Log():
            self.Log().AddStringRecord('Failed to update parameters: ' + str(e))
        if event.StringKey() != 'updateServerParameters':
            raise e

def UpdateVectors(self, event):
    try:
        agent = self.ServerAgent()
        theoreticalPrices = self.PendingTheoreticalPrices()
        underlyingPrices = self.PendingUnderlyingPrices()
        agent.Theoretical_price_1(theoreticalPrices[0])
        agent.Theoretical_price_2(theoreticalPrices[1])
        agent.Theoretical_price_3(theoreticalPrices[2])
        agent.Theoretical_price_4(theoreticalPrices[3])
        agent.Theoretical_price_5(theoreticalPrices[4])
        agent.Theoretical_price_6(theoreticalPrices[5])
        agent.Theoretical_price_7(theoreticalPrices[6])
        agent.Theoretical_price_8(theoreticalPrices[7])
        agent.Theoretical_price_9(theoreticalPrices[8])
        agent.Underlying_price_1(underlyingPrices[0])
        agent.Underlying_price_2(underlyingPrices[1])
        agent.Underlying_price_3(underlyingPrices[2])
        agent.Underlying_price_4(underlyingPrices[3])
        agent.Underlying_price_5(underlyingPrices[4])
        agent.Underlying_price_6(underlyingPrices[5])
        agent.Underlying_price_7(underlyingPrices[6])
        agent.Underlying_price_8(underlyingPrices[7])
        agent.Underlying_price_9(underlyingPrices[8])
        if event.StringKey() == 'updatePriceVectors':
            agent.Commit()
    except Exception as e:
        if self.Log():
            self.Log().AddStringRecord('Failed to update price vectors: ' + str(e))
        if event.StringKey() != 'updatePriceVectors':
            raise e

def LogError(self, event):
    currentError = self.CurrentError()        
    if self.Log():
        self.Log().AddStringRecord(currentError.AsString())
        
    if event.StringKey() == 'notFatalError':
        self.CurrentError(None)
    else:
        self.ErrorHandler().OnError('Fatal', 'Incorrect parameter chosen: Price type cannot be Manual or Market')
        print ('Fatal error: ' + currentError.AsString())


        

