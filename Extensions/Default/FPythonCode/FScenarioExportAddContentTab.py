""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportAddContentTab.py"
"""----------------------------------------------------------------------------
MODULE
    FScenarioExportAddContentTab - Add content to the report

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FScenarioExportReport GUI which makes it possible
    to add additional content to the report on the fly. Portfolios, trade
    filters and trades can be added.
----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI


falseTrue = ['False', 'True']


class ScenarioExportAddContentTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        pfs = acm.FPhysicalPortfolio.Select('')
        tfs = acm.FTradeSelection.Select('')
        allQueries = acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
        tab_name = '_Add trades'
        ttPortfolios = 'Choose the portfolios to report'
        ttTradeFilters = ('Choose the trade filters (virtual portfolios) to '
                'report')
        ttStoredASQLQueries = ('Choose the Trade asql queries to report '
                '(only Shared queries are available)')
        ttTrades = 'Choose the trades report'
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['portfolios',
                        'Portfolios' + tab_name,
                        'FPhysicalPortfolio', pfs, None,
                        0, 1, ttPortfolios, None, 1],
                ['tradeFilters',
                        'Trade Filters' + tab_name,
                        'FTradeSelection', tfs, None,
                        0, 1, ttTradeFilters, None, 1],
                ['storedASQLQueries',
                        'Stored ASQL Queries' + tab_name,
                        'FStoredASQLQuery', allQueries, None,
                        0, 1, ttStoredASQLQueries, None, 1],
                ['trades',
                        'Trades' + tab_name,
                        'FTrade', '', None,
                        0, 1, ttTrades, None, 1],
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    ael_vars = ScenarioExportAddContentTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars
