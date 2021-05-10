""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementStatusQueries.py"
import acm
import FOperationsUtils as Utils
from FOperationsDateUtils import GetAccountingCurrencyCalendar, AdjustDateToday


from FSettlementEnums import RelationType, SettlementStatus, SettlementType
from FOperationsEnums import TradeType, TradeStatus, InsType, SettleType

CONST_UpdatedVoidRecalledStatusQuery = None
CONST_UpdatedVoidStatusQuery = None
CONST_PreReleasedStatusQuery = None
CONST_PreReleasedStatusMaxDaysBackQuery = None
CONST_ClosedStatusQuery = None
CONST_ClosedRecalledStatusQuery = None
CONST_PostReleasedStatusQuery = None
CONST_CompensationPaymentQuery = None
CONST_DefaultSettlementProcessQuery = None
CONST_RecallStatusesQuery = None
CONST_NetPartQuery = None
CONST_NetParentsQuery = None
CONST_DividendQuery = None
CONST_CouponRedemptionQuery = None
CONST_CouponQuery = None
CONST_RedemptionQuery = None
CONST_ApplicableForNettingQuery = None
CONST_IsCancelledSettlementQuery = None
CONST_IsClosingPayoutTradeQuery = None
CONST_IsClosingTradeQuery = None
CONST_IsNDFTradeQuery = None
CONST_IsAdHocNetQuery = None
CONST_CancelledSecuritiesQuery = None
CONST_IsPostReleasedSettlementOrPartOfNetHierarchy = None
CONST_IsVoidCancelCorrectChild = None
CONST_IsCancelledSettlement = None
CONST_PartialSettledQuery = None
CONST_IsSecuritySettlementWithStatusReplaced = None
CONST_IsSettledSecuritySettlementQuery = None
CONST_PairOffHierarchyChildren = None
CONST_PairOffPaymentsQuery = None
CONST_PairOffChildrenQuery = None
CONST_ValueDayAdjustedQuery = None

def GetUpdatedVoidRecalledStatusQuery():
    global CONST_UpdatedVoidRecalledStatusQuery
    if CONST_UpdatedVoidRecalledStatusQuery != None:
        return CONST_UpdatedVoidRecalledStatusQuery

    CONST_UpdatedVoidRecalledStatusQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_UpdatedVoidRecalledStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.UPDATED))
    CONST_UpdatedVoidRecalledStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.VOID))
    CONST_UpdatedVoidRecalledStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.RECALLED))
    
    or2 = CONST_UpdatedVoidRecalledStatusQuery.AddOpNode('AND')
    or2.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))
    or2.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)

    and1 = or2.AddOpNode('OR')
    and1.AddAttrNode('NumberOfChildren', 'EQUAL', 0)
    and1.AddAttrNode('Children.RelationType', 'NOT_EQUAL', RelationType.CANCEL_CORRECT)

    return CONST_UpdatedVoidRecalledStatusQuery

def GetUpdatedVoidStatusQuery():

    global CONST_UpdatedVoidStatusQuery
    if CONST_UpdatedVoidStatusQuery != None:
        return CONST_UpdatedVoidStatusQuery

    CONST_UpdatedVoidStatusQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    or1 = CONST_UpdatedVoidStatusQuery.AddOpNode('OR')
    or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.UPDATED))
    or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.VOID))

    or2 = CONST_UpdatedVoidStatusQuery.AddOpNode('AND')
    or2.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))
    or2.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)

    return CONST_UpdatedVoidStatusQuery

def GetPreReleasedStatusQuery():

    global CONST_PreReleasedStatusQuery
    if CONST_PreReleasedStatusQuery != None:
        return CONST_PreReleasedStatusQuery

    CONST_PreReleasedStatusQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_PreReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))
    CONST_PreReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.EXCEPTION))
    CONST_PreReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.MANUAL_MATCH))
    CONST_PreReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))
    CONST_PreReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AWAITING_CANCELLATION))
    return CONST_PreReleasedStatusQuery

def GetPreReleasedStatusMaxDaysBackQuery():
    import FSettlementParameters as SettlementParameters
    global CONST_PreReleasedStatusMaxDaysBackQuery
    if CONST_PreReleasedStatusMaxDaysBackQuery != None:
        return CONST_PreReleasedStatusMaxDaysBackQuery

    calendar = GetAccountingCurrencyCalendar()
    startDate = AdjustDateToday(calendar, -SettlementParameters.maximumDaysBack)

    CONST_PreReleasedStatusMaxDaysBackQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_PreReleasedStatusMaxDaysBackQuery.AddAttrNode('ValueDay', 'GREATER_EQUAL', startDate)
    orQuery = CONST_PreReleasedStatusMaxDaysBackQuery.AddOpNode('OR')
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.EXCEPTION))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.MANUAL_MATCH))
    return CONST_PreReleasedStatusMaxDaysBackQuery

def GetClosedStatusQuery():
    global CONST_ClosedStatusQuery
    if CONST_ClosedStatusQuery != None:
        return CONST_ClosedStatusQuery
    CONST_ClosedStatusQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_ClosedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.CLOSED))
    return CONST_ClosedStatusQuery

def GetClosedRecalledStatusQuery():
    global CONST_ClosedRecalledStatusQuery
    if CONST_ClosedRecalledStatusQuery != None:
        return CONST_ClosedRecalledStatusQuery

    CONST_ClosedRecalledStatusQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_ClosedRecalledStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.RECALLED))
    CONST_ClosedRecalledStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.CLOSED))
    return CONST_ClosedRecalledStatusQuery

def GetPartialSettled():
    global CONST_PartialSettledQuery
    if CONST_PartialSettledQuery != None:
        return CONST_PartialSettledQuery
    CONST_PartialSettledQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_PartialSettledQuery.AddAttrNode('PartialParent.Oid', 'NOT_EQUAL', 0)
    andQuery = CONST_PartialSettledQuery.AddOpNode('AND')
    andQuery.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
    andQuery.AddAttrNode('Parent.PartialParent.Oid', 'NOT_EQUAL', 0)
    return CONST_PartialSettledQuery

def GetCancelledSecuritiesQuery():
    global CONST_CancelledSecuritiesQuery
    if CONST_CancelledSecuritiesQuery != None:
        return CONST_CancelledSecuritiesQuery
    CONST_CancelledSecuritiesQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_CancelledSecuritiesQuery.AddAttrNode('Parent.IsCancelledByUs', 'EQUAL', True)
    andNode = CONST_CancelledSecuritiesQuery.AddOpNode('AND')
    andNode.AddAttrNode('IsSecurity', 'EQUAL', True)
    andNode.AddAttrNode('IsCancelledByUs', 'EQUAL', True)
    return CONST_CancelledSecuritiesQuery

def GetPairOffHierarchyChildren():
    global CONST_PairOffHierarchyChildren
    if CONST_PairOffHierarchyChildren != None:
        return CONST_PairOffHierarchyChildren
    CONST_PairOffHierarchyChildren = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_PairOffHierarchyChildren.AddAttrNode('GetTopSettlementInHierarchy.NumberOfPairOffChildren', 'NOT_EQUAL', 0)
    return CONST_PairOffHierarchyChildren

def GetPairOffPaymentsQuery():
    global CONST_PairOffPaymentsQuery
    if CONST_PairOffPaymentsQuery != None:
        return CONST_PairOffPaymentsQuery
    CONST_PairOffPaymentsQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_PairOffPaymentsQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.PAIR_OFF_PAYMENT))
    return CONST_PairOffPaymentsQuery

def GetPairOffChildrenQuery():
    global CONST_PairOffChildrenQuery
    if CONST_PairOffChildrenQuery != None:
        return CONST_PairOffChildrenQuery
    CONST_PairOffChildrenQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_PairOffChildrenQuery.AddAttrNode('PairOffParent.Oid', 'NOT_EQUAL', 0)
    return CONST_PairOffChildrenQuery

def GetPostReleasedStatusQuery():
    global CONST_PostReleasedStatusQuery
    if CONST_PostReleasedStatusQuery != None:
        return CONST_PostReleasedStatusQuery
    CONST_PostReleasedStatusQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.RELEASED))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.ACKNOWLEDGED))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.NOT_ACKNOWLEDGED))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_CLOSURE))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.NON_RECEIPT))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.INCORRECT_RECEIPT))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.NON_PAYMENT))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.INCORRECT_PAYMENT))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.UNEXPECTED_CREDIT))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.UNEXPECTED_DEBIT))
    CONST_PostReleasedStatusQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.HOLD))
    #Hold not actually postreleased status but treated the same way. Maybe change in future
    return CONST_PostReleasedStatusQuery

def GetCompensationPaymentQuery():
    global CONST_CompensationPaymentQuery
    if CONST_CompensationPaymentQuery != None:
        return CONST_CompensationPaymentQuery
    CONST_CompensationPaymentQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_CompensationPaymentQuery.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.COMPENSATION_PAYMENT))
    return CONST_CompensationPaymentQuery

def GetNetPartQuery():
    global CONST_NetPartQuery
    if CONST_NetPartQuery != None:
        return CONST_NetPartQuery
    CONST_NetPartQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NET))
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.COUPON_NET))
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.DIVIDEND_NET))
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.REDEMPTION_NET))
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CLOSE_TRADE_NET))
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.AD_HOC_NET))
    CONST_NetPartQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SECURITIES_DVP_NET))
    return CONST_NetPartQuery

def GetNetParentsQuery():
    global CONST_NetParentsQuery
    if CONST_NetParentsQuery != None:
        return CONST_NetParentsQuery

    CONST_NetParentsQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    or2 = CONST_NetParentsQuery.AddOpNode('OR')
    or2.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NET))
    or2.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CLOSE_TRADE_NET))
    or2.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.COUPON_NET))
    or2.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.REDEMPTION_NET))
    or2.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.DIVIDEND_NET))
    or2.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SECURITIES_DVP_NET))
    or1 = CONST_NetParentsQuery.AddOpNode('OR')
    or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))
    or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.EXCEPTION))
    or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.MANUAL_MATCH))
    or1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.NOT_ACKNOWLEDGED))
    return CONST_NetParentsQuery

def GetDefaultSettlementProcessQuery():

    global CONST_DefaultSettlementProcessQuery
    if CONST_DefaultSettlementProcessQuery != None:
        return CONST_DefaultSettlementProcessQuery

    CONST_DefaultSettlementProcessQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    CONST_DefaultSettlementProcessQuery.AddAttrNode('Aggregate', 'EQUAL', 0)
    CONST_DefaultSettlementProcessQuery.AddAttrNode('Type', 'NOT_EQUAL', Utils.GetEnum('TradeType', TradeType.CASH_POSTING))

    orQuery = CONST_DefaultSettlementProcessQuery.AddOpNode('OR')
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.FO_CONFIRMED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.BO_CONFIRMED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.BO_BO_CONFIRMED))
    return CONST_DefaultSettlementProcessQuery

def GetRecallStatusesQuery():
    global CONST_RecallStatusesQuery
    if CONST_RecallStatusesQuery != None:
        return CONST_RecallStatusesQuery
    CONST_RecallStatusesQuery = acm.CreateFASQLQuery(acm.FTrade, 'OR')
    CONST_RecallStatusesQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.VOID))
    CONST_RecallStatusesQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.CONFIRMED_VOID))
    CONST_RecallStatusesQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.TERMINATED))
    CONST_RecallStatusesQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.SIMULATED))
    return CONST_RecallStatusesQuery

def GetDividendQuery():
    global CONST_DividendQuery
    if CONST_DividendQuery != None:
        return CONST_DividendQuery

    CONST_DividendQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')

    and1 = CONST_DividendQuery.AddOpNode('AND')
    and1.AddAttrNode('Trade.Oid', 'GREATER', 0)
    and1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.DIVIDEND))
    and1.AddAttrNode('SecurityInstrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.STOCK))
    and1.AddAttrNode('Trade.Instrument.InsType', 'NOT_EQUAL', Utils.GetEnum('InsType', InsType.TOTAL_RETURN_SWAP))
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))

    and4 = CONST_DividendQuery.AddOpNode('AND')

    orNetParentType = and4.AddOpNode('OR')
    andNetPartStatus = and4.AddOpNode('AND')

    orNetParentType.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.DIVIDEND_NET))
    andNetPartStatus.AddAttrNode('Status', 'NOT_EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))

    return CONST_DividendQuery

def GetCouponRedemptionQuery():

    global CONST_CouponRedemptionQuery
    if CONST_CouponRedemptionQuery != None:
        return CONST_CouponRedemptionQuery
    CONST_CouponRedemptionQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')

    and1 = CONST_CouponRedemptionQuery.AddOpNode('AND')
    and1.AddAttrNode('Trade.Oid', 'GREATER', 0)
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))
    or3 = and1.AddOpNode('OR')
    or3.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.COUPON))
    or3.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.REDEMPTION))

    andNodeNetpart = CONST_CouponRedemptionQuery.AddOpNode('AND')
    orNetParentType = andNodeNetpart.AddOpNode('OR')
    andNodeNetpart.AddAttrNode('Status', 'NOT_EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))

    orNetParentType.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.COUPON_NET))
    orNetParentType.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.REDEMPTION_NET))


    return CONST_CouponRedemptionQuery

def GetCouponQuery():

    global CONST_CouponQuery
    if CONST_CouponQuery != None:
        return CONST_CouponQuery
    CONST_CouponQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')

    and1 = CONST_CouponQuery.AddOpNode('AND')
    and1.AddAttrNode('Trade.Oid', 'GREATER', 0)
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))
    and1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.COUPON))

    andNodeNetpart = CONST_CouponQuery.AddOpNode('AND')
    andNodeNetpart.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.COUPON_NET))
    andNodeNetpart.AddAttrNode('Status', 'NOT_EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))


    return CONST_CouponQuery

def GetRedemptionQuery():

    global CONST_RedemptionQuery
    if CONST_RedemptionQuery != None:
        return CONST_RedemptionQuery
    CONST_RedemptionQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')

    and1 = CONST_RedemptionQuery.AddOpNode('AND')
    and1.AddAttrNode('Trade.Oid', 'GREATER', 0)
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))
    and1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.REDEMPTION))

    andNodeNetpart = CONST_RedemptionQuery.AddOpNode('AND')
    andNodeNetpart.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.REDEMPTION_NET))
    andNodeNetpart.AddAttrNode('Status', 'NOT_EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))


    return CONST_RedemptionQuery


def GetApplicableForNettingQuery(autoNetTypes = None):
    global CONST_ApplicableForNettingQuery
    if CONST_ApplicableForNettingQuery != None:
        return CONST_ApplicableForNettingQuery

    CONST_ApplicableForNettingQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')

    and1 = CONST_ApplicableForNettingQuery.AddOpNode('AND')
    and1.AddAttrNode('Trade.Oid', 'GREATER', 0)
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.AUTHORISED))

    and1.AddAttrNode('Parent', 'EQUAL', None)
    and1.AddAttrNode('SplitParent', 'EQUAL', None)
    if autoNetTypes:
        if 'Coupon' in autoNetTypes:
            and1.AddAttrNode('Type', 'NOT_EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.COUPON))
        if 'Redemption' in autoNetTypes:
            and1.AddAttrNode('Type', 'NOT_EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.REDEMPTION))
        if 'Dividend' in autoNetTypes:
            and1.AddAttrNode('Type', 'NOT_EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.DIVIDEND))

    and1.AddAttrNode('ManualMatch', 'EQUAL', 0)
    and1.AddAttrNode('RestrictNet', 'EQUAL', 0)

    and2 = CONST_ApplicableForNettingQuery.AddOpNode('AND')
    and2.AddAttrNode('Status', 'NOT_EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.EXCEPTION))
    and2.AddAttrNode('Status', 'NOT_EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.PENDING_AMENDMENT))
    or2 = and2.AddOpNode('OR')
    or2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NET))
    or2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CLOSE_TRADE_NET))
    or2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SECURITIES_DVP_NET))

    return CONST_ApplicableForNettingQuery


def GetIsCancelledSettlementQuery():
    global CONST_IsCancelledSettlementQuery
    if CONST_IsCancelledSettlementQuery != None:
        return CONST_IsCancelledSettlementQuery

    CONST_IsCancelledSettlementQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_IsCancelledSettlementQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.VOID))

    or1 = CONST_IsCancelledSettlementQuery.AddOpNode('OR')
    or1.AddAttrNode('IsCancelledByTheCounterparty', 'EQUAL', True)
    or1.AddAttrNode('IsCancelledByUs', 'EQUAL', True)

    return CONST_IsCancelledSettlementQuery


def GetIsClosingPayoutTradeQuery():
    global CONST_IsClosingPayoutTradeQuery
    if CONST_IsClosingPayoutTradeQuery != None:
        return CONST_IsClosingPayoutTradeQuery

    CONST_IsClosingPayoutTradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    CONST_IsClosingPayoutTradeQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('TradeType', TradeType.CLOSING))
    or1 = CONST_IsClosingPayoutTradeQuery.AddOpNode('OR')
    or1.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.FUTURE_FORWARD))
    or1.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.VARIANCE_SWAP))
    return CONST_IsClosingPayoutTradeQuery

def GetIsClosingTradeQuery():
    global CONST_IsClosingTradeQuery
    if CONST_IsClosingTradeQuery != None:
        return CONST_IsClosingTradeQuery
    CONST_IsClosingTradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    CONST_IsClosingTradeQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('TradeType', TradeType.CLOSING))
    return CONST_IsClosingTradeQuery

def GetIsNDFTradeQuery():
    global CONST_IsNDFTradeQuery
    if CONST_IsNDFTradeQuery != None:
        return CONST_IsNDFTradeQuery
    CONST_IsNDFTradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    CONST_IsNDFTradeQuery.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.FUTURE_FORWARD))
    CONST_IsNDFTradeQuery.AddAttrNode('Instrument.Underlying.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.CURR))
    CONST_IsNDFTradeQuery.AddAttrNode('Instrument.SettlementType', 'EQUAL', Utils.GetEnum('SettlementType', SettleType.CASH))
    return CONST_IsNDFTradeQuery

def IsAdHocNetQuery():
    global CONST_IsAdHocNetQuery
    if CONST_IsAdHocNetQuery != None:
        return CONST_IsAdHocNetQuery
    CONST_IsAdHocNetQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_IsAdHocNetQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.AD_HOC_NET))
    CONST_IsAdHocNetQuery.AddAttrNode('RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NONE))

    return CONST_IsAdHocNetQuery

def IsPostReleasedSettlementOrPartOfNetHierarchy():
    global CONST_IsPostReleasedSettlementOrPartOfNetHierarchy
    if CONST_IsPostReleasedSettlementOrPartOfNetHierarchy != None:
        return CONST_IsPostReleasedSettlementOrPartOfNetHierarchy
    CONST_IsPostReleasedSettlementOrPartOfNetHierarchy = acm.CreateFASQLQuery(acm.FSettlement, 'OR')

    and1 = CONST_IsPostReleasedSettlementOrPartOfNetHierarchy.AddOpNode('AND')
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.ACKNOWLEDGED))
    and1.AddAttrNode('Parent', 'EQUAL', None)
    or1 = and1.AddOpNode('OR')
    or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_NOMINAL))
    or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.AGGREGATE_SECURITY))
    or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.END_SECURITY))
    or1.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_DVP))

    and2 = CONST_IsPostReleasedSettlementOrPartOfNetHierarchy.AddOpNode('AND')
    and2.AddAttrNode('IsPartOfHierarchy', 'EQUAL', True)
    and2.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.ACKNOWLEDGED))
    or2 = and2.AddOpNode('OR')
    or2.AddAttrNode('Parent.Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_NOMINAL))
    or2.AddAttrNode('Parent.Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.AGGREGATE_SECURITY))
    or2.AddAttrNode('Parent.Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.END_SECURITY))
    or2.AddAttrNode('Parent.Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.SECURITY_DVP))
    or3 = and2.AddOpNode('OR')
    or3.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SECURITIES_DVP_NET))
    or3.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NET))

    return CONST_IsPostReleasedSettlementOrPartOfNetHierarchy

def IsVoidCancelCorrectChild():
    #Retrieves child of settlement with relation type "Cancel Correct" or child of settlement
    #of relation type "Securities DvP Net" or "Net", which is in turn the child of a settlement
    #of relation type "Cancel Correct"
    global CONST_IsVoidCancelCorrectChild
    if CONST_IsVoidCancelCorrectChild != None:
        return CONST_IsVoidCancelCorrectChild
    CONST_IsVoidCancelCorrectChild = acm.CreateFASQLQuery(acm.FSettlement, 'AND')

    CONST_IsVoidCancelCorrectChild.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.VOID))

    or1 = CONST_IsVoidCancelCorrectChild.AddOpNode('OR')
    or1.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCEL_CORRECT))

    and1 = or1.AddOpNode('AND')
    and1.AddAttrNode('Parent.Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.CANCEL_CORRECT))

    or2 = and1.AddOpNode('OR')
    or2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.SECURITIES_DVP_NET))
    or2.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.NET))

    return CONST_IsVoidCancelCorrectChild

def IsCancelledSettlement():
    global CONST_IsCancelledSettlement
    if CONST_IsCancelledSettlement != None:
        return CONST_IsCancelledSettlement
    CONST_IsCancelledSettlement = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_IsCancelledSettlement.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.CANCELLED))

    return CONST_IsCancelledSettlement

def IsSecuritySettlementWithStatusReplaced():
    global CONST_IsSecuritySettlementWithStatusReplaced
    if CONST_IsSecuritySettlementWithStatusReplaced != None:
        return CONST_IsSecuritySettlementWithStatusReplaced
    CONST_IsSecuritySettlementWithStatusReplaced = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    and1 = CONST_IsSecuritySettlementWithStatusReplaced.AddOpNode('AND')
    and1.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.REPLACED))
    and1.AddAttrNode('IsSecurity', 'EQUAL', 'True')

    and2 = CONST_IsSecuritySettlementWithStatusReplaced.AddOpNode('AND')
    and2.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
    and2.AddAttrNode('Parent.Status', 'EQUAL', Utils.GetEnum('SettlementStatus', SettlementStatus.REPLACED))
    and2.AddAttrNode('Parent.IsSecurity', 'EQUAL', 'True')
    return CONST_IsSecuritySettlementWithStatusReplaced

def GetSettledSecuritySettlementQuery():
    global CONST_IsSettledSecuritySettlementQuery
    if CONST_IsSettledSecuritySettlementQuery != None:
        return CONST_IsSettledSecuritySettlementQuery
    CONST_IsSettledSecuritySettlementQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
    and1 = CONST_IsSettledSecuritySettlementQuery.AddOpNode('AND')
    and1.AddAttrNode('IsSettled', 'EQUAL', True)
    and1.AddAttrNode('IsSecurity', 'EQUAL', True)
    and2 = CONST_IsSettledSecuritySettlementQuery.AddOpNode('AND')
    and2.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
    and2.AddAttrNode('Parent.IsSettled', 'EQUAL', True)
    and2.AddAttrNode('Parent.IsSecurity', 'EQUAL', True)
    return CONST_IsSettledSecuritySettlementQuery

def GetValueDayAdjustedQuery():
    global CONST_ValueDayAdjustedQuery
    if CONST_ValueDayAdjustedQuery != None:
        return CONST_ValueDayAdjustedQuery
    CONST_ValueDayAdjustedQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    CONST_ValueDayAdjustedQuery.AddAttrNode('Parent.Oid', 'NOT_EQUAL', 0)
    CONST_ValueDayAdjustedQuery.AddAttrNode('Parent.RelationType', 'EQUAL', Utils.GetEnum('SettlementRelationType', RelationType.VALUE_DAY_ADJUSTED))
    return CONST_ValueDayAdjustedQuery
