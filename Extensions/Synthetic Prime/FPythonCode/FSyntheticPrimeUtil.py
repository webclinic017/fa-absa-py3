import acm
import FSyntheticPrimeCalculationAPIUtil as CalcUtil
import importlib
importlib.reload(CalcUtil)
import time

createCalendarInformation = acm.GetFunction('createCalendarInformation', 1)
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Portfolio Swap specific get-functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def GetSingleFinancingLeg(portfolioSwap):
    legs = [leg for leg in portfolioSwap.Legs() if leg.IsFinancingLeg()]
    singleFinancingLeg = 1 == len(legs) and legs[0] or None
    if not singleFinancingLeg:
        raise Exception("Single financing leg was not found. Portfolio swap is not set up correctly - Exits")
    return singleFinancingLeg
#----------------------------------------------------------------------------
def GetCallDepositLeg(portfolioSwap, raiseException = True):
    legs = [leg for leg in portfolioSwap.Legs() if leg.IsSyntheticCashLeg()]
        
    callDepositLeg = 1 == len(legs) and legs[0] or None
    if not callDepositLeg and raiseException:
        raise Exception("Single call deposit leg was not found. Portfolio swap is not set up correctly - Exits")
    return callDepositLeg
#----------------------------------------------------------------------------
def GetRedemptionCashFlowFromLeg(callDepositLeg, raiseException = True):
    cashFlows = [cf for cf in callDepositLeg.CashFlows() if "Redemption Amount" == cf.CashFlowType()]
    
    redemptionCF = 1 == len(cashFlows) and cashFlows[0] or None
    if not redemptionCF and raiseException:
        raise Exception("Redemption cash flow not found. Portfolio swap is not set up correctly - Exits")
    return redemptionCF
#----------------------------------------------------------------------------
def ClearPortfolioSwapLegs(portfolioSwap, fromDate):
    legs = [leg for leg in portfolioSwap.Legs()]
    for leg in legs:
        clearFromDate = fromDate 
        if leg.StartDate() >= clearFromDate:
            if leg.IsInfant():
                leg.Delete()
            else:
                portfolioSwap.Legs().Remove(leg)
                leg.Unsimulate()
#----------------------------------------------------------------------------
def ClearFeeDividendAndSyntheticCashflows(portfolioSwap, date):
        
    def CashflowsGreaterThanDate(leg, date):
        cashflows = acm.FArray()
        for cf in leg.CashFlows():
            if leg.IsDividendLeg(): 
                if acm.Time.DateDifference(cf.StartDate(), date) >= 0:
                    cashflows.Add(cf)
            elif leg.IsFeeLeg() or leg.IsSyntheticCashLeg():
                if cf.CashFlowType() == 'Call Float Rate':
                    if acm.Time.DateDifference(cf.StartDate(), date) >= 0:
                        cashflows.Add(cf)
                else:
                    if acm.Time.DateDifference(cf.PayDate(), date) >= 0:
                        cashflows.Add(cf)
        return cashflows
                
    legs = [leg for leg in portfolioSwap.Legs() if (leg.IsFeeLeg() or leg.IsDividendLeg() or leg.IsSyntheticCashLeg())]
    for leg in legs:
        cashflows = CashflowsGreaterThanDate(leg, date)
        for cashflow in cashflows:
            leg.CashFlows().Remove(cashflow)
            cashflow.Unsimulate()
#----------------------------------------------------------------------------
def ClearPerformanceFinancingAndStockBorrowCashflows(portfolioSwap, date):
        
    def CashflowsGreaterThanDate(leg, date):
        filteredSet = acm.FFilteredSet(leg.CashFlows())
        filter = acm.Filter.SimpleOrQuery(acm.FCashFlow, ['StartDate'], ['GREATER_EQUAL'], [date])
        filteredSet.Filter(filter)
        return filteredSet
    legs = [leg for leg in portfolioSwap.Legs() if (leg.IsPerformanceLeg() or leg.IsPerformanceRPLLeg() or leg.IsPerformanceUPLLeg() or leg.IsFinancingLeg() or leg.IsStockBorrowLeg())]
    for leg in legs:
        cashflows = CashflowsGreaterThanDate(leg, date).AsArray()
        for cashflow in cashflows:
            leg.CashFlows().Remove(cashflow)
            cashflow.Unsimulate()
#----------------------------------------------------------------------------
def ClearPortfolioSwapPaymentsPostDate(portfolioSwapTrade, fromDate):
    adjustCashPaymentType = GetAdjustCashPaymentType()
    for payment in portfolioSwapTrade.Payments()[:]:        
        if payment.Type() == adjustCashPaymentType and acm.Time.DateDifference(payment.PayDay(), fromDate) >= 0:
            portfolioSwapTrade.Payments().Remove(payment)
            payment.Unsimulate()
#----------------------------------------------------------------------------
def ClearPortfolioSwapPaymentsPreDate(portfolioSwapTrade, toDate):
    adjustCashPaymentType = GetAdjustCashPaymentType()
    for payment in portfolioSwapTrade.Payments()[:]:        
        if payment.Type() == adjustCashPaymentType and acm.Time.DateDifference(payment.PayDay(), toDate) <= 0:
            portfolioSwapTrade.Payments().Remove(payment)
            payment.Unsimulate()
#----------------------------------------------------------------------------
def ClearPortfolioSwapResets(portfolioSwap, date):
    for leg in portfolioSwap.Legs():
        for reset in leg.Resets()[:]:
            if acm.Time.DateDifference(reset.Day(), date) >= leg.ResetDayOffset():
                leg.Resets().Remove(reset)
                reset.Unsimulate()
#----------------------------------------------------------------------------
def UsePerPortfolioFunding():
    return "true" == acm.GetDefaultValueFromName(acm.GetDefaultContext(), "FPortfolioSwap", "usePerPortfolioFunding")
#----------------------------------------------------------------------------
def _AddNonNil(array, object):
    if object:
        array.append(object)
#----------------------------------------------------------------------------
def _GetPayCalendarInfo(leg):
    calendars = []
    _AddNonNil(calendars, leg.PayCalendar())
    _AddNonNil(calendars, leg.Pay2Calendar())
    _AddNonNil(calendars, leg.Pay3Calendar())
    _AddNonNil(calendars, leg.Pay4Calendar())
    _AddNonNil(calendars, leg.Pay5Calendar())
    return createCalendarInformation(calendars)
#----------------------------------------------------------------------------
def AdjustDateToOffsetMethod(date, leg, paydayOffsetPeriod, paydayOffsetMethod):
    calendarInfo = _GetPayCalendarInfo(leg)
    date = calendarInfo.Modify(acm.Time.PeriodSymbolToRebasedDate(paydayOffsetPeriod, date), paydayOffsetMethod)
    return date
#----------------------------------------------------------------------------
def AdjustBankingDays(leg, date, nbrDays):
    calendarInfo = _GetPayCalendarInfo(leg)
    return calendarInfo.AdjustBankingDays(date, nbrDays)
#----------------------------------------------------------------------------
def GetAdjustCashPaymentType():
    try:
        from PortfolioSwapDealPackageCustomization import GetAdjustCashPaymentType
        adjustCashPaymentType = GetAdjustCashPaymentType()
    except:
        adjustCashPaymentType = 'Cash'
    return adjustCashPaymentType
#----------------------------------------------------------------------------
def CalculateSyntheticCash(portfolioSwapTrade, toDate = acm.Time.DateToday()):
    synthCash = 0.0
    
    try:
        calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FMoneyFlowSheet')
        for moneyFlow in portfolioSwapTrade.MoneyFlows():
            if moneyFlow.Type() in["Fixed Amount", "Interest Reinvestment"]:
                if acm.Time.DateDifference(toDate, moneyFlow.PayDate()) >= 0:
                    if moneyFlow.SourceObject().IsKindOf(acm.FCashFlow):
                        if moneyFlow.SourceObject().Leg().IndexRef() == None:
                            synthCash = synthCash + calcSpace.CalculateValue(moneyFlow, 'Cash Analysis Projected').Number()
    except Exception, e:
        print "CalculateSyntheticCash, could not calculate synthetic cash for trade %s" % (portfolioSwapTrade.Oid())
        print e
        synthCash = 0.0
    return synthCash
#----------------------------------------------------------------------------
def AdjustCashDefaultDate(portfolioSwap):
    date = acm.Time().DateToday()
    legs = [leg for leg in portfolioSwap.Legs() if leg.IsSyntheticCashLeg()]
    syntheticCashLeg = 1 == len(legs) and legs[0] or None
    if syntheticCashLeg:
        date = syntheticCashLeg.EndDate()
    return date
#----------------------------------------------------------------------------
def GetPreviousCashFlow(cashFlow):
    """
    get the previous cashflow of the same type
    """
    previousCashFlow = None
    
    for cf in cashFlow.Leg().CashFlows():
        if cf != cashFlow  and cf.CashFlowType() == cashFlow.CashFlowType():
            if cf.PayDate() == cashFlow.StartDate():
                previousCashFlow = cf
                
    return previousCashFlow
#----------------------------------------------------------------------------
def GetReinvestmentCashFlow(syntheticCashLeg, payDate):
    for cashFlow in syntheticCashLeg.CashFlows():
        if cashFlow.CashFlowType() == "Interest Reinvestment" and cashFlow.PayDate() == payDate:
            return cashFlow
    return None
#----------------------------------------------------------------------------
def CalculateSyntheticInterest(cashFlow, trade):
    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()     
    value = cashFlow.Calculation().Projected(calcSpace, trade)
    return (-1.0) * value.Number()
#----------------------------------------------------------------------------
def AdjustCash(syntheticCashLeg, portfolioSwapTrade, amount, currency, date):
    qtyAdjustedAmount= amount * portfolioSwapTrade.Quantity()
    newCashFlow      = syntheticCashLeg.CreateCashFlow()
    newCashFlow.CashFlowType("Fixed Amount")
    newCashFlow.FixedAmount(-qtyAdjustedAmount)
    newCashFlow.FloatRateFactor(syntheticCashLeg.FloatRateFactor())
    newCashFlow.NominalFactor(syntheticCashLeg.NominalFactor())
    newCashFlow.PayDate(date)
    newCashFlow.FixedRate(syntheticCashLeg.FixedRate())

    paymentType        = GetAdjustCashPaymentType()
    newPayment         = portfolioSwapTrade.CreatePayment()
    newPayment.Amount(amount)
    newPayment.Currency(currency)
    newPayment.Type(paymentType)
    newPayment.PayDay(date)
    newPayment.ValidFrom(acm.Time().DateToday())
    newPayment.Party(portfolioSwapTrade.Counterparty())         
#----------------------------------------------------------------------------
def PortfolioHasIncomingDividendPayment(parameters, date):
    calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FPortfolioSheet)
    calcSpace.InsertItem(parameters.FilteredPortfolio())
    calcSpace.Refresh()
    portfolioIter = calcSpace.RowTreeIterator().FirstChild()
    securityIter = portfolioIter.FirstChild()
    while securityIter:
        item = securityIter.Tree().Item()
        security = item.Instrument() if item else None
        dividendLeg = parameters.GetDividendLeg(security)
        if dividendLeg:
            for cf in dividendLeg.CashFlows():
                if cf.StartDate() <= date and cf.PayDate() > date:
                    globalSimulations = [("Portfolio Profit Loss End Date", "Custom"), \
                            ("Portfolio Profit Loss End Date Custom", cf.StartDate())]
                    CalcUtil.ApplySimulations(calcSpace, globalSimulations, None)
                    calcSpace.Refresh()
                    colValue = calcSpace.CalculateValue(securityIter.Tree(), "Portfolio Profit Loss Period Position")
                    if colValue:
                        return True
        securityIter = securityIter.NextSibling()
    return False
#-----------------------------------------------------------------------------
def PortfolioHasOpenPosition(portfolio, terminateDate):
    globalSimulations = [("Portfolio Profit Loss End Date", "Custom"), \
                    ("Portfolio Profit Loss End Date Custom", terminateDate)]
    positions = CalcUtil.CalculatePerSecurityColumnValues(portfolio, ["Portfolio Profit Loss Period Position"], globalSimulations)
    
    for pos in positions:
        pos = pos[0]
        if pos:
            return True
    return False
#-----------------------------------------------------------------------------

def PayOutAllCash(parameters, fromDate, toDate):
        
    syntheticCashLeg = GetCallDepositLeg(parameters.PortfolioSwap())
    portfolioSwapTrade = parameters.DealPackage().TradeAt("PrfSwap")
    amount   = CalculateSyntheticCash(portfolioSwapTrade, toDate)
    if not acm.Math.AlmostZero(amount, 1.e-6) and acm.Math.IsFinite(amount):
        AdjustCash(syntheticCashLeg, portfolioSwapTrade, amount, parameters.DealPackage().GetAttribute('currency'), toDate)

#-----------------------------------------------------------------------------        
def getRightPsLegs(portSwap, indexRef, legType, nominalScaleType = None):
    query = acm.CreateFASQLQuery(acm.FLeg, 'AND')
    query.AddAttrNode('Instrument.Oid', 'EQUAL', portSwap.Oid())
    query.AddAttrNode('IndexRef.Oid', 'EQUAL', indexRef.Oid())
    query.AddAttrNode('LegType', 'EQUAL', legType)
    
    if nominalScaleType != None:
        query.AddAttrNode('NominalScaling', 'EQUAL', nominalScaleType)    
    return query.Select()
#-----------------------------------------------------------------------------        
def GetPortfolioSwap(fundPortfolio):
    return acm.FPortfolioSwap.Select01("fundPortfolio = %s" %fundPortfolio.Oid(), "More than one portfolio swap use %s as synthetic portfolio" %fundPortfolio.Name() )
