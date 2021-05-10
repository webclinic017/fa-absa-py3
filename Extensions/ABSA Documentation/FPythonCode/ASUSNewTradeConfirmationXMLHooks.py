"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUSNewTradeConfirmationXMLHooks

DESCRIPTION
    This module contains an object used to generate the XML for ASUS New Trade Confirmation that
    will be sent to Adaptiv to form PDF's to be mailed to clients

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Requester               Description
---------------------------------------------------------------------------------------------------------------------
2020-02-17      FAOPS-708       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS New Trade Confirmations
---------------------------------------------------------------------------------------------------------------------
"""

import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

import acm
from FOperationsDocumentXML import FOperationsDocumentXML

import ASUSNewTradeConfirmationGeneral
from ASUSNewTradeConfirmationXMLGenerator import (
    ASUSNewTradeConfirmationXMLGenerator, GenerateASUSNewTradeConfirmationXMLRequest
)
import DocumentGeneral
import DocumentConfirmationGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest


class USCustomEmailRequest(GenerateEmailBodyHTMLRequest):

    def __init__(self, from_department, from_telephone, from_email, document_description):
        super(USCustomEmailRequest, self).__init__(from_department, from_telephone, from_email, document_description)


class USEmailBodyHTMLGenerator(EmailBodyHTMLGenerator):

    def _generate_contact_us_message_row_element(self):
        """
        Generate the contact us message row element.
        """
        text = 'If you have any questions or concerns related to this attachment, please contact us.'
        return self._generate_table_row_element(text, bold=False, padded=True)

    def _generate_from_name_row_element(self, generate_email_body_html_request):
        """
        Generate the from name row element.
        """
        from_department = generate_email_body_html_request.from_department
        from_name = from_department
        if DocumentGeneral.is_string_value_present(from_department):
            from_name = '{from_department}'.format(
                from_department=from_department.strip()
            )
        return self._generate_table_row_element(from_name, bold=False, padded=False)


def get_from_email_address(confirmation):
    """
    Get the Banks Email Address
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_from(confirmation)


def get_bcc_email_address(confirmation):
    """
    Gets the BCC Address for the email
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_bcc(confirmation)


def get_to_email_address(confirmation):
    """
    Gets the Counterparty's email address
    """
    if confirmation.Trade().AdditionalInfo().XtpTradeType() == 'OBP_BLOCK_TRADE':
        contact = ASUSNewTradeConfirmationGeneral.get_counterparty_contact(confirmation.Trade())
        return contact.Email()
    return DocumentConfirmationGeneral.get_default_confirmation_email_to(confirmation)


def get_email_subject(confirmation):
    """
    Generates the Subject of the email
    """
    return get_email_filename(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Generates the Body of the email
    """
    document_description = 'your Transaction '
    if confirmation.Type() in ['Amendment', 'Cancellation']:
        document_description += confirmation.Type()
    document_description += ' Confirmation'
    acquirer_contact = DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation)
    request = USCustomEmailRequest(
        acquirer_contact.Attention(),
        acquirer_contact.Telephone(),
        get_from_email_address(confirmation),
        document_description
    )
    email_body_html_generator = USEmailBodyHTMLGenerator()
    return email_body_html_generator.generate_html(request)


def get_email_filename(confirmation):
    """
    Generates the Filename for the Confirmation
    """
    # Security name.
    instrument = confirmation.Trade().Instrument()
    security_name = instrument.Name()
    if instrument.Underlying() and instrument.InsType() not in ['Stock', 'ETF']:
        security_name = instrument.Underlying().Name()
    # Counterparty name.
    counterparty = ASUSNewTradeConfirmationGeneral.get_counterparty_for_trade(confirmation.Trade())
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(counterparty)
    # Create file name.
    event_type = ''
    if confirmation.Type() in ['Amendment', 'Cancellation']:
        event_type = confirmation.Type()
    file_name_template = 'Transaction Confirmation {security_name} {counterparty_name} {_date}'
    if event_type != '':
        file_name_template = 'Transaction {event_type} Confirmation {security_name} {counterparty_name} {_date}'
    file_name = file_name_template.format(
        event_type=event_type,
        security_name=security_name,
        counterparty_name=counterparty_name,
        _date=ASUSNewTradeConfirmationGeneral.format_string_to_asus_format(acm.Time.DateToday(), '%d%m%y')
    )
    return file_name


def generate_confirmation_xml(confirmation):
    """
    Generates the XML for the Confirmation
    """
    if confirmation.Type() == 'Cancellation':
        xml_string = ASUSNewTradeConfirmationGeneral.get_last_released_xml(confirmation)
        root_element = ElementTree.fromstring(xml_string)
        document_element = root_element.find('.//DOCUMENT')
        subject_element = document_element.find('.//SUBJECT')
        subject_element.text = "TRADE CANCELLATION CONFIRMATION"
        xml_string = ElementTree.tostring(document_element)
        document = minidom.parseString(xml_string)
        # Return a pretty-printed version of the document without
        # the xml declaration (Front doesn't seem to like acmTemplate
        # hooks returning XML with an XML declaration).
        root_element = document.childNodes[0]

        return root_element.toprettyxml(indent='  ')
    else:
        to_party = confirmation.Counterparty()
        to_party_contact = confirmation.CounterpartyContactRef()
        if confirmation.Trade().AdditionalInfo().XtpTradeType() == 'OBP_BLOCK_TRADE':
            contact = ASUSNewTradeConfirmationGeneral.get_counterparty_contact(confirmation.Trade())
            to_party_contact = contact
            to_party = contact.Party()
        xml_request = GenerateASUSNewTradeConfirmationXMLRequest(confirmation.Acquirer(),
                                                                 confirmation.AcquirerContactRef(),
                                                                 to_party,
                                                                 to_party_contact,
                                                                 confirmation)
        return ASUSNewTradeConfirmationXMLGenerator().generate_xml(xml_request)


def get_cancellation_confirmation_xml(cancellation_template, cancellation_confirmation, override_xml):
    """
    Create the XML for a cancellation trade confirmation.

    This hook implementation generates new XML based on the
    cancellation confirmation as opposed to the default Front Arena
    behaviour of returning the previous confirmations XML with only
    the confirmation type element adjusted to reflect a cancellation.
    """
    return FOperationsDocumentXML.GenerateXmlFromTemplateAsString(cancellation_template,
                                                                  cancellation_confirmation,
                                                                  override_xml)
