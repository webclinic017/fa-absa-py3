"""
Override of the Synthetic Prime module.

Keep the Prime 2017 version of FSyntheticPrimeCalculationAPIUtil
to preserve the logic around fixing resets during the RTM tasks.

In the 2018 prime version fixing resets is done in the FIS
internal function, behaves differently and requires a change
in the configuration of the RTM portfolio swap let types.

TODO: Fix the portfolio swap and remove this override.
"""
import acm
#----------------------------------------------------------------
def CalculateRowValueAsDouble(calcSpace, \
                                rowNode, \
                                colId, \
                                entityId = None, \
                                date = None, \
                                replaceNaNWithZero = False, \
                                columnConfig = None):
    rowValue = calcSpace.CalculateValue(rowNode, colId, columnConfig)
    success = True
    if hasattr(rowValue, "IsKindOf") and rowValue.IsKindOf(acm.FArray):
        if 1 == len(rowValue):
            rowValue = rowValue[0]
        else:
            success = False

    if success:
        if hasattr(rowValue, "IsKindOf"):
            if rowValue.IsKindOf(acm.FDenominatedValue):
                rowValue = rowValue.Number()
            elif not rowValue.IsKindOf(acm.FReal):
                success = False
        elif not type(rowValue) in (float, int):
            success = False
    if not success:
        acm.Log("Calculated value from column %s could not be converted to a number: %s" \
                            %(colId, str(rowValue)))
    _CheckForNaN(rowValue, colId, entityId, date)
    return rowValue


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
