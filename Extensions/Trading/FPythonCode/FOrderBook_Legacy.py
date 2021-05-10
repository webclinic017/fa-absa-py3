
import acm

def ActiveQuote(self, level):
    return acm.FAggregatedQuote(self).ActiveQuoteAt(level)
    
def IsPriceRational(self, price, relativeDif):
    return acm.FFreeTextModule(self).AlgoTradingStrategies()

def LastPriceLastWeek(self):
    date = acm.Time.DateToday()
    while acm.Time.DayOfWeek(date) != 'Sunday':
        date = acm.Time.DateAddDelta(date, 0, 0, -1)
    calendar = self.Currency().Calendar()
    while calendar and calendar.IsNonBankingDay(None, None, date):
        date = acm.Time.DateAddDelta(date, 0, 0, -1)
    return self.LastPriceAtDate(date)

def OrderBookStatus(self):
    return self.TradingInterface().Status()

def QuoteChannel(self):
    return acm.FAggregatedQuote(self).Channel()  
   
def QuoteController(self):
    return acm.MarketMaking.GetActiveController(acm.FAggregatedQuote(self).Channel())

def QuoteDetails(self):
    return self.TradingInterface().QuoteDetails()
    
def QuoteParameters(self):
    return acm.MarketMaking.SelectQuoteParameters(self)
    
def UnderlyingsInAutomaticTrade(self, statuses):
    return acm.Trading.InAutomaticTrade(statuses)
    
def WithinStrikeWindow(self, windowSizeITM, windowSizeOTM, underlyingPrice, aroundATM):
    return acm.FStrikeSeries(self.TradingInterface()).WithinStrikeWindow(self.TradingInterface(), windowSizeITM, windowSizeOTM, underlyingPrice, aroundATM)
