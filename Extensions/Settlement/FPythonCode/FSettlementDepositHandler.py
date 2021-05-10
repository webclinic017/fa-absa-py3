""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementDepositHandler.py"
import acm
import FOperationsUtils as Utils
import FOperationsRuleEngine as RuleEngine
from FOperationsEnums import LegType, InsType, OpenEndStatus, CashFlowType
from FSettlementEnums import SettlementType

calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

class DepositHandler(object):

    @staticmethod
    def __CreatePreventionRuleEngine():

        openEndQuery = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
        openEndQuery.AddAttrNode('InsType', 'EQUAL',  Utils.GetEnum('InsType', InsType.DEPOSIT))
        openEndQuery.AddAttrNode('OpenEnd', 'EQUAL', Utils.GetEnum('OpenEndStatus', OpenEndStatus.OPEN_END))

        redemptionQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        redemptionQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.REDEMPTION))
        redemptionQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.REDEMPTION_AMOUNT))

        reinvetsOrCallFixRatAdjQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.INTEREST_REINVEST))
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FIXED_RATE_ADJUSTABLE))
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.FIXED_RATE_ADJUSTABLE))
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FLOAT_RATE))
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FIXED_RATE))
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.FLOAT_RATE))
        reinvetsOrCallFixRatAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.FIXED_RATE))

        preventCond1 = RuleEngine.And([RuleEngine.QueryCondition(openEndQuery), \
                                      RuleEngine.QueryCondition(redemptionQuery)])
        preventRule1 = RuleEngine.Rule(preventCond1, RuleEngine.ActionValue(True))

        floatOrFixedQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        floatOrFixedQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FLOAT_RATE))
        floatOrFixedQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FIXED_RATE))

        reinvestLegQuery = acm.CreateFASQLQuery(acm.FLeg, 'AND')
        reinvestLegQuery.AddAttrNode('Reinvest', 'EQUAL', True)

        preventCond2 = RuleEngine.And([RuleEngine.QueryCondition(openEndQuery), \
                                      RuleEngine.QueryCondition(reinvestLegQuery), \
                                      RuleEngine.QueryCondition(floatOrFixedQuery)])
        preventRule2 = RuleEngine.Rule(preventCond2, RuleEngine.ActionValue(True))

        interestReinvestQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        interestReinvestQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.INTEREST_REINVEST))

        callFixedRateAdjQuery = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        callFixedRateAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FIXED_RATE_ADJUSTABLE))
        callFixedRateAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.FIXED_RATE_ADJUSTABLE))
        callFixedRateAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FLOAT_RATE))
        callFixedRateAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.CALL_FIXED_RATE))
        callFixedRateAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.FLOAT_RATE))
        callFixedRateAdjQuery.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', SettlementType.FIXED_RATE))

        preventCond3 = RuleEngine.And([RuleEngine.QueryCondition(openEndQuery), \
                                       RuleEngine.QueryCondition(reinvestLegQuery), \
                                       RuleEngine.QueryCondition(reinvetsOrCallFixRatAdjQuery)])
        preventRule3 = RuleEngine.Rule(preventCond3, RuleEngine.ActionValue(True))

        terminatedQuery = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
        terminatedQuery.AddAttrNode('InsType', 'EQUAL',  Utils.GetEnum('InsType', InsType.DEPOSIT))
        terminatedQuery.AddAttrNode('OpenEnd', 'EQUAL', Utils.GetEnum('OpenEndStatus', OpenEndStatus.TERMINATED))

        terminatedCond = RuleEngine.And([RuleEngine.QueryCondition(terminatedQuery), \
                                        RuleEngine.QueryCondition(interestReinvestQuery)])
        terminatedRule = RuleEngine.Rule(terminatedCond, \
                                         RuleEngine.ActionFunction(DepositHandler.IsPreventInterestReinvestmentCreation))

        terminatedAndCallFixedRateAdjCond = RuleEngine.And([RuleEngine.QueryCondition(terminatedQuery), \
                                                           RuleEngine.QueryCondition(callFixedRateAdjQuery)])

        callFixedRateAdjRule = RuleEngine.Rule(terminatedAndCallFixedRateAdjCond, \
                                               RuleEngine.ActionFunction(DepositHandler.IsPreventCallRateCreation))


        return RuleEngine.RuleExecutor([preventRule1, preventRule2, preventRule3, terminatedRule, callFixedRateAdjRule], \
                                       RuleEngine.ActionValue(False))



    def __init__(self):

        self.__preventEngine = self.__CreatePreventionRuleEngine()

    @staticmethod
    def IsPreventInterestReinvestmentCreation(settlement):
        prevent = False
        trade = settlement.Trade()
        interestReinvestCashFlow = None
        if (settlement.CashFlow()):
            interestReinvestCashFlow = settlement.SourceObject()
        if not interestReinvestCashFlow:
            raise LookupError('Interest Reinvestment cashflow missing!')

        callRatesSet = None
        if interestReinvestCashFlow.Leg().LegType() == LegType.CALL_FIXED_ADJUSTABLE:
            callRatesSet = DepositHandler.__GetCallFixedRateAdjustableCashFlow(interestReinvestCashFlow)
        elif interestReinvestCashFlow.Leg().LegType() == LegType.CALL_FIXED:
            callRatesSet = DepositHandler.__GetCallFixedRateCashFlow(interestReinvestCashFlow)
        elif interestReinvestCashFlow.Leg().LegType() == LegType.CALL_FLOAT:
            callRatesSet = DepositHandler.__GetCallFloatRateCashFlow(interestReinvestCashFlow)
        else:
            return False

        intReiResultSet = DepositHandler.__GetInterestReinvestCashFlows(interestReinvestCashFlow)
        intReiAmount = 0.0
        callRateAmount = 0.0

        for cashFlow in intReiResultSet:
            projCF = cashFlow.Calculation().Projected(calcSpace, trade).Value().Number()
            intReiAmount = intReiAmount + projCF

        for cashFlow in callRatesSet:
            projCF = cashFlow.Calculation().Projected(calcSpace, trade).Value().Number()
            callRateAmount = callRateAmount + projCF

        if (abs(intReiAmount + callRateAmount) < 1e-3):
            prevent = True

        return prevent


    @staticmethod
    def IsPreventCallRateCreation(settlement):
        prevent = False
        callRate = None
        callRate = None
        trade = settlement.Trade()
        if (settlement.CashFlow()):
            callRate = settlement.SourceObject()
        if not callRate:
            raise LookupError('Settlement is missing cashflow!')
        intReiResultSet = DepositHandler.__GetInterestReinvestCashFlows(callRate)
        intReiAmount = 0.0

        for cashFlow in intReiResultSet:
            projCF = cashFlow.Calculation().Projected(calcSpace, trade).Value().Number()
            intReiAmount = intReiAmount + projCF
        callRateAmount = callRate.Calculation().Projected(calcSpace, trade).Value().Number()
        if (abs(intReiAmount + callRateAmount) < 1e-3):
            prevent = True
        return prevent

    @staticmethod
    def __GetInterestReinvestCashFlows(interestReinvestCashFlow):

        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', interestReinvestCashFlow.Leg().Oid())
        cashFlowQuery.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', CashFlowType.INTEREST_REINVESTMENT))
        cashFlowQuery.AddAttrNode('PayDate', 'EQUAL', interestReinvestCashFlow.PayDate())
        return cashFlowQuery.Select()

    @staticmethod
    def __GetCallFixedRateAdjustableCashFlow(interestReinvestCashFlow):

        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', interestReinvestCashFlow.Leg().Oid())
        cashFlowQuery.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', CashFlowType.CALL_FIXED_RATE_ADJUSTABLE))
        cashFlowQuery.AddAttrNode('PayDate', 'EQUAL', interestReinvestCashFlow.PayDate())
        return cashFlowQuery.Select()

    @staticmethod
    def __GetCallFixedRateCashFlow(interestReinvestCashFlow):

        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', interestReinvestCashFlow.Leg().Oid())
        cashFlowQuery.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', CashFlowType.CALL_FIXED_RATE))
        cashFlowQuery.AddAttrNode('PayDate', 'EQUAL', interestReinvestCashFlow.PayDate())
        return cashFlowQuery.Select()

    @staticmethod
    def __GetCallFloatRateCashFlow(interestReinvestCashFlow):

        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', interestReinvestCashFlow.Leg().Oid())
        cashFlowQuery.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', CashFlowType.CALL_FLOAT_RATE))
        cashFlowQuery.AddAttrNode('PayDate', 'EQUAL', interestReinvestCashFlow.PayDate())
        return cashFlowQuery.Select()

    def PreventSettlementCreation(self, settlement):
        trade = settlement.Trade()
        prevent = False
        if trade:
            instrument = trade.Instrument()
            legs = instrument.Legs()
            leg = None
            if legs.Size() > 0:
                leg = legs.First()
            prevent = self.__preventEngine.Execute([instrument, leg, settlement], \
                                            RuleEngine.ValueType.ANY_IN_LIST, settlement)
        else:
            raise RuntimeError('Trade not found from MoneyFlow!')

        return prevent
