""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSettledAmountHandler.py"
import acm
import FOperationsUtils as Utils
import FSettlementUtils as SettlementUtils
from FSettlementEnums import RelationType


class SettlementReference(object):
    NONE = 0
    CASHFLOW = 1
    DIVIDEND = 2
    PAYMENT = 3

def GetSettledAmount(trade, settlement):
    if settlement.Dividend():
        settlementReference = SettlementReference.DIVIDEND
    elif settlement.CashFlow():
        settlementReference = SettlementReference.CASHFLOW
    elif settlement.Payment():
        settlementReference = SettlementReference.PAYMENT
    else:
        settlementReference = SettlementReference.NONE

    return CalculateSettledAmount(trade, settlement, settlementReference)

def AssertSettlementReference(settlementReference):
    assert settlementReference == SettlementReference.NONE or \
           settlementReference == SettlementReference.CASHFLOW or \
           settlementReference == SettlementReference.DIVIDEND or \
           settlementReference == SettlementReference.PAYMENT

def GetClosedSettlements(trade, settlement, settlementReference):
    AssertSettlementReference(settlementReference)
    query = None
    settlementsSet = set()
    query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    opNode1 = query.AddOpNode('AND')
    opNode1.AddAttrNode('Trade.Oid', 'EQUAL', trade.Oid())
    opNode1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', settlement.Type()))
    if settlement.Counterparty():
        opNode1.AddAttrNode('Counterparty.Oid', 'EQUAL', settlement.Counterparty().Oid())
    else:
        opNode1.AddAttrNode('Counterparty.Oid', 'EQUAL', 0)      

    if settlementReference == SettlementReference.CASHFLOW:
        opNode1.AddAttrNode('CashFlow.Oid', 'EQUAL', settlement.CashFlow().Oid())
    elif settlementReference == SettlementReference.PAYMENT:
        opNode1.AddAttrNode('Payment.Oid', 'EQUAL', settlement.Payment().Oid())
    elif settlementReference == SettlementReference.DIVIDEND:
        opNode1.AddAttrNode('Dividend.Oid', 'EQUAL', settlement.Dividend().Oid())

    selectQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    selectQuery.AddAttrNode('Trade.Oid', 'EQUAL', trade.Oid())
    selectQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', settlement.Type()))

    for aSettlement in selectQuery.Select():
        if not aSettlement.RelationType() in [RelationType.NONE, RelationType.VALUE_DAY_ADJUSTED]:
            continue
        if aSettlement.Parent() and aSettlement.RelationType() == RelationType.NONE and \
           aSettlement.Parent().RelationType() == RelationType.VALUE_DAY_ADJUSTED:
           continue
        topSettlement = SettlementUtils.FindRootInHierarchyTree(aSettlement)
        if not topSettlement.IsSettled():
            continue
        if query.IsSatisfiedBy(aSettlement):
            settlementsSet.add(aSettlement)

    return settlementsSet

def CalculateSettledAmount(trade, settlement, settlementReference):
    settledAmount = 0.0
    closedSettlements = GetClosedSettlements(trade, settlement, settlementReference)
    for aSettlement in closedSettlements:
        settledAmount += aSettlement.SettledAmount()
    return settledAmount
