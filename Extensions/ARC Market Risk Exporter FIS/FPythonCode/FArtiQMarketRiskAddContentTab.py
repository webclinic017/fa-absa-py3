""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FArtiQMarketRiskAddContentTab.py"
"""----------------------------------------------------------------------------
MODULE
    FArtiQMarketRiskAddContentTab - Add content to the report

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which makes it possible
    to add additional content to the report on the fly. Portfolios, trade
    filters and trades can be added.
----------------------------------------------------------------------------"""


import acm
import FRunScriptGUI


class ArtiQMarketRiskAddContentTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        pfs = acm.FPhysicalPortfolio.Select('')
        tfs = acm.FTradeSelection.Select('')
        allQueries = acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
        tab_name = '_Positions'
        ttPortfolios = 'Choose the portfolios to report'
        ttTradeFilters = ('Choose the trade filters (virtual portfolios) to '
                'report')
        ttStoredASQLQueries = ('Choose the trade asql queries to report '
                '(only shared queries are available)')
        ttTrades = 'Choose the trades report'
        ttHorizon = 'The horizon for the report'
        ttPositionSpec = (
        'Used to define the positions and specifies which trade attributes '
        'to report.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                # ExportCalculatedValues expects these to be strings for now.
                ['distributedCalculations',
                         'Use distributed calculations',
                         'int', [0, 1], 0, True, False,
                         'Use distributed calculations for improved performance',
                         None, True],
                ['horizon',
                         'Horizon',
                         'string', None, '1d',
                         0, 0, ttHorizon, None, 1, None],
                ['positionSpec',
                        'Position specification' + tab_name,
                        acm.FPositionSpecification, None, None,
                        0, 0, ttPositionSpec],
                ['portfolios',
                         'Portfolios' + tab_name,
                         'string', pfs, None,
                         0, 1, ttPortfolios, None, 1],
                ['tradeFilters',
                         'Trade filters' + tab_name,
                         'string', tfs, None,
                         0, 1, ttTradeFilters, None, 1],
                ['storedASQLQueries',
                         'Stored ASQL queries' + tab_name,
                         'string', allQueries, None,
                         0, 1, ttStoredASQLQueries, None, 1],
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)


def getAelVariables():

    ael_vars = ArtiQMarketRiskAddContentTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars
