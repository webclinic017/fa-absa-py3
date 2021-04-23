"""-----------------------------------------------------------------------------
PURPOSE              :  SBL amendment process to record all Trade, Instrument, 
                        and Settlement updates done by the OPS SecLend and 
                        PCG Collateral user groups.
REQUESTER, DEPATMENT :  Jennitha Jugnath, PTS
PROJECT              :  SBL onto FA
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-05-26  CHG0102232     Libor Svoboda       Initial implementation
"""
import xml.etree.ElementTree as ET
from collections import defaultdict

import acm
from at_ats_utils import get_param_value, XmlOutputConverter
from at_logging import getLogger


LOGGER = getLogger(__name__)
IGNORED_FIELDS = (
    'UPDAT_TIME',
    'UPDAT_USRNBR',
    'UPDAT_USRNBR.USERID',
    'VERSION_ID',
    'UPDAT_USRNBR.GRPNBR.GRPID',
)
SBL_ACQUIRERS = (
    'SLL PRINCIPAL ACCOUNT',
    'SLB PRINCIPAL ACCOUNT',
    'SLL ABSA SECURITIES LENDING',
    'SLB ABSA SECURITIES LENDING',
    'SLL ABSA BANK NAMIBIAN PRINCIPAL ACC',
    'SLB ABSA BANK NAMIBIAN PRINCIPAL ACC',
)
FPARAM_NAME = 'SBLAmendments'
AMBA_PARAMS = {}


def get_include_groups():
    try:
        return AMBA_PARAMS['include_groups']
    except KeyError:
        pass
    include_groups = get_param_value(FPARAM_NAME, 'IncludeUserGroups')
    AMBA_PARAMS['include_groups'] = [group.strip() for group 
                                     in include_groups.split(',') if group]
    LOGGER.info('Including user groups: %s.' 
                % ', '.join(AMBA_PARAMS['include_groups']))
    return AMBA_PARAMS['include_groups']


def sender_modify(msg, subject):
    # ael_sender_modify AMBA hook
    send_to_amb = (msg, subject)
    business_obj = msg.mbf_last_object()
    if not business_obj:
        msg_str = msg.mbf_object_to_string()
        LOGGER.warning('Sender modify: Invalid message %s' % msg_str)
        return None
    updat_grpid_obj = business_obj.mbf_find_object('UPDAT_USRNBR.GRPNBR.GRPID')
    if updat_grpid_obj:
        updat_grpid = updat_grpid_obj.mbf_get_value()
        if updat_grpid in get_include_groups():
            return send_to_amb
        return None
    LOGGER.warning('Sender modify: UPDAT_USRNBR.GRPNBR.GRPID not found.')
    updat_usrnbr_obj = business_obj.mbf_find_object('UPDAT_USRNBR')
    if not updat_usrnbr_obj:
        LOGGER.warning('Sender modify: UPDAT_USRNBR not specified')
        return send_to_amb
    updat_usrnbr = int(updat_usrnbr_obj.mbf_get_value())
    update_user = acm.FUser[updat_usrnbr]
    if not update_user:
        LOGGER.warning('Sender modify: Invalid update user.')
        return send_to_amb
    if (update_user.UserGroup() 
            and update_user.UserGroup().Name() in get_include_groups()):
        return send_to_amb
    return None


class SourceError(Exception):
    pass


class AmendmentSource(object):
    
    def __init__(self, entity_id, msg_object):
        self.msg_object = msg_object
        self.record_type = msg_object.table_name
        self._parent_table = self.msg_object.parent_table
        self.msg_date = self._get_update_time()[:10]
        self.update_time = self._get_update_time()
        self.update_userid = self._get_update_userid()
        self.update_grpid = self._get_update_grpid()
        self.operation = msg_object.operation
        self.entity_id = entity_id
        self.differences = {}
    
    @staticmethod
    def get_object_type(table):
        if table.name in ('LEG', 'CASHFLOW', 'RESET', 'PAYMENT'):
            try:
                return table.attributes['TYPE']['current']
            except KeyError:
                return ''
        if table.name == 'ADDITIONALINFO':
            try:
                return table.attributes['ADDINF_SPECNBR.FIELD_NAME']['current']
            except KeyError:
                return ''
        return ''
    
    def _get_parent_attr(self, field_name, state='current'):
        return self._parent_table.attributes[field_name][state]
    
    def _get_update_time(self):
        try:
            return self._get_parent_attr('UPDAT_TIME')
        except KeyError:
            raise SourceError('Update time not specified.')
    
    def _get_update_userid(self):
        try:
            return self._get_parent_attr('UPDAT_USRNBR.USERID')
        except KeyError:
            pass
        try:
            user_number = self._get_parent_attr('UPDAT_USRNBR')
        except KeyError:
            raise SourceError('Update user not specified.')
        user = acm.FUser[user_number]
        return user.Name()
    
    def _get_update_grpid(self):
        try:
            return self._get_parent_attr('UPDAT_USRNBR.GRPNBR.GRPID')
        except KeyError:
            pass
        userid = self._get_update_userid()
        return acm.FUser[userid].UserGroup().Name()
    
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
        if table.name == 'SETTLEMENT':
            return table.attributes['SEQNBR']['current']
        if table.name == 'ADDITIONALINFO':
            return table.attributes['VALNBR']['current']
        LOGGER.warning('OID logic not defined for table %s.' % table.name)
        return ''
    
    def _get_field(self, field_name):
        if self.record_type == 'INSTRUMENT':
            try:
                return self._get_parent_attr(field_name)
            except KeyError:
                return ''
        if self.record_type == 'TRADE':
            try:
                return self._get_parent_attr('INSADDR.%s' % field_name)
            except KeyError:
                return ''
        if self.record_type == 'SETTLEMENT':
            try:
                return self._get_parent_attr('TRDNBR.INSADDR.%s' % field_name)
            except KeyError:
                return ''
        return ''
    
    def _get_add_info(self, addinf_spec):
        tables = self.msg_object.get_tables('ADDITIONALINFO')
        for table in tables:
            if ('ADDINF_SPECNBR.FIELD_NAME' in table.attributes
                    and table.attributes['ADDINF_SPECNBR.FIELD_NAME']['current'] == addinf_spec):
                return table.attributes['VALUE']['current']
        return ''
    
    def get_insid(self):
        return self._get_field('INSID')
    
    def get_instype(self):
        return self._get_field('INSTYPE')
    
    def get_und_insid(self):
        return self._get_field('UND_INSADDR.INSID')
    
    def get_ptyid(self):
        if self.record_type == 'SETTLEMENT':
            try:
                return self._get_parent_attr('PARTY_PTYID')
            except KeyError:
                return ''
        if self.record_type == 'TRADE':
            trade_cptyid = ''
            try:
                trade_cptyid = self._get_parent_attr('COUNTERPARTY_PTYNBR.PTYID')
            except KeyError:
                pass
            if self.get_instype() != 'SecurityLoan':
                return trade_cptyid
            cpty1 = self._get_add_info('SL_G1Counterparty1')
            if cpty1 and not cpty1 in SBL_ACQUIRERS:
                return cpty1
            cpty2 = self._get_add_info('SL_G1Counterparty2')
            if cpty2 and not cpty2 in SBL_ACQUIRERS:
                return cpty2
            return trade_cptyid
        return ''
    
    def check_differences(self):
        if not self.operation == 'UPDATE':
            return
        self.differences = defaultdict(list)
        for table in self.msg_object.get_tables():
            if not table.operation:
                continue
            item = {
                'operation': table.operation,
                'oid': self._get_oid(table),
                'diff': {},
            }
            object_type = self.get_object_type(table)
            table_name = ':'.join([_f for _f in [table.name.capitalize(), object_type] if _f])
            if table.operation in ('INSERT', 'DELETE'):
                self.differences[table_name].append(item)
                continue
            diff = defaultdict(lambda: defaultdict(str))
            for attr_name, attr_dict in table.attributes.iteritems():
                if not attr_dict['operation'] == 'UPDATE':
                    continue
                if attr_name in IGNORED_FIELDS:
                    continue
                diff[attr_name]['old'] = attr_dict['previous']
                diff[attr_name]['new'] = attr_dict['current']
            if diff:
                item['diff'] = diff
                self.differences[table_name].append(item)


class OutputConverter(XmlOutputConverter):
    
    def create_output(self):
        ET.SubElement(self._root, 'ObjectType').text = self._source.record_type.capitalize()
        ET.SubElement(self._root, 'ObjectID').text = str(self._source.entity_id)
        ET.SubElement(self._root, 'Operation').text = self._source.operation.lower()
        ET.SubElement(self._root, 'UpdateTime').text = self._source.update_time
        ET.SubElement(self._root, 'UpdateUser').text = self._source.update_userid
        ET.SubElement(self._root, 'UpdateUserGroup').text = self._source.update_grpid
        ET.SubElement(self._root, 'Instrument').text = self._source.get_insid()
        ET.SubElement(self._root, 'InsType').text = self._source.get_instype()
        ET.SubElement(self._root, 'Underlying').text = self._source.get_und_insid()
        ET.SubElement(self._root, 'Counterparty').text = self._source.get_ptyid()
        for table_name, tables in self._source.differences.iteritems():
            for item in tables:
                amendment = ET.SubElement(self._root, 'Amendment')
                ET.SubElement(amendment, 'TableName').text = table_name
                ET.SubElement(amendment, 'Operation').text = item['operation'].lower()
                ET.SubElement(amendment, 'Oid').text = item['oid']
                diff = item['diff']
                for field_name in diff:
                    field = ET.SubElement(amendment, 'Field')
                    ET.SubElement(field, 'FieldName').text = field_name
                    original_value = diff[field_name]['old']
                    new_value = diff[field_name]['new']
                    ET.SubElement(field, 'OriginalValue').text = original_value
                    ET.SubElement(field, 'NewValue').text = new_value

