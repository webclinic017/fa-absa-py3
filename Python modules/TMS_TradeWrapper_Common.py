''' =======================================================================
    TMS TradeWrapper Common

    The commonality between asset classes (FX and FI) are drawn up here.
    This is done for Trades, Instruments, Legs, Cashflows and Payments.

    Eben Mare
    ======================================================================= 

    Purpose                 		:   Updated Instrument Wrapper class, new FX Cash Instrument return None Type for i.exp_day, 
					:   therefore should use t.value_day for FX Cash Instruments
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Babalo Edwana
    CR Number              	:   271320
    Date				:   06-04-2010
    
    Purpose                 		:    Updated PaymentWrapper class to include Payment Currency
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Babalo Edwana
    CR Number              	:   549133
    Date				:   2010-10-14

    Purpose                 		:    Updated Module to include Dummy Cashflows for trades where no cashflows have been generated.
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Babalo Edwana
    CR Number              	:   666137
    Date				:   2011-05-25

    Purpose                     :    Updated to add functionality needed for DIRExT representation of Bermudans and cash-settled swaptions 
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Jan Mach
    CR Number              	:   703795
    Date				:   2011-07-05

    Purpose                     :    Updated OTC flag to be set if trade type = Future
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Jan Mach
    CR Number              	:   840456
    Date				:   2011-11-24

    ======================================================================================================== '''


import ael, time

import TMS_Functions
import TMS_Functions_Common
from TMS_Functions_Common import ReformatDate

from TMS_TradeWrapper_Base import *

from TMS_Config_Static import *

DATE_TIME_Format = "%Y-%m-%d %H:%M:%S"

""" Common base class for all instrument wrappers """
class InstrumentWrapper(Wrapper):
    def __init__(self, instr, trade, clsLegWrapper = None, clsCashFlowWrapper = None):
        Wrapper.__init__(self)
        #Add Instrument Properties
        dateToday = TMS_Functions_Common.Date()
        timeUpdate = ReformatDate(instr.updat_time, DATE_TIME_Format, DATE_TIME_Format)

        undInstr = instr.und_insaddr

        self._addProperty('Family', self._getFamily())
        self._addProperty('Instype', self._getInstrumentType(instr))
        self._addProperty('InsID', instr.insid)

        self._addProperty('version_id', instr.version_id)

        self._addProperty('updat_time', timeUpdate)
        self._addProperty('UpdateUser', TMS_Functions.Get_BarCap_User_ID(instr.updat_usrnbr))
        self._addProperty('otc', instr.otc and instr.paytype!="Future" and "OTC" or "Exchange")

        if undInstr:
            self._addProperty('Global_Reset_Day', TMS_Functions.Get_Global_Reset_Day(undInstr.insaddr, dateToday))
        else:
            self._addProperty('Global_Reset_Day', TMS_Functions.Get_Global_Reset_Day(instr.insaddr, dateToday))

        if instr.instype == "Curr":
            self._addProperty('exp_day', trade.value_day.to_string('%Y-%m-%d'))
        else:
            self._addProperty('exp_day', instr.exp_day.to_string('%Y-%m-%d'))
            
        self._addProperty('contr_size', instr.contr_size)
        self._addProperty('Curr', instr.curr.insid)

        self._addLegsToInstrument(instr, trade, instr.contr_size, clsLegWrapper, clsCashFlowWrapper)

    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper, clsCashFlowWrapper):
        if instr:
            Legs = instr.legs()
            for leg in Legs:
                if not clsLegWrapper:
                    self._addChild( LegWrapper(leg, trade, instr.contr_size) )
                else:
                    self._addChild( clsLegWrapper(leg, trade, instr.contr_size, clsCashFlowWrapper) )

                self._addProperty("Global_Curr", leg.display_id('curr'))


    def _getFamily(self):
        raise NotImplementedError

    def _getInstrumentType(self, instr):
        return instr.instype

    def getTypeName(self):
        return "INSTRUMENT"

class DerivativeInstrumentWrapper(InstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None, clsCashflowWrapper = None):
        InstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsCashflowWrapper)

        #Add option specific fields
        undinstr = getUnderlyingInstrument(trade)
        self._addProperty("Und_Instype", undinstr.instype)
        self._addProperty("exercise_type", instr.exercise_type)
        self._addProperty("exp_time", ReformatDate(instr.exp_time, "%H:%M:%S", "%H:%M:%S"))
        self._addProperty("settlement", instr.settlement)

        #self._addLegsToInstrument(undinstr, trade, instr.contr_size, clsLegWrapper, clsCashflowWrapper)

    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper, clsCashFlowWrapper):
        raise NotImplementedError


""" Common base class for all trade wrappers """
class TradeWrapper(Wrapper):
    def __init__(self, trade):
        Wrapper.__init__(self)
        self._instrument = trade.insaddr

        self._addProperty('TrdNbr', trade.trdnbr)

        self._addProperty('Version_Id', trade.version_id)

        self._addProperty('Type', trade.type)

        self._addProperty("Portfolio", trade.display_id('prfnbr'))
        self._addProperty("Book_ID", TMS_Functions.Get_BarCap_Book_ID(trade.prfnbr))
        self._addProperty("Strategy_Book", TMS_Functions.Get_BarCap_Strategy_Book_Name(trade.prfnbr))
        self._addProperty("Strategy_Book_ID", TMS_Functions.Get_BarCap_Strategy_Book_ID(trade.prfnbr))
        self._addProperty("Acquirer", TMS_Functions.Get_BarCap_SDS_ID(trade.acquirer_ptynbr))

        timeCreate = ReformatDate(trade.creat_time, DATE_TIME_Format, DATE_TIME_Format)
        timeUpdate = ReformatDate(trade.updat_time, DATE_TIME_Format, DATE_TIME_Format)

        latest_update = ReformatDate( max( [self._instrument.updat_time, trade.updat_time ] ), DATE_TIME_Format, DATE_TIME_Format)

        self._addProperty("Time", ReformatDate(trade.time, DATE_TIME_Format, DATE_TIME_Format))
        self._addProperty("Creat_Time", timeCreate)
        self._addProperty("Updat_Time", latest_update)
        self._addProperty("TradeUpdateUser", TMS_Functions.Get_BarCap_User_ID(trade.updat_usrnbr))
        self._addProperty("Status", trade.status)
        self._addProperty("Trader", TMS_Functions.Get_BarCap_User_ID(trade.trader_usrnbr))
        self._addProperty("CP", TMS_Functions.Get_BarCap_SDS_ID(trade.counterparty_ptynbr))
        self._addProperty("CP_Name", trade.counterparty_ptynbr.ptyid)
        self._addProperty("TradeCurr", trade.display_id('curr'))
        self._addProperty("Quantity", trade.quantity)

        #Add broker if available. If not we will later extract from Payment data.
        if trade.broker_ptynbr:
            self._addProperty('Broker', TMS_Functions.Get_BarCap_SDS_ID(trade.broker_ptynbr))
        else:
            self._addProperty('Broker', 0)

    def getTypeName(self):
        return "TRADE"

    # Helper functions
    def _getInstrument(self):
        return self._instrument


""" Common base class for all leg wrappers """
class LegWrapper(Wrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        Wrapper.__init__(self)

        #if leg is none then we just wish to have a empty leg structure so that we can add
        #children to it.
        if leg: 
            instr = leg.parent()

            #Include for all legs of the instrument
            self._addProperty("L_Curr", leg.display_id('curr'))
            self._addProperty("start_day", leg.start_day.to_string('%Y-%m-%d'))
            self._addProperty("end_day", leg.end_day.to_string('%Y-%m-%d'))

            #Get the current or next cashflow number so that the projected cashflow amount can be obtained
            payRec = (leg.payleg and trade.quantity > 0) or (not leg.payleg and trade.quantity < 0)
            self._addProperty("payleg", payRec and "yes" or "no")

            #Will nominal be paid at the start of contract?
            self._addProperty("nominal_at_start", leg.nominal_at_start == 1 and "Yes" or "No")

            #Will nominal be paid at the end?
            self._addProperty("nominal_at_end", leg.nominal_at_end == 1 and "Yes" or "No")

            self._addProperty("LegStartDayOfMonth", leg.start_day.to_string('%d'))
            self._addProperty("LegEndDayOfMonth", leg.end_day.to_string('%d'))
            self._addProperty("PayCal", TMS_Functions_Common.Get_BarCap_Calendar(leg.display_id('pay_calnbr'), leg.display_id('pay2_calnbr'), leg.display_id('pay3_calnbr'), leg.display_id('pay4_calnbr'), leg.display_id('pay5_calnbr')))

            #Get the correct leg nominal
            self._addProperty("LegNominal", abs(trade.quantity * instr.contr_size * leg.nominal_factor))

            if leg.type == "Float":
                self._addProperty("Spread", leg.spread != "None" and leg.spread/100 or 0)

            #Add Cashflows (Child of Leg) (if they exist)
            Flows = list(leg.cash_flows())
            Flows.sort(lambda x, y: cmp(ReformatDate(x.start_day), ReformatDate(y.start_day)))
            self._addProperty("flow_count", len(Flows))
            for i, cf in enumerate(Flows):
                self._addCashflowToLeg(i, cf, leg, trade.quantity, contractsize, clsCashFlowWrapper)

        #Add payments to leg
        for p in trade.payments():
            self._addPaymentToLeg(p, trade, leg)

    def _addCashflowToLeg(self, id, cashflow, leg, quantity, contractsize, clsCashFlowWrapper = None):
        pass

    def _addPaymentToLeg(self, payment, trade, leg):
        pass

    def getTypeName(self):
        return "LEG"

""" Common base class for all cashflow wrappers """
class CashFlowWrapper(Wrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, id=-1):
        Wrapper.__init__(self)

        #instr = _getInstrument(trade)
        dateToday = TMS_Functions_Common.Date()

        if id > -1 : self._addProperty("Id", id)

        #If cashflow is of type Fixed amount then the below properties aren't applicable
        if cashflow.type != 'Fixed Amount':
            self._addProperty("start_day", cashflow.start_day.to_string('%Y-%m-%d'))
            self._addProperty("end_day", cashflow.end_day.to_string('%Y-%m-%d'))
            self._addProperty("pay_day", cashflow.pay_day.to_string('%Y-%m-%d'))

            #Pass the cashflow rate only for fixed legs
            if leg.type == 'Fixed':
                self._addProperty("CFRate", cashflow.rate)

            if leg.type == 'Float':
                if cashflow.spread != 'None':
                    self._addProperty("spread", cashflow.spread/100)
                else:
                    self._addProperty("spread", 0)

            self._addCashflowNominal(cashflow, leg, quantity, contractsize)

    def _addCashflowNominal(self, cashflow, leg, quantity, contractsize):
        #if the payday of the cashflow is before the reporting day, then send through the projected cashflow
        #else the nominal of the cashflow
        dateToday = TMS_Functions_Common.Date()

        if leg.type == 'Float':
            if cashflow.start_day.to_string('%Y-%m-%d') <= dateToday:
                self._addProperty("CFNominal", cashflow.projected_cf() * quantity)
            else:
                self._addProperty("CFNominal", abs(quantity * contractsize * cashflow.nominal_factor))
        else:
            self._addProperty("CFNominal", abs(quantity * contractsize * cashflow.nominal_factor))

    def getTypeName(self):
        return "CASHFLOW"

class DummyCashFlowWrapper(Wrapper):
    def __init__(self, trade, start_day, end_day, pay_day, rate, Nominal, spread, strike_rate):
        Wrapper.__init__(self)
        
        self._addProperty("start_day", start_day.to_string('%Y-%m-%d'))
        self._addProperty("end_day", end_day.to_string('%Y-%m-%d'))
        self._addProperty("pay_day", pay_day.to_string('%Y-%m-%d'))
        self._addProperty("CFRate", rate)
        self._addProperty("CFNominal", Nominal)
        self._addProperty("spread", spread)
        self._addProperty("strike_rate", strike_rate)
	
    def getTypeName(self):
        return "CASHFLOW"
	
class DummyResetWrapper(Wrapper):
    def __init__(self, fixing_rate, day, start_day, end_day, ResetDayOfMonth):
        Wrapper.__init__(self)
        
        self._addProperty("fixing_rate", fixing_rate)
        self._addProperty("day", day)
        self._addProperty("start_day", start_day)
        self._addProperty("end_day", end_day)
        self._addProperty("ResetDayOfMonth", ResetDayOfMonth)

    def getTypeName(self):
        return "RESET"

# Note, FEE/PAYMENT/Broker Fee structure is redundant.
""" Common base class for all payment wrappers """
class PaymentWrapper(Wrapper):
    def __init__(self, trade, type = None, nominal = None, valueDay = None , currency = None):
        Wrapper.__init__(self)

        #Construct payment from trade
        if trade:
            self._addProperty("P_Date", trade.value_day.to_string('%Y-%m-%d'))

            if trade.premium:
                self._addProperty("P_Type", "Premium")
                self._addProperty("P_Nominal", trade.premium)
                self._addProperty("P_Currency", trade.curr.insid)
            elif trade.fee:
                self._addProperty("P_Type", "Fee")
                self._addProperty("P_Nominal", trade.fee)
                self._addProperty("P_Currency", instr.curr.insid)
        else: #Construct from type, nominal and valueDay
            try:
                self._addProperty("P_Type", type)
                self._addProperty("P_Nominal", nominal)
                self._addProperty("P_Date", valueDay)
                if currency:
                   self._addProperty("P_Currency", currency)
            except:
                raise ValueError("type, nominal or valueDay has an innapropriate value.")

    def getTypeName(self):
        return "PAYMENT"

""" Common base class for all flow wrappers """
class FlowWrapper(Wrapper):
    def __init__(self, flowType, flowAmount, flowDate, flowCurrency = None, flowSubType = None, party = None):
        Wrapper.__init__(self)

        self._addProperty("Date", flowDate)
        self._addProperty("Amount", abs(flowAmount))
        self._addProperty("Currency", flowCurrency)
        self._addProperty("Type", flowType)
        self._addProperty("SubType", flowSubType)
        self._addProperty("PayerPartyId", flowAmount >= 0 and party or ABCAP_LEGALENTITY)
        self._addProperty("ReceiverPartyId", flowAmount < 0 and party or ABCAP_LEGALENTITY)

    def getTypeName(self):
        return "FLOW"

def getUnderlyingInstrument(trade):
    return trade.insaddr.und_insaddr

""" Common base class for all trade wrapper factories """
class TradeWrapperFactory(WrapperFactory):
    def supports(self, trade):
        return self._supports(trade.insaddr)

    def _supports(self, instr):
        raise NotImpementedError
