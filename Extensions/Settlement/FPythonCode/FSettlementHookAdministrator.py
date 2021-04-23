""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementHookAdministrator.py"
import FSettlementHooksTemplate as Template
from FOperationsHookAdministrator import HookAdministrator
import types
from FOperationsTypeComparators import PrimitiveTypeComparator, DateTypeComparator, SWIFTMessageTypeComparator
from FOperationsHook import DefaultHook

class SettlementHooks:
    GET_NET_AMOUNT                      = 'GetNetAmount'
    GET_DAYS_FORWARD                    = 'GetDaysForward'
    GET_DAYS_BACK                       = 'GetDaysBack'
    COMPARE_SETTLEMENT_AMOUNTS          = 'CompareSettlementAmounts'
    GET_NOTIFICATION_DATE               = 'GetNotificationDay'
    SETTLEMENT_MODIFICATION             = 'SettlementModification'
    EXCLUDE_TRADE                       = 'ExcludeTrade'
    GET_MT_MESSAGE                      = 'GetMTMessage'
    SPLIT_SETTLEMENT                    = 'SplitSettlement'
    CONFIRMATION_EVENT                  = 'ConfirmationEvent'
    UPDATE_SETTLEMENT_BUSINESS_PROCESS  = 'UpdateSettlementBusinessProcess'
    DECIDE_SETTLEMENTS_TO_PAIR_OFF      = 'DecideSettlementsToPairOff'


class SettlementHookAdministrator(HookAdministrator):

    hookAdmin = None

    def __init__(self, templateModule, customHooks):

        defaultHooks = [(SettlementHooks.GET_NET_AMOUNT, DefaultHook(Template.__name__, SettlementHooks.GET_NET_AMOUNT, PrimitiveTypeComparator(float))),
                        (SettlementHooks.GET_DAYS_FORWARD, DefaultHook(Template.__name__, SettlementHooks.GET_DAYS_FORWARD, PrimitiveTypeComparator(int))),
                        (SettlementHooks.GET_DAYS_BACK, DefaultHook(Template.__name__, SettlementHooks.GET_DAYS_BACK, PrimitiveTypeComparator(int))),
                        (SettlementHooks.COMPARE_SETTLEMENT_AMOUNTS, DefaultHook(Template.__name__, SettlementHooks.COMPARE_SETTLEMENT_AMOUNTS, PrimitiveTypeComparator(bool))),
                        (SettlementHooks.GET_NOTIFICATION_DATE, DefaultHook(Template.__name__, SettlementHooks.GET_NOTIFICATION_DATE, DateTypeComparator())),
                        (SettlementHooks.SETTLEMENT_MODIFICATION, DefaultHook(Template.__name__, SettlementHooks.SETTLEMENT_MODIFICATION, PrimitiveTypeComparator(bytes))),
                        (SettlementHooks.EXCLUDE_TRADE, DefaultHook(Template.__name__, SettlementHooks.EXCLUDE_TRADE, PrimitiveTypeComparator(bool))),
                        (SettlementHooks.GET_MT_MESSAGE, DefaultHook(Template.__name__, SettlementHooks.GET_MT_MESSAGE, SWIFTMessageTypeComparator())),
                        (SettlementHooks.SPLIT_SETTLEMENT, DefaultHook(Template.__name__, SettlementHooks.SPLIT_SETTLEMENT, PrimitiveTypeComparator(list))),
                        (SettlementHooks.CONFIRMATION_EVENT, DefaultHook(Template.__name__, SettlementHooks.CONFIRMATION_EVENT, PrimitiveTypeComparator(type(None)))),
                        (SettlementHooks.UPDATE_SETTLEMENT_BUSINESS_PROCESS, DefaultHook(Template.__name__, SettlementHooks.UPDATE_SETTLEMENT_BUSINESS_PROCESS, PrimitiveTypeComparator(bool))),
                        (SettlementHooks.DECIDE_SETTLEMENTS_TO_PAIR_OFF, DefaultHook(Template.__name__, SettlementHooks.DECIDE_SETTLEMENTS_TO_PAIR_OFF, PrimitiveTypeComparator(list)))]

        HookAdministrator.__init__(self, customHooks, defaultHooks)
        SettlementHookAdministrator.hookAdmin = self

def GetHookAdministrator():
    import FSettlementParameters as SettlementParams
    instance = SettlementHookAdministrator.hookAdmin

    if not instance:
        return SettlementHookAdministrator(Template, SettlementParams.hooks)
    return instance
