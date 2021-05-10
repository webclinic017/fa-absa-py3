"""
Project: ABITFA-5616 - SL Terminate daily
Purpose: Script for termination of SL instruments created during SL sweeping.
         This is part of SL Aggregation work.
Developer: Ondrej Bahounek
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
BUSINESS_DAYS_KEY = "SixBusinessDaysAgo"
BUSINESS_DAYS_VAL = -6
CUSTOM_DATE_KEY = "Custom Date"
SL_STATUS = "Terminated"


def enable_custom_end_date(selected_variable):
    cust = ael_variables.get("custom_end_date")
    cust.enabled = (selected_variable.value == CUSTOM_DATE_KEY)


ael_variables = AelVariableHandler()
ael_variables.add("start_date",
                  label="Start Date",
                  cls="date",
                  default=None,
                  mandatory=False,
                  alt=("If not set, Start Date won't be considered."))
ael_variables.add("end_date",
                  label="End Date",
                  cls="string",
                  collection=(BUSINESS_DAYS_KEY,
                              CUSTOM_DATE_KEY),
                  default=BUSINESS_DAYS_KEY,
                  hook=enable_custom_end_date,
                  alt=("Instruments with less equal EndDate will be selected."))
ael_variables.add("custom_end_date",
                  label="Custom End Date",
                  cls="string",
                  default="2018-06-24",
                  enabled=False,
                  mandatory=False,
                  alt=("Format: '2018-06-24'."))


def sbl_positions_query(start_date, end_date):
    """Return SL instruments with
            - Create User: ATS
            - start date <= SL date <= end date
            - Open End: None
    """
    sl_query = acm.CreateFASQLQuery('FInstrument', 'AND')
    sl_query.AddAttrNode('InsType', 'EQUAL', 'SecurityLoan')
    sl_query.AddAttrNode('ArchiveStatus', 'EQUAL', 0)
    sl_query.AddAttrNode('OpenEnd', 'EQUAL', 0)
    sl_query.AddAttrNode('Legs.EndDate', 'LESS_EQUAL', end_date)
    sl_query.AddAttrNode('CreateUser.Name', 'EQUAL', 'ATS')
    if start_date:
        sl_query.AddAttrNode('Legs.StartDate', 'GREATER_EQUAL', start_date)
    
    return sl_query.Select()


def terminate_sls(instruments):
    for ins in instruments:
        LOGGER.info("Terminating: '%s'", ins.Name())
        ins.OpenEnd(SL_STATUS)
        ins.Commit()


def ael_main(ael_variables):
    start_date = acm.Time.DateFromTime(ael_variables['start_date'])
    if ael_variables['end_date'] == BUSINESS_DAYS_KEY:
        end_date = acm.FInstrument['ZAR'].Calendar().AdjustBankingDays(TODAY, BUSINESS_DAYS_VAL)
    else:
        end_date = acm.Time.DateFromTime(ael_variables['custom_end_date'])
    
    LOGGER.info("Start Date: %s", start_date)
    LOGGER.info("End Date: %s", end_date)

    instrs = sbl_positions_query(start_date, end_date)
    LOGGER.info("Total instruments: %d", len(instrs))
    terminate_sls(instrs)
    LOGGER.info("Completed successfully.")
