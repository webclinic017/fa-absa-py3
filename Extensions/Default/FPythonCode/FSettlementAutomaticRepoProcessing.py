""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/scripts/FSettlementAutomaticRepoProcessing.py"
import acm
import FRunScriptGUI

import FSettlementValidations as Validations
from   FSettlementCommitter import SettlementCommitter, CommitAction
from   FSettlementTransactionCommitter import TransactionCommitter
from FOperationsLoggers import CreateLogger
from   FSettlementEnums import RelationType, SettlementType
from FSettlementSecurityProcessEngine import SecurityProcessEngine
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator
from FSettlementCommitterFunctions import CommitCommitters, RunSTPAndUpdateStateChart
import FSettlementHierarchyFunctions as HierarchyFunctions
from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache
from FOperationsExceptions import CommitException


class SettlementAutomaticRepoProcessingGUI(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)


    def __CreateAelVariables(self):
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        op = query.AddOpNode('AND')
        op.AddAttrNode('Oid', 'GREATER_EQUAL', None)
        op.AddAttrNode('Oid', 'LESS_EQUAL', None)
        op2 = query.AddOpNode('OR')
        op2.AddAttrNode('Status', 'EQUAL', None)
        op3 = query.AddOpNode('OR')
        op3.AddAttrNode('Acquirer.Name', 'EQUAL', None)
        op4 = query.AddOpNode('OR')
        op4.AddAttrNode('Counterparty.Name', 'EQUAL', None)
        op5 = query.AddOpNode('AND')
        op5.AddAttrNode('ValueDay', 'GREATER_EQUAL', None)
        op5.AddAttrNode('ValueDay', 'LESS_EQUAL', None)

        ttTradeSelection = 'Trade Selection'
        aelVariables=[['trades', 'Trades to process', 'FTrade', None, query, 0, 1, ttTradeSelection]]
        return aelVariables

#---------------Update Value Day-----------------------------------------
def UpdateValueDayForSettlements(trades, dateToday, logger, nettingRuleQueryCache):
    for trade in trades:
        calendar = trade.Instrument().Currency().Calendar()
        nextDay = acm.Time.DateAddDelta(dateToday, 0, 0, 1)
        dayToAdjustTo = calendar.ModifyDate(calendar, None, nextDay, 1)

        committerList = list()
        for settlement in trade.Settlements():
            topSettlement = settlement.GetTopSettlementInHierarchy()
            if Validations.IsActiveSecurity(topSettlement) and not topSettlement.Type() == SettlementType.REDEMPTION_SECURITY \
               and not topSettlement.IsSettled() and settlement.ValueDay() <= dateToday and Validations.IsPartOfPartial(topSettlement):
                SecurityProcessEngine.ProcessPartial(topSettlement.PartialParent(), committerList)
                break
        transactionCommitter = TransactionCommitter(committerList, None, nettingRuleQueryCache)
        try:
            transactionCommitter.CommitSettlements()
        except CommitException as error:
            logger.LP_Log("Error processing partial hierarchy for trade {} received error: {}".format(trade.Oid(), error))
            logger.LP_Flush()

        committerList = list()
        for settlement in trade.Settlements():
            topSettlement = settlement.GetTopSettlementInHierarchy()
            if topSettlement.IsSecurity() and not topSettlement.Type() == SettlementType.REDEMPTION_SECURITY and topSettlement.IsPreReleased() and \
               settlement.ValueDay() <= dateToday and settlement.RelationType() == RelationType.NONE and \
               not topSettlement.PartialParent():
                if not Validations.IsCancelOrCorrectSettlement(topSettlement):
                    if settlement.Parent() and settlement.Parent().RelationType() == RelationType.VALUE_DAY_ADJUSTED:
                        adjustedParent = settlement.Parent()
                        pair = acm.Operations.Actions().UpdateValueDay(settlement.Clone(), adjustedParent.Clone(), dayToAdjustTo)
                        adjustedSettlement = pair.First()
                        adjustedParentClone = pair.Second()
                        RunSTPAndUpdateStateChart(adjustedParentClone)
                        adjustedParent.Apply(adjustedParentClone)
                        committerList.append(SettlementCommitter(adjustedParent, CommitAction.UPDATE))
                    else:
                        pair = acm.Operations.Actions().UpdateValueDay(settlement.Clone(), None, dayToAdjustTo)
                        adjustedSettlement = pair.First()
                        adjustedParent = pair.Second()
                        adjustedSettlement.Parent(adjustedParent)
                        RunSTPAndUpdateStateChart(adjustedParent)
                        settlement.Apply(adjustedSettlement)
                        committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))
                        committerList.append(SettlementCommitter(adjustedParent, CommitAction.INSERT))
                else:
                    logger.LP_Log("Skipping updating value date for settlement {} because it is waiting for cancellation".format(settlement.Oid()))
                    logger.LP_Flush()
        transactionCommitter = TransactionCommitter(committerList, None, nettingRuleQueryCache)
        try:
            transactionCommitter.CommitSettlements()
        except CommitException as error:
            logger.LP_Log("Error updating value date for trade {} received error: {}".format(trade.Oid(), error))
            logger.LP_Flush()


#---------------Automatic Pair Off-----------------------------------------
def AutomaticallyPairOffSettlements(trades, dateToday, logger, nettingRuleQueryCache):
    topSettlementsEligibleForPairOffTomorrow = __TopSettlementsEligibleForPairOffTomorrow(trades, dateToday)
    for topSettlementEligibleForPairOffTomorrow in topSettlementsEligibleForPairOffTomorrow:
        settlementsEligibleForPairOffTomorrow = set()
        for childSettlement in topSettlementEligibleForPairOffTomorrow.Children():
            if childSettlement.IsSecurity():
               settlementsEligibleForPairOffTomorrow.add(childSettlement)
        settlementsToPairOff = GetHookAdministrator().HA_CallHook(SettlementHooks.DECIDE_SETTLEMENTS_TO_PAIR_OFF, settlementsEligibleForPairOffTomorrow)
        if len(settlementsToPairOff) > 0:
            pairOffOk = True
            while len(settlementsToPairOff) > 0 and pairOffOk:
                theRealSettlementsToPairOff = __HandleUnNettingOfSettlements(settlementsToPairOff, logger)
                if theRealSettlementsToPairOff:
                    pairOffOk, insertedLeftOverSecurity = __PerformPairOffSettlements(theRealSettlementsToPairOff, logger, nettingRuleQueryCache)
                settlementsEligibleForPairOffTomorrow = settlementsEligibleForPairOffTomorrow - set(settlementsToPairOff)
                if insertedLeftOverSecurity:
                    settlementsEligibleForPairOffTomorrow.add(insertedLeftOverSecurity)
                if not pairOffOk and len(settlementsEligibleForPairOffTomorrow) > 0:
                    firstSecurity = settlementsEligibleForPairOffTomorrow.pop()
                    __ReNetSettlements(firstSecurity, nettingRuleQueryCache)
                if pairOffOk:
                    settlementsToPairOff = GetHookAdministrator().HA_CallHook(SettlementHooks.DECIDE_SETTLEMENTS_TO_PAIR_OFF, settlementsEligibleForPairOffTomorrow)
        else:
            logger.LP_Log("Nothing to pair off")
            logger.LP_Flush()

def __ReNetSettlements(settlement, nettingRuleQueryCache):
    if settlement.Parent() and settlement.Parent().RelationType() == RelationType.VALUE_DAY_ADJUSTED:
        settlement = settlement.Parent()
    committerList = [SettlementCommitter(settlement, CommitAction.UPDATE)]
    transactionCommitter = TransactionCommitter(committerList, None, nettingRuleQueryCache)
    try:
        transactionCommitter.CommitSettlements()
    except CommitException as error:
        logger.LP_Log("Error while netting remaining settlements, received error: {}".format(error))
        logger.LP_Flush()

def __TopSettlementsEligibleForPairOffTomorrow(trades, dateToday):
    topSettlementEligibleForPairOffTomorrow = set()
    for trade in trades:
        calendar = trade.Instrument().Currency().Calendar()
        nextDay = acm.Time.DateAddDelta(dateToday, 0, 0, 1)
        nextBusinessDay = calendar.ModifyDate(calendar, None, nextDay, 1)
        for settlement in trade.Settlements():
            topSettlement = settlement.GetTopNonCancellationSettlementInHierarchy()
            if not topSettlement.Type() == SettlementType.REDEMPTION_SECURITY and topSettlement.IsPreReleased() and \
               topSettlement.ValueDay() == nextBusinessDay:
               topSettlementEligibleForPairOffTomorrow.add(topSettlement)
    return topSettlementEligibleForPairOffTomorrow

def __HandleUnNettingOfSettlements(settlementsToPairOff, logger):
    toBePairedOffTrades = list({settlementTemp.Trade() for settlementTemp in settlementsToPairOff})
    theRealSettlementsToPairOff = set()
    committerList = list()
    handledSettlements = list()
    for settlement in settlementsToPairOff:
        topSettlement = settlement.GetTopNonCancellationSettlementInHierarchy()
        if topSettlement not in handledSettlements:
            handledSettlements.append(topSettlement)
            if topSettlement.IsSystemNet():
                okSettlements, problematicSettlements = HierarchyFunctions.FilterOutSettlementsByTrade(topSettlement.Children(), toBePairedOffTrades)
                okParent, problematicParent, committerListTemp, cleanUp = HierarchyFunctions.DecideParentsForChildren(okSettlements, problematicSettlements, topSettlement)
                committerList.extend(committerListTemp)
                settlementToPairOff = HierarchyFunctions.CreateNetHierarchy(okParent, okSettlements, committerList)
                HierarchyFunctions.CreateNetHierarchy(problematicParent, problematicSettlements, committerList)
                theRealSettlementsToPairOff.add(settlementToPairOff)
                committerList.extend(cleanUp)
            else:
                theRealSettlementsToPairOff.add(topSettlement)

    if CommitCommitters(committerList, logger):
        return theRealSettlementsToPairOff
    else:
        return list()

def __PerformPairOffSettlements(theRealSettlementsToPairOff, logger, nettingRuleQueryCache):
    resultOK = True
    insertedLeftOverSecurity = None
    try:
        theRealSettlementsToPairOff = list(theRealSettlementsToPairOff)
        firstSettlement = theRealSettlementsToPairOff[0]
        pairOffSettlements = acm.FPairOffSettlements([theRealSettlementsToPairOff, firstSettlement.AcquirerAccountRef(), firstSettlement.CounterpartyAccountRef()])
        pairOffSettlements.Execute()
        result = pairOffSettlements.CommitResult()
        committerList = list()
        for settlement in result.InsertedSettlements():
            if settlement.PairOffParent() and not settlement.IsPairedOff():
                if settlement.Parent() and settlement.Parent().RelationType() == RelationType.VALUE_DAY_ADJUSTED:
                    committerList.append(SettlementCommitter(settlement.Parent(), CommitAction.UPDATE))
                else:
                    committerList.append(SettlementCommitter(settlement, CommitAction.UPDATE))
                if settlement.IsSecurity():
                    insertedLeftOverSecurity = settlement

        transactionCommitter = TransactionCommitter(committerList, None, nettingRuleQueryCache)
        transactionCommitter.CommitSettlements()

    except TypeError as e:
        resultOK = False
        logger.LP_Log("Pair Off Settlements not allowed on settlements returned by DecideSettlementsToPairOff")
        logger.LP_Flush()
    except CommitException as error:
        resultOK = False
        logger.LP_Log("Error while netting leftover settlements received error: {}".format(error))
        logger.LP_Flush()
    return resultOK, insertedLeftOverSecurity


#---------------Main-----------------------------------------
def ael_main(parameters):
    trades = parameters["trades"]
    logger = CreateLogger(True, False, True, '', '')
    nettingRuleQueryCache = SettlementNettingRuleQueryCache()
    logger.LP_Log("-------------------------------------------")
    logger.LP_Log("Started updating settlement valuedays.\n")
    logger.LP_Flush()
    UpdateValueDayForSettlements(trades, acm.Time.DateToday(), logger, nettingRuleQueryCache)
    logger.LP_Log("\nFinished updating settlement valuedays.")
    logger.LP_Log("-------------------------------------------")
    logger.LP_Flush()

    logger.LP_Log("\nStarted automatic Pair Off Settlements.")
    logger.LP_Log("-------------------------------------------")
    logger.LP_Flush()
    AutomaticallyPairOffSettlements(trades, acm.Time.DateToday(), logger, nettingRuleQueryCache)
    logger.LP_Log("\nFinished automatic Pair Off Settlements.")
    logger.LP_Log("-------------------------------------------")
    logger.LP_Flush()
ael_gui_parameters = {
                      'runButtonLabel' : 'Run',
                      'hideExtraControls' : False,
                      'windowCaption' : 'Automatic Repo Processing',
                      'version' : '%R%'
                      }

ael_variables = SettlementAutomaticRepoProcessingGUI()
