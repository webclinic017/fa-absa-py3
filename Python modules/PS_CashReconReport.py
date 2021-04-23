"""
-------------------------------------------------------------------------------
MODULE
    PS_CashReconReport

DESCRIPTION
    Date                : 2014-06-05
    Purpose             : This module contains an implementation of Cash Recon
                          Report
    Department and Desk : Prime Services Client Coverage
    Requester           : Ruth Forssman
    Developer           : Jakub Tomaga
    CR Number           : CHNG0001994700

HISTORY
==================================================================================
Date        CR number     Developer         Description
----------------------------------------------------------------------------------
24-06-2014  2049721       Jakub Tomaga      Cash flows from non-banking days are
                                            now taken into account (e.g. weekend
                                            corrections are reflected in the recon)
14-08-2014  2192483       Jakub Tomaga      List of active clients retrieved from
                                            Front Arena (PB_FINANCING portfolio)
14-08-2014  2203781       Jakub Tomaga      Support for strategies added for
                                            identifying backdated cash flows.
21-10-2014  2375043       Jakub Tomaga      Error message for malfunction business
                                            data in static reports added.
11-12-2014  2512804       Jakub Tomaga      Cash Recon Tool aligned with new
                                            reporting suite.
24-05-2017  FAU-938       Vojtech Sidorin   Update dependency on elementtree.
2018-11-12  CHG1001113453 Tibor Reiss       Enable fully funded CFD for MMIBETA2,
                                            exclude this client from cash recon
2019-03-27  FAPE-65       Tibor Reiss       Remove fully funded CFD for MMIBETA2
2019-07-17  FAPE-47       Iryna Shcherbina  Settlement control tab.
2019-09-05  FAU-331       Tibor Reiss       Update file name for CFD pswaps
2020-01-09  FAPE-154      Iryna Shcherbina  Enable deposits. Check the Call Account
                                            even if no records in the performance report.
2020-01-29  FAPE-120      Tibor Reiss       Correct 2020 breaks due to FAPE-120
                                            BREAK_FAPE_120 should be removed 2021
2020-02-04  FAPE-206      Tibor Reiss       Correct 2020 break for MARKSOL
                                            Should also be removed 2021
2021-02-09  INC2334943    Marcus Ambrose    Override perfromance path for COGITIO
----------------------------------------------------------------------------------
"""

import os
import csv
import math

from xml.etree import ElementTree
from collections import defaultdict
from collections import namedtuple

import acm
from at_collections import NestedDict
from at_logging import getLogger
from at_report import DataToXMLReportCreator
from at_time import to_datetime
from PS_FormUtils import DateField
from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_fund_shortname,
                          get_pb_fund_counterparty,
                          get_pb_reporting_portfolio)


LOGGER = getLogger(__name__)


# Clients whose short names are not used directly in Front Arena
EXCEPTION_MAP = {
    'ACU_BLUEINK': 'Acumen_BlueInk_FI',
    'ACU_INVEST': 'Acumen_Invest_FI',
    'MAP501': 'MAP_501',
    'NITRO_TRUST': 'Nitrogen_Trust',
    'MAP250': 'MAP_250_FI',
    'MAP290': 'XFM_MAP290'
}


# All possible values for 'Settled - Fin - InsType' grouper in reports
SETTLED_VALUES = ['Live', 'Expired or Closed Out']  # Settled
FIN_VALUES = ['Financed', 'Fully Funded']           # Fin


# Columns for financed positions:
# Inception TPL delta (end date TPL - start date TPL) against call account
FINANCED_COLUMNS = ['Inception TPL']

# Columns for fully funded positions:
# Delta value against call account
# Closing Cash Resets + Closing Cash Payments + Since Inception Execution Fee
FULLY_FUNDED_COLUMNS = [
    'Closing Cash Resets',
    'Closing Cash Payments',
    'Since Inception Execution Fee'
]
# Settlement tab deposit type columns
DEPOSIT_TYPES = (
    'Margin Deposit',
    'Manual TPL Deposit',
    'Inter Fund Cash Transfer',
    'Exposure Interest',
)
# Settlement tab start and end columns
SETTLEMENTS_COLUMNS_MAP = {
    'Closing Provision': 'Provision',
    'Since Inception Execution Fee': 'Execution Fee',
    'Since Inception Financing': 'Financing'
}
SETTLEMENTS_COLUMNS = SETTLEMENTS_COLUMNS_MAP.keys()
# Map of clinet names to their pswap names
SETTLEMENTS_CLIENT_MAP = {
    'ABAXFIT': 'ABAX'
}
SETTLEMENTS_CLIENT_MAP.update(EXCEPTION_MAP)
# Cash flows types which sum up to balance
BALANCE_CASHFLOW_TYPES = (
    'Fixed Amount',
    'Interest Reinvestment'
)


EXCLUDED_CLIENTS = []

# TO BE REMOVED 2021-01-01
BREAK_FAPE_120_CASH_RECON = {
    ("MARKSOL", "Fully Funded", "Option"): -8018.956359
}
BREAK_FAPE_120 = {
    ("AAMAQUA", "Financed", "Swap"): 5.52077071213076
    , ("ABAXFIT", "Financed", "Swap"): 17.75999354200000
    , ("COGITO", "Financed", "ETF"): -413793.38631838400000
    , ("CORO_CFS", "Financed", "Swap"): 1191.56808952765000
    , ("CORO_GRANITE", "Financed", "Swap"): 816.62689390000000
    , ("FAIRSOPP", "Financed", "Stock"): -1.16782829960000
    , ("MAP250", "Financed", "Swap"): 1702.51907275072000
    , ("MATBINK", "Financed", "FRA"): -259.18756957983900
    , ("MATBINK", "Financed", "Swap"): 29892.32509849550000
    , ("MATBINK2", "Financed", "Swap"): 1261.17535826473000
    , ("MATBINK4", "Financed", "FRA"): -121.38026445541100
    , ("MATBINK4", "Financed", "Swap"): -1877.29499466390000
    , ("MATFI", "Financed", "FRA"): -1140.42530615129000
    , ("MATFI", "Financed", "Swap"): -147.97644130745200
    , ("MATFI2", "Financed", "Swap"): 13435.48144823660000
    , ("MATMULT", "Financed", "FRA"): -207.35005566387100
    , ("MATMULT", "Financed", "Swap"): -2.23167350406670
    , ("MATMULT2", "Financed", "Swap"): 735.87749975434500
    , ("MATMULT4", "Financed", "FRA"): -2.21672398527768
    , ("MATMULT4", "Financed", "Swap"): -1744.78005386410000
    , ("NITROGEN", "Financed", "ETF"): -273.45768603480000
    , ("NOVFI2", "Financed", "FRA"): 896.85174424038000
    , ("NOVFI2", "Financed", "Swap"): -729.58097274000000
    , ("OAKHAVEN", "Financed", "FRA"): -11269.90956522140000
    , ("OAKHAVEN", "Financed", "Swap"): -41.40130927450040
    , ("OAKIDSFI", "Financed", "FRA"): 7.76068749860761
    , ("OAKMANCO", "Financed", "Swap"): -46421.41587243530000
    , ("OAKMANCO2", "Financed", "Swap"): -2480.88329087025000
    , ("OAKMANCO3", "Financed", "Swap"): 2655.56095588121000
    , ("SAKADD", "Financed", "FRA"): 9.68258556775277
    , ("SAKADD", "Financed", "Swap"): -15.20638480590270
    , ("SEFI", "Financed", "Swap"): -79492.536011
    , ("SIMGAMA", "Financed", "FRA"): 596.90238703037900
    , ("SIMHFAMS", "Financed", "FRA"): 730.09082427034000
    , ("SIMHFAMS", "Financed", "Swap"): 85.41852092916670
    , ("TEREBINK", "Financed", "Swap"): 9443.86978757114000
    , ("TEREFI", "Financed", "FRA"): 1918.38775536296000
    , ("TEREFI", "Financed", "Swap"): 2376.60643088994000
    , ("TERETR", "Financed", "FRA"): 1574.95916061725000
    , ("XCHEID", "Financed", "Swap"): 3914.30238214315000
}


# Supported sources for cash reconciliation (static reports)
FILE_PERF = "File_Performance"
PB_SETTLEMENTS = 'PB_SETTLEMENTS_ON_TREE_CFDPSWAPS'
PSWAP_SWEEPING = 'PSwapSweepingReport'


# Default report directory on Y drive
REPORT_DIR = r"Y:\Jhb\FAReports\AtlasEndOfDay"
SETTLEMENTS_REPORT_DIR = r"Y:\Jhb\FAReports\AtlasEndOfDay\TradingManager"

# File_Performance path override
PERFORMANCE_OVERRIDE_CLIENTS = ['COGITO']


def get_onboarding_date(shortname):
    """Return date of onboarding."""
    cp = get_pb_fund_counterparty(shortname)
    reporting_portfolio = get_pb_reporting_portfolio(cp)
    create_time = str(to_datetime(reporting_portfolio.CreateTime()))
    return create_time.split(" ")[0]


def get_instrument_list():
    """Return list of all instrument type available in Front Arena."""
    return sorted(acm.FEnumeration['enum(InsType)'].Enumerators())


INS_TYPE_VALUES = get_instrument_list()


def get_client_list():
    """Return list of active clients."""
    client_list = []
    for cpty in get_pb_fund_counterparties():
        short_name = get_pb_fund_shortname(cpty)
        if short_name not in EXCLUDED_CLIENTS:
            client_list.append(short_name)
    return sorted(client_list)


def str_to_float(val):
    """Convert string to float (ignore commas from within the number."""
    if type(val) == float:
        return val

    try:
        return float(val.replace(',', '')) if val != '' else 0
    except ValueError as err:
        raise MalfunctionDataException(err)


def date_range(start_date, end_date):
    """Business days date range."""
    date_list = []
    next_date = get_next_day(start_date)
    while next_date <= end_date:
        date_list.append(next_date)
        next_date = get_next_day(next_date)
    return date_list


def get_next_day(date, calendar=acm.FCalendar['ZAR Johannesburg']):
    """Return next business day."""
    return calendar.AdjustBankingDays(date, 1)


class ReportException(Exception):
    """General static report exception."""


class MalfunctionDataException(Exception):
    """Malfunction business data in static report."""


class SimpleStaticReport(object):
    """Simple class for parsing static reports.

    This class is very light-weight which means it returns only data per
    instrument type grouped by position: Financed vs. Fully funded.

    For every of these two positions there is a separate dictionary created
    that can be accessed as public members.

    The limitations mentioned above are connected to class' primary usage which
    is Cash Recon Tool. Feel free to subclass it for more specific use.

    To be added: Reports from new reporting suite (once deployed).
    """

    # Settings for basic CSV file
    csv_dialect = None
    skip_first_n_lines = 6
    inception_date = DateField.read_date('Inception')
    columns = FINANCED_COLUMNS + FULLY_FUNDED_COLUMNS + SETTLEMENTS_COLUMNS
    report_name = FILE_PERF

    def __init__(self, client, date, financed_columns,
                 fully_funded_columns, source_path=REPORT_DIR):
        """Initialise data."""
        self.client = client
        self.date = date
        self.source_path = source_path
        self.financed_columns = financed_columns
        self.fully_funded_columns = fully_funded_columns

        # Parse report content
        self.financed_dict, self.fully_funded_dict = self._parse_report()

    def _get_report_path(self):
        """Return path of File_Performance report."""
        file_name_mask = "{}_{}_{}.csv".format(
            self.client, self.report_name,
            to_datetime(self.date).strftime("%Y%m%d"))

        if self.client in PERFORMANCE_OVERRIDE_CLIENTS:
            return self._get_override_file_path(file_name_mask)

        return self._get_default_file_path(file_name_mask)

    def _get_content(self):
        """Return content from the report as list (using CSV reader)."""

        # Get full path of the report
        file_path = self._get_report_path()
        try:
            with open(file_path, 'rU') as f:
                for _ in range(self.skip_first_n_lines):
                    next(f)
                for line in csv.reader(f, dialect=self.csv_dialect):
                    yield line
        except IOError as ex:
            message = "WARNING - report not available: {0}"
            raise ReportException(message.format(ex))

    def _date_before_onboarded(self):
        onboarding_date = get_onboarding_date(self.client)
        return self.date < onboarding_date or self.date == self.inception_date

    def _get_columns_map(self, header):
        column_map = {}
        missing_columns = []
        for column in self.columns:
            try:
                column_map[column] = header.index(column)
            except ValueError:
                missing_columns.append(column)

        if missing_columns:
            message = 'Columns {0} not present in the file'
            raise ReportException(message.format(missing_columns))
        return column_map

    def _parse_report(self):
        """Parse report content and return data in a form of dictionaries."""
        # Instrument type and column value
        financed = defaultdict(lambda: defaultdict(float))
        fully_funded = defaultdict(lambda: defaultdict(float))

        if self._date_before_onboarded():
            return financed, fully_funded

        raw_data = self._get_content()
        header = next(raw_data)
        column_map = self._get_columns_map(header)

        ins_index = 0  # First column for instrument identification
        position = None
        for row in raw_data:
            if row[ins_index] in FIN_VALUES:
                position = row[ins_index]
                continue

            if row[ins_index] in INS_TYPE_VALUES:
                ins_type = row[ins_index]
                if position == "Financed":
                    for col in self.financed_columns + SETTLEMENTS_COLUMNS:
                        financed[ins_type][col] += str_to_float(
                            row[column_map[col]])
                if position == "Fully Funded":
                    for col in set(self.fully_funded_columns + SETTLEMENTS_COLUMNS):
                        fully_funded[ins_type][col] += str_to_float(
                            row[column_map[col]])

        return (financed, fully_funded)

    def _get_default_file_path(self, file_name_mask):
        return os.path.join(
                self.source_path,
                'PrimeForward',
                self.client,
                self.date,
                file_name_mask)

    def _get_override_file_path(self, file_name_mask):
        file_path = os.path.join(
            self.source_path,
            'PrimeForward',
            self.client,
            self.date,
            'PrimeReporting',
            file_name_mask)

        # YTD recon may need deault path
        if not os.path.exists(file_path):
            file_path = self._get_default_file_path(file_name_mask)

        return file_path


class SettlementsReport(SimpleStaticReport):

    """A class to parse PB_SETTLEMENTS report.

    Required to extract CFD PSwap TPL for Settlement Control tab.
    """

    skip_first_n_lines = 5
    columns = ('TPL',)
    report_name = PB_SETTLEMENTS

    def __init__(self, date, source_path=SETTLEMENTS_REPORT_DIR):
        """Initialise data."""
        self.date = date
        self.source_path = source_path

    def _get_report_path(self):
        """Return path of PB_SETTLEMENTS report."""
        file_name_mask = "{}_{}.csv".format(
            self.report_name, to_datetime(self.date).strftime("%y%m%d"))
        return os.path.join(
            self.source_path,
            self.date,
            file_name_mask)

    def _date_before_onboarded(self):
        return self.date == self.inception_date

    def parse(self):
        data = defaultdict(dict)
        if self._date_before_onboarded():
            return data

        raw_data = self._get_content()
        header = next(raw_data)
        column_map = self._get_columns_map(header)

        ins_index = 0  # First column for instrument identification
        for row in raw_data:
            ins_name = row[ins_index]
            for col in self.columns:
                value = str_to_float(row[column_map[col]])
                if value:
                    data[ins_name]['PSwap ' + col] = value
        return data


class PSwapSweepingReport(SimpleStaticReport):

    """A class to parse PSwapSweeping report.

    Required to extract non-CFD PSwap TPL for Settlement Control tab.
    """

    columns = ('TPL',)
    report_name = PSWAP_SWEEPING

    def __init__(self, client, date, source_path=REPORT_DIR):
        self.client = client
        self.date = date
        self.source_path = source_path

    def _get_content(self):
        file_path = self._get_report_path()
        try:
            with open(file_path, 'rU') as file_:
                for line in csv.DictReader(file_):
                    yield line
        except IOError as err:
            raise ReportException(
                "WARNING - report not available: {}".format(err))

    def parse(self):
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        if self._date_before_onboarded():
            return data

        for row in self._get_content():
            # Ignore sweeping from previous days.
            if acm.Time.AsDate(row['Date']) != self.date:
                continue
            # Ignore per instrument breakdown.
            if row['Instrument Name'] != '-':
                continue

            position = row['Position']
            ins_type = row['Instrument Type']

            for col in self.columns:
                value = str_to_float(row[col])
                if position == 'Financed':
                    value += str_to_float(row['Provision']) - str_to_float(row['Funding'])
                if value:
                    data[position][ins_type]['PSwap ' + col] += value
        return data


class CallaccountException(Exception):
    """Exception to be raised when call account extraction fails."""


class SimpleCallaccountExtractor(object):
    """Simple class for extracting data from the call account."""

    def __init__(self, client, start_date, end_date):
        """Initialise the extractor.

        Note: Some clients' call account names are not compliant with our
        naming convention. That's why the exception map is used for direct
        translation from client's short name to the name that is actually used
        in the call account's portfolio name.

        Example: Client's short name is NITRO_TRUST but the portfolio name is
        PB_CALL_MARGIN_Nitrogen_Trust instead of PB_CALL_MARGIN_NITRO_TRUST,
        hence the exception map.

        """
        self.client = EXCEPTION_MAP.get(client, client)

        self.start_date = start_date
        self.end_date = end_date

        # Extract data from the call account
        self.date_list = self._get_callaccnt_date_list()
        self.callaccount = self._get_callaccount()

        self.financed_dict, self.fully_funded_dict, self.settlements = self._extract_data()

    def _get_callaccnt_date_list(self):
        """Return list of dates based on the start date and end date.

        Note: Cash is swept to the call account the day after the transaction,
        hence the date list starts with T+1.

        """
        date_list = []
        next_date = acm.Time().DateAddDelta(self.start_date, 0, 0, 1)
        while next_date <= self.end_date:
            date_list.append(next_date)
            next_date = acm.Time().DateAddDelta(next_date, 0, 0, 1)

        return date_list

    def _get_callaccnt_name(self):
        """Return call account name for the client."""
        trades = (
            acm.FPhysicalPortfolio['PB_CALLACCNT_%s' % self.client] or
            acm.FPhysicalPortfolio['PB_CALL_MARGIN_%s' % self.client]).Trades()

        for t in trades:
            if t.Instrument().InsType() == 'Deposit' and t.Status() not in (
                    'Simulated', 'Void'):
                return t.Instrument().Name()

    def _get_callaccount(self):
        """Return the call account (FInstrument) for a client."""
        return acm.FInstrument[self._get_callaccnt_name()]

    def _extract_data(self):
        """Extract data from call account in a form of dictionaries.

        Significant data from call accounts is a sum of all cash flows per
        instrument type for a given date range (date list). The cash flows
        that we are interested in here are those of Fixed Amount that are not
        the of type Margin Deposit and have Cash Type filled in so that we can
        access their fund portfolio for distinguishing the between Financed
        and Fully funded positions.

        Dictionaries per position and instrument type are then filled with data
        based on the fact if the cash flows are supposed to tie up with
        'Static' reporting or could be subject to 'Back-dated' trading.
        """

        # Dictionaries per instrument type (and per static and back-dated)
        financed_dict = defaultdict(lambda: defaultdict(float))
        fully_funded_dict = defaultdict(lambda: defaultdict(float))
        # Data for settlement control tab
        settlements = defaultdict(lambda: defaultdict(float))

        # Composite key for dictionaries to reflect strategies
        CompositeKey = namedtuple(
            'CompositeKey',
            'cash_type, fund_portfolio, ins_type')

        first_financed_cf = {date: {} for date in self.date_list}
        first_fully_funded_cf = {date: {} for date in self.date_list}

        backdated_first_financed_cf = {}
        backdated_first_fully_funded_cf = {}

        leg = self.callaccount.Legs()[0]
        cash_flows = set()
        for query in (
                "leg={} and payDate >= '{}' and payDate <= '{}'",  # or
                "leg={} and startDate >= '{}' and startDate <= '{}'"):
            cfs_from_query = acm.FCashFlow.Select(
                query.format(leg.Oid(), self.date_list[0], self.date_list[-1]))
            cash_flows.update(list(cfs_from_query))

        day_after = get_next_day(self.date_list[-1])
        cash_flows.update(list(acm.FCashFlow.Select(
                "leg={} and createTime >= '{}' and createTime < '{}'".format(
                leg.Oid(), self.date_list[0], day_after))))

        for cf in cash_flows:
            within_range = self._within_date_range(cf)
            backdated = self._backdated_before_start(cf)
            backdated_before_create = self._backdated_before_create(cf)

            cashflow_type = cf.CashFlowType()
            if cashflow_type in BALANCE_CASHFLOW_TYPES:
                key = 'backdated' if backdated_before_create else 'value'
                settlements['Balance'][key] += cf.FixedAmount()

            if cashflow_type == 'Fixed Amount':
                cf_add_info = cf.AdditionalInfo()
                deposit_type = cf_add_info.PS_DepositType()

                if deposit_type in DEPOSIT_TYPES:
                    key = 'backdated' if backdated_before_create else 'value'
                    settlements[deposit_type][key] += cf.FixedAmount()

                if (deposit_type != 'Margin Deposit' and
                        cf_add_info.PSCashType()):
                    cash_type = cf_add_info.PSCashType()
                    pswap = acm.FPortfolioSwap[cash_type]
                    fund_port = pswap.FundPortfolio()
                    port_type = fund_port.AdditionalInfo().PS_PortfolioType()
                    ins_type = cf_add_info.PS_InstrumentType()
                    pay_date = cf.StartDate() if cf.StartDate() else cf.PayDate()

                    # Check for CFD as instrument type
                    if not ins_type and port_type == 'CFD':
                        ins_type = 'CFD'

                    # Composite key to distinguish between strategies
                    key = CompositeKey(cash_type, fund_port.Name(), ins_type)

                    # First cash flows per position and per instrument type
                    if within_range:
                        # Update proper dictionary based on the position
                        if pswap.AdditionalInfo().PB_PS_Fully_Funded():
                            self._update_dictionary(cf, fully_funded_dict,
                                                    first_fully_funded_cf[pay_date], key)
                        else:
                            self._update_dictionary(cf, financed_dict,
                                                    first_financed_cf[pay_date], key)

                    # Cash-flows from reconciliation period back-dated before start date.
                    if backdated:
                        if pswap.AdditionalInfo().PB_PS_Fully_Funded():
                            self._update_dict_back_dated_only(
                                cf, fully_funded_dict, backdated_first_fully_funded_cf, key)
                        else:
                            self._update_dict_back_dated_only(
                                cf, financed_dict, backdated_first_financed_cf, key)

        return (self._sanitize(financed_dict),
                self._sanitize(fully_funded_dict),
                settlements)

    @staticmethod
    def _sanitize(dictionary):
        # Sanitise - reconciliation is performed per instrument type.
        # That's why we need to sum up all values per instrument type
        # from various strategies.
        sanitized_dict = defaultdict(lambda: defaultdict(float))
        for key, value in dictionary.items():
            sanitized_dict[key.ins_type]['Backdated'] += value['Backdated']
            sanitized_dict[key.ins_type]['Static'] += value['Static']
        return sanitized_dict

    @staticmethod
    def _update_dictionary(cf, d, first_cf, key):
        """Update given dictionary based on the current cash flow.

        Arguments:
            cf - Currently processed cash flow.
            d - Dictionary containing sum per composite key for all the dates
                in the date list (divided into 'Static' and 'Back-dated'.
                It can be either the one for 'Financed' or 'Fully funded'
                position.
            first_cf - Dictionary containing cash flow with the lowest oid
                       (Object ID) per composite key per one day.
            key - Composite key containing cash type, fund portfolio name
                  and instrument type - unique identification of cash flow
                  per strategy (should the client use any).

        In normal situations there is only one cash flow per instrument
        type (meaning per composite key - taking strategies into account)
        per one date. If more than one of such cash flows appear it's
        an indication of back-dated cash flows (trades).

        This method distinguishes back-dated cash flows based on the order
        of their insertion into DB (oid).

        The first cash flow per strategy and instrument type is automatically
        considered being the one that should tie up with the static reporting.

        When the the first cash flow per strategy and instrument type appears,
        it is stored for future reference. The second and every other cash flow
        per the same strategy and instrument type is compared against the first
        one (understand the first one is with the lowest oid per day). When the
        cash flow with lower oid than the one already stored in the 'first_cf'
        variable is processed then the current one becomes the first one and
        its fixed amount is cumulatively added per strategy and instrument type
        as 'static' (where static being the sum that should tie up with data
        from static reporting). The old first cash flow is now handled as
        back-dated and therefore is subtracted from the 'static' portion and
        added to the 'back-dated' one.

        Note: Keep in mind that this method is called for every date in the
        date list hence the cumulative way of calculations.

        Reconciliation is performed per instrument type, therefore values from
        various strategies and summed up per instrument type.

        """

        if key in first_cf:
            # There already was a cash flow per this instrument type
            if first_cf[key].Oid() > cf.Oid():
                # Current cash flow occurred sooner than the one already stored
                d[key]['Backdated'] += first_cf[key].FixedAmount()
                d[key]['Static'] -= first_cf[key].FixedAmount()
                d[key]['Static'] += cf.FixedAmount()
                first_cf[key] = cf
            else:
                # Current cash flow occurred later than the one already stored
                d[key]['Backdated'] += cf.FixedAmount()
        else:
            # First occurrence of cash flow per instrument_type
            d[key]['Static'] += cf.FixedAmount()
            first_cf[key] = cf

    @staticmethod
    def _update_dict_back_dated_only(cf, d, first_cf, key):
        """Special case for back-dated cash flows. Ignore static cash-flows."""
        if key in first_cf:
            # There already was a cash flow for this instrument type
            if first_cf[key].Oid() > cf.Oid():
                # Current cash flow occurred sooner than the one already stored
                d[key]['Backdated'] += first_cf[key].FixedAmount()
                first_cf[key] = cf
            else:
                # Current cash flow occurred later than the one already stored
                d[key]['Backdated'] += cf.FixedAmount()
        else:
            # First occurrence of cash flow for instrument_type
            first_cf[key] = cf

    def _within_date_range(self, cf):
        """Return True if the cash flow fits withing the requested dates."""
        # Use StartDate (used for back-dated cash flows - mostly)
        pay_date = cf.StartDate() if cf.StartDate() else cf.PayDate()
        return pay_date in self.date_list

    def _backdated_before_start(self, cf):
        """Return True if cash flow is back-dated before start date.

        Cash flows created during the recon period back-dated before
        the start date will be reflected in the end date's PnL but won't
        be in the start date's PnL (static report generated before cash flow
        was even created). Therefore this cash flow can be potential cause of
        break - should be captured as back-dated.
        """
        if (cf.PayDate() in self.date_list and
                cf.StartDate() and
                cf.StartDate() < self.date_list[0]):
            return True
        return False

    def _backdated_before_create(self, cf):
        # The Cashflow with PayDate in the past.
        pay_date = cf.StartDate() if cf.StartDate() else cf.PayDate()
        return cf.CreateDay() > pay_date and pay_date not in self.date_list


class CashReconException(Exception):
    """General Cash Recon Exception."""


class CashReconReportCreator(DataToXMLReportCreator):
    """Class responsible for generating cash reconciliation report."""

    # Error in accessing file or data within
    _REPORT_FILES_PROBLEM_MSG = 'Missing report(s)'
    # Malfunction data in the file (e.g. NaN after connection reset)
    _MALFUNCTION_DATA_MSG = 'Malfunction data'
    # Break occurred when analysing data
    _BREAK_MSG = 'Break'
    # No break occurred when analysing data or overall OK status
    _OK_MSG = 'OK'
    # Error occurred when accessing data from client's call account
    _CALLACCNT_ERR_MSG = 'Call account error'
    # Other error while processing data
    _UNKNOWN_ERR_MSG = 'Unknown error'

    def __init__(self, start_date, end_date, client_list, epsilon,
                 output_path, input_path, sc_input_path,
                 file_name, xsl_template):
        self.start_date = start_date
        self.end_date = end_date
        self.epsilon = float(epsilon)
        self.input_path = input_path
        self.sc_input_path = sc_input_path
        self.client_list = client_list

        # Nested dictionary for report data: per client, position, source
        self.data = NestedDict()

        # (Error) messages for clients
        self.messages = {}
        self.sc_messages = {}

        self.file_name = file_name
        super(CashReconReportCreator, self).__init__(self.file_name, 'xls',
                                                     output_path, xsl_template)

    def _collect_data(self):
        """Collect data from specified sources."""
        LOGGER.info("Recon from {}".format(FILE_PERF))
        for client in self.client_list:
            LOGGER.info(client)
            self.messages[client] = self._OK_MSG
            try:
                self._collect_source_data(client)
            except ReportException as ex:
                self.messages[client] = self._REPORT_FILES_PROBLEM_MSG
                LOGGER.error(ex)

            except MalfunctionDataException:
                self.messages[client] = self._MALFUNCTION_DATA_MSG

            except CallaccountException:
                self.messages[client] = self._CALLACCNT_ERR_MSG

            self.sc_messages[client] = self.messages[client]
            try:
                self._collect_pswap_non_cfd(client)
            except ReportException as ex:
                self.sc_messages[client] = self._REPORT_FILES_PROBLEM_MSG
                LOGGER.error(ex)

        try:
            self._collect_pswap_cfd_data()
        except ReportException as ex:
            for client in self.client_list:
                self.sc_messages[client] = self._REPORT_FILES_PROBLEM_MSG
            LOGGER.error(ex)

    def _collect_pswap_cfd_data(self):
        """Collect CFD pswap TPL from PB_SETTLEMENT report."""
        cfd_start = SettlementsReport(self.start_date, self.sc_input_path).parse()
        cfd_end = SettlementsReport(self.end_date, self.sc_input_path).parse()
        for client in self.client_list:
            start_dict = self.data[client]['Financed']['Start']
            end_dict = self.data[client]['Financed']['End']
            pswap_name = 'PB_{}_CFD'.format(SETTLEMENTS_CLIENT_MAP.get(client, client))
            if cfd_start[pswap_name] or cfd_end[pswap_name]:
                start_dict['CFD'].update(cfd_start[pswap_name])
                end_dict['CFD'].update(cfd_end[pswap_name])

    def _collect_pswap_non_cfd(self, client):
        """Collect non-CFD pswap TPL from PSwapSweeping report."""
        non_cdf_start = PSwapSweepingReport(
            client, self.start_date, self.input_path
        ).parse()
        for position in non_cdf_start:
            start_dict = self.data[client][position]['Start']
            for ins_type, data in non_cdf_start[position].items():
                start_dict[ins_type].update(data)
        non_cdf_end = PSwapSweepingReport(
            client, self.end_date, self.input_path
        ).parse()
        for position in non_cdf_end:
            end_dict = self.data[client][position]['End']
            for ins_type, data in non_cdf_end[position].items():
                end_dict[ins_type].update(data)

    def _collect_source_data(self, client):
        """Collect data for all sources to be compared against each other."""
        # Get data from client's call account
        call_account = SimpleCallaccountExtractor(
            client, self.start_date, self.end_date)

        # Financed and Fully Funded positions from call account
        self.data[client]['Financed']['Call'] = \
            call_account.financed_dict
        self.data[client]['Fully Funded']['Call'] = \
            call_account.fully_funded_dict
        self.data[client]['Settlements'] = call_account.settlements

        # Get data from static reporting suite
        report_start = SimpleStaticReport(
            client=client,
            date=self.start_date,
            financed_columns=FINANCED_COLUMNS,
            fully_funded_columns=FULLY_FUNDED_COLUMNS,
            source_path=self.input_path)

        # Financed and Fully Funded from start date report
        self.data[client]['Financed']['Start'] = \
            report_start.financed_dict

        self.data[client]['Fully Funded']['Start'] = \
            report_start.fully_funded_dict

        report_end = SimpleStaticReport(
            client=client,
            date=self.end_date,
            financed_columns=FINANCED_COLUMNS,
            fully_funded_columns=FULLY_FUNDED_COLUMNS,
            source_path=self.input_path)

        # Financed and Fully Funded from end date report
        self.data[client]['Financed']['End'] = \
            report_end.financed_dict

        self.data[client]['Fully Funded']['End'] = \
            report_end.fully_funded_dict

    def _generate_xml(self):
        """Generate XML from collected data."""

        # Create report element
        report_xml = ElementTree.Element('report')
        report_xml.set('type', FILE_PERF)
        report_xml.set('start_date', self.start_date)
        report_xml.set('end_date', self.end_date)

        for client in self.client_list:
            # Create client element
            client_xml = ElementTree.SubElement(report_xml, 'client')
            client_xml.set('name', client)
            client_xml.set('status', self.messages[client])
            client_xml.set('start_date', self.start_date)
            client_xml.set('end_date', self.end_date)
            self._add_settlement_control_deposits(client_xml)

            for position in ('Financed', 'Fully Funded'):
                # Create position element.
                position_xml = ElementTree.SubElement(client_xml, 'position')
                position_xml.set('type', position)

                # Check for error message
                if self.messages[client] != self._OK_MSG:
                    position_xml.set('status', self.messages[client])
                    continue

                self._add_detailed_recon_instruments(position_xml, client_xml)
                self._add_settlement_control_instruments(position_xml, client_xml)

        report_xml_str = ('<?xml version="1.0" encoding="utf-8"?>' +
                          ElementTree.tostring(report_xml))

        LOGGER.info("XML generated")
        return report_xml_str

    @staticmethod
    def _add_xml_element(parent, name, text=None, **kwargs):
        element = ElementTree.SubElement(parent, name)
        element.text = str(text)
        element.attrib.update(kwargs)
        return element

    def _add_detailed_recon_instruments(self, position_xml, client_xml):
        position = position_xml.attrib['type']
        client = client_xml.attrib['name']

        start_dict = self.data[client][position]['Start']
        end_dict = self.data[client][position]['End']
        call_dict = self.data[client][position]['Call']

        for ins_type in self._merge_instrument_keys(start_dict, end_dict, call_dict):
            static_val = call_dict[ins_type]['Static']
            back_dated_val = call_dict[ins_type]['Backdated']
            cash_val = static_val + back_dated_val

            if position == 'Financed':
                start_val = start_dict[ins_type]['Inception TPL']
                end_val = end_dict[ins_type]['Inception TPL']
            else:
                start_val = 0.0
                end_val = 0.0
                for col in FULLY_FUNDED_COLUMNS:
                    start_val += start_dict[ins_type][col]
                    end_val += end_dict[ins_type][col]
                start_dict[ins_type]['Inception TPL'] = start_val
                end_dict[ins_type]['Inception TPL'] = end_val

            change_val = end_val - start_val
            diff_val = change_val - cash_val
            if self.start_date == "2019-12-31":
                if (client, position, ins_type) in BREAK_FAPE_120_CASH_RECON:
                    diff_val += BREAK_FAPE_120_CASH_RECON[(client, position, ins_type)]

            # Identify break
            if abs(diff_val) > self.epsilon:
                status_msg = self._BREAK_MSG
                client_xml.set('status', status_msg)
            else:
                status_msg = self._OK_MSG

            if math.isnan(start_val) or math.isnan(end_val):
                position_xml.set('status', self._MALFUNCTION_DATA_MSG)
                client_xml.set('status', self._MALFUNCTION_DATA_MSG)

            # Create instrument element
            instrument_xml = ElementTree.SubElement(
                position_xml, 'instrument')
            instrument_xml.set('type', ins_type)
            instrument_xml.set('start_val', str(start_val))
            instrument_xml.set('end_val', str(end_val))
            instrument_xml.set('change', str(change_val))
            instrument_xml.set('cash', str(cash_val))
            instrument_xml.set('backdated', str(back_dated_val))
            instrument_xml.set('diff', str(diff_val))
            instrument_xml.set('status', status_msg)

    def _add_settlement_control_instruments(self, position_xml, client_xml):
        position = position_xml.attrib['type']
        client = client_xml.attrib['name']
        # Check for error message
        if self.sc_messages[client] != self._OK_MSG:
            client_xml.set('sc_status', self.sc_messages[client])
            return

        start_dict = self.data[client][position]['Start']
        end_dict = self.data[client][position]['End']
        call_dict = self.data[client][position]['Call']

        for ins_type in self._merge_instrument_keys(start_dict, end_dict, call_dict):
            # Instrument type column
            sinstrument_xml = self._add_xml_element(position_xml, 'sinstrument')
            self._add_xml_element(
                sinstrument_xml, 'value', ins_type,
                style='value_general',
                type='String')

            # Start-End-Change columns
            for column in SETTLEMENTS_COLUMNS + ['Inception TPL', 'PSwap TPL']:
                start = start_dict[ins_type][column]
                end = end_dict[ins_type][column]

                for val, header2 in ((start, self.start_date),
                                     (end, self.end_date)):
                    self._add_xml_element(
                        sinstrument_xml, 'value', val,
                        header=SETTLEMENTS_COLUMNS_MAP.get(column, column),
                        header2=header2,
                        style='numeric_value_gray',
                        type='Number')
                self._add_xml_element(
                    sinstrument_xml, 'value', end - start,
                    header=SETTLEMENTS_COLUMNS_MAP.get(column, column),
                    header2='Change',
                    style='numeric_value_general',
                    type='Number')

            # Break column
            xpath = "value[@header='{}'][@header2='Change']"
            inception_tpl_change = sinstrument_xml.findtext(xpath.format('Inception TPL'))
            pswap_tpl_change = sinstrument_xml.findtext(xpath.format('PSwap TPL'))
            if ins_type == 'CFD':
                pswap_tpl_change = -1.0 * float(pswap_tpl_change)
            val = float(inception_tpl_change) - float(pswap_tpl_change)
            if self.start_date == "2019-12-31":
                if (client, position, ins_type) in BREAK_FAPE_120:
                    val += BREAK_FAPE_120[(client, position, ins_type)]
            self._add_xml_element(
                sinstrument_xml, 'value', val,
                header='TPL Break',
                style='status_ok' if not round(val) else 'status_break',
                type='Number')

    def _add_settlement_control_deposits(self, client_xml):
        client = client_xml.attrib['name']
        settlements = self.data[client]['Settlements']
        for key in ('Balance',) + DEPOSIT_TYPES:
            settlement_xml = self._add_xml_element(client_xml, 'settlement', header=key)
            value = settlements[key]
            self._add_xml_element(settlement_xml, 'value', value['value'])
            self._add_xml_element(settlement_xml, 'backdated', value['backdated'])

    @staticmethod
    def _merge_instrument_keys(start_dict, end_dict, call_dict):
        """Return merged keys from all client's data sources."""
        return sorted(set(start_dict.keys() + end_dict.keys() + call_dict.keys()))

    def get_filename(self):
        """Get file name of the report."""
        return '.'.join([self.file_name, 'xls'])


class CashReconLookupReportCreator(DataToXMLReportCreator):
    """Class responsible for generating detailed lookup report."""

    # Error in accessing file or data within
    _REPORT_FILES_PROBLEM_MSG = 'Missing report(s)'
    # Malfunction data in the file (e.g. NaN after connection reset)
    _MALFUNCTION_DATA_MSG = 'Malfunction data'
    # Break occurred when analysing data
    _BREAK_MSG = 'Break'
    # No break occurred when analysing data or overall OK status
    _OK_MSG = 'OK'
    # Error occurred when accessing data from client's call account
    _CALLACCNT_ERR_MSG = 'Call account error'
    # Other error while processing data
    _UNKNOWN_ERR_MSG = 'Unknown error'

    def __init__(self, start_date, end_date, client, epsilon,
                 output_path, input_path, position, ins_type, xsl_template):

        self.start_date = start_date
        self.end_date = end_date
        self.client = client
        self.epsilon = float(epsilon)
        self.input_path = input_path
        self.position = position
        self.ins_type = ins_type

        self.file_name = 'CashReconLookup_%s_%s_%s_%s_%s' % (
            self.client, self.position, self.ins_type.replace('/', ''),
            self.start_date, self.end_date)

        super(CashReconLookupReportCreator, self).__init__(
            self.file_name, 'xls', output_path, xsl_template)

    def _collect_data(self):
        """Needed for the class to be defined but not used."""
        pass

    def _generate_xml(self):
        """Collect data and create xml from specified sources."""
        LOGGER.info("Lookup from {}".format(FILE_PERF))

        calendar = acm.FCalendar['ZAR Johannesburg']
        start_date = calendar.AdjustBankingDays(self.end_date, -1)
        end_date = self.end_date

        report_xml = ElementTree.Element('report')
        report_xml.set('type', FILE_PERF)
        report_xml.set('start_date', start_date)
        report_xml.set('end_date', end_date)
        report_xml.set('lookup', '1')

        # Run through the date interval
        while start_date > self.start_date:
            LOGGER.info("Break lookup: {0} - {1}".format(start_date, end_date))

            client_xml = ElementTree.SubElement(report_xml, 'client')
            client_xml.set('name', self.client)
            client_xml.set('status', self._OK_MSG)
            client_xml.set('start_date', start_date)
            client_xml.set('end_date', end_date)

            position_xml = ElementTree.SubElement(client_xml, 'position')
            position_xml.set('type', self.position)

            try:
                if self.position == 'Financed':
                    start_date_columns = FINANCED_COLUMNS
                    end_date_columns = FINANCED_COLUMNS

                    # Get data from static reporting suite
                    report_start = SimpleStaticReport(
                        client=self.client,
                        date=start_date,
                        financed_columns=start_date_columns,
                        fully_funded_columns=[],
                        source_path=self.input_path)

                    report_end = SimpleStaticReport(
                        client=self.client,
                        date=end_date,
                        financed_columns=end_date_columns,
                        fully_funded_columns=[],
                        source_path=self.input_path)
                else:
                    start_date_columns = FULLY_FUNDED_COLUMNS
                    end_date_columns = FULLY_FUNDED_COLUMNS

                    # Get data from static reporting suite
                    report_start = SimpleStaticReport(
                        client=self.client,
                        date=start_date,
                        financed_columns=[],
                        fully_funded_columns=start_date_columns,
                        source_path=self.input_path)

                    report_end = SimpleStaticReport(
                        client=self.client,
                        date=end_date,
                        financed_columns=[],
                        fully_funded_columns=end_date_columns,
                        source_path=self.input_path)
            except ReportException:
                status_msg = self._REPORT_FILES_PROBLEM_MSG
                position_xml.set('status', status_msg)
                client_xml.set('status', status_msg)

                # Move to the next set of dates
                start_date = calendar.AdjustBankingDays(start_date, -1)
                end_date = calendar.AdjustBankingDays(end_date, -1)
                continue

            try:
                # Get data from client's call account
                call_account = SimpleCallaccountExtractor(
                    self.client, start_date, end_date)
            except CallaccountException:
                status_msg = self._CALLACCNT_ERR_MSG
                position_xml.set('status', status_msg)
                client_xml.set('status', status_msg)

                # Move to the next set of dates
                start_date = calendar.AdjustBankingDays(start_date, -1)
                end_date = calendar.AdjustBankingDays(end_date, -1)
                continue

            # Financed and Fully Funded from start date report
            if self.position == 'Financed':
                start_dict = report_start.financed_dict
                end_dict = report_end.financed_dict
                call_dict = call_account.financed_dict
            else:
                start_dict = report_start.fully_funded_dict
                end_dict = report_end.fully_funded_dict
                call_dict = call_account.fully_funded_dict

            static_val = call_dict[self.ins_type]['Static']
            back_dated_val = call_dict[self.ins_type]['Backdated']
            cash_val = static_val + back_dated_val

            # Get values
            if self.position == 'Financed':
                start_val = start_dict[self.ins_type]['Inception TPL']
                end_val = end_dict[self.ins_type]['Inception TPL']
            else:
                start_val = 0.0
                end_val = 0.0
                for col in FULLY_FUNDED_COLUMNS:
                    start_val += start_dict[self.ins_type][col]
                    end_val += end_dict[self.ins_type][col]

            change_val = end_val - start_val
            diff_val = change_val - cash_val

            # Identify break
            if abs(diff_val) > self.epsilon:
                status_msg = self._BREAK_MSG
                client_xml.set('status', status_msg)
            else:
                status_msg = self._OK_MSG

            # Create instrument element
            instrument_xml = ElementTree.SubElement(
                position_xml, 'instrument')
            instrument_xml.set('type', self.ins_type)
            instrument_xml.set('start_val', str(start_val))
            instrument_xml.set('end_val', str(end_val))
            instrument_xml.set('change', str(change_val))
            instrument_xml.set('cash', str(cash_val))
            instrument_xml.set('backdated', str(back_dated_val))
            instrument_xml.set('diff', str(diff_val))
            instrument_xml.set('status', status_msg)

            # Move to the next set of dates
            start_date = calendar.AdjustBankingDays(start_date, -1)
            end_date = calendar.AdjustBankingDays(end_date, -1)

        report_xml_str = ('<?xml version="1.0" encoding="utf-8"?>' +
                          ElementTree.tostring(report_xml))

        LOGGER.info("XML generated")
        return report_xml_str

    def get_filename(self):
        """Get file name of the report."""
        return '.'.join([self.file_name, 'xls'])
