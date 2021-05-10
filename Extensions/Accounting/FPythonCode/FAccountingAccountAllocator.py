""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingAccountAllocator.py"
import acm

# accounting
from FAccountingEngineContracts import IAccountingEngine
from FAccountingCreation import CreateChartOfAccount
from FAccountingExceptions import DynamicAccountException
from FAccountingHookAdministrator import AccountingHooks
from FAccountingOperations import Operation
from FAccountingEnums import ReportingClass

#-------------------------------------------------------------------------
class AccountAllocator(IAccountingEngine.IAccountingObjectCreator.IAccountAllocator):

    #-------------------------------------------------------------------------
    def __init__(self):
        self.__accountNumberAndTAccountMap = dict()
        self.__accountNumberAndChartOfAccountMap = dict()
        self.__transactionList = list()

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__accountNumberAndTAccountMap.clear()
        self.__accountNumberAndChartOfAccountMap.clear()
        del self.__transactionList[:]

    #-------------------------------------------------------------------------
    def AA_AddItemsToTransaction(self):
        for tup in self.__transactionList:
            self.__provider.WR_AddItem(tup[0], tup[1])

    #-------------------------------------------------------------------------
    def AA_IsApplicableForDynamicAccount(self, journal):
        return journal.Account().ReportingClass() == ReportingClass.SUMMARY and journal.Book().UseDynamicAccounts() == True

    #-------------------------------------------------------------------------
    def AA_CreateDynamicAccount(self, journal, parentAccount):
        tAccount = self.__provider.HA_CallHook(AccountingHooks.GET_DYNAMIC_ACCOUNT, journal, parentAccount)
        chartOfAccount = None

        parentChartOfAccount = parentAccount.ChartOfAccount(journal.Book())
        persistedTAccount = self.__GetPersistedTAccount(tAccount)

        if persistedTAccount:
            if self.__ValidateTAccount(persistedTAccount):
                chartOfAccount = self.__GetChartOfAccount(parentChartOfAccount, persistedTAccount)
        else:
            if self.__ValidateTAccount(tAccount):
                chartOfAccount = self.__PostOnNewAccount(parentChartOfAccount, tAccount)

        return chartOfAccount

    #-------------------------------------------------------------------------
    def __ValidateTAccount(self, tAccount):
        if not tAccount.Name():
            raise DynamicAccountException('Validation failed, No name given for account')
        if not tAccount.Number():
            raise DynamicAccountException('Validation failed, No number given for account')
        if tAccount.ReportingClass() != ReportingClass.TACCOUNT:
            raise DynamicAccountException('Validation failed, Reporting class should be TAccount')
        if not tAccount.Active():
            raise DynamicAccountException('Validation failed, Dynamic TAccount not active')
        return True

    #-------------------------------------------------------------------------
    def __GetPersistedTAccount(self, tAccount):
        try:
            tAccount = self.__accountNumberAndTAccountMap[tAccount.Number()]
        except KeyError as _:
            tAccount = acm.FTAccount.Select01('number = ' + tAccount.Number(), None)
        return tAccount

    #-------------------------------------------------------------------------
    def __GetPersistedChartOfAccount(self, parent, tAccount, book):
        try:
            chartOfAccount = self.__accountNumberAndChartOfAccountMap[tAccount.Number()]
        except KeyError as _:
            chartOfAccount = tAccount.ChartOfAccount(book)
        return chartOfAccount

    #-------------------------------------------------------------------------
    def __PostOnNewAccount(self, parentChartOfAccount, tAccount):
        chartOfAccount = CreateChartOfAccount(parentChartOfAccount, tAccount)

        self.__transactionList.append((Operation.CREATE, tAccount))
        self.__transactionList.append((Operation.CREATE, chartOfAccount))

        self.__accountNumberAndTAccountMap[tAccount.Number()] = tAccount
        self.__accountNumberAndChartOfAccountMap[tAccount.Number()] = chartOfAccount

        return chartOfAccount

    #-------------------------------------------------------------------------
    def __GetChartOfAccount(self, parentChartOfAccount, tAccount):
        chartOfAccount = self.__GetPersistedChartOfAccount(parentChartOfAccount, tAccount, parentChartOfAccount.Book())

        if chartOfAccount:
            if chartOfAccount.Parent() != parentChartOfAccount:
                raise DynamicAccountException('The account found does not have the matched summary account as parent')
            self.__accountNumberAndChartOfAccountMap[tAccount.Number()] = chartOfAccount
        else:
            chartOfAccount = CreateChartOfAccount(parentChartOfAccount, tAccount)
            self.__accountNumberAndChartOfAccountMap[tAccount.Number()] = chartOfAccount
            self.__transactionList.append((Operation.CREATE, chartOfAccount))

        return chartOfAccount
