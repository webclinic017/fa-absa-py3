# This is a rollback script for sl_terminate_internal_trades 
# and it needs the output from the log from the termination script
import csv

import acm
import ael
import FRunScriptGUI
 
fields = [ "Trade Number",
           "Portfolio",
           "CP Portfolio",
           "Underlying",
           "B/S",
           "SL Rate",
           "Original Price",
           "Quantity",
           "SL_ExternalInternal",
           "StartDate",
           "EndDate",
           "Borrower",
           "Fund / Lender",
           "Instrument.OpenEnd",
           "Trade Type",
           "Und Type",
           "Status",
           "Trader",
           "Orig End Date",
           "Orig Open End",
           "ScriptAction", ]


def _revert_trade(trade_info):
    try:
        trdnbr = int(trade_info["Trade Number"])
    except ValueError:
        raise ValueError("%s is not a valid trade number" % trade_info["Trade Number"])
    
    trd = ael.Trade[trdnbr]
    if trd:
        i = trd.insaddr.clone()
        leg = i.legs()[0]
        leg.end_day = ael.date_from_string(trade_info["Orig End Date"])
        i.open_end = trade_info["Orig Open End"]
        leg.commit()
        i.commit()


def _revert_trades_from_file(filename):
    print("Reverting trades from %s" % filename)
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for record in reader:
            try:
                _revert_trade(record)
            except Exception as e:
                print("Could not revert trade %s: %s" % (record["Trade Number"], e))
            else:
                print("Trade %s reverted" % record["Trade Number"])

fileFilter = "*.csv"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
                 ['csvFile', 'CSV File', inputFile, None, inputFile, 1, 1,
                  'CSV file with terminated trades from sl_terminate_internal_trades', None, 1]
]


def ael_main(ael_dict):
    csv_file = str(ael_dict['csvFile'])

    _revert_trades_from_file(csv_file)
    print("Done")
