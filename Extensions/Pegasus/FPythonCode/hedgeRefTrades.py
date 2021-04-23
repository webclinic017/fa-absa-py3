
import acm
#import hedgeCache

#in hedgeCache
query = r'''
select t.trdnbr, hedge.trdnbr
from trade t join trade hedge on t.trdnbr = hedge.hedge_trdnbr
'''
#mapping = ael.dbsql(query)[0]
#load everything into a dictionary

def getTradesInPosition(trade): 
    hedgeTradeList = []
    ins = trade.Instrument()
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('HedgeTrade.Oid', 'EQUAL', trade.Oid())
    query.AddAttrNode('HedgeTrade.Status', ['Simulated', 'Void', 'Terminated'], 'NOT_EQUAL')
      
    hedgeTradeList = query.Select() 
    
    return hedgeTradeList

def tradeWithSameHedgeRef(trade):
    tradeRef = trade.HedgeTrade()
    hedgeTradeList = []
    if tradeRef is None:
        hedgeTradeList.append(trade)        
    else:
        hedgeTradeList = getTradesInPosition(tradeRef)    
    return [t for t in hedgeTradeList if t.Status() in ('BO Confirmed', 'BO-BO Confirmed')]
