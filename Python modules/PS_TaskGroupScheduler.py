"""
MODULE
    PS_TaskGroupScheduler


DESCRIPTION
    This script sets all tasks, within the specified task group, to be
    executed by the ATS monitoring the group.

    This task can be included in the group and scheduled to allow all tasks
    to be run at a specific time.

    Make a note to include the task name in the ignore list to avoid tasks
    being executed multiple times.


HISTORY
=======================================================================
Date             Developer                  Description
-----------------------------------------------------------------------
2020-05-18       Marcus Ambrose             Initial Implementation
-----------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add('task_group',
                  label='Task group to schedule',
                  cls='FAelTaskGroup',
                  mandatory=True,
                  multiple=False,
                  collection=acm.FAelTaskGroup.Select('')
                  )
ael_variables.add('regex_to_ignore',
                  label='Not to run (regex)',
                  mandatory=False,
                  multiple=True,
                  )


def ael_main(ael_dict):
    task_group = ael_dict['task_group']
    regex_to_ignore = ael_dict['regex_to_ignore']

    for task in task_group.Tasks():
        if not any(exclude in task.Name() for exclude in regex_to_ignore):
            task.ExecuteOnServer()
