""" SEQ_VERSION_NR = 2.3.1 """


"""-----------------------------------------------------------------------------
MODULE
    FCliquetParams - Parameters for Cliquet options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for a cliquet option.
       
-----------------------------------------------------------------------------"""
import ael
import sys
import math
import FOptionParams
import FTimeSeries
import FEqCliquetUtils

# This exception is thrown by all cliquet and fwd start pricing routines.
F_CLIQUET_EXCEPT        = 'f_eq_cliquet_xcp'
F_CLIQUET_WARNING       = 'f_eq_cliquet/fwdstart_warning'
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

        self.mapped_module_tmp = i.used_context_parameter('Valuation Function')

        # Extract the Cliquet Ratio (or the 'alpha')
        alpha_str = i.add_info('FFwdStartAlpha')
        self.alpha = FEqCliquetUtils.convert_alpha(alpha_str)

        # Extract the reset_times, first_reset_occured and the reset_prices:
        reset_dates_tot = []
        
        try: perf = i.add_info('FFwdStart') 
        except: perf = ""
        
        if self.mapped_module_tmp == "FEqCliquetGo.pv" \
        or self.mapped_module_tmp == "FEqCliquetEnd.pv" :
            try:
                reset_dates_tot = FTimeSeries.get_TimeSeries(i, 'FCliquetResetDays', F_CLIQUET_TIMESERIESRUN)
                reset_dates_tot.sort() 
                if len(reset_dates_tot) == 0:
                    print "\n## !! NO VALUE !! ##"
                    raise F_CLIQUET_EXCEPT, 'No timeserie with reset dates is created for the instrument.'    
            except Exception, msg: 
                print "\n## !! EXCEPTION !! ##"
                raise F_CLIQUET_EXCEPT, msg
            try:
                # Backward compatibility
                perf_old = i.add_info('FCliquetPerformance')
            except: perf_old = ""
            if perf == "" and perf_old == "":
                self.performance = 1
                print "\n## !! NO VALUE !! ##"
                raise F_CLIQUET_EXCEPT, "Should the cliquet option be a series of forward start or forward start performance options. Please update the Additional Info field 'FFwdStart'."
            elif perf == "Fwd Start Perf" or perf_old == "Yes": self.performance = 1
            else: self.performance = 0
        else:
            start_day_str = i.add_info('FFwdStartDay')
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
            elif perf == "Fwd Start Perf": self.performance = 1
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
        if self.first_reset_occured:
            strike = self.alpha * self.last_reset_price
            sigma = i.used_volatility(i.curr).volatility(strike, self.reset_dates[1], self.valuation_date, self.put_call)
            self.vol.append(sigma)

        # If the reset day is in the future then we have to estimate the strike price 
        # and a forward volatility. We let the strikeprice be given by alpha times the 
        # price of the underlying asset, in this way we will get the right 'in (or out) 
        # the money ratio'.
        else:
            strike = self.alpha * self.price    
            sigma_fwd = i.used_volatility(self.strike_curr).volatility(self.strike, self.reset_dates[0], self.valuation_date, self.put_call)
            sigma_exp = i.used_volatility(self.strike_curr).volatility(self.strike, self.reset_dates[1], self.valuation_date, self.put_call)
            fvol = FEqCliquetUtils.forward_vol(sigma_fwd, sigma_exp, self.valuation_date, self.reset_dates[0], self.reset_dates[1])
            self.vol.append(fvol)
        
        strike = self.alpha * self.price  
        j = 2
        for date in self.reset_dates[2:]:
            sigma_fwd = i.used_volatility(self.strike_curr).volatility(self.strike, self.reset_dates[j-1], self.valuation_date, self.put_call)
            sigma_exp = i.used_volatility(self.strike_curr).volatility(self.strike, date, self.valuation_date, self.put_call)
            fvol = FEqCliquetUtils.forward_vol(sigma_fwd, sigma_exp, self.valuation_date, self.reset_dates[j-1], date)
            self.vol.append(fvol)
            j = j + 1
    
    def get_info(self):
        s = ''
        s = s + "Instrument: \t" + self.insid + "\t is using parameter(s): \n"  
        s = s + "\t\n"
        for curve in self.yield_curves:
            if curve[0] == 'Repo': insid = self.insid
            elif curve[0] == 'Discount': insid = self.underlying
            else: insid = self.underlying
            s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + self.currency + ")\n" 
        s = s + "\t\n"
        s = s + "Volatility:\t" + str(self.vol_surface) + "\t(" + self.insid + ")\n"
        s = s + "\t\n"  
        nr_of_resets = len(self.reset_times)-1
        s = s + "Number of resets:\t" + str(nr_of_resets) + "\n"
        s = s + "\t\n" 
        for i in range(nr_of_resets):
            s = s + "---------------------------"
            s = s + "\t\n" 
            s = s + "Reset number:\t\t" + str(i+1) + "\n" 
            s = s + "Used repo rate:\t\t%*.*f" % (6, 4, self.repo*100) + "\n"
            s = s + "Used volatility:\t%*.*f" % (6, 4, self.vol[i]*100)  + "\n"
            s = s + "Used discount rate:\t%*.*f" % (6, 4, self.rate[i]*100) + "\n"
            s = s + "Used carry cost:\t%*.*f" % (6, 4, self.carry_cost[i]*100) + "\n"
            s = s + "Next reset:\t\t" + str(self.reset_dates[i+1]) + "\n"
            s = s + "Last reset price:\t" + str(self.last_reset_price) + "\n"
        s = s + "---------------------------"
        s = s + "\t\n" 
        s = s + "Alpha:\t\t\t" + str(self.alpha) + "\n"
        s = s + "\t\n" 
        if self.performance:
            s = s + "Cliquet considered to be series of forward start performance options. \n"
        else:
            s = s + "Cliquet considered to be series of forward start options. \n"
        s = s + "\t\n" 
        s = s + "Underlying:\t\t" + self.underlying + "\n"
        s = s + "Underlying price:\t" + str(self.price) + "\n"

        if self.dividends != []:
            s = s + "\t\n"
            s = s + "Underlying Dividends (in " + self.currency + ") :\n"
            s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
            for d in self.div_entity:
                s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
        s = s + "\t\n"
        return s   
            
                
"""----------------------------------------------------------------------------
FUNCTION        
    UpdateCliquetPrice() - Part of a Mark to Mark procedure

DESCRIPTION
    Pricing update routine. In the Time Serie 'FCliquetResetDays' future values are 
    set to -1. The routine updates the -1 to used_price for the underlying instrument.
    This routine should be run every evening. 
        
ARGUMENTS
    Takes no argument 
RETURNS
    Does not return anything                            
----------------------------------------------------------------------------"""
def UpdateCliquetPrice(*rest):
    # UPDATE CLIQUET OPTIONS
    tsSpec = ael.TimeSeriesSpec[F_CLIQUET_TIMESERIES]
    if tsSpec == None: 
        print "\n## !! EXCEPTION !! ##"
        raise F_CLIQUET_EXCEPT, 'UpdateCliquetPrice(): Invalid time series'
    
    tmp=ael.dbsql("select day,seqnbr,recaddr from time_series where ts_specnbr=" + str(tsSpec.specnbr) + "and value=" + '-1' + "and run_no=" + str(F_CLIQUET_TIMESERIESRUN))[0]
    
    # ts is a vector [(date,seqnbr,recaddr)]. All entries have the value -1.
    ts = map(lambda x:[ael.date(x[0][0:10]), x[1], x[2]], tmp)
    cl_old_nbr     = 0
    cl_saved_nbr   = 0 
    for x in ts:
        # x[2] = recaddr
        i = ael.Instrument[x[2]]
        if i != None :
            c = i.category_chlnbr
            # If the category is set to "CliquetEnd" or "CliquetGo"...
            if c != None and (c.entry == 'CliquetEnd' or c.entry == "CliquetGo" ): 
                # x[0] = Date of Time Series entry.
                if x[0] < ael.date_valueday():
                    print "The reset date", x[0], "for the instrument", i.insid
                    print "has not been priced."
                    print "Change manually in the Time Serie 'FCliquetResetDays'."
                    print "----------------------------------"
                    cl_old_nbr = cl_old_nbr + 1
                if x[0] == ael.date_valueday():
                    # x[1] = sequence number of the Time Series. 
                    tsOld = ael.TimeSeries[x[1]]
                    tsUpdate = tsOld.clone()
                    tsUpdate.value = i.used_und_price()
                    tsUpdate.commit()
                    print "The reset date", x[0], "for the option", i.insid, "has been updated."
                    print "---------------------------------------"
                    cl_saved_nbr = cl_saved_nbr + 1

    print "=============================="
    print "CLIQUET OPTIONS"
    print "Non set Cliquet prices:       ", cl_old_nbr
    print "Updated Cliquet prices:       ", cl_saved_nbr 
    print "=============================="

    # UPDATE FORWARD START STRIKE PRICES and CONTRACT SIZE
    ins = ael.Instrument.select()
    fwd_old_nbr     = 0
    fwd_saved_nbr   = 0 
    for i in ins:
        fwd_start_type = i.add_info('FFwdStart')
        if fwd_start_type != "":
            mapped_module = i.used_context_parameter('Valuation Function')
            if mapped_module != "FEqCliquetGo.pv" \
            and mapped_module != "FEqCliquetEnd.pv" :
                try: fwd_date = ael.date_from_string(i.add_info('FFwdStartDay'))
                except: fwd_date = -1
                if fwd_date != -1:
                    if fwd_date < ael.date_today() and i.strike_price <= 0.0:
                        print "\n## !! EXCEPTION !! ##"
                        print "Instrument: ", i.insid
                        print "Date: ", fwd_date
                        print "ERROR: Strike in the past has not been set. Update manually"
                        fwd_old_nbr = fwd_old_nbr + 1 
                    if fwd_date == ael.date_today():
                        i_clone = i.clone()
                        alpha = float(i.add_info('FFwdStartAlpha'))
                        i_clone.strike_price = alpha * i.und_insaddr.mtm_price(ael.date_today(), i.strike_curr.insid)
                        if fwd_start_type == 'Fwd Start Perf':
                            i_clone.contr_size = i.contr_size / (1.0*i.und_insaddr.mtm_price(ael.date_today(), i.strike_curr.insid))
                        i_clone.commit()
                        ael.poll()
                        print "\nInstrument:\t", i.insid
                        print "Underlying:\t", i.und_insaddr.insid
                        print "Alpha:\t\t", alpha
                        print "Spot price:\t", i.und_insaddr.mtm_price(ael.date_today(), i.strike_curr.insid)
                        print "Strike price:\t", i.strike_price
                        print "---------------------------------------"
                        fwd_saved_nbr = fwd_saved_nbr + 1

    

    print "=============================="
    print "FORWARD START OPTIONS"
    print "Non set Fwd Strikes:          ", fwd_old_nbr
    print "Updated Fwd Strikes:          ", fwd_saved_nbr 
    print "=============================="
                    



#UpdateCliquetPrice()  














