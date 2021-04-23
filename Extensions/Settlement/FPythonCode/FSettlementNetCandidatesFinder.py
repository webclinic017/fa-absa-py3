""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementNetCandidatesFinder.py"
"""
FSettlementNetCandidatesFinder module
"""
import acm
import FOperationsUtils as Utils
import FOperationsRuleEngine as Engine
from FSettlementCommitter import CommitAction
from FSettlementHierarchy import HierarchyTree
from FSettlementEnums import SettlementStatus, RelationType, NettingRuleType, SettlementDeliveryType, SettlementType
from FOperationsEnums import AccountType, InsType
import FSettlementStatusQueries as Queries

def BilateralNetting(settlement, settlementCandidate):
    isBilateralNetting = False
    if settlement.Acquirer().Oid() == settlementCandidate.Acquirer().Oid():
        if settlement.AcquirerAccount() == settlementCandidate.AcquirerAccount():
            if settlement.Counterparty().Oid() == settlementCandidate.Counterparty().Oid():
                if settlement.CounterpartyAccount() == settlementCandidate.CounterpartyAccount():
                    if settlementCandidate.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                        if settlement.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                            isBilateralNetting = True
    return isBilateralNetting

def IntraTradeNetting(settlement, settlementCandidate):
    isIntraTradeNetting = False
    if settlement.Trade() == settlementCandidate.Trade():
        if settlement.Acquirer().Oid() == settlementCandidate.Acquirer().Oid():
            if settlement.AcquirerAccount() == settlementCandidate.AcquirerAccount():
                if settlement.Counterparty().Oid() == settlementCandidate.Counterparty().Oid():
                    if settlement.CounterpartyAccount() == settlementCandidate.CounterpartyAccount():
                        if settlementCandidate.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                            if settlement.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                                isIntraTradeNetting = True
    return isIntraTradeNetting


def CloseTradeNetting(settlement, settlementCandidate):
    isCloseTradeNetting = False
    if settlement.Trade().Contract() == settlementCandidate.Trade().Contract():
        if settlement.Acquirer().Oid() == settlementCandidate.Acquirer().Oid():
            if settlement.AcquirerAccount() == settlementCandidate.AcquirerAccount():
                if settlement.Counterparty().Oid() == settlementCandidate.Counterparty().Oid():
                    if settlement.CounterpartyAccount() == settlementCandidate.CounterpartyAccount():
                        if settlementCandidate.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                            if settlement.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                                isCloseTradeNetting = True
    return isCloseTradeNetting

def ContractRefNetting(settlement, settlementCandidate):
    isContractRefNetting = False
    if settlement.Trade().ContractTrdnbr() == settlementCandidate.Trade().ContractTrdnbr():
        if settlement.Acquirer().Oid() == settlementCandidate.Acquirer().Oid():
            if settlement.AcquirerAccount() == settlementCandidate.AcquirerAccount():
                if settlement.Counterparty().Oid() == settlementCandidate.Counterparty().Oid():
                    if settlement.CounterpartyAccount() == settlementCandidate.CounterpartyAccount():
                        if settlementCandidate.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                            if settlement.DeliveryType() != SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                                isContractRefNetting = True
    return isContractRefNetting

def SecurityDvPNetting(settlement, settlementCandidate):
    isSecurityDvPNetting = False
    if settlement.Acquirer().Oid() == settlementCandidate.Acquirer().Oid():
        if settlement.AcquirerAccountRef() and settlementCandidate.AcquirerAccountRef():
            if settlement.AcquirerAccountRef().AccountType() != AccountType.CASH and settlementCandidate.AcquirerAccountRef().AccountType() != AccountType.CASH:
                if settlement.Counterparty().Oid() == settlementCandidate.Counterparty().Oid():
                    if settlement.CounterpartyAccountRef() and settlementCandidate.CounterpartyAccountRef():
                        if settlement.CounterpartyAccountRef().AccountType() != AccountType.CASH and settlementCandidate.CounterpartyAccountRef().AccountType() != AccountType.CASH:
                            if settlementCandidate.DeliveryType() == SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                                if settlement.DeliveryType() == SettlementDeliveryType.DELIVERY_VERSUS_PAYMENT:
                                        isSecurityDvPNetting = True
    return isSecurityDvPNetting

class NetCandidatesFinder(object):
    AutomaticNettingTypes = []

    def __init__(self):
        self.ruleExecutor1 = None
        self.ruleExecutor2 = None
        self.ruleExecutor3 = None

        NetCandidatesFinder.InitializeAutomaticNettingTypes()
        if NetCandidatesFinder.IsPreventAutomaticNetting():
            self.InitializePreventingAutomaticNettingQueries()
        else:
            self.InitializeDefaultAutomaticNettingQueries()
        self.InitializeNettingRuleQueries()
        self.InitializeAdHocNettingQueries()

    @staticmethod
    def InitializeAutomaticNettingTypes():
        import FSettlementParameters as SettlementParams
        NetCandidatesFinder.AutomaticNettingTypes = []
        if SettlementType.COUPON not in SettlementParams.preventAutomaticNetting:
            NetCandidatesFinder.AutomaticNettingTypes.append(SettlementType.COUPON)
        if SettlementType.REDEMPTION not in SettlementParams.preventAutomaticNetting:
            NetCandidatesFinder.AutomaticNettingTypes.append(SettlementType.REDEMPTION)
        if SettlementType.DIVIDEND not in SettlementParams.preventAutomaticNetting:
            NetCandidatesFinder.AutomaticNettingTypes.append(SettlementType.DIVIDEND)

    def InitializePreventingAutomaticNettingQueries(self):
        rules = list()
        if SettlementType.COUPON in NetCandidatesFinder.AutomaticNettingTypes:
            condition = Engine.QueryCondition(Queries.GetCouponQuery())
            rules.append(Engine.Rule(condition, Engine.ActionFunction(NetCandidatesFinder.GetStoredCouponRedemptionDividendCandidates)))
        if SettlementType.REDEMPTION in NetCandidatesFinder.AutomaticNettingTypes:
            condition = Engine.QueryCondition(Queries.GetRedemptionQuery())
            rules.append(Engine.Rule(condition, Engine.ActionFunction(NetCandidatesFinder.GetStoredCouponRedemptionDividendCandidates)))
        if SettlementType.DIVIDEND in NetCandidatesFinder.AutomaticNettingTypes:
            condition = Engine.QueryCondition(Queries.GetDividendQuery())
            rules.append(Engine.Rule(condition, Engine.ActionFunction(NetCandidatesFinder.GetStoredCouponRedemptionDividendCandidates)))
        self.ruleExecutor1 = Engine.RuleExecutor(rules, Engine.ActionFunction(NetCandidatesFinder.Fallback))

    def InitializeDefaultAutomaticNettingQueries(self):
        condition1 = Engine.QueryCondition(Queries.GetCouponRedemptionQuery())
        rule1 = Engine.Rule(condition1, Engine.ActionFunction(NetCandidatesFinder.GetStoredCouponRedemptionDividendCandidates))
        condition2 = Engine.QueryCondition(Queries.GetDividendQuery())
        rule2 = Engine.Rule(condition2, Engine.ActionFunction(NetCandidatesFinder.GetStoredCouponRedemptionDividendCandidates))
        self.ruleExecutor1 = Engine.RuleExecutor([rule1, rule2], Engine.ActionFunction(NetCandidatesFinder.Fallback))

    def InitializeNettingRuleQueries(self):
        condition3 = Engine.QueryCondition(Queries.GetApplicableForNettingQuery(NetCandidatesFinder.AutomaticNettingTypes))
        rule3 = Engine.Rule(condition3, Engine.ActionFunction(NetCandidatesFinder.GetNetCandidatesFromNettingRule))
        self.ruleExecutor2 = Engine.RuleExecutor([rule3], Engine.ActionFunction(NetCandidatesFinder.NetFallback))

    def InitializeAdHocNettingQueries(self):
        condition4 = Engine.QueryCondition(Queries.IsAdHocNetQuery())
        rule4 = Engine.Rule(condition4, Engine.ActionFunction(NetCandidatesFinder.GetAdHocNetCandidates))
        self.ruleExecutor3 = Engine.RuleExecutor([rule4], Engine.ActionFunction(NetCandidatesFinder.AddHocFallback))

    @staticmethod
    def IsPreventAutomaticNetting():
        if SettlementType.COUPON not in NetCandidatesFinder.AutomaticNettingTypes or \
            SettlementType.REDEMPTION not in NetCandidatesFinder.AutomaticNettingTypes or \
            SettlementType.DIVIDEND not in NetCandidatesFinder.AutomaticNettingTypes:
            return True
        return False

    @staticmethod
    def IsAboutToBeDeleted(settlement, settlementCommitterMap):
        isAboutToBeDeleted = False
        if settlement.Oid() in settlementCommitterMap:
            isAboutToBeDeleted = settlementCommitterMap[settlement.Oid()].GetCommitAction() == CommitAction.DELETE
        return isAboutToBeDeleted

    @staticmethod
    def AddSettlementToNetChildrenList(netCandidatesList, settlementCommitterMap, netChildrenList):
        for netCandidate in netCandidatesList:
            if NetCandidatesFinder.IsAboutToBeDeleted(netCandidate, settlementCommitterMap) == False:
                netChildrenList.Add(netCandidate)

    @staticmethod
    def IsSettlementApplicableForAutomaticNetting(settlement):
        applicable = settlement.Type() in NetCandidatesFinder.AutomaticNettingTypes
        return applicable

    def GetNetCandidates(self, settlementCommitter, settlementCommitterList, netChildrenList, possibleNettingCandidates, nettingRule, settlementCommitterMap):
        settlement = settlementCommitter.GetSettlement()
        netArray = acm.FArray()

        adHocNetcandidates = self.ruleExecutor3.Execute(settlement, Engine.ValueType.SINGLE_VALUE, settlementCommitter)
        if len(adHocNetcandidates):
            NetCandidatesFinder.AddSettlementToNetChildrenList(adHocNetcandidates,
                                                               settlementCommitterMap,
                                                               netChildrenList)
            return

        candidates = self.ruleExecutor1.Execute(settlement, Engine.ValueType.SINGLE_VALUE, settlementCommitter, settlementCommitterList)
        if len(candidates):
            NetCandidatesFinder.AddSettlementToNetChildrenList(candidates,
                                                               settlementCommitterMap,
                                                               netChildrenList)
            return


        self.ruleExecutor2.Execute(settlement, Engine.ValueType.SINGLE_VALUE, nettingRule, netArray, settlementCommitter, possibleNettingCandidates)
        NetCandidatesFinder.AddSettlementToNetChildrenList(netArray,
                                                           settlementCommitterMap,
                                                           netChildrenList)

    @staticmethod
    def GetNetCandidatesFromNettingRule(nettingRule, netChildrenList, settlementCommitter, possibleNettingCandidates):
        settlement = settlementCommitter.GetSettlement()
        if nettingRule:
            candidates = NetCandidatesFinder.FindNettingCandidates(nettingRule, settlement, possibleNettingCandidates)
            netChildrenList.AddAll(candidates)

    @staticmethod
    def CallNettingDefinition(nettingRule, settlement, settlementCandidate):
        if nettingRule.NettingDefinitionByValues():
            if not nettingRule.NettingDefinitionValues():
                Utils.LogAlways("Error: No Netting Definition Values set on the netting rule " + str(nettingRule.Name()))
                return False
            methodChains = nettingRule.NettingDefinitionValues().split(";")
            for aMethodChain in methodChains:
                if(aMethodChain):
                    method = acm.FMethodChain(acm.FSymbol(str(aMethodChain)))
                    if method:
                        valueSettlement = method.Call([settlement])
                        valueSettlementCandidate = method.Call([settlementCandidate])

                        if (valueSettlement == None) or (valueSettlementCandidate == None):
                            return False

                        if not valueSettlement == valueSettlementCandidate:
                            return False
                    else:
                        Utils.LogAlways("Warning: An incorrect method chain, " + str(aMethodChain) + ", was called for netting rule " + str(nettingRule.Name()) + ". This method chain will be ignored.")
            return True
        else:
            definition = str(nettingRule.NettingDefinitionHook())
            if not definition:
                Utils.LogAlways("Error: No Netting Definition Name set on the netting rule " + str(nettingRule.Name()))
                return False
            if definition.split('.')[0] != 'FSettlementNetCandidatesFinder':
                newModule = __import__(definition.split('.')[0]) # used in the eval
                commandString = 'newModule.'+ definition.split('.')[-1]+"(settlement, settlementCandidate)"
            else:
                commandString = definition.split('.')[-1] + "(settlement, settlementCandidate)"
            return eval(commandString)


    @staticmethod
    def IsValidNetStatusAndRelationType(settlement):

        if (settlement.Status() == SettlementStatus.AUTHORISED and
            (settlement.RelationType() == RelationType.NONE or
             settlement.RelationType() == RelationType.VALUE_DAY_ADJUSTED) and
            settlement.PartialParent() == None):
            return True
        else:
            parent = settlement.Parent()
            if (parent and parent.PartialParent() == None):
                if (parent.RelationType() == RelationType.NET or
                    parent.RelationType() == RelationType.CLOSE_TRADE_NET or
                    parent.RelationType() == RelationType.SECURITIES_DVP_NET):
                    return (parent.Status() == SettlementStatus.AUTHORISED or
                            parent.Status() == SettlementStatus.MANUAL_MATCH)

    @staticmethod
    def MatchingInstruments(settlement, candidate):
        if settlement.Instrument() == candidate.Instrument():
            return True
        if not settlement.Instrument().Underlying():
            return False
        if not candidate.Instrument().Underlying():
            return False
        return settlement.Instrument().Underlying() == candidate.Instrument().Underlying()

    @staticmethod
    def FindNettingCandidates(nettingRule, settlement, settlementCandidates):
        result = list()
        securityCurrency = settlement.Trade().Instrument().Currency().Name()
        cashCurrency = settlement.Trade().Currency().Name()
        for candidate in settlementCandidates:
            if candidate != settlement:
                if NetCandidatesFinder.IsValidNetStatusAndRelationType(candidate):
                    if not NetCandidatesFinder.IsSettlementApplicableForAutomaticNetting(candidate):
                        if nettingRule.NettingRuleType() == NettingRuleType.SECURITIES_DVP_NET:
                            if candidate.Trade().Currency().Name() == cashCurrency and \
                               candidate.Trade().Instrument().Currency().Name() == securityCurrency:
                                if NetCandidatesFinder.MatchingInstruments(settlement, candidate):
                                    if NetCandidatesFinder.CallNettingDefinition(nettingRule, settlement, candidate):
                                        result.append(candidate)
                        elif settlement.AccountType() == candidate.AccountType():
                            if settlement.IsSecurity() and candidate.IsSecurity():
                                if settlement.SecurityInstrument() == candidate.SecurityInstrument():
                                    if NetCandidatesFinder.CallNettingDefinition(nettingRule, settlement, candidate):
                                        result.append(candidate)
                            else:
                                if NetCandidatesFinder.CallNettingDefinition(nettingRule, settlement, candidate):
                                    result.append(candidate)
        return result


    @staticmethod
    def AddTypeAndAquirerData(settlement, query):
        import FSettlementParameters as SettlementParams

        cashFlow = settlement.CashFlow()
        dividend = settlement.Dividend()
        if cashFlow and (SettlementType.COUPON in NetCandidatesFinder.AutomaticNettingTypes or SettlementType.REDEMPTION in NetCandidatesFinder.AutomaticNettingTypes):
            query.AddAttrNode('CashFlow.Oid', 'EQUAL', cashFlow.Oid())
            or1 = query.AddOpNode('OR')
            if SettlementType.COUPON in NetCandidatesFinder.AutomaticNettingTypes:
                or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.COUPON))
            if SettlementType.REDEMPTION in NetCandidatesFinder.AutomaticNettingTypes:
                or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.REDEMPTION))
            if SettlementParams.alternativeCouponHandling == False:
                query.AddAttrNode('AcquirerName', 'EQUAL', settlement.AcquirerName())
                query.AddAttrNode('AcquirerAccount', 'EQUAL', settlement.AcquirerAccount())
        elif SettlementType.DIVIDEND in NetCandidatesFinder.AutomaticNettingTypes:
            query.AddAttrNode('AcquirerName', 'EQUAL', settlement.AcquirerName())
            query.AddAttrNode('AcquirerAccount', 'EQUAL', settlement.AcquirerAccount())
            query.AddAttrNode('Dividend.Oid', 'EQUAL', dividend.Oid())
            query.AddAttrNode('SecurityInstrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.STOCK))
            or1 = query.AddOpNode('OR')
            or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.DIVIDEND))


    @staticmethod
    def IsReferencingSamePortfolio(settlement1, settlement2):

        portfolioOid1 = 0
        portfolioOid2 = 0

        if settlement1.ToPortfolio():
            portfolioOid1 = settlement1.ToPortfolio().Oid()
        elif settlement1.FromPortfolio():
            portfolioOid1 = settlement1.FromPortfolio().Oid()

        if settlement2.ToPortfolio():
            portfolioOid2 = settlement2.ToPortfolio().Oid()
        elif settlement2.FromPortfolio():
            portfolioOid2 = settlement2.FromPortfolio().Oid()

        return portfolioOid1 == portfolioOid2

    @staticmethod
    def GetAdHocNetCandidates(settlementCommitter):
        candidates = list()
        settlement = settlementCommitter.GetSettlement()
        hierarchyTree = HierarchyTree(settlement)
        if hierarchyTree.IsNetHierarchyPartOfHierarchy() == True:
            return candidates
        adHocNetParent = settlement.Parent()
        adHocNetChildren = adHocNetParent.Children()
        nonValidStatuses = [SettlementStatus.EXCEPTION, SettlementStatus.PENDING_AMENDMENT]
        for adHocNetChild in adHocNetChildren:
            if adHocNetChild.Oid() != settlement.Oid():
                if settlement.Status() not in nonValidStatuses and adHocNetChild.Status() not in nonValidStatuses:
                    if adHocNetChild.RelationType() == RelationType.NONE:
                        if acm.Operations.IsValidAdHocNetPair(settlement, adHocNetChild):
                            candidates.append(adHocNetChild)
        return candidates


    @staticmethod
    def GetStoredCouponRedemptionDividendCandidates(settlementCommitter, settlementCommitterList):


        settlement = settlementCommitter.GetSettlement()
        candidates = []

        if settlement.Type() not in NetCandidatesFinder.AutomaticNettingTypes:
            return candidates

        if not settlement.CashFlow() and not settlement.Dividend():
            return candidates

        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('CounterpartyName', 'EQUAL', settlement.CounterpartyName())
        query.AddAttrNode('Trade.Oid', 'GREATER', 0)
        query.AddAttrNode('SettlementType', 'EQUAL', settlement.SettlementType())

        NetCandidatesFinder.AddTypeAndAquirerData(settlement, query)
        or2 = query.AddOpNode('OR')
        and1 = or2.AddOpNode('AND')
        and1.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NONE))
        and1.AddAttrNode('Parent', 'EQUAL', None)
        and1.AddAttrNode('SplitParent', 'EQUAL', None)
        or1 = and1.AddOpNode('OR')
        or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.AUTHORISED))
        or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.EXCEPTION))
        and2 = or2.AddOpNode('AND')
        if settlement.Type() == SettlementType.COUPON:
            and2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.COUPON_NET))
        elif settlement.Type() == SettlementType.DIVIDEND:
            and2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.DIVIDEND_NET))
        elif settlement.Type() == SettlementType.REDEMPTION:
            and2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.REDEMPTION_NET))
        or3 = and2.AddOpNode('OR')
        or3.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.NEW))
        or3.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.EXCEPTION))
        or3.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.AUTHORISED))
        or3.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.MANUAL_MATCH))

        possibleCandidates = list()
        if settlement.CashFlow():
            for i in acm.FSettlement.Select( 'cashFlow = %d and oid <> %d' % (settlement.CashFlow().Oid(), settlement.Oid())):
                possibleCandidates.append(i)
        elif settlement.Dividend():
            for i in acm.FSettlement.Select( 'dividend = %d and oid <> %d' % (settlement.Dividend().Oid(), settlement.Oid())):
                possibleCandidates.append(i)

        for possibleCandidate in possibleCandidates:
            NetCandidatesFinder.AppendCouponRedemptionDividend(settlement, possibleCandidate, candidates, query)
        for settlementCommitter in settlementCommitterList:
            if settlementCommitter.GetSettlement().Oid() < 0:
                NetCandidatesFinder.AppendCouponRedemptionDividend(settlement, settlementCommitter.GetSettlement(), candidates, query)

        return candidates


    @staticmethod
    def AppendCouponRedemptionDividend(settlement, settlementCandidate, candidatesList, query):
        import FSettlementParameters as SettlementParams
        if query.IsSatisfiedBy(settlementCandidate):
            if SettlementParams.alternativeCouponHandling == False and \
               (settlementCandidate.Type() == SettlementType.COUPON or settlementCandidate.Type() == SettlementType.REDEMPTION):
                if NetCandidatesFinder.IsReferencingSamePortfolio(settlement, settlementCandidate):
                    candidatesList.append(settlementCandidate)
            else:
                candidatesList.append(settlementCandidate)

    @staticmethod
    def Fallback(dummySettlementCommitter, dummySettlementCommitterList):

        return []

    @staticmethod
    def AddHocFallback(dummySettlementCommitter):

        return []

    @staticmethod
    def NetFallback(dummyNettingRule, dummyNetChildrenList, dummySettlementCommitter, dummySettlementCandidates):
        return []
