import acm
import FOperationsUtils as Utils

def GetMarkitWireFrontArenaTrades(tradeDate):
    Query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    Query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', acm.Time().DateToday())
    Query.AddAttrNode('AdditionalInfo.CCPmiddleware_id', 'NOT_EQUAL', '')
    Query.AddAttrNode('TradeTime', 'GREATER_EQUAL', tradeDate)
    
    instype = Query.AddOpNode('OR')
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'Swap'))
    instype.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'FRA'))
    
    tradestatus = Query.AddOpNode('OR')
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'BO Confirmed'))
    tradestatus.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'FO Confirmed'))
    trades = Query.Select()
    return trades
    
trades = GetMarkitWireFrontArenaTrades('2016-01-14')

for trade in trades:
    if trade.Status() in ('BO Confirmed', 'FO Confirmed'):
        print trade.Oid(), trade.Status(), trade.AdditionalInfo().CCPclearing_status()
        trade.Status('BO-BO Confirmed')
        trade.Commit()
        print 'Updated the following trades', trade.Oid(), trade.Status()
