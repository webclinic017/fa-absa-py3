import TMS_TradeWrapper_Common
from TMS_TradeWrapper_Common import *
import SANLD_NOMINALCURR
import TMS_Functions, TMS_Functions_Common
from TMS_Functions_Common import *
from TMS_Config_Static import *
import acm

''' ==========================================================================================================
    Purpose                 : Specific FX detail is added to our classes in this module. Provision is
                            : currently made for the following instruments:
                            : FX Swap and Outright,
                            : FX Options - Vanillas ,Digitals, Barriers - Continuous, Windowed and Discrete.
    Department and Desk     :
    Requester               : Mathew Berry
    Developer               : Eben Mare, Babalo Edwana
    CR Number               : 261644
    
    Changes             : Update Rebate field for Single and Double Barrier options, calculation changed from (rebate factor * 100 / strike_price)
                            : to (rebate factor/strike_price), also removed rounding to preserve accuracy
                            : Removed the usage of the Module SANLD_NOMINALCURR as this module is not properly maintained and certain
                            : currency pairs such as AUD/CAD are missing , thefore replaced function call with a new function call to Module 
                            : TMS_Functions_Commmon - > getNominalCurrency()
                            : Included new field for an FX Swap Far Trade's trade number, this is a requirement for MOPL
                
                : Updated logic for FXSwap, nearleg and farleg Notional Amount and currency
                : Mapping for FX Forwards trade price updated , inverted price not to be mapped to TMS
                : AEL function trade.nominal_amount returns zero sometimes, therefore trade nominal is calclulated
                            : ael function is no longer invoked.
                
                : Updated logic for extractign settlement currency for FX Options, new Field introduced in FX Hot Fix (Cash Currency)
                : Settlement Currency is now been captured in the new field Settlement_Curr which is the Additional Info Field for Instrument.
                
                : Barrier Crossed date is left blank by users sometimes when updating Barrier Crossed Status in Front Arena
                
                : Updated BasePerQuoted Flag for FXSwap
		
		: Updated Vanilla Options, for FUT trades premium is calculated.
		: Added Functionality to Send Inverted Trades correctly as expected by CRE and Support functionality ofor the new FX Option Strategy GUI.
		
		: Updated CashFlow Count for FUT Trades that are booked as vanillas.
		: Updated Calculation for FUT Premium to include signage.
		
		: Added new Field , ExpiryCutTime for FX Options
		: Update Settlement Currency Logic for Digital options and also removed redundant Settlement_Currency Additional Info Field Usage.

    Date                    : 12/04/2010, 16/04/2010, 21/04/2010, 19/05/2010, 09/07/2010, 02/11/2010, 06/12/2010, 18/01/2011, 10/02/2011, 21/02/2011, 25/02/2011
			                :  17/03/2011, 22/05/2011
    Developer               : Babalo Edwana
    Requester               : Mathew Berry
    CR Number               : 282095, 286190, 289195, 314825, 368378, 513835, 516900, 549166, 571776, 580298, 584998, 603481, 663186 
    
    Changes 	            : Added Futures, Exchange Traded Barrier Options
		                    : Updated Options on Currency Futures

    Date                    : 24/11/2011
    Developer               : Jan Mach
    Requester               : Mathew Berry
    CR Number               : 840456 

    Changes 	            : Rolled back previous updates for Options on Currency Futures and Futures
    
    Date                    : 05/12/2011
    Developer               : Jan Mach
    Requester               : Mathew Berry
    CR Number               : 849784 

    Changes 	            : Rolled back previous roll back - readded Options on Currency Futures and Futures
    
    Date                    : 18/04/2012
    Developer               : Jan Mach
    Requester               : Mathew Berry
    CR Number               : CHNG0000130598 

    Changes 	            : Updated calculated Price for Currency Futures and Options on Currency Futures to apply new
                            : formatting for floating numbers to eliminate scientific notations.
    
    Date                    : 07/09/2012
    Developer               : Babalo Edwana
    Requester               : Mathew Berry
    CR Number               : CHNG0000440842 

    Changes 	            : Updated FXTouchInstrumentWrapper - added code to set default value of zero for OptionStrike
                            : to match Synthesis Template logic for FXTouch Options
    
    Date                    : 13/09/2012
    Developer               : Babalo Edwana
    Requester               : Mathew Berry
    CR Number               : CHNG0000456982 

    Changes 	            : Added Exchange Traded Digital Options
    
    Date                    : 15/2/2013
    Developer               : Jan Mach
    Requester               : Mathew Berry
    CR Number               : CHNG0000803524  
    
    Changes 	            : Raised precision of rate and strike 
	
    Date                    : 19/3/2013
    Developer               : Jan Mach
    Requester               : Mathew Berry
    CR Number               : CHNG0000880086 
    
    Changes 	            : Fixed inverted option strike
	
    Date                    : 13/2/2014
    Developer               : Jan Mach
    CR Number               : CHNG0001716973 
    
=============================================================================================================== '''

""" Base class for all FX trades """
class FXTradeWrapper(TradeWrapper):
    def __init__(self, trade):
        TradeWrapper.__init__(self, trade)

        #Get Instrument
        instr = self._getInstrument()

        #Deal Id of a linked (e.g. exercised trade) + alternate id (e.g. DTC) 
        self._addProperty('DealId', trade.contract_trdnbr != trade.trdnbr and trade.contract_trdnbr or "")
        self._addProperty('AlternateId', trade.optional_key)
        self._addProperty('TMSId', trade.add_info("TMS_Trade_Id"))

        #Handle SalesPerson - Add either trade.sales_person_usrnbr or one of
        #the add info fiels: Sales_Person2, ..., Sales_Person5 if not blank
        salesPersonList = TMS_Functions_Common.GetSalesPersonList(trade, instr)
        self._addProperty("SalesPerson", "%s" % ",".join(salesPersonList))
        
        #The counterparty number of the absa capital legal entity
        self._addProperty("AbCapLegalEntity", ABCAP_LEGALENTITY)

        #Add broker if available. If not we will later extract from Payment data.
        if trade.broker_ptynbr:
            self._addProperty("Broker", TMS_Functions.Get_BarCap_SDS_ID(trade.broker_ptynbr))

        self._addProperty("FlowCount", self._getFlowCount(trade) or 0)

    def _getFlowCount(self, trade):
        ins = trade.insaddr
        cashflow_cnt = 0 #sum ( [len([cf for cf in leg.cash_flows()]) for leg in ins.legs()] )
        payment_cnt = len(list(trade.payments()))
        additional_cnt = (trade.premium or trade.fee) and 1
        return cashflow_cnt + payment_cnt + additional_cnt

""" Base class for all FX trade wrapper factories """
class FXTradeWrapperFactory(WrapperFactory):
    def supports(self, trade):
        return self._supports(trade.insaddr)

    def _name(self):
        raise NotImpementedError

    def _supports(self, instr):
        raise NotImpementedError

""" Base class for all FX Instruments"""
class FXInstrumentWrapper(InstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        InstrumentWrapper.__init__(self, instr, trade, clsLegWrapper)

    def _getFamily(self):
        return "FX"

    def _getInstrumentType(self, instr):
        return instr.instype

class FXLegWrapper(LegWrapper):
    def __init__(self, leg, trade, contractsize):
        LegWrapper.__init__(self, leg, trade, contractsize)

    def _addPaymentToLeg(self, payment, trade, leg):
        #Decide on which leg we will store the payments -
        #temp override: store all cashflows on the pay leg - TODO: Change
        if leg.payleg:
            flowType = CASHFLOWTYPE_MAPPING.get(payment.type) or "Additional"
            self._addChild( FlowWrapper(flowType,
                                        payment.amount,
                                        ReformatDate(payment.payday),
                                        payment.curr.insid,
                                        payment.type,
                                        TMS_Functions.Get_BarCap_SDS_ID(payment.ptynbr)) )
            self._sortCashflows()

class FXDerivativeLegWrapper(LegWrapper):
    #Derivate instruments don't have legs by default but a single dummy leg will 
    #exist to meet the trade structure and it will contain payments.
    def __init__(self, leg, trade, contractsize, clsCashFlowWrapper = None):
        LegWrapper.__init__(self, leg, trade, contractsize, clsCashFlowWrapper)

    def _addPaymentToLeg(self, payment, trade, leg):
        flowType = CASHFLOWTYPE_MAPPING.get(payment.type) or "Additional"
        # These derivative instruments only have a single dummy leg so no need to worry about
        # leg handling
        if payment.type == "Premium" and not trade.premium:
            self._addChild( FlowWrapper("Premium",
                                        payment.amount,
                                        ReformatDate(payment.payday),
                                        payment.curr.insid,
                                        "",
                                        TMS_Functions.Get_BarCap_SDS_ID(payment.ptynbr)) )
        else:
            self._addChild( FlowWrapper(flowType,
                                        payment.amount,
                                        ReformatDate(payment.payday),
                                        payment.curr.insid,
                                        payment.type,
                                        TMS_Functions.Get_BarCap_SDS_ID(payment.ptynbr)) )

        self._sortCashflows()
    
    #Added Method for 4.3 upgrade
    def _sortCashflows(self):
        self._children.sort(lambda cfx, cfy: cmp(cfx._getPropertyValue("Date"), cfy._getPropertyValue("Date")))

### FXSwap (and Outright) Classes ###
class FXOutrightTradeWrapper(FXTradeWrapper):
    def __init__(self, trade):
        FXTradeWrapper.__init__(self, trade)
        
        acmTrade = acm.FTrade[trade.trdnbr]
        acmInstr = acmTrade.Instrument()
        
        instr = self._getInstrument()
                
        #front 4.3 FX cash instrument changes
        baseCcy = getNominalCurrency(trade)
        nominal = baseCcy == instr.curr.insid and trade.quantity or trade.premium
        #rate = baseCcy == instr.curr.insid and trade.price or 1/trade.price
                
        self._addFloatProperty("TradeNominal", abs(nominal)) #Deprecated field - TODO: check template for dependency then remove.
        self._addProperty("BuyFaceFlag", nominal < 0 and "Sell" or "Buy")
        self._changePropertyValue("Quantity", 1)
        self._addFloatProperty("Rate", trade.price, 17)
        
        self._addChild(FXOutrightInstrumentWrapper(instr, trade))

    def _getFlowCount(self, trade):
        ins = trade.insaddr
        cashflow_cnt = 0 #sum ( [len([cf for cf in leg.cash_flows()]) for leg in ins.legs()] )
        payment_cnt = len(list(trade.payments()))
        additional_cnt = trade.fee and 1
        return cashflow_cnt + payment_cnt + additional_cnt
       
    def _getCashflowCount(self, instr):
        # Business logic: we differentiate a FX Forward and FX Swap by the number of cashflows.
        if instr:
            return sum ( [len(list(leg.cash_flows())) for leg in instr.legs()] )

class FXSwapTradeWrapper(FXTradeWrapper):
    def __init__(self, trade):
        FXTradeWrapper.__init__(self, trade)
        
        acmTrade = acm.FTrade[trade.trdnbr]
        acmInstr = acmTrade.Instrument()
        
        instr = self._getInstrument() 
        
        if not self._isFarLeg(trade):
            trd_nbr = trade.trdnbr
            tms_id = trade.add_info("TMS_Trade_Id")
            otherleg_trdnbr = otherleg(trade).Oid()
        else:
            near_leg = otherleg(trade)
            trd_nbr = near_leg.Oid()
            tms_id = near_leg.add_info("TMS_Trade_Id")
            otherleg_trdnbr = trade.trdnbr
            
        self._changePropertyValue("TrdNbr", trd_nbr)
        self._changePropertyValue('TMSId', tms_id)
        
        self._addProperty("TradeNominal", 0) #Deprecated field - TODO: check template for dependency then remove.
        self._addProperty("BuyFaceFlag", acmTrade.Nominal() < 0 and "Sell" or "Buy")
        
        self._changePropertyValue("Quantity", 1)
        
        #Connected_TrdNbr : value passed as alternateId "FRONT2", for DownStream Systems
        self._addProperty("FarTrade_TrdNbr", otherleg_trdnbr)

        self._addChild(FXSwapInstrumentWrapper(instr, trade))

    def _getFlowCount(self, trade):
        ins = trade.insaddr
        cashflow_cnt = 0 #sum ( [len([cf for cf in leg.cash_flows()]) for leg in ins.legs()] )
        payment_cnt = len(list(trade.payments()))
        additional_cnt = trade.fee and 1
        return cashflow_cnt + payment_cnt + additional_cnt

    def _getCashflowCount(self, instr):
        # Business logic: we differentiate a FX Forward and FX Swap by the number of cashflows.
        if instr:
            return sum ( [len(list(leg.cash_flows())) for leg in instr.legs()] )
        
    def _isFarLeg(self, trade):
        acmTrade = acm.FTrade[trade.trdnbr]
        return acmTrade.IsFxSwapFarLeg()


class FXOutrightInstrumentWrapper(FXInstrumentWrapper):
    def __init__(self, instr, trade):
        FXInstrumentWrapper.__init__(self, instr, trade, FXLegWrapper)
        
        acmTrade = acm.FTrade[trade.trdnbr]
        
        self._changePropertyValue("Instype", "FX Forward")
        self._addProperty("SubType", "Forward")
        
        #babalo test this
        baseCcy = getNominalCurrency(trade)
        nominal = baseCcy == instr.curr.insid and trade.quantity or trade.premium
                
        self._changePropertyValue("Curr", baseCcy == instr.curr.insid and instr.curr.insid or trade.curr.insid)
        self._addProperty("BaseCurrency", baseCcy == instr.curr.insid and instr.curr.insid or trade.curr.insid)
        self._addProperty("QuotedCurrency", baseCcy == instr.curr.insid and trade.curr.insid or instr.curr.insid)
        
        #BuyFaceFlag
        self._addProperty("BuyFaceFlag", nominal < 0 and "true" or "false")
        
        self._addProperty("BasePerQuoted", baseCcy == instr.curr.insid and "false" or "true")
                        
        self._changePropertyValue('exp_day', acmTrade.ValueDay())
        self._changePropertyValue('contr_size', abs(acmTrade.Premium()))
        

    def _getCashflowCount(self, instr):
        # Business logic: we differentiate a FX Forward and FX Swap by the number of cashflows.
        if instr:
            return sum ( [len(list(leg.cash_flows())) for leg in instr.legs()] )

    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper, clsCashFlowWrapper):
        acmTrade = acm.FTrade[trade.trdnbr]
        
        if acmTrade:
            legWrappers = []
            
            if self._getSpecialCase(trade):
                baseCcy = getNominalCurrency(trade)
                base_curr = baseCcy == instr.curr.insid and instr.curr.insid or trade.curr.insid
                quoted_curr = baseCcy == instr.curr.insid and trade.curr.insid or instr.curr.insid
                
                Payleg_Wrapper = FXOutrightLegWrapper(trade, quoted_curr, trade.premium, 1)
                
                Receiveleg_Wrapper = FXOutrightLegWrapper(trade, base_curr, trade.quantity, 0)
                
                legWrappers.append(Payleg_Wrapper)
                legWrappers.append(Receiveleg_Wrapper)
            else:
                if trade.premium < 0:
                    Payleg_Wrapper = FXOutrightLegWrapper(trade, self._getLegCurrency(trade, instr, trade.premium), \
                                                          trade.premium, 1)
                    if trade.fee:
                        Payleg_Wrapper._addChild( FlowWrapper("Broker", trade.fee, ReformatDate(trade.value_day), \
                                                self._getLegCurrency(trade, instr, trade.premium), trade.broker_ptynbr not \
                                                in (None, "", 0) and "Broker" or "", TMS_Functions.Get_BarCap_SDS_ID(trade.broker_ptynbr)))
                    
                    Receiveleg_Wrapper = FXOutrightLegWrapper(trade, self._getLegCurrency(trade, instr, trade.quantity), \
                                                              trade.quantity, 0)
                    
                    legWrappers.append(Payleg_Wrapper)
                    legWrappers.append(Receiveleg_Wrapper)
                else:
                    Payleg_Wrapper = FXOutrightLegWrapper(trade, self._getLegCurrency(trade, instr, trade.quantity), \
                                                          trade.quantity, 1)
                    if trade.fee:
                        Payleg_Wrapper._addChild( FlowWrapper("Broker", trade.fee, ReformatDate(trade.value_day), \
                                                self._getLegCurrency(trade, instr, trade.quantity), trade.broker_ptynbr not \
                                                in (None, "", 0) and "Broker" or "", TMS_Functions.Get_BarCap_SDS_ID(trade.broker_ptynbr)))
                    
                    Receiveleg_Wrapper = FXOutrightLegWrapper(trade, self._getLegCurrency(trade, instr, trade.premium), \
                                                              trade.premium, 0)
                    
                    legWrappers.append(Payleg_Wrapper)
                    legWrappers.append(Receiveleg_Wrapper)
                                                    
            for leg in legWrappers:
                self._addChild(leg)
    
    def _getLegCurrency(self, trade, instr, leg):
        
        if trade:
            
            baseCcy = getNominalCurrency(trade)
            nominal = baseCcy == instr.curr.insid and trade.quantity or trade.premium
            
            base_currency = baseCcy == instr.curr.insid and instr.curr.insid or trade.curr.insid
            quoted_currency = baseCcy == instr.curr.insid and trade.curr.insid or instr.curr.insid
            
            if abs(trade.premium) == abs(leg):
                if abs(leg) == abs(nominal):
                    return base_currency
                else:
                    return quoted_currency
            else:
                if  abs(leg) != abs(nominal):
                    return quoted_currency
                else:
                    return base_currency
                    
    def _getSpecialCase(self, trade):
        if trade:
            return (trade.quantity in (-1, 1, 0) and trade.premium in (-1, 1, 0))
        
class FXSwapInstrumentWrapper(FXInstrumentWrapper):
    def __init__(self, instr, trade):
        FXInstrumentWrapper.__init__(self, instr, trade, FXLegWrapper)

        acmTrade = acm.FTrade[trade.trdnbr]
        self._changePropertyValue("Instype", "FX Forward")
        self._addProperty("SubType", "FXSwap")
        
        baseCcy = getNominalCurrency(trade)

        #TODO: check logic and that field mappings are correct.
        if self._isFarLeg(trade):
            far_leg = acmTrade
            near_leg = otherleg(trade)
            
            self._changePropertyValue('exp_day', acmTrade.ValueDay())
            if near_leg:
                 #baseCcy = near_leg.Instrument().Currency().Name()
                 contr_size = near_leg.Premium()
        else:
            far_leg = otherleg(trade)
            near_leg = acmTrade
            contr_size = acmTrade.Premium()
            
            if far_leg:
                self._changePropertyValue('exp_day', far_leg.ValueDay())
        
        self._changePropertyValue('contr_size', contr_size)

        self._changePropertyValue('Curr', baseCcy)
        self._addProperty("BaseCurrency", baseCcy)
        #self._addProperty("BasePerQuoted", near_leg.QuantityIsDerived() and "true" or "false")
        self._addProperty("BasePerQuoted", baseCcy == instr.curr.insid and "false" or "true")
        
        self._addProperty("QuotedCurrency", baseCcy == acmTrade.Currency().Name() and acmTrade.Instrument().Currency().Name() or acmTrade.Currency().Name())
                        
    def _getCashflowCount(self, instr):
        # Business logic: we differentiate a FX Forward and FX Swap by the number of cashflows.
        if instr:
            return sum ( [len(list(leg.cash_flows())) for leg in instr.legs()] )

    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper, clsCashFlowWrapper):
        
        if self._isFarLeg(trade):
            near_trade = otherleg(trade)
            far_trade = acm.FTrade[trade.trdnbr]
        else:
            near_trade = acm.FTrade[trade.trdnbr]
            far_trade = otherleg(trade)
            
        swap_trades = []
        swap_trades.append(ael.Trade[near_trade.Oid()])
        swap_trades.append(ael.Trade[far_trade.Oid()])
                        
        if swap_trades:
            legWrappers = []
            
            for swap_trade in swap_trades:
                legWrapper = FXSwapLegWrapper(None, swap_trade, contractsize)
                
                # All the below logic handles the base and quoted currency as well as whether we are 
                # buying or selling in the given (base/quoted) currency.
                if self._isFarLeg(swap_trade):
                    nearTrade = ael.Trade[near_trade.Oid()]
                    if nearTrade.fee:
                        legWrapper._addChild( FlowWrapper("Broker", nearTrade.fee, ReformatDate(nearTrade.value_day), \
                                            nearTrade.curr.insid, nearTrade.broker_ptynbr not in (None, "", 0) and "Broker" or "", TMS_Functions.Get_BarCap_SDS_ID(nearTrade.broker_ptynbr)) )
                                                
                legWrappers.append(legWrapper)

            for leg in legWrappers:
                self._addChild(leg)

# FXSwap vs FXFwd differences
# It is possible to check if the instrument is a Fx Swap or an Outright by checking if one 
# or both of the fields nominal_at_start and nominal_at_end are set. It is enough to check 
# one of the legs. Fx Swap, both are set. Outright, one or the other is set depending on 
# which leg is used.
       
    def _isFarLeg(self, trade):
        acmTrade = acm.FTrade[trade.trdnbr]
        return acmTrade.IsFxSwapFarLeg()
        
class FXOutrightTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == "FxSwap":
            leg = instr.legs()[0]
            return (leg.nominal_at_start or leg.nominal_at_end) and \
                     not (leg.nominal_at_start and leg.nominal_at_end)

    def _name(self):
        return "FxOutright"

    def create(self, trade):
        return FXOutrightTradeWrapper(trade)

class FXSwapTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == "FxSwap":
            leg = instr.legs()[0]
            return leg.nominal_at_start and leg.nominal_at_end

    def _name(self):
        return "FxSwap"

    def create(self, trade):
        return FXSwapTradeWrapper(trade)

### FXFuture Classes ###
class FXFutureTradeWrapper(FXTradeWrapper):
    def __init__(self, trade):
        FXTradeWrapper.__init__(self, trade)
        
        instr = self._getInstrument()

        if TradeIsInverted(trade):
	        nominal = trade.quantity * instr.contr_size * trade.price
        else:
	        nominal = trade.quantity * instr.contr_size

        self._addFloatProperty("TradeNominal", abs(nominal))
        self._addProperty("BuyFaceFlag", trade.quantity < 0 and "Sell" or "Buy")
        self._changePropertyValue("Quantity", 1)
        self._addFloatProperty("Rate", trade.price, 17)
        
        self._addChild(FXFutureInstrumentWrapper(instr, trade))

class FXFutureInstrumentWrapper(FXInstrumentWrapper):
    def __init__(self, instr, trade):
        FXInstrumentWrapper.__init__(self, instr, trade, FXLegWrapper)
        
        self._changePropertyValue("Instype", "FX Forward")
        self._addProperty("SubType", "Future")
        
        if TradeIsInverted(trade):
            self._addProperty("BaseCurrency", instr.strike_curr.insid)
            self._addProperty("QuotedCurrency", getUnderlyingInstrument(trade).insid)
            self._changePropertyValue("Curr", instr.strike_curr.insid)
            self._addProperty("BasePerQuoted", "true")
                        
        else:
            self._addProperty("BaseCurrency", getUnderlyingInstrument(trade).insid)
            self._addProperty("QuotedCurrency", instr.strike_curr.insid)
            self._changePropertyValue("Curr", getUnderlyingInstrument(trade).insid)
            self._addProperty("BasePerQuoted", "false")
       
        #BuyFaceFlag
        self._addProperty("BuyFaceFlag", trade.quantity < 0 and "true" or "false")

        self._changePropertyValue('contr_size', instr.contr_size)

    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper, clsCashFlowWrapper):
        
        if TradeIsInverted(trade):
            base_curr = instr.strike_curr.insid
            quoted_curr = getUnderlyingInstrument(trade).insid
            base_nominal = trade.quantity * instr.contr_size * trade.price
            quoted_nominal = trade.quantity * instr.contr_size

        else:
            base_curr = getUnderlyingInstrument(trade).insid
            quoted_curr = instr.strike_curr.insid
            base_nominal = trade.quantity * instr.contr_size
            quoted_nominal = trade.quantity * instr.contr_size * trade.price
        
        Payleg_Wrapper = FXOutrightLegWrapper(trade, quoted_curr, quoted_nominal, 1)
        
        Receiveleg_Wrapper = FXOutrightLegWrapper(trade, base_curr, base_nominal, 0)
        
        self._addChild(Payleg_Wrapper)
        self._addChild(Receiveleg_Wrapper)

class FXDerivativeTradeWrapper(FXTradeWrapper):
    def __init__(self, trade):
        FXTradeWrapper.__init__(self, trade)

        instr = self._getInstrument()

        #Calculate trade price - TODO: CHECK.
        if TradeIsInverted(trade):
            if instr.strike_quotation_seqnbr.seqnbr == 9:
                nominal_amount = trade.quantity * instr.strike_price * instr.contr_size
            else:
                nominal_amount = trade.quantity * round(1/instr.strike_price, 5) * instr.contr_size
        else:
            nominal_amount = trade.quantity * instr.contr_size
        
        #Calculate Trade Nominal - ensure that 
        self._addFloatProperty("TradeNominal", abs(nominal_amount))
        
        if instr.paytype == 'Future':
            rate = abs(self._getCurrencyFutureOptionPricePerContract(trade, instr, nominal_amount))
        else:
            rate = abs(trade.premium / nominal_amount)
            
        self._addFloatProperty("Rate", nominal_amount and rate or 0, 17)
        self._addProperty("BuyFaceFlag", nominal_amount < 0 and "Sell" or "Buy")

    def _getCurrencyFutureOptionPricePerContract(self, trade, instr, nominal_amount):
        
        if instr.quote_type == 'Other':
            return ( trade.price / (10 * instr.contr_size) * trade.quantity / nominal_amount )
        if instr.quote_type == 'Per Contract':
	    return trade.price / instr.contr_size
        if instr.quote_type == 'Per 100 Contracts':
            return ( trade.price * 100 * trade.quantity / nominal_amount )
        return ( trade.price * 10 * trade.quantity / nominal_amount )

###FX Vanilla Classes###
class FXVanillaTradeWrapper(FXDerivativeTradeWrapper):
    def __init__(self, trade):
        FXDerivativeTradeWrapper.__init__(self, trade)
        
        instr = self._getInstrument()
        
        self._addChild(FXVanillaInstrumentWrapper(self._getInstrument(), trade, FXBaseLegWrapper))
    

""" Base class for all FX Derivative based Instruments"""
class FXDerivativeInstrumentWrapper(DerivativeInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None, clsCashflowWrapper = None):
        DerivativeInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsCashflowWrapper)
        
        #Strike should be inverted based on Strike Quotation as well as Instrument Quotation.
        if instr.strike_price > 0 and TradeIsInverted(trade) == ( instr.strike_quotation_seqnbr.seqnbr == 9):
            self._addFloatProperty("OptionStrike",  round(1/instr.strike_price, 5), 17)
        else:
            self._addFloatProperty("OptionStrike", instr.strike_price, 17)
                
        self._addFloatProperty("Premium", trade.premium)
        self._addProperty("BuyOrSell", trade.quantity < 0 and "Sell" or "Buy")
        self._addProperty("PayoffInCashOrAsset", instr.settlement == "Physical Delivery" and "Asset" or "Cash")
        self._addProperty("PayOffDate", ReformatDate(GetDeliveryDate(trade)) )
        
        #changes for front 4.3 Strike and Instrument Currency changes
        if TradeIsInverted(trade):
            settle_curr = getUnderlyingInstrument(trade).insid
        else:
            settle_curr = instr.strike_curr.insid
        
        #Add Settlement currency for cash settled options 
        #as well as base and quoted currency and the premium currency.
        if instr.settlement == "Cash":
            # Front Arena 4.3 FX Hotfix , cash Currency change
            #self._addProperty("SettlementCurrency", getAdditionalInfo(trade, "Settlement_Currency") or strike_curr) #default to domestic ccy
            self._addProperty("SettlementCurrency", getAdditionalInfo(instr, "Settlement_Curr") or settle_curr)
        else: #Else settlement is physical and no settlement currency is appropriate, default to ZZZ.
            self._addProperty("SettlementCurrency", "ZZZ")

        if TradeIsInverted(trade):
            self._addProperty("BaseCurrency", instr.strike_curr.insid)
            self._addProperty("QuotedCurrency", getUnderlyingInstrument(trade).insid)
            self._changePropertyValue("Curr", instr.strike_curr.insid)
                        
        else:
            self._addProperty("BaseCurrency", getUnderlyingInstrument(trade).insid)
            self._addProperty("QuotedCurrency", instr.strike_curr.insid)
            self._changePropertyValue("Curr", getUnderlyingInstrument(trade).insid)
            
        self._addProperty("PremiumCurrency", trade.curr.insid)
        #NewField required for CRE
        self._addProperty("ExpiryCutTime", instr.fixing_source_ptynbr and instr.fixing_source_ptynbr.ptyid or "")
            

    #Override default leg structure
    def _addLegsToInstrument(self, instr, trade, contractsize, clsLegWrapper = None, clsCashflowWrapper = None):
        if instr:
            #updated code for 4.3 upgrade, instr.legs() no longer returns dummy leg for derivatives
            #must invoke the legs() method for the underlying instrument
            Legs = getUnderlyingInstrument(trade).legs()
            for leg in Legs:
                if clsLegWrapper:
                    objLeg = clsLegWrapper(leg, trade, instr.contr_size)
                else:
                    objLeg = LegWrapper(leg, trade, instr.contr_size)

                cp = TMS_Functions.Get_BarCap_SDS_ID(trade.counterparty_ptynbr)
                
                # Add fee structure
                if instr.instype == "Option" and instr.und_instype == "Curr" and \
                    instr.exotic_type == "None" and not instr.digital:
                    if instr.paytype != 'Future':
                        if trade.premium:
                            objLeg._addChild( FlowWrapper("Premium", trade.premium, trade.value_day.to_string("%Y-%m-%d"), \
                                                   trade.curr.insid, "", cp))
                else:
                    if trade.premium:
                        objLeg._addChild( FlowWrapper("Premium", trade.premium, trade.value_day.to_string("%Y-%m-%d"), \
                                                   trade.curr.insid, "", cp))
                if trade.fee:
                    objLeg._addChild( FlowWrapper("Broker", trade.fee, trade.value_day.to_string("%Y-%m-%d"), \
                                                   trade.curr.insid, trade.broker_ptynbr not in (None, "", 0) and "Broker Fee" or "", TMS_Functions.Get_BarCap_SDS_ID(trade.broker_ptynbr)) )

                objLeg._sortCashflows()
                self._addChild(objLeg)

    def _getFamily(self):
        return "FXO"
        
class FXVanillaInstrumentWrapper(FXDerivativeInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        FXDerivativeInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper)
        
        self._addProperty("SubType", instr.exotic_type and "" or "Vanilla")
        if TradeIsInverted(trade):
            self._addProperty("OptionPayoffStyle", instr.call_option and "Put" or "Call")
        else:
            self._addProperty("OptionPayoffStyle", instr.call_option and "Call" or "Put")

class FXVanillaTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        #We check that the instrument is an option and the underlying is a currency.
        #We also check that the instrument is not exotic (implies vanilla)
        #else all Currency Options would be picked up by this factory.
        return instr.instype == "Option" and instr.und_instype == "Curr" and \
               instr.exotic_type == "None" and not instr.digital

    def _name(self):
        return "Vanilla"

    def create(self, trade):
        return FXVanillaTradeWrapper(trade)

###FX Digital Classes###
class FXCashOrNothingTradeWrapper(FXDerivativeTradeWrapper):
    def __init__(self, trade):
        FXDerivativeTradeWrapper.__init__(self, trade)

        instr = self._getInstrument()
        self._addChild(FXCashOrNothingInstrumentWrapper(instr, trade, FXBaseLegWrapper))

class FXCashOrNothingInstrumentWrapper(FXDerivativeInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        FXDerivativeInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper)
        
        #settleCcy = getAdditionalInfo(trade, "Settlement_Currency") or instr.strike_curr.insid #default to domestic ccy.
        # Front Arena 4.3 FX Hotfix , cash Currency change
        
        if TradeIsInverted(trade):
            if instr.settlement == "Cash":
                digitalpayoff_settle_Ccy = getAdditionalInfo(instr, "Settlement_Curr") or getUnderlyingInstrument(trade).insid
            else:
                digitalpayoff_settle_Ccy = getAdditionalInfo(instr, "Settlement_Curr") or instr.strike_curr.insid
        else:
            if instr.settlement == "Cash": 
                digitalpayoff_settle_Ccy = getAdditionalInfo(instr, "Settlement_Curr") or instr.strike_curr.insid
            else:
                digitalpayoff_settle_Ccy = getAdditionalInfo(instr, "Settlement_Curr") or getUnderlyingInstrument(trade).insid

        #TODO: refactor base class so append can be used instead of change.
        self._changePropertyValue("Instype", "FX Option")
        self._addProperty("SubType", "Digital")
        
        #Option Ccy/
        self._changePropertyValue("Curr", instr.settlement == "Cash" and digitalpayoff_settle_Ccy or getUnderlyingInstrument(trade).insid)

        #Get option pay-off style
        if TradeIsInverted(trade):
            if instr.strike_curr.insid == digitalpayoff_settle_Ccy:
                payoffStyle = instr.call_option and "DigitalCall" or "DigitalPut"
            else:
                payoffStyle = instr.call_option and "DigitalPut" or "DigitalCall"
        else:
            if getUnderlyingInstrument(trade).insid == digitalpayoff_settle_Ccy:
                payoffStyle = instr.call_option and "DigitalCall" or "DigitalPut"
            else:
                payoffStyle = instr.call_option and "DigitalPut" or "DigitalCall"

        self._addProperty("OptionPayoffStyle", payoffStyle)
        #self._addProperty("DigitalPayoffCurrency", getAdditionalInfo(trade, "Settlement_Currency") or instr.strike_curr.insid)
        # Front Arena 4.3 FX Hotfix , cash Currency change
        self._addProperty("DigitalPayoffCurrency", digitalpayoff_settle_Ccy)
        self._addProperty("PayoffInCashOrAsset", instr.settlement == "Physical Delivery" and "Asset" or "Cash")

class FXCashOrNothingTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        return instr.instype == "Option" and instr.und_instype == "Curr" \
            and instr.digital and instr.exotic_type == "None"

    def _name(self):
        return "Digital"

    def create(self, trade):
        return FXCashOrNothingTradeWrapper(trade)

###FX Barrier Classes###
#The FXBarrierTradeWrapper Class will deal with the following variants due to similarity:
# - Single Barrier
# - Double Barrier

class FXBarrierTradeWrapper(FXDerivativeTradeWrapper):
    def __init__(self, trade):
        FXDerivativeTradeWrapper.__init__(self, trade)

        self._addChild(FXBarrierInstrumentWrapper(self._getInstrument(), trade, FXBaseLegWrapper))

class FXBarrierEvent(Wrapper):
    def __init__(self, startDate, endDate):
        Wrapper.__init__(self)

        self._addProperty("StartDate", startDate)
        self._addProperty("EndDate", endDate)

    def getTypeName(self):
        return "BARRIEREVENT"

class FXBaseBarrierInstrumentWrapper(FXDerivativeInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        FXDerivativeInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper)

        self._exotic = instr.exotic()

        self._changePropertyValue("Instype", "FX Option")
        self._addProperty("BarrierMonitoring", self._exotic.barrier_monitoring)
         
        self._addProperty("OptionExpiryStyle", instr.exercise_type != "None" and instr.exercise_type or "")
        
        #front 4.3 strike and instrument currency changes
        if TradeIsInverted(trade):
            settle_curr = getUnderlyingInstrument(trade).insid
        else:
            settle_curr = instr.strike_curr.insid
            
        strike_curr = instr.strike_curr.insid
        
        #self._addProperty("RebateCurrency", getAdditionalInfo(trade, "Settlement_Currency") or strike_curr) #default to domestic ccy
        # Front Arena 4.3 FX Hotfix , cash Currency change
        self._addProperty("RebateCurrency", getAdditionalInfo(instr, "Settlement_Curr") or settle_curr)
            
        if instr.barrier == 0:
            barrier1_amount = instr.barrier
        else:
            if TradeIsInverted(trade) and instr.strike_quotation_seqnbr.seqnbr == 9:
                barrier1_amount = round((1/instr.barrier), 5)
            else:
                barrier1_amount = instr.barrier
            
        
        if self._exotic.barrier_option_type in ("Double In", "Double Out"):
            if self._exotic.double_barrier == 0:
                barrier2_amount = self._exotic.double_barrier
            else:
                if TradeIsInverted(trade) and instr.strike_quotation_seqnbr.seqnbr == 9:
                    barrier2_amount = round((1/self._exotic.double_barrier), 5)
                else:
                    barrier2_amount = self._exotic.double_barrier
        
        if self._exotic.barrier_option_type in ("Double In", "Double Out"):
            self._addFloatProperty("BarrierAmount", barrier2_amount)
            self._addFloatProperty("Barrier2Amount", barrier1_amount)
        else:
            self._addFloatProperty("BarrierAmount", barrier1_amount)
                   
        self._addProperty("DelayRebate", self._exotic.barrier_rebate_on_expiry and "true" or "false")
        
        #front 4.3 changes, rebate should be revised as per spec... ?
        if TradeIsInverted(trade) and instr.strike_quotation_seqnbr.seqnbr == 9:
            self._addFloatProperty("Rebate", instr.strike_price > 0 and (instr.rebate/(1/instr.strike_price)) or instr.rebate, 17)
        else:
            self._addFloatProperty("Rebate", instr.strike_price > 0 and (instr.rebate/instr.strike_price) or instr.rebate, 17)

        #Handle Barrier Monitoring period depending on type.
        if self._exotic.barrier_monitoring == "Continuous":
            self._addChild(FXBarrierEvent(ReformatDate(trade.time), ReformatDate(instr.exp_day)))
            self._addProperty("MonitoringType", "Single")
        elif self._exotic.barrier_monitoring in ("Discrete", "Window"):
            exoticEvents = list(instr.exotic_events())
            if len(exoticEvents):
                self._addProperty("MonitoringType", len(exoticEvents) > 1 and "Multi" or "Single")
                #Currently only a single discrete/window monitoring period is allowed by TMS.
                for ee in exoticEvents:
                    if ee.type == "Barrier date":
                        self._addChild(FXBarrierEvent(ReformatDate(ee.date),
                                                      self._exotic.barrier_monitoring == "Window" and ReformatDate(ee.end_date) or ReformatDate(ee.date)))

        self._sortBarrierEvents()

        #Get barrier "knock" type
        #front 4.3 changes, Double Knock in and Knock out with new Enumeration values
        if self._exotic.barrier_option_type:
            self._addProperty("UpOrDown", self._exotic.barrier_option_type in ("Up & In", "Up & Out") and "Up" or "Down")
            self._addProperty("InOrOut", self._exotic.barrier_option_type in ("Up & In", "Down & In", "Double In") and "In" or "Out")
            
            #front 4.3 changes, Double Knock in and Knock out with new Enumeration values
            #BarrierCrossed date is sometimes left blank by the users when updating BarrierCrossed Status in front
            if self._exotic.barrier_crossed_status == "Confirmed":
                self._addProperty("BarrierCrossDate", self._exotic.barrier_cross_date and ReformatDate(self._exotic.barrier_cross_date) or ReformatDate(instr.updat_time))
                self._addProperty("BarrierCrossed", self._exotic.barrier_option_type in ("Up & In", "Down & In", "Double In") and "KnockIn" or "KnockOut")

    def _sortBarrierEvents(self):
        #Sort the Barrier Events of the Instrument be ascending start date.
        self._children.sort(lambda x, y: x.getTypeName() == "BARRIEREVENT" and cmp(x._getPropertyValue("StartDate"), y._getPropertyValue("StartDate")))

    def _getExotic(self):
        return self._exotic
    
    def _getBarrierLevels(self, barrier_amount, barrier2_amount, barrier_type):
        if barrier_type == "Double Out":
            self._addFloatProperty("BarrierAmount", barrier_amount > barrier2_amount and barrier_amount or barrier2_amount)
            self._addFloatProperty("Barrier2Amount", barrier_amount < barrier2_amount and barrier_amount or barrier2_amount)
        else:
            self._addFloatProperty("BarrierAmount", barrier_amount < barrier2_amount and barrier_amount or barrier2_amount)
            self._addFloatProperty("Barrier2Amount", barrier_amount > barrier2_amount and barrier_amount or barrier2_amount)

class FXBarrierInstrumentWrapper(FXBaseBarrierInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        FXBaseBarrierInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper)

        if TradeIsInverted(trade):
            self._addProperty("OptionPayoffStyle", instr.call_option and "Put" or "Call")
        else:
            self._addProperty("OptionPayoffStyle", instr.call_option and "Call" or "Put")
            
        #front 4.3 changes handling double barrier options
        self._addProperty("SubType", self._exotic.barrier_option_type in ("Double In", "Double Out") and "DoubleBarrier" or "SingleBarrier")

class FXBarrierTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == "Option" and instr.und_instype == "Curr" \
            and instr.exotic_type != "None":
            #Now we will filter for continuous monitoring period.
            return instr.exotic().barrier_monitoring in ("Continuous", "Discrete", "Window") \
                    and instr.exotic().digital_barrier_type == "None"

    def _name(self):
        return "Barrier"

    def create(self, trade):
        return FXBarrierTradeWrapper(trade)

class FXTouchTradeWrapper(FXDerivativeTradeWrapper):
    def __init__(self, trade):
        FXDerivativeTradeWrapper.__init__(self, trade)

        instr = self._getInstrument()
        self._addChild(FXTouchInstrumentWrapper(self._getInstrument(), trade, FXBaseLegWrapper))

class FXTouchInstrumentWrapper(FXBaseBarrierInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        FXBaseBarrierInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper)

        #front 4.3 payout currency changes
        #payout_curr = instr.settlement == 'Cash' and instr.strike_curr.insid or getUnderlyingInstrument(trade).insid
        
        if TradeIsInverted(trade):
            payout_curr = getAdditionalInfo(instr, "Settlement_Curr") or getUnderlyingInstrument(trade).insid
        else:
            payout_curr = getAdditionalInfo(instr, "Settlement_Curr") or instr.strike_curr.insid
                    
        touchType = self._exotic.barrier_option_type in ('Up & Out', 'Down & Out') and "NoTouch" or "OneTouch"
        
        self._changePropertyValue("SettlementCurrency", payout_curr)
        
        #OptionStrike price not used for American Binary Options - Barrier Amounts are used.
        self._changePropertyValue("OptionStrike", 0)
        #front 4.3 changes, for Digital touches, Touches always settled in cash
        self._changePropertyValue("PayoffInCashOrAsset", "Cash")
        #front 4.3 changes, for Digital touches, Rebate should be defaulted to 1
        self._changePropertyValue("Rebate", 1)
        self._changePropertyValue("exercise_type", self._exotic.barrier_option_type in ("Up & Out", "Up & In", "Down & Out", "Down & In", "Double In", "Double Out") \
                            and "American" or "European")
        self._changePropertyValue("RebateCurrency", payout_curr)
        self._changePropertyValue("PayOffDate", ReformatDate(GetDeliveryDate(trade)) )
        self._changePropertyValue("OptionExpiryStyle", self._exotic.barrier_option_type in ("Up & Out", "Up & In", "Down & Out", "Down & In", "Double In", "Double Out") \
                            and "American" or "European")
        self._addProperty("DigitalPayoffCurrency", payout_curr)
        self._addProperty("SubType", self._exotic.barrier_option_type in ('Double In', 'Double Out') and "DoubleTouch" or touchType)
        self._addProperty("OptionPayoffStyle", "Digital")

class FXTouchTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == "Option" and instr.und_instype == "Curr" \
            and instr.exotic_type != "None":
            #Now we will filter for continuous monitoring period.
            return instr.exotic().barrier_monitoring in ("Continuous", "Discrete", "Window") \
                    and instr.exotic().digital_barrier_type == "Barrier"

    def _name(self):
        return "Touch"

    def create(self, trade):
        return FXTouchTradeWrapper(trade)

    
class FXBaseLegWrapper(FXDerivativeLegWrapper):
    def __init__(self, leg, trade, contractsize):
        FXDerivativeLegWrapper.__init__(self, leg, trade, contractsize)
        
        if TradeIsInverted(trade):
            instr = trade.insaddr
            if instr.strike_quotation_seqnbr.seqnbr == 9:
                self._changePropertyValue("L_Curr", leg.display_id('curr')== instr.strike_curr.insid and getUnderlyingInstrument(trade).insid or instr.strike_curr.insid)
                self._changePropertyValue("LegNominal", abs((trade.quantity * instr.strike_price) * instr.contr_size * leg.nominal_factor))
            else:
                self._changePropertyValue("LegNominal", abs((trade.quantity * round(1/instr.strike_price, 5)) * instr.contr_size * leg.nominal_factor))
        
        
###FX Average Rate###
class FXAvgRateTradeWrapper(FXDerivativeTradeWrapper):
    def __init__(self, trade):
        FXDerivativeTradeWrapper.__init__(self, trade)

        self._addChild(FXAvgRateInstrumentWrapper(self._getInstrument(), trade))

class FXFixingEvent(Wrapper):
    def __init__(self, date, amount, value):
        Wrapper.__init__(self)

        self._addProperty("Date", date)
        self._addFloatProperty("Amount", amount)
        self._addFloatProperty("Value", value)

    def getTypeName(self):
        return "FIXINGEVENT"

class FXAvgRateInstrumentWrapper(FXDerivativeInstrumentWrapper):
    def __init__(self, instr, trade, clsLegWrapper = None):
        FXDerivativeInstrumentWrapper.__init__(self, instr, trade, clsLegWrapper, clsLegWrapper)

        self._exotic = instr.exotic()

        self._changePropertyValue("Instype", "FX Option")
        self._addProperty("SubType", "Asian")

        self._addProperty("OptionPayoffStyle", instr.call_option and "Call" or "Put")
        self._addProperty("OptionExpiryStyle", instr.exercise_type != "None" and instr.exercise_type or "")

        exoticEvents = list(instr.exotic_events())
        if len(exoticEvents):
            timeSeries = getTimeSeriesDict(instr, FIXING_TIMESERIES)
            for ee in exoticEvents:
                #Note that to accomodate weightings (not supported natively by front)
                #we add our fixing weightings to a time series.
                self._addChild(FXFixingEvent(ReformatDate(ee.date),
                                             ee.value,
                                             timeSeries and timeSeries[ReformatDate(ee.date)] or 1.0))

class FXAvgRateTradeWrapperFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == "Option" and instr.und_instype == "Curr" \
            and instr.exotic_type != "None":
            return instr.exotic_type == "Other" and instr.exotic().average_strike_type == "Fix"

    def _name(self):
        return "Avg"

    def create(self, trade):
        return FXAvgRateTradeWrapper(trade)
    
    
class FXHedgingWrapperFactory(FXTradeWrapperFactory):
    def supports(self, trade):
        return self._supports(trade)

class FXSwapFactory(FXHedgingWrapperFactory):
    def _supports(self, trade):
        
        acmTrade = acm.FTrade[trade.trdnbr]
        instr = acmTrade.Instrument()
        if instr.InsType() == "Curr":
            if acmTrade.IsFxSwapNearLeg():
                trd_far_leg = acm.FTrade.Select01("connectedTrdnbr=%i and oid<>%i" % (acmTrade.Oid(), acmTrade.Oid()), "Moan")
                if trd_far_leg:
                    return (acmTrade, trd_far_leg)
            elif acmTrade.IsFxSwapFarLeg():
                trd_near_leg_nbr = acmTrade.ConnectedTrdnbr()
                if trd_near_leg_nbr:
                    trd_near_leg = acm.FTrade[trd_near_leg_nbr]
                if trd_near_leg:
                    return (trd_near_leg, acmTrade)
            
                
    
    def _name(self):
        return "FXSwap"
    
    def create(self, trade):
        return FXSwapTradeWrapper(trade)
    
class FXOutrightFactory(FXHedgingWrapperFactory):
    def _supports(self, trade):
        
        acmTrade = acm.FTrade[trade.trdnbr]
        instr = acmTrade.Instrument()
        if instr.InsType() == "Curr":
            if acmTrade.IsFxForward() or acmTrade.IsFxSpot():
                return (acmTrade)
                
    
    def _name(self):
        return "FxOutright"
    
    def create(self, trade):
        return FXOutrightTradeWrapper(trade)
    
class FXFutureFactory(FXTradeWrapperFactory):
    def _supports(self, instr):
        if instr.instype == "Future/Forward" and instr.und_instype == "Curr" \
            and instr.paytype == "Future":
            return instr.settlement == "Cash"
    
    def _name(self):
        return "FxFuture"
    
    def create(self, trade):
        return FXFutureTradeWrapper(trade)

class FXOutrightLegWrapper(Wrapper):
    def __init__(self, trade, leg_currency, leg_nominal, pay_leg):
        Wrapper.__init__(self)
        
        if trade:
            acmTrade = acm.FTrade[trade.trdnbr]

            self._addProperty("L_Curr", leg_currency)
            self._addProperty("start_day", ReformatDate(trade.time))
            self._addProperty("end_day", ReformatDate(trade.value_day))
            self._addProperty("payleg", pay_leg and "yes" or "no")
            self._addFloatProperty("LegNominal", abs(leg_nominal))
            
            if pay_leg:
                for p in acmTrade.Payments():
                    self._addPaymentToLeg(p, trade, pay_leg)
            
    def _sortCashflows(self):
        self._children.sort(lambda cfx, cfy: cmp((cfx._getPropertyValue("Date"), cfx._getPropertyValue("Amount")), (cfy._getPropertyValue("Date"), cfy._getPropertyValue("Amount"))))
    
    def _addCashflowToLeg(self, cashflow, leg, quantity, contractsize, clsCashFlowWrapper = None):
        pass

    def _addPaymentToLeg(self, acmPayment, trade, leg):
        flowType = CASHFLOWTYPE_MAPPING.get(acmPayment.Type()) or "Additional"
        acmTrade = acm.FTrade[trade.trdnbr]
        if leg:
            if acmPayment.Type() == "Premium" and not trade.premium:
                self._addChild( FlowWrapper("Premium",
                                            acmPayment.Amount(),
                                            ReformatDate(acmPayment.PayDay()),
                                            acmPayment.Currency().Name(),
                                            "",
                                            TMS_Functions.Get_BarCap_SDS_ID(acmPayment.Party())) )
            else:
                self._addChild( FlowWrapper(flowType,
                                            acmPayment.Amount(),
                                            ReformatDate(acmPayment.PayDay()),
                                            acmPayment.Currency().Name(),
                                            acmPayment.Type(),
                                            TMS_Functions.Get_BarCap_SDS_ID(acmPayment.Party())) )
    
            self._sortCashflows()

    def getTypeName(self):
        return "LEG"
                         
class FXSwapLegWrapper(Wrapper):
    def __init__(self, leg, trade, contractsize):
        Wrapper.__init__(self)
        
        if trade:
            acmTrade = acm.FTrade[trade.trdnbr]
            nearLegTrade = self._isFarLeg(acmTrade) and otherleg(trade) or acmTrade
            farLegTrade = self._isFarLeg(acmTrade) and acmTrade or otherleg(trade)
            
            instr = trade.insaddr
            
            self._addProperty("start_day", nearLegTrade.ValueDay())
            self._addProperty("end_day", farLegTrade.ValueDay())
            self._addFloatProperty("Rate", trade.price, 17)
                
            if not self._isFarLeg(acmTrade):
                
                self._addProperty("L_Curr", instr.curr.insid)
                self._addProperty("payleg", trade.quantity > 0 and "no" or "yes")
                self._addFloatProperty("LegNominal", abs(trade.quantity))
                self._addProperty("LegType", "NearLeg")
                self._addProperty("Currency", instr.curr.insid)
                self._addProperty("BuyFaceFlag", trade.quantity > 0 and "true" or "false")
                
            else:
                
                self._addProperty("L_Curr", trade.curr.insid)
                self._addProperty("payleg", trade.premium > 0 and "yes" or "no")
                self._addFloatProperty("LegNominal", abs(trade.premium))
                self._addProperty("LegType", "FarLeg")
                self._addProperty("Currency", trade.curr.insid)
                self._addProperty("BuyFaceFlag", trade.premium > 0 and "true" or "false")
                                            
            for p in acmTrade.Payments():
                self._addPaymentToLeg(p, trade, leg)

    def _isFarLeg(self, trade):
         return trade.IsFxSwapFarLeg()
    
    def _sortCashflows(self):
        self._children.sort(lambda cfx, cfy: cmp((cfx._getPropertyValue("Date"), cfx._getPropertyValue("Amount")), (cfy._getPropertyValue("Date"), cfy._getPropertyValue("Amount"))))
    
    def _addCashflowToLeg(self, cashflow, leg, quantity, contractsize, clsCashFlowWrapper = None):
        pass

    def _addPaymentToLeg(self, acmPayment, trade, leg):
        flowType = CASHFLOWTYPE_MAPPING.get(acmPayment.Type()) or "Additional"
        
        acmTrade = acm.FTrade[trade.trdnbr]
        
        if acmPayment.Type() == "Premium" and not acmTrade.Premium():
           self._addChild( FlowWrapper("Premium",
                                        acmPayment.Amount(),
                                        ReformatDate(acmPayment.PayDay()),
                                        acmPayment.Currency().Name(),
                                        "",
                                        TMS_Functions.Get_BarCap_SDS_ID(acmPayment.Party())) )
        else:
            self._addChild( FlowWrapper(flowType,
                                        acmPayment.Amount(),
                                        ReformatDate(acmPayment.PayDay()),
                                        acmPayment.Currency().Name(),
                                        acmPayment.Type(),
                                        TMS_Functions.Get_BarCap_SDS_ID(acmPayment.Party())) )

        self._sortCashflows()

    def getTypeName(self):
        return "LEG"

#List of Wrapper Factories for external use
TradeWrapperFactories = [
        FXVanillaTradeWrapperFactory(),
        FXCashOrNothingTradeWrapperFactory(),
        FXBarrierTradeWrapperFactory(),
        FXAvgRateTradeWrapperFactory(),
        FXTouchTradeWrapperFactory(),
        FXSwapFactory(),
        FXOutrightFactory(),
        FXFutureFactory()
    ]

