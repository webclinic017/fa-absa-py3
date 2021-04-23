""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FEqLadderUtils - Valuation of ladder options
    
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
   Calculates the theoretical price of a ladder option. 
   European options with discrete / continuous dividends and discrete 
   / continuous rungs (barriers) are handled.
 
----------------------------------------------------------------------------"""
import ael
import math
import FEqBarrier
import FEqBarrierUtils
import FTimeSeries
from FEqUtilsPRIME import *

F_LADDER_TIMESERIES     = 'FLadderRungs'
F_LADDER_EXCEPT         = 'f_eq_ladder_xcp'
F_LADDER_WARNING        = 'f_eq_ladder_warning'
F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp'  
F_LADDER_FIRSTRUNG      = 0

F_BARRIER_CONTINUOUS    = 'Continuous'
F_DAYS_PER_YEAR         = 365.25

"""----------------------------------------------------------------------------
get_rung_data() 
    Extract all time series data for the ladder option.
----------------------------------------------------------------------------"""    
def get_rung_data(i,trading = 0,*rest):
    try:
        rungs_tot = []
        more_rungs = 1 
        j = F_LADDER_FIRSTRUNG 
        while more_rungs:
            rung = FTimeSeries.get_TimeSeries(i, F_LADDER_TIMESERIES, j)      
            more_rungs = len(rung)
            j = j+1             
            if more_rungs > 1:
                if trading: return 'There are more than one rung for some run numbers.'
                print "\n## !! EXCEPTION !! ##"
                raise F_LADDER_EXCEPT, 'There are more than one rung for some run numbers.'
            elif more_rungs:
                if rung[0][1] == -1:
                    if trading: return 'Some rungs equal -1. Update them with .AppLadderRungs.'
                    print "\n## !! EXCEPTION !! ##"
                    raise F_LADDER_EXCEPT, 'Some rungs still equal -1. Update them with the ASQL appl.  .AppLadderRungs.'
                rungs_tot.append(rung[0])
        if rungs_tot == []:
            if trading: return 'No positive ladder rungs are defined!'
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'No rungs are given.'
        return rungs_tot
    except F_LADDER_EXCEPT, msg:
        if trading:
            print '\nModule: FEqLadderUtils'
            print 'Error :', msg
            print 'Instr :', i.insid
            return []
        else:
            raise F_LADDER_EXCEPT, msg
            
"""----------------------------------------------------------------------------
get_rungs() 
    Extract and check the rungs for the ladder option.
----------------------------------------------------------------------------"""    
def get_rungs(insid,rungs_tot,exp_day,put_call,price,barr_freq,strike,trading=0):    
    latest_reached_rung = strike
    rungs = []
    for rung in rungs_tot:
        try: 
            if str(type(rung[0])) == "<type 'str'>":
                float(rung[0])
        except: return [[], 0]
        if rung[0] > exp_day: 
            if trading: return ['There are rung dates after the expiry date']
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'There are rung dates after the expiry date'
        if put_call and rung[1] < price and rung[0] == exp_day and barr_freq == F_BARRIER_CONTINUOUS:
            if trading: return ['The underlying price is above one rung which has not been breached by the underlying asset. Please update the ladder time series.']
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'The underlying price is above one rung which has not been breached by the underlying asset. Please update the ladder time series.'
        if (not put_call) and rung[1] > price and rung[0] == exp_day and barr_freq == F_BARRIER_CONTINUOUS:
            if trading: return ['One rung is negative.']
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'The underlying price is below one rung which has not been breached by the underlying asset. Pleae update the ladder time series.'
        if rung[1] < 0.0:
            if trading: return ['One rung is negative.']
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'One rung is negative.'
        if put_call and rung[1] <= strike:
            #print "\n## !! IGNORING VALUE !! ##"
            #print 'Message : One rung is less than or equal to the strike price. This rung is ignored.'
            pass
        elif not(put_call) and rung[1] >= strike:
            #print "\n## !! IGNORING VALUE !! ##"
            #print 'Message : One rung is greater than or equal to the strike price. This rung is ignored.'
            pass
        elif rung[0] == exp_day:
            rungs.append(rung[1])
        else:
            if put_call and latest_reached_rung < rung[1]:
                latest_reached_rung = rung[1]
            if (not put_call) and latest_reached_rung > rung[1]:      
                latest_reached_rung = rung[1]

    for rung in rungs:
        if put_call and latest_reached_rung > rung:
            if trading: return ["One rung which already has been breached is greater than one which has not been reached."]
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, "One rung which already has been breached is greater than one which has not been reached."
        elif (not put_call) and latest_reached_rung < rung:
            if trading: return ['One rung which already has been breached is less than one which has not been reached.']
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'One rung which already has been breached is less than one which has not been reached.'

    rungs.append(latest_reached_rung)
    rungs.sort()

    # Sort out any doubles
    rungs_temp = []
    temp = -1.0
    if strike < 0.0:
        if trading: return ['The strike price is negative.']
        print "\n## !! EXCEPTION !! ##"
        raise F_LADDER_EXCEPT, 'The strike price is negative.'
    for rung in rungs:
        if rung == temp:
            #raise F_LADDER_WARNING,'One rung is given twice.'
            # Ignore the second rung.
            pass
        else:
            rungs_temp.append(rung) 
        temp = rung

    rungs = rungs_temp 
    return [rungs, latest_reached_rung]
            
"""----------------------------------------------------------------------------
get_ladder_strike() 
    The function extracts the last rung.
----------------------------------------------------------------------------"""    
def get_ladder_strike(rungs):
    rungs = AsList(rungs)
    nr_of_rungs = len(rungs) - 1
    try:
        last_rung = rungs[nr_of_rungs]
        float(last_rung)
        return last_rung
    except: return 'No ladder strike is calculated.'

    
"""----------------------------------------------------------------------------
get_rungs() 
    Extract and check the rungs for the ladder option.
----------------------------------------------------------------------------"""    
def get_ladder_pv(ladder_params,trading=0):
    lp = ladder_params
    try:
        strike_ladder = lp.strike
        res = 0.0
        delta = 0; gamma = 0; theta = 0
        nr_of_rungs = len(lp.rungs) - 1
        if not lp.put_call: lp.rungs.reverse()
        
        # Put => -1, Call => 1
        fi = -1 + 2*lp.put_call
        
        # Put => 1 = "Down & In"  # Call => 3 = "Up & In"
        lp.barrier_type_nbr = (lp.put_call == 0) + 3*(lp.put_call == 1)
        
        for j in range(nr_of_rungs):
            lp.barrier_man = lp.rungs[j+1]
            lp.strike  = lp.rungs[j]
            lp.rebate  = 0.0
            lp.digital = 0
            val_meth_params = FEqBarrierUtils.single_val_meth(lp.dividends,\
                    lp.discrete_barr, lp.barrier_man, lp.barr_monitoring_times,
                    lp.barr_freq, lp.price, lp.texp, lp.vol, 2)
                    
            part_res = FEqBarrierUtils.get_pv(lp, val_meth_params)
            
            lp.rebate = fi*(lp.rungs[j+1] - lp.rungs[j])
            lp.digital = 1
            part_res_digital = FEqBarrierUtils.get_pv(lp, val_meth_params)
            
            res = res + part_res['PV'] - part_res_digital['PV']
            
            if trading:
                has_tree_greeks = has_greeks(part_res)
                has_tree_greeks_digital = has_greeks(part_res_digital)
                if (has_tree_greeks and has_tree_greeks_digital) and \
                   (delta != -1 and gamma != -1 and theta != -1):
                    delta = delta + part_res['Delta'] - part_res_digital['Delta']
                    gamma = gamma + part_res['Gamma'] - part_res_digital['Gamma']
                    theta = theta + part_res['Theta'] - part_res_digital['Theta']
                else: 
                    delta = -1; gamma = -1; theta = -1
            else: delta = -1; gamma = -1; theta = -1
        
        part_res = ael.eq_option(lp.price, lp.texp, lp.vol, lp.rate, lp.carry_cost,
                                lp.rungs[nr_of_rungs], lp.put_call,
                                lp.eur_ame, lp.dividends)
        if part_res == -1:
            print "\n## !! EXCEPTION !! ##"
            raise F_LADDER_EXCEPT, 'Valuation error.'

        part_res_digital = fi * math.exp(-lp.texp*lp.rate) \
                            *(lp.rungs[nr_of_rungs] - strike_ladder)
        res = res + part_res + part_res_digital
        
        if trading:
            if (delta != -1 and gamma != -1 and theta != -1):
                delta = delta + lp.vanilla_res[1]
                gamma = gamma + lp.vanilla_res[2]
                theta = theta + lp.vanilla_res[3] +1.0/F_DAYS_PER_YEAR*lp.rate*part_res_digital
                has_greek = 1
            else: has_greek = 0
        else: has_greek = 0
        if has_greek:
            res_dict = {"PV":res, "Delta":delta, "Gamma":gamma, "Theta":theta}
        else: res_dict = {"PV":res}
        return res_dict
    except F_BARRIER_EXCEPT, msg:
        raise F_LADDER_EXCEPT, msg
        


















