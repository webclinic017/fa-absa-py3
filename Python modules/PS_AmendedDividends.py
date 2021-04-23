"""-----------------------------------------------------------------------------
Sends notification if some of the dividends have been updated after the creation.

It is possible to change the initial date and check the dividend
amendments from the past. Also the backdated dividends
(Created after Ex Div Day) can be checked.

HISTORY
================================================================================
Date            Change no      Developer            Description
--------------------------------------------------------------------------------
2021-02-16      FAPE-507       Katerina Frickova    Initial implementation

--------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import to_datetime
from datetime import datetime
from PS_SendEmailNotification import CreateEmailReport
from PS_NotificationTextObject import NotificationTextObject

LOGGER = getLogger(__name__)
CURRENT_TIME = to_datetime(acm.Time.TimeNow())
DATE_TODAY = acm.Time.DateToday()
TEXT_OBJECT_NAME = 'PS_Amended_Dividends_{}'


def custom_date_hook(selected):
    date_custom = ael_variables.get('custom_date')
    date_custom.enabled = selected.value
    date_custom.mandatory = selected.value


def send_email_hook(selected):
    email_destination = ael_variables.get('email_destinations')
    email_destination.enabled = selected.value
    email_destination.mandatory = selected.value


ael_variables = AelVariableHandler()

ael_variables.add_bool(
    'backdated_bool',
    label='Show backdated dividends',
    default=True,
    alt='Show in the report also dividends which were created after the Ex Div Day.',
)

ael_variables.add_bool(
    'custom_date_bool',
    label='Choose custom Create Date',
    default=False,
    alt='Choose date to see dividends created in the past.',
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
    label='Email Destinations',
    mandatory=True,
    alt='Email Destinations - Comma Separated'
)


class UpdatedDividendsReport(CreateEmailReport):

    def __init__(self, table_header_tuple, table_rows_list, date):
        super(UpdatedDividendsReport, self).__init__(table_header_tuple, table_rows_list)
        self.date = date

    def to_html_description(self):
        return 'Amended Dividends Notification from {current_time}.<br><br>The following dividends were either changed\
                after their creation or created after the Ex Div Day.\
                Both cases can cause valuation differences.<br><small style="color:Tomato;">\
                Dates highlighted in red show the difference in Create day and Ex Div Day.\
                </small><br><br><br>'.format(current_time=self.date)


def check_input_date(date):
    try:
        datetime_output = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        return datetime_output
    except ValueError as ve:
        LOGGER.error('Incorrect date format, should be YYYY-MM-DD.')
        raise ve


class DividendIssues(object):
    """ A class to find the issues in dividends. """

    def __init__(self, date):
        self.dividends_for_date = []
        self.backdated_list = []
        self.updated_list = []
        self.date = date

    def get_dividends_for_specific_date(self):
        all_dividends = acm.FDividend.Select('')

        for dividend in all_dividends:
            if dividend.CreateDay() == self.date or dividend.UpdateDay() == self.date:
                self.dividends_for_date.append(dividend)

        return self.dividends_for_date

    def get_updated_dividends(self):
        self.get_dividends_for_specific_date()

        for dividend in self.dividends_for_date:
            update_time = dividend.ReadProperty('UpdateTime')
            create_time = dividend.ReadProperty('CreateTime')

            if to_datetime(update_time) > to_datetime(create_time):
                self.updated_list.append(dividend)
                LOGGER.info("Amended dividend found for Instrument {instrument}.".format(
                    instrument=dividend.Instrument().Name()))

        return self.updated_list

    def get_backdated_dividends(self):

        for dividend in self.dividends_for_date:
            create_time = dividend.ReadProperty('CreateTime')
            ex_div_day = dividend.ReadProperty('ExDivDay')

            if to_datetime(ex_div_day) < to_datetime(create_time):
                LOGGER.info("Dividend for instrument {} was created on {} which is after the Ex Div Day date {}."
                            .format(dividend.Instrument().Name(), create_time, ex_div_day))
                self.backdated_list.append(dividend)

        return self.backdated_list

    def get_dividends_text_object(self):
        """Collect info about dividend issues and store it in the specified format into the text object."""

        dividend_issues_dict = {str(div.Oid()): (
            div.Oid(), div.Instrument().Name(), div.ReadProperty('CreateTime'), div.ReadProperty('UpdateTime'),
            div.ExDivDay(), div.PayDay(), div.RecordDay(), div.Currency().Name()) for div in
            set(self.updated_list + self.backdated_list)}
        return dividend_issues_dict

    def concatenate_all_dividend_issues(self, resolved_issues):
        dividends_collection = []
        intersection = set(self.updated_list).intersection(self.backdated_list)
        updated_minus_backdated = set(self.updated_list) - intersection

        for div in updated_minus_backdated:
            dividends_collection.append(
                (div.Oid(), div.Instrument().Name(), div.ReadProperty('CreateTime'), div.ReadProperty('UpdateTime'),
                 div.ExDivDay(), div.PayDay(), div.RecordDay(), div.Currency().Name(),
                 '<i style="color:#FF0000">unresolved</i>'))

        for div in self.backdated_list:
            dividends_collection.append((div.Oid(), div.Instrument().Name(),
                                         '<i style="color:Tomato;">{}</i>'.format(div.ReadProperty('CreateTime')),
                                         div.ReadProperty('UpdateTime'), '<i style="color:Tomato;">{}</i>'
                                         .format(div.ExDivDay()), div.PayDay(), div.RecordDay(), div.Currency().Name(),
                                         '<i style="color:#FF0000">unresolved</i>'))

        if resolved_issues:
            for oid, issue in list(resolved_issues.items()):
                issue.append('<i style="color:#228B22">resolved</i>')
                tuple_issue = tuple(issue)
                dividends_collection.append(tuple_issue)

        return dividends_collection


def ael_main(ael_dict):
    if ael_dict['custom_date_bool']:
        date = check_input_date(ael_dict['custom_date'])
    else:
        date = to_datetime(DATE_TODAY).strftime("%Y-%m-%d")

    dividend = DividendIssues(date)
    dividend.get_updated_dividends()

    if ael_dict['backdated_bool']:
        dividend.get_backdated_dividends()

    dividend_text_object = NotificationTextObject(TEXT_OBJECT_NAME.format(date.replace('-', '_')),
                                                  dividend.get_dividends_text_object())
    resolved_issues = dividend_text_object.update_text_object()

    dividends_to_report = dividend.concatenate_all_dividend_issues(resolved_issues)

    if ael_dict['send_email'] and dividends_to_report:
        LOGGER.info('Sending email')
        header_table = (
            'Oid', 'Instrument Name', 'Create Time', 'Update Time', 'Ex Div Day', 'Pay Day', 'Record Day', 'Currency',
            'Issue status')
        updated_dividends_report = UpdatedDividendsReport(header_table, dividends_to_report, date)
        try:
            updated_dividends_report.send_mail('Amended Dividends', ael_dict['email_destinations'])
        except Exception as err:
            LOGGER.error('Failed to send email notification: {}'.format(err))
        else:
            LOGGER.info('Email sent')
    else:
        LOGGER.info('Amended dividends check done.')
