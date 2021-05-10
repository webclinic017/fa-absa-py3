""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportProfitAndLossValuesTab.py"
"""----------------------------------------------------------------------------
MODULE
    FOutputFileSettingsTab - Scenario settings tab

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FScenarioExportReport GUI which contains settings
    that sets up scenario calculations.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI


trueFalse = ["False", "True"]
tab_name = "_profit and loss settings"


class ScenarioExportProfitAndLossValuesTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        accounting_curr = (acm.GetFunction("mappedValuationParameters", 0)(
                ).Parameter().AccountingCurrency())
        calendars = acm.FCalendar.Select("")
        ttCreatePnlValue = "Calculate PnL value and feed into report?"
        ttPlSource = "Source of the PnL calculation?"
        ttPlStartDate = "The start date of the profit and loss period"
        ttPlCalendar = "The calendar used for adjusting reference date"
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ["create_pnl_value",
                        "Profit and Loss" + tab_name,
                        "string", trueFalse, "False",
                        1, 0, ttCreatePnlValue],
                ["pl_source",
                        "Profit and Loss Source" + tab_name,
                        "string", None, None,
                        0, 0, ttPlSource],
                ["pl_start_date",
                        "Profit and Loss Start Date" + tab_name,
                        "string", None, None,
                        0, 0, ttPlStartDate],
                ["pl_calendar",
                        "Calendar" + tab_name,
                        "FCalendar", calendars, accounting_curr.Calendar(),
                        1, 0, ttPlCalendar]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    outtab = ScenarioExportProfitAndLossValuesTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
