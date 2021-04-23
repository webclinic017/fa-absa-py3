""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ps_processing/etc/FPortfolioSwapProcessingPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPortfolioSwapProcessingPerform - Module which executes various PS tasks

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import collections

import acm
import FBDPCommon
from FBDPCurrentContext import Logme, Summary
import importlib

_LOG_DICT = {
    'log': None,
    'summary': None,
    'log_attrs': {},
    'summary_attrs': {},
}
_BUSINESS_PROCESS_MODULE_NAME = 'Portfolio Swap Maintenance'

def _log(msg, target):
    # required to reset logger attributes after GetAttribute call
    log = _LOG_DICT['log']
    log_attrs = _LOG_DICT['log_attrs']
    log.__dict__.update(log_attrs)
    log(msg, target)
    log_attrs.update(log.__dict__.copy())
    return

def _getSummary():
    # required to reset summariser attributes after GetAttribute call
    summary = _LOG_DICT['summary']
    summary_attrs = _LOG_DICT['summary_attrs']
    summary.__dict__.update(summary_attrs)
    return summary, summary_attrs

def _getSummaryConstant(name):
    # required to reset summariser attributes after GetAttribute call
    summary, summary_attrs = _getSummary()
    return getattr(summary, name)

def _summaryLog(params):
    # required to reset summariser attributes after GetAttribute call
    summary, summary_attrs = _getSummary()
    summary.log(params)
    summary_attrs.update(summary.__dict__.copy())
    return

def _summaryOk(obj, action, name):
    # required to reset summariser attributes after GetAttribute call
    summary, summary_attrs = _getSummary()
    summary.ok(obj, action, name)
    summary_attrs.update(summary.__dict__.copy())
    return

def _summaryFail(obj, action, name, msg):
    # required to reset summariser attributes after GetAttribute call
    summary, summary_attrs = _getSummary()
    summary.fail(obj, action, name, msg)
    summary_attrs.update(summary.__dict__.copy())
    return

class Action:
    ASSIGN = 'assign'
    FIX = 'fix'
    EXTEND = 'extend'
    SWEEP = 'sweep'
    REGENERATE = 'regenerate'
    TERMINATE = 'terminate'
    ROLL = 'roll'

    ORDERED_ACTIONS = (ASSIGN, FIX, EXTEND, SWEEP, REGENERATE, TERMINATE, ROLL)

    @staticmethod
    def getSorted(actions, key=None):
        actions = set(actions)
        sorted_actions = []
        for ordered_action in Action.ORDERED_ACTIONS:
            for action in actions:
                action_id = key(action) if key else action.action_id
                if action_id == ordered_action:
                    sorted_actions.append(action)

        return sorted_actions

def perform(params):
    to_remove = params.setdefault('to_remove', [])
    to_remove.append('actions')
    to_remove.append('to_remove')

    if not any(params['actions']):
        raise Exception('No tasks specified')

    use_bp = bool(acm.FExtensionModule[_BUSINESS_PROCESS_MODULE_NAME])
    if 'run_as_normal' in params:
        use_bp = False
        to_remove.append('run_as_normal')

    try:
        log = Logme()
        summary = Summary()
        _LOG_DICT['log'] = log
        _LOG_DICT['summary'] = summary
        _LOG_DICT['log_attrs'] = log.__dict__.copy()
        _LOG_DICT['summary_attrs'] = summary.__dict__.copy()
        if use_bp:
            _runPerformAsBusinessProcess(params)
        else:
            _runPerformAsNormal(params)
    finally:
        for param in set(to_remove):
            del params[param]

        _summaryLog(params)
        _log(None, 'FINISH')

def _runPerformAsBusinessProcess(params):
    FBDPCommon.reloadModule(_BUSINESS_PROCESS_MODULE_NAME)
    import PSBusinessProcessesFactory
    importlib.reload(PSBusinessProcessesFactory)

    actions_to_perform = Action.getSorted(params['actions'])
    params_copy = {}
    for k, v in params.items():
        if k != 'actions':
            params_copy[k] = v

    params_copy['run_as_normal'] = True
    subjects = params_copy['PortfolioSwaps']
    bps = PSBusinessProcessesFactory.MakeBusinessProcesses(subjects)
    for action in actions_to_perform:
        bps.PerformTransition(action, params_copy)

def _runPerformAsNormal(params):
    from FPortfolioSwapProcessing import Param

    _Action = collections.namedtuple(
        'Action', 'action_id, func name summary_type'
    )

    actions_to_perform = params['actions']
    date = _getDate(params.get('Date'), actions_to_perform)
    testmode = bool(params['Testmode'])
    pswaps = params['PortfolioSwaps']
    if not (pswaps and len(pswaps)):
        raise Exception('No portfolio swaps selected')

    actions = []
    for action in actions_to_perform:
        if action == Action.ASSIGN:
            actions.append(_Action(
                action_id=Action.ASSIGN,
                func=lambda ps: ps.GetAttribute('tradeAssign')(date),
                name='trade assignment',
                summary_type=_getSummaryConstant('ASSIGN')
            ))
        elif action == Action.FIX:
            actions.append(_Action(
                action_id=Action.FIX,
                func=lambda ps: ps.GetAttribute('fixPortfolioSwap')(date),
                name='fix',
                summary_type='fixed'
            ))
        elif action == Action.EXTEND:
            actions.append(_Action(
                action_id=Action.EXTEND,
                func=lambda ps: ps.GetAttribute('extendPortfolioSwap')(date),
                name='extension',
                summary_type='extended'
            ))
        elif action == Action.SWEEP:
            actions.append(_Action(
                action_id=Action.SWEEP,
                func=lambda ps: ps.GetAttribute('sweepCash')(date),
                name='cash sweep',
                summary_type=_getSummaryConstant('SWEEP')
            ))
        elif action == Action.REGENERATE:
            sDate = _getDate(params.get(Param.REGENERATE_STARTDATE), [])
            eDate = _getDate(params.get(Param.REGENERATE_ENDDATE), [])
            assert eDate == date
            actions.append(_Action(
                action_id=Action.REGENERATE,
                func=lambda ps: ps.GetAttribute('regenerateAll')(sDate, eDate),
                name='regeneration',
                summary_type='regenerated'
            ))
        elif action == Action.TERMINATE:
            actions.append(_Action(
                action_id=Action.TERMINATE,
                func=lambda ps: ps.GetAttribute('terminate')(),
                name='termination',
                summary_type='terminated'
            ))
        elif action == Action.ROLL:
            name = params[Param.ROLL_NAME]
            actions.append(_Action(
                action_id=Action.ROLL,
                func=lambda ps: ps.GetAttribute('roll')(date, name),
                name='roll',
                summary_type=_getSummaryConstant('ROLL')
            ))

    actions = Action.getSorted(actions, key=lambda x: x.action_id)
    _execPerform(pswaps, date, testmode, actions)

def _getDate(date, actions):
    if (not (date and len(date))) and actions != ['terminate']:
        raise Exception('Invalid date: %s' % (date or None))

    return FBDPCommon.toDate(date)

def _execPerform(pswaps, date, testmode, actions):
    acm.PollDbEvents()
    proccess_summary_constant = _getSummaryConstant('PROCESS')
    for ps in pswaps:
        name = 'PortfolioSwap \'%s\'' % ps.Name()
        ps_dp = _getDealPackageFromPortfolioSwap(ps)
        try:
            _summaryOk(ps_dp, proccess_summary_constant, name)
            ps_dp = ps_dp.Edit()
            for idx, action in enumerate(actions):
                d = None if action.action_id == Action.TERMINATE else date
                try:
                    _logStarted(name, action, d)
                    action.func(ps_dp)
                    if not testmode:
                        ps_dp.Save()

                    _logFinished(name, action, d, ps_dp)
                except Exception as error:
                    _logFailed(str(error), name, action, action, d, ps_dp)
                    root_action = action
                    for action in actions[idx + 1:]:
                        error = '%s failed due to previous failure' % (
                            action.name
                        )
                        _logFailed(error, name, root_action, action, d, ps_dp)

                    break
        except Exception as error:
            msg = 'inspection: %s' % str(error)
            _log('Failed %s %s' % (name, msg), 'INFO')
            _summaryFail(
                ps_dp, proccess_summary_constant,
                ps_dp.Oid(), '%s %s' % (ps.Name(), msg)
            )

    return

def _getDealPackageFromPortfolioSwap(pswap):
    ins_links = pswap.DealPackageInstrumentLinks()
    ins_pkgs = [link.InstrumentPackage() for link in ins_links]
    if len(ins_pkgs) != 1:
        msg = (
            'Got unexpected number of instrument packages: %i instead of 1' % (
                len(ins_pkgs)
            )
        )
        raise Exception(msg)

    ins_pkg = ins_pkgs[0]
    def_name = ins_pkg.DefinitionName()
    if def_name != 'PortfolioSwap':
        msg = (
            'Portfolio swap instrument package has '
            'incorrect definition: %s'
        ) % def_name
        raise Exception(msg)

    dps = ins_pkg.DealPackages()
    if len(dps) != 1:
        msg = (
            'Expected one-to-one mapping of portfolio swap '
            'instrument package to portfolio swap deal package'
        )
        raise Exception(msg)

    return dps[0]

def _logStarted(name, action, date):
    msg = 'Starting %s %s' % (name, action.name)
    if date:
        msg = '%s on date %s' % (msg, str(date))

    _log(msg, 'DEBUG')

def _logFinished(name, action, date, ps):
    msg = 'Successfully performed %s %s' % (name, action.name)
    if date:
        msg = '%s on date %s' % (msg, str(date))

    _log(msg, 'INFO')
    _summaryOk(ps, action.summary_type, name)

def _logFailed(error_msg, name, root_action, failed_action, date, ps):
    msg = '%s when performing %s %s' % (error_msg, name, root_action.name)
    if date:
        msg = '%s on date %s' % (msg, str(date))

    _log('%s error, skipping.' % failed_action.name, 'DEBUG')
    _summaryFail(ps, failed_action.summary_type, ps.display_id(), msg)
