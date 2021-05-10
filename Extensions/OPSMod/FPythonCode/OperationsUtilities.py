import acm

def IsNearLegTrade(trade):
    return (trade.TradeProcessesToString().find('Swap Near Leg') > -1)

def IsFarLegTrade(trade):
    return (trade.TradeProcessesToString().find('Swap Far Leg') > -1)

def GetFarLegTrade(trade):
    farLegTrade = None
    if IsNearLegTrade(trade):
        connectedTrades = acm.FTrade.Select('connectedTrdnbr = %d' % trade.Oid())
        for connectedTrade in connectedTrades:
            if connectedTrade.ConnectedTrdnbr() != connectedTrade.Oid():
                if IsFarLegTrade(connectedTrade):
                    farLegTrade = connectedTrade
                    break
    return farLegTrade

def AllSettlements(trade):
    farLegTrade = GetFarLegTrade(trade)
    if farLegTrade:
        farLegSettlements = farLegTrade.Settlements()
        filteredSet = acm.FFilteredSet()
        filteredSet.AddSource(trade.Settlements())
        filteredSet.AddSource(farLegSettlements)
        return filteredSet
    return trade.Settlements()
    
def AllConfirmations(trade):
    farLegTrade = GetFarLegTrade(trade)
    if farLegTrade:
        farLegConfirmations = farLegTrade.Confirmations()
        filteredSet = acm.FFilteredSet()
        filteredSet.AddSource(trade.Confirmations())
        filteredSet.AddSource(farLegConfirmations)
        return filteredSet
    return trade.Confirmations()
