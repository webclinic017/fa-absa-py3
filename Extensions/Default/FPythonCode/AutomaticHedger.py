from __future__ import print_function
import acm

def CalculateSignedHedgeQuantity(self):
    trade = self.CurrentTrade()
    delta = self.HedgeDelta()
    hedgeOrderBook = self.HedgeOrderBook()
    signedTradeQuantity = 0
    
    if trade.BuySell() == "Buy":
        signedTradeQuantity = abs(trade.Quantity())
    elif trade.BuySell() == "Sell":
        signedTradeQuantity = - abs(trade.Quantity())
    else:
        self.HedgeOrder = None
        self.SmartOrder = None
        raise Exception
    
    signedHedgeQuantity = delta * signedTradeQuantity * trade.Instrument().ContractSize() / hedgeOrderBook.Instrument().ContractSize()
    
    return signedHedgeQuantity

def CleanUp(self, event):
    self.TradingSession().DeleteOrders()
    tag = self.Tag()
    acm.GetCalculatedValueFromString(self.QuoteController(), self.Context(), 'automaticHedgerActive', tag).RemoveSimulation()

def CreateAggressiveOrder(self, buyOrSell, quantity):
    self.HedgeOrder(None)
    trading = self.HedgeOrderBook()
    order = CreateOrder(self, buyOrSell, quantity, trading)
    if order is None:
        LogError(self, "Failed to create aggressive order for order book: " + GetOrderBookLogInfo(self, trading))
        return
        
    self.HedgeOrder(order)

def CreateHedgeOrder(self, event):
    minRoundLots = self.HedgeMinimumRoundLots()
    hedgeOrderBook = self.HedgeOrderBook()
    
    try:
        signedHedgeQuantity = self.CalculateSignedHedgeQuantity()
    except Exception as e:
        self.HedgeOrder = None
        self.SmartOrder = None
        log = self.Log()
        if log:
            logString = 'ERROR> Automatic Hedger failed to create hedge: ' + str(e)
            log.AddStringRecord(logString)
        return
        
    hedgeQuantity = abs(signedHedgeQuantity)
    
    aggressiveQty = hedgeQuantity * self.AggressiveOrderPart()
    smartQty = hedgeQuantity - aggressiveQty
    
    buyOrSell = 'Buy'
    if signedHedgeQuantity > 0:
        buyOrSell = 'Sell'
  
    #Only hedge if total quantity is greater than minRoundLots.
    if((hedgeQuantity / hedgeOrderBook.RoundLot()) < minRoundLots):
        smartQty = 0
        aggressiveQty = 0
    
    #If the smaller of the two parts is smaller than minRoundLots, put all on the greater part.
    if ((smartQty / hedgeOrderBook.RoundLot()) < minRoundLots) and (smartQty<=aggressiveQty):
        aggressiveQty += smartQty
        smartQty=0
    if ((aggressiveQty / hedgeOrderBook.RoundLot()) < minRoundLots) and (aggressiveQty<smartQty):
        smartQty += aggressiveQty
        aggressiveQty=0
    
    if aggressiveQty > 0:
        CreateAggressiveOrder(self, buyOrSell, aggressiveQty)
    else:
        self.HedgeOrder = None
        
    if smartQty > 0:
        CreateSMARTOrder(self, buyOrSell, smartQty)
    else:
        self.SmartOrder = None

    if aggressiveQty <= 0 and smartQty <= 0:
        log = self.Log()
        if log:
            logString = 'INFO> Automatic Hedger did not send hedge order because hedge quantity was below minimum trade size.\n'
            logString += '    Aggressive Quantity = ' + str(aggressiveQty) + '\n'
            logString += '    SMART Quantity = ' + str(smartQty) + '\n'
            log.AddStringRecord(logString)

def CreateOrder(self, buyOrSell, quantity, trading):
    order = self.TradingSession().NewOrder(trading)
    if order is None:
        LogError(self, "Failed to create order for order book: " + GetOrderBookLogInfo(self, trading))
        return None
    
    if self.HedgePriceType() == 'Manual':
        order.Release()
    order.BuyOrSell(buyOrSell)
    order.Quantity(trading.NearestRoundLot(quantity))
    order.OrderType = self.HedgeOrderType()
    order.Account = self.HedgeAccount()
    order.Reference = self.HedgeReference()
    order.IsIndependentModifyEnabled(True)
    order.HedgeOrder(True)
    if SetOrderPrice(self, order):  
        LogHedgerInformation(self, order, self.CurrentTrade())  
        order.LoadOrder()
        return order
    else:
        LogError(self, "Failed to create order because no price was available for order book: " + GetOrderBookLogInfo(self, trading))
        return None

def CreateSMARTOrder(self, buyOrSell, quantity):
    self.SmartOrder(None)
    CreateSMARTTradingInterface(self)
    
    trading = self.SmartTrading() 
    if trading is None:
        LogError(self, "Missing SMART order book for hedge order book: " + GetOrderBookLogInfo(self, self.HedgeOrderBook()))
        return
        
    if not trading.IsAvailable():
        LogError(self, "Internal market is not available for SMART order book: " + GetOrderBookLogInfo(self, trading))
        return
    
    order = CreateOrder(self, buyOrSell, quantity, trading)
    if order is None:
        LogError(self, "Failed to create SMART order for order book: " + GetOrderBookLogInfo(self, trading))
        return
    
    order.TradingStrategy(self.HedgeTradingStrategy())
    self.SmartOrder(order)
    
    if self.ExtendedLogEnabled() and order.TradingStrategy():
        info =  'SMART Order, Trading Strategy: ' + str(order.TradingStrategy())
        LogInfo(self, info)

def CreateSMARTTradingInterface(self):
    if None == self.SmartTrading():
        trading = None
        if self.HedgeInstrumentIsCombination():
            trading = acm.Trading.createSmartBaskedTrading(self.HedgeInstrument())
        else:
            trading = acm.FSmartTradingInterface(self.HedgeOrderBook())
        self.SmartTrading(trading)
        if None != self.SmartTrading():
            tradingSession = self.TradingSession()
            tradingSession.AddTradingInterface(self.SmartTrading())
        else:
            LogError(self, "Failed to create SMART trading interface for order book: " + GetOrderBookLogInfo(self, trading))

def CreateTradingInterface(self, event):
    self.CurrentHedgeTradingStrategy(self.HedgeTradingStrategy())
    self.CurrentAggressiveOrderPart(self.AggressiveOrderPart())
    
    tradingSession = self.TradingSession()
    tradingSession.RemoveOrderBooks()
    
    if None != self.Trading():
        tradingSession.AddTradingInterface(self.Trading())

def CreateTradeFilter(self, event):
    trading = self.Trading()
    tf = acm.FTradeFilter()
    tf.Traders([acm.UserName()])
    tf.SetFromTimeFromNow()
    tf.TradingInterfaces([trading])
    tf.ExcludeNonQuoteOrAutoTrades(True)
    tf.DealSubscriptionTypes("Private")
    
    op = tf.Query()
    
    if self.HedgeAccountFilter():
        op.AddAttrNodeString('AccountId', str(self.HedgeAccountFilter()), 'RE_LIKE_NOCASE')  
        
    if self.HedgeReferenceFilter():
        op.AddAttrNodeString('ReferenceId', str(self.HedgeReferenceFilter()), 'RE_LIKE_NOCASE')  
        
    self.TradeFilter(tf)

def InternalMatch(self, order):
    price = order.Price()
    trading = order.TradingInterface()
    if order.IsBuy():
        level = trading.PriceFeed().AskPriceDepth().LevelOfPrice(price, False)
        for i in range(level):
            if trading.PriceFeed().AskPriceDepth().ContainsOrgOrders(i, -1, -1):
                return True
    else:        
        level = trading.PriceFeed().BidPriceDepth().LevelOfPrice(price, False)
        for i in range(level):
            if trading.PriceFeed().BidPriceDepth().ContainsOrgOrders(i, -1, -1):
                return True
    return False

def SendHedgeOrder(self, event):
    if self.HedgePriceType() != 'Manual':
        hedgeOrder = self.HedgeOrder()
        if hedgeOrder != None:
            SendOrder(self, hedgeOrder)
        smartOrder = self.SmartOrder()
        if smartOrder != None:
            SendOrder(self, smartOrder)
    
def SendOrder(self, order):
    trading = order.TradingInterface()
    if not trading.IsAvailable():
        log = self.Log()
        if log:
            logString = 'INFO> Automatic Hedger did not send hedge order because the hedge order book is not connected.'
            log.AddStringRecord(logString)
            return
    if self.AllowInternalTrade():
        order.HedgeOrder(True)
        order.SendOrder()
    elif InternalMatch(self, order):
        log = self.Log()
        if log:
            logString = 'INFO> Automatic Hedger did not send hedge order because it could cause an internal trade to take place.\n'
            logString += '    hedge order = ' + str(order) + '\n'
            log.AddStringRecord(logString)
    else:
        order.HedgeOrder(True)
        order.SendOrder()

def SetOrderPrice(self, order):
    price = 0
    
    if self.HedgePriceType() == 'Join' or self.HedgePriceType() == 'Best' or self.HedgePriceType() == 'Match' or self.HedgePriceType() == 'Match All':
        price = order.GetPrice(self.HedgePriceType())
    elif self.HedgePriceType() == 'Market':
        MarketPrice = acm.GetFunction('marketPrice', 0)
        price = MarketPrice()
    else:
        price = float(order.TradingInterface().PriceFeed().LastPrice().Get())
    
    if order.TradingInterface().PriceFeed().IsValidPrice(price):
        if self.TickOffset() != 0 and self.HedgePriceType() != 'Market':
            price = TickUpDown(self, order, self.TickOffset(), price)
        order.Price = price
        return True
        
    return False

def TickUpDown(self, order, ticks, price):
    result = price
    tickList = self.HedgeOrderBook().TickSizeList()
    if ticks != 0:
        tickUp = order.IsBuy()
        if ticks < 0:
            tickUp = not tickUp
        result = order.TickUpDown(tickUp, abs(ticks), price)
    return result


# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### #
#
#                         L O G G I N G,   E T C .
#
# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### #

def OnPrepare(self):
    self.CurrentHedgeTradingStrategy(None)
    self.CurrentAggressiveOrderPart(0)
        
def OnPrepared(self):
    pass
    
def OnOrderDelete(self, order):
    pass
    
def LogString(self, prefixString, logString):
    logString = prefixString + logString
    print (logString)
    log = self.Log()
    if log:
        log.AddStringRecord(logString)
    
def LogError(self, errorString):
    LogString(self, "ERROR - Automatic Hedger> ", errorString)

def LogInfo(self, errorString):
    LogString(self, "INFO - Automatic Hedger> ", errorString)

def GetOrderBookLogInfo(self, trading):    
    logString = trading.ExternalId() and trading.ExternalId() or "[Not available]"
    logString += ". Market: "
    logString += trading.MarketPlace() and trading.MarketPlace().Name() or "[Not available]"
    return logString
    
def LogHedgerInformation(self, order, trade):
    if not self.ExtendedLogEnabled():
        return
    
    hedgerInfo = 'Order/Trade Information'

    trading = self.HedgeOrderBook()
    if trading is not None and trading.Instrument() is not None and self.HedgeMarket() is not None:
        hedgerInfo += '\n\tHedge Order Book: '                          + str(trading)                             
        hedgerInfo += '\n\tHedge Order Book Instrument Contract Size: ' + str(trading.Instrument().ContractSize()) 
        hedgerInfo += '\n\tHedge Market Place: '                        + self.HedgeMarket().StringKey()                 
        hedgerInfo += '\n\tHedge Price Type: '                          + str(self.HedgePriceType())               
        hedgerInfo += '\n\tHedge Delta: '                               + str(self.HedgeDelta())                   
        hedgerInfo += '\n\tHedge Minimum Round Lots: '                  + str(self.HedgeMinimumRoundLots())   
    
    orderInfoText = '\n\tOrder Information'
    if order is not None:
        orderInfoText += '\n\tBuy Or Sell: '            + str(order.BuyOrSell())        
        orderInfoText += '\n\tPrice: '                  + str(order.Price())            
        orderInfoText += '\n\tQuantity: '               + str(order.Quantity())             
        orderInfoText += '\n\tOrder type: '             + str(order.OrderType())        
        orderInfoText += '\n\tAccount: '                + str(order.Account())          
        orderInfoText += '\n\tReference: '              + str(order.Reference())    
        
    tradeInfoText = '\n\tTrade Information'
    if trade is not None and trade.Instrument() is not None:        
        tradeInfoText += '\n\tTrade Quantity: '                 + str(trade.Quantity())
        tradeInfoText += '\n\tBuy or Sell: '                    + str(trade.BuySell()) 
        tradeInfoText += '\n\tTrade Instrument Contract Size: ' + str(trade.Instrument().ContractSize()) 
                        
    info = hedgerInfo + orderInfoText + tradeInfoText        
    LogInfo(self, info)
