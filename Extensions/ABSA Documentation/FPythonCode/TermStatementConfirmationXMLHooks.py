"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermStatementConfirmationXMLHooks

DESCRIPTION
    This module contains any hooks used to populate the confirmation XML template 
    for the term deposit statement functionality.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation.
2018-08-01                      Cuen Edwards                                    Refactored to use some functionality from DocumentGeneral.
2018-08-25                      Cuen Edwards                                    Refactored to use EmailBodyHTMLGenerator.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import DocumentConfirmationGeneral
import DocumentGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
import TermStatementGeneral
from TermStatementXMLGenerator import GenerateTermStatementXMLRequest, TermStatementXMLGenerator


_email_body_html_generator = EmailBodyHTMLGenerator()
_xml_generator = TermStatementXMLGenerator()


def get_email_file_name(confirmation):
    """
    Get the file name to be given to a term deposit statement
    confirmation email attachment.
    """
    # Period description.
    period_description = DocumentConfirmationGeneral.get_confirmation_date_range_description(
        confirmation)
    # Counterparty name.
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
        confirmation.Counterparty())
    # Create file name.
    file_name_template = "Interest Statement "
    file_name_template += "{counterparty_name} {period_description}"
    file_name = file_name_template.format(
        counterparty_name=counterparty_name,
        period_description=period_description
    )
    return DocumentGeneral.format_file_name(file_name)


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a term
    deposit statement.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_from(confirmation)


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a term
    deposit statement.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_to(confirmation)


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a term
    deposit statement.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_bcc(confirmation)


def get_email_subject(confirmation):
    """
    Get the email subject to be used when delivering a term
    deposit statement.
    """
    return get_email_file_name(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Get the email body to be used when delivering a term
    deposit statement.
    """
    document_description = 'your {document_type} for {period_description}'
    document_description = document_description.format(
        document_type='Interest Statement',
        period_description=DocumentConfirmationGeneral.get_confirmation_date_range_description(confirmation)
    )
    acquirer_contact = DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation)
    request = GenerateEmailBodyHTMLRequest(
        acquirer_contact.Attention(),
        acquirer_contact.Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return _email_body_html_generator.generate_html(request)


def get_document_xml(confirmation):
    """
    Create the document XML for a term deposit statement.
    """
    # Prevent the generation of XML for a non-affirmation confirmation.
    DocumentConfirmationGeneral.validate_confirmation_for_event(confirmation, TermStatementGeneral
        .get_statement_event_name())
    request = GenerateTermStatementXMLRequest(
        confirmation.Acquirer(),
        DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation),
        confirmation.Counterparty(),
        DocumentConfirmationGeneral.get_confirmation_counterparty_contact(confirmation),
        DocumentConfirmationGeneral.get_confirmation_from_date(confirmation),
        DocumentConfirmationGeneral.get_confirmation_to_date(confirmation),
        DocumentConfirmationGeneral.get_confirmation_schedule(confirmation)
    )
    return _xml_generator.generate_xml(request)
