"""---------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportsUtils

DESCRIPTION
    This module contains NeoX functions share across the NeoX Activity Report Generation.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no        Developer            Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959        Ncediso Nkambule     Cuen Edwards            Initial implementation.
2020-11-12      FAOPS-981        Ncediso Nkambule     Cuen Edwards            Update Production file Path.
2020-10-21      FAOPS-1016       Ncediso Nkambule     Gasant Thulsie          Updated Hook to check for Acquirer on Sec Loan Trades
                                                                              and a check for the SBL True Counterparty.
2021-02-24      FAOPS-982        Ncediso Nkambule     Gasant Thulsie          Added functions to handle Cashflow driven events.

------------------------------------------------------------------------------------------------------------------------
"""

import acm
import sbl_booking_utils as sbl_utils
from at_type_helpers import is_acm, to_ael
import NeoXActivityReportsConstants as Constants
from logging import getLogger


LOGGER = getLogger(__name__)


def get_add_info_value(f_object, add_info_name):
    if add_info_name == "SL_CFD" and f_object.Instrument():
        f_object = f_object.Instrument()
    for add_info in f_object.AddInfos():
        if add_info.AddInf().Name() == add_info_name:
            return add_info.FieldValue()
    return None


def add_has_value(f_object, add_info_name):
    value = get_add_info_value(f_object, add_info_name)
    if value is None:
        return False
    return True


def get_object_value_by_name(event_message, field):
    if event_message and isinstance(event_message, str) is False:
        f_object = event_message.mbf_find_object(field)
        if f_object:
            object_value = f_object.mbf_get_value()
            return object_value
    return None


def is_valid_sbl_loan_trade(acm_trade):
    if acm_trade.Acquirer() is None or acm_trade.Acquirer() != sbl_utils.ACQUIRER:
        return False
    if acm_trade.Instrument() is None:
        return False
    if acm_trade.Instrument().InsType() != Constants.LOAN_INS_TYPE:
        return False
    if acm_trade.Instrument().OpenEnd() not in Constants.OPEN_END_STATUS:
        return False
    if any(add_has_value(acm_trade, name) is False for name in Constants.SBL_LOAN_ADD_INFOS):
        return False
    add_info = acm_trade.AdditionalInfo()
    if add_info and add_info.SL_G1Counterparty1() is None and add_info.SL_G1Counterparty2() is None:
        return False
    return True


def is_valid_sbl_collateral_trade(acm_trade, party_name_prefix="SL"):
    ael_trade = to_ael(acm_trade)
    if not ael_trade.match_portfolio(sbl_utils.COLLATERAL_PORTFOLIO.Name()):
        return False
    if not acm_trade.TradeCategory() == sbl_utils.COLLATERAL_CATEGORY:
        return False
    if acm_trade.Instrument() is None or acm_trade.Instrument().InsType() not in sbl_utils.COLLATERAL_INSTRUMENTS:
        return False
    if acm_trade.Counterparty() is None or not acm_trade.Counterparty().Name().startswith(party_name_prefix):
        return False
    if acm_trade.Acquirer() is None or acm_trade.Acquirer() != sbl_utils.ACQUIRER:
        return False
    return True


def f_object_is_update_today(f_object):
    if f_object and f_object.UpdateTime() > acm.Time.DateTimeToTime(acm.Time.DateToday()):
        return True
    return False


def is_valid_cash_collateral_trade(acm_trade):

    if not acm_trade:
        return False

    ael_trade = to_ael(acm_trade)
    # if acm_trade.OptionalKey() is None or not acm_trade.OptionalKey():
    #     print("I have no optional key")
    #     return False

    if acm_trade.Instrument() is None:
        print("No Instrument")
        return False

    if acm_trade.Instrument().InsType() not in sbl_utils.CASH_COLLATERAL_INS_TYPES:
        print("Not matching instrument type")
        return False
    settle_category = acm_trade.Instrument().SettleCategoryChlItem()
    if settle_category is None or settle_category and settle_category.Name() != 'Collateral':
        print("Instrument Settle category not Collateral")
        return False

    if not ael_trade.match_portfolio(sbl_utils.CASH_COLLATERAL_PORTFOLIO.Name()):
        print("Not Matching portfolio")
        return False

    if acm_trade.Instrument().OpenEnd() != 'Open End':
        print("Instrument not open ")
        return False

    if acm_trade.Acquirer() and acm_trade.Acquirer().Name() != sbl_utils.CASH_COLLATERAL_ACQUIRER.Name():
        print("Not matching acquirer")
        return False

    return True


def get_fparameter(parameters_name, parameter_name):
    """
    Get an FParameter value.
    """

    parameters_extension = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject, parameters_name)
    if parameters_extension is None:
        exception_message = "Unable to find FParameters extension '{parameters_name}'"
        raise ValueError(exception_message.format(parameters_name=parameters_name))

    parameters = parameters_extension.Value()
    if not parameters.HasKey(acm.FSymbol(parameter_name)):
        exception_message = "Unable to find '{parameters_name}' FParameters parameter "
        exception_message += "'{parameter_name}'"
        raise ValueError(exception_message.format(parameters_name=parameters_name, parameter_name=parameter_name))
    return parameters.At(parameter_name)


def is_float(value):
    try:
        float(value)
        return True
    except Exception as error:
        LOGGER.debug(error)
        return False


def get_touched_cashflows(event_message, cash_flow_type='Fixed Amount'):
    """
    Find any child list MBF objects with the specified name updates .
    """

    matching_cashflows = list()
    updated_cashflows = mbf_find_current_cashflow_objects_by_name(event_message)

    for updated_cashflow in updated_cashflows:
        cf_type = get_object_value_by_name(updated_cashflow, "TYPE")
        if cf_type == cash_flow_type:
            matching_cashflows.append(updated_cashflow)

    return updated_cashflows


def is_deleted_object(mbf_object):
    if mbf_object:
        return mbf_object.mbf_get_name().startswith("-")
    return False


def has_updated_cashflows(event_message, cash_flow_type):
    updated_cashflows = get_touched_cashflows(event_message, cash_flow_type=cash_flow_type)
    if updated_cashflows:
        return True

    return False


def mbf_find_current_cashflow_objects_by_name(mbf_object):
    """
    Find any child list MBF objects with the specified name updates .
    """

    updates_prefixes = ['-', '+', '!']
    cash_flows = list()
    updated_instruments = _mbf_find_objects_by_name(mbf_object, "INSTRUMENT", updates_prefixes)

    for updated_instrument in updated_instruments:
        leg_messages = _mbf_find_objects_by_name(updated_instrument, "LEG")
        for leg_message in leg_messages:
            cash_flows.extend(_mbf_find_objects_by_name(leg_message, "CASHFLOW", updates_prefixes))

    return cash_flows


def _mbf_find_objects_by_name(mbf_object, name, name_prefixes=None):
    """
    Find any child MBF objects with the specified name and optional
    prefixes.

    If no name prefixes are specified then objects matching any
    possible prefix will be returned.
    """

    if name_prefixes is None:
        name_prefixes = ['', '+', '!', '-']

    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)

    mbf_objects = list()
    child_mbf_object = mbf_object.mbf_first_object()
    while child_mbf_object is not None:
        if child_mbf_object.mbf_get_name() in names:
            mbf_objects.append(child_mbf_object)
        child_mbf_object = mbf_object.mbf_next_object()

    return mbf_objects


def get_trade_related_to_cashflow(acm_cash_flow):
    if acm_cash_flow is None:
        return None

    acm_instrument = acm_cash_flow.Instrument()
    acm_trade = get_trade_related_to_instrument(acm_instrument)
    return acm_trade


def get_trade_related_to_instrument(acm_instrument):
    trades = [_trade for _trade in acm_instrument.Trades() if _trade.Status() == 'BO Confirmed']
    acm_trade = trades[0] if trades else None
    return acm_trade
