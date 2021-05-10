import acm

def getTradesInPosition(trade):    
    ins = trade.Instrument()
    hedgeTradeList = []
    for t in ins.Trades():
        if trade.HedgeTrade() is not None:            
            if t.HedgeTrade() == trade.HedgeTrade():
                hedgeTradeList.append(t)
        else:            
            hedgeTradeList.append(trade)
            break
    return hedgeTradeList
