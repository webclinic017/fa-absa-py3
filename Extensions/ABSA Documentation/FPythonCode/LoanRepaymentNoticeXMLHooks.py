"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanRepaymentNoticeXMLHooks

DESCRIPTION
    This module contains the xml hooks used to generate the values in the xml template.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-20                      Stuart Wilson           Loan Ops                XML Hooks for confo generation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime

import acm

from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
from LoanRepaymentNoticeXMLGenerator import GenerateRepaymentNoticeXMLRequest, RepaymentNoticeXMLGenerator


email_body_html_generator = EmailBodyHTMLGenerator()
generator = RepaymentNoticeXMLGenerator()


def value_date(confirmation):
    date=acm.Time.DateAddDelta(acm.Time.DateFromTime(confirmation.CreateTime()), 0, 0, 7)
    return datetime(*acm.Time.DateToYMD(date)).strftime('%d %B %Y')

def get_email_body(confirmation):
    """
    This Function creates an html email body
    """
    document_description = 'your {document_type} for {period_description}'
    document_description = document_description.format(
        document_type='Repayment Notice',
        period_description=value_date(confirmation)
    )
    request = GenerateEmailBodyHTMLRequest(
        confirmation.AcquirerContactRef().Attention(),
        confirmation.AcquirerContactRef().Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return email_body_html_generator.generate_html(request)


def get_email_subject(confirmation):
    """
    Function for creates email subject
    """
    conf_date = value_date(confirmation)
    counterparty = str(confirmation.Receiver().Id())
    event_name = confirmation.EventChlItem().Name()
    seq = (event_name + ":", counterparty, conf_date)
    return "".join(seq)


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a term
    deposit statement.
    """
    prod_env = acm.FInstallationData.Select('').At(0).Name() == 'Production'
    if prod_env:
        contact = confirmation.AcquirerContactRef()
        return contact.Email()
    return None


def get_email_file_name(confirmation):
    """
    This Function returns filename which is event name + counterparty + confirmation date
    """

    conf_date = value_date(confirmation)
    counterparty = str(confirmation.Receiver().Id())
    event_name = confirmation.EventChlItem().Name()
    seq = (event_name, counterparty, conf_date)
    return "_".join(seq)


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a term
    deposit statement.
    """
    contact = confirmation.CounterpartyContactRef()
    return contact.Email()


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a term
    deposit statement.
    """
    contact = confirmation.AcquirerContactRef()
    # Ensure that only one from email is specified or the email
    # may be rejected by the mail server.
    return contact.Email().split(',')[0]


def repayment_notice_xml(confirmation):
    """
    Function to return specific xml generated for rate notice document
    """
    xml_request = GenerateRepaymentNoticeXMLRequest(
        confirmation.Acquirer(),
        confirmation.AcquirerContactRef(),
        confirmation.Counterparty(),
        confirmation.CounterpartyContactRef(),
        confirmation
        )
    return generator.generate_xml(xml_request)
