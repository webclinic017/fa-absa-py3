import os
from collections import OrderedDict, namedtuple
from datetime import datetime

import acm
import xlsxwriter

from at_ael_variables import AelVariableHandler
from at_email import EmailHelper
from at_logging import getLogger
from HedgeConstants import STR_LAST_PRICE_MARKET, STR_MTM_PRICE_MARKET

LOGGER = getLogger(__name__)
ZAR_CALENDAR = acm.FCalendar['ZAR Johannesburg']
DATE_TODAY = acm.Time().DateToday()
PREVDAY = ZAR_CALENDAR.AdjustBankingDays(DATE_TODAY, -1)

# xlsx colors
RED = '#E6B8B7'
BLUE = '#8DB4E2'
GREEN = '#92D050'
YELLOW = '#FFFF66'
AQUA = '#92CDDC'
ORANGE = '#FFC000'
PURPLE = '#B1A0C7'


class _RowsBlock(object):
    xlsx_columns = ('Instrument', 'COB_Price', 'SOB_Price', 'Difference', 'Market')
    xlsx_title = None
    xlsx_color = None
    _market = None
    _default_price = 0.0

    Row = namedtuple('Row', 'name, data')

    def __init__(self):
        self.rows = []

    def add_row(self, item):
        raise NotImplementedError()

    def get_rows(self):
        return self.rows


class _CurrencyBlock(_RowsBlock):
    xlsx_color = YELLOW
    xlsx_title = 'FX'
    _market = xlsx_title

    def __init__(self):
        super(_CurrencyBlock, self).__init__()
        usd_zar = acm.FCurrencyPair['USD/ZAR']
        self.FX_r_n = (self._get_cob_price(usd_zar), self._get_sob_price(usd_zar))

    def add_row(self, item):
        if item.Name() == 'USD/ZAR':
            cob_price, sob_price = self.FX_r_n
        else:
            cob_price = self._get_cob_price(item) * self.FX_r_n[0]
            sob_price = self._get_sob_price(item) * self.FX_r_n[1]
        self.rows.append(self.Row(
            name=item.Currency1().Name() + 'ZAR',
            data=[cob_price,
                  sob_price,
                  (cob_price / sob_price - 1) * 100,
                  self._market]
        ))

    def _get_cob_price(self, pair):
        prices = pair.Currency1().Prices().Filter(
            lambda price:
                price.Currency().Name() == pair.Currency2().Name() and
                price.Market().Name() == STR_LAST_PRICE_MARKET)
        if prices:
            return prices[0].Last()
        return self._default_price

    def _get_sob_price(self, pair):
        prices = pair.Currency1().HistoricalPrices().Filter(
            lambda price:
                price.Currency().Name() == pair.Currency2().Name() and
                price.Day() == PREVDAY and
                price.Market().Name() == STR_MTM_PRICE_MARKET)
        if prices:
            return prices[0].Settle()
        return self._default_price


class _CurveBlock(_RowsBlock):
    xlsx_color = YELLOW
    _periods = ["1y", "2y", "5y", "7y", "10y", "15y"]

    def add_rows_for(self, curve):
        day_count = "Act/365"
        rate_type = "Annual Comp"

        for period in self._periods:
            period_years = int(period.replace("y", ""))
            to_date = acm.Time.DateAddDelta(DATE_TODAY, period_years, 0, 0)
            rate = curve.Rate(DATE_TODAY, to_date, rate_type, day_count)
            self.rows.append(self.Row(
                name=period,
                data=[rate * 100]))


class _InstrumentBlock(_RowsBlock):

    def add_row(self, item):
        cob_price = self._get_cob_price(item)
        sob_price = self._get_sob_price(item)
        self.rows.append(self.Row(
            name=self._get_name(item),
            data=[cob_price,
                  sob_price,
                  cob_price - sob_price,
                  self._market]
        ))

    def _get_name(self, item):
        return item.Name()

    def _get_cob_price(self, instrument):
        prices = instrument.Prices().Filter(
            lambda price: price.Market().Name() == STR_LAST_PRICE_MARKET)
        if prices:
            return prices[0].Settle()
        return self._default_price

    def _get_sob_price(self, instrument):
        prices = instrument.HistoricalPrices().Filter(
            lambda price:
                price.Market().Name() == STR_LAST_PRICE_MARKET and
                price.Day() == PREVDAY)
        if prices:
            return prices[0].Settle()
        return self._default_price


class _BondBlock(_InstrumentBlock):
    xlsx_title = 'Bond'
    xlsx_color = RED
    _market = xlsx_title


class _IndexLinkedBondBlock(_InstrumentBlock):
    xlsx_title = 'InflBond'
    xlsx_color = BLUE
    _market = xlsx_title


class _RateIndexBlock(_InstrumentBlock):
    xlsx_title = 'Money Market'
    xlsx_color = GREEN
    _market = xlsx_title

    _pretty_names = {
        'ZAR-JIBAR-ON-DEP': 'O/N',
        'ZAR-JIBAR-1M': '1 Mnth',
        'ZAR-JIBAR-3M': '3 Mnth',
        'ZAR-JIBAR-6M': '6 Mnth',
        'ZAR-JIBAR-12M': '1 Year',
    }

    def _get_name(self, item):
        return self._pretty_names.get(item.Name(), item.Name())

    def get_rows(self):
        order = ('O/N', '1 Mnth', '3 Mnth', '6 Mnth', '1 Year')
        return sorted(self.rows, key=lambda row: order.index(row.name))


class _OTCBlock(_InstrumentBlock):
    xlsx_columns = ('Instrument', 'COB_Price', 'SOB_Price', 'Diff', '')


class _FraBlock(_OTCBlock):
    xlsx_title = 'FRA'
    xlsx_color = AQUA


class _SwapBlock(_OTCBlock):
    xlsx_title = 'Swaps'
    xlsx_color = ORANGE


class _IndexLinkedSwapBlock(_OTCBlock):
    xlsx_title = 'Inflation Linked Swaps'
    xlsx_color = PURPLE


class MarketPriceXLSXReport(object):
    _number_format = {
        'num_format': '#,##0.0000',
    }
    _general_format = {
        'border': 1,
    }
    _title_format = {
        'bold': True,
        'num_format': '@',
    }
    _email_info = {
        'subject': 'EOD Rates {}'.format(DATE_TODAY),
        'body': ''
    }

    _blocks = OrderedDict((
        ('Bond', _BondBlock()),
        ('IndexLinkedBond', _IndexLinkedBondBlock()),
        ('RateIndex', _RateIndexBlock()),
        ('FX', _CurrencyBlock()),
        ('Curve', _CurveBlock()),
        ('FRA', _FraBlock()),
        ('Swap', _SwapBlock()),
        ('IndexLinkedSwap', _IndexLinkedSwapBlock())
    ))

    def __init__(self, output_file):
        self.output_file = output_file
        self._workbook = xlsxwriter.Workbook(self.output_file)
        self._worksheet = None
        self._first_row = 0
        self._first_col = 0
        # Worksheet formats
        self._title = None
        self._general = None
        self._number = None

    @property
    def _next_row(self):
        return self._worksheet.dim_rowmax + 1

    def create(self, instruments, currencies, curve):
        self._setup_worksheet()
        self._setup_instrument_blocks(instruments)
        self._setup_currency_block(currencies)
        self._setup_curve_block(curve)

        self._add_date()
        for block in list(self._blocks.values()):
            self._add_instrument_block(block)

        self._format_worksheet()
        self._workbook.close()

    def clear_blocks(self):
        for block in list(self._blocks.values()):
            block.rows = []

    def send_mail(self, email_to):
        message = EmailHelper(
            mail_to=email_to.split(','),
            attachments=[self.output_file],
            sender_type=EmailHelper.SENDER_TYPE_SMTP,
            host=EmailHelper.get_acm_host(),
            **self._email_info)
        message.send()

    def _setup_worksheet(self):
        self._worksheet = self._workbook.add_worksheet()
        self._title = self._workbook.add_format(self._title_format)
        self._general = self._workbook.add_format(self._general_format)
        self._number = self._workbook.add_format(self._number_format)
        self._worksheet.set_column(0, 0, 30)  # name
        self._worksheet.set_column(1, 3, 12, self._number)  # cob price, sob_price, diff
        self._worksheet.set_column(4, 4, 14)  # market

    def _format_worksheet(self):
        for type_ in ('blanks', 'no_blanks'):
            self._worksheet.conditional_format(
                'A1:E{}'.format(self._next_row),
                {'type': type_, 'format': self._general})

    def _setup_instrument_blocks(self, instruments):
        for instrument in instruments:
            LOGGER.info('Processing {}'.format(instrument.Name()))
            block = self._blocks.get(instrument.InsType())
            if block:
                block.add_row(instrument)
            else:
                LOGGER.warning(
                    'Instrument {} is of unsupported type {}, skipping'.format(
                        instrument.InsType(), instrument.Name()))

    def _setup_currency_block(self, currencies):
        block = self._blocks.get('FX')
        for currency_pair in currencies:
            LOGGER.info('Processing {}'.format(currency_pair.Name()))
            block.add_row(currency_pair)

    def _setup_curve_block(self, yield_curve):
        LOGGER.info('Processing {}'.format(yield_curve.Name()))
        block = self._blocks.get('Curve')
        block.add_rows_for(yield_curve)

    def _add_date(self):
        date = datetime.strptime(DATE_TODAY, '%Y-%m-%d').strftime('%d-%m-%Y')
        self._worksheet.write(self._first_row, self._first_col,
                              date, self._title)

    def _add_instrument_block(self, block):
        self._title_format['bg_color'] = block.xlsx_color
        title_format = self._workbook.add_format(self._title_format)
        if block.xlsx_title:
            self._add_title(block, title_format)
        self._add_rows(block, title_format)
        # Do not add the extra line after the last block.
        if block != list(self._blocks.values())[-1]:
            self._worksheet.write(self._next_row, self._first_col, '', title_format)

    def _add_title(self, block, title_format):
        self._worksheet.write(
            self._next_row, self._first_col, block.xlsx_title, title_format)
        self._worksheet.write_row(
            self._next_row, self._first_col, block.xlsx_columns, title_format)

    def _add_rows(self, block, title_format):
        for row in block.get_rows():
            row_num = self._next_row
            self._worksheet.write(row_num, self._first_col, row.name, title_format)
            self._worksheet.write_row(row_num, self._first_col + 1, row.data)


ael_variables = AelVariableHandler()
ael_variables.add(
    'instruments',
    label='Instruments',
    cls='FStoredASQLQuery',
    collection=acm.FStoredASQLQuery.Select("subType='FInstrument'"),
    alt='A query folder of instruments to be included in the report'
)
ael_variables.add(
    'pairs_of_currencies',
    mandatory=True,
    multiple=True,
    cls='FCurrencyPair',
    label='Currency Pairs',
    alt='Currencies for FX market'
)
ael_variables.add(
    'curve',
    mandatory=True,
    cls='FCompositeCurve',
    label='Curve',
    alt='Curve'
)
ael_variables.add(
    'email_destinations',
    mandatory=False,
    label='Email Destinations',
    alt='Email destinations - comma separated'
)
ael_variables.add(
    'filename',
    label='File',
    cls='string',
    default='MarketPriceSummary.xlsx',
    mandatory=True,
    multiple=False,
    alt='Name of the output file'
)
ael_variables.add_directory(
    'directory',
    label='Directory',
    alt='Output file path'
)


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    report = MarketPriceXLSXReport(os.path.join(
        str(ael_dict['directory'].SelectedDirectory()),
        ael_dict['filename']
    ))
    report.clear_blocks()
    report.create(
        ael_dict['instruments'].Query().Select().SortByProperty('ExpiryDate'),
        ael_dict['pairs_of_currencies'],
        ael_dict['curve']
    )
    if ael_dict['email_destinations']:
        LOGGER.info('Sending email')
        try:
            report.send_mail(ael_dict['email_destinations'])
        except Exception as err:
            LOGGER.error('Failed to send email notification: {}'.format(err))
        else:
            LOGGER.info('Email sent')

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log")

    LOGGER.info("Completed successfully")
