"""
-------------------------------------------------------------------------------
MODULE
    ShortEndDelta

DESCRIPTION
    Date                : 05/08/2014
    Purpose             : Short end delta report.
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002036323

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
11/09/2014  2275369     Jakub Tomaga    Commit for SPOT prices removed.
-------------------------------------------------------------------------------
"""
import acm
import ael

from IRDShortEndCurveProvision import market_rate_instruments
from Provision import ProvisionHandler, ProvisionNotApplicable
import ProvisionReport
from at_ael_variables import AelVariableHandler
from at_logging import  getLogger, bp_start
from PS_Functions import get_pb_fund_shortname


LOGGER = getLogger()


class ShortEndDeltaError(Exception):
    """General Short End Delta error."""


class ShortEndDeltaReportCreator(ProvisionReport.ProvisionReportCreator):
    """Creates the short end curve report."""
    def __init__(self, report_parameters, source, yield_curve, currency):
        super(ShortEndDeltaReportCreator, self).__init__(
            report_parameters, source, yield_curve, currency)

        self.report_type = ProvisionReport.SHORT_END_DELTA

        self.failed_prices_apply = []
        self.failed_prices_revert = []

    def _collect_data(self):
        """Collect all required data relevant for the report."""
        # Add header
        today = acm.Time().DateToday()
        line = (today, self.source.Name(), self.yield_curve.Name())
        self.content.append(line)

        # Calculate clean provision
        clean = 0.0
        clean_provision = ProvisionHandler(self.yield_curve)
        for trade in self.source.Trades():
            try:
                trade_provision = clean_provision.calculate(trade)
            except ProvisionNotApplicable:
                trade_provision = 0.0
            clean += trade_provision
        LOGGER.info('Clean provision: %s', clean)

        # Add clean provision to the report's content
        line = ('Clean provision', clean, '')
        self.content.append(line)

        instrument_list = market_rate_instruments(ael.date(today),
            self.currency.Name())
        bump = 0.01
        for instrument_name in instrument_list:
            yield_curve_clone = self.yield_curve.Clone()
            instrument = acm.FInstrument[instrument_name]
            prices = instrument.Prices()
            LOGGER.info('Benchmark: %s', instrument_name)
            bumped_prices = []
            for price in prices:
                LOGGER.info('Market:%s', price.Market().Name())            
                if price.Market().Name() == 'SPOT':  # Use SPOT_MIN in Playground
                    LOGGER.info('Shifting price. Current: %s', price.Settle())
                    price_clone = price.Clone()
                    price_clone.Settle = price.Settle() + bump
                    price_clone.Last = price.Last() + bump
                    price_clone.Bid = price.Bid() + bump
                    price_clone.Ask = price.Ask() + bump

                    try:
                        price.Apply(price_clone)
                        bumped_prices.append(price)
                    except:
                        self.failed_prices_apply.append(price)

            # Recalculate yield curve
            yield_curve_clone.Calculate()
            self.yield_curve.Apply(yield_curve_clone)

            moved = 0.0
            moved_provision = ProvisionHandler(self.yield_curve)
            for trade in self.source.Trades():
                try:
                    trade_provision = moved_provision.calculate(trade)
                except ProvisionNotApplicable:
                    trade_provision = 0.0
                moved += trade_provision
            LOGGER.info('Moved provision for %s: %s', instrument_name, moved)
            # Add record to the report's content
            line = (
                instrument_name,
                moved,
                clean - moved
            )
            self.content.append(line)

            # Revert prices
            for price in bumped_prices:
                price_clone = price.Clone()
                price_clone.Settle = price.Settle() - bump
                price_clone.Last = price.Last() - bump
                price_clone.Bid = price.Bid() - bump
                price_clone.Ask = price.Ask() - bump

                try:
                    price.Apply(price_clone)
                except:
                    self.failed_prices_revert.append(price)

            # Recalculate yield curve
            yield_curve_clone.Calculate()
            self.yield_curve.Apply(yield_curve_clone)

    def _header(self):
        """Return header columns."""
        return ([
            "Details",
            "Provision",
            "Delta"
        ])

    @staticmethod
    def _log(message):
        '''Basic console logging with timestamp prefix.'''
        print("{0}: {1}".format(acm.Time.TimeNow(), message))


ael_variables = AelVariableHandler()
ael_variables.add('InputType',
    label='Report Input Type',
    collection=['Filter', 'Portfolio'],
    default='Filter')

ael_variables.add('Portfolio',
    label='Portfolio',
    cls='FPhysicalPortfolio',
    mandatory=False,
    multiple=True)

ael_variables.add('TrdFilter',
    label='Trade Filter',
    cls='FTradeSelection',
    mandatory=False,
    multiple=True)

ael_variables.add('ReportType',
    label='Report Type',
    collection=['Short End Delta'],
    default='Short End Delta')

ael_variables.add('Outpath',
    label='Output Path',
    default='/services/frontnt/Task/')

ael_variables.add('Currency',
    label='Currency',
    cls='FCurrency',
    default='ZAR',
    multiple=True)

ael_variables.add('Curve',
    label='Yield Curve',
    cls='FYieldCurve',
    default='ZAR-SWAP',
    multiple=True)

ael_variables.add("clientName",
                  label="Client Name",
                  cls='FCounterParty',
                  mandatory=False)

def ael_main(config, for_report_controller=False):

    process_name = "short_end_delta"
    if config.has_key("clientName") and config["clientName"]:
        # This parameter is passed from other modules (ex PS_RiskSwapAttribution_Report).
        process_name = "short_end_delta.{0}".format(get_pb_fund_shortname(config["clientName"]))
    
    with bp_start(process_name):
        
        file_suffix = 'xls'
        csv_writer_parameters = {'dialect': 'excel-tab'}
    
        path_split = config['Outpath'].replace('\\', '/').split('/')
        path = '/'.join(path_split[0:-1])
        file_name = path_split[-1]
    
        if config['InputType'] == 'Portfolio':
            source = config['Portfolio'][0]
        else:
            source = config['TrdFilter'][0]
        yield_curve = config['Curve'][0]
        currency = config['Currency'][0]
    
        report_parameters = {
            'file_name': file_name,
            'file_suffix': file_suffix,
            'path': path,
            'csv_writer_parameters': csv_writer_parameters
        }
    
        report = ShortEndDeltaReportCreator(report_parameters, source, yield_curve,
            currency)
        if for_report_controller:
            report._collect_data()
            return report.content[2:]
        report.create_report()
    
        if not report.failed_prices_apply and not report.failed_prices_revert:
            LOGGER.info('Wrote secondary output to %s', report._full_path)
            LOGGER.info('Completed Successfully')
        else:
            LOGGER.error('Price adjustment failed.')
            for price in report.failed_prices_apply:
                LOGGER.error('Failed to bump price with ID %s(%s)',
                             price.Oid(), price.Instrument().Name())
    
            for price in report.failed_prices_revert:
                LOGGER.error('Failed to revert bumped price with ID %s(%s)',
                             price.Oid(), price.Instrument().Name())
