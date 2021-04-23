import acm
import time
import FSyntheticPrimeUtil as Util
import importlib
importlib.reload(Util)
import FSyntheticPrimeCalculationAPIUtil as CalcUtil
importlib.reload(CalcUtil)

fixResets = acm.GetFunction("fixResets", 1)
#----------------------------------------------------------------------------
def FixPortfolioSwapResets(pfsParameters, date, fixSingleDate):
    portfolioSwap = pfsParameters.PortfolioSwap()
    resetsToFix = fixSingleDate and _GetResetsToFixOnDate(portfolioSwap, date) or _GetResetsToFixBeforeDate(portfolioSwap, date)
    if resetsToFix:
        _FixResets(pfsParameters, resetsToFix)
#----------------------------------------------------------------------------
def _FixResets(pfsParameters, resetsToFix):
    fixResets(resetsToFix)
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
