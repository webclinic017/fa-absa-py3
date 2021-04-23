""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentHookAdministrator.py"

import FOperationsDocumentHooksTemplate as Template
from FOperationsHookAdministrator import HookAdministrator
from FOperationsTypeComparators import PrimitiveTypeComparator
import types
from FOperationsHook import DefaultHook

class OperationsDocumentHooks:
    SETTLEMENT_TRANSPORT_ROUTER = 'SettlementTransportRouter'

class OperationsDocumentHookAdministrator(HookAdministrator):
    hookAdmin = None

    def __init__(self, templateModule, customHooks):
        defaultHooks = [(OperationsDocumentHooks.SETTLEMENT_TRANSPORT_ROUTER, DefaultHook(Template.__name__, OperationsDocumentHooks.SETTLEMENT_TRANSPORT_ROUTER, PrimitiveTypeComparator(bytes)))]
        super(OperationsDocumentHookAdministrator, self).__init__(customHooks, defaultHooks)

        OperationsDocumentHookAdministrator.hookAdmin = self

    @staticmethod
    def ClearInstance():
        OperationsDocumentHookAdministrator.hookAdmin = None

def GetHookAdministrator():

    instance = OperationsDocumentHookAdministrator.hookAdmin

    if not instance:
        import FDocumentationParameters as DocumentationParams

        return OperationsDocumentHookAdministrator(Template, DocumentationParams.hooks)
        
    return instance
