""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FRiskExport.py"
"""----------------------------------------------------------------------------
MODULE
    FScenarioExportReport - Run Script GUI for scenario export report creation

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""


import acm


import FReportAPI
import FRunScriptGUI
import FLogger


import FScenarioExportMain
import importlib
importlib.reload(FScenarioExportMain)
import FScenarioExportAddContentTab
import FScenarioExportOutputSettingsTab
import FScenarioExportTheoreticalValuesTab
import FScenarioExportProfitAndLossValuesTab
import FScenarioExportLogSettingsTab
import FScenarioExportParameters
importlib.reload(FScenarioExportParameters)

logger = FLogger.FLogger.GetLogger("FAReporting")
falseTrue = ["False", "True"]


class ScenarioExportReport(FRunScriptGUI.AelVariablesHandler):

    def wbCB(self, index, fieldValues):
        """vice versa toggle between workbook and sheet template"""
        if self.ael_variables[index][0] == "wbName":
            changeIndex = index + 1
        else:
            changeIndex = index - 1
        self.ael_variables[changeIndex][9] = (fieldValues[index] == "")
        return fieldValues

    def __init__(self):
        workbooks = [wb for wb in acm.FWorkbook.Select("createUser = " +
            str(acm.FUser[acm.UserName()].Oid()))]
        workbooks.sort()
        templates = acm.FTradingSheetTemplate.Select("")
        currencies = acm.FCurrency.Select("")
        accounting_curr = acm.GetFunction("mappedValuationParameters",
                0)().Parameter().AccountingCurrency()
        variables = [
                 ["wbName", "Workbook", "FWorkbook", workbooks, "", 0, 0,
                  "Choose a work book", self.wbCB, 1],
                 ["template", "Trading Sheet Template",
                     "FTradingSheetTemplate", templates, None, 0, 0,
                     "Choose a trading sheet template", self.wbCB, 1],
                 ["horizon", "Horizon", "dateperiod", None, "1d", 1, 0,
                    "The horizon for the report"],
                 ["report_currency", "Report Currency", "FCurrency",
                     currencies, accounting_curr, 1, 0,
                    "The report currency for the report"],
               ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)
        # add other tabs
        self.extend(FScenarioExportAddContentTab.getAelVariables())
        self.extend(FScenarioExportTheoreticalValuesTab.getAelVariables())
        self.extend(FScenarioExportProfitAndLossValuesTab.getAelVariables())
        self.extend(FScenarioExportOutputSettingsTab.getAelVariables())
        self.extend(FScenarioExportLogSettingsTab.getAelVariables())


ael_gui_parameters = {"windowCaption": __name__}
ael_variables = ScenarioExportReport()
ael_variables.LoadDefaultValues(__name__)


def create_scenario_count_file(scenario_params, pv_scenario_content):
    if scenario_params.do_create_count_file() and pv_scenario_content:
        count_outfile_path = scenario_params.count_file_name()
        logger.LOG("Creating Scenario Count file at '%s'", count_outfile_path)
        count_ostream = acm.FCharacterOutputFileStream(count_outfile_path)
        FScenarioExportMain.produce_scenario_count_report(
            scenario_params.delimiter(),
            scenario_params.sub_delimiter(),
            scenario_params.horizon(),
            scenario_params.horizon_order(),
            scenario_params.var_type(),
            count_ostream,
            pv_scenario_content)
        count_ostream.Close()


def specific_report_header_creator_wrapper(common_content):
    def create_report_header_specifics(params, specific_content, var_type,
            pl_source, curve_date, moneyness, scenario, stress_type):
        if not params.do_create_report() or specific_content is None:
            return

        outfile_path = params.get_output_file_name()
        outfile = acm.FCharacterOutputFileStream(outfile_path)
        common_content.register_writer(outfile)
        specific_content.register_writer(outfile)
        FScenarioExportMain.produce_report_header_using_content_managers(
            params.delimiter(),
            params.sub_delimiter(),
            outfile,
            params.horizon(),
            params.horizon_order(),
            var_type,
            pl_source,
            curve_date,
            moneyness,
            scenario,
            stress_type,
            common_content,
            specific_content)
        logger.LOG("Wrote header to output file '%s'", outfile_path)
        return (outfile, outfile_path)
    return create_report_header_specifics


def create_data_in_reports(trades, delimiter, ostreams, file_names,
        *content_managers):
    FScenarioExportMain.produce_report(
        trades,
        delimiter,
        ostreams,
        *content_managers)
    map(lambda x: logger.LOG("Wrote content to output file '%s'", x),
            file_names)


def create_main_reports(trd_attr_params, pv_scenario_params,
        stress_scenario_params, pl_params, market_value_params, trades,
        trd_attr_content, pv_scenario_content, stress_scenario_content,
        market_value_content, pnl_value_content):
    create_report_header_specifics = specific_report_header_creator_wrapper(
            trd_attr_content)

    output_files_info = []
    output_files_info.append(create_report_header_specifics(pv_scenario_params,
        pv_scenario_content, pv_scenario_params.var_type(), None,
        acm.Time().DateToday(), "1.0", "0", None))
    output_files_info.append(create_report_header_specifics(pl_params,
        pnl_value_content, None,
        pl_params.pl_source(), acm.Time().DateToday(), "1.0", None, None))
    output_files_info.append(create_report_header_specifics(
        stress_scenario_params, stress_scenario_content, None, None,
        acm.Time().DateToday(), "1.0", None, "Standard"))
    output_files_info.append(create_report_header_specifics(
        market_value_params, market_value_content, None, None,
        acm.Time().DateToday(), "1.0", None, None))

    ostreams = [data[0] for data in output_files_info if data is not None]
    file_names = [data[1] for data in output_files_info if data is not None]

    try:
        create_data_in_reports(
            trades,
            pv_scenario_params.delimiter(),
            ostreams,
            file_names,
            trd_attr_content,
            pv_scenario_content,
            stress_scenario_content,
            market_value_content,
            pnl_value_content)
    finally:
        for ostream in ostreams:
            ostream.Close()


def ael_main(ael_params):
    # Initialize the logger, should go _first_ of all initalizations
    FScenarioExportLogSettingsTab.logger_setup(ael_params, "FAReporting")

    trd_params = FScenarioExportParameters.TradeAttributeParameters(ael_params)
    pv_scenario_params = FScenarioExportParameters.PvScenarioParameters(
            ael_params)
    stress_scenario_params = \
            FScenarioExportParameters.StressScenarioParameters(ael_params)
    pl_params = FScenarioExportParameters.PLParameters(ael_params)
    market_value_params = FScenarioExportParameters.MarketValueParameters(
            ael_params)

    """
    Create the content managers responsible for creating the actual
    report content.
    """
    trd_attr_content = (FScenarioExportParameters.
        create_trd_attr_content_manager(trd_params))
    pv_scenario_content = (FScenarioExportParameters.
        create_pv_scenario_content_manager(pv_scenario_params))
    stress_scenario_content = (FScenarioExportParameters.
        create_stress_scenario_content_manager(stress_scenario_params))
    market_value_content = (FScenarioExportParameters.
        create_market_value_content_manager(market_value_params))
    pnl_value_content = (FScenarioExportParameters.
        create_profit_and_loss_content_manager(pl_params))

    """
    Parse the Worksheet report XML to get the range of trades selected
    for export
    """
    trades = trd_attr_content.get_trades()
    logger.LOG("Exporting %s nbr of trades", len(trades))

    create_scenario_count_file(pv_scenario_params, pv_scenario_content)
    create_main_reports(trd_params, pv_scenario_params, stress_scenario_params,
            pl_params, market_value_params, trades, trd_attr_content,
            pv_scenario_content, stress_scenario_content, market_value_content,
            pnl_value_content)
