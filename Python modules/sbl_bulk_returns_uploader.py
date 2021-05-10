'''--------------------------------------------------------------------------------------
MODULE
    sbl_bulk_returns_uploader

DESCRIPTION
    Date                : 2020-03-06
    Purpose             : An uploader used to perform bulk partial/full returns on SecurityLoan trades
    Department and Desk : SBL
    Requester           : James Stevens
    Developer           : Khaya Mbebe
    JIRA                : PCGDEV-220

HISTORY
=========================================================================================
Date            JIRA no                 Developer               Description
-----------------------------------------------------------------------------------------
2020-03-06      PCGDEV-220              Khaya Mbebe             Initial implementation.
2020-12-11      PCGDEV-625              Sihle Gaxa              Added trade time rule
                                                                to always be today or 
                                                                in the past

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''

import acm
import os
import xlrd
import datetime
import collections
import DocumentGeneral
import sl_partial_returns

from at_time import acm_date
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    
    """
    ael_variable_handler = AelVariableHandler()
    # Input File Path
    ael_variable_handler._add_file_selection(
        name='input_file_path',
        label='Input File Path',
        input_output='input',
        file_filter='*.xlsx',
        mandatory=True,
        multiple=False,
        alt='The file path of the input party data excel file.'
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()


def ael_main(ael_parameters):
    """
    AEL Main Function
    
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting Partial Return Bulk Upload {start_date_time}'.format(start_date_time=start_date_time))
        input_file_path = ael_parameters['input_file_path'].AsString()
        _validate_input_file_path(input_file_path)
        _book_sl_partial_returns(input_file_path)
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed Partial Return Bulk Upload at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _validate_input_file_path(input_file_path):
    """
    Validate the input file path.
    
    """
    if not os.path.exists(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not exist."
        raise ValueError(exception_message.format(
        ))
    if not os.path.isfile(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not point to a file."
        raise ValueError(exception_message.format(
        ))


def _book_sl_partial_returns(input_file_path):
    """
    From the excel data provided, retrieve SecurityLoan trade number to book either partial or full return against
    
    """
    for trade_data in _get_trade_data_from_workbook(input_file_path):
        _book_partial_return(trade_data)


def _book_partial_return(party_data):
    """
    This function books the partial return
    
    """
    today = acm.Time().DateNow()
    trade_no = str(party_data.Trade.split(".")[0])
    quantity = float(party_data.Quantity)
    trade = acm.FTrade[trade_no]
    return_date = excel_date_to_acmdate(party_data.ReturnDate, trade)
    return_datetime = excel_date_to_acmdate(party_data.return_datetime, trade)
    if return_datetime > today:
        return_datetime = today
    swift_flag = str(party_data.swift_flag)
    
    try:
        return_trade = sl_partial_returns.partial_return(trade, return_date, quantity, return_datetime, swift_flag)
    except ValueError:
        error_message = 'Failed to Create Partial Return For Trade : {trade}, Please check Excel Data'
        LOGGER.warning(error_message.format(trade1=trade.Oid()))
        return None

    if return_trade:
        LOGGER.info('Successful Partial Return Trade : {trade2} from Trade : {trade1}'.format(trade1=trade.Oid(),
                                                                                              trade2=return_trade.Oid()
                                                                                              ))
    return return_trade


def excel_date_to_acmdate(date, trade):
    """
    This function creates an acm date from the date column given in excel
    
    """
    if date.split('.')[1]:
        try:
            normalised_date = acm.Time.AsDate(float(date))
            return acm_date(normalised_date)
        except ValueError:
            message = 'Cannot determine date for trade {trade} . Date {date} should be in format YYYY-mm-dd'
            LOGGER.warning(message.format(trade=trade.Oid(), date=date))
            return
    normalised_date = acm_date(str(date))

    return normalised_date


def _get_trade_data_from_workbook(input_file_path):
    """
    Get a list of trade data objects for the data contained in the
    workbook represented by a specified path.
    
    """
    column_list = _get_workbook_column_list()
    trade_data_class = collections.namedtuple('TradeData', column_list)
    trade_data = list()
    with xlrd.open_workbook(input_file_path) as workbook:
        for sheet in workbook.sheets():
            if sheet.name == 'Clean' or sheet.name == 'Sheet1':
                sheet_party_data = _get_trade_data_from_sheet(trade_data_class,
                                                              sheet, column_list)
                trade_data.extend(sheet_party_data)
    return trade_data


def _get_workbook_column_list():
    """
    Get the list of expected workbook columns required to do a partial/full return.
    The fields are Trade No., Return Date, Return Quantity, Swift Flag and Is Corp Action
    
    """
    return [
            'Trade',
            'ReturnDate',
            'Quantity',
            'return_datetime',
            'swift_flag'
           ]


def _get_trade_data_from_sheet(trade_data_class, sheet, column_list):
    """
    Get a list of trade data objects for the data contained in a
    specified sheet.
    """
    _validate_sheet_columns(sheet, column_list)
    trade_data = list()
    for row_index in range(sheet.nrows):
        if row_index == 0:
            # Skip the header row in excel
            continue
        row_trade_data = _get_trade_data_from_row(trade_data_class, sheet,
                                                  row_index, column_list)
        trade_data.append(row_trade_data)
    return trade_data


def _validate_sheet_columns(sheet, column_list):
    """
    Validate the columns of a specified sheet.
    
    """
    expected_number_of_columns = len(column_list)
    if sheet.ncols != expected_number_of_columns:
        exception_message = "Expecting {expected} workbook columns, {encountered} "
        exception_message += "encountered on sheet '{}'."
        raise ValueError(exception_message.format(
            expected=expected_number_of_columns,
            encountered=sheet.ncols
        ))


def _get_trade_data_from_row(trade_data_class, sheet, row_index, column_list):
    """
    Get trade data object from the data contained in a specified sheet row.
    
    """
    cell_values_by_column_name = {}
    for column_index in range(sheet.ncols):
        column_name = column_list[column_index]
        cell_values_by_column_name[column_name] = str(sheet.cell(row_index, column_index).value)
    return trade_data_class(**cell_values_by_column_name)
