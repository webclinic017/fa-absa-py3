"""Equity trades uploader.

The module reads data from an xlsx file
and creates equity trades for each row in the file.
"""
from collections import OrderedDict

import acm
import xlrd

from at_feed_processing import ValidatingXLSFeedProcessor, notify_log
from at_feed_field_validators import (
    create_type_validator,
    custom_validator_function as custom,
    party_validator,
    portfolio_validator,
    instrument_validator
)
from at_logging import getLogger
from at_time import is_banking_day
from at_type_helpers import xrepr
from FTradeCreator import DecoratedTradeCreator, GetTradeKey


LOGGER = getLogger(__name__)
SIGN_MAP = {
    'buy': 1,
    'sell': -1,
}
CALENDAR = acm.FCalendar['ZAR Johannesburg']


def validate_time(value):
    try:
        value = float(value)
        date = str(xlrd.xldate.xldate_as_datetime(value, 0).date())
    except ValueError:
        date = str(value)
    if date:
        if not is_banking_day(CALENDAR, date):
            raise ValueError('{} is not a valid business day'.format(date))
        return date


def validate_nominal(value):
    if float(value) % 1:
        raise ValueError('Nominal can not be fractional, please use '
                         'a whole number. Current value: {}'.format(value))
    return int(value)


def to_numeric_string(value):
    # If the value is entered as a number in excel, it is usually
    # interpreted as float. Make sure numeric portfolios/parties/keys
    # are not converted to float.
    try:
        return str(int(value))
    except ValueError:
        return str(value)


def validate_key(value, key_name='OptKey3'):
    value = to_numeric_string(value)
    if value:
        _, key_value = GetTradeKey(key_name, value)
        if not key_value:
            raise ValueError('The key {} with value {} does '
                             'not exist'.format(key_name, value))
        return key_value


def validate_portfolio(value):
    value = to_numeric_string(value)
    if value:
        return portfolio_validator(value)


def validate_party(value):
    value = to_numeric_string(value)
    if value:
        return party_validator(value)


def validate_instrument(value):
    value = to_numeric_string(value)
    if value:
        return instrument_validator(value)


class EquityTradesUploader(ValidatingXLSFeedProcessor):
    """An uploader of equity trades from xlsx file."""

    _validation_parameters = OrderedDict((
        ('Instrument', custom(validate_instrument)),
        ('Direction', create_type_validator(str)),
        ('Nominal', custom(validate_nominal)),
        ('Price', create_type_validator(float)),
        ('TradeTime', custom(validate_time)),
        ('AcquireDay', custom(validate_time)),
        ('Portfolio', custom(validate_portfolio)),
        ('Acquirer', custom(validate_party)),
        ('Counterparty', custom(validate_party)),
        ('MirrorPortfolio', custom(validate_portfolio)),
        ('TradeKey3', custom(validate_key)),
    ))
    # A map of xlsx file columns to trade property names (those which differ).
    _column_map = {
        'TradeKey3': 'OptKey3',
        'Nominal': 'Quantity',
    }
    # Trade properties, which should be set to the same value if provided.
    _duplicated_properties = {
        'ValueDay': 'AcquireDay',
    }
    _required_columns = list(_validation_parameters.keys())

    @classmethod
    def _populate_ael_variables(cls, variables, _):
        variables.add_input_file(
            'input_file',
            label='Input File',
            file_filter='*.xls|*.xlsx',
            alt='Input file in XLS format.')
        variables.add_bool(
            'dry_run',
            label='Dry run')

    @staticmethod
    def _validate_direction(record):
        direction = SIGN_MAP.get(record['Direction'].lower())
        if direction * record['Nominal'] < 0:
            raise ValueError(
                'The direction and the nominal contradict each other: '
                'direction {}, nominal {}'.format(
                    record['Direction'], record['Nominal']))
        return record

    def _validate_record(self, index, record):
        validated_record = super(EquityTradesUploader, self)._validate_record(index, record)
        try:
            self._validate_direction(record)
        except ValueError as err:
            err_msg = 'Validation error on line {}: {}'.format(index, err)
            self._log(err_msg)
            self.errors.append(err_msg)
        else:
            return validated_record

    def _map_columns(self, trade_data):
        for col_name, property_name in list(self._column_map.items()):
            if col_name in trade_data:
                trade_data[property_name] = trade_data.pop(col_name)

    def _duplicate_values(self, trade_data):
        for to_property, from_property in list(self._duplicated_properties.items()):
            if from_property in trade_data:
                trade_data[to_property] = trade_data[from_property]

    def _prepare_data(self, trade_data):
        data = OrderedDict((
            (column, trade_data[column]) for column in self._required_columns
            if trade_data[column] not in (None, '')
        ))
        self._map_columns(data)
        self._duplicate_values(data)
        return data

    def _process_record(self, record, dry_run):
        _, trade_data = record
        trade_data = self._prepare_data(trade_data)
        LOGGER.info('Trade data: {}'.format(xrepr(trade_data)))

        if not dry_run:
            creator = DecoratedTradeCreator(trade_data)
            trade = creator.CreateTrade()
            trade.Commit()
            self.created_trades.append(trade)

    def _process(self, dry_run):
        if dry_run:
            LOGGER.info('DRY RUN activated, no trades will be created')

        acm.BeginTransaction()
        self.created_trades = []
        try:
            super(EquityTradesUploader, self)._process(dry_run)
        except Exception as err:
            LOGGER.error('Failed to upload trades. Error: {}'.format(err))
            acm.AbortTransaction()
        else:
            if self.errors:
                LOGGER.error('Errors occurred, trades were not created.'
                             'Please check ERROR SUMMARY for more info')
                acm.AbortTransaction()
            else:
                acm.CommitTransaction()
                self._log('Created trades: \n\t{}'.format(
                    '\n\t'.join(str(trade.Oid()) for trade in self.created_trades)))


ael_variables = EquityTradesUploader.ael_variables()


def ael_main(ael_params):
    uploader = EquityTradesUploader(str(ael_params['input_file']),
                                    sheet_index=0, sheet_name=None)
    uploader.add_error_notifier(notify_log)
    uploader.process(ael_params['dry_run'])
