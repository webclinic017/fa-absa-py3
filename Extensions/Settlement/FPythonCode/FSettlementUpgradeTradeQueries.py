""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeTradeQueries.py"

import acm
import FOperationsUtils as Utils
from FSettlementUpgradeModuleAdmin import ModuleIndex, GetModuleAdministrator
import FSettlementUpgradeVarHandler

NO_SPECIAL_TREATMENT = 0
ONLY_OTC_INSTRUMENTS = 1
ONLY_NON_OTC_INSTRUMENTS = 2

   
def StoreQuery(query, queryName):
    
    queryStored = False
    storedQuery = acm.FStoredASQLQuery()
    storedQuery.Query(query)
    storedQuery.Name(queryName)
    storedQuery.AutoUser(False)
    storedQuery.User(None)
    try:
        storedQuery.Commit()
        queryStored = True
    except Exception as error:
        print('Could not store query %s: %s' % (queryName, error))
    return queryStored

def ReplaceStringInList(stringList, toBeReplacedString, replaceWithString):
    for index in range(0, len(stringList)):
        if stringList[index] == toBeReplacedString:
            stringList[index] = replaceWithString

def StoreValidInstrumentTypesQuery(variableHandler, queryName):
    queryStored = False
    insTypeList = variableHandler.GetVariables()['valid_instrument_types']
    if len(insTypeList):
        ReplaceStringInList(insTypeList, 'EquitySwap', 'TotalReturnSwap')
        insTypeSet = set(insTypeList)
        query = acm.CreateFASQLQuery(acm.FTrade, 'OR')
        orNode = query.AddOpNode('OR')
        for insType in insTypeSet:
            orNode.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', insType))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreExcludeAcquirerQuery(variableHandler, queryName):
    queryStored = False
    excludeAcquirerList = variableHandler.GetVariables()['exclude_acq']
    if len(excludeAcquirerList):
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        opNode = None
        if variableHandler.GetVariables()['invert_exclude_acq'] == False:
            opNode = query.AddOpNode('AND')
            opNode.Not(True)
        else:
            opNode = query.AddOpNode('OR')
        for acquirerName in excludeAcquirerList:
            opNode.AddAttrNode('Acquirer.Name', 'EQUAL', acquirerName)
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreExcludePortfolioQuery(variableHandler, queryName):
    queryStored = False
    excludePortfolioList = variableHandler.GetVariables()['exclude_portfolio']
    if len(excludePortfolioList):
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        opNode = None
        if variableHandler.GetVariables()['invert_exclude_portfolio'] == False:
            opNode = query.AddOpNode('AND')
            opNode.Not(True)
        else:
            opNode = query.AddOpNode('OR')
        for PortfolioName in excludePortfolioList:
            opNode.AddAttrNode('Portfolio.Name', 'EQUAL', PortfolioName)
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreStatusQuery(variableHandler, queryName):
    queryStored = False
    statusList = variableHandler.GetVariables()['status']
    if len(statusList):
        query = acm.CreateFASQLQuery(acm.FTrade, 'OR')
        orNode = query.AddOpNode('OR')
        for status in statusList:
            orNode.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', status))
        queryStored = StoreQuery(query, queryName)
    return queryStored

def StoreOTCHandlingQuery(variableHandler, queryName):
    queryStored = False
    otc = variableHandler.GetVariables()['special_otc_instrument_handling']
    if otc != NO_SPECIAL_TREATMENT:
        query = acm.CreateFASQLQuery(acm.FTrade, 'OR')
        orNode = query.AddOpNode('OR')
        if otc == ONLY_OTC_INSTRUMENTS:
            orNode.AddAttrNode('Instrument.Otc', 'EQUAL', True)
        elif otc == ONLY_NON_OTC_INSTRUMENTS:
            orNode.AddAttrNode('Instrument.Otc', 'EQUAL', False)
        else:
            return queryStored
        queryStored = StoreQuery(query, queryName)
    return queryStored

def CreateTradeFilterQueries(storedQueriesList):
    variableHandler = FSettlementUpgradeVarHandler.VariableHandler()
    variableHandler.SetTradeFilterVariables()
    if StoreOTCHandlingQuery(variableHandler, 'otc_filter') == True:
        storedQueriesList.append('otc_filter')
    if StoreStatusQuery(variableHandler, 'trade_status_filter') == True:
        storedQueriesList.append('trade_status_filter')
    if StoreExcludePortfolioQuery(variableHandler, 'portfolio_filter') == True:
        storedQueriesList.append('portfolio_filter')
    if StoreExcludeAcquirerQuery(variableHandler, 'acquirer_filter') == True:
        storedQueriesList.append('acquirer_filter')
    if StoreValidInstrumentTypesQuery(variableHandler, 'valid_instruments_filter') == True:
        storedQueriesList.append('valid_instruments_filter')

def CreateTradeFilterQueriesParameter():
    storedQueryNames = list()
    CreateTradeFilterQueries(storedQueryNames)
    moduleAdmin = GetModuleAdministrator()
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'tradeFilterQueries', storedQueryNames)
    moduleAdmin.SaveModule(ModuleIndex.PARAMETER)
