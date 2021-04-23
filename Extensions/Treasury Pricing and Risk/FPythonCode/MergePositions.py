import acm
import FUxCore
import TradeActionUtilityFunctions

def MergeTrades(object):
    trades = TradeActionUtilityFunctions.GetSelectedTrades( object )
    
    mergeValidator = MergeValidator( trades ) 
    if mergeValidator.ValidateTradesToBeMerged():
        mergeHandler = MergeTradesImpl(trades)
        # Get an FInsdefInitData instance and start app with initData
        mergeInitData = acm.TradeActionData().GetBusinessEventInitData( mergeHandler )
        acm.UX().SessionManager().StartApplication( 'Instrument Definition', mergeInitData )

    else:
        acm.Log(mergeValidator.GetErrorMessage())
        func=acm.GetFunction('msgBox', 3)
        func("Error", mergeValidator.GetErrorMessage(), 0)

def MergeTradesImpl(selectedTrades):
    trades = acm.FArray()
    trades.AddAll(selectedTrades)
    newInstrument = CreateInstrument(trades)
    newQuantity = GetQuantity(trades)
    mergeHandler = acm.FTradeMerger(trades, newInstrument, newQuantity)
    return mergeHandler

def CreateInstrument(trades):
    instrument = None
    if trades.Size() > 0:
    
        instrument = acm.TradeActionUtil.CreateSimulatedCopy(trades[0].Instrument())
        instrument.Name = instrument.SuggestName()
        instrument.DeleteExerciseEvents()
        
        enumeration = acm.GetDomain('enum(ExerciseEventType)') 
        event = acm.TradeActionUtil.CreateSimulatedExerciseEvent(instrument)
        event.Type(enumeration.Enumeration('DrawdownPeriod'))
        event.StartDate(GetStartDay(trades))
        event.EndDate(GetEndDay(trades))
        
    return instrument

def GetStartDay(trades):
    startDay = None
    if trades.Size() > 0:
        startDay = trades[0].Instrument().FirstDrawdownDate()
        for trade in trades:
            date = trade.Instrument().FirstDrawdownDate()
            if acm.Time.DateDifference(date, startDay) < 0:
                startDay = date
    if (not startDay or acm.Time.DateDifference(startDay, acm.Time.DateToday()) < 0):
        startDay = acm.Time.DateToday()
    return startDay
        
def GetEndDay(trades):
    endDay = None
    if trades.Size() > 0:
        endDay = trades[0].Instrument().LastDrawdownDate()
        for trade in trades:
            date = trade.Instrument().LastDrawdownDate()
            if acm.Time.DateDifference(date, endDay) > 0:
                endDay = date
    if (not endDay or acm.Time.DateDifference(endDay, acm.Time.DateToday()) < 0):
        endDay = acm.Time.DateToday()
    return endDay
    
def GetQuantity(trades):
    amount = 0
    for trade in trades:
        amount = amount + trade.RemainingDrawdownAmount()
    return -amount

class MergeValidator:
    def __init__( self, trades ):
        self.trades = trades
        self.errMsg = ""
        
    def GetErrorMessage( self ):
        return self.errMsg
        
    def ValidateTradesToBeMerged( self ):
        return self.ValidateNumberOfTrades() and self.ValidateInsTypeODF() and self.ValidateSameDirection() and self.ValidateTradeAttributes()
    
    def ValidateNumberOfTrades( self ):
        if len(self.trades) < 2:
            self.errMsg = "The number of trades is less than 2, cannot merge"
            return False
        return True
    
    def ValidateSameDirection( self ):
        isCallOption = self.trades[0].Instrument().OptionTypeIsCall()
        for trade in self.trades:
            if trade.Instrument().OptionTypeIsCall() != isCallOption:
                self.errMsg = "All trades must be either buy or sell, cannot merge"
                return False
        return True
    
    def ValidateInsTypeODF( self ):
        for trade in self.trades:
            ins = trade.Instrument()
            if ins.InsType() != "FXOptionDatedFwd":
                self.errMsg = "At least one instrument is not an ODF, cannot merge"
                return False
        return True
    
    def ValidateTradeAttributes( self ):
        # Attribute checking
        firstTrade = self.trades[0]
        counterparty = firstTrade.Counterparty()
        currencyPair = firstTrade.CurrencyPair()
        dealtCurrency = firstTrade.Currency()
    
        for trade in self.trades:
            if trade.Counterparty() != counterparty:
                self.errMsg = "The counterparties are not consistent for all trades, cannot merge"
                return False
                
            elif trade.CurrencyPair() != currencyPair:
                self.errMsg = "The currency pairs are not consistent for all trades, cannot merge"
                return False
                
            elif trade.Currency() != dealtCurrency:
                self.errMsg = "The dealt currencies are not consistent for all trades, cannot merge"
                return False
                
            elif trade.RemainingNominal() == 0.0:
                self.errMsg = "At least one trade has zero remaining amount, cannot merge"
                return False
                
        return True
        
