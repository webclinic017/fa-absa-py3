""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeDelQueries.py"
"""
FSettlementUpgradeDeletionQueries
"""

import acm
import FOperationsUtils as Utils
from FSettlementUpgradeVarHandler import VariableHandler
from FSettlementUpgradeTradeQueries import StoreQuery

from FSettlementUpgradeModuleAdmin import ModuleIndex, GetModuleAdministrator

def StoreRecallVoidQuery(variableHandler, queryName):
    queryStored = False
    recallIfTradeStatusIsVoid = variableHandler.GetVariable('recall_if_trade_status_is_void')
    if recallIfTradeStatusIsVoid == False:
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        or1 = query.AddOpNode('OR')
        or1.AddAttrNode('Trade.Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'Void'))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreRecallTerminatedQuery(variableHandler, queryName):
    queryStored = False
    recallIfTradeStatusIsTerminated = variableHandler.GetVariable('recall_if_trade_status_is_terminated')
    if recallIfTradeStatusIsTerminated == False:
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        or1 = query.AddOpNode('OR')
        or1.AddAttrNode('Trade.Status', 'EQUAL', Utils.GetEnum('TradeStatus', 'Terminated'))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreKeepOldSettlementsQuery(variableHandler, queryName):
    queryStored = False
    keepOldSettlementsWhenVoid = variableHandler.GetVariable('keep_old_settlements_when_void')
    keepStatusList = variableHandler.GetVariable('keep_status')
    if keepOldSettlementsWhenVoid == True:
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        or1 = query.AddOpNode('OR')
        or1.AddAttrNode('ValueDay', 'LESS_EQUAL', '0d')
        or2 = query.AddOpNode('OR')
        for status in keepStatusList:
            or2.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', status))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def CreatePreventSettlementDeletionQueries(storedQueriesList):
    variableHandler = VariableHandler()
    if StoreRecallVoidQuery(variableHandler, 'prvnt_del_trd_status_void') == True:
        storedQueriesList.append('prvnt_del_trd_status_void')
    if StoreRecallTerminatedQuery(variableHandler, 'prvnt_del_trd_status_terminated') == True:
        storedQueriesList.append('prvnt_del_trd_status_terminated')
    if StoreKeepOldSettlementsQuery(variableHandler, 'prvnt_del_old_settlements') == True:
        storedQueriesList.append('prvnt_del_old_settlements')

def CreatePreventSettlementDeletionQueriesParameter():
    storedQueryNames = list()
    CreatePreventSettlementDeletionQueries(storedQueryNames)
    moduleAdmin = GetModuleAdministrator()
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'preventSettlementDeletionQueries', storedQueryNames)
    moduleAdmin.SaveModule(ModuleIndex.PARAMETER)