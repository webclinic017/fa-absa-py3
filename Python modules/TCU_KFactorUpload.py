"""----------------------------------------------------------------------------
MODULE
    TCU_KFactorUpload

DESCRIPTION
    Date                : 2018-07-26
    Purpose             : Uploads KFactor values from an XLS file
                          for a specific instrument.
                          This script is dependent on at_timeSeries.
    Department and Desk : TCU
    Requester           : Sean Laing
    Developer           : Qaqamba Ntshobane

HISTORY
===============================================================================
Date            Developer               Description
-------------------------------------------------------------------------------
2018-07-26      Qaqamba Ntshobane       The script pulls k factor values from a
                                        given xls file and uploads them to the
                                        KFactor time series.

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import re
import os
import xlrd
import FRunScriptGUI
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_timeSeries import get_time_series_values, add_time_series_value, remove_time_series_values

LOGGER = getLogger()
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
FILE_NAME = 'CILI'
FILE_NAME2 = 'MTMDetailed'
TIME_SERIES_NAME = 'KFactor'
K_FACTOR_DIFF = 1000000000000000000
INSTRUMENTS = ['ZAR/ALBI_NEXT', 'ZAR/ALBI_PREVIOUS', 'ZAR/ALBI_Weights',
               'ZAR/GOVI_NEXT', 'ZAR/GOVI_PREVIOUS', 'ZAR/GOVI_Weights',
               'ZAR/IGOV_NEXT', 'ZAR/IGOV_PREVIOUS', 'ZAR/IGOV_Weights']


def get_ael_variables():
    directory_selection = FRunScriptGUI.DirectorySelection()
    directory_selection.SelectedDirectory(
            r'Y:\Jhb\PCG\Middle Office\Credit\Bond Index Factors&Weights\K Factor')
    variables = AelVariableHandler()
    variables.add('start_date',
                  label='Date',
                  default='Now',
                  alt='Date for which the file should be selected. The date'
                      'should be in the format YYYMMDD (na special characters inbetween)',
                  cls='date')
    variables.add('file_name',
                  label='File name',
                  default=FILE_NAME,
                  collection=(FILE_NAME, FILE_NAME2),
                  alt='File name prefix. Will be followed by the date'
                      'specifieds')
    variables.add('file_path',
                  label='Directory',
                  cls=directory_selection,
                  default=directory_selection,
                  multiple=True,
                  alt='Directory where files will be uploaded from.')
    return variables

ael_variables = get_ael_variables()


def read_k_factors(file_path, date):
    '''Reads k factors from excel file and returns a dict of k factors,
    with index name as dictionary key
    '''
    k_factors = {}

    with xlrd.open_workbook(file_path) as wb:
        '''One of the workbooks has more than one sheet.
        Below finds the sheet by name.
    	'''

        if 'BEASSA TRI' in wb.sheet_names():
            sheet = wb.sheet_by_name('BEASSA TRI')
        else:
            sheet = wb.sheet_by_index(0)

        rows = sheet.nrows
        data_row = 6  # first row with index names
        rows = rows - data_row
        name_column = 1

        date_cell = sheet.cell(4, 2).value
        v_date = str(xlrd.xldate.xldate_as_datetime(date_cell, wb.datemode)).split(' ')[0]
        val_date = re.sub(r'-', r'', v_date)

        index_postfix = 1

        if date <= val_date:
            while data_row < rows:
                sector = str(sheet.cell(data_row, name_column).value)

                if sector == 'ALBI':
                    date_cell = sheet.cell(data_row-2, 2).value
                    val_date = str(xlrd.xldate.xldate_as_datetime(date_cell, wb.datemode)).split(' ')[0]

                elif sector == 'IGOV':
                    date_cell = sheet.cell(data_row-3, 2).value
                    val_date = str(xlrd.xldate.xldate_as_datetime(date_cell, wb.datemode)).split(' ')[0]

                if sector == 'GOVI' or sector == 'IGOV' or sector == 'ALBI':
                    prev_kfactor = round(float(sheet.cell(data_row, 11).value * K_FACTOR_DIFF), 0)
                    next_kfactor = round(float(sheet.cell(data_row, 12).value * K_FACTOR_DIFF), 0)
                    k_factors[sector+str(index_postfix)] = [val_date, prev_kfactor, next_kfactor]

                index_postfix += 1
                data_row += 1
    return k_factors


def upload_k_factors(k_factors):
    '''Uploads K Factors into time series.

    The values read from the XLS files have to be multiplied by 1000000000000000000
    in order before being uploaded into the time series.
    '''

    for index, value in sorted(k_factors.iteritems(), key=lambda (k, v): (v, k)):
        for ins_name in INSTRUMENTS:
            ins = re.split('(\d+)', index)[0]
            k_value = value[2]

            following_date = acm.Time.DateAddDelta(value[0], 0, 0, 1)
            next_recaddr = acm.FInstrument[ins_name].Oid()

            if ins in ins_name and ins_name.endswith('_NEXT'):
                ins = ins_name.split('_')[0]
                prev_recaddr = acm.FInstrument[ins+'_PREVIOUS'].Oid()
                weights_recaddr = acm.FInstrument[ins+'_Weights'].Oid()

                try:
                    next_point = get_time_series_values(TIME_SERIES_NAME, next_recaddr, value[0])[0].TimeValue()
                    prev_point = get_time_series_values(TIME_SERIES_NAME, prev_recaddr, value[0])[0].TimeValue()

                    add_time_series_value(TIME_SERIES_NAME, next_recaddr, k_value, following_date, 0, True)
                    add_time_series_value(TIME_SERIES_NAME, weights_recaddr, k_value, following_date, 0, True)

                    '''if the index_NEXT value of the previous day is the same as the following day's value then
                    all values from the previous day are replicated, otherwise the previous day's index_NEXT becomes
                    the following day's index_PREVIOUS value.
                    '''

                    if k_value == next_point:
                        add_time_series_value(TIME_SERIES_NAME, prev_recaddr, prev_point, following_date, 0, True)
                        break
                    else:
                        add_time_series_value(TIME_SERIES_NAME, prev_recaddr, next_point, following_date, 0, True)
                        break
                except Exception:
                    LOGGER.exception('Failed to update KFactor values. Please make sure '
                                     'that the KFactor values for the previous day exist')
                    return

    LOGGER.info('Successfuly uploaded kfactors onto time series')


def ael_main(dictionary):
    file_path = dictionary['file_path'].SelectedDirectory().Text()
    file_name = dictionary['file_name']
    name_date = dictionary['start_date'].to_string('%Y%m%d')
    file_name = ''.join([file_name, name_date, '.xls'])
    full_path = os.path.join(file_path, file_name)

    try:
        # read k factors from file
        k_factors = read_k_factors(full_path, name_date)
    except Exception:
        LOGGER.exception('Failed to read kfactors from file: %s, no kfactors will be uploaded.', full_path)
        raise

    # upload k factors to time series
    upload_k_factors(k_factors)
