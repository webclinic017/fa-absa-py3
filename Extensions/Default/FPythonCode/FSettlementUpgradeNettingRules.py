""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeNettingRules.py"
import acm

def StoreQuery(query, queryName):
    try:
        storedQuery = acm.FStoredASQLQuery()
        storedQuery.Query(query)
        storedQuery.Name(queryName)
        storedQuery.AutoUser(False)
        storedQuery.User(None)
        storedQuery.SubType("nettingMapping")
        storedQuery.Commit()
    except Exception as errorMessage:
        Utils.LogAlways("Failed to create filter: " +str(queryName))
        raise errorMessage
    return storedQuery

def NettingRuleParametersToQuery(nettingRule):
    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    if nettingRule.Currency() != None:
        currencyNode = query.AddOpNode('AND')
        currencyNode.AddAttrNode('Currency.Name', 'EQUAL', nettingRule.Currency().Name())
    if nettingRule.Acquirer() != None:
        acquirerNode = query.AddOpNode('AND')
        acquirerNode.AddAttrNode('Acquirer.Name', 'EQUAL', nettingRule.Acquirer().Name() )
    if nettingRule.InsType() != 'None':
        insTypeNode = query.AddOpNode('AND')
        insTypeNode.AddAttrNode('Trade.Instrument.InsType', 'EQUAL',  Utils.GetEnum('InsType', nettingRule.InsType()) )
    if nettingRule.CurrencyPair() != None:
        currencyPairNode = query.AddOpNode('AND')
        currencyPairNode.AddAttrNode('GetCurrencyPairForTrade.Name', 'EQUAL', nettingRule.CurrencyPair().Name() )


    if nettingRule.ClsNetting():
        clsNettingNode = query.AddOpNode('AND')
        clsNettingNode.AddAttrNode('Trade.ClsStatus', 'EQUAL', Utils.GetEnum('CLSStatus', 'CLS') )
    closeTradeNettingNode = query.AddOpNode('AND')
    closeTradeNettingNode.AddAttrNode('IsTradeClosingOrClosed', 'EQUAL', nettingRule.CloseTradeNetting() )
    return query

def GetQueryName(nettingRule):
    if len(acm.FNettingRule.Select("name ='%s'"% nettingRule.Name())) == 1:
        return nettingRule.Name()
    return str(nettingRule.Name()) + str(nettingRule.Oid())

def UpgradeNettingRules():
    for nettingRule in acm.FNettingRule.Select(""):
        Utils.LogAlways("Upgrading the netting rule: " +str(nettingRule.Ruleid()))
        try:
            storedQuery = StoreQuery(NettingRuleParametersToQuery(nettingRule), GetQueryName(nettingRule))
            nettingRule.Query(storedQuery)

            if nettingRule.BilateralNetting():
                nettingRule.NettingDefinitionHook('FSettlementNetCandidatesFinder.BilateralNetting')
            elif nettingRule.CloseTradeNetting():
                nettingRule.NettingDefinitionHook('FSettlementNetCandidatesFinder.CloseTradeNetting')
            else:
                nettingRule.NettingDefinitionHook('FSettlementNetCandidatesFinder.IntraTradeNetting')

            nettingRule.Commit()
        except Exception as errorMessage:
            Utils.LogAlways("Warning: Failed to upgrade the netting rule " +str(nettingRule.Ruleid()) + " : " +str(errorMessage) )
    Utils.LogAlways("Done")

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    import acm
    import FOperationsUtils as Utils

    ael_variables = []

    def ael_main(dict):
        pr = '<< Settlement Upgrade - %s >>' % (__file__)
        Utils.Log(True, pr)
        UpgradeNettingRules()

except Exception as e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    Utils.Log(True, 'Could not run FSettlementUpgradeNettingRules due to ')
    Utils.Log(True, str(e))



