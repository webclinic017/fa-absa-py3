"""-----------------------------------------------------------------------------
This script sends an email notification about all upcoming Portfolio Swaps
expiries. By default it will include all PSwaps expiring in the next 5 business
days.
It is possible to set different initial date.

HISTORY
================================================================================
Date            Change no       Developer               Description
--------------------------------------------------------------------------------
2021-02-16      FAPE-506        Katerina Frickova       Initial Implementation
--------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import bankingday_timediff
from datetime import datetime
from PS_SendEmailNotification import CreateEmailReport
from PS_NotificationTextObject import NotificationTextObject

LOGGER = getLogger(__name__)
DATE_TODAY = acm.Time.DateToday()
TEXT_OBJECT_NAME = 'PS_Pswaps_Expiry_{}'


def custom_date_hook(selected):
    date_custom = ael_variables.get('custom_date')
    date_custom.enabled = selected.value
    date_custom.mandatory = selected.value


def send_email_hook(selected):
    email_destination = ael_variables.get('email_destinations')
    email_destination.enabled = selected.value
    email_destination.mandatory = selected.value


ael_variables = AelVariableHandler()

ael_variables.add(
    'days_to_expiry',
    mandatory=True,
    default=5,
    cls='int',
    label='Business Days to Expiry',
    alt='How many days before expiry should the instrument be included in the report'
)

ael_variables.add_bool(
    'custom_date_bool',
    label='Choose custom date',
    default=False,
    alt='Change initial date for Portfolio Swaps expiry.',
    hook=custom_date_hook
)

ael_variables.add(
    'custom_date',
    label='Custom Date',
    default='YYYY-MM-DD',
    alt='Date in the format YYYY-MM-DD'
)

ael_variables.add_bool(
    'send_email',
    label='Send email',
    default=True,
    alt='Send email to the given email addresses.',
    hook=send_email_hook
)

ael_variables.add(
    'email_destinations',
    mandatory=True,
    label='Email Destinations',
    alt='Email Destinations - Comma Separated'
)


class PortfolioExpiryReport(CreateEmailReport):

    def __init__(self, table_header_tuple, table_rows_list, date, business_days):
        super(PortfolioExpiryReport, self).__init__(table_header_tuple, table_rows_list)
        self.date = date
        self.business_days = business_days

    def to_html_description(self):
        return "Portfolio Swap Expiry Notification from {current_time}.<br><br>The following portfolio swaps\
                will expire in the next {days} business days\
                :<br><br>".format(current_time=self.date, days=self.business_days)


def check_input_date(date):
    try:
        datetime_output = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        return datetime_output
    except ValueError as ve:
        LOGGER.error('Incorrect date format, should be YYYY-MM-DD.')
        raise ve


def add_issue_status(resolved_issues, unresolved_issues):
    issue_collection = []

    if unresolved_issues:
        for oid, issue in list(unresolved_issues.items()):
            issue.append('<i style="color:#FF0000">unresolved</i>')
            tuple_issue = tuple(issue)
            issue_collection.append(tuple_issue)

    if resolved_issues:
        for oid, issue in list(resolved_issues.items()):
            issue.append('<i style="color:#228B22">resolved</i>')
            tuple_issue = tuple(issue)
            issue_collection.append(tuple_issue)

    return issue_collection


class PswapsIssues(object):

    def __init__(self, date, business_days):
        self.date = date
        self.business_days = business_days
        self.all_pswaps = acm.FPortfolioSwap.Select('')

    def expires_within(self, pswap):
        expiry_date = pswap.ExpiryDate()
        if expiry_date and self.date <= expiry_date:
            timediff = bankingday_timediff(
                pswap.Currency().Calendar(), self.date, expiry_date)
            return timediff.days <= self.business_days
        else:
            return False

    def find_expiring_pswaps(self):
        pswaps_collection = {}

        for pswap in self.all_pswaps:
            if self.expires_within(pswap):
                expiry_date = pswap.ExpiryDateOnly()
                LOGGER.info('Portfolio Swap {name} will expire on {date}.'.format(name=pswap.Name(), date=expiry_date))
                pswaps_collection[str(pswap.Oid())] = [pswap.Oid(), pswap.Name(), expiry_date]

        return pswaps_collection


def ael_main(ael_dict):

    if ael_dict['custom_date_bool']:
        initial_date = check_input_date(ael_dict['custom_date'])
    else:
        initial_date = DATE_TODAY

    business_days_expiry = ael_dict['days_to_expiry']

    pswap_issues = PswapsIssues(initial_date, business_days_expiry)
    pswaps_expiries = pswap_issues.find_expiring_pswaps()

    pswaps_text_object = NotificationTextObject(TEXT_OBJECT_NAME.format(initial_date.replace('-', '_')),
                                                pswaps_expiries)
    resolved_issues = pswaps_text_object.update_text_object()

    issue_collection = add_issue_status(resolved_issues, pswaps_expiries)

    if ael_dict['send_email'] and issue_collection:
        LOGGER.info('Sending email')
        header_table = ('Oid', 'Pswap name', 'Expiry date', 'Issue status')
        pswaps_expiry_report = PortfolioExpiryReport(header_table, issue_collection, initial_date, business_days_expiry)
        try:
            pswaps_expiry_report.send_mail('Portfolio Swap Expiry', ael_dict['email_destinations'])
        except Exception as err:
            LOGGER.error('Failed to send email notification: {}'.format(err))
        else:
            LOGGER.info('Email sent')
    else:
        LOGGER.info('Portfolio swap expiry checked.')
