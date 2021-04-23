import acm
import FSyntheticPrimeUtil as Util
from DealPackageUtil import UnDecorate
reload(Util)
from FSyntheticPrimeUtil import AdjustDateToOffsetMethod  # override
#----------------------------------------------------------------------------
def CreateDailyExecutionFeeCashFlows(pfsParameters, startDate, valuationSystemDate, generate):
    _CreateExecutionFeeCashFlows(pfsParameters, startDate, _ExecutionFeeCashFlowsTodate(pfsParameters, valuationSystemDate, generate))

#----------------------------------------------------------------------------    
def _ExecutionFeeCashFlowsTodate(pfsParameters, valuationSystemDate, generate):
    tradesWithPayments = _ApplyFilter(pfsParameters.FilteredPortfolio().Trades())
    return _TradePaymentsDict(tradesWithPayments, pfsParameters.AccountingParameters(), None, valuationSystemDate, generate)
#----------------------------------------------------------------------------    
def ExecutionFeeCashFlowsPostdate(pfsParametersOrPortfolio, valuationDate, valuationSystemDate):
    if hasattr(pfsParametersOrPortfolio, 'Trades'):
        trades = pfsParametersOrPortfolio.Trades()
        accountingParameters = pfsParametersOrPortfolio.MappedAccountingParametersLink().Link()
    else:
        trades = pfsParametersOrPortfolio.FilteredPortfolio().Trades()
        accountingParameters = pfsParametersOrPortfolio.FundPortfolio().MappedAccountingParametersLink().Link()
    tradesWithPayments = _ApplyFilter(trades)
    return _TradePaymentsDict(tradesWithPayments, accountingParameters, valuationDate, valuationSystemDate, False)
#----------------------------------------------------------------------------    
def ExecutionFeeCashFlowsToday(pfsParametersOrPortfolio, valuationDate, valuationSystemDate, notUsed = None):
    perSecurityFees = ExecutionFeeCashFlowsPostdate(pfsParametersOrPortfolio, valuationDate, valuationSystemDate)
    returnDict = {}
    for ins in perSecurityFees.keys():
        paymentInfo = perSecurityFees[ins]
        for validFrom in paymentInfo.keys():
            if validFrom <= valuationDate: 
                dvBasket = paymentInfo[validFrom]
                returnDict[ins] = dvBasket
    return returnDict
#----------------------------------------------------------------------------        
def _ApplyFilter(trades):
    filteredSet = acm.FFilteredSet(trades)
    filter = acm.Filter.SimpleAndQuery(acm.FTrade, ['PaymentCount', 'Status'], ['GREATER', 'NOT_EQUAL'], [0, 'Void'])
    filteredSet.Filter(filter)
    return filteredSet
#----------------------------------------------------------------------------
def _TradePaymentsDict(tradesWithPayments, accountingParameters, valuationDate, valuationSystemDate, generate):
    
    perSecurityFees = {}
    
    def ApplyPaymentFilter(trade):                
        if generate:
            validFromOperator = 'LESS'
            payDayOperator = 'LESS_EQUAL'
            payDayCompareDate = valuationSystemDate
        else:
            validFromOperator = 'GREATER'
            payDayOperator = 'GREATER'
            payDayCompareDate = max(valuationDate, valuationSystemDate)
            
            
        filteredSetHistorical = acm.FFilteredSet(trade.Payments())
        filteredSetToday = acm.FFilteredSet(trade.Payments())
        
        
        validHistoricalPayments = acm.Filter.SimpleAndQuery(acm.FPayment, ['Currency',       'ValidFrom'], 
                                                                          ['EQUAL',           validFromOperator], 
                                                                          [trade.Currency(),  valuationSystemDate])
                                                                          
        
                                                         
        validPaymentsToday = acm.Filter.SimpleAndQuery(acm.FPayment, ['Currency',       'ValidFrom',           'PayDay'], 
                                                                     ['EQUAL',          'EQUAL',               payDayOperator], 
                                                                     [trade.Currency(),  valuationSystemDate,  payDayCompareDate])
                                                    
        filteredSetHistorical.Filter(validHistoricalPayments)
        filteredSetToday.Filter(validPaymentsToday)
        filteredSet = filteredSetHistorical.AddAll(filteredSetToday)
        return filteredSet
    
    def AddPaymentInfo(ins, validFrom, dv):
        if ins in perSecurityFees:
            paymentInfo = perSecurityFees[ins]
            if validFrom in paymentInfo:
                dvBasket = paymentInfo[validFrom]
                dvBasket.Add(dv)
            else:
                dvBasket = acm.FDenominatedBasket()
                dvBasket.Add(dv)
                paymentInfo[validFrom] = dvBasket
        else:
            paymentInfo = {}
            dvBasket = acm.FDenominatedBasket()
            dvBasket.Add(dv)
            paymentInfo[validFrom] = dvBasket
            perSecurityFees[ins] = paymentInfo
            
    for trade in tradesWithPayments:
        payments = ApplyPaymentFilter(trade)
        for payment in payments:
            if payment.IsAccountedForAsFee(accountingParameters):
                dv = acm.DenominatedValue(-payment.Amount(), payment.Currency(), payment.Type(), payment.PayDay())
                validFrom = payment.ValidFrom()
                ins = trade.Instrument()
                AddPaymentInfo(ins, validFrom, dv)
                
    return perSecurityFees
#----------------------------------------------------------------------------
def _DayOffsetToDatePeriod(dayOffset):
    return "%sd"%str(dayOffset)
#----------------------------------------------------------------------------        
def _CreateExecutionFeeCashFlows(pfsParameters, startDate, perSecurityFees):

    def ApplyPaymentInPortfolioSwapFilter(dvBasket):
        filteredSet = acm.FFilteredSet(dvBasket)
        filter = acm.Filter.SimpleAndQuery(acm.FDenominatedValue, ['DateTime'], ['GREATER_EQUAL'], [startDate])  # override
        filteredSet.Filter(filter)
        return filteredSet
        
    securities = perSecurityFees.keys()
    for security in securities:
        executionFeeLeg = pfsParameters.GetFeeLeg(security)
        paymentInfo = perSecurityFees[security]
        validFromDates = paymentInfo.keys()
        for validFrom in validFromDates:
            payments = paymentInfo[validFrom]
            paymentsAsFilteredSet = ApplyPaymentInPortfolioSwapFilter(payments)
            spotBankingDaysOffset = _DayOffsetToDatePeriod( pfsParameters.PortfolioSwap().SpotBankingDaysOffset() )
            _CreateExecutionFeeCashFlow(executionFeeLeg, paymentsAsFilteredSet, spotBankingDaysOffset, validFrom)
#----------------------------------------------------------------------------
def _CreateExecutionFeeCashFlow(executionFeeLeg, \
                                paymentsAsDVbasket, \
                                spotBankingDaysOffset,
                                validFrom):
                                
    def GetFixedAmountPayDate(leg, dv):
        cashFlowValidFromDate = acm.Time.AsDate(dv.DateTime())
        return cashFlowValidFromDate if acm.Time().DateDifference(cashFlowValidFromDate, str(leg.StartDate())) >= 0 else None
 
    
    def ExecutionFeeCashFlow(executionFeeLeg, validFrom, payDate):
        filteredSet = acm.FFilteredSet(executionFeeLeg.CashFlows())
        filter = acm.Filter.SimpleAndQuery(acm.FCashFlow, ['StartDate', 'PayDate'], ['Equal', 'Equal'], [validFrom, payDate])
        filteredSet.Filter(filter)
        return None if not filteredSet.Size() else filteredSet.AsIndexedCollection().At(0)
    
    if executionFeeLeg:
        for dv in paymentsAsDVbasket:
            payDate = GetFixedAmountPayDate(executionFeeLeg, dv)
            cashFlow = ExecutionFeeCashFlow(executionFeeLeg, validFrom, payDate)
            if not cashFlow:
                _CreatePortfolioSwapCashFlow(executionFeeLeg, \
                                         dv.Value().Number(), \
                                         "Fixed Amount", \
                                         spotBankingDaysOffset, \
                                         validFrom, \
                                         validFrom, \
                                         payDate)
        
            
            
#----------------------------------------------------------------------------
def CreateRedemptionCashFlow(depositLeg):
    if not Util.GetRedemptionCashFlowFromLeg(depositLeg, False):
        cashFlow = _CreatePortfolioSwapCashFlow(depositLeg, \
                                                        0.0, \
                                                        "Redemption Amount", \
                                                        None, \
                                                        depositLeg.StartDate(), \
                                                        depositLeg.StartDate(), \
                                                        depositLeg.StartDate())
#----------------------------------------------------------------------------
def _CreatePortfolioSwapCashFlow(leg, \
                                fixedAmount, \
                                type, \
                                paydayOffsetPeriod, \
                                startDay, \
                                endDay, \
                                payDay):

    if not payDay:
        if not endDay:
            raise Exception("No end date when creating cashflow.")
        payDay = AdjustDateToOffsetMethod(endDay, leg, paydayOffsetPeriod, leg.PayDayMethod())
        
    cashFlow = leg.CreateCashFlow()
    cashFlow.StartDate = startDay
    cashFlow.EndDate = endDay
    cashFlow.PayDate = payDay
    cashFlow.NominalFactor = leg.NominalFactor()
    cashFlow.FixedAmount = fixedAmount
    cashFlow.CashFlowType = type
    cashFlow.FloatRateFactor = leg.FloatRateFactor()
    cashFlow.FixedRate = leg.FixedRate()
    if cashFlow.GenerateResets(True, 0.0, True, payDay).Size():
        cashFlow.RegisterInStorage()
    return cashFlow
#----------------------------------------------------------------------------
def SweepCash(pfsParameters, date):

    def CalculateProjectedValue(leg, date, trade):
        calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        aggValue = 0
        for cashFlow in leg.CashFlows():
            if cashFlow.PayDate() == date:   
                value = cashFlow.Calculation().Projected(calcSpace, trade)
                if value != 0 and acm.Math.IsFinite(value):
                    aggValue -= value.Number()
        return aggValue
    
    def IsAdjustCashCashFlow(cashFlow):
        adjustCashPaymentType = Util.GetAdjustCashPaymentType()
        for payment in pfsParameters.DealPackage().TradeAt("PrfSwap").Payments():
            if payment.Type() == Util.GetAdjustCashPaymentType() and payment.PayDay() == cashFlow.PayDate() and payment.Amount() == -cashFlow.FixedAmount():
                return True
        return False
    
    def CreateOrUpdate(aggValue):
        #Fetch synthetic cash leg
        syntheticLeg = Util.GetCallDepositLeg(pfsParameters.PortfolioSwap())
        
        # Our aggregated cashflow
        newAggCashFlow = None
        
        # There might exist one on the same date, if so we update that one.
        updateCashFlows = acm.FCashFlow.Select('leg = ' + str(syntheticLeg.Oid()) + ' payDate = "' + date + '" \
                                                cashFlowType = "Fixed Amount"' )
        
        updateCashFlow = [cf for cf in updateCashFlows if not IsAdjustCashCashFlow(cf)]
        if len(updateCashFlow) == 1:
            newAggCashFlow = updateCashFlow[0]
            newAggCashFlow.FixedAmount(aggValue)
        else:
            newAggCashFlow = _CreatePortfolioSwapCashFlow(syntheticLeg, \
                                                          aggValue, \
                                                          'Fixed Amount', \
                                                          0, \
                                                          None, \
                                                          None, \
                                                          date)
        
    
    portfolioSwap = pfsParameters.PortfolioSwap()    
    trade = UnDecorate(pfsParameters.DealPackage().TradeAt("PrfSwap").Clone())
    trade.Quantity(1) #We want to be long
    
    aggValue = 0
    for leg in portfolioSwap.Legs():
        if not leg.IsSyntheticCashLeg():
            aggValue += CalculateProjectedValue(leg, date, trade)
            
    if acm.Math.IsFinite(aggValue) and not acm.Math.AlmostZero(aggValue, 1.e-6):
        CreateOrUpdate(aggValue)
#----------------------------------------------------------------------------  
def CreateInterestReinvestmentCashFlow(syntheticCashLeg, cashFlow, interest):
    if not acm.Math.AlmostZero(interest, 1.e-6) and acm.Math.IsFinite(interest):
        reinvestmentCashFlow = Util.GetReinvestmentCashFlow(syntheticCashLeg, cashFlow.PayDate())
        if not reinvestmentCashFlow:
            reinvestmentCashFlow = syntheticCashLeg.CreateCashFlow()
            
        reinvestmentCashFlow.CashFlowType("Interest Reinvestment")
        reinvestmentCashFlow.FixedAmount(-interest)
        reinvestmentCashFlow.FloatRateFactor(syntheticCashLeg.FloatRateFactor())
        reinvestmentCashFlow.NominalFactor(1.0)
        reinvestmentCashFlow.StartDate(0)
        reinvestmentCashFlow.EndDate(0)
        reinvestmentCashFlow.PayDate(cashFlow.PayDate())
        reinvestmentCashFlow.Manually(0)
#----------------------------------------------------------------------------
def CreatePeriodicalPayout(pfsParameters, date):
    syntheticCashLeg = pfsParameters.GetSyntheticCashLeg()
    if syntheticCashLeg and syntheticCashLeg.RollingPeriod()[0]!="0":
        nextBusinessDay = date
        today = Util.AdjustBankingDays(syntheticCashLeg, nextBusinessDay, -1)
        for cashFlow in syntheticCashLeg.CashFlows():
            if cashFlow.CashFlowType() == "Call Float Rate":
                if cashFlow.StartDate() == today and cashFlow.PayDate() == nextBusinessDay:
                    previousCashFlow = Util.GetPreviousCashFlow(cashFlow)
                    if previousCashFlow:
                        interest = Util.CalculateSyntheticInterest(previousCashFlow, pfsParameters.DealPackage().TradeAt("PrfSwap"))
                        CreateInterestReinvestmentCashFlow(syntheticCashLeg, previousCashFlow, interest)
                        Util.PayOutAllCash(pfsParameters, pfsParameters.DealPackage().GetAttribute('startDate'), previousCashFlow.PayDate())
                    break
#----------------------------------------------------------------------------    
def CreatePeriodicalPayouts(pfsParameters, toDate):
    syntheticCashLeg = pfsParameters.GetSyntheticCashLeg()
    portfolioSwapTrade = pfsParameters.DealPackage().TradeAt("PrfSwap")
    for cashFlow in syntheticCashLeg.CashFlows():
        if cashFlow.CashFlowType() == "Call Float Rate":
            if acm.Time().DateDifference(toDate, cashFlow.PayDate()) > 0:
                interest = Util.CalculateSyntheticInterest(cashFlow, portfolioSwapTrade)
                CreateInterestReinvestmentCashFlow(syntheticCashLeg, cashFlow, interest)
                Util.PayOutAllCash(pfsParameters, pfsParameters.DealPackage().GetAttribute('startDate'), cashFlow.PayDate())
#----------------------------------------------------------------------------    
