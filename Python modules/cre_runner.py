"""----------------------------------------------------------------------------
PROJECT                 :  CRE into Front Arena
PURPOSE                 :  This module handles task(s) for calculating and
                           uploading CRE values.
DEPATMENT AND DESK      :  Middle Office, FX Trading
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0003040071
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer         Description
-------------------------------------------------------------------------------
18/02/2018  CHG1000032049 Libor Svoboda     Updated logging, added exception
                                            report and option to delete old TS.

"""
import os
import acm
import cre_calc
import cre_upload
import cre_exc_report
from at_ael_variables import AelVariableHandler
from at_time import acm_date
from at_logging import getLogger


TRADE_INDEX = 0
LOGGER = getLogger('CRE_FA_valuations')


def enable_custom_date(ael_input):
    """Hook enabling custom date."""
    custom_date = ael_variables.get('val_date')
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = acm.Time.DateToday()


def select_ts_history(ael_input):
    """Hook enabling time series history selection."""
    delete_older_than = ael_variables.get('delete_older_than')
    enabled = ael_input.value == '1'
    delete_older_than.enabled = enabled


def enable_trades_tab(ael_input):
    """Hook enabling Trades options."""
    enabled = ael_input.value == '1'
    for var in ael_variables:
        if '_Trades' in var.label and var is not ael_input:
            var.enabled = enabled


def enable_calculations_tab(ael_input):
    """Hook enabling Calculations options."""
    enabled = ael_input.value == '1'
    for var in ael_variables:
        if '_Calculations' in var.label and var is not ael_input:
            var.enabled = enabled


def enable_upload_tab(ael_input):
    """Hook enabling Upload options."""
    enabled = ael_input.value == '1'
    for var in ael_variables:
        if '_Upload' in var.label and var is not ael_input:
            var.enabled = enabled


def enable_report_tab(ael_input):
    """Hook enabling Exception report options."""
    enabled = ael_input.value == '1'
    for var in ael_variables:
        if '_Report' in var.label and var is not ael_input:
            var.enabled = enabled


def validate_column_specs(ael_input):
    """Hook validating column specifications."""
    specs_dict = cre_upload.ColumnSpecs.parse_column_specs(ael_input.value)
    ael_input.value = ', '.join([': '.join([key, str(value)])
                                 for key, value in specs_dict.items()])


ael_variables = AelVariableHandler()
# General tab
ael_variables.add(
    'date_selection',
    label='Valuation Date_General',
    collection=['Date Today', 'Custom Date'],
    default='Date Today',
    cls='string',
    hook=enable_custom_date,
    alt='Choose between Custom Date and Date Today.'
)

ael_variables.add(
    'val_date',
    label='Custom Date_General',
    cls='date',
    default=acm.Time.DateToday(),
    alt='Custom valuation date.'
)

ael_variables.add(
    'save_trades',
    label='Save Trade File_General',
    collection=[0, 1],
    cls='int',
    hook=enable_trades_tab,
)

ael_variables.add(
    'calculate_values',
    label='Calculate Values_General',
    collection=[0, 1],
    cls='int',
    hook=enable_calculations_tab,
)

ael_variables.add(
    'upload_values',
    label='Upload Values_General',
    collection=[0, 1],
    cls='int',
    hook=enable_upload_tab,
)

ael_variables.add(
    'exception_report',
    label='Generate Exception report_General',
    collection=[0, 1],
    cls='int',
    hook=enable_report_tab,
)

ael_variables.add(
    'delete_ts',
    label='Delete TS Values_General',
    collection=[0, 1],
    cls='int',
    hook=select_ts_history,
)

ael_variables.add(
    'delete_older_than',
    label='Older than_General',
    default='-7d',
    cls='string',
)

# Trades tab
ael_variables.add(
    'val_group',
    label='ValGroup_Trades',
    cls='FChoiceList',
    default='',
    alt='Val Group specifying instruments for CRE valuation.'
)

ael_variables.add(
    'ext_val_trades',
    label='Include ExternalVal trades_Trades',
    collection=[0, 1],
    cls='int',
    alt='Include trades with ExternalVal add info value.'
)

ael_variables.add(
    'additional_trades',
    label='Additional Trades_Trades',
    cls='FTrade',
    mandatory=False,
    multiple=True,
    alt='Specific trades to be valued.'
)

ael_variables.add(
    'trade_file',
    label='Trade File Name_Trades',
    cls='string',
    default='',
    alt='CRE CalculationRunner input trade file.'
)

ael_variables.add(
    'trade_dir',
    label='Trade Directory_Trades',
    cls='string',
    default='',
    alt='CRE CalculationRunner trade input directory.'
)

# Calculations tab
ael_variables.add(
    'wsdl',
    label='CalculationRunner WSDL_Calculations',
    cls='string',
    default='',
    alt='CRE CalculationRunner WSDL file.'
)

ael_variables.add(
    'risk',
    label='Risk_Calculations',
    cls='string',
    default='Front',
    alt='CRE CalculationRunner risk type.'
)

ael_variables.add(
    'error_file',
    label='Error File Name_Calculations',
    cls='string',
    default='',
    mandatory=0,
    alt='CRE CalculationRunner error file.'
)

ael_variables.add(
    'error_dir',
    label='Error Directory_Calculations',
    cls='string',
    default='',
    mandatory=0,
    alt='CRE CalculationRunner error output directory.'
)

# Upload tab
ael_variables.add(
    'cre_file',
    label='CRE File_Upload',
    cls='string',
    default='',
    alt='CRE CalculationRunner output file.'
)
    
ael_variables.add(
    'cre_dir',
    label='CRE Directory_Upload',
    cls='string',
    default='',
    alt='CRE CalculationRunner output directory.'
)

ael_variables.add(
    'satisfied_by_qf',
    label='Satisfied by QF_Upload',
    alt='Trade value is only uploaded if the trade is selected by this QF.',
    cls=acm.FStoredASQLQuery,
    collection=acm.FStoredASQLQuery.Select("subType='FTrade'"),
    mandatory=0
)

ael_variables.add(
    'ts_specs',
    label='Time Series Columns_Upload',
    cls='string',
    default='',
    hook=validate_column_specs,
    alt=("Specification of time series names and corresponding csv columns of "
         "the CRE file in the form 'name:column' separated by comma.")
)

ael_variables.add(
    'ts_no_scaling',
    label='Columns w/o Scaling_Upload',
    cls='string',
    default='',
    multiple=True,
    mandatory=0,
    alt='Names of above time series whose values should not be scaled.'
)

ael_variables.add(
    'currency_specs',
    label='Currency Columns_Upload',
    cls='string',
    default='',
    mandatory=0,
    hook=validate_column_specs,
    alt=("Specification of currency codes and corresponding csv columns of "
         "the CRE file in the form 'code:column' separated by comma.")
)

# Report tab
ael_variables.add(
    'mail_list',
    label='Emails_Report',
    #default='PrimeServicesPCG@barclayscapital.com',
    multiple=True,
    mandatory=False,
)


def get_file_path(directory, file_name, date, create_dir=False):
    """Return complete path to a file."""
    file_path = os.path.join(directory, file_name)
    file_path = file_path.replace('YYYYMMDD', date.replace('-', ''))
    file_path = file_path.replace('YYYY-MM-DD', date)
    if create_dir:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
    return file_path


def get_val_date(ael_params):
    """Return valuation date."""
    if ael_params['date_selection'] == 'Date Today':
        return acm.Time.DateToday()
    return acm_date(ael_params['val_date'])


def generate_trade_file(ael_params, save_file=True):
    """Generate trade file and return the trade numbers."""
    val_date = get_val_date(ael_params)
    trade_path = get_file_path(ael_params['trade_dir'],
                               ael_params['trade_file'], val_date, True)
    val_group = ael_params['val_group']
    ext_val_trades = ael_params['ext_val_trades']
    additional_trades = ael_params['additional_trades']
    file_generator = cre_calc.TradeFileGenerator(val_group, ext_val_trades,
                                                 additional_trades)
    if save_file:
        file_generator.save_file(trade_path)
    requested_trade_numbers = file_generator.get_trade_numbers()
    return requested_trade_numbers
    

def calculate_values(ael_params):
    """Calculate CRE values."""
    wsdl = ael_params['wsdl']
    val_date = get_val_date(ael_params)
    risk = ael_params['risk']
    error_path = get_file_path(ael_params['error_dir'],
                               ael_params['error_file'], val_date)
    calc_runner = cre_calc.CalculationRunner(wsdl, val_date, risk, error_path)
    calc_runner.run()


def upload_values(ael_params):
    """Upload CRE values to Front Arena time series 
    and return processed trade numbers."""
    val_date = get_val_date(ael_params)
    trade_qf = ael_params['satisfied_by_qf']
    cre_path = get_file_path(ael_params['cre_dir'],
                             ael_params['cre_file'], val_date)
    column_specs = cre_upload.ColumnSpecs(TRADE_INDEX,
                                          ael_params['ts_specs'],
                                          ael_params['ts_no_scaling'],
                                          ael_params['currency_specs'])
    file_processor = cre_upload.FileProcessor(cre_path, val_date,
                                              column_specs, trade_qf)
    file_processor.run()
    processed_trade_numbers = file_processor.get_trade_numbers()
    return processed_trade_numbers


def delete_ts_values(ts_name, to_date):
    ts_spec = acm.FTimeSeriesDvSpec[ts_name]
    if ts_spec:
        query = "timeSeriesDvSpecification=%s and storageDate<='%s'" % (
                    ts_spec.Oid(), to_date)
        ts_vals = acm.FTimeSeriesDv.Select(query)
        count = len(ts_vals)
        for ts in ts_vals[:]:
            ts.Delete()
        LOGGER.info('Deleted %s %s values older than %s.' % (count, ts_name, to_date))


def delete_old_values(ael_params):
    """Delete old time series values."""
    ts_spec = cre_upload.ColumnSpecs.parse_column_specs(ael_params['ts_specs'])
    ts_names = list(ts_spec.keys())
    val_date = get_val_date(ael_params)
    delete_period = ael_params['delete_older_than']
    try:
        to_date = acm.Time.DateAdjustPeriod(val_date, delete_period)
    except Exception as exc:
        LOGGER.error('Failed to delete old time series: %s' % str(exc))
        return
    for ts_name in ts_names:
        delete_ts_values(ts_name, to_date)


def generate_exception_report(ael_params, requested, processed):
    recipients = ael_params['mail_list']
    val_date = get_val_date(ael_params)
    report = cre_exc_report.EmailReport(recipients, requested, 
                                        processed, val_date)
    report.create_report()
    report.send_report()


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    
    LOGGER.info('Starting CRE runner.')
    requested_trade_numbers = []
    if ael_params['save_trades']:
        requested_trade_numbers = generate_trade_file(ael_params)
    
    if ael_params['calculate_values']:
        calculate_values(ael_params)
    
    processed_trade_numbers = []
    if ael_params['upload_values']:
        processed_trade_numbers = upload_values(ael_params)
        if ael_params['exception_report']:
            if not requested_trade_numbers:
                requested_trade_numbers = generate_trade_file(ael_params, False)
            generate_exception_report(ael_params, requested_trade_numbers, 
                                      processed_trade_numbers)
    
    if ael_params['delete_ts']:
        delete_old_values(ael_params)
    
    LOGGER.info('CRE runner finished.')
