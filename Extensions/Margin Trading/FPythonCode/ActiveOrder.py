import acm

def activeOrdersFilteredSetFilteredForInstrument(activeOrdersCollection, instrument):
    saq = acm.Filter.SimpleAndQuery
    filtered_set = acm.FFilteredSet(activeOrdersCollection)
    filtered_set.Filter = saq(acm.FActiveOrder, "instrument.Oid", None, instrument.Oid())
    return filtered_set
    
def activeOrdersSingleSide(portfolioActiveOrders, buy):
    filtered_set = acm.FFilteredSet(portfolioActiveOrders)
    if buy:
        filtered_set.Filter = acm.Filter.SimpleAndQuery( acm.FActiveOrder, "Quantity", "GREATER", 0 )
    else:
        filtered_set.Filter = acm.Filter.SimpleAndQuery( acm.FActiveOrder, "Quantity", "LESS", 0 )
    return filtered_set
    
def activeOrdersFilteredSetFilteredForInstrumentCompound(activeOrdersCollections, instrument):
    saq = acm.Filter.SimpleAndQuery
    filtered_set = acm.FFilteredSet()
    for aoc in activeOrdersCollections:
        filtered_set.AddSource( aoc )
    filtered_set.Filter = saq(acm.FActiveOrder, "instrument.Oid", "EQUAL", instrument.Oid())
    return filtered_set

def activeOrdersHandler(activeOrdersSubset, portfolioActiveOrders):
    return activeOrdersSubset
