"""-----------------------------------------------------------------------------
PURPOSE              :  SBL amendment process to record all Trade, Instrument, 
                        and Settlement updates done by the OPS SecLend and 
                        PCG Collateral user groups.
REQUESTER, DEPATMENT :  Jennitha Jugnath, PTS
PROJECT              :  SBL onto FA
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-05-26  CHG0102232     Libor Svoboda       Initial implementation
"""
import csv
import datetime
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

import acm
from at_ael_variables import AelVariableHandler
from at_ats_utils import XmlOutput
from at_logging import getLogger
from at_time import acm_date


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
YESTERDAY = acm.Time.DateAddDelta(TODAY, 0, 0, -1)
DATE_CHOICES = {
    'Custom Date': TODAY,
    'Date Today': TODAY,
    'Yesterday': YESTERDAY,
}
COLUMNS = (
    'Object Type',
    'Object ID',
    'Instrument',
    'InsType',
    'Operation',
    'Update Time',
    'Update User',
    'User Group',
    'Underlying',
    'Counterparty',
    'Amended Object Type',
    'Amended Object ID',
    'Amended Object Operation',
    'Amended Field',
    'Original Value',
    'New Value',
)
MAPPING_ENTITY = {
    'Object Type': 'ObjectType',
    'Object ID': 'ObjectID',
    'Operation': 'Operation',
    'Update Time': 'UpdateTime',
    'Update User': 'UpdateUser',
    'User Group': 'UpdateUserGroup',
    'Instrument': 'Instrument',
    'InsType': 'InsType',
    'Underlying': 'Underlying',
    'Counterparty': 'Counterparty',
}
MAPPING_AMENDMENT = {
    'Amended Object Type': 'TableName',
    'Amended Object ID': 'Oid',
    'Amended Object Operation': 'Operation',
}
MAPPING_FIELD = {
    'Amended Field': 'FieldName',
    'Original Value': 'OriginalValue',
    'New Value': 'NewValue',
}


def enable_custom_date(ael_input, custom_date_var):
    custom_date = ael_variables.get(custom_date_var)
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = TODAY


ael_variables = AelVariableHandler()
ael_variables.add(
    'run_date',
    label='Run Date',
    collection=list(DATE_CHOICES.keys()),
    default='Date Today',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'run_date_custom'),
)
ael_variables.add(
    'run_date_custom',
    label='Custom Run Date',
    cls='date',
)
ael_variables.add(
    'input_dir',
    label='Input Directory',
    default='/services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment',
)
ael_variables.add(
    'input_file',
    label='Input File',
    default='SBL_Amendments_{:%Y-%m-%d}.xml',
)
ael_variables.add(
    'output_dir',
    label='Output Directory',
    default='/services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment',
)
ael_variables.add(
    'output_file',
    label='Output File',
    default='SBL_Amendments_Report_{:%Y-%m-%d}.csv',
)


def write_data_to_csv(xml_path, csv_path):
    output = []
    with open(xml_path, 'r') as xml_output:
        xml_string = xml_output.read()
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError:
        LOGGER.warning('Could not parse %s, adding closing tag.' % xml_path)
        root = ET.fromstring(xml_string + Output.close_tag)
    for entity in root.findall('Entity'):
        entity_dict = defaultdict(str)
        for csv_col, xml_tag in MAPPING_ENTITY.items():
            entity_dict[csv_col] = entity.find(xml_tag).text
        amendments = entity.findall('Amendment')
        if not len(amendments):
            output.append(entity_dict)
            continue
        for amendment in amendments:
            amendment_dict = defaultdict(str)
            amendment_dict.update(entity_dict)
            for csv_col, xml_tag in MAPPING_AMENDMENT.items():
                amendment_dict[csv_col] = amendment.find(xml_tag).text
            fields = amendment.findall('Field')
            if not len(fields):
                output.append(amendment_dict)
                continue
            for field in fields:
                field_dict = defaultdict(str)
                field_dict.update(amendment_dict)
                for csv_col, xml_tag in MAPPING_FIELD.items():
                    field_dict[csv_col] = field.find(xml_tag).text
                output.append(field_dict)
    with open(csv_path, 'wb') as csvfile:
        csvwriter = csv.DictWriter(csvfile, COLUMNS)
        csvwriter.writeheader()
        for row in output:
            csvwriter.writerow(row)


def get_date(params, param_name):
    date_choice = params[param_name]
    if date_choice == 'Custom Date':
        return acm_date(params[param_name + '_custom'])
    return DATE_CHOICES[date_choice]


def get_path(folder, file_name, run_date):
    path = os.path.join(folder, file_name)
    dt = datetime.datetime(*acm.Time.DateToYMD(run_date))
    return path.format(dt)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    run_date = get_date(ael_params, 'run_date')
    input_path = get_path(ael_params['input_dir'], ael_params['input_file'], run_date)
    output_path = get_path(ael_params['output_dir'], ael_params['output_file'], run_date)
    LOGGER.info('Processing %s' % input_path)
    write_data_to_csv(input_path, output_path)
    LOGGER.info('Wrote secondary output to: %s' % output_path)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
