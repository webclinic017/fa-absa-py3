"""
Description
===========
Date                          :  2018-04-05
Purpose                       :  ABITFA-5316: Reopen terminated instruments
Department and Desk           :  TCU for SBL
Requester                     :  Relief Nonyane
Developer                     :  Ondrej Bahounek

Details:
========
This script automates reopenning and extending terminated SL instruments.

When an SL instrument is terminated same day as is its Start Day,
then no cashflows will be generated on it.
When an instrument is manually reopenned by TCU,
cashflows are not necessarily being regenerated.
By using this script, a re-opending and re-extending of an instrument
will always result in an instrument in correct state and with a cashflow.

Acceptable inputs are both trade numbers and instrument names.
Input can be also given from a csv file (trade/instr per line).

Changes:
========
2020-01-09  CHG0073639   Libor Svoboda      Update sec loan regenerate logic.
"""

import csv
import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
import FRunScriptGUI

FILE_SELECTION = FRunScriptGUI.InputFileSelection(FileFilter="CSV Files (*.csv)|*.csv")


TODAY = acm.Time.DateToday()
LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()


ael_variables.add("input",
                  label="Input",
                  cls="string",
                  mandatory=False,
                  multiple=True,
                  alt=("Trade numbers or instrument names"))
ael_variables.add("input_file",
                  label="Input File",
                  cls=FILE_SELECTION,
                  default=FILE_SELECTION,
                  mandatory=False,
                  multiple=True,
                  alt=("Input csv file with one trade/instrument on each row"))


def reopen(instr):
    if instr.OpenEnd() != "Open End":
        LOGGER.info("\t - Open Ending")
        instr.OpenEnd("Open End")
        instr.Commit()
    
    if instr.EndDate() <= TODAY:
        LOGGER.info("\t - Extending")
        leg = instr.Legs()[0]
        leg.EndDate(acm.Time.DateAddDelta(leg.StartDate(), 0, 0, 1))
        leg.RollingPeriodBase(instr.StartDate())
        leg.Commit()
        instr.SLExtendOpenEnd()
        instr.SLGenerateCashflows()


def get_input(ael_dict):
    input_objs = []
    filename = str(ael_dict['input_file'])
    # input file has a priority over task input
    if filename:        
        LOGGER.info("From file: '%s'", filename)
        with open(filename, "rb") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            
            for line in reader:
                if not line:
                    continue
                obj = line[0]
                obj = obj.replace(",", "")
                input_objs.append(obj)
        return input_objs
    else:
        return ael_dict['input']


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    input_objs = get_input(ael_dict)
    for obj in input_objs:
        LOGGER.info("Processing input: '%s'", obj)
        try:
            instr = acm.FInstrument.Select01("name='%s'" % obj, None)
            if instr is None:
                trade = acm.FTrade[obj]
                instr = trade.Instrument()
            LOGGER.info("Reopening: '%s'", instr.Name())
            
            reopen(instr)
        except:
            LOGGER.exception("Reopening failed.")
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
        
    LOGGER.info("Completed successfully.")
