""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementNettingEngine.py"
import acm
import FSettlementNetting
from FSettlementEnums import RelationType, NettingRuleType, SettlementType
from collections import defaultdict
from itertools import chain
import FOperationsUtils as Utils
import FSettlementStatusQueries as Queries
import types
import FSettlementValidations as Validations
try:
    import FSettlementClientNetting
except ImportError:
    import FSettlementClientNettingTemplate as FSettlementClientNetting

class SettlementNettingEngine(object):
    def __init__(self, nettingRuleQueryCache):
        self.__nettingRuleQueryCache = nettingRuleQueryCache

    def Net(self, settlementCommitterList, settlementCommitterMap):
        netParentCleanUpList = list()
        netHierarchiesList = list()
        if len(settlementCommitterList) > 0:
            sortedAndFilteredSettlementsInCommitterList, valueDayCurrencyPairs  = self.__SortAndFilterByNettingAttributes(settlementCommitterList)
            allPossibleNettingCandidates = self.__FindAllPossibleNettingCandidates(valueDayCurrencyPairs)
            sortedAndFilteredPossibleNettingCandidates = self.__SortAndFilterListOfSettlementsByNettingAttributes(allPossibleNettingCandidates, sortedAndFilteredSettlementsInCommitterList)


            while(len(settlementCommitterList)):
                settlementCommitter = settlementCommitterList.pop()
                settlement = settlementCommitter.GetSettlement()
                netHierarchyList = list()
                if not settlement.Children() or settlement.RelationType() == RelationType.VALUE_DAY_ADJUSTED or Validations.IsCorrectedSingleRecord(settlement):
                    nettingRule = settlementCommitter.GetNettingRule()
                    if nettingRule and nettingRule.NettingRuleType() == NettingRuleType.SECURITIES_DVP_NET:
                        securityCurrencyName = settlement.Trade().Instrument().Currency().Name()
                        cashCurrencyName = settlement.Trade().Currency().Name()
                    else:
                        securityCurrencyName = settlement.Currency().Name()
                        cashCurrencyName = settlement.Currency().Name()

                    if nettingRule:
                        possibleNettingCandidates = list()
                        for settlement in sortedAndFilteredSettlementsInCommitterList[nettingRule.Name()][settlement.ValueDay()][securityCurrencyName][cashCurrencyName]:
                            if settlement.Oid() < 0 or settlement.IsModified():
                                if not settlement.RestrictNet():
                                    if not settlement.ManualMatch() and settlement not in possibleNettingCandidates:
                                        possibleNettingCandidates.append(settlement)
                        possibleNettingCandidates.extend(self.__FilterOutExistingCandidates(possibleNettingCandidates, sortedAndFilteredPossibleNettingCandidates[nettingRule.Name()][settlement.ValueDay()][securityCurrencyName][cashCurrencyName]))
                        netHierarchyList = FSettlementNetting.Net(settlementCommitter, netParentCleanUpList, settlementCommitterList, possibleNettingCandidates, nettingRule, settlementCommitterMap)
                    else:
                        netHierarchyList = FSettlementNetting.Net(settlementCommitter, netParentCleanUpList, settlementCommitterList, list(), nettingRule, settlementCommitterMap)
                netHierarchiesList.append((settlementCommitter, netHierarchyList))

        return netHierarchiesList, netParentCleanUpList

    def __FindAllPossibleNettingCandidates(self, valueDayCurrencyPairs):
        if not valueDayCurrencyPairs:
            return list()

        possibleNettingCandidates = list()
        for (valueDay, currency) in valueDayCurrencyPairs:
            possibleNettingCandidates.extend(acm.FSettlement.Select("valueDay = '{}' currency = '{}' restrictNet = false manualMatch = false".format(valueDay, currency)))
            
        return possibleNettingCandidates

    def __SortAndFilterListOfSettlementsByNettingAttributes(self, settlements, sorting):
        sortedSettlements = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(list))))
        for settlement in settlements:
            nettingRule = self.__FindNettingRule(settlement)
            if nettingRule:
                nettingRuleName = nettingRule.Name()
                valueDay = settlement.ValueDay()
                if settlement.Trade():
                    if nettingRule.NettingRuleType() == NettingRuleType.SECURITIES_DVP_NET:
                        securityCurrencyName = settlement.Trade().Instrument().Currency().Name()
                        cashCurrencyName = settlement.Trade().Currency().Name()
                    else:
                        securityCurrencyName = settlement.Currency().Name()
                        cashCurrencyName = settlement.Currency().Name()
                    if sorting[nettingRuleName][valueDay][securityCurrencyName][cashCurrencyName]:
                        sortedSettlements[nettingRuleName][valueDay][securityCurrencyName][cashCurrencyName].append(settlement)

        return sortedSettlements

    def __SortAndFilterByNettingAttributes(self, settlementCommitters):
        sortedSettlementCommitters = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(list))))
        automaticNettingType = self.__GetAutomaticNettingTypes()
        applicableForNettingQuery = Queries.GetApplicableForNettingQuery(automaticNettingType)
        valueDayCurrencyPairs = set()
        for sc in settlementCommitters:
            settlement = sc.GetSettlement()
            if applicableForNettingQuery.IsSatisfiedBy(settlement):
                nettingRule = self.__FindNettingRule(settlement)
                if nettingRule:
                    nettingRuleName = nettingRule.Name()
                    if settlement.Trade():                        
                        valueDay = settlement.ValueDay()
                        currencyName = settlement.Currency().Name()
                        valueDayCurrencyPairs.add((valueDay, currencyName))
                        if nettingRule.NettingRuleType() == NettingRuleType.SECURITIES_DVP_NET:
                            cashCurrencyName = settlement.Trade().Currency().Name()
                            securityCurrencyName = settlement.Trade().Instrument().Currency().Name()
                            if settlement.IsSecurity():
                                valueDayCurrencyPairs.add((valueDay, cashCurrencyName))
                            else:
                                valueDayCurrencyPairs.add((valueDay, securityCurrencyName))
                            sortedSettlementCommitters[nettingRuleName][valueDay][securityCurrencyName][cashCurrencyName].append(settlement)
                        else:
                            sortedSettlementCommitters[nettingRuleName][valueDay][currencyName][currencyName].append(settlement)

                        sc.SetNettingRule(nettingRule)

        return sortedSettlementCommitters, valueDayCurrencyPairs

    def __FindNettingRule(self, settlement):
        nettingRuleLinks = self.__GetNettingRuleLinks(settlement)
        bestMatchingRule = None
        parent = settlement.Parent()
        if parent and parent.RelationType() in [RelationType.COUPON_NET, RelationType.REDEMPTION_NET, RelationType.DIVIDEND_NET]:
            return None

        for nettingRuleLink in nettingRuleLinks:
            if nettingRuleLink.NettingRule().Query():
                query = self.__nettingRuleQueryCache.GetNettingQuery(nettingRuleLink.NettingRule().Query().Name())
                if query:
                    if query.IsSatisfiedBy(settlement):
                        if self.__IsApplicableAfterClientNetting(nettingRuleLink.NettingRule(), settlement):
                            bestMatchingRule = nettingRuleLink.NettingRule()
                            break
                else:
                    Utils.LogVerbose("Warning: Could not find query {} for netting rule {}".format(nettingRuleLink.NettingRule().Query().Name(), nettingRuleLink.NettingRule().Name()))
            else:
                Utils.LogVerbose("Warning: No query set on the netting rule {}".format(nettingRuleLink.NettingRule().Name()))
        return bestMatchingRule

    def __GetNettingRuleLinks(self, settlement):
        nettingRuleLinks = list()
        counterparty = settlement.Counterparty()
        if counterparty:
            for nettingRuleLink in counterparty.NettingRuleLinks().SortByProperty('OrderNumber', True):
                if nettingRuleLink.Enabled():
                    nettingRuleLinks.append(nettingRuleLink)
        return nettingRuleLinks

    def __IsApplicableAfterClientNetting(self, rule, settlement):
        applicable = True
        if rule.NettingHook():
            applicable = False
            hookName = rule.NettingHook()
            try:
                clientNettingFunction = getattr(FSettlementClientNetting, hookName)
                if not type(clientNettingFunction) == types.FunctionType:
                    raise TypeError('Attribute %s in module FSettlementClientNetting is not a function.' % hookName)
                applicable = clientNettingFunction(settlement)
            except AttributeError:
                Utils.LogAlways('Attribute %s could not be found in module FSettlementClientNetting.' % hookName)
            except TypeError as error:
                Utils.LogAlways(error)
        return applicable

    def __GetAutomaticNettingTypes(self):
        import FSettlementParameters as SettlementParams
        automaticNettingTypes = list()
        if SettlementType.COUPON not in SettlementParams.preventAutomaticNetting:
            automaticNettingTypes.append(SettlementType.COUPON)
        if SettlementType.REDEMPTION not in SettlementParams.preventAutomaticNetting:
            automaticNettingTypes.append(SettlementType.REDEMPTION)
        if SettlementType.DIVIDEND not in SettlementParams.preventAutomaticNetting:
            automaticNettingTypes.append(SettlementType.DIVIDEND)

        return automaticNettingTypes

    def __FilterOutExistingCandidates(self, possibleNettingCandidates, sortedAndFilteredPossibleNettingCandidates):
        candidateOids = list(chain([settlement.Oid() for settlement in possibleNettingCandidates]))
        return list(ifilter(lambda settlement: settlement.Oid() not in candidateOids, sortedAndFilteredPossibleNettingCandidates ))
