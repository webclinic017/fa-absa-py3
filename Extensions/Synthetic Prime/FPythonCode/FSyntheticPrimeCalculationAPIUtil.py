import acm
#----------------------------------------------------------------
def CalculatePerSecurityColumnValues(portfolio, columnIds, globalSimulations):
    calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FPortfolioSheet)
    calcSpace.InsertItem(portfolio)
    ApplySimulations(calcSpace, globalSimulations, None)
    calcSpace.Refresh()
    portfolioIter = calcSpace.RowTreeIterator().FirstChild()
    securityIter = portfolioIter.FirstChild()
    
    perSecurityValues = []
    while securityIter:
        securityValues = []
        for colId in columnIds:
            colValue = calcSpace.CalculateValue(securityIter.Tree(), colId)
            securityValues.append(colValue)
        perSecurityValues.append(securityValues)
        securityIter = securityIter.NextSibling()

    RemoveSimulations(calcSpace, globalSimulations, None)
    return perSecurityValues
#----------------------------------------------------------------------------
nanStr = str(acm.Math.NotANumber())
def _CheckForNaN(value, fieldId, entityId, date):
    global nanStr
    if nanStr == str(value):
        errMess = "NaN in input data for entity '%s', %s = %s (date: %s)"%(entityId, fieldId, str(value), date)
        raise Exception(errMess)
        return True
    return False
#----------------------------------------------------------------------------
def ApplySimulations(calcSpace, globalSimulations, localSimulations):
    if globalSimulations:
        for colId, value in globalSimulations:
            calcSpace.SimulateGlobalValue(colId, value)
    if localSimulations:
        for object, colId, value in localSimulations:
            calcSpace.SimulateValue(object, colId, value)
#----------------------------------------------------------------------------
def RemoveSimulations(calcSpace, globalSimulations, localSimulations):
    if globalSimulations:
        for colId, value in globalSimulations:
            calcSpace.RemoveGlobalSimulation(colId)
    if localSimulations:
        for object, colId, value in localSimulations:
            calcSpace.RemoveSimulation(object, colId)
