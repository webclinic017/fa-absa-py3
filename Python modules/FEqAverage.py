
""" SEQ_VERSION_NR = PRIME 2.8.1, ABSA customized!!!"""

#Note! Upgrading the SEQ package requires the following
#    Include the ABSA specific code on line 78-87 and 553-590

"""----------------------------------------------------------------------------
MODULE
    FEqAverage - Parameters and valuation of average options
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts standard and additional parameters for an instrument of average
    option type. Performs valuation of average options using routines in 
    FEqAverageNumeric and FEqAverageAnalytic.


DATA-PREP       
    For an option to be valued with these routines its Category field has
    to be set to Average. The Additional Info field, FAverageType, must be set. 
    A corresponding Time Serie, 'FAveragePrices', must be created with 
    the default value -1. A Context mapping the instrument or its Valgroup
    to FEqAverage.pv has to be used.
----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import FOptionParams
import FTimeSeries
import FEqAverageAnalytic
import FEqBasket
import FEqCliquet
import FEqAverageUtils

F_AVERAGE_EXCEPT        = 'f_eq_average_xcp'  ## This exception is thrown by all average routines
F_BASKET_EXCEPT         = 'f_eq_basket_xcp'  
F_AVERAGE_TIMESERIES    = 'FAveragePrices'    ## The timeseries where averages are stored
F_AVERAGE_TIMESERIESRUN = 0                   ## The run_nbr of the average timeseries
F_AVERAGE_FUTAVGVAL     = -1                  ## Value stored in timeseries for unknown average points
F_STRIKE_TIMESERIES     = 'FAverageStrike'    ## The timeseries where prices are stored to calculate a strike
F_CLIQUET_EXCEPT        = 'f_eq_cliquet_fwdstart_xcp'

AvgTypeDict = { 'ArithmeticFix': 0, 'ArithmeticFloating': 1,
                'GeometricFix' : 2, 'GeometricFloating' : 3,
                'HarmonicFix'  : 4, 'HarmonicFloating'  : 5 }
counter = 0

"""----------------------------------------------------------------------------
CLASS                   
    FAverageParams - Parameters for average options

INHERITS
    FOptionParams
                
DESCRIPTION             
    The class extracts all parameters needed to value an average option.

CONSTRUCTION    
    i               Instrument  An instrument that is an average option

MEMBERS                 
    avgFromDB       [(date,float)]  Unsorted list of pairs. The first value in the pair
                                    is the average date and the second is the price of 
                                    the underlying.
    avg_type_text   string          The average and strike type (additional info field).        
    old_avgs        [dates]         List of all average points before today.
    avg_dates       [dates]         The dates at which averages are to be taken.
    avg_so_far      [dates]         Average of underlying at old_avgs dates.
    cont_div        float           Continuous dividend.
    fix_float       int             If the strike is fix: fix_float=0. Else: fix_float=1.
    avg_type        int             Arithmetic average=0, geometric=1 and harmonic=2.
----------------------------------------------------------------------------"""
class FAverageParams(FOptionParams.FOptionParams):
    def __init__(self, i):
        FOptionParams.FOptionParams.__init__(self, i)

    

    	# ABSA specific code adjusting for dividend yield handling and volatility skew handling.
    	
   	import math
	
	if i.und_instype in ('EquityIndex', 'Stock'):
	    self.carry_cost = i.used_discount_rate()/100 - divYield(i) 
	    FairForward = (i.used_und_price(i.undprice_type()) - i.und_price_shift()) * math.exp((self.carry_cost)*self.texp)
	    self.vol = i.used_volatility(i.curr).volatility((i.strike_price/FairForward-1)*100, i.exp_day) 

    	# End - ABSA specific code
        
        self.strike_curr = i.strike_curr
        self.avg_fwd_start = i.add_info('FFwdStart')
        try:self.avg_in = i.add_info('FAverageIn')
        except: self.avg_in = ""
        
        # First value in each pair is date of average,
        # Second value is the price of the underlying or 
        # F_AVERAGE_FUTAVGVAL if the date is in the future 
        [avgFromDB_dict, und_instrs, average_price_list] = FTimeSeries.get_average_TimeSeries(i, F_AVERAGE_TIMESERIES, F_AVERAGE_TIMESERIESRUN)
        self.avgStrike = FTimeSeries.get_TimeSeries(i, F_STRIKE_TIMESERIES, F_AVERAGE_TIMESERIESRUN)
        
        if len(avgFromDB_dict) > 1:
            # The instrument should be priced as a basket option.
            self.average_basket = 1
            self.bp = FEqBasket.BasketParams(i)
        else: self.average_basket = 0
        
        if self.average_basket: self.underlyings = self.bp.basket_stocks
        else: self.underlyings = [i.und_insaddr.insid]
        
        # Remove old timeseries for components no longer in the basket
        self.avgFromDB_dict = {}
        for underlying in self.underlyings:
            if avgFromDB_dict.has_key(underlying):
                self.avgFromDB_dict[underlying] = avgFromDB_dict[underlying]
        if len(self.avgFromDB_dict) != len(avgFromDB_dict):
            [und_instrs, average_price_list] = [self.avgFromDB_dict.keys(), self.avgFromDB_dict.values()]
        
        # ERROR CHECK
        if self.avgFromDB_dict == {}:
            print "\n## !! NO VALUE !! ##"
            raise F_AVERAGE_EXCEPT, "No Time Series exists for the instrument. Create one with the ASQL-application .MaintCreateAverageDates."
        else:
            for underlying in self.underlyings:
                if not self.avgFromDB_dict.has_key(underlying):
                    print "\n## !! NO VALUE !! ##"
                    raise F_AVERAGE_EXCEPT, "No TimeSerie is created for the stock " + underlying + ". Create one with the ASQL-application .MaintCreateAverageDates."    
        
        # QUANTO ASIAN HANDLING
        self.quanto_flag = FEqAverageUtils.get_asian_quanto_flag(self.fix_fx, self.strike_curr, i.curr)
        if self.quanto_flag:
            [self.corr_stock_fx, self.corr_name] = FEqAverageUtils.get_corr_stock_fx(i)
        
        # FORWARD START ASIAN HANDLING
        if self.avg_fwd_start != "":
            if self.average_basket:
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "FwdStart valuation does not handle baskets as underlyings. Add the equity index to the page NonSplitIndexes and create a new timeseries for the instrument."
            try:
                fp = FEqCliquet.FCliquetParams(i)
                self.start_day = fp.start_day
                self.fwd_start_time = fp.reset_times[0]
                self.vol = fp.vol[0]
                self.fwd_strike = fp.fwd_strike
                self.alpha = fp.alpha
            except F_CLIQUET_EXCEPT, msg: 
                raise F_AVERAGE_EXCEPT, msg
        else:   
            self.fwd_start_time = 0
            self.alpha = 1
        fwdstart_params = [self.fwd_start_time, self.alpha, self.strike]
        
        [self.old_avgs_dict, self.avg_dates_dict, self.avg_start_dict, self.avg_end_dict, self.avg_dates] = \
            FEqAverageUtils.get_avg_price_dict(i, und_instrs, average_price_list, self.avgStrike, self.average_basket,\
            self.avg_fwd_start, fwdstart_params, ael.date_valueday())

        self.avg_type_text = i.add_info('FAverageType')
        try: FAvgType = AvgTypeDict[self.avg_type_text]
        except: 
            print "\n## !! EXCEPTION !! ##"
            raise F_AVERAGE_EXCEPT, 'Parameter error. No known FAverageType ' 
        
        # Even FAvgType -> Fix -> fix_float=0 , Odd->Float->fix_float=1 
        self.fix_float = FEqAverageUtils.get_fix_float(FAvgType)
        
        self.cont_div = self.rate - self.carry_cost
        
        if not self.average_basket: 
            basket_weights = []
            avg_dates_values = self.avg_dates_dict.values()
            old_avgs_values = self.old_avgs_dict.values()
        else: 
            basket_weights = self.bp.weights
            avg_dates_values = []
            old_avgs_values = []
            for insid in self.bp.basket_stocks:
                if self.avg_dates_dict.has_key(insid):
                    avg_dates_values.append(self.avg_dates_dict[insid])   
                    old_avgs_values.append(self.old_avgs_dict[insid]) 
        
        # Determine option type and calculate avg_so_far
        [self.avg_type, self.avg_so_far_dict, self.avg_so_far] = \
            FEqAverageUtils.get_avg_so_far(FAvgType, self.old_avgs_dict.keys(), self.old_avgs_dict.values(), i.und_insaddr)

        # Sorting out the asian dates/weights that are in the future
        [self.fut_avg_dates, self.fut_avg_weights] = \
            FEqAverageUtils.get_future_avgs(avg_dates_values, self.texp, self.avg_type_text, self.average_basket)
        
        self.mod_strike = FEqAverageUtils.get_mod_strike(self.average_basket,\
            self.avg_fwd_start, self.avg_dates_dict.values(), self.strike, old_avgs_values, basket_weights, self.avg_type_text, self.avg_in)
    
    def pv(self):
        [val_meth, nbr_of_sim] = FEqAverageUtils.val_meth(self.average_basket, self.avg_dates_dict.values(),\
                                 self.avg_type_text, self.avg_fwd_start, self.avg_in, self.texp)
        res = FEqAverageUtils.get_pv(self, [val_meth, nbr_of_sim])
        if res >= 0.0 and not self.quanto_flag: res = res * self.strike_theor_curr_fx
        return res

    def __str__(self):
        return str(self.__dict__)

def get_error_string(msg, i):
    s = '\nModule: FEqAverage' + '\n'
    s = s + 'Error : ' + str(msg) + '\n'
    s = s + 'Instr : ' + i.insid + '\n'
    return s
    
"""----------------------------------------------------------------------------
FUNCTION        
    pv() 
    
DESCRIPTION
    Calculates the theoretical price of an average option. Using analytical
    methods if possible, otherwise it uses numerical methods per default
    a binomial tree method.

ARGUMENTS
    i           Instrument      Average Option
    calc        Integer(0?1)    0->No calculation 1->Perform calculation
    ref                         Optimisation parameter

RETURNS
   [res         Float           Value of instrument
    expday      Date            Maturity date
    curr        String          Currency in which it was valued
    fixed       String          Constant = 'Fixed']                                     
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    extra_days = 0
    res = 0.0
    if calc:
        try:
            if i.und_insaddr.instype != "Stock" and i.und_insaddr.instype != "EquityIndex" and \
               i.und_insaddr.instype != "Combination" and i.und_insaddr.instype != "Curr":
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "The underlying instrument type " + str(i.und_insaddr.instype) + " of the instrument " + i.insid + ", is not handled. Only stocks and equity indexes."
            if i.exotic_type != "None":
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "Pricing of barrier average options is not implemented."
            if i.digital: 
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "Pricing of digital average options is not implemented"
            if i.exercise_type != 'European': 
                print "\n## !! EXCEPTION !! ##"
                raise F_AVERAGE_EXCEPT, "Pricing of American average options is not implemented." 
            
            # Checking if the instrument has an average type.
            avg_type = i.add_info('FAverageType')
            if   avg_type == 'ArithmeticFix':     pass
            elif avg_type == 'ArithmeticFloating':pass
            elif avg_type == 'GeometricFix':      pass
            elif avg_type == 'GeometricFloating': pass
            else: 
                print "\n## !! NO VALUE !! ##"
                raise F_AVERAGE_EXCEPT, "No average type is set. Choose type in the Additional Info field FAverageType."
            
            # Checking if the instrument has a TimeSerie.
            series = FTimeSeries.get_average_TimeSeries(i, F_AVERAGE_TIMESERIES, F_AVERAGE_TIMESERIESRUN)   
            if series == {}:
                print "\n## !! NO VALUE !! ##"
                raise F_AVERAGE_EXCEPT, "No TimeSeries is created for the instrument " + i.insid +  "Create one with the ASQL-application .MaintCreateAverageDates."
            try: avg_in = i.add_info('FAverageIn')                
            except: avg_in = ""
            if avg_in != "":
                series2 = FTimeSeries.get_TimeSeries(i, F_STRIKE_TIMESERIES, F_AVERAGE_TIMESERIESRUN)
                if series2 == []:
                    print "\n## !! NO VALUE !! ##"
                    raise F_AVERAGE_EXCEPT, "The instrument is an average in styled Asian option but no Strike time series is created for the instrument " + i.insid +  ". Create one with the ASQL-application .MaintCreateAverageDates."
        
            try:    print_info = i.add_info("FPrintInfo")
            except: print_info = ""
        
            
            avgParams = FAverageParams(i)
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if avgParams.texp >= 0: print get_info(avgParams)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if i.exp_day < ael.date_valueday():  res = 0.0
            else: res = avgParams.pv()
            extra_days = avgParams.extra_days
        except F_AVERAGE_EXCEPT, msg:
            print get_error_string(msg, i)
        except F_BASKET_EXCEPT, msg:
            print get_error_string(msg, i)
        except F_CLIQUET_EXCEPT, msg:
            print get_error_string(msg, i)
    return [ [ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ] ]

"""----------------------------------------------------------------------------
get_info()
    The function returns a string with average option valuation parameters.
----------------------------------------------------------------------------"""
def get_info(ap):
    s = '\t\n'
    s = s + "Instrument: \t" + ap.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    for curve in ap.yield_curves:
        if curve[0] == 'Repo': insid = ap.insid
        elif curve[0] == 'Discount': insid = ap.underlying
        else: insid = ap.underlying
        if not ap.average_basket or curve[0] == 'Repo': 
            s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + ap.currency + ")\n" 
    s = s + "\t\n"
    if not ap.average_basket:
        s= s + "Volatility:\t" + str(ap.vol_surface) + "\t(" + ap.insid + ")\n"
        s = s + "\t\n"  
        s = s + "Used volatility:\t%*.*f" % (6, 4, ap.vol*100)  + "\n"
        s = s + "Used discount rate:\t%*.*f" % (6, 4, ap.rate*100) + "\n"
    s = s + "Used repo rate:\t\t%*.*f" % (6, 4, ap.repo*100) + "\n"
    s = s + "\t\n" 
    avg_type = "No known average type"
    if   ap.avg_type_text=='ArithmeticFix':     avg_type = "Arithmetic fix"
    elif ap.avg_type_text=='ArithmeticFloating':avg_type = "Arithmetic floating"
    elif ap.avg_type_text=='GeometricFix':      avg_type = "Geometric fix"  
    elif ap.avg_type_text=='GeometricFloating': avg_type = "Geometric floating"
    s = s + "Average type:\t\t" + str(avg_type) + "\n"
    s = s + "Average start:\t\t" + str(ap.avg_start_dict.values()[0]) + "\n"
    s = s + "Average end:\t\t" + str(ap.avg_end_dict.values()[0]) + "\n"
    s = s + "\t\n"
    if ap.avg_in != "":
        ap.avgStrike.sort()
        s = s + "Average Strike Start:\t" + str(ap.avgStrike[0][0]) + "\n" 
        s = s + "Average Strike End:\t" + str(ap.avgStrike[len(ap.avgStrike)-1][0]) + "\n" 
        s = s + "\t\n"
    if not ap.average_basket:
        s = s + "Number of fixings made:\t" + str(len(ap.old_avgs_dict[ap.underlying])) + "\n" 
        s = s + "Average so far:\t\t%0.3f" % (ap.avg_so_far_dict.values()[0]) + "\n" 
    s = s + "\t\n"
    i = 0
    if ap.average_basket:
        s = s + "Mapped to correlation:\t" + ap.bp.corr_name + "\n"
        s = s + "\t\n"
        if ap.bp.quanto_flag:
            s = s + "Used correlation between the asset and the FX rates:\t" + "\n"
            for item in ap.bp.corr_stock_fx_dict.items():
                s = s + "\t\t\t" + "'" + str(item[0][0])+ "'"+ " .vs " + "'" + str(item[0][1]) + "'\t" + " = " + str(item[1]) + "\n"
                s = s + "\t\n"
            check = 0
            for item in ap.bp.corr_fx_fx.items():
                if item[0][0] != item[0][1]: 
                    check = 1
                    break
            if check:    
                s = s + "\t\n"
                s = s + "Used correlation between the FX rates:\t" + "\n"
                for item in ap.bp.corr_fx_fx.items():
                    s = s + "\t\t\t" + "'" + str(item[0][0])+ "'"+ " / " + "'" + str(item[0][1]) + "'\t" + " = " + str(item[1]) + "\n"
    for stock in ap.underlyings:
        s = s + "Underlying:\t\t" + stock + "\n"
        if ap.average_basket: price = ap.bp.price[i]
        else: price = ap.price
        
        s = s + "Underlying price:\t" + str(price) + "\n"
        if ap.average_basket:
            s = s + "Index weight:\t\t" + str(ap.bp.weights[i]) + "\n"
            s = s + "Volatility surface:\t" + str(ap.bp.vol_surfaces[i]) + "\n" 
            s = s + "Number of fixings made:\t" + str(len(ap.old_avgs_dict[stock])) + "\n" 
            s = s + "Average so far :\t%0.3f" % (ap.avg_so_far_dict[stock]) + "\n" 
            s = s + "Used volatility:\t%*.*f" % (6, 4, ap.bp.vol[i]*100)  + "\n"
            s = s + "Used yield curve:\t" + str(ap.bp.yield_curves[i]) + "\n"
            s = s + "Used risk free rate:\t%*.*f" % (6, 4, ap.bp.rate_stocks[i]*100) + "\n"
            if ap.bp.quanto_flag:
                if ap.bp.vol_surf_fx[i] != 'None':
                    s = s + "FX Volatility surface:\t" + str(ap.bp.vol_surf_fx[i]) + "\n" 
                    s = s + "FX Volatility:\t\t" + str(ap.bp.fxvol[i]*100) + "\n"       
                    s = s + "Fix FX rate:\t\t" + str(ap.bp.fx[i]) + "\n"
                    s = s + "Correlation:\n"
                    for item in ap.bp.correlation_dict[ap.bp.basket_stocks[i]].items():
                        s = s + "\t\t\t" + str(item[0])+ "\t= " + str(item[1]) + "\n"
            if ap.bp.dividends[i] != []:
                s = s + "Underlying Dividends (in " + ap.bp.currency + ") :\n"
                s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
                for d in ap.bp.div_entities[i]:
                    s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
            s = s + "---------------------------------\n"
            i = i + 1
        else:
            if ap.quanto_flag:
                if ap.vol_surf_fx != 'None':
                    s = s + "FX Volatility surface:\t" + str(ap.vol_surf_fx) + "\n" 
                    s = s + "FX Volatility:\t\t" + str(ap.fx_vol*100) + "\n"       
                    s = s + "Fix FX rate:\t\t" + str(ap.fx_rate) + "\n"
                    s = s + "Mapped Correlation:\t" + str(ap.corr_name) + "\n"
                    s = s + "Correlation:\n"
                    fx = ap.strike_curr.insid +"/" + ap.currency 
                    s = s + "\t\t\t" + str(ap.underlying)+ " vs. " + str(fx) + "\t= " + str(ap.corr_stock_fx) + "\n"  
                    s = s + "Foreign yield curve:\t" + ap.foreign_yc + "\n"    
                    s = s + "Foreign rate:\t\t" + str(ap.foreign_rate*100) + "\n"   
            if ap.dividends != []:
                s = s + "\t\n"
                s = s + "Underlying Dividends:\n"
                s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
                for d in ap.div_entity:
                    s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
        s = s + "\t\n"
    if ap.avg_fwd_start != "":
        s = s + "Average forward start day:\t" + str(ap.start_day) + "\n"
        s = s + "Average forward start alpha:\t" + str(ap.alpha) + "\n"
        s = s + "Average forward start strike:\t" + str(ap.fwd_strike) + "\n"
        if ap.avg_fwd_start == "Fwd Start Perf": perf = "Yes"
        else: perf = "No"
        s = s + "Average forward start perf.:\t" + perf + "\n" 
    s = s + "\t\n"
    
    if avg_type == "Arithmetic floating":
        nbr_avgs = len(ap.fut_avg_dates[0])-1
    else: nbr_avgs = len(ap.fut_avg_dates[0])
    s = s + "Number of future averages:\t" + str(nbr_avgs) + "\n"
    s = s + "\t\n"
    [val_meth, nbr_of_sim] = FEqAverageUtils.val_meth(ap.average_basket, ap.avg_dates_dict.values(), ap.avg_type_text,\
                                    ap.avg_fwd_start, ap.avg_in, ap.texp)
    s = s + "Valuation method:\t\t" + val_meth + "\n"
    if nbr_of_sim != 0:
        s = s + "Number of simulations:\t\t" + str(nbr_of_sim) + "\n"
    s = s + "\t\n" 
    s = s + "Used valuation function: \tFEqAverage.pv \n"
    s = s + "Mapped in context:\t\t" + ap.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s   
        

"""----------------------------------------------------------------------------
FUNCTIONS
    Access routines for sql applications

DESCRIPTION
    The following set of functions is intended to be used by sql applications

ARGUMENTS (identical for all functions)
    i       Instrument      Average option 
    
RETURNS
    FUNCTION    TYPE    DESCRIPTION
    Strike      String  The strike price or 'Floating'
    callput     String  'Call' or 'Put'                 
    AvgType     String  Average and strike type, ex: 'Arithmetic Fix'
    NbrAvgs     Int     The number of future averages    
    NbrDivs     Int     The number of dividends
    AvgStart    Date    The first average date
    AvgEnd      Date    The last average date
    UsedValFun  String  Used valuation method. 
    AvgSoFar    Float   Calculated average prior to valuation date
----------------------------------------------------------------------------"""
def Strike(i, *rest):
    try:
        avgParams = FAverageParams(i)
        if avgParams.fix_float&1:
            return "floating"
        else:
            return str(avgParams.strike)
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return ""
        
def callput(i, *rest):
    try:
        avgParams = FAverageParams(i)
        if avgParams.put_call==0:
            return "Put"
        else: return "Call"
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return ""

def AvgType(i, *rest):
    try:
        ap = FAverageParams(i)
        return ap.avg_type_text
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return ""

def NbrAvgs(i, *rest):            
    try:
        ap = FAverageParams(i)
        return len(ap.fut_avg_dates[0])
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return 0

def NbrDivs(i, *rest):
    try:
        ap = FAverageParams(i) 
        if ap.average_basket: n = len(ap.bp.dividends[0])
        else:
            future_dividends = []; tmp=ap.dividends
            for x in tmp:
                if x[1]>0:
                    future_dividends.append(x)
            n = len(future_dividends)
        return n
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return 0

def AvgStart(i, *rest):
    try:
        ap = FAverageParams(i)
        return ap.avg_start_dict.values()[0]
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return ""
        
def AvgEnd(i, *rest):
    try:
        ap = FAverageParams(i)
        return ap.avg_end_dict.values()[0]
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return ""
    
def UsedValFun(i, *rest):
    try:
        ap = FAverageParams(i)
        [val_meth, nbr_of_sim] = \
            FEqAverageUtils.val_meth(ap.average_basket, ap.avg_dates_dict.values(),\
            ap.avg_type_text, ap.avg_fwd_start)
        return val_meth
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return ""
    
def AvgSoFar(i, *rest):
    try:
        ap = FAverageParams(i)
        if ap.avg_so_far_dict.has_key(i.und_insaddr.insid): 
            return ap.avg_so_far_dict[i.und_insaddr.insid]
        else: return 0
    except F_AVERAGE_EXCEPT, msg:
        print '\nModule:  FEqAverage'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return 0


# ABSA specific code


import math

def nac2ccr(m, r):
    """nac2ccr(m, r)

    Converts notional amount compounded annually/semi-annually etc
    to continuous compounded format.

    m       (int):         Number of compounds per annum (1 for annually)
    r       (float):       Interest rate per annum
    returns (float):       Continuous compounded yield"""

    try:
        m = float(m)
        r = float(r)
    except:
        print 'Arguments must be numeric values'
        sys.exit()

    return m * math.log(1 + r/m)

def divYield(aelOption):
    
    d = 0.0
    div = aelOption.und_insaddr.add_info('DividendYield')
    if div:
        try: 
            d = float(aelOption.und_insaddr.add_info('DividendYield'))
            # Convert d from NACA to CCR format
            d = nac2ccr(1, d) 
        except:
            print 'Wrong DividendYield for:', aelOption.insid
    return d    



