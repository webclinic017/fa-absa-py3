"""-----------------------------------------------------------------------------
PURPOSE              :  Sparks ATS listener to capture intraday amendments,
                        backdates and reversals.
REQUESTER, DEPATMENT :  Linda Breytenbach, OPS
PROJECT              :  Fix the Front - Sparks
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2018-07-19  CHG1000679237  Libor Svoboda       Initial Implementation
"""
import ael
import acm
from queue import Queue
from Sparks_Config import SparksConfig
from Sparks_Util import SparksUtil, SUPPRESSED_CURR, DEPO_SUPPRESSIONS
from midasSettlement import midas_settlement
from at_logging import getLogger
''' AMD-434. '''
import re


LOGGER = getLogger(__name__)

AEL_DATE_TODAY = ael.date_today()
AEL_CALENDAR = ael.Calendar['ZAR Johannesburg']
AEL_NEXT_BUS_DAY = AEL_DATE_TODAY.add_banking_day(AEL_CALENDAR, 1)
AEL_FIVE_BUS_DAYS_AGO = AEL_DATE_TODAY.add_banking_day(AEL_CALENDAR, -5)
AEL_BACKDATE_START = AEL_DATE_TODAY.add_days(-30)

ACM_DATE_TODAY = acm.Time.DateToday()
ACM_CALENDAR = acm.FCalendar['ZAR Johannesburg']
ACM_NEXT_BUS_DAY = ACM_CALENDAR.AdjustBankingDays(ACM_DATE_TODAY, 1)
ACM_BACKDATE_START = acm.Time.DateAddDelta(ACM_DATE_TODAY, 0, 0, -30)

CONFIG = SparksConfig()
NEXT_DAY_CURR = CONFIG.next_day_currencies
VALID_STATUS = (
    'BO Confirmed',
    'BO-BO Confirmed',
    'FO Confirmed',
    'Terminated',
)
IGNORED_TRADE_FIELDS = (
    'updat_time',
    'updat_usrnbr',
    'version_id',
    'trader_usrnbr',
    'group_trdnbr',
)

worker_queue = Queue()
sparks_util = SparksUtil(ACM_DATE_TODAY, 'listener')


def get_paynbrs(ael_trade):
    if not ael_trade:
        return []
    try:
        return [pay.paynbr for pay in ael_trade.payments()]
    except:
        LOGGER.exception('Failed to get payments.')
        return []


class Worker(object):
    
    def __init__(self, entity):    
        self._entity = entity
        self._old_mf_ids = []
        self._new_mf_objects = []
        self._mf_ids_to_reverse = []
        self._mfs_to_post = []
        self._record_type = entity.record_type if entity else ''
        self._create_time = acm.Time.TimeNow()
    
    def __str__(self):
        text = ''
        text += 'Record Type: %s\n' % self._record_type
        text += '%s\n' % self.__class__.__name__
        text += 'MF objects: %s\n' % len(self._new_mf_objects)
        for mf in self._new_mf_objects:
            text += '\t%s: %s\n' % (mf.Type(), self.get_moneyflow_id(mf))
        text += 'Old MF IDs: %s\n' % len(self._old_mf_ids)
        for mf_id in self._old_mf_ids:
            text += '\t%s\n' % mf_id
        text += 'Worker create time: %s' % self._create_time
        return text
    
    @classmethod
    def get_moneyflow_id(cls, mf):
        return SparksUtil.get_moneyflow_id(mf)
    
    def _get_moneyflows_from_entity(self, entity=None):
        entity = entity if entity else self._entity
        try:
            acm_entity = acm.Ael.AelToFObject(entity)
        except Exception as exc:
            msg = '%s: Failed to convert Ael to FObject. %s'
            LOGGER.warning(msg % (self.__class__.__name__, str(exc)))
            return []
        if not acm_entity:
            return []
        trades = []
        if acm_entity.IsKindOf(acm.FPayment):
            trades = [acm_entity.Trade()]
        elif acm_entity.IsKindOf(acm.FCashFlow):
            trades = acm_entity.Leg().Instrument().Trades()
        moneyflows = []
        for trade in trades:
            if not TradeListener.is_acm_trade_valid(trade):
                continue
            ''' AMD-429.
                Generate money flows for cash flows that fall within active trade/instrument intervals. '''
            start_boundary = None
            end_boundary = None
            if trade.Instrument().Cid() == 'BasketRepo/Reverse':
                start_boundary = trade.Instrument().StartDate()
                end_boundary = trade.Instrument().EndDate()
            elif trade.TradeCategory() == 'Collateral': # Cash collateral Trades
                start_boundary = trade.AcquireDay()
                end_boundary = trade.ReAcquireDay()
            mf = acm.Risk.CreateMoneyFlowFromObject(acm_entity, trade)
            if start_boundary is not None and end_boundary is not None:
                if start_boundary <= acm_entity.PayDate() and acm_entity.PayDate() <= end_boundary:
                    moneyflows.append(mf)
            else: # For everything else, continue as before
                moneyflows.append(mf)
        return moneyflows
    
    def _preprocess_moneyflows(self):
        self._mf_ids_to_reverse = self._old_mf_ids
        self._mfs_to_post = self._new_mf_objects
        
        for mf in self._mfs_to_post:
            mf_id = self.get_moneyflow_id(mf)
            if mf_id in self._mf_ids_to_reverse:
                self._mf_ids_to_reverse.remove(mf_id)
                
    
    ''' AMD-434.
        Add missing coupon transfers for each coupon, for reversal, should they not be included. '''
    def add_reversal_cpt_mfs(self):
        cpt_mf_ids_to_reverse = []
        for mf_id in self._mf_ids_to_reverse:
            if 'CP' in mf_id and 'CPT' not in mf_id:
                mf_id_trade_id = re.findall('([0-9]+)', mf_id)[0]
                no_trade_id_mf_id = (re.findall('([A-Z]+[0-9_\-(Rev|V)]+)', mf_id)[0])[2:]
                cpt_mf_id = mf_id_trade_id + 'CPT' + no_trade_id_mf_id
                if cpt_mf_id not in self._mf_ids_to_reverse:
                    cpt_mf_ids_to_reverse.append(cpt_mf_id)
        if cpt_mf_ids_to_reverse:
            for mf_id in cpt_mf_ids_to_reverse:
                self._mf_ids_to_reverse.append(mf_id)


    ''' AMD-434.
        Add missing coupon transfers for each coupon, for posting, should they not be included. '''
    def add_posting_cpt_mfs(self):
        cpt_mfs_to_post = []
        for mf in self._mfs_to_post:
            mf_id = self.get_moneyflow_id(mf)
            if 'CP' in mf_id and 'CPT' not in mf_id: #cp mf id
                cp_mf_id = re.findall('([0-9]+)', mf_id)[1]
                cp_trade_id = re.findall('([0-9]+)', mf_id)[0]
                cp_trade_mfs = acm.FTrade[cp_trade_id].MoneyFlows()
                cpt_mf = None
                for cp_trade_mf in cp_trade_mfs:
                    if (hasattr(cp_trade_mf.SourceObject(), 'Oid')):
                        if (str(cp_trade_mf.SourceObject().Oid()) == cp_mf_id and cp_trade_mf.Type() == 'Coupon transfer'):
                            cpt_mf = cp_trade_mf
                if cpt_mf is not None and cpt_mf not in self._mfs_to_post:
                    cpt_mfs_to_post.append(cpt_mf)
        if cpt_mfs_to_post:
            for mf in cpt_mfs_to_post:
                self._mfs_to_post.append(mf)


    def process(self, void=False):
        LOGGER.info('ATS Worker - processing started - %s.' % acm.Time.TimeNow())
        LOGGER.info(self.__str__())
        self._preprocess_moneyflows()
        class_name = self.__class__.__name__
        self.add_reversal_cpt_mfs() #AMD-434
        for mf_id in self._mf_ids_to_reverse:
            try:
                sparks_util.reverse(mf_id, void)
            except Exception as exc:
                msg = '%s: Failed to reverse message %s. %s'
                LOGGER.exception(msg % (class_name, mf_id, str(exc)))
        self.add_posting_cpt_mfs() #AMD-434
        for mf in self._mfs_to_post:
            try:
                sparks_util.post(mf)
            except Exception as exc:
                mf_id = self.get_moneyflow_id(mf)
                msg = '%s: Failed to post message %s. %s'
                LOGGER.exception(msg % (class_name, mf_id, str(exc)))
        LOGGER.info('ATS Worker - processing done - %s.' % acm.Time.TimeNow())


class TradeWorker(Worker):    
    
    def _get_moneyflows_from_entity(self, entity=None):
        entity = entity if entity else self._entity
        try:
            acm_entity = acm.Ael.AelToFObject(entity)
        except Exception as exc:
            msg = '%s: Failed to convert Ael to FObject. %s'
            LOGGER.warning(msg % (self.__class__.__name__, str(exc)))
            return []
        if not acm_entity:
            return []
        moneyflows = []
        for mf in acm_entity.MoneyFlows(ACM_BACKDATE_START, ACM_NEXT_BUS_DAY):
            if mf.Currency().Name() in SUPPRESSED_CURR:
                continue
            if (mf.SourceObject().RecordType() == 'Payment' 
                    and mf.SourceObject().Trade().Oid() != entity.trdnbr):
                msg = '%s: Payment %s does not correspond to trade %s.' 
                LOGGER.warning(msg % (self.__class__.__name__, 
                                      mf.SourceObject().Oid(), entity.trdnbr))
                continue
            if (mf.Currency().Name() in NEXT_DAY_CURR 
                    or mf.PayDate() <= ACM_DATE_TODAY):
                moneyflows.append(mf)
        return moneyflows
    
    def _get_trade_moneyflows(self, entity=None):
        mfs = self._get_moneyflows_from_entity(entity)
        return [mf for mf in mfs if mf.SourceObject().RecordType() == 'Trade']


class TradeWorkerPostAll(TradeWorker):

    def process(self):
        paynbrs = get_paynbrs(self._entity)
        msg = '%s: Trade %s payments: %s'
        LOGGER.info(msg % (self.__class__.__name__, self._entity.trdnbr,
                           ', '.join([str(paynbr) for paynbr in paynbrs])))
        self._new_mf_objects = self._get_moneyflows_from_entity()
        super(TradeWorkerPostAll, self).process()


class TradeWorkerReverseAll(TradeWorker):
    
    def __init__(self, entity, void=False): 
        super(TradeWorkerReverseAll, self).__init__(entity)
        self._void = void
        mfs = self._get_moneyflows_from_entity()
        for mf in mfs:
            self._old_mf_ids.append(self.get_moneyflow_id(mf))
    
    def process(self):
        super(TradeWorkerReverseAll, self).process(self._void)


class TradeWorkerReverseAndPost(TradeWorker):
    
    def __init__(self, entity, old_entity):
        super(TradeWorkerReverseAndPost, self).__init__(entity)
        mfs = self._get_trade_moneyflows(old_entity)
        for mf in mfs:
            self._old_mf_ids.append(self.get_moneyflow_id(mf))
    
    def process(self):
        paynbrs = get_paynbrs(self._entity)
        msg = '%s: Trade %s payments: %s'
        LOGGER.info(msg % (self.__class__.__name__, self._entity.trdnbr,
                           ', '.join([str(paynbr) for paynbr in paynbrs])))
        self._new_mf_objects = self._get_trade_moneyflows()
        super(TradeWorkerReverseAndPost, self).process()


class TradeWorkerReverseAndPostAll(TradeWorker):
    
    def __init__(self, entity, old_entity):
        super(TradeWorkerReverseAndPostAll, self).__init__(entity)
        mfs = self._get_moneyflows_from_entity(old_entity)
        for mf in mfs:
            self._old_mf_ids.append(self.get_moneyflow_id(mf))
    
    def process(self):
        paynbrs = get_paynbrs(self._entity)
        msg = '%s: Trade %s payments: %s'
        LOGGER.info(msg % (self.__class__.__name__, self._entity.trdnbr,
                           ', '.join([str(paynbr) for paynbr in paynbrs])))
        self._new_mf_objects = self._get_moneyflows_from_entity()
        super(TradeWorkerReverseAndPostAll, self).process()


class WorkerReverseAndPost(Worker):
    
    def __init__(self, entity, old_entity):
        super(WorkerReverseAndPost, self).__init__(entity)
        mfs = self._get_moneyflows_from_entity(old_entity)
        for mf in mfs:
            self._old_mf_ids.append(self.get_moneyflow_id(mf))
    
    def process(self):
        self._new_mf_objects = self._get_moneyflows_from_entity()
        super(WorkerReverseAndPost, self).process()


class WorkerReverse(Worker):  
    
    def __init__(self, entity):
        super(WorkerReverse, self).__init__(entity)
        mfs = self._get_moneyflows_from_entity()
        for mf in mfs:
            self._old_mf_ids.append(self.get_moneyflow_id(mf))


class WorkerPost(Worker):

    def process(self):
        self._new_mf_objects = self._get_moneyflows_from_entity()
        super(WorkerPost, self).process()


class Listener(object):
    
    def __init__(self, entity, old_entity, operation):
        self._entity = entity
        self._old_entity = old_entity
        self._operation = operation
        self._pay_day = None
        self._old_pay_day = None
        self._curr = None
        self._old_curr = None
    
    def _reverse(self, end_date):
        if (self._pay_day >= AEL_BACKDATE_START
                and self._pay_day <= end_date):
            return WorkerReverse(self._old_entity)
    
    def _delete(self, end_date):
        if (self._pay_day >= AEL_BACKDATE_START
                and self._pay_day <= end_date):
            return WorkerReverse(self._entity)
    
    def _update(self, end_date):
        if (self._pay_day >= AEL_BACKDATE_START
                and self._pay_day <= end_date):
            if self._old_pay_day <= end_date:
                return WorkerReverseAndPost(self._entity, self._old_entity)
            else:
                return WorkerPost(self._entity)
        elif (self._pay_day > end_date and self._old_pay_day <= end_date
                and self._old_pay_day >= AEL_BACKDATE_START):
            return WorkerReverse(self._old_entity)
    
    def _insert(self, end_date):
        if (self._pay_day >= AEL_BACKDATE_START
                and self._pay_day <= end_date):
            return WorkerPost(self._entity)
    
    def process(self):
        pass


class TradeListener(object):

    def __init__(self, entity, old_entity, operation):
        self._entity = entity
        self._old_entity = old_entity
        self._operation = operation
    
    @classmethod
    def is_prf_valid(cls, prf_name):
        prf = acm.FPhysicalPortfolio[prf_name]
        if prf and prf.add_info('MIDAS_Customer_Num'):
            return True
        return False
    
    @classmethod
    def is_trade_valid(cls, ael_trade):
        if not ael_trade or not ael_trade.prfnbr:
            return False
        prf_name = ael_trade.prfnbr.prfid
        if midas_settlement(ael_trade.trdnbr, prf_name):
            return False
        status = ael_trade.status
        if status in VALID_STATUS and cls.is_prf_valid(prf_name):
            return True
        return False
    
    @classmethod
    def is_acm_trade_valid(cls, acm_trade):
        if not acm_trade:
            return False
        return cls.is_trade_valid(ael.Trade[acm_trade.Oid()])
    
    @classmethod
    def is_cf_instrument(cls, ael_trade):
        if not ael_trade or not ael_trade.insaddr:
            return False
        acm_ins = acm.FInstrument[ael_trade.insaddr.insid]
        if not acm_ins:
            return False
        return acm_ins.IsKindOf(acm.FCashFlowInstrument)
    
    def _get_updated_fields(self):
        new_pp = self._entity.pp().split('\n')
        old_pp = self._old_entity.pp().split('\n')
        different_fields = []
        for old_value, new_value in zip(old_pp, new_pp):
            if old_value == new_value:
                continue
            field_name = new_value.split(' ')[0]
            different_fields.append(field_name)
        return list(set(different_fields) - set(IGNORED_TRADE_FIELDS))
    
    def process(self):
        new_valid = self.is_trade_valid(self._entity)
        if self._operation == 'insert':
            if not new_valid:
                return
            return TradeWorkerPostAll(self._entity)
        elif self._operation == 'update':
            if (self._entity and self._old_entity 
                    and not self._get_updated_fields()):
                return
            old_valid = self.is_trade_valid(self._old_entity)
            if not new_valid and not old_valid:
                return
            paynbrs = get_paynbrs(self._entity)
            msg = '%s: Trade %s payments: %s'
            LOGGER.info(msg % (self.__class__.__name__, self._entity.trdnbr,
                               ', '.join([str(paynbr) for paynbr in paynbrs])))
            if new_valid and not old_valid:
                return TradeWorkerPostAll(self._entity)
            if not new_valid and old_valid:
                void = self._entity.status == 'Void'
                return TradeWorkerReverseAll(self._old_entity, void)
            if self.is_cf_instrument(self._entity):
                return TradeWorkerReverseAndPostAll(self._entity, self._old_entity)
            return TradeWorkerReverseAndPost(self._entity, self._old_entity)


class CashFlowListener(Listener):

    rate_cashflows = (
        'Call Fixed Rate Adjustable',
        'Fixed Rate Adjustable',
        'Call Fixed Rate',
        'Fixed Rate',
        'Call Float Rate',
        'Float Rate',
    )

    def __init__(self, entity, old_entity, operation):
        super(CashFlowListener, self).__init__(entity, old_entity, operation)
        self._pay_day = entity.pay_day
        if entity.legnbr and entity.legnbr.curr:
            self._curr = entity.legnbr.curr.insid
        else:
            self._curr = None
        if old_entity:
            self._old_pay_day = old_entity.pay_day
    
    def check_rate_cashflows(self):
        return (self._entity.legnbr and self._entity.legnbr.insaddr
                and self._entity.legnbr.insaddr.instype == 'Deposit'
                and not self._entity.type in self.rate_cashflows)
    
    def process(self):
        # no currency updates possible (curr is leg level update)
        if not self._curr or not self._pay_day:
            return
        if self._curr in SUPPRESSED_CURR:
            return
        end_date = AEL_NEXT_BUS_DAY if self._curr in NEXT_DAY_CURR else AEL_DATE_TODAY
        if self._operation == 'delete':
            return self._delete(end_date)
        elif self._operation == 'reverse':
            return self._reverse(end_date)
        elif self._operation == 'update':
            return self._update(end_date)
        elif self._operation == 'insert':
            return self._insert(end_date)


class ResetListener(Listener):
        
    def process(self):
        cfw = self._entity.cfwnbr
        if cfw and cfw.legnbr and cfw.legnbr.curr:
            self._curr = cfw.legnbr.curr.insid
        else:
            return
        cfw_pay_day = cfw.pay_day
        if not cfw_pay_day:
            return
        end_date = AEL_NEXT_BUS_DAY if self._curr in NEXT_DAY_CURR else AEL_DATE_TODAY
        if (cfw_pay_day >= AEL_BACKDATE_START
                and cfw_pay_day <= end_date):
            cfw_listener = CashFlowListener(cfw, cfw, 'update')
            return cfw_listener.process()


class LegListener(Listener):
    
    def __init__(self, entity, old_entity, operation):
        super(LegListener, self).__init__(entity, old_entity, operation)
        self._curr = entity.curr.insid
        if old_entity:
            self._old_curr = old_entity.curr.insid

    def process(self):
        if not self._operation == 'update':
            return []
        if not self._curr:
            return []
        if self._curr in SUPPRESSED_CURR and self._old_curr in SUPPRESSED_CURR:
            return []
        if (self._curr in SUPPRESSED_CURR 
                and not self._old_curr in SUPPRESSED_CURR):
            operation = 'reverse'
        elif (self._old_curr in SUPPRESSED_CURR 
                and not self._curr in SUPPRESSED_CURR):
            operation = 'insert'
        else:
            operation = 'update'
        output = []
        for cfw in self._entity.cash_flows():
            if (self._entity.insaddr.instype == 'Deposit'
                    and cfw.type in DEPO_SUPPRESSIONS
                    and cfw.pay_day < AEL_FIVE_BUS_DAYS_AGO
                    and not self._entity.reinvest == self._old_entity.reinvest):
                continue
            cfw_listener = CashFlowListener(cfw, cfw, operation)
            cfw_worker = cfw_listener.process()
            if cfw_worker:
                output.append(cfw_worker)
        return output
        

class PaymentListener(Listener):
    
    def __init__(self, entity, old_entity, operation):
        super(PaymentListener, self).__init__(entity, old_entity, operation)
        self._pay_day = entity.payday
        self._curr = entity.curr.insid
        if old_entity:
            self._old_pay_day = old_entity.payday
            self._old_curr = old_entity.curr.insid
    
    def process(self):
        # currency updates possible
        if not self._curr or not self._pay_day:
            return
        end_date = AEL_NEXT_BUS_DAY if self._curr in NEXT_DAY_CURR else AEL_DATE_TODAY
        if self._operation == 'delete':
            if self._curr in SUPPRESSED_CURR:
                return
            return self._delete(end_date)
        elif self._operation == 'update':
            if (self._curr in SUPPRESSED_CURR 
                    and self._old_curr in SUPPRESSED_CURR):
                return
            if (self._curr in SUPPRESSED_CURR 
                    and not self._old_curr in SUPPRESSED_CURR):
                return self._reverse(end_date)
            if (self._old_curr in SUPPRESSED_CURR 
                    and not self._curr in SUPPRESSED_CURR):
                return self._insert(end_date)
            return self._update(end_date)
        elif self._operation == 'insert':
            if self._curr in SUPPRESSED_CURR:
                return
            return self._insert(end_date)


def listener(o, entity, arg, operation):    
    if not entity:
        return
    old_entity = ael.get_old_entity()
    if entity.record_type == 'CashFlow':
        cf_listener = CashFlowListener(entity, old_entity, operation)
        worker = cf_listener.process()
        worker_queue.put(worker)
        
        if cf_listener.check_rate_cashflows():
            for cfw in entity.legnbr.cash_flows():
                if not cfw.type in CashFlowListener.rate_cashflows:
                    continue
                rate_cf_listener = CashFlowListener(cfw, cfw, 'update')
                worker = rate_cf_listener.process()
                worker_queue.put(worker)
    elif entity.record_type == 'Payment':
        pm_listener = PaymentListener(entity, old_entity, operation)
        worker = pm_listener.process()
        worker_queue.put(worker)
    elif entity.record_type == 'Reset':
        reset_listener = ResetListener(entity, old_entity, operation)
        worker = reset_listener.process()
        worker_queue.put(worker)
    elif entity.record_type == 'Leg':
        leg_listener = LegListener(entity, old_entity, operation)
        workers = leg_listener.process()
        for worker in workers:
            worker_queue.put(worker)
    elif entity.record_type == 'Trade':
        trade_listener = TradeListener(entity, old_entity, operation)
        worker = trade_listener.process()
        worker_queue.put(worker)


def start():
    ael.Trade.subscribe(listener)
    ael.Payment.subscribe(listener)
    ael.CashFlow.subscribe(listener)
    ael.Reset.subscribe(listener)
    ael.Leg.subscribe(listener)


def stop():
    ael.Trade.unsubscribe(listener)
    ael.Payment.unsubscribe(listener)
    ael.CashFlow.unsubscribe(listener)
    ael.Reset.unsubscribe(listener)
    ael.Leg.unsubscribe(listener)


def status():
    pass


def work():
    while not worker_queue.empty():
        worker = worker_queue.get()
        if not worker:
            continue
        worker.process()
    
