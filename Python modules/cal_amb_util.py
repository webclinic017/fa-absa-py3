"""-----------------------------------------------------------------------------
PURPOSE              :  Alternative CAL implementation using AMB instead of
                        direct table subscriptions via AEL.
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-05-16  CHG1001670427  Libor Svoboda       Initial Implementation
2019-09-21  FAU            Libor Svoboda       Implement ael_sender_add hook
2020-05-26  CHG0102232     Libor Svoboda       Refactor
2020-11-26  CHG0141021     Bhavnisha Sarawan   Include other types in is_fair_value
"""
import time
import xml.etree.ElementTree as ET
from collections import defaultdict

import acm
from at_amba_message import AmbaMessage
from at_ats_utils import XmlOutputConverter
from cal_amb_config import (IGNORED_FIELDS, 
                            BO_FIELDS_SET, 
                            SKIP_CALC_TRADE_FIELDS,
                            VALID_INSTYPE,
                            VALID_STATUS,
                            PRFTREE_EXCLUDE_BACKEND)


def timestamp_to_acm(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def ael_date_to_acm(ael_date):
    return acm.Time.DateFromYMD(*ael_date.to_ymd())


def get_late_cutoff(acm_date):
    return '%s 19:00:00' % acm_date


def is_backdated_insert(ael_trade):
    if not ael_trade.value_day or not ael_trade.creat_time:
        return False
    value_day = ael_date_to_acm(ael_trade.value_day)
    create_day = timestamp_to_acm(ael_trade.creat_time)[:10]
    return value_day < create_day


def is_late(ael_trade):
    if not ael_trade.creat_time:
        return False
    create_time = timestamp_to_acm(ael_trade.creat_time)
    late_cutoff = get_late_cutoff(create_time[:10])
    return create_time > late_cutoff


def is_ins_valid(acm_ins):
    if not acm_ins:
        return False
    return acm_ins.InsType() in VALID_INSTYPE


def is_trade_valid(acm_trade):
    if not acm_trade:
        return False
    if not is_ins_valid(acm_trade.Instrument()):
        return False
    status = acm_trade.Status()
    if status in VALID_STATUS:
        return True
    return False


def is_trade_valid_backend(acm_trade):
    if not is_trade_valid(acm_trade):
        return False
    if not acm_trade.Portfolio():
        return False
    prfid = acm_trade.Portfolio().Name()
    if any([tree.has(prfid) for tree in PRFTREE_EXCLUDE_BACKEND]):
        return False
    return True


def is_fair_value(acm_portfolio):
    return (acm_portfolio.TypeChlItem()
            and acm_portfolio.TypeChlItem().Name() in ('Held For Trading', 'Mark to Market'))


class SourceError(Exception):
    pass


class AmendmentSource(object):
    
    """Wrapper for the amendment source entity."""
    
    def __init__(self, entity_id, msg_object):
        self.msg_object = msg_object
        self.record_type = msg_object.table_name
        self._parent_table = self.msg_object.parent_table
        self.msg_date = self._get_update_time()[:10]
        self.update_time = self._get_update_time()
        self.update_user = self._get_update_user()
        self.operation = msg_object.operation
        self.entity_id = entity_id
        self.differences = {}
        self.amend_reason = self._get_amend_reason()
        self.amend_type = self._get_amend_type()
    
    def _get_update_time(self):
        return self._parent_table.attributes['UPDAT_TIME']['current']
    
    def _get_update_user(self):
        user_number = self._parent_table.attributes['UPDAT_USRNBR']['current']
        user = acm.FUser[user_number]
        if not user:
            raise SourceError('Update user not specified.')
        return user
    
    def _get_amend_reason(self):
        if 'AMEND_REASON' in self._parent_table.attributes:
            return self._parent_table.attributes['AMEND_REASON']['current']
        return ''
    
    def _get_amend_type(self):
        if 'AMEND_TYPE' in self._parent_table.attributes:
            return self._parent_table.attributes['AMEND_TYPE']['current']
        return ''
    
    def _get_oid(self, table):
        if table.name == self.record_type:
            return str(self.entity_id)
        if table.name == 'INSTRUMENT':
            return table.attributes['INSADDR']['current']
        if table.name == 'LEG':
            return table.attributes['LEGNBR']['current']
        if table.name == 'CASHFLOW':
            return table.attributes['CFWNBR']['current']
        if table.name == 'RESET':
            return table.attributes['RESNBR']['current']
        if table.name == 'TRADE':
            return table.attributes['TRDNBR']['current']
        if table.name == 'PAYMENT':
            return table.attributes['PAYNBR']['current']
        return ''
    
    def is_bo_process(self):
        updated_tables = set(self.differences.keys())
        if not updated_tables == {'TRADE'}:
            return False
        trade_diff = self.differences['TRADE'][0]['diff']
        if ('STATUS' in trade_diff
                and trade_diff['STATUS']['new'] in ['BO Confirmed', 'BO-BO Confirmed']
                and trade_diff['STATUS']['old'] 
                    in ['BO Confirmed', 'FO Confirmed', 'Reserved', 'Internal']
                and set(trade_diff.keys()) <= BO_FIELDS_SET):
            return True
        return False
    
    def skip_calculation(self):
        updated_tables = set(self.differences.keys())
        if self.record_type == 'TRADE' and updated_tables == {'TRADE'}:
            trade_diff = self.differences['TRADE'][0]['diff']
            if self.is_bo_process() or set(trade_diff.keys()) <= SKIP_CALC_TRADE_FIELDS:
                return True
        return False
    
    def check_differences(self):
        if not self.operation == 'UPDATE':
            return
        self.differences = defaultdict(list)
        for table in self.msg_object.get_tables():
            if not table.operation:
                continue
            if (self.record_type == 'INSTRUMENT' 
                    and table.name not in ('INSTRUMENT', 'LEG', 'CASHFLOW', 'RESET')):
                continue
            if self.record_type == 'TRADE' and table.name not in ('TRADE', 'PAYMENT'):
                continue
            item = {
                'operation': table.operation,
                'oid': self._get_oid(table),
                'diff': {},
            }
            if table.operation in ('INSERT', 'DELETE'):
                self.differences[table.name].append(item)
                continue
            diff = defaultdict(lambda: defaultdict(str))
            for attr_name, attr_dict in table.attributes.items():
                if not attr_dict['operation'] == 'UPDATE':
                    continue
                if attr_name in IGNORED_FIELDS:
                    continue
                diff[attr_name]['old'] = attr_dict['previous']
                diff[attr_name]['new'] = attr_dict['current']
            if diff:
                item['diff'] = diff
                self.differences[table.name].append(item)


class OutputConverter(XmlOutputConverter):
    
    def __init__(self, acm_trade, source):
        self._trade = acm_trade
        super(OutputConverter, self).__init__(source)
    
    def create_output(self):
        trade_id = self._source.entity_id if self._source.record_type == 'TRADE' else self._trade.Oid()
        ET.SubElement(self._root, 'TradeID').text = str(trade_id)
        ET.SubElement(self._root, 'PortfolioID').text = str(self._trade.Portfolio().Oid())
        ET.SubElement(self._root, 'Portfolio').text = self._trade.Portfolio().Name()
        ET.SubElement(self._root, 'Instrument').text = self._trade.Instrument().Name()
        ET.SubElement(self._root, 'InsType').text = self._trade.Instrument().InsType()
        ET.SubElement(self._root, 'Currency').text = self._trade.Currency().Name()
        ET.SubElement(self._root, 'Status').text = self._trade.Status()
        trader = self._trade.Trader()
        ET.SubElement(self._root, 'Trader').text = trader.Name() if trader else 'N/A'
        ET.SubElement(self._root, 'Acquirer').text = self._trade.Acquirer().Name()
        ET.SubElement(self._root, 'Counterparty').text = self._trade.Counterparty().Name()
        trade_side = 'Buy' if self._trade.Quantity() > 0 else 'Sell'
        ET.SubElement(self._root, 'TradeSide').text = trade_side
        ET.SubElement(self._root, 'ValueDay').text = self._trade.ValueDay()
        ET.SubElement(self._root, 'UpdateTime').text = self._source.update_time
        ET.SubElement(self._root, 'UpdateUser').text = self._source.update_user.Name()
        ET.SubElement(self._root, 'AmendReason').text = ''
        ET.SubElement(self._root, 'CommentType').text = ''
        ET.SubElement(self._root, 'FairValuePortfolio').text = 'No'
        ET.SubElement(self._root, 'PLImpact').text = '0'
        ET.SubElement(self._root, 'PLImpactFairValue').text = '0'
        ET.SubElement(self._root, 'CALFlag').text = 'A'
        ET.SubElement(self._root, 'SourceType').text = self._source.record_type.capitalize()
        ET.SubElement(self._root, 'SourceID').text = str(self._source.entity_id)
        ET.SubElement(self._root, 'SourceOperation').text = self._source.operation.lower()
        execution_time = ('' if self._trade.ExecutionTime()[:10] == acm.Time.SmallDate() 
                          else self._trade.ExecutionTime())
        ET.SubElement(self._root, 'ExecutionTime').text = execution_time
        
        differences = self._source.differences
        for table_name, tables in differences.items():
            for item in tables:
                amendment = ET.SubElement(self._root, 'Amendment')
                ET.SubElement(amendment, 'TableName').text = table_name
                ET.SubElement(amendment, 'Operation').text = item['operation']
                ET.SubElement(amendment, 'Oid').text = item['oid']
                diff = item['diff']
                for field_name in diff:
                    field = ET.SubElement(amendment, 'Field')
                    ET.SubElement(field, 'FieldName').text = field_name
                    original_value = diff[field_name]['old']
                    new_value = diff[field_name]['new']
                    ET.SubElement(field, 'OriginalValue').text = original_value
                    ET.SubElement(field, 'NewValue').text = new_value
    
    def set_text(self, element_name, value):
        if not len(self._root):
            return
        for element in self._root.iter(element_name):
            element.text = str(value)


class AmbaMessageCal(AmbaMessage):
    
    fields_to_skip = {
        'INSTRUMENT': (
            'INSID',
            'INSADDR',
            'AMEND_REASON',
            'AMEND_TYPE',
        ),
        'TRADE': (
            'TRDNBR',
            'OPTIONAL_KEY',
            'PREV_IN_CONTR_TRDNBR',
            'AMEND_REASON',
            'AMEND_TYPE',
        ),
    }
