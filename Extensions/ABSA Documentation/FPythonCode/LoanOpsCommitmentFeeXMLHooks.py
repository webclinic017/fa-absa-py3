"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanOpsCommitmentFeeXMLHooks

DESCRIPTION
    This module contains any hooks used to populate the confirmation XML template
    for the Commitment Fee Invoice functionality.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-05      FAOPS-530       Joash Moodley                                   Initial Implementation.
2021-02-18      FAOPS-1078      Joshua Mvelase          Gasant Thulsie          Updated function get_branch_code
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_time import to_date, acm_date
import CommFeeCalculation as calc
import DocumentConfirmationGeneral
import DocumentGeneral
from EmailBodyHTMLGenerator import EmailBodyHTMLGenerator, GenerateEmailBodyHTMLRequest
from HelperFunctions import HelperFunctions
from LoanOpsCommitmentFeeXMLGenerator import GenerateLoanOpsCommitmentFeetXMLRequest, LoanOpsCommitmentFeeXMLGenerator


email_body_html_generator = EmailBodyHTMLGenerator()
xml_generator = LoanOpsCommitmentFeeXMLGenerator()
TODAY = acm.Time().DateToday()


def COMMITMENT_FEE(trade):
    return False


def COMMITMENT_FEE_AMENDMENT(trade):
    return False


def _get_cmf_payment(payments, pay_date):
    payment = None
    for pay in payments:
        if pay.Type() == 'Commitment Fee' and pay.PayDay() == pay_date:
            payment = pay
            break

    return payment


def get_facility_id(confirmation):
    return confirmation.Trade().AdditionalInfo().PM_FacilityID()


def get_currency_name(confirmation):
    trade = confirmation.Trade()
    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()
    payments = trade.Payments().SortByProperty('ValidFrom').Reverse()
    payment = _get_cmf_payment(payments, valid_from_date)
    return payment.Currency().Name()


def get_pay_day(confirmation):
    return confirmation.AdditionalInfo().DocumentFromDate()


def get_invoice_future_amount(confirmation):
    trade = confirmation.Trade()
    name = '{0}{1}'.format('CMF', trade.Name())
    all_valid_trades = HelperFunctions().get_trade_list()
    com_fee_calculator = calc.CMFTrades(trade, name, False)
    record = com_fee_calculator.dataAcess.Select(name)
    com_fee_calculator.load_from_json(record)

    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()

    calc_space = acm.Calculations().CreateCalculationSpace(
        acm.GetDefaultContext(),
        'FTradeSheet'
    )

    rate_per_day = com_fee_calculator._calculate_comm_fee(
        [],
        all_valid_trades,
        calc_space,
        False
    )

    payments = trade.Payments().SortByProperty('ValidFrom').Reverse()
    if valid_from_date == TODAY:
        payment = _get_cmf_payment(payments, TODAY)
    else:
        payment = _get_cmf_payment(payments, valid_from_date)
    amount = payment.Amount()
    today = acm.Time.DateToday()
    days_left = to_date(payment.PayDay()) - to_date(today)
    comm_fee_charge = 0
    payments = confirmation.Trade().Payments()
    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()

    for payment in payments:
        if payment.PayDay() == valid_from_date and payment.Type() in ['Cash', 'Commitment Fee']:
            comm_fee_charge = comm_fee_charge + payment.Amount()

    if not rate_per_day:
        amount_charged = amount
    elif days_left.days < 0:
        amount_charged = comm_fee_charge
    else:
        amount_charged = (days_left.days * rate_per_day) + comm_fee_charge
    return round(amount_charged, 2)


def get_invoice_amount(confirmation):
    payments = confirmation.Trade().Payments()
    fees = 0
    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()

    if  valid_from_date > TODAY:
        fees = get_invoice_future_amount(confirmation)
    elif valid_from_date <= TODAY:
        for payment in payments:
            if payment.PayDay() == valid_from_date and payment.Type() in ['Cash', 'Commitment Fee']:
                fees = fees + payment.Amount()
    return round(fees, 2)


def get_account_details(confirmation):
    def _get_account(account_id):
        acquirer = confirmation.Acquirer()
        for account in acquirer.Accounts():
            if str(account.Oid()) == account_id:
                return account
        return None

    currency_name = get_currency_name(confirmation)
    if currency_name =='ZAR':
        settle_cat = confirmation.Trade().SettleCategoryChlItem()
        if settle_cat:
            settle_cat = settle_cat.Name()
            if settle_cat == 'Syndicated_Absa':
                return _get_account('33313')

        return _get_account('21839')

    if currency_name =='USD':
        return _get_account('21846')
    if currency_name =='EUR':
        return _get_account('21845')
    if currency_name =='GBP':
        return _get_account('21844')
    return None


def get_branch_code(confirmation):
    branch_code = ''
    currency_name = get_currency_name(confirmation)
    account = get_account_details(confirmation)
    if account:
        branch_code = account.Accounting()
    return branch_code


def get_institution(confirmation):
    account = get_account_details(confirmation)
    return account.CorrespondentBank().Name()


def get_account_number(confirmation):
    account = get_account_details(confirmation)
    if len(account.Account().split(" ")) > 1:
        return account.Account().split(" ")[1]
    return account.Account()


def get_account_name(confirmation):
    return 'ABSA Bank Limited'


def get_reference(confirmation):
    return '%s Commitment Fee' % confirmation.Counterparty().Name()


def get_vat_amount(confirmation):
    is_foreign_party = confirmation.Counterparty().Free2ChoiceList()
    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()
    if is_foreign_party:
        if is_foreign_party.Name()  == 'Yes':
            return 0

    if  valid_from_date > TODAY:
        amount = get_invoice_future_amount(confirmation)
    elif valid_from_date <= TODAY:
        amount = get_invoice_amount(confirmation)

    return round( amount * 0.15, 2)


def get_total_amount(confirmation):
    vat = get_vat_amount(confirmation)
    invoice_amount = get_invoice_amount(confirmation)
    total = vat + invoice_amount

    return round(total, 2)


def get_swift_code(confirmation):
     account = get_account_details(confirmation)
     return account.CorrespondentBank().Swift()


def acquirer_vat_number(confirmation):
    acquirer = confirmation.Acquirer()
    return acquirer.AdditionalInfo().Vat_Number()


def counterparty_vat_number(confirmation):
    counterparty = confirmation.Counterparty()
    return counterparty.AdditionalInfo().Vat_Number()


def get_valid_from_date(confirmation):
    trade = confirmation.Trade()
    payments = trade.Payments().SortByProperty('ValidFrom').Reverse()
    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()
    if not valid_from_date:
        payment = _get_cmf_payment(payments, TODAY)
    else:
        payment = _get_cmf_payment(payments, valid_from_date)

    return payment.ValidFrom()


def get_pay_date(confirmation):
    trade = confirmation.Trade()
    payments = trade.Payments().SortByProperty('ValidFrom').Reverse()
    valid_from_date = confirmation.AdditionalInfo().DocumentFromDate()
    if not valid_from_date:
        payment = _get_cmf_payment(payments, TODAY)
    else:
        payment = _get_cmf_payment(payments, valid_from_date)

    return payment.PayDay()


def get_email_file_name(confirmation):
    """
    Get the file name to be given to a Commitment Fee Invoice email attachment.
    """
    # Period description.
    period_description = DocumentConfirmationGeneral.get_confirmation_date_range_description(
        confirmation)
    # Counterparty name.
    counterparty_name = DocumentGeneral.get_party_full_name_and_short_code(
        confirmation.Counterparty())
    # Create file name.
    file_name_template = confirmation.EventType()
    file_name_template += " {counterparty_name} {period_description}"
    file_name = file_name_template.format(
        counterparty_name=counterparty_name,
        period_description=period_description
    )
    return DocumentGeneral.format_file_name(file_name)


def get_email_from(confirmation):
    """
    Get the From email address to use for delivery of a Commitment Fee Invoice.
    """
    contact = confirmation.AcquirerContactRef()
    # Ensure that only one from email is specified or the email
    # may be rejected by the mail server.
    return contact.Email().split(',')[0]


def get_email_to(confirmation):
    """
    Get the To email address to use for delivery of a Commitment Fee Invoice.
    """
    contact = confirmation.CounterpartyContactRef()
    return contact.Email()


def get_email_bcc(confirmation):
    """
    Get any email address to be BCC'ed when delivering a Commitment Fee Invoice.
    """
    prod_env = acm.FInstallationData.Select('').At(0).Name() == 'Production'
    if prod_env:
        contact = confirmation.AcquirerContactRef()
        return contact.Email()


def get_email_subject(confirmation):
    """
    Get the email subject to be used when delivering a Commitment Fee Invoice.
    """
    subject = 'Commitment Fee Invoice %s' % confirmation.Counterparty().Name()
    if confirmation.EventType() == 'Loan Ops Commitment Fee Amendment':
        subject = 'Amended Commitment Fee Invoice %s' % confirmation.Counterparty().Name()
    return subject


def get_email_body(confirmation):
    """
    Get the email body to be used when delivering a Commitment Fee Invoice.
    """
    document_description = 'your {document_type} for {period_description}'

    document_description = document_description.format(
        document_type='Commitment Fee Invoice',
        period_description=DocumentConfirmationGeneral.get_confirmation_date_range_description(confirmation)
    )

    if confirmation.EventType() == 'Loan Ops Commitment Fee Future Date':
        disclaimer = '''
        Please note that the attached commitment fee invoice for a future date is based on the utilisation on date of this invoice.
        Should the utilisation amount change after date of this invoice, this invoice will not be valid.
        The commitment fee will be recalculated and a replacement invoice will be issued.

        '''
        document_description = document_description + disclaimer

    elif confirmation.EventType() == 'Loan Ops Commitment Fee Amendment':
        document_description = '''
        your Amended Commitment Fee Invoice for {period_description}. Kindly disregard previous commitment fee invoice issued for this period.
        '''.format(period_description=DocumentConfirmationGeneral.get_confirmation_date_range_description(confirmation))
    request = GenerateEmailBodyHTMLRequest(
        confirmation.AcquirerContactRef().Attention(),
        confirmation.AcquirerContactRef().Telephone(),
        get_email_from(confirmation),
        document_description
    )
    return email_body_html_generator.generate_html(request)


def get_document_xml(confirmation):
    """
    Create the document XML for a commitment fee.
    """

    DocumentConfirmationGeneral.validate_confirmation_for_event(
        confirmation,
        confirmation.EventType()
    )
    request = GenerateLoanOpsCommitmentFeetXMLRequest(
        confirmation.Acquirer(),
        confirmation.AcquirerContactRef(),
        confirmation.Counterparty(),
        confirmation.CounterpartyContactRef(),
        DocumentConfirmationGeneral.get_confirmation_from_date(confirmation),
        DocumentConfirmationGeneral.get_confirmation_to_date(confirmation),
        DocumentConfirmationGeneral.get_confirmation_schedule(confirmation)
        )
    return xml_generator.generate_xml(request)
