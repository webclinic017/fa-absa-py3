"""----------------------------------------------------------------------------
MODULE
    FMonitorBarrierPrice - Update barrier status if barrier crossed.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        This module corrects aggregated trades in a ARENA Database. An 
        aggregated trade may be marked dirty if for example it is moved 
        to another portfolio. 
        
----------------------------------------------------------------------------"""

import ael
import FEqBarrier
import FEqDblBarrier
F_BARRIER_MONITOR_FRQ = 'FBarrierMonitorFrq'
F_BARRIER_CONTINUOUS  = 'Continuous'

counter = 0
statuslist = ""
update_single_barrier = 0
update_double_barrier = 0
und_to_single_dict = {}
und_to_double_dict = {}

def start():
    global und_to_single_dict
    global und_to_double_dict
    print("Starting price subscription")
    
    # Single Barrier options 
    cl_b = ael.ChoiceList.read('list="Category" and entry="Barrier"') 
    barriers = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_b.seqnbr))  

    for i in barriers: 
        barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        if i.exp_day > ael.date_valueday() and barr_freq == F_BARRIER_CONTINUOUS:
            if und_to_single_dict.has_key(i.und_insaddr):
                und_to_single_dict[i.und_insaddr].append(i)
            else:
                und_to_single_dict[i.und_insaddr] = [i]

    # Double Barrier options
    cl_dbl_b = ael.ChoiceList.read('list="Category" and entry="DoubleBarrier"') 
    dbl_barriers = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_dbl_b.seqnbr))  

    for i in dbl_barriers: 
        barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        if i.exp_day > ael.date_valueday() and barr_freq == F_BARRIER_CONTINUOUS:
            if und_to_double_dict.has_key(i.und_insaddr):
                und_to_double_dict[i.und_insaddr].append(i)
            else:
                und_to_double_dict[i.und_insaddr] = [i]
    ael.Price.subscribe(price_update_cb)
    return   

def status():
    global statuslist
    str1 = "\nNumber of corrections made so far = %d" % counter
    return statuslist + str1
    
def stop():
    print("Stopping price subscription")
    ael.Price.unsubscribe(price_update_cb)

def price_update_cb(obj, price, arg, event): 
    global counter
    global statuslist
    global update_single_barrier
    global update_double_barrier
    global und_to_ins_dict
    
    if price == None: return
        
    if event == "update":
        if und_to_single_dict.has_key(price.insaddr):
            update_single_barrier = price.insaddr
        if und_to_double_dict.has_key(price.insaddr):
            update_double_barrier = price.insaddr
        
    elif (event != "insert" and event != "delete"):
        ael.log("price_update_cb: Unexpected event %s" % event)
    
    if update_single_barrier or update_double_barrier:
        statuslist = "Caught %s %s" % (price.insaddr.insid, event) 
        counter = counter + 1
        if update_single_barrier:
            for i in und_to_single_dict[update_single_barrier]:
                FEqBarrier.calc_diff_spot_barrier(i)
            update_single_barrier = 0
        if update_double_barrier:
            for i in und_to_double_dict[update_double_barrier]:
                FEqDblBarrier.calc_diff_spot_lower_barrier(i)
                FEqDblBarrier.calc_diff_spot_upper_barrier(i)
        update_double_barrier = 0


#start()
#stop()




