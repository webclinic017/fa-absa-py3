'''
Collects metrics for Prime Services overnight batch.
Limitations:
  Only live clients
  Data from previous business day
'''

import csv
import datetime
import os

import acm

from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_fund_shortname)
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_time import to_date

LOGGER = getLogger()
ZAR_CALENDAR = acm.FCalendar["ZAR Johannesburg"]
PREV_BUS_DAY = to_date(ZAR_CALENDAR.AdjustBankingDays(acm.Time.DateNow(), -1))
PS_TASK_NAMES = ["PS_AddTradeFees",
                 "PS_Extend_General_PSwaps",
                 "PS_TPLSweep_General_PSwaps",
                 "PS_Payments",
                 "PS_Generate",
                 "PS_MTM",
                 "PS_Sweeping",
                 "PS_SetAddInfoDate",
                 "PS_LoanAccountSweeper",
                 "PS_FRerate",
                 "PS_Reporting"]

ael_variables = AelVariableHandler()
ael_variables.add_directory(
    "output_dir",
    label="Output directory",
    default="/services/frontnt/Task",
    mandatory=True,
    multiple=False)
ael_variables.add_output_file(
    "output_file",
    label="Output file name",
    default="PrimeServices_Metrics",
    mandatory=True,
    multiple=False)


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()

    output_file_name = os.path.join(str(ael_dict["output_dir"]),
                                    str(ael_dict["output_file"]) + "_" + PREV_BUS_DAY.strftime("%Y%m%d") + ".csv")

    client_list = []
    for client in get_pb_fund_counterparties():
        short_name = get_pb_fund_shortname(client)
        client_list.append(short_name)

    with open(output_file_name, "wb") as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow([''] + [task_name for task_name in PS_TASK_NAMES])
        for short_name in client_list:
            line = [short_name]
            for task_name in PS_TASK_NAMES:
                full_task_name = task_name + "_" + short_name + "_SERVER"
                task = acm.FAelTask[full_task_name]
                if task:
                    hist = acm.FAelTaskHistory.Select01("task='%s'" % full_task_name, None)
                    if hist and datetime.date.fromtimestamp(hist.StartTime()) >= PREV_BUS_DAY:
                        line.append(str(hist.StopTime() - hist.StartTime()))
                    else:
                        line.append("0")
                else:
                    line.append("0")
            csv_writer.writerow(line)

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Wrote secondary output to {}".format(output_file_name))
    LOGGER.info("Completed successfully")
