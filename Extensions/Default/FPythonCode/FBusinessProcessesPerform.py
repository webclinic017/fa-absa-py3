""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_processes/etc/FBusinessProcessesPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FBusinessProcessPerform - Business processes perform base implementation

DESCRIPTION


ENDDESCRIPTION
---------------------------------------------------------------------------"""

import acm
import ael

import FBDPCommon
from FBDPCurrentContext import Logme, Summary

def perform(params, performer):
    try:
        _perform(params, performer)
    finally:
        _cleanParams(params)
        Summary().log(params)
        Logme()(None, 'FINISH')

def _perform(params, performer):
    name = params['ScriptName']
    date = _getAelDate(FBDPCommon.toDate(params['Date']), name)
    other_params = params['other_params']
    states = params['States']
    assert states, 'No states chosen for state chart'

    # baseParams are the parameters required by BusinessProcessesPerform
    baseParams = {
        'date': date,
        'name': name,
        'state_oids': [str(state.Oid()) for state in states],
        'src_archive_status': other_params['src_archive_status'],
        'task': other_params['task'].capitalize(),
        'action': other_params['action'],
    }
    # remove the other params no longer needed so that other_params
    # only consists of the parameters required by the sub-class
    for param in ('src_archive_status', 'task', 'action'):
        del other_params[param]

    # execute perform
    executor = performer(bool(params['Testmode']), baseParams, other_params)
    executor.perform()

def _cleanParams(params):
    # cleanup params entries and remove those unnecessary for logging
    params['States'] = [s.Name() for s in params['States']]
    del params['other_params']
    return

def _getAelDate(acm_date, name):
    if not acm_date or acm_date == '':
        raise Exception('Invalid date: %s' % (acm_date or None))

    ael_date = ael.date(acm_date).to_time()
    if ael_date > ael.date_today():
        raise Exception('Date cannot be in the future: %s' % acm_date)

    Logme()('%s date: %s' % (name, str(acm_date)))
    return ael_date

class BusinessProcessesPerform(object):
    # constructor
    def __init__(self, testmode, baseParams, otherParams):
        # public
        self.testmode = testmode
        self.other_params = otherParams

        # private
        self._date = baseParams['date']
        self._state_oids = baseParams['state_oids']
        self._src_archive_status = baseParams['src_archive_status']
        self._task = baseParams['task']
        self._action = baseParams['action']
        self._bp_to_steps = {}

    # public
    def perform(self):
        acm.PollDbEvents()
        name = 'Business processes'
        Logme()('%s %s' % (self._task, name), 'INFO')
        bps = self._getBusinessProcesses()
        finished_msg = None
        if bps:
            self.processBusinessProcesses(bps)
            finished_msg = 'Finished %s all %s' % (self._task.lower(), name)
        else:
            finished_msg = 'Finished %s %s: No business processes found' % (
                self._task.lower(), name
            )

        Logme()(finished_msg, 'INFO')
        return

    def getAelName(self, obj):
        return '%s %s' % (obj.record_type, obj.display_id())

    def logProcessed(self, obj):
        if not isinstance(obj, list):
            Summary().ok(obj, Summary().PROCESS)
        elif len(obj):
            Summary().ok(obj[0], Summary().PROCESS, None, len(obj))

    def logActionStarted(self, name, indentation):
        Logme()('%s%s %s' % (indentation, self._task, name), 'DEBUG')

    def logActionFinished(self, obj, name, indentation):
        Summary().ok(obj, self._action, name)
        Logme()('%sFinished %s %s' % (
            indentation, self._task.lower(), name), 'DEBUG'
        )

    def logActionFailed(self, obj, reason):
        Summary().fail(obj, self._task.lower(), obj.seqnbr, reason)

    # for overriding
    def processBusinessProcesses(self, bps):
        """
        The method used to actually perform the task on the business process
        """
        for bp in bps:
            self.processBusinessProcess(bp)

    # private
    def processBusinessProcess(self, bp):
        name = self.getAelName(bp)
        indentation = '  '
        self.logActionStarted(name, indentation)
        try:
            diary = bp.diary_seqnbr
            self.procesBusinessProcessDiary(diary)
            self.processObj(bp)
            for step in self._bp_to_steps[bp]:
                self.processBusinessProcessStep(step)
            self.logActionFinished(bp, name, indentation)
        except Exception as e:
            self.logActionFailed(bp, str(e))

    def procesBusinessProcessDiary(self, diary):
        self.logProcessed(diary)
        name = self.getAelName(diary)
        indentation = '    '
        self.logActionStarted(name, indentation)
        try:
            self.processObj(diary)
            self.logActionFinished(diary, name, indentation)
        except Exception as e:
            self.logActionFailed(diary, str(e))

    def processBusinessProcessStep(self, step):
        self.logProcessed(step)
        name = self.getAelName(step)
        indentation = '    '
        self.logActionStarted(name, indentation)
        try:
            self.processObj(step)
            self.logActionFinished(step, name, indentation)
        except Exception as e:
            self.logActionFailed(step, str(e))

    def getExtraSqlConditions(self):
        """
        The method used to append SQL command with extra select conditions
        """
        pass

    def processObj(self, obj):
        """
        Performs actual transformation on entity
        """

    def _getBusinessProcessSteps(self, bp):

        query = (
            'SELECT DISTINCT bps.seqnbr'
            ' FROM'
            ' business_process AS bp,'
            ' business_process_step AS bps'
            ' WHERE ('
            ' (bps.business_process_seqnbr = %s)'
            ')'
        ) % (bp.seqnbr)

        bpslist = sorted([
            bps for bps in FBDPCommon.FBDPQuerySelection(
                name='Business Process Steps',
                query_expr=query,
                result_types=[ael.BusinessProcessStep]
            ).Run()
        ], key=lambda bps: bps.seqnbr)
        return bpslist

    def _shouldIncludeBP(self, bp):
        steps = self._getBusinessProcessSteps(bp)
        for step in steps:
            if step.creat_time >= self._date:
                return False
        self._bp_to_steps[bp] = steps
        return True

   # private
    def _getBusinessProcesses(self):
        extra_conditions = self.getExtraSqlConditions() or ''
        if len(extra_conditions):
            extra_conditions = ' AND (%s) ' % ', '.join(extra_conditions)

        query = (
            'SELECT DISTINCT bp.seqnbr'
            ' FROM'
            ' business_process AS bp,'
            ' business_process_step AS bps,'
            ' state_chart_state AS scs'
            ' WHERE ('
            '(bp.archive_status = %s)'
            ' AND (bp.seqnbr = bps.business_process_seqnbr)'
            ' AND (bps.state_name = scs.name)'
            ' AND (scs.seqnbr in (%s))'
            '%s'
            ')'
        ) % (
            self._src_archive_status,
            ', '.join(self._state_oids),
            extra_conditions
        )
        bps = sorted([
            bp for bp in FBDPCommon.FBDPQuerySelection(
                name='Business Processes',
                query_expr=query,
                result_types=[ael.BusinessProcess]
            ).Run() if self._shouldIncludeBP(bp)
        ], key=lambda bp: bp.seqnbr)
        self.logProcessed(bps)
        return bps
