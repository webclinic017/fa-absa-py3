"""-----------------------------------------------------------------------------------------
MODULE
    sbl_call_account_rates_update

DESCRIPTION
    Date                : 2020-05-21
    Purpose             : Updates call account rates
    Department and Desk : SBL Ops Collateral
    Requester           : Shaun Du Plessis
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2020-05-21      PCGDEV-359      Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
import csv
import FRunScriptGUI
from datetime import datetime

from collections import OrderedDict
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger()

file_filter = "CSV Files (*.csv)|*.csv|"
input_file = FRunScriptGUI.InputFileSelection(FileFilter=file_filter)
input_file.SelectedFile(r"Y:\Jhb\Secondary Markets IT\Fix_the_Front\Q\Data Cleanup Scripts\Call Accounts Reset Dates\Files\G1_CallAccount_Changes.csv")

ael_variables = AelVariableHandler()
ael_variables.add(
    "input_file",
    label="CSV File",
    cls=input_file,
    mandatory=True,
    multiple=True,
    default=input_file
    )


def ael_main(dictionary):

    file = str(dictionary["input_file"])
    dict_list = read_file(file)
    process_data(dict_list)


def read_file(file):

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        dict_list = []
        year = acm.Time.DateToYMD(acm.Time.DateToday())[0]

        for titles in csv_reader:
            col_titles = titles
            break

        for row in csv_reader:
            field_dict = OrderedDict()

            for col_title, field in zip(col_titles, row):
                if col_title in ["Leg", "Cashflow", "Reset"]:
                    field = field.replace(",", "")
                    field = field.replace(".", "")
                elif ("Date" in col_title or col_title == "Leg Rolling") and field:
                    try:
                        field = datetime.strptime(field, "%Y-%m-%d")
                    except:
                        if not field == "today" and len(field) == 8:
                            field = field.replace(field[-2:], str(year)[:2]) + field[-2:]
                        field = acm.Time.DateAddDelta(field, 0, 0, 0)
                field_dict[col_title] = field
            dict_list.append(field_dict)
    return dict_list


def process_data(dict_list):

    for data in dict_list:
        cashflow = None
        trade_number = data["Trade Number"]
        leg = acm.FTrade[trade_number].Instrument().Legs()[0]

        if data["Leg"]:
            leg = acm.FLeg[data["Leg"]]

            if not leg:
                LOGGER.warning("Leg '%s' not found" %data["Leg"])
                continue
            LOGGER.info("\n**********Updating Leg: %s**********" %data["Leg"])

            if data["Leg Rolling"]:
                LOGGER.info("Rolling Period Base from %s to --> %s" %(leg.RollingPeriodBase(), data["Leg Rolling"]))
                leg.RollingPeriodBase(data["Leg Rolling"])
            if data["Leg Fixed Rate"]:
                LOGGER.info("Fixed Rate from %s to --> %s" %(leg.FixedRate(), data["Leg Fixed Rate"]))
                leg.FixedRate(data["Leg Fixed Rate"])
            leg.Commit()

        elif data["Cashflow"] and not data["Reset"]:
            if "Create" in data["Cashflow"]:
                cashflow = acm.FCashFlow()
                cashflow.Leg(leg)
                cashflow.CashFlowType ("Call Fixed Rate Adjustable")
            else:
                cashflow = acm.FCashFlow[data["Cashflow"]]

                if not cashflow:
                    LOGGER.warning("Cashflow '%s' not found" %data["Cashflow"])
                    continue
            LOGGER.info("\n**********Updating Cashflow: %s**********" %data["Cashflow"])

            if data["Start Date"]:
                LOGGER.info("Start Date from %s to --> %s" %(cashflow.StartDate(), data["Start Date"]))
                cashflow.StartDate(data["Start Date"]) 
            if data["End Date"]:
                LOGGER.info("End Date from %s to --> %s" %(cashflow.EndDate(), data["End Date"]))
                cashflow.EndDate(data["End Date"])
            if data["Pay Date"]:
                LOGGER.info("Pay Date from %s to --> %s" %(cashflow.PayDate(), data["Pay Date"]))
                cashflow.PayDate(data["Pay Date"])
            if data["Comment"] and "opposite" in data["Comment"]:
                LOGGER.info("Changed Fixed Amount from %s to --> %s" %(cashflow.FixedAmount(), -cashflow.FixedAmount()))
                cashflow.FixedAmount(-cashflow.FixedAmount())
            cashflow.Commit()

        if data["Reset"] or data["Date"]:
            if "Create" in data["Reset"] or (not data["Reset"] and data["Date"]):
                reset = acm.FReset()
                reset.Leg(leg)
                reset.ResetType ("Weighted")

                if not cashflow:
                    cashflow = acm.FCashFlow[data["Cashflow"]]

                if not cashflow:
                    LOGGER.warning("Reset for cashflow linked to trade %s is missing a cashflow" %trade_number)
                    continue
                reset.CashFlow(cashflow)
            else:
                reset = acm.FReset[data["Reset"]]

                if not reset:
                    LOGGER.warning("Reset '%s' not found" %data["Reset"])
                    continue
            LOGGER.info("\n**********Updating Reset: %s**********" %data["Reset"])

            if data["Date"]:
                LOGGER.info("Day from %s to --> %s" %(reset.Day(), data["Date"]))
                reset.Day(data["Date"])
            if data["Start Date"]:
                LOGGER.info("Start Date from %s to --> %s" %(reset.StartDate(), data["Start Date"]))
                reset.StartDate(data["Start Date"])
            if data["End Date"]:
                LOGGER.info("End Date from %s to --> %s" %(reset.EndDate(), data["End Date"]))
                reset.EndDate(data["End Date"])
            if data["Reset Rate"]:
                LOGGER.info("Fixing Value from %s to --> %s" %(reset.FixingValue(), data["Reset Rate"]))
                reset.FixingValue(data["Reset Rate"])

                if not reset.IsFixed():
                    reset.FixFixingValue(data["Reset Rate"])
            reset.Commit()
