

import acm

def startYieldHedger(quoteController, trading, context, tag):
    startYieldHedger = False
    yieldTypeInstruments = acm.GetCalculatedValueFromString(quoteController, context, 'automaticHedgerYieldTypeInstruments', tag).Value()
    i = 0
    while i < yieldTypeInstruments.Size():
        instrument = yieldTypeInstruments.At(i)
        if trading.Instrument().IsKindOf(instrument):
            startYieldHedger = True
        i = i + 1
        
    return startYieldHedger

def startAutoHedger(quoteController, trading, context, tag):
    createYieldHedger = startYieldHedger(quoteController, trading, context, tag)
    if(createYieldHedger):
        agentName = 'YieldHedger - ' + str(trading)
    else:
        agentName = 'AutomaticHedger - ' + str(trading)
        
    agentEval = acm.GetCalculatedValueFromString(quoteController, context, 'automaticHedgerAgent', tag)
    agentServer = acm.GetCalculatedValueFromString(quoteController, context, 'automaticHedgerAlgoServer', tag).Value()
    agent = agentEval.Value()
    agentClass = None
    
    if agentServer:
        agentClass = 'AlgoServerHedger'
    elif createYieldHedger:
        agentClass = 'YieldHedger'
    else:
        agentClass = 'AutomaticHedger'
        
    if agent:
        if agent.IsKindOf(agentClass):
            agent.Start()
            return
        elif agent.CanBeStopped():
            agent.Stop()
        agentEval.RemoveSimulation()
   
    try:
        agent = acm.Trading.CreateAgent(agentName, agentClass, context, tag)        
        if agent: 
            agent.QuoteController(quoteController)
            
            if agentServer:
                agent.AlgoServer(agentServer)
            else:
                agent.Tag(tag)
                
            agent.Start()
            agentEval.Simulate(agent, False)
        else:
            print ('Failed to create auto hedger agent')
    except Exception as e:
        print ('Failed to create auto hedger agent: ' + str(e))
        
   
def onAgentActivateClick(quoteLevelRow, col, cell, activate, operation):
    quoteController = quoteLevelRow.QuoteController() 
    trading = quoteLevelRow.TradingInterface()
    context = col.Context()
    tag = cell.GetEvaluator().Tag()

    if activate:
        startAutoHedger(quoteController, trading, context, tag)
    else:
        agent = acm.GetCalculatedValueFromString(quoteController, context, 'automaticHedgerAgent', tag).Value()
        if agent:
            agent.Stop()

def OnInstrumentSelect(quoteLevelRow, col, cell, instrument, operation):  
    quoteController = quoteLevelRow.QuoteController() 
    trading = quoteLevelRow.TradingInterface() 
    context = col.Context()
    tag = cell.Tag()
        
    hedgeOrderBook = acm.Trading.DefaultTradingInterface(instrument)
    if (not hedgeOrderBook or not hedgeOrderBook.MarketPlace()) :
        try:
            hedgeOrderBook = acm.Trading.CreateBasketTrading(instrument)
        except:
            pass
            
    quoteSettings = quoteController.QuoteSettings()
    if quoteSettings and quoteSettings.AutomaticHedger():
        quoteSettings.AutomaticHedger().OrderBook(hedgeOrderBook)

    return False;
    
def OnOrderBookSelect(quoteLevelRow, col, cell, hedge, operation):   
    quoteController = quoteLevelRow.QuoteController()
    context = col.Context()
    tag = cell.Tag()
    hedgeInstrument = hedge.Instrument()
    
    quoteSettings = quoteController.QuoteSettings()
    if quoteSettings and quoteSettings.AutomaticHedger():
        quoteSettings.AutomaticHedger().Instrument(hedgeInstrument)
    
    return False;
