"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteBulkXLSXGenerator
    
DESCRIPTION
    This module contains an object used for generating the Excel XLSX rendering of a
    broker note .

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-20      FAOPS-702       Joash Moodley                                   Initial Implementation.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import collections
import datetime
import types
import xml.etree.ElementTree as ElementTree

import xlsxwriter

from BrokerNoteBulkGeneral import Trade, get_instrument_type_description


class GenerateBrokerNoteBulkXLSXRequest(object):
    """
    An object embodying the request to generate the Excel XLSX
    rendering of a broker note .
    """

    def __init__(self, xml_string, output_file):
        """
        Constructor.
        """
        self.xml_string = xml_string
        self.output_file = output_file


class BrokerNoteBulkXLSXGenerator(object):
    """
    An object responsible for generating the Excel XLSX rendering of
    a broker note.
    """

    # Cell format names.
    BOLD_TEXT_FORMAT = 'Bold Text'
    TABLE_HEADER_FORMAT = 'Table Header'
    TABLE_DATA_DEFAULT_FORMAT = 'Table Data Default'
    TABLE_DATA_MONETARY_FORMAT = 'Table Data Monetary'
    TABLE_DATA_RATE_FORMAT = 'Table Data Rate'
    TABLE_DATA_DATE_FORMAT = 'Table Data Date'
    TABLE_DATA_INTEGER_FORMAT = 'Table Data Integer'

    # Column names.    
    TRADE_DATE_COLUMN = 'Trade Date'
    TRADE_NO_COLUMN = 'Trade Number'
    SETTLEMENT_DATE_COLUMN = 'Settlement Date'
    SECURITY_DESCR_COLUMN = 'Security Description'
    BUYER_COLUMN = 'Buyer'
    SELLER_COLUMN = 'Seller'
    ISSUER_COLUMN = 'Issuer'
    ISIN_COLUMN = 'ISIN'
    MATURITY_DATE_COLUMN = 'Maturity Date'
    CURRENCY_COLUMN = 'Currency'
    NOMINAL_COLUMN = 'Nominal'
    YIELD_TO_MATURITY_COLUMN = 'Yield To Maturity'
    CLEAN_PRICE_COLUMN = 'Clean Price'
    CONSIDERATION_INTEREST_COLUMN = 'Accrued Interest'
    ACCRUED_INTEREST = 'Accrued Interest'
    ALL_IN_CONSIDERATION_COLUMN = 'All In Consideration'
    COMPANION_COLUMN = 'Companion'
    CLEAN_CONSIDERATION_COLUMN = 'Clean Consideration'
    COMPANION_SPREAD_COLUMN = 'Companion Spread'
    NUTRON_CODE_COLUMN = 'Counterparty Nutron Code'
    UNEXCOR_CODE_COLUMN = 'Counterparty Unexcor Code'
    ALL_IN_PRICE_COLUMN = 'All In Price'
    AMENDMENT_REASON = 'Amendment Reason'

    @classmethod
    def generate_xlsx(cls, generate_xlsx_request):
        """
        Generate the Excel XLSX rendering of a broker note .
        """
        xml_string = generate_xlsx_request.xml_string
        output_file = generate_xlsx_request.output_file
        root_element = ElementTree.fromstring(xml_string)
        instrument_type = root_element.find('INSTRUMENT_TYPE').text
        trade_data = cls._get_trades_data(instrument_type, root_element)
        if trade_data:
            with xlsxwriter.Workbook(output_file) as workbook:
                formats = cls._create_formats(workbook)
                cls._add_economics_worksheet(workbook, instrument_type, trade_data, formats)
        else:
            raise RuntimeError('No Data found') 
    
    @classmethod
    def _get_trades_data(cls, instrument_type, root_element):
        if instrument_type in ['Bond', 'IndexLinkedBond']:
            return cls._get_bond_data(root_element)
        elif instrument_type == 'FRN':
            return cls._get_frn_data(root_element)
        return []
    
    @classmethod
    def _get_bond_data(cls, root_element):
        """
        Get the trade data for the broker note .
        """
        trade_data = []
        for trade_element in root_element.iterfind('BROKER_NOTE'):
            trade = Trade.from_xml_element(trade_element)
            trade_date = trade.trade_date
            maturity_date = trade.maturity_date 
            trade_row_data = {}
            trade_row_data[cls.TRADE_NO_COLUMN] = trade.trade_no
            trade_row_data[cls.TRADE_DATE_COLUMN] = trade_date
            trade_row_data[cls.SETTLEMENT_DATE_COLUMN] = trade.settlement_date
            trade_row_data[cls.SECURITY_DESCR_COLUMN] = trade.security_descr
            trade_row_data[cls.BUYER_COLUMN] = trade.buyer
            trade_row_data[cls.SELLER_COLUMN] = trade.seller
            trade_row_data[cls.ISSUER_COLUMN] = trade.issuer
            trade_row_data[cls.ISIN_COLUMN] = trade.isin
            trade_row_data[cls.MATURITY_DATE_COLUMN] = maturity_date
            trade_row_data[cls.CURRENCY_COLUMN] = trade.currency
            trade_row_data[cls.NOMINAL_COLUMN] = trade.nominal
            trade_row_data[cls.YIELD_TO_MATURITY_COLUMN] = trade.yield_to_maturity
            trade_row_data[cls.CLEAN_PRICE_COLUMN] = trade.clean_price
            trade_row_data[cls.CLEAN_CONSIDERATION_COLUMN] = trade.clean_consideration
            trade_row_data[cls.CONSIDERATION_INTEREST_COLUMN] = trade.consideration_interest
            trade_row_data[cls.ALL_IN_CONSIDERATION_COLUMN] = trade.all_in_consideration
            trade_row_data[cls.COMPANION_COLUMN] = trade.companion
            trade_row_data[cls.COMPANION_SPREAD_COLUMN] = trade.companion_spread
            trade_row_data[cls.NUTRON_CODE_COLUMN] = trade.nutron_code
            trade_row_data[cls.UNEXCOR_CODE_COLUMN] = trade.unexcor_code
            trade_data.append(trade_row_data)
        return trade_data
    
    @classmethod
    def _get_frn_data(cls, root_element):
        """
        Get the trade data for the broker note .
        """
        trade_data = []
        for trade_element in root_element.iterfind('BROKER_NOTE'):
            trade = Trade.from_xml_element(trade_element)
            trade_date = trade.trade_date
            maturity_date = trade.maturity_date 
            trade_row_data = {}
            trade_row_data[cls.TRADE_NO_COLUMN] = trade.trade_no
            trade_row_data[cls.TRADE_DATE_COLUMN] = trade_date
            trade_row_data[cls.SETTLEMENT_DATE_COLUMN] = trade.settlement_date
            trade_row_data[cls.SECURITY_DESCR_COLUMN] = trade.security_descr
            trade_row_data[cls.BUYER_COLUMN] = trade.buyer
            trade_row_data[cls.SELLER_COLUMN] = trade.seller
            trade_row_data[cls.ISSUER_COLUMN] = trade.issuer
            trade_row_data[cls.ISIN_COLUMN] = trade.isin
            trade_row_data[cls.ALL_IN_PRICE_COLUMN] = trade.all_in_price
            trade_row_data[cls.MATURITY_DATE_COLUMN] = maturity_date
            trade_row_data[cls.CURRENCY_COLUMN] = trade.currency
            trade_row_data[cls.NOMINAL_COLUMN] = trade.nominal
            trade_row_data[cls.ACCRUED_INTEREST] = trade.consideration_interest
            trade_row_data[cls.ALL_IN_CONSIDERATION_COLUMN] = trade.all_in_consideration
            trade_row_data[cls.COMPANION_COLUMN] = trade.companion
            trade_row_data[cls.COMPANION_SPREAD_COLUMN] = trade.companion_spread
            trade_row_data[cls.NUTRON_CODE_COLUMN] = trade.nutron_code
            trade_row_data[cls.UNEXCOR_CODE_COLUMN] = trade.unexcor_code
            trade_data.append(trade_row_data)
        return trade_data

    @classmethod
    def _create_formats(cls, workbook):
        """
        Create standard formats for worksheet cell formatting.
        """
        formats = dict()
        # Format for bold text that is not within a table.
        formats[cls.BOLD_TEXT_FORMAT] = workbook.add_format({
            'bold': True
        })
        # Format for tables headers.
        formats[cls.TABLE_HEADER_FORMAT] = workbook.add_format({
            'bg_color': '#FF0800',
            'border': 1,
            'color': '#FFFFFF',
            'bold': True
        })
        # Formats for table data.
        formats[cls.TABLE_DATA_DEFAULT_FORMAT] = workbook.add_format({
            'bg_color': '#FFEFEF',
            'border': 1
        })
        formats[cls.TABLE_DATA_MONETARY_FORMAT] = workbook.add_format({
            'bg_color': '#FFEFEF',
            'border': 1,
            'num_format': '#0.00'
        })
        formats[cls.TABLE_DATA_RATE_FORMAT] = workbook.add_format({
            'bg_color': '#FFEFEF',
            'border': 1,
            'num_format': '#0.0####'
        })
        formats[cls.TABLE_DATA_DATE_FORMAT] = workbook.add_format({
            'bg_color': '#FFEFEF',
            'border': 1,
            'num_format': 'yyyy-mm-dd'
        })
        formats[cls.TABLE_DATA_INTEGER_FORMAT] = workbook.add_format({
            'bg_color': '#FFEFEF',
            'border': 1,
            'num_format': '#0'
        })
        return formats

    @classmethod
    def _add_economics_worksheet(
            cls, workbook, instrument_type,
            trades_data, formats):
        """
        Add the economics worksheet to the broker note  Excel
        XLSX workbook.
        """
        worksheet = workbook.add_worksheet('Economics')
        current_row_index = 0
        # Write current trade economics table.
        # Write heading.
        cls._write_economics_heading(
            worksheet, current_row_index, 0, 
            instrument_type, formats)
        current_row_index += 2
        current_economics_data = cls._get_current_economics_data(
            trades_data, instrument_type
        )
        if len(current_economics_data) > 0:
            # Write current trade economics table.
            cls._sort_trades_data(current_economics_data)
            column_definitions = cls._get_current_economics_column_definitions(instrument_type)            
            cls._write_table(worksheet, current_row_index, 0, column_definitions, current_economics_data, formats)

    @classmethod
    def _get_current_economics_data(cls, trades_data, instrument_type):
        """
        Get the current economics data.
        """
        if instrument_type in ['Bond', 'IndexLinkedBond']:
            return cls._get_bond_economics_data(trades_data)
        elif instrument_type == 'FRN':
            return cls._get_frn_economics_data(trades_data)
        return {}

    @classmethod
    def _get_bond_economics_data(cls, trades_data):
        """
        Get the current economics data.
        """
        current_economics_data_by_key = dict()
        for trade_data in trades_data:
            reference = trade_data[cls.TRADE_NO_COLUMN]
            currency = trade_data[cls.CURRENCY_COLUMN]
            payment_date = trade_data[cls.MATURITY_DATE_COLUMN]
            economics_key = '{reference}_{currency}_{payment_date}'.format(
                reference=reference,
                currency=currency,
                payment_date=payment_date
            )
            economics_data = {}
            economics_data[cls.TRADE_NO_COLUMN] = trade_data[cls.TRADE_NO_COLUMN]
            economics_data[cls.TRADE_DATE_COLUMN] = trade_data[cls.TRADE_DATE_COLUMN]
            economics_data[cls.SETTLEMENT_DATE_COLUMN] = trade_data[cls.SETTLEMENT_DATE_COLUMN]
            economics_data[cls.SECURITY_DESCR_COLUMN] = trade_data[cls.SECURITY_DESCR_COLUMN]
            economics_data[cls.BUYER_COLUMN] = trade_data[cls.BUYER_COLUMN]
            economics_data[cls.SELLER_COLUMN] = trade_data[cls.SELLER_COLUMN]
            economics_data[cls.ISSUER_COLUMN] = trade_data[cls.ISSUER_COLUMN]
            economics_data[cls.ISIN_COLUMN] = trade_data[cls.ISIN_COLUMN]
            economics_data[cls.MATURITY_DATE_COLUMN] = trade_data[cls.MATURITY_DATE_COLUMN]
            economics_data[cls.CURRENCY_COLUMN] = trade_data[cls.CURRENCY_COLUMN]
            economics_data[cls.NOMINAL_COLUMN] = trade_data[cls.NOMINAL_COLUMN]
            economics_data[cls.YIELD_TO_MATURITY_COLUMN] = trade_data[cls.YIELD_TO_MATURITY_COLUMN]
            economics_data[cls.CLEAN_PRICE_COLUMN] = trade_data[cls.CLEAN_PRICE_COLUMN]
            economics_data[cls.CLEAN_CONSIDERATION_COLUMN] = trade_data[cls.CLEAN_CONSIDERATION_COLUMN]
            economics_data[cls.CONSIDERATION_INTEREST_COLUMN] = trade_data[cls.CONSIDERATION_INTEREST_COLUMN]
            economics_data[cls.ALL_IN_CONSIDERATION_COLUMN] = trade_data[cls.ALL_IN_CONSIDERATION_COLUMN]
            economics_data[cls.COMPANION_COLUMN] = trade_data[cls.COMPANION_COLUMN]
            economics_data[cls.COMPANION_SPREAD_COLUMN] = trade_data[cls.COMPANION_SPREAD_COLUMN]
            economics_data[cls.NUTRON_CODE_COLUMN] = trade_data[cls.NUTRON_CODE_COLUMN]
            economics_data[cls.UNEXCOR_CODE_COLUMN] = trade_data[cls.UNEXCOR_CODE_COLUMN]
            current_economics_data_by_key[economics_key] = economics_data

        return current_economics_data_by_key.values()

    @classmethod
    def _get_frn_economics_data(cls, trades_data):
        """
        Get the current economics data.
        """
        current_economics_data_by_key = dict()
        for trade_data in trades_data:
            reference = trade_data[cls.TRADE_NO_COLUMN]
            currency = trade_data[cls.CURRENCY_COLUMN]
            payment_date = trade_data[cls.MATURITY_DATE_COLUMN]
            economics_key = '{reference}_{currency}_{payment_date}'.format(
                reference=reference,
                currency=currency,
                payment_date=payment_date
            )
            economics_data = {}
            economics_data[cls.TRADE_NO_COLUMN] = trade_data[cls.TRADE_NO_COLUMN]
            economics_data[cls.TRADE_DATE_COLUMN] = trade_data[cls.TRADE_DATE_COLUMN]
            economics_data[cls.SETTLEMENT_DATE_COLUMN] = trade_data[cls.SETTLEMENT_DATE_COLUMN]
            economics_data[cls.SECURITY_DESCR_COLUMN] = trade_data[cls.SECURITY_DESCR_COLUMN]
            economics_data[cls.BUYER_COLUMN] = trade_data[cls.BUYER_COLUMN]
            economics_data[cls.SELLER_COLUMN] = trade_data[cls.SELLER_COLUMN]
            economics_data[cls.ISSUER_COLUMN] = trade_data[cls.ISSUER_COLUMN]
            economics_data[cls.ISIN_COLUMN] = trade_data[cls.ISIN_COLUMN]
            economics_data[cls.ALL_IN_PRICE_COLUMN] = trade_data[cls.ALL_IN_PRICE_COLUMN]
            economics_data[cls.MATURITY_DATE_COLUMN] = trade_data[cls.MATURITY_DATE_COLUMN]
            economics_data[cls.CURRENCY_COLUMN] = trade_data[cls.CURRENCY_COLUMN]
            economics_data[cls.NOMINAL_COLUMN] = trade_data[cls.NOMINAL_COLUMN]
            economics_data[cls.ACCRUED_INTEREST] = trade_data[cls.ACCRUED_INTEREST]
            economics_data[cls.ALL_IN_CONSIDERATION_COLUMN] = trade_data[cls.ALL_IN_CONSIDERATION_COLUMN]
            economics_data[cls.COMPANION_COLUMN] = trade_data[cls.COMPANION_COLUMN]
            economics_data[cls.COMPANION_SPREAD_COLUMN] = trade_data[cls.COMPANION_SPREAD_COLUMN]
            economics_data[cls.NUTRON_CODE_COLUMN] = trade_data[cls.NUTRON_CODE_COLUMN]
            economics_data[cls.UNEXCOR_CODE_COLUMN] = trade_data[cls.UNEXCOR_CODE_COLUMN]
            current_economics_data_by_key[economics_key] = economics_data

        return current_economics_data_by_key.values()

    @classmethod
    def _get_current_economics_column_definitions(cls, instrument_type):
        if instrument_type in ['Bond', 'IndexLinkedBond']:
            return cls._get_current_bond_column_definitions()
        elif instrument_type == 'FRN':
            return cls._get_current_frn_column_definitions()
        return {}    
    
    @classmethod
    def _get_current_frn_column_definitions(cls):
        """
        Get economics column definitions.
        """
        # Ordered dict defining order and properties of economics columns.
        column_definitions = collections.OrderedDict()
        
        column_definitions[cls.TRADE_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.TRADE_NO_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.BUYER_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.SELLER_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.SETTLEMENT_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.SECURITY_DESCR_COLUMN] = {
            'width': 15
        }
        
        column_definitions[cls.ISSUER_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.ISIN_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.MATURITY_DATE_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.CURRENCY_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.NOMINAL_COLUMN] = {
            'width': 18,
            'type': 'Monetary',

        }
        column_definitions[cls.ALL_IN_PRICE_COLUMN] = {
            'width': 18,
            'type': 'Monetary',

        }
        column_definitions[cls.ACCRUED_INTEREST] = {
            'width': 18
        }
        column_definitions[cls.ALL_IN_CONSIDERATION_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.COMPANION_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.COMPANION_SPREAD_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.NUTRON_CODE_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.UNEXCOR_CODE_COLUMN] = {
            'width': 18
        }
        return column_definitions
    
    @classmethod
    def _get_current_bond_column_definitions(cls):
        """
        Get economics column definitions.
        """
        # Ordered dict defining order and properties of economics columns.
        column_definitions = collections.OrderedDict()
        
        column_definitions[cls.TRADE_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.TRADE_NO_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.BUYER_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.SELLER_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.SETTLEMENT_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.SECURITY_DESCR_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.ISIN_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.ISSUER_COLUMN] = {
            'width': 18
        }
        
        column_definitions[cls.MATURITY_DATE_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.CURRENCY_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.NOMINAL_COLUMN] = {
            'width': 18,
            'type': 'Monetary',

        }
        column_definitions[cls.YIELD_TO_MATURITY_COLUMN] = {
            'type': 'Monetary',
            'width': 20
        }
        column_definitions[cls.CLEAN_PRICE_COLUMN] = {
            'width': 20,
            'type': 'Monetary',

        }
        column_definitions[cls.CLEAN_CONSIDERATION_COLUMN] = {
            'width': 20,
            'type': 'Monetary',

        }
        column_definitions[cls.CONSIDERATION_INTEREST_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.ALL_IN_CONSIDERATION_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.COMPANION_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.COMPANION_SPREAD_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.NUTRON_CODE_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.UNEXCOR_CODE_COLUMN] = {
            'width': 18
        }
        return column_definitions

    @classmethod
    def _write_economics_heading(cls, worksheet, row_index, column_index, instrument_type, formats):
        """
        Write the broker note  economics heading.
        """
        bold_text_format = formats[cls.BOLD_TEXT_FORMAT]
        heading = ""
        heading += "{instrument_type_description} Broker Note  Economics".format(
            instrument_type_description=get_instrument_type_description(instrument_type),
        )
        worksheet.write(row_index, column_index, heading, bold_text_format)

    @classmethod
    def _get_current_trades_data(cls, trades_data):
        """
        Get the current trade data.
        """
        current_trades_data = list()
        for trade_data in trades_data:
            current_trades_data.append(trade_data)
        return current_trades_data

    @classmethod
    def _sort_trades_data(cls, trades_data):
        """
        Sort the trade data in order in which it should be
        displayed.
        """
        # Sort by trade no, currency, maturity date.
        trades_data.sort(key=lambda x: int(x[cls.TRADE_NO_COLUMN]))
        trades_data.sort(key=lambda x: x[cls.CURRENCY_COLUMN], reverse=True)
        trades_data.sort(key=lambda x: x[cls.MATURITY_DATE_COLUMN])

    @classmethod
    def _write_table(cls, worksheet, start_row_index, start_column_index, column_definitions, table_data, formats):
        """
        Write a worksheet table using the specified position, column
        definitions and table data.
        """
        # Add table.
        end_row_index = start_row_index + len(table_data)
        end_column_index = start_column_index + len(column_definitions) - 1
        table_header_format = formats[cls.TABLE_HEADER_FORMAT]
        column_options = list()
        for column_name in column_definitions.keys():
            column_options.append({
                'header': column_name,
                'header_format': table_header_format
            })
        table_options = {
            'columns': column_options,
            'style': 'TableStyle Light 10'
        }
        worksheet.add_table(start_row_index, start_column_index, end_row_index, end_column_index, table_options)
        # Write table data.
        current_row_index = start_row_index + 1
        cls._write_table_data(worksheet, current_row_index, start_column_index, column_definitions, table_data,
            formats)
        # Set column widths.
        cls._set_column_widths(worksheet, start_column_index, column_definitions)

    @classmethod
    def _write_table_data(cls, worksheet, starting_row_index, starting_column_index, column_definitions, table_data,
            formats):
        """
        Write the worksheet table data using the specified column
        definitions and table data.
        """
        table_data_default_format = formats[cls.TABLE_DATA_DEFAULT_FORMAT]
        table_data_monetary_format = formats[cls.TABLE_DATA_MONETARY_FORMAT]
        table_data_rate_format = formats[cls.TABLE_DATA_RATE_FORMAT]
        table_data_date_format = formats[cls.TABLE_DATA_DATE_FORMAT]
        table_data_integer_format = formats[cls.TABLE_DATA_INTEGER_FORMAT]
        current_row_index = starting_row_index
        for row_data in table_data:
            for column_number, column_name in enumerate(column_definitions.keys()):
                column_index = starting_column_index + column_number
                cell_value = row_data[column_name]
                if isinstance(cell_value, type(None)):
                    worksheet.write_blank(current_row_index, column_index, cell_value, table_data_default_format)
                elif isinstance(cell_value, bytes):
                    worksheet.write_string(current_row_index, column_index, cell_value, table_data_default_format)
                elif isinstance(cell_value, datetime.datetime):
                    worksheet.write_datetime(current_row_index, column_index, cell_value, table_data_date_format)
                elif isinstance(cell_value, float):
                    economics_column = column_definitions[column_name]
                    cell_format = table_data_default_format
                    if 'type' in economics_column.keys():
                        column_type = economics_column['type']
                        if column_type == 'Monetary':
                            cell_format = table_data_monetary_format
                        elif column_type == 'Rate':
                            cell_format = table_data_rate_format
                    worksheet.write_number(current_row_index, column_index, cell_value, cell_format)
                elif isinstance(cell_value, int):
                    worksheet.write_number(current_row_index, column_index, cell_value, table_data_integer_format)
                else:
                    worksheet.write(current_row_index, column_index, cell_value, table_data_default_format)
            current_row_index += 1

    @staticmethod
    def _set_column_widths(worksheet, starting_column_index, column_definitions):
        """
        Set the worksheet column widths using the specified column
        definitions.
        """
        for column_number, column_name in enumerate(column_definitions.keys()):
            column_index = starting_column_index + column_number
            economics_column = column_definitions[column_name]
            worksheet.set_column(column_index, column_index, economics_column['width'])

    @staticmethod
    def _iso_date_string_to_datetime(iso_date_string):
        """
        Convert a string date in ISO format to a datetime object.
        """
        return datetime.datetime.strptime(iso_date_string, '%Y-%m-%d')
