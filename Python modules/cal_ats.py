"""-----------------------------------------------------------------------------
PURPOSE              :  CAL ATS listener
                        * Subscribes to the following events:
                            Trade - insert (if backdated or late), update
                            Instrument - update
                            Leg - update, delete
                            CashFlow - update, delete, insert
                            Reset - update, delete
                            Payment - update, delete, insert
                        * Calculates trade-level PnL impact for each event
                        * Retrieves amendment reasons from custom text objects or
                            add infos (only for trade insert)
                        * Creates real-time XML output
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
2019-02-05  CHG1001325774  Libor Svoboda       Skip reporting of BO confirmation
"""
import datetime
import os
import acm
import ael
from collections import defaultdict
from queue import Queue
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from cal_util import (Output, OutputConverter, AmendmentSource,
                      get_add_info_value,
                      is_fair_value,
                      is_trade_valid_backend,
                      is_ins_valid_backend,
                      is_backdate,
                      is_late,
                      booked_today,
                      created_today,
                      get_cto,
                      get_stored_reason_and_type)
from cal_config import (CALCULATED_COLUMNS, CALC_CURRENCY, 
                        DEFAULT_MAPPING_USER,
                        DEFAULT_MAPPING_GROUP,
                        DEFAULT_MAPPING_PORTFOLIO,
                        DEFAULT_MAPPING_INS,
                        DEFAULTS,
                        CAL_FLAGS,
                        USRNBR_EXCLUDE_BACKEND,
                        INITIAL_STATUS)


LOGGER = getLogger(__name__)

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
CALC_SPACE.SimulateGlobalValue('Fixed Currency', CALC_CURRENCY)
CALC_SPACE.SimulateGlobalValue('Position Currency Choice', 'Fixed Curr')
CALC_SPACE.SimulateGlobalValue('Aggregate Currency Choice', 'Fixed Curr')

DATE_TODAY = acm.Time.DateToday()

OUTPUT_FILE = 'CAL_%s.xml' % DATE_TODAY
OUTPUT_DIR = (r'L:\FALOG\PRODA\ATS_CAL' if os.name == 'nt' 
                  else '/services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
LISTENER_CUTOFF = '19:30:00'
ATS_PARAMS = {
    'subscribed': False,
    'closed': True,
    'table': '',
    'cutoff': LISTENER_CUTOFF,
    'path': OUTPUT_PATH,
}

worker_queue = Queue()
cal_output = Output()

ael_variables = AelVariableHandler()
ael_variables.add(
    'output_dir',
    label='Output Directory',
    default=OUTPUT_DIR,
)
ael_variables.add(
    'output_file',
    label='Output File',
    default=OUTPUT_FILE,
)
ael_variables.add(
    'table',
    label='Table',
    collection=['', 'Trade', 'Payment', 'Instrument', 'Leg', 'CashFlow', 'Reset'],
    default='',
    mandatory=False,
)
ael_variables.add(
    'cutoff',
    label='Listener Cutoff',
    default=LISTENER_CUTOFF,
)


def get_output_path(output_dir, output_file, report_date):
    output_path = os.path.join(output_dir, output_file)
    dt = datetime.datetime(*acm.Time.DateToYMD(DATE_TODAY))
    return output_path.format(dt)


class Worker(object):
    
    default_reason_key = ''
    
    def __init__(self, entity, source):
        self._entity = entity
        self._source = source
        self._entity_id = ''
        self._amend_reason = DEFAULTS['global'][0]
        self._comment_type = DEFAULTS['global'][1]
    
    @classmethod
    def calc_pnl_impact(cls, portfolio, values, fair_value=False):
        if fair_value or is_fair_value(portfolio):
            return (values['new']['Portfolio Cash End']
                    + values['new']['Total Val End']
                    - values['old']['Portfolio Cash End']
                    - values['old']['Total Val End'])
        return (values['new']['Portfolio Cash End']
                + values['new']['Portfolio Profit Loss Period Position']
                + values['new']['Portfolio Accrued Interest']
                - values['old']['Portfolio Cash End']
                - values['old']['Portfolio Profit Loss Period Position']
                - values['old']['Portfolio Accrued Interest'])
    
    @classmethod
    def calculate_value(cls, acm_trade, column_id):
        value = CALC_SPACE.CalculateValue(acm_trade, column_id)
        return float(value)
    
    @classmethod
    def clear_calc_space(cls):
        CALC_SPACE.Clear()
        CALC_SPACE.SimulateGlobalValue('Fixed Currency', CALC_CURRENCY)
        CALC_SPACE.SimulateGlobalValue('Position Currency Choice', 'Fixed Curr')
        CALC_SPACE.SimulateGlobalValue('Aggregate Currency Choice', 'Fixed Curr')
    
    def _uses_default_reason(self):
        for amend_reason, comment_type in DEFAULTS.values():
            if (self._amend_reason == amend_reason 
                    and self._comment_type == comment_type):
                return True
        return False
    
    def _skip_reporting(self):
        if (self._source.update_usrnbr.usrnbr in USRNBR_EXCLUDE_BACKEND 
                and self._uses_default_reason()):
            msg = 'Reporting skipped. Non-PRIME amendment by %s.'
            LOGGER.info(msg % self._source.update_usrnbr.userid)
            return True
        return False
    
    def _amend_reason_and_type_default(self):
        usrnbr = self._source.update_usrnbr.usrnbr
        grpnbr = self._source.update_usrnbr.grpnbr.grpnbr
        if usrnbr in DEFAULT_MAPPING_USER:
            if self.default_reason_key in DEFAULT_MAPPING_USER[usrnbr]:
                return DEFAULT_MAPPING_USER[usrnbr][self.default_reason_key]
            return DEFAULT_MAPPING_USER[usrnbr]['default']
        if grpnbr in DEFAULT_MAPPING_GROUP:
            if self.default_reason_key in DEFAULT_MAPPING_GROUP[grpnbr]:
                return DEFAULT_MAPPING_GROUP[grpnbr][self.default_reason_key]
            return DEFAULT_MAPPING_GROUP[grpnbr]['default']
        return DEFAULTS['global']
    
    def _amend_reason_and_type_delete(self):
        cto_name = 'CAL_%s_%s_Delete' % (self._source.record_type,
                                         self._source.entity_id)
        cto = get_cto(cto_name)
        try:
            reason_and_type = get_stored_reason_and_type(cto)
        except:
            reason_and_type = None
        if reason_and_type:
            self._source.update_time = cto.updat_time
            self._source.update_usrnbr = cto.updat_usrnbr
        return reason_and_type
    
    def _amend_reason_and_type_update(self):
        update_userid = self._source.update_usrnbr.userid
        source_cto_name = 'CAL_%s_%s_%s' % (self._source.record_type,
                                            self._source.entity_id,
                                            update_userid)
        source_cto = get_cto(source_cto_name)
        if source_cto and source_cto.updat_time >= self._source.update_time:
            try:
                return get_stored_reason_and_type(source_cto)
            except:
                pass
        entity_cto_name = 'CAL_%s_%s_%s' % (self._entity.record_type,
                                            self._entity_id,
                                            update_userid)
        entity_cto = get_cto(entity_cto_name)
        if entity_cto and entity_cto.updat_time >= self._source.update_time:
            try:
                return get_stored_reason_and_type(entity_cto)
            except:
                pass
        return None
    
    def _get_amend_reason_and_type(self):
        reason_and_type = None
        if self._source.operation in ('update', 'insert'):
            reason_and_type = self._amend_reason_and_type_update()
        elif self._source.operation == 'delete':
            reason_and_type = self._amend_reason_and_type_delete()
        if reason_and_type:
            self._amend_reason = reason_and_type[0]
            self._comment_type = reason_and_type[1]
            return
        LOGGER.warning('Amend reason and type not found in CTO, using default.')
        amend_reason, comment_type = self._amend_reason_and_type_default()
        self._amend_reason = amend_reason
        self._comment_type = comment_type
    

class TradeWorker(Worker):
    
    cal_flag = ''
    
    def __init__(self, entity, source):
        super(TradeWorker, self).__init__(entity, source)
        self._entity_id = entity.trdnbr
        self._values = defaultdict(lambda: defaultdict(float))
    
    def _amend_reason_and_type_default(self):
        if self._source.is_bo_process():
            return DEFAULTS['bo']
        prfnbr = self._entity.prfnbr.prfnbr
        if prfnbr in DEFAULT_MAPPING_PORTFOLIO:
            if self.default_reason_key in DEFAULT_MAPPING_PORTFOLIO[prfnbr]:
                return DEFAULT_MAPPING_PORTFOLIO[prfnbr][self.default_reason_key]
            return DEFAULT_MAPPING_PORTFOLIO[prfnbr]['default']
        instype = self._entity.insaddr.instype
        if instype in DEFAULT_MAPPING_INS:
            for func in DEFAULT_MAPPING_INS[instype]:
                if func(self._entity.insaddr):
                    return DEFAULT_MAPPING_INS[instype][func]
        return super(TradeWorker, self)._amend_reason_and_type_default()
        
    def _calculate_values(self, entity, values_flag):
        for column_id in CALCULATED_COLUMNS:
            try:
                trade = acm.Ael.AelToFObject(entity)
                value = self.calculate_value(trade, column_id)
            except Exception as exc:
                value = float('nan')
                msg = 'Failed to calculate "%s": %s'
                LOGGER.warning(msg % (column_id, str(exc)))
            self._values[values_flag][column_id] = value
    
    def _skip_reporting(self):
        if self._source.is_bo_process():
            LOGGER.info('Reporting skipped, BO Confirmation.')
            return True
        return super(TradeWorker, self)._skip_reporting()
    
    def _calculate(self):
        pass
    
    def process(self):
        LOGGER.info('ATS Worker - processing started - %s.' % acm.Time.TimeNow())
        LOGGER.info('%s: %s' % (self._entity_id, self.__class__.__name__))
        LOGGER.info('Source type: %s' % self._source.record_type)
        self._get_amend_reason_and_type()
        if self._skip_reporting():
            LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())
            return
        self._calculate()
        for column_id in CALCULATED_COLUMNS:
            LOGGER.info('\tOriginal %s: %s' % (column_id, str(self._values['old'][column_id])))
            LOGGER.info('\tNew %s: %s' % (column_id, str(self._values['new'][column_id])))
        pnl_impact = self.calc_pnl_impact(self._entity.prfnbr, self._values)
        pnl_impact_fv = self.calc_pnl_impact(self._entity.prfnbr, self._values, True)
        output_converter = OutputConverter(self._entity, self._source)
        output_converter.create_output()
        output_converter.set_text('AmendReason', self._amend_reason)
        output_converter.set_text('CommentType', self._comment_type)
        output_converter.set_text('PLImpact', pnl_impact)
        output_converter.set_text('PLImpactFairValue', pnl_impact_fv)
        if is_fair_value(self._entity.prfnbr):
            output_converter.set_text('FairValuePortfolio', 'Yes')
        if self.cal_flag in CAL_FLAGS:
            output_converter.set_text('CALFlag', self.cal_flag)
        xml_string = output_converter.get_string()
        cal_output.write(xml_string)
        self.clear_calc_space()
        LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())


class TradeWorkerBackdate(TradeWorker):
    
    default_reason_key = 'backdate'
    cal_flag = 'B'
    
    def __init__(self, entity, source, old_entity=None):
        super(TradeWorkerBackdate, self).__init__(entity, source)
        self._old_entity = old_entity
    
    def _skip_reporting(self):
        return False
    
    def _get_amend_reason_and_type(self):
        if not self._source.operation == 'insert':
            super(TradeWorkerBackdate, self)._get_amend_reason_and_type()
            return
        amend_reason = get_add_info_value(self._entity, 'AmendReasonTrd')
        comment_type = get_add_info_value(self._entity, 'AmendReasonTypeTrd')
        if amend_reason and comment_type:
            self._amend_reason = amend_reason
            self._comment_type = comment_type
            return
        LOGGER.warning('Amend reason and type not found in TS, using default.')
        amend_reason, comment_type = self._amend_reason_and_type_default()
        self._amend_reason = amend_reason
        self._comment_type = comment_type
    
    def _calculate(self):
        self._calculate_values(self._entity, 'new')
        if self._old_entity:
            self._calculate_values(self._old_entity, 'old')


class TradeWorkerLate(TradeWorker):
    
    cal_flag = 'L'
    
    def _calculate(self):
        self._calculate_values(self._entity, 'new')


class TradeWorkerVoid(TradeWorker):
    
    cal_flag = 'C'
    
    def _skip_reporting(self):
        return False
    
    def _calculate(self):
        self._calculate_values(self._entity, 'old')


class TradeWorkerUpdate(TradeWorker):
    
    cal_flag = 'A'
    
    def __init__(self, entity, old_entity, source):
        super(TradeWorkerUpdate, self).__init__(entity, source)
        self._old_entity = old_entity
    
    def _calculate(self):
        if self._source.skip_calculation():
            LOGGER.info('Calculation skipped.')
            return
        self._calculate_values(self._entity, 'new')
        self._calculate_values(self._old_entity, 'old')


class InstrumentWorker(Worker):
    
    def __init__(self, entity, old_entity, source, trades=None):
        super(InstrumentWorker, self).__init__(entity, source)
        self._entity_id = entity.insaddr
        self._old_entity = old_entity
        self._trades = trades if trades else entity.trades()
        self._values = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    
    def _amend_reason_and_type_default(self):
        instype = self._entity.instype
        if instype in DEFAULT_MAPPING_INS:
            for func in DEFAULT_MAPPING_INS[instype]:
                if func(self._entity):
                    return DEFAULT_MAPPING_INS[instype][func]
        return super(InstrumentWorker, self)._amend_reason_and_type_default()
    
    def _calculate_values(self, values_flag, ael_ins):
        for trade in self._trades:
            if not is_trade_valid_backend(trade):
                continue
            trade_clone = trade.clone()
            trade_clone.insaddr = ael_ins
            try:
                acm_trade = acm.Ael.AelToFObject(trade_clone)
            except Exception as exc:
                acm_trade = None
                msg = 'Failed to convert ael trade "%s" to acm: %s'
                LOGGER.warning(msg % (trade.trdnbr, str(exc)))
            for column_id in CALCULATED_COLUMNS:
                try:
                    value = self.calculate_value(acm_trade, column_id)
                except Exception as exc:
                    value = float('nan')
                    msg = 'Failed to calculate "%s" for trade %s: %s'
                    LOGGER.warning(msg % (column_id, trade.trdnbr, str(exc)))
                self._values[trade.trdnbr][values_flag][column_id] = value
    
    def _calculate(self):
        if self._source.skip_calculation():
            LOGGER.info('Calculation skipped.')
            return
        self._calculate_values('new', self._entity)
        self._calculate_values('old', self._old_entity)
    
    def process(self):
        LOGGER.info('ATS Worker - processing started - %s.' % acm.Time.TimeNow())
        LOGGER.info('%s: %s' % (self._entity_id, self.__class__.__name__))
        LOGGER.info('Source type: %s' % self._source.record_type)
        self._get_amend_reason_and_type()
        if self._skip_reporting():
            LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())
            return
        self._calculate()
        for trade_num in self._values:
            ael_trade = ael.Trade[int(trade_num)]
            if not ael_trade:
                continue
            LOGGER.info('%s: %s' % (trade_num, self.__class__.__name__))
            for column_id in CALCULATED_COLUMNS:
                LOGGER.info('\tOriginal %s: %s' % (column_id, str(self._values[trade_num]['old'][column_id])))
                LOGGER.info('\tNew %s: %s' % (column_id, str(self._values[trade_num]['new'][column_id])))
            pnl_impact = self.calc_pnl_impact(ael_trade.prfnbr, self._values[trade_num])
            pnl_impact_fv = self.calc_pnl_impact(ael_trade.prfnbr, self._values[trade_num], True)
            output_converter = OutputConverter(ael_trade, self._source)
            output_converter.create_output()
            output_converter.set_text('AmendReason', self._amend_reason)
            output_converter.set_text('CommentType', self._comment_type)
            output_converter.set_text('PLImpact', pnl_impact)
            output_converter.set_text('PLImpactFairValue', pnl_impact_fv)
            if is_fair_value(ael_trade.prfnbr):
                output_converter.set_text('FairValuePortfolio', 'Yes')
            xml_string = output_converter.get_string()
            cal_output.write(xml_string)
        self.clear_calc_space()
        LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())


class Listener(object):
    
    ignore_columns = ()
    
    def __init__(self, entity, old_entity, operation):
        self._entity = entity
        self._old_entity = old_entity
        self._operation = operation

    @classmethod
    def copy_values(cls, old_entity, new_entity):
        for column in old_entity.columns():
            if column in cls.ignore_columns:
                continue
            try:
                setattr(new_entity, column, getattr(old_entity, column))
            except Exception as exc:
                LOGGER.info('Failed to set "%s": %s' % (column, str(exc)))


class TradeListener(Listener):
    
    ignore_columns = (
        'trdnbr',
    )
    
    def process(self):
        new_valid = is_trade_valid_backend(self._entity)
        source = AmendmentSource(self._entity, self._operation, 'trdnbr')
        if not source.is_valid():
            msg = 'Invalid source: %s %s, operation %s.'
            LOGGER.info(msg % (source.record_type, source.entity_id, source.operation))
            return
        if self._operation == 'insert':
            if not new_valid:
                return
            if is_backdate(self._entity):
                return TradeWorkerBackdate(self._entity.clone(), source)
            if is_late(self._entity):
                return TradeWorkerLate(self._entity.clone(), source)
        if self._operation == 'update':
            old_valid = is_trade_valid_backend(self._old_entity)
            if not new_valid and not old_valid:
                return
            if (self._entity.status in INITIAL_STATUS + ('Void',)
                    and self._old_entity.status in INITIAL_STATUS 
                    and booked_today(self._entity)):
                msg = 'Ignoring Trade %s, trade %s %s and booked today.'
                LOGGER.info(msg % (self._operation, self._entity.status, self._entity.trdnbr))
                return
            source.check_differences(self._entity, self._old_entity)
            if not source.differences:
                return
            new_backdated = is_backdate(self._entity)
            old_backdated = is_backdate(self._old_entity)
            old_entity_clone = self._entity.clone()
            self.copy_values(self._old_entity, old_entity_clone)
            if new_valid and not old_valid:
                if new_backdated:
                    return TradeWorkerBackdate(self._entity.clone(), source)
                return
            if not new_valid and old_valid:
                return TradeWorkerVoid(self._old_entity.clone(), source)
            if new_backdated and not old_backdated:
                return TradeWorkerBackdate(self._entity.clone(), source, old_entity_clone)
            return TradeWorkerUpdate(self._entity.clone(), old_entity_clone, source)


class InstrumentListener(Listener):
    
    ignore_columns = (
        'insaddr',
    )
    
    def process(self):
        if not is_ins_valid_backend(self._entity):
            return
        trades = self._entity.trades()
        if not trades:
            return
        if self._operation == 'update':
            if created_today(self._entity):
                msg = 'Ignoring Instrument %s, instrument %s created today.'
                LOGGER.info(msg % (self._operation, self._entity.insid))
                return
            source = AmendmentSource(self._entity, self._operation, 'insaddr')
            if not source.is_valid(self._entity):
                msg = 'Invalid source: %s %s, operation %s.'
                LOGGER.info(msg % (source.record_type, source.entity_id, source.operation))
                return
            source.check_differences(self._entity, self._old_entity)
            if not source.differences:
                return
            old_entity_clone = self._entity.clone()
            self.copy_values(self._old_entity, old_entity_clone)
            return InstrumentWorker(self._entity.clone(), old_entity_clone, source, trades)


class PaymentListener(Listener):
    
    ignore_columns = (
        'trdnbr',
        'paynbr',
    )
    
    @classmethod
    def get_updated_entity(cls, trade, entity):
        for payment in trade.payments():
            if payment.paynbr == entity.paynbr:
                return payment
    
    @classmethod
    def revert_delete(cls, trade, deleted_entity):
        new_payment = ael.Payment.new(trade)
        cls.copy_values(deleted_entity, new_payment)
    
    def process(self):
        trade = self._entity.trdnbr
        if not is_trade_valid_backend(trade):
            return
        if trade.status in INITIAL_STATUS and booked_today(trade):
            msg = 'Ignoring Payment %s, trade %s %s and booked today.'
            LOGGER.info(msg % (self._operation, trade.status, trade.trdnbr))
            return
        trade_clone = trade.clone()
        source = AmendmentSource(self._entity, self._operation, 'paynbr')
        if not source.is_valid() and not self._operation == 'delete':
            msg = 'Invalid source: %s %s, operation %s.'
            LOGGER.info(msg % (source.record_type, source.entity_id, source.operation))
            return
        if self._operation == 'update':
            source.check_differences(self._entity, self._old_entity)
            if not source.differences:
                return
            entity_clone = self.get_updated_entity(trade_clone, self._old_entity)
            if not entity_clone:
                return
            self.copy_values(self._old_entity, entity_clone)
            return TradeWorkerUpdate(trade.clone(), trade_clone, source)
        if self._operation == 'insert':
            if not trade.creat_time < self._entity.creat_time:
                return
            entity_clone = self.get_updated_entity(trade_clone, self._entity)
            if not entity_clone:
                return
            entity_clone.delete()
            return TradeWorkerUpdate(trade.clone(), trade_clone, source)
        if self._operation == 'delete':
            source = AmendmentSource(self._entity, self._operation, 'paynbr', 
                                     trade.updat_usrnbr, trade.updat_time)
            if not source.is_valid():
                msg = 'Invalid source: %s %s, operation %s.'
                LOGGER.info(msg % (source.record_type, source.entity_id, source.operation))
                return
            try:
                self.revert_delete(trade_clone, self._entity)
            except Exception as exc:
                msg = '%s, %s: Failed to revert deleted object in listener: %s'
                LOGGER.warning(msg % (source.record_type, source.entity_id, str(exc)))
                return
            return TradeWorkerUpdate(trade.clone(), trade_clone, source)


class CfBaseListener(Listener):
    
    """Listener base class for CashFlow instrument child entities."""
    
    oid_attr = ''
    process_insert = False
    
    @classmethod
    def get_ins(cls, entity):
        raise NotImplementedError
    
    @classmethod
    def get_updated_entity(cls, ins, entity):
        raise NotImplementedError
    
    @classmethod
    def revert_delete(cls, ins, deleted_entity):
        raise NotImplementedError
    
    def process(self):
        ins = self.get_ins(self._entity)
        if not is_ins_valid_backend(ins):
            return
        trades = ins.trades()
        if not trades:
            return
        ins_clone = ins.clone()
        source = AmendmentSource(self._entity, self._operation, self.oid_attr)
        if not source.is_valid(ins) and not self._operation == 'delete':
            msg = 'Invalid source: %s %s, operation %s.'
            LOGGER.info(msg % (source.record_type, source.entity_id, source.operation))
            return
        if created_today(ins):
            msg = 'Ignoring %s %s, instrument %s created today.'
            LOGGER.info(msg % (self._entity.record_type, self._operation, ins.insid))
            return
        if self._operation == 'update':
            source.check_differences(self._entity, self._old_entity)
            if not source.differences:
                return
            entity_clone = self.get_updated_entity(ins_clone, self._old_entity)
            if not entity_clone:
                return
            self.copy_values(self._old_entity, entity_clone)
            return InstrumentWorker(ins.clone(), ins_clone, source, trades)
        if self._operation == 'insert':
            if not self.process_insert:
                return
            if not ins.creat_time < self._entity.creat_time:
                return
            entity_clone = self.get_updated_entity(ins_clone, self._entity)
            if not entity_clone:
                return
            entity_clone.delete()
            return InstrumentWorker(ins.clone(), ins_clone, source, trades)
        if self._operation == 'delete':
            source = AmendmentSource(self._entity, self._operation, self.oid_attr, 
                                     ins.updat_usrnbr, ins.updat_time)
            if not source.is_valid(ins):
                msg = 'Invalid source: %s %s, operation %s.'
                LOGGER.info(msg % (source.record_type, source.entity_id, source.operation))
                return
            try:
                self.revert_delete(ins_clone, self._entity)
            except Exception as exc:
                msg = '%s, %s: Failed to revert deleted object in listener: %s'
                LOGGER.warning(msg % (source.record_type, source.entity_id, str(exc)))
                return
            return InstrumentWorker(ins.clone(), ins_clone, source, trades)


class LegListener(CfBaseListener):

    ignore_columns = (
        'insaddr',
        'legnbr',
    )
    oid_attr = 'legnbr'
    
    @classmethod
    def get_ins(cls, entity):
        return entity.insaddr
    
    @classmethod
    def get_updated_entity(cls, ins, entity):
        for leg in ins.legs():
            if leg.legnbr == entity.legnbr:
                return leg
    
    @classmethod
    def revert_delete(cls, ins, deleted_entity):
        new_leg = ael.Leg.new(ins)
        cls.copy_values(deleted_entity, new_leg)
        for cfw in deleted_entity.cash_flows():
            new_cfw = ael.CashFlow.new(new_leg)
            CashFlowListener.copy_values(cfw, new_cfw)
            for reset in cfw.resets():
                new_reset = ael.Reset.new(new_cfw)
                ResetListener.copy_values(reset, new_reset)


class CashFlowListener(CfBaseListener):

    ignore_columns = (
        'legnbr',
        'cfwnbr',
    )
    oid_attr = 'cfwnbr'
    process_insert = True
    
    @classmethod
    def get_ins(cls, entity):
        leg = entity.legnbr
        if not leg:
            return
        return LegListener.get_ins(leg)
    
    @classmethod
    def get_updated_entity(cls, ins, entity):
        for leg in ins.legs():
            for cfw in leg.cash_flows():
                if cfw.cfwnbr == entity.cfwnbr:
                    return cfw
    
    @classmethod
    def get_parent_entity(cls, ins, entity):
        for leg in ins.legs():
            if leg.legnbr == entity.legnbr.legnbr:
                return leg
    
    @classmethod
    def revert_delete(cls, ins, deleted_entity):
        leg = cls.get_parent_entity(ins, deleted_entity)
        if not leg:
            return
        new_cfw = ael.CashFlow.new(leg)
        cls.copy_values(deleted_entity, new_cfw)
        for reset in deleted_entity.resets():
            new_reset = ael.Reset.new(new_cfw)
            ResetListener.copy_values(reset, new_reset)


class ResetListener(CfBaseListener):

    ignore_columns = (
        'legnbr',
        'cfwnbr',
        'resnbr',
    )
    oid_attr = 'resnbr'
    
    @classmethod
    def get_ins(cls, entity):
        cfw = entity.cfwnbr
        if not cfw:
            return
        return CashFlowListener.get_ins(cfw)
    
    @classmethod
    def get_updated_entity(cls, ins, entity):
        for leg in ins.legs():
            for cfw in leg.cash_flows():
                for reset in cfw.resets():
                    if reset.resnbr == entity.resnbr:
                        return reset
    
    @classmethod
    def get_parent_entity(cls, ins, entity):
        for leg in ins.legs():
            for cfw in leg.cash_flows():
                if cfw.cfwnbr == entity.cfwnbr.cfwnbr:
                    return cfw
    
    @classmethod
    def revert_delete(cls, ins, deleted_entity):
        cfw = cls.get_parent_entity(ins, deleted_entity)
        if not cfw:
            return
        new_reset = ael.Reset.new(cfw)
        cls.copy_values(deleted_entity, new_reset)


def listener(_object, entity, _args, operation):
    if acm.Time.TimeNow()[11:] > ATS_PARAMS['cutoff'] and ATS_PARAMS['subscribed']:
        unsubscribe()
        return
    if not entity:
        return
    worker = None
    old_entity = None
    try:
        old_entity = ael.get_old_entity()
    except:
        LOGGER.exception('Failed to retrieve old entity in listener.')
    
    if entity.record_type == 'Trade':
        trade_listener = TradeListener(entity, old_entity, operation)
        try:
            worker = trade_listener.process()
        except:
            LOGGER.exception('TradeListener failed.')
            return
    elif entity.record_type == 'Payment':
        payment_listener = PaymentListener(entity, old_entity, operation)
        try:
            worker = payment_listener.process()
        except:
            LOGGER.exception('PaymentListener failed.')
            return
    elif entity.record_type == 'Instrument':
        ins_listener = InstrumentListener(entity, old_entity, operation)
        try:
            worker = ins_listener.process()
        except:
            LOGGER.exception('InstrumentListener failed.')
            return
    elif entity.record_type == 'Leg':
        leg_listener = LegListener(entity, old_entity, operation)
        try:
            worker = leg_listener.process()
        except:
            LOGGER.exception('LegListener failed.')
            return
    elif entity.record_type == 'CashFlow':
        cfw_listener = CashFlowListener(entity, old_entity, operation)
        try:
            worker = cfw_listener.process()
        except:
            LOGGER.exception('CashFlowListener failed.')
            return
    elif entity.record_type == 'Reset':
        reset_listener = ResetListener(entity, old_entity, operation)
        try:
            worker = reset_listener.process()
        except:
            LOGGER.exception('ResetListener failed.')
            return
    if worker:
        worker_queue.put(worker)


def subscribe():
    if ATS_PARAMS['table'] == 'Trade' or not ATS_PARAMS['table']:
        ael.Trade.subscribe(listener)
        LOGGER.info('ATS subscribed Trade at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Payment' or not ATS_PARAMS['table']:
        ael.Payment.subscribe(listener)
        LOGGER.info('ATS subscribed Payment at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Instrument' or not ATS_PARAMS['table']:
        ael.Instrument.subscribe(listener)
        LOGGER.info('ATS subscribed Instrument at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Leg' or not ATS_PARAMS['table']:
        ael.Leg.subscribe(listener)
        LOGGER.info('ATS subscribed Leg at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'CashFlow' or not ATS_PARAMS['table']:
        ael.CashFlow.subscribe(listener)
        LOGGER.info('ATS subscribed CashFlow at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Reset' or not ATS_PARAMS['table']:
        ael.Reset.subscribe(listener)
        LOGGER.info('ATS subscribed Reset at %s.' % acm.Time.TimeNow())
    ATS_PARAMS['subscribed'] = True


def unsubscribe():
    if ATS_PARAMS['table'] == 'Trade' or not ATS_PARAMS['table']:
        ael.Trade.unsubscribe(listener)
        LOGGER.info('ATS unsubscribed Trade at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Payment' or not ATS_PARAMS['table']:
        ael.Payment.unsubscribe(listener)
        LOGGER.info('ATS unsubscribed Payment at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Instrument' or not ATS_PARAMS['table']:
        ael.Instrument.unsubscribe(listener)
        LOGGER.info('ATS unsubscribed Instrument at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Leg' or not ATS_PARAMS['table']:
        ael.Leg.unsubscribe(listener)
        LOGGER.info('ATS unsubscribed Leg at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'CashFlow' or not ATS_PARAMS['table']:
        ael.CashFlow.unsubscribe(listener)
        LOGGER.info('ATS unsubscribed CashFlow at %s.' % acm.Time.TimeNow())
    if ATS_PARAMS['table'] == 'Reset' or not ATS_PARAMS['table']:
        ael.Reset.unsubscribe(listener)
        LOGGER.info('ATS unsubscribed Reset at %s.' % acm.Time.TimeNow())
    ATS_PARAMS['subscribed'] = False


def start():
    cal_output.init_file(ATS_PARAMS['path'])
    LOGGER.info('Init output file %s' % ATS_PARAMS['path'])
    ATS_PARAMS['closed'] = False
    subscribe()


def start_ex(params):
    ATS_PARAMS['table'] = params['table']
    ATS_PARAMS['cutoff'] = params['cutoff']
    output_path = get_output_path(params['output_dir'], params['output_file'], DATE_TODAY)
    ATS_PARAMS['path'] = output_path
    start()


def status():
    pass


def work():
    if acm.Time.TimeNow()[11:] > ATS_PARAMS['cutoff'] and ATS_PARAMS['subscribed']:
        unsubscribe()
    if not worker_queue.empty() and ATS_PARAMS['closed']:
        cal_output.init_file()
        ATS_PARAMS['closed'] = False
        LOGGER.info('CAL output init at %s.' % acm.Time.TimeNow())
    while not worker_queue.empty():
        worker = worker_queue.get()
        if not worker:
            continue
        worker.process()
        # Process only one item at a time if still subscribed
        if ATS_PARAMS['subscribed']:
            break
    if (not ATS_PARAMS['subscribed'] and worker_queue.empty() 
            and not ATS_PARAMS['closed']):
        cal_output.close_file()
        ATS_PARAMS['closed'] = True
        LOGGER.info('CAL output closed at %s.' % acm.Time.TimeNow())
    
