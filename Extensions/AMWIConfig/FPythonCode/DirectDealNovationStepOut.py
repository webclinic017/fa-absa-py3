"""

DirectDealNovationStepOut

"""
from AMWICommon import AMWI_STATUS_TERMINATED
from AMWICustomUtil import set_status, log_in_method, set_contract_status, set_status_by_context


def condition_entry_state_initiated(context):
    log_in_method(context)
    return True


def condition_exit_state_agreed(context):
    log_in_method(context)
    return True


def on_entry_state_novation_affirmed(context):
    set_status_by_context(context)


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
    # A closing trade means this is a full novation
    if context.Subject().Type() == "Closing":
        set_status(context, AMWI_STATUS_TERMINATED)
    else:
        set_status_by_context(context)

    set_contract_status(context, AMWI_STATUS_TERMINATED)


def on_entry_state_withdrawn(context):
    set_status_by_context(context)
