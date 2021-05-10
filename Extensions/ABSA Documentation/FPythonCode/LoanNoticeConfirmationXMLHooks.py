"""
-------------------------------------------------------------------------------
MODULE
    LoanNoticeConfirmationXMLHooks


DESCRIPTION
    Date                : 2018-06-14
    Purpose             :
    Requester           : Kgomotso Gumbo
    Developer           : Stuart Wilson


HISTORY
===============================================================================
2018-09-20    Stuart Wilson      FAOPS-97  Refactor additional module
-------------------------------------------------------------------------------"""

import DocumentConfirmationGeneral
import DocumentGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
from LoanNoticeConfirmationXMLGenerator import GenerateRateNoticeXMLRequest, RateNoticeXMLGenerator
import LoanNoticeGeneral


_email_body_html_generator = EmailBodyHTMLGenerator()
_xml_generator = RateNoticeXMLGenerator()


def get_email_file_name(confirmation):
    """
    Get the file name to be given to a loan rate notice email
    attachment.
    """
    conf_date = LoanNoticeGeneral.get_conf_date(confirmation)
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
        confirmation.Counterparty())
    event_name = confirmation.EventChlItem().Name()
    seq = (event_name, counterparty_name, conf_date)
    file_name = " ".join(seq)
    return DocumentGeneral.format_file_name(file_name)


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a loan
    rate notice.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_from(confirmation)


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a loan
    rate notice.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_to(confirmation)


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a loan
    rate notice.
    """
    return DocumentConfirmationGeneral.get_default_confirmation_email_bcc(confirmation)


def get_email_subject(confirmation):
    """
    Get the email subject to be used when delivering a loan
    rate notice.
    """
    return get_email_file_name(confirmation) + '.pdf'


def get_email_body(confirmation):
    """
    Get the email body to be used when delivering a loan rate
    notice.
    """
    document_description = 'your {document_type} for {document_date}'
    document_description = document_description.format(
        document_type='Rate Notice',
        document_date=LoanNoticeGeneral.get_conf_date(confirmation)
    )
    acquirer_contact = DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation)
    request = GenerateEmailBodyHTMLRequest(
        acquirer_contact.Attention(),
        acquirer_contact.Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return _email_body_html_generator.generate_html(request)


def rate_notice_xml(confirmation):
    """
    Create the confirmation XML for a loan rate notice.
    """
    xml_request = GenerateRateNoticeXMLRequest(
        confirmation.Acquirer(),
        DocumentConfirmationGeneral.get_confirmation_acquirer_contact(confirmation),
        confirmation.Counterparty(),
        DocumentConfirmationGeneral.get_confirmation_counterparty_contact(confirmation),
        confirmation
    )
    return _xml_generator.generate_xml(xml_request)
