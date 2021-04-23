
import acm

"""
    Default behavior - override in sub classes
"""

def ConvertFromOrderBookToTrading(self):
    if self.IsKindOf('FOrderBook'):
        return self.TradingInterface()
    else:
        return self


def OnPrepare(self):
    pass

def OnPrepared(self):
    pass
    
def OnCommandError(self, command):
    errors = command.Errors()
    for e in errors:
        if e.IsMarketError():
            if e.Type() == 'TimeStamp':
                continue
        self.ErrorHandler().OnError('Fatal', e.AsString())
        
def OnOrderDelete(self, order):
    # Stop agent if order is deleted by external source and not due to a broken session.
    if (not order.IsDeleteIssuedByOwner()) and (not order.IsDeletedOnBrokenSession()) :
        self.ErrorHandler().OnError('Fatal', 'Order deletion not issued by agent')

def OnTrade(self, order, trade):
    pass
    
def PrepareManualOrder(self, order):
    pass
    


"""
    Button actions
"""
def showStartStopButtons(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        try:
            rowObject = cell.RowObject()
            if rowObject.IsKindOf(acm.FAgentRow):
                return True
            agent = rowObject.Agent()
            
            if(rowObject.IsKindOf(acm.FOwnOrder)):
                if(rowObject.IsKindOf(acm.FSalesOrder) or rowObject.IsKindOf(acm.FOrderProgram)):
                    return True
                elif agent:
                    strategy = acm.FAlgoTradingStrategy[agent.Class().DisplayName()]
                    if strategy:
                        if rowObject.IsKindOf(strategy.OrderClass()):
                            return True
                        return False
            
            
            return None != agent
        except:
            pass
    return False

class AgentCmd:
    
    def _accept(self, agent):
        raise NotImplementedError
        
    def _collect(self, row):
        if row.IsKindOf('FOrderProgram'):
            orders = row.OwnOrders()
            for o in orders:
                self._collect(o)
        else:
            agent = row.Agent()
            if agent:
                self._accept(agent)
    
    def _execute(self, shell):
        raise NotImplementedError
    
    def execute(self, shell, row):
        self._collect(row)
        self._execute(shell)
        
        
class AgentStartCmd(AgentCmd):
    def __init__(self):
        self.startable = acm.FArray()
        
    def _accept(self, agent):
        if agent.CanBeStarted():
            self.startable.Add(agent)
            
    def _execute(self, shell):
        if not self.startable.IsEmpty():
            acm.Agents.StartAgents(shell, self.startable)


class AgentStopCmd(AgentCmd):
    def __init__(self):
        self.stoppable = acm.FArray()
        
    def _accept(self, agent):
        if agent.CanBeStopped():
            self.stoppable.Add(agent)
            
    def _execute(self, shell):
        if not self.stoppable.IsEmpty():
            acm.Agents.StopAgents(shell, self.stoppable)
            

class AgentStartStopCmd(AgentCmd):
    def __init__(self):
        self.startable = acm.FArray()
        self.stoppable = acm.FArray()
        
    def _accept(self, agent):
        if agent.CanBeStopped():
            self.stoppable.Add(agent)
        elif agent.CanBeStarted():
            self.startable.Add(agent)
            
    def _execute(self, shell):
        if not self.startable.IsEmpty():
            acm.Agents.StartAgents(shell, self.startable)    
        if not self.stoppable.IsEmpty():
            acm.Agents.StopAgents(shell, self.stoppable)
        
        
def agent_do(invokation_info, command):
    sheet = invokation_info.ExtensionObject().ActiveSheet()
    button = invokation_info.Parameter('ClickedButton')
    shell = invokation_info.Parameter('shell')
    if button:
        row = button.RowObject()
        command.execute(shell, row)
        
def startAgent(agent):
    if agent and agent.CanBeStarted():
        agent.Start()
        
def stopAgent(agent):
    if agent and agent.CanBeStopped():
        agent.Stop()
                   
def onStartButton(invokation_info):
    agent_do(invokation_info, AgentStartCmd())

def onStopButton(invokation_info):
    agent_do(invokation_info, AgentStopCmd())

def onStartStopButton(invokation_info):
    agent_do(invokation_info, AgentStartStopCmd())

def showStopButton(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        try:
            agent = cell.RowObject().Agent()
            return None != agent
        except:
            pass
    return False    
    
"""
    Old stuff
"""          
def makeSound(soundFileName):
    if soundFileName == '':
        return
    from winsound import PlaySound, SND_ASYNC
    try:
        PlaySound(soundFileName, SND_ASYNC)
    except:
        #print ('(Could not play sound.)')
        pass
 
