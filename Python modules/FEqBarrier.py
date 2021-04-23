""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqBarrier - Parameters for barrier options are extracted and barrier 
                 options are valued.
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Extracts standard and additional parameters for an instrument of barrier 
   type. Calculates the price of a barrier option. European options with 
   discrete dividends are handled.
----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import math
import FTimeSeries   
import FOptionParams
import FEqBarrierUtils

# This exception is thrown by all barrier and double barrier routines.
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp'    
# The timeseries where barrier monitor dates are stored.
F_BARRIER_TIMESERIES    = 'FBarrierMonitorDays' 
# The run_nbr of barrier time series. 
F_BARRIER_TIMESERIESRUN = 0                     

F_BARRIER_CROSSED       = 'FBarrier Crossed'
F_BARRIER_CROSSED_DATE  = 'FBarrier Cross Date'
F_BARRIER_MONITOR_FRQ   = 'FBarrierMonitorFrq'
F_BARRIER_MODEL         = 'FBarrierModel'
F_BARRIER_RISK_MAN      = 'FBarrier RiskMan'
F_BARRIER_PAY_REBATE    = 'FBarrierPayRebate'

# Barrier type
F_BARRIER_ARBITRARY     = 'Arbitrary'           
F_BARRIER_CONTINUOUS    = 'Continuous'
F_BARRIER_DAILY         = 'Daily'
F_BARRIER_MONTHLY       = 'Monthly'
F_BARRIER_WEEKLY        = 'Weekly'
F_BARRIER_YEARLY        = 'Yearly'
F_BARRIER_DAILY_LAST_MONTH = 'DailyLastMonth'
F_BARRIER_WEEKLY_LAST_MONTH = 'WeeklyLastMonth'
F_BARRIER_DAILY_LAST_TWO_WEEKS = 'DailyLastTwoWeeks'

# The analytic greeks are stored in a dictionary.
NOT_CALC = 'not_calculated_greek'
CALC = 'calculated_greek' 

counter = 0

use_model_enum_dict = {"Analytical":0,"Trinomial":1,"Smart":2,"":2, "Monte Carlo":3}

"""----------------------------------------------------------------------------
CLASS           
    FBarrierParams - Parameters for barrier options

INHERITS
    FOptionParams
            
DESCRIPTION     
    The class extracts all parameters needed to value a barrier option.

CONSTRUCTION    
    i                       Instrument  An instrument that is a barrier option

MEMBERS         
    type                    int         Type of barrier option. For single 
                                        Barrier options this means:
                                            type = 1 => 'Down & Out'
                                            type = 2 => 'Down & In'
                                            type = 3 => 'Up & Out'
                                            type = 4 => 'Up & In'
                                        while for double barriers it should be 
                                        interpreted as
                                            type = 1 or type = 3 => Knock-Out 
                                                                    Corridor option
                                            type = 2 or type = 4 => Knock-In 
                                                                    Corridor option
    barrier                 float       Barrier level.          
    rebate                  float       Rebate.
    barr_type               string      Describes the barrier, if it's 
                                        
                                        continuous      => barr_type = F_BARRIER_CONTINUOUS
                                        arbitrary disc. => barr_type = F_BARRIER_ARBITRARY 
                                        daily monitored => barr_type = F_BARRIER_DAILY 
                                        weekly monitored => barr_type = F_BARRIER_WEEKLY 
                                        etc. ..
                                        
    discrete_barr            int        Boolean variable: 
                                            discreteb=1 => the barrier is discrete. 
                                            discreteb=0 => the barrier is continuous.
    barr_monitoring_times   int         Number of monitoring times.
    barr_dates              [floats]    Monitoring times.   
--------------------------------------------------------------------------------""" 
class FBarrierParams(FOptionParams.FOptionParams):
    def __init__(self, i):
        FOptionParams.FOptionParams.__init__(self, i)
        
        mapped_module = i.used_context_parameter('Valuation Function')
        if not mapped_module == 'FEqLadder.pv':
            self.exotic_type = i.exotic_type
            barrier_type_nbr = FEqBarrierUtils.get_exotic_number(self.exotic_type) + 1
        else: barrier_type_nbr = 1
        
        self.barrier_type_nbr = barrier_type_nbr    
        self.barrier = i.barrier    
        self.rebate = i.rebate        
        self.digital = i.digital
        
        # Check if the user has defined two different barriers. The first barrier 
        # decides when the option is knocked. The valuation and greeks are based 
        # on the second barrier.
        barrier_man = i.add_info(F_BARRIER_RISK_MAN)
        if barrier_man != "": 
            self.barrier_man = FEqBarrierUtils.get_float_man_barrier(barrier_man)
            self.has_barrier_man = 1
        else: 
            self.barrier_man = i.barrier
            self.has_barrier_man = 0
        
        self.pay_rebate = i.add_info(F_BARRIER_PAY_REBATE)
        self.knocked = i.add_info(F_BARRIER_CROSSED)
        knocked_date_str = i.add_info(F_BARRIER_CROSSED_DATE)
        if self.knocked != "":
            if knocked_date_str != '':
                self.knocked_date = ael.date_from_string(knocked_date_str)
                # Check historical mode.
                try:
                    if ael.historical_mode() and self.knocked_date > self.valuation_date:
                        self.knocked = ""
                        self.knocked_date = ""
                    elif self.knocked_date > self.valuation_date: 
                        print "\n## !! EXCEPTION !! ##"
                        raise F_BARRIER_EXCEPT, "The barrier cross date is in the future."
                    else: self.time_from_knocked = self.knocked_date.years_between(self.valuation_date, 'Act/365')
                except: 
                    self.time_from_knocked = self.knocked_date.years_between(self.valuation_date, 'Act/365')
            else: 
                self.time_from_knocked = 0
                print "\n## !! NO VALUE !! ##"
                raise F_BARRIER_EXCEPT, "The barrier is crossed but no knock date is given. Please update the Additional Info field 'FBarrier Cross Date'." 
        
        barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        FEqBarrierUtils.is_valid_mon_freq(barr_freq)
        self.barr_freq = barr_freq

        if self.barr_freq == F_BARRIER_CONTINUOUS:
            self.discrete_barr = 0   # continuous
        else: self.discrete_barr = 1 # discrete    
        
        monitor_days = FTimeSeries.get_TimeSeries(i, F_BARRIER_TIMESERIES, F_BARRIER_TIMESERIESRUN)
        
        barrier_dict = FEqBarrierUtils.create_monitoring_dates(self.discrete_barr, \
            self.barr_freq, monitor_days, self.valuation_date, self.texp, self.exp_day)
        self.barr_dates = barrier_dict["barrier_mon_dates"]
        self.barr_monitoring_times = barrier_dict["barrier_mon_times"]
        
        # Remove all dividends which aren't paid out during the option's lifetime. The
        # method 'barrier_val_meth' will otherwise not be able to derive the most
        # efficient valuation method.  
        div_tmp = []
        has_past_div = 0
        for div in self.dividends:
            if (div[1] <= self.texp) and (div[0] > 0.0):
                if div[1] < 0.0: has_past_div = 1 
                else: div_tmp.append(div)
        if len(div_tmp)==0 and has_past_div:
            div_tmp.append((0, self.texp/2.0))
        self.dividends = div_tmp
        self.greeks = {'Greeks':{'Delta':-1,'Gamma':-1, 'Theta':-1}, 'Status': NOT_CALC}
        
        try: use_model = i.add_info(F_BARRIER_MODEL)
        except: use_model = ""
        
        self.use_model = use_model_enum_dict[use_model]
        
        if self.fix_fx:
            [self.corr_stock_fx, self.corr_matrix] = FEqBarrierUtils.get_corr_stock_fx(i)
            
    def pv(self):
        val_meth_params = FEqBarrierUtils.single_val_meth(self.dividends,\
                                self.discrete_barr, self.barrier_man, self.barr_monitoring_times,
                                self.barr_freq, self.price, self.texp, self.vol, self.use_model)
        res = FEqBarrierUtils.get_pv(self, val_meth_params)
        if not self.fix_fx:
            if str(type(res)) == "<type 'dict'>" or str(type(res)) == "<type 'dictionary'>":
                pv = res['PV'] * self.strike_theor_curr_fx
                res['PV'] = pv
            else: res = res * self.strike_theor_curr_fx 
        return res 

                
"""----------------------------------------------------------------------------
FUNCTION    
    pv() 

DESCRIPTION
    The function pv() calculates the price of a barrier option. 

ARGUMENTS
    i       Instrument  Barrier Option
    calc    Integer     0=>No calculation 1=>Perform calculation
    ref                 Optimisation parameter

RETURNS
   [res     float       Value of instrument
    exp_day date        Maturity date
    curr    string      Currency in which it was valued
    Fixed   string      Constant = 'Fixed']                      
----------------------------------------------------------------------------"""
def pv(i,calc=1,ref=0):
    try:
        extra_days = 0
        if calc:
            res = 0.0
            barrier_params = FBarrierParams(i)
            if barrier_params.price <= 0.0: 
                print "\n## !! EXCEPTION !! ##"
                raise F_BARRIER_EXCEPT, "The underlying price is zero!"
            try:
                print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if barrier_params.texp > 0: print get_info(barrier_params)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if i.exp_day < ael.date_valueday(): res = 0.0
            else:
                try: 
                    result = barrier_params.pv()
                    if str(type(result)) == "<type 'dict'>" or str(type(result)) == "<type 'dictionary'>":
                        has_greeks = 0; greeks = []
                        greeks.append(result["Delta"])
                        greeks.append(result["Gamma"])
                        greeks.append(result["Theta"])

                        for greek in greeks:
                            if greek != -1: 
                                has_greeks = 1
                                break       
                        if has_greeks: 
                            res = [result["PV"]]
                            res.extend(greeks)
                        else: res = result["PV"]
                    else: res = result
                except Exception, msg: 
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BARRIER_EXCEPT, msg
            extra_days = barrier_params.extra_days
        else: res = 0.0
    except F_BARRIER_EXCEPT, msg:
        print '\nModule:  FEqBarrier'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        res = 0.0
    return [ [ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ] ]

def get_info(BarrierParams):
    bp = BarrierParams
    s = ''
    s = s + "Instrument: \t" + bp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    for curve in bp.yield_curves:
        if curve[0] == 'Repo': insid = bp.insid
        elif curve[0] == 'Discount': insid = bp.underlying
        else: insid = bp.underlying
        s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + bp.currency + ")\n" 
    s = s + "\t\n"
    s= s + "Volatility:\t" + str(bp.vol_surface) + "\t(" + bp.insid + ")\n"
    s = s + "\t\n"  
    s = s + "Used repo rate:\t\t%*.*f" % (6, 4, bp.repo*100) + "\n"
    s = s + "Used volatility:\t%*.*f" % (6, 4, bp.vol*100)  + "\n"
    s = s + "Used discount rate:\t%*.*f" % (6, 4, bp.rate*100) + "\n"
    s = s + "\t\n" 

    s = s + "Barrier type:\t\t" + bp.exotic_type + "\n"
    s = s + "Barrier level:\t\t" + str(bp.barrier) + "\n"
    if bp.has_barrier_man:
        s = s + "Risk Management level:\t" + str(bp.barrier_man) + "\n"
    s = s + "\t\n" 
    
    s = s + "Rebate:\t\t\t" + str(bp.rebate) + "\n"
    if bp.pay_rebate == "Expiry": rebate_day = "Expiry"
    else: 
        if not bp.digital and (bp.exotic_type == "Down & Out" or bp.exotic_type == "Up & Out"):
            rebate_day = "Hit"
        elif bp.digital and (bp.exotic_type == "Down & Out" or bp.exotic_type == "Up & Out"): 
            rebate_day = "Expiry"
        elif not bp.digital and (bp.exotic_type == "Down & In" or bp.exotic_type == "Up & In"):
            rebate_day = "Expiry"
        else: rebate_day = "Hit"
    s = s + "Rebate will be paid on\t" + str(rebate_day) + "\n"
    s = s + "\t\n"
    
    if bp.discrete_barr: disc = 'Yes'
    else: disc = 'No'
    s = s + "Discrete barrier:\t" + disc + "\n"
    s = s + "Monitoring times:\t" + str(bp.barr_monitoring_times) + "\n"
    if bp.digital: digital = "Yes"
    else: digital = "No"
    s = s + "Digital:\t\t" + str(digital) + "\n"
    s = s + "\t\n" 
    if bp.fix_fx: quanto = "Yes"
    else: quanto = "No"
    s = s + "Quanto:\t\t\t" + quanto + "\n"
    if bp.fix_fx:
        s = s + "Fixed FX rate:\t\t" + str(bp.fx_rate) + "\n"
        s = s + "FX volatility:\t\t%*.*f" % (6, 4, bp.fx_vol*100) + "\n"
        s = s + "FX vol. surface:\t" + bp.vol_surf_fx + "\n"
        s = s + "Correlation:\n"
        fx = bp.strike_curr.insid +"/" + bp.currency 
        s = s + "\t\t\t" + str(bp.underlying)+ " vs. " + str(fx) + " = " + str(bp.corr_stock_fx) + "\n"  
        s = s + "Corr Matrix:\t\t" + bp.corr_matrix + "\n"
        s = s + "Foreign disc. rate:\t%*.*f" % (6, 4, bp.foreign_rate*100) + "\n"
        s = s + "Foreign yield curve:\t" + bp.foreign_yc + "\n"
    s = s + "\t\n"
    if bp.knocked != "Yes": 
        status = "Not yet knocked"
        date = ""
    else: 
        status = "Knocked"
        try: date = bp.knocked_date
        except: date = ""

    s = s + "Barrier status:\t\t" + status + "\n"
    if date != "":
        s = s + "Barrier knock date:\t" + str(date) + "\n"
    [val_meth, steps] = FEqBarrierUtils.single_val_meth(bp.dividends,\
                         bp.discrete_barr, bp.barrier_man, bp.barr_monitoring_times,
                         bp.barr_freq, bp.price, bp.texp, bp.vol, bp.use_model)
    if status != "Knocked":
        s = s + "Valuation method:\t" + str(val_meth) + "\n"
        s = s + "Steps:\t\t\t" + str(steps) + "\n"
    s = s + "\t\n" 
    
    s = s + "Underlying:\t\t" + bp.underlying + "\n"
    s = s + "Underlying price:\t" + str(bp.price) + "\n"

    if bp.dividends != []:
        s = s + "\t\n"
        s = s + "Underlying Dividends (in " + bp.currency + ") :\n"
        s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
        for d in bp.div_entity:
            s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
    s = s + "\t\n"
    s = s + "Used valuation function: \tFEqBarrier.pv \n"
    s = s + "Mapped in context:\t\t" + bp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s



# Utility functions used by ASQL Query
# ./App/PricingBarrier

def GetUser(*rest):
    return ael.userid()

def UsedValFun(i, *rest):
    B = FBarrierParams(i)
    b = FEqBarrierUtils.single_val_meth(B.dividends,\
                                    B.discrete_barr, B.barrier, B.barr_monitoring_times,
                                B.barr_freq, B.price, B.texp, B.vol, B.use_model)
    val_meth = b[0]
    return str(val_meth)

"""----------------------------------------------------------------------------
FUNCTION    
    update_addinfo() 

DESCRIPTION
    The function updates the Addtional Info fields 'FBarrier Crossed' and 
    'FBarrier Cross Date' when the barrier has been hit. 

ARGUMENTS
    i       Instrument  Barrier Option
    value   String      What the Addtional Info field should be set to.
    barrier Integer     The upper or lower barrier for double barrier options.

RETURNS
   diff     If the barrier is already crossed the value zero is returned.
----------------------------------------------------------------------------"""
def update_addinfo(i,value,barrier=None):
    res = 0       
    # Set addinfo field for "FBarrier Crossed" to "Yes TEMP?"
    ic = i.clone() 
    ai = ael.AdditionalInfo.new(ic)
    ais  = ael.AdditionalInfoSpec[F_BARRIER_CROSSED]
    ai.addinf_specnbr = ais.specnbr
    ai.value = value
    try: 
        ic.commit()
        if barrier == None: barrier = i.barrier
        print "\n## !! UPDATED VALUE !! ##"
        print "Instr : ", i.insid
        print "Event :  The spot price has crossed the barrier = ", barrier
    except: pass

    # Set addinfo field for "FBarrier Cross Date" to date of knock.
    ic = i.clone() 
    ai = ael.AdditionalInfo.new(ic)
    ais = ael.AdditionalInfoSpec[F_BARRIER_CROSSED_DATE]
    ai.addinf_specnbr = ais.specnbr
    ai.value = str(ael.date_valueday())
    try:
        ic.commit() 
        ael.poll()
        print "Action: The AddInfo fields 'FBarrier Crossed' and 'FBarrier Cross Date' have been set."
    except RuntimeError:
        print "Action: The instrument has already been updated."
    return 0


def create_barrier_timeserie(i):    
    barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
    monitor_days = FTimeSeries.get_TimeSeries(i, F_BARRIER_TIMESERIES, F_BARRIER_TIMESERIESRUN)
    start_date = ael.date_valueday()
    end_date = i.exp_day
    if len(monitor_days) == 0:
        if barr_freq == F_BARRIER_DAILY:
            period = 'daily'
            print "CREATING DAILY TIMESERIES for instrument ", i.insid
        elif barr_freq == F_BARRIER_WEEKLY:
            period = '-1w'
            start_date = i.exp_day
            end_date = ael.date_valueday()
            print "CREATING WEEKLY TIMESERIES for instrument ", i.insid
        elif barr_freq == F_BARRIER_MONTHLY:
            period = '-1m'
            start_date = i.exp_day
            end_date = ael.date_valueday()
            print "CREATING MONTHLY TIMESERIES for instrument ", i.insid
        elif barr_freq == F_BARRIER_YEARLY:
            period = '-1y'
            start_date = i.exp_day
            end_date = ael.date_valueday()
            print "CREATING YEARLY TIMESERIES for instrument ", i.insid
        elif barr_freq == F_BARRIER_DAILY_LAST_MONTH:
            period = 'daily'
            start_date = i.exp_day.add_period('-1m')
            if i.exp_day > ael.date_valueday().add_period('1m'):
                start_date = i.exp_day.add_period('-1m')
            else:
                start_date = ael.date_valueday()
            print "CREATING DAILY TIMESERIES LAST MONTH for instrument ", i.insid
        elif barr_freq == F_BARRIER_WEEKLY_LAST_MONTH:
            period = 'weekly'
            start_date = i.exp_day.add_period('-1m')
            print "CREATING WEEKLY TIMESERIES LAST MONTH for instrument ", i.insid
        elif barr_freq == F_BARRIER_DAILY_LAST_TWO_WEEKS:
            period = 'daily'
            if i.exp_day > ael.date_valueday().add_period('2w'):
                start_date = i.exp_day.add_period('-2w')
            else: start_date = ael.date_valueday()
            print "CREATING DAILY TIMESERIES LAST TWO WEEKS for instrument ", i.insid
        else:
            # Assuming daily monitor frequency
            period = 'daily'
            print "CREATING DAILY TIMESERIES for instrument ", i.insid

        print "This is only done the first time when running the function UpdateBarrierStatus. It may take several minutes."

        monitor_days = FTimeSeries.make_periodic_TimeSeries_runno_fix(i,
               F_BARRIER_TIMESERIES, start_date, end_date, period, -1, 'Yes')
    return 0


"""----------------------------------------------------------------------------
FUNCTION    
    calc_diff_spot_barrier() 

DESCRIPTION
    The function calculates the difference (in percent) between the barrier and
    the spot price. 

ARGUMENTS
    i       Instrument  Barrier Option

RETURNS
   diff     If the barrier is already crossed the value zero is returned.
----------------------------------------------------------------------------"""
def calc_diff_spot_barrier(i,*rest):
    try:
        barrier_status = i.add_info(F_BARRIER_CROSSED)
        barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        if barrier_status !="Yes" and barrier_status !="Yes TEMP?" : 
            price = i.und_insaddr.used_price(None, i.strike_curr.insid) 
            if price != 0.0:
                if i.exotic_type == "Down & Out" or i.exotic_type == "Down & In":
                    res = (price - i.barrier)/(1.0*price)*100
                elif i.exotic_type == "Up & Out" or i.exotic_type == "Up & In":
                    res = (i.barrier - price)/(1.0*price)*100
                else:
                    print "\n## !! EXCEPTION !! ##"
                    raise F_BARRIER_EXCEPT, "Wrong Barrier type."   
            else:
                print "\n## !! NO VALUE !! ##"
                raise F_BARRIER_EXCEPT, "No underlying price exist for " + str(i.und_insaddr.insid)
            if res <= 0 and barr_freq == F_BARRIER_CONTINUOUS:
                res = 0       
                update_addinfo(i, "Yes TEMP?")
                res = 0.0
            else:
                res = int(res+1)
        elif barrier_status == "Yes" or barrier_status == "Yes TEMP?":res = 0.0
        else: 
            print "\n## !! EXCEPTION !! ##"
            raise F_BARRIER_EXCEPT, "Wrong Barrier status in addinfo field 'FBarrier Knocked'."
        return res
    except F_BARRIER_EXCEPT, msg:
        print
        print 'Module: FEqBarrier'
        print 'Error : ', msg
        print 'Instr : ', i.insid
        return 0.0




