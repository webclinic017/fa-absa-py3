""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEngineBaseCreator.py"

import acm

# operations
from FOperationsFilter import Filter
from FOperationsDateUtils import AdjustDateToday, GetAccountingCurrencyCalendar
from FOperationsOperationValidator import OperationValidator
from FOperationsTransactionWriter import TransactionWriter
from FOperationsTransactionCommitter import TransactionCommitter
from FOperationsResultCounter import ResultCounter
from FOperationsTaskConfiguration import Configuration
from FOperationsTransactionModifiers import SortingTransactionModifier

# accounting
from FAccountingAmendmentManager import AmendmentManager
from FAccountingEngineBase import AccountingEngine
from FAccountingHookAdministrator import GetHookAdministrator, AccountingHooks
from FAccountingObjectCreator import AccountingCreator
from FAccountingOperations import Operation, GetOperations
from FAccountingSorting import SortOrderDefaultTup
from FAccountingObjectModifier import AccountingObjectModifier

import FAccountingQueriesBase as Queries


#-------------------------------------------------------------------------
def CreateParameters(startDate=None, endDate=None, endOfDayDate=None, processDate=None, \
                     bookFilter=None, bookLinkFilter=None, treatmentLinkFilter=None):

    import FAccountingParams as Params

    params = dict()
    params['startDate'] = startDate if startDate else AdjustDateToday(GetAccountingCurrencyCalendar(), -Params.daysBack)
    params['endDate'] = endDate if endDate else AdjustDateToday(GetAccountingCurrencyCalendar(), Params.daysForward)
    params['endOfDayDate'] = endOfDayDate if endOfDayDate else acm.Time.DateToday()
    params['processDate'] = processDate if processDate else acm.Time.DateToday()
    params['bookFilter'] = bookFilter
    params['bookLinkFilter'] = bookLinkFilter
    params['treatmentLinkFilter'] = treatmentLinkFilter
    params['inheritProtection'] = Params.setProtectionAndOwnerFromTrade
    params['createZeroAmountJournals'] = Params.createZeroAmountJournals
    params['detailedLog'] = Params.detailedLogging
    return params

#-------------------------------------------------------------------------
def CreateCommonInterfaces(hookAdmin, params, committerIF=None):

    #-------------------------------------------------------------------------
    validationEngines = dict()

    if params.preventJournalCreationQueries:

        validationEngine = OperationValidator(acm.FJournal, {Operation.CREATE : params.preventJournalCreationQueries})
        validationEngines['FJournal'] = validationEngine

    #-------------------------------------------------------------------------
    committer = committerIF if committerIF != None else TransactionCommitter(GetOperations(), ResultCounter)

    if hookAdmin.HA_IsCustomHook(AccountingHooks.GET_COMMIT_JOURNAL_LOG_MSG):
        committer.CO_RegisterLogHook('FJournal', AccountingHooks.GET_COMMIT_JOURNAL_LOG_MSG)

    #-------------------------------------------------------------------------
    objectModifier = AccountingObjectModifier()

    if hookAdmin.HA_IsCustomHook(AccountingHooks.JOURNAL_MODIFICATION):
        objectModifier.RegisterModificationHook('FJournal', AccountingHooks.JOURNAL_MODIFICATION, ['CustomType'])

    if hookAdmin.HA_IsCustomHook(AccountingHooks.JOURNAL_INFORMATION_MODIFICATION):
        objectModifier.RegisterModificationHook('FJournalInformation', AccountingHooks.JOURNAL_INFORMATION_MODIFICATION, [])

    #-------------------------------------------------------------------------
    transactionModifier = SortingTransactionModifier(SortOrderDefaultTup)

    #-------------------------------------------------------------------------
    transactionWriter = TransactionWriter(committer, transactionModifier)

    configuration = dict()
    configuration['validatorsIF'] = validationEngines
    configuration['objectModifierIF'] = objectModifier
    configuration['writerIF'] = transactionWriter
    configuration['hookAdminIF'] = hookAdmin
    return configuration

#-------------------------------------------------------------------------
def CreateTradeFilter():
    import FAccountingParams as Params

    hookAdmin = GetHookAdministrator(Params.hooks, 'FAccountingHooksTemplate')

    validTradeCb = None
    if hookAdmin.HA_IsCustomHook(AccountingHooks.IS_VALID_TRADE):
        validTradeCb = hookAdmin.GetHook(AccountingHooks.IS_VALID_TRADE)

    tradesForEodCb = None
    if hookAdmin.HA_IsCustomHook(AccountingHooks.GET_TRADES_FOR_EOD):
        tradesForEodCb = hookAdmin.GetHook(AccountingHooks.GET_TRADES_FOR_EOD)

    return Filter(acm.FTrade, Params.tradeFilterQueries, None, validTradeCb, tradesForEodCb)

#-------------------------------------------------------------------------
def CreateSettlementFilter():
    import FAccountingParams as Params

    hookAdmin = GetHookAdministrator(Params.hooks, 'FAccountingHooksTemplate')
    settlementsForEodCb = None
    if hookAdmin.HA_IsCustomHook(AccountingHooks.GET_SETTLEMENTS_FOR_EOD):
        settlementsForEodCb = hookAdmin.GetHook(AccountingHooks.GET_SETTLEMENTS_FOR_EOD)

    return Filter(acm.FSettlement, Params.settlementFilterQueries, None, None, settlementsForEodCb)

#-------------------------------------------------------------------------
def CreateEngineForTrades(params, logger, committerIF=None, isSupportedObjectCb=None, useHook=True):
    import FAccountingParams as Params

    hookAdmin = GetHookAdministrator(Params.hooks, 'FAccountingHooksTemplate')

    useDaysBackHook = False
    if hookAdmin.HA_IsCustomHook(AccountingHooks.GET_DAYS_BACK_TRADE) and useHook:
        useDaysBackHook = True

    configuration = dict()
    configuration['params'] = params
    configuration['loggerIF'] = logger
    configuration['objClass'] = acm.FTrade
    configuration['isSupportedObjectCb'] = isSupportedObjectCb if isSupportedObjectCb else lambda obj : True
    configuration['amendmentIF'] = AmendmentManager(Queries.GetLiveTradeJournalsQuery, Queries.GetLiveJournalsForAggregationLevels)
    configuration['creatorIF'] = AccountingCreator('accounting', useDaysBackHook, AccountingHooks.GET_DAYS_BACK_TRADE)
    configuration['processFilter'] = CreateTradeFilter()
    configuration.update(CreateCommonInterfaces(hookAdmin, Params, committerIF))

    return AccountingEngine(Configuration(configuration))

#-------------------------------------------------------------------------
def CreateEngineForSettlements(params, logger, committerIF=None, isSupportedObjectCb=None, useHook=True):
    import FAccountingParams as Params

    hookAdmin = GetHookAdministrator(Params.hooks, 'FAccountingHooksTemplate')

    useDaysBackHook = False
    if hookAdmin.HA_IsCustomHook(AccountingHooks.GET_DAYS_BACK_SETTLEMENT) and useHook:
        useDaysBackHook = True

    configuration = dict()
    configuration['params'] = params
    configuration['loggerIF'] = logger
    configuration['objClass'] = acm.FSettlement
    configuration['isSupportedObjectCb'] = isSupportedObjectCb if isSupportedObjectCb else lambda obj : True
    configuration['amendmentIF'] = AmendmentManager(Queries.GetLiveSettlementJournalsQuery, None)
    configuration['creatorIF'] = AccountingCreator('settlementAccounting', useDaysBackHook, AccountingHooks.GET_DAYS_BACK_SETTLEMENT)
    configuration['processFilter'] = CreateSettlementFilter()
    configuration.update(CreateCommonInterfaces(hookAdmin, Params, committerIF))

    return AccountingEngine(Configuration(configuration))

