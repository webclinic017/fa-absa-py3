""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FPortfolioSwapFixing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPortfolioSwapFixing - Script for performing PortfolioSwap fixing

----------------------------------------------------------------------------"""

#Import Front modules

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import acm


# Tool Tip
ttPortfolioSwap = 'Select the PortfolioSwap to fix'

q = FBDPGui.insertPortfolioSwap()

ael_variables = FBDPGui.TestVariables(
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
    ['Date',
            'Date',
            'string', [acm.Time.DateToday(), 'Today'], 'Today',
            1, 0],
    ['PortfolioSwaps',
            'Portfolio Swaps',
            'FPortfolioSwap', None, q,
            1, 1, ttPortfolioSwap],
)

def ael_main(dictionary):

    import FPortfolioSwapPerform
    importlib.reload(FPortfolioSwapPerform)
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)

    ScriptName = 'PortfolioSwap Fixing'
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPCommon.execute_script(FPortfolioSwapPerform.Fix, dictionary)
    FBDPCurrentContext.Logme()('FINISH')
