""" Compiled: 2017-07-12 14:02:19 """

#__src_file__ = "extensions/ps_processing/etc/FPortfolioSwapProcessing.py"
"""----------------------------------------------------------------------------
    (c) Copyright 2017 SunGard Front Arena. All rights reserved.
----------------------------------------------------------------------------"""
"""----------------------------------------------------------------------------
MODULE
    FPortfolioSwapProcessing - GUI for performing various PS tasks

DESCRIPTION

NOTE
    Running this script required the loading of the of following modules:
        - Deal Package
        - Synthetic Prime Templates
        - Synthetic Prime
ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)

class Param:
    ASSIGN = 'Task_TradeAssign'
    FIX = 'Task_Fix'
    EXTEND = 'Task_Extend'
    SWEEP = 'Task_SweepCash'
    REGENERATE = 'Task_RegenerateLegs'
    REGENERATE_STARTDATE = 'Task_RegenerateLegs_StartDate'
    REGENERATE_ENDDATE = 'Task_RegenerateLegs_EndDate'
    TERMINATE = 'Task_Terminate'
    ROLL = 'Task_Roll'
    ROLL_NAME = 'Task_Roll_NewName'

pswaps = []

ScriptName = 'FPortfolioSwapProcessing'

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters(
    'FBDPParameters', ScriptName
)

acm_dates = [acm.Time.DateToday(), 'Today']

# Tool Tip
ttDate = 'Date. By default this will be today.'
ttPortfolioSwap = 'Select portfolio swap(s) on which to perform tasks.'
ttAssign = (
    'Perform trade assignment. Select if any new securities have recently '
    'been added to reference portfolio(s).'
)
ttFix = 'Fix unfixed resets with fixing date before or up to today\'s date.'
ttExtend = (
    'Extend cash flows by one business day '
    '(or create new cash flows if a rolling period is passed).'
)
ttSweep = (
    'Transfer cash from the different portfolio swap components into '
    'the synthetic cash account.'
)
ttRegenerate = (
    'Regenerate legs of portfolio swap(s). Select if there have recently '
    'been historical amendments to trades in reference portfolio(s).'
)
ttStartDate = (
    'Choose the start date for the regeneration. By default this will '
    'be the earliest start date of all the chosen portfolio swap(s).'
)
ttEndDate = (
    'The end date for the regeneration. '
    'Value is taken from the date specified in the General tab.'
)
ttTerminate = (
    'Terminate portfolio swap(s). By doing this any selected portfolio swaps '
    'will be excluded from all future maintenance scripts. '
    '(Only possible for portfolio swaps that have closed out all positions.'
)
ttRoll = (
    'Terminate a portfolio swap(s) regardless of where it has any open ',
    'position, and create a new one given a name ',
    'and date (used as expiry date).'
)
ttNewName = 'Name of portfolio swap to be created.'
ttDisableNewName = (
    'Check \'Roll swap\' with a single portfolio swap selection to enable.'
)

default_portfolio_swaps = FBDPGui.insertPortfolioSwap()

def setDateMandatory(value):
    getattr(ael_variables, 'Date')[5] = value

def disableVariables(variables, enable=False, disabledTooltip=None):
    for i in variables:
        getattr(ael_variables, i).enable(enable, disabledTooltip)

def getStartDate(portfolio_swaps):
    start_date = acm.Time.DateToday()
    for ps in portfolio_swaps:
        ps_start_date = ps.StartDate()
        if ps_start_date < start_date:
            start_date = ps_start_date

    return start_date

def dateCb(index, field_values):
    if getattr(ael_variables, Param.REGENERATE_STARTDATE).isEnabled():
        ed = getattr(ael_variables, Param.REGENERATE_ENDDATE)
        field_values[ed.sequenceNumber] = field_values[index]

    return field_values

def swapsCb(index, field_values):
    ps_ids = field_values[index]
    del pswaps[:]
    for ps_id in ps_ids.split(','):
        ps_id = ps_id.strip()
        if len(ps_id):
            pswaps.append(acm.FPortfolioSwap[ps_id])

    index = getattr(ael_variables, Param.ROLL_NAME).sequenceNumber
    field_values = rollCb(index, field_values)
    index = getattr(ael_variables, Param.REGENERATE).sequenceNumber
    field_values = regenerateCb(index, field_values)
    return field_values

def regenerateCb(index, field_values):
    do_perform = field_values[index] == '1'
    disableVariables(
        (Param.REGENERATE_STARTDATE,),
        do_perform, 'Check \'Regenerate legs\' to enable'
    )
    sd_var = getattr(ael_variables, Param.REGENERATE_STARTDATE)
    sd_var[5] = int(do_perform)
    sd_idx = sd_var.sequenceNumber

    ed_var = getattr(ael_variables, Param.REGENERATE_ENDDATE)
    ed_var[5] = int(do_perform)
    ed_idx = ed_var.sequenceNumber

    if do_perform:
        date_idx = getattr(ael_variables, 'Date').sequenceNumber
        if field_values[sd_idx] not in ('Inception', '-3', '-1', 'Today'):
            field_values[sd_idx] = getStartDate(pswaps)
        field_values[ed_idx] = field_values[date_idx]
    else:
        field_values[sd_idx] = None
        field_values[ed_idx] = None

    return field_values

def terminateCb(index, field_values):
    do_perform = field_values[index] == '1'
    setDateMandatory(do_perform)

def rollCb(index, field_values):
    do_perform = field_values[index] == '1'
    enable_name = do_perform and (len(pswaps) <= 1)
    disableVariables((Param.ROLL_NAME,), enable_name, ttDisableNewName)
    getattr(ael_variables, Param.ROLL_NAME)[5] = int(enable_name)
    if not enable_name:
        rn_var = getattr(ael_variables, Param.ROLL_NAME).sequenceNumber
        field_values[rn_var] = ''

    return field_values

global ael_variables
ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Date',
                'Date',
                'string', acm_dates, 'Today',
                1, False, ttDate, dateCb],
        ['PortfolioSwaps',
                'Portfolio Swaps',
                'FPortfolioSwap', None, default_portfolio_swaps,
                1, True, ttPortfolioSwap, swapsCb],
        [Param.ASSIGN,
                'Trade assignment',
                'int', [0, 1], 0,
                1, False, ttAssign, None],
        [Param.FIX,
                'Fix resets',
                'int', [0, 1], 0,
                1, False, ttFix, None],
        [Param.EXTEND,
                'Extend',
                'int', [0, 1], 0,
                1, False, ttExtend, None],
        [Param.SWEEP,
                'Sweep cash',
                'int', [0, 1], 0,
                1, False, ttSweep, None],
        [Param.REGENERATE,
                'Regenerate legs',
                'int', [0, 1], 0,
                1, False, ttRegenerate, regenerateCb],
        [Param.REGENERATE_STARTDATE,
                'Start date_Regenerate',
                'string', ['Today', 'Inception'], None,
                0, False, ttStartDate, None, False],
        [Param.REGENERATE_ENDDATE,
                'End date_Regenerate',
                'string', acm_dates, None,
                0, False, ttEndDate, None, False],
        [Param.TERMINATE,
                'Terminate',
                'int', [0, 1], 0,
                1, False, ttTerminate, terminateCb],
        [Param.ROLL,
                'Roll swap',
                'int', [0, 1], 0,
                1, False, ttRoll, rollCb],
        [Param.ROLL_NAME,
                'New name_Roll',
                'string', None, None,
                0, False, ttNewName, None, False],
)

def ael_main(params):
    #Import Front modules
    import FPortfolioSwapProcessingPerform as perform
    importlib.reload(perform)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPCurrentContext

    FBDPCurrentContext.CreateLog(
        ScriptName,
        params['Logmode'],
        params['LogToConsole'],
        params['LogToFile'],
        params['Logfile'],
        params['SendReportByMail'],
        params['MailList'],
        params['ReportMessageType']
    )

    params_to_actions_map = {}
    for action in perform.Action.ORDERED_ACTIONS:
        param = getattr(Param, action.upper(), None)
        if param is not None:
            params_to_actions_map[param] = action

    actions = []
    for k, v in params.items():
        action = params_to_actions_map.get(k)
        if action and (v is not None) and bool(v):
            actions.append(action)

    params['actions'] = actions
    FBDPCommon.execute_script(perform.perform, params)
