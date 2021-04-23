'''
Purpose: Corrected functions AccruedDiscBal, PLPos and DailyAccrued for use by ASQL query called "IB internal MM trades". 
	 Added currentnominal function to return current nominal from Trading Manager. 
	 Added function to return Daily Cash column from TM.
	 Added function to return the notional amount, underlying instrument type, underlying instrument id and dividend amounts.
	 Added in Commodities as underlying type for Fut/Fwd - was not included previously.
	 Change notional amount calculation for TRS with underlying Bond or Index Linked Bond instrument
         Add in functions to return the correct issuer for instruments.
	 Corrected the notional calcualtion for forwards and option with underlying commodity instrument (base metal and energy)
	 Added in function to return the PV of ACM trade object - called from extension attribute ExternalVal
	 Added Notional calculation for Price Swap instruments and Underlying Instrument logic for PriceSwap Instruments
	 Added Quote Type Metric Tonne and apdated Future/Forward Notional AMount calculation.
Department: MM, SM PCG MONEY MARKET, OPS, Regulatory reporting, Regulatory reporting, F&CM - Regulatory, MR, PCG, Pricing & Risk I.T., PCG, PCG, PCG
Requester: Balan Pillay, Lizel Graham, Christo Davids, Callie Joubert, Callie Joubert, Noloyiso Mahlakahlaka, Tshiamo Tsogang, Suveshan Iyaloo, Matthew Berry, Priyanka Padayachee, Tammy Bourgstein
Developer: Willie van der Bank, Jaysen Naicker, Bhavnisha Sarawanm,  Jaysen Naicker,  Jaysen Naicker,  Jaysen Naicker, Jaysen Naicker, Jaysen Naicker, Jaysen Naicker, Heinrich Cronje, Heinrich Cronje
CR Number: 194677 (12/01/2010), 289044 (2010-04-22), 394472 (2010-08-10), 420707 (2010-09-03), 486730 (2010-11-12), 576445 (2011-02-18), 706729 (07/07/2011), 889905  (10/02/2012), CHNG0000318798  (12/07/2012), XXXXXX, CHNG0001589018 (12/03/2013)
'''

import ael	
import acm
import math
import FCreditLimit
from FBDPCommon import acm_to_ael 
from FBDPCommon import ael_to_acm 
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FPortfolioSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
class TradeSheetCalcSpace(object):
    TS_CALC_SPACE = acm.FCalculationSpace('FTradeSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = TradeSheetCalcSpace.TS_CALC_SPACE.CreateCalculation( obj, column_id )
        return calc

def get_fxSubTypeDetail(temp, aelTrade, columnId, *rest):
    calc = TradeSheetCalcSpace.get_column_calc(acm.FTrade[aelTrade.trdnbr], columnId)
    return calc.Value()

def ValEnd(temp,trd,repdate,curr, *rest):	
    t           = acm.FTrade[trd.trdnbr]	
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', NewEndDate)
	SheetCalcSpace.CALC_SPACE.SimulateValue(t, 'Portfolio Currency', curr)
        calc  = SheetCalcSpace.get_column_calc(t, 'Portfolio Value End')
	Value = calc.Value().Number()
    finally:
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        SheetCalcSpace.CALC_SPACE.RemoveSimulation(t, 'Portfolio Currency')
    return Value


def ValEnd_ACM(temp,t,repdate,curr, *rest):	
    repdate = ael.date(repdate)
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', repdate)
	SheetCalcSpace.CALC_SPACE.SimulateValue(t, 'Portfolio Currency', curr)
        calc  = SheetCalcSpace.get_column_calc(t, 'Portfolio Value End')
	Value = calc.Value().Number()
    finally:
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        SheetCalcSpace.CALC_SPACE.RemoveSimulation(t, 'Portfolio Currency')
    return Value
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def CashDaily(temp,trd,repdate,curr, *rest):	
    t           = acm.FTrade[trd.trdnbr]	
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', NewEndDate)
	SheetCalcSpace.CALC_SPACE.SimulateValue(t, 'Portfolio Currency', curr)
        calc  = SheetCalcSpace.get_column_calc(t, 'Portfolio Accumulated Cash Daily')
	Value = calc.Value().Number()
    finally:
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        SheetCalcSpace.CALC_SPACE.RemoveSimulation(t, 'Portfolio Currency')
    return Value    


'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def AccruedDiscBal(temp, trd, repdate, curr, *rest):
   
    t           = acm.FTrade[trd.trdnbr]	
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	#SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date','Custom Date')
	#SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom' ,NewEndDate)
	#SheetCalcSpace.CALC_SPACE.SimulateValue(t,'Portfolio Currency' ,curr)
        #calc  = SheetCalcSpace.get_column_calc(t,'Accrued Discount Balance')
	#Value = calc.Value().Number()
	calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', repdate)
        calc        = calc_space.CalculateValue(t, 'Accrued Discount Balance')
	Value = calc
    finally:
        #SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        #SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        #SheetCalcSpace.CALC_SPACE.RemoveSimulation(t,'Portfolio Currency')
    return Value
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def PresentValue(temp, trd, *rest):
    t       = acm.FTrade[trd.trdnbr]
    calc    = SheetCalcSpace.get_column_calc(t, 'Portfolio Value End')
    pv      = calc.Value().Number()
    return pv
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def PLPos(temp, trd, repdate, curr, *rest):

    t           = acm.FTrade[trd.trdnbr]	
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', NewEndDate)
	SheetCalcSpace.CALC_SPACE.SimulateValue(t, 'Portfolio Currency', curr)
        calc  = SheetCalcSpace.get_column_calc(t, 'Portfolio Position')
	#Value = calc.Value().Number()
	Value = calc.Value()
    finally:
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        SheetCalcSpace.CALC_SPACE.RemoveSimulation(t, 'Portfolio Currency')
    return Value


'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def DailyAccrued(temp, trd, curr, *rest):

    t           = acm.FTrade[trd.trdnbr]	
    calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
    calc        = calc_space.CalculateValue(t, 'Daily Interest')
    Value       = calc.Value().Number()

    return Value
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def CreditLimitCP(temp, trd, *rest):
    return FCreditLimit.limit_cp(trd.counterparty_ptynbr)


'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def CurrentNominal(temp, trd, repdate, curr, *rest):

    t           = acm.FTrade[trd.trdnbr]	
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', NewEndDate)
	SheetCalcSpace.CALC_SPACE.SimulateValue(t, 'Portfolio Currency', curr)
        calc  = SheetCalcSpace.get_column_calc(t, 'Current Nominal')
	Value = calc.Value()
    finally:
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        SheetCalcSpace.CALC_SPACE.RemoveSimulation(t, 'Portfolio Currency')
    return Value
    
    '''
    t = acm.FTrade[trd.trdnbr]
    trdrow = acm.CreateTradeRow(t,1)
    tag = acm.CreateEBTag()
    v = acm.GetCalculatedValueFromString(trdrow,'Standard','object:*"Credit_Limit_cp"',tag)
    if v.PropertiesText('Value') == ' ':
        val = 0    
    else:
        val = v.Value()
    '''
    
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
def PLPosTM(temp, trd, repdate, curr, *rest):

    t           = acm.FTrade[trd.trdnbr]	
    diff        = ael.date_today().days_between(repdate)
    NewEndDate  = ael.date_today().add_days(diff)
    Value       = 0
    try:
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
	SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', NewEndDate)
	SheetCalcSpace.CALC_SPACE.SimulateValue(t, 'Portfolio Currency', curr)
        calc  = SheetCalcSpace.get_column_calc(t, 'Portfolio Profit Loss Period Position')
        if type(calc.Value()) == type(1.00):
            Value = calc.Value()
        else:
            Value = 0
    finally:
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        SheetCalcSpace.CALC_SPACE.RemoveSimulation(t, 'Portfolio Currency')
    return Value
    
    
'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
'''
[AbsaSpecific]FInstrument:Credit_Limit_cp = (ael("FCreditLimit", context).limit_cp(CParty));
[AbsaSpecific]FMultiInstrumentAndTrades:Credit_Limit_cp = maxOf(trades :* "Credit_Limit_cp");
[AbsaSpecific]FPortfolioInstrumentAndTrades:Credit_Limit_cp = nil;
[AbsaSpecific]FSingleInstrumentAndTrades:Credit_Limit_cp = nil;
[AbsaSpecific]FTrade:Credit_Limit_cp = (ael("FCreditLimit", context).limit_cp(CParty));
[AbsaSpecific]FTradeRow:Credit_Limit_cp = trade:Credit_Limit_cp;


[AbsaSpecific]FTradingSheet:Daily Accrued Interest =
  ExtensionAttribute=accrued_daily
  GroupLabel=Trade
  LabelList=Daily Accrued Interest
  Name=Daily Accrued Interest


[AbsaSpecific]FCashFlowInstrument:accrued_daily = object.interest_accrued( , endDate);
[AbsaSpecific]FInstrumentAndTrades:accrued_daily = accrued - object :* "accruedEnd - accruedStart" [endDate = date_add_banking_day(endDate, , -1)];
'''

# Used to get insaddr of external ccy from CRE
def get_currnbr(temp, curr, *rest):
    if ael.Instrument[curr]:
        try:
            return str(ael.Instrument[curr].insaddr)
        except:
            return ""
    else:
        return ""

'''--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------'''
Quote_type = {}
Quote_type['None'] = 1.0
Quote_type['Pct of Nominal'] = 1.0
Quote_type['Clean'] = 1.0
Quote_type['Unadj Clean'] = 1.0
Quote_type['100-rate'] = 1.0
Quote_type['Yield'] = 1.0
Quote_type['Coupon'] = 1.0
Quote_type['Per Unit'] = 1.0
Quote_type['Per 100 Units'] = 0.01
Quote_type['Per 10 000 Units'] = 0.0001
Quote_type['Per Million'] = 0.000001
Quote_type['Per Contract'] = 1.0
Quote_type['Simple Rate'] = 1.0
Quote_type['Discount Rate'] = 1.0
Quote_type['Pctpct of Nom'] = 1.0
Quote_type['Per 100 Contracts'] = 1.0
Quote_type['Per 1000 of Nom'] = 1.0
Quote_type['Per 1000 Clean'] = 1.0
Quote_type['Volatility'] = 1.0
Quote_type['Float Factor'] = 1.0
Quote_type['Metric Tonne'] = 1.0


def get_underlyingIns(temp, t, *rest):
    uins = None
    ins = ael_to_acm(t).Instrument()
    if t.insaddr.instype == 'TotalReturnSwap':
        iLegs = t.insaddr.legs()
        for iLeg in iLegs:
            if iLeg.type == 'Total Return':
                uins = iLeg.index_ref     
            
    elif ins.InsType() == 'IndexLinkedSwap':     
        
        for iLeg in ins.Legs():
            if iLeg.InflationScalingRef() is not None:
                uins = acm_to_ael(iLeg.InflationScalingRef())    

    elif t.insaddr.instype == 'Swap':
        iLegs = t.insaddr.legs()
        for iLeg in iLegs:
            if iLeg.type == 'Float':
                uins = iLeg.float_rate
                
    elif t.insaddr.instype == 'CreditDefaultSwap':
        iLegs = t.insaddr.legs()
        for iLeg in iLegs:
            if iLeg.type == 'Credit Default':
                uins = iLeg.credit_ref
    
    elif t.insaddr.instype == 'Combination':
        c_links = t.insaddr.combination_links()
        for c_link in c_links:
            if c_link.member_insaddr.instype == 'CreditDefaultSwap':
                iLegs = c_link.member_insaddr.legs()
                for iLeg in iLegs:
                    if iLeg.type == 'Credit Default':
                        uins = iLeg.credit_ref
    
    elif t.insaddr.instype == 'PriceSwap':
        iLegs = t.insaddr.legs()
        for iLeg in iLegs:
            if iLeg.type == 'Float':
                uins = iLeg.float_rate
                break
    
    elif t.insaddr.instype in ('Future/Forward', 'Option', 'VarianceSwap'):
        uins = t.insaddr.und_insaddr
    return uins


def get_underlyingInsType(temp, t, *rest):
    uinstype = ''
    if get_underlyingIns('', t):
        uinstype = get_underlyingIns('', t).instype
    return uinstype


def get_underlyingInsID(temp, t, *rest):
    uinsID = None
    if get_underlyingIns('', t):
        uinsID = get_underlyingIns('', t).insid
    return uinsID
    
   
def get_dividend(temp, i, start_day, end_day, *rest):   
    val = 0.0    
    divs = i.historical_dividends()
    for div in divs:
        if div.ex_div_day > start_day and div.ex_div_day < end_day:
            val = val + div.dividend
    return val            

            
def get_underlyingDividend(temp, t, start_day, end_day, *rest):
    val = 0.0
    uins = get_underlyingIns('', t)
    if uins.instype == 'Stock':
        val = get_dividend('', uins, start_day, end_day)
            
    elif uins.instype == 'EquityIndex':
        for cl in uins.combination_links():
            val = val + get_dividend('', cl.member_insaddr, start_day, end_day) * cl.weight / uins.index_factor          
    return val

        
def get_dividendEstimate(temp, i, start_day, end_day, *rest):   
    val = 0.0    
    divStreams = ael.DividendStream.select("insaddr = %s" % i.insaddr)
    
    for divStream in divStreams.members():
        for divEst in divStream.estimates():
            if divEst.ex_div_day > start_day and divEst.ex_div_day < end_day:
                val = val + divEst.dividend
    return val            

            
def get_underlyingDividendEstimate(temp, t, start_day, end_day, *rest):
    val = 0.0
    uins = get_underlyingIns('', t)
    if uins.instype == 'Stock':
        val = get_dividendEstimate('', uins, start_day, end_day)
            
    elif uins.instype == 'EquityIndex':
        for cl in uins.combination_links():
            val = val + get_dividendEstimate('', cl.member_insaddr, start_day, end_day) * cl.weight / uins.index_factor          
    return val


def get_price(temp, ins, rep_day, curr, *rest):
    if ins.mtm_price(rep_day, curr, 0, 0) <> 0.0:
        return ins.mtm_price(rep_day, curr, 0, 0)
    elif ins.used_price(rep_day, curr, 'None', 0, 'SPOT') <> 0 :
        return ins.used_price(rep_day, curr, 'None', 0, 'SPOT')
    elif ins.used_price(rep_day, curr, 'None', 0, 'internal') <> 0:
        return ins.used_price(rep_day, curr, 'None', 0, 'internal')
    else:
        return 0


def get_underlyingInsaddr(temp, t, *rest):
    uinsID = ''
    
    if get_underlyingIns('', t):
        uinsID = get_underlyingIns('', t).insaddr

    return str(uinsID)


def get_IssuerName(temp, t, *rest):
    IssuerName = ''
    if t.insaddr.instype == 'CreditDefaultSwap':
        if get_underlyingIns('', t):
            IssuerName = get_underlyingIns('', t).issuer_ptynbr.ptyid
    elif t.insaddr.instype == 'Combination':
        c_links = t.insaddr.combination_links()
        for c_link in c_links:
            if c_link.member_insaddr.instype == 'CreditDefaultSwap':
                iLegs = c_link.member_insaddr.legs()
                for iLeg in iLegs:
                    if iLeg.type == 'Credit Default':
                        IssuerName = iLeg.credit_ref.issuer_ptynbr.ptyid
    else:
        if t.insaddr.issuer_ptynbr:
            IssuerName = t.insaddr.issuer_ptynbr.ptyid
        
    return IssuerName

    
def get_notional(temp, t, rep_day, curr, fx_rate, *rest):
    val = 0.0
    rep_day = ael.date(rep_day)
    
    if t.insaddr.instype == 'TotalReturnSwap':
        u = get_underlyingIns('', t)
        if u.instype in ('Stock', 'EquityIndex'):
            if t.insaddr.insid.lower().__contains__('divswap'):
                val = (get_underlyingDividend('', t, t.value_day, t.insaddr.exp_day) + get_underlyingDividendEstimate('', t, t.value_day, t.insaddr.exp_day)) * t.quantity
            else:
		if rep_day == ael.date_today() :
                	val = t.insaddr.used_und_price() * fx_rate * t.quantity * Quote_type[u.quote_type]
		else:
			val = get_price('', u, rep_day, u.curr.insid) * t.quantity * Quote_type[u.quote_type]
        elif u.instype in ('IndexLinkedBond', 'Bond'):
                val = t.nominal_amount(rep_day) * fx_rate
        else:
            if t.insaddr.exp_day > rep_day:
                val = t.quantity * fx_rate
            else:
                val = t.nominal_amount(rep_day) * fx_rate
                
    elif t.insaddr.instype == 'Future/Forward':
        u = get_underlyingIns('', t)
        if u.instype in ('Stock', 'EquityIndex'):
            if u.insid.lower().__contains__('_divfut_underlying'):
                val = get_underlyingDividendEstimate('', t, rep_day, t.insaddr.exp_day) * t.nominal_amount(rep_day)
            else :
                if rep_day == ael.date_today() :
                    val = t.insaddr.used_und_price() * fx_rate  * t.nominal_amount(rep_day) * Quote_type[u.quote_type]
                else:
                    val = get_price('', u, rep_day, curr) * t.nominal_amount(rep_day) * Quote_type[u.quote_type]
        elif u.instype == 'Curr':
            val = t.nominal_amount(rep_day) 
        elif u.instype == 'RateIndex':
            val = t.nominal_amount(rep_day) * fx_rate
        elif u.instype == 'Commodity':
            # Portfolios Base Energy Approx and Coal_BTB
            if t.add_info('Barcap BTB UnitType') <> '':
                try:
                    val = get_price('', u, rep_day, curr) * float(t.add_info('Barcap BTB UnitType'))* Quote_type[t.insaddr.quote_type]
                except: 
                    val = 0.0
            else:
                if rep_day == ael.date_today() :
                    try:
                        val = t.insaddr.used_und_price() * fx_rate  * t.nominal_amount(rep_day) * Quote_type[u.quote_type]
                    except:
                        val = t.insaddr.used_und_price() * fx_rate  * t.nominal_amount(rep_day) * Quote_type[u.quotation_seqnbr.name]
                else:
                    try:
                        val = get_price('', u, rep_day, curr) * t.nominal_amount(rep_day) * Quote_type[u.quote_type]
                    except:
                        val = get_price('', u, rep_day, curr) * t.nominal_amount(rep_day) * Quote_type[u.quotation_seqnbr.name]
        else:
            val = t.nominal_amount(rep_day) * fx_rate * t.price 
    
    elif t.insaddr.instype == 'Option':
        u = get_underlyingIns('', t)
        if u.instype in ('Stock', 'EquityIndex'):
            if t.insaddr.digital == 1 or t.insaddr.add_info('Forward Start Type') == 'Performance':
                val = t.nominal_amount(rep_day)
            else:
                if rep_day == ael.date_today() :
                    val = t.insaddr.used_und_price() * fx_rate * t.nominal_amount(rep_day) * Quote_type[u.quote_type]
                else:
                    val = get_price('', u, rep_day, curr) * t.nominal_amount(rep_day) * Quote_type[u.quote_type]
        elif u.instype in ('Bond', 'Swap', 'FRA'):
            if t.insaddr.digital == 1:
                val = t.quantity * fx_rate * Quote_type[u.quote_type]
            else:
                val = t.nominal_amount(rep_day) * fx_rate * Quote_type[u.quote_type]
        # instrument is a Commodity and in portfolio Base Energy Approx or Coal_BTB
        elif u.instype == 'Commodity' and t.add_info('Barcap BTB UnitType') <>  '':
            try:
                val = get_price('', u, rep_day, curr) * float(t.add_info('Barcap BTB UnitType'))* Quote_type[t.insaddr.quote_type]
            except:
                val = 0.0
        else:
            if t.insaddr.digital == 1:
                val = t.quantity * get_price('', u, rep_day, curr) * Quote_type[u.quote_type]
            else:
                val = t.nominal_amount(rep_day) * fx_rate * get_price('', u, rep_day, t.insaddr.curr.insid) * Quote_type[u.quote_type]
                
    elif t.insaddr.instype in ('IndexLinkedSwap', 'Swap', 'CreditDefaultSwap', 'Bond', 'FRN' ):
        val = t.nominal_amount(rep_day)* fx_rate
        
    elif t.insaddr.instype == 'VarianceSwap':
        val = 2* math.sqrt(t.price) * t.quantity
    
    elif t.insaddr.instype == 'PriceSwap':
        acmUndInstrument = None
        quotationType = 'None'
        quotationFactor = 0.0
        underlyingPrice = 0.0
        aelInstrument = t.insaddr
        acmInstrument = acm.FInstrument[aelInstrument.insaddr]

        if acmInstrument:
            for leg in acmInstrument.Legs():
                if leg.LegType() == 'Float':
                    acmUndInstrument = leg.FloatRateReference()
                    break
        
        if acmUndInstrument:
            aelUndInstrument = ael.Instrument[acmUndInstrument.Oid()]
            quotation = acmUndInstrument.Quotation()
            if quotation:
                quotationType = quotation.QuotationType()
                quotationFactor = quotation.QuotationFactor()
                
            underlyingPrice = get_price(temp, aelUndInstrument, rep_day, curr)
        
        if quotationType == 'Weight':
            val = t.quantity * underlyingPrice
        else:
            val = t.quantity * quotationFactor * underlyingPrice
            
    return val

def get_base_underlying(temp, i, *rest):
    if i.und_insaddr != None:
        #print 'xxxx', i.und_insaddr.und_insaddr
        if i.und_insaddr.und_insaddr:
            return i.und_insaddr.und_insaddr
        else:
            return i.und_insaddr
    else:
        return i        
        
    return 0
    

def GNA_Asset_Code(temp, ins, *rest):
    #t = ael.Trade[1581345]          #deposit
    #t = ael.Trade[17975074]         #stock
    #t = ael.Trade[17973926]         #cfd on stock
    #t = ael.Trade[17975073]         #option on cfd on stock
    
    value = ''
    base_und = get_base_underlying(1, ael.Instrument[ins])
    if base_und.add_info('SEDOL'):
        value = base_und.add_info('SEDOL')
    #else:
    #    print 'No SEDOL'

    if value == '':
        value = base_und.isin
    #else:
    #    print 'No ISIN'

    return value
