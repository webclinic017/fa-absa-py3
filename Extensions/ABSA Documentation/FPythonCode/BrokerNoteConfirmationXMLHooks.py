"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteConfirmationXMLHooks

DESCRIPTION
    This module contains any hooks used to populate the confirmation XML template
    for the broker note functionality.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-28      FAOPS-61        Stuart Wilson           Capital Markets         Initial Implementation.
2020-02-10      FAOPS-725       Cuen Edwards            Kgomotso Gumbo          Minor refactoring.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime

import BrokerNoteGeneral
from BrokerNoteXMLGenerator import BrokerNoteXMLGenerator, GenerateBrokerNoteXMLRequest, GenerateCustodianAccountDetails
import DocumentGeneral
import DocumentConfirmationGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest


email_body_html_generator = EmailBodyHTMLGenerator()
xml_generator = BrokerNoteXMLGenerator()


def get_email_file_name(confirmation):
    """
    Get the file name to be given to a broker note email attachment.
    """
    # Security name.
    instrument = confirmation.Trade().Instrument()
    security_name = instrument.Name()
    if instrument.Underlying():
        security_name = instrument.Underlying().Name()
    # Counterparty name.
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(confirmation.Counterparty())
    # Create file name.
    file_name_template = 'Transaction Notice {security_name} {counterparty_name} {date_today}'
    file_name = file_name_template.format(
        security_name=security_name,
        counterparty_name=counterparty_name,
        date_today=datetime.today().strftime('%d%m%y')
    )
    return file_name


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a broker note.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_from(confirmation)


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a broker note.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_to(confirmation)


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a broker note.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_bcc(confirmation)


def get_email_subject(confirmation):
    """
    Get the email subject to be used when delivering a broker note.
    """
    return get_email_file_name(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Get the email body to be used when delivering a broker note.
    """
    document_description = 'your {document_type}'
    document_description = document_description.format(
        document_type='Transaction Notice')
    request = GenerateEmailBodyHTMLRequest(
        confirmation.AcquirerContactRef().Attention(),
        confirmation.AcquirerContactRef().Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return email_body_html_generator.generate_html(request)


def get_document_xml(confirmation):
    """
    Create the document XML for a broker note.
    """
    # Prevent the generation of XML for a non-broker note confirmation.
    DocumentConfirmationGeneral.validate_confirmation_for_event(confirmation, BrokerNoteGeneral
        .get_broker_note_event_name())
    custodian_details = GenerateCustodianAccountDetails(confirmation)
    request = GenerateBrokerNoteXMLRequest(confirmation, custodian_details)
    return xml_generator.generate_xml(request)
