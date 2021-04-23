""" SEQ_VERSION_NR = PRIME 2.8.1 """



"""----------------------------------------------------------------------------
MODULE
    FEqBasket - Valuation of European basket options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

NOTE
    To print the valuation parameters of a basket options in the AEL console, 
    set LOG_PARAMETERS = 1. The information will be printed next time the 
    instrument is opened.
    
    This flag can be helpful when setting up the instrument. Thereafter, 
    LOG_PARAMETERS should once again be set to 0 to make sure that performance
    is not worsened.
 ----------------------------------------------------------------------------""" 
LOG_PARAMETERS = 0
import ael
import math
import FEqBasketUtils
import FOptionParams

counter = 0
F_BASKET_EXCEPT   = 'f_eq_basket_xcp'  
F_BASKET_WARNING  = 'f_eq_basket_warning,'  

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
    price[]               float       The price of the underlying assets.
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
    pv() 

DESCRIPTION
    Calculates the theoretical price of a plain basket option. 

ARGUMENTS
    i           Instrument      Plain vanilla option to be valued
    calc        int             Flag specifying whether a theoretical price
                                should be calculated or not.  0=>No calculation 
                                1=>Perform calculation
    ref                         Optimisation parameter.

RETURNS
   [res         float           Value of instrument
    expday      date            Maturity date
    curr        string          Currency in which the option was valued
    fixed       string          Constant = 'Fixed']                                     
-----------------------------------------------------------------------------"""
def pv(i,calc=1,ref=0):
    try:
        extra_days = 0
        if calc:        
            if i.exotic_type != "None": 
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'Barrier basket options are not handled.'
            if i.digital: 
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'Digital basket options are not handled.'
            bp = BasketParams(i)
            if globals()['counter'] == 5: globals()['counter'] = 0
            try: print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if bp.texp > 0: print get_info(bp)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            
            if (i.strike_price < 0.0):
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, 'The strikeprice is less than or equal to zero.'
            try: res = bp.pv()     
            except Exception, msg: 
                print "\n## !! EXCEPTION !! ##"
                raise F_BASKET_EXCEPT, msg
            extra_days = bp.extra_days
        else: res = 0.0
    except F_BASKET_EXCEPT, msg:
        print
        print 'Module:  FEqBasket'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        res = 0.0
    return [ [ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ] ] 


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
    
"""----------------------------------------------------------------------------
get_info()
    Log the valuation parameters in the AEL console.
----------------------------------------------------------------------------"""
def get_info(BasketParams):
    bp = BasketParams
    s = ''
    s = s + "Instrument: \t" + bp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    s = s + "Underlying:\t\t" + bp.underlying + "\n"
    s = s + "Underlying price:\t%*.*f" % (6, 4, bp.und_price) + "\n"
    s = s + "Used discount rate:\t%*.*f" % (6, 4, bp.rate*100) + "\n"
    s = s + "Mapped to correlation:\t" + bp.corr_name + "\n"
    s = s + "\t\n"
    if bp.quanto_flag:
        s = s + "Used correlation between the asset and the FX rates:\t" + "\n"
        for item in bp.corr_stock_fx_dict.items():
            s = s + "\t\t\t" + "'" + str(item[0][0])+ "'"+ " / " + "'" + str(item[0][1]) + "'\t" + " = " + str(item[1]) + "\n"
        
        check = 0
        for item in bp.corr_fx_fx.items():
            if item[0][0] != item[0][1]: 
                check = 1
                break
        if check:    
            s = s + "\t\n"
            s = s + "Used correlation between the FX rates:\t" + "\n"
            for item in bp.corr_fx_fx.items():
                s = s + "\t\t\t" + "'" + str(item[0][0])+ "'"+ " / " + "'" + str(item[0][1]) + "'\t" + " = " + str(item[1]) + "\n"
    
    #s = s + "FX Volatility:\t" + str(bp.fxvol) + "\n"       
    #s = s + "\t\n"
    s = s + "---------------------------------\n"
    for i in range(bp.dim):
        s = s + "Basket member:\t\t" + str(bp.basket_stocks[i]) + "\n"
        s = s + "Member price:\t\t" + str(bp.price[i]) + "\n"
        s = s + "Member weight:\t\t" + str(bp.weights[i]) + "\n"
        s = s + "Volatility surface:\t" + str(bp.vol_surfaces[i]) + "\n" 
        s = s + "Used volatility:\t%*.*f" % (6, 4, bp.vol[i]*100)  + "\n"
        s = s + "Used yield curve:\t" + str(bp.yield_curves[i]) + "\n"
        s = s + "Used risk free rate:\t" + str(bp.rate_stocks[i]*100) + "\n"
        if bp.quanto_flag:
            if bp.vol_surf_fx[i] != 'None':
                s = s + "FX Volatility surface:\t" + str(bp.vol_surf_fx[i]) + "\n" 
                s = s + "FX Volatility:\t\t" + str(bp.fxvol[i]*100) + "\n"       
            s = s + "Fix FX rate:\t\t" + str(bp.fx[i]) + "\n"
        s = s + "Correlation:\n"
        for item in bp.correlation_dict[bp.basket_stocks[i]].items():
            s = s + "\t\t\t" + str(item[0])+ "\t= " + str(item[1]) + "\n"
            
        if bp.dividends[i] != []:
            s = s + "Underlying Dividends (in " + bp.currency + ") :\n"
            s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
            for d in bp.div_entities[i]:
                s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
        s = s + "---------------------------------\n"
    s = s + "\t\n"
    [val_meth, simul] = FEqBasketUtils.basket_val_meth()
    s = s + "Used valuation method:\t\t" + val_meth + "\n"
    if simul != 0:
        s = s + "Number of simulations:\t\t" + str(simul) + "\n"
    s = s + "Used valuation function: \tFEqBasket.pv \n"
    s = s + "Mapped in context:\t\t" + bp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s  

