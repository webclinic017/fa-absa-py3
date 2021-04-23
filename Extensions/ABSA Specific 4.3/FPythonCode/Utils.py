import acm

def __CreateAdHocPortfolio__(tradeList):
    adHocPortfolio = acm.FAdhocPortfolio()
    for trade in tradeList:
        print(type(trade))
        assert trade.IsKindOf(acm.FTrade)
        adHocPortfolio.Add(trade)
    return adHocPortfolio

def CreateSingleInstrumentAndTradesFromTrades(tradeList):
    print(tradeList)
    portfolio = __CreateAdHocPortfolio__(tradeList)
    instrumentSet = acm.FSet()
    for trade in tradeList:
        print(type(trade))
        
        instrumentSet.Add(trade.Instrument())
    assert len(instrumentSet) == 1
    for instrument in instrumentSet:
        break
    return acm.Risk().CreateSingleInstrumentAndTradesBuilder(portfolio, instrument).GetTargetInstrumentAndTrades()


