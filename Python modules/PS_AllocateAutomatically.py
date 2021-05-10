'''
Automatic allocation based on the specified strategy

To implement a new strategy:
    1. Extend STRATEGY
    2. Define new function for this strategy
    3. Extend if-else branch for strategies

HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2019-09-05  CHG1002204820  Tibor Reiss        Initial implementation
2019-09-06  INC1014540604  Tibor Reiss        Accommodate back end copying
'''

import csv
import os

import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_time import to_date

STRATEGY = ["1to1"]
TASK_LIST_1 = [task.Name() for task in acm.FAelTask.Select("moduleName='PS_AllocateTrades'")]
TASK_LIST_2 = [task.Name() for task in acm.FAelTask.Select("moduleName='PS_AllocateTradesSplit'")]
LOGGER = getLogger()


def alloc_strategy_1to1(config, directory, input_filename, output_filename):
    LOGGER.info("Modifying allocations file according to 1-to-1 strategy...")
    if len(config["descriptions"]) != 1 or len(config["portfolios"]) != 1:
        msg = "Can't run 1-to-1 strategy due to too few/many descriptions/portfolios!"
        LOGGER.error(msg)
        raise RuntimeError(msg)
    new_rows = []
    with open(directory + input_filename, "rb") as csv_file:
        csv_reader = csv.reader(csv_file)
        new_rows.append(next(csv_reader, None))
        new_rows.append(next(csv_reader, None))
        for row in csv_reader:
            new_rows.append(row)
            new_rows[-1][-1] = new_rows[-1][-2]
    with open(directory + output_filename, "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(new_rows)


ael_variables = AelVariableHandler()
ael_variables.add('client_name',
                  label='Client name',
                  cls='string',
                  mandatory=True,
                  multiple=False
                  )
ael_variables.add('strategy',
                  label='Allocations strategy',
                  collection=STRATEGY,
                  cls='string',
                  mandatory=True,
                  multiple=False
                  )
ael_variables.add('task1',
                  label='Task 1',
                  collection=sorted(TASK_LIST_1),
                  cls='string',
                  mandatory=True,
                  multiple=False
                  )
ael_variables.add('task2',
                  label='Task 2',
                  collection=sorted(TASK_LIST_2),
                  cls='string',
                  mandatory=True,
                  multiple=False
                  )
ael_variables.add('descriptions',
                  label='Descriptions for task 1',
                  cls='string',
                  mandatory=False,
                  multiple=True
                  )
ael_variables.add('portfolios',
                  label='Portfolios for task 1',
                  cls='string',
                  mandatory=False,
                  multiple=True
                  )
ael_variables.add('date_to_run',
                  label='Date to run',
                  cls='string',
                  default="TODAY",
                  mandatory=True,
                  multiple=False
                  )
ael_variables.add('stocks',
                  label='Stock list',
                  cls='string',
                  mandatory=False,
                  multiple=True,
                  alt='If blank, will run for all instruments.'
                  )


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()

    alloc_strategy = ael_dict["strategy"]
    date_to_run = str(to_date(ael_dict["date_to_run"]))
    stocks = ','.join(ael_dict["stocks"])
    descriptions = ','.join(ael_dict["descriptions"])
    portfolios = ','.join(ael_dict["portfolios"])

    filename_alloc = "Task1_" + ael_dict['client_name'] + "_" + date_to_run.replace("-", "") + ".csv"
    filename_split = "Task2_" + ael_dict['client_name'] + "_" + date_to_run.replace("-", "") + "_Split.csv"
    directory = "/services/frontnt/Task/"

    # Adjusting parameters and running PS_AllocateTrades
    LOGGER.info("Running 1st task...")
    task1 = acm.FAelTask[ael_dict["task1"]].Clone()
    params = task1.Parameters()
    params.AtPutStrings("filename", filename_alloc)
    params.AtPutStrings("directory", directory)
    params.AtPutStrings("for_date", date_to_run)
    if descriptions:
        params.AtPutStrings("descriptions", descriptions)
    if portfolios:
        params.AtPutStrings("portfolios", portfolios)
    if stocks:
        params.AtPutStrings("stocks", stocks)
    task1.Parameters(params)
    task1.Execute()
    LOGGER.info('Wrote secondary output to {}'.format(os.path.join(directory, filename_alloc)))

    if os.path.isfile(directory + filename_alloc):
        if alloc_strategy == "1to1":
            alloc_strategy_1to1(ael_dict, directory, filename_alloc, filename_split)
        else:
            msg = "Allocation strategy not implemented"
            LOGGER.error(msg)
            raise RuntimeError(msg)

        LOGGER.info("Running 2nd task...")
        task2 = acm.FAelTask[ael_dict["task2"]].Clone()
        params = task2.Parameters()
        params.AtPutStrings("input_file", directory + filename_split)
        params.AtPutStrings("date", "Custom Date")
        params.AtPutStrings("dateCustom", date_to_run)
        if stocks:
            params.AtPutStrings("stocks", stocks)
        task2.Parameters(params)
        task2.Execute()
        LOGGER.info('Wrote secondary output to {}'.format(os.path.join(directory, filename_split)))
    else:
        LOGGER.warning("No allocation file generated!")

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully")
