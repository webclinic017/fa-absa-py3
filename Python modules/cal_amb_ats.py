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
"""
import datetime
import os
from collections import defaultdict

import acm
import amb
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_ats_utils import AmbConnection, XmlOutput
from cal_amb_util import (OutputConverter, AmendmentSource, AmbaMessageCal,
                          is_trade_valid_backend, is_fair_value, 
                          get_late_cutoff)
from cal_amb_config import (INITIAL_STATUS, CALC_CURRENCY, DEFAULTS,
                            USRNBR_EXCLUDE_BACKEND,
                            CALCULATED_COLUMNS,
                            CAL_FLAGS,
                            VALID_INSTYPE,
                            VALID_STATUS,
                            PRFTREE_EXCLUDE_BACKEND,
                            CAL_PARAMS_NAME)


LOGGER = getLogger(__name__)
AMB_CONNECTION = AmbConnection(CAL_PARAMS_NAME)

OUTPUT_FILE = 'CAL_AMB_{:%Y-%m-%d}.xml'
OUTPUT_DIR = (r'L:\FALOG\PRODA\ATS_CAL' if os.name == 'nt' 
                  else '/services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
ATS_PARAMS = {
    'path': OUTPUT_PATH,
    'calc_space': acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet'),
}

CAL_OUTPUT = {}


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


def simulate_globals(val_date):
    ATS_PARAMS['calc_space'].SimulateGlobalValue('Fixed Currency', CALC_CURRENCY)
    ATS_PARAMS['calc_space'].SimulateGlobalValue('Position Currency Choice', 'Fixed Curr')
    ATS_PARAMS['calc_space'].SimulateGlobalValue('Aggregate Currency Choice', 'Fixed Curr')
    ATS_PARAMS['calc_space'].SimulateGlobalValue('Valuation Date', val_date) 
    ATS_PARAMS['calc_space'].SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    ATS_PARAMS['calc_space'].SimulateGlobalValue('Portfolio Profit Loss End Date Custom', val_date)


def init_output(msg_date):
    dt = datetime.datetime(*acm.Time.DateToYMD(msg_date))
    output_path = ATS_PARAMS['path'].format(dt)
    output = XmlOutput()
    output.init_file(output_path)
    CAL_OUTPUT[msg_date] = output
    LOGGER.info('Init output file %s' % output_path)


def write_to_output(xml_string, msg_date):
    if not msg_date in CAL_OUTPUT:
        init_output(msg_date)
    CAL_OUTPUT[msg_date].write(xml_string)


class Worker(object):
    
    def __init__(self, source):
        self._entity = None
        self._source = source
        self._entity_id = source.entity_id
        self._amend_reason = source.amend_reason
        self._amend_type = source.amend_type
    
    @staticmethod
    def calc_pnl_impact(portfolio, values, fair_value=False):
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
    
    @staticmethod
    def calculate_value(acm_trade, column_id):
        value = ATS_PARAMS['calc_space'].CalculateValue(acm_trade, column_id)
        return float(value)
    
    @staticmethod
    def set_calc_space(val_date):
        acm.PollDbEvents()
        try:
            ATS_PARAMS['calc_space'].Clear()
            simulate_globals(val_date)
            ATS_PARAMS['calc_space'].Refresh()
        except:
            LOGGER.exception('Reinitialize calc space.')
            ATS_PARAMS['calc_space'] = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
            simulate_globals(val_date)
    
    def _uses_default_reason(self):
        for amend_reason, amend_type in list(DEFAULTS.values()):
            if (self._amend_reason == amend_reason 
                    and self._amend_type == amend_type):
                return True
        return False
    
    def _skip_reporting(self):
        if (self._source.update_user.Oid() in USRNBR_EXCLUDE_BACKEND 
                and self._uses_default_reason()):
            msg = 'Reporting skipped. Non-PRIME amendment by %s.'
            LOGGER.info(msg % self._source.update_user.Name())
            return True
        if not self._amend_reason or not self._amend_type:
            msg = 'Reporting skipped. Amend reason or type not specified.'
            LOGGER.error(msg)
            return True
        return False


class TradeWorker(Worker):
    
    cal_flag = ''
    
    def __init__(self, source):
        super(TradeWorker, self).__init__(source)
        self._values = defaultdict(lambda: defaultdict(float))
    
    def _calculate_values(self, entity, values_flag):
        for column_id in CALCULATED_COLUMNS:
            try:
                value = self.calculate_value(entity, column_id)
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
        if self._skip_reporting():
            LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())
            return
        self.set_calc_space(self._source.msg_date)
        self._calculate()
        for column_id in CALCULATED_COLUMNS:
            LOGGER.info('\tOriginal %s: %s' % (column_id, str(self._values['old'][column_id])))
            LOGGER.info('\tNew %s: %s' % (column_id, str(self._values['new'][column_id])))
        pnl_impact = self.calc_pnl_impact(self._entity.Portfolio(), self._values)
        pnl_impact_fv = self.calc_pnl_impact(self._entity.Portfolio(), self._values, True)
        output_converter = OutputConverter(self._entity, self._source)
        output_converter.create_output()
        output_converter.set_text('AmendReason', self._amend_reason)
        output_converter.set_text('CommentType', self._amend_type)
        output_converter.set_text('PLImpact', pnl_impact)
        output_converter.set_text('PLImpactFairValue', pnl_impact_fv)
        if is_fair_value(self._entity.Portfolio()):
            output_converter.set_text('FairValuePortfolio', 'Yes')
        if self.cal_flag in CAL_FLAGS:
            output_converter.set_text('CALFlag', self.cal_flag)
        xml_string = output_converter.get_string()
        write_to_output(xml_string, self._source.msg_date)
        LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())


class TradeWorkerBackdate(TradeWorker):
    
    cal_flag = 'B'
    
    def __init__(self, source, old_entity=False):
        super(TradeWorkerBackdate, self).__init__(source)
        self._old_entity = old_entity
    
    def _skip_reporting(self):
        if not self._amend_reason or not self._amend_type:
            msg = 'Reporting skipped. Amend reason or type not specified.'
            LOGGER.error(msg)
            return True
        return False
    
    def _calculate(self):
        current_msg_string = self._source.msg_object.get_current_message()
        self._entity = acm.AMBAMessage.CreateCloneFromMessage(current_msg_string)
        self._calculate_values(self._entity, 'new')
        if self._old_entity:
            previous_msg_string = self._source.msg_object.get_previous_message()
            old_entity = acm.AMBAMessage.CreateCloneFromMessage(previous_msg_string)
            self._calculate_values(old_entity, 'old')


class TradeWorkerLate(TradeWorker):
    
    cal_flag = 'L'
    
    def _calculate(self):
        current_msg_string = self._source.msg_object.get_current_message()
        self._entity = acm.AMBAMessage.CreateCloneFromMessage(current_msg_string)
        self._calculate_values(self._entity, 'new')


class TradeWorkerUpdate(TradeWorker):
    
    cal_flag = 'A'
    
    def _calculate(self):
        current_msg_string = self._source.msg_object.get_current_message()
        self._entity = acm.AMBAMessage.CreateCloneFromMessage(current_msg_string)
        if self._source.skip_calculation():
            LOGGER.info('Calculation skipped.')
            return
        previous_msg_string = self._source.msg_object.get_previous_message()
        old_entity = acm.AMBAMessage.CreateCloneFromMessage(previous_msg_string)
        self._calculate_values(self._entity, 'new')
        self._calculate_values(old_entity, 'old')


class TradeWorkerVoid(TradeWorker):
    
    cal_flag = 'C'
    
    def _skip_reporting(self):
        if not self._amend_reason or not self._amend_type:
            msg = 'Reporting skipped. Amend reason or type not specified.'
            LOGGER.error(msg)
            return True
        return False
    
    def _calculate(self):
        previous_msg_string = self._source.msg_object.get_previous_message()
        self._entity = acm.AMBAMessage.CreateCloneFromMessage(previous_msg_string)
        self._calculate_values(self._entity, 'old')


class InstrumentWorker(Worker):
    
    def __init__(self, source):
        super(InstrumentWorker, self).__init__(source)
        self._trades = []
        self._values = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    
    def _calculate_values(self, values_flag, acm_ins):
        for trade in self._trades:
            if not is_trade_valid_backend(trade):
                continue
            trade_clone = trade.Clone()
            trade_clone.Instrument(acm_ins)
            for column_id in CALCULATED_COLUMNS:
                try:
                    value = self.calculate_value(trade_clone, column_id)
                except Exception as exc:
                    value = float('nan')
                    msg = 'Failed to calculate "%s" for trade %s: %s'
                    LOGGER.warning(msg % (column_id, trade.Oid(), str(exc)))
                self._values[trade.Oid()][values_flag][column_id] = value
    
    def _calculate(self):
        ins = acm.FInstrument[self._entity_id]
        self._trades = ins.Trades() if ins else []
        if not self._trades:
            LOGGER.info('Ignoring Instrument update, no trades found.')
            return
        current_msg_string = self._source.msg_object.get_current_message()
        self._entity = acm.AMBAMessage.CreateCloneFromMessage(current_msg_string)
        previous_msg_string = self._source.msg_object.get_previous_message()
        old_entity = acm.AMBAMessage.CreateCloneFromMessage(previous_msg_string)
        self._calculate_values('new', self._entity)
        self._calculate_values('old', old_entity)
    
    def process(self):
        LOGGER.info('ATS Worker - processing started - %s.' % acm.Time.TimeNow())
        LOGGER.info('%s: %s' % (self._entity_id, self.__class__.__name__))
        LOGGER.info('Source type: %s' % self._source.record_type)
        if self._skip_reporting():
            LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())
            return
        self.set_calc_space(self._source.msg_date)
        self._calculate()
        for trade_num in self._values:
            acm_trade = acm.FTrade[int(trade_num)]
            if not acm_trade:
                continue
            LOGGER.info('%s: %s' % (trade_num, self.__class__.__name__))
            for column_id in CALCULATED_COLUMNS:
                LOGGER.info('\tOriginal %s: %s' % (column_id, str(self._values[trade_num]['old'][column_id])))
                LOGGER.info('\tNew %s: %s' % (column_id, str(self._values[trade_num]['new'][column_id])))
            pnl_impact = self.calc_pnl_impact(acm_trade.Portfolio(), self._values[trade_num])
            pnl_impact_fv = self.calc_pnl_impact(acm_trade.Portfolio(), self._values[trade_num], True)
            output_converter = OutputConverter(acm_trade, self._source)
            output_converter.create_output()
            output_converter.set_text('AmendReason', self._amend_reason)
            output_converter.set_text('CommentType', self._amend_type)
            output_converter.set_text('PLImpact', pnl_impact)
            output_converter.set_text('PLImpactFairValue', pnl_impact_fv)
            if is_fair_value(acm_trade.Portfolio()):
                output_converter.set_text('FairValuePortfolio', 'Yes')
            xml_string = output_converter.get_string()
            write_to_output(xml_string, self._source.msg_date)
        LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())


class MessageProcessor(object):
    
    def __init__(self, msg_object):
        self._msg_object = msg_object
        self._table_name = msg_object.table_name
        self._operation = msg_object.operation
        self._table = msg_object.parent_table
        self._msg_date = self._get_value('UPDAT_TIME')[:10]
    
    @staticmethod
    def ins_valid(instype, open_end=''):
        if instype not in VALID_INSTYPE:
            return False
        if instype == 'Deposit' and open_end == 'Open End':
            return False
        return True
    
    @classmethod
    def trade_valid(cls, status, prfid, instype):
        if not cls.ins_valid(instype):
            return False
        if not status in VALID_STATUS:
            return False
        if any([tree.has(prfid) for tree in PRFTREE_EXCLUDE_BACKEND]):
            return False
        return True
    
    def _get_value(self, field_name, state='current'):
        if not field_name in self._table.attributes:
            msg = 'Attribute "%s" not included in the AMBA message.'
            LOGGER.warning(msg % field_name)
            return ''
        if state == 'current':
            return self._table.attributes[field_name]['current']
        if state == 'previous':
            previous_value = self._table.attributes[field_name]['previous']
            if previous_value:
                return previous_value
            return self._table.attributes[field_name]['current']
        msg = 'Invalid attribute state "%s", "current" or "previous" expected.' % state
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    def _get_oid(self):
        if self._table_name == 'TRADE':
            return int(self._get_value('TRDNBR'))
        if self._table_name == 'INSTRUMENT':
            return int(self._get_value('INSADDR'))
        msg = 'Invalid table "%s", TRADE or INSTRUMENT expected.' % self._table_name
        LOGGER.error(msg)
        raise RuntimeError(msg)
    
    def _created_today(self, state='current'):
        return self._get_value('CREAT_TIME', state)[:10] == self._msg_date
    
    def _is_backdate(self, state='current'):
        return self._get_value('VALUE_DAY', state)[:10] < self._msg_date
    
    def _is_late(self, state='current'):
        late_cutoff = get_late_cutoff(self._msg_date)
        return self._get_value('CREAT_TIME', state) > late_cutoff
    
    def _booked_today(self, state='current'):
        return self._get_value('TIME', state)[:10] == self._msg_date
    
    def _process_instrument(self):
        if not self._operation == 'UPDATE':
            return
        oid = self._get_oid()
        insid = self._get_value('INSID')
        if oid < 0:
            msg = 'Ignoring Instrument %s, %s has negative Oid.'
            LOGGER.info(msg % (self._operation, insid))
            return
        instype = self._get_value('INSTYPE')
        open_end = self._get_value('OPEN_END')
        if not self.ins_valid(instype, open_end):
            return
        if self._created_today():
            msg = 'Ignoring Instrument %s, %s created today.'
            LOGGER.info(msg % (self._operation, insid))
            return
        source = AmendmentSource(oid, self._msg_object)
        source.check_differences()
        if not source.differences:
            msg = 'Ignoring Instrument %s, no differences found for %s.'
            LOGGER.info(msg % (self._operation, insid))
            return
        return InstrumentWorker(source)
    
    def _process_trade(self):
        oid = self._get_oid()
        if oid < 0:
            msg = 'Ignoring Trade %s, %s has negative Oid.'
            LOGGER.info(msg % (self._operation, oid))
            return
        new_status = self._get_value('STATUS')
        new_prfid = self._get_value('PRFNBR.PRFID')
        instype = self._get_value('INSADDR.INSTYPE')
        new_valid = self.trade_valid(new_status, new_prfid, instype)
        if self._operation == 'INSERT':
            if not new_valid:
                return
            if self._is_backdate():
                source = AmendmentSource(oid, self._msg_object)
                return TradeWorkerBackdate(source)
            if self._is_late():
                source = AmendmentSource(oid, self._msg_object)
                return TradeWorkerLate(source)
        if self._operation == 'UPDATE':
            old_status = self._get_value('STATUS', 'previous')
            old_prfid = self._get_value('PRFNBR.PRFID', 'previous')
            old_valid = self.trade_valid(old_status, old_prfid, instype)
            if not new_valid and not old_valid:
                return
            if (new_status in INITIAL_STATUS + ('Void',)
                    and old_status in INITIAL_STATUS and self._booked_today()):
                msg = 'Ignoring Trade %s, trade %s %s and booked today.'
                LOGGER.info(msg % (self._operation, oid, new_status))
                return
            source = AmendmentSource(oid, self._msg_object)
            source.check_differences()
            if not source.differences:
                msg = 'Ignoring Trade %s, trade %s. No differences found.'
                LOGGER.info(msg % (self._operation, oid))
                return
            new_backdated = self._is_backdate()
            old_backdated = self._is_backdate('previous')
            if new_valid and not old_valid and not new_backdated:
                return
            if new_valid and not old_valid:
                return TradeWorkerBackdate(source)
            if not new_valid and old_valid:
                return TradeWorkerVoid(source)
            if new_backdated and not old_backdated:
                return TradeWorkerBackdate(source, True)
            return TradeWorkerUpdate(source)
    
    def process(self):
        if self._table_name == 'TRADE':
            return self._process_trade()
        elif self._table_name == 'INSTRUMENT':
            return self._process_instrument()


def start():
    simulate_globals(acm.Time.DateToday())
    AMB_CONNECTION.connect()
    init_output(acm.Time.DateToday())


def start_ex(params):
    output_path = os.path.join(params['output_dir'], params['output_file'])
    ATS_PARAMS['path'] = output_path
    start()


def stop():
    for output in list(CAL_OUTPUT.values()):
        output.close_file()
        LOGGER.info('%s closed at %s.' % (output.get_path(), acm.Time.TimeNow()))


def work():
    while not AMB_CONNECTION.queue.empty():
        event, channel_number, amb_message_number = AMB_CONNECTION.queue.get()
        LOGGER.info('Started processing: %s' % amb_message_number)
        message_buffer = amb.mbf_create_buffer_from_data(event.data_p)
        amba_message = message_buffer.mbf_read()
        msg_object = AmbaMessageCal(amba_message)
        worker = None
        try:
            msg_processor = MessageProcessor(msg_object)
            worker = msg_processor.process()
        except: 
             LOGGER.exception('Message processing failed.')
        if worker:
            try:
                worker.process()
            except: 
                LOGGER.exception('Worker processing failed.')
        amb.mb_queue_accept(channel_number, event, str(amb_message_number))
        amba_message.mbf_destroy_object()
        message_buffer.mbf_destroy_buffer()
        LOGGER.info('Processing done: %s' % amb_message_number)
    
    if AMB_CONNECTION.disconnected and AMB_CONNECTION.queue.empty():
        AMB_CONNECTION.connect()
