"""----------------------------------------------------------------------------
MODULE      PS_FormUtils

Read/validate values from Task forms.

History:
Date        CR Number   Who               What

2012-11-13  620753      Hynek Urban       Initial version.
2014-05-27  TODO        Jakub Tomaga      'First Of Month' and 'First Of Year'
                                          adjusted to next banking day if
                                          necessary.
11-12-2014  2512804     Jakub Tomaga      Option for 'Last of Previous Month'
                                          added.
22-01-2015  2587956     Jakub Tomaga      Option to specify today's date added.
----------------------------------------------------------------------------"""

import acm


class DateField(object):
    """Class for working with user-provided dates."""

    @staticmethod
    def _mapping(today=acm.Time.DateToday()):
        """Build the mapping dynamically upon each call to avoid aging."""
        calendar = acm.FCalendar['ZAR Johannesburg']

        first_of_year = acm.Time.FirstDayOfYear(today)
        if calendar.IsNonBankingDay(None, None, first_of_year):
            first_of_year = calendar.AdjustBankingDays(first_of_year, 1)

        first_of_month = acm.Time.FirstDayOfMonth(today)
        if calendar.IsNonBankingDay(None, None, first_of_month):
            first_of_month = calendar.AdjustBankingDays(first_of_month, 1)

        last_of_prev_month = calendar.AdjustBankingDays(
            acm.Time.FirstDayOfMonth(today), -1)

        last_of_prev_year = calendar.AdjustBankingDays(
            acm.Time.FirstDayOfYear(today), -1)

        return {
            'Inception': acm.Time.DateFromYMD(1970, 1, 1),
            'First Of Year': first_of_year,
            'Last of Previous Year': last_of_prev_year,
            'First Of Month': first_of_month,
            'Last of Previous Month': last_of_prev_month,
            'PrevBusDay': calendar.AdjustBankingDays(today, -1),
            'TwoBusinessDaysAgo': calendar.AdjustBankingDays(today, -2),
            'TwoDaysAgo': acm.Time.DateAddDelta(today, 0, 0, -2),
            'Yesterday': acm.Time.DateAddDelta(today, 0, 0, -1),
            'Custom Date': today,
            'Now': today,
        }

    @classmethod
    def get_captions(cls, caption_list):
        """Validate and sort the given caption list."""
        mapping = cls._mapping()
        if not all(c in mapping for c in caption_list):
            raise ValueError('Unknown caption(s) in: %r' % caption_list)
        return sorted(caption_list)

    @classmethod
    def read_date(cls, date, today=acm.Time.DateToday(), default=None):
        """Convert user input to standard string-based date representation."""
        mapping = cls._mapping(today)
        if date in mapping:
            return mapping[date]
        elif date == "":
            cal = acm.FCalendar['ZAR Johannesburg']
            return default or cal.AdjustBankingDays(acm.Time.DateToday(), -1)
        else:
            return date
