"""
CSV extract

Department and Desk      : PS OPS
Requester                : Zimu, Simphiwe
Developer                : Frantisek Jahoda

HISTORY
==============================================================================
2015-06-03 ABITFA-3446 Frantisek Jahoda - Initial implementation
------------------------------------------------------------------------------
"""

import csv
import os

import acm
from at_ael_variables import AelVariableHandler
from at_calculation_space import prepare_calc_space
from at_time import to_date

TRADE_FILTER_NAME = "PB_Executed_Stocks"

ael_variables = AelVariableHandler() # pylint: disable=C0103
ael_variables.add("output_path",
                  mandatory=True,
                  default="C:\\",
                  label="Output path")
ael_variables.add("output_name",
                  mandatory=True,
                  default="FA_PB_TRADECONFIRMS_%Y%m%d.csv",
                  label="Output name",
                  alt="The string can contain datetime placeholders for "
                      "formatting date")


def fmt_timestamp(timestamp):
    """Format integer timestamp into a string"""
    return str(timestamp)


def fmt_number(number):
    """Format floating number into a string"""
    if isinstance(number, float):
        return "%.2f" % number
    else:
        return number


SCHEMA = (
    ("Trade", lambda t, c: t.Oid()),
    ("Instrument", lambda t, c: t.Instrument().Name()),
    ("Price", lambda t, c: fmt_number(t.Price())),
    ("Quantity", lambda t, c: t.Quantity()),
    ("Value Day", lambda t, c: t.ValueDay()),
    ("Execution Time", lambda t, c: fmt_timestamp(t.ExecutionTime())),
    ("Portfolio", lambda t, c: t.Portfolio().Name()),
    ("Portfolio's BDA Account Number", lambda t, c: \
            t.Portfolio().AdditionalInfo().Prt_BDA_AccountNum()),
    ("Currency", lambda t, c: t.Currency().Name()),
    ("Bought or Sold", lambda t, c: c("Bought or Sold")),
    ("Type", lambda t, c: t.Instrument().InsType()),
    ("Premium", lambda t, c: fmt_number(t.Premium())),
    ("Daily Equity Brokerage", lambda t, c: \
            fmt_number(c("Daily Equity Brokerage"))),
    ("Daily Equity INS", lambda t, c: fmt_number(c("Daily Equity INS"))),
    ("Daily Equity SET", lambda t, c: fmt_number(c("Daily Equity SET"))),
    ("Securities Transfer Tax", lambda t, c: \
            fmt_number(c("Securities Transfer Tax"))),
    ("Total Consideration", lambda t, c: fmt_number(c("Total Consideration"))),
)


def write_trades(fout, trades, schema):
    """
    Writes trades according the schema into the file fout
    """
    writer = csv.writer(fout)
    writer.writerow([key for key, _gen in schema])
    cspace = prepare_calc_space("FTradeSheet")
    for trade in trades:
        row = [gen(trade, cspace(trade)) for _key, gen in schema]
        row = [str(x) for x in row]
        writer.writerow(row)


def ael_main(data):
    date = to_date("TODAY")
    filename = date.strftime(data["output_name"])
    filepath = os.path.join(data["output_path"], filename)
    print("Starting report")
    trades = acm.FTradeSelection[TRADE_FILTER_NAME].Trades()
    with open(filepath, "wb") as fout:
        write_trades(fout, trades, SCHEMA)
    print("Output file was written to:", filepath)
    print("Finished successfully")

