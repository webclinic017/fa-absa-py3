""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeDuplicatesFinder.py"
import acm
from FOperationsExceptions import WrapperException 

class MenuException(WrapperException):
    def __init__(self, message, innerException = None):
        WrapperException.__init__(self, message, innerException)

class CashFlowGrouper:
    def __init__(self, cashFlow):
        assert cashFlow != None
        self.__cashFlow = cashFlow
        self.__oldSolutionSettlements = acm.FArray()
        self.__newSolutionSettlements = acm.FArray()
    
    def CashFlow(self):
        return self.__cashFlow

    def AddSettlement(self, settlement):
        assert self.__cashFlow == settlement.CashFlow()
        if CashFlowGrouper.__IsNewSolutionSettlement(settlement):
            self.__newSolutionSettlements.Add(settlement)
        else:
            self.__oldSolutionSettlements.Add(settlement)
    
    @staticmethod    
    def __IsNewSolutionSettlement(settlement):
        return settlement.Trade() != None

    @staticmethod
    def __CreateSettlementsQuery(settlements):
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        for s in settlements:
            query.AddAttrNode('Oid', 'EQUAL', s.Oid())
        return query
        
    def HasBothNewAndOldSolutionSettlements(self):
        return self.__newSolutionSettlements.Size() > 0 and \
               self.__oldSolutionSettlements.Size() > 0

    def CreateFolderForNewSolutionSettlements(self):
        assert self.__newSolutionSettlements.IsEmpty() == False
        folderName = 'CashFlow %d (New)' % (self.__cashFlow.Oid())
        query = CashFlowGrouper.__CreateSettlementsQuery(self.__newSolutionSettlements)
        return acm.FASQLQueryFolder(name = folderName, asqlQuery = query)
        
    def CreateFolderForOldSolutionSettlements(self):
        assert self.__oldSolutionSettlements.IsEmpty() == False
        folderName = 'CashFlow %d (Old)' % (self.__cashFlow.Oid())
        query = CashFlowGrouper.__CreateSettlementsQuery(self.__oldSolutionSettlements)
        return acm.FASQLQueryFolder(name = folderName, asqlQuery = query)
        
                
def __FindSettlementsThatMightHaveDuplicates():
    query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    query.AddAttrNode('Type', 'EQUAL', 'Coupon')
    query.AddAttrNode('Type', 'EQUAL', 'Redemption')
    query.AddAttrNode('Type', 'EQUAL', 'Dividend')
    return query.Select()
    
def GroupSettlementsBasedOnCashFlows(settlements):
    sortedSettlements = settlements.SortByProperty('CashFlow.Oid', True)
    cashFlowGroupers = acm.FArray()
    currentGrouper = None
    for settlement in sortedSettlements:
        cashFlow = settlement.CashFlow()
        if cashFlow:
            if currentGrouper == None or currentGrouper.CashFlow() != cashFlow:
                currentGrouper = CashFlowGrouper(cashFlow)
                cashFlowGroupers.Add(currentGrouper)
            currentGrouper.AddSettlement(settlement)
    return cashFlowGroupers

def InsertIntoSheet(invokationInfo):
    INSERT_FIRST = 1
    sheet = invokationInfo.ExtensionObject().ActiveSheet()
    settlements = __FindSettlementsThatMightHaveDuplicates()
    cashFlowGroupers = GroupSettlementsBasedOnCashFlows(settlements)
    for cashFlowGrouper in cashFlowGroupers:
        if cashFlowGrouper.HasBothNewAndOldSolutionSettlements():
            sheet.InsertObject(cashFlowGrouper.CreateFolderForNewSolutionSettlements(), INSERT_FIRST)
            sheet.InsertObject(cashFlowGrouper.CreateFolderForOldSolutionSettlements(), INSERT_FIRST)

def CreateMenuInSettlementSheet():
    MODULE_NAME = 'SettlementUpgradeMod'
    MENU_EXTENSION = '''FSettlementSheet:Manage Duplicate Folders =
    Function=FSettlementUpgradeDuplicatesFinder.InsertIntoSheet
    MenuType=GridColumnHeader
    ParentMenu=Upgrade Tools'''
    msgInCaseOfException = ''
    try:
        context = acm.GetStandardContext()
        newModule = acm.FExtensionModule()
        msgInCaseOfException = 'Could not create module %s:' % (MODULE_NAME)
        newModule.Name(MODULE_NAME)
        newModule.Commit()
        msgInCaseOfException = 'Could not add module %s to standard context:' % (MODULE_NAME)
        context.AddModule(newModule)
        context.Commit()
        msgInCaseOfException = 'Could not add menu extension to module %s:' % (MODULE_NAME)
        extension = context.EditImport('FMenuExtension', MENU_EXTENSION)
        extension.Commit()
        newModule.Commit()
    except Exception as e:
        raise MenuException(msgInCaseOfException, e)
