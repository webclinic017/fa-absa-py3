"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeConfirmationXMLHooks

DESCRIPTION
    This module contains any hooks used to populate the confirmation XML template 
    for trade confirmations.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

from FOperationsDocumentXML import FOperationsDocumentXML

import DocumentGeneral
import DocumentConfirmationGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
import TradeConfirmationGeneral
from TradeConfirmationXMLGenerator import GenerateTradeConfirmationXMLRequest, TradeConfirmationXMLGenerator


email_body_html_generator = EmailBodyHTMLGenerator()
xml_generator = TradeConfirmationXMLGenerator()


def get_email_file_name(confirmation):
    """
    Get the file name to be given to a trade confirmation email
    attachment.
    """
    # Counterparty name.
    counterparty_name = DocumentGeneral.get_party_full_name(confirmation.Counterparty())
    counterparty_short_code = DocumentGeneral.get_party_short_code(confirmation.Counterparty())
    if counterparty_short_code is not None:
        counterparty_name += ' ({counterparty_short_code})'.format(
            counterparty_short_code=counterparty_short_code
        )
    file_name_template = "{event_description} {trade_oid} {counterparty_name}"
    file_name = file_name_template.format(
        event_description=TradeConfirmationGeneral.get_event_description(confirmation),
        trade_oid=confirmation.Trade().Oid(),
        counterparty_name=counterparty_name
    )
    return DocumentGeneral.format_file_name(file_name)


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a trade
    confirmation.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_from(confirmation)


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a trade
    confirmation.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_to(confirmation)


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a trade
    confirmation.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_bcc(confirmation)


def get_email_subject(confirmation):
    """
    Get the email subject to be used when delivering a trade
    confirmation.
    """
    return get_email_file_name(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Get the email body to be used when delivering a trade
    confirmation.
    """
    document_description = 'your {event_description} for trade {trade_oid}'
    document_description = document_description.format(
        event_description=TradeConfirmationGeneral.get_event_description(confirmation),
        trade_oid=confirmation.Trade().Oid()
    )
    acquirer_contact = DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation)
    request = GenerateEmailBodyHTMLRequest(
        acquirer_contact.Attention(),
        acquirer_contact.Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return email_body_html_generator.generate_html(request)


def get_document_xml(confirmation):
    """
    Create the document XML for a trade confirmation.
    """
    if confirmation.Type() == 'Cancellation':
        xml_string = TradeConfirmationGeneral.get_last_released_xml(confirmation)
        root_element = ElementTree.fromstring(xml_string)
        document_element = root_element.find('.//DOCUMENT')
        subject_element = document_element.find('.//SUBJECT')
        subject_element.text = TradeConfirmationGeneral.get_event_description(confirmation)
        xml_string = ElementTree.tostring(document_element)
        document = minidom.parseString(xml_string)
        # Return a pretty-printed version of the document without
        # the xml declaration (Front doesn't seem to like acmTemplate
        # hooks returning XML with an XML declaration).
        root_element = document.childNodes[0]
        return root_element.toprettyxml(indent='  ')
    else:
        # Prevent the generation of XML for a non-trade confirmation.
        DocumentConfirmationGeneral.validate_confirmation_for_event(confirmation, TradeConfirmationGeneral
            .get_trade_confirmation_event_name())
        request = GenerateTradeConfirmationXMLRequest(confirmation)
        return xml_generator.generate_xml(request)


def get_cancellation_confirmation_xml(cancellation_template, cancellation_confirmation, override_xml):
    """
    Create the XML for a cancellation trade confirmation.

    This hook implementation generates new XML based on the
    cancellation confirmation as opposed to the default Front Arena
    behaviour of returning the previous confirmations XML with only
    the confirmation type element adjusted to reflect a cancellation.
    """
    return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(cancellation_template,
        cancellation_confirmation, override_xml)
