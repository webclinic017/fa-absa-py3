"""-----------------------------------------------------------------------------
PURPOSE              :  Classes and functions used in cal_ats and 
                        FValidation_cal.
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2018-11-13  CHG1001100033  Libor Svoboda       Initial Implementation
2018-11-27  CHG1001134332  Libor Svoboda       Enable work task (add parameters)
2019-02-05  CHG1001325774  Libor Svoboda       Improve BO process identification
2020-11-26  CHG0141021     Bhavnisha Sarawan   Include other types in is_fair_value
"""
import os
import json
import time
import xml.etree.ElementTree as ET
import acm
import ael
from collections import defaultdict
from at_logging import getLogger
from cal_config import (IGNORED_FIELDS, LATE_CUTOFF, DATE_TODAY,
                        CTO_TYPE, CTO_SUBTYPE,
                        VALID_STATUS, VALID_INSTYPE,
                        PRFTREE_EXCLUDE_BACKEND,
                        CAL_PARAMS_NAME,
                        EXCLUDE_USERS_FRONTEND_PARAM,
                        BO_FIELDS_SET,
                        SKIP_CALC_TRADE_FIELDS,
                        SKIP_CALC_CASHFLOW_FIELDS,
                        USRGRP_SYSTEM)


LOGGER = getLogger(__name__)


def get_param_value(ext_name, param_name):
    try:
        ext_obj = acm.GetDefaultContext().GetExtension(acm.FParameters, 
                                                       acm.FObject, ext_name)
    except:
        return ''
    if not ext_obj:
        return ''
    params = ext_obj.Value()
    value = params.At(param_name)
    if value is None:
        return ''
    return str(value)


def get_exclude_users_frontend():
    value = get_param_value(CAL_PARAMS_NAME, EXCLUDE_USERS_FRONTEND_PARAM)
    if not value:
        return []
    try:
        return value.split(',')
    except:
        return []


def create_cto(name):
    cto = ael.TextObject.new()
    cto.name = name
    cto.subtype = CTO_SUBTYPE
    cto.type = CTO_TYPE
    return cto


def get_cto(name):
    return ael.TextObject.read('type="%s" and name="%s"' % (CTO_TYPE, name))


def update_cto(cto_name, cto_data):
    cto = get_cto(cto_name)
    if cto:
        cto_clone = cto.clone()
        cto_clone.data = cto_data
        return cto_clone, 'Update'
    cto_new = create_cto(cto_name)
    cto_new.data = cto_data
    return cto_new, 'Insert'


def get_stored_reason_and_type(ael_cto):
    values = json.loads(ael_cto.data)
    return values['amend_reason'], values['amend_type']


def has_exponent(input_string):
        if 'E+' in input_string or 'E-' in input_string:
            return True
        return False


def is_float(input_string):
    try:
        _ = float(input_string)
    except ValueError:
        return False
    return True


def is_ins_valid(ael_ins):
    if not ael_ins:
        return False
    return ael_ins.instype in VALID_INSTYPE


def is_ins_valid_backend(ael_ins):
    if not is_ins_valid(ael_ins):
        return False
    if ael_ins.instype == 'Deposit' and ael_ins.open_end == 'Open End':
        return False
    return True


def is_trade_valid(ael_trade):
    if not ael_trade:
        return False
    if not is_ins_valid(ael_trade.insaddr):
        return False
    status = ael_trade.status
    if status in VALID_STATUS:
        return True
    return False


def is_trade_valid_backend(ael_trade):
    if not is_trade_valid(ael_trade):
        return False
    if not ael_trade.prfnbr:
        return False
    prfid = ael_trade.prfnbr.prfid
    if any([tree.has(prfid) for tree in PRFTREE_EXCLUDE_BACKEND]):
        return False
    return True


def timestamp_to_acm(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def ael_date_to_acm(ael_date):
    return acm.Time.DateFromYMD(*ael_date.to_ymd())


def created_today(ael_entity):
    timestamp = ael_entity.creat_time
    if not timestamp:
        return False
    create_date = timestamp_to_acm(timestamp)[:10]
    return create_date == DATE_TODAY


def booked_today(ael_trade):
    timestamp = ael_trade.time
    trade_date = timestamp_to_acm(timestamp)[:10]
    return trade_date == DATE_TODAY


def is_backdate(ael_trade):
    value_day = ael_date_to_acm(ael_trade.value_day)
    return value_day < DATE_TODAY


def is_late(ael_trade):
    timestamp = ael_trade.creat_time
    creat_time = timestamp_to_acm(timestamp)
    return creat_time > LATE_CUTOFF


def set_add_info(ael_entity, ai_spec_name, value):
    found_ai = None
    for ai in ael_entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_spec_name:
            found_ai = ai
            break
    
    if found_ai:
        found_ai.value = value
        return
    new_ai = ael.AdditionalInfo.new(ael_entity)
    new_ai.value = value
    ai_spec = ael.AdditionalInfoSpec[ai_spec_name]
    new_ai.addinf_specnbr = ai_spec.specnbr


def get_add_info_value(ael_entity, ai_spec_name):
    for ai in ael_entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_spec_name:
            return ai.value
    return ''


def is_fair_value(ael_portfolio):
    return (ael_portfolio.type_chlnbr 
            and ael_portfolio.type_chlnbr.entry in ('Held For Trading', 'Mark to Market'))


class Output(object):
    
    """CAL ouptut XML file handler."""
    
    open_tag = '<TODAY>\n'
    close_tag = '</TODAY>\n'
    encoding = '<?xml version="1.0" encoding="ISO-8859-1" ?>\n'
    
    def __init__(self):
        self._path = ''
        self._init = False
        self._closed = False
    
    @classmethod
    def mandatory_lines(cls):
        return [cls.open_tag, cls.close_tag, cls.encoding]
    
    def _create_new(self):
        with open(self._path, 'w') as xml_file:
            xml_file.write(self.encoding)
            xml_file.write(self.open_tag)
    
    def _check_existing(self):
        with open(self._path, 'r') as xml_file:
            lines = xml_file.readlines()
        if not lines:
            self._create_new()
            return
        if not lines[-1] == self.close_tag:
            return
        filtered_lines = [x for x in lines if x not in self.mandatory_lines()]
        with open(self._path, 'w') as xml_file:
            xml_file.write(self.encoding)
            xml_file.write(self.open_tag)
            xml_file.writelines(filtered_lines)
    
    def init_file(self, file_path):
        self._path = file_path
        if self._init and not self._closed:
            return
        if os.path.exists(self._path):
            self._check_existing()
        else:
            self._create_new()
        self._init = True
        self._closed = False
    
    def close_file(self):
        if not self._init or self._closed:
            return
        with open(self._path, 'a') as xml_file:
            xml_file.write(self.close_tag)
        self._closed = True
    
    def write(self, text):
        with open(self._path, 'a') as xml_file:
            xml_file.write(text)


class AmendmentSource(object):
    
    """Wrapper for the amendment source entity."""
    
    def __init__(self, entity, operation, 
                 oid_attr, update_usrnbr=None, update_time=None):
        self.record_type = entity.record_type
        self.update_time = update_time if update_time else entity.updat_time
        self.update_usrnbr = update_usrnbr if update_usrnbr else entity.updat_usrnbr
        self.operation = operation
        self.entity_id = getattr(entity, oid_attr)
        self.differences = {}
    
    def is_valid(self, instrument=None):
        if self.entity_id < 0:
            return False
        if not timestamp_to_acm(self.update_time)[:10] == DATE_TODAY:
            return False
        if (instrument and instrument.instype == 'Deposit' 
                and instrument.open_end == 'Open End'
                and self.update_usrnbr.grpnbr.grpnbr in USRGRP_SYSTEM):
            return False
        return True
    
    def is_bo_process(self):
        if ('status' in self.differences 
                and self.differences['status']['new'] in ['BO Confirmed', 'BO-BO Confirmed']
                and self.differences['status']['old'] 
                    in ['BO Confirmed', 'FO Confirmed', 'Reserved', 'Internal']
                and set(self.differences.keys()) <= BO_FIELDS_SET):
            return True
        return False
    
    def skip_calculation(self):
        if not self.operation == 'update':
            return False
        if (self.record_type == 'Trade'
                and (self.is_bo_process()
                     or set(self.differences.keys()) <= SKIP_CALC_TRADE_FIELDS)):
            return True
        if (self.record_type == 'CashFlow' 
                and set(self.differences.keys()) <= SKIP_CALC_CASHFLOW_FIELDS):
            return True
        return False
    
    def check_differences(self, new_entity, old_entity):
        self.differences = defaultdict(lambda: defaultdict(str))
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
            if field_name in IGNORED_FIELDS:
                continue
            old_value = ' '.join(old_row_split[1:]).lstrip()
            new_value = ' '.join(new_row_split[1:]).lstrip()
            if has_exponent(new_row) and is_float(new_value):
                try:
                    old_value = getattr(old_entity, field_name)
                    new_value = getattr(new_entity, field_name)
                except:
                    msg = 'Failed to get "%s" for %s %s.'
                    LOGGER.exception(msg % (field_name, self.record_type, self.entity_id))
            if old_value == new_value:
                continue
            self.differences[field_name]['old'] = str(old_value)
            self.differences[field_name]['new'] = str(new_value)


class OutputConverter(object):
    
    def __init__(self, ael_trade, source):
        self._trade = ael_trade
        self._source = source
        self._root = ET.Element('Entity')
    
    @classmethod
    def translate(cls, column, value):
        if not value:
            return value
        if column.endswith('curr') or column.endswith('insaddr'):
            ins = ael.Instrument[int(value)]
            return ins.insid if ins else ''
        if column.endswith('usrnbr'):
            user = ael.User[int(value)]
            return user.userid if user else ''
        if column.endswith('ptynbr'):
            party = ael.Party[int(value)]
            return party.ptyid if party else ''
        if column.endswith('prfnbr'):
            prf = ael.Portfolio[int(value)]
            return prf.prfid if prf else ''
        return value
    
    def create_output(self):
        ET.SubElement(self._root, 'TradeID').text = str(self._trade.trdnbr)
        ET.SubElement(self._root, 'PortfolioID').text = str(self._trade.prfnbr.prfnbr)
        ET.SubElement(self._root, 'Portfolio').text = self._trade.prfnbr.prfid
        ET.SubElement(self._root, 'Instrument').text = self._trade.insaddr.insid
        ET.SubElement(self._root, 'InsType').text = self._trade.insaddr.instype
        ET.SubElement(self._root, 'Currency').text = self._trade.curr.insid
        ET.SubElement(self._root, 'Status').text = self._trade.status
        trader = self._trade.trader_usrnbr
        ET.SubElement(self._root, 'Trader').text = trader.userid if trader else 'N/A'
        ET.SubElement(self._root, 'Acquirer').text = self._trade.acquirer_ptynbr.ptyid
        ET.SubElement(self._root, 'Counterparty').text = self._trade.counterparty_ptynbr.ptyid
        trade_side = 'Buy' if self._trade.quantity > 0 else 'Sell'
        ET.SubElement(self._root, 'TradeSide').text = trade_side
        ET.SubElement(self._root, 'ValueDay').text = ael_date_to_acm(self._trade.value_day)
        update_time = self._source.update_time
        ET.SubElement(self._root, 'UpdateTime').text = timestamp_to_acm(update_time)
        update_usrnbr = self._source.update_usrnbr
        ET.SubElement(self._root, 'UpdateUser').text = update_usrnbr.userid
        ET.SubElement(self._root, 'AmendReason').text = ''
        ET.SubElement(self._root, 'CommentType').text = ''
        ET.SubElement(self._root, 'FairValuePortfolio').text = 'No'
        ET.SubElement(self._root, 'PLImpact').text = '0'
        ET.SubElement(self._root, 'PLImpactFairValue').text = '0'
        ET.SubElement(self._root, 'CALFlag').text = 'A'
        ET.SubElement(self._root, 'SourceType').text = self._source.record_type
        ET.SubElement(self._root, 'SourceID').text = str(self._source.entity_id)
        ET.SubElement(self._root, 'SourceOperation').text = self._source.operation
        execution_time = (timestamp_to_acm(self._trade.execution_time) 
                          if self._trade.execution_time else '')
        ET.SubElement(self._root, 'ExecutionTime').text = execution_time
        
        differences = self._source.differences
        for field_name in differences:
            amendment = ET.SubElement(self._root, 'Amendment')
            ET.SubElement(amendment, 'FieldName').text = field_name
            original_value = differences[field_name]['old']
            new_value = differences[field_name]['new']
            ET.SubElement(amendment, 'OriginalValue').text = self.translate(field_name, original_value)
            ET.SubElement(amendment, 'NewValue').text = self.translate(field_name, new_value)
    
    def set_text(self, element_name, value):
        if not len(self._root):
            return
        for element in self._root.iter(element_name):
            element.text = str(value)
    
    def get_string(self, init_indent=1, indent='\t'):
        if not len(self._root):
            return ''
        elements = ET.tostring(self._root).replace('><', '>\n<').split('\n')
        output = ''
        current_indent = init_indent
        for element in elements:
            if element.startswith('</'):
                current_indent -= 1
            output += current_indent * indent + element + '\n'
            if not ('/>' in element or '</' in element):
                current_indent += 1
        return output
