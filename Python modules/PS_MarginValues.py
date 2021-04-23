'''
Created on 13 May 2013

@author: conicova
Offers the possibility to add time-series values by 
loading data from a CSV file. 
'''
import acm, csv, FRunScriptGUI
from collections import namedtuple
from datetime import datetime

from PS_Functions import getCallAccounts
from at_logging import bp_start, getLogger
import at_timeSeries as at_ts


LOGGER = getLogger(__name__)

SYS_GROUPS = ['Integration Process']

MarginCheckResult = namedtuple("MarginCheckResult", ["MarginFound", "MarginAlreadyGenerated"])


def get_call_accounts(counterparty):
    call_accs = getCallAccounts(counterparty)
    call_accs_zar = [ca for ca in call_accs if ca.Currency().Name() == 'ZAR']
    return call_accs_zar


def _check_margin(date, check_margin, ts_name, margin_account):
    if check_margin not in ("Yes", "No"):
        raise Exception("Unexpected check_margin value '{0}'. Expecting 'Yes'/'No'".format(check_margin))
    
    margin_found = True
    margin_already_generated = False
    if check_margin == "Yes":
        margin_found = False
        ts_data = at_ts.get_time_series_values(ts_name, recaddr=margin_account.Oid(), date=date)
        for ts in ts_data:
            margin_found = True
            if ts.UpdateUser().UserGroup().Name() in SYS_GROUPS:
                margin_already_generated = True
            break
    
    result = MarginCheckResult(margin_found, margin_already_generated)
    LOGGER.debug("Check margin: margin found: %s, margin already generated: %s",
                 result.MarginFound, result.MarginAlreadyGenerated)
    return result

def check_margin(counterparty, date, checkEqMargin, checkFiMargin, checkCreditMargin='No'):

    callAccounts = get_call_accounts(counterparty)
    if len(callAccounts) > 1:
        LOGGER.warning("Expecting only one ZAR call account, using first in list")
    marginAccount = callAccounts.pop()

    results = []
    
    results.append(_check_margin(date, checkEqMargin, 'PS_Margin_Equity', marginAccount))
    results.append(_check_margin(date, checkFiMargin, 'PS_Margin_FI', marginAccount))
    results.append(_check_margin(date, checkCreditMargin, 'PS_Margin_Credit', marginAccount))
    
    return (all(map(lambda i: i.MarginFound, results)),
            all(map(lambda i: i.MarginAlreadyGenerated, results)))

def _touch_margin(date, check_margin, ts_name, margin_account):
    LOGGER.debug("Touching margin: Name: %s, check margin: %s, margin account: %s",
                 ts_name, check_margin, margin_account.Oid())
    if check_margin not in ("Yes", "No"):
        raise Exception("Unexpected check_margin value '{0}'. Expecting 'Yes'/'No'".format(check_margin))
    if check_margin == "Yes":
        ts_data = at_ts.get_time_series_values(ts_name, recaddr=margin_account.Oid(), date=date)
        for ts in ts_data:
            ts.Touch()
            ts.Commit()
            break

def touch_margin(counterparty, date, check_eq_margin, check_fi_margin, check_credit_margin='No'):
    """Touch the margin TimeSeries for the given counterparty and date."""
    call_accounts = get_call_accounts(counterparty)
    if len(call_accounts) > 1:
        LOGGER.warning("Expecting only one ZAR call account, using first in list.")
    if not call_accounts:
        LOGGER.warning("No ZAR call account retrieved for counterparty %s.", counterparty.Name())
        return
        
    margin_account = call_accounts.pop()
    _touch_margin(date, check_eq_margin, 'PS_Margin_Equity', margin_account)
    _touch_margin(date, check_fi_margin, 'PS_Margin_FI', margin_account)
    _touch_margin(date, check_credit_margin, 'PS_Margin_Credit', margin_account)


def _AddTimeSeriesValue(ts_name, instrument_name, date, run_number, value):
    '''Adds or updates a time-series value.
    '''
    entity = acm.FInstrument[instrument_name]
    
    if not(entity):
        raise Exception("The instrument '{0}' is missing in FA.".format(instrument_name))
    
    date_object = datetime.strptime(date, '%d/%m/%Y')
    date = acm.Time().DateFromYMD(date_object.year, date_object.month, date_object.day)
    
    removed_ts = at_ts.remove_time_series_values(ts_name, entity.Oid(), date, run_number)
    if removed_ts:
        LOGGER.info('Deleted existing %s time-series entries ...', removed_ts)
    
    at_ts.add_time_series_value(ts_name, entity.Oid(), value, date, run_number)
    LOGGER.info('Added: ts_name=%s, instrument=%s, date=%s, run_number=%s, value=%s',
            ts_name, instrument_name, date, run_number, value)

def _ReadCsv(input_path):
    ''' Read the specified CSV file. The file has to contain 4 items per row.
    The first row contains the header.
    Returns a list of tuples. One tuple for each row.
    '''
    result = []
    with open(input_path, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        row_nr = 2
        next(csvreader)  # skip header
        for row in csvreader:
            row_nr += 1
            if len(row) != 4:
                msg = 'The row {0} contains unexpected number of values'.format(row_nr)
                raise  csv.Error(msg)
            result.append((row[0], row[1], row[2], row[3]))
    
    return result
        
def _GetTimeSeriesList():
    ''' Returns the list of timesSeries names
    '''
    return ['PS_Margin_Credit', 'PS_Margin_Equity', 'PS_Margin_FI']

def _get_process_name(ts_name):
    result = "ps.margin.default"
    if ts_name == 'PS_Margin_Credit':
        result = "ps.margin.credit"
    if ts_name == 'PS_Margin_Equity':
        result = "ps.margin.equity"
    if ts_name == 'PS_Margin_FI':
        result = "ps.margin.fi"
    if result == '':
        LOGGER.warning('Unexpected ts_name: %s. Using default process name.', ts_name)
        result = "ps.margin.default"
        
    return result

fileSelection = FRunScriptGUI.InputFileSelection()
fileSelection.FileFilter('CSV Files (*.csv)|*.csv')

ael_variables = [('ts_name', 'Time Series Name:', 'string', _GetTimeSeriesList(), ''),
                ('input_path', 'File Path', fileSelection, None,
                  r'c:\tmp', 0, 1, None, None, 1)
                ]
                
def ael_main(dict):
    
    show_dialog = acm.GetFunction('msgBox', 3)

    ts_name = dict['ts_name']
    if ts_name == '':
        show_dialog("Warning", "Please select one of the provided time series name!", 0)       
        return
    
    input_path = str(dict['input_path'])
        
    if input_path == '':
       show_dialog("Warning", "Please enter a valid input file path!", 0)       
       return

    with bp_start(_get_process_name(ts_name), ael_main_args=dict):
        LOGGER.info('Reading CSV file')
        try:
            input_values = _ReadCsv(input_path)
        except Exception as ex:
            LOGGER.exception('Could not read the csv')
            show_dialog("Error", ex, 0)  
            return
         
        LOGGER.info('Adding values to TimeSeries')
       
        current_item = None
        try:
            for instrument_name, day, run_number, value in input_values:
                current_item = (instrument_name, day, run_number, value)
                _AddTimeSeriesValue(ts_name, instrument_name, day, run_number, value)
        except Exception as ex:
            LOGGER.exception("Could not add the value '%s' to the time series", current_item)
            ex_msg = "{0}: '{1}'".format(ex, current_item)
            show_dialog("Error", ex_msg, 0)  
            return 
