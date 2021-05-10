"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FC_TermStatementServices

DESCRIPTION
    This module contains services used to provide up-to-date term deposit statement
    data to Front Cache.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-29      FAOPS-402       Cuen Edwards            Chris van der Walt      Initial Implementation.
2019-05-27      FAOPS-402       Cuen Edwards            Chris van der Walt      Changed to support generation of statements for parties
                                                                                without contacts.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentConfirmationGeneral
import DocumentGeneral
from MultiTradeConfirmationOwnerProvider import MultiTradeConfirmationOwnerProvider
import TermStatementGeneral
from TermStatementXMLGenerator import GenerateTermStatementXMLRequest, TermStatementXMLGenerator


_confirmation_owner_trade_provider = MultiTradeConfirmationOwnerProvider()
_xml_generator = TermStatementXMLGenerator()


def generate_statement_xml(acquirer, counterparty, from_date, to_date):
    """
    Generate the document XML for a term deposit statement.
    """
    _validate_statement_date_range(acquirer, counterparty, from_date, to_date)
    # Create a temporary confirmation so that Front Arena selects
    # the statement contacts according to its rules and we avoid
    # attempting to duplicate this logic.
    confirmation = _create_statement_confirmation(acquirer, counterparty)
    request = GenerateTermStatementXMLRequest(
        confirmation.Acquirer(),
        confirmation.AcquirerContactRef(),
        confirmation.Counterparty(),
        confirmation.CounterpartyContactRef(),
        from_date,
        to_date,
        None
    )
    return _xml_generator.generate_xml(request)


def _validate_statement_date_range(acquirer, counterparty, from_date, to_date):
    """
    Validate that a term statement may be generated for a specified
    acquirer, counterparty, and date range.
    """
    document_name = 'statement'
    DocumentGeneral.validate_document_date_range(document_name, from_date, to_date)
    # Only permit creation of statements up to two years back.
    date_today = acm.Time.DateToday()
    first_of_month = acm.Time.FirstDayOfMonth(date_today)
    first_of_month_two_years_back = acm.Time.DateAddDelta(first_of_month, -2, 0, 0)
    if from_date < first_of_month_two_years_back:
        raise ValueError('A statement from date may not be further than two years back.')
    if not TermStatementGeneral.statement_trades_exist(acquirer, counterparty, from_date, to_date):
        exception_message = "No statement trades found for acquirer '{acquirer_name}' "
        exception_message += "and '{counterparty_name}'."
        exception_message = exception_message.format(
            acquirer_name=acquirer.Name(),
            counterparty_name=counterparty.Name()
        )
        raise ValueError(exception_message)


def _create_statement_confirmation(acquirer, counterparty):
    """
    Create a term statement confirmation.
    """
    trade = _confirmation_owner_trade_provider.provide_owner_trade(acquirer, counterparty)
    event_name = TermStatementGeneral.get_statement_event_name()
    event = DocumentConfirmationGeneral.get_confirmation_event(event_name)
    method = acm.FMethodChain(acm.FSymbol(str(event.receiver)))
    receiver = method.Call([trade])
    return acm.Operations.CreateConfirmation(trade, event.eventName, None, receiver, method, None)
