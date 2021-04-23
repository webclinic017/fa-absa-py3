""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingObjectCreator.py"
import acm

# operations
from FOperationsExceptions import InvalidHookException

# accounting
from FAccountingAccountAllocator import AccountAllocator
from FAccountingExceptions import DynamicAccountException
from FAccountingEngineContracts import IAccountingEngine


#-------------------------------------------------------------------------
class AccountingCreator(IAccountingEngine.IAccountingObjectCreator):

    #-------------------------------------------------------------------------
    def __init__(self, flowName, useStartDateHook, startDateHookName):
        self.__accountAllocator = AccountAllocator()
        self.__mappingFlow = acm.Mapping.Get(flowName)
        self.__useStartDateHook = useStartDateHook
        self.__startDateHookName = startDateHookName

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider
        self.__accountAllocator.PO_Init(provider)
        self.ConfigureMappingEngine()

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__accountAllocator.PO_Clear()
        self.__mappingFlow.GetHost().ClearWorkFlowLog()

    #-------------------------------------------------------------------------
    def AOC_CreateObjects(self, obj):
        journals = acm.FArray()
        startDate = self.__GetStartDate(obj)
        self.SetPeriod(obj, startDate)

        self.__mappingFlow.GetHost().Match(obj, self.OnMatchCb, journals, self.__parameters, self.__mappingFlow)

        if len(self.MappingFlowLog()) > 0:
            self.__provider.LP_Log("\n".join(self.MappingFlowLog()))

        self.__accountAllocator.AA_AddItemsToTransaction()

        return startDate, journals, {journal.JournalInformation() for journal in journals}

    #-------------------------------------------------------------------------
    def AOC_IsPositionCached(self, positionKey):
        return self.__mappingFlow.GetHost().IsPositionCached(positionKey)

    #-------------------------------------------------------------------------
    def AOC_ClearCalculations(self):
        self.__mappingFlow.GetHost().ClearCalculationSpace()

    #-------------------------------------------------------------------------
    def AOC_ClearProcessedPositions(self):
        return self.__mappingFlow.GetHost().ClearProcessedPositions()

    #-------------------------------------------------------------------------
    def MappingFlowLog(self):
        return self.__mappingFlow.GetHost().WorkflowLog()

    #-------------------------------------------------------------------------
    def ConfigureMappingEngine(self):
        bookFilter = self.__provider.Param('bookFilter')
        bookLinkFilter = self.__provider.Param('bookLinkFilter')
        treatmentLinkFilter = self.__provider.Param('treatmentLinkFilter')
        detailedLog = self.__provider.Param('detailedLog')

        self.__mappingFlow.GetHost().DetailedLogging(detailedLog)
        self.__parameters = self.__mappingFlow.GetHost().CreateParameters(bookFilter, bookLinkFilter, treatmentLinkFilter)

    #-------------------------------------------------------------------------
    def SetPeriod(self, obj, startDate):
        endDate = self.__provider.Param('endDate')
        endOfDayDate = self.__provider.Param('endOfDayDate')
        processDate = self.__provider.Param('processDate')

        self.__mappingFlow.GetHost().SetPeriod(startDate, endDate, endOfDayDate, processDate)

    #-------------------------------------------------------------------------
    def OnMatchCb(self, target, journal, journals):

        if self.__accountAllocator.AA_IsApplicableForDynamicAccount(journal):

            try:
                chartOfAccount = self.__accountAllocator.AA_CreateDynamicAccount(journal, journal.Account())

            except (DynamicAccountException, InvalidHookException) as e:
                chartOfAccount = journal.Book().SuspenseChartOfAccount()
                journal.IsSuspenseAccountNoAccountFound(True)
                self.__provider.LP_Log('ERROR: Exception occurred when allocating dynamic account, posting on suspense: %s' % str(e))

            journal.ChartOfAccount(chartOfAccount)

        journals.Add(journal)

    #-------------------------------------------------------------------------
    def __GetStartDate(self, obj):
        if self.__useStartDateHook:
            return self.__provider.HA_CallHook(self.__startDateHookName, obj)
        else:
            return self.__provider.Param('startDate')
