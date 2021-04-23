""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FPortfolioSwapRegenerate.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPortfolioSwapRegenerate - Script for regenerating portfolio swaps

----------------------------------------------------------------------------"""

#Import Front modules

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FPortfolioSwapProcessing
importlib.reload(FPortfolioSwapProcessing)
import acm


# Tool Tips
ttPortfolioSwap = 'Select the Portfolio Swap to regenerate'
ttStartDate = (
    'Choose the start date for the regeneration. By default this will '
    'be the earliest start date of the chosen portfolio swaps.'
)
ttEndDate = (
    'Select the end date for the regeneration. By default this will be today.'
)

q = FBDPGui.insertPortfolioSwap()

def swapsCb(index, field_values):
    ps_ids = field_values[index]
    pswaps = []
    for ps_id in ps_ids.split(','):
        ps_id = ps_id.strip()
        if len(ps_id):
            pswaps.append(acm.FPortfolioSwap[ps_id])

    field_values = setDates(field_values, pswaps)
    return field_values

def setDates(field_values, pswaps):
    # get earliest start date
    sd_idx = getattr(ael_variables, 'StartDate').sequenceNumber
    disable_variables(
        ('StartDate', 'EndDate'), bool(len(pswaps)), ttPortfolioSwap
    )
    if len(pswaps):
        start_date = FPortfolioSwapProcessing.getStartDate(pswaps)
        field_values[sd_idx] = start_date
    else:
        field_values[sd_idx] = None

    return field_values

def disable_variables(variables, enable=0, disabledTooltip=None):
    for i in variables:
        getattr(ael_variables, i).enable(enable, disabledTooltip)

ael_variables = FBDPGui.TestVariables(
    # [VariableName,
    #       DisplayName,
    #       Type, CandidateValues, Default,
    #       Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
    ['PortfolioSwaps',
            'Portfolio Swaps',
            'FPortfolioSwap', None, q,
            1, 1, ttPortfolioSwap, swapsCb],
    ['StartDate',
            'Start Date',
            'string', ['Today'], 'Today',
            0, 0, ttStartDate, None],
    ['EndDate',
            'End Date',
            'string', [acm.Time.DateToday(), 'Today'], 'Today',
            0, 0, ttEndDate],
    )

def ael_main(dictionary):

    import FPortfolioSwapPerform
    importlib.reload(FPortfolioSwapPerform)
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)

    ScriptName = 'PortfolioSwap Regenerate'
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPCommon.execute_script(FPortfolioSwapPerform.Regenerate, dictionary)
    FBDPCurrentContext.Logme()('FINISH')
