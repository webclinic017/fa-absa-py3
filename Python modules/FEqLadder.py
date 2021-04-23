""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqLadder - Valuation of ladder options
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the theoretical price of a ladder option. 
   European options with discrete / continuous dividends and discrete 
   / continuous rungs (barriers) are handled.
 
----------------------------------------------------------------------------"""
LOG_PARAMETERS = 0

import ael
import FEqBarrier
import FEqBarrierUtils
import FTimeSeries
import FEqLadderUtils

F_LADDER_TIMESERIES     = 'FLadderRungs'
F_LADDER_EXCEPT         = 'f_eq_ladder_xcp'
F_LADDER_WARNING        = 'f_eq_ladder_warning'
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp'  
F_LADDER_FIRSTRUNG      = 0
F_BARRIER_MONITOR_FRQ   = 'FBarrierMonitorFrq'
F_BARRIER_CONTINUOUS    = 'Continuous'
counter = 0

"""----------------------------------------------------------------------------
CLASS                   
    FLadderParams - Parameters for ladder options.

INHERITS
    FEqBarrier
                
DESCRIPTION             
    The class extracts all parameters needed to value a ladder option.

CONSTRUCTION    
    i               Instrument  An instrument that is a ladder option.
    
MEMBERS (excluding the barrier members)
    rungs       List[Float]     contains the latest breached rung plus all
                                the remaining rungs which have not been breached
                                by the underlying asset. If the underlying asset 
                                has not reached any rung we also let the strikeprice
                                be included in this list.

----------------------------------------------------------------------------"""
class FLadderParams(FEqBarrier.FBarrierParams):
    def __init__(self, i):
        FEqBarrier.FBarrierParams.__init__(self, i)
        
        self.rung_data = FEqLadderUtils.get_rung_data(i)
        
        [self.rungs, self.latest_reached_rung] = FEqLadderUtils.get_rungs(i.insid,\
                    self.rung_data, self.exp_day, self.put_call, self.price,\
                    self.barr_freq, self.strike)   
    def pv(self):
        res_dict = FEqLadderUtils.get_ladder_pv(self)
        res = res_dict['PV']* self.strike_theor_curr_fx 
        return res 

"""----------------------------------------------------------------------------
FUNCTION    
    pv() 

DESCRIPTION
    The function pv() calculates the price of a ladder option. 

ARGUMENTS
    i       Instrument  Ladder Option
    calc    Integer     0=>No calculation 1=>Perform calculation
    ref                 Optimisation parameter

RETURNS
   [res     float       Value of instrument
    exp_day date        Maturity date
    curr    string      Currency in which it was valued
    Fixed   string      Constant = 'Fixed']                      
----------------------------------------------------------------------------"""
def pv(i, calc, ref):
    res = 0.0
    try:
        extra_days = 0
        if calc:
            if (i.exercise_type == 'American') or (i.exercise_type == 'Bermudan'): 
                print "\n## !! EXCEPTION !! ##"
                raise F_LADDER_EXCEPT, 'The ladder option valuation only handles plain European options.'
            if i.digital: 
                print "\n## !! EXCEPTION !! ##"
                raise F_LADDER_EXCEPT, 'The ladder option valuation does not handle digital options.'
            if not(i.und_instype == 'Stock' or i.und_instype == 'EquityIndex'):
                print "\n## !! EXCEPTION !! ##"
                raise F_LADDER_EXCEPT, 'The ladder option valuation only handles Stock or EquityIndex as underlying instrument' 
            
            ladder_params = FLadderParams(i)
            try:
                print_info = i.add_info("FPrintInfo")
            except: print_info = ""
            if globals()['counter'] == 5: globals()['counter'] = 0
            if (LOG_PARAMETERS or print_info == "Yes") and globals()['counter'] == 0:
                if ladder_params.texp > 0: print get_info(ladder_params)
                else: print "\n## !! OPTION " + i.insid + " HAS EXPIRED !! ##"
            globals()['counter'] = globals()['counter'] + 1
            if i.exp_day < ael.date_valueday(): res = 0.0
            else:
                res = ladder_params.pv()
                extra_days = ladder_params.extra_days
    except F_LADDER_EXCEPT, msg:
        print '\nModule: FEqLadder'
        print 'Error :', msg
        print 'Instr :', i.insid
        res = 0.0
    return  [[ res, i.exp_day.add_days(extra_days), i.curr, 'Fixed' ]]


"""----------------------------------------------------------------------------
get_info() 
    Retrieves the valuation parameters for a ladder option.
----------------------------------------------------------------------------"""    
def get_info(ladder_params):
    lp = ladder_params
    s = ''
    s = s + "Instrument: \t" + lp.insid + "\t is using parameter(s): \n"  
    s = s + "\t\n"
    for curve in lp.yield_curves:
        if curve[0] == 'Repo': insid = lp.insid
        elif curve[0] == 'Discount': insid = lp.underlying
        else: insid = lp.underlying
        s = s + "Yield curve:\t" + str(curve[1]) + " for " + str(curve[0]) + " (" + insid + ", " + lp.currency + ")\n" 
    s = s + "\t\n"
    s= s + "Volatility:\t" + str(lp.vol_surface) + "\t(" + lp.insid + ")\n"
    s = s + "\t\n"  
    s = s + "Used repo rate:\t\t%*.*f" % (6, 4, lp.repo*100) + "\n"
    s = s + "Used volatility:\t%*.*f" % (6, 4, lp.vol*100)  + "\n"
    s = s + "Used discount rate:\t%*.*f" % (6, 4, lp.rate*100) + "\n"
    s = s + "\t\n" 
    
    tot_no_rungs = len(lp.rung_data) 
    no_future_rungs = len(lp.rungs) - 1
    no_passed_rungs = tot_no_rungs - no_future_rungs
    if no_passed_rungs == 0.0: latest_rung = ""
    else: latest_rung = lp.latest_reached_rung
    s = s + "Number of passed rungs:\t" + str(no_passed_rungs) + "\n"
    s = s + "Number of future rungs:\t" + str(no_future_rungs) + "\n"
    s = s + "Latest reached Rung:\t" + str(latest_rung) + "\n"
    rungs_copy = lp.rungs[:]
    rungs_copy.remove(lp.latest_reached_rung)
    s = s + "Future Rung Values:\t" + str(rungs_copy) + "\n"
    s = s + "\t\n" 
    
    if lp.discrete_barr: disc = 'Yes'
    else: disc = 'No'
    s = s + "Discrete Monitor Freq.:\t" + disc + "\n"
    if disc == 'Yes':
        s = s + "Monitoring times:\t" + str(lp.barr_monitoring_times) + "\n"

    [val_meth, steps] = FEqBarrierUtils.single_val_meth(lp.dividends,\
                         lp.discrete_barr, lp.latest_reached_rung, lp.barr_monitoring_times,
                         lp.barr_freq, lp.price, lp.texp, lp.vol, lp.use_model)
    s = s + "Valuation method:\t" + str(val_meth) + "\n"
    s = s + "Steps:\t\t\t" + str(steps) + "\n"
    s = s + "\t\n" 
    
    s = s + "Underlying:\t\t" + lp.underlying + "\n"
    s = s + "Underlying price:\t" + str(lp.price) + "\n"

    if lp.dividends != []:
        s = s + "\t\n"
        s = s + "Underlying Dividends (in " + lp.currency + ") :\n"
        s = s + "\t\tEx Div Day \tRecord Day \tAmount \tTax Factor\n"
        for d in lp.div_entity:
            s = s + "\t\t" + str(d.ex_div_day) + "\t" + str(d.day) + "\t" + str(d.dividend) + "\t" + str(d.tax_factor) + "\n"
    s = s + "\t\n"
    s = s + "Used valuation function: \tFEqLadder.pv \n"
    s = s + "Mapped in context:\t\t" + lp.used_context + "\n"
    s = s + "\t\n" + "\t\n"
    return s


"""----------------------------------------------------------------------------
FUNCTION    
    calc_diff_spot_rung() 

DESCRIPTION
    The function calculates the difference (in percent) between the closest rung and
    the spot price. 

ARGUMENTS
    i       Instrument  Ladder Option

RETURNS
   diff     If all rungs have been crosed, the value 0 is returned.
----------------------------------------------------------------------------"""
def calc_diff_spot_rung(i,*rest):
    barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
    price = i.und_insaddr.used_price()
    if price == 0.0: return 0
    rungs = []
    ts_specnbr = ael.TimeSeriesSpec[F_LADDER_TIMESERIES]
    for t in i.time_series():
        if (t.ts_specnbr == ts_specnbr and t.day == i.exp_day):
            rungs.append([t.value, t.run_no, t.seqnbr])
    if rungs != []:
        [rung_value, run_no, seqnbr] = min(rungs[:])
        if i.call_option:
            res = (rung_value - price)/(1.0*price)*100
        else:     
            res = (price - rung_value)/(1.0*price)*100
        if res <= 0 and barr_freq == F_BARRIER_CONTINUOUS:
            t = ael.TimeSeries[seqnbr]
            if t.ts_specnbr == ts_specnbr:
                t_clone = t.clone()
                t_clone.day = ael.date_valueday()
                t_clone.commit()
                print "## !! UPDATED VALUE !! ##"
                print "Instr : ", i.insid
                print "Event :  The spot price has crossed a ladder rung = ", rung_value, "\n"
                ael.poll()
                return calc_diff_spot_rung(i)
    else: res = 0
    return res




















