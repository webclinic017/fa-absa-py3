""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/SecuritiesLending.py"
import FSecLendHooks


def on_entry_state_bo_export(business_process):
    business_process.Subject().AddInfoValue("SBL_PendingOrder", True)
    business_process.Subject().Status(FSecLendHooks.ApprovedTradeStatus())


def on_entry_state_booked(business_process):
    trade = business_process.Subject()
    trade.AddInfoValue("SBL_PendingOrder", False)
    if trade.Status() not in (FSecLendHooks.SettlementTradeStatus(), 'Void'):
        trade.Status(FSecLendHooks.FillTradeStatus())


def on_entry_state_rejected(business_process):
    trade = business_process.Subject()
    trade.Status('Void')
    trade.AddInfoValue("SBL_PendingOrder", False)


def on_entry_state_ready_for_processing(business_process):
    business_process.Subject().AddInfoValue("SBL_PendingOrder", False)


def on_entry_state_awaiting_reply(business_process):
    business_process.Subject().AddInfoValue("SBL_PendingOrder", True)
