""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementUtils.py"
import acm
import FOperationsUtils as Utils
from FSettlementHierarchy import HierarchyTree
from FOperationsDateUtils import AdjustDateToday
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator
from FSettlementStatusQueries import GetIsClosingPayoutTradeQuery, GetIsClosingTradeQuery, GetIsNDFTradeQuery
from FOperationsEnums import TradeType, InsType
from FSettlementEnums import SettlementStatus
from FOperationsExceptions import InvalidHookException

INFINITE_NUMBER_OF_DAYS = None

def IsApplicableForPayoutProcessing(instrument):

    return (instrument.Otc() == True)

def GetSettlementNetParent(settlement):

    parent = None
    if settlement.Parent():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Oid', 'EQUAL', settlement.Parent().Oid())
        resultSet = query.Select()
        if len(resultSet):
            parent = resultSet[0]
    return parent

def IsWithinTimeWindow(settlement):
    if settlement.Trade():
        calendar = settlement.Trade().Currency().Calendar()
    else:
        calendar = settlement.Currency().Calendar()

    startDate = GetHookAdministrator().HA_CallHook(SettlementHooks.GET_DAYS_BACK, settlement)
    adjustedStartDate = AdjustDateToday(calendar, -startDate)
    if settlement.ValueDay() < adjustedStartDate:
        return False
    endDate = GetHookAdministrator().HA_CallHook(SettlementHooks.GET_DAYS_FORWARD, settlement)
    adjustedEndDate = AdjustDateToday(calendar, endDate)
    return (settlement.ValueDay() >= adjustedStartDate and settlement.ValueDay() <= adjustedEndDate)

def IsBeforeTimeWindow(settlement):
    if settlement.Trade():
        calendar = settlement.Trade().Currency().Calendar()
    else:
        calendar = settlement.Currency().Calendar()

    startDate = GetHookAdministrator().HA_CallHook(SettlementHooks.GET_DAYS_BACK, settlement)
    adjustedStartDate = AdjustDateToday(calendar, -startDate)

    return True if settlement.ValueDay() < adjustedStartDate else False


def __GetClosingTrades(trade, query):
    closingTrades = list()
    tradeCandidates = acm.FTrade.Select('contractTrdnbr = %d' % trade.Oid())
    for _trade in tradeCandidates:
        if query.IsSatisfiedBy(_trade):
            closingTrades.append(_trade)
    return closingTrades

def GetClosingTrades(trade):
    return __GetClosingTrades(trade, GetIsClosingTradeQuery())

def GetClosingPayoutTrades(trade):
    return __GetClosingTrades(trade, GetIsClosingPayoutTradeQuery())

def IsClosingTrade(trade):
    return trade.Type() == TradeType.CLOSING

def IsClosedTrade(trade):
    return len(GetClosingTrades(trade)) != 0

def IsNDFTrade(trade):
    return GetIsNDFTradeQuery().IsSatisfiedBy(trade)

def GetNonExcludedTrades(trades):
    _trades = list()
    for trade in trades:
        try:
            if GetHookAdministrator().HA_CallHook(SettlementHooks.EXCLUDE_TRADE, trade) == False:
                _trades.append(trade)
        except InvalidHookException as error:
            Utils.LogAlways('Skipping trade %s due to error' % str(trade.Oid()))
            Utils.LogAlways(error)

    return _trades


def CorrectTradePayNet(settlement):
    import FSettlementParameters as Params
    if hasattr(Params, 'correctTradePayNetQueries'):
        for aQuery in Params.correctTradePayNetQueries:
            payNetQuery = Utils.GetStoredQuery(aQuery, acm.FSettlement)
            if payNetQuery:
                if payNetQuery.Query().IsSatisfiedBy(settlement):
                    return True
    return False

def FindRootInHierarchyTree(settlement):
    hierarchyTree = HierarchyTree(settlement)
    for aNodePath in hierarchyTree.GetNodePaths():
        for aSettlement in aNodePath.GetSettlements():
            if aSettlement.Parent() == None:
                return aSettlement
    return settlement

def FindRootInPartialHierarchyTree(settlement):
    partialTopParent = None

    if settlement.PartialParent():
        partialTopParent = FindRootInPartialHierarchyTree(settlement.PartialParent())
    elif settlement.PartialChildren() and not settlement.PartialParent():
        partialTopParent = settlement
    return partialTopParent

def FindRootInPairOffHierarchyTree(settlement):
    pairOffTopParent = None

    if settlement.PairOffParent():
        pairOffTopParent = FindRootInPairOffHierarchyTree(settlement.PairOffParent())
    elif settlement.PairOffChildren() and not settlement.PairOffParent():
        pairOffTopParent = settlement
    return pairOffTopParent

def CallMethodChain(attribute, settlement):
    methodChain = acm.FMethodChain(attribute)
    if methodChain:
        try:
            value = methodChain.Call([settlement])
        except Exception:
            Utils.LogAlways('Exception occurred when trying to extract value from settlement %s' % str(settlement.Oid()))
    return str(value) if value else ''

def ComputeKeyForSettlement(settlement):
    chains = ['Type', 'ValueDay', 'Dividend.Oid', 'Payment.Oid', 'CashFlow.Oid']

    keyValues = None
    try:
        keyValues = [CallMethodChain(attribute, settlement) for attribute in chains]
    except Exception:
        Utils.LogAlways('Exception when computing keys for settlement %s' % (str(settlement.Oid())))
        return None

    if settlement.SecurityInstrument() and settlement.CashFlow() == None and settlement.Dividend() == None:
        keyValues.append(str(settlement.SecurityInstrument().Oid()))
    keyValues = '-'.join(keyValues)

    return keyValues

def MergeSameSourceSettlements(trade, settlementList):
    ''' MergeSameSourceSettlements is used to merge the amount if two or more
        settlements has the same source
    '''
    settlementDict = {}
    if trade.Instrument().InsType() == InsType.COMBINATION:
        for settlement in settlementList:
            keyValue = ComputeKeyForSettlement(settlement)
            if keyValue not in settlementDict:
                settlementDict[keyValue] = settlement
            else:
                settlementDict[keyValue] = AddUpAmountsForSameSourceSettlements(settlementDict[keyValue], settlement)
        return settlementDict.values()
    else:
        return settlementList

def AddUpAmountsForSameSourceSettlements(sumSettlement, settlement):
    if not sumSettlement:
        return None
    sumSettlement.Amount(sumSettlement.Amount() + settlement.Amount())

    return sumSettlement
