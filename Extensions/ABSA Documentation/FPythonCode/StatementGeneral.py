"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    StatementGeneral

DESCRIPTION
    This module contains general functionality shared by all statements.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation
2018-08-01                      Cuen Edwards                                    Refactored some functionality out to DocumentGeneral.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime
import re

import acm
import ael

import DocumentConfirmationGeneral
import DocumentGeneral


class Month(object):
    """
    An object representing a calendar month.
    """

    @staticmethod
    def parse_month(month_string):
        """
        Parse a month represented as a string to a month object.
        """
        if month_string.strip().lower() == 'previous':
            previous_month = ael.date_today().add_months(-1)
            month_string = previous_month.to_string('%Y/%m')
        return Month(month_string)

    def __init__(self, month_string):
        """
        Constructor.

        Takes a month represented as a string in the form YYYY/MM
        (e.g. 2018/01).
        """
        self._date_time = self._parse_as_datetime(month_string)

    @property
    def year(self):
        """
        Get the year portion of the calendar month as an integer.
        """
        return self._date_time.year

    @property
    def month(self):
        """
        Get the month portion of the calendar month as an integer.
        """
        return self._date_time.month

    def get_first_day_of_month(self):
        """
        Get the first day of the month as an ACM date string.
        """
        return acm.Time.FirstDayOfMonth(self._date_time.strftime('%Y-%m-%d'))

    def get_last_day_of_month(self):
        """
        Get the last day of the month as an ACM date string.
        """
        days_in_month = acm.Time.DaysInMonth(self.get_first_day_of_month())
        return acm.Time.DateFromYMD(self.year, self.month, days_in_month)

    def __str__(self):
        """
        Get the month as a string.
        """
        return self._date_time.strftime('%Y/%m')

    @staticmethod
    def _parse_as_datetime(month_string):
        """
        Parse a month represented as a string to a Python datetime
        object.
        """
        try:
            pattern = r'\D'
            separator_matches = re.findall(pattern, month_string)
            if len(separator_matches) > 1:
                raise ValueError('More than one date separator found.')
            unformatted_month_string = re.sub(pattern, '', month_string.strip())
            date_time = datetime.datetime.strptime(unformatted_month_string, '%Y%m')
            return date_time
        except ValueError:
            raise ValueError("Invalid month '{month_string}' specified.".format(
                month_string=month_string
            ))


def get_recreate_statement_operation_name():
    """
    Get the name of the operation used to control access to
    the recreation of a statement (the generation of a statement
    with the same criteria as an existing statement).
    """
    return 'Recreate Statement'


def statement_confirmation_exists(statement_event_name, acquirer, counterparty,
        from_date, to_date, document_schedule):
    """
    Determine if a statement confirmation exists for the specified
    statement event name, acquirer, counterparty, inclusive statement
    from date and inclusive statement to date.
    """
    return len(DocumentConfirmationGeneral.get_existing_document_confirmations(statement_event_name,
        acquirer, counterparty, from_date, to_date, document_schedule)) > 0


def validate_statement_date_range(from_date, to_date):
    """
    Validate a statement date range.
    """
    document_name = 'statement'
    DocumentGeneral.validate_document_date_range(document_name, from_date, to_date)
    # Only permit creation of statements up to two years back.
    date_today = acm.Time.DateToday()
    first_of_month = acm.Time.FirstDayOfMonth(date_today)
    first_of_month_two_years_back = acm.Time.DateAddDelta(first_of_month, -2, 0, 0)
    if from_date < first_of_month_two_years_back:
        raise ValueError('A statement from date may not be further than two years back.')
    # Only permit creation of statements for completed days.
    if to_date >= date_today:
        raise ValueError('A statement to date must be before today.')
