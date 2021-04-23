"""------------------------------------------------------------------------------------------------------------------
PURPOSE                                    : Code is used to convert an xml file into a csv file.
                                             The xml file contains amendments done on trades during the trading day
                                             This was done as part of FtF-14 CAL. 
REQUESTER, DEPARTMENT                      : Nhlanhleni Mchunu, PCT
PROJECT                                    : Fix the Front - CAL
DEVELOPER                                  : Nkosinathi Sikhakhane
-----------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Date            Change no   Developer        Description
------------------------------------------------------------------------------------------------------------------------
2018-09-07        JIRA -> FtF-125            Initial Implementation
2019-02-05  CHG1001325774   Libor Svoboda    Support multiple input files
"""
import xml.etree.ElementTree as ET
import acm
import csv
import os
import datetime
import string
from collections import OrderedDict
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from cal_util import Output



TODAY = acm.Time().DateToday()
DATE_LIST = {
             'Now': TODAY,
             'Custom Date': TODAY,
             }
DATE_KEYS = DATE_LIST.keys()
DATE_KEYS.sort()
LOGGER = getLogger(__name__)

FILE_HEADER = (
    'TradeID',
    'PortfolioID',
    'Portfolio',
    'Instrument',
    'InsType',
    'Currency',
    'Status',
    'Trader',
    'Acquirer',
    'Counterparty',
    'TradeSide',
    'ValueDay',
    'UpdateTime',
    'UpdateUser',
    'AmendReason',
    'CommentType',
    'FairValuePortfolio',
    'PLImpact',
    'CALFlag',
    'SourceType',
    'ExecutionTime',
)

SOURCE_TYPE_MAPPING = {
    'Trade': 'Trade',
    'Payment': 'Trade',
    'Instrument': 'Instrument',
    'Leg': 'Instrument',
    'CashFlow': 'Instrument',
    'Reset': 'Instrument',
}


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')
    cust.value = TODAY

ael_variables = AelVariableHandler()

ael_variables.add('date',
                  label='Date',
                  cls='string',
                  default='Now',
                  collection=DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=('A date for which files will be taken.'))

ael_variables.add('custom_date',
                  label='Custom Date',
                  cls='string',
                  default=TODAY,
                  enabled=False,
                  alt=("Format: '2016-09-30'."))
                  
ael_variables.add("file_dir",
                  label="Directory",
                  default=r"//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/",
                  alt=("A Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))

ael_variables.add('input_files',
                  label = 'Input Files',
                  default = 'CAL_${DATE}.xml',
                  mandatory = True,
                  multiple = True,
                  alt = 'XML files to be converted to csv')

ael_variables.add('output_file',
                  label = 'Output File',
                  default = 'CAL_Report_${DATE}.csv',
                  mandatory = True,
                  multiple = False,
                  alt = 'CSV file generated from the xml file')


class MissingFileException(Exception): pass


def get_file_path(ael_dict, file_name, check_existing=False):

    if not file_name:
        return None

    # date in string
    if ael_dict['date'] == 'Custom Date':
        the_date = ael_dict['custom_date']
    else:
        the_date = DATE_LIST[ael_dict['date']]

    # file date will be converted to "YYYY-mm-dd"
    # directory date will be converted to "YYYY-mm-dd"
    _dt = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    file_date_string = _dt.strftime("%Y-%m-%d")
    dir_date_string = the_date

    # directory in string
    file_dir = ael_dict["file_dir"]
    fdir_template = string.Template(file_dir)
    file_dir = fdir_template.substitute(DATE=dir_date_string)
    # filename in string
    fname_template = string.Template(file_name)
    file_name = fname_template.substitute(DATE=file_date_string)

    if not os.path.isabs(file_name):
        fullpath = os.path.join(file_dir, file_name)
    else:
        fullpath = file_name
        
    if check_existing and not os.path.exists(fullpath):
        LOGGER.error("ERROR: File not found: '%s'" % fullpath)
        raise MissingFileException(fullpath)
    return fullpath


def get_key(row_dict):
    return '%s_%s_%s_%s_%s_%s_%s' % (row_dict['TradeID'], row_dict['UpdateTime'], 
                                     row_dict['UpdateUser'], row_dict['AmendReason'],
                                     row_dict['CommentType'], row_dict['CALFlag'],
                                     row_dict['SourceType'])


def write_data_to_csv(xml_files, csv_file):
    """Write data from xml file to a csv file """
    output = {}
    for xml_file in xml_files:
        with open(xml_file, 'r') as xml_output:
            xml_string = xml_output.read()
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError:
            LOGGER.warning('Could not parse %s, adding closing tag.' % xml_file)
            root = ET.fromstring(xml_string + Output.close_tag)
        
        for trade_tag in root.findall('Entity'):
            items = {}
            for item in FILE_HEADER:
                value = ''
                try:
                    value = trade_tag.find(item).text
                except AttributeError:
                    LOGGER.exception('Failed to find "%s" attribute.' % item)
                
                if item == 'PLImpact':
                    try:
                        items[item] = float(value)
                    except ValueError:
                        items[item] = float('nan')
                elif item == 'SourceType':
                    items[item] = SOURCE_TYPE_MAPPING[value]
                else:
                    items[item] = value
            row_key = get_key(items)
            if row_key in output:
                output[row_key]['PLImpact'] += items['PLImpact']
            else:
                output[row_key] = items
    
    output_ordered = OrderedDict(sorted(output.items(), key=lambda t: t[1]['UpdateTime']))
    with open(csv_file, 'w') as f:
        csvwriter = csv.DictWriter(f, FILE_HEADER, lineterminator='\n')
        csvwriter.writeheader()
        for item in output_ordered.values():
            csvwriter.writerow(item)


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    xml_paths = []
    for input_file in ael_dict['input_files']:
        xml_paths.append(get_file_path(ael_dict, input_file, True))
    csv_path = get_file_path(ael_dict, str(ael_dict['output_file']))
    LOGGER.info('Processing %s.' % ', '.join(xml_paths))
    write_data_to_csv(xml_paths, csv_path)
    LOGGER.info('Created CAL report: %s.' % csv_path)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')

