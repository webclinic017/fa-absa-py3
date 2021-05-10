import acm
#----------------------------------------------------------------------------     
def GetPortfolioSwapSecurity(moneyFlow):
    security = None
    cashFlow = moneyFlow.CashFlow()
    if cashFlow:
        security = cashFlow.Leg().IndexRef()
    return security
#----------------------------------------------------------------------------     
def GetPortfolioSwapLegTypeFromMF(moneyFlow):
    legType = None
    cashFlow = moneyFlow.CashFlow()
    if cashFlow:
        legType = cashFlow.Leg().CategoryChlItem()
    return legType 
#----------------------------------------------------------------------------
