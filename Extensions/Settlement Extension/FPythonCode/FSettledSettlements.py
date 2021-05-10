import acm
import FOperationsUtils as Utils

earliestSettledDay = acm.Time().SmallDate()

def SettledSettlements(trade, settlementTypes=None, startDate=None, endDate=None):
    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')

    query.AddAttrNode('Trade.Oid', 'EQUAL', trade.Oid())

    if settlementTypes is not None:
        numberOfSettlementTypes = len(settlementTypes)
        if numberOfSettlementTypes == 1:
            query.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', settlementTypes[0]))
        elif numberOfSettlementTypes > 1:
            typeNode = query.AddOpNode('Or')  
            for settlementType in settlementTypes:
                typeNode.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', settlementType))
    
    startDateOrSmallDate = startDate if startDate != '' and startDate is not None else earliestSettledDay
    query.AddAttrNode('SettledDay', 'GREATER_EQUAL', startDateOrSmallDate)
    if endDate is not None and endDate != '':
        query.AddAttrNode('SettledDay', 'LESS_EQUAL', endDate)
    
    return query.Select()
