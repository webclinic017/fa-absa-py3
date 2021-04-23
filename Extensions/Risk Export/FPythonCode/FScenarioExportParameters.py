""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportParameters.py"
"""---------------------------------------------------------------------------
MODULE
    FScenarioExportParameters - Parameter helper class to provide utility
        and validation of the supplied ael_parameters dictionary

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

---------------------------------------------------------------------------"""


from exceptions import NotImplementedError, Exception


import acm


import FScenarioExportUtils


import FReportAPI
import FLogger


from FScenarioExportTradeAttributesManager import (
    ScenarioExportTradeAttributesManager)
from FScenarioExportScenarioPVManager import (
    ScenarioExportScenarioPVManager)
from FScenarioExportStressScenarioManager import (
    ScenarioExportStressScenarioManager)
from FScenarioExportSingleCalculatedValueManager import (
    ScenarioExportSingleCalculatedValueManager)
from FScenarioExportMultipleCalculatedValueManager import (
    ScenarioExportMultipleCalculatedValueManager)


from FScenarioExportUtils import (STD_CALC_PARAM_DISPLAY_CURR,
        STD_CALC_PARAM_START_DATE, STD_CALC_PARAM_END_DATE)


DEFAULT_FILE_NAME_PL = "plexport"
DEFAULT_FILE_NAME_PV_SCENARIO = "pv_scenario"
DEFAULT_FILE_NAME_STRESS_SCENARIO = "stress_scenario"
DEFAULT_FILE_NAME_MARKET_VALUE = "market_value"


logger = FLogger.FLogger.GetLogger("FAReporting")
falseTrue = ["False", "True"]


class CommonParameters(object):
    """
    Base class for all the parameter helper classes
    """
    def __init__(self, ael_parameters):
        self.ael_params = ael_parameters
        self.today = acm.Time().DateToday()

    def reference_date(self):
        return self.today

    def horizon(self):
        hor = self.ael_params["horizon"]
        if not hor:
            raise Exception("Horizon not set")
        return hor

    def horizon_order(self):
        dp = self.horizon()
        if dp.endswith("d"):
            n = 1
        elif dp.endswith("w"):
            n = 7
        elif dp.endswith("y"):
            n = 365
        try:
            count = int(dp[:-1])
        except:
            count = 0
        return count * n

    def delimiter(self):
        return self.ael_params["delimiter"]

    def sub_delimiter(self):
        return self.ael_params["sub_delimiter"]

    def report_currency(self):
        return self.ael_params["report_currency"]

    def _file_path(self):
        fp = self.ael_params["File Path"]
        if isinstance(fp, str):
            outdir = fp
        else:
            outdir = fp.AsString()
        return outdir

    def _do_date_dir(self):
        return falseTrue.index(self.ael_params["Create directory with date"])

    def _output_directory(self):
        outdir = self._file_path()
        date_directory = self._do_date_dir()
        outdir = FScenarioExportUtils.get_directory(outdir,
                self.reference_date(), date_directory)
        try:
            if FScenarioExportUtils.create_directory(outdir):
                logger.LOG("Created report output directory:" + outdir)
        except:
            msg = "Failed to create report directory:" + outdir
            logger.ELOG(msg)
            raise
        return outdir

    def _base_file_name(self):
        raise NotImplementedError("Use derived class")

    def _overwrite(self):
        return falseTrue.index(self.ael_params["Overwrite if file exists"])

    def get_output_file_name(self, is_count_file=False):
        outdir = self._output_directory()
        overwrite = self._overwrite()
        file_name = (self.ael_params["Output File Prefix"] +
                self._base_file_name())
        try:
            ofile = FScenarioExportUtils.get_output_file_name(outdir,
                    file_name, overwrite, is_count_file)
        except:
            logger.ELOG("Failed to create output file")
            raise
        return ofile


class TradeAttributeParameters(CommonParameters):
    """
    Helper class for all trade attribute parameters used in the report
    creation/calculation
    """
    def __init__(self, ael_parameters):
        super(TradeAttributeParameters, self).__init__(ael_parameters)

    def get_api_params(self):
        params = self.ael_params
        return {
                "workbook": params["wbName"],
                "template": params["template"],
                "tradeFilters": params["tradeFilters"],
                "portfolios": params["portfolios"],
                "tradeFilters": params["tradeFilters"],
                "storedASQLQueries": params["storedASQLQueries"],
                "trades": params["trades"],
                "expiredPositions": True,
                "zeroPositions": True,
                "clearSheetContent": True,
                "htmlToFile": False,
                "htmlToScreen": False,
                "tradeRowsOnly": True,
                "instrumentRows": True,
                "includeFormattedData": False,
                "includeRawData": True
                }


class ScenarioParameters(CommonParameters):
    """
    Helper class for all scenario parameters used in the
    report creation/calculation
    """
    def __init__(self, ael_parameters):
        super(ScenarioParameters, self).__init__(ael_parameters)

    def display_type(self):
        return self.ael_params["display_type"]


class PvScenarioParameters(ScenarioParameters):
    def __init__(self, ael_parameters):
        super(PvScenarioParameters, self).__init__(ael_parameters)

    def do_create_report(self):
        return self.pv_scenario_file_exists()

    def _base_file_name(self):
        fn = self.ael_params["PV Scenario File Name"]
        if not fn:
            fn = DEFAULT_FILE_NAME_PV_SCENARIO
        return fn

    def risk_types_include_in_residual(self):
        risk_types_incl = ["Interest Rate", "Volatility",
                           "Equity", "FX", "Credit", "Commodity"]
        return FScenarioExportUtils.incl_in_residual_dict(risk_types_incl)

    def do_create_count_file(self):
        return falseTrue.index(self.ael_params["create_utility_files"])

    def risk_factor_types(self):
        unadj_risk_factor_types = self.ael_params["risk_types"]
        if not unadj_risk_factor_types:
            risk_types = ["None"]
        else:
            risk_types = FScenarioExportUtils.convert_risk_types(
                unadj_risk_factor_types)
        return risk_types

    def count_file_name(self):
        return self.get_output_file_name(True)

    def pv_scenario_file(self):
        file_path = self.ael_params["scenario_file"]
        if not file_path or not file_path.SelectedFile():
            raise Exception("No pv scenario file specified")
        return file_path.SelectedFile()

    def pv_scenario_file_exists(self):
        try:
            f = self.pv_scenario_file()
            return bool(f)
        except:
            return False

    def var_type(self):
        var_type = self.ael_params["var_type"]
        if self.pv_scenario_file_exists():
            if not var_type:
                raise Exception("VaR Type is mandatory for PV Scenario "
                        "exports")
            else:
                return var_type
        return None


class StressScenarioParameters(ScenarioParameters):
    def __init__(self, ael_parameters):
        super(StressScenarioParameters, self).__init__(ael_parameters)

    def _base_file_name(self):
        fn = self.ael_params["Stress Scenario File Name"]
        if not fn:
            fn = DEFAULT_FILE_NAME_STRESS_SCENARIO
        return fn

    def do_create_report(self):
        return self.stress_scenario_file_exists()

    def stress_scenario_file(self):
        file_path = self.ael_params["stress_scenario_file"]
        if not file_path or not file_path.SelectedFile():
            raise Exception("No stress scenario file specified")
        return file_path.SelectedFile()

    def stress_scenario_file_exists(self):
        try:
            f = self.stress_scenario_file()
            return bool(f)
        except:
            return False


class MarketValueParameters(CommonParameters):
    """
    Helper class for all user defined parameters used for the market value
    calculations and reporting.
    """
    def __init__(self, ael_parameters):
        super(MarketValueParameters, self).__init__(ael_parameters)

    def do_create_report(self):
        return self._do_create_market_value()

    def _base_file_name(self):
        fn = self.ael_params["Market Value File Name"]
        if not fn:
            fn = DEFAULT_FILE_NAME_MARKET_VALUE
        return fn

    def _do_create_market_value(self):
        return falseTrue.index(self.ael_params["create_market_value"])


class PLParameters(CommonParameters):
    """
    Helper class for all user defined parameters used for the profit and
    loss calculations and reporting.
    """
    def __init__(self, ael_parameters):
        super(PLParameters, self).__init__(ael_parameters)

    def do_create_report(self):
        return self._do_create_pl_value()

    def calendar(self):
        cal = self.ael_params["pl_calendar"]
        if not cal:
            raise Exception("PL calendar not specified")
        return cal

    def _unadj_pl_start_date(self):
        rdate = self.ael_params["pl_start_date"]
        if not rdate:
            raise Exception("PL start date not set")
        return rdate

    def reference_date(self):
        return self.pl_start_date()

    def pl_start_date(self):
        unadj_pl_start_date = self._unadj_pl_start_date()
        return str(FScenarioExportUtils.adjust_ref_date(unadj_pl_start_date,
            self.calendar()))

    def pl_end_date(self):
        pl_start_date = self.pl_start_date()
        pl_end_date = str(FScenarioExportUtils.get_end_date(pl_start_date,
            self.calendar(), self.horizon()))
        return pl_end_date

    def pl_source(self):
        return self.ael_params["pl_source"]

    def _base_file_name(self):
        fn = self.ael_params["PL File Name"]
        if not fn:
            fn = DEFAULT_FILE_NAME_PL
        return fn

    def _do_create_pl_value(self):
        return falseTrue.index(self.ael_params["create_pnl_value"])

"""
The functions below all aid in the creation of the content manager objects
used in the main processing to calculate the actual content of the report.
"""


def create_trd_attr_content_manager(trd_attr_params):
    api_params = trd_attr_params.get_api_params()
    report_params = FReportAPI.FWorksheetReportApiParameters(**api_params)
    xml = FReportAPI.FReportParametersBase.GenerateReportXml(report_params)
    if not xml:
        return None
    return ScenarioExportTradeAttributesManager(xml)


def create_stress_scenario_content_manager(scenario_params):
    try:
        file_path = scenario_params.stress_scenario_file()
    except:
        return None
    cman = ScenarioExportStressScenarioManager(
        scenario_params.report_currency(), file_path,
        scenario_params.sub_delimiter(), scenario_params.display_type())
    return cman


def create_pv_scenario_content_manager(scenario_params):
    try:
        file_path = scenario_params.pv_scenario_file()
    except:
        return None
    risk_types = scenario_params.risk_factor_types()
    _incl_in_residual = scenario_params.risk_types_include_in_residual()
    cman = ScenarioExportScenarioPVManager(scenario_params.report_currency(),
        file_path, scenario_params.sub_delimiter(), risk_types,
        scenario_params.display_type())
    return cman


def create_market_value_content_manager(market_value_params):
    if not market_value_params.do_create_report():
        return None
    std_calc_name = ["TheoreticalValue"]
    measure_name = "Market Value"
    measure_group_name = ["Market Value"]
    measure_header = []
    provide_measure_values = False
    std_calc_params = {
            STD_CALC_PARAM_DISPLAY_CURR: market_value_params.report_currency()}
    return ScenarioExportMultipleCalculatedValueManager(measure_name,
            measure_group_name, measure_header,
            market_value_params.sub_delimiter(), std_calc_name,
            std_calc_params, None, 1, provide_measure_values)


def create_profit_and_loss_content_manager(pl_params):
    """
    Creates a profit and loss content manager
    """
    if not pl_params.do_create_report():
        return None

    pnl_start = pl_params.pl_start_date()
    pnl_end = pl_params.pl_end_date()
    std_calc_params = {
            STD_CALC_PARAM_START_DATE: pnl_start,
            STD_CALC_PARAM_END_DATE: pnl_end,
            STD_CALC_PARAM_DISPLAY_CURR: pl_params.report_currency()}
    measure_label = []
    measure_name = "Profit and Loss"
    std_calc_name = "TotalProfitLoss"
    measure_header = []
    measure_group_name = "Profit and Loss"
    return ScenarioExportSingleCalculatedValueManager(measure_name,
        measure_group_name, measure_header, pl_params.sub_delimiter(),
        std_calc_name, std_calc_params, measure_label)
