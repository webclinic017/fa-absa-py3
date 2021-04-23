"""
Override of the Synthetic Prime module.

Keep the Prime 2017 version of FSyntheticPrimeFixing
to preserve the logic around fixing resets during the RTM tasks.

In the 2018 prime version fixing resets is done in the FIS
internal function, behaves differently and requires a change
in the configuration of the RTM portfolio swap let types.

TODO: Fix the portfolio swap and remove this override.
"""
import acm
import time
import FSyntheticPrimeUtil as Util
import importlib
importlib.reload(Util)
import FSyntheticPrimeCalculationAPIUtil as CalcUtil
importlib.reload(CalcUtil)

fixResets = acm.GetFunction("fixResets", 1)
#----------------------------------------------------------------------------
# Standard columns
#----------------------------------------------------------------------------
colIdPnLEndDate = "Portfolio Profit Loss End Date"
colIdPnLEndDateCustom = "Portfolio Profit Loss End Date Custom"
colIdPnLDividendCompMethod = "Portfolio Profit Loss Dividend Comparison Method"
colIdClientFloatRef = "Portfolio Swap Client Float Reference"
#----------------------------------------------------------------------------
# Total return
#----------------------------------------------------------------------------
def _ColIdReturnTPL():
    return "Portfolio Cost Profit and Loss Portfolio Currency"
#----------------------------------------------------------------------------
# Financing
#----------------------------------------------------------------------------
def _ColIdFinancingAmount():
    return "Portfolio Unfunded Cash Portfolio Currency"
    
def _ColIdTotalFinancingSpread():
    return "Total Financing Spread"
#----------------------------------------------------------------------------
# Dividend
#----------------------------------------------------------------------------
def _ColIdDidivendNominal():
    return "Portfolio Open Invested"

def _ColIdDidivendScalingPrice():
    return "Portfolio Negative Average Value"
#----------------------------------------------------------------------------
# Stock Borrow
#----------------------------------------------------------------------------
def _ColIdStockBorrowSpreadHook():
    return "Stock Borrow Spread"
    
def _ColIdStockBorrowAmount():
    return "Portfolio Open Invested Portfolio Currency"
#----------------------------------------------------------------------------
def FixPortfolioSwapResets(pfsParameters, date, fixSingleDate):
    portfolioSwap = pfsParameters.PortfolioSwap()
    resetsToFix = fixSingleDate and _GetResetsToFixOnDate(portfolioSwap, date) or _GetResetsToFixBeforeDate(portfolioSwap, date)
    if resetsToFix:
        _FixResets(pfsParameters, resetsToFix)
#----------------------------------------------------------------------------
def _FixResets(pfsParameters, resetsToFix):
    clientFloatRef = pfsParameters.GetClientSpreadInstrument()
    context = acm.GetDefaultContext()
    sheetType = acm.FPortfolioSheet
    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
    calcSpace.SimulateGlobalValue(colIdPnLEndDate, "Custom Date")
    calcSpace.SimulateGlobalValue(colIdClientFloatRef, clientFloatRef)
    calcSpace.SimulateGlobalValue(colIdPnLDividendCompMethod, "Trade day vs ex div day")
    calcSpace.InsertItem(pfsParameters.FilteredPortfolio())
    calcSpace.Refresh()
    
    resetsToFixInFixingScript = []
    for reset in resetsToFix:
        column = _FixingColumnId(reset)
        if column:
            try:
                _FixReset(pfsParameters, reset, column, calcSpace)
            except Exception, e:
                if column == _ColIdTotalFinancingSpread() and not _ClientSpreadPrice(clientFloatRef, reset.Day()):
                    errMess = "Historical price missing for client spread rate index " + clientFloatRef.Name() + " at date " + reset.Day()
                    acm.Log(errMess)
                else:
                    acm.Log(str(e))
        else:
            resetsToFixInFixingScript.append(reset)
    if resetsToFixInFixingScript:
        fixResets(resetsToFixInFixingScript)
            
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDate)
    calcSpace.RemoveGlobalSimulation(colIdPnLDividendCompMethod)
    calcSpace.RemoveGlobalSimulation(colIdClientFloatRef)
#----------------------------------------------------------------------------
def _ClientSpreadPrice(clientSpreadIns, day):
    query = "day = '" + day + "' and instrument = " + str(clientSpreadIns.Oid())
    price = acm.FPrice.Select(query)
    return price
#----------------------------------------------------------------------------
def _GetResetsToFixOnDate(portfolioSwap, date):
    resets = []
    currentDate = acm.Time.DateNow()
    if acm.Time.DateDifference(currentDate, date) >= 0:
        for leg in portfolioSwap.Legs():
            resets.extend(list(leg.GetResetsToFix(date, acm.Time().DateAddDelta(date, 0, 0, 1))))
    return resets
#----------------------------------------------------------------------------
def _GetResetsToFixBeforeDate(portfolioSwap, date):
    resets = []
    currentDate = acm.Time.DateNow()
    fixUntilDate = acm.Time.DateDifference(currentDate, date) > 0 and date or currentDate
    for leg in portfolioSwap.Legs():
        resets.extend(list(leg.GetResetsToFix(None, fixUntilDate)))
    return resets
#----------------------------------------------------------------------------
def _FixReset(pfsParameters, reset, column, calcSpace):
    date = reset.Day()
    fixingValue = None
    columnValue = _CalculateColumnValue(pfsParameters, reset, column, date, calcSpace)

    if acm.Math.IsFinite(columnValue):
        if reset.Leg().IsFinancingLeg():
            if reset.ResetType() == "Nominal Scaling":
                fixingValue = -columnValue
                
            elif reset.ResetType() == "Spread":
                if abs(columnValue) < 1e-7:
                    fixingValue = 0.0
                else:
                    fixingValue = columnValue
         
        else:
            fixingValue = columnValue

    if fixingValue != None:
        reset.FixingValue = fixingValue
        reset.ReadTime(reset.Day())
#----------------------------------------------------------------------------
def _CalculateColumnValue(pfsParameters, reset, column, date, calcSpace):
    columnValue = 0.0
    calcSpace.SimulateGlobalValue(colIdPnLEndDateCustom, date)
    
    portfolioIter = calcSpace.RowTreeIterator().FirstChild()
    if reset.Leg().IndexRef():
        childIter = portfolioIter.FirstChild()
        while childIter:
            name = calcSpace.CalculateValue(childIter.Tree(), 'Instrument Name')
            if name == reset.Leg().IndexRef().Name():
                treeNode = childIter.Tree()
                break
            childIter = childIter.NextSibling()
    else:
        name = "Portfolio"
        treeNode = portfolioIter.Tree()
        
    columnValue = CalcUtil.CalculateRowValueAsDouble(calcSpace, \
                                                        treeNode, \
                                                        column, \
                                                        name, \
                                                        date)
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDateCustom)
    return columnValue
#----------------------------------------------------------------------------
def _FixingColumnId(reset):
    columnId = None
    if reset.ResetType() == "Settlement FX":
        return None
    if reset.Leg().IsFinancingLeg():
        if reset.ResetType() == "Nominal Scaling":
            columnId = _ColIdFinancingAmount()
        if reset.ResetType() == "Spread":
            columnId = _ColIdTotalFinancingSpread()
    if reset.Leg().IsPerformanceLeg():
        columnId = _ColIdReturnTPL()
    if reset.Leg().IsPerformanceDividendLeg():
        if reset.ResetType() == "Nominal Scaling":
            columnId = _ColIdDidivendNominal()
        if reset.ResetType() == "Dividend Scaling":
            columnId = _ColIdDidivendScalingPrice()
    if reset.Leg().IsStockBorrowLeg():
        if reset.ResetType() == "Nominal Scaling":
            columnId = _ColIdStockBorrowAmount()
        if reset.ResetType() == "Spread":
            columnId = _ColIdStockBorrowSpreadHook()
    
    return columnId
