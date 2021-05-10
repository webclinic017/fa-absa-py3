"""

LCH.Clearnet_T2_Client

"""
from AMWICommon import AMWI_NEW_STATUS_REJECTED_CLEARING, AMWI_STATUS_FO_CONFIRMED
from AMWICustomUtil import log_in_method, set_status, set_status_by_context, is_mwire_new_status
from AMWITradeUtil import get_default_party


def condition_entry_state_initiated(context):
    log_in_method(context)
    return True


def condition_exit_state_agreed(context):
    log_in_method(context)
    return True


def on_entry_state_ready(context):
    set_status_by_context(context)


def on_entry_state_pickedup(context):
    set_status_by_context(context)


def on_entry_state_affirmed(context):
    set_status_by_context(context)


def on_entry_state_cptyaffirmed(context):
    set_status_by_context(context)


def on_entry_state_agreed(context):
    set_status_by_context(context)


def on_entry_state_released(context):
    set_status_by_context(context)


def on_entry_state_withdrawn(context):
    if is_mwire_new_status(context.Subject(), AMWI_NEW_STATUS_REJECTED_CLEARING):
        if not context.Subject().Counterparty():
            context.Subject().Counterparty(get_default_party())
        set_status(context, AMWI_STATUS_FO_CONFIRMED)
    else:
        set_status_by_context(context)


def on_entry_state_chsubmitted(context):
    set_status_by_context(context)


def on_entry_state_registered(context):
    set_status_by_context(context)


def on_entry_state_cleared(context):
    set_status_by_context(context)


def on_entry_state_beta_cleared(context):
    set_status_by_context(context)


def on_entry_state_rejected(context):
    set_status_by_context(context)
