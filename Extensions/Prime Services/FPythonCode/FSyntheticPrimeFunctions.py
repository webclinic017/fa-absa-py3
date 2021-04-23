import acm
import time
import FSyntheticPrimeCreateLegs as CreateLegs
import importlib
importlib.reload(CreateLegs)
import FSyntheticPrimeMaintainCF as MaintainCF
importlib.reload(MaintainCF)
import FSyntheticPrimeCreateCF as CreateCF
importlib.reload(CreateCF)
import FSyntheticPrimeFixing as Fixing
importlib.reload(Fixing)
import FSyntheticPrimeUtil as Util
importlib.reload(Util)

#----------------------------------------------------------------------------
def TradeAssign(pfsParameters, fromDate, toDate):
    #Remove passing of fromDate to function
    fromDate = pfsParameters.PortfolioSwap().StartDate()
    newLegs = CreateLegs.CreatePerSecurityLegs(pfsParameters, fromDate, toDate)
    MaintainCF.GeneratePerSecurityCashFlows(newLegs)
    Fixing.FixPortfolioSwapResets(pfsParameters, toDate, False)
#----------------------------------------------------------------------------
def GeneratePortfolioSwap(pfsParameters, fromDate, toDate):
    portfolioSwap = pfsParameters.PortfolioSwap()
    Util.ClearFeeDividendAndSyntheticCashflows(portfolioSwap, fromDate)
    Util.ClearPortfolioSwapLegs(portfolioSwap, fromDate)
    payCal=pfsParameters.DealPackage().GetAttribute('payCalendar')
    dayAfterToDate=payCal.AdjustBankingDays(toDate, 1)
    rolling = pfsParameters.DealPackage().GetAttribute('cashRolling')
    if rolling[0] != '0':
        portfolioSwapTrade = pfsParameters.DealPackage().TradeAt("PrfSwap")
        Util.ClearPortfolioSwapPaymentsPostDate(portfolioSwapTrade, fromDate)
    CreateLegs.CreatePortfolioSwapLegs(pfsParameters, fromDate, dayAfterToDate)
    CreateLegs.UpdatePortfolioSwapLegsEndDates(portfolioSwap, dayAfterToDate)
    MaintainCF.ExtendCashFlows(portfolioSwap, fromDate)
    MaintainCF.RegenerateDividendCashFlows(portfolioSwap, fromDate, toDate)
    # CreateCF.CreateDailyExecutionFeeCashFlows(pfsParameters, fromDate, toDate, True)  # override
    Fixing.FixPortfolioSwapResets(pfsParameters, dayAfterToDate, False)
    if pfsParameters.CashEnabled():
        callDepositLeg = pfsParameters.GetSyntheticCashLeg()
        CreateCF.CreateRedemptionCashFlow(callDepositLeg)
        MaintainCF.SetCallAccountEndDate(callDepositLeg, dayAfterToDate)    
        SweepCashPortfolioSwap(pfsParameters, fromDate, toDate)
        CreateCF.CreatePeriodicalPayouts(pfsParameters, dayAfterToDate)

#----------------------------------------------------------------------------
def ExtendPortfolioSwap(pfsParameters, date):
    payCal=pfsParameters.DealPackage().GetAttribute('payCalendar')
    toDate=payCal.AdjustBankingDays(date, 1)
    CreateLegs.UpdatePortfolioSwapLegsEndDates(pfsParameters.PortfolioSwap(), toDate)
    MaintainCF.ExtendCashFlows(pfsParameters.PortfolioSwap(), date)
    MaintainCF.RegenerateDividendCashFlows(pfsParameters.PortfolioSwap(), date, toDate)
    # CreateCF.CreateDailyExecutionFeeCashFlows(pfsParameters, pfsParameters.PortfolioSwap().StartDate(), date, True)  # override
    Fixing.FixPortfolioSwapResets(pfsParameters, toDate, False)
    if pfsParameters.CashEnabled():
        callDepositLeg = pfsParameters.GetSyntheticCashLeg()
        CreateCF.CreateRedemptionCashFlow(callDepositLeg)
        MaintainCF.SetCallAccountEndDate(callDepositLeg, toDate)
        CreateCF.SweepCash(pfsParameters, date)
        CreateCF.CreatePeriodicalPayout(pfsParameters, toDate)
#----------------------------------------------------------------------------
def FixPortfolioSwapResetsOnDate(pfsParameters, date):
    Fixing.FixPortfolioSwapResets(pfsParameters, date, True)
#----------------------------------------------------------------------------
def TerminatePortfolioSwap(pfsParameters, terminateDate = None):

    def ClearLegsCashFlowsResetsAndPaymentsAfterTerminateDate(portfolioSwap, portfolioSwapTrade):
        dayAfterTerminateDate = Util.AdjustBankingDays(portfolioSwap.Legs().First(), terminateDate, 1)
        Util.ClearFeeDividendAndSyntheticCashflows(portfolioSwap, dayAfterTerminateDate) # Clear cashflows starting tomorrow
        Util.ClearPerformanceFinancingAndStockBorrowCashflows(portfolioSwap, terminateDate) # Clear cashflows starting today
        Util.ClearPortfolioSwapLegs(portfolioSwap, dayAfterTerminateDate)
        Util.ClearPortfolioSwapResets(portfolioSwap, dayAfterTerminateDate) 
        Util.ClearPortfolioSwapPaymentsPostDate(portfolioSwapTrade, dayAfterTerminateDate)
       
    portfolioSwap = pfsParameters.PortfolioSwap()
    portfolioSwapTrade = pfsParameters.DealPackage().TradeAt("PrfSwap")
    startDate = portfolioSwap.StartDate()
    endDate = portfolioSwap.LongestLeg().EndDate()
    if not terminateDate:
        terminateDate = endDate
    pfsParameters.DealPackage().SetAttribute('expiryDate', terminateDate)
    ClearLegsCashFlowsResetsAndPaymentsAfterTerminateDate(portfolioSwap, portfolioSwapTrade)
    CreateLegs.UpdatePortfolioSwapLegsEndDates(portfolioSwap, terminateDate)
    CreateLegs.UpdatePortfolioSwapCashFlowsPayDates(pfsParameters, terminateDate)
    CreateLegs.UpdatePerformanceLegResetDates(pfsParameters, terminateDate)
    Fixing.FixPortfolioSwapResets(pfsParameters, terminateDate, False)
    if pfsParameters.CashEnabled():
        callDepositLeg = pfsParameters.GetSyntheticCashLeg()
        CreateCF.CreateRedemptionCashFlow(callDepositLeg)
        MaintainCF.SetCallAccountEndDate(callDepositLeg, terminateDate)
        SweepCashPortfolioSwap(pfsParameters, startDate, terminateDate)
        Util.PayOutAllCash(pfsParameters, startDate, terminateDate)
    
    portfolioSwap.OpenEnd('Terminated')
#----------------------------------------------------------------------------
def SweepCashPortfolioSwap(pfsParameters, fromDate, toDate):    
    #Sweep all dates (banking days of the pay calendar) from fromDate until toDate    
    
    #Never sweep beyond today
    toSweepDate = toDate
    if toSweepDate > acm.Time.DateToday():
        toSweepDate = acm.Time.DateToday()
        
    cal = pfsParameters.PayCalendar()
    while fromDate <= toSweepDate:
        CreateCF.SweepCash(pfsParameters, fromDate)
        fromDate = cal.AdjustBankingDays(fromDate, 1)
#----------------------------------------------------------------------------
