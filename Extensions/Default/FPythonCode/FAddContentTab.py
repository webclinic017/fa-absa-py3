"""-------------------------------------------------------------------------------------------------------
MODULE
    FAddContentTab - Add content to the report

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FWorksheetReport GUI which makes it possible to add
    additional content to the report on the fly. Portfolios and trade filters can
    be added to portfolio sheets and trades can be added to trade sheets.

-------------------------------------------------------------------------------------------------------"""

import acm
import FRunScriptGUI

falseTrue = ['False', 'True']

class AddContentTab(FRunScriptGUI.AelVariablesHandler):
    def portfolioRowOnlyCB(self, index, fieldValues):
        """disable/enable display settings after snapsheet toggle"""
        notChecked = not (falseTrue.index(fieldValues[index]))
        self.zeroPositions.enable(notChecked)
        self.expiredPositions.enable(notChecked)
        self.instrumentRows.enable(notChecked)
        return fieldValues
        
    def dummy_cb(self, index, fieldvalues):
        pass
       
    def getParameterPortfolios(self):
        return acm.FPhysicalPortfolio.Select('')

    def getParameterTradeSelections(self):
        return acm.FTradeSelection.Select('')

    def getParameterQueriesTrades(self):
        return acm.FStoredASQLQuery.Select('user=0 and subType="FTrade"')
    
    def getParameterQueriesInstrument(self):
        return acm.FStoredASQLQuery.Select('user=0 and subType="FInstrument"')

    def getParameterQueriesTradesInfoManQueries(self):
        return acm.FSQL.Select('subType = "Trade"')

    def getParameterQueriesInstrumentInfoManQueries(self):
        return acm.FSQL.Select('subType = "Instrument"')
    
    def __init__(self, onInfoManQueriesChanged = None):
        tab_name = '_Add sheet content'
        if onInfoManQueriesChanged == None:
            onInfoManQueriesChanged = self.dummy_cb
        vars =[
                ['portfolios', 'Portfolios' + tab_name, 'FPhysicalPortfolio', self.getParameterPortfolios, None, 0, 1, 'Choose the portfolios to report', None, 1],
                ['tradeFilters', 'Trade Filters' + tab_name, 'FTradeSelection', self.getParameterTradeSelections, None, 0, 1, 'Choose the trade filters (virtual portfolios) to report', None, 1],
                ['storedASQLQueries', 'Stored Trade ASQL Queries' + tab_name, 'FStoredASQLQuery', self.getParameterQueriesTrades, None, 0, 1, 'Choose the Trade asql queries to report (only Shared queries are available)', None, 1],
                ['storedASQLQueriesInstrument', 'Stored Instrument ASQL Queries' + tab_name, 'FStoredASQLQuery', self.getParameterQueriesInstrument, None, 0, 1, 'Choose the Instrument asql queries to report (only Shared queries are available)', None, 1],
                ['infoManQueriesTrades', 'Trade Information Manager Queries' + tab_name, 'FSQL', self.getParameterQueriesTradesInfoManQueries, None, 0, 1, 'Choose the Information Manager Queries (only queries installed as filter are available)', onInfoManQueriesChanged, 1],
                ['infoManQueriesInstrument', 'Instrument Information Manager Queries' + tab_name, 'FSQL', self.getParameterQueriesInstrumentInfoManQueries, None, 0, 1, 'Choose the Information Manager Queries (only queries installed as filter are available)', onInfoManQueriesChanged, 1],
                ['macros', 'Macros' + tab_name, 'string', [], None, 0, 0, 'FMACROGUI variable1=value:variable2=value', None, 1],
                ['useMacroGUI', 'Use Macro GUI' + tab_name, 'string', falseTrue, 'False', 1, 0, 'Should the extended Macro GUI be used?', None, 1],
                ['trades', 'Trades' + tab_name, 'FTrade', '', None, 0, 1, 'Choose the trades report', None, 1],
                ['tradeRowsOnly', 'Trade Rows Only (Trade Sheet)' + tab_name, 'string', falseTrue, 'True', 1, 0, 'Insert trade rows only in trade sheet report', None, 1],
                ['portfolioRowOnly', 'Portfolio Row Only' + tab_name, 'string', falseTrue, 'False', 1, 0, 'Show portfolio row only in report', self.portfolioRowOnlyCB, 1],
                ['zeroPositions', 'Include Zero Positions' + tab_name, 'string', falseTrue, 'False', 1, 0, 'Include zero positions in report', None, 1],
                ['expiredPositions', 'Include Expired Positions' + tab_name, 'string', falseTrue, 'False', 1, 0, 'Include expired positions in report', None, 1],
                ['instrumentRows', 'Show Instrument Rows' + tab_name, 'string', falseTrue, 'True', 1, 0, 'Show instrument rows in report', None, 1],
                ['clearSheetContent', 'Clear Workbook/Template Content' + tab_name, 'string', falseTrue, 'False', 1, 0, 'The output will only contain the content added here, and not the original content of the portfolio or trade sheet.', None, 1],
                ['grouping', 'Grouping' + tab_name, 'FStoredPortfolioGrouper', None, '', 0, 1, 'Set the grouping wanted for each portfolio', None, 1],
                ['timeBuckets', 'Time Buckets' + tab_name, 'FStoredTimeBuckets', None, '', 0, 1, 'Set the time buckets (Portfolio Sheet and Time Sheet)', None, 1],
                ['verticalScenario', 'Vertical Scenario' + tab_name, 'FStoredScenario', None, '', 0, 1, 'Vertical Scenario(Portfolio Sheet )', None, 1]]
                

        FRunScriptGUI.AelVariablesHandler.__init__(self, vars, __name__)
        

def getAelVariables():
    ael_vars=AddContentTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars

def getAelVariablesWithCB(onInfoManQueriesChanged):
    ael_vars=AddContentTab(onInfoManQueriesChanged)
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars

