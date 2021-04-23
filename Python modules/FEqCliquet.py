""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""--------------------------------------------------------------------------
DESCRIPTION
    Computes the value of a Cliquet option. 
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

NOTE
    To print the valuation parameters of cliquet end options in the AEL console, 
    set LOG_PARAMETERS = 1. The information will be printed next time the 
    instrument is opened.
    
    This flag can be helpful when setting up the instrument. Thereafter, 
    LOG_PARAMETERS should once again be set to 0 to make sure that performance
    is not worsened.

-----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import sys
import math
import FOptionParams
import FEqCliquetUtils
import FTimeSeries

counter = 0

F_CLIQUET_EXCEPT  = 'f_eq_cliquet_fwdstart_xcp'   
F_CLIQUET_WARNING = 'f_eq_cliquet_warning'
F_FWD_PERF        = 'Fwd Start Perf'
F_FWD_START       = 'FFwdStart'
F_FWD_START_DAY   = 'FFwdStartDay'
F_FWD_START_ALPHA = 'FFwdStartAlpha'
# The timeseries where the reset days are stored.
F_CLIQUET_TIMESERIES    = 'FCliquetResetDays' 
# The run_nbr of cliquet time series. 
F_CLIQUET_TIMESERIESRUN = 0                     

"""----------------------------------------------------------------------------
CLASS           
    FCliquetParams 

DESCRIPTION     
    The class extracts all parameters needed to value a cliquet or
    a forward start performance option.

CONSTRUCTION    
    i           Instrument      An instrument that is an cliquet
                                or a forward start option
    
MEMBERS
    reset_times         List[Float]         The latest and all remaining 
                                            reset days plus the expiry date
                                            (measured in years between
                                            the valuation date and the 
                                            reset date).
    reset_prices        List[Float]         The prices of the underlying
                                            asset at the reset times before
                                            the valuation date.
    first_reset_occured Int                 Boolean variable indicating if 
                                            there has been any reset dates.
    last_reset_price    Float               The price of the underlying asset
                                            at the latest reset day. The 
                                            variable is equal to -1 if 
                                            first_reset_occured = 0.    
    alpha               Float               Alpha factor (ratio indicating how 
                                            much in or out of the money the 
                                            forward strike should be)
    vol                 List[Float]         Volatilities, one for each forward
                                            start option in the cliquet 
                                            option.
    rate                List[Float]         Contains the forward rate from the
                                            valuation date to the reset days 
                                            and to the expiration day.
    carry_cost          List[Float]         Cost of carry rates. 
    df                  List[Float]         The discountfactor between the
                                            expiry date and the payout date.
    dividends           List[(Float,Float)] List of dividends, pairs 
                                        
----------------------------------------------------------------------------"""
class FCliquetParams(FOptionParams.FOptionParams):
    def __init__(self, i):
        FOptionParams.FOptionParams.__init__(self, i)
        if (i.exercise_type == 'American') or (i.exercise_type == 'Bermudan') or not(i.exotic_type == 'None'): 
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, 'Valuation only handles plain European options.'
        if i.digital: 
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, 'Valuation does not handle digital options.'
        if not(i.und_instype == 'Stock' or i.und_instype == 'EquityIndex' or i.und_instype == 'Curr'):
            print "\n## !! EXCEPTION !! ##"
            raise F_CLIQUET_EXCEPT, 'Valuation only handles Stock, EquityIndex and Currency as underlying instrument' 
        try: self.cliquet_type = i.add_info("FCliquetType")
        except: self.cliquet_type = ""
        
        self.mapped_module_tmp = i.used_context_parameter('Valuation Function')
        
        if self.mapped_module_tmp == "FEqCliquet.pv" and self.cliquet_type == "":
            print "\n## !! NO VALUE !! ##"
            raise F_CLIQUET_EXCEPT, "Is it a 'Pay in the End' or a 'Pay as you Go' cliquet option? Please update the 'FCliquetType' Add Info field."

        # Extract the Cliquet Ratio (or the 'alpha')
        alpha_str = i.add_info(F_FWD_START_ALPHA)
        self.alpha = FEqCliquetUtils.convert_alpha(alpha_str)

        # Extract the reset_times, first_reset_occured and the reset_prices:
        reset_dates_tot = []
        
        perf = i.add_info(F_FWD_START) 
        if self.mapped_module_tmp == "FEqCliquet.pv":
            try:
                reset_dates_tot = FTimeSeries.get_TimeSeries(i, F_CLIQUET_TIMESERIES, F_CLIQUET_TIMESERIESRUN)
                reset_dates_tot.sort() 
                if len(reset_dates_tot) == 0:
                    print "\n## !! NO VALUE !! ##"
                    raise F_CLIQUET_EXCEPT, 'No timeseries with reset dates is created for the instrument.'    
            except Exception, msg: 
                print "\n## !! EXCEPTION !! ##"
                raise F_CLIQUET_EXCEPT, msg
            if perf == "":
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "Should the cliquet option be a series of forward start or forward start performance options. Please update the Additional Info field 'FFwdStart'."
            elif perf == "Fwd Start Perf": self.performance = 1
            else: self.performance = 0
        else:
            start_day_str = i.add_info(F_FWD_START_DAY)
            self.start_day = FEqCliquetUtils.convert_start_day(start_day_str)
            # Compensate for the fact that the alpha factor already is included 
            # in the strike price.
            if self.start_day <= self.valuation_date:
                self.fwd_strike = i.strike_price/self.alpha
            else: self.fwd_strike = "Spot price * alpha"
            reset_dates_tot = [(self.start_day, i.strike_price/self.alpha)]
            if perf == "":
                self.performance = 0
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "Should the option be a forward start or forward start performance option. Please update the AdditionalInfo field 'FFwdStart'."
            elif perf == F_FWD_PERF: self.performance = 1
            else: self.performance = 0
        
        [self.first_reset_occured, self.reset_dates, self.reset_prices,\
        self.last_reset_price, self.reset_times] = \
                FEqCliquetUtils.get_reset_dates(reset_dates_tot, self.price,\
                self.mapped_module_tmp, self.valuation_date, self.exp_day)

        # Extract the rates ...
        self.rate = []
        yc = i.used_yield_curve(i.curr) 
        for date in self.reset_dates[1:]:
            self.rate.append( yc.yc_rate(self.valuation_date, date, 'Continuous', 'Act/365', 'Spot Rate') )

        # ... and the carry costs and df:
        self.carry_cost = []
        self.df = []
        # The carry cost will not be the same if the underlying is a stock/equity index
        # or if the underlying is a currency.
        if i.und_instype == 'Stock' or i.und_instype == 'EquityIndex':
            yc_repo = i.und_insaddr.used_repo_curve(i.strike_curr)
            valuation_date_offset = self.valuation_date.add_banking_day(i.und_insaddr.curr, i.und_insaddr.spot_banking_days_offset)
            for date in self.reset_dates[1:]:
                exp_offset = date.add_banking_day(i.curr, i.pay_day_offset)
                self.repo = yc_repo.yc_rate(valuation_date_offset, exp_offset, 'Continuous', 'Act/365', 'Spot Rate')
                texp_carry = valuation_date_offset.years_between(exp_offset, 'Act/365')
                temp = self.valuation_date.years_between(date, 'ACT/365')
                if temp != 0.0:
                    self.carry_cost.append(self.repo * texp_carry / temp)
                else:
                    self.carry_cost.append(0.0)
                # Calculate the discount factor
                rf_exp = yc.yc_rate(date, exp_offset, 'Annual Comp', 'Act/365', 'Spot Rate')
                toffset = date.years_between(exp_offset, 'Act/365')
                self.df.append(math.pow(1+rf_exp, -toffset))
        # The underlying is a currency.
        else:
            j = 0;
            yc_und_rate = i.und_insaddr.used_repo_curve(i.und_insaddr.curr)
            valuation_date_offset = self.valuation_date.add_banking_day(i.und_insaddr.curr, i.und_insaddr.spot_banking_days_offset)
            for date in self.reset_dates[1:]:
                exp_offset = date.add_banking_day(i.und_insaddr.curr, i.pay_day_offset)
                und_rate = yc_und_rate.yc_rate(valuation_date_offset, exp_offset, 'Continuous', 'Act/365', 'Spot Rate')
                texp_carry = valuation_date_offset.years_between(exp_offset, 'Act/365')
                temp = self.valuation_date.years_between(date, 'ACT/365')
                if temp != 0.0:
                    self.carry_cost.append((self.rate[j]-und_rate) * texp_carry / temp)
                else:
                    self.carry_cost.append(0.0)

                j = j+1
                # Calculate the discount factor
                exp_offset = date.add_banking_day(i.curr, i.pay_day_offset)
                rf_exp = yc.yc_rate(date, exp_offset, 'Annual Comp', 'Act/365', 'Spot Rate')
                toffset = date.years_between(exp_offset, 'Act/365')
                self.df.append(math.pow(1+rf_exp, -toffset))
    
        
        # Extract the volatilities:
        self.vol = []
        # If the reset day already has occured then the strike price is given by 
        # alpha times the value of the underlying asset at the reset date. 
        
        sigma_array = []
        strike = self.alpha * self.price    
        for date in self.reset_dates:
            sigma_array.append(i.used_volatility(self.strike_curr).volatility(strike, date, self.valuation_date, self.put_call))
            
        if self.first_reset_occured:
            strike = self.alpha * self.last_reset_price
            sigma = i.used_volatility(i.curr).volatility(strike, self.reset_dates[1], self.valuation_date, self.put_call)
            first_vol = sigma

        # If the reset day is in the future then we have to estimate the strike price 
        # and a forward volatility. We let the strikeprice be given by alpha times the 
        # price of the underlying asset, in this way we will get the right 'in (or out) 
        # the money ratio'.
        else:
            sigma_fwd = sigma_array[0]
            sigma_exp = sigma_array[1]
            first_vol = FEqCliquetUtils.forward_vol(sigma_fwd, sigma_exp, self.valuation_date, self.reset_dates[0], self.reset_dates[1])
        
        self.vol = FEqCliquetUtils.get_cliquet_vola(first_vol, sigma_array, self.reset_dates)

    def pv(self):
        val_meth_params = FEqCliquetUtils.fwdstart_val_meth(self.dividends)
        res = FEqCliquetUtils.cliquet_pv(self, val_meth_params)
        return res*self.strike_theor_curr_fx

"""----------------------------------------------------------------------------
FUNCTION    
    pv() 

DESCRIPTION
    The function pv() calculates the price of a cliquet pay
    at the end option. 

ARGUMENTS
    i       Instrument  Cliquet Option
    calc    Integer     0=>No calculation 1=>Perform calculation
    ref                 Optimisation parameter

RETURNS
   [res     float       Value of instrument
    exp_day date        Maturity date
    curr    string      Currency in which it was valued
    Fixed   string      Constant = 'Fixed']                      
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    try:
        extra_days = 0
        if calc:
            cep = FCliquetParams(i)
            try:print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if cep.texp > 0: print get_info(cep)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if i.exp_day < ael.date_valueday():  res = 0.0
            else:
                reset_dates_tot = FTimeSeries.get_TimeSeries(i, 'FCliquetResetDays', F_CLIQUET_TIMESERIESRUN)
                if len(reset_dates_tot) == 0:
                    print "\n## !! NO VALUE !! ##"
                    raise F_CLIQUET_EXCEPT, "No reset dates are given. Create them with the ASQL application .MaintCreateCliquetResets."
                res = cep.pv() 
                extra_days = cep.extra_days
        else: res = 0.0
    except F_CLIQUET_EXCEPT, msg: 
        print
        print 'Module:  FEqCliquet'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        res = 0.0
    return [[ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ]] 



"""----------------------------------------------------------------------------
get-info()                   
    The function returns a string with valuation parameters.
----------------------------------------------------------------------------"""
def get_info(CliquetParams):
    cp = CliquetParams
    s = ''
    s = s + "Instrument: \t" + cp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    for curve in cp.yield_curves:
        if curve[0] == 'Repo': insid = cp.insid
        elif curve[0] == 'Discount': insid = cp.underlying
        else: insid = cp.underlying
        s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + cp.currency + ")\n" 
    s = s + "\t\n"
    s = s + "Volatility:\t" + str(cp.vol_surface) + "\t(" + cp.insid + ")\n"
    s = s + "\t\n"  
    nr_of_resets = len(cp.reset_times)-1
    s = s + "Cliquet Type:\t\t" + cp.cliquet_type + "\n"
    s = s + "Number of resets:\t" + str(nr_of_resets) + "\n"
    s = s + "Last reset price:\t" + str(cp.last_reset_price) + "\n"
    s = s + "\t\n" 
    for i in range(nr_of_resets):
        s = s + "---------------------------"
        s = s + "\t\n" 
        s = s + "Reset number:\t\t" + str(i+1) + "\n" 
        s = s + "Used repo rate:\t\t%*.*f" % (6, 4, cp.repo*100) + "\n"
        s = s + "Used volatility:\t%*.*f" % (6, 4, cp.vol[i]*100)  + "\n"
        s = s + "Used discount rate:\t%*.*f" % (6, 4, cp.rate[i]*100) + "\n"
        s = s + "Used carry cost:\t%*.*f" % (6, 4, cp.carry_cost[i]*100) + "\n"
        s = s + "Used disc. factor:\t%*.*f" % (6, 4, cp.df[i]) + "\n"
        s = s + "This reset:\t\t" + str(cp.reset_dates[i]) + "\n"
        s = s + "Next reset:\t\t" + str(cp.reset_dates[i+1]) + "\n"
    s = s + "---------------------------"
    s = s + "\t\n" 
    s = s + "Alpha:\t\t\t" + str(cp.alpha) + "\n"
    s = s + "\t\n" 
    if cp.performance:
        s = s + "Cliquet considered to be series of forward start performance options. \n"
    else:
        s = s + "Cliquet considered to be series of forward start options. \n"
    s = s + "\t\n" 
    s = s + "Underlying:\t\t" + cp.underlying + "\n"
    s = s + "Underlying price:\t" + str(cp.price) + "\n"

    if cp.dividends != []:
        s = s + "\t\n"
        s = s + "Underlying Dividends (in " + cp.currency + ") :\n"
        s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
        for d in cp.div_entity:
            s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
            s = s + "\t\n"
    [val_meth, steps] = FEqCliquetUtils.fwdstart_val_meth(cp.dividends)
    s = s + "Valuation method:\t\t" + str(val_meth) + "\n"
    if str(val_meth) != "analytical":
        s = s + "Steps:\t\t\t\t" + str(steps) + "\n"
    s = s + "\t\n" 
    s = s + "Used valuation function: \tFEqCliquet.pv \n"
    s = s + "Mapped in context:\t\t" + cp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s   

















