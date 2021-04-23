"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceXLSXGenerator
    
DESCRIPTION
    This module contains an object used for generating the Excel XLSX rendering of a
    pre-settlement advice.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
                                Tawanda Mukhalela
                                Stuart Wilson
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-02-21      FAOPS-544/547   Cuen Edwards            Letitia Carboni         Added support for FRAs.
2020-02-21      FAOPS-578/591   Cuen Edwards            Letitia Carboni         Added support for Currency Swaps.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import collections
import datetime
import types
import xml.etree.ElementTree as ElementTree

import xlsxwriter

from PreSettlementAdviceGeneral import AmendmentActions, Settlement, SettlementInstruction
import PreSettlementAdviceGeneral


class GeneratePreSettlementAdviceXLSXRequest(object):
    """
    An object embodying the request to generate the Excel XLSX
    rendering of a pre-settlement advice.
    """

    def __init__(self, xml_string, output_file):
        """
        Constructor.
        """
        self.xml_string = xml_string
        self.output_file = output_file


class PreSettlementAdviceXLSXGenerator(object):
    """
    An object responsible for generating the Excel XLSX rendering of
    a pre-settlement advice.
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
    BANK_TRADE_REFERENCE_COLUMN = 'Reference'
    MARKITWIRE_TRADE_REFERENCE_COLUMN = 'Markitwire Ref'
    COUNTERPARTY_TRADE_REFERENCE_COLUMN = 'Counterparty Ref'
    COUNTERPARTY_COLUMN = 'Counterparty'
    PAY_RECEIVE_COLUMN = 'Pay/Receive'
    CURRENCY_COLUMN = 'Currency'
    PAY_AMOUNT_COLUMN = 'Pay Amount'
    NOMINAL_COLUMN = 'Nominal'
    PAY_TYPE_COLUMN = 'Pay Type'
    TRADE_DATE_COLUMN = 'Trade Date'
    EFFECTIVE_DATE_COLUMN = 'Effective Date'
    TERMINATION_DATE_COLUMN = 'Termination Date'
    PAY_DATE_COLUMN = 'Pay Date'
    PAY_BUS_DAY_CONVENTION_COLUMN = 'Pay Bus Day Convention'
    PAY_CALENDARS_COLUMN = 'Pay Calenders'
    FLOAT_RATE_REF_COLUMN = 'Float Rate Ref'
    FLOAT_RATE_COLUMN = 'Float Rate'
    FIXED_RATE_COLUMN = 'Fixed Rate'
    SPREAD_COLUMN = 'Spread'
    RESET_CALENDARS_COLUMN = 'Reset Calendars'
    DAYS_COLUMN = 'Days'
    FIXING_OFFSET_COLUMN = 'Fixing Offset'
    DAY_COUNT_CONVENTION_COLUMN = 'Day Count Convention'
    ROLLING_PERIOD_COLUMN = 'Rolling Period'
    RESET_BUS_DAY_CONVENTION_COLUMN = 'Reset Bus Day Convention'
    ACCOUNT_NUMBER_COLUMN = 'Account Number'
    BENEFICIARY_BANK_NAME = 'Beneficiary Bank'
    BENEFICIARY_BANK_BIC = 'Beneficiary BIC'
    CORRESPONDENT_BANK_NAME = 'Correspondent Bank'
    CORRESPONDENT_BANK_BIC = 'Correspondent BIC'
    AMENDMENT_ACTION = 'Amendment Action'
    AMENDMENT_REASON = 'Amendment Reason'

    @classmethod
    def generate_xlsx(cls, generate_xlsx_request):
        """
        Generate the Excel XLSX rendering of a pre-settlement advice.
        """
        xml_string = generate_xlsx_request.xml_string
        output_file = generate_xlsx_request.output_file
        root_element = ElementTree.fromstring(xml_string)
        bank_abbreviated_name = root_element.find('BANK_ABBREVIATED_NAME').text
        instrument_type = root_element.find('INSTRUMENT_TYPE').text
        from_date = root_element.find('FROM_DATE').text
        to_date = root_element.find('TO_DATE').text
        is_amended = root_element.find('SETTLEMENTS/SETTLEMENT[@amendment_action]') is not None
        settlements_data = cls._get_settlements_data(root_element)
        settlement_instruction_data_by_currency = cls._get_settlement_instruction_data_by_currency(root_element)
        with xlsxwriter.Workbook(output_file) as workbook:
            formats = cls._create_formats(workbook)
            cls._add_summary_worksheet(workbook, instrument_type, from_date, to_date, is_amended, settlements_data,
                bank_abbreviated_name, formats)
            cls._add_details_worksheet(workbook, instrument_type, from_date, to_date, is_amended, settlements_data,
                formats)
            if len(settlement_instruction_data_by_currency.keys()) > 0:
                cls._add_settlement_instructions_worksheet(workbook, settlement_instruction_data_by_currency,
                    bank_abbreviated_name, formats)

    @classmethod
    def _get_settlements_data(cls, root_element):
        """
        Get the settlements data for the pre-settlement advice.
        """
        settlements_data = list()
        for settlement_element in root_element.iterfind('SETTLEMENTS/SETTLEMENT'):
            settlement = Settlement.from_xml_element(settlement_element)
            trade_date = cls._iso_date_string_to_datetime(settlement.trade_date)
            effective_date = cls._iso_date_string_to_datetime(settlement.effective_date)
            termination_date = cls._iso_date_string_to_datetime(settlement.termination_date)
            payment_date = cls._iso_date_string_to_datetime(settlement.payment_date)
            payment_amount = 'TBC'
            if not settlement.is_estimate:
                payment_amount = float(settlement_element.find('AMOUNT').text)
            float_rate = None
            if settlement.float_rate is not None:
                if settlement.is_estimate:
                    float_rate = 'TBC'
                else:
                    float_rate = settlement.float_rate
            settlement_row_data = dict()
            settlement_row_data[cls.BANK_TRADE_REFERENCE_COLUMN] = settlement.bank_trade_reference
            settlement_row_data[cls.MARKITWIRE_TRADE_REFERENCE_COLUMN] = settlement.markitwire_trade_reference
            settlement_row_data[cls.COUNTERPARTY_TRADE_REFERENCE_COLUMN] = settlement.counterparty_trade_reference
            settlement_row_data[cls.COUNTERPARTY_COLUMN] = settlement.counterparty_name
            settlement_row_data[cls.CURRENCY_COLUMN] = settlement.currency
            settlement_row_data[cls.NOMINAL_COLUMN] = settlement.nominal
            settlement_row_data[cls.PAY_TYPE_COLUMN] = settlement.pay_type
            settlement_row_data[cls.TRADE_DATE_COLUMN] = trade_date
            settlement_row_data[cls.EFFECTIVE_DATE_COLUMN] = effective_date
            settlement_row_data[cls.TERMINATION_DATE_COLUMN] = termination_date
            settlement_row_data[cls.PAY_DATE_COLUMN] = payment_date
            settlement_row_data[cls.PAY_BUS_DAY_CONVENTION_COLUMN] = settlement.payment_business_day_convention
            settlement_row_data[cls.PAY_CALENDARS_COLUMN] = settlement.payment_calendars
            settlement_row_data[cls.PAY_AMOUNT_COLUMN] = payment_amount
            settlement_row_data[cls.FLOAT_RATE_REF_COLUMN] = settlement.float_rate_reference
            settlement_row_data[cls.FLOAT_RATE_COLUMN] = float_rate
            settlement_row_data[cls.FIXED_RATE_COLUMN] = settlement.fixed_rate
            settlement_row_data[cls.SPREAD_COLUMN] = settlement.spread
            settlement_row_data[cls.RESET_CALENDARS_COLUMN] = settlement.reset_calendars
            settlement_row_data[cls.DAYS_COLUMN] = settlement.days
            settlement_row_data[cls.FIXING_OFFSET_COLUMN] = settlement.fixing_offset
            settlement_row_data[cls.DAY_COUNT_CONVENTION_COLUMN] = settlement.day_count_method
            settlement_row_data[cls.ROLLING_PERIOD_COLUMN] = settlement.rolling_period
            settlement_row_data[cls.RESET_BUS_DAY_CONVENTION_COLUMN] = settlement.reset_business_day_convention
            settlement_row_data[cls.AMENDMENT_ACTION] = settlement.amendment_action
            settlement_row_data[cls.AMENDMENT_REASON] = settlement.amendment_reason
            settlements_data.append(settlement_row_data)
        return settlements_data

    @classmethod
    def _get_settlement_instruction_data_by_currency(cls, root_element):
        """
        Get the settlements instruction data by currency for the pre-settlement
        advice.
        """
        settlement_instruction_data_by_currency = dict()
        for instruction_element in root_element.iterfind('SETTLEMENT_INSTRUCTIONS/SETTLEMENT_INSTRUCTION'):
            settlement_instruction = SettlementInstruction.from_xml_element(instruction_element)
            currency = settlement_instruction.currency
            account_number = settlement_instruction.account_number
            beneficiary_bank_name = settlement_instruction.beneficiary_bank_name
            beneficiary_bank_bic = settlement_instruction.beneficiary_bank_bic
            correspondent_bank_name = settlement_instruction.correspondent_bank_name
            correspondent_bank_bic = settlement_instruction.correspondent_bank_bic
            if correspondent_bank_name == beneficiary_bank_name:
                # Don't display correspondent bank details if the same as beneficiary bank.
                # Favour any BIC defined on the account level.
                beneficiary_bank_bic = correspondent_bank_bic
                correspondent_bank_name = None
                correspondent_bank_bic = None
            settlement_instruction_data = dict()
            settlement_instruction_data[cls.ACCOUNT_NUMBER_COLUMN] = account_number
            settlement_instruction_data[cls.BENEFICIARY_BANK_NAME] = beneficiary_bank_name
            settlement_instruction_data[cls.BENEFICIARY_BANK_BIC] = beneficiary_bank_bic
            settlement_instruction_data[cls.CORRESPONDENT_BANK_NAME] = correspondent_bank_name
            settlement_instruction_data[cls.CORRESPONDENT_BANK_BIC] = correspondent_bank_bic
            settlement_instruction_data_by_currency[currency] = settlement_instruction_data
        return settlement_instruction_data_by_currency

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
    def _add_summary_worksheet(cls, workbook, instrument_type, from_date, to_date, is_amended, settlements_data,
            bank_abbreviated_name, formats):
        """
        Add the Summary worksheet to the pre-settlement advice Excel
        XLSX workbook.
        """
        worksheet = workbook.add_worksheet('Summary')
        current_row_index = 0
        # Write current settlements summary table.
        # Write heading.
        cls._write_summary_heading(worksheet, current_row_index, 0, instrument_type, from_date, to_date, is_amended,
            formats)
        current_row_index += 2
        current_summary_data = cls._get_current_summary_data(settlements_data, bank_abbreviated_name)
        if len(current_summary_data) > 0:
            # Write current settlements summary table.
            cls._sort_settlements_data(current_summary_data)
            column_definitions = cls._get_current_summary_column_definitions()
            cls._write_table(worksheet, current_row_index, 0, column_definitions, current_summary_data, formats)
            current_row_index = current_row_index + len(current_summary_data) + 3
        if is_amended:
            # Write amended settlements summary table.
            # Write heading.
            cls._write_amendment_summary_heading(worksheet, current_row_index, 0, formats)
            amended_summary_data = cls._get_amended_summary_data(settlements_data, bank_abbreviated_name)
            cls._sort_settlements_data(amended_summary_data)
            current_row_index += 2
            # Write table.
            amended_summary_column_definitions = cls._get_amended_summary_column_definitions()
            cls._write_table(worksheet, current_row_index, 0, amended_summary_column_definitions, amended_summary_data,
                formats)

    @classmethod
    def _get_current_summary_data(cls, settlements_data, bank_abbreviated_name):
        """
        Get the current summary data.
        """
        current_summary_data_by_key = dict()
        for settlement_data in settlements_data:
            if settlement_data[cls.AMENDMENT_ACTION] in [AmendmentActions.REMOVED]:
                continue
            reference = settlement_data[cls.BANK_TRADE_REFERENCE_COLUMN]
            currency = settlement_data[cls.CURRENCY_COLUMN]
            payment_date = settlement_data[cls.PAY_DATE_COLUMN]
            summary_key = '{reference}_{currency}_{payment_date}'.format(
                reference=reference,
                currency=currency,
                payment_date=payment_date
            )
            if summary_key in current_summary_data_by_key.keys():
                summary_data = current_summary_data_by_key[summary_key]
                current_payment_amount = summary_data[cls.PAY_AMOUNT_COLUMN]
                new_payment_amount = settlement_data[cls.PAY_AMOUNT_COLUMN]
                payment_amount = 'TBC'
                pay_receive = 'TBC'
                if (isinstance(current_payment_amount, float) and
                        isinstance(new_payment_amount, float)):
                    payment_amount = current_payment_amount + new_payment_amount
                    pay_receive = cls._get_pay_receive_description(payment_amount, bank_abbreviated_name)
                summary_data[cls.PAY_RECEIVE_COLUMN] = pay_receive
                summary_data[cls.PAY_AMOUNT_COLUMN] = payment_amount
            else:
                counterparty_name = settlement_data[cls.COUNTERPARTY_COLUMN]
                payment_amount = settlement_data[cls.PAY_AMOUNT_COLUMN]
                pay_receive = 'TBC'
                if isinstance(payment_amount, float):
                    pay_receive = cls._get_pay_receive_description(payment_amount, bank_abbreviated_name)
                markitwire_reference = settlement_data[cls.MARKITWIRE_TRADE_REFERENCE_COLUMN]
                counterparty_reference = settlement_data[cls.COUNTERPARTY_TRADE_REFERENCE_COLUMN]
                summary_data = dict()
                summary_data[cls.BANK_TRADE_REFERENCE_COLUMN] = reference
                summary_data[cls.COUNTERPARTY_COLUMN] = counterparty_name
                summary_data[cls.PAY_DATE_COLUMN] = payment_date
                summary_data[cls.PAY_RECEIVE_COLUMN] = pay_receive
                summary_data[cls.CURRENCY_COLUMN] = currency
                summary_data[cls.PAY_AMOUNT_COLUMN] = payment_amount
                summary_data[cls.MARKITWIRE_TRADE_REFERENCE_COLUMN] = markitwire_reference
                summary_data[cls.COUNTERPARTY_TRADE_REFERENCE_COLUMN] = counterparty_reference
                current_summary_data_by_key[summary_key] = summary_data
        return current_summary_data_by_key.values()

    @classmethod
    def _get_current_summary_column_definitions(cls):
        """
        Get summary column definitions.
        """
        # Ordered dict defining order and properties of summary columns.
        column_definitions = collections.OrderedDict()
        column_definitions[cls.BANK_TRADE_REFERENCE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_RECEIVE_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.CURRENCY_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.PAY_AMOUNT_COLUMN] = {
            'type': 'Monetary',
            'width': 20
        }
        column_definitions[cls.COUNTERPARTY_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.MARKITWIRE_TRADE_REFERENCE_COLUMN] = {
            'width': 18
        }
        column_definitions[cls.COUNTERPARTY_TRADE_REFERENCE_COLUMN] = {
            'width': 18
        }
        return column_definitions

    @classmethod
    def _get_amended_summary_column_definitions(cls):
        """
        Get amended summary column definitions.
        """
        column_definitions = cls._get_current_summary_column_definitions()
        column_definitions[cls.AMENDMENT_REASON] = {
            'width': 15
        }
        return column_definitions

    @classmethod
    def _get_amended_summary_data(cls, settlements_data, bank_abbreviated_name):
        """
        Get the amended summary data.
        """
        amended_summary_keys = set()
        for settlement_data in settlements_data:
            reference = settlement_data[cls.BANK_TRADE_REFERENCE_COLUMN]
            currency = settlement_data[cls.CURRENCY_COLUMN]
            payment_date = settlement_data[cls.PAY_DATE_COLUMN]
            summary_key = '{reference}_{currency}_{payment_date}'.format(
                reference=reference,
                currency=currency,
                payment_date=payment_date
            )
            amendment_action = settlement_data[cls.AMENDMENT_ACTION]
            if amendment_action is not None:
                amended_summary_keys.add(summary_key)
        amended_summary_data_by_key = dict()
        for settlement_data in settlements_data:
            reference = settlement_data[cls.BANK_TRADE_REFERENCE_COLUMN]
            currency = settlement_data[cls.CURRENCY_COLUMN]
            payment_date = settlement_data[cls.PAY_DATE_COLUMN]
            summary_key = '{reference}_{currency}_{payment_date}'.format(
                reference=reference,
                currency=currency,
                payment_date=payment_date
            )
            if summary_key not in amended_summary_keys:
                continue
            if summary_key in amended_summary_data_by_key.keys():
                summary_data = amended_summary_data_by_key[summary_key]
                current_payment_amount = summary_data[cls.PAY_AMOUNT_COLUMN]
                new_payment_amount = settlement_data[cls.PAY_AMOUNT_COLUMN]
                payment_amount = 'TBC'
                pay_receive = 'TBC'
                if (isinstance(current_payment_amount, float) and
                        isinstance(new_payment_amount, float)):
                    payment_amount = current_payment_amount + new_payment_amount
                    pay_receive = cls._get_pay_receive_description(payment_amount, bank_abbreviated_name)
                summary_data[cls.PAY_RECEIVE_COLUMN] = pay_receive
                summary_data[cls.PAY_AMOUNT_COLUMN] = payment_amount
                amendment_reason = settlement_data[cls.AMENDMENT_REASON]
                if amendment_reason is not None:
                    summary_data[cls.AMENDMENT_REASON] = amendment_reason
            else:
                counterparty_name = settlement_data[cls.COUNTERPARTY_COLUMN]
                payment_amount = settlement_data[cls.PAY_AMOUNT_COLUMN]
                pay_receive = 'TBC'
                if isinstance(payment_amount, float):
                    pay_receive = cls._get_pay_receive_description(payment_amount, bank_abbreviated_name)
                markitwire_reference = settlement_data[cls.MARKITWIRE_TRADE_REFERENCE_COLUMN]
                counterparty_reference = settlement_data[cls.COUNTERPARTY_TRADE_REFERENCE_COLUMN]
                amendment_reason = settlement_data[cls.AMENDMENT_REASON]
                summary_data = dict()
                summary_data[cls.BANK_TRADE_REFERENCE_COLUMN] = reference
                summary_data[cls.COUNTERPARTY_COLUMN] = counterparty_name
                summary_data[cls.PAY_DATE_COLUMN] = payment_date
                summary_data[cls.PAY_RECEIVE_COLUMN] = pay_receive
                summary_data[cls.CURRENCY_COLUMN] = currency
                summary_data[cls.PAY_AMOUNT_COLUMN] = payment_amount
                summary_data[cls.MARKITWIRE_TRADE_REFERENCE_COLUMN] = markitwire_reference
                summary_data[cls.COUNTERPARTY_TRADE_REFERENCE_COLUMN] = counterparty_reference
                if amendment_reason is not None:
                    summary_data[cls.AMENDMENT_REASON] = amendment_reason
                amended_summary_data_by_key[summary_key] = summary_data
        return amended_summary_data_by_key.values()

    @classmethod
    def _write_summary_heading(cls, worksheet, row_index, column_index, instrument_type, from_date, to_date, is_amended,
            formats):
        """
        Write the pre-settlement advice summary heading.
        """
        bold_text_format = formats[cls.BOLD_TEXT_FORMAT]
        heading = ""
        if is_amended:
            heading = "Amended "
        heading += "{instrument_type_description} Pre-settlement Advice Summary for {from_date} to {to_date}".format(
            instrument_type_description=PreSettlementAdviceGeneral.get_instrument_type_description(instrument_type),
            from_date=from_date,
            to_date=to_date
        )
        worksheet.write(row_index, column_index, heading, bold_text_format)

    @classmethod
    def _write_amendment_summary_heading(cls, worksheet, row_index, column_index, formats):
        """
        Write the pre-settlement advice amendment summary heading.
        """
        bold_text_format = formats[cls.BOLD_TEXT_FORMAT]
        heading = "Amendment Summary"
        worksheet.write(row_index, column_index, heading, bold_text_format)

    @classmethod
    def _get_pay_receive_description(cls, payment_amount, bank_abbreviated_name):
        """
        Get a description of whether the bank is paying or receiving
        the specified amount.
        """
        pay_receive = '{bank_name} Pays' if payment_amount < 0 else '{bank_name} Receives'
        return pay_receive.format(
            bank_name=bank_abbreviated_name
        )

    @classmethod
    def _add_details_worksheet(cls, workbook, instrument_type, from_date, to_date, is_amended, settlements_data,
            formats):
        """
        Add the Details worksheet to the pre-settlement advice Excel
        XLSX workbook.
        """
        worksheet = workbook.add_worksheet('Details')
        current_row_index = 0
        # Write current settlements detail table.
        # Write heading.
        cls._write_details_heading(worksheet, current_row_index, 0, instrument_type, from_date, to_date, is_amended,
            formats)
        current_row_index += 2
        current_detail_data = cls._get_current_settlements_data(settlements_data)
        if len(current_detail_data) > 0:
            # Write current settlements detail table.
            cls._sort_settlements_data(current_detail_data)
            current_detail_column_definitions = cls._get_current_detail_column_definitions(instrument_type)
            cls._write_table(worksheet, current_row_index, 0, current_detail_column_definitions, current_detail_data,
                formats)
            current_row_index = current_row_index + len(current_detail_data) + 3
        if is_amended:
            # Write amended settlements detail table.
            # Write heading.
            cls._write_amendment_details_heading(worksheet, current_row_index, 0, formats)
            amended_detail_data = cls._get_amended_settlements_data(settlements_data)
            cls._sort_settlements_data(amended_detail_data)
            current_row_index += 2
            # Write table.
            amended_detail_column_definitions = cls._get_amended_detail_column_definitions(instrument_type)
            cls._write_table(worksheet, current_row_index, 0, amended_detail_column_definitions, amended_detail_data,
                formats)

    @classmethod
    def _get_current_detail_column_definitions(cls, instrument_type):
        """
        Get current detail column definitions.
        """
        if instrument_type in ['CurrSwap', 'Swap']:
            return cls._get_swap_current_detail_column_definitions()
        elif instrument_type == 'FRA':
            return cls._get_fra_current_detail_column_definitions()
        raise ValueError("Unsupported instrument type specified.")

    @classmethod
    def _get_swap_current_detail_column_definitions(cls):
        """
        Get current detail column definitions for Swaps.
        """
        # Ordered dict defining order and properties of summary columns.
        column_definitions = collections.OrderedDict()
        column_definitions[cls.BANK_TRADE_REFERENCE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.COUNTERPARTY_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.CURRENCY_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.NOMINAL_COLUMN] = {
            'type': 'Monetary',
            'width': 20
        }
        column_definitions[cls.PAY_TYPE_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.TRADE_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.EFFECTIVE_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.TERMINATION_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_BUS_DAY_CONVENTION_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_CALENDARS_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_AMOUNT_COLUMN] = {
            'type': 'Monetary',
            'width': 20
        }
        column_definitions[cls.FLOAT_RATE_REF_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.FLOAT_RATE_COLUMN] = {
            'type': 'Rate',
            'width': 12
        }
        column_definitions[cls.FIXED_RATE_COLUMN] = {
            'type': 'Rate',
            'width': 12
        }
        column_definitions[cls.SPREAD_COLUMN] = {
            'type': 'Rate',
            'width': 12
        }
        column_definitions[cls.RESET_CALENDARS_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.DAYS_COLUMN] = {
            'width': 10
        }
        column_definitions[cls.FIXING_OFFSET_COLUMN] = {
            'width': 10
        }
        column_definitions[cls.DAY_COUNT_CONVENTION_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.ROLLING_PERIOD_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.RESET_BUS_DAY_CONVENTION_COLUMN] = {
            'width': 15
        }
        return column_definitions

    @classmethod
    def _get_fra_current_detail_column_definitions(cls):
        """
        Get current detail column definitions for FRAs.
        """
        # Ordered dict defining order and properties of summary columns.
        column_definitions = collections.OrderedDict()
        column_definitions[cls.BANK_TRADE_REFERENCE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.COUNTERPARTY_COLUMN] = {
            'width': 20
        }
        column_definitions[cls.CURRENCY_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.NOMINAL_COLUMN] = {
            'type': 'Monetary',
            'width': 20
        }
        column_definitions[cls.PAY_TYPE_COLUMN] = {
            'width': 12
        }
        column_definitions[cls.TRADE_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.EFFECTIVE_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.TERMINATION_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_DATE_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_BUS_DAY_CONVENTION_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_CALENDARS_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.PAY_AMOUNT_COLUMN] = {
            'type': 'Monetary',
            'width': 20
        }
        column_definitions[cls.FLOAT_RATE_REF_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.FLOAT_RATE_COLUMN] = {
            'type': 'Rate',
            'width': 12
        }
        column_definitions[cls.FIXED_RATE_COLUMN] = {
            'type': 'Rate',
            'width': 12
        }
        column_definitions[cls.RESET_CALENDARS_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.DAYS_COLUMN] = {
            'width': 10
        }
        column_definitions[cls.FIXING_OFFSET_COLUMN] = {
            'width': 10
        }
        column_definitions[cls.DAY_COUNT_CONVENTION_COLUMN] = {
            'width': 15
        }
        column_definitions[cls.RESET_BUS_DAY_CONVENTION_COLUMN] = {
            'width': 15
        }
        return column_definitions

    @classmethod
    def _get_current_settlements_data(cls, settlements_data):
        """
        Get the current settlements data.
        """
        current_settlements_data = list()
        for settlement_data in settlements_data:
            if settlement_data[cls.AMENDMENT_ACTION] not in [AmendmentActions.REMOVED]:
                current_settlements_data.append(settlement_data)
        return current_settlements_data

    @classmethod
    def _get_amended_detail_column_definitions(cls, instrument_type):
        """
        Get amended detail column definitions.
        """
        column_definitions = cls._get_current_detail_column_definitions(instrument_type)
        column_definitions[cls.AMENDMENT_REASON] = {
            'width': 15
        }
        return column_definitions

    @classmethod
    def _get_amended_settlements_data(cls, settlements_data):
        """
        Get the amended settlements data.
        """
        amended_settlements_data = list()
        for settlement_data in settlements_data:
            if settlement_data[cls.AMENDMENT_ACTION] is not None:
                amended_settlements_data.append(settlement_data)
        return amended_settlements_data

    @classmethod
    def _sort_settlements_data(cls, settlements_data):
        """
        Sort the settlements data in order in which it should be
        displayed.
        """
        # Sort by Pay Date ASC, Currency DESC, Bank Ref ASC.
        settlements_data.sort(key=lambda x: int(x[cls.BANK_TRADE_REFERENCE_COLUMN]))
        settlements_data.sort(key=lambda x: x[cls.CURRENCY_COLUMN], reverse=True)
        settlements_data.sort(key=lambda x: x[cls.PAY_DATE_COLUMN])

    @classmethod
    def _write_details_heading(cls, worksheet, row_index, column_index, instrument_type, from_date, to_date, is_amended,
            formats):
        """
        Write the pre-settlement advice detail heading.
        """
        bold_text_format = formats[cls.BOLD_TEXT_FORMAT]
        heading = ""
        if is_amended:
            heading = "Amended "
        heading += "{instrument_type_description} Pre-settlement Advice Details for {from_date} to {to_date}".format(
            instrument_type_description=PreSettlementAdviceGeneral.get_instrument_type_description(instrument_type),
            from_date=from_date,
            to_date=to_date
        )
        worksheet.write(row_index, column_index, heading, bold_text_format)

    @classmethod
    def _write_amendment_details_heading(cls, worksheet, row_index, column_index, formats):
        """
        Write the pre-settlement advice amendment detail heading.
        """
        bold_text_format = formats[cls.BOLD_TEXT_FORMAT]
        heading = "Amendment Details"
        worksheet.write(row_index, column_index, heading, bold_text_format)

    @classmethod
    def _add_settlement_instructions_worksheet(cls, workbook, settlement_instruction_data_by_currency,
            bank_abbreviated_name, formats):
        """
        Add the Settlement Instructions worksheet to the pre-settlement
        advice Excel XLSX workbook.
        """
        worksheet = workbook.add_worksheet('Settlement Instructions')
        current_row_index = 0
        # Write heading.
        bold_text_format = formats[cls.BOLD_TEXT_FORMAT]
        heading = "{bank_abbreviated_name} Bank Settlement Instructions".format(
            bank_abbreviated_name=bank_abbreviated_name
        )
        worksheet.write(current_row_index, 0, heading, bold_text_format)
        # Write table.
        row_names = [
            cls.BENEFICIARY_BANK_NAME,
            cls.BENEFICIARY_BANK_BIC,
            cls.ACCOUNT_NUMBER_COLUMN,
            cls.CORRESPONDENT_BANK_NAME,
            cls.CORRESPONDENT_BANK_BIC
        ]
        current_row_index += 2
        current_column_index = 0
        starting_row_index = current_row_index
        table_header_format = formats[cls.TABLE_HEADER_FORMAT]
        table_data_default_format = formats[cls.TABLE_DATA_DEFAULT_FORMAT]
        # Write currency headers.
        for row_name in row_names:
            current_row_index += 1
            worksheet.write(current_row_index, current_column_index, row_name, table_header_format)
        # Write currency settlement instruction columns.
        currencies = sorted(settlement_instruction_data_by_currency.keys(), reverse=True)
        for currency in currencies:
            current_column_index += 1
            current_row_index = starting_row_index
            worksheet.write(current_row_index, current_column_index, currency, table_header_format)
            settlement_instruction_data = settlement_instruction_data_by_currency[currency]
            for row_name in row_names:
                current_row_index += 1
                cell_value = settlement_instruction_data[row_name]
                if isinstance(cell_value, type(None)):
                    worksheet.write_blank(current_row_index, current_column_index, cell_value,
                        table_data_default_format)
                else:
                    worksheet.write_string(current_row_index, current_column_index, cell_value,
                        table_data_default_format)
        current_row_index += 2
        message = "To ensure straight through processing of your payment; kindly comply with below:"
        worksheet.write_string(current_row_index, 0, message)
        current_row_index += 1
        message = "* If paying via a bank to bank transfer; please ensure you quote our account number in field 58"
        worksheet.write_string(current_row_index, 0, message)
        current_row_index += 1
        message = "* If paying via a customer to bank transfer; please ensure you quote our account number in field 59"
        worksheet.write_string(current_row_index, 0, message)
        # Set column widths.
        worksheet.set_column(0, 0, 25)
        worksheet.set_column(1, len(currencies), 20)

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
                    summary_column = column_definitions[column_name]
                    cell_format = table_data_default_format
                    if 'type' in summary_column.keys():
                        column_type = summary_column['type']
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
            summary_column = column_definitions[column_name]
            worksheet.set_column(column_index, column_index, summary_column['width'])

    @staticmethod
    def _iso_date_string_to_datetime(iso_date_string):
        """
        Convert a string date in ISO format to a datetime object.
        """
        return datetime.datetime.strptime(iso_date_string, '%Y-%m-%d')
