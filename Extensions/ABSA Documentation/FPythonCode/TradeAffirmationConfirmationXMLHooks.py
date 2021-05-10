"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeAffirmationConfirmationXMLHooks

DESCRIPTION
    This module contains any hooks used to populate the confirmation XML template 
    for trade affirmations.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-25      FAOPS-226       Cuen Edwards            Letitia Carboni         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from FOperationsDocumentXML import FOperationsDocumentXML

import DocumentConfirmationGeneral
import DocumentGeneral
import TradeAffirmationGeneral
from TradeAffirmationXMLGenerator import GenerateTradeAffirmationXMLRequest, TradeAffirmationXMLGenerator
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest


_email_body_html_generator = EmailBodyHTMLGenerator()
_xml_generator = TradeAffirmationXMLGenerator()


def get_email_file_name(confirmation):
    """
    Get the file name to be given to a trade affirmation email
    attachment.
    """
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
        confirmation.Counterparty())
    file_name_template = "{event_description} {trade_oid} {counterparty_name}"
    file_name = file_name_template.format(
        event_description=TradeAffirmationGeneral.get_event_description(confirmation),
        trade_oid=confirmation.Trade().Oid(),
        counterparty_name=counterparty_name
    )
    return DocumentGeneral.format_file_name(file_name)


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a trade
    affirmation.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_from(confirmation)


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a trade
    affirmation.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_to(confirmation)


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a trade
    affirmation.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_bcc(confirmation)


def get_email_subject(confirmation):
    """
    Get the email subject to be used when delivering a trade
    affirmation.
    """
    return get_email_file_name(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Get the email body to be used when delivering a trade
    affirmation.
    """
    document_description = 'your {event_description} for trade {trade_oid}'
    document_description = document_description.format(
        event_description=TradeAffirmationGeneral.get_event_description(confirmation),
        trade_oid=confirmation.Trade().Oid()
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
    Create the document XML for a trade affirmation.
    """
    # Prevent the generation of XML for a non-trade affirmation confirmation.
    DocumentConfirmationGeneral.validate_confirmation_for_event(confirmation, TradeAffirmationGeneral
        .get_trade_affirmation_event_name())
    request = GenerateTradeAffirmationXMLRequest(confirmation)
    return _xml_generator.generate_xml(request)


def get_cancellation_confirmation_xml(cancellation_template, cancellation_confirmation, override_xml):
    """
    Create the XML for a cancellation trade affirmation confirmation.

    This hook implementation generates new XML based on the
    cancellation confirmation as opposed to the default Front Arena
    behaviour of returning the previous confirmations XML with only
    the confirmation type element adjusted to reflect a cancellation.
    """
    return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(cancellation_template,
        cancellation_confirmation, override_xml)
