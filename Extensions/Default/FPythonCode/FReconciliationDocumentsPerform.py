""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/reconciliation_documents/etc/FReconciliationDocumentsPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FReconciliationDocumentsPerform -
        Reconciliation documents perform base implementation

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
    docs = params['Documents']
    assert docs, 'No valid reconciliation documents chosen'

    # baseParams are the parameters required by ReconciliationDocumentsPerform
    baseParams = {
        'date': date,
        'name': name,
        'docs': docs,
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
    docs = params['Documents']
    params['Documents'] = [_getRecDocName(ael_doc=doc) for doc in docs]
    del params['other_params']
    return

def _getAelDate(acm_date, name):
    if not acm_date or acm_date == '':
        raise Exception('Invalid date: %s' % (acm_date or None))

    ael_date = ael.date(acm_date).to_time()
    if ael_date > ael.date_today():
        raise Exception('Date cannot be in the future: %s' % acm_date)

    if name:
        Logme()('%s date: %s' % (name, str(acm_date)))

    return ael_date

def _getRecDocName(ael_doc):
    return '%s(%d)' % (ael_doc.reconciliation_name, ael_doc.seqnbr)

class ReconciliationDocumentsPerform(object):
    # constructor
    def __init__(self, testmode, baseParams, otherParams):
        # public
        self.testmode = testmode
        self.other_params = otherParams

        # private
        self._date = baseParams['date']
        self._docs = baseParams['docs']
        self._src_archive_status = baseParams['src_archive_status']
        self._task = baseParams['task']
        self._action = baseParams['action']

    # public
    def perform(self):
        acm.PollDbEvents()
        name = 'Reconciliation documents'
        Logme()('%s %s' % (self._task, name), 'INFO')
        finished_msg = None
        if self._docs:
            self.logProcessed()
            for doc in self._docs:
                self.process(obj=doc, indentation='')

            finished_msg = 'Finished %s all %s' % (self._task.lower(), name)
        else:
            finished_msg = (
                'Finished %s %s: No reconciliation documents found' % (
                    self._task.lower(), name
                )
            )

        Logme()(finished_msg, 'INFO')
        return

    # for overriding
    def processObj(self, obj):
        """
        Performs actual transformation on entity
        """

    # private
    def logProcessed(self):
        log = lambda obj: Summary().ok(obj, Summary().PROCESS)
        for doc in self._docs:
            log(obj=doc)
            for ri in doc.reference_in():
                if ri.record_type == 'ReconciliationItem':
                    log(obj=ri)

        return

    def getAelName(self, obj):
        return '%s %s' % (obj.record_type, obj.display_id())

    def logActionStarted(self, name, indentation):
        Logme()('%s%s %s' % (indentation, self._task, name), 'DEBUG')

    def logActionFinished(self, obj, name, indentation, ignored):
        prefix = 'Skipped' if ignored else 'Finished'
        if not ignored:
            Summary().ok(obj, self._action, name)

        Logme()('%s%s %s %s' % (
            indentation, prefix, self._task.lower(), name), 'DEBUG'
        )
        return

    def logActionFailed(self, obj, reason):
        Summary().fail(obj, self._task.lower(), obj.seqnbr, reason)

    def process(self, obj, indentation):
        def ignore(obj):
            if obj.archive_status != self._src_archive_status:
                oid = obj.seqnbr
                reason = 'Invalid archive status: %s not %s' % (
                    obj.archive_status, self._src_archive_status
                )
                Summary().ignore(obj, Summary().PROCESS, reason, oid)
                return True

            return False

        name = self.getAelName(obj)
        self.logActionStarted(name, indentation)
        try:
            if obj.record_type == 'ReconciliationDocument':
                for ri in obj.reference_in():
                    if ri.record_type == 'ReconciliationItem':
                        self.process(obj=ri, indentation='  ')

            if ignore(obj=obj):
                self.logActionFinished(obj, name, indentation, True)
            else:
                self.processObj(obj=obj)
                self.logActionFinished(obj, name, indentation, False)
        except Exception as e:
            self.logActionFailed(obj, str(e))

        return
