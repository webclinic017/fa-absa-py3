import acm
import time
import FSyntheticPrimeUtil as Util
import importlib
importlib.reload(Util)
import FSyntheticPrimeCreateCF as CreateCF
importlib.reload(CreateCF)

#----------------------------------------------------------------------------
def GeneratePerPortfolioSwapCashFlows(portfolioSwap, fromDate):
    if Util.UsePerPortfolioFunding():
        financingLeg = Util.GetSingleFinancingLeg(portfolioSwap)
        financingLeg.GenerateCashFlowsFromDate(fromDate)
    syntheticCashLeg = Util.GetCallDepositLeg(portfolioSwap, False)
    if syntheticCashLeg:
        syntheticCashLeg.GenerateCashFlowsFromDate(fromDate)
#----------------------------------------------------------------------------
def GeneratePerSecurityCashFlows(perSecurityLegs):
    for securityLegs in perSecurityLegs:
        for leg in securityLegs:
            if leg and leg.StartDate() < leg.EndDate():
                leg.GenerateCashFlowsFromDate(leg.StartDate())
#----------------------------------------------------------------------------
def _GetLegsToExtend(portfolioSwap):
    legs = []
    for leg in portfolioSwap.Legs():
        if leg.IndexRef:
            isDividendLeg = leg.IsDividendLeg() and leg.PassingType() == "CashFlow Payday"
            if leg.IsPerformanceLeg() or leg.IsPerformanceRPLLeg() or leg.IsPerformanceUPLLeg() or leg.IsFinancingLeg() or leg.IsStockBorrowLeg() or isDividendLeg:
                legs.append(leg)
    callDepositLeg = Util.GetCallDepositLeg(portfolioSwap, False)
    if callDepositLeg:
        legs.append(callDepositLeg)
    if Util.UsePerPortfolioFunding():
        legs.append(Util.GetSingleFinancingLeg(portfolioSwap))
    return legs
#----------------------------------------------------------------------------
def ExtendCashFlows(portfolioSwap, fromDate):
    legs = _GetLegsToExtend(portfolioSwap)
    for leg in legs:
        leg.ExtendToEnd(fromDate)
#----------------------------------------------------------------------------           
def RegenerateDividendCashFlows(portfolioSwap, fromDate, toDate):

    def SetDividendLegCategory(portfolioSwap):
        from PortfolioSwapMetaLegs import LEG_CATEGORY_DIVIDEND
        for leg in portfolioSwap.Legs():
            if leg.IsDividendLeg() and None == leg.CategoryChlItem():
                leg.CategoryChlItem(LEG_CATEGORY_DIVIDEND)
    portfolioSwap.RegenerateDividendCashFlows(fromDate, toDate)
    SetDividendLegCategory(portfolioSwap)
#----------------------------------------------------------------------------
def SetCallAccountEndDate(callDepositLeg, endDate):
    redemptionCF = Util.GetRedemptionCashFlowFromLeg(callDepositLeg, True)
    redemptionCF.EndDate = endDate
    redemptionCF.PayDate = endDate
#----------------------------------------------------------------------------
