"""-----------------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2011-06-17 685737        Paul J.-Guillarmod Added a completed succesfully print statement
2013-04-10 935599        Peter Fabian       Added support for sweeping Int fut fees
2014-06-05 2018619       Hynek Urban        Handling errors in PB overnight batch correctly
2015-07-14 2961517       Jakub Tomaga       Sweeping report added.
2015-09-11 3090331       Jakub Tomaga       Portfolio independent sweeping.
2019-11-21 FAPE-147      Tibor Reiss        Propagate error
-----------------------------------------------------------------------------"""
import acm
import string

import PS_CallAccountSweeperFunctions
from at_logging import getLogger, bp_start
from sweeping_report import CallAccountSweepingReport
from PS_Functions import (TODAY, START_DATE_KEYS, START_DATE_LIST, END_DATE_KEYS, END_DATE_LIST)


LOGGER = getLogger()


def enable_custom_start_date(index, field_values):
    ael_variables[2][9] = (field_values[1] == 'Custom Date')
    return field_values


def enable_custom_end_date(index, field_values):
    ael_variables[4][9] = (field_values[3] == 'Custom Date')
    return field_values


# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['portfolioSwaps', 'Portfolio Swaps', 'FInstrument', None, None, 0, 1, 'Portfolio swaps that call account sweeping will be performed for', None, 1],
                 ['startDate', 'Start Date', 'string', START_DATE_KEYS, 'Now', 1, 0, 'Date from which call account sweeping will take place.', enable_custom_start_date, 1],
                 ['startDateCustom', 'Start Date Custom', 'string', None, TODAY, 0, 0, 'Custom from date', None, 0],
                 ['endDate', 'End Date', 'string', END_DATE_KEYS, 'Now', 1, 0, 'Date to which call account sweeping will be run.', enable_custom_end_date, 1],
                 ['endDateCustom', 'End Date Custom', 'string', None, TODAY, 0, 0, 'Custom to date', None, 0],
                 ['sweepingReport', 'Sweeping Report', 'string', None, None, 0, 0, 'Report with detailed breakdown of swept amounts', None, 1],
                 ['clientName', 'Short name', 'string', None, 'CLIENT', 0, 0]
                ]


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    process_name = "ps.call_account_sweeper.{0}".format(ael_dict["clientName"])
        
    with bp_start(process_name, ael_main_args=ael_dict):
        if ael_dict['startDate'] == 'Custom Date':
            start_date = ael_dict['startDateCustom']
        else:
            start_date = START_DATE_LIST[ael_dict['startDate']]
    
        if ael_dict['endDate'] == 'Custom Date':
            end_date = ael_dict['endDateCustom']
        else:
            end_date = END_DATE_LIST[ael_dict['endDate']]
    
        # Validate the date input (otherwise strange things might happen).
        if not acm.Time.IsValidDateTime(start_date):
            raise ValueError('Invalid date: %s' % start_date)
        if not acm.Time.IsValidDateTime(end_date):
            raise ValueError('Invalid date: %s' % end_date)
        if not start_date <= end_date:
            raise ValueError('Start date must be prior or equal to end date.')
    
        current_tpl = {}
        historical_tpl = {}
        call_account_tpl = {}
        current_tpl_breakdown = {}
        historical_tpl_breakdown = {}
    
        for portfolioSwap in ael_dict['portfolioSwaps']:
            name = portfolioSwap.Name()
            (
                current_tpl[name],
                historical_tpl[name],
                call_account_tpl[name],
                current_tpl_breakdown[name],
                historical_tpl_breakdown[name]
            ) = PS_CallAccountSweeperFunctions.TPLSweeper(
                portfolioSwap, start_date, end_date)

        report_filename = ael_dict["sweepingReport"]
        if report_filename:
            try:
                data = (
                    current_tpl,
                    historical_tpl,
                    call_account_tpl,
                    current_tpl_breakdown,
                    historical_tpl_breakdown
                )
                file_path_template = string.Template(report_filename)
                file_path = file_path_template.substitute(DATE=end_date.replace("-", ""))
                report = CallAccountSweepingReport(file_path, data)
                report.create_report()
                LOGGER.info("Wrote secondary output to {0}".format(file_path))
            except:
                LOGGER.exception("Sweeping report wasn't generated.")

        if LOGGER.msg_tracker.errors_counter:
            raise RuntimeError("ERRORS occurred. Please check the log.")

        LOGGER.info("Completed Successfully")
