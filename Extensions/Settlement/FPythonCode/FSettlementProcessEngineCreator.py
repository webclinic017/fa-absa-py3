""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementProcessEngineCreator.py"
import acm

# settlement
from FSettlementCommitter import SettlementCommitter
from FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
from FSettlementDocumentUpdater import FSettlementDocumentUpdater
from FSettlementDefaultUpdater import FSettlementDefaultUpdater
from FSettlementHookAdministrator import GetHookAdministrator, SettlementHooks
from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache
from FSettlementPartyUpdateHandler import PartyUpdateHandler
from FSettlementPartyUpdater import FSettlementPartyUpdater
from FSettlementProcessTradeSelector import SettlementProcessTradeSelector
from FSettlementSecuritySelector import SettlementSecuritySelector
from FSettlementSecurityProcessEngine import SecurityProcessEngine
from FSettlementSelector import SettlementSelector, SettlementPicker
from FSettlementTransactionCommitter import TransactionCommitter, PartyUpdateCommitter

# operations
from FOperationsEnginesBase import OperationsTaskEngine
from FOperationsEnginesHookTask import FOperationsEnginesHookTask
from FOperationsAMBAMessage import AMBAMessage
from FOperationsLoggers import ConsoleLogger
from FOperationsTaskConfiguration import Configuration
from FOperationsTransactionWriter import TransactionWriter
from FOperationsTransactionCommitter import TransactionCommitter as TransactionCommitterOps
from FOperationsResultCounter import ResultCounter
from FOperationsExceptions import InvalidHookException, AMBAMessageException
from FOperationsTransactionModifiers import SortingTransactionModifier

# accounting
from FAccountingSorting import SortOrderDefaultTup
from FAccountingOperations import GetOperations

#-------------------------------------------------------------------------
def CreateSettlementProcessEngine(logger, nettingRule = None):
    nettingRuleCache = nettingRule
    if nettingRuleCache == None:
        nettingRuleCache = SettlementNettingRuleQueryCache()


    documentUpdater = __CreateSettlementDocumentUpdater(nettingRuleCache)
    partyUpdater = __CreateSettlementPartyUpdater(nettingRuleCache)
    hookNotify = __CreateSettlementHookNotify(nettingRuleCache) 
    defaultUpdater = __CreateSettlementDefaultUpdater(nettingRuleCache) 

    tasks = []
    __AddTaskToList(tasks, 
                    documentUpdater,
                    lambda msg, obj: 
                        AMBAMessage(msg).GetNameOfUpdatedTable() == "OPERATIONSDOCUMENT" and
                        obj == None, 
                    AMBAMessageException)

    __AddTaskToList(tasks, 
                    partyUpdater,
                    lambda msg, obj: 
                        AMBAMessage(msg).GetNameOfUpdatedTable() == "PARTY" and
                        obj == None, 
                    (InvalidHookException, AMBAMessageException))

    __AddTaskToList(tasks, 
                    hookNotify,
                    lambda msg, obj: 
                        obj != None and
                        obj.IsKindOf(acm.FConfirmation),
                    InvalidHookException)

    __AddTaskToList(tasks, 
                    defaultUpdater,
                    lambda msg, obj: 
                        obj != None and
                        obj.IsKindOf(acm.FConfirmation) == False,
                    InvalidHookException)


    return __CreateBaseProcessEngine(tasks, logger)

#-------------------------------------------------------------------------
def CreateSettlementProcessEngineDocuments(logger):
    nettingRuleCache = SettlementNettingRuleQueryCache()
    documentUpdater = __CreateSettlementDocumentUpdater(nettingRuleCache)

    tasks = []
    __AddTaskToList(tasks, 
                    documentUpdater,
                    lambda msg, obj: True,
                    AMBAMessageException)

    return __CreateBaseProcessEngine(tasks, logger)

#-------------------------------------------------------------------------
def __CreateBaseProcessEngine(tasks, logger):
    args = {}    
    args['params'] = {}
    args['isSupportedObjectCb'] = False
    args['loggerIF'] = logger
    args['tasks'] = tasks 
    args.update(__CreateCommonInterfaces(GetHookAdministrator()))

    return OperationsTaskEngine(Configuration(args))

#-------------------------------------------------------------------------
def __CreateSettlementDocumentUpdater(nettingRuleCache):
    args = {}    
    args['settlementCommitterIF'] = SettlementCommitter
    args['nettingRuleCacheIF'] = nettingRuleCache
    args['ambaMessageIF'] = AMBAMessage
    return FSettlementDocumentUpdater(Configuration(args))

#-------------------------------------------------------------------------
def __CreateSettlementPartyUpdater(nettingRuleCache):
    args = {}    
    args['nettingRuleCacheIF'] = nettingRuleCache
    args['pickerIF'] = SettlementPicker
    args['ambaMessageIF'] = AMBAMessage
    args['transactionCommiterIF'] = TransactionCommitter 
    args['correctTradeRecallerIF'] = FSettlementCorrectTradeRecaller()
    args['partyUpdateCommiterIF'] = PartyUpdateCommitter
    args['securitySelectorIF'] = SettlementSecuritySelector
    args['securityProcessEngineIF'] = SecurityProcessEngine
    args['partyUpdateHandlerIF'] = PartyUpdateHandler
    return FSettlementPartyUpdater(Configuration(args))

#-------------------------------------------------------------------------
def __CreateSettlementHookNotify(nettingRuleCache):
    args = {}
    args['hookIF'] = SettlementHooks.CONFIRMATION_EVENT
    return FOperationsEnginesHookTask(Configuration(args))

#-------------------------------------------------------------------------
def __CreateSettlementDefaultUpdater(nettingRuleCache):
    args = {}    
    args['nettingRuleCacheIF'] = nettingRuleCache
    args['processTradeSelectorIF'] = SettlementProcessTradeSelector
    args['selectorIF'] = SettlementSelector
    args['transactionCommiterIF'] = TransactionCommitter 
    return FSettlementDefaultUpdater(Configuration(args))

#-------------------------------------------------------------------------
def __CreateCommonInterfaces(hookAdmin, committerIF=None):
    validationEngines = {}
    committer = committerIF if committerIF != None else TransactionCommitterOps(GetOperations(), ResultCounter)
    transactionModifier = SortingTransactionModifier(SortOrderDefaultTup)
    transactionWriter = TransactionWriter(committer, transactionModifier)

    configuration = dict()
    configuration['validatorsIF'] = validationEngines
    configuration['writerIF'] = transactionWriter
    configuration['hookAdminIF'] = hookAdmin
    return configuration

#-------------------------------------------------------------------------
def __AddTaskToList(list, task, condition, exception):
    list.append((task, condition, exception))
    return list
