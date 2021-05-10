""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSecuritySelector.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementSecuritySelector - Selecting or excluding security settlements
                                  from the main settlement process

    (c) Copyright 2016 FIS Global. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""

import acm
from FOperationsRuleEngine import QueryCondition, RuleExecutor, Rule, ValueType, ActionFunction
from FSettlementEnums import RelationType, SettlementStatus, SettlementType
import FSettlementModificationInspectorSingleton as Singleton
import FOperationsUtils as Utils
import FSettlementMatcher as Matcher

class SettlementSecuritySelector(object):
    '''This class includes functions for retrieving security settlements from FTrade.'''

    def __init__(self, fTrade, oldSettlements, newSettlements):
        ''' Constructor. '''
        self.__fTrade = fTrade
        self.__ruleExecutor = None
        self.__oldSettlements = oldSettlements
        self.__newSettlements = newSettlements
        self.__securitySettlements = []

    def FilterOutSecuritySettlements(self):
        self.__securitySettlements = self.__GetSecuritySettlements()
        securitySettlements = list(self.__securitySettlements)
        matcher = Matcher.SettlementMatcher(securitySettlements, self.__newSettlements)
        return self.__RemoveSettlementsFromLists(matcher.GetMatchedSettlementsList())

    def SecuritySettlements(self):
        return self.__securitySettlements

    def SetSettlements(self, oldSettlements, newSettlements):
        self.__oldSettlements = oldSettlements
        self.__newSettlements = newSettlements
        self.__securitySettlements = []

    def __RemoveSettlementsFromLists(self, matchedSettlements):
        pairOffPayments = list()
        if len(matchedSettlements):
            for (old, new) in matchedSettlements:
                if old and new:
                    if old in self.__oldSettlements:
                        self.__oldSettlements.remove(old)

                    if new in self.__newSettlements:
                        stateChart = acm.Operations.GetMappedSettlementProcessStateChart(new)
                        new.StateChart(stateChart)
                        if self.__IsModifed(old, new) == False:
                            if old in self.__securitySettlements:
                                self.__securitySettlements.remove(old)
                        self.__newSettlements.remove(new)
                elif old and old.Type() == SettlementType.PAIR_OFF_PAYMENT:
                    pairOffPayments.append(old)
        self.__HandlePairOffPayments(pairOffPayments)
        return self.__oldSettlements, self.__newSettlements

    def __HandlePairOffPayments(self, pairOffPayments):
        modInspector = Singleton.GetModInspector()
        for payment in pairOffPayments:
            oldCashSettlements = list()
            oldSecuritySettlements = list()
            pairOffParent = payment.PairOffParent()
            for settlement in pairOffParent.Children():
                if not settlement.IsSecurity():
                    oldCashSettlements.append(settlement)
                else:
                    oldSecuritySettlements.append(settlement)
            matcher = Matcher.SettlementMatcher(oldCashSettlements, self.__newSettlements)
            matchedSettlements = matcher.GetMatchedSettlementsList()
            cashSum = 0
            isModifed = False
            for (old, new) in matchedSettlements:
                if old and new:
                    stateChart = acm.Operations.GetMappedSettlementProcessStateChart(new)
                    new.StateChart(stateChart)
                    modifedFields = modInspector.GetModifiedFields(old, new)
                    if modifedFields == ['Amount']:
                        cashSum += new.CashAmount()
                    else:
                        isModifed = True
                        Utils.LogVerbose('The following fields should be updated for settlement %d: %s.' % (old.Oid(), modifedFields))
                        break
                    self.__newSettlements.remove(new)
            if not isModifed:
                if abs(payment.CashAmount() - cashSum) < 10e-6:
                    self.__securitySettlements.remove(payment)
                else:
                    Utils.LogVerbose('The following fields should be updated for settlement %d: %s.' % (old.Oid(), ['Amount']))
            if payment in self.__oldSettlements:
                self.__oldSettlements.remove(payment)

            matcher = Matcher.SettlementMatcher(oldSecuritySettlements, self.__newSettlements)
            matchedSettlements = matcher.GetMatchedSettlementsList()
            for (old, new) in matchedSettlements:
                if old and new:
                    self.__newSettlements.remove(new)


    def __IsModifed(self, old, new):
        modInspector = Singleton.GetModInspector()
        modifedFields = modInspector.GetModifiedFields(old, new)
        isModifed = False
        if modifedFields:
            if modifedFields == ['Status']:
                isModifed = old.Status() != SettlementStatus.PENDING_AMENDMENT
            elif all(field in ['ToPortfolio.Oid', 'FromPortfolio.Oid'] for field in modifedFields):
                isModified = False
                Utils.LogVerbose('Portfolio updates are ignored for settlement %d in security process.' % old.Oid())
            else:
                isModifed = True
                Utils.LogVerbose('The following fields should be updated for settlement %d: %s.' % (old.Oid(), modifedFields))
        else:
            Utils.LogVerbose('No relevant updates for settlement %d' % old.Oid())
        return isModifed

    def __GetSecuritySettlements(self):
        ret = []
        if not self.__ruleExecutor and len(self.__oldSettlements):
            self.__ruleExecutor = RuleExecutor([ \
                SettlementSecuritySelector.__IsPartOfPairOff(), \
                SettlementSecuritySelector.__IsCancelled(), \
                SettlementSecuritySelector.__IsRedemptionSecurity(), \
                SettlementSecuritySelector.__IsPostReleasedSecuritySettlement(), \
                SettlementSecuritySelector.__IsPartOfSecurityNetHierarchy(), \
                SettlementSecuritySelector.__IsCancelledSecuritySettlement(), \
                SettlementSecuritySelector.__IsPartOfCancelledSecurityNetHierarchy(), \
                SettlementSecuritySelector.__IsPartOfPartialSettlement(), \
                SettlementSecuritySelector.__IsReplaced(), \
                SettlementSecuritySelector.__IsPostReleasedValueDayAdjustedSecuritySettlement(), \
                ], \
                ActionFunction(SettlementSecuritySelector.GetSecuritySettlementsFallback))

        for s in self.__oldSettlements:
            self.__ruleExecutor.Execute(s, ValueType.SINGLE_VALUE, s, ret)
        return ret

    @staticmethod
    def __IsReplaced():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.REPLACED))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsSecuritySettlement(attribute, nodeToAddTo):
        node = nodeToAddTo.AddOpNode('OR')
        node.AddAttrNode(attribute, 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_NOMINAL))
        node.AddAttrNode(attribute, 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.AGGREGATE_SECURITY))
        node.AddAttrNode(attribute, 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.END_SECURITY))
        node.AddAttrNode(attribute, 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_DVP))

    @staticmethod
    def __IsParentDvPOrNormalNet(nodeToAddTo):
        node = nodeToAddTo.AddOpNode('OR')
        node.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SECURITIES_DVP_NET))
        node.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NET))

    @staticmethod
    def __IsPostReleasedSecuritySettlement():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.ACKNOWLEDGED))
        query.AddAttrNode('Parent', 'EQUAL', None)
        SettlementSecuritySelector.__IsSecuritySettlement('Type', query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsPartOfSecurityNetHierarchy():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)
        SettlementSecuritySelector.__IsSecuritySettlement('GetTopNonCancellationSettlementInHierarchy.Type', query)
        query.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.ACKNOWLEDGED))
        SettlementSecuritySelector.__IsParentDvPOrNormalNet(query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsCancelledSecuritySettlement():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        query.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode('GetTopSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCEL_CORRECT))
        orNode.AddAttrNode('GetTopSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCELLATION))
        SettlementSecuritySelector.__IsSecuritySettlement('Type', query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsPartOfPartialSettlement():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        query.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.PartialParent.Oid', 'NOT_EQUAL', 0)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsPartOfCancelledSecurityNetHierarchy():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)
        SettlementSecuritySelector.__IsSecuritySettlement('GetTopSettlementInHierarchy.Type', query)
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode('GetTopSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCEL_CORRECT))
        orNode.AddAttrNode('GetTopSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCELLATION))
        SettlementSecuritySelector.__IsParentDvPOrNormalNet(query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsCancelled():
        '''Rule that returns settlement that is cancelled'''

        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.CANCELLED))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.DoNotAddSettlement))

    @staticmethod
    def __IsRedemptionSecurity():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Type', 'EQUAL', Utils.GetEnum("SettlementCashFlowType", SettlementType.REDEMPTION_SECURITY))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.DoNotAddSettlement))

    @staticmethod
    def __IsPartOfPairOff():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        query.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.PairOffParent.Oid', 'NOT_EQUAL', 0)
        query.AddAttrNode('PairOffParent.Oid', 'NOT_EQUAL', 0)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def __IsPostReleasedValueDayAdjustedSecuritySettlement():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        query.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.VALUE_DAY_ADJUSTED))
        query.AddAttrNode('GetTopNonCancellationSettlementInHierarchy.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.ACKNOWLEDGED))
        SettlementSecuritySelector.__IsSecuritySettlement('Type', query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSecuritySelector.AppendSettlement))

    @staticmethod
    def GetSecuritySettlementsFallback(s, dummyL):
        pass

    @staticmethod
    def AppendSettlement(s, l):
        '''Add settlement to the return list l'''
        if s not in l:
            l.append(s)

    @staticmethod
    def DoNotAddSettlement(s, l):
        '''Do not add settlement s to return list l '''
