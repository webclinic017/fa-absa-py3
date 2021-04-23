""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingLedgerKeyMapper.py"
import acm

# operations
from FOperationsExceptions import ExtensionNotFoundException

# accounting
from FAccountingLedgerKeyParser import ParseLedgerKey

#-------------------------------------------------------------------------
class TAccountLedgerKeyMapper(object):
    def __init__(self, ledgerKeys):
        self.__ledgerKeyMethodChainsDict = dict()
        self.__ledgerKeyAttributesDict = dict()
        self.__tAccountMethodChainsDict = dict()
        self.__tAccountAttributesDict = dict()

        domainsInPath = ['FJournal', 'FJournalInformation', 'FJournalAdditionalInfo', 'FJournalInformationAdditionalInfo']

        for key in ledgerKeys:
            extension = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FJournal', key)

            if extension:
                chains, attributes = ParseLedgerKey(domainsInPath, extension.Value().split(';'), acm.FJournal)

                self.__ledgerKeyMethodChainsDict[str(key)] = chains
                self.__ledgerKeyAttributesDict[str(key)] = attributes
            else:
                raise ExtensionNotFoundException('Error detected when processing ledger key %s: extension value not found' % key)

    #-------------------------------------------------------------------------
    def GetLedgerKeyMethodChains(self, tAccount):
        if self.__tAccountMethodChainsDict.has_key(tAccount):
            methodChains = self.__tAccountMethodChainsDict[tAccount]
        else:
            methodChains = GetLedgerKeyAttributes(tAccount, self.__ledgerKeyMethodChainsDict)
            self.__tAccountMethodChainsDict[tAccount] = methodChains

        return methodChains

    #-------------------------------------------------------------------------
    def GetLedgerKeyAttributes(self, tAccount):
        if self.__tAccountAttributesDict.has_key(tAccount):
            attributes = self.__tAccountAttributesDict[tAccount]
        else:
            attributes = GetLedgerKeyAttributes(tAccount, self.__ledgerKeyAttributesDict)
            self.__tAccountAttributesDict[tAccount] = attributes

        return attributes

#-------------------------------------------------------------------------
def GetLedgerKeyAttributes(tAccount, partitionKeyDict):
    attributes = None
    if tAccount.IsRevaluation() and tAccount.InheritLedgerKey():
        ledgerKeys = {revaluatedTAccount.LedgerKey() for revaluatedTAccount in tAccount.RevaluatedTAccounts()}
        ledgerKeys2 = {revaluatedTAccount.LedgerKey() for revaluatedTAccount in tAccount.RevaluatedTAccounts2()}
        allLedgerKeys = set().union(ledgerKeys, ledgerKeys2)
        attributes = set().union(*[partitionKeyDict[ledgerKey] for ledgerKey in allLedgerKeys])
    else:
        ledgerKey = tAccount.LedgerKey()
        if ledgerKey:
            attributes = partitionKeyDict[ledgerKey]

    return attributes
