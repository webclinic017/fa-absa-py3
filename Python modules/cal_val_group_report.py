"""-----------------------------------------------------------------------------
PURPOSE              :  Instrument val group amendments extract based on raw CAL 
                        data
REQUESTER            :  James Jackson, PCT
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-08-17  CHG0119882     Libor Svoboda       Initial implementation
"""
import csv
import datetime
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import acm_date
from cal_util import Output


LOGGER = getLogger(__name__)
VAL_GROUP_FIELD = 'product_chlnbr'
TODAY = acm.Time.DateToday()
DATES = {
    'Yesterday': acm.Time.DateAddDelta(TODAY, 0, 0, -1),
    'Custom Date': TODAY,
    'Now': TODAY,
}
ENTITY_COLS = (
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
    'SourceID',
    'SourceOperation',
)
AMENDMENT_COLS = (
    'OriginalValue',
    'NewValue',
)


def enable_custom_date(ael_input, custom_date_var):
    """Hook enabling custom date."""
    custom_date = ael_variables.get(custom_date_var)
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = TODAY


ael_variables = AelVariableHandler()
ael_variables.add(
    'report_date',
    label='Report Date',
    collection=list(DATES.keys()),
    default='Now',
    cls='string',
    hook=lambda x: enable_custom_date(x, 'report_date_custom'),
)
ael_variables.add(
    'report_date_custom',
    label='Custom Report Date',
    cls='date',
)
ael_variables.add(
    'input_path',
    label='Input path',
    cls='string',
)
ael_variables.add(
    'input_file',
    label='Input File',
    cls='string',
)
ael_variables.add(
    'output_path',
    label='Output path',
    cls='string',
)
ael_variables.add(
    'output_file',
    label='Output File',
    cls='string',
)


def get_path(dir_path, file_name, report_date):
    full_path = os.path.join(dir_path, file_name)
    dt = datetime.datetime(*acm.Time.DateToYMD(report_date))
    return full_path.format(dt)


def write_report(input_path, output_path):
    with open(input_path, 'r') as xml_file:
        xml_string = xml_file.read()
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError:
        LOGGER.warning('Could not parse %s, adding closing tag.' % xml_file)
        root = ET.fromstring(xml_string + Output.close_tag)
    output = []
    for entity in root.findall("Entity/Amendment[FieldName='%s'].." % VAL_GROUP_FIELD):
        amendment = entity.find("Amendment[FieldName='%s']" % VAL_GROUP_FIELD)
        if amendment is None:
            continue
        row = defaultdict(str)
        for item in ENTITY_COLS:
            try:
                value = entity.find(item).text
            except AttributeError:
                LOGGER.exception('Failed to find "%s" attribute.' % item)
                continue
            row[item] = value
        for item in AMENDMENT_COLS:
            try:
                value = amendment.find(item).text
            except AttributeError:
                LOGGER.exception('Failed to find "%s" attribute.' % item)
                continue
            try:
                val_group = acm.FChoiceList[int(value)]
            except ValueError:
                LOGGER.warning('Failed to find a val group, integer expected, got "%s".' % value)
                row[item] = value
                continue
            if val_group:
                row[item] = val_group.Name()
            else:
                LOGGER.warning('Failed to find a val group with ID "%s".' % value)
                row[item] = value
        output.append(row)
    with open(output_path, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ENTITY_COLS + AMENDMENT_COLS)
        writer.writeheader()
        for row in output:
            writer.writerow(row)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    report_date = (acm_date(ael_params['report_date_custom']) 
                       if ael_params['report_date'] == 'Custom Date' 
                       else DATES[ael_params['report_date']])
    input_path = get_path(ael_params['input_path'], 
                          ael_params['input_file'], report_date)
    output_path = get_path(ael_params['output_path'], 
                           ael_params['output_file'], report_date)
    LOGGER.info('Processing %s.' % input_path)
    write_report(input_path, output_path)
    LOGGER.info('Wrote secondary output to: %s' % output_path)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
