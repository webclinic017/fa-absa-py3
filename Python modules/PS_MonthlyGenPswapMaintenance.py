"""
DEPARTMENT: Prime Services

DESCRIPTION
Maintenance of PS portfolio swaps' funding and total return resets:
  daily: keep all resets of this and previous months
  monthly: keep month end resets of this and previous year
  yearly: keep year end resets of years smaller than (current year - 2)

Usage:
  A) run for selected clients by specifying them in a comma separated list
  B) run for set of clients which are between the two provided strings
  C) run for all active clients by leaving all fields blank (default)

HISTORY
Date        Change no        Developer           Description
-------------------------------------------------------------------------------------------------------------
2019-01-23  CHG1001315259    Tibor Reiss         Initial Implementation
2019-05-28  CHG1001786026    Tibor Reiss         Moving functionality into new function for reusability
2019-06-11  CHG1001867217    Tibor Reiss         Enable also Total Return legs
2019-06-13  CHG1001877373    Tibor Reiss         When there are more than 1 resets for a given date, archive all
2019-09-05  CHG1002204820    Tibor Reiss         Correcting module name due to renaming
"""


from datetime import datetime
import time
from collections import defaultdict

import acm

from PS_FundingSweeper import GetFloatCashFlow
from PS_Functions import (get_pb_fund_pswaps,
                          get_pb_fund_counterparties,
                          get_pb_fund_shortname)
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import to_date as at_to_date


LOGGER = getLogger(__name__)
ZAR_CALENDAR = acm.FCalendar["ZAR Johannesburg"]
NOW = datetime.now()
DATE_TODAY = at_to_date(acm.Time().DateToday())
CURRENT_YEAR = NOW.year
CURRENT_MONTH = NOW.month
if CURRENT_MONTH == 1:
    KEEP_DAILY_VALUES_FOR_MONTH = 12
else:
    KEEP_DAILY_VALUES_FOR_MONTH = CURRENT_MONTH - 1


def last_business_day_of_year(date, calendar=ZAR_CALENDAR):
    first_day_of_year = acm.Time.FirstDayOfYear(date)
    first_day_of_next_year = acm.Time.DateAddDelta(first_day_of_year, 1, 0, 0)
    return calendar.AdjustBankingDays(first_day_of_next_year, -1)


def last_business_day_of_month(date, calendar=ZAR_CALENDAR):
    first_day_of_month = acm.Time.FirstDayOfMonth(date)
    first_day_of_next_month = acm.Time.DateAddDelta(first_day_of_month, 0, 1, 0)
    return calendar.AdjustBankingDays(first_day_of_next_month, -1)


def get_all_clients():
    clients = {}
    for client in get_pb_fund_counterparties():
        clients[get_pb_fund_shortname(client)] = client
    return clients


def get_shortnames_to_process(client_list=None, client_from=None, client_to=None):
    all_active_clients = get_all_clients()
    all_short_names = list(all_active_clients.keys())
    clients = {}
    if client_list:
        for short_name in client_list:
            if short_name not in all_short_names:
                msg = "Invalid client {}".format(short_name)
                LOGGER.exception(msg)
                raise RuntimeError(msg)
            clients[short_name] = all_active_clients[short_name]
    elif client_from and client_to:
        for short_name in all_short_names:
            if client_from <= short_name < client_to:
                clients[short_name] = all_active_clients[short_name]
    else:
        clients = all_active_clients.copy()
    return clients


def candidate_cash_flows(leg):
    candidates = []
    if leg.LegType() == "Float":
        cash_flow = GetFloatCashFlow(leg, "Funding")
        if cash_flow:
            candidates.append(cash_flow)
    elif leg.LegType() == "Total Return":
        for cf in leg.CashFlows():
            if cf.CashFlowType() == "Position Total Return":
                candidates.append(cf)
    return candidates


def read_resets(cash_flow):
    cash_flow_type = cash_flow.CashFlowType()
    cash_flow_add_info = cash_flow.add_info('PS_FundWarehouse')
    allowed_resets = []
    if cash_flow_type == "Float Rate" and (not cash_flow_add_info or cash_flow_add_info == "Funding"):
        allowed_resets.append("Return")
    elif cash_flow_type == "Position Total Return":
        allowed_resets.extend(["Nominal Scaling", "Return"])
    LOGGER.info("\t\tReading resets for: instrument={}, cf_type={}, cf_ai={}..."
                .format(cash_flow.Leg().IndexRef().Name(), cash_flow_type, cash_flow_add_info))
    all_resets = defaultdict(list)
    for reset in cash_flow.Resets():
        reset_type = reset.ResetType()
        if reset_type not in allowed_resets:
            LOGGER.error("\t\tReset type {} not allowed!".format(reset_type))
            return None
        reset_day = reset.Day()
        all_resets[reset_day].append(reset.Oid())
    return all_resets


def keep_reset(reset_date):
    reset_year = reset_date.year
    reset_month = reset_date.month
    if reset_year < CURRENT_YEAR - 1:
        last_day_of_year = last_business_day_of_year(str(reset_year) + "-01-01")
        if reset_date != at_to_date(last_day_of_year):
            return False, last_day_of_year
        else:
            if reset_year == CURRENT_YEAR - 2:
                return True, last_business_day_of_month(str(CURRENT_YEAR - 1) + "-01-01")
            else:
                return True, last_business_day_of_year(str(reset_year + 1) + "-01-01")
    if reset_year == CURRENT_YEAR - 1:
        if KEEP_DAILY_VALUES_FOR_MONTH == 12 and reset_month == KEEP_DAILY_VALUES_FOR_MONTH:
            return True, ZAR_CALENDAR.AdjustBankingDays(str(reset_date), +1)
        else:
            return keep_only_month_end(reset_date)
    if reset_month >= KEEP_DAILY_VALUES_FOR_MONTH or (KEEP_DAILY_VALUES_FOR_MONTH == 12 and reset_month == 1):
        return True, ZAR_CALENDAR.AdjustBankingDays(str(reset_date), +1)
    else:
        return keep_only_month_end(reset_date)


def keep_only_month_end(reset_date):
    reset_year = reset_date.year
    reset_month = reset_date.month
    last_day_of_month = last_business_day_of_month(str(reset_year) + "-"
                                                   + ("{num:02d}".format(num=reset_month))
                                                   + "-01")
    if reset_date != at_to_date(last_day_of_month):
        return False, last_day_of_month
    else:
        if ( (reset_year == CURRENT_YEAR - 1 and reset_month == 11 and KEEP_DAILY_VALUES_FOR_MONTH == 12)
             or (reset_year == CURRENT_YEAR - 1 and reset_month == 12 and KEEP_DAILY_VALUES_FOR_MONTH == 1)
             or (reset_year == CURRENT_YEAR and reset_month == KEEP_DAILY_VALUES_FOR_MONTH - 1)):
            next_date_to_keep = last_business_day_of_month(str(reset_year) + "-"
                                                           + ("{num:02d}".format(num=reset_month))
                                                           + "-01")
            next_date_to_keep = ZAR_CALENDAR.AdjustBankingDays(next_date_to_keep, +1)
            return True, next_date_to_keep
        else:
            if reset_month == 12:
                return True, last_business_day_of_month(str(reset_year + 1) + "-01-01")
            return (True, last_business_day_of_month(str(reset_year) + "-"
                                                     + ("{num:02d}".format(num=reset_month+1))
                                                     + "-01"))


def check_resets(resets):
    resets_to_archive = []
    next_date_to_keep = None
    last_reset = sorted(resets.keys())[-1]
    for r in sorted(resets):
        # Always keep the last reset
        if r == last_reset:
            return resets_to_archive
        reset_date = at_to_date(r)
        if reset_date is None or reset_date >= DATE_TODAY:
            continue
        if next_date_to_keep:
            if at_to_date(next_date_to_keep) > reset_date:
                resets_to_archive.extend(resets[r])
                LOGGER.info("\t\tMarking reset {} for archiving".format(reset_date))
            elif at_to_date(next_date_to_keep) < reset_date:
                LOGGER.warning("\t\tMissing reset for date {}. Next reset found is {}.".format(next_date_to_keep, reset_date))
                (keep, next_date_to_keep) = keep_reset(reset_date)
            else:
                (keep, next_date_to_keep) = keep_reset(reset_date)
        else:
            (keep, next_date_to_keep) = keep_reset(reset_date)
            if not keep:
                resets_to_archive.extend(resets[r])
                LOGGER.info("\t\tMarking reset {} for archiving".format(reset_date))
    return resets_to_archive


def archive_old_resets(resets_to_archive):
    LOGGER.info("\t\tArchiving {} resets...".format(len(resets_to_archive)))
    acm.BeginTransaction()
    try:
        for oid in resets_to_archive:
            reset = acm.FReset[oid]
            reset.ArchiveStatus(1)
            reset.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Something went wrong during archiving resets...")


ael_variables = AelVariableHandler()
ael_variables.add("clients",
                  cls="string",
                  label="Client list",
                  mandatory=False,
                  multiple=True)
ael_variables.add("clients_from",
                  cls="string",
                  label="Take into account clients from (greater equal)",
                  mandatory=False)
ael_variables.add("clients_to",
                  cls="string",
                  label="Take into account clients until (smaller)",
                  mandatory=False)


def ael_main(ael_dict):
    delta_days = (at_to_date(NOW) - DATE_TODAY).days
    if delta_days not in [0, 1]:
        raise RuntimeError("Date parameters are incorrect!")

    LOGGER.msg_tracker.reset()
    LOGGER.info("CURRENT YEAR = {} CURRENT_MONTH = {}".format(CURRENT_YEAR, CURRENT_MONTH))

    clients = get_shortnames_to_process(client_list=ael_dict["clients"],
                                        client_from=ael_dict["clients_from"],
                                        client_to=ael_dict["clients_to"])
    LOGGER.info("Run monthly funding maintenance for {} clients".format(len(clients)))

    for short_name in sorted(clients):
        start = time.time()
        LOGGER.info("START client {}".format(short_name))
        for pswap in get_pb_fund_pswaps(clients[short_name]):
            LOGGER.info("\tSTART pswap {}".format(pswap.Name()))
            for leg in pswap.Legs():
                for cash_flow in candidate_cash_flows(leg):
                    all_resets = read_resets(cash_flow)
                    if all_resets:
                        resets_to_archive = check_resets(all_resets)
                        if resets_to_archive:
                            archive_old_resets(resets_to_archive)
        end = time.time()
        LOGGER.info("TOTAL TIME for client {} = {}".format(short_name, end-start))

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully.")
