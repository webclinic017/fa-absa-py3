
import acm
import FAgent

def OnPrepare( self):
    FAgent.OnPrepare( self)
    
    if self.TradeSource() is None:
        self.TradeSource(               acm.Trading.CreateTradeTickerSource(None, self.TradingSession().StoredTrades(), -1, False))
    if self.OrderPositions() is None:
        self.OrderPositions(            acm.FOrderPositions( self.TradingSession().Orders()))        
    if self.PendingCommands() is None:
        self.PendingCommands(           acm.FList())
    if self.PriceMonitors() is None:
        self.PriceMonitors(             acm.FDependentArray())
    if self.DoneOrDeletedPriceMonitors() is None:
        self.DoneOrDeletedPriceMonitors(_GetPriceMonitors( self, acm.Filter.SimpleOrQuery( 'FPriceMonitor', ['Order.IsOrderDone', 'Order.IsOrderDeleted'], None, [True, True])))
    if self.BreachedPriceMonitors() is None:
        self.BreachedPriceMonitors(     _GetPriceMonitors( self, acm.Filter.SimpleAndQuery('FPriceMonitor', ['Order.IsOrderActive', 'IsOutsideTarget', 'TradingInterface.Status.EnterOrder'], None, [True, True, True])))
    if self.SendablePriceMonitors() is None:
        self.SendablePriceMonitors(     _GetPriceMonitors( self, acm.Filter.SimpleAndQuery('FPriceMonitor', ['Order.IsOrderInactive', 'IsTargetValid', 'TradingInterface.Status.EnterOrder'], None, [True, True, True])))

def OnCommandError(self, command):
    errors = command.Errors()
    for e in errors:
        if e.IsMarketError():
            if e.Type() == 'TimeStamp':
                continue
        self.ErrorHandler().OnError('Fatal', e.AsString())
        
def OnOrderDelete(self, order):
    pass
    
    
""" xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Actions xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

def DeleteOrders( self, event):
    self.TradingSession().DeleteOrders()

def HandleDoneOrDeletedPriceMonitors( self, event):
    doneOrDeleted       = acm.FArray()
    doneOrDeleted.AddAll(self.DoneOrDeletedPriceMonitors())
    self.PriceMonitors().RemoveAll( doneOrDeleted)

def HandleErrors( self, event):
    self.ErrorHandler().OnError( 'Fatal', self.ErrorMessage())

def HandleSendablePriceMonitors( self, event):
    _UpdatePricesAndSend( self, self.SendablePriceMonitors())

def NotApplicable( self, event):
    self.ErrorHandler().OnError( 'Information', 'Algorithm is not applicable for selected row')

def ProcessTrade(self, event):
    tradeSource = self.TradeSource()
    filledQty = self.LastFilledQuantity()
    while not tradeSource.IsEmpty():
        filledQty += abs(tradeSource.Get().Quantity())
    self.LastFilledQuantity(filledQty)
              
def RemoveProcessedCommand( self, event):
    self.PendingCommands().Remove( self.ProcessedCommand())    
    
def UpdateErrorFromCommand( self, event):
    print ('UpdateErrorFromCommand')
    
def UpdateOrders(self, event):
    instructions                = self.TradingInstructions()
    
    if instructions is None:
        return
        
    instruments                 = instructions.Instruments()
    orderPositions              = self.OrderPositions()
            
    try:
        for instrument in instruments:
            quantity            = instructions.GetQuantity(instrument)
            trading           = _GetTradingInterface(self, instrument)
                                     
            if quantity > 0:
                roundQty            = trading.NearestRoundLot(quantity)
                _UpdatePosition( self, instrument, 'Buy', roundQty, orderPositions.OrdersIn(instrument), trading)
            elif quantity < 0:
                roundQty            = trading.NearestRoundLot(-quantity)
                _UpdatePosition( self, instrument, 'Sell', roundQty, orderPositions.OrdersIn(instrument), trading)
            else:
                _Trace(self, 'No position update in ' + instrument.StringKey())                
    except Exception as e:
        self.ErrorMessage( str( e))

def UpdatePrices( self, event):
    _UpdatePricesAndSend( self, self.BreachedPriceMonitors())



""" xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Helper functions xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
def _AddPendingCommand( self, cmd):    
    self.PendingCommands().Add(cmd)    
    

def _CanEnterOrder(self, trading):
    return trading.Status().EnterOrder()
    
def _CreatePriceMonitor( self, trading, order):
    priceFeed           = trading.PriceFeed()
    priceType           = self.PriceType()
    priceQuantity       = _GetDefaultValue(self, trading, 'portfolioHedgerPriceSourceQuantity')
    priceOffsetTicks    = None
    
    valueSource         = None
    valueSourceQuantity = 0.0
    priceOffset         = None
    
    if priceType == 'Join':
        valueSource = order.IsBuy() and priceFeed.AverageBidPrice() or priceFeed.AverageAskPrice()
        priceOffsetTicks = _GetDefaultValue(self, trading, 'portfolioHedgerPriceJoinOffset')
    elif priceType == 'Match':
        valueSource = order.IsBuy() and priceFeed.AverageAskPrice() or priceFeed.AverageBidPrice()
        priceOffsetTicks = _GetDefaultValue(self, trading, 'portfolioHedgerPriceMatchOffset')
    else:
        valueSource = priceFeed.LastPrice()
        priceOffsetTicks = _GetDefaultValue(self, trading, 'portfolioHedgerPriceLastOffset')
    
    if priceQuantity != None:
        valueSourceQuantity = priceQuantity
        
    if priceOffsetTicks != None and priceOffsetTicks != 0:
        priceOffset = acm.FPriceTickOffset( priceOffsetTicks)
        
    monitor = acm.Trading.CreatePriceMonitor( order, valueSource, valueSourceQuantity, priceOffset)
    
    # order book status is used in filters for BreachedPriceMonitors and 
    # SendablePriceMonitors so we need a dependency for it.
    status = monitor.TradingInterface().Status()
    status.AddDependent(monitor)
    return monitor

def _GetDefaultValue( self, owner, name):
    try:
        val = owner.GetDefaultValueEx( name, self.Context())
        if val == '':
            return None
        return val
    except Exception as e:
        _Trace(self, 'Failed to retrieve default value ' + name)
        return None

def _GetTradingInterface( self, instrument):
    trading = acm.Trading.DefaultTradingInterface( instrument)
    
    if trading != None and self.Smart():
        try:
            smartTrading = acm.FSmartTradingInterface( trading )
            
            if not smartTrading.ImTradingInterface():
                raise Exception('IM order book not found')
            return smartTrading
            
        except Exception as e:
            _Trace(self, 'SMART could not be created for ' + trading.StringKey() + ': ' + str(e))

    if trading is None or trading.IsKindOf( 'FAdsTradingInterface'):
        raise Exception('Order book could not be determined for ' + instrument.StringKey())
    
    return trading

    
def _GetPriceMonitors( self, filter):
    monitors = acm.FFilteredSet( self.PriceMonitors())
    monitors.Filter( filter)
    return monitors


def _SendOrder( self, trading, buyOrSell, quantity):
    order = self.TradingSession().NewOrder( trading)
    
    order.BuyOrSell( buyOrSell)
    
    quantity = trading.NearestRoundLot(quantity)  
    
    order.Quantity( quantity)
    order.Account( self.Account())
    order.Reference( self.Reference())
    order.RemoveOnBrokenSession( True)
    order.IsIndependentModifyEnabled( True)
    order.HedgeOrder(True)
    
    if self.Smart():
        order.TradingStrategy( self.TradingStrategy())
        order.SetStartAgent( True)
        
    monitor = _CreatePriceMonitor( self, trading, order)
    self.PriceMonitors().Add( monitor)
    _UpdatePriceAndSend( self, monitor)

 
def _Trace( self, message):
    if self.IsTraceEnabled():
        log = self.Log()
        if log:
            log.AddStringRecord( message)
       
def _UpdatePosition( self, instrument, buyOrSell, quantity, orders, trading):    
    
    finalQty = quantity
    
    _Trace(self, 'Position update: ' + str( buyOrSell) + ' ' + str(finalQty) + ' in ' + instrument.StringKey())

    if orders:
        for order in orders:
            if acm.Math.AlmostZero( finalQty, 1e-10):
                break
            
            if (order.IsOrderActive() or order.IsOrderInactive()) and order.BuyOrSell() != buyOrSell:                                
                orderQty = order.Quantity()
                cmd = None                
                if orderQty > finalQty:                    
                    finalQty = orderQty - finalQty
                    order.Quantity(finalQty)
                    if order.IsOrderActive():
                        cmd = order.SendOrder()
                    finalQty = 0
                else:
                    cmd = order.DeleteOrder()
                    finalQty = finalQty - orderQty                                        
               
                if cmd is not None:
                    _AddPendingCommand( self, cmd)
            
    if finalQty > 0:
        _SendOrder( self, trading, buyOrSell, finalQty)

            
def _UpdatePriceAndSend( self, monitor):
    if not monitor:
        _Trace(self, 'Received no monitor')
        return False
    if not _CanEnterOrder(self, monitor.TradingInterface()):
        _Trace(self, monitor.TradingInterface().StringKey() + ': Enter order not allowed in current phase')
        return False
    if not monitor.IsTargetValid():
        _Trace(self, monitor.Order().StringKey() + ': Target not valid')
        return False
        
        
    try:
        order       = monitor.Order()
        target      = monitor.TargetPrice()
        order.Price( target)
        _AddPendingCommand( self, order.SendOrder())
        return True
    except Exception as e:
        _Trace(self, 'Error while updating order price: ' + str(e))
    return False


def _UpdatePricesAndSend( self, monitors):
    for monitor in monitors:
        _UpdatePriceAndSend( self, monitor)

def onAgentActivateClick(row, col, cell, activate, operation):  

    if activate:            
        context = col.Context()
        tag = cell.GetEvaluator().Tag()
        portfolio = row.Portfolio()                
        agentName = 'PortfolioYieldHedger/' + portfolio.Name() + '/' + row.StringKey()
        agent = acm.Trading.CreateAgent(agentName, 'GenericPortfolioHedger', context.Name(), tag)        
        if agent:
            agent.InstrumentAndTrades(row)
            agent.Start()
            

    
