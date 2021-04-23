""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationHookAdministrator.py"
from FOperationsHookAdministrator import HookAdministrator
from FOperationsHook import DefaultHook
import FConfirmationHooksTemplate
from FOperationsTypeComparators import PrimitiveTypeComparator, SWIFTMessageTypeComparator
import types

#-------------------------------------------------------------------------
class ConfirmationHooks:
    GET_EXPIRY_DAY_COUNT = 'GetExpiryDayCount'
    GET_MT_MESSAGE = 'GetMTMessage'
    GET_TRADES_TO_BE_PROCESSED = 'GetTradesToBeProcessed'
    CANCELLATION_AND_NEW_INSTEAD_OF_AMENDMENT = 'CancellationAndNewInsteadOfAmendment'

#-------------------------------------------------------------------------
class ConfirmationHookAdministrator(HookAdministrator):

    hookAdmin = None

    #-------------------------------------------------------------------------
    def __init__(self, templateModule, customHooks):
        name = templateModule.__name__

        defaultHooks = [
            (ConfirmationHooks.GET_EXPIRY_DAY_COUNT, DefaultHook(name, ConfirmationHooks.GET_EXPIRY_DAY_COUNT, PrimitiveTypeComparator(int))),
            (ConfirmationHooks.GET_MT_MESSAGE, DefaultHook(name, ConfirmationHooks.GET_MT_MESSAGE, SWIFTMessageTypeComparator())),
            (ConfirmationHooks.GET_TRADES_TO_BE_PROCESSED, DefaultHook(name, ConfirmationHooks.GET_TRADES_TO_BE_PROCESSED, PrimitiveTypeComparator(list))),
            (ConfirmationHooks.CANCELLATION_AND_NEW_INSTEAD_OF_AMENDMENT, DefaultHook(name, ConfirmationHooks.CANCELLATION_AND_NEW_INSTEAD_OF_AMENDMENT, PrimitiveTypeComparator(bool)))]

        HookAdministrator.__init__(self, customHooks, defaultHooks)
        ConfirmationHookAdministrator.hookAdmin = self

    @staticmethod
    #-------------------------------------------------------------------------
    def Clear():
        ConfirmationHookAdministrator.hookAdmin = None

#-------------------------------------------------------------------------
def GetConfirmationHookAdministrator():

    instance = ConfirmationHookAdministrator.hookAdmin

    if not instance:
        import FConfirmationParameters as ConfirmationParameters

        return ConfirmationHookAdministrator(FConfirmationHooksTemplate, ConfirmationParameters.hooks)
        
    return instance
