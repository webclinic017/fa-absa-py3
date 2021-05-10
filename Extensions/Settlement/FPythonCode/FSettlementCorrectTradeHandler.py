""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCorrectTradeHandler.py"
import acm
import FOperationsUtils as Utils
import FOperationsRuleEngine as Engine
import FSettlementUtils as SettlementUtils
from FSettlementEnums import SettlementStatus, RelationType

class SettlementReference(object):
    NONE = 0
    CASHFLOW = 1
    DIVIDEND = 2
    PAYMENT = 3

class CorrectTradeHandler(object):

    def __init__(self):
        query = acm.CreateFASQLQuery(acm.FTrade, 'OR')
        query.AddAttrNode('CorrectionTrade.Oid', 'GREATER', 0)

        condition = Engine.QueryCondition(query)
        actionFunc = Engine.ActionFunction(CorrectTradeHandler.CalculateCorrectedAmount)
        rules = [Engine.Rule(condition, actionFunc)]
        self.ruleExecutor = Engine.RuleExecutor(rules, Engine.ActionFunction(CorrectTradeHandler.FallBack))

    def GetCorrectedAmount(self, trade, settlement):

        if settlement.Dividend():
            settlementReference = SettlementReference.DIVIDEND
        elif settlement.CashFlow():
            settlementReference = SettlementReference.CASHFLOW
        elif settlement.Payment():
            settlementReference = SettlementReference.PAYMENT
        else:
            settlementReference = SettlementReference.NONE

        return self.ruleExecutor.Execute(trade, Engine.ValueType.SINGLE_VALUE, trade, settlement, settlementReference)

    @staticmethod
    def GetCorrectedTrades(trade):
        if not trade.CorrectionTrade() or trade.CorrectionTrade().Oid() == trade.Oid():
            return []
        else:
            return [trade.CorrectionTrade()] + CorrectTradeHandler.GetCorrectedTrades(trade.CorrectionTrade())

    @staticmethod
    def AssertSettlementReference(settlementReference):
        assert settlementReference == SettlementReference.NONE or \
               settlementReference == SettlementReference.CASHFLOW or \
               settlementReference == SettlementReference.DIVIDEND or \
               settlementReference == SettlementReference.PAYMENT

    @staticmethod
    def GetClosedSettlements(trade, settlement, settlementReference):
        CorrectTradeHandler.AssertSettlementReference(settlementReference)
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
            if aSettlement.RelationType() != RelationType.NONE:
                continue
            topSettlement = SettlementUtils.FindRootInHierarchyTree(aSettlement)
            if not (topSettlement.Status() == SettlementStatus.CLOSED or SettlementUtils.CorrectTradePayNet(topSettlement)):
                continue

            if aSettlement.Status() == SettlementStatus.RECALLED:
                continue
            if query.IsSatisfiedBy(aSettlement):
                settlementsSet.add(aSettlement)

        return settlementsSet


    @staticmethod
    def FallBack(dummyTrade, dummySettlement, dummySettlementReference):
        return 0.0

    @staticmethod
    def GetPaymentAmount(settlement):
        '''In: settlement - the settlement that the payment amount will be calculated for
           Out: A float that will is the amount for the settlement
        '''

        settlementToQueue = acm.FSettlement.Select("payment = %d" % settlement.RefPayment().Oid())
        amount = 0
        Queue = []
        usedSettlement = []
        for s in settlementToQueue:
            Queue.append(s)
        settlement = Queue.pop()
        while settlement != None:
            if settlement.Status() == SettlementStatus.CLOSED or SettlementUtils.CorrectTradePayNet(settlement):
                amount = amount + settlement.Amount()

            if settlement.Status() == SettlementStatus.VOID and settlement.Parent() and \
               (settlement.Parent().RelationType() == RelationType.NET or settlement.Parent().RelationType() == RelationType.AD_HOC_NET):
                amount = amount + settlement.Amount()

            if settlement.RefPayment() != None:
                settlementToQueue = acm.FSettlement.Select("payment = %d" %settlement.RefPayment().Oid())
                for s in settlementToQueue:
                    if not s in usedSettlement:
                        Queue.append(s)
                        usedSettlement.append(s)

            if len(Queue) == 0:
                settlement = None
            else:
                settlement = Queue.pop()
        return amount


    @staticmethod
    def CalculateCorrectedAmount(trade, settlement, settlementReference):
        correctedAmount = 0.0
        if settlement.RefPayment() != None:
            correctedAmount = CorrectTradeHandler.GetPaymentAmount(settlement)
        else:
            correctedTrades = CorrectTradeHandler.GetCorrectedTrades(trade)
            for correctedTrade in correctedTrades:
                closedSettlements = CorrectTradeHandler.GetClosedSettlements(correctedTrade, settlement, settlementReference)
                for aSettlement in closedSettlements:
                    correctedAmount += aSettlement.Amount()
        return correctedAmount