''' =======================================================================
    TMS TradeWrapper IRD

Purpose                 		:   Update Module to include Currency for Premium Payments, BrokerFee as well as Additional Paymnets
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Babalo Edwana
    CR Number              	:   549133
    Date				:   2010-10-14

Purpose                 		:   Updated Module to Include Dummy cashflow when no cahsflows are captured.
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

Purpose                     :    Fixed issue with dummy cashflow
    Department and Desk     	:   SM IT Pricing & Risk
    Requester               	:   Matthew Berry
    Developer               	:   Matthew Stephanou
    CR Number              	:   706555
    Date				:   2011-07-07

Purpose                     :    Removed FX trades
    Department and Desk     	:   SM IT Pricing & Risk
    Developer               	:   Jan Mach
    CR Number              	:   CHNG0001177565
    Date				:   2013-07-18

Purpose                     :    Fix Swap Fixed Amount CashFlow
    Department and Desk     	:   SM IT Pricing & Risk
    Developer               	:   Michal Spurny
    CR Number              	:   CHNG0001635706
    Date				:   2014-01-14

Purpose                     :    Remove zero cashflow generator
    Department and Desk     	:   SM IT Pricing & Risk
    Developer               	:   Jan Mach
    CR Number              	:   CHNG0002679363
    Date				:   2015-03-05

    ======================================================================================================== '''

import TMS_TradeWrapper_Common
from TMS_TradeWrapper_Common import *

import TMS_Functions

import TMS_Functions_Common
from TMS_Functions_Common import ReformatDate
#from TMS_Template_IRSwap_Legacy import IRSwap_Message

### IRD view on IR ###
""" Base class for all IR trades """
class IRDTradeWrapper(TradeWrapper):
    def __init__(self, trade):
        TradeWrapper.__init__(self, trade)

        self._addProperty("TradeNominal", trade.nominal_amount().value())

        #Add the deal ID if one exists
        if trade.trx_trdnbr:
            self._addProperty("DealID", trade.trx_trdnbr)

    def _getFamily(self):
        return "IRD"

""" Base class for all IRD trade wrapper factories """
class IRDTradeWrapperFactory(WrapperFactory):
    def supports(self, trade):
        return self._supports(trade.insaddr)

    def _supports(self, instr):
        raise NotImpementedError

class IRLegWrapper(LegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        LegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)

        self._addProperty("Type", leg.type)

        #All IR Instruments will either have resets on the legs of the instrument or
        #on the legs of the underlying (in the case of an option).
        self._addProperty("rolling_period.count", getattr(leg, 'rolling_period.count'))
        self._addProperty("rolling_period.unit", getattr(leg, 'rolling_period.unit'))
        self._addProperty("daycount_method", leg.daycount_method)
        self._addProperty("LegFloatRate", leg.display_id('float_rate'))
        
        #Reset Day Method
        self._addProperty("reset_day_method", leg.reset_day_method or '')
        
        if leg.type == "Fixed":
            self._addProperty("fixed_rate", leg.fixed_rate)

        #Pay Conventions
        self._addProperty("pay_day_method", leg.pay_day_method)
        self._addProperty("pay_day_offset.count", getattr(leg, 'pay_day_offset.count'))

        ##########Temporary hack to allow FRA, FXSwap and IRSwaption to have negative LegNominal value
        ##########Move to proper wrapper class or remove once determined why this is the case
        instr = trade.insaddr
        if instr.und_instype != 'None':
            Und_instr = trade.insaddr.und_insaddr
        if instr.instype == "FRA" or (instr.instype == 'Option' and Und_instr.instype == 'Swap') or (instr.instype == 'FxSwap'):
            self._changePropertyValue("LegNominal", (trade.quantity * instr.contr_size * leg.nominal_factor))
        ##########End Temporary hack

        #Add reset properties to leg
        if leg.type == "Float":
            self._addResetPropertiesToLeg(leg)

            # If the rate consists of weighted fixings - e.g. for PRIME swaps.
            tenor = ""
            if leg.reset_type == "Weighted":
                forecast_instr = ael.Instrument[leg.display_id('float_rate')]
                forecast_leg = forecast_instr.legs()[0]
                tenor = "%s%s" % (getattr(forecast_leg, 'end_period.count'), getattr(forecast_leg, 'end_period.unit')[0].upper())
            else:
                tenor = "%s%s" % (getattr(leg, 'rolling_period.count'), getattr(leg, 'rolling_period.unit')[0].upper())

            self._addProperty("Forecast_Tenor", tenor)

        #Add premium or brokerage fee as a payment:
        #Pass Payment Currency to Wrapper
        if trade.premium:
            self._addPremiumBrokerageToLeg(trade.value_day, trade.premium, "Premium", trade.curr.insid, leg.payleg, trade.quantity)
        if trade.fee:
            self._addPremiumBrokerageToLeg(trade.value_day, trade.fee, "Brokerage", instr.curr.insid, leg.payleg, trade.quantity)

        self._sortCashflows()

    def _sortCashflows(self):
        #Sort cashflows of the leg by ascending order of cashflow pay-out date
        self._children.sort(lambda cfx, cfy: cmp(cfx._getPropertyValue("start_day"), cfy._getPropertyValue("start_day")))
            
    def _addPremiumBrokerageToLeg(self, value_day, amount, type, currency, payleg = None, trade_qty = None):
        self._addChild(IRPremiumBrokeragePaymentWrapper(value_day, amount, type, currency))

    def _addCashflowToLeg(self, id, cashflow, leg, quantity, contractsize, clsCashFlowWrapper = None):
        if cashflow:
            if not clsCashFlowWrapper:
                objCashFlow = CashFlowWrapper(cashflow, leg, quantity, contractsize, id)
            else:
                objCashFlow = clsCashFlowWrapper(cashflow, leg, quantity, contractsize, id)

            objCashFlow._sortProperties()
            #MS 05/12
            if objCashFlow.properties() != [] or objCashFlow.children() != []:
                if cashflow.type != "Fixed Amount":
                    self._addChild(objCashFlow)
            #If cashflow is of type fixed amount then we rather add "cashflows"
            #to a Payment table at the same level as cashflow.
            if cashflow.type == "Fixed Amount":
                #Exchanges
                type = "Exchange"
                valueDay = cashflow.pay_day.to_string('%Y-%m-%d')
                nominal = cashflow.projected_cf() * quantity
                #add currency for this Payment
                leg = cashflow.legnbr
                currency = leg.insaddr.curr.insid
                self._addChild(PaymentWrapper(None, type, nominal, valueDay, currency))

    def _addPaymentToLeg(self, payment, trade, leg):
        if payment.display_id('curr') == leg.display_id('curr'):
            self._addChild( IRPaymentWrapper(payment, trade, leg) )

    def _addResetPropertiesToLeg(self, leg):
        self._addProperty("AccruedIncluded", leg.accrued_included)
        self._addProperty("reset_day_offset", leg.reset_day_offset)
        self._addProperty("reset_in_arrear", leg.reset_in_arrear)
        self._addProperty("ResetCal", TMS_Functions_Common.Get_BarCap_Calendar(leg.display_id('reset_calnbr'), leg.display_id('reset2_calnbr'), leg.display_id('reset3_calnbr'), leg.display_id('reset4_calnbr'), leg.display_id('reset5_calnbr')))
        self._addProperty("reset_period_count", getattr(leg, 'reset_period.count'))    
        self._addProperty("reset_period_unit", getattr(leg, 'reset_period.unit'))

class IRPremiumBrokeragePaymentWrapper(Wrapper):
    def __init__(self, payDate, payNominal, payType, currency):
        Wrapper.__init__(self)
        self._addProperty("P_Date", payDate.to_string('%Y-%m-%d'))
        self._addProperty("P_Nominal", payNominal)
        self._addProperty("P_Type", payType)
        #add currency for payment
        self._addProperty("P_Currency", currency)            

    def getTypeName(self):
        return "PAYMENT"

class IRPaymentWrapper(Wrapper):
    def __init__(self, payment, trade, leg):
        Wrapper.__init__(self)
        self._addProperty("P_Date", payment.payday.to_string('%Y-%m-%d'))
        self._addProperty("P_Nominal", payment.amount)
        self._addProperty("P_Type", payment.type)
        #add payment currency as well
        self._addProperty("P_Currency", payment.curr.insid)            

    def getTypeName(self):
        return "PAYMENT"

class IRInstrumentWrapper(InstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper, clsFlowWrapper):
        InstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsFlowWrapper)

        self._changePropertyValue("otc", instr.otc and "1" or "0")
        
    def _getFamily(self):
        return "IRD"

""" Common base class for all reset wrappers """
class ResetWrapper(Wrapper):
    def __init__(self, reset):
        Wrapper.__init__(self)

        dateToday = TMS_Functions_Common.Date()

        if reset.day.to_string('%Y-%m-%d') <= dateToday:
            self._addProperty("fixing_rate", reset.value)
        else:
            self._addProperty("fixing_rate", 0)

        self._addProperty("day", reset.day.to_string('%Y-%m-%d'))
        if reset.start_day is not None and reset.end_day is not None:
            self._addProperty("start_day", reset.start_day.to_string('%Y-%m-%d'))
            self._addProperty("end_day", reset.end_day.to_string('%Y-%m-%d'))
        else:
            self._addProperty("start_day", reset.cfwnbr.start_day.to_string('%Y-%m-%d'))
            self._addProperty("end_day", reset.cfwnbr.end_day.to_string('%Y-%m-%d'))
        self._addProperty("ResetDayOfMonth", reset.day.to_string('%d'))

    def getTypeName(self):
        return "RESET"

### IRSwap Classes ###
class IRSwapInstrumentWrapper(IRInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper, clsCashFlowWrapper):
        IRInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsCashFlowWrapper)

class IRSwapTradeWrapper(IRDTradeWrapper):
    def __init__(self, trade):
        IRDTradeWrapper.__init__(self, trade)

        instr = self._getInstrument()
        objInstrument = IRSwapInstrumentWrapper(instr, trade, IRSwapLegWrapper, IRSwapCashFlowWrapper)

        self._addChild(objInstrument)

class IRSwapTradeWrapperFactory(IRDTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == 'Swap':
            #If the trade is a swap and it has no cashflows then it has been
            #bastardized into a "Payments Holder" - do not send through as
            #the cash extract will cater for these payments. Also, cashflowless
            #swaps break the trade feed.
            return len(instr.cash_flows())

    def _name(self):
        return "Swap"

    def create(self, trade):
        return IRSwapTradeWrapper(trade)

class IRDerivativeInstrumentWrapper(DerivativeInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper, clsCashFlowWrapper):
        DerivativeInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsCashFlowWrapper)
        undInstr = ael.Instrument[trade.insaddr.und_insaddr.insaddr]
        dateToday = ael.date_today()
        self._addProperty('Global_Reset_Day', undInstr and TMS_Functions.Get_Global_Reset_Day(undInstr.insaddr, dateToday) \
                                               or TMS_Functions.Get_Global_Reset_Day(instr.insaddr, dateToday))
        self._changePropertyValue("otc", instr.otc and "1" or "0")

    def _getFamily(self):
        return "IRD"

    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper, clsCashFlowWrapper):
        #Legs will be on the underlying instrument
        und_instr = ael.Instrument[trade.insaddr.und_insaddr.insaddr]
        if und_instr:
            Legs = und_instr.legs()
            for leg in Legs:
                if not clsLegWrapper:
                    self._addChild( LegWrapper(leg, trade, instr.contr_size) )
                    self._addProperty("Global_Curr", leg.display_id('curr'))
                else:
                    self._addChild( clsLegWrapper(leg, trade, instr.contr_size, clsCashFlowWrapper) )
                    self._addProperty("Global_Curr", leg.display_id('curr'))

class IRSwapLegWrapper(IRLegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        IRLegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)
        if leg.type == 'Float':
            self._addProperty("IsAverage", leg.reset_type == "Weighted" and 1 or 0)
            self._addProperty("L_AvgFreq", "%s%s" % (getattr(leg, 'reset_period.count'), getattr(leg, 'reset_period.unit')[0].upper()))

    def _addPremiumBrokerageToLeg(self, value_day, amount, type, currency, payleg = None, trade_qty = None):
        if (payleg and trade_qty > 0) or (not payleg and trade_qty < 0):
            self._addChild(IRPremiumBrokeragePaymentWrapper(value_day, amount, type, currency))

    def _addPaymentToLeg(self, payment, trade, leg):
        if (leg.payleg and trade.quantity > 0) or (not leg.payleg and trade.quantity < 0):
            self._addChild( IRPaymentWrapper(payment, trade, leg) )

class IRSwapCashFlowWrapper(CashFlowWrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, id):
        CashFlowWrapper.__init__(self, cashflow, leg, quantity, contractsize, id)
        if leg.reset_type == "Weighted":
            #Add a reset populated with some cashflow properties
            fixing_rate = cashflow.known_cashflow() and cashflow.period_rate(cashflow.start_day, cashflow.end_day).value() or 0
            wrapper = IRResetWrapper(cashflow.end_day, cashflow.start_day, cashflow.end_day, fixing_rate)
            self._addChild(wrapper)
        else:
            if len(cashflow.resets()) >= 1:
                wrapper = ResetWrapper(cashflow.resets()[0])
                self._addChild(wrapper)

    def _addCashflowNominal(self, cashflow, leg, quantity, contractsize):
        #if the payday of the cashflow is before the reporting day, then send through the projected cashflow
        #else the nominal of the cashflow
        dateToday = TMS_Functions_Common.Date()

        cf_amt = 0
        if leg.type == 'Float':
            fixing_rate = 0
            if leg.reset_type == "Weighted":
                fixing_rate = cashflow.known_cashflow() and cashflow.period_rate(cashflow.start_day, cashflow.end_day).value() or 0
            else:
                if len(cashflow.resets()) >= 1:
                    r = cashflow.resets()[0]
                    fixing_rate = r.value

            #If our rate has been fixed send through the projected cashflow through to TMS else send
            #through the cashflow nominal.
            cf_amt = fixing_rate and cashflow.known_cashflow() * quantity or abs(contractsize * cashflow.nominal_factor * quantity)
        else:
            cf_amt = abs(quantity * contractsize * cashflow.nominal_factor)

        self._addProperty("CFNominal", cf_amt)

class IRResetWrapper(Wrapper):
    def __init__(self, day, start_day, end_day, reset_value):
        Wrapper.__init__(self)

        dateToday = TMS_Functions_Common.Date()

        self._addProperty("fixing_rate", reset_value)
        self._addProperty("day", day.to_string('%Y-%m-%d'))
        self._addProperty("start_day", start_day.to_string('%Y-%m-%d'))
        self._addProperty("end_day", end_day.to_string('%Y-%m-%d'))
        self._addProperty("ResetDayOfMonth", day.to_string('%d'))

    def getTypeName(self):
        return "RESET"

### IRSwaption Classes ###
class IRSwaptionEventWrapper(Wrapper):
    def __init__(self, id, event):
        Wrapper.__init__(self)
        self._addProperty("Id", id)
        self._addProperty("Exp_Day", event.day.to_string('%Y-%m-%d'))
        self._addProperty("Exp_Day_Serial", int(TMS_Functions.AelDate2Serial(event.day)))
        self._addProperty("Notice_Day", event.notice_day.to_string('%Y-%m-%d'))
        
    def getTypeName(self):
        return "EXERCISE_EVENTS"

class IRSwaptionCashFlowWrapper(CashFlowWrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, id):
        CashFlowWrapper.__init__(self, cashflow, leg, quantity, contractsize, id)

        #Add Resets (Child of Cashflow)
        for reset in cashflow.resets():
            objReset = ResetWrapper(reset)
            objReset._sortProperties()
            
            self._addChild(objReset)
    
    def _addCashflowNominal(self, cashflow, leg, quantity, contractsize):
        self._addProperty("CFNominal", (quantity * contractsize * cashflow.nominal_factor))

class IRSwaptionLegWrapper(IRLegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        IRLegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)
        
    def _addPaymentToLeg(self, payment, trade, leg):
        #We dont want to add payments to the leg level in Swaptions - have them as fees on trade level instead.
        pass
    
    def _addPremiumBrokerageToLeg(self, value_day, amount, type, currency, payleg = None, trade_qty = None):
        #Swaptions have this as a fee on the trade level instead of a payment
        pass

class IRSwaptionInstrumentWrapper(IRDerivativeInstrumentWrapper):
    def __init__(self, instr, trade):
        IRDerivativeInstrumentWrapper.__init__(self, instr, trade, IRSwaptionLegWrapper, IRSwaptionCashFlowWrapper)
        
    def _getFamily(self):
        return "IRD"

class IRDirextSwaptionInstrumentWrapper(IRDerivativeInstrumentWrapper):
    def __init__(self, instr, trade):
        IRDerivativeInstrumentWrapper.__init__(self, instr, trade, IRDirextSwaptionLegWrapper, IRDirextSwaptionCashFlowWrapper)
        
    def _getFamily(self):
        return "IRD"

class IRBermudanSwaptionInstrumentWrapper(IRDirextSwaptionInstrumentWrapper):
    def __init__(self, instr, trade):
        IRDirextSwaptionInstrumentWrapper.__init__(self, instr, trade)

        Events = list(instr.exercise_events())
        Events.sort(lambda x, y: cmp(ReformatDate(x.day), ReformatDate(y.day)))

	self._addProperty("exercise_count", len(Events))	
        for i, e in enumerate(Events):
            self._addChild(IRSwaptionEventWrapper(i, e))

class IRDirextSwaptionCashFlowWrapper(IRSwaptionCashFlowWrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, id):
        IRSwaptionCashFlowWrapper.__init__(self, cashflow, leg, quantity, contractsize, id)

        #Pass the cashflow rate only for fixed legs
        if leg.type == 'Fixed':
            self._changePropertyValue("CFRate", cashflow.rate * 0.01)
    
    def _addCashflowNominal(self, cashflow, leg, quantity, contractsize):
        if ((leg.payleg and leg.type == 'Fixed') or (not leg.payleg and leg.type == 'Float')):
            mult=1
        else:
            mult=-1
        if leg.type == 'Fixed':			
            self._addProperty("CFNominal", mult * quantity * abs(contractsize * cashflow.nominal_factor))
        else:
            self._addProperty("CFNominal", mult * -1 * quantity * abs(contractsize * cashflow.nominal_factor))

class IRDirextSwaptionLegWrapper(IRSwaptionLegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        IRSwaptionLegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)

        if ((leg.payleg and leg.type == 'Fixed') or (not leg.payleg and leg.type == 'Float')):
            mult=1
        else:
            mult=-1
        if leg.type == 'Fixed':
            self._changePropertyValue("LegNominal", mult * trade.quantity * abs(contractsize * leg.nominal_factor))
            self._addProperty("AbsLegNominal", abs(trade.quantity * contractsize * leg.nominal_factor))
        else:
            self._changePropertyValue("LegNominal", mult * -1 * trade.quantity * abs(contractsize * leg.nominal_factor))
            self._addProperty("AbsLegNominal", abs(trade.quantity * contractsize * leg.nominal_factor))
		
        self._changePropertyValue("payleg", leg.payleg and "yes" or "no")
        self._addProperty("InitialPayment", 0)

class IRSwaptionTradeWrapper(IRDTradeWrapper):
    def __init__(self, trade):
        IRDTradeWrapper.__init__(self, trade)

        self._addProperty("Fee", trade.fee)
        self._addProperty("Premium", trade.premium)
        self._addProperty("Value_Day", trade.value_day.to_string('%Y-%m-%d'))

        instr = self._getInstrument()
        if ( instr.exercise_type == 'Bermudan'):
            objInstrument = IRBermudanSwaptionInstrumentWrapper(instr, trade)
        elif (instr.settlement == 'Cash'):
            objInstrument = IRDirextSwaptionInstrumentWrapper(instr, trade)
        else:
            objInstrument = IRSwaptionInstrumentWrapper(instr, trade)

        self._addChild(objInstrument)

        #Add the payments as fees to the trade level:
        #added currency for the Fees
        if trade.premium:
            self._addChild(IRSwaptionPremiumBrokerageFeeWrapper(trade.value_day, trade.premium, "Premium", trade.curr.insid))
        if trade.fee:
            self._addChild(IRSwaptionPremiumBrokerageFeeWrapper(trade.value_day, trade.fee, "Brokerage", instr.curr.insid))
        for p in trade.payments():
            self._addChild(IRSwaptionFeeWrapper(p, (instr.exercise_type == 'European' and p.type or 'Premium'), p.curr.insid))        

class IRSwaptionFeeWrapper(Wrapper):
    def __init__(self, payment, type, currency):
        Wrapper.__init__(self)
        self._addProperty("FEE_DATE", payment.payday.to_string('%Y-%m-%d'))
        self._addProperty("FEE_AMOUNT", payment.amount)
        self._addProperty("FEE_TYPE", type)
        #currency field added for foreign currency
        self._addProperty("FEE_CURRENCY", currency)   
        
    def getTypeName(self):
        return "FEES"
    
class IRSwaptionPremiumBrokerageFeeWrapper(Wrapper):
    def __init__(self, payday, amount, type, currency):
        Wrapper.__init__(self)
        self._addProperty("FEE_DATE", payday.to_string('%Y-%m-%d'))
        self._addProperty("FEE_AMOUNT", amount)
        self._addProperty("FEE_TYPE", type)
        #currency field added for foreign currency
        self._addProperty("FEE_CURRENCY", currency)   
        
    def getTypeName(self):
        return "FEES"

class IRSwaptionTradeWrapperFactory(IRDTradeWrapperFactory):
    def _supports(self, instr):
        return instr.instype == 'Option' and instr.und_instype == 'Swap'

    def create(self, trade):
        return IRSwaptionTradeWrapper(trade)
    
    def _name(self):
        return "Swaption"

### FRA Classes ###
class IRFRATradeWrapper(IRDTradeWrapper):
    def __init__(self, trade):
        IRDTradeWrapper.__init__(self, trade)

        instr = self._getInstrument()
        objInstrument = IRFRAInstrumentWrapper(instr, trade, IRFRALegWrapper, IRFRACashFlowWrapper)

        self._addChild(objInstrument)

class IRFRALegWrapper(IRLegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        IRLegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)
        self._changePropertyValue("Spread", (leg.fixed_rate*-1)/100)

class IRFRAInstrumentWrapper(IRInstrumentWrapper):
     def __init__(self, instr, trade, clsLegWrapper, clsCashFlowWrapper):
        IRInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsCashFlowWrapper)

class IRFRATradeWrapperFactory(IRDTradeWrapperFactory):
    def _supports(self, instr):
        return instr.instype == 'FRA'

    def _name(self):
        return "FRA"

    def create(self, trade):
        return IRFRATradeWrapper(trade)

class IRFRACashFlowWrapper(CashFlowWrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, id):
        CashFlowWrapper.__init__(self, cashflow, leg, quantity, contractsize, id)
        if leg.type == 'Float':
            if cashflow.spread != 'None':
                self._changePropertyValue("spread", (leg.fixed_rate*-1)/100)

            #Add Resets
            for reset in cashflow.resets():
                objReset = ResetWrapper(reset)
                objReset._sortProperties()
                
                self._addChild(objReset)

### IRG Classes ###
class IRGFRAInstrumentWrapper(IRDerivativeInstrumentWrapper):
    def __init__(self, instr, trade):
        IRDerivativeInstrumentWrapper.__init__(self, instr, trade, IRGLegWrapper, IRGFRACashFlowWrapper)
        self._addProperty("call_option", instr.call_option)

    def _getFamily(self):
        return "IRD"
    
class IRGCapFloorInstrumentWrapper(IRInstrumentWrapper):
    def __init__(self, instr, trade):
        IRInstrumentWrapper.__init__(self, instr, trade, IRGCapFloorLegWrapper, IRGCapFloorCashFlowWrapper)
        self._addProperty("call_option", instr.instype=="Cap" and 1 or 0)

class IRGLegWrapper(IRLegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        self.strike_price = trade.insaddr.strike_price       
        IRLegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)

        if leg.type != "Fixed":
            self._addProperty("fixed_rate", leg.fixed_rate)

    def _addCashflowToLeg(self, id, cashflow, leg, quantity, contractsize, clsCashFlowWrapper = None):
        if cashflow:
            if not clsCashFlowWrapper:
                objCashFlow = CashFlowWrapper(cashflow, leg, quantity, contractsize)
            else:
                objCashFlow = clsCashFlowWrapper(cashflow, leg, quantity, contractsize, self.strike_price)

            objCashFlow._sortProperties()

            if objCashFlow.properties() != [] or objCashFlow.children() != []:
                self._addChild(objCashFlow)
            #If cashflow is of type fixed amount then we rather add "cashflows"
            #to a Payment table at the same level as cashflow.
            if cashflow.type == "Fixed Amount":
                #Exchanges
                type = "Exchange"
                valueDay = cashflow.pay_day.to_string('%Y-%m-%d')
                nominal = cashflow.projected_cf() * quantity
                #add currency for this Payment
                leg = cashflow.legnbr
                currency = leg.insaddr.curr.insid
                self._addChild(PaymentWrapper(None, type, nominal, valueDay, currency))      

class IRGCapFloorLegWrapper(IRGLegWrapper):
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        IRGLegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)
        #Also has spread and reset-properties on a non-floating leg
        if leg.type != "Float":
            self._addProperty("Spread", leg.spread != "None" and leg.spread/100 or 0)
            self._addResetPropertiesToLeg(leg)

class IRGTradeWrapper(IRDTradeWrapper):
    def __init__(self, trade):
        IRDTradeWrapper.__init__(self, trade)

        self._addProperty("Premium", trade.premium)
        self._addProperty("Value_Day", trade.value_day.to_string('%Y-%m-%d'))

        instr = self._getInstrument()
        if instr.instype == 'Cap' or instr.instype == 'Floor':
            objInstrument = IRGCapFloorInstrumentWrapper(instr, trade)
        else:
            objInstrument = IRGFRAInstrumentWrapper(instr, trade)

        self._addChild(objInstrument)

class IRGFRACashFlowWrapper(CashFlowWrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, strike_price):
        CashFlowWrapper.__init__(self, cashflow, leg, quantity, contractsize)

        #Add Resets
        for reset in cashflow.resets():
            objReset = ResetWrapper(reset)
            objReset._sortProperties()
            
            self._addChild(objReset)
        
        self._addProperty("strike_rate", strike_price)
        self._changePropertyValue("pay_day", cashflow.end_day.to_string('%Y-%m-%d'))

    def _addCashflowNominal(self, cashflow, leg, quantity, contractsize):
        #For the Option on a FRA - pass the Contract_Size * Quantity
        #For Caps & Floors pass the nominal amount of the cashflow
        self._addProperty("CFNominal", abs(contractsize * quantity))

class IRGCapFloorCashFlowWrapper(CashFlowWrapper):
    def __init__(self, cashflow, leg, quantity, contractsize, strike_price):
        if cashflow.nominal_factor == 0.00:
            Wrapper.__init__(self)
            return    
            #MS26022013
        CashFlowWrapper.__init__(self, cashflow, leg, quantity, contractsize)

        #Add Resets
        if leg.reset_type == 'Weighted':
            objReset = IRResetWrapper(cashflow.start_day, cashflow.start_day, cashflow.end_day, cashflow.forward_rate()*100)
            objReset._sortProperties()
            self._addChild(objReset)
        else:
            for reset in cashflow.resets():
                objReset = ResetWrapper(reset)
                objReset._sortProperties()

                self._addChild(objReset)

        self._addProperty("strike_rate", cashflow.strike_rate)
        #Also has spread on non-floating leg cashflows:
        if leg.type != "Float":
            self._addProperty("spread", cashflow.spread != "None" and cashflow.spread/100 or 0)

    def _addCashflowNominal(self, cashflow, leg, quantity, contractsize):
        #For the Option on a FRA - pass the Contract_Size * Quantity
        #For Caps & Floors pass the nominal amount of the cashflow
        self._addProperty("CFNominal", abs(quantity * contractsize * cashflow.nominal_factor))

class IRGTradeWrapperFactory(IRDTradeWrapperFactory):
    def _supports(self, instr):
        if instr.und_instype == 'None':
            return instr.instype in ('Cap', 'Floor')
        else:
            return instr.instype == 'Option' and \
             instr.und_instype == 'FRA'
    
    def create(self, trade):
        return IRGTradeWrapper(trade)
    
    def _name(self):
        return "IRG"


#List of Wrapper Factories for external use
TradeWrapperFactories = [ 
    IRSwapTradeWrapperFactory(),
    IRSwaptionTradeWrapperFactory(),
    IRGTradeWrapperFactory(),
    IRFRATradeWrapperFactory()
    ]
