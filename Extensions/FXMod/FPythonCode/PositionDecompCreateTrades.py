import acm
import FUxCore
from math import floor
from math import log10
from math import fabs
import FBDPRollback
import FBDPString
import importlib

scriptName = 'Position Move/Split'

def callAdjustTradeHook(trade, scriptName):
    try:
        import FBDPHook
        importlib.reload(FBDPHook)
    except ImportError:
        return
    try:
        FBDPHook.adjust_fx_ftrade(trade, scriptName)
    except:
        return

class CreateTrades():

    def __init__(self, parameters):
        self.rollback = FBDPRollback.RollbackWrapper(scriptName, 0)
        self.__dict__.update(parameters)
        self.parameters = parameters
        self.createCommitTrades()

    def createCommitTrades( self ):
        self.rollback.beginTransaction()
        trades = self.createTrades()
        businessEvent = self.createBusinessEvent(trades)
        try:
            for trade in trades:
                self.rollback.add(trade)
            self.rollback.add(businessEvent)
            self.rollback.commitTransaction()
            for trade in trades:
                self.rollback.logCreatedMirrorTrade(trade)
        except Exception as ex:
            self.rollback.abortTransaction()
            raise ex
            
    def createBusinessEvent( self, trades ):
        #Create BusinessEvent of type "Position Move/Split"
        businessEvent = acm.FBusinessEvent()
        businessEvent.EventType("Position Move/Split")
        for trade in trades:
            link = acm.FBusinessEventTradeLink()
            link.BusinessEvent(businessEvent)
            link.Trade(trade)
            businessEvent.TradeLinks().Add(link)
        return businessEvent
        
    def createTrades( self ):
        trades = acm.FArray()
        
        #Create position move trade
        trade1 = self.CreatePositionMoveTrade()
        trades.Add(trade1)
        
        #Create swap if from currency pair
        if self.fromPairNeedsSwap:
            mainSwapNear, mainSwapFar = self.CreateFromSwap()
            trades.Add(mainSwapNear)
            trades.Add(mainSwapFar)
                                            
        
        #Create swap in to currency pair
        if self.toPairNeedsSwap:
            toSwapNear, toSwapFar = self.CreateToSwap(trade1)
            trades.Add(toSwapNear)
            trades.Add(toSwapFar)     
        
        #Create position move split trade
        if self.splitCurrency:
            trade2 = self.CreatePositionMoveSplitTrade(trade1)
            trades.Add(trade2)
            
            #Create swap in split currency pair
            if self.splitPairNeedsSwap:
                splitSwapNear, splitSwapFar = self.CreateSplitSwap(trade2.Quantity(), trade2.Premium())
                trades.Add(splitSwapNear)
                trades.Add(splitSwapFar)
        
        return trades
    
    def SetTradeProcessBit( self, trade, currency1, currency2):
        spotProcessBit = 4096 # spot
        fwdProcessBit = 8192 # forward

        cp = currency1.InstrumentPair(currency2)
        if cp:
            if cp.SpotDate(acm.Time.DateToday()) == self.moveDate:
                trade.TradeProcess(spotProcessBit)
            else:
                trade.TradeProcess(fwdProcessBit)
        else:
            trade.TradeProcess(self.tradeProcessNumber)


    def createTrade( self, currency1, currency2, positionPair, quantity, premium, portfolio, acquirer, counterParty, price, spotPrice ):
        counterParty = counterParty or self.fromPortfolio.PortfolioOwner()
        acquirer = acquirer or portfolio.PortfolioOwner()
        
        trade = acm.FTrade()
        trade.ValueDay(self.moveDate)
        trade.AcquireDay(self.moveDate)

        self.SetTradeProcessBit( trade, currency1, currency2)    
        trade.QuantityIsDerived(self.quantityIsDerived)
        trade.TradeTime(acm.Time.DateToday())
        trade.Trader(acm.User())
        trade.Status('Internal')

        trade.Price(price)
        trade.ReferencePrice(spotPrice)
        trade.Instrument(currency1)
        trade.Currency(currency2)
        trade.Quantity(quantity)
        trade.Premium(premium)
        trade.Portfolio(portfolio)
        trade.PositionPair(positionPair)
        trade.Acquirer(acquirer)
        trade.Counterparty(counterParty)
        
        callAdjustTradeHook(trade, scriptName)
        return trade
        
    # Creates a swap that moves a non-spot position to a spot position
    def createSwap( self, currencyPair, amount1, amount2, portfolio, acquirer, counterPortfolio, counterparty, pairRate, pairSpotRate, swapPoints, spotDayIsEarlier):
        outrightLeg = self.createTrade(currencyPair.Instrument1(), currencyPair.Instrument2(), currencyPair,
                                       amount1, amount2, portfolio, acquirer, counterparty, 
                                       pairRate, pairSpotRate)
        outrightLeg.MirrorPortfolio(counterPortfolio, currencyPair)
        
        spotLeg = acm.FTrade()
        spotLeg.Apply(outrightLeg)
        
        pointValue = swapPoints * currencyPair.PointValue()
        spotLeg.Price(outrightLeg.Price() - pointValue)
        
        if self.quantityIsDerived:
            spotLeg.Premium(-outrightLeg.Premium())
            spotLeg.UpdateQuantity()
        else:
            spotLeg.Quantity(-outrightLeg.Quantity()) 
            spotLeg.UpdatePremium(True)
            
        spotLeg.ValueDay(currencyPair.SpotDate(acm.Time().DateToday()))
        spotLeg.AcquireDay(spotLeg.ValueDay())
        spotLeg.MirrorPortfolio(counterPortfolio, currencyPair)
                
        if spotDayIsEarlier:
            outrightLeg.TradeProcess(32768) #Swap Far Leg
            spotLeg.TradeProcess(16384) #Swap Near Leg
            outrightLeg.ConnectedTrade(spotLeg)
            return spotLeg, outrightLeg
        else:
            outrightLeg.TradeProcess(16384) #Swap Near Leg
            spotLeg.TradeProcess(32768) #Swap Far Leg
            spotLeg.ConnectedTrade(outrightLeg)
            return outrightLeg, spotLeg        
    
    def CreatePositionMoveTrade( self ):
        amount1, amount2 = [self.amount1, self.amount2] if self.selectedCurrency == self.rowCurrency1 else [self.amount2, self.amount1]
        trade = self.createTrade(self.rowCurrency1, self.rowCurrency2, self.toCurrencyPair,
                                 amount1, amount2, self.toPortfolio, self.toAcquirer, self.fromAcquirer, 
                                 self.mainRate, self.mainSpotRate)

        trade.MirrorPortfolio(self.fromPortfolio, self.fromCurrencyPair)
        return trade
        
    def CreatePositionMoveSplitTrade( self, trade1 ):
        amount1, amount2 = [-self.splitAmount, self.nonSplitAmountSplitPair] if self.splitCurrency == self.splitCurrencyPair.Instrument1() else [self.nonSplitAmountSplitPair,  -self.splitAmount]        
        trade2 = self.createTrade(self.splitCurrencyPair.Instrument1(), self.splitCurrencyPair.Instrument2(), self.splitCurrencyPair,
                                  amount1, amount2, self.splitPortfolio, self.splitAcquirer, self.toAcquirer, 
                                  self.splitPairRate, self.splitPairSpotRate)
        
        trade2.MirrorPortfolio(self.toPortfolio, self.toCurrencyPair)
        trade2.ConnectedTrade(trade1)
        return trade2
    
    def GetToPairSwapAmounts( self, trade1 ):
        amount1 = 0.0
        amount2 = 0.0
        if self.toCurrencyPair and self.fromCurrencyPair:
            if self.toCurrencyPair.Instrument1() == self.fromCurrencyPair.Instrument1():
                amount1 = trade1.Quantity()
                amount2 = self.splitAmount
            
            elif self.toCurrencyPair.Instrument1() == self.fromCurrencyPair.Instrument2():
                amount1 = trade1.Premium()
                amount2 = self.splitAmount
                
            elif self.toCurrencyPair.Instrument2() == self.fromCurrencyPair.Instrument1():
                amount1 = self.splitAmount
                amount2 = trade1.Quantity()
                
            elif self.toCurrencyPair.Instrument2() == self.fromCurrencyPair.Instrument2():
                amount1 = self.splitAmount
                amount2 = trade1.Premium()
            
        return [amount1, amount2]
            
    def CreateToSwap( self, trade1 ):
        amount1, amount2 = self.GetToPairSwapAmounts(trade1)
        toSwapNear, toSwapFar = self.createSwap(self.toCurrencyPair, amount1, amount2, 
                                                self.toFwdPortfolio, self.toFwdAcquirer, 
                                                self.toPortfolio, self.toAcquirer,
                                                self.toPairRate, self.toPairSpotRate, self.toPairPoints, 
                                                (self.toPairSpotDate < self.moveDate))
        return [toSwapNear, toSwapFar]
        
    def CreateFromSwap( self ):
        amount1, amount2 = [-self.amount1, -self.amount2] if self.selectedCurrency == self.rowCurrency1 else [-self.amount2, -self.amount1]
        mainSwapNear, mainSwapFar = self.createSwap(self.fromCurrencyPair, amount1, amount2, 
                                                    self.fromFwdPortfolio, self.fromFwdAcquirer, 
                                                    self.fromPortfolio, self.fromAcquirer,
                                                    self.mainRate, self.mainSpotRate, self.fromPairPoints, 
                                                    (self.fromPairSpotDate < self.moveDate))
        return [mainSwapNear, mainSwapFar]
        
        
    def CreateSplitSwap( self, amount1, amount2 ):
        splitSwapNear, splitSwapFar = self.createSwap(self.splitCurrencyPair, amount1, amount2, 
                                                      self.splitFwdPortfolio, self.splitFwdAcquirer,
                                                      self.splitPortfolio, self.splitAcquirer,
                                                      self.splitPairRate, self.splitPairSpotRate, self.splitPairPoints, 
                                                      (self.splitPairSpotDate < self.moveDate))
        return [splitSwapNear, splitSwapFar]
