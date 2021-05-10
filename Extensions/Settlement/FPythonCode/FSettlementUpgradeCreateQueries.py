""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeCreateQueries.py"
import acm
import FOperationsUtils as Utils
from FSettlementUpgradeVarHandler import VariableHandler
from FSettlementUpgradeTradeQueries import StoreQuery

from FSettlementUpgradeModuleAdmin import ModuleIndex, GetModuleAdministrator

def StoreHandleCombinationQuery(variableHandler, queryName):
    queryStored = False
    hccf = variableHandler.GetVariables()['handle_combination_cash_flows']
    if hccf == False:
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        or1 = query.AddOpNode('OR')
        or2 = query.AddOpNode('OR')
        or2.Not(True)
        or1.AddAttrNode('Trade.Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', 'Combination'))
        or2.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', 'Premium'))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreAccruedInterestQuery(variableHandler, queryName):
    queryStored = False
    insTypes = variableHandler.GetVariables()['valid_instrument_types_accrued_interest']
    if len(insTypes):
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        or1 = query.AddOpNode('OR')
        or2 = query.AddOpNode('OR')
        or2.Not(True)
        or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', 'Interest Accrued'))
        for insType in insTypes:
            or2.AddAttrNode('Trade.Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', insType))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def CreatePreventSettlementCreationQueries(storedQueriesList):
    variableHandler = VariableHandler()
    if StoreHandleCombinationQuery(variableHandler, 'prvnt_create_comb_cash_flow') == True:
        storedQueriesList.append('prvnt_create_comb_cash_flow')
    if StoreAccruedInterestQuery(variableHandler, 'prvnt_create_accrued_interest') == True:
        storedQueriesList.append('prvnt_create_accrued_interest')

def CreatePreventSettlementCreationQueriesParameter():
    storedQueryNames = list()
    CreatePreventSettlementCreationQueries(storedQueryNames)
    moduleAdmin = GetModuleAdministrator()
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'preventSettlementCreationQueries', storedQueryNames)
    moduleAdmin.SaveModule(ModuleIndex.PARAMETER)
