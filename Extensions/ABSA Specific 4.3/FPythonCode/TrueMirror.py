
import acm

def getTrueMirror(trade):
    mirrorTrade = None
    if not trade.MirrorTrade():
        return mirrorTrade
        
    if trade.MirrorTrade().Oid() == trade.Oid():
        mirrorTrades = acm.FTrade.Select('mirrorTrade=%i and oid <> %i' %(trade.Oid(), trade.Oid()))
        if len(mirrorTrades) == 1:
             mirrorTrade = mirrorTrades[0]
    else:
        mirrorTrade = trade.MirrorTrade()

    return mirrorTrade
   
def getTrueMirrorCounterparty(trade):
    trueMirror = getTrueMirror(trade)
    if trueMirror:
        if trueMirror.Counterparty():
            return trueMirror.Counterparty().Name()
        else:
            return ''
    return ''

def getTrueMirrorPortfolio(trade):
    trueMirror = getTrueMirror(trade)
    if trueMirror:
        if trueMirror.Portfolio():
            return trueMirror.Portfolio().Name()
        else:
            return ''
    return ''
