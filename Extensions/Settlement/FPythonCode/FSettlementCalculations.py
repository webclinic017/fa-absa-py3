""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCalculations.py"
import FSettlementValidations as Validations
from FOperationsEnums import InsType
import acm

#-------------------------------------------------------------------------
# Settlement calculation functions - used to calculate values in 
# settlement flows.
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
def CalculateAmountFactor(settledAmount, totalAmount, trade):
    offsettingAmountFactor = None
    offsettingTransferAmountFactor = None
    if totalAmount != 0:
        if Validations.IsAfterMaturity(trade.Instrument()):
            if trade.Instrument().InsType() != InsType.BUY_SELLBACK:
                offsettingAmountFactor = -1*(settledAmount / totalAmount)
                offsettingTransferAmountFactor = settledAmount / totalAmount
            else:
                offsettingAmountFactor = -1*(settledAmount / totalAmount)
                offsettingTransferAmountFactor = settledAmount / totalAmount - 1
        else:
            offsettingAmountFactor = settledAmount / totalAmount - 1
            offsettingTransferAmountFactor = 1- settledAmount / totalAmount
    return offsettingAmountFactor, offsettingTransferAmountFactor

#-------------------------------------------------------------------------
def CalculateSettledAmountOnDate(trade, date):
    settledAmount = 0.0
    totalAmount = 0.0
    for settlement in trade.Settlements():                          
        topSettlement = settlement.GetTopSettlementInHierarchy()
        if Validations.IsConsideredInSettlementAmountCalculation(settlement, trade.Instrument(), date):
            totalAmount += settlement.Amount()
            if topSettlement.IsSettled() and settlement.SettledDay() <= date:
                settledAmount += settlement.Amount()

    return settledAmount, totalAmount
