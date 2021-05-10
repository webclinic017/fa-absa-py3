"""
-------------------------------------------------------------------------------
MODULE
    ProvisionReport

DESCRIPTION
    Date                : 05/08/2014
    Purpose             : Basic provision report with banner.
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002036323

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
02/10/2014  2325358     Jakub Tomaga    Support for price testing added.
-------------------------------------------------------------------------------
"""

import acm
from at_report import CSVReportCreator


PROVISION_PER_RESET = 'Provision Per Reset'
PROVISION_PER_RESET_BUCKET = 'Provision Per Reset Bucket'
RESET_RISK = 'Reset Risk'
SHORT_END_DELTA = 'Short End Delta'


class ProvisionReportError(Exception):
    """General provision report error."""


class ProvisionReportCreator(CSVReportCreator):
    """Creates provision report with banner."""
    def __init__(self, report_parameters, source, yield_curve, currency,
            market_rate_instruments=None):
        super(ProvisionReportCreator, self).__init__(
            report_parameters['file_name'],
            report_parameters['file_suffix'],
            report_parameters['path'],
            report_parameters['csv_writer_parameters']
        )

        self.source = source
        self.yield_curve = yield_curve
        self.currency = currency
        self.report_type = None
        self.market_rate_instruments = market_rate_instruments

    def _collect_data(self):
        """This enables initialise subclasses with content through __init__."""
        pass

    def _banner(self):
        """Return report's banner."""
        if self.source.IsKindOf(acm.FTradeSelection):
            input_data_type = 'Filter'
        elif self.source.IsKindOf(acm.FPhysicalPortfolio):
            input_data_type = 'Portfolio'
        else:
            message = "Invalid input data type: {0}".format(type(self.source))
            raise ProvisionReportError(message)

        banner = []
        banner.append(['Report Type: ', self.report_type])
        banner.append(['Input Data Type: ', input_data_type])
        banner.append(['Input Data Name: ', self.source.Name()])
        banner.append(['Currency: ', self.currency.Name()])
        banner.append(['Yield Curve: ', self.yield_curve.Name()])

        return banner
