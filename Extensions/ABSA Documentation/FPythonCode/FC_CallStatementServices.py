"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FC_CallStatementServices

DESCRIPTION
    This module contains services used to provide up-to-date call deposit statement
    data to Front Cache.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-03-12      FAOPS-401       Cuen Edwards            Chris van der Walt      Initial Implementation.
2019-05-27      FAOPS-401       Cuen Edwards            Chris van der Walt      Changed to support generation of statements for parties
                                                                                without contacts.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import CallStatementGeneral
from CallStatementXMLGenerator import GenerateCallStatementXMLRequest, CallStatementXMLGenerator
import DocumentConfirmationGeneral
import DocumentGeneral


_xml_generator = CallStatementXMLGenerator()


def is_eligible_for_statement(trade):
    """
    Determine whether or not a specified trade is eligible for
    a call deposit statement.
    """
    return CallStatementGeneral.is_eligible_for_statement(trade)


def generate_statement_xml(trade, from_date, to_date):
    """
    Generate the document XML for a call deposit statement.
    """
    _validate_statement_trade(trade)
    _validate_statement_date_range(trade, from_date, to_date)
    # Create a temporary confirmation so that Front Arena selects
    # the statement contacts according to its rules and we avoid
    # attempting to duplicate this logic.
    confirmation = _create_statement_confirmation(trade)
    request = GenerateCallStatementXMLRequest(
        confirmation.Trade(),
        confirmation.Acquirer(),
        confirmation.AcquirerContactRef(),
        confirmation.Counterparty(),
        confirmation.CounterpartyContactRef(),
        from_date,
        to_date,
        None
    )
    return _xml_generator.generate_xml(request)


def _validate_statement_trade(trade):
    """
    Validate that a trade is eligible for a call statement.
    """
    if not is_eligible_for_statement(trade):
        raise ValueError('Trade {trade_oid} is not eligible for a call statement.'.format(
            trade_oid=trade.Oid()
        ))


def _validate_statement_date_range(trade, from_date, to_date):
    """
    Validate that a call statement may be generated for a specified
    trade and date range.
    """
    document_name = 'statement'
    DocumentGeneral.validate_document_date_range(document_name, from_date, to_date)
    # Only permit creation of statements up to two years back.
    date_today = acm.Time.DateToday()
    first_of_month = acm.Time.FirstDayOfMonth(date_today)
    first_of_month_two_years_back = acm.Time.DateAddDelta(first_of_month, -2, 0, 0)
    if from_date < first_of_month_two_years_back:
        raise ValueError('A statement from date may not be further than two years back.')
    if not CallStatementGeneral.statement_money_flows_exist(trade, from_date, to_date):
        exception_message = "No statement money flows found for trade "
        exception_message += "'{trade_oid}'."
        exception_message = exception_message.format(
            trade_oid=trade.Oid()
        )
        raise ValueError(exception_message)


def _create_statement_confirmation(trade):
    """
    Create a call statement confirmation.
    """
    event_name = CallStatementGeneral.get_statement_event_name()
    event = DocumentConfirmationGeneral.get_confirmation_event(event_name)
    method = acm.FMethodChain(acm.FSymbol(str(event.receiver)))
    receiver = method.Call([trade])
    return acm.Operations.CreateConfirmation(trade, event.eventName, None, receiver, method, None)
