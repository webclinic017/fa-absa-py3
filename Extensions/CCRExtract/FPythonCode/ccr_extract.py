"""-----------------------------------------------------------------------------
MODULE
    CCRExtract
DESCRIPTION
    Developer           : Matthew French (matthew.french@sungard.com)
                        : Frantisek Jahoda (frantisek.jahoda@barclays.com)
    Date                : 2014-11-14
    Purpose             : Counterparty Credit Risk (CCR) Extract
    Requestor           : Cindy Lottering
    CR Number           :
ENDDESCRIPTION

HISTORY
    Date:       CR Number:      Developer:              Description:
--------------------------------------------------------------------------------

The CCR Extract provides a feed from Front to the credit risk system.

Notes:
------
After testing it was determined that asql and query folders took a long time to
load and filter the large amounts of data needed for this extract. For this
reason it became necessary to select eligible trades directly from the database
first using dbsql and then to load the trades that were required.

The output is written as the process runs so if the process crashes it is
possible to have an incomplete output file. However no control file will be
written so this should not be an issue.
"""

from math import fabs, isnan
import time
import csv
import traceback
import hashlib
import ael
import acm

# Nobody ever reads the documentation...
# pylint: disable=missing-docstring

################################################################################
#                                   Constants
################################################################################

EXTENSION_CONTEXT = 'CCR'

BLANK = ""

# Default parameter values
# For ATS use PREFIX "/services/frontnt/Task/Front_TradeAndSensitivity_CCR"
DEF_FILENAME_PREFIX = "C:\\TEMP\\CCR\\Front_TradeAndSensitivity_CCR"
DEF_COMMODITY_CURRENCIES = "XAG,XAU,XPD,XPT,XRH,XZN"
DEF_EXCLUDE_STATUS = ('Void', 'Terminated', 'Simulated')
DEF_INSTRUMENTS = "Bill,Bond,BuySellback,CD,CFD,Deposit,FRN," + \
                  "IndexLinkedBond,Repo/Reverse,Stock,ETF"
DEF_INT_PARTIES = "MIDAS DUAL KEY"
DEF_PORTFOLIOS = "SECONDARY MARKETS TRADING"
DEF_COLLATERAL = "Call_3014,CSA Non ZAR Collateral"

# Parameter names
PARM_REPORT_DATE = "report_date"
PARM_SPLIT_TOTAL = "split_total"
PARM_SPLIT_INSTANCE = "split_instance"
PARM_PORTFOLIOS = "portfolios"
PARM_INSTRUMENTS = "exclude_ins"
PARM_INT_PARTIES = "include_parties"
PARM_COLLATERAL = "col_filter"
PARM_COMMODITY_CCYS = "commodity_currencies"
PARM_TRADE_IDS = "trade_ids"
PARM_FILE_PREFIX = "file_prefix"
PARM_SAMPLE_DATA_B = "sample_data"
PARM_CP_LIKE = "counterparty_like"

# Columns
COL_TRADE_NO = "TradeNo"
COL_INSTRUMENT = "Instrument"
COL_INSTRUMENT_TYPE = "InstrumentType"
COL_TRADE_TIME = "TradeTime"
COL_EXPIRY_DATE = "ExpiryDate"
COL_TRADE_CURRENCY = "TradeCurrency"
COL_STATUS = "Status"
COL_TRADER = "Trader"
COL_COUNTERPARTY_ID = "CounterpartyId"
COL_COUNTERPARTY_NAME = "CounterpartyName"
COL_ACQUIRER_NAME = "AcquirerName"
COL_ROOT_PORTFOLIO = "RootPortfolio"
COL_PORTFOLIO_CODE = "PortfolioCode"
COL_PORTFOLIO_NAME = "PortfolioName"
COL_BUY_OR_SELL = "BuyOrSell"
COL_ZAR_NOMINAL = "ZARNominal"
COL_ZAR_MTM = "ZARMTM"
COL_UNDERLYING_TYPE = "UnderlyingType"
COL_UNDERLYING_NAME = "UnderlyingName"
COL_UNDERLYING_EXPIRY = "UnderlyingExpiryDate"
COL_ISSUER = "Issuer"
COL_UNDERLYING_ISSUER = "UnderlyingIssuer"
COL_SENSITIVITY_CCY = "SensitivityCurrency"
COL_SENSITIVITY_TYPE = "SensitivityType"
COL_SENSITIVITY_CURVE = "Sensitivity Curve"
COL_SENSITIVITY_BUCKET = "Sensitivity Bucket"
COL_SENSITIVITY_PCD = "Sensitivity - PriceCurveDeltaCash"
COL_SENSITIVITY = "Sensitivity"
COL_MIDAS_ID = "Source Trade ID - Midas"
COL_SOVEREIGN_ISSUER = "Sovereignty - Issuer"
COL_SENSITIVITY_SOV = "Sovereignty - Curves"
COL_MTM_FROM_FEED = "MTMFromFeed"
COL_MTM_SOURCE = "MTMFromFeedSource"
COL_ROW_ERROR = "Error"
COL_COLLATERAL = "Collateral"
COL_SENSITIVITY_BSOU = "BenchmarkSensitivityOfUnderlying"
COL_OTC = "OTC"
COL_PAY_TYPE = "Pay Type"
COL_INTEREST_RATE_TYPE = "InterestRateType"

HEADINGS = (
    COL_TRADE_NO,
    COL_INSTRUMENT,
    COL_INSTRUMENT_TYPE,
    COL_TRADE_TIME,
    COL_EXPIRY_DATE,
    COL_TRADE_CURRENCY,
    COL_STATUS,
    COL_TRADER,
    COL_COUNTERPARTY_ID,
    COL_COUNTERPARTY_NAME,
    COL_ACQUIRER_NAME,
    COL_ROOT_PORTFOLIO,
    COL_PORTFOLIO_CODE,
    COL_PORTFOLIO_NAME,
    COL_BUY_OR_SELL,
    COL_ZAR_NOMINAL,
    COL_ZAR_MTM,
    COL_UNDERLYING_TYPE,
    COL_UNDERLYING_NAME,
    COL_UNDERLYING_EXPIRY,
    COL_ISSUER,
    COL_UNDERLYING_ISSUER,
    COL_SENSITIVITY_CCY,
    COL_SENSITIVITY_TYPE,
    COL_SENSITIVITY_CURVE,
    COL_SENSITIVITY_BUCKET,
    COL_SENSITIVITY,
    COL_SENSITIVITY_PCD,
    COL_MIDAS_ID,
    COL_SOVEREIGN_ISSUER,
    COL_SENSITIVITY_SOV,
    COL_MTM_FROM_FEED,
    COL_MTM_SOURCE,
    COL_ROW_ERROR,
    COL_COLLATERAL,
    COL_OTC,
    COL_PAY_TYPE,
    COL_SENSITIVITY_BSOU
)

AQUA_VAL_GROUPS = (
    "AQUA_MEPDN_ED_OPTIONS",
    "AQUA_MEUAT_ED_OPTIONS"
)

VALUE_DAY_INSTRUMENTS = (
    "Bill",
    "Bond",
    "Commodity",
    "Curr",
    "EquityIndex",
    "ETF",
    "IndexLinkedBond",
    "Stock"
)

# Sensitivities and Calculation Groups
CALC_GROUP_SENSITIVITY = "Sensitivity"

SENS_FX_DELTA = "FXDelta"
SENS_IR_YIELD_DELTA = "IRDeltaYield"
SENS_IR_BENCHMARK_DELTA = "IRDeltaBenchmark"
SENS_PRICE_DELTA = "PriceDeltaCash"
SENS_PRICE_CURVE_DELTA = "PriceCurveDeltaCash"

SENSITIVITIES = (
    (COL_ZAR_NOMINAL, "ZARNominal", COL_ZAR_NOMINAL),
    (COL_ZAR_MTM, "Portfolio Value", COL_ZAR_MTM),
    (COL_SENSITIVITY_PCD, "Price Curve Delta Cash", COL_SENSITIVITY_PCD),
    (CALC_GROUP_SENSITIVITY, "Portfolio FX Delta %", SENS_FX_DELTA),
    (CALC_GROUP_SENSITIVITY, "Portfolio Delta Cash", SENS_PRICE_DELTA),
    (CALC_GROUP_SENSITIVITY, "Benchmark Delta Full Per Curve Per Bucket",
     SENS_IR_BENCHMARK_DELTA),
    (CALC_GROUP_SENSITIVITY, "Portfolio Delta Yield Full Per Curve Per Bucket",
     SENS_IR_YIELD_DELTA)
)

# Other
INS_FILTERED = "Filtered"
INS_TOTAL = "Total"

MIDAS_CP_ID = 32845

#  Oracle SQL has a limit of 1000 elements in an IN clause. We are using SQL
#  server which is limited to 65k characters, but the Oracle limit (with
#  padding to cater for boundary conditions is a useful one to respect.
MAX_SQL_IN_SIZE = 997


################################################################################
#                            Column Value Functions
################################################################################
def col_expiry_date(trade, instrument):
    if instrument.InsType() in ("Curr", "Stock", "ETF"):
        return trade.ValueDay()
    else:
        return instrument.ExpiryDate()


def col_sovereign_issuer(issuer):
    if (issuer and
        issuer.Free4ChoiceList() and
        issuer.Free4ChoiceList().Name() == "SOV"):
            return 1
    return 0


def col_mtm_source(fa_trade):
    val_group = fa_trade.Instrument().ValuationGrpChlItem()

    if val_group and val_group.Name() in AQUA_VAL_GROUPS:
        return "AQUA"

    if fa_trade.AdditionalInfo().TMS_Trade_Id():
        return "CRE"

    return BLANK


################################################################################
#                    Utility Functions / Static Methods
################################################################################
def log(msg):
    print("%s - %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg))


def translate_enum(node_value, enum):
    if not isinstance(node_value, str):
        if node_value.IsKindOf(acm.FInteger):
            return node_value.Number()

    return ael.enum_from_string(enum, str(node_value))


def enums_to_int(names, enum):
    ids = []
    for name in names:
        i = translate_enum(name, enum)

        if i == 0:
            raise ValueError("Invalid %s enum: '%s'" % (enum, name))

        ids.append(str(i))

    return ",".join(ids)


def get_portfolio_child_ids(root_portfolio):
    result = []
    if root_portfolio:
        if root_portfolio.Compound():
            for portfolio in root_portfolio.AllPhysicalPortfolios():
                result.append(portfolio.Oid())
        else:
            result.append(root_portfolio.Oid())

    return result


def bucket_portfolio_ids(in_set, max_bucket_size=10):
    """Convert a set into an array of arrays.

    The portfolio list can get very long, which makes the SQL statement very
    messy. To get around this we display 10 id's per line.

    The returned array contains integers represented as string to simplify
    the use of join.
    """
    result = []
    for i in range(0, len(in_set), max_bucket_size):
        result.append(",".join([str(portfolio_id) for portfolio_id in
                                in_set[i:i+max_bucket_size]]))

    return ",\n".join(result)


def write_control_file(source_file, number_of_records, my_report_date):
    header_text = "SystemDate|RowCount|MD5 Hash of CSV file"

    control_file = source_file.replace(".csv", ".ctl")
    if control_file == source_file:  # Paranoid check
        raise ValueError("Control file should not have the same" +
                         "name as the output file!")

    with open(source_file, "r") as fin:
        hashed_sum = hashlib.md5(fin.read()).hexdigest()

    with open(control_file, "w") as fout:
        content_text = "%s|%s|%s" % (
            my_report_date,
            number_of_records,
            hashed_sum)

        fout.write("%s\n" % header_text)
        fout.write("%s\n" % content_text)
        print("Control file written to %s" % control_file)


def is_interest_rate_curve(curve):
    return (curve.IsKindOf(acm.FYieldCurve) or
            curve.IsKindOf(acm.FBenchmarkCurve))


################################################################################
#                    Class Definitions
################################################################################
class Timer(object):
    """Used for statistics and performance monitoring.

    The extract involves a lot of data and can take a long time to run. To aid
    performance tuning and capacity planning it is necessary to track the
    throughput.

    This class is used to keep a running total of the extract progress, and
    to store statistics that are displayed at the end of the extract. It also
    helps to keep the performance monitoring outside of the primary code as
    much as possible.
    """
    def __init__(self):
        self.last_time = time.clock()
        self.last_batch = self.last_time
        self.timings = []
        self.last_count = 0

    def step_complete(self, task):
        now = time.clock()
        self.timings.append("%s took %d seconds" % (task, (now-self.last_time)))
        self.last_time = now
        self.last_batch = now
        self.last_count = 0

    def update_throughput(self, count):
        now = time.clock()
        move = count - self.last_count
        duration = now - self.last_time
        last_duration = now - self.last_batch
        self.last_count = count
        self.last_batch = now

        if duration == 0:
            duration = 1
        if last_duration == 0:
            last_duration = 1

        timings = (60.0*move/last_duration, 60.0*count/duration)

        return "Last: %.1f rec/min   Overall: %.1f rec/min" % timings

    def display(self):
        for timing in self.timings:
            print("  ", timing)


# This class stores configuration parameters. Of course it has a lot of
# attributes.
# pylint: disable=too-many-instance-attributes
class ExtractParameters(object):
    """Manages and interprets parameter values used throughout the extract.

    This close contains the original vdict used to initialise the task. But it
    also has knowledge about how to interpret the vdict and convert certain
    parameters to more useful lists.

    There are also some data sets, such as lists of sovereign curves and
    currencies that are frequently referenced but never change. This class is
    responsible for managing and storing those lists, which means we don't
    need globals.
    """
    def __init__(self, vdict):
        self.parameters = vdict
        self.currencies = None
        self.ccy_config = None
        self.government_issuers = None
        self.government_curves = None
        self.single_instrument_curves = None
        self.price_curve_config = None
        self.collateral_portfolios = None
        self.portfolios = None

    def get(self, name):
        if name not in self.parameters:
            return None

        return self.parameters[name]

    def _create_price_curve_config(self):
        valuation_parameters = acm.FDictionary()
        valuation_parameters.AtPut('AggCurrChoice', 'Fixed Curr')
        valuation_parameters.AtPut('FixedCurr', 'ZAR')
        self.price_curve_config = acm.Sheet.Column().\
            ConfigurationFromColumnParameterDefinitionNamesAndValues(
                valuation_parameters)

    def _load_government_issuers(self):
        self.government_issuers = []

        for issuer in acm.FParty.Select("issuer=yes"):
            if issuer and issuer.Free4ChoiceList():
                if issuer.Free4ChoiceList().Name() == "SOV":
                    self.government_issuers.append(issuer.Name())

    def _is_sovereign_benchmark(self, benchmark):
        ins = benchmark.Instrument()
        if ins.Issuer() and ins.Issuer().Name() in self.government_issuers:
            return True

        return False

    def _load_curves(self):
        self.government_curves = {}
        self.single_instrument_curves = {}

        for curve in acm.FYieldCurve.Select(""):
            benchmarks = curve.Benchmarks()
            if benchmarks:
                if all(self._is_sovereign_benchmark(bm) for bm in benchmarks):
                    self.government_curves[curve.Name()] = benchmarks
                if len(benchmarks) == 1:
                    benchmark_name = benchmarks[0].Instrument().Name()
                    self.single_instrument_curves[curve.Name()] = benchmark_name

        print("  Loaded %i government/sovereign curves" % len(
            self.government_curves))
        print("  Loaded %i single instrument curves" % len(
            self.single_instrument_curves))

    def _create_currency_config(self):
        currencies = acm.FInstrument.Select("insType='Curr'")
        com_ccys = self.parameters[PARM_COMMODITY_CCYS]
        self.currencies = []

        farray = acm.FArray()
        for ccy in currencies:
            #  Database has a number of legacy commodities created as
            #  currencies. Real currencies always have 3 characters,
            #  although some instruments with 3 characters may be commodities
            #  using the official designation: e.g. XAU
            if len(ccy.Name()) == 3 and str(ccy.Name()) != "ZAR":
                if ccy.Name() not in com_ccys:
                    self.currencies.append(ccy.Name())

                    param = acm.FNamedParameters()
                    param.AddParameter("currency", ccy)
                    farray.Add(param)

        self.ccy_config = acm.Sheet.Column().ConfigurationFromVector(farray)

        print("  Loaded %i currencies" % len(self.currencies))

    def get_report_date(self):
        if PARM_REPORT_DATE in self.parameters:
            if self.parameters[PARM_REPORT_DATE]:
                return self.parameters[PARM_REPORT_DATE]

        return ael.date_valueday()

    def get_party_ids(self, parameter_name):
        result = []
        for party_name in self.parameters[parameter_name]:
            parties = acm.FParty.Select("name='%s'" % party_name)
            if len(parties) > 1:
                raise ValueError("Duplicate counterparty name: %s" % party_name)
            elif len(parties) != 1:
                raise ValueError("Cannot find party with name: %s" % party_name)

            result.append(str(parties[0].Oid()))

        return result

    def get_safe_trade_ids(self):
        trade_ids = self.parameters[PARM_TRADE_IDS]
        int_ids = [int(i) for i in trade_ids.split(",")]

        return [str(i) for i in int_ids]

    def get_counterparties_like(self):
        like_clause = self.parameters[PARM_CP_LIKE]
        result = []
        query = "select ptynbr from party where ptyid like '%s'" % like_clause
        for (party, ) in ael.asql(query, 1)[1][0]:
            result.append(str(party.ptynbr))

        if not result:
            raise ValueError("No counterparties with names like '%s'" %
                             like_clause)

        return result

    def _load_portfolio_ids(self, parameter_name):
        result = {}
        if parameter_name in self.parameters:
            portfolio_names = self.parameters[parameter_name]
            for name in portfolio_names:
                portfolio = acm.FPhysicalPortfolio[name]
                for portfolio_id in get_portfolio_child_ids(portfolio):
                    result[portfolio_id] = portfolio

        return result

    def load_data(self):
        self._create_price_curve_config()
        self._load_government_issuers()
        self._load_curves()
        self._create_currency_config()
        self.portfolios = self._load_portfolio_ids(PARM_PORTFOLIOS)
        self.collateral_portfolios = self._load_portfolio_ids(PARM_COLLATERAL)


class SensitivityResult(object):
    """Data object to store the results of a sensitivity calculation.

    The SensitivityResult class is essentially a structure to hold details
    about a sensitivity calculation. It does include some logic to ensure the
    calculated value is valid.
    """
    def __init__(self, name, cs_result, curve, parameter):
        self.name = name
        self.value = 0.0

        if curve:
            self.currency = curve.Currency().Name()
            self.curve_name = curve.Name()
            self.bucket = parameter
        elif parameter:
            self.currency = parameter
            self.curve_name = None
            self.bucket = None
        else:
            self.currency = None
            self.curve_name = None
            self.bucket = None

        self.cs_result = cs_result
        self.is_error = False

        if isinstance(cs_result, float):
            self.value = cs_result
        elif cs_result.IsKindOf(acm.FDenominatedValue):
            if name not in (COL_ZAR_NOMINAL, COL_SENSITIVITY_PCD):
                if cs_result.Unit().AsString() != "ZAR":
                    raise ValueError("Sensitivity result is not in ZAR.")

            self.value = cs_result.Number()
        else:
            raise ValueError("Don't know how to handle a result of type '%s'" %
                             type(cs_result))

        if isnan(self.value):
            self.is_error = True

    def include_result(self):
        if self.name in (COL_ZAR_NOMINAL, COL_ZAR_MTM):
            return True

        # Not a float is an error condition and should not be excluded.
        if self.is_error or not isinstance(self.value, float):
            return True

        return fabs(self.value) >= 0.001


class BatchCalculator(object):
    """Pre-load sensitivities for the batch extract.

    The Batch class uses the BatchCalculator to pre-load all calculations. The
    BatchCalculator was originally intended as a way to improve performance by
    running all calculations at once. However in local testing it turned out
    to be slightly quicker to calculate results per trade, but as it is still
    convenient to have the complex calculation logic in one place the class
    was kept separate.

    There are better ways to encapsulate the calculation logic, but the
    effort required at this stage outweighs the benefits.
    """
    def __init__(self, report_parameters, calc_space, root_item):
        self.report_parameters = report_parameters
        self.calc_space = calc_space
        self.root_item = root_item
        self.root_node = calc_space.InsertItem(root_item)
        self.results = {}

        calc_space.Refresh()

    def get_results(self, group_name, trade):
        if group_name in self.results:
            group = self.results[group_name]
            if trade.Oid() in group:
                return group[trade.Oid()]

        return None

    def get_value(self, group_name, trade):
        results = self.get_results(group_name, trade)
        if not results:
            return ""
        else:
            if len(results) != 1:
                #  This may happen if we are trying to get more than one value
                #  from a group that has multiple sensitivities.
                raise ValueError("Too many results for trade %s in group %s" %
                                 (trade.Oid(), group_name))

            return results[0].value

    def _add_result(self, group_name, trade, result):
        if group_name in self.results:
            group = self.results[group_name]
        else:
            group = {}
            self.results[group_name] = group

        if trade.Oid() in group:
            results = group[trade.Oid()]
        else:
            results = []
            group[trade.Oid()] = results

        results.append(result)

    # This method is doing a lot, very hard to use member variables instead
    # of arguments as these are all context sensitive. If you are refactoring
    # this code, this method would be a good point to start.
    # pylint: disable=too-many-arguments
    def _add_calc(self, node, trade, calc_info, config, curve, source_values):
        group_name, pm_name, result_name = calc_info
        if config:
            value = self.calc_space.CalculateValue(node, pm_name, config)
        else:
            value = self.calc_space.CalculateValue(node, pm_name)

        if not value:
            return

        if isinstance(value, float) or not value.IsKindOf(acm.FArray):
            result = SensitivityResult(result_name, value, curve, None)
            if result.include_result():
                self._add_result(group_name, trade, result)
                if result.is_error:
                    self._add_result(COL_ROW_ERROR, trade, result)
        else:
            for i, single_value in enumerate(value):
                result = SensitivityResult(
                    result_name,
                    single_value,
                    curve,
                    source_values[i])

                if result.include_result():
                    self._add_result(group_name, trade, result)

    def _get_curve_names(self, node, adfl_method):
        result = []
        curve_dict = {}
        curves = self.calc_space.CalculateValue(node, adfl_method)
        if curves:
            if not curves.IsKindOf(acm.FArray):
                curve_dict[curves.Name()] = curves
            else:
                for curve in curves:
                    curve_dict[curve.Name()] = curve

        for k in curve_dict.keys():
            result.append(curve_dict[k])

        return result

    def _do_interest_rate_delta(self, node, trade, calc_info, curve):
        if not is_interest_rate_curve(curve):
            return

        today = acm.Time().DateToday()
        bucket_names = (
            "t <= 1Y",
            "1Y < t <= 5Y",
            "5Y < t"
        )
        time_buckets = acm.Time.CreateTimeBuckets(
            today,
            "'1Y' '5Y' 'Rest'",
            None,
            None,
            0,
            False,
            False,
            False,
            False,
            False)

        farray = acm.FArray()
        farray.Add(curve)

        acm_column = acm.Sheet().Column()
        config = acm_column.ConfigurationFromVectorItem(farray)
        config = acm_column.ConfigurationFromTimeBuckets(time_buckets, config)

        self._add_calc(node, trade, calc_info, config, curve, bucket_names)

    def _do_calc_curves(self, node, trade, calc_info, curve_attr):
        for curve in self._get_curve_names(node, curve_attr):
            self._do_interest_rate_delta(node, trade, calc_info, curve)

    def _do_calc(self, node, trade, calc_info):
        result_name = calc_info[2]

        if result_name == SENS_FX_DELTA:
            self._add_calc(
                node,
                trade,
                calc_info,
                self.report_parameters.ccy_config,
                None,
                self.report_parameters.currencies)
        elif result_name == COL_SENSITIVITY_PCD:
            self._add_calc(
                node,
                trade,
                calc_info,
                self.report_parameters.price_curve_config,
                None,
                None)
        elif result_name == SENS_IR_BENCHMARK_DELTA:
            self._do_calc_curves(
                node,
                trade,
                calc_info,
                "BenchmarkCurvesInTheoreticalValue")
        elif result_name == SENS_IR_YIELD_DELTA:
            self._do_calc_curves(
                node,
                trade,
                calc_info,
                "YieldCurvesInTheoreticalValue")
        else:
            self._add_calc(node, trade, calc_info, None, None, None)

    def _do_calculations(self, node, trade, calc_list):
        for calc_info in calc_list:
            # If a calculation fails for any reason, we still want to continue.
            # Yes - we also catch exceptions that may be code problems, but if
            # this happens and nobody notices the data is missing or the log
            # file is enormous, then we may as well pack up and go home.
            # pylint: disable=broad-except
            try:
                self._do_calc(node, trade, calc_info)
            except Exception, ex:
                pm_name = calc_info[1]
                self._add_result(
                    COL_ROW_ERROR,
                    trade,
                    SensitivityResult(COL_ROW_ERROR, 1.0, None, None))
                print("Exception when calculating '%s' for trade %i: %s" % (
                    pm_name, trade.Oid(), str(ex)))
                traceback.print_exc()

    def _recurse_tree(self, node, calc_list):
        item = node.Item()

        if item.IsKindOf(acm.FTradeRow):
            self._do_calculations(node, item.Trade(), calc_list)
        elif node.NumberOfChildren():
            child = node.Iterator().FirstChild()
            while child:
                self._recurse_tree(child.Tree(), calc_list)
                child = child.NextSibling()

    def calc_using_tree(self, calc_list):
        root = self.root_item
        self.calc_space.SimulateValue(root, "Portfolio Currency", "ZAR")
        self._recurse_tree(self.root_node, calc_list)
        self.calc_space.RemoveSimulation(root, "Portfolio Currency")

    def calc_using_iteration(self, calc_list):
        for trade in self.root_item:
            self.calc_space.SimulateValue(trade, "Portfolio Currency", "ZAR")
            self._do_calculations(trade, trade, calc_list)
            self.calc_space.RemoveSimulation(trade, "Portfolio Currency")


class Batch(object):
    """Generates output rows in batches.

    The Batch class is responsible for formatting/generation of the output rows.
    Each Batch instance is intended to run as a separate thread (but doesn't at
    this point) and has its own calc space.

    Most of the logic for generating field values happens here. However more
    complex fields will have a "col_..." method at the top of this module.

    Sensitivities are pre-calculated using an instance of BatchCalculator.
    """
    def __init__(self, context, csv_out, report_parameters):
        self.csv_out = csv_out
        self.by_instrument = {}
        self.row_count = 0
        self.parameters = report_parameters
        self.calc_space = acm.Calculations().CreateCalculationSpace(
            context,
            acm.FTradeSheet)

    def by_instrument_totals(self):
        return self.by_instrument

    def instrument_total(self, name):
        if name in self.by_instrument:
            return self.by_instrument[name]

        return 0

    def is_sovereign(self, curve_name):
        return curve_name in self.parameters.government_curves

    def curve_matches_instrument(self, curve_name, ins_name):
        single_instrument_curves = self.parameters.single_instrument_curves
        if curve_name in single_instrument_curves:
            curve_ins = single_instrument_curves[curve_name]
            if ins_name == curve_ins:
                return True

        return False

    def find_commodity_currency(self, trade):
        commodity_currencies = self.parameters.get(PARM_COMMODITY_CCYS)
        if trade.Currency().Name() in commodity_currencies:
            return trade.Currency().Name()
        elif trade.Instrument().Currency().Name() in commodity_currencies:
            return trade.Instrument().Currency().Name()

        return None

    def _write_row(self, row_data):
        output = []
        for heading in HEADINGS:
            if heading in row_data:
                value = row_data[heading]
                if value and isinstance(value, float):
                    if isnan(value):
                        value = BLANK
                    elif fabs(value) < 0.01:
                        value = "%.11f" % value
                    else:
                        value = "%.2f" % value

                output.append(value)
            else:
                output.append(BLANK)

        self.csv_out.writerow(output)
        self.row_count += 1

    def _write_sensitivities(self, original_data, pcd, sensitivities):
        if not sensitivities:
            self._write_row(original_data)
        else:
            for sensitivity in sensitivities:
                curve_name = sensitivity.curve_name
                is_sovereign = self.is_sovereign(curve_name)

                row_data = original_data.copy()
                row_data[COL_SENSITIVITY_CCY] = sensitivity.currency
                row_data[COL_SENSITIVITY_TYPE] = sensitivity.name
                row_data[COL_SENSITIVITY_CURVE] = curve_name
                row_data[COL_SENSITIVITY_SOV] = 1 if is_sovereign else 0
                row_data[COL_SENSITIVITY_BUCKET] = sensitivity.bucket
                row_data[COL_SENSITIVITY] = sensitivity.value
                row_data[COL_SENSITIVITY_PCD] = pcd

                if COL_UNDERLYING_NAME in row_data:
                    match = self.curve_matches_instrument(
                        curve_name,
                        row_data[COL_UNDERLYING_NAME])
                    if match:
                        row_data[COL_SENSITIVITY_BSOU] = 1

                if sensitivity.is_error:
                    row_data[COL_ROW_ERROR] = 1

                self._write_row(row_data)

    # This method is the center of business logic. No wonder it has too many
    # variables. The variable count could be reduced by creating sub-methods
    # but this will probably make legibility worse, not better.
    # pylint: disable=too-many-locals
    def _process_trade(self, batch_calc, trade):
        add_info = trade.AdditionalInfo()
        instrument = trade.Instrument()
        counterparty = trade.Counterparty()
        portfolio = trade.Portfolio()
        trader = trade.Trader()
        underlying = instrument.Underlying()
        issuer = instrument.Issuer()
        und_issuer = None

        instype = instrument.InsType()
        is_midas_trade = (counterparty.Oid() == MIDAS_CP_ID)

        is_buy = trade.Quantity() >= 0

        zar_nominal = batch_calc.get_value(COL_ZAR_NOMINAL, trade)
        zar_mtm = batch_calc.get_value(COL_ZAR_MTM, trade)
        pcd = batch_calc.get_value(COL_SENSITIVITY_PCD, trade)

        row_data = {
            COL_TRADE_NO:           trade.Oid(),
            COL_TRADE_CURRENCY:     trade.Currency().Name(),
            COL_TRADE_TIME:         trade.TradeTime(),
            COL_TRADER:             trader.FullName() if trader else BLANK,
            COL_STATUS:             trade.Status(),
            COL_ACQUIRER_NAME:      trade.Acquirer().Name(),
            COL_INSTRUMENT:         instrument.Name(),
            COL_INSTRUMENT_TYPE:    instype,
            COL_EXPIRY_DATE:        col_expiry_date(trade, instrument),
            COL_UNDERLYING_TYPE:    instrument.UnderlyingType(),
            COL_BUY_OR_SELL:        "BUY" if is_buy else "SELL",
            COL_ZAR_NOMINAL:        zar_nominal,
            COL_ZAR_MTM:            zar_mtm,
            COL_MIDAS_ID:           trade.AdditionalInfo().Source_Trade_Id(),
            COL_ISSUER:             issuer.Name() if issuer else BLANK,
            COL_MTM_SOURCE:         col_mtm_source(trade),
            COL_PAY_TYPE:           instrument.PayType(),
            COL_COLLATERAL:         0,
            COL_OTC:                1 if instrument.Otc() else 0,
            COL_MTM_FROM_FEED:      1 if instrument.MtmFromFeed() else 0,
            COL_ROW_ERROR:          0,
            COL_SENSITIVITY_BSOU:   0
        }

        if is_midas_trade:
            row_data[COL_COUNTERPARTY_ID] = add_info.Source_Ctpy_Id()
            row_data[COL_COUNTERPARTY_NAME] = add_info.Source_Ctpy_Name()
        else:
            row_data[COL_COUNTERPARTY_ID] = counterparty.Oid()
            row_data[COL_COUNTERPARTY_NAME] = counterparty.Name()

        if underlying:
            und_issuer = underlying.Issuer()
            row_data[COL_UNDERLYING_NAME] = underlying.Name()
            row_data[COL_UNDERLYING_EXPIRY] = underlying.ExpiryDate()
            if und_issuer:
                row_data[COL_UNDERLYING_ISSUER] = und_issuer.Name()
        elif instype == "Curr":
            commodity = self.find_commodity_currency(trade)

            if commodity:
                row_data[COL_UNDERLYING_TYPE] = "Commodity"
                row_data[COL_UNDERLYING_NAME] = commodity

        if portfolio:
            pid = portfolio.Oid()
            row_data[COL_PORTFOLIO_CODE] = pid
            row_data[COL_PORTFOLIO_NAME] = portfolio.Name()

            if pid in self.parameters.portfolios:
                row_data[COL_ROOT_PORTFOLIO] = \
                    self.parameters.portfolios[pid].Name()
            if pid in self.parameters.collateral_portfolios:
                row_data[COL_COLLATERAL] = 1

        row_data[COL_SOVEREIGN_ISSUER] = col_sovereign_issuer(
            issuer or und_issuer)

        error = batch_calc.get_results(COL_ROW_ERROR, trade)
        if error:
            row_data[COL_ROW_ERROR] = 1

        self._write_sensitivities(
            row_data,
            pcd,
            batch_calc.get_results(CALC_GROUP_SENSITIVITY, trade))

    def _add_instrument_to_total(self, instype):
        if instype in self.by_instrument:
            self.by_instrument[instype] += 1
        else:
            self.by_instrument[instype] = 1

    def process(self, batch):
        """Load all trades in batch.

        Combination trades do not have an expiry date in the database, but the
        API will return a date, so we need to do a second check after loading
        the trade objects into memory.

        ASQLQuery.Select() does not return results in the correct order, so we
        need to reorder the results to match the incoming list of trade IDs.
        """
        if len(batch) == 0:
            return

        query = acm.CreateFASQLQuery(acm.FTrade, "OR")
        for trdnbr in batch:
            query.AddAttrNode("Oid", "EQUAL", trdnbr)

        trades = {}
        report_date = self.parameters.get_report_date().\
            to_string("%Y-%m-%d")
        for trade in query.Select():
            # Neither expiry_date nor report_date are based on datetime, which
            # makes comparison a pain. So we do a string compare instead.
            expiry_date = trade.Instrument().ExpiryDate()[0:10]
            if expiry_date and expiry_date < report_date:
                self._add_instrument_to_total(INS_FILTERED)
            else:
                trades[trade.Oid()] = trade

        if not trades:
            return

        batch_calc = BatchCalculator(
            self.parameters,
            self.calc_space,
            trades.values())

        batch_calc.calc_using_iteration(SENSITIVITIES)

        for trade_id in batch:
            if trade_id in trades:
                trade = trades[trade_id]
                instrument = trade.Instrument()
                self._add_instrument_to_total(instrument.InsType())
                self._add_instrument_to_total(INS_TOTAL)

                # There is no telling what values Front may return and it is
                # very difficult to predict what may go wrong because of other
                # changes in the system. It is better to catch everything and
                # let the process continue then have it die because of one
                # dodgy trade.
                # pylint: disable=broad-except
                try:
                    self._process_trade(batch_calc, trade)
                except Exception as ex:
                    print("Exception in trade %i: %s" % (trade.Oid(), str(ex)))
                    row_error = {
                        COL_TRADE_NO:  trade.Oid(),
                        COL_ROW_ERROR: 1
                    }
                    self._write_row(row_error)
                    traceback.print_exc()

        self.calc_space.Clear()


class Extract(object):
    """The Extract class is responsible for managing the extract process.

    The extract process starts here. The Extract class starts by building a
    list of trade IDs using dbsql. It then batches these into groups and passes
    the trade IDs to the Batch class. Doing it this way improves performance
    because only a few trades have to be instantiated at a time which saves
    memory while still benefiting from caching.
    """
    def __init__(self, timer, run_date):
        self.timer = timer
        self.run_date = run_date
        self.custom_filter = ""
        self.query_folders = []
        self.trade_ids = []
        self.query_counter = 0
        self.parameters = None
        self.row_count = 0

    def _get_split(self):
        split_total = self.parameters.get(PARM_SPLIT_TOTAL)
        split_instance = self.parameters.get(PARM_SPLIT_INSTANCE)

        if split_instance > split_total:
            raise ValueError("Split instance cannot be greater than " +
                             "the number of split files.")

        return split_instance, split_total

    def _get_trade_buckets(self):
        result = []

        sample_data_only = self.parameters.get(PARM_SAMPLE_DATA_B)
        split_instance, split_total = self._get_split()

        trade_bucket = []
        for trade_id in self.trade_ids:
            if split_total == 1:
                trade_bucket.append(trade_id)
            elif trade_id % split_total == split_instance - 1:
                trade_bucket.append(trade_id)

            if len(trade_bucket) > MAX_SQL_IN_SIZE:
                if sample_data_only:
                    result.append(trade_bucket[0:9])
                else:
                    result.append(trade_bucket)

                trade_bucket = []

        if trade_bucket:
            result.append(trade_bucket)

        return result

    def add_filter(self, new_filter):
        self.custom_filter += "\nAND %s" % new_filter

    def set_report_parameters(self, parameters):
        self.parameters = parameters

    def build_filename(self):
        prefix = self.parameters.get(PARM_FILE_PREFIX)
        report_date = self.run_date.to_string("%Y%m%d")
        current_time = time.strftime("%Y%m%d_%H%M%S")

        split_instance, split_total = self._get_split()

        if split_total != 1:
            return "%s_%i_of_%i_%s_%s.csv" % (
                prefix,
                split_instance,
                split_total,
                report_date,
                current_time)
        else:
            return "%s_%s_%s.csv" % (prefix, report_date, current_time)

    def load_trade_ids(self):
        log("Running query...")

        report_date = self.run_date.to_string("%Y-%m-%d")

        query = """
select t.trdnbr
from trade t,instrument i,party p
where t.insaddr=i.insaddr
and p.ptynbr=t.counterparty_ptynbr
and t.archive_status=0 %s
and (i.instype not in (%s) or t.value_day>='%s')
and (i.exp_day is null or i.exp_day>='%s')
order by i.instype,i.insaddr,t.trdnbr
        """ % (
            self.custom_filter,
            enums_to_int(VALUE_DAY_INSTRUMENTS, "InsType"),
            report_date, report_date
        )

        #  Grouping calculations by instrument type and instrument increases
        #  the cache hit ratio and can have a significant performance
        #  benefit.
        for trdnbr, in ael.dbsql(query)[0]:
            self.trade_ids.append(trdnbr)

    def run_batches(self, batch):
        trade_buckets = self._get_trade_buckets()
        progress_tick = int(len(trade_buckets)/100)
        if progress_tick < 1:
            progress_tick = 1

        trade_count = 0
        for counter, trade_bucket in enumerate(trade_buckets):
            if counter % progress_tick == 0:
                progress = int(100*counter/len(trade_buckets))
                log("=========== Completed: %3i%% =========== (%s)" % (
                    progress,
                    self.timer.update_throughput(trade_count)))

            batch.process(trade_bucket)

            trade_count = batch.instrument_total(INS_TOTAL)
        self.row_count = batch.row_count

    def desc(self, text, parameter):
        if self.parameters.get(parameter):
            print("  %s: %s" % (
                text,
                ",".join(self.parameters.get(parameter))
            ))

    def run_extract(self, fout):
        log("Extracting data:")
        log("  Report date: %s" % self.run_date.to_string("%Y-%m-%d"))

        split_instance, split_total = self._get_split()

        if self.parameters.get(PARM_SAMPLE_DATA_B):
            log("  Extracting a limited sample ******")
        if split_total != 1:
            log("  Extracting file %i of %i" % (split_instance, split_total))

        context = acm.FExtensionContext[EXTENSION_CONTEXT]
        csv_out = csv.writer(fout, delimiter="|")
        csv_out.writerow(HEADINGS)

        batch = Batch(context, csv_out, self.parameters)

        self.run_batches(batch)

        log("Done! %s" % (self.timer.update_throughput(
            batch.instrument_total(INS_TOTAL))))
        self.timer.step_complete("Analysis")

        print()
        print("Parameters:")
        self.desc("Portfolios", PARM_PORTFOLIOS)
        self.desc("Collateral", PARM_COLLATERAL)
        self.desc("Exclude Instruments", PARM_INSTRUMENTS)
        self.desc("Commodity Currencies", PARM_COMMODITY_CCYS)

        print()
        print("Instruments:")
        by_instrument = batch.by_instrument_totals()
        for instype, total in by_instrument.items():
            if instype != INS_TOTAL and instype != INS_FILTERED:
                print("  %-20.20s : %i" % (instype, total))

        print()
        print("Post filtered:", batch.instrument_total(INS_FILTERED))
        print("Total extracted:", batch.instrument_total(INS_TOTAL))
        print()


################################################################################
#                    Helper Functions for Task Definition
################################################################################
def get_instrument_types():
    return acm.FEnumeration["enum(InsType)"].Enumerators()


def get_internal_parties():
    return [party.Name() for party in acm.FParty.Select("type='Intern Dept'")]


def get_portfolios():
    return [portfolio.Name() for portfolio in acm.FPhysicalPortfolio.Select("")]


def get_currencies():
    result = []
    for ccy in acm.FInstrument.Select("insType='Curr'"):
        result.append(ccy.Name())

    return result


# This name is mandated by Front for tasks. Nothing we can do about it.
# pylint: disable=invalid-name
ael_variables = [
    (PARM_REPORT_DATE, "Report Date", "date", None, None, 0),
    (PARM_PORTFOLIOS, "Portfolios", "string",
     get_portfolios(), DEF_PORTFOLIOS, 1, 1),
    (PARM_COLLATERAL, "Collateral Portfolios", "string",
     get_portfolios(), DEF_COLLATERAL, 1, 1),
    (PARM_INSTRUMENTS, "Exclude Instruments", "string",
     get_instrument_types(), DEF_INSTRUMENTS, 1, 1),
    (PARM_INT_PARTIES, "Include Int. Parties", "string",
     get_internal_parties(), DEF_INT_PARTIES, 1, 1),
    (PARM_COMMODITY_CCYS, "Commodity Currencies", "string",
     get_currencies(), DEF_COMMODITY_CURRENCIES, 0, 1),
    (PARM_SPLIT_TOTAL, "Split into # files", "int", None, 1, 1),
    (PARM_SPLIT_INSTANCE, "  This is split #", "int", None, 1, 1),
    (PARM_FILE_PREFIX, "File Prefix", "string", None, DEF_FILENAME_PREFIX, 1),
    (PARM_SAMPLE_DATA_B, "Small Sample_Debug", "bool", [False, True], False, 2),
    (PARM_TRADE_IDS, "Trade IDs_Debug", "string", None, "", 0),
    (PARM_CP_LIKE, "Counterparties like_Debug", "string", None, "", 0),
]


################################################################################
#                             Task Entry Point
################################################################################
def ael_main(vdict):
    timer = Timer()
    print("Running:")

    parameters = ExtractParameters(vdict)

    parameters.load_data()

    my_report_date = parameters.get_report_date()
    extract = Extract(timer, my_report_date)

    extract.set_report_parameters(parameters)

    extract.add_filter("t.status not in (%s)" %
                       enums_to_int(DEF_EXCLUDE_STATUS, "TradeStatus"))

    portfolio_query = "t.prfnbr IN (%s) and i.instype not in (%s)" % (
        bucket_portfolio_ids(parameters.portfolios.keys()),
        enums_to_int(parameters.get(PARM_INSTRUMENTS), "InsType")
    )

    if parameters.get(PARM_COLLATERAL):
        extract.add_filter("((%s) \nOR t.prfnbr IN (%s))" % (
            portfolio_query,
            bucket_portfolio_ids(parameters.collateral_portfolios.keys())))
    else:
        extract.add_filter(portfolio_query)

    if parameters.get(PARM_INT_PARTIES):
        ids = parameters.get_party_ids(PARM_INT_PARTIES)
        extract.add_filter("(p.type not in (%s) or p.ptynbr in (%s))" % (
            enums_to_int(("Intern Dept", ), "PartyType"),
            ",".join(ids)))
    else:
        extract.add_filter("p.type not in (%s)" %
                           enums_to_int(("Intern Dept", ), "PartyType"))

    if parameters.get(PARM_TRADE_IDS):
        ids = parameters.get_safe_trade_ids()
        extract.add_filter("t.trdnbr IN(%s) " % ",".join(ids))

    if parameters.get(PARM_CP_LIKE):
        ids = parameters.get_counterparties_like()
        extract.add_filter("t.counterparty_ptynbr IN (%s)" % ",".join(ids))

    timer.step_complete("Init")

    extract.load_trade_ids()
    log("  Total unique trade IDs found: %i" % len(extract.trade_ids))

    timer.step_complete("Queries")

    file_name = extract.build_filename()
    with open(file_name, "wb") as fout:
        extract.run_extract(fout)

    print()
    print("Timings:")
    timer.display()

    write_control_file(file_name, extract.row_count, my_report_date)

    print("Output written to %s" % file_name)
