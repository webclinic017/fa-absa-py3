""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementProcess.py"
"""
MODULE
    FSettlementProcess 

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
"""

import acm, traceback
try:
    import FSettlementCreatorSingleton
    import FSettlementMatcher as Matcher
    from   FSettlementTransactionCommitter import TransactionCommitter
    import FSettlementUtils
    from FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
    from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache
    import FSettlementGetters as Getters
    from FSettlementProcessFunctions import SettlementProcessData
except Exception as e:
    acm.Log('Failed to import FSettlementProcess')
    acm.Log('Traceback: {}'.format(traceback.format_exc()))
    raise e

def RegenerateSettlementsFromSettlement(oldSettlement):
    creator = FSettlementCreatorSingleton.GetSettlementCreator()


    newSettlements = creator.CreateSettlements(oldSettlement.Trade(),  FSettlementCorrectTradeRecaller())
    newSettlements = FSettlementUtils.MergeSameSourceSettlements(oldSettlement.Trade(), newSettlements)
    matcher = Matcher.SettlementMatcher([oldSettlement], newSettlements)

    oldSettlements = acm.FArray()
    newSettlements = acm.FArray()
    for (old, new) in matcher.GetMatchedSettlementsList():
        if old == oldSettlement and new != None:
            oldSettlements.Add(old)
            newSettlements.Add(new)

    pair = acm.FPair()
    pair.First(oldSettlements)
    pair.Second(newSettlements)
    return pair

def CommitSettlementList(oldSettlements, newSettlements, commitedSettlements = None,  trade = None, settlementCorrectTradeRecaller = None ):
    if settlementCorrectTradeRecaller == None:
        settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()
    settlements = list()
    for counter in range(0, newSettlements.Size()):
        settlements.append((oldSettlements.At(counter), newSettlements.At(counter)))

    spd = SettlementProcessData(settlements, trade, "")
    scl = Getters.GetSettlementCommitterList(spd, trade, settlementCorrectTradeRecaller)


    nettingRuleQueryCache = SettlementNettingRuleQueryCache()
    tc  = TransactionCommitter(scl, spd, nettingRuleQueryCache, commitedSettlements)
    return tc.CommitSettlements()
