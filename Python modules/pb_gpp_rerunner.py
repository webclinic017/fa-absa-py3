"""
Description
===========
Date                          :  2018-02-06
Purpose                       :  GPP project: Upload task rerunner
Department and Desk           :  FO Prime Services
Requester                     :  Eveshnee Naidoo
Developer                     :  Ondrej Bahounek

Details:
========
This script should enable to rerun Upload task for a range of days.
"""

import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler


LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

TASK_NAME = 'PB_GPP_UPLOAD_FRONT'
WEEKEND_DAYS = ("Saturday", "Sunday")

ael_variables.add("task",
                  label="Task Name",
                  cls="FAelTask",
                  default="PB_GPP_UPLOAD_FRONT",
                  mandatory=False,
                  alt=("Only parameter this task has to have is 'custom_date'")
                  )
ael_variables.add("start_date",
                  label="Start Date",
                  cls="date",
                  default="",
                  mandatory=False,
                  alt=('Start date: first date for which the task will be run')
                  )
ael_variables.add("end_date",
                  label="End Date",
                  cls="date",
                  default="",
                  mandatory=False,
                  alt=('End date: last date for which the task will be run')
                  )


def get_dates_from_range(start_date, end_date):
    dates = []
    num_days = acm.Time.DateDifference(end_date, start_date) + 1
    for days_to_add in range(num_days):
        sweep_date = acm.Time.DateAddDelta(start_date, 0, 0, days_to_add)
        dates.append(sweep_date)
    return dates


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    start_date = ael_dict['start_date'].to_string("%Y-%m-%d")
    end_date = ael_dict['end_date'].to_string("%Y-%m-%d")
    task = ael_dict['task']
    LOGGER.info("Rerun data:")
    LOGGER.info("Task: %s", task.Name())
    LOGGER.info("Start Date: %s", start_date)
    LOGGER.info("End Date: %s", end_date)

    sweeping_dates = get_dates_from_range(start_date, end_date)

    params = task.Parameters()
    try:
        for for_date in sweeping_dates:
            LOGGER.info("Running for date: '%s'", for_date)
            if acm.Time.DayOfWeek(for_date) in WEEKEND_DAYS:
                LOGGER.info("Skipping weekend day...")
                continue
            
            params.AtPutStrings('custom_date', for_date)
            task.Parameters(params)
            task.Execute()
    except:
        LOGGER.exception("Task wasn't rerun successfully.")
    finally:
        task.Undo()
    
    if LOGGER.msg_tracker.errors_counter:
        msg = "Errors occurred. Please check the log."
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    if LOGGER.msg_tracker.warnings_counter:
        LOGGER.warning("Completed with some warnings.")
    else:
        LOGGER.info("Completed successfully.")
