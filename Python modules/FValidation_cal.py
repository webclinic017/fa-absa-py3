"""-----------------------------------------------------------------------------
PURPOSE              :  CAL user-side logic triggered from FValidation
                        * Applicable only to front end (PRIME)
                        * Prompts the user to select amendment reason and type
                          using a pop-up GUI
                        * Stores the selected reason and type in custom text
                          objects or add infos (only for trade insert)
                        * Raises ValidationError if the user does not select
                          anything
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2018-11-13  CHG1001100033  Libor Svoboda       Initial Implementation
2019-02-05  CHG1001325774  Libor Svoboda       Ignore T0 voids
"""
import json
import time
import ael
import acm
import cal_gui
from collections import defaultdict
from FValidation_core import validate_transaction, ValidationError
from cal_config import (UPDATE_THRESHOLD, 
                        PRFNBR_EXCLUDE_FRONTEND,
                        USRGRP_EXCLUDE_FRONTEND,
                        BO_FIELDS_SET,
                        INITIAL_STATUS)
from cal_util import (update_cto,
                      is_trade_valid,
                      is_backdate,
                      booked_today,
                      created_today,
                      set_add_info,
                      get_exclude_users_frontend,
                      has_exponent,
                      is_float)
try:
    from win32gui import GetWindowText, GetForegroundWindow
except ImportError:
    pass


ENTITY_OIDS = {
    'Trade': 'trdnbr',
    'Payment': 'paynbr',
    'Instrument': 'insaddr',
    'Leg': 'legnbr',
    'CashFlow': 'cfwnbr',
    'Reset': 'resnbr',
}
USERID = ael.userid()
LAST_AMEND = {}


def get_current_window():
    try:
        window_name = GetWindowText(GetForegroundWindow())
    except:
        return None
    running_apps = acm.UX().SessionManager().RunningApplications()
    for app in running_apps:
        app_name = str(app)[1:-1]
        if app_name == window_name:
            return app
    return None


def get_amend_reason_and_type(backdate):
    if ('amend_time' in LAST_AMEND
            and (int(LAST_AMEND['amend_time']) + UPDATE_THRESHOLD) > time.time()):
        return LAST_AMEND['amend_reason'], LAST_AMEND['amend_type']
    frame = get_current_window()
    shell = frame.Shell() if frame else acm.UX().SessionManager().Shell()
    values = cal_gui.start_dialog(shell, backdate)
    if not values:
        raise ValidationError('Amendment reason required.')
    try:
        return values['amend_reason'], values['amend_type']
    except:
        raise ValidationError('Amendment reason required.')


def get_trades(entity):
    if entity.record_type == 'Trade':
        return [entity]
    if entity.original():
        entity = entity.original()
    if entity.record_type == 'Instrument':
        return entity.trades()
    elif entity.record_type == 'Leg':
        return entity.insaddr.trades()
    elif entity.record_type == 'CashFlow':
        return entity.legnbr.insaddr.trades()
    elif entity.record_type == 'Reset':
        return entity.cfwnbr.legnbr.insaddr.trades()
    elif entity.record_type == 'Payment':
        return [entity.trdnbr]
    return []


def get_parent(entity):
    if not entity:
        return None
    if entity.record_type == 'Trade':
        return entity
    if entity.record_type == 'Instrument':
        return entity
    if entity.record_type == 'Leg':
        return entity.insaddr
    if entity.record_type == 'CashFlow':
        return get_parent(entity.legnbr)
    if entity.record_type == 'Reset':
        return get_parent(entity.cfwnbr)
    if entity.record_type == 'Payment':
        return entity.trdnbr
    return None


def get_children(entity):
    output = []
    if entity.record_type == 'Trade':
        return list(entity.payments())
    if entity.record_type == 'CashFlow':
        return list(entity.resets())
    if entity.record_type == 'Leg':
        for cashflow in entity.cash_flows():
            output.append(cashflow)
            output.extend(get_children(cashflow))
        return output
    if entity.record_type == 'Instrument':
        for leg in entity.legs():
            output.append(leg)
            output.extend(get_children(leg))
        return output
    return []


class Differences(object):

    ignore = {
        'Trade': ('trdnbr', 'insaddr', 'connected_trdnbr', 'updat_time', 'your_ref', 'updat_usrnbr'),
        'Payment': ('paynbr', 'trdnbr'),
        'Instrument': ('insaddr', 'exp_time'),
        'Leg': ('insaddr', 'legnbr'),
        'CashFlow': ('legnbr', 'cfwnbr'),
        'Reset': ('cfwnbr', 'resnbr', 'legnbr'),
    }
    
    def __init__(self, entity):
        self._entity = entity
        self._differences = {}
        self._inserted_children = []
        self.deleted_children = []
    
    @classmethod
    def get_type_and_id(cls, entities):
        output = []
        for entity in entities:
            record_type = entity.record_type
            entity_id = getattr(entity, ENTITY_OIDS[record_type])
            output.append((record_type, entity_id))
        return output
    
    def _bo_process(self):
        keys = list(self._differences.keys())
        if not (len(keys) == 1 and keys[0] == 'Trade'):
            return False
        trade_diff = self._differences['Trade']
        if ('status' in trade_diff
                and trade_diff['status'] in ['BO Confirmed', 'BO-BO Confirmed']
                and set(trade_diff.keys()) <= BO_FIELDS_SET):
            return True
        return False
    
    def _compare(self, new_entity, old_entity):
        if not new_entity or not old_entity:
            return
        new_pp = new_entity.pp().split('\n')
        old_pp = old_entity.pp().split('\n')
        for old_row, new_row in zip(old_pp, new_pp):
            if old_row == new_row and not has_exponent(new_row):
                continue
            old_row_split = old_row.split(' ')
            new_row_split = new_row.split(' ')
            field_name = new_row_split[0]
            if field_name in self.ignore[new_entity.record_type]:
                continue
            old_value = ' '.join(old_row_split[1:]).lstrip()
            new_value = ' '.join(new_row_split[1:]).lstrip()
            if has_exponent(new_row) and is_float(new_value):
                try:
                    old_value = getattr(old_entity, field_name)
                    new_value = getattr(new_entity, field_name)
                except:
                    pass
            if old_value == new_value:
                continue
            self._differences[new_entity.record_type][field_name] = str(new_value)
    
    def _find_deleted_children(self):
        updated_children = get_children(self._entity)
        orig_entity = self._entity.original()
        orig_children = get_children(orig_entity)
        self.deleted_children = list(set(self.get_type_and_id(orig_children))
                                     - set(self.get_type_and_id(updated_children)))
    
    def _find_inserted_children(self):
        updated_children = get_children(self._entity)
        self._inserted_children = [child for child in updated_children 
                                   if not child.original()]
    
    def _find_differences(self):
        self._differences = defaultdict(lambda: defaultdict(str))
        orig_entity = self._entity.original()
        self._compare(self._entity, orig_entity)
        children = get_children(self._entity)
        for child in children:
            orig_child = child.original()
            self._compare(child, orig_child)
    
    def process(self):
        self._find_differences()
        self._find_inserted_children()
        self._find_deleted_children()
    
    def inserted_children_only(self):
        return (self._inserted_children 
                and not self.deleted_children and not self._differences)
    
    def skip_update(self):
        if (not self._differences 
                and not self._inserted_children and not self.deleted_children):
            return True
        if self._bo_process():
            return True
        return False


class EntityProcessor(object):
    
    def __init__(self, entity, operation):
        self._entity = entity
        self._operation = operation
        self._parent = get_parent(entity)
        self.amendments = []
        self.backdated_inserts = []
        self.backdate = False
    
    @classmethod
    def exclude_portfolio(cls, trade):
        if not trade:
            return True
        if trade.prfnbr and trade.prfnbr.prfnbr in PRFNBR_EXCLUDE_FRONTEND:
            return True
        return False
    
    @classmethod
    def get_update_id(cls, entity):
        if entity.original():
            entity = entity.original()
        entity_id = getattr(entity, ENTITY_OIDS[entity.record_type])
        return 'CAL_%s_%s_%s' % (entity.record_type, entity_id, USERID)
    
    @classmethod
    def get_delete_id(cls, entity):
        entity_id = getattr(entity, ENTITY_OIDS[entity.record_type])
        return 'CAL_%s_%s_Delete' % (entity.record_type, entity_id)
    
    def _is_call_account_amend(self):
        if not self._parent:
            return False
        if not self._parent.record_type == 'Instrument':
            return False
        return (self._parent.instype == 'Deposit' 
                and self._parent.open_end == 'Open End')
    
    def _has_valid_trades(self):
        try:
            trades = get_trades(self._entity)
        except:
            return False
        for trade in trades:
            if is_trade_valid(trade) and not self.exclude_portfolio(trade):
                return True
        return False
    
    def _ignore_instype(self):
        if not self._parent:
            return True
        ins = (self._parent.insaddr 
               if self._parent.record_type == 'Trade' else self._parent)
        if ins.instype == 'SecurityLoan':
            return True
        return False
    
    def _ignore_amendment(self):
        if not self._parent:
            return True
        if (self._parent.record_type == 'Trade' and booked_today(self._parent)
                and self._parent.status in INITIAL_STATUS + ('Void',)):
            return True
        elif (self._parent.record_type == 'Instrument' 
                and created_today(self._parent)):
            return True
        return False
    
    def _process_entity_insert(self):
        if self._entity.record_type not in ('Payment', 'CashFlow'):
            return
        if self._is_call_account_amend():
            return
        if not self._has_valid_trades():
            return
        if not self._parent or not self._parent.creat_time:
            return
        update_id = self.get_update_id(self._parent)
        self.amendments.append(update_id)
    
    def _process_entity_delete(self):
        if not self._has_valid_trades():
            return
        delete_id = self.get_delete_id(self._entity)
        self.amendments.append(delete_id)
        children = get_children(self._entity)
        for child in children:
            delete_id = self.get_delete_id(child)
            self.amendments.append(delete_id)

    def _process_entity_update(self):
        if (not self._entity.record_type == 'Trade' 
                and not self._has_valid_trades()):
            return
        entity_diff = Differences(self._entity)
        entity_diff.process()
        if entity_diff.skip_update():
            return
        if self._is_call_account_amend():
            return
        update_id = self.get_update_id(self._entity)
        self.amendments.append(update_id)
        for child_type, child_id in entity_diff.deleted_children:
            delete_id = 'CAL_%s_%s_Delete' % (child_type, child_id)
            self.amendments.append(delete_id)
    
    def _process_entity(self):
        if self._operation == 'Update':
            self._process_entity_update()
        elif self._operation == 'Delete':
            self._process_entity_delete()
        elif self._operation == 'Insert':
            self._process_entity_insert()
    
    def run(self):
        if self._ignore_instype() or self._ignore_amendment():
            return
        self._process_entity()


class TradeProcessor(EntityProcessor):
    
    def run(self):
        if self._ignore_instype():
            return
        if (self._operation == 'Insert' and is_trade_valid(self._entity) 
                and is_backdate(self._entity) 
                and not self.exclude_portfolio(self._entity)):
            self.backdated_inserts.append(self._entity)
        elif self._operation == 'Update':
            orig_entity = self._entity.original()
            new_valid = is_trade_valid(self._entity)
            old_valid = is_trade_valid(orig_entity)
            if not new_valid and not old_valid:
                return
            if self._ignore_amendment() and orig_entity.status in INITIAL_STATUS:
                return
            if (self.exclude_portfolio(self._entity) 
                    and self.exclude_portfolio(orig_entity)):
                return
            if not old_valid and not is_backdate(self._entity):
                return
            if (new_valid and is_backdate(self._entity) 
                        and (not old_valid or not is_backdate(orig_entity))):
                self.backdate = True
            self._process_entity_update()


class AmendmentExtractor(object):
    
    def __init__(self, transaction_list):
        self._transaction_list = transaction_list
        self.amendments = []
        self.backdated_inserts = []
        self.backdate = False
    
    @classmethod
    def skip_transaction(cls):
        if (ael.user().grpnbr 
                and ael.user().grpnbr.grpnbr in USRGRP_EXCLUDE_FRONTEND):
            return True
        if USERID in get_exclude_users_frontend():
            return True
        return False
    
    def is_backdate(self):
        return bool(self.backdated_inserts) or self.backdate
    
    def run(self):
        if self.skip_transaction():
            return
        for entity, operation in self._transaction_list:
            entity_process = None
            if entity.record_type == 'Trade':
                entity_process = TradeProcessor(entity, operation)
            elif entity.record_type in ('Instrument', 'Leg', 'CashFlow',
                                        'Reset', 'Payment'):
                entity_process = EntityProcessor(entity, operation)
            if not entity_process:
                continue
            entity_process.run()
            self.amendments.extend(entity_process.amendments)
            self.backdated_inserts.extend(entity_process.backdated_inserts)
            self.backdate = self.backdate or entity_process.backdate
        self.amendments = list(set(self.amendments))


@validate_transaction
def add_amend_reason(transaction_list):
    if not str(acm.Class()) == 'FTmServer':
        return transaction_list
    amend_extractor = AmendmentExtractor(transaction_list)
    amend_extractor.run()
    amendments = amend_extractor.amendments
    backdated_inserts = amend_extractor.backdated_inserts
    if not amendments and not backdated_inserts:
        return transaction_list
    backdate = amend_extractor.is_backdate()
    amend_reason, amend_type = get_amend_reason_and_type(backdate)
    for trade in backdated_inserts:
        set_add_info(trade, 'AmendReasonTrd', amend_reason)
        set_add_info(trade, 'AmendReasonTypeTrd', amend_type)
    amend_dict = {
        'amend_reason': amend_reason, 
        'amend_type': amend_type,
        'amend_time': str(int(time.time())),
    }
    LAST_AMEND.update(amend_dict)
    amend_dict_json = json.dumps(amend_dict)
    for amend_id in amendments:
        transaction_tuple = update_cto(amend_id, amend_dict_json)
        transaction_list.append(transaction_tuple)
    return transaction_list

