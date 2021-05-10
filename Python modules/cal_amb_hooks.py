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
2019-09-21  FAU            Libor Svoboda       Initial Implementation
2020-05-26  CHG0102232     Libor Svoboda       Refactor
"""
import json

import acm
import ael
from at_ats_utils import get_param_value
from at_logging import getLogger
from cal_amb_config import (DEFAULTS,
                            DEFAULT_MAPPING_USER,
                            DEFAULT_MAPPING_GROUP,
                            DEFAULT_MAPPING_PORTFOLIO,
                            DEFAULT_MAPPING_INS,
                            CTO_TYPE,
                            CAL_PARAMS_NAME,
                            AMBA_FEED_START_PARAM,
                            AMBA_FEED_STOP_PARAM)
from cal_amb_util import is_backdated_insert, is_late
                            

LOGGER = getLogger(__name__)
AMEND_REASON_SPEC = ael.AdditionalInfoSpec.read('field_name="AmendReasonTrd"')
AMEND_TYPE_SPEC = ael.AdditionalInfoSpec.read('field_name="AmendReasonTypeTrd"')

AMBA_FEED_START = get_param_value(CAL_PARAMS_NAME, AMBA_FEED_START_PARAM)
AMBA_FEED_STOP = get_param_value(CAL_PARAMS_NAME, AMBA_FEED_STOP_PARAM)

DAYS_OF_WEEK = {}


def get_cto(name):
    return ael.TextObject.read('type="%s" and name="%s"' % (CTO_TYPE, name))


def get_stored_reason_and_type(ael_cto):
    values = json.loads(ael_cto.data)
    return values['amend_reason'], values['amend_type']


def get_add_info_value(entity_id, ai_spec):
    ai = ael.AdditionalInfo.read('addinf_specnbr=%s and recaddr=%s' 
                                 % (ai_spec.specnbr, entity_id))
    return ai.value if ai else ''


def get_day_of_week(update_time):
    update_date = update_time[:10]
    if update_date in DAYS_OF_WEEK:
        return DAYS_OF_WEEK[update_date]
    day_of_week = acm.Time.DayOfWeek(update_date)
    DAYS_OF_WEEK[update_date] = day_of_week
    return day_of_week


class Sender(object):
    
    default_reason_key = ''
    
    def __init__(self, entity):
        self._entity = entity
        self._entity_id = ''
        self._update_time = entity.updat_time
        self._update_usrnbr = entity.updat_usrnbr
    
    def _amend_reason_and_type_default(self):
        user = self._update_usrnbr
        usrnbr = user.usrnbr if user else ''
        grpnbr = user.grpnbr.grpnbr if (user and user.grpnbr) else ''
        if usrnbr in DEFAULT_MAPPING_USER:
            if self.default_reason_key in DEFAULT_MAPPING_USER[usrnbr]:
                return DEFAULT_MAPPING_USER[usrnbr][self.default_reason_key]
            return DEFAULT_MAPPING_USER[usrnbr]['default']
        if grpnbr in DEFAULT_MAPPING_GROUP:
            if self.default_reason_key in DEFAULT_MAPPING_GROUP[grpnbr]:
                return DEFAULT_MAPPING_GROUP[grpnbr][self.default_reason_key]
            return DEFAULT_MAPPING_GROUP[grpnbr]['default']
        return DEFAULTS['global']
    
    def _amend_reason_and_type_stored(self):
        userid = self._update_usrnbr.userid if self._update_usrnbr else ''
        cto_name = 'CAL_%s_%s_%s' % (self._entity.record_type,
                                     self._entity_id,
                                     self._update_usrnbr.userid)
        cto = get_cto(cto_name)
        if cto and cto.updat_time >= self._update_time:
            try:
                return get_stored_reason_and_type(cto)
            except:
                pass
        return None
    
    def get_amend_reason_and_type(self):
        reason_and_type = self._amend_reason_and_type_stored()
        if reason_and_type:
            return reason_and_type
        LOGGER.warning('%s %s: Amend reason and type not found in CTO, using default.'
                       % (self._entity.record_type, self._entity_id))
        return self._amend_reason_and_type_default()


class TradeSender(Sender):
    
    def __init__(self, entity):
        super(TradeSender, self).__init__(entity)
        self._entity_id = entity.trdnbr
    
    def _amend_reason_and_type_default(self):
        prfnbr = self._entity.prfnbr.prfnbr if self._entity.prfnbr else ''
        if prfnbr in DEFAULT_MAPPING_PORTFOLIO:
            if self.default_reason_key in DEFAULT_MAPPING_PORTFOLIO[prfnbr]:
                return DEFAULT_MAPPING_PORTFOLIO[prfnbr][self.default_reason_key]
            return DEFAULT_MAPPING_PORTFOLIO[prfnbr]['default']
        instype = self._entity.insaddr.instype if self._entity.insaddr else ''
        if instype in DEFAULT_MAPPING_INS:
            for func in DEFAULT_MAPPING_INS[instype]:
                if func(self._entity.insaddr):
                    return DEFAULT_MAPPING_INS[instype][func]
        return super(TradeSender, self)._amend_reason_and_type_default()


class InsertTradeSender(TradeSender):
    
    def get_amend_reason_and_type(self):
        amend_reason = get_add_info_value(self._entity_id, AMEND_REASON_SPEC)
        amend_type = get_add_info_value(self._entity_id, AMEND_TYPE_SPEC)
        if amend_reason and amend_type:
            return amend_reason, amend_type
        LOGGER.warning('%s %s: Amend reason and type not found in add info, using default.'
                       % (self._entity.record_type, self._entity_id))
        return self._amend_reason_and_type_default()


class BackdateTradeSender(InsertTradeSender):
    
    default_reason_key = 'backdate'


class InstrumentSender(Sender):
    
    def __init__(self, entity):
        super(InstrumentSender, self).__init__(entity)
        self._entity_id = entity.insaddr
    
    def _amend_reason_and_type_default(self):
        instype = self._entity.instype
        if instype in DEFAULT_MAPPING_INS:
            for func in DEFAULT_MAPPING_INS[instype]:
                if func(self._entity):
                    return DEFAULT_MAPPING_INS[instype][func]
        return super(InstrumentSender, self)._amend_reason_and_type_default()


def sender_add(entity, operation):
    # ael_sender_add AMBA hook
    if not entity.record_type in ('Instrument', 'Trade'):
        return []
    sender = None
    amend_reason = ''
    amend_type = ''
    if entity.record_type == 'Instrument' and operation == 'Update':
        sender = InstrumentSender(entity)
    elif entity.record_type == 'Trade':
        if operation == 'Insert':
            if is_backdated_insert(entity):
                sender = BackdateTradeSender(entity)
            elif is_late(entity):
                sender = InsertTradeSender(entity)
        elif operation == 'Update':
            sender = TradeSender(entity)
    if sender:
        amend_reason, amend_type = sender.get_amend_reason_and_type()
    return [
        ['AMEND_REASON', amend_reason],
        ['AMEND_TYPE', amend_type]
    ]


def sender_modify(msg, subject):
    # ael_sender_modify AMBA hook
    send_to_amb = (msg, subject)
    business_obj = msg.mbf_last_object()
    if not business_obj:
        msg_str = msg.mbf_object_to_string()
        LOGGER.warning('Sender modify: Invalid message %s' % msg_str)
        return None
    updat_time_obj = business_obj.mbf_find_object('UPDAT_TIME')
    if not updat_time_obj:
        LOGGER.warning('Sender modify: UPDAT_TIME not specified')
        return send_to_amb
    update_time = updat_time_obj.mbf_get_value()
    try:
        day_of_week = get_day_of_week(update_time)
    except:
        LOGGER.exception('Sender modify: Invalid UPDAT_TIME %s.' % update_time)
        return None
    if day_of_week in ('Saturday', 'Sunday'):
        LOGGER.info('Sender modify: Ignoring update on %s at %s.'
                    % (day_of_week, update_time))
        return None
    update_time_only = update_time[11:]
    if update_time_only < AMBA_FEED_START or update_time_only > AMBA_FEED_STOP:
        LOGGER.info('Sender modify: Update time outside of the feed period %s.' 
                    % update_time)
        return None
    return send_to_amb
