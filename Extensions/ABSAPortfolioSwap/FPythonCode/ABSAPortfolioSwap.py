"""-----------------------------------------------------------------------------
MODULE
    ABSAPortfolioSwap

    Created from FSEQPortfolioSwap

DESCRIPTION
    Institutional CFD Project

    Date                : 2010-10-23
    Purpose             : Functions that handle leg-, cash flow- and reset-generation for Portfolio Swaps.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2018-12-21 CHG1001240466 Tibor Reiss        Sweeping of dividend suppression
2019-08-05 FAU-324       Tibor Reiss        Adjust for Upgrade2018
2019-11-21 FAPE-147      Tibor Reiss        Propagate error
2020-01-29 FAPE-120      Tibor Reiss        Remove code for old funding method
-----------------------------------------------------------------------------"""
import time

import acm
import ael

import ABSAPortfolioSwapConfig as Conf
reload(Conf)
import ABSAPortfolioSwapUtil as Util
reload(Util)
if Conf.customValuationModuleName is not None:
    Custom = Util.ImportModuleByName(Conf.customValuationModuleName)
else:
    Custom = None
if Custom:
    reload(Custom)

from at_logging import getLogger
import PS_FundingCalculations
import FBDPCommon
from PS_FundingSweeper import sweep_zero_values
from at_time import acm_date


LOGGER = getLogger(__name__)
#----------------------------------------------------------------------------
ID_PER_PORTFOLIO_FUNDING_AMOUNT = "ID_PER_PORTFOLIO_FUNDING_AMOUNT"
ID_PER_PORTFOLIO_FUNDING_RATE = "ID_PER_PORTFOLIO_FUNDING_RATE"
ID_PER_PORTFOLIO_EXECUTION_FEE = "ID_PER_PORTFOLIO_EXECUTION_FEE"
ID_PER_PORTFOLIO_RPL = "ID_PER_PORTFOLIO_RPL"
ID_PER_SECURITY_POSITION = "ID_PER_SECURITY_POSITION"
ID_PER_SECURITY_INV_POSITION = "ID_PER_SECURITY_INV_POSITION"
ID_PER_SECURITY_RETURN_FIXING = "ID_PER_SECURITY_RETURN_FIXING"
ID_PER_SECURITY_FUNDING_RATE = "ID_PER_SECURITY_FUNDING_RATE"
ID_PER_SECURITY_FUNDING_AMOUNT = "ID_PER_SECURITY_FUNDING_AMOUNT"
ID_PER_SECURITY_EXECUTION_FEE = "ID_PER_SECURITY_EXECUTION_FEE"
ID_PER_SECURITY_DIVIDEND_SUPPRESSION = "ID_PER_SECURITY_DIVIDEND_SUPPRESSION"
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
        if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
            if IsRollingDay(pfsParameters, fixingDate):
                PortfolioSwapExtendOpenEnd(pfsParameters, fixingDate, adjustToPeriodEndDay, True)
                acm.PollDbEvents()  # Let the end return resets update
                FixEndTotalReturnResets(pfsParameters, fixingDate, adjustToPeriodEndDay)
                RollPortfolioSwap(pfsParameters, fixingDate)
            else:
                PortfolioSwapExtendOpenEnd(pfsParameters, fixingDate, False, False)
                ael.poll()  # Let the cash flow dates update

        elif not acm.Time.DateDifference(fixingDate, pfsParameters.portfolioSwap.ExpiryDate()) or \
                adjustToPeriodEndDay:
            FixEndTotalReturnResets(pfsParameters, fixingDate, adjustToPeriodEndDay)

        if UseDividendLegs():
            UpdateDividendLegs(pfsParameters, UsePerPortfolioFunding())

        # The redemption cash flow must be prolonged before calculating the call deposit cash
        # to get the correct net amount
        if UseCallDepositLeg():
            SetCallAccountEndDate(pfsParameters.portfolioSwap,
                                    pfsParameters.calendar.AdjustBankingDays(fixingDate, 1))
        PerformDailyFixing(pfsParameters, fixingDate)

        ael.poll()  # Needed to get correct resets
        sweep_zero_values(pfsParameters.portfolioSwap, acm_date(fixingDate), "Float", "Funding")


        fixingDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, 1)
        fixingDate = acm.Time.DateDifference(fixingDate, resetEndDate) <= 0 and fixingDate or None

#----------------------------------------------------------------------------
def IsPeriodCashFlowEndDay(pfsParameters, date):
    return Util.IsPeriodEndDay(pfsParameters.portfolioSwap, \
                            pfsParameters.rollingBaseDay, \
                            pfsParameters.isFixPeriod, \
                            date, \
                            pfsParameters.calendar, \
                            False)
#----------------------------------------------------------------------------
def IsOpenEndRollingPeriodEndDay(pfsParameters, date):
    return "Open End" == pfsParameters.portfolioSwap.OpenEnd() and \
        IsPeriodCashFlowEndDay(pfsParameters, date) and \
        acm.Time.DateDifference(pfsParameters.portfolioSwap.StartDate(), date)
#----------------------------------------------------------------------------
def IsRollingDay(pfsParameters, fixingDate):
    result = False
    isPeriodEndDay = IsPeriodCashFlowEndDay(pfsParameters, fixingDate)
    if isPeriodEndDay and acm.Time.DateDifference(fixingDate, pfsParameters.portfolioSwap.StartDate()):
        result = True
    elif IsBankingDayBeforePeriodEndDay(pfsParameters, fixingDate):
        result = True
    return result
#----------------------------------------------------------------------------
def IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, fixingDate):
    return "Open End" == pfsParameters.portfolioSwap.OpenEnd() and \
        IsBankingDayBeforePeriodEndDay(pfsParameters, fixingDate)
#----------------------------------------------------------------------------
def PeriodCashFlowStartDay(pfsParameters, date, closedPeriod, isAel, aelPortfolioSwap=None):
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

#----------------------------------------------------------------------------
# AR636875 - Date conversion issue when running the Generate Portfolio Swap script from the Server
# Workaround with ael
#----------------------------------------------------------------------------
def RestorePortfolioSwapEndDate(pfsParameters, resetEndDate):
    periodEndDay = PeriodCashFlowEndDay(pfsParameters, \
                                        pfsParameters.calendar.AdjustBankingDays(\
                                            pfsParameters.portfolioSwap.StartDate(), \
                                            1), \
                                        False)
    pfsName = pfsParameters.portfolioSwap.Name()
    aelSwap = ael.Instrument[pfsName]

    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        endDate = PeriodCashFlowEndDay(pfsParameters, acm.Time.DateAddDelta(resetEndDate, 0, 0, 1), False)
        # pfsParameters.portfolioSwap.ExpiryDate = endDate
        # pfsParameters.portfolioSwap.Commit()
        aelSwap = aelSwap.clone()
        aelSwap.exp_day = ael.date(endDate)
        aelSwap.exp_time = 0
        aelSwap.commit()
        ael.poll()
        UpdatePortfolioSwapLegsEndDates(pfsParameters.portfolioSwap, \
                                        pfsParameters.returnLegIsPayLeg, \
                                        endDate)

#----------------------------------------------------------------------------
# Add legs and cash flows to represent any new positions in the portfolio.
#----------------------------------------------------------------------------
def AddNewLegs(pfsParameters, \
                resetStartDate, \
                resetEndDate):

    newAELSecurities = Util.GetNewAelSecurities(\
                                        pfsParameters.portfolioSwap, \
                                        pfsParameters.portfolioSwap.FundPortfolio(), \
                                        pfsParameters.returnLegIsPayLeg)

    (legStartDate, legEndDate) = GetLegStartAndEndDate(pfsParameters, \
                                                        resetStartDate, \
                                                        resetEndDate)

    baseLegs = GeneratePerSecurityLegs(pfsParameters, \
                                        newAELSecurities, \
                                        legStartDate, \
                                        legEndDate, \
                                        not UsePerPortfolioFunding(), \
                                        not UsePerPortfolioExecutionFee(), \
                                        UsePerSecurityRepo(), \
                                        UseDividendLegs())

    # The rolling procedure creates cash flows for the new period
    isOpenEnd = "Open End" == pfsParameters.portfolioSwap.OpenEnd()
    if isOpenEnd:
        cashFlowEndDate = resetEndDate
    else:
        cashFlowEndDate = legEndDate

    if not (isOpenEnd and IsRollingDay(pfsParameters, resetStartDate)):
        perSecurityCashFlows = GeneratePerSecurityCashFlows(pfsParameters, \
                                                            baseLegs, \
                                                            legStartDate, \
                                                            cashFlowEndDate, \
                                                            False)
        acm.PollDbEvents()  # In order for the automatically created resets to show up in ACM
        ClearPerSecurityCashFlowsResets(perSecurityCashFlows)
        GenerateInitialResets(perSecurityCashFlows, pfsParameters, resetStartDate)

#----------------------------------------------------------------------------
def TransferPreviousPortfolioSwapData(pfsParameters, startDate):
    portfolioSwap = pfsParameters.portfolioSwap
    previousPfSwap = pfsParameters.previousPfSwap

    # Get the daily cash (the call account net of the previous portfolio swap and add
    # it to the account of the current swap.
    if UseCallDepositLeg():
        previousPfSwapData = CalculatePortfolioSwapFixingData(previousPfSwap, startDate, True)
        startDayCash = -1.0 * Util.GetValueConditionally(previousPfSwapData, \
                                                ID_PORTFOLIO_SWAP_DAILY_CASH, \
                                                True)

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
    if UseCallDepositLeg():
        CloseCallDeposit(portfolioSwap, calendar, terminationDate)

    portfolioSwap.ExpiryDate(terminationDate)
    for leg in portfolioSwap.Legs():
        leg.EndDate(terminationDate)
    portfolioSwap.OpenEnd("Terminated")
    portfolioSwap.Commit()
#----------------------------------------------------------------------------
# On termination - Close out all accumulated cash in the call deposit leg.
# First calculate the cash that is paid on the termination date (ex. funding),
# then close out the net of the account. The total cash generated will be the
# daily cash of the swap on the termination date.
#----------------------------------------------------------------------------
def CloseCallDeposit(portfolioSwap, calendar, terminationDate):

    SetCallAccountEndDate(portfolioSwap, calendar.AdjustBankingDays(terminationDate, 1))
    portfolioSwapData = CalculatePortfolioSwapFixingData(portfolioSwap, terminationDate)
    portfolioSwapDepositAmount = Util.GetValueConditionally(portfolioSwapData, \
                                            ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT, \
                                            True)

    callDepositLeg = Util.GetCallDepositLeg(portfolioSwap, False)
    Util.CreatePortfolioSwapCashFlow(callDepositLeg, \
                                    portfolioSwapDepositAmount, \
                                    "Fixed Amount", \
                                    None, \
                                    None, \
                                    None, \
                                    None, \
                                    None, \
                                    terminationDate, \
                                    False, \
                                    False)

    SetCallAccountEndDate(portfolioSwap, terminationDate)
    portfolioSwapData = CalculatePortfolioSwapFixingData(portfolioSwap, terminationDate, True)
    lastDayCash = Util.GetValueConditionally(portfolioSwapData, \
                                            ID_PORTFOLIO_SWAP_DAILY_CASH, \
                                            True)

    Util.CreatePortfolioSwapCashFlow(callDepositLeg, \
                                    lastDayCash, \
                                    "Fixed Amount", \
                                    None, \
                                    None, \
                                    None, \
                                    None, \
                                    None, \
                                    terminationDate, \
                                    False, \
                                    False)
#----------------------------------------------------------------------------
def RollPortfolioSwap(pfsParameters, fixingDate):
    newExpiryDate = PeriodCashFlowEndDay(pfsParameters, \
                                    pfsParameters.calendar.AdjustBankingDays(fixingDate, 1), \
                                    False)

    pfsParameters.portfolioSwap.ExpiryDate = newExpiryDate
    pfsParameters.portfolioSwap.Commit()

    UpdatePortfolioSwapLegsEndDates(pfsParameters.portfolioSwap, \
                                    pfsParameters.returnLegIsPayLeg, \
                                    newExpiryDate)

    cashFlowStartDay = PeriodCashFlowEndDay(pfsParameters, fixingDate, False)

    indexRefToLegsDict = Util.GetIndexRefToLegsDictionary(pfsParameters.portfolioSwap, \
                                                            pfsParameters.returnLegIsPayLeg, \
                                                            False)
    perSecurityCashFlows = GeneratePerSecurityCashFlows(pfsParameters, \
                                                        indexRefToLegsDict.values(), \
                                                        cashFlowStartDay, \
                                                        pfsParameters.portfolioSwap.ExpiryDate())

    acm.PollDbEvents()  # In order to find the new cash flows
    ClearPerSecurityCashFlowsResets(perSecurityCashFlows)

    GenerateInitialResets(perSecurityCashFlows, pfsParameters, fixingDate)

    GeneratePerPortfolioSwapCashFlows(pfsParameters, \
                                        cashFlowStartDay, \
                                        UsePerPortfolioFunding(), \
                                        UsePerPortfolioRepo(), \
                                        UseCallDepositLeg())

    acm.PollDbEvents()  # In order to find the new cash flows
    ClearPerPortfolioSwapCashFlowsResets(pfsParameters.portfolioSwap, \
                                        pfsParameters.returnLegIsPayLeg, \
                                        cashFlowStartDay, \
                                        UsePerPortfolioFunding(), \
                                        UsePerPortfolioRepo())
#----------------------------------------------------------------------------
def UpdatePortfolioSwapLegsEndDates(portfolioSwap, \
                                    returnLegIsPayLeg, \
                                    newLegEndDate):

    indexRefToLegsDict = Util.GetIndexRefToLegsDictionary(portfolioSwap, \
                                                            returnLegIsPayLeg, \
                                                            False)
    UpdatePerSecurityLegsEndDates(indexRefToLegsDict.values(), \
                            portfolioSwap, \
                            newLegEndDate)
    UpdatePerPortfolioSwapLegsEndDates(portfolioSwap, \
                            returnLegIsPayLeg, \
                            newLegEndDate, \
                            UsePerPortfolioFunding(), \
                            UsePerPortfolioRepo(), \
                            UseCallDepositLeg(), \
                            UseMarginLeg())
#----------------------------------------------------------------------------
def UpdatePerSecurityLegsEndDates(perSecurityLegs, portfolioSwap, newLegEndDate):
    legsFlattened = [leg for leg in Util.IterFlattenRemoveNone(perSecurityLegs)]
    batchIndexArray = Util.GetBatchIndices(len(legsFlattened), Conf.legBatchSize)
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
    LOGGER.info("Updating legs batch end dates (batch size: %s)...", len(batchIndex))
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            legs[index].EndDate = newEndDay
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to update legs batch end dates.")
        raise
    LOGGER.info("... Legs batch updated in %s seconds.", time.time() - startTime)
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
    aelLegsAndCashFlowsClones = Util.GetAelBaseLegsAndCashFlowsClonesPerSecurity(\
                                                    aelPortfolioSwap, \
                                                    UsePerPortfolioFunding(), \
                                                    ReturnCashFlowType(), \
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
                                    pfsParameters.calendar, \
                                    adjustToPeriodEndDay, \
                                    PeriodCashFlowEndDay(pfsParameters, fixingDate, False))
#----------------------------------------------------------------------------
def UpdatePerSecurityCashFlowsOpenEnd(aelPortfolioSwap, \
                                        aelLegsAndCashFlowsClones, \
                                        cashFlowEndDate, \
                                        cashFlowPayDate, \
                                        pfsParameters):

    batchIndexArray = Util.GetBatchIndices(len(aelLegsAndCashFlowsClones), Conf.legBatchSize / 3)
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
    LOGGER.info("Updating cash flow batch open end (batch size: %s)...", len(batchIndex))
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
    except:
        LOGGER.warning("WARNING: Failed to update open ended cash flows.")
        ael.abort_transaction()
    LOGGER.info("... Cash flow batch open end update finished in %s seconds.", time.time() - startTime)
#----------------------------------------------------------------------------
def UpdatePerPortfolioSwapCashFlowsOpenEnd(pfsParameters, fixingDate, cashFlowEndDate, cashFlowPayDate):

    aelPortfolioSwap = ael.Instrument[pfsParameters.portfolioSwap.Oid()]

    periodStartDate = PeriodCashFlowStartDay(pfsParameters, fixingDate, False, True, aelPortfolioSwap)
    aelPerPortfolioLegs = Util.GetPerPortfolioSwapLegs(aelPortfolioSwap, \
                                                    pfsParameters.returnLegIsPayLeg, \
                                                    UsePerPortfolioFunding(), \
                                                    UsePerPortfolioRepo(), \
                                                    UseCallDepositLeg())

    if UsePerPortfolioFunding():
        aelFinancingLeg = Util.FinancingLegFromList(aelPerPortfolioLegs)
        aelFinancingLegClone = aelFinancingLeg.clone()
        aelFinancingCF = Util.GetSingleFinancingCashFlowFromLeg(aelFinancingLegClone, periodStartDate)
        aelFinancingCF.end_day = ael.date(cashFlowEndDate)
        aelFinancingCF.pay_day = ael.date(cashFlowPayDate)
        aelFinancingLegClone.commit()

    if UsePerPortfolioRepo():
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
    LOGGER.info("Performing daily fixing for date %s ...", date)
    aelPortfolioSwap = ael.Instrument[pfsParameters.portfolioSwap.Name()]

    #MKLIMKE Add Portfolio Swap as Parameter----------------------------------------------------------------------------
    (aelSecurities, perSecurityData, perPortfolioData) = GetPortfolioFixingData(aelPortfolioSwap,
                                                            pfsParameters.portfolioSwap.FundPortfolio(),
                                                            date,
                                                            pfsParameters.floatRef,
                                                            pfsParameters.returnLegIsPayLeg,
                                                            pfsParameters.calendar)
    #-------------------------------------------------------------------------------------------------------------------
    if len(aelSecurities):
        portfolioSwapData = CalculatePortfolioSwapFixingData(pfsParameters.portfolioSwap, date)
        SpreadAdjustFundingRates(aelSecurities,
                                pfsParameters,
                                perPortfolioData,
                                perSecurityData)
        GeneratePerSecurityResets(aelPortfolioSwap, aelSecurities, pfsParameters, perSecurityData, date)
        GenerateDailyCashFlows(aelPortfolioSwap,\
                                aelSecurities,
                                perSecurityData,
                                perPortfolioData,
                                portfolioSwapData,
                                date,
                                pfsParameters)
        if UsePerPortfolioFunding():
            FixSingleFinancingAmount(pfsParameters, perPortfolioData, date, Conf.includeExpiryDayFunding)
        GenerateDailyPayments(pfsParameters, date, perPortfolioData)

    LOGGER.info("... Daily fixing for date %s finished in %s seconds.", date, time.time() - startTime)
#----------------------------------------------------------------------------
def GenerateInitialResets(perSecurityCashFlows, pfsParameters, fixingDate):
    if len(perSecurityCashFlows):
        if "Open End" != pfsParameters.portfolioSwap.OpenEnd():
            fixingDate = pfsParameters.portfolioSwap.ExpiryDate()
    batchIndexArray = Util.GetBatchIndices(len(perSecurityCashFlows), Conf.resetBatchSize)
    for batchIndex in batchIndexArray:
        GenerateSecurityBatchInitialResets(batchIndex, \
                                            perSecurityCashFlows, \
                                            pfsParameters.calendar, \
                                            fixingDate)
#----------------------------------------------------------------------------
def GenerateSecurityBatchInitialResets(batchIndex, \
                                        cashFlowsPerSecurity, \
                                        calendar, \
                                        endResetDate):

    startTime = time.time()
    LOGGER.info("Generating security initial resets batch (batch size: %s)...", len(batchIndex))
    try:
        ael.begin_transaction()
        for index in batchIndex:
            returnCF = Util.ReturnCashFlowFromList(cashFlowsPerSecurity[index])
            CreateEndReturnReset(ael.CashFlow[returnCF.Oid()], calendar, endResetDate)
        ael.commit_transaction()
    except Exception:
        ael.abort_transaction()
        LOGGER.exception("Failed to generate initial resets.")
        raise
    LOGGER.info("... Security initial resets batch generated in %s seconds", time.time() - startTime)
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
                                                not UsePerPortfolioFunding())

    financingRates = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_FUNDING_RATE, \
                                                not UsePerPortfolioFunding())

    repoAmounts = Util.GetValueConditionally(perSecurityData, \
                                            ID_PER_SECURITY_REPO_AMOUNT, \
                                            UsePerSecurityRepo())

    repoFinancingRates = Util.GetValueConditionally(perSecurityData, \
                                                ID_PER_SECURITY_REPO_FINANCING_RATE, \
                                                UsePerSecurityRepo())

    startTime = time.time()
    LOGGER.info("Generating security daily resets batch (batch size: %s)...", len(batchIndex))
    try:
        ael.begin_transaction()
        for index in batchIndex:
            CreateSecurityResetsOnDate(aelCashFlowsPerSecurity[index], \
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
    except Exception:
        ael.abort_transaction()
        LOGGER.exception("Failed to generate resets batch.")
        raise
    LOGGER.info("... Security daily resets batch generated in %s seconds", time.time() - startTime)
#----------------------------------------------------------------------------
def GeneratePerSecurityResets(aelPortfolioSwap, \
                                aelSecurities, \
                                pfsParameters, \
                                perSecurityData, \
                                fixingDate):
    periodStartDay = PeriodCashFlowStartDay(pfsParameters, fixingDate, False, True, aelPortfolioSwap)
    aelCashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(aelPortfolioSwap, \
                                                        ReturnCashFlowType(), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay, \
                                                        aelSecurities)

    aelFollowingPeriodCashFlowsPerSecurity = None
    if IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, fixingDate) or \
            IsOpenEndRollingPeriodEndDay(pfsParameters, fixingDate):
        periodEndDay = PeriodCashFlowEndDay(pfsParameters, fixingDate, False)
        aelFollowingPeriodCashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(aelPortfolioSwap, \
                                                        ReturnCashFlowType(), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodEndDay, \
                                                        aelSecurities)
        if not len(aelFollowingPeriodCashFlowsPerSecurity) == len(aelCashFlowsPerSecurity):
            raise Exception("Number of cash flows mis-match - Exits")

    batchIndexArray = Util.GetBatchIndices(len(aelSecurities), Conf.resetBatchSize)
    for batchIndex in batchIndexArray:
        GenerateSecurityBatchResets(batchIndex, \
                                    aelCashFlowsPerSecurity, \
                                    aelFollowingPeriodCashFlowsPerSecurity, \
                                    perSecurityData, \
                                    fixingDate, \
                                    pfsParameters, \
                                    Conf.includeExpiryDayFunding, \
                                    "Open End" == pfsParameters.portfolioSwap.OpenEnd())
#----------------------------------------------------------------------------
def GenerateDailyCashFlows(aelPortfolioSwap,
                            aelSecurities,
                            perSecurityData,
                            perPortfolioData,
                            perPortfolioSwapData,
                            fixingDate,
                            pfsParameters):

    calendar = pfsParameters.calendar
    returnLegIsPayLeg = pfsParameters.returnLegIsPayLeg

    if not UsePerPortfolioExecutionFee():
        executionFees = Util.GetValueConditionally(perSecurityData,
                                                ID_PER_SECURITY_EXECUTION_FEE,
                                                True)
        aelExecutionFeeLegs = Util.GetExecutionFeeLegs(aelPortfolioSwap, returnLegIsPayLeg, aelSecurities)
        batchIndexArray = Util.GetBatchIndices(len(aelSecurities), Conf.cashFlowBatchSize)
        for batchIndex in batchIndexArray:
            GenerateExecutionFeeCashFlowsBatch(batchIndex,
                                                aelSecurities,
                                                aelExecutionFeeLegs,
                                                executionFees,
                                                fixingDate,
                                                pfsParameters)

    if UseDividendLegs():
        inventoryPositions = Util.GetValueConditionally(perSecurityData, ID_PER_SECURITY_INV_POSITION, True)
        dividendSuppressions = Util.GetValueConditionally(perSecurityData, ID_PER_SECURITY_DIVIDEND_SUPPRESSION, True)
        portfolioSwap = acm.FPortfolioSwap[aelPortfolioSwap.insaddr]
        aelDividendLegsPerSecurity = Util.GetDividendLegs(aelPortfolioSwap, returnLegIsPayLeg, aelSecurities)
        batchIndexArray = Util.GetBatchIndices(len(aelDividendLegsPerSecurity), Conf.cashFlowBatchSize)
        for batchIndex in batchIndexArray:
            GenerateDividendCashFlowsBatch(batchIndex,
                                           aelSecurities,
                                           aelDividendLegsPerSecurity,
                                           inventoryPositions,
                                           dividendSuppressions,
                                           fixingDate)

    if UseCallDepositLeg():
        callDepositAmount = Util.GetValueConditionally(perPortfolioSwapData,
                                                        ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT,
                                                        True)
        if abs(callDepositAmount) > Conf.cashFlowEpsilon:
            aelCallDepositLeg = Util.GetCallDepositLeg(aelPortfolioSwap)
            Util.CreatePortfolioSwapCashFlow(aelCallDepositLeg,
                                             callDepositAmount,
                                             "Fixed Amount",
                                             None,
                                             None,
                                             None,
                                             None,
                                             None,
                                             fixingDate,
                                             False)
#----------------------------------------------------------------------------
# MKLIMKE Change Payday in Execution Fee to Equal Fixing Date Rather then Adjust for Spot Days Offset
# WWW
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

                payDay = Util.AdjustDateToOffsetMethod(fixingDate, \
                                                        pfsParameters.calendar, \
                                                        Util.DayOffsetToDatePeriod(\
                                                            aelSecurity.spot_banking_days_offset), \
                                                        pfsParameters.paydayOffsetMethod)


                #MKLIMKE---------------------------------------------------------------------------
                if acm.Time.DateDifference(pfsParameters.portfolioSwap.StartDate(), fixingDate) == 0:

                    Util.CreatePortfolioSwapCashFlow(aelExecutionFeeLegs[index], \
                                                    executionFees[index], \
                                                    "Fixed Amount", \
                                                    None, \
                                                    None, \
                                                    None, \
                                                    None, \
                                                    None, \
                                                    fixingDate, \
                                                    False)
                else:
                    Util.CreatePortfolioSwapCashFlow(aelExecutionFeeLegs[index], \
                                                    executionFees[index], \
                                                    "Fixed Amount", \
                                                    None, \
                                                    None, \
                                                    None, \
                                                    fixingDate, \
                                                    fixingDate, \
                                                    fixingDate, \
                                                    False)
                #---------------------------------------------------------------------------------

        ael.commit_transaction()
    except Exception:
        ael.abort_transaction()
        LOGGER.exception("Failed to generate execution fee cash flows batch.")
        raise
#----------------------------------------------------------------------------
def GenerateDividendCashFlowsBatch(batchIndex,
                                   aelSecurities,
                                   aelDividendLegsPerSecurity,
                                   inventoryPositions,
                                   dividendSuppressions,
                                   fixingDate):

    try:
        ael.begin_transaction()
        for index in batchIndex:
            dividendLegs = aelDividendLegsPerSecurity[index]
            if dividendLegs:
                aelSecurity = aelSecurities[index]
                inventoryPosition = inventoryPositions[index]
                dividendSuppression = dividendSuppressions[index]
                for leg in dividendLegs:
                    if dividendSuppression:
                        Util.CreatePortfolioSwapCashFlow(leg,
                                                         dividendSuppression,
                                                         "Dividend",
                                                         None,
                                                         None,
                                                         None,
                                                         str(fixingDate),
                                                         str(fixingDate),
                                                         str(fixingDate),
                                                         False)
                        LOGGER.info("Dividend suppression cash flow created for %s.", leg.index_ref.insid)
                    aelCashFlowDividends = [d for d in aelSecurity.dividends() \
                                            if d.ex_div_day == ael.date(fixingDate) and
                                            d.curr == leg.curr]
                    for aelDividend in aelCashFlowDividends:
                        if inventoryPosition:
                            CreatePortfolioSwapDividendCashFlow(leg, \
                                                                aelDividend, \
                                                                inventoryPosition)
        ael.commit_transaction()
    except Exception:
        ael.abort_transaction()
        LOGGER.exception("Failed to generate dividend cash flows batch.")
        raise
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
def CreateSecurityResetsOnDate(aelSecurityCashFlows, \
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

    aelTotalReturnCF = Util.ReturnCashFlowFromList(aelSecurityCashFlows)
    if aelTotalReturnCF and \
        acm.Time.DateDifference(PeriodCashFlowEndDay(pfsParameters, date, False), date) > 0 or \
            not acm.Time.DateDifference(date, pfsParameters.portfolioSwap.StartDate()):
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
        if not aelFollowingTotalReturnCF:
            raise Exception("Following period total return cash flow not found - Exits")
        CreateReturnResetsOnDate(pfsParameters, \
                        aelFollowingTotalReturnCF, \
                        date, \
                        True, \
                        returnFixingValue, \
                        position)

    aelFinancingCF = Util.FundingCashFlowFromList(aelSecurityCashFlows)
    aelFollowingFinancingCF = aelSecurityFollowingPeriodCashFlows and \
                Util.FundingCashFlowFromList(aelSecurityFollowingPeriodCashFlows) or None
    if aelFinancingCF and financingAmount:
        CreateFinancingResetsOnDate(aelFinancingCF, \
                                    aelFollowingFinancingCF, \
                                    financingAmount, \
                                    financingRate, \
                                    date, \
                                    pfsParameters, \
                                    includeExpiryDayFunding)

    aelRepoCF = Util.RepoCashFlowFromList(aelSecurityCashFlows)
    aelFollowingRepoCF = aelSecurityFollowingPeriodCashFlows and \
                Util.RepoCashFlowFromList(aelSecurityFollowingPeriodCashFlows) or None
    if aelRepoCF and repoAmount:
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
                            Util.IsPreviousFixingZero(aelReturnCF, date, "Nominal Scaling")
    if position or (not position and createZeroReturnReset):
        Util.CreateReset(aelReturnCF, "Return", date, date, endDate, returnFixingValue)
        Util.CreateReset(aelReturnCF, "Nominal Scaling", date, date, endDate, position)
#----------------------------------------------------------------------------
def CreateFinancingResetsOnDate(aelFinancingCF,
                                aelFollowingPeriodFinancingCF,
                                financingAmount,
                                financingRate,
                                date,
                                pfsParameters,
                                includeExpiryDayFunding):

    cashFlowStartDate = str(aelFinancingCF.start_day)
    cashFlowEndDate = str(aelFinancingCF.end_day)

    excludeLastDayFunding = not acm.Time.DateDifference(date, pfsParameters.portfolioSwap.ExpiryDate()) and \
                                    not includeExpiryDayFunding
    excludeFirstDayFunding = not acm.Time.DateDifference(date, cashFlowStartDate) and \
                                    includeExpiryDayFunding and None != pfsParameters.previousPfSwap

    if acm.Time.DateDifference(date, cashFlowEndDate) <= 0 and \
            not excludeLastDayFunding and \
            not excludeFirstDayFunding:

        (fixingDate, fundingStartDate, fundingEndDate) = \
            GetPeriodAdjustedFundingResetDates(date,
                                               cashFlowStartDate,
                                               cashFlowEndDate,
                                               pfsParameters)

        CreateResetsOnCashFlow(aelFinancingCF, date, fixingDate, fundingStartDate,
                               fundingEndDate, financingAmount, financingRate)

        if IsFollowingOpenEndPeriodAdjustmentNeeded(pfsParameters, date):
            if not aelFollowingPeriodFinancingCF:
                raise Exception("Following period cash flow not found - Exits")

            fundingStartDate = fundingEndDate
            fundingEndDate = pfsParameters.calendar.ModifyDate(None, None, fundingStartDate)

            CreateResetsOnCashFlow(aelFollowingPeriodFinancingCF, date, fixingDate,
                                   fundingStartDate, fundingEndDate, financingAmount,
                                   financingRate)
#----------------------------------------------------------------------------
def CreateResetsOnCashFlow(cashFlow, date, fixingDate, fundingStartDate, fundingEndDate, financingAmount, financingRate):
    prevReset = PS_FundingCalculations.GetReset(FBDPCommon.ael_to_acm(cashFlow),
                                                'Return',
                                                acm.Time().DateAddDelta(date, 0, 0, 0),
                                                False, True)
    prevResetValue = 0.0
    if prevReset:
        prevResetValue = prevReset.FixingValue()
    Util.CreateReset(cashFlow,
                     'Return',
                     ael.date(fixingDate),
                     ael.date(fundingStartDate),
                     ael.date(fundingEndDate),
                     prevResetValue + financingAmount * acm.Time.DateDifference(fundingEndDate, fundingStartDate) * financingRate / PS_FundingCalculations.DAYS_PERCENT)
#----------------------------------------------------------------------------
# MKLIMKE TTT
#----------------------------------------------------------------------------
def GetPeriodAdjustedFundingResetDates(date, \
                                        cashFlowStartDate, \
                                        cashFlowEndDate, \
                                        pfsParameters):

    fundingStartDate = date

    if IsBankingDayBeforePeriodEndDay(pfsParameters, date):  # NEED to check this???
        fundingEndDate = PeriodCashFlowEndDay(pfsParameters, date, False)

    else:
        # MKLIMKE old code simply adjusted to next working day...
        fundingEndDate = acm.Time.DateAddDelta(date, 0, 0, 1)
        PreviousBusinessDay = pfsParameters.calendar.AdjustBankingDays(date , -1)
        fundingStartDate = acm.Time.DateAddDelta(PreviousBusinessDay, 0, 0, 1)


    if MonthEndAdjustFunding():

        followingBankingDay = pfsParameters.calendar.AdjustBankingDays(date, 1)

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
    LOGGER.info("Fixing total return end resets ...")
    periodStartDay = PeriodCashFlowStartDay(pfsParameters, endDate, False, False)
    cashFlowsPerSecurity = Util.GetCashFlowsPerSecurity(pfsParameters.portfolioSwap, \
                                                        ReturnCashFlowType(), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay,
                                                        None, \
                                                        False)

    returnCashFlows = [Util.ReturnCashFlowFromList(cfs) for cfs in cashFlowsPerSecurity]

    if len(returnCashFlows):
        endDate = adjustToPeriodEndDay and PeriodCashFlowEndDay(pfsParameters, endDate, False) or endDate
        endReturnResets = GetEndReturnResets(returnCashFlows, endDate, None, False)


        batchIndexArray = Util.GetBatchIndices(len(endReturnResets), Conf.resetBatchSize)
        for batchIndex in batchIndexArray:
            FixEndTotalReturnResetsBatch(endReturnResets, endDate, batchIndex)
    LOGGER.info("... Total return end resets fixed in %s seconds", time.time() - startTime)
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
                    returnReset.ReadTime = acm.FDateTime(endDate)
                    returnReset.Commit()
                else:
                    errMess = "Failed to fix end day return reset for security '%s'" \
                                % returnReset.CashFlow().Leg().IndexRef().Name()
                    LOGGER.error(errMess)
                    raise Exception(errMess)
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
                                                        ReturnCashFlowType(), \
                                                        pfsParameters.returnLegIsPayLeg, \
                                                        periodStartDay, \
                                                        None, \
                                                        False)

    returnCashFlows = [Util.ReturnCashFlowFromList(baseCFList) for baseCFList in cashFlowsPerSecurity]
    newFixingDate = pfsParameters.calendar.AdjustBankingDays(fixingDate, 1)
    endReturnResets = GetEndReturnResets(returnCashFlows, fixingDate, newFixingDate, False)
    return endReturnResets and True or False
#----------------------------------------------------------------------------
def AdjustEndReturnResetsOpenEnd(aelReturnCashFlowsClones, \
                                fixingDate, \
                                calendar, \
                                adjustToPeriodEndDay, \
                                periodEndDay):
    startTime = time.time()
    LOGGER.info("Extending end total return resets open end...")
    newFixingDate = calendar.AdjustBankingDays(fixingDate, 1)
    newEndDate = calendar.AdjustBankingDays(newFixingDate, 1)
    aelEndReturnResetsClones = GetEndReturnResets(aelReturnCashFlowsClones, fixingDate, newFixingDate)
    if not aelEndReturnResetsClones:
        errMess = "ERROR: Could not adjust end return resets from date %s - Exits" % fixingDate
        LOGGER.error(errMess)
        raise Exception(errMess)

    if adjustToPeriodEndDay:
        newFixingDate = periodEndDay
        newEndDate = calendar.AdjustBankingDays(periodEndDay, 1)

    aelCashFlowsAndResetsClones = list(zip(aelReturnCashFlowsClones, aelEndReturnResetsClones))
    batchIndexArray = Util.GetBatchIndices(len(aelCashFlowsAndResetsClones), Conf.cashFlowBatchSize)
    for batchIndex in batchIndexArray:
        AdjustEndReturnResetsOpenEndBatch(batchIndex, \
                                            aelCashFlowsAndResetsClones, \
                                            newFixingDate, \
                                            newEndDate)
    LOGGER.info("... End return resets extended in %s seconds", time.time() - startTime)
#----------------------------------------------------------------------------
def GetEndReturnResets(returnCashFlows, fixingDate, newFixingDate=None, isAel=True):
    endReturnResets = []
    if newFixingDate:
        endReturnResets = Util.GetResetsOfTypeAtDate(returnCashFlows, "Return", newFixingDate, isAel)
    if not endReturnResets:
        endReturnResets = Util.GetResetsOfTypeAtDate(returnCashFlows, "Return", fixingDate, isAel)
    if not endReturnResets:
        LOGGER.error("End return resets not found for fixing date %s", fixingDate)
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
    except Exception:
        ael.abort_transaction()
        raise
#----------------------------------------------------------------------------
def ClearCashFlowsFromDateUntilEnd(pfsParameters, fromDate):
    portfolioSwap = pfsParameters.portfolioSwap
    if not acm.Time.DateDifference(fromDate, portfolioSwap.StartDate()) or \
        ("Open End" == portfolioSwap.OpenEnd() and \
            not acm.Time.DateDifference(fromDate, \
                                    PeriodCashFlowStartDay(pfsParameters, fromDate, True, False))):
        fromDate = acm.Time.DateAddDelta(fromDate, 0, 0, 1)

    cashFlowsToDelete = []
    for leg in portfolioSwap.Legs():
        for cashFlow in leg.CashFlows():
            if acm.Time.DateDifference(cashFlow.StartDate(), fromDate) >= 0:
                cashFlowsToDelete.append(cashFlow)

    batchIndexArray = Util.GetBatchIndices(len(cashFlowsToDelete), Conf.cashFlowBatchSize)
    for batchIndex in batchIndexArray:
        Util.ClearCashFlowsBatch(batchIndex, cashFlowsToDelete)
#----------------------------------------------------------------------------
def ClearResetsFromDateUntilEnd(pfsParameters, \
                                fromDate, \
                                excludeFinalReturnResets):
    excludeReturnResetsDate = None

    portfolioSwap = pfsParameters.portfolioSwap
    lastResetDate = Util.GetLastResetDate(portfolioSwap)
    if "Open End" == portfolioSwap.OpenEnd():
        if excludeFinalReturnResets:
            if not acm.Time.DateDifference(PeriodCashFlowStartDay(pfsParameters, \
                                                                    fromDate, \
                                                                    True, \
                                                                    False), \
                                            fromDate):
                excludeReturnResetsDate = acm.Time.DateAddDelta(fromDate, 0, 0, 1)
            else:
                excludeReturnResetsDate = fromDate
    elif excludeFinalReturnResets:
        excludeReturnResetsDate = portfolioSwap.ExpiryDate()

    currentDate = fromDate
    while currentDate and acm.Time.DateDifference(lastResetDate, currentDate) >= 0:
        excludeReturnResets = excludeReturnResetsDate and \
                                (not acm.Time.DateDifference(currentDate, excludeReturnResetsDate)) \
                                    or False
        Util.ClearPortfolioSwapDailyResets(portfolioSwap, \
                                            currentDate, \
                                            excludeReturnResets, \
                                            Conf.resetClearingBatchSize)
        currentDate = acm.Time.DateAddDelta(currentDate, 0, 0, 1)
#----------------------------------------------------------------------------
def ClearPaymentsFromDateUntilEnd(pfSwap, periodStartDate):
    if UsesPayments():
        singleTrade = Util.GetSingleTrade(pfSwap)
        lastPaymentDate = acm.Time.SmallDate()
        for payment in singleTrade.Payments():
            if acm.Time.DateDifference(payment.ValidFrom(), lastPaymentDate) >= 0:
                lastPaymentDate = payment.ValidFrom()

        fixingDate = periodStartDate
        while fixingDate:
            Util.ClearPayments(pfSwap, fixingDate)
            fixingDate = acm.Time.DateAddDelta(fixingDate, 0, 0, 1)
            fixingDate = acm.Time.DateDifference(fixingDate, lastPaymentDate) >= 0 \
                                    and fixingDate or None
#----------------------------------------------------------------------------
# Get fixing data for the portfolio positions.
# NOTE: Securities are returned as AEL-entities
#----------------------------------------------------------------------------
# MKLIMKE passed the Portfoli Swap Instrument aslso we need to get Info from it when doing calculations.
def GetPortfolioFixingData(prfSwap, \
                            portfolio, \
                            fixingDate, \
                            floatRef, \
                            returnLegIsPayLeg, \
                            calendar):
    startTime = time.time()
    LOGGER.info("Calculating fixing data for date %s ...", fixingDate)

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
                                                        floatRef, \
                                                        returnLegIsPayLeg)
    aelSecurities = []
    perSecurityData = {}

    childIter = portfolioIter.FirstChild()

    while childIter:
        insAndTrades = childIter.Tree().Item()
        securityName = calcSpace.CalculateValue(insAndTrades, 'Instrument Name')
        securityType = calcSpace.CalculateValue(insAndTrades, 'Instrument Type')

        validTrades = 0
        if securityType in Util.AllowedTrades.allowedInstrumentTypes:

            for t in insAndTrades.Trades().AsArray():
                if t.Status() in Util.AllowedTrades.allowedTradeStatus:
                    validTrades = 1
                    break

        if validTrades:
            aelSecurities.append(ael.Instrument[securityName])

            # MKLIMKE Need to add Portfolio Swap to fixing Data calculations do we want to pass the Portfolio?
            securityData = CalculatePerSecurityFixingData(prfSwap, \
                                                        portfolio, \
                                                        calcSpace, \
                                                        childIter.Tree(), \
                                                        fixingDate, \
                                                        floatRef, \
                                                        returnLegIsPayLeg, \
                                                        calendar)
            #--------------------------------------------------------------------------------------------------------------


            AppendSecurityData(perSecurityData, securityData)
        childIter = childIter.NextSibling()

    calcSpace.RemoveGlobalSimulation(colIdPnLEndDate)
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDateCustom)

    LOGGER.info("... Fixing data for date %s calculated in %s seconds", fixingDate, time.time() - startTime)

    return (aelSecurities, perSecurityData, perPortfolioData)
#----------------------------------------------------------------------------
def CalculatePerPortfolioFixingData(calcSpace, \
                                    portfolioTreeNode, \
                                    fixingDate, \
                                    floatRef, \
                                    returnLegIsPayLeg):
    customFixingData = None
    if Custom:
        try:
            customFixingData = Custom.CalculatePerPortfolioFixingData(calcSpace, \
                                                                    portfolioTreeNode, \
                                                                    UsePerPortfolioFunding(), \
                                                                    UsePerPortfolioExecutionFee(), \
                                                                    UsePerPortfolioRPL())
        except Exception:
            LOGGER.exception("Failed to evaluate custom per portfolio swap fixing data for date %s.", fixingDate)
            raise

    fixingData = CalculatePerPortfolioDefaultFixingData(calcSpace, \
                                                        portfolioTreeNode, \
                                                        customFixingData, \
                                                        fixingDate, \
                                                        floatRef, \
                                                        returnLegIsPayLeg)
    return fixingData
#----------------------------------------------------------------------------
def CalculatePerPortfolioDefaultFixingData(calcSpace, \
                                            portfolioTreeNode, \
                                            customFixingData, \
                                            fixingDate, \
                                            floatRef, \
                                            returnLegIsPayLeg):
    if customFixingData:
        fixingData = customFixingData
    else:
        fixingData = {}

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_FUNDING_AMOUNT, \
                                        UsePerPortfolioFunding()):
        financingAmount = Util.CalculateRowValueAsDouble(\
                                                        calcSpace, \
                                                        portfolioTreeNode, \
                                                        Conf.colIdFinancingAmount, \
                                                        "Portfolio", \
                                                        fixingDate)
        if not returnLegIsPayLeg:
            financingAmount = -financingAmount

        fixingData[ID_PER_PORTFOLIO_FUNDING_AMOUNT] = financingAmount

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_FUNDING_RATE, \
                                        UsePerPortfolioFunding()):
        overnightRate = GetOvernightRate(floatRef, fixingDate)
        Util.CheckForNaN(overnightRate, "Overnight rate", floatRef.Name(), fixingDate)
        fixingData[ID_PER_PORTFOLIO_FUNDING_RATE] = overnightRate

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_EXECUTION_FEE, \
                                        UsePerPortfolioExecutionFee()):
        fixingData[ID_PER_PORTFOLIO_EXECUTION_FEE] = Util.CalculateRowValueAsDouble(\
                                                                        calcSpace, \
                                                                        portfolioTreeNode, \
                                                                        Conf.colIdDailyExecutionFee, \
                                                                        "Portfolio", \
                                                                        fixingDate)

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_PORTFOLIO_RPL, \
                                        UsePerPortfolioRPL()):
        pass

    return fixingData
#----------------------------------------------------------------------------
# MKLIMKE Passed Portfolio Swap to Functions , maybe can replace with Parameters
def CalculatePerSecurityFixingData(prfSwap, \
                                    portfolio, \
                                    calcSpace, \
                                    securityTreeNode, \
                                    fixingDate, \
                                    floatRef, \
                                    returnLegIsPayLeg, \
                                    calendar):
    customFixingData = None
    if Custom:
        try:
            customFixingData = Custom.CalculatePerSecurityFixingData(fixingDate, \
                                                            prfSwap, \
                                                            portfolio, \
                                                            calcSpace, \
                                                            securityTreeNode, \
                                                            not UsePerPortfolioFunding(), \
                                                            not UsePerPortfolioExecutionFee(), \
                                                            UsePerSecurityRepo())
        except Exception:
            LOGGER.exception("Failed to evaluate custom per security fixing data for date %s.", fixingDate)
            raise

    fixingData = CalculatePerSecurityDefaultFixingData(calcSpace, \
                                                        securityTreeNode, \
                                                        fixingDate, \
                                                        floatRef, \
                                                        customFixingData, \
                                                        returnLegIsPayLeg, \
                                                        calendar)
    return fixingData
#----------------------------------------------------------------------------
# MKLIMKE
'''
Changes made here, to calculate the divedens we use Invetory position which is a Vector column and then go get the correct Vector, however is is simpler and better to go get the actuall position for the day. 
'''
def CalculatePerSecurityDefaultFixingData(calcSpace, \
                                        securityTreeNode, \
                                        fixingDate, \
                                        floatRef, \
                                        customFixingData, \
                                        returnLegIsPayLeg, \
                                        calendar):
    if customFixingData:
        fixingData = customFixingData
    else:
        fixingData = {}

    security = securityTreeNode.Item().Instrument()
    securityName = security.Name()
    position = Util.CalculateRowValueAsDouble(calcSpace, \
                                                securityTreeNode, \
                                                Conf.colIdPosition, \
                                                securityName, \
                                                fixingDate)

    # Dividend comparison rule: acquire day < ex div day + spot
    #----------------------------------------------------------------------------------------------
    securitySpotDate = ael.date(fixingDate).add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
    calcSpace.SimulateGlobalValue(colIdPnLEndDate, "Custom Date")
    calcSpace.SimulateGlobalValue(colIdPnLEndDateCustom, securitySpotDate)
    inventoryPosition = Util.CalculateRowValueAsDouble(calcSpace, \
                                                        securityTreeNode, \
                                                        Conf.colIdPosition, \
                                                        securityName, \
                                                        None, \
                                                        None, \
                                                        None)
    calcSpace.SimulateGlobalValue(colIdPnLEndDateCustom, fixingDate)
    #----------------------------------------------------------------------------------------------

    if Conf.fixTotalInvested:
        returnFixingValue = Util.CalculateRowValueAsDouble(\
                                                    calcSpace, \
                                                    securityTreeNode, \
                                                    Conf.colIdTotalInvested, \
                                                    securityName, \
                                                    fixingDate)
        # WWW
        # returnFixingValue = abs(returnFixingValue)
    else:
        averagePrice = Util.CalculateRowValueAsDouble(calcSpace, \
                                                    securityTreeNode, \
                                                    Conf.colIdAveragePrice, \
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
                                        not UsePerPortfolioFunding()):

        financingAmount = Util.CalculateRowValueAsDouble(\
                                                        calcSpace, \
                                                        securityTreeNode, \
                                                        Conf.colIdFinancingAmount, \
                                                        securityName, \
                                                        fixingDate)

        if not returnLegIsPayLeg:
            financingAmount = -financingAmount
        fixingData[ID_PER_SECURITY_FUNDING_AMOUNT] = financingAmount

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_FUNDING_RATE, \
                                        not UsePerPortfolioFunding()):
        overnightRate = GetOvernightRate(floatRef, fixingDate)
        Util.CheckForNaN(overnightRate, "Overnight rate", floatRef.Name(), fixingDate)
        fixingData[ID_PER_SECURITY_FUNDING_RATE] = overnightRate

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_EXECUTION_FEE, \
                                        not UsePerPortfolioExecutionFee()):
        fixingData[ID_PER_SECURITY_EXECUTION_FEE] = Util.CalculateRowValueAsDouble(\
                                                                        calcSpace, \
                                                                        securityTreeNode, \
                                                                        Conf.colIdDailyExecutionFee, \
                                                                        securityName, \
                                                                        fixingDate)

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_REPO_AMOUNT, \
                                        UsePerSecurityRepo()):
        fixingData[ID_PER_SECURITY_REPO_AMOUNT] = 0.0

    if not Util.CheckValueConditionally(fixingData, \
                                        ID_PER_SECURITY_REPO_FINANCING_RATE, \
                                        UsePerSecurityRepo()):
        fixingData[ID_PER_SECURITY_REPO_FINANCING_RATE] = 0.0

    return fixingData
#----------------------------------------------------------------------------
def CalculatePortfolioSwapFixingData(portfolioSwap, fixingDate, calculateDailyCash=False):
    startTime = time.time()
    LOGGER.info("Calculating Portfolio Swap fixing data for date %s ...", fixingDate)

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

        # MKLIMKE How many params should we pass
        '''----------------------------------------------------------------------------------------
        portfolioSwapData = Custom.CalculatePortfolioSwapFixingData(calcSpace, \
                                                                    portfolioSwapIter.Tree(), \
                                                                    UseCallDepositLeg(), \
                                                                    calculateDailyCash)
        -------------------------------------------------------------------------------------------'''
        portfolioSwapData = Custom.CalculatePortfolioSwapFixingData(calcSpace, \
                                                                    portfolioSwapIter.Tree(), \
                                                                    calculateDailyCash)


    if not Util.CheckValueConditionally(portfolioSwapData, \
                                        ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT, \
                                        UseCallDepositLeg()):

        portfolioSwapData[ID_PORTFOLIO_SWAP_DEPOSIT_AMOUNT] = -1.0 * Util.CalculateRowValueAsDouble(\
                                                                                calcSpace, \
                                                                                portfolioSwapIter.Tree(), \
                                                                                Conf.colIdCallDepositAmount, \
                                                                                portfolioSwap.Name(), \
                                                                                fixingDate)

    if calculateDailyCash and not Util.CheckValueConditionally(portfolioSwapData, \
                                                                ID_PORTFOLIO_SWAP_DAILY_CASH, \
                                                                UseCallDepositLeg()):
        portfolioSwapData[ID_PORTFOLIO_SWAP_DAILY_CASH] = Util.CalculateRowValueAsDouble(\
                                                                calcSpace, \
                                                                portfolioSwapIter.Tree(), \
                                                                Conf.colIdDailyCash, \
                                                                portfolioSwap.Name(), \
                                                                fixingDate)

    calcSpace.RemoveGlobalSimulation(colIdPnLEndDate)
    calcSpace.RemoveGlobalSimulation(colIdPnLEndDateCustom)

    LOGGER.info("... Portfolio Swap fixing data for date %s calculated in %s seconds", fixingDate, time.time() - startTime)
    return portfolioSwapData
#----------------------------------------------------------------------------
def AppendSecurityData(perSecurityData, securityData):

    try:
        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_POSITION, True)
        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_INV_POSITION, True)
        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_RETURN_FIXING, True)

        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_FUNDING_AMOUNT, \
                                    not UsePerPortfolioFunding())
        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_FUNDING_RATE, \
                                    not UsePerPortfolioFunding())

        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_EXECUTION_FEE, \
                                    not UsePerPortfolioExecutionFee())

        Util.AppendListConditionally(perSecurityData, securityData, ID_PER_SECURITY_DIVIDEND_SUPPRESSION, True)

        Util.AppendListConditionally(perSecurityData, \
                                    securityData, \
                                    ID_PER_SECURITY_REPO_AMOUNT, \
                                    UsePerSecurityRepo())

        Util.AppendListConditionally(perSecurityData, \
                                    securityData,
                                    ID_PER_SECURITY_REPO_FINANCING_RATE, \
                                    UsePerSecurityRepo())
    except Exception:
        LOGGER.exception("Missing per security data.")
        raise
#----------------------------------------------------------------------------
def GetOvernightRate(floatRef, date):
    calcSpace = acm.FStandardCalculationsSpaceCollection()
    priceDV = floatRef.Calculation().MarketPrice(calcSpace, \
                                                date,  # date \
                                                False,  # correct date \
                                                None,  # currency \
                                                False,  # correct currency \
                                                None,  # market place \
                                                False,  # correct market place \
                                                "ClosePrice",  # price type \
                                                False)  # correct type

    return priceDV and priceDV.Number() or acm.Math.NotANumber()
#----------------------------------------------------------------------------
# - Generates legs and cash flows corresponding to the positions in the selected
# portfolio.
# - Clears old legs and cash flows.
# - Generates initial return resets
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# AR636875 - Date conversion issue when running the Generate Portfolio Swap script from the Server
# Workaround with ael
#----------------------------------------------------------------------------
def GeneratePortfolioSwap(pfsParameters):
    periodEndDay = PeriodCashFlowEndDay(pfsParameters, \
                                        pfsParameters.calendar.AdjustBankingDays(\
                                            pfsParameters.portfolioSwap.StartDate(), \
                                            1), \
                                        False)
    pfsName = pfsParameters.portfolioSwap.Name()
    aelSwap = ael.Instrument[pfsName]

    if "Open End" == pfsParameters.portfolioSwap.OpenEnd():
        # pfsParameters.portfolioSwap.ExpiryDate = periodEndDay
        # pfsParameters.portfolioSwap.Commit()
        aelSwap = aelSwap.clone()
        aelSwap.exp_day = ael.date(periodEndDay)
        aelSwap.exp_time = 0
        aelSwap.commit()
        ael.poll()

    Util.ClearPortfolioSwapLegs(pfsParameters.portfolioSwap, Conf.legClearingBatchSize)
    baseLegs, perSecurityCashFlows = GeneratePortfolioSwapLegsAndCashFlows(pfsParameters, periodEndDay)

    Util.ClearPortfolioSwapResets(pfsParameters.portfolioSwap, Conf.resetClearingBatchSize)
    if UsesPayments():
        Util.ClearPayments(pfsParameters.portfolioSwap)
    GenerateInitialResets(perSecurityCashFlows, pfsParameters, pfsParameters.portfolioSwap.StartDate())
#----------------------------------------------------------------------------
def GeneratePortfolioSwapLegsAndCashFlows(pfsParameters, periodEndDay):

    (legStartDate, legEndDate) = GetLegStartAndEndDate(pfsParameters, \
                                                        pfsParameters.portfolioSwap.StartDate(), \
                                                        periodEndDay)
    legEndDate = periodEndDay and periodEndDay or legEndDate

    GeneratePerPortfolioSwapLegs(pfsParameters, \
                                legStartDate, \
                                legEndDate, \
                                UsePerPortfolioFunding(), \
                                UsePerPortfolioExecutionFee(), \
                                UsePerPortfolioRepo(), \
                                UseCallDepositLeg(), \
                                UseMarginLeg())

    GeneratePerPortfolioSwapCashFlows(pfsParameters, \
                                        legStartDate, \
                                        UsePerPortfolioFunding(), \
                                        UsePerPortfolioRepo(), \
                                        UseCallDepositLeg())

    aelSecurities = Util.GetAelSecurities(pfsParameters.portfolioSwap.FundPortfolio())

    baseLegs = GeneratePerSecurityLegs(pfsParameters, \
                                        aelSecurities, \
                                        legStartDate, \
                                        legEndDate, \
                                        not UsePerPortfolioFunding(), \
                                        not UsePerPortfolioExecutionFee(), \
                                        UsePerSecurityRepo(), \
                                        UseDividendLegs())

    perSecurityCashFlows = GeneratePerSecurityCashFlows(pfsParameters, \
                                                    baseLegs, \
                                                    legStartDate, \
                                                    legEndDate, \
                                                    "Open End" == pfsParameters.portfolioSwap.OpenEnd())
    return (baseLegs, perSecurityCashFlows)
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
        legEndDate = PeriodCashFlowEndDay(pfsParameters, resetEndDate, False)
    else:
        legStartDate = pfsParameters.portfolioSwap.StartDate()
        legEndDate = pfsParameters.portfolioSwap.ExpiryDate()

    return (legStartDate, legEndDate)
#----------------------------------------------------------------------------
def GeneratePerSecurityLegs(pfsParameters, \
                            aelSecurities, \
                            legStartDate, \
                            legEndDate, \
                            generateFinancingLegs, \
                            generateExecutionFeeLegs, \
                            generateRepoLegs, \
                            generateDividendLegs):

    batchIndexArray = Util.GetBatchIndices(len(aelSecurities), Conf.legBatchSize)
    baseLegs = []
    dividendLegs = []
    for batchIndex in batchIndexArray:
        batchBaseLegs = GeneratePerSecurityLegsBatch(batchIndex, \
                                                    pfsParameters, \
                                                    aelSecurities, \
                                                    legStartDate, \
                                                    legEndDate, \
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
                                openEndAdjustDates=True):

    perSecurityCashFlows = []
    batchIndexArray = Util.GetBatchIndices(len(baseLegs), Conf.cashFlowBatchSize)
    for batchIndex in batchIndexArray:
        batchPerSecurityCashFlows = GeneratePerSecurityCashFlowsBatch(batchIndex, \
                                                            baseLegs, \
                                                            pfsParameters, \
                                                            cFStartDate, \
                                                            cFEndDate, \
                                                            openEndAdjustDates)
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
                                            "Dividend", \
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

    securityBatchBaseLegs = GenerateSecurityBaseLegsBatch(batchIndex, \
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
    LOGGER.info("Generating portfolio swap base legs batch (batch size: %s)", len(batchIndex))
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
    except Exception:
        LOGGER.exception("Failed to generate base legs.")
        raise
    LOGGER.info("... Portfolio swap base legs batch generated in %s seconds", time.time() - startTime)
    return legs
#----------------------------------------------------------------------------
def GeneratePortfolioSwapDividendLegsBatch(portfolioSwap, \
                                            returnLegIsPayLeg, \
                                            securityBaseLegs, \
                                            useSingleFinancingLeg, \
                                            periodStartDate):
    startTime = time.time()
    LOGGER.info("Generating portfolio swap dividend legs batch (batch size: %s)", len(securityBaseLegs))

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
        LOGGER.info("... Portfolio swap dividend legs batch generated in %s seconds", time.time() - startTime)
    except Exception:
        LOGGER.exception("Failed to generate dividend legs.")
        raise
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
        raise Exception("Unhandled number of dividend legs for security: %s - Exits" % str(legs.Size()))
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
                                    "Dividend")
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
                                        openEndAdjustDates):

    calendar = pfsParameters.calendar
    paydayOffset = pfsParameters.paydayOffset
    paydayOffsetMethod = pfsParameters.paydayOffsetMethod

    startTime = time.time()
    LOGGER.info("Generating portfolio swap cash flows batch (batch size: %s)", len(securityBatchBaseLegs))
    batchPerSecurityCashFlows = []
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            returnLeg, financingLeg, repoLeg, executionFeeLeg, dividendLegs = \
                                                    securityBatchBaseLegs[index]
            returnCFs = Util.GetCashFlowsInPeriod(returnLeg, cFStartDay, False)
            if returnCFs:
                returnCF = returnCFs[0]
            else:
                returnCF = Util.CreatePortfolioSwapCashFlow(returnLeg, \
                                                        0.0, \
                                                        ReturnCashFlowType(), \
                                                        calendar, \
                                                        paydayOffset, \
                                                        paydayOffsetMethod, \
                                                        cFStartDay, \
                                                        cFEndDay, \
                                                        None, \
                                                        openEndAdjustDates, \
                                                        False)
            if financingLeg:
                financingCF = Util.GetSingleFinancingCashFlowFromLeg(financingLeg,
                                                                     cFStartDay,
                                                                     False)
                if not financingCF:
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
                repoCFs = Util.GetCashFlowsInPeriod(repoLeg, cFStartDay, False)
                if repoCFs:
                    repoCF = repoCFs[0]
                else:
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
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to generate cash flows.")
        raise
    LOGGER.info("... Portfolio swap cash flows batch generated in %s seconds", time.time() - startTime)
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
    except Exception:
        LOGGER.exception("Dividend leg update failed.")
        raise
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
def GenerateDailyPayments(pfsParameters, \
                            fixingDate, \
                            perPortfolioData):

    portfolioSwap = pfsParameters.portfolioSwap
    returnLegIsPayLeg = pfsParameters.returnLegIsPayLeg

    payDate = Util.AdjustDateToOffsetMethod(portfolioSwap.ExpiryDate(), \
                                            pfsParameters.calendar, \
                                            pfsParameters.paydayOffset, \
                                            pfsParameters.paydayOffsetMethod)

    dailyExFee = Util.GetValueConditionally(perPortfolioData, \
                                            ID_PER_PORTFOLIO_EXECUTION_FEE, \
                                            UsePerPortfolioExecutionFee())
    dailyRPL = Util.GetValueConditionally(perPortfolioData, \
                                            ID_PER_PORTFOLIO_RPL, \
                                            UsePerPortfolioRPL())

    isSwapStartDay = acm.Time.DateDifference(fixingDate, portfolioSwap.StartDate()) == 0

    if None != dailyExFee and 0.0 != dailyExFee:
        dailyExFee = returnLegIsPayLeg and -dailyExFee or dailyExFee
        GenerateDailyPayment(portfolioSwap, dailyExFee, Conf.executionFeePaymentType, fixingDate, payDate)
    if None != dailyRPL and 0.0 != dailyRPL and not (pfsParameters.previousPfSwap and isSwapStartDay):
        dailyRPL = returnLegIsPayLeg and -dailyRPL or dailyRPL
        GenerateDailyPayment(portfolioSwap, dailyRPL, Conf.RPLPaymentType, fixingDate, payDate)

    if Conf.calculateDivUPL:
        portfolioDividendUPL = GetPortfolioDividendUPL(portfolio, fixingDate, portfolioSwap.StartDate())
        if returnLegIsPayLeg:
            portfolioDividendUPL = -portfolioDividendUPL
        portfolioSwapDividendUPL = GetPortfolioSwapDividendUPL(portfolioSwap, fixingDate)
        GenerateDailyDeltaPayment(portfolioSwap, \
                                    portfolioSwapDividendUPL, \
                                    portfolioDividendUPL, \
                                    Conf.divUPLPaymentType, \
                                    fixingDate, \
                                    payDate, \
                                    Conf.divUPLPaymentType)
#----------------------------------------------------------------------------
def ClearPerSecurityCashFlowsResets(perSecurityCashFlows):
    cashFlows = [cF for securityCFs in perSecurityCashFlows for cF in securityCFs if None != cF]
    Util.ClearCashFlowsResets(cashFlows, Conf.resetClearingBatchSize)
#----------------------------------------------------------------------------
def ClearPerPortfolioSwapCashFlowsResets(portfolioSwap, \
                                        returnLegIsPayLeg, \
                                        periodStartDate, \
                                        clearFinancingCashFlow, \
                                        clearRepoCashFlow):
    cashFlows = []
    if clearFinancingCashFlow:
        cashFlows.append(Util.GetSingleFinancingCashFlow(portfolioSwap, \
                                                            returnLegIsPayLeg, \
                                                            periodStartDate, \
                                                            False))
    if clearRepoCashFlow:
        cashFlows.append(Util.GetSingleRepoCashFlow(portfolioSwap, \
                                                    returnLegIsPayLeg, \
                                                    periodStartDate, \
                                                    False))
    Util.ClearCashFlowsResets(cashFlows, Conf.resetClearingBatchSize)
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
        LOGGER.error("Failed to find counterparty payment account for trade: %s", singleTrade.Oid())
        raise Exception("Counterparty account not found")
    if not acquirerAccount:
        LOGGER.error("Failed to find acquirer payment account for trade: %s", singleTrade.Oid())
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
    except Exception:
        LOGGER.exception("Failed to create payment.")
        raise
#----------------------------------------------------------------------------
def SpreadAdjustFundingRates(aelSecurities, \
                            pfsParameters, \
                            perPortfolioData, \
                            perSecurityData):
    if UsePerPortfolioFunding():
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
def SpreadAdjustOvernightRate(position, \
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
def GetPortfolioSwapDividendUPL(portfolioSwap, fixingDate):
    singleTrade = Util.GetSingleTrade(portfolioSwap)
    dividendUPL = 0.0

    globalSimulations = [(colIdPnLStartDate, "Custom"), \
                        (colIdPnLStartDateCustom, fixingDate)]
    dividendUPL = Util.CalculateSingleSheetValue("FPortfolioSheet", \
                                            singleTrade, \
                                            Conf.colIdPortfolioSwapDivUPL, \
                                            1, \
                                            globalSimulations, \
                                            None).Number()
    if singleTrade.Quantity() < 0.0:
        dividendUPL = -dividendUPL
    return dividendUPL
#----------------------------------------------------------------------------
def GetPortfolioDividendUPL(portfolio, \
                            fixingDate, \
                            portfolioSwapStartDate):

    colConfigVector = acm.FArray()
    configParameters = acm.FNamedParameters()
    configParameters.AddParameter("paymentType", Conf.divUPLPaymentType)
    colConfigVector.Add(configParameters)
    columnConfig = acm.Sheet().Column().ConfigurationFromVector(colConfigVector)

    periodStartDate = acm.Time().DateAddDelta(fixingDate, 0, 0, -1)
    globalSimulations = [(colIdPnLStartDate, "Custom"), (colIdPnLStartDateCustom, periodStartDate), \
                        (colIdPnLEndDate, "Custom"), (colIdPnLEndDateCustom, fixingDate)]
    localSimulations = [(portfolio, "PFS paymentsComparisonRuleOverride", "ValidFromDay")]

    dividendUPL = Util.CalculateSingleSheetValue("FPortfolioSheet", \
                                            portfolio, \
                                            colIdPortfolioDivUPL, \
                                            0, \
                                            globalSimulations, \
                                            localSimulations, \
                                            columnConfig)
    return dividendUPL.Number()
#----------------------------------------------------------------------------
def ReturnCashFlowType():
    if Conf.fixTotalInvested:
        return "Position Total Return"
    return "Total Return"
#----------------------------------------------------------------------------
def UsesPayments():
    return Conf.usePerPortfolioRPL or \
            Conf.usePerPortfolioExecutionFee or \
            Conf.calculateDivUPL
#----------------------------------------------------------------------------
columnIds = []
if Conf.usePerPortfolioRPL and Conf.colIdDailyRPL:
    columnIds.extend([Conf.colIdDailyRPL, Conf.colIdPaymentsComparisonRule])
if Conf.colIdDailyExecutionFee:
    columnIds.append(Conf.colIdDailyExecutionFee)
if Conf.calculateDivUPL and Conf.colIdPortfolioDivUPL and Conf.colIdPortfolioSwapDivUPL:
    columnIds.extend([Conf.colIdPortfolioDivUPL, Conf.colIdPortfolioSwapDivUPL])
Util.CheckColumnDefinitions(columnIds, \
                        acm.GetDefaultContext(), \
                        True)
if UsesPayments():
    Util.AssertPaymentTypes((Conf.executionFeePaymentType, Conf.divUPLPaymentType, Conf.RPLPaymentType))
#----------------------------------------------------------------------------
def UsePerPortfolioFunding():
    return True == Conf.usePerPortfolioFunding
#----------------------------------------------------------------------------
def UsePerPortfolioExecutionFee():
    return True == Conf.usePerPortfolioExecutionFee
#----------------------------------------------------------------------------
def UsePerSecurityRepo():
    return "Per Security" == Conf.repoLegConfig
#----------------------------------------------------------------------------
def UsePerPortfolioRepo():
    return "Single" == Conf.repoLegConfig
#----------------------------------------------------------------------------
def UsePerPortfolioRPL():
    return True == Conf.usePerPortfolioRPL
#----------------------------------------------------------------------------
def UseCallDepositLeg():
    return True == Conf.useCallDepositLeg
#----------------------------------------------------------------------------
def UseDividendLegs():
    return True == Conf.generateDividendLegs
#----------------------------------------------------------------------------
def UseMarginLeg():
    return True == Conf.useMarginLeg
#----------------------------------------------------------------------------
def MonthEndAdjustFunding():
    return True == Conf.monthEndAdjustFunding
