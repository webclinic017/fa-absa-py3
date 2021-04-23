""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FScripDividend.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FScripDividend - Module to process scrip dividend

DESCRIPTION
    This is the start-script for the Scrip Dividend procedure. It mainly
    contains the parameter GUI. The script FScripDivPerform then takes
    over the execution of the procedure.
----------------------------------------------------------------------------"""


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FScripDivConst
importlib.reload(FScripDivConst)


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',)


qInstrument = FBDPGui.insertInstruments(generic=0,
        instype=FScripDivConst.INS_TYPES_ALLOWED)

qPortfolio = FBDPGui.insertPhysicalPortfolio()


# ## Tool Tip


ttInstrument = 'Select the scrip dividend instrument'
ttScripIssuePerShare = ('The fraction that each currently held share '
        ' is entitled to if the cash dividend is to be converted.'
        '  eg. 0.123456')
ttTradeQuantityRounding = 'Select the rounding convention'
ttPortfolios = ('Trades of the specified instrument in the selected '
        'portfolios will be processed.')
ttTradeFilters = ('Trades of the specified instrument selected by these '
        'trade filters will be processed.')


cvTradeQuantityRounding = FScripDivConst.ROUNDING_CHOICES

def cbPosition(index, fieldValues):

    tt = 'You can only select one type of object.'
    for variableName in ('Instrument', 'CorporateAction'):
        field = getattr(ael_variables, variableName)
        if field.sequenceNumber != index:
            field.enable(not fieldValues[index], tt)
    return fieldValues

def cbInstrument(index, fieldValues):
    fieldValues = cbPosition(index, fieldValues)
    fieldValues[index] = fieldValues[index].split(',')[0]
    return fieldValues

def cbCorpAction(index, fieldValues):
    fieldValues = cbPosition(index, fieldValues)
    for variableName in ('TradeFilters', 'Portfolios'):
        field = getattr(ael_variables, variableName)
        field.enable(not fieldValues[index], '')
    return fieldValues


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Instrument',
                'Instrument',
                'FInstrument', None, qInstrument,
                0, 0, ttInstrument, cbInstrument, None],
        ['CorporateAction',
                'Corporate Action',
                'FCorporateAction', None, None,
                0, 1, ttPortfolios, cbCorpAction, None],
        ['ScripIssuePerShare',
                'Scrip Issue Per Share',
                'string', None, None,
                1, 0, ttScripIssuePerShare, None, None],
        ['TradeQuantityRounding',
                'Trade Quantity Rounding',
                'string', cvTradeQuantityRounding, None,
                1, 0, ttTradeQuantityRounding, None, None],
        ['Portfolios',
                'Portfolios_Position',
                'FPhysicalPortfolio', None, qPortfolio,
                0, 1, ttPortfolios, None, None],
        ['TradeFilters',
                'Trade Filters_Position',
                'FTradeSelection', None, None,
                0, 1, ttTradeFilters, None, None],
)


def ael_main(execParam):

    import FBDPString
    importlib.reload(FBDPString)
    ScriptName = "Scrip Dividend"
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      execParam['Logmode'],
                      execParam['LogToConsole'],
                      execParam['LogToFile'],
                      execParam['Logfile'],
                      execParam['SendReportByMail'],
                      execParam['MailList'],
                      execParam['ReportMessageType'])

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FScripDivPerform
    importlib.reload(FScripDivPerform)

    execParam['ScriptName'] = 'Scrip Dividend'
    FBDPCommon.execute_script(FScripDivPerform.perform, execParam)
