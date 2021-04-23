"""-----------------------------------------------------------------------------------------
MODULE
    sbl_datalend_inventory_report

DESCRIPTION
    Date                : 2019-12-30
    Purpose             : This will generate a txt file for reporting on available holdings
    Department and Desk : PTS Change
    Requester           : James Stevens
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2019-12-30      PCGDEV-55      Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
------------------------------------------------------------------------------------------"""

import acm
import os
import FRunScriptGUI
import csv
import at_calculation_space as acs
from at_ael_variables import AelVariableHandler
from at_logging import getLogger

outputSelection = FRunScriptGUI.DirectorySelection()
directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory("Y:\Jhb\SL Operations\G1Uploads\PROD\Out")

DATA = []
LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
ael_variables.add(
    'file_drop_location',
    label = 'File Drop Location',
    cls = directorySelection,
    default = directorySelection,
    multiple = True
    )


def ael_main(dictionary):

    directory = str(dictionary['file_drop_location'])
    date_time_string = acm.Time.TimeNow().split(".")[0].replace(" ", "-").replace(":", "-")
    output_filename = "inventory.%s.absacapital.intl.txt" % str(date_time_string)
    output_file = os.path.join(directory, output_filename)

    _run_extraction()
    _generate_report(output_file)
    LOGGER.info('>>> %s COMPLETED SUCCESSFULLY' % str(acm.Time.TimeNow())[:-4])
    LOGGER.info("Wrote secondary output to: {path}".format(path=output_file))


def _run_extraction():

    context = acm.GetDefaultContext()
    extension = context.GetExtension('FParameters', 'FObject', 'SASOLStatementOfHoldings')
    extension_dict = extension.Value()
    empty_fields = ['', '', '', '']

    trades = [trade for trade in acm.FPhysicalPortfolio["Lender_Availability"].Trades() if trade.Quantity() != 0.0]

    for trade in trades:
        isin = trade.Instrument().Underlying().Isin()
        security_description = trade.Instrument().FreeText()
        available_quantity = round(acs.calculate_value('FPortfolioSheet', trade, 'Available Quantity'))
        available_value = round(available_quantity * trade.Instrument().RefPrice())

        DATA.append([isin] + empty_fields + [security_description, available_quantity, available_value, 'ZAR'] + empty_fields)

    for isin in extension_dict:
        if len(isin) == 12:
            ls = str(extension_dict[isin])[1:-1]
            ls = ls.split(",")
            DATA.append([str(isin)] + empty_fields + ls + empty_fields)


def _generate_report(output_file):

    column_titles = ['isin', 'sedol', 'cusip', 'quick',
                    'ticker', 'secDesc', 'unitQty', 
                    'invValue', 'invCur', 'Entity 1', 
                    'Entity 2', 'Entity 3', 'Entity 4'
                    ]

    if DATA:
        with open(output_file, 'wb') as myCsvfile:
            wr = csv.writer(myCsvfile, delimiter="\t")
            wr.writerow(column_titles)

            for rownum in range(len(DATA)):
                wr.writerow(DATA[rownum])
            LOGGER.info('Report saved to . %s' % str(output_file)) 
