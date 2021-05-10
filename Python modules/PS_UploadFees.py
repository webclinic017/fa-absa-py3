"""-----------------------------------------------------------------------
MODULE
    PS_UploadFees

DESCRIPTION
    Date                : 2011-07-01
    Purpose             : Uploads the SAFEX prices from a flat file from GCMS.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 699989

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------
2011-07-01 699989               Herman Hoon        Initial Implementation
2014-11-20 2450799              Frantisek Jahoda   Refactor to use at_concepts
2015-02-27 2673238              Jakub Tomaga       Print warnings instead of
                                                   errors and add "completed
                                                   successfully"
2015-09-11 3090331              Jakub Tomaga       Portfolio independent sweeping
2019-06-06 CHG1001820029        Jakub Tomaga       Add allocation commission as
                                                   a pass through to the client
2020-01-14 FAPE-187             Iryna Shcherbina   Ignore rows with blank fees
ENDDESCRIPTION
-----------------------------------------------------------------------"""
from csv import DictReader
from os.path import join, realpath

import acm
import ael
from at_addInfo import save as save_add_info
from at_ael_variables import AelVariableHandler
from at_logging import bp_start, getLogger
from at_logging_handlers import BufferingSMTPHandler
from PS_Functions import get_trades
from PS_TradeFees import _GetVATFactor

LOGGER = getLogger(__name__)


class InvalidFileFormat(Exception):
    pass


def _add_allocation_commission_as_payment(trade, amount):
    trade_date = trade.TradeTime().split(" ")[0]
    payment = acm.FPayment()
    payment.Trade(trade)
    payment.Currency(trade.Instrument().Currency())
    payment.Type("Cash")
    payment.Party(acm.FParty["PRIME SERVICES DESK"])
    payment.Amount(amount)
    payment.PayDay(trade_date)
    payment.ValidFrom(trade_date)
    payment.Commit()


def _load_fees(input_file):
    LOGGER.info('Reading fees from the input file "%s".',
                realpath(input_file.name))
    fees = {}
    dict_reader = DictReader(input_file)
    for row in dict_reader:
        jseref = row['JSEReference']
        try:
            exchange_fee = -float(row['NettExchangeFeeExVAT'])
            clearing_fee = -float(row['NettClearingMemberFeeExVat'])
            commission_fee = -float(row['NettCommissionExVAT'])
        except ValueError:
            LOGGER.error(
                'Failed to convert the fee value to float on line %d',
                dict_reader.line_num)
            raise RuntimeError(
                'Errors occurred when loading the fees, aborting. '
                'No fees will be uploaded. Please check the file data '
                'and rerun the task.'
            )

        if jseref in fees:
            LOGGER.warning('Duplicate record for JSE reference "%s" '
                           'on line %d.',
                           jseref,
                           dict_reader.line_num)
        else:
            fees[jseref] = exchange_fee, clearing_fee, commission_fee
    LOGGER.info('All the fees have been read successfully.')
    return fees


def _set_trade_fees(trades, fees, date_string):
    for trade in trades:
        jseref = trade.Text1()
        if acm.Time().AsDate(trade.TradeTime()) == date_string and jseref != '':
            if jseref not in fees:
                LOGGER.warning('No fees for trade %s '
                               'with JSE Reference: %s on %s',
                               trade.Oid(),
                               jseref,
                               date_string)
                continue

            exchange_fee, clearing_fee, commission_fee = fees[jseref]
            save_add_info(trade, 'PS_ExchangeFee', exchange_fee)
            save_add_info(trade, 'PS_ClearingFee', clearing_fee)
            save_add_info(trade, 'PS_CommissionFee', commission_fee)

            vat_factor = _GetVATFactor(trade)
            _add_allocation_commission_as_payment(trade, commission_fee * vat_factor)


def get_start_day_config():
    """Generate date lists to be used as drop downs in the GUI."""
    today = acm.Time().DateToday()
    calendar = acm.FCalendar['ZAR Johannesburg']
    time = acm.Time()
    return {
        'Inception': time.DateFromYMD(1970, 1, 1),
        'First Of Year': time.FirstDayOfYear(today),
        'First Of Month': time.FirstDayOfMonth(today),
        'PrevBusDay': calendar.AdjustBankingDays(today, -1),
        'TwoBusinessDaysAgo': calendar.AdjustBankingDays(today, -2),
        'TwoDaysAgo': time.DateAddDelta(today, 0, 0, -2),
        'Yesterday': time.DateAddDelta(today, 0, 0, -1),
        'Custom Date': today,
        'Now': today,
    }


def enable_custom_start_date(date):
    """
    If the supplied ael_variable ('date') has a value 'Custom Date',
    enable the ael_variable 'dateCustom'.
    Otherwise disable it.
    """
    custom_date = date.handler.get('dateCustom')
    custom_date.enabled = (date.value == 'Custom Date')


def get_ael_variables():
    today = acm.Time().DateToday()
    variables = AelVariableHandler()
    variables.add('date',
                  label='Date',
                  collection=sorted(get_start_day_config().keys()),
                  default='Now',
                  alt='Date for which the fees file will be loaded.',
                  hook=enable_custom_start_date)
    variables.add('dateCustom',
                  label='Date Custom',
                  cls='date',
                  default=today,
                  mandatory=False,
                  alt='Custom date',
                  enabled=False)
    variables.add('fileName',
                  label='File name',
                  default='DealFees_',
                  alt='File name prefix. '
                      'Will be followed by a date in the YYYYMMDD form '
                      'and a .csv extension.')
    variables.add_directory('filePath',
                            label='Directory',
                            default='/apps/frontnt/REPORTS/'
                                    'BackOffice/Atlas-End-Of-Day/'
                                    'PrimeServices',
                            alt='Directory where the fees file '
                                'will be looked for. '
                                'A date subfolder in the form '
                                'yyyy-mm-dd will be automatically added.')
    variables.add('emails',
                  label='E-mail list',
                  alt='Comma-delimited list of e-mails '
                      'where the task log will be sent.',
                  mandatory=False,
                  tab='Logging')
    return variables


ael_variables = get_ael_variables()


def ael_main(dictionary):
    LOGGER.msg_tracker.reset()
    with bp_start('ps_upload_fees', ael_main_args=dictionary):

        if dictionary['emails']:
            emails = dictionary['emails'].split(',')
            handler = BufferingSMTPHandler(
                emails,
                subject='Script "{0}" failed to complete'.format(__name__))
            LOGGER.addHandler(handler)

        if dictionary['date'] == 'Custom Date':
            ael_date = dictionary['dateCustom']
            date_string = ael_date.to_string(ael.DATE_ISO)
        else:
            date_string = get_start_day_config()[dictionary['date']]

        directory = dictionary['filePath'].SelectedDirectory().Text()
        filename = dictionary['fileName']
        filename_date = date_string.replace('-', '')
        filename += filename_date + '.csv'
        filepath = join(directory, date_string, filename)

        with open(filepath, 'r') as input_file:
            fees = _load_fees(input_file)

        safex_trades = get_trades('SAFEX exchange', 'PB_CR_LIVE')
        yieldx_trades = get_trades('YieldX exchange', 'PB_CR_LIVE')
        commodity_trades = get_trades('Commodities', 'PB_CR_LIVE')
        trades = safex_trades + yieldx_trades + commodity_trades
        _set_trade_fees(trades, fees, date_string)

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')

    LOGGER.info('Completed successfully.')
