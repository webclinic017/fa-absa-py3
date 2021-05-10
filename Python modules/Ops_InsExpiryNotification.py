"""-----------------------------------------------------------------------------
PURPOSE                 :  This script will evaluate all instruments contained
                           within a specified compound portfolio. If there's an
                           instrument containing valid trades, expiring today or
                           within a set nr of business days, then the script will
                           send out an email notification to the specified
                           destinations as well as save down the report.
DEPATMENT AND DESK      :  AAM
REQUESTER               :  Suvarn Naidoo
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  2419446
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no       Developer            Description
--------------------------------------------------------------------------------
2014-10-30  2419446         Rohan vd Walt        Initial Implementation
2019-02-11  CHG1001378099   Iryna Shcherbina     Do not send email if no expiring
            (FAPE-37)                            instruments found; some refactoring
2019-02-26  FAPE-51         Iryna Shcherbina     Add trade portfolios' positions on
                                                 demand; switch to html body
2019-10-14  FAPE-118        Iryna Shcherbina     Ignore Void and Simulated trades
"""

from collections import defaultdict
from operator import methodcaller
from textwrap import dedent

import acm

from at import INST_DEPOSIT
from at_ael_variables import AelVariableHandler
from at_email import EmailHelper
from at_logging import getLogger
from at_time import bankingday_timediff
from PS_Functions import is_child_portf


LOGGER = getLogger(__name__)
DATE_TODAY = acm.Time.DateToday()
OPEN_END_STATUS_TEXT = 'Open End'


def email_hook(selected):
    email_destinations = ael_variables.get('email_destinations')
    email_destinations.enabled = selected.value
    email_destinations.mandatory = selected.value


ael_variables = AelVariableHandler()
ael_variables.add(
    'portfolio',
    mandatory=True,
    cls='FCompoundPortfolio',
    multiple=True,
    label='Portfolio',
    alt='Compound portfolios that should be checked for expiring instruments'
)
ael_variables.add(
    'days_to_expiry',
    mandatory=True,
    cls='int',
    label='Business Days to Expiry',
    alt='How many days before expiry should the instrument be included in the report'
)
ael_variables.add(
    'excl_ins_type',
    mandatory=False,
    multiple=True,
    label='Exclude Instrument Types',
    collection=acm.FEnumeration['enum(InsType)'].Values(),
    alt=('This will exclude the selected instrument types\n'
         'Call Accounts (Open End Deposits) will always be excluded')
)
ael_variables.add(
    'excl_trade_status',
    mandatory=False,
    multiple=True,
    label='Exclude Trade Statuses',
    collection=acm.FEnumeration['enum(TradeStatus)'].Values()
)
ael_variables.add_bool(
    'show_positions',
    label='Show Positions',
    default=False,
    alt='Include the list of trade portfolios and positions'
)
ael_variables.add_bool(
    'send_email',
    label='Send Email',
    default=True,
    hook=email_hook,
    alt='This will send email to recipients in addition to the file report'
)
ael_variables.add(
    'email_destinations',
    mandatory=True,
    label='Email Destinations',
    alt='Email Destinations - Comma Separated'
)
ael_variables.add(
    'output_location',
    mandatory=False,
    label='Report Output Location',
    alt='Location where report will be saved',
)


class ExpiryReport(object):

    SUBJECT = 'Instrument Expiry Notification - {date_today} - {env}'
    REPORT_BODY = dedent("""\
    <html>
      <head>
        <style type="text/css">p {{margin:0}}</style>
      </head>
      <body>
        <p>Instrument Expiry Notification: {date_today}<br>
        <br>
        Checking within the following portfolios:<br>
        <div style='margin-left: 4em;'>{portfolios}</div>
        <br>
        The following instruments are expiring within {business_days} business day(s):<br>
        <div style='margin-left: 4em;'>{instruments}</div>
        </p>
      </body>
    </html>
    """)
    POSITIONS = dedent("""
    <table style='padding-left: 4em;'>
      <tr>
        <td style="width: 300px;">Trades Portfolios</td>
        <td>Prime_Expiries</td>
      </tr>
      <tr>{}</tr>
    </table>
    """)

    def __init__(self, portfolios, business_days, show_positions, ignore_trades=()):
        self.instruments = set()
        self.portfolios = portfolios
        self.business_days = business_days
        self.show_positions = show_positions
        self.ignore_trade_statuses = ignore_trades

    def _sort_instruments_by(self, method):
        return sorted(self.instruments, key=methodcaller(method))

    def _positions(self, instrument):
        ratio = 1.0 / instrument.ContractSize()
        portfolio_to_position = defaultdict(float)
        for trade in instrument.Trades():
            if trade.Status() in self.ignore_trade_statuses:
                continue
            portfolio = trade.Portfolio()
            if any(is_child_portf(portfolio, parent) for parent in self.portfolios):
                portfolio_to_position[portfolio.Name()] += trade.Position() * ratio

        if any(portfolio_to_position.values()):
            return self.POSITIONS.format('</tr><tr>'.join(
                '<td>{}</td><td>{:,}</td>'.format(portfolio, pos)
                for portfolio, pos in sorted(portfolio_to_position.items()) if pos))
        else:
            return ''

    def _instrument_line(self, instrument):
        line = 'Expiring: {} - {}'.format(
            instrument.ExpiryDateOnly(),
            instrument.Name())
        if self.show_positions:
            line += self._positions(instrument)
        return line

    def add_instrument(self, instrument):
        self.instruments.add(instrument)

    def get_body(self):
        return self.REPORT_BODY.format(
            date_today=DATE_TODAY,
            business_days=self.business_days,
            portfolios='<br>'.join(portfolio.Name() for portfolio in self.portfolios),
            instruments='<br>'.join(
                self._instrument_line(instrument) for instrument in
                self._sort_instruments_by('ExpiryDateOnly')))

    def write_to_file(self, full_path):
        with open(full_path, "w+") as output_file:
            output_file.write(self.get_body())

    def send_mail(self, email_to):
        message = EmailHelper(
            body=self.get_body(),
            subject=self.SUBJECT.format(date_today=DATE_TODAY, env=get_env_name()),
            mail_to=email_to.split(','),
            sender_type=EmailHelper.SENDER_TYPE_SMTP,
            host=EmailHelper.get_acm_host())
        message.send()


def get_env_name():
    return acm.FInstallationData.Select('').At(0).Name()


def expires_within(instrument, business_days):
    expiry_date = instrument.ExpiryDate()
    if expiry_date and DATE_TODAY <= expiry_date:
        timediff = bankingday_timediff(
            instrument.Currency().Calendar(), DATE_TODAY, instrument.ExpiryDate())
        return timediff.days <= business_days
    else:
        return False


def is_valid(instrument, invalid_instypes):
    """Check if the instrument type is valid given the list of invalid types.

    Always exclude call account expires - it does not
    make sense since they will show up daily.
    """
    return not (
        instrument.InsType() in invalid_instypes or
        (instrument.InsType() == INST_DEPOSIT and
         instrument.OpenEnd() == OPEN_END_STATUS_TEXT)
    )


def collect_instruments(portfolios, exclude_trade_statuses, exclude_ins_types):
    instrument_collection = set()

    for portfolio in portfolios:
        LOGGER.info('Checking portfolio: {}'.format(portfolio.Name()))
        for trade in portfolio.Trades():
            if (trade.Status() not in exclude_trade_statuses and
                    is_valid(trade.Instrument(), exclude_ins_types)):
                instrument_collection.add(trade.Instrument())

    return instrument_collection


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    LOGGER.info('Collecting Instruments In Portfolios')
    instruments = collect_instruments(
        ael_dict['portfolio'],
        ael_dict['excl_trade_status'],
        ael_dict['excl_ins_type']
    )
    expiry_report = ExpiryReport(
        ael_dict['portfolio'],
        ael_dict['days_to_expiry'],
        ael_dict['show_positions'],
        ael_dict['excl_trade_status'],
    )

    LOGGER.info('Checking Expiry Dates')
    for instrument in instruments:
        if expires_within(instrument, ael_dict['days_to_expiry']):
            LOGGER.info('{} expires on {}'.format(
                instrument.Name(), instrument.ExpiryDateOnly()))
            expiry_report.add_instrument(instrument)

    if not expiry_report.instruments:
        LOGGER.info(
            'There are no instruments expiring within '
            '{} business day(s)'.format(ael_dict['days_to_expiry']))
        return

    if ael_dict['output_location']:
        LOGGER.info('Writing to file')
        try:
            expiry_report.write_to_file(ael_dict['output_location'])
        except (IOError, OSError) as err:
            LOGGER.error('Failed to write to file: {}'.format(err))
        else:
            LOGGER.info('Wrote to {}'.format(ael_dict['output_location']))

    if ael_dict['send_email']:
        LOGGER.info('Sending email')
        try:
            expiry_report.send_mail(ael_dict['email_destinations'])
        except Exception as err:
            LOGGER.error('Failed to send email notification: {}'.format(err))
        else:
            LOGGER.info('Email sent')

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully.")
