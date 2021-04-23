"""
-------------------------------------------------------------------------------
MODULE
    ShortEndProvisionReport

DESCRIPTION
    Date                : 05/08/2014
    Purpose             : Various specialised short end provision reports.
    Department and Desk : Middle Office
    Requester           : Helder Loio
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002036323

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
05-09-2014  2234300      Jakub Tomaga   - 'future' trades excluded from
                                          calculation
02/10/2014  2325358     Jakub Tomaga    Support for price testing added.
-------------------------------------------------------------------------------
"""
import acm
import ael
from datetime import datetime

from Provision_SimulatedTrades import (ProvisionHandler, ProvisionNotApplicable,
    VALID_TRADE_STATUSES)
import ProvisionReport
import at_logging


LOGGER = at_logging.getLogger()


def sanitize(name):
    """Remove directory delimiters from names used to construct filename."""
    if '/' in name:
        name = name.replace('/', '_')
    elif '\\' in name:
        name = name.replace('\\', '_')

    return name


class ShortEndProvisionError(Exception):
    """General error."""


class ShortEndProvisionHandler(ProvisionHandler):
    """Common parent class for 'bucket' handling reports."""

    # Nominal indices
    _NOMINAL_1M = 0
    _NOMINAL_3M = 1
    _NOMINAL_6M = 2
    _NOMINAL_9M = 3
    _NOMINAL_12M = 4

    def __init__(self, yield_curve, market_rate_instruments):
        super(ShortEndProvisionHandler, self).__init__(yield_curve,
            market_rate_instruments)
        self.report_content = []

    def _bucket_index(self, reset_period):
        """Return bucket index for reset period: 1m, 3m, 6m, 9m, 12m."""
        if reset_period < 0.2:
            return self._NOMINAL_1M
        elif reset_period >= 0.2 and reset_period < 0.45:
            return self._NOMINAL_3M
        elif reset_period >= 0.45 and reset_period < 0.7:
            return self._NOMINAL_6M
        elif reset_period >= 0.7 and reset_period < 1:
            return self._NOMINAL_9M
        else:
            return self._NOMINAL_12M


class ProvisionPerResetHandler(ShortEndProvisionHandler):
    """Specialised handler for Provision Per Reset report.

    Creates report records from the progress of provision calculation.

    """
    def __init__(self, yield_curve, currency, market_rate_instruments):
        super(ProvisionPerResetHandler, self).__init__(yield_curve,
            market_rate_instruments)
        self.reset_dict = {}
        self.risk_content = []
        self.report_type = ProvisionReport.PROVISION_PER_RESET

    def _create_report_record(self, trade, common_object, reset_period,
            nominal, provision, short_end_rate, forward_rate):
        """Create reset and risk report records."""
        if common_object.IsKindOf(acm.FReset):
            reset_day = common_object.Day()
        elif common_object.IsKindOf(acm.FCashFlow):
            reset_day = common_object.StartDate()
        else:
            message = "Undefined report structure for type {0}".format(
                type(common_object))
            raise ShortEndProvisionError(message)
        index = self._bucket_index(reset_period)

        buckets = [0, 0, 0, 0, 0]
        buckets[index] = nominal

        key = reset_day
        if key in self.reset_dict:
            record = self.reset_dict[key]
            record[index + 1] += nominal
            record[6] += provision
        else:
            record = []
            record.append(reset_day)
            record.extend(buckets)
            record.append(provision)
            self.reset_dict[key] = record

        if common_object.IsKindOf(acm.FReset):
            reset_type = common_object.ResetType()
            reset_day = common_object.Day()
        elif common_object.IsKindOf(acm.FCashFlow):
            reset_type = ''
            reset_day = common_object.StartDate()

        if common_object.Instrument().InsType() == 'CurrSwap':
            rate_ref = common_object.Leg().FixedRate()
        else:
            rate_ref = common_object.Leg().FloatRateReference().Name()

        self.risk_content.append([
            trade.Oid(),
            common_object.Instrument().InsType(),
            common_object.Leg().RollingPeriodCount(),
            common_object.Leg().RollingPeriodUnit(),
            reset_type,
            reset_day,
            common_object.StartDate(),
            common_object.EndDate(),
            rate_ref,
            buckets[self._NOMINAL_1M],
            buckets[self._NOMINAL_3M],
            buckets[self._NOMINAL_6M],
            buckets[self._NOMINAL_9M],
            buckets[self._NOMINAL_12M],
            common_object.Leg().Currency().Name(),
            reset_period,
            self.forward_yield_curve.Name(),
            forward_rate,
            short_end_rate,
            provision
        ])


class ProvisionPerResetReport(object):
    """Report wrapper for generating two different reports.

    This class wraps two individual ProvisionReportCreators that generate
    Risk and Reset report.

    """

    class RiskReportCreator(ProvisionReport.ProvisionReportCreator):
        """Risk Report for Provision Per Reset.

        Just fill report with content from provision. handler.

        """
        def __init__(self, report_parameters, source, yield_curve, currency,
                     content):
            super(ProvisionPerResetReport.RiskReportCreator, self).__init__(
                report_parameters, source, yield_curve, currency)
            self.content = content
            self.report_type = ProvisionReport.PROVISION_PER_RESET

        def _header(self):
            """Specific header."""
            return ([
                "Trade",
                "Instrument",
                "Rolling Period Count",
                "Rolling Period Unit",
                "ResetType",
                "Reset Day",
                "Reset Start",
                "Reset End",
                "Float Ref",
                "Nominal 1m",
                "Nominal 3m",
                "Nominal 6m",
                "Nominal 9m",
                "Nominal 12m",
                "Currency",
                "Reset Period",
                "Forward Curve",
                "Forward Rate",
                "Mkt Rate",
                "ZAR Provision"
            ])

    class ResetReportCreator(ProvisionReport.ProvisionReportCreator):
        """Reset report for Provision Per Reset.

        Just fill report with content from provision. handler.

        """
        def __init__(self, report_parameters, source, yield_curve, currency,
                content):
            super(ProvisionPerResetReport.ResetReportCreator, self).__init__(
                report_parameters, source, yield_curve, currency)
            self.content = content
            self.report_type = ProvisionReport.PROVISION_PER_RESET

        def _header(self):
            """Specific header."""
            return ([
                'ResetDay',
                'Nominal 1m',
                'Nominal 3m',
                'Nominal 6m',
                'Nominal 9m',
                'Nominal 12m',
                'ZAR Provision'
            ])

    def __init__(self, file_suffix, path, csv_writer_parameters, source,
             yield_curve, currency, market_rate_instruments):
        """Initialise reports' wrapper."""
        if source.IsKindOf(acm.FTradeSelection):
            input_type = 'Filter'
        else:
            input_type = 'Portfolio'

        source_name = sanitize(source.Name())
        currency_name = sanitize(currency.Name())
        yield_curve_name = sanitize(yield_curve.Name())

        file_name = '_'.join([path + 'Data_File', input_type, source_name,
            currency_name, yield_curve_name, 'ProvisionPerReset', 'Per_Reset'])
        reset_report_file_name = file_name
        risk_report_file_name = '_'.join([file_name, 'Day'])

        self.reset_report_parameters = {
            'file_name': reset_report_file_name,
            'file_suffix': file_suffix,
            'path': path,
            'csv_writer_parameters': csv_writer_parameters
        }
        self.risk_report_parameters = {
            'file_name': risk_report_file_name,
            'file_suffix': file_suffix,
            'path': path,
            'csv_writer_parameters': csv_writer_parameters
        }
        self.source = source
        self.yield_curve = yield_curve
        self.currency = currency

        self.market_rate_instruments = market_rate_instruments

    def create_reports(self):
        """Calculate provision and generate two reports."""
        # Calculate provision
        provision_handler = ProvisionPerResetHandler(self.yield_curve,
            self.currency, self.market_rate_instruments)
        total_provision = 0.0
        for trade in self.source.Trades():
            try:
                trade_provision = provision_handler.calculate(trade)
            except ProvisionNotApplicable:
                trade_provision = 0.0
            total_provision += trade_provision

        LOGGER.info("Total provision: %s", total_provision)

        # Generate reset report
        reset_content = provision_handler.reset_dict.values()
        reset_content.sort(lambda x, y: cmp(acm.Time().AsDate(x[0]), acm.Time().AsDate(y[0])))
        reset_report = ProvisionPerResetReport.ResetReportCreator(
            self.reset_report_parameters, self.source, self.yield_curve,
            self.currency, reset_content)
        reset_report.create_report()
        LOGGER.info('Wrote secondary output to: %s.%s',
                    self.reset_report_parameters['file_name'], self.reset_report_parameters['file_suffix'])

        # Generate risk report
        risk_content = provision_handler.risk_content
        risk_report = ProvisionPerResetReport.RiskReportCreator(
            self.risk_report_parameters, self.source, self.yield_curve,
            self.currency, risk_content)
        risk_report.create_report()
        LOGGER.info('Wrote secondary output to %s.%s',
            self.risk_report_parameters['file_name'],
            self.risk_report_parameters['file_suffix'])

        LOGGER.info('Completed Successfully')


class ProvisionPerResetClientHandler(ShortEndProvisionHandler):
    """Specialised handler for Provision Per Reset reports (per client)."""
    def __init__(self, yield_curve):
        super(ProvisionPerResetClientHandler, self).__init__(yield_curve, None)
        self.risk_content = []
        self.report_type = ProvisionReport.PROVISION_PER_RESET

    def _create_report_record(self, trade, common_object, reset_period,
            nominal, provision, short_end_rate, forward_rate):
        """Create specialise report records."""
        if common_object.IsKindOf(acm.FReset):
            reset_day = common_object.Day()
            reset_type = common_object.ResetType()
        elif common_object.IsKindOf(acm.FCashFlow):
            reset_day = common_object.StartDate()
            reset_type = ''
        else:
            message = "Undefined report structure for type {0}".format(
                type(common_object))
            raise ShortEndProvisionError(message)

        index = self._bucket_index(reset_period)
        buckets = [0, 0, 0, 0, 0]
        buckets[index] = nominal

        if common_object.Instrument().InsType() == 'CurrSwap':
            rate_ref = common_object.Leg().FixedRate()
        else:
            rate_ref = common_object.Leg().FloatRateReference().Name()

        self.risk_content.append([
            trade.Oid(),
            trade.add_info('PS_ClosedOut'),
            common_object.Instrument().InsType(),
            common_object.Leg().RollingPeriodCount(),
            common_object.Leg().RollingPeriodUnit(),
            reset_type,
            reset_day,
            common_object.StartDate(),
            common_object.EndDate(),
            rate_ref,
            buckets[self._NOMINAL_1M],
            buckets[self._NOMINAL_3M],
            buckets[self._NOMINAL_6M],
            buckets[self._NOMINAL_9M],
            buckets[self._NOMINAL_12M],
            common_object.Leg().Currency().Name(),
            reset_period,
            self.forward_yield_curve.Name(),
            forward_rate,
            short_end_rate,
            provision
        ])


class ProvisionPerResetClientReportCreator(ProvisionReport.ProvisionReportCreator):
    """Report creator for Provision Per Reset Client report.

    Unlike other report types (wrappers) - only one report is generated here.

    """
    def __init__(self, report_parameters, source, yield_curve, currency):
        super(ProvisionPerResetClientReportCreator, self).__init__(
            report_parameters, source, yield_curve, currency)
        self.report_type = ProvisionReport.PROVISION_PER_RESET

    def _collect_data(self):
        """Collect all required data relevant for the report."""
        provision_handler = ProvisionPerResetClientHandler(self.yield_curve)
        total_provision = 0.0
        for trade in self.source.Trades():
            try:
                trade_provision = provision_handler.calculate(trade)
            except ProvisionNotApplicable as ex:
                trade_provision = 0.0
            total_provision += trade_provision

        self.content = provision_handler.risk_content
        LOGGER.info("Total provision: %s", total_provision)

    def _header(self):
        """Specific header."""
        return ([
            "Trade",
            "Closed Out",
            "Instrument",
            "Rolling Period Count",
            "Rolling Period Unit",
            "ResetType",
            "Reset Day",
            "Reset Start",
            "Reset End",
            "Float Ref",
            "Nominal 1m",
            "Nominal 3m",
            "Nominal 6m",
            "Nominal 9m",
            "Nominal 12m",
            "Currency",
            "Reset Period",
            "Forward Curve",
            "Forward Rate",
            "Mkt Rate",
            "ZAR Provision"
        ])


class ProvisionPerResetBucketHandler(ShortEndProvisionHandler):
    """Specialised handler for Provision Per Reset Bucket report."""
    def __init__(self, yield_curve, market_rate_instruments):
        super(ProvisionPerResetBucketHandler, self).__init__(yield_curve,
            market_rate_instruments)
        self.reset_dict = {}
        self.report_type = ProvisionReport.PROVISION_PER_RESET_BUCKET

    def _create_report_record(self, trade, common_object, reset_period,
            nominal, provision, short_end_rate, forward_rate):
        """Create specialise report records."""
        key = (common_object.StartDate(), common_object.EndDate())
        if key in self.reset_dict:
            self.reset_dict[key][2] += nominal
            self.reset_dict[key][5] += provision
        else:
            day_count_method = common_object.Leg().DayCountMethod()
            if day_count_method != 'Act/365':
                rate_start_date, rate_end_date = self._rate_dates(common_object)
                forward_rate = self.forward_yield_curve_ael.yc_rate(
                    ael.date(rate_start_date), ael.date(rate_end_date),
                    'Quarterly', 'Act/365', 'Forward Rate')

            self.reset_dict[key] = [
                common_object.StartDate(),
                common_object.EndDate(),
                nominal,
                forward_rate,
                short_end_rate,
                provision
            ]


class ProvisionPerResetBucketReportCreator(ProvisionReport.ProvisionReportCreator):
    """Report creator for Provision Per Reset Bucket report.

    Unlike other report types (wrappers) - only one report is generated here.

    """
    def __init__(self, report_parameters, source, yield_curve, currency,
                market_rate_instruments):
            super(ProvisionPerResetBucketReportCreator, self).__init__(
                report_parameters, source, yield_curve, currency,
                market_rate_instruments)
            self.report_type = ProvisionReport.PROVISION_PER_RESET_BUCKET

    def _collect_data(self):
        """Collect all required data relevant for the report."""
        provision_handler = ProvisionPerResetBucketHandler(self.yield_curve,
            self.market_rate_instruments)
        total_provision = 0.0
        for trade in self.source.Trades():
            try:
                trade_provision = provision_handler.calculate(trade)
            except ProvisionNotApplicable:
                trade_provision = 0.0
            total_provision += trade_provision

        self.content = provision_handler.reset_dict.values()
        self.content.sort(lambda x, y: cmp(acm.Time().AsDate(x[1]), acm.Time().AsDate(y[1])))
        self.content.sort(lambda x, y: cmp(acm.Time().AsDate(x[0]), acm.Time().AsDate(y[0])))
        LOGGER.info("Total provision: %s", total_provision)

    def _header(self):
        """Specific header."""
        return ([
            "StartDate",
            "EndDate",
            "Nominal",
            "FwdRate",
            "SE rate",
            "Provision"
        ])


class ResetRiskHandler(ShortEndProvisionHandler):
    """Handler for reset risk reports"""
    def __init__(self, yield_curve, currency, market_rate_instruments):
        super(ResetRiskHandler, self).__init__(yield_curve,
            market_rate_instruments)
        self.reset_dict = {}
        self.risk_content = []
        self.report_type = ProvisionReport.RESET_RISK

    def calculate(self, trade):
        """Return reset risk record for trade."""
        self._calculate(trade)

    def _is_valid_trade(self, trade):
        """Simplified trade validation."""
        if not trade:
            return False

        if trade.Status() in VALID_TRADE_STATUSES:
            if acm.Time().AsDate(trade.TradeTime()) > self.start_date:
                return False

            instrument_type = trade.Instrument().InsType()
            if instrument_type == 'Curr':
                if trade.ValueDay() > self.start_date:
                    return True
            elif instrument_type == 'Combination':
                for comb_instrument in trade.Instrument().Instruments():
                    comb_trades = comb_instrument.Trades()
                    if comb_trades:
                        comb_trade = comb_trades[0]
                        if comb_trade.Status() in VALID_TRADE_STATUSES:
                            return True
            else:
                if trade.Instrument().ExpiryDateOnly() > self.start_date:
                    return True

        return False

    def _is_valid_cashflow(self, cash_flow):
        """Return True if cash flow is valid, otherwise return False."""
        if not cash_flow.StartDate() or not cash_flow.EndDate():
            return False

        if (cash_flow.EndDate() >= self.start_date and
                cash_flow.StartDate() <= self.end_date):
            return True

        return False

    def _calculate(self, trade):
        """Simplified calculation for Reset Risk report."""
        if not self._is_valid_trade(trade):
            return

        for leg in trade.Instrument().Legs():
            if leg.LegType() not in ['Call Float', 'Float']:
                continue
            if leg.Currency() != self.currency:
                continue
            if not leg.FloatRateReference():
                continue
            if self.forward_yield_curve != self._mapped_forward_curve(leg):
                continue

            for cash_flow in leg.CashFlows():
                # Verify if provision is applicable for cash flow
                if not self._is_valid_cashflow(cash_flow):
                    continue
                for reset in cash_flow.Resets():
                    # Verify if provision is applicable for reset
                    if not self._is_valid_reset(reset):
                        continue

                    reset_period = self._reset_period(reset)
                    nominal = self._trade_nominal(trade, cash_flow)
                    index = self._bucket_index(reset_period)
                    buckets = [0, 0, 0, 0, 0]
                    buckets[index] = nominal

                    reset_day = reset.Day()
                    key = reset_day
                    if key in self.reset_dict:
                        record = self.reset_dict[key]
                        record[index + 1] += nominal
                    else:
                        record = []
                        record.append(reset_day)
                        record.extend(buckets)
                        self.reset_dict[key] = record

                    self.risk_content.append([
                        trade.Oid(),
                        reset.Instrument().InsType(),
                        leg.RollingPeriodCount(),
                        leg.RollingPeriodUnit(),
                        reset.ResetType(),
                        reset_day,
                        reset.StartDate(),
                        reset.EndDate(),
                        leg.FloatRateReference().Name(),
                        buckets[self._NOMINAL_1M],
                        buckets[self._NOMINAL_3M],
                        buckets[self._NOMINAL_6M],
                        buckets[self._NOMINAL_9M],
                        buckets[self._NOMINAL_12M],
                        leg.Currency().Name(),
                        reset_period
                    ])


class ResetRiskReport(object):
    """Report for generating two different reports."""

    class RiskReportCreator(ProvisionReport.ProvisionReportCreator):
        """Risk report for Reset Risk report wrapper.

        Just fill report with content from provision. handler.

        """
        def __init__(self, report_parameters, source, yield_curve, currency, content):
            super(ResetRiskReport.RiskReportCreator, self).__init__(
                report_parameters, source, yield_curve, currency)
            self.content = content
            self.report_type = ProvisionReport.RESET_RISK

        def _header(self):
            """Specific header."""
            return ([
                "Trade",
                "Instrument",
                "Rolling Period Count",
                "Rolling Period Unit",
                "ResetType",
                "Reset Day",
                "Reset Start",
                "Reset End",
                "Float Ref",
                "Nominal 1m",
                "Nominal 3m",
                "Nominal 6m",
                "Nominal 9m",
                "Nominal 12m",
                "Currency",
                "Reset Period"
            ])

    class ResetReportCreator(ProvisionReport.ProvisionReportCreator):
        """Reset report for Reset Risk report wrapper.

        Just fill report with content from provision. handler.

        """
        def __init__(self, report_parameters, source, yield_curve, currency, content):
            super(ResetRiskReport.ResetReportCreator, self).__init__(
                report_parameters, source, yield_curve, currency)
            self.content = content
            self.report_type = ProvisionReport.RESET_RISK

        def _header(self):
            """Specific header."""
            return ([
                'ResetDay',
                'Nominal 1m',
                'Nominal 3m',
                'Nominal 6m',
                'Nominal 9m',
                'Nominal 12m'
            ])

    def __init__(self, file_suffix, path, csv_writer_parameters, source,
             yield_curve, currency, market_rate_instruments):

        if source.IsKindOf(acm.FTradeSelection):
            input_type = 'Filter'
        else:
            input_type = 'Porfolio'

        source_name = sanitize(source.Name())
        currency_name = sanitize(currency.Name())
        yield_curve_name = sanitize(yield_curve.Name())

        file_name = '_'.join([path + 'Data_File', input_type, source_name,
            currency_name, yield_curve_name, 'ResetRisk', 'Per_Reset'])
        reset_report_file_name = file_name
        risk_report_file_name = '_'.join([file_name, 'Day'])

        self.reset_report_parameters = {
            'file_name': reset_report_file_name,
            'file_suffix': file_suffix,
            'path': path,
            'csv_writer_parameters': csv_writer_parameters
        }
        self.risk_report_parameters = {
            'file_name': risk_report_file_name,
            'file_suffix': file_suffix,
            'path': path,
            'csv_writer_parameters': csv_writer_parameters
        }
        self.source = source
        self.yield_curve = yield_curve
        self.currency = currency
        self.market_rate_instruments = market_rate_instruments

    def create_reports(self):
        # Calculate provision
        handler = ResetRiskHandler(self.yield_curve, self.currency,
            self.market_rate_instruments)
        for trade in self.source.Trades():
            handler.calculate(trade)

        # Generate reset report
        reset_content = handler.reset_dict.values()
        reset_content.sort(lambda x, y: cmp(acm.Time().AsDate(x[0]), acm.Time().AsDate(y[0])))
        reset_report = ResetRiskReport.ResetReportCreator(
            self.reset_report_parameters, self.source, self.yield_curve,
            self.currency, reset_content)

        reset_report.create_report()
        LOGGER.info('Wrote secondary output to %s.%s',
                    self.reset_report_parameters['file_name'],
                    self.reset_report_parameters['file_suffix'])

        # Generate risk report
        risk_content = handler.risk_content
        risk_report = ResetRiskReport.RiskReportCreator(
            self.risk_report_parameters, self.source, self.yield_curve,
            self.currency, risk_content)
        risk_report.create_report()
        LOGGER.info('Wrote secondary output to %s.%s',
                    self.risk_report_parameters['file_name'],
                    self.risk_report_parameters['file_suffix'])

        LOGGER.info('Completed Successfully')


class PSResetRiskReport(object):
    """Report for generating Reset Risk Report for ReportController2"""

    class PSResetReportCreator(ProvisionReport.ProvisionReportCreator):
        """Reset report for Reset Risk report wrapper.

        Just fill report with content from provision. handler.

        """
        def __init__(self, report_parameters, source, yield_curve, currency, content, frameworkVersion):
            super(PSResetRiskReport.PSResetReportCreator, self).__init__(
                report_parameters, source, yield_curve, currency)
            self.report_type = ProvisionReport.RESET_RISK
            self.frameworkVersion = frameworkVersion
            next_mpc_dates = PSResetRiskReport.PSResetReportCreator.PickUpMPC('MO_MPC_ZAR', acm.Time().DateToday())
            contentDict = {}
            for line in content:
                contentDict[line[0]] = line[:-2]
            for mpcDate in next_mpc_dates:
                if mpcDate not in contentDict:
                    contentDict[mpcDate] = [mpcDate, 0, 0, 0]
            l1 = contentDict.values()
            l1.sort(lambda x, y: cmp(acm.Time().AsDate(x[0]), acm.Time().AsDate(y[0])))
            for l in l1:
                if l[0] in next_mpc_dates:
                    l.insert(1, 'MPC')
                else:
                    l.insert(1, '')
            self.content = l1
            self.sourceName = source.Name()
            
        def _header(self):
            """Specific header."""
            return ([
                'ResetDay',
                'MPC Meeting',
                'Nominal 1m',
                'Nominal 3m',
                'Nominal 6m'
            ])

        def _banner(self):
            generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            UTC_offset = (datetime.now() - datetime.utcnow()).seconds / 3600
            generated_time += ' (UTC+0%i:00)' % UTC_offset
            return ([[],
                    ['            Report Name:', 'File_RiskResetDates'],
                    ['            Generated Time:', generated_time],
                    ['            Report Date:', acm.Time().DateToday()],
                    ['            Version:', self.frameworkVersion],
                    [],
                    [self.sourceName]])

        @staticmethod
        def PickUpMPC(TSspec_Name, acmdate):

            date_list = []
            tsspec = acm.FTimeSeriesSpec[TSspec_Name]
            ts = tsspec.TimeSeries()

            for t in ts:
                if acm.Time().AsDate(t.Day()) > acmdate:
                    date_list.append(t.Day())

            date_list.sort(lambda x, y: cmp(acm.Time().AsDate(x), acm.Time().AsDate(y)))

            if not date_list:
                msg = ('ERROR: DATA PROBLEM, script will fail. The time series (%s) needs to have a date in the future.'
                'Please ask MO to complete it.' % TSspec_Name)
                LOGGER.error(msg)
                raise ValueError(msg)

            return date_list

    def __init__(self, file_suffix, path, csv_writer_parameters, source,
             yield_curve, currency, frameworkVersion, file_name):
        self.frameworkVersion = frameworkVersion
        self.file_name = file_name
        reset_report_file_name = file_name

        self.reset_report_parameters = {
            'file_name': reset_report_file_name,
            'file_suffix': file_suffix,
            'path': path,
            'csv_writer_parameters': csv_writer_parameters
        }

        self.source = source
        self.yield_curve = yield_curve
        self.currency = currency

    def create_reports(self):
        # Calculate provision
        handler = ResetRiskHandler(self.yield_curve, self.currency, None)
        for trade in self.source.Trades():
            handler.calculate(trade)

        # Generate reset report
        reset_content = handler.reset_dict.values()
        reset_content.sort(lambda x, y: cmp(acm.Time().AsDate(x[0]), acm.Time().AsDate(y[0])))
        reset_report = PSResetRiskReport.PSResetReportCreator(
            self.reset_report_parameters, self.source, self.yield_curve,
            self.currency, reset_content, self.frameworkVersion)

        reset_report.create_report()
        
        LOGGER.info('Wrote secondary output to %s%s.%s',
                    self.reset_report_parameters['path'],
                    self.reset_report_parameters['file_name'],
                    self.reset_report_parameters['file_suffix'])

        LOGGER.info('Completed Successfully')
