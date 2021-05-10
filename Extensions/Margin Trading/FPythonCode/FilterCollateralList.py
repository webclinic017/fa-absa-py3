
import acm

def getCollateralList(name):
    return acm.FStoredASQLQuery.Select01("name='%s'" % name, None)

def getCollateralListForPortfolio(portfolio):
    name = portfolio.AdditionalInfo().CollateralList()
    if name:
        return getCollateralList(name)
    else:
        return acm.FStoredASQLQuery
    
def filterTradesBasedOnInstrumentList(portfolio, instruments, marginableInstruments):
    marginableTrades = acm.FFilteredSet()
    for i in instruments.Intersection( marginableInstruments or [] ):
        marginableTrades.AddSource( portfolio.TradesIn( i ) )
    return marginableTrades    
    
