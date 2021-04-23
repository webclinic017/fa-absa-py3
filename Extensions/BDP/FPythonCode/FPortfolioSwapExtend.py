""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FPortfolioSwapExtend.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPortfolioSwapExtend - Script for performing PortfolioSwap extend

----------------------------------------------------------------------------"""

#Import Front modules

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import acm


# Tool Tip
ttPortfolioSwap = 'Select the PortfolioSwap to extend'
ttSweepCash = 'Sweep Cash after performing the extend'

q = FBDPGui.insertPortfolioSwap()

ael_variables = FBDPGui.TestVariables(
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
    ['Date',
            'Date',
            'string', [acm.Time.DateToday(), 'Today'],
            'Today', 1, 0],
    ['PortfolioSwaps',
            'Portfolio Swaps',
            'FPortfolioSwap', None, q,
            1, 1, ttPortfolioSwap],
    ['SweepCash',
            'Sweep Cash',
            'int', [1, 0], 1,
            0, 0, ttSweepCash],
)

def ael_main(dictionary):

    import FPortfolioSwapPerform
    importlib.reload(FPortfolioSwapPerform)
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)

    ScriptName = 'PortfolioSwap Extend'
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPCommon.execute_script(FPortfolioSwapPerform.Extend, dictionary)
    FBDPCurrentContext.Logme()('FINISH')
