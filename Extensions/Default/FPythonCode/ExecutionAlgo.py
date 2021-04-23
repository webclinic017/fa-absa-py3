import acm
import random
import time
import math

import datetime
import FSliceExtrapolation
import FSlicesAndDuration
import ExecutionAlgoOrder


timeFormatter = acm.FDateTimeFormatter('TimeOnly')
ZERO_QTY_EPSILON = 1e-4
 
def Version(self):
    version = 'Version 3.10.9'
    TraceLog(self, version)
    TraceLog(self, 'Time Variables are in UTC')

def AsDays(datetime):
    return acm.Time.NumberOfUtcDays(acm.Time.UtcToLocal(datetime))

def DateTimeCmp(dt1, dt2):
    dt1Days = AsDays(dt1)
    dt2Days = AsDays(dt2)
    if dt1Days < dt2Days:
        return -1
    elif dt1Days > dt2Days:
        return 1
    return 0
    
def FatalError(self, message):
    self.ErrorHandler().OnError('Fatal', message)
    self.BaseOrder().SetAlgoAgentState('Agent Error', message)
    
def SetAgentInfo(self, message):
    currentInfo = self.BaseOrder().AlgoTradingInstruction().AgentModifyReason()
    if message != currentInfo:
        self.BaseOrder().SetAlgoAgentState('Agent Executing', message)

def ClaimBaseOrder(self, event):
    self.PendingCommand(self.BaseOrder().SetAlgoAgentState('Agent Executing', self.StartInfo()))

def ClearCurrentOrder(self, event):
    if self.CurrentOrder():
        self.CurrentOrder(None)
        self.CurrentOrderQty(0.0)
        self.CurrentTrigger(None)
    
def ClearNextSlice(self, event):
    self.NextSliceOrder(None)
    self.NextSliceQuantity(0)
    
def CreateNewOrder(self, price, quantity, isInitialFillOrder):
    order = None
    if quantity <= 0:
        TraceLog(self, 'ZERO QTY NOT ACCEPTED')
        return order

    if True == isInitialFillOrder:
        strategy = self.OrderRoutingInitialFill()
    else:
        strategy = self.OrderRouting()
        
    if (None == strategy) or ("None" == strategy.StringKey()):        
        order = self.TradingSession().CreateExecutionOrder(self.BaseOrder(), True)
    else:
        order = self.TradingSession().CreateExecutionOrder(self.BaseOrder(), False)
        order.TradingStrategy(strategy)
        order.AlgoTradingInstruction().StartAgent(True)
        TraceLog(self, 'Adding Trading Strategy: ' + strategy.StringKey())
        
    order.Price(price)
    order.Quantity(quantity)    
    order.RemoveOnBrokenSession(True)

    if '' == order.Account():        
        account = GetDefaultValue(self, 'ownOrderAccount')
        if '' != account:
            order.Account = account
    if '' == order.Reference():
        reference = GetDefaultValue(self, 'ownOrderReference')        
        if '' != reference:
            order.Reference = reference
            
    return order

def DeleteCurrentOrder(self, event):
    if self.CurrentOrderActive():
        self.PendingCommand(self.CurrentOrder().DeleteOrder())
        TraceLog(self, 'pendingCommand = DeleteOrder')
    
def DeleteOrders(self, event):
    self.PendingCommand(self.TradingSession().DeleteOrders(True))
    TraceLog(self, 'pendingCommand = DeleteOrders')

def GetExtendedTriggerInfo(refType, offset):
    dOffset = 0.0
    if type(offset) is float:
        dOffset = offset
    else:
        dOffset = offset.Number()  
          
    info = ': ' + refType

    if dOffset > 0:
        info = info + ' +'
    else:
        info = info + ' '    

    return info + acm.Get('formats/Price').Format(offset)

def GetDefaultValue(self, name):
    return self.BaseTradingInterface().GetDefaultValueEx(name, self.Context())
    
def GetLimitReason(self):
    limitReason = ''
    if self.LimHighLowPriceIsExceeded():
        limitReason = ' (limit High/Low: ' + str(self.LimHighLow()) + ')'
    elif self.LimMaxPriceDiffTraderIsExceeded():
        limitReason = GetMaxPriceLimitReason(self)
    elif self.LimSlicePriceIsExceeded():
        limitReason = ' (limit ' + str(self.LimSlicePrice()) + ')'
    else:
        limitReason = ' (limited by price restriction)'
        
    return limitReason

def GetMaxPriceLimitReason(self):
    arPrc   = 0.0
    maxDiff = round(self.LimMaxPriceDiffTrader() * 100, 1)
    ppTA    = self.BaseOrder().PrePostTradeAnalysis()
    
    if ppTA:
        arPrc = ppTA.ArrivalPrice()
     
    return ' (limit MaxPriceDiff: ' +str(maxDiff)+ '% from Arrival ' +str(arPrc)+')'

    
def GetPrice(self, event):
    return self.TargetPrice()

def IsMultiMarket(self):
    if self.VolumeFeedMarketSourceValid() == "Home market":
        return False
    else:
        return True
    
    
def AnyQuantityLeftToExecute(self):
    completedOrdersSumUpToTotalQty = acm.Math.AlmostEqual(self.VolumeDoneFromCompletedOrders(), self.GoalVolume())
    noBalanceLeftToExecute         = acm.Math.AlmostEqual(self.Balance(), 0.0)
    remainingQtyZero               = acm.Math.AlmostEqual(self.ExecutionPlan().RemainingQuantity(), 0.0)
    
    TraceLog(self, "completedOrdersSumUpToTotalQty: "+str(completedOrdersSumUpToTotalQty)+" noBalanceLeftToExecute: "+str(noBalanceLeftToExecute)+" remainingQtyZero: "+str(remainingQtyZero))
    if remainingQtyZero or completedOrdersSumUpToTotalQty or noBalanceLeftToExecute or self.BaseOrderDone() :
        return False
    else:
        return True

def RandomizeQuantity(self, quantity, slices, remainingQuantity):

    result = 0
    roundlot = self.TradingInterface().RoundLot()
    roundlots = quantity / roundlot
    remainingRoundlots = remainingQuantity / roundlot
    
    if slices == 1:
        TraceLog(self, 'Only one slice; use all quantity: ' + str(quantity))
        result = quantity
    elif slices > 1:
        halfQty = remainingQuantity / 2
        avgQty = quantity / slices
        delta = avgQty * self.SliceSizeRange()
        
        if halfQty < (avgQty - delta) or halfQty < roundlot:
            TraceLog(self, 'Quantity cannot be split; using remaining quantity')
            result = remainingQuantity
        elif remainingQuantity <= (avgQty + delta):
            TraceLog(self, 'Remaining quantity less than max slice; using remaining quantity')
            result = remainingQuantity
        else:
            randomQty = random.uniform(avgQty - delta, avgQty + delta)
            TraceLog(self, 'Random quantity: ' + str(randomQty))
            result = ExecutionAlgoOrder.RoundQuantity(randomQty)
            TraceLog(self, 'Rounded quantity: ' + str(result))
                
    if result > remainingQuantity:
        TraceLog(self, "Quantity exceeds remaining quantity: " + str(result))
        result = remainingQuantity
    
    return self.TradingInterface().PrevRoundLot(result + 0.001) 


def GetNewSliceQuantity(self):

    executionPlan = self.ExecutionPlan()
    quantity      = executionPlan.CurrentPhaseQuantity()
    slices        = executionPlan.CurrentPhaseSlices()
    remainingQty  = min(executionPlan.RemainingQuantity(), executionPlan.RemainingQuantityCurrentPhase())
    
    return RandomizeQuantity(self, quantity, slices, remainingQty)


def GetNewPhaseSliceQuantity(self):

    if self.SplitPhases():
    
        executionPlan = self.ExecutionPlan()
        slices        = executionPlan.NbrOfSlicesNextPhase()
        volume        = executionPlan.NextPhaseQuantity()
        remainingQty  = executionPlan.RemainingQuantity()

        return RandomizeQuantity(self, volume, slices, remainingQty)
            
    return GetNewSliceQuantity(self)

def NextPhase(self, event):
    TraceLog(self, 'NextPhase')
            
    try:
        UpdateBalanceAndDoneValue(self, event)
        AddDoneQuantity(self, event)

        if AnyQuantityLeftToExecute(self):   

            executionPlan = self.ExecutionPlan()            
            remainingQty  = executionPlan.RemainingQuantity()

            currentPhase = self.ExecutionPlan().Phase()
            lastPhase = self.TradingSchedule().LastTradingPhase()
            
            TraceLog(self, "Remaining quantity: " + str(remainingQty))
            
            if currentPhase == lastPhase:
                if remainingQty > 0:
                    FatalError(self, 'Not participating in any more trading phases - failed to reach target quantity')
                    return
                    
            qty = min(GetNewPhaseSliceQuantity(self), self.Balance())
                                    
            slice = self.ExecutionPlan().MoveNext(qty, True)
            self.Slice(slice)
            
        ClearCurrentOrder(self, event)
        ClearNextSlice(self, event)
        
        TraceLog(self, 'Balance: '+ str(self.Balance()) +', BaseQty: '+ str(self.BaseOrder().Balance()))
        
    except Exception as e:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Failed to move to next slice: ' + str(e))

    
def NextSlice(self, event):
    TraceLog(self, 'NextSlice')
    
    try:
        UpdateBalanceAndDoneValue(self, event)
        AddDoneQuantity(self, event)
        
        if AnyQuantityLeftToExecute(self):   
            qty = 0.0
            nextSliceOrder = self.NextSliceOrder()
            nextSliceQty = self.NextSliceQuantity()

            if nextSliceOrder:
                qty = nextSliceQty
                TraceLog(self, 'Using quantity left from last slice: ' + str(qty))
            else:
                qty = min(GetNewSliceQuantity(self), self.Balance())
                TraceLog(self, 'New slice quantity: ' + str(qty))

                
            slice = self.ExecutionPlan().MoveNext(qty, False)
            
            if acm.Math.AlmostZero(qty, ZERO_QTY_EPSILON):
                if not acm.Math.AlmostZero(self.ExecutionPlan().CurrentPhaseQuantity(), ZERO_QTY_EPSILON):
                    raise Exception('Next slice has no quantity')

            self.Slice(slice)
            
            if nextSliceOrder:
                if nextSliceOrder.IsOrderDeleted():
                    nextSliceOrder = None
                    nextSliceQty = 0.0
                elif nextSliceOrder.IsOrderDone():
                    deletedQty = nextSliceOrder.DeletedQuantity()
                    if deletedQty > 0:
                        slice.AddDoneQuantity(nextSliceQty - deletedQty)
                        nextSliceOrder = None
                        nextSliceQty = 0.0

               
            if nextSliceQty > qty:
                raise Exception('Active order quantity exceeds slice quantity')
                
            self.CurrentOrder(nextSliceOrder)
            self.CurrentOrderQty(nextSliceQty)
            self.CurrentTrigger(self.Trigger())
            
        ClearNextSlice(self, event)
    
        TraceLog(self, 'Balance: '+ str(self.Balance()) +', BaseQty: '+ str(self.BaseOrder().Balance()))
            
    except Exception as e:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Failed to move to next slice: ' + str(e))


def OnAlgoInstructionUpdate(self):
    dealFilter = self.BaseOrder().PrePostTradeAnalysis().DealFilter()
    if dealFilter and self.BaseOrder().BuyOrSell() == 'Sell':
        dealFilter.MaxPriceLimit(0)
        dealFilter.MinPriceLimit(self.LimSlicePriceUsed())
    elif dealFilter:
        dealFilter.MaxPriceLimit(self.LimSlicePriceUsed())
        dealFilter.MinPriceLimit(0)
    
def OnCommandError(self, command):
    pass
    
def UpdateIsPlannedAuction(self, event):
    if self.IsVolaAuction():
        TraceLog(self, 'Volatility Auction')
        self.RegularAuction(False)
    elif self.IsOpeningAuction():
        TraceLog(self, 'Opening Auction')
        self.RegularAuction(True)
    elif self.IsIntradayAuction():
        TraceLog(self, 'Intraday Auction')
        self.RegularAuction(False)
    elif self.IsClosingAuction():
        TraceLog(self, 'Closing Auction')
        self.RegularAuction(True)
    else:
        TraceLog(self, 'Unknown Auction')
        self.RegularAuction(False)

    if self.IsVolaAuction() and self.AuctionVolaAllowed():
        self.CurrentAuctionIsPlanned(False)
        self.ParticipateInAuction(True)
    elif self.IsOpeningAuction() and self.AuctionOpenAllowed():
        self.CurrentAuctionIsPlanned(True)
        self.ParticipateInAuction(True)
    elif self.IsIntradayAuction() and self.AuctionIntradayAllowed():
        self.CurrentAuctionIsPlanned(False)
        self.ParticipateInAuction(True)
    elif self.IsClosingAuction() and self.AuctionCloseAllowed():
        self.CurrentAuctionIsPlanned(True)
        self.ParticipateInAuction(True)
    else:
        self.CurrentAuctionIsPlanned(False)
        self.ParticipateInAuction(False)

    
def OnEnterAuctionPhase(self, event):
    isPlanned        = self.CurrentAuctionIsPlanned()
    tradeInUnplanned = (not isPlanned and self.AuctionVolaAllowed())
    
    if (not isPlanned) and (not self.UnplannedAuctionEnd()) and self.IsVolaAuction():
        volaAuctionLenght = self.AuctionVolaLength()
        TraceLog(self, 'Timer: ' + str(volaAuctionLenght)+ ' (marketVolatilityInterruptionLengthInSeconds)')
        self.UnplannedAuctionEnd(acm.Time.Timer().CreateTimerEvent(volaAuctionLenght, None, None))
    
    info = self.BaseOrder().AlgoTradingInstruction().AgentModifyReason()    
    

    if not self.CurrentOrderFilled() :
        if (not self.ParticipateInAuction()) :
            if self.IsClosingAuction():
                if self.ExecutionPlan().RemainingQuantity() > 0:
                    FatalError(self, 'Not instructed to participate in closing auction')
                    return
            info = 'Auction, not participating' 
        elif (isPlanned or tradeInUnplanned) and self.OrderBookInAuctionPhase() :
            enoughEqQty = self.MinimumEquilibriumQuantity()

            if not self.OkToEnterAuctionOrder():
                if self.NotEnoughEquilibriumVolume():
                    if enoughEqQty > 0.000001 :
                        info = 'Waiting for EqQty > ' + str(int(enoughEqQty))
                    else:
                        info = 'Waiting for Equilibrium info'
                else:
                    info = 'Waiting to enter auction order'
        elif (not self.OrderBookInAuctionPhase()) :
            info = 'Not Auction, waiting for fills'            
        else:
            info = 'Unplanned Auction, waiting for CONTR'

            
    SetAgentInfo(self, info)       

def OnEnterDone(self, event):
    errHandler = self.ErrorHandler() 
    errHandler.UnregisterCondition('baseOrderClaimed')
    errHandler.ClearErrors()
    self.BaseOrder().SetAlgoAgentState('Agent Done', ' ')
    if (self.BaseOrder().Balance()) < 0 :
        errHandler.OnError('Fatal', 'Order has over filled')
  
    

def OnEnterError(self, event):
    fatalErrorMessage = self.FatalErrorString()
    if fatalErrorMessage == None or fatalErrorMessage == '':
        fatalErrorMessage = 'Unknown error'
        
    self.TradingSession().DeleteOrders(True)
    
    FatalError(self, fatalErrorMessage)

def OnEnterRestart(self, event):
    reason = ''
    if self.ExternalDealDetected():
        reason = 'External deal detected'
        self.ExternalDealDetected(False)
    elif self.OriginalQuantityChanged():
        reason = 'Quantity changed'
    elif self.ExecutionTimeChanged():
        reason = 'Execution time changed'
    elif self.StartTimeInput() != self.LastStartTimeInput():
        reason = 'Start time parameter has changed'
    elif self.StopTimeInput() != self.LastStopTimeInput():
        reason = 'Stop time parameter has changed'
    elif self.ManualQuantity() != self.InitialManualQuantity():
        reason = 'Manual order detected'

        size = self.TradingSession().ManualOrders().Size()
        TraceLog(self, 'Manual OrdersSize: ' + str(size))
        
        TraceLog(self, "order Info")
        for orderDbg in self.TradingSession().ManualOrders():
            orderId = orderDbg.OrderId()
            marketId = orderDbg.MarketOrderId()
            orderQty = orderDbg.Balance()
            orderDne = orderDbg.IsOrderDone()
            oInfo = "orderId: "+str(orderId)
            oInfo = oInfo+"marketId: "+str(marketId)
            oInfo = oInfo+"orderQty: "+str(orderQty)
            oInfo = oInfo+"Done: "+str(orderDne)            
            TraceLog(self, oInfo)
    else:
        reason = self.ReoptimizeReason()
        
    if reason == None or reason == '':
        reason = 'Unknown reason'
        

    SetAgentInfo(self, 'Reoptimizing: ' + reason)
    
    
def OnEnterOrderFilled(self, event):
    self.UpdateCompletedOrderVolume(event)
    if (not self.SliceDone()) and (not self.OrdersHaveDeletedQty()): 
        info = 'Slice filled'
        sliceEndTime = self.ExecutionPlan().SliceEndTime()
        
        if sliceEndTime != None :
            info = info + ', next starts: ' + timeFormatter.Format(sliceEndTime)
        else:
            info = info + ' and slice time has not yet ended'
            
        SetAgentInfo(self, info)

    
def OnEnterWait(self, event):
    if not self.SafetyRuleTimeToStart():
        SetAgentInfo(self, 'Not yet time to start (' + timeFormatter.Format(self.StartTime()) + ')')


def OnEnterWouldStateMonitor(self, event):
    info = "Would Price Crossed: " + str(self.WouldPriceValid())  
    SetAgentInfo(self, info)

def OnEnterStart(self, event):
    Version(self)
    self.TradingSession().UserId( self.BaseOrder().UserId() )
    self.BaseOrder().IsIndependentModifyEnabled(True)
    
    TraceLog(self, 'UserId set to ' + self.TradingSession().UserId() )
    
    prePostTradeAnalysis = self.BaseOrder().PrePostTradeAnalysis()
    
    prePostTradeAnalysis.PreTradeMarkets(self.VolumeFeedMarketSourceValid())
    prePostTradeAnalysis.PostTradeMarkets(self.VolumeFeedMarketSourceValid())
    prePostTradeAnalysis.ExcludedQuantity(self.ManualActiveQuantity())
    
    dealFilter = acm.Trading.CreateVolumeParticipationDealFilter(self.TradingSession())
    if dealFilter and self.BaseOrder().BuyOrSell() == 'Sell' :
        dealFilter.MaxPriceLimit(0)
        dealFilter.MinPriceLimit(self.LimSlicePriceUsed())
    elif dealFilter:
        dealFilter.MaxPriceLimit(self.LimSlicePriceUsed())
        dealFilter.MinPriceLimit(0)
    prePostTradeAnalysis.DealFilter(dealFilter)
    
    prePostTradeAnalysis.Refresh()
    self.GoalVolume(prePostTradeAnalysis.Quantity())

    
def OnEnterStop(self, event):
    baseOrder = self.BaseOrder()
   
    if self.ErrorHandler().FatalError():
        self.BaseOrder().SetAlgoAgentState('Agent Error', self.ErrorHandler().StringKey())
    elif self.BaseOrderDone():
        self.BaseOrder().SetAlgoAgentState('Agent Done',  ' ')
    else:
        self.BaseOrder().SetAlgoAgentState('Agent Stopped', ' ')
        
    baseOrder.Release()
    if self.ExecutionPlan():
        self.ExecutionPlan().Release()
        
    self.TradingSession().DeleteOrders(True)

def OnEnterTradingPhase(self, event):
    self.ExecutingSlice(True)
    info = self.Trigger().StringKey()

    if info == 'Enter':
        info = info + GetExtendedTriggerInfo(self.RefTypeEnter(), self.PriceOffsetEnter())
    elif info == 'Join':
        info = info + GetExtendedTriggerInfo(self.RefTypeJoin(), self.PriceOffsetJoin())
    elif self.PriceLimitExceeded():
        info = info + GetLimitReason(self)
        
    currentInfo = self.BaseOrder().AlgoTradingInstruction().AgentModifyReason()
    if info != currentInfo:
        SetAgentInfo(self, info)
        
    HandleModificationDelay(self, event)

def OnEnterWaitForFills(self, event):
    timerEvent = None
    if not self.ReadyForRestart():
        SetAgentInfo(self, 'Synchronizing trades with done quantity in order')
        timerEvent = acm.Time.Timer().CreateTimerEvent(GetDefaultValue(self, 'AlgoWaitForFillsTimeout'), None, None)
    self.TimerEvent(timerEvent)
        

def OnExitWaitForFills(self, event):
    self.TimerEvent(None)
        
def OnModifyOrderError(self, event):
    command = self.PendingCommand()
    errors = command.Errors()
    for e in errors:
        if e.IsExceptionError():
            # internal error or excessive updating
            self.FatalErrorString(e.Message())
        elif e.Order() == self.BaseOrder():
            fatal = True
            if e.IsMarketError():
                fatal = e.Type() != 'TimeStamp'
            if fatal:
                self.FatalErrorString(e.Message())
        else:
            failedNbr = e.Order().ConsecutiveErrors()
            maxFailedNbr = self.MaxNbrFailedModifications()
            if failedNbr >= maxFailedNbr:
                self.FatalErrorString('Max number of order modification failures reached (' + str(maxFailedNbr) + '), last error:' + e.Message())


def OnOrderDelete(self, order):
    if (not order.IsDeleteIssuedByOwner()) and (not order.IsDeletedOnBrokenSession()) and (not self.WouldPriceCrossed()) :
        self.ErrorHandler().OnError('Fatal', 'Order deletion not issued by agent')


def OnPrepare(self):
    self.TradingSession().RemoveOrderBooks()
    acm.AlgorithmicTrading.RegisterAlgoInstructionHook(self, 'OnUpdate', OnAlgoInstructionUpdate)


def OnPrepared(self):
    pass


def OnTrade(self, order, trade):
    if self.BaseOrder() == order:
    
        if None == self.ExecutionPlan():
            #agent not started
            pass
        elif trade.IsShapeTrade():
            pass
        elif trade.OrderId() == '' or trade.OrderId() == None:
            # manual fill
            self.ExternalDealDetected(True)
            self.ExecutionPlan().AddExternalQuantity(abs(trade.Quantity()));
        elif None == self.TradingSession().FindOrder(trade.OrderId()):
            # manual trade
            self.ExternalDealDetected(True)
            self.ExecutionPlan().AddExternalQuantity(abs(trade.Quantity()));
        else:
            #The order is already taken into account so we don't have to care about it.
            pass


def OnWaitForFillsTimeout(self, event):
    self.FatalErrorString('Timeout - done quantity in order does not match traded quantity')

    
# In PlaceFishingOrder we should find only one order from the previous cycle as everything else should have been matched 
# The remaining order qty represents the best qty left in terms of price and precedence from the previous cycle
# Our role in this action is to create an order or to complete the order up to the necessary qty to fulfill the next order
def PlaceFishingOrder(self, event): 
    if self.CurrentOrderActive():
        self.ErrorHandler().OnError('Fatal', 'Place fishing order - active order already in market')
        return
        
    slice = self.Slice()
    qty = slice.RemainingQuantity()
    
    order = CreateNewOrder(self, GetPrice(self, event), qty, False)
    
    if order:
        self.CurrentOrder(order)
        self.CurrentOrderQty(qty)
        self.CurrentTrigger(self.Trigger())
        self.PendingCommand(order.SendOrder())
    elif qty > 0:
        self.ErrorHandler().OnError('Fatal', 'Failed to prepare new fishing order')
     
# Choose whether to send a new match order or modify the existing one
def PlaceMatchOrder(self, event): 
    currentSliceQty = self.CurrentOrderQty()
    currentOrder = self.CurrentOrder()
    currentQty   = currentOrder.MovedQuantity()
    slice        = self.Slice()
    executionPlan= self.ExecutionPlan()
    remainingQty = min(executionPlan.RemainingQuantityCurrentPhase(True), executionPlan.RemainingQuantity(True))
    
    TraceLog(self, 'RemainingQty: ' + str(remainingQty) + ' CurrentQty: ' + str(currentQty))

    if currentQty <= 0.0:
        TraceLog(self, 'Current order has no active quantity - no match order will be placed')
        return
    elif remainingQty < currentQty:
        TraceLog(self, 'Remaining quantity after current slice is less than active quantity - modify current order')
        return
    elif self.QuantityMightBreakParticipationLimit(currentSliceQty + currentQty):
        TraceLog(self, 'Sending new match order might break participation limit - modify current order')
        return
        
    quantity      = executionPlan.CurrentPhaseQuantity()
    slices        = executionPlan.CurrentPhaseSlices()
    
    matchQty = currentQty
    if (executionPlan.RemainingQuantityCurrentPhase() <= 1):
        matchQty = remainingQty
    
    minSliceQty = self.TradingInterface().PrevRoundLot((quantity / slices) * (1 - self.SliceSizeRange()) + 0.001)


    if currentQty < minSliceQty:
        TraceLog(self, 'Active quantity is less than min slice quantity (' + str(minSliceQty) + ') - modify current order')
        return

        
    if not self.CurrentOrderCanBeModified():
        TraceLog(self, 'Current order cannot be modified - modify current order')
        return
    

    proposedPrice = GetPrice(self, event)
    
    if self.PriceLimitExceeded() and acm.Math.AlmostEqual(proposedPrice, currentOrder.Price()):
        TraceLog(self, 'Price limit exceeded - no match order will be placed')
        return
        
    TraceLog(self, 'Send new match order; leaving ' + str(currentQty) + ' active for next slice')     
    self.NextSliceOrder(currentOrder)
    self.NextSliceQuantity(currentQty)
    slice.AddDoneQuantity(currentSliceQty - currentQty)
    matchOrder = CreateNewOrder(self, GetPrice(self, event), matchQty, False)
    self.CurrentOrder(matchOrder)
    self.CurrentOrderQty(currentQty)
    self.CurrentTrigger(self.Trigger())
    self.PendingCommand(matchOrder.SendOrder())

def PrintBidAsk(self, event):
    info = 'Prices Bid/Ask '+str(self.PriceFeed().BestBidPrice().Get().Number())+' '+str(self.PriceFeed().BestAskPrice().Get().Number())
    TraceLog(self, info)

def PlaceWouldOrder(self, event):
    SetAgentInfo(self, "Would Price Crossed: " + str(self.WouldPriceValid()))
    self.PrintBidAsk(event)

    baseOrderBidOrAsk = 'Bid';
    if self.BaseOrder().BuyOrSell() == 'Sell':
        baseOrderBidOrAsk = 'Ask'
        
    currentOrder = self.CurrentOrder()
    if currentOrder:
        currentQty = currentOrder.Balance()
    else:
        currentQty = 0
    
        
    nextSliceOrder = self.NextSliceOrder()
    if nextSliceOrder:
        currentQty = currentQty + nextSliceOrder.Balance()
        
    qtyLeft = max(0, self.GoalVolume() - self.DoneVolume() - currentQty - self.WouldQuantityFilled());

    
    leveltAtWouldPrice = self.PriceFeed().BidPriceDepth()
    if self.BaseOrder().IsBuy():
        leveltAtWouldPrice = self.PriceFeed().AskPriceDepth()

    if leveltAtWouldPrice:
        qtyAtWouldPrice = leveltAtWouldPrice.QuantityAtPrice(self.WouldPriceValid())
        qtyAtWouldPrice = min(qtyLeft, qtyAtWouldPrice)
    
    if qtyAtWouldPrice > 0:
        order = CreateNewOrder(self, self.WouldPriceValid(), qtyAtWouldPrice, False) 
        TraceLog(self, 'qtyAtWouldPrice: '+str(qtyAtWouldPrice)+' @price: '+str(self.WouldPriceValid()))
        
        if order:
            PlaceWouldOrderFaK(self, order)
        else:
            self.ErrorHandler().OnError('Fatal', 'Failed to prepare new would order')


def PlaceWouldOrderFaK(self,  order): 
    
    order.OrderType('Fill and Kill (IOC)')
    self.CurrentOrder(order)
    self.CurrentOrderQty(order.Quantity())
    self.PendingCommand(order.SendOrder())                

def QuantityMightBreakParticipationLimit(self, quantity):
    participationLimit = self.LimVolumeParticipation()
    
    if acm.Math.IsFinite(participationLimit) and participationLimit > 0:
        qty = self.DoneVolumeFromAgent() + quantity
        marketQty = self.MarketVolumeDone() + quantity
        return qty / marketQty > participationLimit
        
    return False
    
def RegisterSafetyRules(self):
    errHandler = self.ErrorHandler()     
    errHandler.RegisterCondition('vitalRuleActiveOrder', 'Fatal', 'Order is not active')
    errHandler.RegisterCondition('vitalRuleNotTimeToStop', 'Fatal', 'Reached stop time')    
    errHandler.RegisterCondition('vitalRuleAheadOfMaxLag', 'Fatal', 'Too far behind to be safe to continue (max lag breached)')
    errHandler.RegisterCondition('vitalRuleCostOfRiskUnchanged', 'Fatal', 'Parameter Cost of Risk changed while agent was active')
    errHandler.RegisterCondition('vitalRuleOrderIsConnected', 'Fatal', 'Lost connection to the market')
    errHandler.RegisterCondition('safetyRuleOrderBookConnected', 'Information', 'Order book not connected')
    errHandler.RegisterCondition('safetyRuleAskSideNotEmpty', 'Information', 'Ask side is empty')
    errHandler.RegisterCondition('safetyRuleBidSideNotEmpty', 'Information', 'Bid side is empty')
    errHandler.RegisterCondition('safetyRuleParticipationOk', 'Information', 'Exceeded volume participation limit')
    errHandler.RegisterCondition('safetyRuleTimeToStart', 'Information', 'Not yet time to start')    
    errHandler.RegisterCondition('safetyRuleNoCross', 'Information', 'There are crossing prices in the order book')
    errHandler.RegisterCondition('safetyRuleMaxSpreadOk', 'Information', 'The spread is too wide')
    errHandler.RegisterCondition('safetyRuleHighLowPriceExist', 'Information', 'Missing high/low price during time window')
    errHandler.RegisterCondition('infoRuleLimSlicePriceUnbreached', 'Information', 'Target price is adjusted to meet Slice Price Limit')
    errHandler.RegisterCondition('infoRuleLimMaxPriceDiffTraderUnbreached', 'Information', 'Target price is adjusted to meet Max Price Diff Limit')
    errHandler.RegisterCondition('infoRuleLimHighLowPriceUnbreached', 'Information', 'Target price is adjusted to meet High/Low Price Limit')
    errHandler.RegisterCondition('infoRuleSliceParticipationUnbreached', 'Information', 'Slice quantity might breach participation limit; waiting for market to turn over quantity')
    errHandler.RegisterCondition('baseOrderClaimed', 'Information', 'Claiming order')    
    errHandler.RegisterCondition('orderBookInTradingPhase', 'Information', 'Order book not in automatic trading phase')
    errHandler.RegisterCondition('modificationDelayExceeded', 'Information', 'Attempt to modify order failed; retrying')

def SetManualSlices(self, event):
    self.SlicesToExecute(self.ManualSlices())

def SetOrderPrice(self, order, proposedPrice):
    current = order.Price().Number()   
    if (order.BuyOrSell() == 'Buy' and (current > proposedPrice)) or (order.BuyOrSell() == 'Sell' and (current < proposedPrice)):
        TraceLog(self, 'Proposed price not logical: e.g. a buy order with lower price will only lose its place in queue without gaining any other advantage.')
    else:
        if acm.Math.AlmostEqual(proposedPrice, current):
            TraceLog(self, 'Proposed order price identical to previous price')
        elif self.PriceFeed().IsValidPrice(proposedPrice):
            order.Price(proposedPrice)
            self.PendingCommand(order.SendOrder())

def TraceLog(self, message):
    if self.IsTraceEnabled() and self.Log():
        self.Log().AddStringRecord(message)
    
def UpdateCompletedOrderVolume(self, event):
    order   = self.CurrentOrder()
    prevQty = self.VolumeDoneFromCompletedOrders()  
    
    if order:
        prevQty = prevQty + order.FilledQuantity("Order")
        TraceLog(self, 'Filled Qty: ' + str(order.FilledQuantity("Order")) + ' Previous Filled Qty: '+str(self.VolumeDoneFromCompletedOrders()))
    
    qtyfilled = prevQty
    self.VolumeDoneFromCompletedOrders(qtyfilled)

def UpdatePrice(self, event):
    order = self.CurrentOrder()
    
    if order and order.IsOrderActive():
        price = self.TargetPrice()
        
        if self.Trigger() == self.CurrentTrigger():
            price = ExecutionAlgoOrder.GetNewOrderPrice(self, event, order)
          
        SetOrderPrice(self, order, price)
        
    # should actually only be done if the command succeed    
    self.CurrentTrigger(self.Trigger()) 
  
        
def UpdateFatalErrorMessage(self, event):
    command = self.PendingCommand()
    errors  = command.Errors()
    message = ''
    
    for e in errors:
        if message != '':
            message = message + ', '
        message = message + e.Message()
        
    self.FatalErrorString(message)
    self.PendingCommand(None)
    
def UpdateNextOrderQuantity(self, event):
    if self.CurrentOrder():
        if self.CurrentOrder().IsOrderDone():
            temp = self.CurrentOrder().DeletedQuantity()
            self.Slice().AddDoneQuantity(self.CurrentOrderQty() - temp)
        self.ClearCurrentOrder(event)  
        

def UpdateNextOrderQuantityWouldMode(self, event):
    self.Slice().AddDoneQuantity(self.CurrentOrder().FilledQuantity('Order'))
    self.ClearCurrentOrder(event)
 
        
def UpdateWaitMessage(self, event):
    info = self.WaitMessage()
    TraceLog(self, "info: " +  info)
    SetAgentInfo(self, info)


def OnOptimize(self, event):   
    try:
        volatility = round(100 * self.Volatility(), 2)

        if self.PreTradePriceDetailsInfoVolatility():
            volDays = self.PreTradePriceDetailsInfoVolatility().CalculationDays()
        else:
            volDays = 'NaN'
            
        
        TraceLog(self, 'External OrderBookId: ' + self.TradingInterface().ExternalId())
        TraceLog(self, 'PreTradePeriodAverageTradeSize: ' + str(self.PeriodAverageTradeSize()) )
        TraceLog(self, 'AuctionQuantityRatio: ' + str(self.AuctionQuantityRatio()) )        
        TraceLog(self, 'VolumePattern: ' + self.VolumePattern().AsString())
        TraceLog(self, 'Volatility: ' + str(volatility) + ' % based on ' + str(volDays) + 'd closing prices')
        
        FSlicesAndDuration.optimize(self)
        
        if self.IsKindOf('ExecutionAlgoVolumeParticipation'):
            slicesAdjustedForGoalVolume = FSliceExtrapolation.getSlices(self)
            slices = int(slicesAdjustedForGoalVolume)
        else:
            slices = int(self.EstimatedSlices())
        
        if slices > 0:
            self.SlicesToExecute(slices)
            self.EstimatedSlicesFound(True)
            if IsMultiMarket(self) :
                SetAgentInfo(self, 'Optimized ' + str(slices) + ' slices (Multi Mkt), ' + str(volatility) + ' % volatility etc')            
            else:
                SetAgentInfo(self, 'Optimized ' + str(slices) + ' slices using ' + str(volatility) + ' % volatility etc')            
        else:
            UpdateIsPlannedAuction(self)
            if self.IsClosingAuction():
                self.SlicesToExecute(1.0)
                self.EstimatedSlicesFound(True)            
                SetAgentInfo(self, 'Forced 1 slice in Auction')            
            else:
                raise Exception('Number of slices not found')
    except Exception as e:
        self.SlicesToExecute(0)
        self.EstimatedSlices(0)
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Failed to optimize slices and duration: ' + str(e))
        self.EstimatedSlicesFound(False)
    


def OnPreparations(self, event):
    ClearPreviousPlanData(self, event)
    SaveOrderBook(self, event)
    s = self.PreparationsTimeOut()
    self.TimerEvent(acm.Time.Timer().CreateTimerEvent(s, None, None))
    
    if IsMultiMarket(self) :
        preTradeMarkets  = GetDefaultValue(self, 'ownOrderPreTradeBenchmarkMarkets')
        postTradeMarkets = GetDefaultValue(self, 'ownOrderPostTradeBenchmarkMarkets')
        TraceLog(self, 'ownOrderPreTradeBenchmarkMarkets  = '  + str(preTradeMarkets) )
        TraceLog(self, 'ownOrderPostTradeBenchmarkMarkets = '  + str(postTradeMarkets))
    
    
    cD = self.DaysOfClosingPrices()
    vD = self.DaysOfVolumePattern()
    
    if not self.PreparationsDone() and not self.BaseOrderDone():
        if IsMultiMarket(self) :
            SetAgentInfo(self, 'Waiting <'+str(s)+'s for ' +str(vD)+ 'd Multi-VolumePattern and ' +str(cD)+ 'd ClosingPrices')
        else:
            SetAgentInfo(self, 'Waiting <'+str(s)+'s for ' +str(vD)+ 'd VolumePattern and ' +str(cD)+ 'd ClosingPrices')


def OnEnterCreateExecutionPlan(self, event):
    try:
        baseOrder = self.BaseOrder()
        prePostTradeAnalysis = baseOrder.PrePostTradeAnalysis()
        
        prePostTradeAnalysis.PreTradeMarkets(self.VolumeFeedMarketSourceValid())
        prePostTradeAnalysis.PostTradeMarkets(self.VolumeFeedMarketSourceValid())
        prePostTradeAnalysis.ExcludedQuantity(self.ManualActiveQuantity())
        prePostTradeAnalysis.Refresh()
        self.GoalVolume(prePostTradeAnalysis.Quantity())
        
        
        self.Balance(baseOrder.Balance())
        self.OriginalQuantity(baseOrder.OriginalQuantity())
        self.OriginalFilledQuantity(baseOrder.FilledQuantity('Order'))
        self.OriginalReservedQuantity(baseOrder.ReservedQuantity())
        self.OriginalStartTime(baseOrder.ValidStartExecutionTime())
        self.OriginalStopTime(baseOrder.ValidEndExecutionTime())
        self.InitialManualQuantity(self.ManualQuantity())
        self.InitialManualDoneQuantity(self.ManualDoneQuantity())

        self.ExternalDealDetected(False)

        plan = self.CreateExecutionPlan()
        TraceLog(self, 'Plan: ' + str(plan))

        tradingQuantities, slices = GetTradingQuantities(self, event)
        plan.Prepare(self.TradingSchedule(), tradingQuantities, slices)
        
        nCommands  = GetDefaultValue(self, 'AlgoMaxNbrOfCommands')
        nCommandMs = GetDefaultValue(self, 'AlgoMaxCommandsMs')
        self.TradingSession().LimitCommands(nCommands, nCommandMs)
        
        # Create trigger points
        plan.AddTrigger('Enter', 0.5 - self.TrigEnter())
        plan.AddTrigger('Join', 0.5 - self.TrigJoin())
        plan.AddTrigger('Match', 0.5 - self.TrigMatch())
        plan.AddTrigger('MatchAll', 0.5 - self.TrigMatchAll())
        if self.LimMaxLag() > 0:
            plan.AddTrigger('MaxLag', 1.0 + self.LimMaxLag())
            
        self.ExecutionPlan(plan)
        
        self.StartEvent(acm.Time.Timer().CreateTimerEventAt(self.StartTime(), None, None))
        
        vitalStopTime = self.VitalStopTime()
        
        if acm.Time.IsValidDateTime(vitalStopTime):
            self.StopEvent(acm.Time.Timer().CreateTimerEventAt(self.VitalStopTime(), None, None))
        else:
            self.StopEvent(None)
            
        self.NextSlice(event)
        
    except Exception as e:
        TraceLog(self, 'Exception OnCreateExecutionPlan: ' + str(e))
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Failed to create execution plan')


def OnVerify(self, event):
    verificationFailed = False
    
    try:
        trading         = self.TradingInterface()
        startTime       = self.StartDateTimeInput()
        stopTime        = self.StopDateTimeInput()
        timeNow         = acm.Time.TimeNow()
        hasStartTime    = acm.Time.IsValidDateTime(startTime)
        hasStopTime     = acm.Time.IsValidDateTime(stopTime)

        tradingSchedule = trading.Schedule()
        phase           = tradingSchedule.GetPhase(timeNow)  
        startPhase      = self.TradingSchedule().FirstPhase()
        firstExecPhase  = self.TradingSchedule().FirstTradingPhase()
        
        roundlot = int(trading.RoundLot())
        intVolume = int(self.GoalVolume())
        if intVolume % roundlot != 0:
            self.VerificationError('Volume (%d) is not a multiple of roundlot (%d)' % (intVolume, roundlot))
            verificationFailed = True
            
        elif phase and phase.IsClosedPhase() and not phase.Next():
        
            if trading.Status().Closed():
                self.VerificationError('Market is closed')
            else:
                self.VerificationError('Market closed according to trading schedule')
            verificationFailed = True
                    
        elif hasStartTime and startPhase and startPhase.IsClosedPhase() and not startPhase.Next():
        
            self.VerificationError('StartTime is after market closing time')
            verificationFailed = True


        elif not firstExecPhase:
            
            if phase.IsClosingAuctionPhase():
                self.VerificationError('Not instructed to participate in closing auction')
            else:
                self.VerificationError('Not instructed to participate in any of the remaining phases')
            verificationFailed = True
                        
        elif hasStopTime:
            
            if DateTimeCmp(stopTime, timeNow) <= 0:
                self.VerificationError('StopTime occurs in the past')
                verificationFailed = True
            elif acm.Time.DateDifference(acm.Time.DateNow(), acm.Time.AsDate(stopTime)) < 0:
                self.VerificationError('StopTime occurs after today')
                verificationFailed = True
            elif hasStartTime and DateTimeCmp(startTime, stopTime) >= 0:
                self.VerificationError('StartTime must be less than StopTime')
                verificationFailed = True


        if self.AutoOptimizeSlicesAndDuration():
            if self.CheckArrivalPrice():
                ppTA = self.BaseOrder().PrePostTradeAnalysis()
                if not self.PriceFeed().IsValidPrice(ppTA.ArrivalPrice()):
                    self.VerificationError('Arrival Price: ' + str(ppTA.ArrivalPrice()) + ' is invalid')
                    verificationFailed = True
            if self.Volatility() < 0.000001 :
                self.VerificationError('Volatility must be greater than zero')
                verificationFailed = True
            if self.VolumePattern().IsEmpty():
                self.VerificationError('Volume Pattern is empty')
                verificationFailed = True
            
        elif self.ManualSlices() < 1.0:
            self.VerificationError('Invalid number of slices: ' + str(self.ManualSlices()))
            verificationFailed = True
        
        if self.FirstVerification():
            wouldPrice = self.WouldPriceInfo()
            if wouldPrice > 0:
                if self.BaseOrder().IsBuy() :
                    if wouldPrice > self.PriceFeed().BestAskPrice().Get().Number() :
                        self.VerificationError('Would Price Higher than Best Market Ask')
                        verificationFailed = True
                else:
                    if wouldPrice < self.PriceFeed().BestBidPrice().Get().Number() :
                        self.VerificationError('Would Price Lower than Best Market Bid')
                        verificationFailed = True
    except Exception as e:
        TraceLog(self, 'Exception during verification: ' + str(e))
        self.VerificationError('Exception during verification: ' + str(e))
        verificationFailed = True        
        
    self.VerificationFailed(verificationFailed)
    self.FirstVerification(False)

def OnEnterVerifyNotOK(self, event):
    FatalError(self, self.VerificationError())
    
    

def PlaceInitialFillOrder(self, event):
    if self.Slice() != None:
        initialFillQty = 0.0
        nextSliceQty = self.Slice().RemainingQuantity()
    
        if nextSliceQty > 0:
            initialFillQty = self.ComfortFillsInfo()
            if initialFillQty > nextSliceQty:
                TraceLog(self, 'initialFillQty '+str(initialFillQty)+' exceeds firstSlice '+str(nextSliceQty)+'; therefore setting initialFillQty to '+str(nextSliceQty))
                initialFillQty = nextSliceQty
            
        if initialFillQty > 0:
            trading = self.TradingInterface()
            price = trading.PriceFeed().RoundTickUpDown(not self.BaseOrder().IsBuy(), self.TargetPriceMatchAll())
            s = self.MaxWaitInMsForInitialFill() / 1000
            TraceLog(self, 'Sending initial fill order of qty: '+str(initialFillQty)+' price: ' +str(price)+' to show that the agent is alive, within ' +str(s) +'s')

            if trading.PriceFeed().IsValidPrice(price) and trading.Status().AutomaticTrade():             
                initialFillOrder =  CreateNewOrder(self, price, initialFillQty, True)
                self.TimerEvent(acm.Time.Timer().CreateTimerEvent(0.001 * self.MaxWaitInMsForInitialFill(), None, None))
                self.CurrentOrder(initialFillOrder)
                self.CurrentOrderQty(initialFillQty)
                self.PendingCommand(initialFillOrder.SendOrder())
            else:
                TraceLog(self, 'Invalid price: '+str(price) + ' or not trading: ' + trading.Status().PhaseAbbreviation() )      

def OnEnterContinuousTrading(self, event):
    self.ExecutingSlice(False)
    self.ModificationDelay(None)

    if NowInScheduleIsCONTR(self, event):
        self.TradingScheduleNowIsCONTR(True)
        SetTradingPhaseChangeTime(self, event)
    else:
        self.TradingScheduleNowIsCONTR(False)
    
    if not self.BaseOrderDone() and self.Trigger() == None:
        SetAgentInfo(self, 'Wait')

def SaveStartStopTime(self, event):

    tradingSchedule = self.TradingInterface().Schedule()
    startTime       = self.StartDateTimeInput()
    stopTime        = self.StopDateTimeInput()
    presentTime     = acm.Time.TimeNow()
    openingTime     = tradingSchedule.FirstTradingPhase().StartTime()
    
    self.LastStartTimeInput(self.StartTimeInput())
    self.LastStopTimeInput( self.StopTimeInput())
      
    if not acm.Time.IsValidDateTime(startTime):
        TraceLog(self, 'Start Time not set')
        if DateTimeCmp(presentTime, openingTime) < 0:
            TraceLog(self, 'Market not yet open; using market opening time')
            startTime = openingTime
        else:
            TraceLog(self, 'Market open; using present time')
            startTime = presentTime
    elif DateTimeCmp(startTime, presentTime) < 0:
        TraceLog(self, 'Start Time occurs in the past')
        if DateTimeCmp(presentTime, openingTime) < 0:
            TraceLog(self, 'Market not yet open; using market opening time')
            startTime = openingTime
        else:
            TraceLog(self, 'Market open; using present time')
            startTime = presentTime
    else:
        if DateTimeCmp(startTime, openingTime) < 0:
            TraceLog(self, 'Start Time occurs before market opens; using market opening time')
            startTime = openingTime
        else:
            TraceLog(self, 'Start Time set and valid')
        
    if not acm.Time.IsValidDateTime(stopTime):
        TraceLog(self, 'Stop Time not set; using closing time')
        stopTime = tradingSchedule.ClosingTime()
    
    self.StartTime(startTime)
    self.StopTime(stopTime)
        

def SaveOrderBook(self, event):
    tradingInterface = self.TradingInterface()
    
    if tradingInterface != None:
        self.TradingSession().AddTradingInterface(tradingInterface)

def SetTradingPhaseChangeTime(self, event):
    schedule            = self.TradingSchedule()
    timeNow             = acm.Time.TimeNow()
    phaseNow            = schedule.GetPhase(timeNow)
    if phaseNow:
        currentPhaseEndTime = phaseNow.StopTime()
        TraceLog(self, 'Current scheduled phase: ' + str(phaseNow))        
        self.TradingSchedulePhaseChange(acm.Time.Timer().CreateTimerEventAt(currentPhaseEndTime, None, None)) 
            
def UpdateComfortFillPrice(self, event):
    price = self.PriceFeed().RoundTickUpDown(not self.BaseOrder().IsBuy(), self.TargetPriceMatchAll())

    if self.PriceFeed().IsValidPrice(price):
        currentOrder = self.CurrentOrder()
        currentOrder.Price(price)
        self.PendingCommand(currentOrder.SendOrder())
    else:
        TraceLog(self, 'Initial order price updated is invalid: '+str(price))

def SaveComfortFilledQty(self, event):
    UpdateCompletedOrderVolume(self, event)
    UpdateBalanceAndDoneValue(self, event)
    AddDoneQuantity(self, event)
    ClearCurrentOrder(self, event)
        

def OnEnterVerifyOK(self, event):
    RegisterSafetyRules(self)

def OnPreparationsTimedOut(self, event):
    info = ''
    
    if self.ExternalMarket():
        marketServer       = self.ExternalMarket().MarketServer()    
        emStatus    = self.ExternalMarket().ConnectionStatus()
        ramsaStatus = self.ExternalMarket().ArchiveConnectionStatus()
        
        if not self.ExternalMarket().IsConnected():
            info += str(marketServer) + ': ' + str(emStatus) + ' '
            
        if not self.ExternalMarket().IsArchiveConnected():
            info += 'RAMSA: ' + str(ramsaStatus) + ' '        
            
        TraceLog(self, 'External market ' + str(marketServer) + ' connection status: ' + str(emStatus) + ' RAMSA status: ' +str(ramsaStatus))
    else:
        info += 'No External market '
        TraceLog(self, 'No External market connection found')
    
    
    if not self.TradingInterface():
        imObId = self.BaseOrder().TradingInterface().ExternalId()
        info += 'Cannot determine Home OrderBook (' + imObId +') '
    elif self.ExternalMarket():
        if not self.PriceDetailsOK() :
            info += 'No price details received from market '
        if self.ExternalMarket().IsArchiveConnected():
            if not self.VolumePatternOK():
                if self.VolumePattern():
                    preTradeMkts = GetDefaultValue(self, 'ownOrderPreTradeBenchmarkMarkets')
                    if self.VolumePattern().IsDirty():
                        if IsMultiMarket(self) :
                            
                            info += 'No Consolidated VolumePattern ' + str(preTradeMkts) + ' '                       
                        else:
                            info += 'No VolumePattern '
                    else:
                        days = self.DaysOfVolumePattern()
                        if IsMultiMarket(self) :
                            info += 'Consolidated VolumePattern Emtpy ' + str(preTradeMkts) + ' '                          
                        else:
                            info += 'Empty VolumePattern (' + str(days) + 'd) '
                else:
                    info = 'Nil VolumePattern '
                    
            if (not self.VolatilityOK()) and (not self.VolumePatternOK()) :
                info += ' and no RAMSA closing prices '
            elif not self.VolatilityOK() :
                info += 'No RAMSA closing prices '
    else:
        info += 'Loading market data took too long'
    
    self.FatalErrorString(info)

def PlaceAuctionOrder(self, event):
    sliceQty = self.AuctionSliceQuantity()
    newQty = self.LimVolumeParticipationAuctionQty()

    if sliceQty > 0.000001 and newQty > 0.000001:
        priceFeed = self.PriceFeed()
        limited, price = GetAuctionPrice(self, event)
        if priceFeed.IsValidPrice(price):            
            UpdateAuctionOrderStatus(self, limited)              
            TraceLog(self, 'Participation limited Order Quantity: ' + str(newQty))
            TraceLog(self, 'Max participation quantity: ' + str(self.AuctionMaxParticipationAuctionQuantity()))
            TraceLog(self, 'Max participation rate: ' + str(self.AuctionMaxParticipationRate()))
            TraceLog(self, 'Auction Surplus: ' + str(self.AuctionSurplus()))
            TraceLog(self, 'Auction Equilibirum Quantity: ' + str(self.AuctionEquilibriumQuantity()))
            auctionOrder =  CreateNewOrder(self, price, newQty, False)
            self.CurrentOrder(auctionOrder)
            self.CurrentOrderQty(newQty)
                
            self.PendingCommand(auctionOrder.SendOrder())
            self.LastLimitPrice(self.AuctionPriceLimit())
    else:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Non-valid Qty for Auction order sliceQty: ' + str(sliceQty) + 'Participation limited Order Qty:' + str(newQty))

def CreateTradingSchedule(self, event):

    try:
        tradingSchedule = self.TradingInterface().Schedule()
        agentSchedule   = tradingSchedule.Section(self.StartTime(), self.StopTime());
        phases          = agentSchedule.Phases()
        
        for phase in phases:
            if not phase.IsAuctionPhase():
                continue
                
            if phase.IsOpeningAuctionPhase():
                if not self.AuctionOpenAllowed():
                    phase.PhaseType('NoTrading')
                    
            elif phase.IsIntradayAuctionPhase():
                if not self.AuctionIntradayAllowed():
                    phase.PhaseType('NoTrading')
                    
            elif phase.IsClosingAuctionPhase():
                if not self.AuctionCloseAllowed():
                    phase.PhaseType('NoTrading')
                    
            else:
                phase.PhaseType('NoTrading')
                    
        self.TradingSchedule(agentSchedule)    
        TraceLog(self, str(tradingSchedule) )
        TraceLog(self, 'Agent ' + str(agentSchedule) )
    except Exception as e:
        TraceLog(self, 'Exception in CreateTradingSchedule: ' + str(e))
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Failed to create trading schedule')

def GetAuctionPrice(self, event):
    priceFeed        = self.PriceFeed()
    tickList         = priceFeed.TickSizeList()
    equilibriumPrice = priceFeed.EquilibriumPrice().Get().Number()
    nrOfTicks        = self.EquilibriumPriceOffset()
    priceMaxDiff     = self.EquilibriumPriceMaxDiff()
    limitPrice       = self.AuctionPriceLimit()   
    
    if limitPrice < 0:
        limitPrice   = 0.0
    
    if priceFeed.IsValidPrice(equilibriumPrice):
        if self.BaseOrder().IsBuy():
            priceX = equilibriumPrice * (1 + priceMaxDiff)
            priceX = priceFeed.RoundTickUp(priceX)
            priceY = equilibriumPrice
            for i in range(1, int(nrOfTicks) + 1):
                priceY = tickList.NextTick(priceY)

            price = min(priceX, priceY)
            if limitPrice > 0 and price > limitPrice:
                return (limitPrice < equilibriumPrice, limitPrice)
            else:
                return (False, price)

        else:
            priceX = equilibriumPrice * (1 - priceMaxDiff)
            priceX = priceFeed.RoundTickDown(priceX)
            priceY = equilibriumPrice            
            for i in range(1, int(nrOfTicks) + 1):
                priceY = tickList.PrevTick(priceY)
            price = max(priceX, priceY)      
            if limitPrice > 0 and price < limitPrice:
                return (limitPrice > equilibriumPrice, limitPrice)
            else:
                return (False, price)
    else:
        return (None, None)

def UpdateAuctionOrderStatus(self, limited):    
    if limited:
        maxPrcLimit = self.LimMaxPriceDiffAllowed()
        upDown = not self.BaseOrder().IsBuy()
        
        if abs( self.AuctionPriceLimit() - self.PriceFeed().RoundTickUpDown(upDown, maxPrcLimit) ) < 0.00001 :
            reason = GetMaxPriceLimitReason(self)
        else:
            reason = '(limit ' + str(self.AuctionPriceLimit()) + ')'
        SetAgentInfo(self, 'Unlikely to trade ' + reason)
    else:
        SetAgentInfo(self, 'Likely to trade ' + str(int(self.AuctionSliceQuantity())) + ' in auction')
      
  
def EquilibriumChanged(self, event):
    oldPrice = self.LastEquilibriumPrice()
    newPrice = self.PriceFeed().EquilibriumPrice().Get().Number()
    limit = self.LastLimitPrice()
       
    if limit > 0:
        if (oldPrice <= limit <= newPrice) or (newPrice <= limit <= oldPrice):
            order = self.CurrentOrder()
            if order and order.IsOrderActive():
                limited, proposedPrice = GetAuctionPrice(self, event)
                UpdateAuctionOrderStatus(self, limited)
    self.LastEquilibriumPrice(newPrice)

def UpdateAuctionPrice(self, event):
    order = self.CurrentOrder()
    self.LastLimitPrice(self.AuctionPriceLimit())
    
    if order and order.IsOrderActive():
        limited, proposedPrice = GetAuctionPrice(self, event)
          
        if self.PriceFeed().IsValidPrice(proposedPrice):
            order.Price(proposedPrice)
            self.PendingCommand(order.SendOrder())
            UpdateAuctionOrderStatus(self, limited)
            

def HandleModificationDelay(self, event):
    msOffset = 20
    msFactor = 10
    OrderModificationDelay(self, event, msOffset, msFactor)
    
def OrderModificationDelay(self, even, msOffset, msFactor):
    # check order for errors    
    order = self.CurrentOrder()
    if (order == None or 0 == order.ConsecutiveErrors()):
        self.ModificationDelay(None)
    else:
        msDelay  = 0

        if order != None:
            failedNbr = order.ConsecutiveErrors()
            msDelay = min(msOffset + msFactor * pow(2, failedNbr - 1), 10000)                
                      
        self.ModificationDelay(acm.Time.Timer().CreateTimerEvent(0.001 * msDelay, None, None))
        TraceLog(self, str(failedNbr) + ' consecutive order modification failures. Earliest retry in ' + str(msDelay) + ' ms') 

def GetTradingQuantities(self, event):
    quantitiesArray   = acm.FArray()
    slicesArray       = acm.FArray()

    goalVolume        = self.GoalVolume()
    nrOfSlices        = int(self.SlicesToExecute())
    roundlot          = int(self.TradingInterface().RoundLot())
    goalRoundlots     = int(goalVolume) / roundlot
    
    if goalRoundlots * roundlot != goalVolume:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Volume is not an even amount of round lots')
        return quantitiesArray, slicesArray
        
    if goalRoundlots < nrOfSlices:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Slices are fewer than round lots')
        return quantitiesArray, slicesArray
        
    
    averageQuantityPerSlice = goalVolume / self.SlicesToExecute()
    roundedQtyPerSlice      = self.TradingInterface().PrevRoundLot(averageQuantityPerSlice + 0.001) 
    self.AverageSliceQuantity(roundedQtyPerSlice)
    
    if not self.SplitPhases():
        quantitiesArray.Add(goalVolume)
        slicesArray.Add(nrOfSlices)
        return quantitiesArray, slicesArray
    
    schedule          = self.TradingSchedule()
    nrOfPhases        = len(schedule.Phases())
    nrOfAuctions      = 0
    nrOfTradePhases   = 0
    indexForAuction1       = -1
    indexForTradePhase1    = -1 # For CONTR
    indexForTradePhase2    = -1 # Only needed if LunchAuctions split CONTR in two

    
    for i in range(0, nrOfPhases):
        
        quantitiesArray.AtInsert(i, 0.0)
        slicesArray.AtInsert(i, 1) # at least one slice per phase (may have 0 quantity)
        phase = schedule.Phases().At(i)
        if phase.IsAuctionPhase():
            if indexForAuction1 == -1:
                indexForAuction1 = i
            nrOfAuctions+= 1
        elif phase.IsAutomaticTradePhase():
            nrOfTradePhases+=1
            if indexForTradePhase1 == -1:
                indexForTradePhase1 = i
            else:
                indexForTradePhase2 = i
        

    # set quantities for autions
    if nrOfAuctions == 1 and nrOfTradePhases == 0:
        # special case - everything in one auction
        quantitiesArray.AtPut(indexForAuction1, goalVolume)
        goalVolume = 0
    elif nrOfAuctions > 0:
        for a in range(0, nrOfPhases):
            phase = schedule.Phases().At(a)
            if phase.IsAuctionPhase():
                nrOfSlices = nrOfSlices - 1
                
                if nrOfSlices > 0:
                    quantitiesArray.AtPut(a, roundedQtyPerSlice)
                    goalVolume = goalVolume - roundedQtyPerSlice
                else:
                    quantitiesArray.AtPut(a, goalVolume)
                    goalVolume = 0
                      
    # set quantities for COTR
    if nrOfTradePhases == 1:
        quantitiesArray.AtPut(indexForTradePhase1, goalVolume)
        slicesArray.AtPut(indexForTradePhase1, nrOfSlices)
    elif nrOfTradePhases == 2:
        if goalRoundlots%2 == 0 :
            quantitiesArray.AtPut(indexForTradePhase1, goalRoundlots / 2 * roundlot)    
            quantitiesArray.AtPut(indexForTradePhase2, goalRoundlots / 2 * roundlot)
        else:
            quantitiesArray.AtPut(indexForTradePhase1, (goalRoundlots - 1) / 2  * roundlot)    
            quantitiesArray.AtPut(indexForTradePhase2, (((goalRoundlots - 1)/ 2) + 1) * roundlot)
        if nrOfSlices%2==0 :
            #Remaining Nr of Slices are even
            slicesArray.AtPut(indexForTradePhase1, int(nrOfSlices / 2) )    
            slicesArray.AtPut(indexForTradePhase2, int(nrOfSlices / 2) )
        else:
            slicesArray.AtPut(indexForTradePhase1, int((nrOfSlices - 1) / 2     ))    
            slicesArray.AtPut(indexForTradePhase2, int(((nrOfSlices - 1)/ 2) + 1))
    elif nrOfTradePhases > 2:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Cannot handle more than one intraday auction')
    elif goalVolume > 0:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'Not instructed to participate in any scheduled trading phase')
        
    TraceLog(self, 'Planned quantities per Trading Phase: ' + str(quantitiesArray))
    TraceLog(self, 'Planned nr of slices per Trading Phase: ' + str(slicesArray))
    return quantitiesArray, slicesArray

def NextSliceAfterAuction(self, event):
    NextPhase(self, event)
    

def AddDoneQuantity(self, event):
    slice = self.Slice()
    if slice:
        currentOrder = self.CurrentOrder()
        if currentOrder and currentOrder.IsOrderDone():
            slice.AddDoneQuantity(self.CurrentOrderQty() - currentOrder.DeletedQuantity())
            TraceLog(self, 'Done quantity in slice set to: ' + str(slice.DoneQuantity()))


def SetPhaseChangeError(self, event):
    self.FatalErrorString('Failed to execute all volume during instructed trading phases')

def UpdateBalanceAndDoneValue(self, event):
    filledValue = 0.0
    if self.CurrentOrder() != None and self.CurrentOrder().IsOrderDone():
        filledValue = self.CurrentOrder().FilledQuantity('Order')*self.CurrentOrder().FilledPrice()  
           
    self.DoneValue(filledValue + self.DoneValue())
    self.Balance(self.BaseOrder().Balance())

def GetEnterAuctionQuantity(self, event):
    sliceQty = 0.0

    if self.CurrentAuctionIsPlanned():
        if self.Slice():
            sliceQty = min(self.ExecutionPlan().RemainingQuantityCurrentPhase(), self.ExecutionPlan().RemainingQuantity())
            
            if sliceQty < 0.000001 :
                TraceLog(self, 'RemainingQtyCurrentPhase = 0, AuctionQuantity = SliceQty')
                sliceQty = self.Slice().Quantity()
            else:
                TraceLog(self, 'AuctionQty = RemainingQtyCurrentPhase')
    else:
        sliceQty = self.AverageSliceQuantity()
        TraceLog(self, 'Unplanned auction, AuctionQuantity = AverageSliceQuantity')
    
    return min(sliceQty, self.ExecutionPlan().RemainingQuantity())

def ReoptimizeAfterPhaseChange(self, event):
    self.ReoptimizeReason('New phase, reoptimizing...')

def NowInScheduleIsCONTR(self, event):
    schedule = self.TradingSchedule()
    
    if schedule :
        timeNow  = acm.Time.TimeNow()
        if schedule.GetPhase(timeNow):
            return schedule.GetPhase(timeNow).IsAutomaticTradePhase()
        else:
            self.ErrorHandler().Clear()
            self.ErrorHandler().OnError('Fatal', 'No TradingPhase exists now')
    else:
        self.ErrorHandler().Clear()
        self.ErrorHandler().OnError('Fatal', 'No TradingSchedule exists')
     



def OnWaitForRealPhaseChange(self, event):
    msDiff = self.MaxMsDiffScheduleAndReality()
    self.MaxDiffScheduleAndReality(acm.Time.Timer().CreateTimerEvent(0.001 * msDiff, None, None))
    SetTradingPhaseChangeTime(self, event)
    SetAgentInfo(self, 'Waiting for auction')

def OnWaitForSchedulePhaseChange(self, event):
    UpdateIsPlannedAuction(self, event)
    msDiff = self.MaxMsDiffScheduleAndReality()
    TraceLog(self, 'Max diff between schedule and real phase change: ' + str(msDiff) + ' ms')
    self.MaxDiffScheduleAndReality(acm.Time.Timer().CreateTimerEvent(0.001 * msDiff, None, None))
    SetTradingPhaseChangeTime(self, event)        
    SetAgentInfo(self, 'Wait: synchronizing phase with schedule')


def OnAuctionWaitForTimer(self, event):
    isPlanned = self.CurrentAuctionIsPlanned()
    startWaitForBalanceTimer = False
    
    if self.UnplannedAuctionEnd():
        if self.UnplannedAuctionEnd().IsExpired():
            startWaitForBalanceTimer = True
    elif isPlanned:
        startWaitForBalanceTimer = True
    
    if startWaitForBalanceTimer:
        waitLenghtInSeconds = self.AuctionVolaLength() * 0.1
        TraceLog(self, 'Starting timer to wait for SalesOrder Balance: ' + str(waitLenghtInSeconds) + 's' )
        self.AfterAuctionWaitForBalance(acm.Time.Timer().CreateTimerEvent(waitLenghtInSeconds, None, None))
    
    info = ''
    
    if isPlanned :
        info = 'Auction over, synchronizing...'
    elif (not isPlanned and self.AuctionVolaAllowed()) :
        info = 'Unplanned Auction over, synchronizing...'
        
    SetAgentInfo(self, info)

def SetAuctionSliceQuantity(self, event):
    sliceQty = GetEnterAuctionQuantity(self, event)
    self.AuctionSliceQuantity(sliceQty)

def SetMaxWaitInitialFillError(self, event):
    s = self.MaxWaitInMsForInitialFill() / 1000
    strategy = self.OrderRoutingInitialFill()
    
    if (None == strategy) or ("None" == strategy.StringKey()):  
        error = "Waited " +str(s)+ "s for InitialFill (no TradingStrategy)" 
    else:    
        error = "Waited " +str(s)+ "s for InitialFill (" +strategy.StringKey()+  ")" 
        
    self.FatalErrorString(error)

def OnEnterMarketClosed(self, event):
    FatalError(self, 'Market closed')

def OnEnterReady(self, event):
    if self.MarketClosed():
        SetAgentInfo(self, 'Waiting for market to open')

def UpdateAuctionOrder(self, event):
    order = self.CurrentOrder()
    if order and order.IsOrderActive():
                
        updatedQty = self.LimVolumeParticipationAuctionQty()
        TraceLog(self, 'Participation limited Order Quantity: ' + str(updatedQty))
        TraceLog(self, 'Max participation quantity: ' + str(self.AuctionMaxParticipationAuctionQuantity()))
        TraceLog(self, 'Max participation rate: ' + str(self.AuctionMaxParticipationRate()))
        TraceLog(self, 'Auction Surplus: ' + str(self.AuctionSurplus()))
        TraceLog(self, 'Auction Equilibirum Quantity: ' + str(self.AuctionEquilibriumQuantity()))
            
        
        if updatedQty > 0 :
            order.Quantity(updatedQty)
            self.CurrentOrderQty(updatedQty)
            self.PendingCommand(order.SendOrder())
            UpdateAuctionOrderStatus(self, False)
        else:
            TraceLog(self, 'Non-valid modify Qty for Auction order (limited order qty): ' + str(updatedQty))

def UpdateAuctionQuantity(self, event):
    pass

def ClearPreviousPlanData(self, event):
    self.Slice(None)
    self.VolumeDoneFromCompletedOrders(0.0)
    self.DoneValue(0.0)
    ClearCurrentOrder(self, event)
    ClearNextSlice(self, event)
            
    



