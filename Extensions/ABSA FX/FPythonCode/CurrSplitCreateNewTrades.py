

import acm
import FUxCore
from math import floor
from math import log10
from math import fabs
import FBDPRollback
import FBDPString
import FLogger


scriptName = 'Currency_Split'

LOGGER = FLogger.FLogger(scriptName)
LOGGER.Reinitialize(
        keep=False, 
        logOnce=False, 
        logToConsole=False, 
        logToPrime=True, 
        #logToFileAtSpecifiedPath="C:\\Front Arena\\CurrencySplitLog.txt", 
        filters=None)
        
def callAdjustTradeHook(trade, scriptName):
    try:
        import FBDPHook
        reload(FBDPHook)
    except ImportError:
        return
    try:
        FBDPHook.adjust_fx_ftrade(trade, scriptName)
    except:
        return

class CreateTrades():

    def __init__(self, parameters):
        self.__dict__.update(parameters)
        self.parameters = parameters
        self.rollback = FBDPRollback.RollbackWrapper(scriptName + '_' + self.fromPortfolio.Name(), 0)
        fromIns1 = self.fromCurrencyPair.Instrument1().Name()
        fromIns2 = self.fromCurrencyPair.Instrument2().Name()
        toIns1 = self.toCurrencyPair.Instrument1().Name()
        toIns2 = self.toCurrencyPair.Instrument2().Name()
        LOGGER.LOG("From portfolio: %s" % self.fromPortfolio.Name())
        LOGGER.LOG("From pair: %s/%s" % (fromIns1, fromIns2))
        LOGGER.LOG("To pair: %s/%s" % (toIns1, toIns2))
        LOGGER.LOG("Amount1: %d" % self.amount1)
        LOGGER.LOG("Amount2: %d" % self.amount2)
        LOGGER.LOG("-" * 30)
        self.createCommitTrades()

    def createCommitTrades( self ):
        self.rollback.beginTransaction()
        trades = self.createTrades()
        try:
            for trade in trades:
                self.rollback.add(trade)
            self.rollback.commitTransaction()
            for trade in trades:
                self.rollback.logCreatedMirrorTrade(trade)
        except Exception as ex:
            self.rollback.abortTransaction()
            raise ex
     
        
    def createTrades( self ):
        trades = acm.FArray()
        if self.cashPayment :
            close_trade = self.CreateCloseTrade(True)
            trades.Add(close_trade)
            if self.selectedCurrency in [self.toCurrencyPair.Instrument1(), self.toCurrencyPair.Instrument2()]:
                to_trade, amount = self.CreateToTrade(return_amount=True)
                trades.Add(to_trade)
                neg_trade = self.CreateToTrade(neg_amount=-amount)
                trades.Add(neg_trade)
                
            else:
                split_trade, amount = self.CreateSplitTrade(return_amount=True)
                trades.Add(split_trade)
                neg_trade = self.CreateSplitTrade(neg_amount=-amount)
                trades.Add(neg_trade)
        else:
            close_trade = self.CreateCloseTrade()
            trades.Add(close_trade)
            if self.mainRate == 0:
                if self.selectedCurrency in [self.toCurrencyPair.Instrument1(), self.toCurrencyPair.Instrument2()]:
                    to_trade, amount = self.CreateToTrade(return_amount=True)
                    trades.Add(to_trade)
                    split_trade = self.CreateSplitTrade(neg_amount=-amount)
                    trades.Add(split_trade)
                else:
                    split_trade, amount = self.CreateSplitTrade(return_amount=True)
                    trades.Add(split_trade)
                    to_trade = self.CreateToTrade(neg_amount=-amount)
                    trades.Add(to_trade)
            else:
                to_trade = self.CreateToTrade()
                trades.Add(to_trade)
                split_trade = self.CreateSplitTrade()
                trades.Add(split_trade)
        
        return trades
        
        
    def CreateToTrade(self, return_amount=False, neg_amount=None):
        ins1 = self.toCurrencyPair.Instrument1()
        ins2 = self.toCurrencyPair.Instrument2()   
        amount1, amount2 = [self.amount1, self.amount2] if self.selectedCurrency == self.rowCurrency1 else [self.amount2, self.amount1]
        quantity = None
        premium = amount2
        if neg_amount:
            quantity = neg_amount
            premium = None
        rate = self.toPairRate
        if self.rowCurrency1 == ins2 or self.rowCurrency2 == ins1:
            ins1, ins2 = ins2, ins1
            rate = 1 / rate
        if self.rowCurrency1 == ins1:
            quantity = amount1
            premium = None
            if neg_amount:
                quantity = None
                premium = neg_amount
        if neg_amount:
            rate = 0
        trade = self.createTrade(ins1, ins2, self.toCurrencyPair, quantity, premium, self.toPortfolio, self.toAcquirer, None, rate, self.toPairSpotRate)
        if return_amount:
            if premium:
                amount = -premium / rate
            else:
                amount = -quantity * rate
            return trade, amount
        return trade
        
    def CreateSplitTrade(self, return_amount=False, neg_amount=None):
        ins1 = self.splitCurrencyPair.Instrument1() 
        ins2 = self.splitCurrencyPair.Instrument2() 
        amount1, amount2 = [self.amount1, self.amount2] if self.selectedCurrency == self.rowCurrency1 else [self.amount2, self.amount1]
        quantity = None
        premium = amount2
        if neg_amount:
            quantity = neg_amount
            premium = None
        rate = self.splitPairRate
        if rate == 0:
            rate = self.Rate(ins1, ins2)
        if self.rowCurrency1 == ins2 or self.rowCurrency2 == ins1:
            ins1, ins2 = ins2, ins1
            if rate:
                rate = 1 / rate
            else:
                rate = 0
        if self.rowCurrency1 == ins1:
            quantity = amount1
            premium = None
            if neg_amount:
                quantity = None
                premium = neg_amount
        if neg_amount:
            rate = 0
        trade = self.createTrade(ins1, ins2, self.splitCurrencyPair, quantity, premium, self.splitPortfolio, self.splitAcquirer, None, rate, self.splitPairSpotRate)
        if return_amount:
            if premium:
                if rate:
                    amount = -premium / rate
                else:
                    amount = 0
            else:
                amount = -quantity * rate
            return trade, amount
        return trade


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


    def createTrade( self, currency1, currency2, positionPair, quantity, premium, portfolio, acquirer, counterParty, price, spotPrice, discType='CCYBasis'):
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
        trade.Text1("FX Split")

        trade.Price(price)
        trade.ReferencePrice(spotPrice)
        trade.Instrument(currency1)
        trade.Currency(currency2)
        if quantity and premium:
            trade.Quantity(quantity)
            trade.Premium(premium)
        elif quantity:
            trade.Quantity(quantity)
            trade.Premium(-quantity * price)
        elif premium:
            trade.Premium(premium)
            if price:
                trade.Quantity(-premium / price)
            else:
                trade.Quantity(0.0)
        trade.Portfolio(portfolio)
        trade.PositionPair(positionPair)
        trade.Acquirer(acquirer)
        trade.Counterparty(counterParty)
        trade.DiscountingType(discType)

        callAdjustTradeHook(trade, scriptName)
        return trade
           
    
    def CreateCloseTrade( self, zeroAmount=False):
        if zeroAmount:
            amount1, amount2 = [-self.amount1, 0] if self.selectedCurrency == self.rowCurrency1 else [0, -self.amount1]
            rate = 0.0
            trade = self.createTrade(self.rowCurrency1, self.rowCurrency2, self.toCurrencyPair,
                                 amount1, amount2, self.toPortfolio, self.toAcquirer, self.fromAcquirer, 
                                 rate, self.mainSpotRate)
        else:
            amount1, amount2 = [-self.amount1, -self.amount2] if self.selectedCurrency == self.rowCurrency1 else [-self.amount2, -self.amount1]
            trade = self.createTrade(self.rowCurrency1, self.rowCurrency2, self.toCurrencyPair,
                                 amount1, amount2, self.toPortfolio, self.toAcquirer, self.fromAcquirer, 
                                 self.mainRate, self.mainSpotRate)
        return trade
        
    def Rate(self, curr1, curr2):
        space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        fxRate = curr1.Calculation().FXRate(space, curr2, acm.Time.DateToday()).Value().Number()
        space.Clear()
        return fxRate


