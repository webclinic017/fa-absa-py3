""" SEQ_VERSION_NR = 2.3.1 """


"""-----------------------------------------------------------------------------
MODULE
    FBasketParams - Parameters for Basket options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for a basket option.
       
EXTERNAL DEPENDENCIES
    FEqBasket
    
-----------------------------------------------------------------------------"""
import ael
import math
import FOptionParams
import FEqBasketUtils
import sys

F_BASKET_EXCEPT = 'f_eq_basket_xcp'  
F_BASKET_WARNING = 'f_eq_basket_warning,'  
DIV_EXCEPTION = "the sum of the discounted dividends' amount are greater than the initial asset price."
UND_EXCEPTION = 'the initial asset price(s) are less than or equal to zero.'
TIMETOEXP_WARNING = 'the option has already expired.'

"""----------------------------------------------------------------------------
CLASS                   
    BasketParams - Parameters for basket options

INHERITS
    FOptionParams
                
DESCRIPTION             
    The class extracts all parameters needed to value a basket option.

CONSTRUCTION    
    i               Instrument  An instrument that is a basket option

MEMBERS                 
    carry_cost[]          float       The cost of carry of the underlying assets.
    weights[]             float       Numbers (or weights) of the underlying assets 
                                      included the option.  
    dim                   float       The number of underlying assets for the option.
    vol[]                 float       A vector with the volatilities of the basket stocks.      
    dividends[]
    rho[[]]               float       rho is a list of lists, with correlations.
    exotic_type
    digital
    currency
    basket_stocks[]
    price_vol_part[]      float       The value of the volatility part of the underlying 
                                      assets, that is,the initial value of the underlying 
                                      asset minus the discounted sum of all future dividends 
                                      paid out prior expiration.
    rate[]                float       A vector of compatibility reasons.
                                      For a normal basket option the rate is the same
                                      for all stocks, but not for a quanto basket option.
----------------------------------------------------------------------------"""
class BasketParams(FOptionParams.FOptionParams):
    def __init__(self, i):
        FOptionParams.FOptionParams.__init__(self, i)
        
        if not (i.und_instype == 'Combination' or i.und_instype == 'EquityIndex'):
            print "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, 'underlying instrument type is not a combination instrument or an EquityIndex.'
        
        und_valgroup = i.und_insaddr.used_context_parameter('Valuation Function')
        if und_valgroup == "EqBasket":
            print "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, 'The underlying instrument ' + str(i.und_insaddr.insid) + ' should NOT be mapped to EqBasket. Pleasa remove the mapping.'
        
        stock_links = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
        stocks = []
        for stock_link in stock_links:
            stocks.append(stock_link.member_insaddr)
        self.dim = len(stock_links)
        if self.dim == 0:
            print "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, 'The basket is empty.'
            
        self.corr_name = FEqBasketUtils.get_corr_matrix(i).name
        
        self.exotic_type = i.exotic_type 
        self.digital = i.digital
        self.underlying = i.und_insaddr.insid
        self.und_price = i.und_insaddr.theor_price()
        adj_fact = i.und_insaddr.index_factor
        try: self.used_context = i.used_context_parameter('Valuation Function', 1)
        except: self.used_context = 'used_context'
        
        # Check if the basket option is a quanto basket option.
        curr_dict = {}
        curr_dict[self.strike_curr.insid] = 1
        for stock_link in stock_links:
            if len(curr_dict) > 1: break
            else:
                stock_curr = stock_link.member_insaddr.curr.insid
                if not curr_dict.has_key(stock_curr):
                    curr_dict[stock_curr] = 1
        if len(curr_dict) > 1 and i.fix_fx: 
            self.quanto_flag = 1
        else: self.quanto_flag = 0
        
        self.vol_surfaces    = []
        self.rate_stocks     = []
        self.basket_stocks   = []
        self.und_quote_types = []
        self.weights         = [] 
        self.price           = []
        self.dividends       = []
        self.div_entities    = []
        self.carry_cost      = []
        self.repo            = []
        self.vol             = []
        self.corr_stocks     = []
        self.fx              = []
        basketsum = 0.0
        
        self.corr_stock_fx_dict = {}
        self.corr_fx_fx = {}
        if self.quanto_flag:
            self.corr_stock_fx  = []
            self.corr_fx        = []
            self.fxvol          = []
            [self.corr_fx, self.corr_fx_fx] = FEqBasketUtils.CorrFx(stocks, i, self.valuation_date, self.strike_curr)
            [self.corr_stock_fx, self.corr_stock_fx_dict] = FEqBasketUtils.CorrStockFx(stocks, i, self.valuation_date, self.strike_curr)
            self.fixfx_flag = 1
            self.fx = FEqBasketUtils.get_fx_rates(stock_links)
        
        # Discrete dividends, the value of the volatility part of the underlying assets
        self.dividends = FEqBasketUtils.get_dividends(stocks, self.exp_day)
        self.yield_curves = [] 
        self.repo_curves = []   
        self.vol_surf_fx = []
        exp_offset = self.exp_day.add_banking_day(self.strike_curr, i.pay_day_offset)
        j = 0
        for stock_link in stock_links:
            # GET ALL PARAMETERS NECESSARY FOR STOCK J.
            stock_j = stock_link.member_insaddr
            try:    
                self.vol_surfaces.append(stock_j.used_volatility(stock_j.curr).vol_name)
            except: self.vol_surfaces = 'vol_name'
               
            # Rate, Get the riskfree rate for each stock.
            yc_j  = stock_j.used_yield_curve(stock_j.curr)
            self.yield_curves.append(yc_j.ir_name)
            self.rate_stocks.append(yc_j.yc_rate(self.valuation_date, self.exp_day, 'Continuous', 'Act/365', 'Spot Rate'))

            # Members, list with stock id's
            self.basket_stocks.append(stock_j.insid)
            
            # Quote types for each stock.
            self.und_quote_types.append(stock_j.quote_type)    
            
            # Weigths
            weight = stock_link.weight
            if (weight <= 0):
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'The weight(s) are less than or equal to zero.'
            self.weights.append(weight)
            
            # Price
            if self.quanto_flag:
                price = stock_j.used_price()
            else:
                price = stock_j.used_price(None, self.strike_curr.insid)
            if stock_j.quote_type == 'Per 100 Units': price = price / 100.0
            self.price.append(price)
            if price == 0.0:
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'The initial price of ' + stock_j.insid + ' is equal to 0.0.'           

            # Used for the information string
            self.div_entities.append(stock_j.dividends(self.exp_day))
            
            # Cost of carry
            yc_repo_j = stock_j.used_repo_curve(stock_j.curr)
            self.repo_curves.append(yc_repo_j.ir_name)
            valuation_date_offset_j = self.valuation_date.add_banking_day(stock_j.curr, \
                                                     stock_j.spot_banking_days_offset)
            texp_carry_j = valuation_date_offset_j.years_between(exp_offset, 'Act/365')
            repo_j = yc_repo_j.yc_rate(valuation_date_offset_j, exp_offset, 'Continuous', 'Act/365', 'Spot Rate')
            self.repo.append(repo_j)
            try:
                self.carry_cost.append(repo_j * texp_carry_j / self.texp)
            except ZeroDivisionError:
                self.carry_cost.append(0.0)
                
            # Compute the sum of the basket today
            if self.quanto_flag:
                # Get the volatilities of the FX rates
                # Volatility surfaces
                if stock_j.curr != self.strike_curr:
                    jvol_surf_fx = stock_j.curr.used_volatility(self.strike_curr)
                    self.vol_surf_fx.append(jvol_surf_fx.vol_name)
                
                    # Determing the volatility:
                    jvol_fx = jvol_surf_fx.volatility(stock_j.curr.used_price(None, self.strike_curr.insid), self.exp_day, self.valuation_date, self.put_call)
                    self.fxvol.append(jvol_fx)
                else: 
                    self.vol_surf_fx.append('None')
                    self.fxvol.append(0.0)
                    
                basketsum = basketsum + weight*stock_j.used_price()*self.fx[j]
            else:
                basketsum = basketsum + weight*stock_j.used_price()
            j = j + 1
            
        # Correlations
        # rho is a list of lists, where the i:th list corresponds the i:th colonn in 
        # the correlation matrix between the returns of the underlying assets. Since the 
        # correlation matrix is symmetrical we only define the upper triangular in the 
        # correlation matrix.
        [self.corr_stocks, self.correlation_dict] = FEqBasketUtils.Corr(stocks, i)

        # Ratio - how much the basket is in the money 
        [self.fx_error, self.no_fx_ins] = FEqBasketUtils.get_fx_error(self.fx, stocks)
        try:
            if not self.fx_error:
                ratio = self.strike / basketsum  
            else: ratio = 0
        except ZeroDivisionError:
            print "\n## !! EXCEPTION !! ##"
            raise F_BASKET_EXCEPT, 'No basket stocks can be found or the prices of all stocks are zero.'
        
        self.orig_currency = {}
        
        for stock_link in stock_links:
            stock_j = stock_link.member_insaddr
            
            # Volatility surfaces
            jvol_surf = stock_j.used_volatility(stock_j.curr)
            
            # Determing the volatility:
            jvol = jvol_surf.volatility(ratio*stock_j.used_price(), self.exp_day, self.valuation_date, self.put_call)
            self.vol.append(jvol)
            if (jvol < 0.0):  
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'The volatility is less than zero.'
            
            # Original currencies of the basket stocks.
            if stock_j.original_curr != None: 
                self.orig_currency.update({stock_j.insid:stock_j.original_curr.insid})

        # Adjust the weights with the adjustment divisor (new_weight = weight/adj divisor).
        self.weights = map(lambda x,y=adj_fact: x/(1.0*y), self.weights)

        # price_vol_part is the volatility part of the underlying assets, i.e.
        # the initial value of the underlying assets minus the discounted
        # sum of all future dividends paid out prior expiration.
        divsum = 0.0
        self.price_vol_part=[]
        for j in range(self.dim): 
            for div in self.dividends[j]:
                if (div[1] <= self.texp) and (div[1] >= 0): 
                    divsum = divsum + div[0]*math.exp(-self.rate_stocks[j]*div[1])
            self.price_vol_part.append(self.price[j]-divsum)
            if ( self.price_vol_part[j] < 0.0 ):
                if (self.price[j] < 0.0):
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BASKET_EXCEPT, UND_EXCEPTION
                else:
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BASKET_EXCEPT, DIV_EXCEPTION
            divsum = 0.0

    def pv(self):
        val_meth_params = FEqBasketUtils.basket_val_meth()
        res = FEqBasketUtils.get_pv(self, val_meth_params)
        return res * self.strike_theor_curr_fx

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()       
    

"""-----------------------------------------------------------------------------
FUNCTION        
    create_addinfo_field()

NOTE
    ONLY USED FOR CLIENTS BASED ON ADM VERSIONS OLDER THAN 33000.
    USE THE ASQL SCRIPT .MaintCreateQuantoBasketFX_ADM32.sql.
    
DESCRIPTION
    Creates AdditionalInfo fields for CombinationLinks. Used when defining the
    fix FX rates for the Quanto Basket option.

ARGUMENTS
    i           Instrument      Quanto Basket option

RETURNS
   insid        string          The name of the option.                           
-----------------------------------------------------------------------------"""
def create_addinfo_field(i,*rest):
    try:
        ai_specnbr = ael.AdditionalInfoSpec['FBasketFixFX']
        if ai_specnbr == None: raise 'F_BASKET_EXCEPT', 'create_addinfo_field() ERROR: No Additional Info Specification exist.'
        stock_links = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
        for stock_link in stock_links:
            ic = stock_link.clone()
            nai = ael.AdditionalInfo.new(ic)
            nai.recaddr = stock_link.seqnbr
            nai.addinf_specnbr = ai_specnbr.specnbr 
            nai.value = '0.0'
            try: nai.commit()
            except Exception, msg:
                if str(msg) == 'Commit failed (Duplicate)': pass
                else: raise 'F_BASKET_EXCEPT', msg
    except Exception, msg: raise 'F_BASKET_EXCEPT', msg
    return i.insid

"""-----------------------------------------------------------------------------
FUNCTION        
    convert_addinfo_field()

DESCRIPTION
    This function is used to convert previously defined Additional info fields 
    specifying fix FX rates. Instead of using Additional info fields for combination 
    links, the new column fix_fx_rate is used.

ARGUMENTS
    i           Instrument      Quanto Basket option

RETURNS
   insid        string          The name of the option.                           
-----------------------------------------------------------------------------"""
def convert_addinfo_field(i,*rest):
    for s in ael.ServerData:
        data_model = s.data_model_nbr
    if data_model < 33000:
        print "\n## !! WARNING: Data Model OLDER than 33000. Use the script .MaintCreateQuantoBasket_ADM32.sql instead. !! ##"
        return i.insid  
    else:
        stock_links = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
        for stock_link in stock_links:
            if stock_link.fix_fx_rate == 0.0:
                old_value_vec = ael.dbsql('select value from additional_info where recaddr = ' + str(stock_link.seqnbr))
                try: old_value = float(old_value_vec[0][0][0])
                except:old_value = 0.0   
                if old_value_vec != [[]]:
                    if old_value != 0.0:
                        cs = stock_link.clone()
                        cs.fix_fx_rate = old_value
                        cs.commit()
                elif stock_link.member_insaddr.curr == i.strike_curr:
                    cs = stock_link.clone()
                    cs.fix_fx_rate = 1.0
                    cs.commit()
    return i.insid

        









