"""
-------------------------------------------------------------------------------
MODULE
    on_tree_trade_report

DESCRIPTION
    Date                : 2017-04-12
    Purpose             : PCG is required post ledger entries at a trade level
                          per portfolio in new GLS service platform. This
                          report provides latest trade in all physical
                          portfolios for a given date under given compound.
    Department and Desk : Product Control Group
    Requester           : Stefan Du Toit
    Developer           : Jakub Tomaga
    CR Number           : CHNG0004491729

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
12-04-2017  4491729     Jakub Tomaga    Initial implementation.
-------------------------------------------------------------------------------
"""

import string
import os.path
import acm
from at_ael_variables import AelVariableHandler
from at_report import CSVReportCreator
from at_time import to_datetime


class BaseReport(CSVReportCreator):
    """Base class simplifying file path handling."""
    def __init__(self, full_file_path):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)

        super(BaseReport, self).__init__(
            file_name_only,
            file_suffix,
            file_path)


class TradeReport(BaseReport):
    """Creates the report."""
    def __init__(self, full_file_path, compound_portfolio, my_date):
        self.compound_portfolio = compound_portfolio
        self.my_date = my_date
        super(TradeReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for portfolio in self.compound_portfolio.AllPhysicalPortfolios():
            trades = list(portfolio.Trades())
            if trades:
                for trade in reversed(trades):
                    if trade.Status() in ["Simulated", "Terminated", "Void"]:
                        continue
                    if str(to_datetime(trade.CreateTime())).split(" ")[0] > self.my_date:
                        continue
                    line = [
                        trade.Portfolio().Name(),
                        trade.Oid(),
                        trade.Instrument().Name(),
                        trade.Trader().Name() if trade.Trader() else "None",
                        to_datetime(trade.CreateTime()),
                        trade.Status()
                    ]
                    self.content.append(line)
                    break

    def _header(self):
        """Return columns of the header."""
        header = [
            "Portfolio",
            "Trade Number",
            "Instrument Name",
            "Trader",
            "Create Time",
            "Status"
        ]
        return header

    @staticmethod
    def log(message):
        """Basic console logging with time stamp prefix."""
        print("{0}: {1}".format(acm.Time.TimeNow(), message))
        

ael_variables = AelVariableHandler()
ael_variables.add_directory("output_directory",
                            label="Ouput Directory",
                            default="/services/frontnt/Task")
ael_variables.add("file_name",
                 label="File Name",
                 default="on_tree_trade_report.csv")
ael_variables.add("compound_portfolio",
                 label="Compound Portfolio",
                 cls=acm.FCompoundPortfolio,
                 collection=sorted(acm.FCompoundPortfolio.Select("")),
                 default=acm.FCompoundPortfolio["PRIME BROKER"])
ael_variables.add("my_date",
                  label="Date")

def ael_main(config):
    fpath_template = string.Template(config["file_name"])
    my_date = config["my_date"]
    file_path = fpath_template.substitute(DATE=my_date.replace("-", ""))
    full_file_path = os.path.join(str(config["output_directory"]), file_path)
    report = TradeReport(full_file_path, config["compound_portfolio"], my_date)
    report.log('Generating on-tree trade report...')
    report.create_report()
    report.log("Secondary output wrote to {0}".format(full_file_path))
    report.log("Completed successfully")
