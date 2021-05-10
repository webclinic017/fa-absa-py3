"""
-------------------------------------------------------------------------------
MODULE
    acs_funding_portfolio_report

DESCRIPTION
    Purpose             : Interdesk funding
    Department and Desk : ACS Post Trade Services
    Requester           : Jennitha Jugnath and Martin Wortmann
    Developer           : Jakub Tomaga

HISTORY
===============================================================================
Date        CR number           Developer       Description
-------------------------------------------------------------------------------
2019-04-17  CHG1001639975       Jakub Tomaga    Initial implementation.
"""

import os
import logging
import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_report import CSVReportCreator


# Logging
LOGGER = getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
VERSION = "1.0"


class ACSFundingPortfolioReport(CSVReportCreator):
    """Report displaying portfolio level."""
    def __init__(self, full_file_path, compound):
        self.compound = compound
        # Split full path into individual parameters of the parent class.
        file_name_only, file_suffix = os.path.splitext(full_file_path)
        # Remove a dot from the extension
        file_suffix = file_suffix[1:]
        file_path = os.path.dirname(full_file_path)
        super(ACSFundingPortfolioReport, self).__init__(
            file_name_only,
            file_suffix,
            file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for portfolio in self.compound.AllPhysicalPortfolios():
            row = [
                portfolio.Oid(),
                portfolio.Name(),
                portfolio.AdditionalInfo().Prt_BDA_AccountNum(),
                portfolio.AdditionalInfo().CostCenter(),
                portfolio.AdditionalInfo().FundingIndicator()
            ]
            self.content.append(row)

    def _header(self):
        """Return columns of the header."""
        header = [
          "Portfolio Number",
          "Portfolio Name",
          "prt_BDA AccountNum",
          "CostCenter",
          "FundingIndicator"
        ]
        return header


ael_variables = AelVariableHandler()
ael_variables.add("output_file",
                  label="Output file")
ael_variables.add("compound",
                  label="Compound portfolio",
                  cls=acm.FCompoundPortfolio,
                  default=acm.FCompoundPortfolio["ABSA CAPITAL SECURITIES"])


def ael_main(config):
    """Entry point of the script."""
    compound = config["compound"]
    output_file = config["output_file"]
    
    # Generate the report
    report = ACSFundingPortfolioReport(output_file, compound)
    try:
        report.create_report()
        LOGGER.info("Secondary output wrote to %s", output_file)
    except Exception as ex:
        LOGGER.exception("Failed to generate the report %s", ex)
        raise ex
