"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        Statements ATS implementation. The ATS handles the core
                        functionality implemented using business process objects
                        as well as manual user requests through custom text 
                        objects.
                        The ATS subscribes to business process objects with
                        "Party" Subject_type, and custom text objects with 
                        "Statements" SubType.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2019-04-12  CHG1001590405  Libor Svoboda       Enable Swap, Cap & Floor, and 
                                               Structured Deal statements
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
"""
import json
import threading
from collections import defaultdict
from Queue import Queue

import acm

from at_classes import Singleton
from at_logging import getLogger
from statements_config import STATEMENTS, get_bp_config
from statements_params import STATE_CHART
from statements_util import can_user_force, get_first_step


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
YESTERDAY = acm.Time.DateAddDelta(TODAY, 0, 0, -1)
MAX_THREADS = 8
ACTIVE_STATES = (
    'Ready',
    'Pending Calculation',
    'Calculated',
    'Pending Generation',
    'Generated',
    'Hold',
    'Pending Send',
    'Sent',
    'Generate Failed',
)
PROCESS_MULTI_THREAD = (
    # 'Pending Generation',
    # 'Pending Send',
)


class StatementsAts(object, metaclass=Singleton):
    def __init__(self):
        self._bp_queue = defaultdict(Queue)
        self._cto_queue = Queue()
        self._bps = acm.FBusinessProcess.Select(
            'subject_type="Party" and stateChart=%s and updateTime>="%s"'
            % (STATE_CHART.Oid(), YESTERDAY)
        )
        self._text_objects = []
        if not acm.ArchivedMode():
            self._text_objects = acm.FCustomTextObject.Select('subType="Statements"')
        self._init_queue()
        self._subscribe()
        LOGGER.info('ATS init finished.')
    
    @staticmethod
    def is_bp_valid(bp):
        config = get_bp_config(bp)
        if not config:
            LOGGER.info('No statements config found for BP %s.' % bp.Oid())
            return False
        return config.is_bp_valid(bp)
    
    @staticmethod
    def cto_handle_bp_event(bp, event, params, params_state=''):
        acm.BeginTransaction()
        try:
            bp.HandleEvent(event, params)
            bp.Commit()
            if params_state:
                first_step = get_first_step(bp, params_state)
                diary_entry = first_step.DiaryEntry()
                diary_entry.Parameters(params)
                diary = bp.Diary()
                diary.PutEntry(bp, first_step, diary_entry)
                diary.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            LOGGER.exception('CTO: BP %s failed to handle event %s.' 
                             % (bp.Oid(), event))
        else:
            LOGGER.info('CTO: BP %s handled event %s successfully.' 
                        % (bp.Oid(), event))
    
    @staticmethod
    def cto_force_bp_to_state(bp, state, reason=''):
        try:
            bp.ForceToState(state, reason)
            bp.Commit()
        except:
            LOGGER.exception('CTO: BP %s failed to force to %s.' 
                             % (bp.Oid(), state))
        else:
            LOGGER.info('CTO: BP %s successfully forced to %s.' 
                        % (bp.Oid(), state))
    
    def _init_queue(self):
        for bp in self._bps:
            if (acm.Time.DateFromTime(bp.UpdateTime()) == TODAY 
                    and self.is_bp_valid(bp) and not bp.IsInEndState()):
                current_state = str(bp.CurrentStep().State().Name())
                self._bp_queue[current_state].put(bp)
    
    def _subscribe(self):
        self._bps.AddDependent(self)
        if not acm.ArchivedMode():
            self._text_objects.AddDependent(self)
    
    def _process_cto_new_bp(self, data_dict):
        statement_type = str(data_dict['statement'])
        if not statement_type in STATEMENTS:
            LOGGER.info('CTO: Statement type "%s" does not have config.' 
                        % statement_type)
            return
        config = STATEMENTS[statement_type]
        contact = acm.FContact[int(data_dict['contact_id'])]
        if not contact:
            LOGGER.info('CTO: Contact not found')
            return
        val_date = str(data_dict['val_date'])
        party = contact.Party()
        if not config.always_new_bp and config.find_bps(contact, val_date):
            LOGGER.info('CTO: Statement "%s" already exists %s %s.' 
                        % (statement_type, party.Name(), val_date))
            return
        bp_params = {}
        if 'start_date' in data_dict:
            bp_params['start_date'] = str(data_dict['start_date'])
        if 'end_date' in data_dict:
            bp_params['end_date'] = str(data_dict['end_date'])
        try:
            bp = config.create_bp(contact, val_date, **bp_params)
        except:
            LOGGER.exception('CTO: Failed to create BP.')
            return
        LOGGER.info('CTO: Created BP %s.' % bp.Oid())
        event_params = acm.FDictionary()
        event_params['user'] = str(data_dict['user'])
        event_params['event'] = 'New'
        self.cto_handle_bp_event(bp, 'Request Document', event_params, 'Ready')
    
    def _process_cto_event(self, data_dict):
        bp_step = acm.FBusinessProcessStep[int(data_dict['step_id'])]
        if not bp_step:
            LOGGER.info('CTO: BP step not found')
            return
        bp = bp_step.BusinessProcess()
        if not bp.CurrentStep() == bp_step:
            LOGGER.info('CTO: BP step is not the current step.')
            return
        event = str(data_dict['event'])
        if bp.CanHandleEvent(event):
            params = acm.FDictionary()
            params['user'] = str(data_dict['user'])
            params['event'] = event
            self.cto_handle_bp_event(bp, event, params)
            return
        can_force, _ = can_user_force(bp, event)
        if can_force:
            reason = 'Forced to "%s" by %s.' % (event, str(data_dict['user']))
            self.cto_force_bp_to_state(bp, event, reason)
            return
        LOGGER.info('CTO: BP %s cannot handle event or force to state "%s".' 
                    % (bp.Oid(), event))
    
    def _process_cto(self, cto):
        LOGGER.info('CTO: Started processing %s.' % cto.Name())
        try:
            data_dict = json.loads(cto.Text())
        except:
            LOGGER.exception('CTO: Failed to retrieve data %s.' % cto.Name())
            return
        LOGGER.info('CTO: Data %s.' % data_dict)
        event = str(data_dict['event'])
        if event == 'New':
            self._process_cto_new_bp(data_dict)
        else:
            self._process_cto_event(data_dict)
    
    def _process_bp_queue_single(self, bp_queue):
        while not bp_queue.empty():
            bp = bp_queue.get()
            config = get_bp_config(bp)
            if not config:
                LOGGER.info('No statements config found for BP %s.' % bp.Oid())
                continue
            statement_process = config.init_process(bp)
            statement_process.process_states()
    
    def _process_bp_queue_multi(self, bp_queue):
        bp_processes = {}
        statement_process = None
        for _ in range(MAX_THREADS):
            if bp_queue.empty():
                break
            bp = bp_queue.get()
            config = get_bp_config(bp)
            if not config:
                LOGGER.info('No statements config found for BP %s.' % bp.Oid())
                continue
            statement_process = config.init_process(bp)
            if bp.Oid() in bp_processes:
                break
            bp_processes[bp.Oid()] = statement_process
            statement_process = None
        
        threads = []
        for bp_id, process in bp_processes.iteritems():
            t = threading.Thread(target=process.process_states)
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        if statement_process:
            statement_process.process_states()
    
    def remove_all_subscriptions(self):
        self._bps.RemoveDependent(self)
        if not acm.ArchivedMode():
            self._text_objects.RemoveDependent(self)
    
    def process_cto(self):
        while not self._cto_queue.empty():
            cto = self._cto_queue.get()
            self._process_cto(cto)
    
    def process_bps(self):
        for state in ACTIVE_STATES:
            bp_queue = self._bp_queue[state]
            if not bp_queue.empty():
                if state not in PROCESS_MULTI_THREAD:
                    self._process_bp_queue_single(bp_queue)
                    return
                break
        
        if not bp_queue.empty():
            self._process_bp_queue_multi(bp_queue)
    
    def ServerUpdate(self, _sender, operation, entity):
        if (entity.IsKindOf(acm.FBusinessProcess)
                and str(operation) in ('update', 'insert')):
            if not self.is_bp_valid(entity):
                return
            current_state = str(entity.CurrentStep().State().Name())
            self._bp_queue[current_state].put(entity)
        elif (entity.IsKindOf(acm.FCustomTextObject)
                and str(operation) in ('update', 'insert')):
            self._cto_queue.put(entity.Clone())


def start():
    StatementsAts()
    LOGGER.info('ATS Started')


def stop():
    ats = StatementsAts()
    ats.remove_all_subscriptions()
    LOGGER.info('ATS Finished')


def work():
    ats = StatementsAts()
    ats.process_cto()
    ats.process_bps()
