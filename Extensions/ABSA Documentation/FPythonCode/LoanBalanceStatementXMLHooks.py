"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanBalanceStatementXMLHooks

DESCRIPTION
    This module contains any hooks used to populate the confirmation XML template
    for the loan balance statement functionality.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-05-29      FAOPS-513       Stuart Wilson           Kershia Perumal         Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import DocumentConfirmationGeneral
import DocumentGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
from LoanBalanceStatementXMLGenerator import LoanBalanceStatementXMLGenerator, GenerateLoanBalanceStatementXMLRequest


_email_body_html_generator = EmailBodyHTMLGenerator()
_xml_generator = LoanBalanceStatementXMLGenerator()


def get_email_file_name(confirmation):
    """
    Creates file name for broker note email sent out through adaptiv
    """
    period_description = DocumentConfirmationGeneral.get_confirmation_date_range_description(
        confirmation)
    # Counterparty name.
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
        confirmation.Counterparty())
    # Create file name.
    file_name_template = "Balance Statement {counterparty_name} {period_description}"
    file_name = file_name_template.format(
        counterparty_name=counterparty_name,
        period_description=period_description
    )
    return file_name


def get_email_from(confirmation):
    """
    Gets email that is being used to send from
    """
    contact = confirmation.AcquirerContactRef()
    # Ensure that only one from email is specified or the email
    # may be rejected by the mail server.
    return contact.Email().split(',')[0]


def get_email_to(confirmation):
    """
    Gets email that broker note is being sent to
    """
    contact = confirmation.CounterpartyContactRef()
    return contact.Email()


def get_email_bcc(confirmation):
    """
    Gets the bcc email to be added
    """
    contact = confirmation.AcquirerContactRef()
    return contact.Email()


def get_email_subject(confirmation):
    """
    Gets subject for email
    """
    return get_email_file_name(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Creates the body for the email
    """
    document_description = 'your {document_type}'
    document_description = document_description.format(
        document_type='Balance Statement')
    request = GenerateEmailBodyHTMLRequest(
        confirmation.AcquirerContactRef().Attention(),
        confirmation.AcquirerContactRef().Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return _email_body_html_generator.generate_html(request)


def get_balance_statement_xml(confirmation):
    """
    Gets xml for specific broker note components of xml message structure
    """
    request = GenerateLoanBalanceStatementXMLRequest(
        confirmation.Trade(),
        confirmation.Acquirer(),
        DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation),
        confirmation.Counterparty(),
        DocumentConfirmationGeneral.get_confirmation_counterparty_contact(confirmation),
        DocumentConfirmationGeneral.get_confirmation_from_date(confirmation),
        DocumentConfirmationGeneral.get_confirmation_to_date(confirmation)
    )
    return _xml_generator.generate_xml(request)
