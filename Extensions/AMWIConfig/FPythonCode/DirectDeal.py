"""

DirectDeal

Note 1: Standard Markitwire workflow is (Ready/Pickedup)->(Affirmed/CptyAffirmed)->Agreed->Released

Note 2: context is of type FBusinessProcessCallbackContext

"""
from AMWICommon import AMWI_STATUS_FO_CONFIRMED, AMWI_STATUS_BO_CONFIRMED, AMWI_STATUS_VOID
from AMWICustomUtil import set_status, set_status_by_context, log_in_method
from AMWIIdentity import is_allocate_trade

CONTRACT_STATUS_ALLOCATED = "Allocated"
CONTRACT_STATUS_NEW_ALLOCATION = "New-Allocation"


def _contract_status_is(context, status):
    contract_status = context.Subject().AdditionalInfo().CCPmwire_contract_s()
    if contract_status == status:
        return True

    return False


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
    if _contract_status_is(context, CONTRACT_STATUS_ALLOCATED):
        set_status(context, AMWI_STATUS_FO_CONFIRMED, True)
    else:
        set_status_by_context(context)


def on_entry_state_cptyaffirmed(context):
    if is_allocate_trade(context.Subject()):
        set_status(context, AMWI_STATUS_FO_CONFIRMED)
    elif _contract_status_is(context, CONTRACT_STATUS_ALLOCATED):
        set_status(context, AMWI_STATUS_BO_CONFIRMED, True)
    else:
        set_status_by_context(context)


def on_entry_state_agreed(context):
    if is_allocate_trade(context.Subject()):
        set_status(context, AMWI_STATUS_FO_CONFIRMED)
    else:
        set_status_by_context(context)


def on_entry_state_released(context):
    if _contract_status_is(context, CONTRACT_STATUS_ALLOCATED):
        set_status(context, AMWI_STATUS_VOID)
    elif is_allocate_trade(context.Subject()):
        set_status(context, AMWI_STATUS_FO_CONFIRMED)
    else:
        set_status_by_context(context)


def on_entry_state_withdrawn(context):
    set_status_by_context(context)
