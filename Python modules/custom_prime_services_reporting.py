"""
-------------------------------------------------------------------------------
MODULE
    custom_prime_services_reporting.py

DESCRIPTION
    In case of Prime Services overnight failures, we might need to re-run
    client reporting. Quite often, errors / invalid figures are present in only
    a few out of many EOD reports. This module allows RTB to create custom
    reporting tasks with only those reports ticked that need to have data
    corrected after the re-run.

    Date       : 2016-11-15
    Department : Prime Services
    Developer  : Jakub Tomaga
    CR Number  : CHNG0004085929

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
15-11-2016  4085929     Jakub Tomaga    Initial implementation
-------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from task_creator import TaskCreator
from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_fund_shortname)


class CustomPrimeServicesReportingCreator(TaskCreator):
    """Custom Prime Services reporting task creator."""
    def __init__(self, config):
        super(CustomPrimeServicesReportingCreator, self).__init__()
        self.funds = config["Funds"]
        self.output_path = config["OutputPath"].SelectedDirectory().AsString()
        self.reports = config["Reports"]
        self.name_modifier = config["NameModifier"]

    def _task_filter(self, task):
        """Return True if task meets conditions. Otherwise return False."""
        name = task.Name()
        for fund in self.funds:
            if name == "PS_Reporting_%s_SERVER" % fund:
                return True
        return False

    def _update(self, task):
        """Update task."""
        self._update_name(task)
        self._update_params(task)
        
    def _update_name(self, task):
        """Set new name."""
        task.Name('_'.join([task.Name(), self.name_modifier]))
    
    def _update_params(self, task):
        """Update task parameters."""
        params = task.Parameters()
        for report in ALL_REPORTS:
            param = report.split(' (')[0]
            if report in self.reports:
                params.AtPutStrings(param, "Yes")
            else:
                params.AtPutStrings(param, "No")
        if params.AtString("OutputPath") != self.output_path:
            params.AtPutStrings("OutputPath", self.output_path)
        params.Commit()
        task.Parameters(params)                


ALL_FUNDS = [get_pb_fund_shortname(cp) for cp in get_pb_fund_counterparties()]
ALL_REPORTS = [
    'Heavy Trade (File_TradeRoll)',
    'Light Trade (Report_TradeActivity)',
    'Heavy Position (File_Performance)',
    'Light Position (Report_Position)',
    'Heavy Instrument Position (File_PositionInstrument)',
    'Heavy Corporate Actions (File_CorporateActions)',
    'Light Corporate Actions (Report_CorporateActions)',
    'Heavy Financing (File_Financing)',
    'Light Financing (Report_Financing)',
    'Light Performance (Report_Performance)',
    'Heavy Collateral Trades (File_CollateralTrade)',
    'Heavy Collateral Positions (File_CollateralPosition)',
    'Light Collateral Positions (Report_CollateralPosition)',
    'Heavy Risk FX (File_RiskFX)',
    'Heavy Cash (File_CashAnalysis)',
    'Heavy Valuations (File_Valuations)',
    'Heavy Risk Yield Delta (File_RiskYieldDelta)',
    'Light Valuations (Report_Valuations)',
    'Heavy Cashflows (File_CashInstrument)',
    'Heavy Risk Swap Attribution Report (File_RiskSwapAttribution)',
    'Heavy Risk Bond Attribution Report (File_RiskBondAttribution)',
    'Heavy Risk Report - Reset Dates (File_RiskResetDates)'
]


ael_variables = AelVariableHandler()
ael_variables.add('Funds',
                  label='Funds',
                  multiple=True,
                  collection=ALL_FUNDS)
ael_variables.add_directory('OutputPath',
                  label='Output Path',
                  default='/services/frontnt/Task')
ael_variables.add('Reports',
                  label='Reports',
                  multiple=True,
                  collection=ALL_REPORTS)
ael_variables.add("NameModifier",
                  label='Name Modifier')


def ael_main(config):
    """Entry point of the script."""
    task_creator = CustomPrimeServicesReportingCreator(config)
    task_creator.run()
    print("Completed successfully.")
