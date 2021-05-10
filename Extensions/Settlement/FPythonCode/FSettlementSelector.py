""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSelector.py"
import acm
from FOperationsRuleEngine import QueryCondition, RuleExecutor, Rule, ValueType, ActionFunction, Condition
from FSettlementEnums import RelationType, SettlementStatus, SettlementType
import FOperationsUtils as Utils
import FSettlementSelectorConditionFunctions as ConditionFunctions

class IsCorrectedTradeCondition(Condition):
    def __init__(self):


        Condition.__init__(self)

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        assert value.IsKindOf(acm.FSettlement), 'No settlement given.'
        isMet = False
        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = ConditionFunctions.IsCorrectedTrade(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class IsInactivePartial(Condition):
    def __init__(self):


        Condition.__init__(self)

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        assert value.IsKindOf(acm.FSettlement), 'No settlement given.'
        isMet = False
        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = ConditionFunctions.IsInactivePartial(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class IsInactivePairOff(Condition):
    def __init__(self):


        Condition.__init__(self)

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        assert value.IsKindOf(acm.FSettlement), 'No settlement given.'
        isMet = False

        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = ConditionFunctions.IsInactivePairOff(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class IsInactivePartOfPartial(Condition):
    def __init__(self):


        Condition.__init__(self)

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        assert value.IsKindOf(acm.FSettlement), 'No settlement given.'
        isMet = False

        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = ConditionFunctions.IsInactivePartOfPartial(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class IsInactivePartOfPairOff(Condition):
    def __init__(self):


        Condition.__init__(self)

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        assert value.IsKindOf(acm.FSettlement), 'No settlement given.'
        isMet = False

        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = ConditionFunctions.IsInactivePartOfPairOff(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class IsStoredForAccounting(Condition):
    def __init__(self):
        Condition.__init__(self)

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        assert value.IsKindOf(acm.FSettlement), 'No settlement given.'
        isMet = False
        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = ConditionFunctions.IsStoredForAccounting(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class SettlementSelector(object):
    '''This class includes functions for retrieving settlements from FTrade.
    Initial published functions are GetUpdateCandidates and GetAllTradeSettlements.'''

    def __init__(self, fTrade):
        ''' Constructor. '''
        self.__fTrade = fTrade
        if fTrade:
            self.__settlements = self.__AllTradeSettlements()
        else:
            self.__settlements = []

        self.__ruleExecutor = None


    def __AllTradeSettlements(self):
        ''' AllTradeSettlements '''

        settlementList = []
        for settlement in self.__fTrade.Settlements():
            if settlement.Type() != SettlementType.STAND_ALONE_PAYMENT and settlement.RelationType() == RelationType.NONE:
                settlementList.append(settlement)
        return settlementList

    def GetSettlements(self):
        '''This function returns all settlements including those that are
        connected to the trade via sec_insaddr.
        '''

        return self.__settlements

    def SetSettlements(self, settlementList):
        self.__settlements = settlementList

    def GetUpdateCandidates(self):
        '''Returns settlements that should be taken into
        consideration by the matching process.'''

        ret = []
        if not self.__ruleExecutor and len(self.__settlements):
            self.__ruleExecutor = RuleExecutor([ \
                SettlementSelector.__IsValueDayAdjusted(), \
                SettlementSelector.__IsInactivePartial(), \
                SettlementSelector.__IsInactivePairOff(), \
                SettlementSelector.__IsInactivePartOfPartial(), \
                SettlementSelector.__IsInactivePartOfPairOff(), \
                SettlementSelector.__IsSettlementStoredForAccounting(), \
                SettlementSelector.__IsPartOfPairOff(), \
                SettlementSelector.__IsPartOfPartial(), \
                SettlementSelector.__IsCancelled(), \
                SettlementSelector.__IsTradeCorrectedAndPostReleasedSettlements(), \
                SettlementSelector.__IsManuallyAdjusted(), \
                SettlementSelector.__IsVoidAndHasChildren(), \
                SettlementSelector.__IsReferencedAndInVUR(), \
                SettlementSelector.__IsSingleRow(), \
                SettlementSelector.__IsClosedAfterOperationsAction(), \
                SettlementSelector.__IsParentOfCancelCorrect(), \
                SettlementSelector.__IsReplaced(), \
                SettlementSelector.__IsAwaitingCancellation()
                ], \
                ActionFunction(SettlementSelector.GetUpdateCandidatesFallback))

        for s in self.__settlements:
            self.__ruleExecutor.Execute(s, ValueType.SINGLE_VALUE, s, ret)
        printList = []
        for settlement in ret:
            printList.append(settlement.Oid())
        Utils.LogVerbose('SettlementSelector returns %s' % printList)

        return ret

    @staticmethod
    def __IsInactivePartial():
        return Rule(IsInactivePartial(), ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsInactivePairOff():
        return Rule(IsInactivePairOff(), ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsInactivePartOfPartial():
        return Rule(IsInactivePartOfPartial(), ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsInactivePartOfPairOff():
        return Rule(IsInactivePartOfPairOff(), ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsTradeCorrectedAndPostReleasedSettlements():
        return Rule(IsCorrectedTradeCondition(), ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsSettlementStoredForAccounting():
        return Rule(IsStoredForAccounting(), ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsManuallyAdjusted():
        '''Rule that returns settlement that is not adjusted.'''
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        query.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.ADJUSTED))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsReplaced():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.REPLACED))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))


    @staticmethod
    def __IsVoidAndHasChildren():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        query.AddAttrNode('NumberOfChildren', 'GREATER', 0)
        query.AddAttrNode('RelationType', 'NOT_EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SPLIT))
        query.AddAttrNode('Children.RelationType', 'NOT_EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCEL_CORRECT))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsVUR(nodeToAddTo):
        '''OR node for settlements to be updated.'''

        node = nodeToAddTo.AddOpNode('OR')
        node.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        node.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.UPDATED))
        node.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.RECALLED))
        node.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.PENDING_AMENDMENT))

    @staticmethod
    def __IsNotPartialSettlementPart(nodeToAddTo):
        '''OR node for settlements to be updated.'''

        node = nodeToAddTo.AddOpNode('OR')
        andQuery1 = node.AddOpNode('AND')
        andQuery1.AddAttrNode('Parent.Oid', 'EQUAL', 0)
        andQuery1.AddAttrNode('PartialParent.Oid', 'EQUAL', 0)
        andQuery2 = node.AddOpNode('AND')
        andQuery2.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
        andQuery2.AddAttrNode('Parent.PartialParent.Oid', 'EQUAL', 0)

    @staticmethod
    def __IsReferencedAndInVUR():
        '''Rule that returns settlement that is single row and in status VUR'''
        #IsPartOfHierarchy
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)
        query.AddAttrNode('RelationType', 'NOT_EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SPLIT))
        SettlementSelector.__IsVUR(query)
        SettlementSelector.__IsNotPartialSettlementPart(query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsSingleRow():
        '''Rule that returns settlement that is not part of Hierarchy'''

        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('IsPartOfHierarchy', 'EQUAL', False)
        SettlementSelector.__IsNotPartialSettlementPart(query)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsClosedAfterOperationsAction():
        """
        This rule considers the following hierarchy:
        s2    settleSettlement = s1
        |__s1 status = Closed

        Return s1
        """
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('NumberOfChildren', 'EQUAL', 0)
        query.AddAttrNode('Parent.Oid', 'GREATER', 0)
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.CLOSED))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsCancelled():
        '''Rule that finds settlement that is cancelled'''

        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        andNode1 = query.AddOpNode('AND')
        andNode1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.CANCELLED))
        andNode2 = query.AddOpNode('AND')
        andNode2.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        andNode2.AddAttrNode('Parent', 'NOT_EQUAL', 0)
        andNode2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum("SettlementRelationType", RelationType.CANCELLATION))
        andNode2.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        andNode3 = query.AddOpNode('AND')
        andNode3.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        andNode3.AddAttrNode('Parent', 'NOT_EQUAL', 0)
        andNode3.AddAttrNode('Parent.Parent', 'NOT_EQUAL', 0)
        andNode3.AddAttrNode('Parent.Parent.RelationType', 'EQUAL', Utils.GetEnum("SettlementRelationType", RelationType.CANCELLATION))
        andNode3.AddAttrNode('Parent.Parent.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.VOID))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def __IsParentOfCancelCorrect():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)
        query.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NONE))
        query.AddAttrNode('NumberOfChildren', 'EQUAL', 1)
        query.AddAttrNode('Children.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCEL_CORRECT))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsSecuritySettlement(nodeToAddTo):
        node = nodeToAddTo.AddOpNode('OR')
        node.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_NOMINAL))
        node.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.AGGREGATE_SECURITY))
        node.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.END_SECURITY))
        node.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_DVP))

    @staticmethod
    def __IsAwaitingCancellation():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.AWAITING_CANCELLATION))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsPartOfPairOff():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        andNode1 = query.AddOpNode('AND')
        andNode1.AddAttrNode('PairOffParent.Oid', 'NOT_EQUAL', 0)
        andNode2 = query.AddOpNode('AND')
        andNode2.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
        andNode2.AddAttrNode('Parent.PairOffParent.Oid', 'NOT_EQUAL', 0)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsPartOfPartial():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        query.AddAttrNode('PartialParent.Oid', 'NOT_EQUAL', 0)
        query.AddAttrNode('NumberOfPartialChildren', 'NOT_EQUAL', 0)
        andNode1 = query.AddOpNode('AND')
        andNode1.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
        andNode1.AddAttrNode('Parent.PartialParent.Oid', 'NOT_EQUAL', 0)
        andNode2 = query.AddOpNode('AND')
        andNode2.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
        andNode2.AddAttrNode('Parent.NumberOfPartialChildren', 'NOT_EQUAL', 0)
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.AppendSettlement))

    @staticmethod
    def __IsValueDayAdjusted():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        query.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.VALUE_DAY_ADJUSTED))
        condition = QueryCondition(query)
        return Rule(condition, ActionFunction(SettlementSelector.DoNotAddSettlement))

    @staticmethod
    def GetUpdateCandidatesFallback(s, dummyL):
        '''Print to the log if a settlement does not satisfy any rule.'''
        Utils.LogVerbose('Settlement %s does not match any rule and will not be updated.' % (s.Name()))

    @staticmethod
    def AppendSettlement(s, l):
        '''Add settlement to the return list l'''
        if s not in l:
            l.append(s)

    @staticmethod
    def DoNotAddSettlement(s, l):
        '''Do not add settlement s to return list l '''

class SettlementPicker(SettlementSelector):
    def __init__(self, settlementList):
        SettlementSelector.__init__(self, None)
        self.SetSettlements(settlementList)

def ShowMembers(l):
    '''Use if you want get all members in the FObject list. '''

    return [s.Oid() for s in l]

