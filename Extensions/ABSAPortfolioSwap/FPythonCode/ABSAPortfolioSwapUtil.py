"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapUtil
    
    Created from FSEQPortfolioSwapUtil

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Utility functions used by the ABSAPortfolioSwap functions.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael
import time

from at_logging import getLogger

from PS_MirrorToCR import VALID_INS_TYPE_FOR_CFD


LOGGER = getLogger()

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Portfolio Swap specific get-functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
class AllowedTrades:
    allowedTradeStatus = ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']
    allowedInstrumentTypes = list(VALID_INS_TYPE_FOR_CFD)

def GetCashFlowsInPeriod(leg, periodStartDay, isAel=True):
    if isAel:
        cashFlows = leg.cash_flows()
    else:
        cashFlows = leg.CashFlows()
    
    matchingCashFlows = []
    for cashFlow in cashFlows:
        if isAel and not acm.Time.DateDifference(str(cashFlow.start_day), periodStartDay):
            matchingCashFlows.append(cashFlow)
        elif not isAel and not acm.Time.DateDifference(cashFlow.StartDate(), periodStartDay):
            matchingCashFlows.append(cashFlow)
    return matchingCashFlows
#----------------------------------------------------------------------------
def GetPreviousFixing(cashFlow, \
                  resetType, \
                  fixingDate, \
                  isAel=True):
                  
    if isAel:
        resets = [r for r in cashFlow.resets() if resetType == r.type]
    else:
        resets = [r for r in cashFlow.Resets() if resetType == r.ResetType()]

    if len(resets):
        if isAel:
            resets.sort(lambda x, y : x.day.to_time() - y.day.to_time())
        else:
            resets.sort(lambda x, y : acm.Time.DateDifference(x.Day(), y.Day()))

    previousReset = None        
    for reset in resets:
        if (isAel and reset.day < ael.date(fixingDate)) or \
                (not isAel and acm.Time.DateDifference(reset.Day(), fixingDate) < 0):
            previousReset = reset
        else:
            break
    return previousReset
#----------------------------------------------------------------------------
def GetResetOfTypeAtDate(cashFlow, resetType, date, isAel=True):
    resultReset = None
    if isAel:
        aelDate = ael.date(date)
        cFResets = cashFlow.resets()
    else:
        cFResets = cashFlow.Resets()

    for reset in cFResets:
        if isAel and (resetType == reset.type and reset.day == aelDate):
            resultReset = reset
            break
        elif (not isAel) and resetType == reset.ResetType() and \
                not acm.Time.DateDifference(reset.Day(), date):
            resultReset = reset
            break
    return resultReset
#----------------------------------------------------------------------------
def GetResetsOfTypeAtDate(cashFlows, resetType, date, isAel=True):
    resultResets = []
    for cashFlow in cashFlows:
        if cashFlow:
            resultResets.append(GetResetOfTypeAtDate(cashFlow, resetType, date, isAel))
        else:
            resultResets.append(None)
    if not len([r for r in resultResets if None != r]):
        resultResets = None
    return resultResets
#----------------------------------------------------------------------------
# Get a list with the Portfolio Swap 'Base Cash Flows' where each item
# is a tuple on the form (returnCF, financingCF, repoCF).
# The list aelSecurities may be passed to verify the order of the cash flows.
#----------------------------------------------------------------------------
def GetCashFlowsPerSecurity(portfolioSwap, \
                            returnCashFlowType, \
                            returnLegIsPayLeg, \
                            periodStartDate, \
                            securities=None, \
                            isAel=True):
    indexRefToLegsDict = GetIndexRefToLegsDictionary(portfolioSwap, returnLegIsPayLeg, isAel)
    if not securities:
        securities = indexRefToLegsDict.keys()
    
    cashFlowsPerSecurity = []
    for security in securities:
        securityLegs = indexRefToLegsDict.get(security)
        if not securityLegs:
            raise Exception("ERROR: No legs for index reference: %s - Exits" % (isAel and security.insid or security.Name()))
        securityCashFlows = GetSecurityCashFlows(securityLegs, \
                                                returnCashFlowType, \
                                                periodStartDate, \
                                                isAel)
        cashFlowsPerSecurity.append(securityCashFlows)
    return cashFlowsPerSecurity
#----------------------------------------------------------------------------
def GetAelBaseLegsAndCashFlowsClonesPerSecurity(aelPortfolioSwap, \
                                                isSingleLegFinancing, \
                                                returnCashFlowType, \
                                                returnLegIsPayLeg, \
                                                periodStartDate):
                                                
    indexRefToLegsDict = GetIndexRefToLegsDictionary(aelPortfolioSwap, returnLegIsPayLeg)
    
    legsAndCashFlowsClones = []
    for security, securityBaseLegs in indexRefToLegsDict.iteritems():
        securityBaseLegsClones = [ReturnLegFromList(securityBaseLegs).clone(), \
                                FinancingLegFromList(securityBaseLegs) and \
                                    FinancingLegFromList(securityBaseLegs).clone() or None, \
                                RepoLegFromList(securityBaseLegs) and
                                    RepoLegFromList(securityBaseLegs).clone() or None]
        securityBaseCashFlowsClones = GetSecurityCashFlows(securityBaseLegsClones, \
                                                            returnCashFlowType, \
                                                            periodStartDate)
        legsAndCashFlowsClones.append((securityBaseLegsClones, securityBaseCashFlowsClones))
    return legsAndCashFlowsClones
#----------------------------------------------------------------------------
def GetPerPortfolioSwapLegs(portfolioSwap, \
                            returnLegIsPayLeg, \
                            getFinancingLeg, \
                            getRepoLeg, \
                            getCallDepositLeg, \
                            isAel=True):
    financingLeg = getFinancingLeg and \
                    GetSingleFinancingLeg(portfolioSwap, returnLegIsPayLeg, isAel) or None
    repoLeg = getRepoLeg and GetSingleRepoLeg(portfolioSwap, returnLegIsPayLeg, isAel) or None
    callDepositLeg = getCallDepositLeg and GetCallDepositLeg(portfolioSwap, isAel) or None
    return (None, financingLeg, repoLeg, None, None, callDepositLeg)
#----------------------------------------------------------------------------
def GetSecurityCashFlows(securityLegs, \
                        returnCashFlowType, \
                        periodStartDate, \
                        isAel=True):
    
    returnTemp = securityLegs and ReturnLegFromList(securityLegs) or None
    financingTemp = securityLegs and FinancingLegFromList(securityLegs) or None

    dailyReturnLeg = returnTemp and \
                        (isAel and "Daily Return" == returnTemp.reset_type or \
                            (not isAel and "Daily Return" == returnTemp.ResetType())) \
                            and returnTemp or None
    simpleOvernightLeg = financingTemp and \
                        (isAel and "Simple Overnight" == financingTemp.reset_type or \
                            (not isAel and "Simple Overnight" == financingTemp.ResetType())) \
                            and financingTemp or None
                        
    repoLeg = securityLegs and RepoLegFromList(securityLegs) or None

    cFsDailyReturn = dailyReturnLeg and GetCashFlowsInPeriod(dailyReturnLeg, \
                                                            periodStartDate, isAel) or None
    cFsSimpleOvernight = simpleOvernightLeg and GetCashFlowsInPeriod(simpleOvernightLeg, \
                                                                        periodStartDate, isAel) or None
    cFsRepo = repoLeg and GetCashFlowsInPeriod(repoLeg, periodStartDate, isAel) or None

    cFDailyReturn = cFsDailyReturn and cFsDailyReturn[0] or None
    cFSimpleOvernight = cFsSimpleOvernight and cFsSimpleOvernight[0] or None
    cFRepo = cFsRepo and len(cFsRepo) and cFsRepo[0] or None

    return (cFDailyReturn, cFSimpleOvernight, cFRepo)
#----------------------------------------------------------------------------
def GetAelSecurities(portfolio):
    aelSecurityDict = {}
    for trade in portfolio.Trades():
        instrument = trade.Instrument()
        
        if instrument.InsType() in AllowedTrades.allowedInstrumentTypes:
            aelSecurity = ael.Instrument[instrument.Name()]

            if not aelSecurity:
                raise Exception("Could not find ael entity: '%s'" % instrument.Name())

            if not aelSecurityDict.has_key(aelSecurity) and trade.Status() in AllowedTrades.allowedTradeStatus:
                aelSecurityDict[aelSecurity] = 1


    return aelSecurityDict.keys()
#----------------------------------------------------------------------------
def GetNewAelSecurities(portfolioSwap, \
                    portfolio, \
                    returnLegIsPayLeg):
    newAELSecurities = []
    aelPortfolioSwap = ael.Instrument[portfolioSwap.Oid()]
    aelIndexRefToLegsDict = GetIndexRefToLegsDictionary(aelPortfolioSwap, returnLegIsPayLeg)
    aelSecurities = GetAelSecurities(portfolio)
    for aelSecurity in aelSecurities:
        if not aelIndexRefToLegsDict.get(aelSecurity):
            newAELSecurities.append(aelSecurity)
    return newAELSecurities
#----------------------------------------------------------------------------
def GetIndexRefToLegsDictionary(portfolioSwap, returnLegIsPayLeg, isAel=True):
    indexRefToLegs = {}
    
    if isAel: 
        legs = portfolioSwap.legs() 
    else:
        legs = portfolioSwap.Legs()

    for leg in legs:
        if isAel:
            indexRef = leg.index_ref
        else:
            indexRef = leg.IndexRef()
        if indexRef:
            legsAtIndexRef = indexRefToLegs.get(indexRef)
            if not legsAtIndexRef:
                # [returnLeg, financingLeg, repoLeg, executionFeeLeg, dividendLegs]
                legsAtIndexRef = [None, None, None, None, None]
                indexRefToLegs[indexRef] = legsAtIndexRef
            if LegIsReturn(leg, isAel):
                legsAtIndexRef[0] = leg
            elif LegIsFinancing(leg, returnLegIsPayLeg, isAel):
                legsAtIndexRef[1] = leg
            elif LegIsRepo(leg, returnLegIsPayLeg, isAel):
                legsAtIndexRef[2] = leg
            elif LegIsExecutionFee(leg, returnLegIsPayLeg, isAel):
                legsAtIndexRef[3] = leg
            elif LegIsDividend(leg, isAel):
                dividendLegsList = legsAtIndexRef[4]
                if not dividendLegsList:
                    dividendLegsList = []               
                    legsAtIndexRef[4] = dividendLegsList
                dividendLegsList.append(leg)
    return indexRefToLegs
#----------------------------------------------------------------------------
def GetBatchIndices(totalSize, batchSize):
    batches = []
    allIndices = list(range(totalSize))
    nbrOfFullBatches = totalSize / int(batchSize)
    nbrOfBatches = (totalSize / float(batchSize) - nbrOfFullBatches) and \
                                                nbrOfFullBatches + 1 or \
                                                nbrOfFullBatches
    for i in range(nbrOfBatches):
        batchStart = i * batchSize
        batchEnd = i < nbrOfBatches - 1 and batchStart + batchSize or len(allIndices)
        batches.append(allIndices[batchStart:batchEnd])
    
    return batches
#----------------------------------------------------------------------------
def GetSingleFinancingLeg(portfolioSwap, \
                            returnLegIsPayLeg, \
                            isAel=True):
    if isAel:
        legs = [l for l in portfolioSwap.legs() if LegIsFinancing(l, returnLegIsPayLeg, isAel)]
    else:
        legs = [l for l in portfolioSwap.Legs() if LegIsFinancing(l, returnLegIsPayLeg, isAel)]
    singleFinancingLeg = 1 == len(legs) and legs[0] or None
    if not singleFinancingLeg:
        raise Exception("Single financing leg was not found. Portfolio swap is not set up correctly - Exits")
    return singleFinancingLeg
#----------------------------------------------------------------------------
def GetCallDepositLeg(portfolioSwap, isAel=True):
    if isAel:
        legs = [l for l in portfolioSwap.legs() if LegIsCallDeposit(l, isAel)]
    else:
        legs = [l for l in portfolioSwap.Legs() if LegIsCallDeposit(l, isAel)]
        
    callDepositLeg = 1 == len(legs) and legs[0] or None
    if not callDepositLeg:
        raise Exception("Single call deposit leg was not found. Portfolio swap is not set up correctly - Exits")
    return callDepositLeg
#----------------------------------------------------------------------------
def GetSingleRepoLeg(portfolioSwap, returnLegIsPayLeg, isAel=True):
    if isAel:
        legs = [leg for leg in portfolioSwap.legs() if LegIsRepo(leg, returnLegIsPayLeg, isAel)]
    else:
        legs = [leg for leg in portfolioSwap.Legs() if LegIsRepo(leg, returnLegIsPayLeg, isAel)]
    repoLeg = 1 == len(legs) and legs[0] or None
    if not repoLeg:
        raise Exception("Repo leg was not found. Portfolio swap is not set up correctly - Exits")
    return repoLeg
#----------------------------------------------------------------------------
def GetSingleMarginLeg(portfolioSwap, returnLegIsPayLeg, isAel=True):
    if isAel:
        legs = [leg for leg in portfolioSwap.legs() if LegIsMargin(leg, returnLegIsPayLeg, isAel)]
    else:
        legs = [leg for leg in portfolioSwap.Legs() if LegIsMargin(leg, returnLegIsPayLeg, isAel)]
    marginLeg = 1 == len(legs) and legs[0] or None
    if not marginLeg:
        raise Exception("Margin leg was not found. Portfolio swap is not set up correctly - Exits")
    return marginLeg
#----------------------------------------------------------------------------
def GetSingleRepoCashFlow(portfolioSwap, returnLegIsPayLeg, startDate, isAel=True):
    singleRepoLeg = GetSingleRepoLeg(portfolioSwap, returnLegIsPayLeg, isAel)
    return GetSingleRepoCashFlowFromLeg(singleRepoLeg, startDate, isAel)
#----------------------------------------------------------------------------
def GetSingleRepoCashFlowFromLeg(repoLeg, startDate, isAel=True):
    if isAel:
        cashFlows = [cF for cF in repoLeg.cash_flows() if cF.start_day == ael.date(startDate)]
    else:
        cashFlows = [cF for cF in repoLeg.CashFlows() if \
                        not acm.Time.DateDifference(cF.StartDate(), startDate)]
    repoCashFlow = 1 == len(cashFlows) and cashFlows[0] or None
    if not repoCashFlow:
        raise Exception("Repo cash flow was not found. Portfolio swap is not set up correctly - Exits")
    return repoCashFlow
#----------------------------------------------------------------------------
def GetExecutionFeeLegs(portfolioSwap, returnLegIsPayLeg, securities=None, isAel=True):
    executionFeeLegs = []
    indexRefToLegsDict = GetIndexRefToLegsDictionary(portfolioSwap, returnLegIsPayLeg, isAel)
    if not securities:
        securities = indexRefToLegsDict.keys()
    for security in securities:
        securityLegs = indexRefToLegsDict.get(security)
        if not securityLegs:
            securityName = isAel and security.insid or security.Name()
            raise Exception("ERROR: Security legs not found for security %s - Exits" \
                                % securityName)
        executionFeeLegs.append(ExecutionFeeLegFromList(securityLegs))
    return executionFeeLegs
#----------------------------------------------------------------------------
def GetDividendLegs(portfolioSwap, returnLegIsPayLeg, securities=None, isAel=True):
    dividendLegs = []
    indexRefToLegsDict = GetIndexRefToLegsDictionary(portfolioSwap, returnLegIsPayLeg, isAel)   
    if not securities:
        securities = indexRefToLegsDict.keys()
    for security in securities:
        securityLegs = indexRefToLegsDict.get(security)
        if not securityLegs:
            securityName = isAel and security.insid or security.Name()
            raise Exception("ERROR: Security legs not found for security %s - Exits" \
                                % securityName)
        dividendLegs.append(DividendLegsFromList(securityLegs))
    return dividendLegs
#----------------------------------------------------------------------------
def GetSingleExecutionFeeLeg(portfolioSwap, returnLegIsPayLeg):
    legs = [l for l in portfolioSwap.Legs() if LegIsExecutionFee(leg, returnLegIsPayLeg, False)]
    executionFeeLeg = 1 == len(legs) and legs[0] or None
    if not executionFeeLeg:
        raise Exception("Execution fee leg was not found. Portfolio swap is not set up correctly - Exits")
    return executionFeeLeg
#----------------------------------------------------------------------------
def GetSingleFinancingCashFlow(portfolioSwap, returnLegIsPayLeg, startDate, isAel=True):
    singleFinancingLeg = GetSingleFinancingLeg(portfolioSwap, returnLegIsPayLeg, isAel)
    return GetSingleFinancingCashFlowFromLeg(singleFinancingLeg, startDate, isAel)
#----------------------------------------------------------------------------
def GetSingleFinancingCashFlowFromLeg(financingLeg, startDate, isAel=True):
    if isAel:
        cashFlows = [cf for cf in financingLeg.cash_flows() if \
                        "Float Rate" == cf.type and cf.start_day == ael.date(startDate)]
    else:
        cashFlows = [cf for cf in financingLeg.CashFlows() if \
                        "Float Rate" == cf.CashFlowType() and \
                            not acm.Time.DateDifference(cf.StartDate(), startDate)]

    singleFinancingCF = 1 == len(cashFlows) and cashFlows[0] or None
    if not singleFinancingCF:
        raise Exception("Single financing cash flow was not found (startDate = %s). Portfolio swap is not set up correctly - Exits" % startDate)
    return singleFinancingCF
#----------------------------------------------------------------------------
def GetRedemptionCashFlowFromLeg(callDepositLeg, raiseException=True, isAel=True):
    if isAel:
        cashFlows = [cf for cf in callDepositLeg.cash_flows() if "Redemption Amount" == cf.type]
    else:
        cashFlows = [cf for cf in callDepositLeg.CashFlows() if "Redemption Amount" == cf.CashFlowType()]
    
    redemptionCF = 1 == len(cashFlows) and cashFlows[0] or None
    if not redemptionCF and raiseException:
        raise Exception("Redemption cash flow not found. Portfolio swap is not set up correctly - Exits")
    return redemptionCF
#----------------------------------------------------------------------------
def GetSingleTrade(portfolioSwap, raiseException=True):
    trades = [t for t in portfolioSwap.Trades() if "Void" != t.Status()]
    if 1 == len(trades):
        trade = trades[0]
        return trade
    else: 
        errMess = "Failed to find single non-void trade in portfolio swap '%s'" % portfolioSwap.Name()
        LOGGER.error(errMess)
        if raiseException:
            raise Exception(errMess)
        return None
#----------------------------------------------------------------------------
def GetLastResetDate(portfolioSwap, onlyFixedResets=False):
    lastResetDate = acm.Time.SmallDate()
    for leg in portfolioSwap.Legs():
        for cashFlow in leg.CashFlows():
            for reset in cashFlow.Resets():
                if acm.Time.DateDifference(reset.Day(), lastResetDate) > 0 and \
                        (not onlyFixedResets or \
                            acm.Time.DateDifference(reset.ReadTime(), acm.Time.SmallDate())):
                    lastResetDate = reset.Day()
    return lastResetDate
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Portfolio Swap specific create functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def CreatePortfolioSwapLeg(portfolioSwap, \
                            legType, \
                            resetType, \
                            isPayLeg, \
                            security, \
                            legStartDate, \
                            legEndDate, \
                            spreadLong, \
                            spreadShort, \
                            daycountMethod, \
                            nominalScaling, \
                            floatRef=None):

    try:
        leg = portfolioSwap.CreateLeg(int(isPayLeg))
        leg.LegType = legType
        leg.ResetType = resetType
        leg.PayLeg = isPayLeg
        leg.IndexRef = security
        leg.NominalFactor = 1.0
        leg.Currency = security and security.Currency() or portfolioSwap.Currency()
        leg.StartDate = legStartDate
        leg.EndDate = legEndDate
        leg.NominalScaling = nominalScaling
        leg.Spread = spreadLong
        leg.Spread2 = spreadShort
        leg.DayCountMethod = daycountMethod
        leg.PassingType = "Dividend Payday"
        if floatRef:
            leg.FloatRateReference = floatRef
    except Exception:
        LOGGER.exception("Failed to create portfolio swap leg.")
        raise
    return leg
#----------------------------------------------------------------------------
def CreatePortfolioSwapCashFlow(leg, \
                                fixedAmount, \
                                type, \
                                calendar, \
                                paydayOffsetPeriod, \
                                paydayOffsetMethod, \
                                startDay, \
                                endDay, \
                                payDay, \
                                openEndAdjustDates=True, \
                                isAel=True):

    if (openEndAdjustDates or not payDay) and not calendar:
        raise Exception("No calendar passed to 'CreatePortfolioSwapCashFlow' - Exits")

    if openEndAdjustDates:
        if not startDay:
            raise Exception("No start date passed - Exits")
        endDay = calendar.AdjustBankingDays(startDay, 1)
        payDay = AdjustDateToOffsetMethod(endDay, calendar, paydayOffsetPeriod, paydayOffsetMethod)
    elif not payDay:
        if not endDay:
            raise Exception("No end date passed - Exits")
        payDay = AdjustDateToOffsetMethod(endDay, calendar, paydayOffsetPeriod, paydayOffsetMethod)
        
    if isAel:
        legClone = leg.clone()
        cashFlow = ael.CashFlow.new(legClone)
        cashFlow.start_day = startDay and ael.date(startDay) or None
        cashFlow.end_day = endDay and ael.date(endDay) or None
        cashFlow.pay_day = ael.date(payDay)
        cashFlow.nominal_factor = leg.nominal_factor
        cashFlow.fixed_amount = fixedAmount
        cashFlow.type = type
        if type == "Float Rate":
            cashFlow.rate = 1.0
        legClone.commit()
    else:
        cashFlow = leg.CreateCashFlow()
        cashFlow.StartDate = startDay
        cashFlow.EndDate = endDay
        cashFlow.PayDate = payDay
        cashFlow.NominalFactor = leg.NominalFactor()
        cashFlow.FixedAmount = fixedAmount
        cashFlow.CashFlowType = type
        if type == "Float Rate":
            cashFlow.FixedRate = 1.0
        cashFlow.Commit()
    return cashFlow
#----------------------------------------------------------------------------
# Resets are created via AEL for performance reasons (ACM clones the instrument
# on Commit). 
#----------------------------------------------------------------------------
def CreateReset(cashFlow, \
                resetType, \
                fixingDate, \
                startDate, \
                endDate, \
                resetValue, \
                fixValue=True):
    
    cashFlowClone = cashFlow.clone()
    reset = ael.Reset.new(cashFlowClone)
    reset.type = resetType
    reset.day = ael.date(fixingDate)
    reset.start_day = ael.date(startDate)
    reset.end_day = ael.date(endDate)
    if fixValue:
        reset.value = resetValue
        reset.read_time = ael.date(fixingDate).to_time()
    cashFlowClone.commit()
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Portfolio Swap specific clear functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Clear resets corresponding to daily portfolio swap fixings.
# Optional parameter fixingDate decides the fixing date for which resets
# should be deleted.
#----------------------------------------------------------------------------
def ClearPortfolioSwapDailyResets(portfolioSwap, fixingDate, excludeReturnResets, batchSize):
    legs = portfolioSwap.Legs()
    batchIndexArray = GetBatchIndices(len(legs), batchSize)
    for batchIndex in batchIndexArray:
        ClearPortfolioSwapDailyResetsBatch(batchIndex, legs, fixingDate, excludeReturnResets)
#----------------------------------------------------------------------------
def ClearPortfolioSwapDailyResetsBatch(batch, legs, fixingDate, excludeReturnResets):
    try:
        acm.BeginTransaction()
        for index in batch:
            ClearLegResets(legs[index], fixingDate, excludeReturnResets)
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to clear resets batch.")
        raise
#----------------------------------------------------------------------------
def ClearCashFlowsBatch(batchIndex, \
                        cashFlows):
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            cashFlows[index].Delete()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to clear cash flows batch.")
        raise
#----------------------------------------------------------------------------
def ClearPayments(portfolioSwap, fixingDate=None):
    singleTrade = GetSingleTrade(portfolioSwap)
    if singleTrade:
        payments = [payment for payment in singleTrade.Payments() \
                    if (not fixingDate) or (fixingDate and \
                        not acm.Time.DateDifference(fixingDate, payment.ValidFrom()))]
        try:
            acm.BeginTransaction()
            for payment in payments:
                payment.Delete()
            acm.CommitTransaction()
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception("Failed to clear portfolio swap payments.")
            raise
#----------------------------------------------------------------------------
def ClearPortfolioSwapLegs(portfolioSwap, batchSize):
    legs = [leg for leg in portfolioSwap.Legs()]
    batchIndexArray = GetBatchIndices(len(legs), batchSize)
    for batchIndex in batchIndexArray:
        ClearPortfolioSwapLegsBatch(batchIndex, legs)
    portfolioSwap.Legs().Clear()
#----------------------------------------------------------------------------
def ClearPortfolioSwapLegsBatch(batchIndex, legs):
    startTime = time.time()
    LOGGER.info("Clearing portfolio swap legs batch (batch size: %s) ...", len(batchIndex))
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            leg = legs[index]
            leg.Delete()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to clear portfolio swap legs batch.")
        raise
    LOGGER.info("... Cleared portfolio swap legs batch in %s seconds" , time.time() - startTime)
#----------------------------------------------------------------------------
def ClearCashFlowsResets(cashFlows, batchSize):
    batchIndexArray = GetBatchIndices(len(cashFlows), batchSize)
    for batchIndex in batchIndexArray:
        ClearCashFlowsResetsBatch(batchIndex, cashFlows)
#----------------------------------------------------------------------------
def ClearCashFlowsResetsBatch(batchIndex, cashFlows):
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            ClearCashFlowResets(cashFlows[index], None)
        acm.CommitTransaction()
    except Exception, e:
        acm.AbortTransaction()
        raise e
#----------------------------------------------------------------------------
def ClearPortfolioSwapResets(portfolioSwap, batchSize):
    legs = [l for l in portfolioSwap.Legs()]
    batchIndexArray = GetBatchIndices(len(legs), batchSize)
    for batchIndex in batchIndexArray:
        ClearPortfolioSwapResetsBatch(batchIndex, legs)
#----------------------------------------------------------------------------
def ClearPortfolioSwapResetsBatch(batchIndex, legs):
    try:
        acm.BeginTransaction()
        for index in batchIndex:
            ClearLegResets(legs[index], None)
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception("Failed to clear portfolio swap resets batch.")
        raise
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Portfolio Swap specific utility functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def ReturnLegFromList(securityLegs):
    return securityLegs[0]
#----------------------------------------------------------------------------
def FinancingLegFromList(securityLegs):
    return securityLegs[1]
#----------------------------------------------------------------------------
def RepoLegFromList(securityLegs):
    return securityLegs[2]
#----------------------------------------------------------------------------
def ExecutionFeeLegFromList(securityLegs):
    return securityLegs[3]
#----------------------------------------------------------------------------
def DividendLegsFromList(securityLegs):
    return securityLegs[4]
#----------------------------------------------------------------------------
def CallDepositLegFromList(securityLegs):
    return securityLegs[5]
#----------------------------------------------------------------------------
def ReturnCashFlowFromList(securityBaseCashFlows):
    return securityBaseCashFlows[0]
#----------------------------------------------------------------------------
def FundingCashFlowFromList(securityBaseCashFlows):
    return securityBaseCashFlows[1]
#----------------------------------------------------------------------------
def RepoCashFlowFromList(securityBaseCashFlows):
    return securityBaseCashFlows[2]
#----------------------------------------------------------------------------
def LegIsReturn(leg, isAel=True):
    if isAel:
        resetType = leg.reset_type
    else:
        resetType = leg.ResetType()
    if "Daily Return" == resetType:
        return True
    return False
#----------------------------------------------------------------------------
def LegIsFinancing(leg, returnLegIsPayLeg, isAel=True):
    if isAel:
        legType = leg.type
        resetType = leg.reset_type
        isPayLeg = leg.payleg
    else:
        legType = leg.LegType()
        resetType = leg.ResetType()
        isPayLeg = leg.PayLeg()
    if "Float" == legType and "Simple Overnight" == resetType and \
            isPayLeg != returnLegIsPayLeg:
        return True
    return False
#----------------------------------------------------------------------------
def LegIsExecutionFee(leg, returnLegIsPayLeg, isAel=True):
    if isAel:
        legType = leg.type
        creditRef = leg.credit_ref
        isPayLeg = leg.payleg
    else:
        legType = leg.LegType()
        creditRef = leg.CreditRef()
        isPayLeg = leg.PayLeg()
    if "Fixed" == legType and None == creditRef and isPayLeg != returnLegIsPayLeg:
        return True
    return False
#----------------------------------------------------------------------------
def LegIsRepo(leg, returnLegIsPayLeg, isAel=True):
    if isAel:
        legType = leg.type
        resetType = leg.reset_type
        isPayLeg = leg.payleg
    else:
        legType = leg.LegType()
        resetType = leg.ResetType()
        isPayLeg = leg.PayLeg()
    if "Float" == legType and "Simple Overnight" == resetType and \
            isPayLeg == returnLegIsPayLeg:
        return True
    return False
#----------------------------------------------------------------------------
def LegIsDividend(leg, isAel=True):
    if isAel:
        legType = leg.type
        creditRef = leg.credit_ref
    else:
        legType = leg.LegType()
        creditRef = leg.CreditRef()
    if "Fixed" == legType and None != creditRef:
        return True
    return False
#----------------------------------------------------------------------------
def LegIsCallDeposit(leg, isAel=True):
    if isAel:
        legType = leg.type
    else:
        legType = leg.LegType()
    return "Call Fixed" == legType
#----------------------------------------------------------------------------
def LegIsMargin(leg, returnLegIsPayLeg, isAel=True):
    if isAel:
        legType = leg.type
        creditRef = leg.credit_ref
        isPayLeg = leg.payleg        
    else:
        legType = leg.LegType()
        creditRef = leg.CreditRef()
        isPayLeg = leg.PayLeg()        
    if "Fixed" == legType and None == creditRef and isPayLeg == returnLegIsPayLeg:
        return True
    return False
#----------------------------------------------------------------------------
def IsPreviousFixingZero(aelCashFlow, \
                        fixingDate, \
                        resetType):
    previousFixing = GetPreviousFixing(aelCashFlow, resetType, fixingDate)
    if previousFixing and not previousFixing.value:
        return True
    return False
#----------------------------------------------------------------------------
def ClearLegResets(leg, fixingDate, excludeReturnResets=False):
    for cashFlow in leg.CashFlows():
        ClearCashFlowResets(cashFlow, fixingDate, excludeReturnResets)
#----------------------------------------------------------------------------
def ClearCashFlowResets(cashFlow, fixingDate, excludeReturnResets=False):
    #APO-36: funding becomes "Return" reset type on a "Float Rate" cash flow. This needs to be deleted as well.
    cashFlowType = cashFlow.CashFlowType()
    resets_to_delete = []
    for reset in cashFlow.Resets():
        if (not fixingDate) or (fixingDate and not acm.Time.DateDifference(fixingDate, reset.Day())):
            if reset.ResetType() == "Return" and excludeReturnResets and cashFlowType != "Float Rate":
                reset.ReadTime = 0
                reset.Commit()
            else:
                resets_to_delete.append(reset.Oid())
    for r in resets_to_delete:
        reset = acm.FReset[r]
        reset.Delete()
#----------------------------------------------------------------------------
def IsPeriodEndDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel=True):
    if not acm.Time.DateDifference(PeriodEndDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel), date):
        return True
    return False
#----------------------------------------------------------------------------    
# TTT
def IsBankingDayBeforePeriodEndDay(portfolioSwap, \
                                        rollingBaseDay, \
                                        isFixPeriod, \
                                        fixingDate, \
                                        calendar, \
                                        isAel=True):
    result = False
    if not calendar.IsNonBankingDay(None, None, fixingDate):
    
        date = acm.Time.DateAddDelta(fixingDate, 0, 0, 1)

        while not result and calendar.IsNonBankingDay(None, None, date):

            if IsPeriodEndDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel):
                result = True

            date = acm.Time.DateAddDelta(date, 0, 0, 1)    

    return result
#----------------------------------------------------------------------------
def PeriodEndDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel=True):
    openEnd = isAel and portfolioSwap.open_end or portfolioSwap.OpenEnd()
    if "Open End" == openEnd:
        if not rollingBaseDay:
            raise Exception("No rolling base day provided - Exits")
        
        rollingPeriod = isAel and acm.FPortfolioSwap[portfolioSwap.insaddr].NoticePeriod() or \
                                                        portfolioSwap.NoticePeriod()

        if rollingPeriod in ("0d", "0m", "0y"):
            raise Exception("Zero rolling period is not supported - Exits")
                
        periodEndDay = rollingBaseDay
        
        while acm.Time.DateDifference(date, periodEndDay) > 0:
            periodEndDay = acm.Time.DateAdjustPeriod(periodEndDay, rollingPeriod)
    else:
        periodEndDay = isAel and str(portfolioSwap.exp_day) or acm.Time.AsDate(portfolioSwap.ExpiryDate())
    return periodEndDay
#----------------------------------------------------------------------------
def PeriodStartDayClosed(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel=True):
    periodStartDay = IsPeriodEndDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel) \
                        and date or \
                        PeriodStartDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel)
    return periodStartDay
#----------------------------------------------------------------------------
def PeriodStartDay(portfolioSwap, rollingBaseDay, isFixPeriod, date, calendar, isAel=True):
    periodStartDay = isAel and str(portfolioSwap.start_day) or portfolioSwap.StartDate()
    openEnd = isAel and portfolioSwap.open_end or portfolioSwap.OpenEnd()
    
    if "Open End" == openEnd:
        periodEndDay = periodStartDay
        while acm.Time.DateDifference(date, periodEndDay) > 0:
            periodEndDay = PeriodEndDay(portfolioSwap, \
                                        rollingBaseDay, \
                                        isFixPeriod, \
                                        periodEndDay, \
                                        calendar, \
                                        isAel)
            if acm.Time.DateDifference(date, periodEndDay) > 0:
                periodStartDay = periodEndDay

            if not acm.Time.DateDifference(periodEndDay, periodStartDay):
                periodEndDay = acm.Time.DateAddDelta(periodEndDay, 0, 0, 1)
            else:
                break
    return periodStartDay
#----------------------------------------------------------------------------
def AdjustDateToOffsetMethod(date, calendar, paydayOffsetPeriod, paydayOffsetMethod):
    return calendar.ModifyDate(None, \
                                None, \
                                acm.Time.PeriodSymbolToRebasedDate(paydayOffsetPeriod, date), \
                                paydayOffsetMethod)
#----------------------------------------------------------------------------
def DayOffsetToDatePeriod(dayOffset):
    return "%sd" % str(dayOffset)
#----------------------------------------------------------------------------
def GetCorrespondingLeg(portfolioSwap, otherSwapLeg):
    legMatch = lambda leg : leg.LegType() == otherSwapLeg.LegType() and \
                            leg.PayLeg() == otherSwapLeg.PayLeg() and \
                            leg.IndexRef() == otherSwapLeg.IndexRef() and \
                            leg.CreditRef() == otherSwapLeg.CreditRef() and \
                            True or False
    matches = filter(legMatch, list(portfolioSwap.Legs()))
    if 1 != len(matches):
        raise Exception("Corresponding leg not found: LegType = %s, PayLeg = %s, IndexRef = %s, CreditRef = %s" \
                        % (otherSwapLeg.LegType(), \
                        otherSwapLeg.PayLeg(), \
                        otherSwapLeg.IndexRef() and otherSwapLeg.IndexRef().Name() or "", \
                        otherSwapLeg.CreditRef() and otherSwapLeg.CreditRef().Name() or ""))
    return matches[0]
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# General utility functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def GetEnum(enumType, enumValue):
    enums = acm.FEnumeration['enum(%s)' % enumType]
    assert enums != None, 'The enum-type could not be found in ACM.'
    return enums.Enumeration(enumValue)
#----------------------------------------------------------------------------
def GetAccounts(party, accountType, accountCurrency=None):
    query = acm.CreateFASQLQuery(acm.FAccount, 'AND')
    query.AddAttrNode('Party.Oid', 'EQUAL', party.Oid())
    query.AddAttrNode('AccountType', 'EQUAL', GetEnum('AccountType', accountType))
    if accountCurrency:
        query.AddAttrNode('Currency.Oid', 'EQUAL', accountCurrency.Oid())
    else:
        query.AddAttrNode('Currency.Oid', 'EQUAL', None)
    return query.Select()
#----------------------------------------------------------------------------
def GetAccount(party, currency=None):
    paymentAccount = None
    cashAccounts = GetAccounts(party, 'Cash', currency)
    for cashAccount in cashAccounts:
        paymentAccount = cashAccount
        break
    else:
        cashAndSecurityAccounts = GetAccounts(party, 'Cash and Security', currency)
        for cashAndSecurityAccount in cashAndSecurityAccounts:
            paymentAccount = cashAndSecurityAccount
            break
    return paymentAccount
#----------------------------------------------------------------------------
def GetPaymentAccount(party, paymentCurrency):
    account = GetAccount(party, paymentCurrency)
    if not account:
        account = GetAccount(party)
    return account
#----------------------------------------------------------------------------
def ImportModuleByName(moduleName):
    try:
        module = __import__(moduleName)
        if module:
            return module
        return None
    except Exception, e:
        raise Exception("Failed to import module '%s' - %s" % (str(moduleName), str(e)))
#----------------------------------------------------------------------------
def AppendListConditionally(destDictionary, \
                            sourceDictionary, \
                            key, \
                            require):
    value = None
    if sourceDictionary.has_key(key):
        value = sourceDictionary[key]
    elif require:
        raise Exception("Key not found: %s" % str(key))

    if None != value:
        if not destDictionary.has_key(key):
            list = []
            destDictionary[key] = list
        else:
            list = destDictionary[key]
        list.append(value)
#----------------------------------------------------------------------------
def GetValueConditionally(dictionary, key, require):
    if dictionary.has_key(key):
        return dictionary[key]
    elif require:
        raise Exception("Key not found in dictionary: %s" % str(key))
    return None
#----------------------------------------------------------------------------
def CheckValueConditionally(dictionary, key, require, raiseException=False):
    result = False
    if require:
        if dictionary.has_key(key):
            result = True
        elif raiseException:
            raise Exception("Required key not found '%s'" % str(key))
    else:
        result = True
    return result
#----------------------------------------------------------------------------
def IterFlattenRemoveNone(iterable):
    it = iter(iterable)
    for item in it:
        if isinstance(item, (list, tuple)):
            for innerItem in IterFlattenRemoveNone(item):
                if None != innerItem:
                    yield innerItem
        else:
            if None != item:
                yield item
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Error-check utility functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def AssertPaymentTypes(paymentTypeNames):
    additionalPayments = acm.FChoiceList.Select("name = 'Additional Payments'")
    additionalPaymentsChoiceList = 1 == len(additionalPayments) and additionalPayments[0] or None
    
    if not additionalPaymentsChoiceList:
        raise Exception("Choice list 'Additional Payments' not defined - Exits")
    for paymentTypeName in paymentTypeNames:
        paymentTypeChoices = [choice for choice in additionalPaymentsChoiceList.Choices() if \
                            paymentTypeName == choice.Name()]
        if 1 != len(paymentTypeChoices):
            raise Exception("Payment type '%s' not defined - Exits" % paymentTypeName)
#----------------------------------------------------------------------------
def CheckColumnDefinitions(colIds, context, raiseException=False):
    columnsDefined = True
    for colId in colIds:
        if None == context.GetDefinition(acm.FColumnDefinition, colId):
            columnsDefined = False
            LOGGER.warning("WARNING: Column '%s' is not defined. Some values may not be calculated correctly.", colId)
            if raiseException:
                raise Exception("ERROR: Column '%s' not found. Please install this column before running the script.", colId)
    return columnsDefined
#----------------------------------------------------------------------------
nanStr = str(acm.Math.NotANumber())
def CheckForNaN(value, fieldId, entityId, date, throwException=True):
    global nanStr
    if nanStr == str(value):
        if throwException:
            errMess = "NaN in input data for entity '%s', %s = %s (date: %s)"\
                                % (entityId, fieldId, str(value), str(date))
            LOGGER.error(errMess)
            raise Exception(errMess)
        return True
    return False
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Calc-API utility functions
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def CalculateSingleSheetValue(sheetType, \
                              sheetObject, \
                              colId, \
                              iteratorDepth, \
                              globalSimulations, \
                              localSimulations, \
                              columnConfig=None):
    context = acm.GetDefaultContext()
    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
    calcSpace.InsertItem(sheetObject)
    calcSpace.Refresh()
    ApplySimulations(calcSpace, globalSimulations, localSimulations)
    iterator = calcSpace.RowTreeIterator().FirstChild()
    for i in range(iteratorDepth):
        iterator = iterator.FirstChild()
    value = calcSpace.CalculateValue(iterator.Tree(), colId, columnConfig)
    RemoveSimulations(calcSpace, globalSimulations, localSimulations)
    return value
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
#----------------------------------------------------------------------------
def CalculateRowValueAsDouble(calcSpace, \
                                rowNode, \
                                colId, \
                                entityId=None, \
                                date=None, \
                                replaceNaNWithZero=False, \
                                columnConfig=None):
    try:
        rowValue = calcSpace.CalculateValue(rowNode, colId, columnConfig)
        if type(rowValue) not in (float, str, int):
            if rowValue.IsKindOf(acm.FDenominatedValue):
                rowValue = rowValue.Number()
            else:
                raise Exception("Calculated value from column %s could not be converted to a number: %s" \
                                    % (colId, str(rowValue)))
        if CheckForNaN(rowValue, colId, entityId, date, not replaceNaNWithZero):
            rowValue = 0.0
        return rowValue
    except Exception:
        LOGGER.exception("Failed to calculate row column value '%s', entity: '%s'.", colId, entityId)
        raise
#----------------------------------------------------------------------------
class PortfolioSwapParameters:
    def __init__(self, parameterDict):
        for (name, value) in parameterDict.items():
            setattr(self, name, value)
