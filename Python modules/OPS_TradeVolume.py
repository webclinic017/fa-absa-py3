'''
#   Desk        Requester               Developer               CR Number
#   What
# =============================================================================
    Ops         Letitia Roux         Andrei Conicov     CHNGXXX (2014-06-23)
    Ops MI      Manabeng Makaba      Fancy Dire         CNHGXXX (2014-09-11)
    Ops         Letitia Roux         Andrei Conicov     CHNG0002341674 (2014-10-09)
'''

import TradeBucketGUI
import acm, ael
from at_ael_variables import AelVariableHandler
import csv
import datetime
import os

import FMacroGUI


_ALL_ASQL = 'All OPS_TradeVolume'

directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory('C:/')
ael_gui_parameters = {'windowCaption':'OPS Trade Volume'}
trade_volume_asql = map(lambda x: x.Name(), 
                        acm.FSQL.Select('name LIKE "OPS_TradeVolume*"'))
asql_queries = []
asql_queries.append(_ALL_ASQL)
asql_queries.extend(trade_volume_asql)

default_name = 'OPS_TradeVolume'

_first_day = ael.date_today().first_day_of_month()

_START_DATE = _first_day.add_months(-1).to_string()
_END_DATE = _first_day.add_days(-1).to_string()

def custom_dates_hook(fieldValues):
    """Input hook for ael_variables"""
    use_custom_dates = ael_variables[2].value == '1'
    ael_variables[3].enabled = use_custom_dates
    ael_variables[4].enabled = use_custom_dates
    ael_variables[1].enabled = not use_custom_dates
    return fieldValues

ael_variables = AelVariableHandler()
ael_variables.add(
    'asql',
    label='ASQL query',
    collection=asql_queries,
    default='OPS_TradeVolume_CM',
    alt='Choose the ASQL query.',
    mandatory=1
    )
ael_variables.add(
    'time_period',
    label='Time period:',
    default='month',
    collection=['day', 'month'],
    alt=('Sets the value of the report period'),
    mandatory=1
    )
ael_variables.add(
    'custom_dates',
    label='Custom dates',
    collection=[0, 1],
    alt='Check this in order to use custom from and to dates',
    cls='int',
    hook=custom_dates_hook
    )
ael_variables.add(
    'start_date',
    label='Date from',
    default=_START_DATE,
    alt=('The minimal date from which the events should occur.'
    'This does not backdate FA'),
    mandatory=1
    )
ael_variables.add(
    'end_date',
    label='Date to',
    default=_END_DATE,
    alt=('The maximal date until which the events should occur.'
    'This does not backdate FA'),
    mandatory=1
    )
ael_variables.add(
    'for_expired_trades',
    label='For expired trades:',
    default='no',
    collection=['yes', 'no'],
    alt=('Sets the value of the ASQL parameter 3_ForExpiredTrades'),
    mandatory=1
    )
ael_variables.add(
    'output_directory',
    label='Output Directory',
    cls=directorySelection,
    default=directorySelection,
    alt='The directory where the report(s) will be generated.',
    mandatory=0,
    multiple=1
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='OPS_TradeVolume',
    alt='The file name',
    mandatory=0
    )

def _generate_report(asql, start_date, end_date, for_expired_trades, full_path):
    """ Generate the report with the specified parameters
    """
    # get the query text and macros
    query_text = acm.FSQL[asql].Text()
    macros = FMacroGUI.searchMacros(query_text)
    bindings = {'1_StartDate': start_date,
                '2_EndDate': end_date,
                '3_ForExpiredTrades': for_expired_trades}

    # fill the params
    macro_list, value_list = FMacroGUI.mapMacros(bindings, macros)

    # run the query
    res = ael.asql(query_text, 0, macro_list, value_list)

    with open(full_path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(["Start date", start_date])
        writer.writerow(["End date", end_date])
        writer.writerow([])

        # write the header
        writer.writerow(res[0][:14] + ['Comments'] + res[0][14:])
        # process and write the rows
        for table in res[1]:
            for row in table:
                # the textobject records are pulled here because in ASQL, the data length
                # is limited to 256 characters
                text_object = ael.TextObject.read(
                    'type="Customizable" and name="{0}"'.format(row[8]))

                if text_object:
                    comments = TradeBucketGUI.get_formatted_comments(text_object)
                else:
                    comments = ''

                new_row = list(row)
                new_row = new_row[:14] + [comments] + new_row[14:]
                writer.writerow(new_row)

    print("Wrote secondary output to " + full_path)

def ael_main(parameters):
    """ Main entry point
    """
    # set the default values for the start and end dates
    start_date = _START_DATE
    end_date = _END_DATE
    # get the params
    extension = '.csv'
    output_directory = str(parameters['output_directory'].SelectedDirectory())
    file_name = parameters['file_name']
    asql = parameters['asql']

    asqls = [asql]
    if asql == _ALL_ASQL:
        asqls = trade_volume_asql

    # check the path
    if not os.path.isdir(output_directory):
        raise ValueError('"{0}" is not a valid directory.'.format(output_directory))

    # build the filename
    if file_name.lower().endswith(extension):
        file_name = file_name[:-4]

    today_str = datetime.date.today().strftime('%Y-%m-%d')

    custom_dates = parameters['custom_dates']
    if custom_dates:
        start_date = parameters['start_date']
        end_date = parameters['end_date']
    else:
        time_period = parameters['time_period']
        if time_period == 'day':
            start_date = ael.date_today().to_string()
            end_date = ael.date_today().to_string()
        if time_period == 'month':
            pass  # this is the default value

    for_expired_trades = 'no'
    # backward compatibility
    if 'for_expired_trades' in parameters:
        for_expired_trades = parameters['for_expired_trades']



    for asql in asqls:
        rep_file_name = file_name
        rep_file_name += asql
        if for_expired_trades == 'yes':
            rep_file_name += '_Exp'
        if time_period == 'day':
            rep_file_name += '_EOD'
        rep_file_name += '_' + today_str + extension

        full_path = os.path.join(output_directory, rep_file_name)
        _generate_report(asql, start_date, end_date, for_expired_trades, full_path)


    print("completed successfully")

