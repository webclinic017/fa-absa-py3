""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementUpdateFunctions.py"
import acm

#-------------------------------------------------------------------------
def AdjustLeftOverCash(newLeftOverCash, cashSettlementsToMerge):
    settlementsToMerge = list()
    newAmount = 0
    for settlement in cashSettlementsToMerge:
        newAmount += settlement.Amount()
    newLeftOverCash.Amount(newAmount)
    acm.Operations.AccountAllocator().SetSettlementAccountInfo(newLeftOverCash)
    if newLeftOverCash.IsValidForSTP():
        newLeftOverCash.STP()
    stateChart = acm.Operations.GetMappedSettlementProcessStateChart(newLeftOverCash)
    newLeftOverCash.StateChart(stateChart)
    if newLeftOverCash.IsValidForSTP():
        newLeftOverCash.STP()

    return newLeftOverCash