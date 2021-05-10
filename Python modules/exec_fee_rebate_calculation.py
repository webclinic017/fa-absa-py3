import os
import time
from datetime import datetime
import csv

import acm
import ael

from at_ael_variables import AelVariableHandler
from at_logging import getLogger

LOGGER = getLogger()
DATE_TODAY = acm.Time().DateToday()

NEXT = 1
CURRENT = 0
PREVIOUS = -1

IGNORED_STATUSES = ["Simulated", "Terminated", "Void"]
XTP_EXCLUDED = ['OD']
PS_NO_FEES = ['PS No Fees']
EXCLUDED_USERS = ['FMAINTENANCE']

POSSIBLE_DATE_FORMATS = ['%Y-%m-%d', '%Y-%d-%m', '%Y/%m/%d', '%d/%m/%Y', '%m-%d-%Y']


def get_last_day_of_prev_month(which_month=CURRENT):
    first_day_of_current_month = acm.Time().FirstDayOfMonth(DATE_TODAY)
    return acm.Time().DateAddDelta(first_day_of_current_month, 0, which_month, -1)


ael_variables = AelVariableHandler()

ael_variables.add(
    name='output_directory',
    label='Trade Files Output Directory',
    cls='string',
    default='/services/frontnt/Task',
    mandatory=True,
    alt="Output directory for CSV files with trades"
)

ael_variables.add(
    name='start_date',
    label='Start Date',
    enabled=True,
    default=get_last_day_of_prev_month(PREVIOUS),
    alt=("Start Date of time span from which trades will be taken "
         "(format: '2018-12-31')")
)

ael_variables.add(
    name='end_date',
    label='End Date',
    enabled=True,
    default=get_last_day_of_prev_month(CURRENT),
    alt=("End Date of time span from which trades will be taken "
         "(format: '2019-01-31')")
)


def get_rebate_trd_filters():
    rebate_trd_filters = []
    try:
        for rebate_trd_filter in ael.TradeFilter.select():
            if ("PS_" in rebate_trd_filter.fltid) and ("_REBATE" in rebate_trd_filter.fltid):
                rebate_trd_filters.append(rebate_trd_filter.fltid)
        return rebate_trd_filters
    except Exception as exception:
        LOGGER.error(exception)
        raise exception


def convert_date_formats(input_date, str_format_output="%Y-%m-%d"):
    """
        Expects date in formats defined in POSSIBLE_DATE_FORMATS
        returns a date in "YYYY-MM-DD" format
    """
    for input_date_format in POSSIBLE_DATE_FORMATS:
        try:
            seconds = time.mktime(time.strptime(str(input_date), input_date_format))
            LOGGER.info("Input date has the following format: %s for the date = %s" % (input_date_format, input_date))
            return datetime.fromtimestamp(seconds).strftime(str_format_output)
        except ValueError:
            pass

    LOGGER.error("Input date cannot be formatted, none of date formats expected: %s", input_date)
    raise Exception


def rebate_calculator(total_traded_volume, rebate_filter, agreement_hurtle_rate_ranges=None):
    """
        Calculate Execution Fee Rebate
        using Agreement matrix for hurtle rates
    """
    rate_above = float(agreement_hurtle_rate_ranges[0][2])
    rebate = []
    for rate_bracket in agreement_hurtle_rate_ranges:
        if all([total_traded_volume > rate_bracket[0], total_traded_volume > rate_bracket[1]]):
            rebate.append((rate_bracket[1] - rate_bracket[0]) * rate_bracket[2] / 10000.0)
        elif all([total_traded_volume > rate_bracket[0], total_traded_volume <= rate_bracket[1]]):
            rebate.append((total_traded_volume - rate_bracket[0]) * rate_bracket[2] / 10000.0)

    blended_rate = sum(rebate) / total_traded_volume * 10000.0
    rebate = round((rate_above - blended_rate) * total_traded_volume / 10000.0)

    return rebate


def rebate_trade_selection(trades_from_trd_filter, start_date, end_date):
    """
        Perform further selection of trades chosen by the rebate trade filter as an input
    """
    selected_trades = []
    for trade in trades_from_trd_filter:
        if ((trade.Status() not in IGNORED_STATUSES)
                and (start_date <= trade.ExecutionTime() < end_date)
                and (trade.AdditionalInfo().XtpTradeType() not in XTP_EXCLUDED)
                and (trade.OptKey3() not in PS_NO_FEES)
                and (trade.TraderId() not in EXCLUDED_USERS)):
            selected_trades.append(trade)
    return selected_trades


def get_agreement_calc_matrix(file_path, rebate_filter):
    """"
        Reading Agreement Definition files for each rebate trade filter, files must exist
    """
    agreement_def_file_name = os.path.join(file_path + "\\Agreements", "%s.csv" % rebate_filter)

    try:
        with open(agreement_def_file_name, 'rb') as agreement_file:
            agreement_reader = csv.reader(agreement_file, delimiter=',')
            agreement_calc_matrix = [(float(row[0]), float(row[1]), float(row[2]))
                                     for row in agreement_reader if len(row) > 1]
            LOGGER.info("Agreement hurtle rate ranges read from %s file for filter %s" %
                        (agreement_def_file_name, rebate_filter))
            LOGGER.info("Aggreement matrix: %s" % agreement_calc_matrix)
        return agreement_calc_matrix
    except IOError as io_exception:
        LOGGER.error("Missing hurtle rate agreement matrix file %s", agreement_def_file_name)
        raise io_exception
    except Exception:
        raise "There is something wrong with the agreement matrix file for rebate trade filter %s" % rebate_filter


def ael_main(ael_dict):
    """
        Calculate Execution Fee Rebates using Agreement matrix
        for hurtle rates and find out which of our clients actually qualify for it
    """
    start = time.time()
    start_date = convert_date_formats(ael_dict['start_date'])
    end_date = convert_date_formats(ael_dict['end_date'])

    file_path = ael_dict['output_directory']
    if os.path.exists(file_path):
        LOGGER.info("Output directory set to %s", file_path)
    else:
        os.mkdir(file_path)
        LOGGER.warning("Output directory %s did not exist, it was created", file_path)

    month_folder = datetime.strptime(ael_dict['end_date'], "%Y-%m-%d").strftime("%Y-%m")
    month_folder = os.path.join(file_path, month_folder)
    if os.path.exists(month_folder):
        LOGGER.info("Output directory set to %s", month_folder)
    else:
        os.mkdir(month_folder)
        LOGGER.warning("Output directory %s did not exist, it was created", month_folder)
    rebate_output_file_name = "exec_fee_rebate_qualification_report_%s_%s.csv" % (start_date, end_date)
    rate_report_file_name = os.path.join(month_folder, rebate_output_file_name)

    with open(rate_report_file_name, mode='wb') as rebate_file:
        rebate_writer = csv.writer(rebate_file)
        rebate_writer.writerow(['Filter', 'Total traded volume', 'Rebate'])

        for rebate_filter in get_rebate_trd_filters():
            LOGGER.info("Calculating rebate for filter %s on %s for the period between %s and %s" % (
                rebate_filter, DATE_TODAY, start_date, end_date))
            agreement_calc_matrix = get_agreement_calc_matrix(file_path, rebate_filter)
            csv_file_name = os.path.join(month_folder, "%s_%s_%s.csv" % (rebate_filter, start_date, end_date))
            with open(csv_file_name, mode='wb') as csv_file:
                csv_writer = csv.writer(csv_file)
                trade_filter = ael.TradeFilter[rebate_filter]
                acm_tf = acm.FTradeSelection[trade_filter.fltnbr]
                csv_writer.writerow(['Trade', 'Instrument', 'Price', 'Qty', 'Abs', 'Acquire Day', 'Portfolio',
                                     'Status', 'Cpty', 'Trader', 'B/S', 'Execution', 'XtpTradeType', 'Text1',
                                     'OptKey3AsEnum', 'Daily Execution Fee', 'Key3'])

                total_traded_volume = 0.0
                filtered_trades = rebate_trade_selection(acm_tf.Trades(), start_date, end_date)
                for trade in filtered_trades:
                    csv_writer.writerow(
                        [str(trade.Oid()),
                         trade.Instrument().Name(),
                         str(trade.Price()),
                         str(trade.Quantity()),
                         str(abs(trade.Price() * trade.Quantity() * trade.Instrument().ContractSize() / 100.0)),
                         trade.AcquireDay(),
                         trade.Portfolio().Name(),
                         trade.Status(),
                         trade.Counterparty().Name(),
                         trade.TraderId(),
                         trade.Direction(),
                         str(datetime.strptime(trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")),
                         str(trade.AdditionalInfo().XtpTradeType()),
                         trade.Text1(),
                         trade.OptKey3AsEnum()])
                    total_traded_volume += abs(
                        trade.Price() * trade.Quantity() * trade.Instrument().ContractSize() / 100.0)

            LOGGER.info("File %s for filter %s populated" % (csv_file_name, rebate_filter))
            LOGGER.info("Total number of trades for filter %s is %s and filtered out are %s" %
                        (rebate_filter, len(acm_tf.Trades()), len(filtered_trades)))
            LOGGER.info("%s filter total traded volume = %s", rebate_filter,
                        '{:15,.2f}'.format(total_traded_volume))
            if total_traded_volume > 0.0:
                calculated_rebate = rebate_calculator(total_traded_volume, rebate_filter, agreement_calc_matrix)
                rebate_writer.writerow([rebate_filter, total_traded_volume, calculated_rebate])
                LOGGER.info("Total rebate for client %s is %s \n", rebate_filter,
                            '{:7,.2f}'.format(calculated_rebate))
            else:
                LOGGER.warning("All trades filtered out by our requirements\n")
    end = time.time()
    LOGGER.info("Completed successfully in %s", end - start)
