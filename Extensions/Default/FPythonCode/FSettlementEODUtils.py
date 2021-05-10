""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementEODUtils.py"
import acm, os, amb
from FSettlementUtils import GetNonExcludedTrades
import FOperationsUtils as OpsUtils
from FSettlementProcessFunctions import CreateSettlementsFromTrade
import FSettlementStatusQueries as Queries
from FSettlementProcessEngineCreator import CreateSettlementProcessEngine
import time
from FSettlementEnums import SettlementStatus, RelationType, SettlementType
import FSettlementValidations as Validations
from   FSettlementCommitter import SettlementCommitter, CommitAction
from   FSettlementTransactionCommitter import TransactionCommitter
import FSettlementGetters as Getters
import FSettlementCalculations as Calculations
import FSettlementCreationFunctions as CreationFunctions
from FOperationsExceptions import CommitException, InvalidHookException
import FOperationsDateUtils as DateUtils

class EODSelector:

    def __init__(self, tradeFilterHandler):
        self.__defaultProcessTrades   = list()
        self.__amendmentProcessTrades = list()
        self.__tradeFilterHandler = tradeFilterHandler
        self.__acknowledgedQuery = self.__GetAcknowledgedQuery()
        self.__acknowledgedExcludingSecuritesQuery = self.__GetAcknowledgedExcludingSecurityQuery()
        self.__notAcknowledgedQuery = self.__GetNotAcknowledgedQuery()

    def GetDefaultProcessTrades(self):
        return self.__defaultProcessTrades

    def GetAmendmentProcessTrades(self):
        return self.__amendmentProcessTrades

    def SetDefaultProcessTrades(self, trades):
        self.__defaultProcessTrades = trades

    def SetAmendmentProcessTrades(self, trades):
        self.__amendmentProcessTrades = trades

    def GetTotalNumberOfTrades(self):
        return (len(self.__defaultProcessTrades) + len(self.__amendmentProcessTrades))

    def __GetAcknowledgedQuery(self):
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', OpsUtils.GetEnum("SettlementStatus", SettlementStatus.ACKNOWLEDGED))
        return query

    def __GetAcknowledgedExcludingSecurityQuery(self):
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', OpsUtils.GetEnum("SettlementStatus", SettlementStatus.ACKNOWLEDGED))
        query.AddAttrNode('Type', 'NOT_EQUAL', OpsUtils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_DVP))
        query.AddAttrNode('Type', 'NOT_EQUAL', OpsUtils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_NOMINAL))
        query.AddAttrNode('Type', 'NOT_EQUAL', OpsUtils.GetEnum('SettlementCashFlowType', SettlementType.END_SECURITY))
        query.AddAttrNode('Type', 'NOT_EQUAL', OpsUtils.GetEnum('SettlementCashFlowType', SettlementType.AGGREGATE_SECURITY))
        return query

    def __GetNotAcknowledgedQuery(self):
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', OpsUtils.GetEnum("SettlementStatus", SettlementStatus.NOT_ACKNOWLEDGED))
        return query

    def GetTradeFilterHandler(self):
        return self.__tradeFilterHandler

    def GetAcknowledgedQuery(self):
        return self.__acknowledgedQuery

    def GetAcknowledgedExcludingSecuritiesQuery(self):
        return self.__acknowledgedExcludingSecuritesQuery

    def GetNotAcknowledgedQuery(self):
        return self.__notAcknowledgedQuery

class RegeneratePaymentSelector(EODSelector):

    def __init__(self, userSelectedTrades, tradeFilterHandler, logger):
        EODSelector.__init__(self, tradeFilterHandler)
        self.__userSelectedTrades = userSelectedTrades
        self.__settlements = list()
        self.__settlementsSelected = False
        self.__logger = logger

    def __SelectSettlements(self):
        if (False == self.__settlementsSelected):
            for trade in self.GetDefaultProcessTrades():
                self.__settlements.extend(trade.Settlements())
            for trade in self.GetAmendmentProcessTrades():
                self.__settlements.extend(trade.Settlements())
            self.__settlementsSelected = True

    def SetUserSelectedTrades(self, userSelectedTrades):
        self.__userSelectedTrades = userSelectedTrades

    def GetUserSelectedTrades(self):
        return self.__userSelectedTrades

    def SelectTrades(self):
        nonExcludedTrades = GetNonExcludedTrades(self.__userSelectedTrades.SortByProperty('Oid', True))
        for trade in nonExcludedTrades:
            if self.GetTradeFilterHandler().IsTradeValidForDefaultProcessing(trade):
                self.GetDefaultProcessTrades().append(trade)
            elif self.GetTradeFilterHandler().IsTradeValidForAmendmentProcessing(trade):
                self.GetAmendmentProcessTrades().append(trade)
            else:
                self.__logger.LP_Log("Trade %d does not match trade filter and will not be considered for settlement processing." % trade.Oid())
                self.__logger.LP_Flush()
        self.__settlementsSelected = False

    def SelectSettlementsForSTP(self):
        self.__SelectSettlements()
        stpSettlements = list()
        query = Queries.GetPreReleasedStatusMaxDaysBackQuery()
        for settlement in self.__settlements:
            if query.IsSatisfiedBy(settlement):
                stpSettlements.append(settlement)
        return stpSettlements

    def SelectAcknowledgedSettlements(self):
        self.__SelectSettlements()
        ackSettlements = list()
        for settlement in self.__settlements:
            if self.GetAcknowledgedQuery().IsSatisfiedBy(settlement):
                ackSettlements.append(settlement)
        return ackSettlements

    def SelectNotAcknowledgedSettlements(self):
        self.__SelectSettlements()
        nakSettlements = list()
        for settlement in self.__settlements:
            if self.GetNotAcknowledgedQuery().IsSatisfiedBy(settlement):
                nakSettlements.append(settlement)
        return nakSettlements

    def SelectAcknowledgedExcludingSecuritiesSettlements(self):
        self.__SelectSettlements()
        ackSettlements = list()
        for settlement in self.__settlements:
            if self.GetAcknowledgedExcludingSecuritiesQuery().IsSatisfiedBy(settlement):
                ackSettlements.append(settlement)
        return ackSettlements




class EODProcessSelector(EODSelector):

    def __init__(self, tradeFilterHandler):
        EODSelector.__init__(self, tradeFilterHandler)

    def SelectTrades(self):
        defaultProcessTrades = self.GetTradeFilterHandler().GetDefaultProcessTrades()
        defaultProcessTrades.SortByProperty('Oid', True)
        self.SetDefaultProcessTrades(GetNonExcludedTrades(defaultProcessTrades))
        amendmentProcessTrades = self.GetTradeFilterHandler().GetAmendmentProcessTrades()
        amendmentProcessTrades.SortByProperty('Oid', True)
        self.GetAmendmentProcessTrades().extend(amendmentProcessTrades)

    def SelectSettlementsForSTP(self):
        return Queries.GetPreReleasedStatusMaxDaysBackQuery().Select()

    def SelectAcknowledgedSettlements(self):
        return self.GetAcknowledgedQuery().Select()

    def SelectAcknowledgedExcludingSecuritiesSettlements(self):
        return self.GetAcknowledgedExcludingSecuritiesQuery().Select()

    def SelectNotAcknowledgedSettlements(self):
        return self.GetNotAcknowledgedQuery().Select()

class EODParameters:
    def __init__(self, runEOD, ackToPc, excludePostSec, netParentCleanup, createOffsettingSettlements, handleRedemptionSecurities, totalNumberOfSteps, procedureName):
        self.runEOD = runEOD
        self.ackToPc = ackToPc
        self.excludePostSec = excludePostSec
        self.netParentCleanup = netParentCleanup
        self.createOffsettingSettlements = createOffsettingSettlements
        self.handleRedemptionSecurities = handleRedemptionSecurities
        self.totalNumberOfSteps = totalNumberOfSteps
        self.procedureName = procedureName

def StepCreateSettlements(eodSelector, procedureName, nettingRuleQueryCache, logger):
    defaultProcessMessage = '%s called CreateSettlementsFromTrade.' % procedureName
    amendmentProcessMessage = '%s called AmendmentProcess.' % procedureName
    eodSelector.SelectTrades()
    totalNumberOfTrades = eodSelector.GetTotalNumberOfTrades()
    i = 0
    settlementProcessEngine = CreateSettlementProcessEngine(logger, nettingRuleQueryCache)


    for trade in eodSelector.GetDefaultProcessTrades():
        i = i + 1
        logger.LP_Log("Processing trade %d (%d of %d)" % (trade.Oid(), i, totalNumberOfTrades))
        logger.LP_Flush()
        try:
            CreateSettlementsFromTrade(trade, defaultProcessMessage, nettingRuleQueryCache)
        except InvalidHookException as error:
            logger.LP_Log("Failed to process Trade with id {}".format(trade.Oid()))
            logger.LP_Log(error)
            logger.LP_Flush()
    for trade in eodSelector.GetAmendmentProcessTrades():
        i = i + 1
        logger.LP_Log("Processing trade %d (%d of %d)" % (trade.Oid(), i, totalNumberOfTrades))
        logger.LP_Flush()
        generator = acm.FAMBAMessageGenerator()
        ambaBuffer = amb.mbf_create_buffer_from_data(str(generator.Generate(trade)))
        ambaMessage = ambaBuffer.mbf_read()
        settlementProcessEngine.Process(ambaMessage, trade)

def StepSTP(eodSelector, logger):
    RunSTPOnSettlements(eodSelector.SelectSettlementsForSTP(), logger)

def StepPostReleasedToPendingClosure(eodSelector, excludePostSec, logger):
    if excludePostSec:
        ackSettlements = eodSelector.SelectAcknowledgedExcludingSecuritiesSettlements()
    else:
        ackSettlements = eodSelector.SelectAcknowledgedSettlements()
    SetAcknowledgedToPendingClosure(ackSettlements, logger)

def StepNotAcknowledgedToException(eodSelector, logger):
    nakSettlements = eodSelector.SelectNotAcknowledgedSettlements()
    SetNotAcknowledgedToException(nakSettlements, logger)

def StepCreateOffsettingSettlementsForPartiallySettledTrades(eodSelector, nettingRuleQueryCache, logger):
    if eodSelector.GetTotalNumberOfTrades() == 0:
        eodSelector.SelectTrades()
    trades = eodSelector.GetDefaultProcessTrades()
    totalNumberOfTrades = len(trades)
    i = 0
    for trade in trades:
        i = i + 1
        logger.LP_Log("Processing trade %d (%d of %d)" % (trade.Oid(), i, totalNumberOfTrades))
        logger.LP_Flush()
        CreateOffsettingSettlementsForPartiallySettledTrades(trade, nettingRuleQueryCache, logger)

def StepHandleRedemptionSecurities(eodSelector, logger):
    if eodSelector.GetTotalNumberOfTrades() == 0:
        eodSelector.SelectTrades()
    trades = eodSelector.GetDefaultProcessTrades()
    totalNumberOfTrades = len(trades)
    i = 0
    for trade in trades:
        i = i + 1
        logger.LP_Log("Processing trade %d (%d of %d)" % (trade.Oid(), i, totalNumberOfTrades))
        logger.LP_Flush()
        HandleRedemptionSecurities(trade, logger)

def RunSTPOnSettlements(settlements, logger):
    for s in settlements:
        if s.IsValidForSTP():
            logger.LP_Log("Running STP on settlement %d" % s.Oid())
            logger.LP_Flush()
            clone = s.Clone()
            clone.STP()
            s.Apply(clone)
            try:
                s.Commit()
            except Exception as error:
                logger.LP_Log("Error: Failed to run STP on settlement %d. %s" % (s.Oid(), error))
                logger.LP_Flush()

def SetAcknowledgedToPendingClosure(settlements, logger):
    for s in settlements:
        logger.LP_Log("Changing status on settlement %d from Acknowledged to Pending Closure" % s.Oid() )
        logger.LP_Flush()
        clone = s.Clone()
        clone.Status (SettlementStatus.PENDING_CLOSURE)
        s.Apply(clone)
        try:
            s.Commit()
        except Exception as error:
            logger.LP_Log("Error: Failed to set status on settlement %d. %s" % (s.Oid(), error))
            logger.LP_Flush()

def SetNotAcknowledgedToException(settlements, logger):
    for s in settlements:
        logger.LP_Log("Changing status on settlement %d from Not Acknowledged to Exception" % s.Oid())
        logger.LP_Flush()
        clone = s.Clone()
        clone.Status (SettlementStatus.EXCEPTION)
        s.Apply(clone)
        try:
            s.Commit()
        except Exception as error:
            logger.LP_Log("Error: Failed to set status on settlement %d. %s" % (s.Oid(), error))
            logger.LP_Flush()

def NetParentCleanup(logger):
    query = Queries.GetNetParentsQuery()
    resultSet = query.Select()
    for netParent in resultSet:
        netChildren = netParent.Children()
        numOfChildren = len(netChildren)
        if numOfChildren == 0:
            try:
                SettlementCommitter(netParent, CommitAction.DELETE).Commit()
            except Exception as exceptionString:
                logger.LP_Log('Could not delete net parent %d. Cause: %s' % (netParent.Oid(), exceptionString))
                logger.LP_Flush()
        elif numOfChildren == 1:
            netChild = netChildren.First()
            netChild.Status(SettlementStatus.EXCEPTION)
            netChild.Parent(None)
            if netChild.IsValidForSTP():
                netChild.STP()
            try:
                netChild.Commit()
                try:
                    SettlementCommitter(netParent, CommitAction.DELETE).Commit()
                except Exception as exceptionString:
                    logger.LP_Log('Could not delete net parent %d. Cause: %s' % (netParent.Oid(), exceptionString))
                    logger.LP_Flush()
            except Exception as exceptionString:
                logger.LP_Log('Could not delete net child %d. Cause: %s' % (netChild.Oid(), exceptionString))
                logger.LP_Flush()

def CreateOffsettingSettlementsForPartiallySettledTrades(trade, nettingRuleQueryCache, logger):
    instrument = trade.Instrument().Underlying() or trade.Instrument()
    committerList = list()
    if not Validations.TradeFullySettledOnDate(trade, acm.Time.DateToday()) and not trade.PrimaryIssuance():
        if not Validations.IsThereAtLeastOnePostReleasedOffsettingSettlement(trade.Settlements()):
            settledAmount, totalAmount = Calculations.CalculateSettledAmountOnDate(trade, acm.Time.DateToday())
            offsettingAmountFactor, offsettingTransferAmountFactor = Calculations.CalculateAmountFactor(settledAmount, totalAmount, trade)
            if offsettingAmountFactor != None and offsettingTransferAmountFactor != None:
                calendar = instrument.Currency().Calendar()
                committerList.extend(DeleteOutDatedOffsettingSettlements(trade))
                for leg in instrument.Legs():
                    for cashFlow in leg.CashFlows():
                        nextBusinessDay = DateUtils.AdjustDateToday(calendar, 1)
                        if Validations.IsCashflowThatShouldBeOffsetted(cashFlow, instrument) \
                           and Validations.IsDateInInterval(cashFlow.ExCouponDate(), acm.Time.DateToday(), nextBusinessDay):
                            settlement, committerListTemp = GetAffectedSettlement(trade, cashFlow, logger)
                            if settlement and Getters.GetSettlementTransferTypeFromSettlementType(settlement.Type()) != SettlementType.NONE:
                                topSettlement = settlement.GetTopSettlementInHierarchy()
                                if topSettlement.IsPreReleased():
                                    committerList.extend(committerListTemp)
                                    committerList.extend(CreationFunctions.CreateOffsettingSettlementAndTransfer(settlement, offsettingAmountFactor, offsettingTransferAmountFactor, cashFlow))
                                else:
                                    logger.LP_Log('Skipping creation of offsetting settlements because settlement {} is not pre released'.format(settlement.Oid()))
                                    logger.LP_Flush()
                            else:
                                logger.LP_Log('Skipping creation of offsetting settlements for cashflow {} of type {} for trade {}'.format(cashFlow.Oid(), cashFlow.CashFlowType(), trade.Oid()))
                                logger.LP_Flush()
                tc  = TransactionCommitter(committerList, None, nettingRuleQueryCache)
                try:
                    tc.CommitSettlements()
                except CommitException as error:
                    logger.LP_Log('Error while committing new settlements: {} for trade {}'.format(str(error), trade.Oid()))
                    logger.LP_Flush()
        else:
            logger.LP_Log('Skipping trade {} due to existing post released offsetting settlement(s)'.format(trade.Oid()))
            logger.LP_Flush()


def DeleteOutDatedOffsettingSettlements(trade):
    committerList = list()
    for settlement in trade.Settlements():     
        if Validations.IsCreatedDueToPartiallySettledTrade(settlement):
            if settlement.Parent() and settlement.Parent().RelationType() == RelationType.NONE and settlement.Parent().IsPreReleased():
                committerList.append(SettlementCommitter(settlement.Parent(), CommitAction.DELETE))
            committerList.append(SettlementCommitter(settlement, CommitAction.DELETE))
    return committerList

def GetAffectedSettlement(trade, cashFlow, logger):
    committerList = list()
    affectedSettlement = None
    if Validations.IsAfterMaturity(trade.Instrument()):
        committerListTemp, affectedSettlement = CreationFunctions.CreateSettlementsAfterMaturity(trade, cashFlow, logger)
        committerList.extend(committerListTemp)
    else:
        try:
            settlements = acm.FSettlement.Select('cashFlow = {} and trade = {}'.format(cashFlow.Oid(), trade.Oid()))
            settlementTypes = [settlement.Type() for settlement in settlements]
            if len(settlements) == 0 or any(settlementTypes.count(settlementType) > 1 for settlementType in settlementTypes):
                logger.LP_Log("Could not identify a settlement to offset for cashflow {} and trade {}".format(cashFlow.Oid(), trade.Oid()))
                logger.LP_Flush()
            else:
                for settlement in settlements:
                    if not settlement.IsSecurity() and not Validations.IsTransferType(settlement.Type()):
                        affectedSettlement = settlement
                        break
        except RuntimeError as e:
            logger.LP_Log("Error trying to select settlements for trade {}".format(trade.Oid()))
            logger.LP_Flush()
    return affectedSettlement, committerList

def HandleRedemptionSecurities(trade, logger):
    for settlement in trade.Settlements().AsArray():
        if settlement.Type() == SettlementType.REDEMPTION_SECURITY and \
           settlement.ValueDay() <= acm.Time.DateToday() and \
           settlement.Status() == SettlementStatus.AUTHORISED:
                settledAmount, totalAmount = Calculations.CalculateSettledAmountOnDate(trade, acm.Time.DateToday())
                settledFactor = settledAmount / totalAmount
                if settledFactor == 0:
                    break
                elif settledFactor == 1:
                    __SetSettledData(settlement)
                else:
                    if settlement.PartialParent():
                        partialParent = Getters.FindTopmostPartialParent(settlement)
                        originalAmount = partialParent.Amount()
                        totalPartialSettled = Getters.TotalSettledAmount(Getters.AllPartialChildren(partialParent))
                        if abs(settledFactor*originalAmount - totalPartialSettled) < 10e-6:
                            #Nothing new has been settled
                            break
                        amountToSettle = settledFactor*originalAmount - totalPartialSettled
                    else:
                        amountToSettle = settlement.Amount()*settledFactor
                    partialSettlement = acm.FPartialSettlement(settlement, amountToSettle)
                    partialSettlement.Execute()
                    acm.BeginTransaction()
                    try:
                        result = partialSettlement.CommitResult()
                        childToSettle = Getters.GetSettlementWithAmount(result.InsertedSettlements(), amountToSettle)
                        __SetSettledData(childToSettle)
                        acm.CommitTransaction()
                    except CommitException as e:
                        acm.AbortTransaction()
                        logger.LP_Log('Error while committing new settlements: {} for trade {}'.format(str(e), trade.Oid()))
                        logger.LP_Flush()

def __SetSettledData(settlement):
    settlement.Status(SettlementStatus.ACKNOWLEDGED)
    acm.Operations.SetSettledDataOnHierarchy(settlement, settlement.ValueDay(), settlement.CashAmount(), settlement.Amount())
    settlement.Commit()

def RunEODSteps(eodSelector, eodParameters, nettingRuleQueryCache, logger):
    totSteps = eodParameters.totalNumberOfSteps
    procedureName = eodParameters.procedureName
    currentStep = 0
    logger.LP_Log("===========================================================================")
    logger.LP_Log(">> Starting {} at {}".format(procedureName, time.asctime(time.localtime())))
    logger.LP_Log("===========================================================================")
    logger.LP_Flush()

    currentStep += 1
    if eodParameters.runEOD:
        logger.LP_Log(">> Step {} of {} - Creating new settlements...\n".format(currentStep, totSteps))
        logger.LP_Flush()
        StepCreateSettlements(eodSelector, procedureName, nettingRuleQueryCache, logger)
    else:
        logger.LP_Log(">> Skipping step {} of {} - Creating new settlements...\n".format(currentStep, totSteps))
        logger.LP_Flush()
    
    currentStep += 1
    logger.LP_Log(">> Step {} of {} - Running STP...\n".format(currentStep, totSteps))
    logger.LP_Flush()
    StepSTP(eodSelector, logger)
    
    currentStep += 1
    if eodParameters.ackToPc:
        logger.LP_Log(">> Step {} of {} - Setting post released settlements to status Pending Closure...\n".format(currentStep, totSteps))
        logger.LP_Flush()
        StepPostReleasedToPendingClosure(eodSelector, eodParameters.excludePostSec, logger)
    else:
        logger.LP_Log(">> Skipping step {} of {} - Setting settlements in status Acknowledged to status Pending Closure...\n".format(currentStep, totSteps))
        logger.LP_Flush()
    
    currentStep += 1
    logger.LP_Log(">> Step {} of {} - Setting settlements in status Not Acknowledged to status Exception...\n".format(currentStep, totSteps))
    logger.LP_Flush()
    StepNotAcknowledgedToException(eodSelector, logger)
    

    if eodParameters.netParentCleanup:
        currentStep += 1
        logger.LP_Log(">> Step {} of {} - Checking for incorrect net structures...\n".format(currentStep, totSteps))
        logger.LP_Flush()
        NetParentCleanup(logger)
    
    currentStep += 1
    if eodParameters.createOffsettingSettlements:
        logger.LP_Log(">> Step {} of {} - Creating offsetting settlements for not fully settled trades...\n".format(currentStep, totSteps))
        logger.LP_Flush()
        StepCreateOffsettingSettlementsForPartiallySettledTrades(eodSelector, nettingRuleQueryCache, logger)
    else:
        logger.LP_Log(">> Skipping step {} of {} - Creating offsetting settlements for not fully settled trades...\n".format(currentStep, totSteps))
        logger.LP_Flush()

    currentStep += 1
    if eodParameters.handleRedemptionSecurities:
        logger.LP_Log(">> Step {} of {} - Setting redemption security to Settled...\n".format(currentStep, totSteps))
        logger.LP_Flush()
        StepHandleRedemptionSecurities(eodSelector, logger)
    else:
        logger.LP_Log(">> Skipping step {} of {} - Setting redemption security to Settled...\n".format(currentStep, totSteps))
        logger.LP_Flush()


    logger.LP_Log("===========================================================================")
    logger.LP_Log(">> {} has finished at {}".format(procedureName, time.asctime(time.localtime())))
    logger.LP_Log("===========================================================================")
    logger.LP_Flush()

