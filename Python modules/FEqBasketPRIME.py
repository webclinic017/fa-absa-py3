""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqBasketPRIME - Basket options are valued. PRIME calls the valuation.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the price of a basket option. European options with 
   discrete dividends are handled.
 ----------------------------------------------------------------------------""" 
import ael
import math
import FEqBasketUtils
from FEqUtilsPRIME import *

F_BASKET_EXCEPT = 'f_eq_basket_xcp'  

"""----------------------------------------------------------------------------
refCombLink() 
    Find a certain combinationlink, given a combination instrument and a 
    stock/equity index.
----------------------------------------------------------------------------"""    
def refCombLink(und, objReference):
    if und and objReference:
        try:
            return ael.CombinationLink.read('owner_insaddr='+str(und.insaddr)+ \
                               'and member_insaddr='+str(objReference.insaddr)+ \
                               'and orderbook_oid=0')                                       
        except: return None
"""----------------------------------------------------------------------------
get_fix_rate() 
    Return the fix fx rate for a basket component.
----------------------------------------------------------------------------"""    
def get_fix_rate(stock_link):
    return stock_link.fix_fx_rate
    

"""----------------------------------------------------------------------------
get_basket_dividends_sum
    The function calculates the sum of the future dividends discounted to today.
----------------------------------------------------------------------------"""    
def get_basket_dividends_sum(stock, valuation_date, exp_day, texp):
    yc = stock.used_yield_curve(stock.curr)
    rate = yc.yc_rate(valuation_date, exp_day, 'Continuous', 'Act/365', 'Spot Rate')
    div_sum = 0
    for div in stock.dividends(exp_day):
        value = div.dividend
        time = valuation_date.years_between(div.ex_div_day, 'Act/365')
        if 0 <= time <= texp and value >= 0:
            div_sum = div_sum + value*math.exp(-rate*time)
    return div_sum

"""----------------------------------------------------------------------------
FBasketParams
    The class contains all valuation parameters necessary for basket option val.
----------------------------------------------------------------------------"""    
class FBasketParams:
    def __init__(self, i, vanilla_params, basket_params, quanto_params):
        # Plain vanilla parameters
        self.texp     = vanilla_params[0]
        self.rate     = vanilla_params[1]
        self.strike   = vanilla_params[2]
        self.put_call = vanilla_params[3]
        exc_type      = vanilla_params[4]
        
        # Basket parameters
        self.price       = AsList(basket_params[0])
        self.vol         = AsList(basket_params[1])
        
        try:
            if str(type(basket_params[2])) == "<type 'str'>":
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, basket_params[2]
            self.corr_stocks= AsMatrix(basket_params[2])
        except Exception, msg:
            print "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, "No correlations are defined."
        
        self.carry_cost  = AsList(basket_params[3])
        self.weights     = AsList(basket_params[4])
        self.dim         = basket_params[5]   
        self.quanto_flag = basket_params[6]
        self.fx_error    = basket_params[7]
        self.no_fx_ins   = basket_params[8]
        self.dividends   = AsMatrix(basket_params[9])
        
        # Quanto Basket parameters
        if self.quanto_flag:
            self.fx            = AsList(quanto_params[0])
            try: float(self.fx[0])
            except: 
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, self.fx[0]
            self.fxvol         = AsList(quanto_params[1])
            try:
                if str(type(quanto_params[2])) == "<type 'str'>":
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BASKET_EXCEPT, quanto_params[2]
                self.corr_fx = AsMatrix(quanto_params[2])
            except Exception, msg:
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, "No FX correlations are defined."
            try:
                if str(type(quanto_params[3])) == "<type 'str'>":
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BASKET_EXCEPT, quanto_params[3]
                self.corr_stock_fx = AsMatrix(quanto_params[3])
            except Exception, msg:
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, "No FX/Stock correlations are defined."
            self.corr_stock_fx = AsMatrix(quanto_params[3])
            self.rate_stocks   = AsList(quanto_params[4])
        
        if exc_type == 'European' or exc_type == 0:self.eur_ame = 0
        else: self.eur_ame = 1
        
        if self.quanto_flag: self.fixfx_flag = 1
        else: self.fixfx_flag = 0

"""----------------------------------------------------------------------------
FUNCTION    
    TheorBasketOption() 

DESCRIPTION
    The function TheorBasketOption() calculates the price of a basket 
    option. 
    
ARGUMENTS
    vanilla_params[]    A list with all standard vanilla parameters, like strike.
    basket_params[]     A list with quanto basket specific parameters. 
                          - price[]:          The stock prices
                          - stock_vol[]:      Volatilities for each stock
                          - fx[]:             The fx rates for each combination link
                          - fx_vol[]:         The volatilites of the fx rates.
                          - corr_stocks[[]]:  The correlations between the stocks in 
                                              the basket.
                          - corr_fx[[]]:      The correlation between the fx rates.
                          - corr_stock_fx[[]]:The correlation between each stock and
                                              its fx rate.
                          - stock_rate[]:     The discount rate for each stock.
                          - stock_carry_cost[]:The carry_cost for each stock.
                          - stock_weights[]:  The weights of the stocks in the basket.
                          - dim               The number of stocks in the basket.             
    n_o_simulation      The number of simulations to use if a numerical valuation 
                        method is chosen.
    val_model           The name of the valuation method to use.

RETURNS
   res                  float                 The value of the basket option.
----------------------------------------------------------------------------"""   
def TheorBasketOption(i, vanilla_params, basket_params, quanto_params, val_meth_params):
    for p in basket_params[0]:
        try: float(p)
        except: return {"PV":'No underlying price!'}
    if len(basket_params[0]) == 0: return {"PV":'The basket is empty!'}
    try:
        bp = FBasketParams(i, vanilla_params, basket_params, quanto_params)
        bp.df = get_discount_factor(i)            
        res = FEqBasketUtils.get_pv(bp, val_meth_params)
        return {"PV":res, "Delta":"theorGlobalBasketDelta", "DeltaPct":"theorGlobalBasketDeltaPct",\
                "Gamma":"theorGlobalBasketGamma", "GammaPct":"theorGlobalBasketGammaPct",\
                "Vega":"theorGlobalVega"}
    except F_BASKET_EXCEPT, msg: 
        print '\nModule: FEqBasketPRIME'
        print 'Error :', msg
        print 'Instr :', i.insid
        return {"PV":'Valuation error!'}

    






