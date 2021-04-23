import acm
import time
import FSyntheticPrimeUtil as Util
import importlib
importlib.reload(Util)
import FSyntheticPrimeCalculationAPIUtil as CalcUtil
importlib.reload(CalcUtil)
import FSyntheticPrimeMaintainCF as MaintainCF
importlib.reload(MaintainCF)
import FSyntheticPrimeCreateCF as CreateCF
importlib.reload(CreateCF)
from DealPackageUtil import UnDecorate

#----------------------------------------------------------------------------
def CreatePortfolioSwapLegs(pfsParameters, fromDate, toDate):
    _CreatePerPortfolioSwapLegs(pfsParameters, fromDate, toDate)
    perSecurityLegs = CreatePerSecurityLegs(pfsParameters, fromDate, toDate)
    return perSecurityLegs
#----------------------------------------------------------------------------
def CreatePerSecurityLegs(pfsParameters, fromDate, toDate):
    newSecurities = _GetNewSecurities(pfsParameters.PortfolioSwap(), pfsParameters.FilteredPortfolio(), fromDate, toDate)
    return _GeneratePerSecurityLegs(pfsParameters, newSecurities, fromDate, toDate)
#----------------------------------------------------------------------------
def UpdatePortfolioSwapLegsEndDates(portfolioSwap, toDate):
    for leg in portfolioSwap.Legs():
        leg.EndDate = _CalculateLegEndDate(leg, portfolioSwap.ExpiryDate(), toDate)
#----------------------------------------------------------------------------
def _GetPortfolioSecurities(portfolio, date):
    globalSimulations = [("Portfolio Profit Loss End Date", "Custom"), \
                        ("Portfolio Profit Loss End Date Custom", date)]
    columnIds = ["Instrument Name", "Portfolio Profit Loss Period Position"]
    columnValues = CalcUtil.CalculatePerSecurityColumnValues(portfolio, columnIds, globalSimulations)
    securities = []
    for columnValuesSecurity in columnValues:
        checkNonZeroValues = columnValuesSecurity[1:]
        if _CheckAnyNonZero(checkNonZeroValues):
            securityName = columnValuesSecurity[0]
            security = acm.FInstrument[securityName]
            if not security:
                raise Exception("Instrument not found: '%s' - Exits"%securityName)
            securities.append(security)
    return securities
#----------------------------------------------------------------------------
def _CheckAnyNonZero(values):
    for value in values:
        if type(value) in (float, int):
            number = value
        elif hasattr(value, "IsKindOf") and value.IsKindOf(acm.FDenominatedValue):
            number = value.Number()
        elif not value:
            number = 0.0
        else:
            raise Exception("Unknown return type: %s"%str(type(value)))
        if number:
            return True
    return False
#----------------------------------------------------------------------------
def _GetPeriodSecurities(portfolio, periodStartDate, periodEndDate):
    periodSecuritiesDict = {}
    date = periodStartDate
    while acm.Time().DateDifference(periodEndDate, date) >= 0:
        dateSecurities = _GetPortfolioSecurities(portfolio, date)
        for security in dateSecurities:
            securityName = security.Name()
            if not periodSecuritiesDict.has_key(securityName):
                periodSecuritiesDict[securityName] = security
        date = acm.Time().DateAddDelta(date, 0, 0, 1)
    return periodSecuritiesDict.values()
#----------------------------------------------------------------------------
def _GetExistingSecurities(portfolioSwap):
    securities = []
    for leg in portfolioSwap.Legs():
        if leg.IsPerformanceLeg() or leg.IsPerformanceRPLLeg():
            indexRef = leg.IndexRef()
            if not indexRef in securities:
                securities.append(indexRef)
    return securities
#----------------------------------------------------------------------------
def _GetNewSecurities(portfolioSwap, portfolio, periodStartDate, periodEndDate):
    newSecurities = []
    existingSecurities = _GetExistingSecurities(portfolioSwap)
    securities = _GetPeriodSecurities(portfolio, periodStartDate, periodEndDate)
    for security in securities:
        if not security in existingSecurities:
            newSecurities.append(security)
    return newSecurities
#----------------------------------------------------------------------------
def _CalculateLegEndDate(leg, maxEndDate, toDate):
    return min(maxEndDate, toDate)
#----------------------------------------------------------------------------
def _CalculateLegStartDate(leg, minStartDate, fromDate):
    return max(minStartDate, fromDate)
#----------------------------------------------------------------------------
def _AdjustForAdjustCash(callDepositLeg, pfsParameters):
    adjustCashPaymentType = Util.GetAdjustCashPaymentType()
    portfolioSwapTrade = pfsParameters.DealPackage().TradeAt("PrfSwap")

    for payment in portfolioSwapTrade.Payments():
        if payment.Type() == adjustCashPaymentType:
            newCashFlow = callDepositLeg.CreateCashFlow()
            newCashFlow.CashFlowType("Fixed Amount")
            newCashFlow.FixedAmount(-payment.Amount())
            newCashFlow.FloatRateFactor(callDepositLeg.FloatRateFactor())
            newCashFlow.NominalFactor(callDepositLeg.NominalFactor())
            newCashFlow.PayDate(payment.PayDay())
            newCashFlow.FixedRate(callDepositLeg.FixedRate())

#----------------------------------------------------------------------------
def _CreatePerPortfolioSwapLegs(pfsParameters, \
                                fromDate, \
                                toDate):
    if pfsParameters.CashEnabled():
        callDepositLeg = _CreateCallDepositLeg(pfsParameters, fromDate, toDate)
    if Util.UsePerPortfolioFunding():
        financingLeg = _CreateSingleFinancingLeg(pfsParameters, fromDate, toDate)
#----------------------------------------------------------------------------
def _GeneratePerSecurityLegs(pfsParameters, securities, fromDate, toDate):
    perSecurityLegs = []
    for security in securities:
        rplPerformanceLeg = None
        uplPerformanceLeg = None
        performanceLeg = None
        financingLeg = None
        repoLeg = None
        executionFeeLeg = None
        
        if not pfsParameters.NoPerformanceSplitEnabled():
            rplPerformanceLeg = pfsParameters.GetPerformanceRPLLeg(security)
            if not rplPerformanceLeg:
                metaLeg = pfsParameters.PerformanceRPLMetaLeg()
                rplPerformanceLeg = _CreateTotalReturnLeg(pfsParameters, metaLeg, fromDate, toDate, security)
            
            uplPerformanceLeg = pfsParameters.GetPerformanceUPLLeg(security)
            if not uplPerformanceLeg:
                metaLeg = pfsParameters.PerformanceUPLMetaLeg()
                uplPerformanceLeg = _CreateTotalReturnLeg(pfsParameters, metaLeg, fromDate, toDate, security)

        else:
            performanceLeg = pfsParameters.GetPerformanceLeg(security)
            if not performanceLeg:
                metaLeg = pfsParameters.PerformanceMetaLeg()
                performanceLeg = _CreateTotalReturnLeg(pfsParameters, metaLeg, fromDate, toDate, security)
        
        if not Util.UsePerPortfolioFunding():
            financingLeg = _CreateFinancingLeg(pfsParameters, fromDate, toDate, security)

        if pfsParameters.StockBorrowEnabled():
            repoLeg = _CreateStockBorrowLeg(pfsParameters, fromDate, toDate, security)

        executionFeeLeg = _CreateExecutionFeeLeg(pfsParameters, fromDate, toDate, security)
        
        perSecurityLegs.append([rplPerformanceLeg, uplPerformanceLeg, performanceLeg, financingLeg, repoLeg, executionFeeLeg])
    return perSecurityLegs
#----------------------------------------------------------------------------
def _CreateLegFromMetaLeg(metaLeg, portfolioSwap):
    leg = None
    if metaLeg:
        leg = UnDecorate(metaLeg.Clone())
        leg.Instrument = portfolioSwap
        leg.RegisterInStorage()
        leg.CashFlows().Delete()
    return leg
#----------------------------------------------------------------------------
def _SetLegAttributes(metaLeg, pfsParameters, fromDate, toDate, security, floatRef, originalCurrency):
    portSwap = pfsParameters.PortfolioSwap()
    leg = _CreateLegFromMetaLeg(metaLeg, portSwap)
    if leg:
        leg.StartDate = _CalculateLegStartDate(leg, portSwap.StartDate(), fromDate)
        leg.EndDate = _CalculateLegEndDate(leg, portSwap.ExpiryDate(), toDate)
        leg.IndexRef = security
        if floatRef:
            leg.FloatRateReference = floatRef
        if originalCurrency and originalCurrency != leg.Currency():
            leg.OriginalCurrency = originalCurrency
    return leg
#----------------------------------------------------------------------------
def _GetFundPortfolioCurrency(pfsParameters):
    return pfsParameters.FundPortfolio().Currency() if pfsParameters.FundPortfolio() else None
#----------------------------------------------------------------------------
def _CreateTotalReturnLeg(pfsParameters, metaLeg, fromDate, toDate, security):
    originalCurrency = _GetFundPortfolioCurrency(pfsParameters)
    return _SetLegAttributes(metaLeg, pfsParameters, fromDate, toDate, security, security, originalCurrency)
#----------------------------------------------------------------------------
def _CreateFinancingLeg(pfsParameters, fromDate, toDate, security):
    leg = pfsParameters.GetFinancingLeg(security)
    if not leg:
        metaLeg = pfsParameters.FinancingMetaLeg()
        originalCurrency = _GetFundPortfolioCurrency(pfsParameters)
        leg = _SetLegAttributes(metaLeg, pfsParameters, fromDate, toDate, security, None, originalCurrency)
    return leg
#----------------------------------------------------------------------------
def _CreateSingleFinancingLeg(pfsParameters, fromDate, toDate):
    return _CreateFinancingLeg(pfsParameters, fromDate, toDate, None)
#----------------------------------------------------------------------------
def _CreateStockBorrowLeg(pfsParameters, fromDate, toDate, security):
    leg = pfsParameters.GetStockBorrowLeg(security)
    if not leg:
        metaLeg = pfsParameters.StockBorrowMetaLeg()
        originalCurrency = _GetFundPortfolioCurrency(pfsParameters)
        leg = _SetLegAttributes(metaLeg, pfsParameters, fromDate, toDate, security, None, originalCurrency)
    return leg
#----------------------------------------------------------------------------
def _CreateCallDepositLeg(pfsParameters, fromDate, toDate):
    leg = pfsParameters.GetSyntheticCashLeg()
    if not leg:
        metaLeg = pfsParameters.SyntheticCashMetaLeg()
        leg = _SetLegAttributes(metaLeg, pfsParameters, fromDate, toDate, None, None, None)
        rolling = pfsParameters.DealPackage().GetAttribute('cashRolling')
        if rolling[0] == '0':
            _AdjustForAdjustCash(leg, pfsParameters)
    return leg
#----------------------------------------------------------------------------
def _CreateExecutionFeeLeg(pfsParameters, fromDate, toDate, security):
    leg = pfsParameters.GetFeeLeg(security)
    if not leg:
        metaLeg = pfsParameters.FeeMetaLeg()
        originalCurrency = pfsParameters.DealPackage().InstrumentAt("MetaLegs").OriginalCurrency()
        leg = _SetLegAttributes(metaLeg, pfsParameters, fromDate, toDate, security, None, originalCurrency)
    return leg
#----------------------------------------------------------------------------
def UpdatePortfolioSwapCashFlowsPayDates(pfsParameters, endDate):
    portfolioSwap = pfsParameters.PortfolioSwap()
    startDate = pfsParameters.DealPackage().GetAttribute('startDate')
    legs = [leg for leg in portfolioSwap.Legs() if (leg.IsPerformanceLeg() or leg.IsPerformanceRPLLeg() or leg.IsPerformanceUPLLeg() or leg.IsFinancingLeg() or leg.IsStockBorrowLeg() or leg.IsSyntheticCashLeg())]
    for leg in legs:
        for cf in leg.CashFlows():
            if cf.StartDate() <= endDate and cf.PayDate() > endDate:
                cf.PayDate(endDate)
                cf.EndDate(endDate)
#----------------------------------------------------------------------------
def UpdatePerformanceLegResetDates(pfsParameters, terminateDate):
    def LastCashFlow(leg):
        lastCashFlow = leg.CashFlows().First()
        if leg.CashFlows().Size():
            for cashFlow in leg.CashFlows():
                if acm.Time.DateDifference(cashFlow.StartDate(), lastCashFlow.StartDate()) > 0:
                    lastCashFlow = cashFlow
        return lastCashFlow
    
    def LastReset(cashFlow):
        lastReset = cashFlow.Resets().First()
        if cashFlow.Resets().Size():
            for reset in cashFlow.Resets():
                if acm.Time.DateDifference(reset.Day(), lastReset.Day()) > 0:
                    lastReset = reset
        return lastReset
            
    portfolioSwap = pfsParameters.PortfolioSwap()
    for leg in portfolioSwap.Legs():
        if leg.IsPerformanceLeg() or leg.IsPerformanceRPLLeg() or leg.IsPerformanceUPLLeg():
            lastCashFlow = LastCashFlow(leg)
            if lastCashFlow:
                lastResetDate = Util.AdjustBankingDays(leg, terminateDate, leg.ResetDayOffset())
                lastReset = LastReset(lastCashFlow)
                if lastCashFlow.Resets().Size() == 1:
                    lastReset = lastReset.StorageNew()
                    leg.Resets().Add(lastReset) # Because of a bug, it does not show up in this set before commit
                lastReset.Day(lastResetDate)
                lastReset.StartDate(terminateDate)
                lastReset.EndDate(terminateDate)
                lastReset.ReadTime(0)
                    
