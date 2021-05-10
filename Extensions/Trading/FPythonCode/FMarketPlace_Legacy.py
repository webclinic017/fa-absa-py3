
import acm
 
def Accounts(self):
    return acm.FTradingAccountModule(self).Accounts()

def ClientInvestmentDecisionMakerAccounts(self, client):
    return acm.FTradingAccountModule(self).GetClientInvestmentDecisionMakers(client)
   
def AlgoTradingStrategies(self):
    return acm.FFreeTextModule(self).AlgoTradingStrategies()

def ArchiveConnectionStatus(self):
    return acm.FMarketService(self).ArchiveStatus()

def CapabilityModel(self):
    return acm.FMarketCapabilitiesModule(self).CapabilityModel()
   
def ClosingCallStartTime(self):
    return acm.GetDefaultValueEx(self, 'marketClosingCallStartTime', acm.GetDefaultContext(), 'FOrderBook')

def ClosingTime(self):
    return acm.GetDefaultValueEx(self, 'marketCloseTime', acm.GetDefaultContext(), 'FOrderBook')
    
def Connect(self):
    acm.FMarketService(self).Connect()
    
def ConnectWithTimeout(self, timout):
    acm.FMarketService(self).Connect(timout)
    
def Disconnect(self):
    acm.FMarketService(self).Disconnect()

def GetAccount(self, accountId):
    return acm.FTradingAccountModule(self).GetAccount(accountId)
    
def IntradayCallStartTime(self):
    return acm.GetDefaultValueEx(self, 'marketIntraDayCallStartTime', acm.GetDefaultContext(), 'FOrderBook')

def IntradayCallStopTime(self):
    return acm.GetDefaultValueEx(self, 'marketIntraDayCallStopTime', acm.GetDefaultContext(), 'FOrderBook')

def IsArchiveConnected(self):
    return acm.FMarketService(self).IsArchiveAvailable()
    
def Leave(self):
    acm.FMarketService(self).Leave()

def LastError(self):
    return acm.FMarketService(self).StatusMessage()

def Lists(self):
    return acm.FOrderBookModule(self).Lists()
    
def MarketServer(self):
    return acm.FMarketService(self).MarketServer()

def Members(self):
    return acm.FMembersModule(self)

def OpeningCallStartTime(self):
    return acm.GetDefaultValueEx(self, 'marketOpeningCallStartTime', acm.GetDefaultContext(), 'FOrderBook')

def OpeningTime(self):
    return acm.GetDefaultValueEx(self, 'marketOpenTime', acm.GetDefaultContext(), 'FOrderBook')

def QuoteRequesting(self):
    return acm.FQuoteModule(self).QuoteRequesting()

def QuoteRules(self):
    return acm.FQuoteModule(self).QuoteRules()

def Quoting(self):
    return acm.FQuoteModule(self)

def TickSizeLists(self):
    return acm.FOrderBookModule(self).TickSizeLists()

def TieringCategories(self):
    return acm.FQuoteModule(self).TieringCategories()

def TradeTypes(self, orderBook):
    return acm.FTradeModule(self).TradeTypes(orderBook)
