"""
Description: 
    Update the SL_SWIFT flag in production after having moved the additional
    info from instrument to trade.
    
    Script will be deleted once the BAU process is being followed correctly.
    (G1 is golden source of data but moving on FA. FA has not been kept updated
    with changes made in G1).

Project:     SBL onto FA
Developer:   Bhavnisha Sarawan
Date:        2020/01/02, 2020/03/05 (set all values in file)
"""

import acm
import csv

from at_ael_variables import AelVariableHandler
from at_addInfo import save
from at_logging import getLogger

LOGGER = getLogger(__name__)


def update_swift_flag(swift_update):
    for key in swift_update:
        acm.BeginTransaction()
        try:
            trade = acm.FTrade[key]
            save(trade, "SL_SWIFT", swift_update[key])
            if swift_update[key] == "SWIFT":
                trade.SettleCategoryChlItem("SL_STRATE")
            if swift_update[key] == "DOM":
                trade.SettleCategoryChlItem("SL_CUSTODIAN") 
            trade.Commit()
            acm.CommitTransaction()
            LOGGER.info("Trade: '%s' saved with SL_SWIFT = '%s' and Settlement Category updated." %(trade.Oid(), swift_update[key]))
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception("Failed for: '%s'" % (key))


def get_contract_trades(swift_update):
    contract_swift_update = {}
    for key in swift_update:
        trade = acm.FTrade[key]
        if trade:
            position_trades = acm.FTrade.Select("contractTrdnbr = %i and status <> 'Void'" % trade.ContractTrdnbr())
            count = 0
            for link_trade in position_trades:
                contract_swift_update[link_trade.Oid()] = swift_update[key]
    return contract_swift_update


ael_gui_parameters = {"hideExtracControls": True,
                      "windowCaption": "SWIFT flag Uploader"}

ael_variables = AelVariableHandler()
ael_variables.add_input_file("input_file",
                            label="CSV File",
                            collection=None,
                            mandatory=True,
                            default="F:\\SL_SWIFT.csv",
                            alt='Enter path + file name.csv',
                            enabled=True)

def ael_main(parameter):
    input_file = str(parameter["input_file"])
    swift_update = {}
    with open(input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in reader:
            try:
                trade = row[0]
                SL_SWIFT = row[1]
                swift_update[trade] = SL_SWIFT
            except Exception:
                LOGGER.exception("Error processing '%s' 'with error: '" % (trade))
        trades_to_update = get_contract_trades(swift_update)
        update_swift_flag(trades_to_update)

