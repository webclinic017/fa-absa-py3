"""
This is GPP onboarding script that executes all onboarding tasks.

onboarding directory: 'y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\GPP\onboarding'
"""

import acm
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()

ONBOARD_UPLOAD_SINCE_INCEPT = [
    "PB_GPP_ONBOARD_CFDS_AGG",
    "PB_GPP_ONBOARD_FUTS_AGG",
    "PB_GPP_ONBOARD_STOCKS_AGG",
    ]

ONBOARD_LAST_5_BUS_DAYS = [
    "PB_GPP_ONBOARD_20171201",
    "PB_GPP_ONBOARD_20171204",
    "PB_GPP_ONBOARD_20171205",
    "PB_GPP_ONBOARD_20171206",
    "PB_GPP_ONBOARD_20171207",
    "PB_GPP_ONBOARD_20171208",
    ]


TASKS = ONBOARD_UPLOAD_SINCE_INCEPT + ONBOARD_LAST_5_BUS_DAYS
        
def ael_main(ael_dict):
    for task_name in TASKS:
        print("Executing task: '%s'" % task_name)
        task = acm.FAelTask[task_name]
        task.Execute()
        
        print("*" * 50)
        print("Completed successfully.")
