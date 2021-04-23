""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FOptionParams - Option parameters
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts common option parameters for a given instrument
    
NOTE            
    Concerning the new naming conventions:
    call_option has been replaced by put_call, since _option is redundant
    and the order put, call makes it easier to associate to the numeric
    representations put=0, call=1.
    
----------------------------------------------------------------------------"""
import ael
import math
import sys

FOptionError = "EXPC_F_OPTION_ERROR"

"""----------------------------------------------------------------------------
CLASS                   
    FOptionParams - Parameters for vanilla options

INHERITS
    
DESCRIPTION             
    The class extracts all parameters needed to value an ordinary option.

CONSTRUCTION    
    i               Instrument  An instrument that is a vanilla option

MEMBERS                 
    insid           string      The instrument insid.
    valuation_date  date        The valuation date. Information when shifting time.
    price           Float       Price of underlying stock
    exp_day         date        The expiry, AEL date    
    texp            Float       Time to expiry (in years)                       
    vol             Float       Volatility of stock price
    rate            Float       Risk-free interest rate
    underlying      string      The underlying instrument id
    carry_cost      Float       Cost of carry rate
    strike          Float       Strike price
    put_call        Int 0|1     1=call option, 0=put option
    eur_ame         Int 0|1     0=European option, 1=American option
    dividends       List        List of dividends, pairs[value,date]
    currency        string      The instrument isdefines in this currency
    contr_size      double      The contract size.
    quote_type      string      The quote type.
    und_quote_type  string      The quote type of the underlying instrument.
    df              Float       Discount factor.
    
METHODS
    pv()            The method returns the present value of the option.
                    The method takes no arguments.
    __str__()       Returns an informal string description of the class.
    __repr__()      Returns a foraml string description of the class.
    
----------------------------------------------------------------------------"""
class FOptionParams:
    def __init__(self, i):
        "Class to extract common option parameters"
         
        self.insid = i.insid    
        self.valuation_date = ael.date_valueday() 
        self.exp_day = i.exp_day    
        und_ins = i.und_insaddr
        if und_ins == None:
            raise FOptionError, "The option " + self.insid + " has no underlying instrument."
        self.und_instype = und_ins.instype
        self.price = i.used_und_price(i.undprice_type())
        self.texp = self.valuation_date.years_between(self.exp_day, 'Act/365')
        self.strike = i.strike_price
        self.strike_curr = i.strike_curr
        self.vol = i.used_vol() / 100
        
        self.underlying = und_ins.insid
        self.currency = i.curr.insid
        self.contr_size = i.contr_size
        self.quote_type = i.quote_type
        self.und_quote_type = und_ins.quote_type
        if self.und_quote_type == 'Per 100 Units':
            self.price = self.price / 100.0
        if self.und_instype != "Curr":
            self.strike_theor_curr_fx = i.strike_curr.used_price(None, i.curr.insid) 
        else: self.strike_theor_curr_fx = 1    

        self.yield_curves = i.used_yield_curves()
        self.used_context = i.used_context_parameter('Valuation Function', 1)
        self.vol_surface = i.used_volatility(i.curr).vol_name
        
        yc = i.used_yield_curve(i.curr) 
        self.rate = i.used_discount_rate()/100
        
        yc_repo = i.und_insaddr.used_repo_curve(i.und_insaddr.curr)
        exp_offset = self.exp_day.add_banking_day(i.curr, i.pay_day_offset)
        valuation_date_offset = self.valuation_date.add_banking_day(i.und_insaddr.curr, i.und_insaddr.spot_banking_days_offset)
        self.repo = yc_repo.yc_rate(valuation_date_offset, exp_offset, 'Continuous', 'Act/365', 'Spot Rate')
        
        self.carry_cost = i.used_carry_cost()/100
        self.put_call = i.call_option
        
        if    i.exercise_type == 'American': self.eur_ame = 1
        elif  i.exercise_type == 'European': self.eur_ame = 0
        elif  i.instype == 'Future/Forward': self.eur_ame = 0
        else: raise FOptionError, "Excercise type not handled."
        
        self.div_entity = i.und_insaddr.dividends(self.exp_day)
        self.dividends = []
        
        for d in i.und_insaddr.dividends(self.exp_day):
            div_date = self.valuation_date.years_between(d.ex_div_day, 'Act/365')
            # Only take in account the dividends that are payed out before the expiry of the option. 
            if div_date <= self.texp: self.dividends.append((d.dividend, div_date))
        
        rf_exp = yc.yc_rate(self.exp_day, exp_offset, 'Annual Comp', 'Act/365', 'Spot Rate')
        toffset = self.exp_day.years_between(exp_offset, 'Act/365')
        self.df = math.pow(1+rf_exp, -toffset)
        self.settlement = i.settlement
        if und_ins.original_curr != None: self.orig_currency = {und_ins.insid:und_ins.original_curr.insid}
        
        self.fix_fx = i.fix_fx
        if self.fix_fx:
            self.fx_rate     = i.fix_fx_rate

            # Determine the fx volatility
            vol_surf_fx      = self.strike_curr.used_volatility(i.curr)
            self.vol_surf_fx = vol_surf_fx.vol_name
            self.fx_vol      = vol_surf_fx.volatility(self.strike_curr.used_price(None, i.curr.insid), self.exp_day, self.valuation_date, self.put_call)

            # Get the foreign risk free rate.
            ycf              = i.und_insaddr.used_yield_curve(i.und_insaddr.curr)
            self.foreign_yc  = ycf.ir_name
            self.foreign_rate= ycf.yc_rate(self.valuation_date, self.exp_day, 'Continuous', 'Act/365', 'Spot Rate') 
        
        # Number of days to add to the expiry when specifying the last cash flow date.
        if i.settlement == "Physical": self.extra_days = i.pay_day_offset
        else: self.extra_days = i.und_insaddr.spot_banking_days_offset           
        
    def pv(self):
        try:
            if not (self.und_instype == 'Stock' or self.und_instype == 'EquityIndex' or self.und_instype == 'Curr'):
                raise FOptionError, "FEqOption only handles vanilla options with Stock,EquityIndex or Curr as underlying instrument, not "+ self.und_instype
            if self.exp_day < self.valuation_date:
                # FOptionParams: The option has expired.
                i = ael.Instrument[self.insid]
                if self.valuation_date > ael.date_today():
                    # A time shift has been made. Use a forward underlying price.
                    exp_price = math.exp(-self.rate*self.texp)*self.price
                else:
                    # Use the historic price of the underlying asset.
                    exp_price = i.und_insaddr.mtm_price(self.exp_day)
                if self.settlement == 'Cash':
                    if self.put_call: return max(exp_price - self.strike, 0)
                    else: return max(self.strike - exp_price, 0)
                elif self.settlement == 'Physical Delivery':
                    if self.put_call:
                        if (exp_price - self.strike) > 0.0: return max(self.price - self.strike, 0)
                        else:return 0.0
                    else: 
                        if (self.strike - exp_price) > 0.0: return max(self.strike - self.price, 0)
                        else: return 0.0
                else:
                    raise FOptionError, "The settlementtype " + str(self.settlement) + "is not handled."

            res = ael.eq_option(self.price, self.texp, self.vol, self.rate, self.carry_cost,
                                    self.strike, self.put_call, self.eur_ame, self.dividends)
            if res != -1:
                res = res * self.df
            else: 
                # Some error occured or the option is expired.
                res = 0
            return res
        except FOptionError, msg:
            print msg
            return 0

    def __str__(self):
        return 'insid=%(insid)s price=%(price)f texp=%(texp)f vol=%(vol)f rate=%(rate)f carry_cost=%(carry_cost)f \
                strike=%(strike)f put_call=%(put_call)d eur_ame=%(eur_ame)d df=%(df)f    '%vars(self)

    def __repr__(self):
        return self.__str__()
    

def FOptionParamsList(i):
    o = FOptionParams(i)
    return [o.price, o.texp, o.vol, o.rate, o.carry_cost, o.strike, o.put_call, o.eur_ame, o.dividends, o.df]



    




