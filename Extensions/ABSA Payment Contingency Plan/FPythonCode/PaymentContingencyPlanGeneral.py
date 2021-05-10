"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PaymentContingencyPlanGeneral

DESCRIPTION
    This module contains general functionality related to the payment contingency plan.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-03-23      FAOPS-681       Cuen Edwards            Linda Breytenbach       Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
from FOperationsDocumentEnums import OperationsDocumentStatus
from FSettlementEnums import SettlementStatus


def is_enabled():
    """
    Determine whether or not the payment contingency plan is enabled.
    """
    return _boolean_from_string(str(_get_contingency_plan_parameter('Enabled')))


def is_supported_settlement(settlement):
    """
    Determine whether or not a settlement is supported by the payment
    contingency plan.
    """
    if settlement.AccountType() != 'Cash':
        # Using this check instead of settlement.IsSecurity() as
        # IsSecurity() is not reliable in all instances (it only
        # works for non-net settlements or for net settlements
        # that are netted for the same settlement type).
        return False
    if settlement.CashCurrency().Name() != 'ZAR':
        return False
    return settlement.Amount() < 0


def get_document_status_explanation():
    """
    Get the operations document status explanation that indicates that
    a settlement is being processed via the payment contingency plan.
    """
    return 'Payment Contingency Plan'


def get_settlements_to_send():
    """
    Get any settlements that need to be sent in the next payment
    contingency plan file.
    """
    settlements = list()
    for settlement in _get_released_settlements_for_today():
        if not is_supported_settlement(settlement):
            continue
        if not _has_document_sending_via_payment_contingency_plan(settlement):
            continue
        settlements.append(settlement)
    return settlements


def _get_released_settlements_for_today():
    """
    Get any settlements that are in released status for payment date
    today.
    """
    asql_query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    asql_query.AddAttrNode('Status', 'EQUAL', SettlementStatus.RELEASED)
    asql_query.AddAttrNode('ValueDay', 'EQUAL', acm.Time.DateToday())
    return asql_query.Select()


def _has_document_sending_via_payment_contingency_plan(settlement):
    """
    Determine whether or not a settlement has a document set for
    sending via the payment contingency plan.
    """
    if settlement.Documents().Size() != 1:
        return False
    operations_document = settlement.Documents()[0]
    if operations_document.Status() != OperationsDocumentStatus.SENDING:
        return False
    if operations_document.StatusExplanation() != get_document_status_explanation():
        return False
    return True


def _boolean_from_string(string_value):
    """
    Safely parse a string to a boolean value.
    """
    string_value_normalised = string_value.lower().strip()
    if string_value_normalised in ['true', '1']:
        return True
    if string_value_normalised in ['false', '0']:
        return False
    raise ValueError("Invalid boolean value '{string_value}' specified.".format(
        string_value=string_value
    ))


def _get_contingency_plan_parameter(parameter_name):
    """
    Get a payment contingency plan FParameter value.
    """
    return _get_fparameter('ABSAPaymentContingencyPlanParameters', parameter_name)


def _get_fparameter(parameters_name, parameter_name):
    """
    Get an FParameter value.
    """
    parameters_extension = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject,
        parameters_name)
    if parameters_extension is None:
        exception_message = "Unable to find FParameters extension '{parameters_name}'"
        raise ValueError(exception_message.format(
            parameters_name=parameters_name
        ))
    parameters = parameters_extension.Value()
    if not parameters.HasKey(acm.FSymbol(parameter_name)):
        exception_message = "Unable to find '{parameters_name}' FParameters parameter "
        exception_message += "'{parameter_name}'"
        raise ValueError(exception_message.format(
            parameters_name=parameters_name,
            parameter_name=parameter_name
        ))
    return parameters.At(parameter_name)
