"""
Logs daily statistics of the live view tasks run for prime portal.
Scheduled daily to run at 7.30pm after Portal EOD run.
"""
import acm
import csv
import os
from datetime import timedelta, date

from at_logging import getLogger
from at_ael_variables import AelVariableHandler


PORTAL_TASK_GROUP = "prime_portal_tasks"
REPORT_COLUMNS = (
    "Task",
    "Run count",
    "Average run time",
    "Shortest run",
    "Longest run",
)
LOGGER = getLogger()


def log_task_stats(task, writer):
    run_count = len(task.History())
    run_times = get_run_times(task)

    if run_times:
        avg_run_time = str(timedelta(seconds=sum(run_times) / len(run_times)))
        shortest_run = str(timedelta(seconds=min(run_times)))
        longest_run = str(timedelta(seconds=max(run_times)))

        writer.writerow(
            [task.Name(), run_count, avg_run_time, shortest_run, longest_run]
        )


def get_run_times(task):
    run_times = []

    for history in task.History():
        # Confirm task run was successfully completed.
        if history.StopTime() != 0:
            run_times.append(history.StopTime() - history.StartTime())

    return run_times


def get_portal_tasks():
    task_group = acm.FAelTaskGroup[PORTAL_TASK_GROUP]

    if not task_group:
        LOGGER.warning(
            "No task group {} found, report will be blank!".format(PORTAL_TASK_GROUP)
        )
        return []

    return [task for task in task_group.Tasks() if "Template" not in task.Name()]


ael_variables = AelVariableHandler()
ael_variables.add(
    "output_directory",
    label="Output Directory",
    cls="string",
    mandatory=True,
    default="/services/frontnt/Task/",
)
ael_variables.add(
    "file_name",
    label="File Name",
    mandatory=True,
    default="PrimePortalLiveViewStatistics",
)


def ael_main(ael_dict):
    LOGGER.info("Processing live view statistics...")

    file_name = "{}_{}.{}".format(
        ael_dict["file_name"], date.today().strftime("%Y%m%d"), "csv"
    )
    file_path = os.path.join(ael_dict["output_directory"], file_name)

    with open(file_path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(REPORT_COLUMNS)

        for task in get_portal_tasks():
            log_task_stats(task, writer)

    LOGGER.info("Processing complete. Output written to {}".format(file_path))
