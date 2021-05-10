""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSetters.py"
from FSettlementEnums import SettlementStatus


#-------------------------------------------------------------------------
def SetPostSettleActionIfNotStatusVoid(settlement):
    if settlement:
        if settlement.Status() != SettlementStatus.VOID:
            settlement.PostSettleAction(True)

#-------------------------------------------------------------------------
def SetPendingAmendmentStatusExplanation(settlement, isAmendmentProcess):
    if isAmendmentProcess:
        settlement.IsAmendmentProcess(True)