""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementExCouponDateHandler.py"
"""
Module implementing the ExCouponDateHandler class.
"""


import acm
import FOperationsUtils as Utils
import FOperationsRuleEngine as Engine
from FSettlementEnums import SettlementType
from FOperationsEnums import InsType, LegType


class ExCouponDateHandler(object):
    """
    Class for determining whether a cashflow settlement record shall be created or not with respect
    of the ex coupon date of the cashflow.
    """

    def __init__(self, settlement, cashFlow):
        """
        Constructor for ExCouponDateHandler.
        An instance of the ExCouponDateHandler class has four attribute variables:
        1) trade, an FTrade object
        2) cashFlow, an FCashFlow object
        3) ruleExecutor2, a RuleExecutor object for evaluation of the query returned from
           GetTradeAcquireDayQuery.
        """

        self.trade = settlement.Trade()
        self.cashFlow = cashFlow
        self.settlement = settlement

        condition0 = Engine.QueryCondition(self.GetCashflowDividendQuery())
        rule0 = Engine.Rule(condition0, Engine.ActionFunction(ExCouponDateHandler.CashflowDividendAction))
        self.ruleExecutor0 = Engine.RuleExecutor([rule0], Engine.ActionValue(True))

        condition2 = Engine.QueryCondition(self.GetTradeAcquireDayQuery())
        rule2 = Engine.Rule(condition2, Engine.ActionValue(False))
        self.ruleExecutor2 = Engine.RuleExecutor([rule2], Engine.ActionValue(True))


    def GetCashflowDividendQuery(self):

        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CASHFLOW_DIVIDEND))
        query.AddAttrNode('SecurityInstrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.TOTAL_RETURN_SWAP))
        return query

    def IsExCouponDateApproved(self):
        """
        This function shall be called after creating an ExCouponDateHandler object.
        IsExCouponDateApproved returns True or False depending on whether the conditions are met
        in the RuleExecutor objects ruleExecutor1, ruleExecutor2.
        """
        isExCouponDateApproved = True
        if self.cashFlow.CashFlowType() == SettlementType.DIVIDEND:
            isExCouponDateApproved = self.ruleExecutor0.Execute(self.settlement, Engine.ValueType.SINGLE_VALUE, self.settlement, self.cashFlow)
            return isExCouponDateApproved

        isExCouponDateApproved = self.ruleExecutor2.Execute(self.trade, Engine.ValueType.SINGLE_VALUE)
        if not isExCouponDateApproved:
            if self.cashFlow.CashFlowType() == SettlementType.FIXED_AMOUNT and \
               self.cashFlow.Leg().StartDate() == self.trade.AcquireDay():
                isExCouponDateApproved = True
            else:
                self.AcquireDayPrintout()

        return isExCouponDateApproved

    def GetTradeAcquireDayQuery(self):
        """
        Retrieve query for self.ruleExecutor2
        """

        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        query.AddAttrNode('AcquireDay', 'GREATER_EQUAL', self.cashFlow.ExCouponDate())
        return query

    def AcquireDayPrintout(self):
        """
        ActionFunction for self.ruleExecutor2 if query from GetTradeAcquireDayQuery is not satisfied.
        The ActionFucntion simply prints out a message.
        """
        cfType = self.settlement.Type()
        tradeOid = self.trade.Oid()
        cashFlowOid = self.cashFlow.Oid()
        exCouponDate = self.cashFlow.ExCouponDate()
        acquireDay = self.trade.AcquireDay()
        Utils.LogVerbose(\
        "The ex coupon date (%s) of cashflow %d\n" % (exCouponDate, cashFlowOid) + \
        "is earlier or at the same date as the\n" + \
        "acquire day (%s) of trade %d.\n" % (acquireDay, tradeOid) + \
        "A %s settlement record for cashflow %d will\n" % (cfType, cashFlowOid) + \
        "therefore not be created.\n")

    @staticmethod
    def CashflowDividendAction(settlement, cashFlow):
        import FSettlementParameters as Params
        isExDivDayApproved = False
        trade = settlement.Trade()
        instrument = cashFlow.Leg().Instrument()
        if Params.considerResetsForTRSDividends:
            earliestResetDay, latestResetDay = \
            ExCouponDateHandler.GetEarliestAndLatestResetDay(ExCouponDateHandler.GetResets(instrument))
            if earliestResetDay and latestResetDay:
                isExDivDayApproved = (earliestResetDay < cashFlow.StartDate() <= latestResetDay)
                if not isExDivDayApproved:
                    ExCouponDateHandler.ExDivDayResetLog(earliestResetDay, latestResetDay, cashFlow)
            else:
                ExCouponDateHandler.ExDivDayNoResetLog(cashFlow, instrument)
        else:
            isExDivDayApproved = trade.ValueDay() <= cashFlow.StartDate()
            if not isExDivDayApproved:
                ExCouponDateHandler.ExDivDayValueDayLog(trade, cashFlow)
        return isExDivDayApproved

    @staticmethod
    def GetResets(instrument):
        for leg in instrument.Legs():
            if leg.LegType() == LegType.TOTAL_RETURN and leg.IndexRef():
                return leg.Resets()
        return acm.FArray()

    @staticmethod
    def GetEarliestAndLatestResetDay(resetSet):
        earliestDay = None
        latestDay = None
        if resetSet.Size():
            for reset in resetSet:
                if not earliestDay and not latestDay:
                    earliestDay = reset.Day()
                    latestDay = reset.Day()
                    continue
                if reset.Day() < earliestDay:
                    earliestDay = reset.Day()
                if reset.Day() > latestDay:
                    latestDay = reset.Day()
        return (earliestDay, latestDay)

    @staticmethod
    def ExDivDayNoResetLog(cashFlow, instrument):
        Utils.LogVerbose('A settlement record for cashflow %d will not be created.\n' % cashFlow.Oid() + \
                  'Could not retrieve resets for instrument %s' % instrument.Name())

    @staticmethod
    def ExDivDayResetLog(earliestResetDay, latestResetDay, cashFlow):
        if not earliestResetDay < cashFlow.ExCouponDate():
            Utils.LogVerbose('A settlement record for cashflow %d will not be created.\n' % cashFlow.Oid() + \
                      'Ex coupon day %s is earlier or at the same date as reset day %s' % (cashFlow.ExCouponDate(), earliestResetDay))
        elif not cashFlow.ExCouponDate() <= latestResetDay:
            Utils.LogVerbose('A settlement record for cashflow %d will not be created.\n' % cashFlow.Oid() + \
                      'Ex coupon day %s is later than reset day %s' % (cashFlow.ExCouponDate(), latestResetDay))

    @staticmethod
    def ExDivDayValueDayLog(trade, cashFlow):
        Utils.LogVerbose('A settlement record for cashflow %d will not be created.\n' % cashFlow.Oid() + \
                  'Ex coupon day %s is earlier than trade value day %s' % (cashFlow.ExCouponDate(), trade.ValueDay()))


