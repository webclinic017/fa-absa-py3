'''
Created on 1 Nov 2016

@author: conicova
'''


from collections import namedtuple

import acm

import at_time
import at_logging

LOGGER = at_logging.getLogger(__name__)

USE_ACM = True

LOGGER.debug("Using ACM: %s", USE_ACM)

LegDB = namedtuple("LegDB", ["end_day", "start_day", "legnbr", "type", "nominal_scaling", "daycount_method", "index_ref", "payleg"])
CashFlowDB = namedtuple("CashFlowDB", ["end_day", "start_day", "pay_day", "type", "fixed_amount", "cfwnbr", "rate"])
ResetDB = namedtuple("ResetDB", ["end_day", "start_day", "type", "value", "resnbr"])

CONN_STRING = "DRIVER={SQL Server};SERVER=JHBDSM050000052\ADPT_MAIN1_DEV;DATABASE=fa_pswap;Integrated Security=True"

if not USE_ACM:
    import pyodbc
    LOGGER.debug("Connecting to the DB")
    cnxn = pyodbc.connect(CONN_STRING)
    cursor = cnxn.cursor()
    LOGGER.debug("Connected to the DB")

class PBProxy(object):
    
    def __init__(self, id):
        self.id = id
        self._entity = None
    
    def load_ref_from_db(self):
        LOGGER.debug("load_from_db not implemented")
    
    def Oid(self):
        return self.id
    
    @classmethod
    def loader(cls, acm_entity):
        if USE_ACM:
            return acm_entity
        else:
            return cls.load_from_db(acm_entity.Oid())
        
class PBTradeProxy(PBProxy):
    
    def __init__(self, trade_id):
        super(PBTradeProxy, self).__init__(trade_id)
        self._entity_acm = acm.FTrade[trade_id]
        self._instrument = None
    
    @staticmethod
    def load_from_db(trade_id):
        return PBTradeProxy(trade_id)
    
    def load_ref_from_db(self):
        self._instrument = PBInstrumentProxy(self._entity_acm.Instrument().Oid())
    
    def Instrument(self):
        if not self._instrument:
            self.load_ref_from_db()
        return self._instrument
    
    def Payments(self):
        return self._entity_acm.Payments()
    
class PBInstrumentProxy(PBProxy):
    
    def __init__(self, instrument_id):
        LOGGER.debug("new PBInstrumentProxy(%s)", instrument_id)
        super(PBInstrumentProxy, self).__init__(instrument_id)
        self._legs = None
        self._entity_acm = acm.FInstrument[instrument_id]
    
    def load_ref_from_db(self):
        LOGGER.debug("Loading legs for instrument '%s'", self.id)
        self._legs = []
        sql_cmd = "SELECT {0} FROM leg WHERE insaddr = ?".format(",".join(LegDB._fields))
        curr = cursor.execute(sql_cmd, (self.id))
        row = curr.fetchone()
        while row is not None:
            leg = PBLegProxy(LegDB(*row))
            self._legs.append(leg)
            
            row = curr.fetchone()
        LOGGER.debug("%s legs loaded", len(self._legs))
        
    def Legs(self):
        if not self._legs:
            self.load_ref_from_db()
        return self._legs
    
    def used_price(self):
        return self._entity_acm.used_price()
    
    def Name(self):
        return self._entity_acm.Name()
        
class PBLegProxy(PBProxy):
    
    def __init__(self, entity):
        super(PBLegProxy, self).__init__(entity.legnbr)
        self._entity = entity
        self._cashflows = None
    
    @staticmethod
    def load_from_db(legnbr):
        LOGGER.debug("Loading leg for legnbr '%s'", legnbr)
        sql_cmd = "SELECT {0} FROM leg WHERE legnbr = ?".format(",".join(LegDB._fields))

        curr = cursor.execute(sql_cmd, (legnbr))
        row = curr.fetchone()
        
        return PBLegProxy(LegDB(*row))
    
    def load_ref_from_db(self):
        LOGGER.debug("Loading cashflows for leg '%s'", self.id)
        self._cashflows = []
        sql_cmd = "SELECT {0} FROM cash_flow WHERE legnbr = ?".format(",".join(CashFlowDB._fields))
        curr = cursor.execute(sql_cmd, (self.id))
        row = curr.fetchone()
        while row is not None:
            cf = PBCashFlowProxy(CashFlowDB(*row))
            self._cashflows.append(cf)
            
            row = curr.fetchone()
        
        LOGGER.debug("%s cashflows loaded", len(self._cashflows))
        
    def CashFlows(self):
        if not self._cashflows:
            self.load_ref_from_db()
            
        return self._cashflows
    
    def LegType(self):
        return acm.EnumToString("LegType", self._entity.type).Text()
    
    def NominalScaling(self):
        return self._entity.nominal_scaling
    
    def PayLeg(self):
        return self._entity.payleg
    
    def DayCountMethod(self):
        return acm.EnumToString("DaycountMethod", self._entity.daycount_method).Text()
        
    def IndexRef(self):
        if self._entity.index_ref:
            index_ref = PBInstrumentProxy(int(self._entity.index_ref))
            return index_ref
        else:
            return None
    
class PBCashFlowProxy(PBProxy):
    
    def __init__(self, entity):
        super(PBCashFlowProxy, self).__init__(entity.cfwnbr)
        self._entity = entity
        self._resets = []
    
    def load_ref_from_db(self):
        LOGGER.debug("Loading resets for cash-flow '%s'", self.id)
        self._resets = []
        sql_cmd = "SELECT {0} FROM reset WHERE cfwnbr = ?".format(",".join(ResetDB._fields))
        curr = cursor.execute(sql_cmd, (self.id))
        row = curr.fetchone()
        while row is not None:
            reset = PBResetProxy(ResetDB(*row))
            self._resets.append(reset)
            
            row = curr.fetchone()
            
        LOGGER.debug("%s resets loaded", len(self._resets))
            
    def StartDate(self):
        return at_time.acm_date(self._entity.start_day, None)
    
    def EndDate(self):
        return at_time.acm_date(self._entity.end_day, None)
    
    def PayDate(self):
        return at_time.acm_date(self._entity.pay_day, None)
    
    def Resets(self):
        if not self._resets:
            self.load_ref_from_db()
        
        return self._resets
    
    def CashFlowType(self):
        return acm.EnumToString("CashFlowType", self._entity.type).Text()
    
    def FixedAmount(self):
        return self._entity.fixed_amount
    
    def FixedRate(self):
        return self._entity.rate
    
class PBResetProxy(PBProxy):
    
    def __init__(self, entity):
        super(PBResetProxy, self).__init__(entity.resnbr)
        self._entity = entity
    
    def StartDate(self):
        return at_time.acm_date(self._entity.start_day, None)
    
    def EndDate(self):
        return at_time.acm_date(self._entity.end_day, None)
    
    def ResetType(self):
        return acm.EnumToString("ResetType", self._entity.type).Text()
    
    def FixingValue(self):
        return self._entity.value
