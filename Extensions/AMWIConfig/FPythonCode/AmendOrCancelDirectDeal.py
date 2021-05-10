"""

Amend/CancelDirectDeal

"""
from AMWICommon import AMWI_STATUS_TERMINATED, AMWI_STATUS_BOBO_CONFIRMED
from AMWICustomUtil import set_status, log_in_method, set_contract_status, set_status_by_context
from AMWITradeUtil import set_trade_dates


def _is_amendment(context):
    params = context.Parameters()
    if params.HasKey('AmendmentDate'):
        return True

    return False


def _is_partial_amendment(context):
    params = context.Parameters()
    amendment_type = params["AmendmentType"] if "AmendmentType" in params else None

    if amendment_type == "PartialTermination":
        return True

    return False


def _regenerate_legs(context):
    """
        Regenerate cashflows on this replacement trade, with amended leg start date
        in FSWMLImportExtension matching amendmentDate, structured cashflows will
        be deleted.
    """
    for leg in context.Subject().Instrument().Legs():
        leg.GenerateCashFlows(0)


def condition_entry_state_initiated(context):
    log_in_method(context)
    return True


def condition_exit_state_agreed(context):
    log_in_method(context)
    return True


def on_entry_state_initiated(context):
    log_in_method(context)


def on_entry_state_pickedup(context):
    set_status_by_context(context)


def on_entry_state_affirmed(context):
    set_status_by_context(context)


def on_entry_state_agreed(context):
    set_status_by_context(context)


def on_entry_state_cptyaffirmed(context):
    set_status_by_context(context)


def on_entry_state_released(context):
    log_in_method(context)

    # Check the contract status, if it is not set to 'Cancelled'
    # then we assume it is an amendment.
    if context.Subject().AdditionalInfo().CCPmwire_contract_s() == 'Cancelled':
        set_status(context, AMWI_STATUS_TERMINATED)
        set_contract_status(context, AMWI_STATUS_TERMINATED)
    else:
        amendment_date = context.Parameters()["AmendmentDate"]
        set_status_by_context(context)
        if _is_partial_amendment(context):
            set_contract_status(context, AMWI_STATUS_TERMINATED)
            set_trade_dates(context.Subject(), amendment_date)
        else:
            context.Subject().ValueDay(amendment_date)
            context.Subject().AcquireDay(amendment_date)

            _regenerate_legs(context)


def on_entry_state_withdrawn(context):
    set_status_by_context(context)
    set_contract_status(context, AMWI_STATUS_BOBO_CONFIRMED)
