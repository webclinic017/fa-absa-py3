import acm

#-----------------------------------------------------------------------
def ValidMoneyFlowTypes(extension):
    enums = acm.FEnumeration['enum(SettlementCashFlowType)']

    excludedMoneyFlowTypes = extension.split(';')
    
    validMoneyFlowTypes = acm.FArray()
    
    for e in enums.Enumerators():
        if e not in excludedMoneyFlowTypes:
            validMoneyFlowTypes.Add(enums.Enumeration(e))
            
    return validMoneyFlowTypes

#-----------------------------------------------------------------------
def TradesPerCounterparty( trades ):
    tradesPerCounterParty = acm.FDictionary()
    
    for trade in trades:
        parent = trade.Counterparty()
        
        while parent:
            AddTradeForCounterparty( tradesPerCounterParty, trade, parent )
            
            parent = parent.Parent()
            
    return tradesPerCounterParty

#-----------------------------------------------------------------------        
def AddTradeForCounterparty( tradesPerCounterParty, trade, counterparty ):
    if not tradesPerCounterParty.HasKey( counterparty ):
        tradesPerCounterParty[counterparty] = acm.FArray()
        
    tradesPerCounterParty[counterparty].Add( trade )

