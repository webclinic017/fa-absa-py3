""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingHookAdministrator.py"

import acm, types

# operations
from FOperationsHook import DefaultHook
from FOperationsHookAdministrator import HookAdministrator
from FOperationsTypeComparators import PrimitiveTypeComparator, AcmTypeComparator, DateTypeComparator


#-------------------------------------------------------------------------
class AccountingHooks:
    GET_DYNAMIC_ACCOUNT                 = 'GetDynamicAccount'
    GET_TRADES_FOR_EOD                  = 'GetTradesForEOD'
    GET_COMMIT_JOURNAL_LOG_MSG          = 'GetCommitJournalLogMessage'
    IS_VALID_TRADE                      = 'IsValidTrade'
    JOURNAL_MODIFICATION                = 'JournalModification'
    JOURNAL_INFORMATION_MODIFICATION    = 'JournalInformationModification'
    GET_DAYS_BACK_TRADE                 = 'GetDaysBackAsDateTrade'
    GET_DAYS_BACK_SETTLEMENT            = 'GetDaysBackAsDateSettlement'
    GET_SETTLEMENTS_FOR_EOD             = 'GetSettlementsForEOD'

#-------------------------------------------------------------------------
def GetHookAdministrator(hooks, name):

    defaultHooks = [
        (AccountingHooks.GET_DYNAMIC_ACCOUNT, DefaultHook(name, AccountingHooks.GET_DYNAMIC_ACCOUNT, AcmTypeComparator(acm.FTAccount))),
        (AccountingHooks.GET_TRADES_FOR_EOD, DefaultHook(name, AccountingHooks.GET_TRADES_FOR_EOD, PrimitiveTypeComparator(list))),
        (AccountingHooks.GET_COMMIT_JOURNAL_LOG_MSG, DefaultHook(name, AccountingHooks.GET_COMMIT_JOURNAL_LOG_MSG, PrimitiveTypeComparator(bytes))),
        (AccountingHooks.IS_VALID_TRADE, DefaultHook(name, AccountingHooks.IS_VALID_TRADE, PrimitiveTypeComparator(bool))),
        (AccountingHooks.JOURNAL_MODIFICATION, DefaultHook(name, AccountingHooks.JOURNAL_MODIFICATION, AcmTypeComparator(acm.FJournal))),
        (AccountingHooks.JOURNAL_INFORMATION_MODIFICATION, DefaultHook(name, AccountingHooks.JOURNAL_INFORMATION_MODIFICATION, AcmTypeComparator(acm.FJournalInformation))),
        (AccountingHooks.GET_DAYS_BACK_TRADE, DefaultHook(name, AccountingHooks.GET_DAYS_BACK_TRADE, DateTypeComparator())),
        (AccountingHooks.GET_DAYS_BACK_SETTLEMENT, DefaultHook(name, AccountingHooks.GET_DAYS_BACK_SETTLEMENT, DateTypeComparator())),
        (AccountingHooks.GET_SETTLEMENTS_FOR_EOD, DefaultHook(name, AccountingHooks.GET_SETTLEMENTS_FOR_EOD, PrimitiveTypeComparator(list)))]

    return HookAdministrator(hooks, defaultHooks)

