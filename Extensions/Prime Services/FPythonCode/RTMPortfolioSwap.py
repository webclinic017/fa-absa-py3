""" Compiled: 2013-11-07 14:33:49 """

"""----------------------------------------------------------------------------
MODULE

    RTMPortfolioSwap

    (c) Copyright 2009 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    Functions that handle leg-, cash flow- and reset-generation for portfolio
    swaps.

----------------------------------------------------------------------------"""
import ael
import acm
import time
import RTMPortfolioSwapConfig as Conf
reload(Conf)
import RTMPortfolioSwapUtil as Util
reload(Util)
if None != Conf.customValuationModuleName:
    Custom = Util.ImportModuleByName(Conf.customValuationModuleName)
else:
    Custom = None
if Custom:
    reload(Custom)

# "Portfolio Accumulated Cash" Calculation incorrectly returns NaN
workAroundCAPIBug = True

#----------------------------------------------------------------------------
ID_PER_PORTFOLIO_FUNDING_AMOUNT = "ID_PER_PORTFOLIO_FUNDING_AMOUNT"
ID_PER_PORTFOLIO_FUNDING_RATE = "ID_PER_PORTFOLIO_FUNDING_RATE"
ID_PER_PORTFOLIO_EXECUTION_FEE = "ID_PER_PORTFOLIO_EXECUTION_FEE"
ID_PER_PORTFOLIO_RPL = "ID_PER_PORTFOLIO_RPL"
ID_PER_PORTFOLIO_PAYMENTS = "ID_PER_PORTFOLIO_PAYMENTS"
ID_PER_SECURITY_POSITION = "ID_PER_SECURITY_POSITION"
ID_PER_SECURITY_INV_POSITION = "ID_PER_SECURITY_INV_POSITION"
ID_PER_SECURITY_RETURN_FIXING = "ID_PER_SECURITY_RETURN_FIXING"
ID_PER_SECURITY_FUNDING_RATE = "ID_PER_SECURITY_FUNDING_RATE"
ID_PER_SECURITY_FUNDING_AMOUNT = "ID_PER_SECURITY_FUNDING_AMOUNT"
ID_PER_SECURITY_EXECUTION_FEE = "ID_PER_SECURITY_EXECUTION_FEE"
ID_PER_SECURITY_REPO_AMOUNT = "ID_PER_SECURITY_REPO_AMOUNT"
ID_PER_SECURITY_REPO_FINANCING_RATE = "ID_PER_SECURITY_REPO_FINANCING_RATE"
ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT = "ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT"
ID_PORTFOLIO_SWAP_DAILY_CASH = "ID_PORTFOLIO_SWAP_DAILY_CASH"
#----------------------------------------------------------------------------
# Standard columns
#----------------------------------------------------------------------------
colIdPnLStartDate = "Portfolio Profit Loss Start Date"
colIdPnLStartDateCustom = "Portfolio Profit Loss Start Date Custom"
colIdPnLEndDate = "Portfolio Profit Loss End Date"
colIdPnLEndDateCustom = "Portfolio Profit Loss End Date Custom"
#----------------------------------------------------------------------------
def PerformDailyUpdatesInPeriod(pfsParameters, resetStartDate, resetEndDate):

    fixingDate = resetStartDate
    while fixingDate and acm.Time.DateDifference(fixingDate, resetEndDate) <= 0:
        adjustToPeriodEndDay = IsBankingDayBeforePeriodEndDay(pfsParameters, fixingDate)
        isRollingDay = IsRollingDay(pfsParameters, fixingDate)
        isOpenEnd = "Open End" == pfsParameters.portfolioSwap.OpenEnd()
        if isOpenEnd:
            if isRollingDay:
                PortfolioSwapExtendOpenEnd(pfsParameters, fixingDate, adjustToPeriodEndDay, True)
                RollPortfolioSwap(pfsParameters, fixingDate)
            else:
                PortfolioSwapExtendOpenEnd(pfsParameters, fixingDate, False, False)

        acm.PollDbEvents() # Let the end return resets update

        if UseDividendLegs(pfsParameters):
            UpdateDividendLegs(pfsParameters, UsePerPortfolioFunding(pfsParameters))

        # The redemption cash flow must be prolonged before calculating the call deposit cash
        # to get the correct net amount
        if UseCallDepositLeg(pfsParameters):
            SetCallAccountEndDate(pfsParameters.portfolioSwap, 
                                    pfsParameters.calendar.AdjustBankingDays(fixingDate, 1))

        PerformDailyFixing(pfsParameters, fixingDate)

        if not acm.Time.DateDifference(fixingDate, pfsParameters.portfolioSwap.ExpiryDate()) or \
                isRollingDay:
            FixEndTotalReturnResets(pfsParameters, fixingDate, adjustToPeriodEndDay)

        ael.poll() # Needed to get correct resets

        fixingDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, 1)
        fixingDate = acm.Time.DateDifference(fixingDate, resetEndDate) <= 0 and fixingDate or None

#----------------------------------------------------------------------------
def IsPeriodEndDay(pfsParameters, date):
    return Util.IsPeriodEndDay(pfsParameters.portfolioSwap, \
                            pfsParameters.rollingBaseDay, \
                            pfsParameters.isFixPeriod, \
                            date, \
                            pfsParameters.calendar, \
                            False)
#----------------------------------------------------------------------------
def IsOpenEndRollingPeriodEndDay(pfsParameters, date):
    return "Open End" == pfsParameters.portfolioSwap.OpenEnd() and \
        IsPeriodEndDay(pfsParameters, date) and \
        acm.Time.DateDifference(pfsParameters.portfolioSwap.StartDate(), date)
#----------------------------------------------------------------------------
def IsRollingDay(pfsParameters, fixingDate):
    result = False
    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        isPeriodEndDay = IsPeriodEndDay(pfsParameters, fixingDate)
        if isPeriodEndDay and acm.Time.DateDifference(fixingDate, pfsParameters.portfolioSwap.StartDate()):
            result = True
        elif IsBankingDayBeforePeriodEndDay(pfsParameters, fixingDate):
            result = True
    return result
#----------------------------------------------------------------------------
def IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, fixingDate):
    return "Open End" == pfsParameters.portfolioSwap.OpenEnd() and \
        pfsParameters.isFixPeriod and \
        IsBankingDayBeforePeriodEndDay(pfsParameters, fixingDate)
#----------------------------------------------------------------------------
def PeriodCashFlowStartDay(pfsParameters, date, closedPeriod, isAel, aelPortfolioSwap = None):
    if "Open End" != pfsParameters.portfolioSwap.OpenEnd() and \
            not acm.Time.DateDifference(pfsParameters.portfolioSwap.ExpiryDate(), date):
        periodStartDay = pfsParameters.portfolioSwap.StartDate()
    elif closedPeriod:
        periodStartDay = Util.PeriodStartDayClosed(isAel and aelPortfolioSwap or pfsParameters.portfolioSwap, \
                                                    pfsParameters.rollingBaseDay, \
                                                    pfsParameters.isFixPeriod, \
                                                    date, \
                                                    pfsParameters.calendar, \
                                                    isAel)
    else:
        periodStartDay = Util.PeriodStartDay(isAel and aelPortfolioSwap or pfsParameters.portfolioSwap, \
                                            pfsParameters.rollingBaseDay, \
                                            pfsParameters.isFixPeriod, \
                                            date, \
                                            pfsParameters.calendar, \
                                            isAel)

    if not pfsParameters.isFixPeriod:
        periodStartDay = Util.AdjustDateToOffsetMethod(periodStartDay, \
                                                        pfsParameters.calendar, \
                                                        '0d', \
                                                        pfsParameters.paydayOffsetMethod)

    return periodStartDay
#----------------------------------------------------------------------------
def IsBankingDayBeforePeriodEndDay(pfsParameters, fixingDate):
    return Util.IsBankingDayBeforePeriodEndDay(pfsParameters.portfolioSwap, \
                                                pfsParameters.rollingBaseDay, \
                                                pfsParameters.isFixPeriod, \
                                                fixingDate, \
                                                pfsParameters.calendar, \
                                                False)
#----------------------------------------------------------------------------
def IsBankingDayAfterPeriodEndDay(pfsParameters, fixingDate):
    return Util.IsBankingDayAfterPeriodEndDay(pfsParameters.portfolioSwap, \
                                            pfsParameters.rollingBaseDay, \
                                            pfsParameters.isFixPeriod, \
                                            fixingDate, \
                                            pfsParameters.calendar, \
                                            False)
#----------------------------------------------------------------------------
def PeriodCashFlowEndDay(pfsParameters, date, isAel):
    periodEndDay = Util.PeriodEndDay(pfsParameters.portfolioSwap, \
                                pfsParameters.rollingBaseDay, \
                                pfsParameters.isFixPeriod, \
                                date, \
                                pfsParameters.calendar, \
                                isAel)
    if not pfsParameters.isFixPeriod:
        periodEndDay = Util.AdjustDateToOffsetMethod(periodEndDay, \
                                                    pfsParameters.calendar, \
                                                    '0d', \
                                                    pfsParameters.paydayOffsetMethod)
    return periodEndDay
#----------------------------------------------------------------------------
def GetCashFlowPeriods(pfsParameters, startDate, endDate):
    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        periodStartDate = PeriodCashFlowStartDay(pfsParameters, startDate, True, False)
        periodEndDate = periodStartDate

        while acm.Time.DateDifference(endDate, periodEndDate) >= 0:
            periodEndDate = PeriodCashFlowEndDay(pfsParameters, \
                                                acm.Time.DateAddDelta(periodEndDate, 0, 0, 1), \
                                                False)
            yield (periodStartDate, periodEndDate)
            periodStartDate = periodEndDate
        return
    else:
        periodStartDate = pfsParameters.portfolioSwap.StartDate()
        periodEndDate = pfsParameters.portfolioSwap.ExpiryDate()
        yield (periodStartDate, periodEndDate)
    return
#----------------------------------------------------------------------------
def RestorePortfolioSwapEndDate(pfsParameters, resetEndDate):
    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        endDate = PeriodCashFlowEndDay(pfsParameters, acm.Time.DateAddDelta(resetEndDate, 0, 0, 1), False)
        pfsParameters.portfolioSwap.ExpiryDate = endDate
        pfsParameters.portfolioSwap.Commit()
        UpdatePortfolioSwapLegsEndDates(pfsParameters, endDate)
#----------------------------------------------------------------------------
# Add legs and cash flows to represent any new positions in the portfolio.
#----------------------------------------------------------------------------
def AddNewLegs(pfsParameters, \
                resetStartDate, \
                resetEndDate):

    GeneratePerSecurityLegs(pfsParameters, \
                            resetStartDate, \
                            resetEndDate, \
                            not UsePerPortfolioFunding(pfsParameters), \
                            not UsePerPortfolioExecutionFee(pfsParameters), \
                            UsePerSecurityRepo(pfsParameters), \
                            UseDividendLegs(pfsParameters))
#----------------------------------------------------------------------------
def AddNewCashFlows(pfsParameters, \
                    resetStartDate, \
                    resetEndDate):
    # If the current day is a rolling day, new cash flows will be generated by the rolling procedure.
    if not IsRollingDay(pfsParameters, resetStartDate) or \
            (IsRollingDay(pfsParameters, resetStartDate) and \
                IsBankingDayBeforePeriodEndDay(pfsParameters, resetStartDate)):
                
        (legStartDate, legEndDate) = GetLegStartAndEndDate(pfsParameters, \
                                                            resetStartDate, \
                                                            resetEndDate)

        if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
            cashFlowEndDate = resetEndDate
        else:
            cashFlowEndDate = legEndDate

        legsWithoutCashFlows = Util.GetLegsPerSecurityWithoutCashFlows(pfsParameters.portfolioSwap, \
                                                                        pfsParameters.returnLegIsPayLeg, \
                                                                        legStartDate, \
                                                                        ReturnCashFlowType(pfsParameters))

        perSecurityCashFlows = GeneratePerSecurityCashFlows(pfsParameters, \
                                                            legsWithoutCashFlows, \
                                                            legStartDate, \
                                                            cashFlowEndDate, \
                                                            "Open End" == pfsParameters.portfolioSwap.OpenEnd())

        acm.PollDbEvents() # In order for the automatically created resets to show up in ACM
        ClearPerSecurityCashFlowsResets(perSecurityCashFlows, pfsParameters)
#----------------------------------------------------------------------------
def TransferPreviousPortfolioSwapData(pfsParameters, startDate):
    portfolioSwap = pfsParameters.portfolioSwap
    previousPfSwap = pfsParameters.previousPfSwap

    # Get the daily cash (the call account net of the previous portfolio swap and add
    # it to the account of the current swap.
    if UseCallDepositLeg(pfsParameters):
        previousPfSwapData = CalculatePortfolioSwapFixingData(previousPfSwap, pfsParameters, startDate, True)
        startDayCash = -1.0 * Util.GetValueConditionally(previousPfSwapData, \
                                                ID_PORTFOLIO_SWAP_DAILY_CASH, \
                                                True)

        if startDayCash:
            Util.CreatePortfolioSwapCashFlow(Util.GetCallDepositLeg(portfolioSwap, False), \
                                                startDayCash, \
                                                "Fixed Amount", \
                                                None, \
                                                None, \
                                                None, \
                                                None, \
                                                None, \
                                                startDate, \
                                                False, \
                                                False)
#----------------------------------------------------------------------------
def TerminatePortfolioSwap(pfsParameters):
    lastResetDate = Util.GetLastResetDate(pfsParameters.portfolioSwap)
    portfolioSwap = pfsParameters.portfolioSwap
    calendar = pfsParameters.calendar
    
    if "Open End" == portfolioSwap.OpenEnd():
        terminationDate = lastResetDate
    else:
        terminationDate = Util.GetLastResetDate(portfolioSwap, True)
    
    FixEndTotalReturnResets(pfsParameters, lastResetDate, False)
    if UseCallDepositLeg(pfsParameters):
        CloseCallDeposit(pfsParameters, terminationDate)
    
    portfolioSwap.ExpiryDate(terminationDate)
    for leg in portfolioSwap.Legs():
        leg.EndDate(terminationDate)
    portfolioSwap.OpenEnd("Terminated")
    portfolioSwap.Commit()
#----------------------------------------------------------------------------
# On termination - Close out all accumulated cash in the call deposit leg.
# First the Total Cash of the portfolio swap is calculated and added to the account to 
# close out the account. This amount will hold both cash already on the account but
# also the new cash paid on the termination day.
# Secondly calculate the daily cash of the last day and add it to the account to get
# a net balance of zero on the account.
#----------------------------------------------------------------------------
def CloseCallDeposit(pfsParameters, terminationDate):

    portfolioSwap = pfsParameters.portfolioSwap
    SetCallAccountEndDate(portfolioSwap, pfsParameters.calendar.AdjustBankingDays(terminationDate, 1))

    callDepositLeg = Util.GetCallDepositLeg(portfolioSwap, False)
    portfolioSwapData = CalculatePortfolioSwapFixingData(portfolioSwap, \
                                                        pfsParameters, \
                                                        terminationDate)
    portfolioSwapDepositAmount = Util.GetValueConditionally(portfolioSwapData, \
                                            ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT, \
                                            True)

    if portfolioSwapDepositAmount:
        Util.CreatePortfolioSwapCashFlow(callDepositLeg, \
                                        portfolioSwapDepositAmount, \
                                        "Fixed Amount", \
                                        None, \
                                        None, \
                                        None, \
                                        terminationDate, \
                                        terminationDate, \
                                        terminationDate, \
                                        False, \
                                        False)

    SetCallAccountEndDate(portfolioSwap, terminationDate)
    portfolioSwapData = CalculatePortfolioSwapFixingData(portfolioSwap, \
                                                        pfsParameters, \
                                                        terminationDate, \
                                                        True)    

    lastDayCash = Util.GetValueConditionally(portfolioSwapData, \
                                            ID_PORTFOLIO_SWAP_DAILY_CASH, \
                                            True)

    if lastDayCash:
        Util.CreatePortfolioSwapCashFlow(callDepositLeg, \
                                        lastDayCash, \
                                        "Fixed Amount", \
                                        None, \
                                        None, \
                                        None, \
                                        terminationDate, \
                                        terminationDate, \
                                        terminationDate, \
                                        False, \
                                        False)
#----------------------------------------------------------------------------
def RollPortfolioSwap(pfsParameters, fixingDate):
    periodEndDate = PeriodCashFlowEndDay(pfsParameters, \
                                        pfsParameters.calendar.AdjustBankingDays(fixingDate, 1), \
                                        False)

    pfsParameters.portfolioSwap.ExpiryDate = periodEndDate
    pfsParameters.portfolioSwap.Commit()

    UpdatePortfolioSwapLegsEndDates(pfsParameters, periodEndDate)

    cashFlowStartDay = PeriodCashFlowEndDay(pfsParameters, fixingDate, False)
    
    legsPerSecurityInPortfolio = Util.GetLegsPerSecurityInPortfolio( \
                                                        pfsParameters.portfolioSwap.FundPortfolio(), \
                                                        pfsParameters.portfolioSwap, \
                                                        fixingDate, \
                                                        periodEndDate, \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        NonZeroColumnsIds(pfsParameters), \
                                                        False)
    
    perSecurityCashFlows = GeneratePerSecurityCashFlows(pfsParameters, \
                                                        legsPerSecurityInPortfolio, \
                                                        cashFlowStartDay, \
                                                        pfsParameters.portfolioSwap.ExpiryDate(), \
                                                        True, \
                                                        False)
    
    acm.PollDbEvents() # In order to find the new cash flows
    ClearPerSecurityCashFlowsResets(perSecurityCashFlows, pfsParameters)

    GenerateInitialResets(perSecurityCashFlows, \
                            pfsParameters, \
                            pfsParameters.calendar.AdjustBankingDays(fixingDate, 1))
    
    GeneratePerPortfolioSwapCashFlows(pfsParameters, \
                                        cashFlowStartDay, \
                                        UsePerPortfolioFunding(pfsParameters), \
                                        UsePerPortfolioRepo(pfsParameters), \
                                        UseCallDepositLeg(pfsParameters))

    acm.PollDbEvents() # In order to find the new cash flows
    ClearPerPortfolioSwapCashFlowsResets(pfsParameters, \
                                        cashFlowStartDay, \
                                        UsePerPortfolioFunding(pfsParameters), \
                                        UsePerPortfolioRepo(pfsParameters))
#----------------------------------------------------------------------------
def UpdatePortfolioSwapLegsEndDates(pfsParameters, newLegEndDate):

    indexRefToLegsDict = Util.GetIndexRefToLegsDictionary(pfsParameters.portfolioSwap, \
                                                            pfsParameters.returnLegIsPayLeg, \
                                                            False)
    UpdatePerSecurityLegsEndDates(indexRefToLegsDict.values(), \
                            pfsParameters, \
                            newLegEndDate)
    UpdatePerPortfolioSwapLegsEndDates(pfsParameters.portfolioSwap, \
                            pfsParameters.returnLegIsPayLeg, \
                            newLegEndDate, \
                            UsePerPortfolioFunding(pfsParameters), \
                            UsePerPortfolioRepo(pfsParameters), \
                            UseCallDepositLeg(pfsParameters), \
                            UseMarginLeg(pfsParameters))
#----------------------------------------------------------------------------
def UpdatePerSecurityLegsEndDates(perSecurityLegs, pfsParameters, newLegEndDate):
    legsFlattened = [leg for leg in Util.IterFlattenRemoveNone(perSecurityLegs)]
    batchIndexArray = Util.GetBatchIndices(len(legsFlattened), \
                                        GetConfigParameter("legBatchSize", pfsParameters.paramDict))
    for batchIndex in batchIndexArray:
        UpdateLegsEndDatesBatch(batchIndex, legsFlattened, newLegEndDate)
#----------------------------------------------------------------------------
def UpdatePerPortfolioSwapLegsEndDates(portfolioSwap, \
                            returnLegIsPayLeg, \
                            newLegEndDate, \
                            rollFundingLeg, \
                            rollRepoLeg, \
                            rollDepositLeg, \
                            rollMarginLeg):
    perPortfolioSwapLegs = []
    if rollFundingLeg:
        perPortfolioSwapLegs.append(Util.GetSingleFinancingLeg(portfolioSwap, \
                                                                returnLegIsPayLeg, \
                                                                False))
    if rollRepoLeg:
        perPortfolioSwapLegs.append(Util.GetSingleRepoLeg(portfolioSwap, \
                                                            returnLegIsPayLeg, \
                                                            False))
    if rollDepositLeg:
        perPortfolioSwapLegs.append(Util.GetCallDepositLeg(portfolioSwap, False))
        
    if rollMarginLeg:
        perPortfolioSwapLegs.append(Util.GetSingleMarginLeg(portfolioSwap, \
                                                            returnLegIsPayLeg, \
                                                            False))
                                                            
    UpdateLegsEndDatesBatch(range(len(perPortfolioSwapLegs)), perPortfolioSwapLegs, newLegEndDate)
#----------------------------------------------------------------------------
def UpdateLegsEndDatesBatch(batchIndex, legs, newEndDay):
    startTime = time.time()
    acm.LogAll("Updating legs batch end dates (batch size: %s)..."%len(batchIndex))
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            legs[index].EndDate = newEndDay
        acm.CommitTransaction()
    except Exception, e:
        acm.AbortTransaction()
        errMess = "Failed to update legs batch end dates: %s - Exits"%str(e)
        acm.Log(errMess)
        raise Exception(errMess)
    acm.LogAll("... Legs batch updated in %s seconds."%(str(time.time()-startTime)))
#----------------------------------------------------------------------------
# Update cash flow end- and pay-dates in case the Portfolio Swap is open
# ended.
#----------------------------------------------------------------------------
def PortfolioSwapExtendOpenEnd(pfsParameters, fixingDate, adjustToPeriodEndDay, isRollingDay):

    if isRollingDay:
        cashFlowEndDate = PeriodCashFlowEndDay(pfsParameters, fixingDate, False)
    else:
        cashFlowEndDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, 1)

    cashFlowPayDate = Util.AdjustDateToOffsetMethod(cashFlowEndDate, \
                                                    pfsParameters.calendar, \
                                                    pfsParameters.paydayOffset, \
                                                    pfsParameters.paydayOffsetMethod)
    
    aelPortfolioSwap = ael.Instrument[pfsParameters.portfolioSwap.Oid()]
    
    periodStartDay = PeriodCashFlowStartDay(pfsParameters, fixingDate, False, True, aelPortfolioSwap)
    aelLegsAndCashFlowsClones = Util.GetAelBaseLegsAndCashFlowsClonesPerSecurity( \
                                                    aelPortfolioSwap, \
                                                    UsePerPortfolioFunding(pfsParameters), \
                                                    ReturnCashFlowType(pfsParameters), \
                                                    pfsParameters.returnLegIsPayLeg, \
                                                    periodStartDay)

    UpdatePerSecurityCashFlowsOpenEnd(aelPortfolioSwap, \
                                        aelLegsAndCashFlowsClones, \
                                        cashFlowEndDate, \
                                        cashFlowPayDate, \
                                        pfsParameters)
                                        
    UpdatePerPortfolioSwapCashFlowsOpenEnd(pfsParameters, fixingDate, cashFlowEndDate, cashFlowPayDate)

    aelReturnCashFlowClones = [Util.ReturnCashFlowFromList(legsAndCashFlows[1]) \
                                    for legsAndCashFlows in aelLegsAndCashFlowsClones]

    if len(aelReturnCashFlowClones) and (not isRollingDay or (isRollingDay and adjustToPeriodEndDay)):
        AdjustEndReturnResetsOpenEnd(aelReturnCashFlowClones, \
                                    fixingDate, \
                                    pfsParameters, \
                                    adjustToPeriodEndDay, \
                                    PeriodCashFlowEndDay(pfsParameters, fixingDate, False))
#----------------------------------------------------------------------------
def UpdatePerSecurityCashFlowsOpenEnd(aelPortfolioSwap, \
                                        aelLegsAndCashFlowsClones, \
                                        cashFlowEndDate, \
                                        cashFlowPayDate, \
                                        pfsParameters):

    batchIndexArray = Util.GetBatchIndices(len(aelLegsAndCashFlowsClones), \
                                        GetConfigParameter("legBatchSize", pfsParameters.paramDict)/3)
    for batchIndex in batchIndexArray:
        UpdatePerSecurityCashFlowsOpenEndBatch(aelPortfolioSwap, \
                                                aelLegsAndCashFlowsClones, \
                                                cashFlowEndDate, \
                                                cashFlowPayDate, \
                                                batchIndex)
#----------------------------------------------------------------------------
def UpdatePerSecurityCashFlowsOpenEndBatch(aelPortfolioSwap, \
                                            aelLegsAndCashFlowsClones, \
                                            cashFlowEndDate, \
                                            cashFlowPayDate, \
                                            batchIndex):
    startTime = time.time()
    acm.LogAll("Updating cash flow batch open end (batch size: %s)..."%str(len(batchIndex)))
    try:
        ael.begin_transaction()
        aelEndDay = ael.date(cashFlowEndDate)
        aelPayDay = ael.date(cashFlowPayDate)
        
        for index in batchIndex:
            (securityLegClones, securityCFClones) = aelLegsAndCashFlowsClones[index]
            for (legClone, CFClone) in zip(securityLegClones, securityCFClones):
                if CFClone:
                    CFClone.end_day = aelEndDay
                    CFClone.pay_day = aelPayDay
                    legClone.commit()
        ael.commit_transaction()
    except Exception, e:
        acm.LogAll("Could not update end return resets.")
        ael.abort_transaction()
        raise e
    acm.LogAll("... Cash flow batch open end update finished in %s seconds."%(str(time.time()-startTime)))
#----------------------------------------------------------------------------
def UpdatePerPortfolioSwapCashFlowsOpenEnd(pfsParameters, fixingDate, cashFlowEndDate, cashFlowPayDate):

    aelPortfolioSwap = ael.Instrument[pfsParameters.portfolioSwap.Oid()]
    
    periodStartDate = PeriodCashFlowStartDay(pfsParameters, fixingDate, False, True, aelPortfolioSwap)
    aelPerPortfolioLegs = Util.GetPerPortfolioSwapLegs(aelPortfolioSwap, \
                                                    pfsParameters.returnLegIsPayLeg, \
                                                    UsePerPortfolioFunding(pfsParameters), \
                                                    UsePerPortfolioRepo(pfsParameters), \
                                                    UseCallDepositLeg(pfsParameters))
    
    if UsePerPortfolioFunding(pfsParameters):
        aelFinancingLeg = Util.FinancingLegFromList(aelPerPortfolioLegs)
        aelFinancingLegClone = aelFinancingLeg.clone()
        aelFinancingCF = Util.GetSingleFinancingCashFlowFromLeg(aelFinancingLegClone, periodStartDate)
        aelFinancingCF.end_day = ael.date(cashFlowEndDate)
        aelFinancingCF.pay_day = ael.date(cashFlowPayDate)
        aelFinancingLegClone.commit()
        
    if UsePerPortfolioRepo(pfsParameters):
        aelRepoLeg = Util.RepoLegFromList(aelPerPortfolioLegs)
        aelRepoLegClone = aelRepoLeg.clone()
        aelRepoCF = Util.GetSingleRepoCashFlowFromLeg(aelRepoLegClone, periodStartDate)
        aelRepoCF.end_day = ael.date(cashFlowEndDate)
        aelRepoCF.pay_day = ael.date(cashFlowPayDate)
        aelRepoLegClone.commit()
#----------------------------------------------------------------------------
def SetCallAccountEndDate(portfolioSwap, endDate):
    callDepositLeg = Util.GetCallDepositLeg(portfolioSwap, False)
    redemptionCF = Util.GetRedemptionCashFlowFromLeg(callDepositLeg, True, False)
    redemptionCF.EndDate = endDate
    redemptionCF.PayDate = endDate
    
    redemptionCF.Commit()
#----------------------------------------------------------------------------
# Generates resets, cash flows and payments for the given fixing date
#----------------------------------------------------------------------------
def PerformDailyFixing(pfsParameters, date):
    
    startTime = time.time()
    acm.LogAll("Performing daily fixing for date %s ..."%ael.date(date))
    aelPortfolioSwap = ael.Instrument[pfsParameters.portfolioSwap.Name()]
                      
    (aelSecurities, perSecurityData, perPortfolioData) = GetPortfolioFixingData(
                                                            pfsParameters.portfolioSwap.FundPortfolio(), \
                                                            date, \
                                                            pfsParameters)

    if len(aelSecurities):
        SpreadAdjustFundingRates(aelSecurities, \
                                pfsParameters, \
                                perPortfolioData, \
                                perSecurityData)

        GeneratePerSecurityResets(aelPortfolioSwap, aelSecurities, pfsParameters, perSecurityData, date)
        GenerateDailyCashFlowsPortfolioData(aelPortfolioSwap, \
                                            aelSecurities, \
                                            perSecurityData, \
                                            perPortfolioData, \
                                            date, \
                                            pfsParameters)

        if UsePerPortfolioFunding(pfsParameters):
            FixSingleFinancingAmount(pfsParameters, \
                                    perPortfolioData, \
                                    date, \
                                    GetConfigParameter("includeExpiryDayFunding", pfsParameters.paramDict))

        acm.PollDbEvents()
        portfolioSwapData = CalculatePortfolioSwapFixingData(pfsParameters.portfolioSwap, pfsParameters, date)
        GenerateDailyCashFlowsPortfolioSwapData(aelPortfolioSwap, \
                                                    portfolioSwapData, \
                                                    date, \
                                                    pfsParameters)

        GenerateDailyPayments(pfsParameters, date, perPortfolioData)
                                    
    acm.Log("... Daily fixing for date %s finished in %s seconds."%(ael.date(date), str(time.time()-startTime)))
#----------------------------------------------------------------------------
def GenerateEndReturnResets(pfsParameters, resetStartDate):
    periodStartDay = PeriodCashFlowStartDay( pfsParameters, \
                                            resetStartDate, \
                                            False, \
                                            False)
    perSecurityCashFlows = Util.GetCashFlowsPerSecurity(pfsParameters.portfolioSwap,\
                                                        ReturnCashFlowType(pfsParameters), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay, \
                                                        None, \
                                                        False)

    GenerateInitialResets(perSecurityCashFlows, pfsParameters, resetStartDate)
#----------------------------------------------------------------------------
def GenerateInitialResets(perSecurityCashFlows, pfsParameters, resetEndDate):
    batchIndexArray = Util.GetBatchIndices(len(perSecurityCashFlows), \
                                        GetConfigParameter("resetBatchSize", pfsParameters.paramDict))

    if "Open End" != pfsParameters.portfolioSwap.OpenEnd():
        resetEndDate = pfsParameters.portfolioSwap.ExpiryDateOnly()
    
    for batchIndex in batchIndexArray:
        GenerateSecurityBatchInitialResets(batchIndex, \
                                            perSecurityCashFlows, \
                                            pfsParameters.calendar, \
                                            resetEndDate)
#----------------------------------------------------------------------------
def GenerateSecurityBatchInitialResets(batchIndex, \
                                        cashFlowsPerSecurity, \
                                        calendar, \
                                        endResetDate):
    startTime = time.time()
    acm.LogAll("Generating security initial resets batch (batch size: %s)..."%str(len(batchIndex)))
    try:
        ael.begin_transaction()
        for index in batchIndex:
            returnCF = Util.ReturnCashFlowFromList(cashFlowsPerSecurity[index])
            CreateEndReturnReset(ael.CashFlow[returnCF.Oid()], calendar, endResetDate)
        ael.commit_transaction()
    except Exception, e:
        ael.abort_transaction()
        acm.Log("Failed to generate initial resets: %s"%str(e))
        raise e
    acm.Log("... Security initial resets batch generated in %s seconds"%str(time.time()-startTime))           
#----------------------------------------------------------------------------
def CreateEndReturnReset(aelReturnCF, calendar, endResetDate):
    aelFixingDate = ael.date(endResetDate)
    aelEndDate = ael.date(calendar.AdjustBankingDays(endResetDate, 1))

    Util.CreateReset(aelReturnCF, \
                    "Return", \
                    aelFixingDate, \
                    aelFixingDate, \
                    aelEndDate, \
                    0.0, \
                    False)
#----------------------------------------------------------------------------
def GenerateSecurityBatchResets(batchIndex, \
                                aelCashFlowsPerSecurity, \
                                aelFollowingPeriodCashFlowsPerSecurity, \
                                perSecurityData, \
                                date, \
                                pfsParameters, \
                                includeExpiryDayFunding, \
                                createZeroReturnResets):

    returnFixingValues = Util.GetValueConditionally(perSecurityData, ID_PER_SECURITY_RETURN_FIXING, True)
    positions = Util.GetValueConditionally(perSecurityData, ID_PER_SECURITY_POSITION, True)

    financingAmounts = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_FUNDING_AMOUNT, \
                                                not UsePerPortfolioFunding(pfsParameters))
                                                
    financingRates = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_FUNDING_RATE, \
                                                not UsePerPortfolioFunding(pfsParameters))
    
    repoAmounts = Util.GetValueConditionally(perSecurityData, \
                                            ID_PER_SECURITY_REPO_AMOUNT, \
                                            UsePerSecurityRepo(pfsParameters))
                                            
    repoFinancingRates = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_REPO_FINANCING_RATE, \
                                                UsePerSecurityRepo(pfsParameters))
 
    startTime = time.time()
    acm.LogAll("Generating security daily resets batch (batch size: %s)..."%str(len(batchIndex)))
    try:
        ael.begin_transaction()
        for index in batchIndex:
            CreateSecurityResetsOnDate( aelCashFlowsPerSecurity[index], \
                                        aelFollowingPeriodCashFlowsPerSecurity and \
                                            aelFollowingPeriodCashFlowsPerSecurity[index] or None, \
                                        returnFixingValues[index], \
                                        financingAmounts and financingAmounts[index] or 0.0, \
                                        financingRates and financingRates[index] or 0.0, \
                                        repoAmounts and repoAmounts[index] or 0.0, \
                                        repoFinancingRates and repoFinancingRates[index] or 0.0, \
                                        positions[index], \
                                        date, \
                                        pfsParameters, \
                                        includeExpiryDayFunding, \
                                        createZeroReturnResets)
        ael.commit_transaction()
    except Exception, e:
        ael.abort_transaction()
        acm.Log("Failed to generate resets batch: %s"%str(e))
        raise e
    acm.LogAll("... Security daily resets batch generated in %s seconds"%str(time.time()-startTime))
#----------------------------------------------------------------------------
def GeneratePerSecurityResets(aelPortfolioSwap, \
                                aelSecurities, \
                                pfsParameters, \
                                perSecurityData, \
                                fixingDate):
    periodStartDay = PeriodCashFlowStartDay(pfsParameters, fixingDate, True, True, aelPortfolioSwap)
    
    aelCashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(aelPortfolioSwap, \
                                                        ReturnCashFlowType(pfsParameters), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay, \
                                                        aelSecurities)

    aelFollowingPeriodCashFlowsPerSecurity = None
    if IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, fixingDate) or \
            IsOpenEndRollingPeriodEndDay(pfsParameters, fixingDate):
        periodEndDay = PeriodCashFlowEndDay(pfsParameters, fixingDate, False)
        aelFollowingPeriodCashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(aelPortfolioSwap, \
                                                        ReturnCashFlowType(pfsParameters), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodEndDay, \
                                                        aelSecurities)
    
    batchIndexArray = Util.GetBatchIndices(len(aelSecurities), \
                                            GetConfigParameter("resetBatchSize", pfsParameters.paramDict))
    for batchIndex in batchIndexArray:
        GenerateSecurityBatchResets(batchIndex, \
                                    aelCashFlowsPerSecurity, \
                                    aelFollowingPeriodCashFlowsPerSecurity, \
                                    perSecurityData, \
                                    fixingDate, \
                                    pfsParameters, \
                                    GetConfigParameter("includeExpiryDayFunding", pfsParameters.paramDict), \
                                    True)
#----------------------------------------------------------------------------
def GenerateDailyCashFlowsPortfolioData(aelPortfolioSwap, \
                                        aelSecurities, \
                                        perSecurityData, \
                                        perPortfolioData, \
                                        fixingDate, \
                                        pfsParameters):
    
    returnLegIsPayLeg = pfsParameters.returnLegIsPayLeg
    
    if UsePerPortfolioExecutionFee(pfsParameters):
        executionFee = Util.GetValueConditionally(perPortfolioData, \
                                                ID_PER_PORTFOLIO_EXECUTION_FEE, \
                                                True)
        executionFeeLeg = Util.GetSingleExecutionFeeLeg(aelPortfolioSwap, returnLegIsPayLeg)
        GenerateExecutionFeeCashFlow(executionFeeLeg, executionFee, fixingDate, pfsParameters)
    else:
        executionFees = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_EXECUTION_FEE, \
                                                True)
        aelExecutionFeeLegs = Util.GetExecutionFeeLegs(aelPortfolioSwap, returnLegIsPayLeg, aelSecurities)
        batchIndexArray = Util.GetBatchIndices(len(aelSecurities), \
                                                GetConfigParameter("cashFlowBatchSize", pfsParameters.paramDict))
        for batchIndex in batchIndexArray:
            GenerateExecutionFeeCashFlowsBatch(batchIndex, \
                                                aelSecurities, \
                                                aelExecutionFeeLegs, \
                                                executionFees, \
                                                fixingDate, \
                                                pfsParameters)

    if UseDividendLegs(pfsParameters):
        inventoryPositions = Util.GetValueConditionally(perSecurityData, ID_PER_SECURITY_INV_POSITION, True)
        portfolioSwap = acm.FPortfolioSwap[aelPortfolioSwap.insaddr]
        aelDividendLegsPerSecurity = Util.GetDividendLegs(aelPortfolioSwap, returnLegIsPayLeg, aelSecurities)
        batchIndexArray = Util.GetBatchIndices(len(aelDividendLegsPerSecurity), \
                                                GetConfigParameter("cashFlowBatchSize", pfsParameters.paramDict))
        for batchIndex in batchIndexArray:
            GenerateDividendCashFlowsBatch(batchIndex, \
                                            aelSecurities, \
                                            aelDividendLegsPerSecurity, \
                                            inventoryPositions, \
                                            fixingDate)
#----------------------------------------------------------------------------
def GenerateDailyCashFlowsPortfolioSwapData(aelPortfolioSwap, \
                                            perPortfolioSwapData, \
                                            fixingDate, \
                                            pfsParameters):
    if UseCallDepositLeg(pfsParameters):
        callDepositAmount = Util.GetValueConditionally(perPortfolioSwapData, \
                                                        ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT, \
                                                        True)
        if abs(callDepositAmount) > GetConfigParameter("cashFlowEpsilon", pfsParameters.paramDict):
            aelCallDepositLeg = Util.GetCallDepositLeg(aelPortfolioSwap)
            startAndEndDate = Util.GetFixedAmountStartAndEndDate( \
                                                                str(aelCallDepositLeg.start_day), \
                                                                fixingDate)
            Util.CreatePortfolioSwapCashFlow(aelCallDepositLeg, \
                                                callDepositAmount, \
                                                "Fixed Amount", \
                                                None, \
                                                None, \
                                                None, \
                                                startAndEndDate, \
                                                startAndEndDate, \
                                                fixingDate, \
                                                False)
#----------------------------------------------------------------------------
def GenerateExecutionFeeCashFlow(aelExecutionFeeLeg, \
                                executionFee, \
                                fixingDate, \
                                pfsParameters, \
                                payDay = None):
    if not executionFee:
        return
    if not payDay:
        payDay = Util.AdjustDateToOffsetMethod(fixingDate, \
                                                pfsParameters.calendar, \
                                                Util.DayOffsetToDatePeriod( \
                                                    pfsParameters.portfolioSwap.SpotBankingDaysOffset()), \
                                                pfsParameters.paydayOffsetMethod)

    startAndEndDate = Util.GetFixedAmountStartAndEndDate(str(aelExecutionFeeLeg.start_day), fixingDate)
    Util.CreatePortfolioSwapCashFlow(aelExecutionFeeLeg, \
                                    -1 * executionFee, \
                                    "Fixed Amount", \
                                    None, \
                                    None, \
                                    None, \
                                    startAndEndDate, \
                                    startAndEndDate, \
                                    payDay, \
                                    False)
#----------------------------------------------------------------------------
def GenerateExecutionFeeCashFlowsBatch(batchIndex, \
                                        aelSecurities, \
                                        aelExecutionFeeLegs, \
                                        executionFees, \
                                        fixingDate, \
                                        pfsParameters):
    try:
        ael.begin_transaction()
        for index in batchIndex:
            if executionFees[index]:
                aelSecurity = aelSecurities[index]
                payDay = fixingDate
                
                aelLeg = aelExecutionFeeLegs[index]
                if None != aelLeg:
                    GenerateExecutionFeeCashFlow(aelLeg, \
                                                executionFees[index], \
                                                fixingDate, \
                                                pfsParameters, \
                                                payDay)
        ael.commit_transaction()
    except Exception, e:
        ael.abort_transaction()
        acm.Log("Failed to generate execution fee cash flows batch: %s - Exits"%str(e))
        raise(e)
#----------------------------------------------------------------------------
def GenerateDividendCashFlowsBatch(batchIndex, \
                                    aelSecurities, \
                                    aelDividendLegsPerSecurity, \
                                    inventoryPositions, \
                                    fixingDate):

    try:
        ael.begin_transaction()
        for index in batchIndex:
            dividendLegs = aelDividendLegsPerSecurity[index]
            if dividendLegs:
                aelSecurity = aelSecurities[index]
                inventoryPosition = inventoryPositions[index]
                for leg in dividendLegs:
                    aelCashFlowDividends = [d for d in aelSecurity.dividends() \
                                            if d.ex_div_day == ael.date(fixingDate) and
                                            d.curr == leg.curr]
                    for aelDividend in aelCashFlowDividends:
                        if inventoryPosition:
                            CreatePortfolioSwapDividendCashFlow(leg, \
                                                                aelDividend, \
                                                                inventoryPosition)
        ael.commit_transaction()
    except Exception, e:
        ael.abort_transaction()
        acm.Log("Failed to generate dividend cash flows batch: %s - Exits"%str(e))        
        raise e
#----------------------------------------------------------------------------
def CreatePortfolioSwapDividendCashFlow(aelLeg, \
                                        aelDividend, \
                                        position):
    Util.CreatePortfolioSwapCashFlow(aelLeg, \
                                    aelDividend.dividend * position, \
                                    "Dividend", \
                                    None, \
                                    None, \
                                    None, \
                                    str(aelDividend.ex_div_day), \
                                    str(aelDividend.ex_div_day), \
                                    str(aelDividend.pay_day), \
                                    False)
#----------------------------------------------------------------------------
def CreateSecurityResetsOnDate( aelSecurityCashFlows, \
                                aelSecurityFollowingPeriodCashFlows, \
                                returnFixingValue, \
                                financingAmount, \
                                financingRate, \
                                repoAmount, \
                                repoFinancingRate, \
                                position, \
                                date, \
                                pfsParameters, \
                                includeExpiryDayFunding, \
                                createZeroReturnResets):
    
    aelTotalReturnCF = aelSecurityCashFlows and Util.ReturnCashFlowFromList(aelSecurityCashFlows) or None

    if aelTotalReturnCF and \
        (acm.Time.DateDifference(PeriodCashFlowEndDay(pfsParameters, date, False), date) > 0 or \
            not acm.Time.DateDifference(date, pfsParameters.portfolioSwap.StartDate())):
        CreateReturnResetsOnDate(pfsParameters, \
                                aelTotalReturnCF, \
                                date, \
                                createZeroReturnResets, \
                                returnFixingValue, \
                                position)
                                    
    if IsOpenEndRollingPeriodEndDay(pfsParameters, date):
        aelFollowingTotalReturnCF = None
        if aelSecurityFollowingPeriodCashFlows:
            aelFollowingTotalReturnCF = Util.ReturnCashFlowFromList(aelSecurityFollowingPeriodCashFlows)
        if aelFollowingTotalReturnCF:
            CreateReturnResetsOnDate(pfsParameters, \
                                    aelFollowingTotalReturnCF, \
                                    date, \
                                    True, \
                                    returnFixingValue, \
                                    position)

    aelFinancingCF = aelSecurityCashFlows and Util.FundingCashFlowFromList(aelSecurityCashFlows) or None
    aelFollowingFinancingCF = aelSecurityFollowingPeriodCashFlows and \
                Util.FundingCashFlowFromList(aelSecurityFollowingPeriodCashFlows) or None

    if financingAmount:
        CreateFinancingResetsOnDate(aelFinancingCF, \
                                    aelFollowingFinancingCF, \
                                    financingAmount, \
                                    financingRate, \
                                    date, \
                                    pfsParameters, \
                                    includeExpiryDayFunding)
                                    
    aelRepoCF = aelSecurityCashFlows and Util.RepoCashFlowFromList(aelSecurityCashFlows) or None
    aelFollowingRepoCF = aelSecurityFollowingPeriodCashFlows and \
                Util.RepoCashFlowFromList(aelSecurityFollowingPeriodCashFlows) or None
    if repoAmount:
        CreateFinancingResetsOnDate(aelRepoCF, \
                                    aelFollowingRepoCF, \
                                    repoAmount, \
                                    repoFinancingRate, \
                                    date, \
                                    pfsParameters, \
                                    includeExpiryDayFunding)
#----------------------------------------------------------------------------
def CreateReturnResetsOnDate(pfsParameters, \
                            aelReturnCF, \
                            date, \
                            createZeroReturnResets, \
                            returnFixingValue, \
                            position):

    endDate = pfsParameters.calendar.AdjustBankingDays(date, 1)
    createZeroReturnReset = createZeroReturnResets or \
                            not Util.IsPreviousFixingZero(aelReturnCF, date, "Return")

    if position or (not position and createZeroReturnReset):
        Util.CreateReset(aelReturnCF, "Return", date, date, endDate, returnFixingValue)
        Util.CreateReset(aelReturnCF, "Nominal Scaling", date, date, endDate, position)
#----------------------------------------------------------------------------
def CreateFinancingResetsOnDate(aelFinancingCF, \
                                aelFollowingPeriodFinancingCF, \
                                financingAmount, \
                                financingRate, \
                                date, \
                                pfsParameters, \
                                includeExpiryDayFunding):

    cashFlowStartDate = PeriodCashFlowStartDay(pfsParameters, date, True, False)
    cashFlowEndDate = PeriodCashFlowEndDay(pfsParameters, date, False)

    excludeLastDayFunding = not acm.Time.DateDifference(date, pfsParameters.portfolioSwap.ExpiryDate()) and \
                                    not includeExpiryDayFunding
    excludeFirstDayFunding = not acm.Time.DateDifference(date, cashFlowStartDate) and \
                                    includeExpiryDayFunding and None != pfsParameters.previousPfSwap

    if acm.Time.DateDifference(date, cashFlowEndDate) <= 0 and not excludeLastDayFunding and \
            not excludeFirstDayFunding:

        (fixingDate, fundingStartDate, fundingEndDate) = \
            GetPeriodAdjustedFundingResetDates(date, \
                                                cashFlowStartDate, \
                                                cashFlowEndDate, \
                                                pfsParameters)
        if aelFinancingCF:
            Util.CreateReset(aelFinancingCF, \
                            "Nominal Scaling", \
                            ael.date(fixingDate), \
                            ael.date(fundingStartDate), \
                            ael.date(fundingEndDate), \
                            financingAmount)
            Util.CreateReset(aelFinancingCF, \
                            "Simple Overnight", \
                            ael.date(fixingDate), \
                            ael.date(fundingStartDate), \
                            ael.date(fundingEndDate), \
                            financingRate)

        if IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, date):
            if not aelFollowingPeriodFinancingCF:
                raise Exception("Following period cash flow not found - Exits")
            
            fundingStartDate = fundingEndDate
            fundingEndDate = pfsParameters.calendar.ModifyDate(None, None, fundingStartDate)
            
            Util.CreateReset(aelFollowingPeriodFinancingCF, \
                            "Nominal Scaling", \
                            ael.date(fixingDate), \
                            ael.date(fundingStartDate), \
                            ael.date(fundingEndDate), \
                            financingAmount)
            Util.CreateReset(aelFollowingPeriodFinancingCF, \
                            "Simple Overnight", \
                            ael.date(fixingDate), \
                            ael.date(fundingStartDate), \
                            ael.date(fundingEndDate), \
                            financingRate)
#----------------------------------------------------------------------------
def GetPeriodAdjustedFundingResetDates(date, \
                                        cashFlowStartDate, \
                                        cashFlowEndDate, \
                                        pfsParameters):

    fundingStartDate = date
    periodEndDate = PeriodCashFlowEndDay(pfsParameters, date, False)
    if IsBankingDayBeforePeriodEndDay(pfsParameters, date) and \
            acm.Time.DateDifference(date, periodEndDate):
        fundingEndDate = periodEndDate
    else:
        fundingEndDate = pfsParameters.calendar.AdjustBankingDays(date, 1)

    if MonthEndAdjustFunding(pfsParameters):
        followingBankingDay = pfsParameters.calendar.AdjustBankingDays(date, 1)
        resetDates = (resetStartDate, resetStartDate, followingBankingDay)

        isMonthEnd = acm.Time.DateToYMD(date)[1] != acm.Time.DateToYMD(followingBankingDay)[1]

        if isMonthEnd and (not acm.Time.DateDifference(date, cashFlowStartDate) and \
                    pfsParameters.previousPfSwap) or not acm.Time.DateDifference(date, cashFlowEndDate):
                    
            firstDayOfNewMonth = acm.Time.FirstDayOfMonth(followingBankingDay)
            lastDayOfMonth = acm.Time.DateAddDelta(firstDayOfNewMonth, 0, 0, -1)
            if not acm.Time.DateDifference(date, cashFlowStartDate):
                fundingStartDate = firstDayOfNewMonth
                fundingEndDate = followingBankingDay
            else:
                fundingStartDate = date
                fundingEndDate = firstDayOfNewMonth
    
    return (date, fundingStartDate, fundingEndDate)
#----------------------------------------------------------------------------
# Fix the end return resets via ACM in order to not having to clone the
# entire instrument.
#----------------------------------------------------------------------------
def FixEndTotalReturnResets(pfsParameters, endDate, adjustToPeriodEndDay):
    startTime = time.time()
    acm.LogAll("Fixing total return end resets ...")
    periodStartDay = PeriodCashFlowStartDay(pfsParameters, endDate, False, False)
    cashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(pfsParameters.portfolioSwap, \
                                                        ReturnCashFlowType(pfsParameters), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay,
                                                        None, \
                                                        False)

    returnCashFlows = [Util.ReturnCashFlowFromList(cfs) for cfs in cashFlowsPerSecurity]
    
    if len(returnCashFlows):
        endDate = adjustToPeriodEndDay and PeriodCashFlowEndDay(pfsParameters, endDate, False) or endDate
        endReturnResets = GetEndReturnResets(returnCashFlows, endDate, None, False)

        batchIndexArray = Util.GetBatchIndices(len(endReturnResets), \
                                                GetConfigParameter("resetBatchSize", pfsParameters.paramDict))
        for batchIndex in batchIndexArray:
            FixEndTotalReturnResetsBatch(endReturnResets, endDate, batchIndex)
    acm.LogAll("... Total return end resets fixed in %s seconds"%str(time.time()-startTime))
#----------------------------------------------------------------------------
def FixEndTotalReturnResetsBatch(endReturnResets, \
                                    endDate, \
                                    batchIndex):
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            returnReset = endReturnResets[index]
            if returnReset:
                previousReturnReset = Util.GetPreviousFixing(returnReset.CashFlow(), "Return", endDate, False)
                if previousReturnReset:
                    returnReset.FixingValue = previousReturnReset.FixingValue()
                    returnReset.ReadTime(endDate)
                    returnReset.Commit()
        acm.CommitTransaction()
    except Exception, e:
        acm.AbortTransaction()
        raise e
#----------------------------------------------------------------------------
def CheckEndReturnResets(pfsParameters, fixingDate):
    if not acm.Time.DateDifference(fixingDate, pfsParameters.portfolioSwap.StartDate()):
        return True
    if pfsParameters.calendar.IsNonBankingDay(None, None, fixingDate):
        fixingDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, 1)

    periodStartDay = PeriodCashFlowStartDay(pfsParameters, fixingDate, False, False)
    cashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(pfsParameters.portfolioSwap, \
                                                        ReturnCashFlowType(pfsParameters), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay, \
                                                        None, \
                                                        False)

    returnCashFlows = [Util.ReturnCashFlowFromList(baseCFList) for baseCFList in cashFlowsPerSecurity]
    if len(returnCashFlows):
        endReturnResetDate = GetEndReturnResetDate(pfsParameters, fixingDate)
        endReturnResets = GetEndReturnResets(returnCashFlows, fixingDate, endReturnResetDate, False)
        return endReturnResets and True or False
    return True
#----------------------------------------------------------------------------
def GetEndReturnResetDate(pfsParameters, fixingDate):
    endResetDate = None
    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        if IsRollingDay(pfsParameters, fixingDate):
            endResetDate = PeriodCashFlowEndDay(pfsParameters, fixingDate, False)
        else:
            endResetDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, 1)
    else:
        endResetDate = pfsParameters.ExpiryDate()
    return endResetDate
#----------------------------------------------------------------------------
def AdjustEndReturnResetsOpenEnd(aelReturnCashFlowsClones, \
                                fixingDate, \
                                pfsParameters, \
                                adjustToPeriodEndDay, \
                                periodEndDay):
    startTime = time.time()
    calendar = pfsParameters.calendar
    acm.LogAll("Extending end total return resets open end...")
    newFixingDate = calendar.AdjustBankingDays(fixingDate, 1)
    newEndDate = calendar.AdjustBankingDays(newFixingDate, 1)
    aelEndReturnResetsClones = GetEndReturnResets(aelReturnCashFlowsClones, fixingDate, newFixingDate)
    if not aelEndReturnResetsClones:
        errMess = "ERROR: Could not adjust end return resets from date %s - Exits"%ael.date(fixingDate)
        acm.Log(errMess)
        raise Exception(errMess)

    if adjustToPeriodEndDay:
        newFixingDate = periodEndDay
        newEndDate = calendar.AdjustBankingDays(periodEndDay, 1)

    aelCashFlowsAndResetsClones = list(zip(aelReturnCashFlowsClones, aelEndReturnResetsClones))
    batchIndexArray = Util.GetBatchIndices(len(aelCashFlowsAndResetsClones), \
                                            GetConfigParameter("cashFlowBatchSize", pfsParameters.paramDict))
    for batchIndex in batchIndexArray:
        AdjustEndReturnResetsOpenEndBatch(batchIndex, \
                                            aelCashFlowsAndResetsClones, \
                                            newFixingDate, \
                                            newEndDate)
    acm.Log("... End return resets extended in %s seconds"%str(time.time()-startTime))
#----------------------------------------------------------------------------
def GetEndReturnResets(returnCashFlows, fixingDate, newFixingDate = None, isAel = True):
    endReturnResets = []
    if newFixingDate:
        endReturnResets = Util.GetResetsOfTypeAtDate(returnCashFlows, "Return", newFixingDate, isAel)
    if not endReturnResets:
        endReturnResets = Util.GetResetsOfTypeAtDate(returnCashFlows, "Return", fixingDate, isAel)
    if not endReturnResets:
        acm.LogAll("End return resets not found for fixing date %s"%ael.date(fixingDate))
        raise Exception()
    return endReturnResets
#----------------------------------------------------------------------------
def AdjustEndReturnResetsOpenEndBatch(batchIndex, \
                                        aelCashFlowsAndReturnResets, \
                                        newFixingDate, \
                                        newEndDate):
    try:
        ael.begin_transaction()
        for index in batchIndex:
            aelCashFlowClone, aelResetClone = aelCashFlowsAndReturnResets[index]
            if aelCashFlowClone and aelResetClone:
                aelNewFixingDate = ael.date(newFixingDate)
                aelResetClone.day = aelNewFixingDate
                aelResetClone.start_day = aelNewFixingDate
                aelResetClone.end_day = ael.date(newEndDate)
                aelResetClone.value = 0.0                    
                aelResetClone.read_time = 0
                aelCashFlowClone.commit()
        ael.commit_transaction()
    except Exception, e:
        ael.abort_transaction()
        raise e
#----------------------------------------------------------------------------
def ClearCashFlowsFromDateUntilEnd(pfsParameters, fromDate):

    portfolioSwap = pfsParameters.portfolioSwap
    if not acm.Time.DateDifference(fromDate, portfolioSwap.StartDate()) or \
            IsBankingDayAfterPeriodEndDay(pfsParameters, fromDate):
        fromDate = acm.Time.DateAddDelta(fromDate, 0, 0, 1)

    cashFlowsToDelete = []
    for leg in portfolioSwap.Legs():
        for cashFlow in leg.CashFlows():
            if acm.Time.DateDifference(cashFlow.StartDate(), fromDate) >= 0:
                cashFlowsToDelete.append(cashFlow)

    batchIndexArray = Util.GetBatchIndices(len(cashFlowsToDelete), \
                                    GetConfigParameter("cashFlowBatchSize", pfsParameters.paramDict))
    for batchIndex in batchIndexArray:
        Util.ClearCashFlowsBatch(batchIndex, cashFlowsToDelete)
#----------------------------------------------------------------------------
def ClearResetsFromDateUntilEnd(pfsParameters, fromDate):
    allCashFlows = [cf for leg in pfsParameters.portfolioSwap.Legs() for cf in leg.CashFlows()]
    
    lastResetDate = Util.GetLastResetDate(pfsParameters.portfolioSwap)
    currentDate = fromDate

    while currentDate and acm.Time.DateDifference(lastResetDate, currentDate) >= 0:
        Util.ClearPortfolioSwapDailyResets(allCashFlows, \
                                        currentDate, \
                                        GetConfigParameter("resetClearingBatchSize", pfsParameters.paramDict))
        currentDate = acm.Time.DateAddDelta(currentDate, 0, 0, 1)
#----------------------------------------------------------------------------
def ClearPaymentsFromDateUntilEnd(pfsParameters, periodStartDate):
    if UsesPayments(pfsParameters):
        singleTrade = Util.GetSingleTrade(pfsParameters.portfolioSwap)
        tradePayments = singleTrade.Payments()
        if len(tradePayments):
            lastPaymentDate = acm.Time.SmallDate()
            for payment in tradePayments:
                if acm.Time.DateDifference(payment.ValidFrom(), lastPaymentDate) >= 0:
                    lastPaymentDate = payment.ValidFrom()
                    
            fixingDate = periodStartDate
            while acm.Time.DateDifference(lastPaymentDate, fixingDate) >= 0:
                Util.ClearPayments(pfsParameters.portfolioSwap, fixingDate)
                fixingDate = acm.Time.DateAddDelta(fixingDate, 0, 0, 1)
#----------------------------------------------------------------------------
# Get fixing data for the portfolio positions.
# NOTE: Securities are returned as AEL-entities
#----------------------------------------------------------------------------
def GetPortfolioFixingData(portfolio, \
                            fixingDate, \
                            pfsParameters):
    startTime = time.time()
    acm.LogAll("Calculating fixing data for date %s ..."%ael.date(fixingDate))

    context = acm.GetDefaultContext()
    sheetType = acm.FPortfolioSheet

    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
    calcSpace.SimulateGlobalValue(colIdPnLEndDate, "Custom Date")
    calcSpace.SimulateGlobalValue(colIdPnLEndDateCustom, fixingDate)

    calcSpace.InsertItem(portfolio)
    calcSpace.Refresh()

    portfolioIter = calcSpace.RowTreeIterator().FirstChild()
   
    perPortfolioData = CalculatePerPortfolioFixingData(calcSpace, \
                                                        portfolioIter.Tree(), \
                                                        fixingDate, \
                                                        pfsParameters)
    aelSecurities = []
    perSecurityData = {}
   
    childIter = portfolioIter.FirstChild()
    while childIter:
        securityName = calcSpace.CalculateValue(childIter.Tree(), 'Instrument Name')
        aelSecurities.append(ael.Instrument[securityName])

        securityData = CalculatePerSecurityFixingData(calcSpace, \
                                                    childIter.Tree(), \
                                                    fixingDate, \
                                                    pfsParameters)
                                                    
        AppendSecurityData(perSecurityData, securityData, pfsParameters)
        childIter = childIter.NextSibling()
        
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDate)
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDateCustom)

    acm.LogAll("... Fixing data for date %s calculated in %s seconds"% \
                (ael.date(fixingDate), str(time.time()-startTime)))

    return (aelSecurities, perSecurityData, perPortfolioData)
#----------------------------------------------------------------------------
def CalculatePerPortfolioFixingData(calcSpace, \
                                    portfolioTreeNode, \
                                    fixingDate, \
                                    pfsParameters):
    customFixingData = None
    if Custom:
        try:
            customFixingData = Custom.CalculatePerPortfolioFixingData(calcSpace, \
                                                                    portfolioTreeNode, \
                                                                    UsePerPortfolioFunding(pfsParameters), \
                                                                    UsePerPortfolioExecutionFee(pfsParameters), \
                                                                    UsePerPortfolioRPL(pfsParameters))
        except Exception, e:
            acm.Log("Failed to evaluate custom per portfolio swap fixing data for date %s: %s" \
                    %(ael.date(fixingDate), str(e)))
            raise e

    fixingData = CalculatePerPortfolioDefaultFixingData(calcSpace, \
                                                        portfolioTreeNode, \
                                                        customFixingData, \
                                                        fixingDate, \
                                                        pfsParameters)
    return fixingData
#----------------------------------------------------------------------------
def CalculatePerPortfolioDefaultFixingData(calcSpace, \
                                            portfolioTreeNode, \
                                            customFixingData, \
                                            fixingDate, \
                                            pfsParameters):
    if customFixingData:
        fixingData = customFixingData
    else:
        fixingData = {}

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_FUNDING_AMOUNT, \
                                        UsePerPortfolioFunding(pfsParameters)):
        financingAmount = Util.CalculateRowValueAsDouble( \
                                                calcSpace, \
                                                portfolioTreeNode, \
                                                GetConfigParameter("colIdFinancingAmount", pfsParameters.paramDict), \
                                                "Portfolio", \
                                                fixingDate)
        if not pfsParameters.returnLegIsPayLeg:
            financingAmount = -financingAmount

        fixingData[ID_PER_PORTFOLIO_FUNDING_AMOUNT] = financingAmount
        
    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_FUNDING_RATE, \
                                        UsePerPortfolioFunding(pfsParameters)):
        floatRef = pfsParameters.floatRef
        overnightRate = GetOvernightRate(floatRef, fixingDate)
        Util.CheckForNaN(overnightRate, "Overnight rate", floatRef.Name(), fixingDate)
        fixingData[ID_PER_PORTFOLIO_FUNDING_RATE] = overnightRate

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_EXECUTION_FEE, \
                                        UsePerPortfolioExecutionFee(pfsParameters)):
        fixingData[ID_PER_PORTFOLIO_EXECUTION_FEE] = Util.CalculateRowValueAsDouble( \
                                                        calcSpace, \
                                                        portfolioTreeNode, \
                                                        GetConfigParameter("colIdDailyExecutionFee", pfsParameters.paramDict), \
                                                        "Portfolio", \
                                                        fixingDate)

    fixingData[ID_PER_PORTFOLIO_PAYMENTS] = CalculatePayments(\
                                    calcSpace, \
                                    portfolioTreeNode, \
                                    GetConfigParameter("paymentTypes", pfsParameters.paramDict), \
                                    pfsParameters, \
                                    pfsParameters.portfolioSwap.FundPortfolio().Name(), \
                                    fixingDate)
    return fixingData
#----------------------------------------------------------------------------
def CalculatePerSecurityFixingData( calcSpace, \
                                    securityTreeNode, \
                                    fixingDate, \
                                    pfsParameters):
    customFixingData = None
    if Custom:
        try:
            customFixingData = Custom.CalculatePerSecurityFixingData(calcSpace, \
                                                            securityTreeNode, \
                                                            not UsePerPortfolioFunding(pfsParameters), \
                                                            not UsePerPortfolioExecutionFee(pfsParameters), \
                                                            UsePerSecurityRepo(pfsParameters))
        except Exception, e:
            acm.Log("Failed to evaluate custom per security fixing data for date %s - %s" \
                    %(ael.date(fixingDate), str(e)))
            raise e

    fixingData = CalculatePerSecurityDefaultFixingData(calcSpace, \
                                                        securityTreeNode, \
                                                        fixingDate, \
                                                        customFixingData, \
                                                        pfsParameters)
    return fixingData
#----------------------------------------------------------------------------
def CalculatePerSecurityDefaultFixingData(calcSpace, \
                                        securityTreeNode, \
                                        fixingDate, \
                                        customFixingData, \
                                        pfsParameters):
    if customFixingData:
        fixingData = customFixingData
    else:
        fixingData = {}

    security = securityTreeNode.Item().Instrument()
    securityName = security.Name()
    position = Util.CalculateRowValueAsDouble(calcSpace, \
                                                securityTreeNode, \
                                                GetConfigParameter("colIdPosition", pfsParameters.paramDict), \
                                                securityName, \
                                                fixingDate)
    
    # Dividend comparison rule: acquire day < ex div day + spot
    securitySpotDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, security.SpotBankingDaysOffset() - 1)
    spotOffset = acm.Time.DateDifference(securitySpotDate, fixingDate)

    timeBucketsInventory = acm.Time.CreateTimeBuckets(fixingDate, \
                                                        "'0d'", \
                                                        None, \
                                                        None, \
                                                        spotOffset, \
                                                        False, False, False, False, False)
    inventoryPositionColumnConfig = acm.Sheet().Column().ConfigurationFromTimeBuckets(timeBucketsInventory)
    
    inventoryPosition = Util.CalculateRowValueAsDouble(calcSpace, \
                                            securityTreeNode, \
                                            GetConfigParameter("colIdInventoryPosition", pfsParameters.paramDict), \
                                            securityName, \
                                            fixingDate, \
                                            False, \
                                            inventoryPositionColumnConfig)

    if GetConfigParameter("fixTotalInvested", pfsParameters.paramDict):
        returnFixingValue = Util.CalculateRowValueAsDouble( \
                                            calcSpace, \
                                            securityTreeNode, \
                                            GetConfigParameter("colIdTotalInvested", pfsParameters.paramDict), \
                                            securityName, \
                                            fixingDate)
    else:
        averagePrice = Util.CalculateRowValueAsDouble(calcSpace, \
                                            securityTreeNode, \
                                            GetConfigParameter("colIdAveragePrice", pfsParameters.paramDict), \
                                            securityName, \
                                            fixingDate, \
                                            True)
        if not acm.Math.IsFinite(averagePrice):
            averagePrice = 0.0
        returnFixingValue = averagePrice

    fixingData[ID_PER_SECURITY_POSITION] = position
    fixingData[ID_PER_SECURITY_INV_POSITION] = inventoryPosition
    fixingData[ID_PER_SECURITY_RETURN_FIXING] = returnFixingValue

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_FUNDING_AMOUNT, \
                                        not UsePerPortfolioFunding(pfsParameters)):

        financingAmount = Util.CalculateRowValueAsDouble( \
                                            calcSpace, \
                                            securityTreeNode, \
                                            GetConfigParameter("colIdFinancingAmount", pfsParameters.paramDict), \
                                            securityName, \
                                            fixingDate)
                                                        
        if not pfsParameters.returnLegIsPayLeg:
            financingAmount = -financingAmount
        fixingData[ID_PER_SECURITY_FUNDING_AMOUNT] = financingAmount

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_FUNDING_RATE, \
                                        not UsePerPortfolioFunding(pfsParameters)):
        floatRef = pfsParameters.floatRef
        overnightRate = GetOvernightRate(floatRef, fixingDate)
        Util.CheckForNaN(overnightRate, "Overnight rate", floatRef.Name(), fixingDate)
        fixingData[ID_PER_SECURITY_FUNDING_RATE] = overnightRate

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_EXECUTION_FEE, \
                                        not UsePerPortfolioExecutionFee(pfsParameters)):
        fixingData[ID_PER_SECURITY_EXECUTION_FEE] = Util.CalculateRowValueAsDouble( \
                                            calcSpace, \
                                            securityTreeNode, \
                                            GetConfigParameter("colIdDailyExecutionFee", pfsParameters.paramDict), \
                                            securityName, \
                                            fixingDate)

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_REPO_AMOUNT, \
                                        UsePerSecurityRepo(pfsParameters)):
        fixingData[ID_PER_SECURITY_REPO_AMOUNT] = 0.0
        
    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_REPO_FINANCING_RATE, \
                                        UsePerSecurityRepo(pfsParameters)):
        fixingData[ID_PER_SECURITY_REPO_FINANCING_RATE] = 0.0

    return fixingData
#----------------------------------------------------------------------------
def CalculatePortfolioSwapFixingData(portfolioSwap, pfsParameters, fixingDate, calculateDailyCash = False):
    startTime = time.time()
    acm.LogAll("Calculating Portfolio Swap fixing data for date %s ..."%ael.date(fixingDate))

    context = acm.GetDefaultContext()
    sheetType = acm.FPortfolioSheet

    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)

    calcSpace.SimulateGlobalValue(colIdPnLEndDate, "Custom Date")
    calcSpace.SimulateGlobalValue(colIdPnLEndDateCustom, fixingDate)

    calcSpace.InsertItem(Util.GetSingleTrade(portfolioSwap))
    calcSpace.Refresh()

    portfolioSwapIter = calcSpace.RowTreeIterator().FirstChild()


    portfolioSwapData = {}
    if Custom:
        portfolioSwapData = Custom.CalculatePortfolioSwapFixingData(calcSpace, \
                                                                    portfolioSwapIter.Tree(), \
                                                                    UseCallDepositLeg(pfsParameters), \
                                                                    calculateDailyCash)
    
    if not Util.CheckValueConditionally(portfolioSwapData, \
                                        ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT, \
                                        UseCallDepositLeg(pfsParameters)):

        portfolioSwapData[ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT] = -1.0 * \
                            Util.CalculateRowValueAsDouble( \
                                calcSpace, \
                                portfolioSwapIter.Tree(), \
                                GetConfigParameter("colIdCallDepositAmount", pfsParameters.paramDict), \
                                portfolioSwap.Name(), \
                                fixingDate, \
                                workAroundCAPIBug)
    
    if calculateDailyCash and not Util.CheckValueConditionally(portfolioSwapData, \
                                                                ID_PORTFOLIO_SWAP_DAILY_CASH, \
                                                                UseCallDepositLeg(pfsParameters)):
        portfolioSwapData[ID_PORTFOLIO_SWAP_DAILY_CASH] = \
                                            Util.CalculateRowValueAsDouble( \
                                                calcSpace, \
                                                portfolioSwapIter.Tree(), \
                                                GetConfigParameter("colIdDailyCash", pfsParameters.paramDict), \
                                                portfolioSwap.Name(), \
                                                fixingDate)
    
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDate)
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDateCustom)

    acm.LogAll("... Portfolio Swap fixing data for date %s calculated in %s seconds"% \
                (ael.date(fixingDate), str(time.time()-startTime)))
    return portfolioSwapData
#----------------------------------------------------------------------------
def CalculatePayments(calcSpace, \
                        rowNode, \
                        paymentTypes, \
                        pfsParameters, \
                        entityId, \
                        fixingDate):

    colId = GetConfigParameter("colIdPaymentsPerType", pfsParameters.paramDict)

    payments = {}
    for paymentType in paymentTypes:
        namedParameters = acm.FNamedParameters()
        namedParameters.AddParameter("paymentType", paymentType)
        columnConfig = acm.Sheet().Column().ConfigurationFromVector(namedParameters)
        payment = Util.CalculateRowValueAsDouble(calcSpace, \
                                                rowNode, \
                                                colId, \
                                                entityId, \
                                                fixingDate, \
                                                False, \
                                                columnConfig)
        payments[paymentType] = payment
    return payments
#----------------------------------------------------------------------------
def AppendSecurityData(perSecurityData, securityData, pfsParameters):
    
    try:
        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_POSITION, True)
        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_INV_POSITION, True)
        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_RETURN_FIXING, True)

        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_FUNDING_AMOUNT, \
                                    not UsePerPortfolioFunding(pfsParameters))
        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_FUNDING_RATE, \
                                    not UsePerPortfolioFunding(pfsParameters))
        
        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_EXECUTION_FEE, \
                                    not UsePerPortfolioExecutionFee(pfsParameters))
        
        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_REPO_AMOUNT, \
                                    UsePerSecurityRepo(pfsParameters))
                                    
        Util.AppendListConditionally(perSecurityData, \
                                    securityData, 
                                    ID_PER_SECURITY_REPO_FINANCING_RATE, \
                                    UsePerSecurityRepo(pfsParameters))
                                    
    except Exception, e:
        acm.Log("Missing per security data - %s"%str(e))
        raise e
#----------------------------------------------------------------------------
def GetOvernightRate(floatRef, date):
    calcSpace = acm.FStandardCalculationsSpaceCollection()
    priceDV = floatRef.Calculation().MarketPrice(calcSpace, \
                                                date,          # date \
                                                False,         # correct date \
                                                None,          # currency \
                                                False,         # correct currency \
                                                None,          # market place \
                                                False,         # correct market place \
                                                "ClosePrice",  # price type \
                                                False)         # correct type

    if priceDV is None:
        return acm.Math.NotANumber()
    return priceDV.Number()
#----------------------------------------------------------------------------
# - Generates legs and cash flows corresponding to the positions in the selected
# portfolio.
# - Clears old legs and cash flows.
# - Generates initial return resets
#----------------------------------------------------------------------------
def GeneratePortfolioSwap(pfsParameters, resetEndDate):
    periodStartDate = pfsParameters.portfolioSwap.StartDate()
    followingBankingDay = pfsParameters.calendar.AdjustBankingDays(periodStartDate, 1)
    
    periodEndDate = PeriodCashFlowEndDay(pfsParameters, \
                                        followingBankingDay, \
                                        False)

    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        pfsParameters.portfolioSwap.ExpiryDate = periodEndDate
        pfsParameters.portfolioSwap.Commit()
  
    Util.ClearPortfolioSwapLegs(pfsParameters.portfolioSwap, Conf.legClearingBatchSize)
    perSecurityCashFlows = GeneratePortfolioSwapLegsAndCashFlows(pfsParameters, \
                                                                    pfsParameters.portfolioSwap.StartDate(), \
                                                                    resetEndDate)
    
    Util.ClearPortfolioSwapResets(pfsParameters.portfolioSwap, \
                                    GetConfigParameter("resetClearingBatchSize", pfsParameters.paramDict))
    Util.ClearPayments(pfsParameters.portfolioSwap)
    GenerateInitialResets(perSecurityCashFlows, pfsParameters, periodStartDate)
#----------------------------------------------------------------------------
def GeneratePortfolioSwapLegsAndCashFlows(pfsParameters, periodStartDate, periodEndDate):
    (legStartDate, legEndDate) = GetLegStartAndEndDate(pfsParameters, \
                                                        pfsParameters.portfolioSwap.StartDate(), \
                                                        periodEndDate)
    GeneratePerPortfolioSwapLegs(pfsParameters, \
                                legStartDate, \
                                legEndDate, \
                                UsePerPortfolioFunding(pfsParameters), \
                                UsePerPortfolioExecutionFee(pfsParameters), \
                                UsePerPortfolioRepo(pfsParameters), \
                                UseCallDepositLeg(pfsParameters), \
                                UseMarginLeg(pfsParameters))
                                
    GeneratePerPortfolioSwapCashFlows(pfsParameters, \
                                        legStartDate, \
                                        UsePerPortfolioFunding(pfsParameters), \
                                        UsePerPortfolioRepo(pfsParameters), \
                                        UseCallDepositLeg(pfsParameters))
    
    baseLegs = GeneratePerSecurityLegs(pfsParameters, \
                                        periodStartDate, \
                                        periodEndDate, \
                                        not UsePerPortfolioFunding(pfsParameters), \
                                        not UsePerPortfolioExecutionFee(pfsParameters), \
                                        UsePerSecurityRepo(pfsParameters), \
                                        UseDividendLegs(pfsParameters))

    perSecurityCashFlows = GeneratePerSecurityCashFlows(pfsParameters, \
                                                    baseLegs, \
                                                    legStartDate, \
                                                    legEndDate, \
                                                    "Open End" == pfsParameters.portfolioSwap.OpenEnd())
    return perSecurityCashFlows
#----------------------------------------------------------------------------
def GeneratePerPortfolioSwapLegs(pfsParameters, \
                                legStartDate, \
                                legEndDate, \
                                createFinancingLeg, \
                                createExecutionFeeLeg, \
                                createRepoLeg, \
                                createCallDepositLeg, \
                                createMarginLeg):
    if createFinancingLeg:
        financingLeg = CreateSingleFinancingLeg(pfsParameters, legStartDate, legEndDate)
        financingLeg.Commit()
    
    if createCallDepositLeg:
        callDepositLeg = CreateCallDepositLeg(pfsParameters, legStartDate, legEndDate)
        callDepositLeg.Commit()

    if createRepoLeg:
        repoLeg = CreateRepoLeg(pfsParameters, legStartDate, legEndDate, None)
        repoLeg.Commit()
        
    if createExecutionFeeLeg:
        executionFeeLeg = CreateExecutionFeeLeg(pfsParameters, legStartDate, legEndDate, None)
        executionFeeLeg.Commit()

    if createMarginLeg:
        marginLeg = CreateMarginLeg(pfsParameters, \
                                    legStartDate, \
                                    legEndDate)
        marginLeg.Commit()
#----------------------------------------------------------------------------
def GeneratePerPortfolioSwapCashFlows(pfsParameters, \
                                    periodStartDate, \
                                    createFinancingCashFlow, \
                                    createRepoCashFlow, \
                                    createCallDepositRedemptionCashFlow):
                                    
    aelPortfolioSwap = ael.Instrument[pfsParameters.portfolioSwap.Oid()]
    if createFinancingCashFlow:
        aelFinancingLeg = Util.GetSingleFinancingLeg(aelPortfolioSwap, pfsParameters.returnLegIsPayLeg)
        Util.CreatePortfolioSwapCashFlow(aelFinancingLeg, \
                                        0.0, \
                                        "Float Rate", \
                                        pfsParameters.calendar, \
                                        pfsParameters.paydayOffset, \
                                        pfsParameters.paydayOffsetMethod, \
                                        periodStartDate, \
                                        str(aelFinancingLeg.end_day), \
                                        None, \
                                        "Open End" == pfsParameters.portfolioSwap.OpenEnd())

    if createRepoCashFlow:
        pass

    if createCallDepositRedemptionCashFlow:
        aelDepositLeg = Util.GetCallDepositLeg(aelPortfolioSwap)
        if not Util.GetRedemptionCashFlowFromLeg(aelDepositLeg, False):
            Util.CreatePortfolioSwapCashFlow(aelDepositLeg, \
                                            0.0, \
                                            "Redemption Amount", \
                                            pfsParameters.calendar, \
                                            pfsParameters.paydayOffset, \
                                            pfsParameters.paydayOffsetMethod, \
                                            periodStartDate, \
                                            periodStartDate, \
                                            None, \
                                            False)
#----------------------------------------------------------------------------
def GetLegStartAndEndDate(pfsParameters, \
                            resetStartDate, \
                            resetEndDate):

    isOpenEnd = "Open End" == pfsParameters.portfolioSwap.OpenEnd()
    if isOpenEnd:
        legStartDate = PeriodCashFlowStartDay(pfsParameters, resetStartDate, True, False)
        if not acm.Time.DateDifference(resetStartDate, resetEndDate):
            resetEndDate = acm.Time.DateAddDelta(resetEndDate, 0, 0, 1)
        legEndDate = PeriodCashFlowEndDay(pfsParameters, resetEndDate, False)
    else:
        legStartDate = pfsParameters.portfolioSwap.StartDate()
        legEndDate = pfsParameters.portfolioSwap.ExpiryDate()
    return (legStartDate, legEndDate)
#----------------------------------------------------------------------------
def GeneratePerSecurityLegs(pfsParameters, \
                            resetStartDate, \
                            resetEndDate, \
                            generateFinancingLegs, \
                            generateExecutionFeeLegs, \
                            generateRepoLegs, \
                            generateDividendLegs):
    baseLegs = []

    for periodStartDate, periodEndDate in GetCashFlowPeriods(pfsParameters, \
                                                            resetStartDate, \
                                                            resetEndDate):
        newAELSecurities = Util.GetNewSecurities( \
                                            ael.Instrument[pfsParameters.portfolioSwap.Name()], \
                                            pfsParameters.portfolioSwap.FundPortfolio(), \
                                            pfsParameters.returnLegIsPayLeg, \
                                            NonZeroColumnsIds(pfsParameters), \
                                            periodStartDate, \
                                            IsOpenEndRollingPeriodEndDay(pfsParameters, periodEndDate) and \
                                                acm.Time.DateAddDelta(periodEndDate, 0, 0, -1) or \
                                                periodEndDate)
        
        batchIndexArray = Util.GetBatchIndices(len(newAELSecurities), \
                                        GetConfigParameter("legBatchSize", pfsParameters.paramDict))

        for batchIndex in batchIndexArray:
            batchBaseLegs = GeneratePerSecurityLegsBatch(batchIndex, \
                                                        pfsParameters, \
                                                        newAELSecurities, \
                                                        periodStartDate, \
                                                        periodEndDate, \
                                                        generateFinancingLegs, \
                                                        generateExecutionFeeLegs, \
                                                        generateRepoLegs, \
                                                        generateDividendLegs)
            baseLegs.extend(batchBaseLegs)
    return baseLegs
#----------------------------------------------------------------------------
def GeneratePerSecurityCashFlows(pfsParameters, \
                                baseLegs, \
                                cFStartDate, \
                                cFEndDate, \
                                openEndAdjustDates = True, \
                                onlyAfterLegStartDate = True):

    perSecurityCashFlows = []
    batchIndexArray = Util.GetBatchIndices(len(baseLegs), \
                                            GetConfigParameter("cashFlowBatchSize", pfsParameters.paramDict))
    for batchIndex in batchIndexArray:
        batchPerSecurityCashFlows = GeneratePerSecurityCashFlowsBatch(batchIndex, \
                                                            baseLegs, \
                                                            pfsParameters, \
                                                            cFStartDate, \
                                                            cFEndDate, \
                                                            openEndAdjustDates, \
                                                            onlyAfterLegStartDate)
        perSecurityCashFlows.extend(batchPerSecurityCashFlows)
    return perSecurityCashFlows
#----------------------------------------------------------------------------
def CreateSingleFinancingLeg(pfsParameters, legStartDate, legEndDate):
    financingLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                            "Float", \
                                            "Simple Overnight", \
                                            not pfsParameters.returnLegIsPayLeg, \
                                            None, \
                                            legStartDate, \
                                            legEndDate, \
                                            0.0, \
                                            0.0, \
                                            pfsParameters.daycountMethod, \
                                            "Position Total", \
                                            pfsParameters.floatRef)
    return financingLeg
#----------------------------------------------------------------------------
def CreateCallDepositLeg(pfsParameters, legStartDate, legEndDate):
    callDepositLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                            "Call Fixed", \
                                            "None", \
                                            not pfsParameters.returnLegIsPayLeg, \
                                            None, \
                                            legStartDate, \
                                            legEndDate, \
                                            0.0, \
                                            0.0, \
                                            pfsParameters.daycountMethod, \
                                            "None", \
                                            None)
    return callDepositLeg
#----------------------------------------------------------------------------
def CreateRepoLeg(pfsParameters, legStartDate, legEndDate, security):
    repoLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                            "Float", \
                                            "Simple Overnight", \
                                            pfsParameters.returnLegIsPayLeg, \
                                            security, \
                                            legStartDate, \
                                            legEndDate, \
                                            0.0, \
                                            0.0, \
                                            pfsParameters.daycountMethod, \
                                            "Position Total", \
                                            pfsParameters.floatRef)
    return repoLeg
#----------------------------------------------------------------------------
def CreateExecutionFeeLeg(pfsParameters, legStartDate, legEndDate, security):
    executionFeeLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                            "Fixed", \
                                            "None", \
                                            not pfsParameters.returnLegIsPayLeg, \
                                            security, \
                                            legStartDate, \
                                            legEndDate, \
                                            0.0, \
                                            0.0, \
                                            pfsParameters.daycountMethod, \
                                            "None")
    return executionFeeLeg
#----------------------------------------------------------------------------
def CreateMarginLeg(pfsParameters, legStartDate, legEndDate):
    marginLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                            "Fixed", \
                                            "None", \
                                            pfsParameters.returnLegIsPayLeg, \
                                            None, \
                                            legStartDate, \
                                            legEndDate, \
                                            0.0, \
                                            0.0, \
                                            pfsParameters.daycountMethod, \
                                            "None")
    return marginLeg
#----------------------------------------------------------------------------
def GeneratePerSecurityLegsBatch(batchIndex, \
                                    pfsParameters, \
                                    aelSecurities, \
                                    legStartDate, \
                                    legEndDate, \
                                    generateFinancingLegs, \
                                    generateExecutionFeeLegs, \
                                    generateRepoLegs, \
                                    generateDividendLegs):

    securityBatchBaseLegs = GenerateSecurityBaseLegsBatch(batchIndex,\
                                                            pfsParameters, \
                                                            aelSecurities, \
                                                            legStartDate, \
                                                            legEndDate, \
                                                            generateFinancingLegs, \
                                                            generateExecutionFeeLegs, \
                                                            generateRepoLegs)

    securityBatchDividendLegs = []
    if generateDividendLegs:
        securityBatchDividendLegs = GeneratePortfolioSwapDividendLegsBatch(pfsParameters.portfolioSwap, \
                                                                        pfsParameters.returnLegIsPayLeg, \
                                                                        securityBatchBaseLegs, \
                                                                        not generateFinancingLegs, \
                                                                        legStartDate)
    
    map(lambda x, y : x.append(y), securityBatchBaseLegs, securityBatchDividendLegs)
    return securityBatchBaseLegs
#----------------------------------------------------------------------------
def GenerateSecurityBaseLegsBatch(batchIndex, \
                                    pfsParameters, \
                                    aelSecurities, \
                                    legStartDate, \
                                    legEndDate, \
                                    generateFinancingLegs, \
                                    generateExecutionFeeLegs, \
                                    generateRepoLegs):
    startTime = time.time()
    acm.LogAll("Generating portfolio swap base legs batch (batch size: %s)"%str(len(batchIndex)))
    legs = []
    try:

        for index in batchIndex:
            acmSecurity = acm.FInstrument[aelSecurities[index].insid]
            securityLegs = GenerateSecurityBaseLegs(pfsParameters, \
                                                acmSecurity, \
                                                legStartDate, \
                                                legEndDate, \
                                                generateFinancingLegs, \
                                                generateExecutionFeeLegs, \
                                                generateRepoLegs)

            legs.append(securityLegs)
        pfsParameters.portfolioSwap.Legs().Commit()
    except Exception, e:
        acm.Log("Failed to generate base legs: %s"%str(e))
        raise e
    acm.Log("... Portfolio swap base legs batch generated in %s seconds"%str(time.time()-startTime))
    return legs
#----------------------------------------------------------------------------
def GeneratePortfolioSwapDividendLegsBatch(portfolioSwap, \
                                            returnLegIsPayLeg, \
                                            securityBaseLegs, \
                                            useSingleFinancingLeg, \
                                            periodStartDate):
    startTime = time.time()
    acm.LogAll("Generating portfolio swap dividend legs batch (batch size: %s)"%str(len(securityBaseLegs)))

    singleFinancingLeg = None
    if useSingleFinancingLeg:
        singleFinancingLeg = Util.GetSingleFinancingLeg(portfolioSwap, returnLegIsPayLeg, False)

    dividendLegs = []
    try:
        for securityBaseLegs in securityBaseLegs:
            returnLeg = Util.ReturnLegFromList(securityBaseLegs)
            financingLeg = singleFinancingLeg and singleFinancingLeg or \
                                Util.FinancingLegFromList(securityBaseLegs)
            
            if not financingLeg:
                raise Exception("Financing leg not found, could not generate dividend legs - Exits")
            
            dividendLegs.append(CreateDividendLegs(portfolioSwap, returnLeg, financingLeg))
        acm.Log("... Portfolio swap dividend legs batch generated in %s seconds" \
                %str(time.time()-startTime))
    except Exception, e:
        acm.Log("Failed to generate dividend legs: %s - Exits"%str(e))
        raise e
    return dividendLegs
#----------------------------------------------------------------------------
def CreateDividendLegs(portfolioSwap, \
                        returnLeg, \
                        financingLeg):
    dividendLegs = []
    legs = portfolioSwap.CreateDividendLegs(returnLeg, financingLeg)
    if 1 == legs.Size():
        dividendLegs.append(legs[0])
    elif legs.Size() > 1:
        raise Exception("Unhandled number of dividend legs for security: %s - Exits"%str(legs.Size()))
    return dividendLegs
#----------------------------------------------------------------------------
def GenerateSecurityBaseLegs(pfsParameters, \
                        security, \
                        legStartDate, \
                        legEndDate, \
                        generateFinancingLeg, \
                        generateExecutionFeeLeg, \
                        generateRepoLeg):
    
    returnLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                    "Total Return", \
                                    "Daily Return", \
                                    pfsParameters.returnLegIsPayLeg, \
                                    security, \
                                    legStartDate, \
                                    legEndDate, \
                                    0.0, \
                                    0.0, \
                                    pfsParameters.daycountMethod, \
                                    "Price",
                                    security)
    if generateFinancingLeg:
        financingLeg = Util.CreatePortfolioSwapLeg(pfsParameters.portfolioSwap, \
                                        "Float", \
                                        "Simple Overnight", \
                                        not pfsParameters.returnLegIsPayLeg, \
                                        security, \
                                        legStartDate, \
                                        legEndDate, \
                                        0.0, \
                                        0.0, \
                                        pfsParameters.daycountMethod, \
                                        "Position Total", \
                                        pfsParameters.floatRef)
    else:
        financingLeg = None
    
    if generateRepoLeg:
        repoLeg = CreateRepoLeg(pfsParameters, legStartDate, legEndDate, security)
    else:
        repoLeg = None

    if generateExecutionFeeLeg:
        executionFeeLeg = CreateExecutionFeeLeg(pfsParameters, legStartDate, legEndDate, security)
    else:
        executionFeeLeg = None
        
    return [returnLeg, financingLeg, repoLeg, executionFeeLeg]
#----------------------------------------------------------------------------
def GeneratePerSecurityCashFlowsBatch(batchIndex, \
                                        securityBatchBaseLegs, \
                                        pfsParameters, \
                                        cFStartDay, \
                                        cFEndDay, \
                                        openEndAdjustDates, \
                                        onlyAfterLegStartDate):

    calendar = pfsParameters.calendar
    paydayOffset = pfsParameters.paydayOffset
    paydayOffsetMethod = pfsParameters.paydayOffsetMethod

    startTime = time.time()
    acm.LogAll("Generating portfolio swap cash flows batch (batch size: %s)" \
                %str(len(securityBatchBaseLegs)))
    batchPerSecurityCashFlows = []
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            returnLeg, financingLeg, repoLeg, executionFeeLeg, dividendLegs = \
                                                    securityBatchBaseLegs[index]
            
            if onlyAfterLegStartDate and acm.Time.DateDifference(returnLeg.StartDate(), cFStartDay) > 0:
                continue
            
            returnCF = Util.CreatePortfolioSwapCashFlow(returnLeg, \
                                                    0.0, \
                                                    ReturnCashFlowType(pfsParameters), \
                                                    calendar, \
                                                    paydayOffset, \
                                                    paydayOffsetMethod, \
                                                    cFStartDay, \
                                                    cFEndDay, \
                                                    None, \
                                                    openEndAdjustDates, \
                                                    False)
            if financingLeg:
                financingCF = Util.CreatePortfolioSwapCashFlow(financingLeg, \
                                                                0.0, \
                                                                "Float Rate", \
                                                                calendar, \
                                                                paydayOffset, \
                                                                paydayOffsetMethod, \
                                                                cFStartDay, \
                                                                cFEndDay, \
                                                                None, \
                                                                openEndAdjustDates, \
                                                                False)
            else:
                financingCF = None
            if repoLeg:
                repoCF = Util.CreatePortfolioSwapCashFlow(repoLeg, \
                                                            0.0, \
                                                            "Float Rate", \
                                                            calendar, \
                                                            paydayOffset, \
                                                            paydayOffsetMethod, \
                                                            cFStartDay, \
                                                            cFEndDay, \
                                                            None, \
                                                            openEndAdjustDates, \
                                                            False)
            else:
                repoCF = None
            batchPerSecurityCashFlows.append((returnCF, financingCF, repoCF))
        acm.CommitTransaction()
    except Exception, e:
        acm.Log("Failed to generate cash flows: %s"%str(e))
        acm.AbortTransaction()
        raise e
    acm.Log("... Portfolio swap cash flows batch generated in %s seconds"%str(time.time()-startTime))
    return batchPerSecurityCashFlows
#----------------------------------------------------------------------------
def UpdateDividendLegs(pfsParameters, useSingleFinancingLeg):
    portfolioSwap = pfsParameters.portfolioSwap
    returnLegIsPayLeg = pfsParameters.returnLegIsPayLeg
    
    indexRefToLegsDict = Util.GetIndexRefToLegsDictionary(portfolioSwap, returnLegIsPayLeg, False)
    try:
        singleFinancingLeg = None
        if useSingleFinancingLeg:
            singleFinancingLeg = Util.GetSingleFinancingLeg(portfolioSwap, returnLegIsPayLeg, False)
    
        for securityLegs in indexRefToLegsDict.values():
            returnLeg = Util.ReturnLegFromList(securityLegs)
            financingLeg = singleFinancingLeg and singleFinancingLeg or \
                                        Util.FinancingLegFromList(securityLegs)

            if not financingLeg:
                raise Exception("No financing leg found, dividend leg update failed - Exits")
            
            dividendLegs = Util.DividendLegsFromList(securityLegs)
            if not dividendLegs:
                CreateDividendLegs(portfolioSwap, \
                                    returnLeg, \
                                    financingLeg)
    except Exception, e:
        acm.Log("Dividend leg update failed: %s - Exits"%str(e))
        raise e
#----------------------------------------------------------------------------
def FixSingleFinancingAmount(pfsParameters, \
                            perPortfolioData, \
                            date, \
                            includeExpiryDayFunding):
    
    periodStartDay = PeriodCashFlowStartDay(pfsParameters, date, True, False)
 
    financingCF = Util.GetSingleFinancingCashFlow(pfsParameters.portfolioSwap, \
                                                pfsParameters.returnLegIsPayLeg, \
                                                periodStartDay, \
                                                False)
    aelFinancingCF = ael.CashFlow[financingCF.Oid()]

    aelFollowingFinancingCF = None
    if IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, date):
        periodEndDay = PeriodCashFlowEndDay(pfsParameters, date, False)
        followingFinancingCF = Util.GetSingleFinancingCashFlow(pfsParameters.portfolioSwap, \
                                                                pfsParameters.returnLegIsPayLeg, \
                                                                periodEndDay, \
                                                                False)
        aelFollowingFinancingCF = ael.CashFlow[followingFinancingCF.Oid()]
        
    financingAmount = Util.GetValueConditionally(perPortfolioData, \
                                                ID_PER_PORTFOLIO_FUNDING_AMOUNT, \
                                                True)
    financingRate = Util.GetValueConditionally(perPortfolioData, \
                                                ID_PER_PORTFOLIO_FUNDING_RATE, \
                                                True)

    if aelFinancingCF and financingAmount:
        CreateFinancingResetsOnDate(aelFinancingCF, \
                                    aelFollowingFinancingCF, \
                                    financingAmount, \
                                    financingRate, \
                                    date, \
                                    pfsParameters, \
                                    includeExpiryDayFunding)
#----------------------------------------------------------------------------
def GenerateDailyPayments(  pfsParameters, \
                            fixingDate, \
                            perPortfolioData):
    
    portfolioSwap = pfsParameters.portfolioSwap
    returnLegIsPayLeg = pfsParameters.returnLegIsPayLeg
    
    payDate = Util.AdjustDateToOffsetMethod(portfolioSwap.ExpiryDate(), \
                                            pfsParameters.calendar, \
                                            pfsParameters.paydayOffset, \
                                            pfsParameters.paydayOffsetMethod)

    perPortfolioPayments = Util.GetValueConditionally(perPortfolioData, \
                                            ID_PER_PORTFOLIO_PAYMENTS, \
                                            False)

    isSwapStartDay = acm.Time.DateDifference(fixingDate, portfolioSwap.StartDate()) == 0

    for paymentType, payment in perPortfolioPayments.items():
        if GetConfigParameter("calculateDivUPL", pfsParameters.paramDict) and \
                paymentType == GetConfigParameter("divUPLPaymentType", pfsParameters.paramDict):

            portfolioDividendUPL = payment
            if returnLegIsPayLeg:
                portfolioDividendUPL = -portfolioDividendUPL
            portfolioSwapDividendUPL = GetPortfolioSwapDividendUPL(pfsParameters, fixingDate)
            GenerateDailyDeltaPayment(portfolioSwap, \
                                        portfolioSwapDividendUPL, \
                                        portfolioDividendUPL, \
                                        GetConfigParameter("divUPLPaymentType", pfsParameters.paramDict), \
                                        fixingDate, \
                                        payDate, \
                                        GetConfigParameter("divUPLPaymentType", pfsParameters.paramDict))

        elif 0.0 != payment:
            payment = returnLegIsPayLeg and -payment or payment
            if UsePerPortfolioRPL(pfsParameters) and \
                    paymentType == GetConfigParameter("RPLPaymentType", pfsParameters.paramDict):
                if not (pfsParameters.previousPfSwap and isSwapStartDay):
                    GenerateDailyPayment(portfolioSwap, \
                                        payment, \
                                        paymentType, \
                                        fixingDate, \
                                        payDate)
            else:
                GenerateDailyPayment(portfolioSwap, \
                                    payment, \
                                    paymentType, \
                                    fixingDate, \
                                    payDate)
#----------------------------------------------------------------------------
def ClearPerSecurityCashFlowsResets(perSecurityCashFlows, pfsParameters):
    cashFlows = [cF for securityCFs in perSecurityCashFlows for cF in securityCFs if None != cF]
    Util.ClearCashFlowsResets(cashFlows, GetConfigParameter("resetClearingBatchSize", pfsParameters.paramDict))
#----------------------------------------------------------------------------
def ClearPerPortfolioSwapCashFlowsResets(pfsParameters, \
                                        periodStartDate, \
                                        clearFinancingCashFlow, \
                                        clearRepoCashFlow):
    cashFlows = []
    if clearFinancingCashFlow:
        cashFlows.append(Util.GetSingleFinancingCashFlow(pfsParameters.portfolioSwap, \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDate, \
                                                        False))
    if clearRepoCashFlow:
        cashFlows.append(Util.GetSingleRepoCashFlow(pfsParameters.portfolioSwap, \
                                                    pfsParameters.returnLegIsPayLeg, \
                                                    periodStartDate, \
                                                    False))
    Util.ClearCashFlowsResets(cashFlows, GetConfigParameter("resetClearingBatchSize", pfsParameters.paramDict))
#----------------------------------------------------------------------------
def GenerateDailyPayment(portfolioSwap, \
                         paymentValue, \
                         payType, \
                         date, \
                         payDate):
    singleTrade = Util.GetSingleTrade(portfolioSwap)
    paymentValue = singleTrade.Quantity() > 0 and paymentValue or -paymentValue
    counterparty = singleTrade.Counterparty()
    acquirer = singleTrade.Acquirer()
    
    counterpartyAccount = counterparty and \
                        Util.GetPaymentAccount(counterparty, singleTrade.Currency()) or None
    acquirerAccount = acquirer and \
                        Util.GetPaymentAccount(acquirer, singleTrade.Currency()) or None

    if not counterpartyAccount:
        acm.Log("Failed to find counterparty payment account for trade: %s"%str(singleTrade.Oid()))
        raise Exception("Counterparty account not found")
    if not acquirerAccount:
        acm.Log("Failed to find acquirer payment account for trade: %s"%str(singleTrade.Oid()))
        raise Exception("Acquirer account not found")

    CreateDailyPayment(singleTrade, \
                        payType, \
                        paymentValue, \
                        date, \
                        payDate, \
                        counterpartyAccount, \
                        acquirerAccount)
#----------------------------------------------------------------------------       
def CreateDailyPayment(trade, \
                        payType, \
                        paymentValue, \
                        date, \
                        payDate, \
                        counterpartyAccount, \
                        ourAccount):  
    try:
        payment = acm.FPayment()
        payment.Trade = trade.Oid()
        payment.Type = payType
        payment.Amount = paymentValue
        payment.Currency = trade.Currency()
        payment.ValidFrom = date
        payment.PayDay = payDate
        payment.Account = counterpartyAccount
        payment.OurAccount = ourAccount
        payment.Party = trade.Counterparty()
        payment.Commit()
    except Exception, e:
        acm.Log("Failed to create payment: %s"%str(e))
        raise e 
#----------------------------------------------------------------------------
def SpreadAdjustFundingRates(aelSecurities, \
                            pfsParameters, \
                            perPortfolioData, \
                            perSecurityData):
    if UsePerPortfolioFunding(pfsParameters):
        fundingRate = Util.GetValueConditionally(perPortfolioData, \
                                                    ID_PER_PORTFOLIO_FUNDING_RATE, \
                                                    True)
        fundingAmount = Util.GetValueConditionally(perPortfolioData, \
                                                    ID_PER_PORTFOLIO_FUNDING_AMOUNT, \
                                                    True)
        fundingAmount = pfsParameters.returnLegIsPayLeg and -fundingAmount or fundingAmount
        perPortfolioData[ID_PER_PORTFOLIO_FUNDING_RATE] = SpreadAdjustOvernightRate(
                                                                    fundingAmount, \
                                                                    fundingRate, \
                                                                    pfsParameters.spreadShort, \
                                                                    pfsParameters.spreadLong)
    else:
        fundingRates = Util.GetValueConditionally(perSecurityData, \
                                                    ID_PER_SECURITY_FUNDING_RATE, \
                                                    True)
        positions = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_POSITION, \
                                                True)
        for index, fundingRate, position in zip(range(len(aelSecurities)), \
                                                fundingRates, \
                                                positions):
            fundingRates[index] = SpreadAdjustOvernightRate(position, \
                                                            fundingRate, \
                                                            pfsParameters.spreadShort, \
                                                            pfsParameters.spreadLong)
#----------------------------------------------------------------------------
def SpreadAdjustOvernightRate(  position, \
                                overnightRate, \
                                spreadShort, \
                                spreadLong):
    adjustedRate = overnightRate
    if position:
        if position > 0.0:
            if spreadLong:
                adjustedRate += spreadLong
        else:
            if spreadShort:
                adjustedRate -= spreadShort
    return adjustedRate
#----------------------------------------------------------------------------
def GenerateDailyDeltaPayment(portfolioSwap, \
                                previousAmount, \
                                newAmount, \
                                paymentType, \
                                date, \
                                payDate, \
                                divUPLPaymentType):

    deltaAmount = newAmount - previousAmount
    if not acm.Time.DateDifference(date, portfolioSwap.ExpiryDate()):
        if divUPLPaymentType == paymentType and previousAmount:
            GenerateDailyPayment(portfolioSwap, -previousAmount, paymentType, date, payDate)
    elif abs(deltaAmount) > 1e-9:
        GenerateDailyPayment(portfolioSwap, deltaAmount, paymentType, date, payDate)
#----------------------------------------------------------------------------
def GetPortfolioSwapDividendUPL(pfsParameters, fixingDate):
    singleTrade = Util.GetSingleTrade(pfsParameters.portfolioSwap)
    dividendUPL = 0.0
    
    globalSimulations = [(colIdPnLStartDate, "Custom"), \
                        (colIdPnLStartDateCustom, fixingDate)]
    dividendUPL = Util.CalculateSingleSheetValue( \
                                    "FPortfolioSheet", \
                                    singleTrade, \
                                    GetConfigParameter("colIdPortfolioSwapDivUPL", pfsParameters.paramDict), \
                                    1, \
                                    globalSimulations, \
                                    None).Number()
    if singleTrade.Quantity() < 0.0:
        dividendUPL = -dividendUPL
    return dividendUPL
#----------------------------------------------------------------------------
def ReturnCashFlowType(pfsParameters):
    if GetConfigParameter("fixTotalInvested", pfsParameters.paramDict):
        return "Position Total Return"
    return "Total Return"
#----------------------------------------------------------------------------
def ReturnFixingColumnId(pfsParameters):
    if GetConfigParameter("fixTotalInvested", pfsParameters.paramDict):
        return GetConfigParameter("colIdTotalInvested", pfsParameters.paramDict)
    return GetConfigParameter("colIdPosition", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def NonZeroColumnsIds(pfsParameters):
    configIds = list(GetConfigParameter("nonZeroColumnsIds", pfsParameters.paramDict))
    configIds.append(ReturnFixingColumnId(pfsParameters))
    return configIds
#----------------------------------------------------------------------------
def UsePerPortfolioFunding(pfsParameters):
    return True == GetConfigParameter("usePerPortfolioFunding", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UsePerPortfolioExecutionFee(pfsParameters):
    return True == GetConfigParameter("usePerPortfolioExecutionFee", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UsePerSecurityRepo(pfsParameters):
    return "Per Security" == GetConfigParameter("repoLegConfig", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UsePerPortfolioRepo(pfsParameters):
    return "Single" == GetConfigParameter("repoLegConfig", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UsePerPortfolioRPL(pfsParameters):
    return True == GetConfigParameter("usePerPortfolioRPL", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UseCallDepositLeg(pfsParameters):
    return True == GetConfigParameter("useCallDepositLeg", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UseDividendLegs(pfsParameters):
    return True == GetConfigParameter("generateDividendLegs", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def UseMarginLeg(pfsParameters):
    return True == GetConfigParameter("useMarginLeg", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def MonthEndAdjustFunding(pfsParameters):
    return True == GetConfigParameter("monthEndAdjustFunding", pfsParameters.paramDict)
#----------------------------------------------------------------------------
def GetConfigParameter(parameterName, parameterDictionary):
    parameter = None
    if parameterDictionary and parameterDictionary.has_key(parameterName):
        parameter = parameterDictionary[parameterName]
    else:
        parameter = getattr(Conf, parameterName)
    if None == parameter:
        raise Exception("Configuration parameter not found: " + parameterName)
    return parameter
#----------------------------------------------------------------------------
def UsesPayments(pfsParameters):
    return 0 != len(GetConfigParameter("paymentTypes", pfsParameters.paramDict))
#----------------------------------------------------------------------------
def AddPaymentType(addedType, pfsParameters, paymentTypeId):
    paymentTypes = GetConfigParameter("paymentTypes", pfsParameters.paramDict)
    if not addedType:
        raise Exception("No payment type specified: %s"%paymentTypeId)
    if not addedType in paymentTypes:
        paymentTypes.append(addedType)
#----------------------------------------------------------------------------
def AssertPaymentTypes(pfsParameters):
    if GetConfigParameter("usePerPortfolioRPL", pfsParameters.paramDict):
        AddPaymentType(GetConfigParameter("RPLPaymentType", pfsParameters.paramDict), pfsParameters, "RPLPaymentType")
    if GetConfigParameter("calculateDivUPL", pfsParameters.paramDict):
        AddPaymentType(GetConfigParameter("divUPLPaymentType", pfsParameters.paramDict), pfsParameters, "divUPLPaymentType")
    if UsesPayments(pfsParameters):
        Util.AssertPaymentTypes(GetConfigParameter("paymentTypes", pfsParameters.paramDict))
    
columnIds = []
if Conf.colIdDailyExecutionFee:
    columnIds.append(Conf.colIdDailyExecutionFee)
if Conf.calculateDivUPL and Conf.colIdPortfolioSwapDivUPL:
    columnIds.extend([Conf.colIdPortfolioDivUPL, Conf.colIdPortfolioSwapDivUPL])
Util.CheckColumnDefinitions(columnIds, \
                        acm.GetDefaultContext(), \
                        True)
