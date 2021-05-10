"""A module to check loan account.

Make sure sweeper ran correctly for the loan accounts:
the correct cash flow and time series were created.

Send email notification if cash flow does not match the
time series difference between the two days, or if either
of the postings are missing.

Date         JIRA         Developer             Change
==========   =========    ====================  ==================================
2019-12-04   FAPE-144     Iryna Shcherbina      Initial development
2019-12-11   FAPE-169     Tibor Reiss           Rename to follow naming convention
                                                Also see errors from imports
"""
from itertools import tee

import acm

from PS_CashReconReport import date_range, get_client_list
from PS_FormUtils import DateField
from PS_Functions import get_pb_reporting_portfolio, get_pb_fund_counterparty
from PS_LoanAccountSweeper import PRECISION_MIN
from at_ael_variables import AelVariableHandler
from at_logging import getLogger, bp_start, get_buffering_smtp_variables


LOGGER = getLogger()
START_DATES = DateField.get_captions([
    'Last of Previous Year',
    'Last of Previous Month',
    'PrevBusDay',
    'Custom Date'])
END_DATES = DateField.get_captions([
    'PrevBusDay',
    'Now',
    'Custom Date'])
ael_variables = AelVariableHandler()
ael_variables.add(
    'clients',
    label='Clients',
    alt='List of clients (leave blank for all)',
    multiple=True,
    mandatory=False
)
ael_variables.add(
    'start_date',
    label='Start Date',
    default='PrevBusDay',
    collection=START_DATES,
    alt='Start date of the check',
)
ael_variables.add(
    'start_date_custom',
    label='Start Date Custom',
    default=DateField.read_date('PrevBusDay'),
    alt='Custom start date of the check',
)
ael_variables.add(
    'end_date',
    label='End Date',
    default='PrevBusDay',
    collection=END_DATES,
    alt='End date of the check',
)
ael_variables.add(
    'end_date_custom',
    label='End Date Custom',
    default=DateField.read_date('PrevBusDay'),
    alt='Custom end date of the check',
)
ael_variables = ael_variables + get_buffering_smtp_variables()


def pairs(seq):
    """Return the seq as pairs of values.
    Example: [1,2,3] -> [(1,2), (2,3), (3,4)]
    """
    iterable, copied = tee(seq)
    next(copied)
    for x, y in zip(iterable, copied):
        yield x, y


def days_between(first_day, last_day, include_start=False, include_end=False):
    # date_range includes first day+1 to last date.
    between = date_range(first_day, last_day)[:-1]
    if include_start:
        between.insert(0, first_day)
    if include_end:
        between.append(last_day)
    return between


class LoanAccountChecker(object):

    def __init__(self, fund, start_date, end_date):
        self.fund = fund
        self.start_date = start_date
        self.end_date = end_date

        counter_party = get_pb_fund_counterparty(fund)
        self.portfolio = get_pb_reporting_portfolio(counter_party)
        self.loan_account_name = counter_party.add_info('PB_Loan_Account')
        self.spec_name = '{}_PnL'.format(self.portfolio.Name())[0:19]
        self.loan_leg = self.get_loan_leg()
        self.time_series = self.get_time_series()
        self.client_start = self.get_client_start_date()

        self.errors = []

    def get_loan_leg(self):
        loan_account = acm.FDeposit[self.loan_account_name]
        return loan_account.Legs()[0]

    def get_time_series(self):
        time_series_spec = acm.FTimeSeriesSpec[self.spec_name]
        if time_series_spec:
            time_series = acm.FTimeSeries.Select(
                "recaddr={} and timeSeriesSpec={}".format(
                    self.portfolio.Oid(), time_series_spec.Oid()))
            return sorted(time_series, key=lambda value: value.Day())
        return []

    def get_client_start_date(self):
        first_cf = self.get_first_tpl_cash_flow_date()
        first_ts = self.get_first_time_series_date()

        return (
            min(first_cf, first_ts)  # earlier date
            or (first_cf or first_ts)  # if one of them is None
        )

    def get_first_time_series_date(self):
        if self.time_series:
            return self.time_series[0].Day()

    def get_first_tpl_cash_flow_date(self):
        """Return the date of the first fixed amount cash flow on the loan account."""
        cash_flows = acm.FCashFlow.Select(
            'leg={} and cashFlowType="Fixed Amount"'.format(self.loan_leg.Oid()))
        if cash_flows:
            cash_flows = sorted(cash_flows, key=lambda value: value.PayDate())
            return cash_flows[0].PayDate()

    def verify_time_series(self):
        if not self.within_period():
            LOGGER.info('The client was not live during this time period')
            return

        if self.after_start():
            LOGGER.info('The client started on %s, using it as start date',
                        self.client_start)
            self.start_date = self.client_start

        time_series = list(self.get_time_series_for_period())
        if not time_series:
            # The client started, we should have some time series and cash flows.
            self.check_missing_days(days_between(
                self.start_date, self.end_date,
                include_start=True, include_end=True))
            return

        self.check_start(time_series)
        for prev_series, series in pairs(time_series):
            prev_series_value = prev_series.TimeValue()
            series_value = series.TimeValue()

            dates_between = days_between(prev_series.Day(), series.Day())
            self.check_missing_days(dates_between)

            if dates_between:
                prev_series_value = 0

            # Time series difference should match the cash flow amount.
            series_diff = prev_series_value - series_value
            self.check_cashflow(series.Day(), series_diff)
        self.check_end(time_series)

    def within_period(self):
        return (
            self.client_start and
            self.client_start <= self.end_date)

    def after_start(self):
        return self.start_date < self.client_start

    def get_time_series_for_period(self):
        for time_series in self.time_series:
            if self.start_date <= time_series.Day() <= self.end_date:
                yield time_series

    def check_missing_days(self, missing_ts_dates):
        """Check if there is a cash flow for each day we do not
        have a time series entry supplied as missing_ts_dates.
        """
        for day in missing_ts_dates:
            self.errors.append(
                '{}: Missing inception TPL value on {} time '
                'series'.format(day, self.spec_name))
            loan_tpl = self.get_loan_account_tpl(day)
            if loan_tpl is None:
                self.errors.append(
                    '{}: Daily TPL was not posted to the loan '
                    'account {}'.format(day, self.loan_account_name))
            else:
                self.errors.append(
                    '{}: Daily TPL ({}) was posted to the loan account {},'
                    ' although the time series value is missing'.format(
                        day, loan_tpl, self.loan_account_name))

    def get_loan_account_tpl(self, run_date):
        """Return the TPL amount posted to the loan account for the run_date."""
        cash_flows = acm.FCashFlow.Select(
            'leg={} and payDate="{}" and cashFlowType='
            '"Fixed Amount"'.format(self.loan_leg.Oid(), run_date))
        if cash_flows:
            return sum([cf.FixedAmount() for cf in cash_flows])

    def check_start(self, time_series):
        first_ts_day = time_series[0].Day()
        if first_ts_day > self.start_date:
            self.check_missing_days(days_between(
                self.start_date, first_ts_day, include_start=True))

    def check_cashflow(self, date, amount):
        """The daily TPL posting to the loan account should be equal
        to the time series difference between the two days."""
        if not round(amount, PRECISION_MIN):
            # We do not post amounts that small.
            return

        loan_tpl = self.get_loan_account_tpl(date)
        if loan_tpl is None:
            self.errors.append(
                '{}: The daily TPL ({}) was not posted to the loan '
                'account {}'.format(date, amount, self.loan_account_name))
            return

        if round(amount) != round(loan_tpl):
            self.errors.append(
                '{}: The inception TPL difference on the time series {} '
                'and the daily TPL posted to the loan account {} do not match:'
                ' {} vs {}'.format(
                    date, self.spec_name, self.loan_account_name,
                    amount, loan_tpl))

    def check_end(self, time_series):
        last_ts_day = time_series[-1].Day()
        if self.client_start <= last_ts_day < self.end_date:
            self.check_missing_days(days_between(
                last_ts_day, self.end_date, include_end=True))


def check_loan_accounts(config):
    if config['end_date'] == 'Custom Date':
        end_date = config['end_date_custom']
    else:
        end_date = DateField.read_date(config['end_date'])

    if config['start_date'] == 'Custom Date':
        start_date = config['start_date_custom']
    else:
        start_date = DateField.read_date(config['start_date'])

    for fund in config['clients'] or get_client_list():
        LOGGER.info('Checking %s', fund)
        checker = LoanAccountChecker(fund, start_date, end_date)
        checker.verify_time_series()
        if checker.errors:
            LOGGER.critical('%s:\n' + '\n'.join(checker.errors), fund)


def ael_main(config):
    LOGGER.msg_tracker.reset()
    with bp_start('ps.loan_check', ael_main_args=config):
        check_loan_accounts(config)

        if LOGGER.msg_tracker.errors_counter:
            LOGGER.error("ERRORS occurred. Please check the log.")
        else:
            LOGGER.info("Completed Successfully")
