import acm

portfolioId = acm.FTrade[69116182].PortfolioId()
portfolio = acm.FPhysicalPortfolio[portfolioId]
#print portfolio

context = acm.GetDefaultContext()
calcSpace = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
proxy = calcSpace.InsertItem(portfolio)
value = calcSpace.CreateCalculation(proxy, 'Portfolio Swap Execution Premium TPL', None).Value()

print(value)
