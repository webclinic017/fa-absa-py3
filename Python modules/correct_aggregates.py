""" AggregationArchiving:1.3.2.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
        correct_aggregates - correction of aggregates that are invalid

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        
        
ENDDESCRIPTION
----------------------------------------------------------------------------"""
import sys
import ael
import time
import string

from GenAgg import *

counter = 0
statuslist = []

def correct_aggregates():

    global statuslist
    
    M = {}
    
    indata = {'date': ael.date_today(), 'daysalive': 0, 'portfolio': [], \
             'instrument': [], 'underlying': [], 'instype': [], \
             'ClearPLTime': '1970-01-01 00:00:00', 'positionsize': 2, 
             'correctagg': 'Correct', 'verbose': 1}

    if store_variables(M, indata) == -1:
        print '\Correction of aggregate trades could not start.'

    result = 'finished'
    if perform_correction(M) == -1:
        result = 'failed'

    status = '\nCorrection of aggregate trades %s %s' % \
        (result, time.ctime(time.time()))
    statuslist.append(status)

def start():
    print "Starting trade subscription"
    ael.Trade.subscribe(trade_update_cb)
    correct_aggregates()
    return   

def status():
    global counter
    global statuslist
    status = string.join(statuslist, '\n')
    status2 = "\nNumber of corrections made so far = %d" % counter
    return status + status2
    
def stop():
    print "Stopping trade subscription"
    ael.Trade.unsubscribe(trade_update_cb)

def find_aggregate(trade):
    if trade.prfnbr != None:
        for t in trade.prfnbr.trades():
            if t.insaddr == trade.insaddr:
                if t.aggregate_trdnbr != None:
                    return t.aggregate_trdnbr
    return None

def trade_update_cb(obj, trade, arg, event): 
    global counter
    correct = 0
    if trade == None: 
        return
        
    if event == "insert":
        agg = find_aggregate(trade)
        if agg != None and agg.aggregate == -1:
            correct = 1
    elif event == "delete":
        if trade.aggregate_trdnbr != None:
            correct = 1
    elif event == "update":
        old = ael.get_old_entity()
        if old != None and (trade.value_day != old.value_day or \
           trade.prfnbr != old.prfnbr):
            correct = 1
        elif trade.aggregate_trdnbr != None and \
            trade.aggregate_trdnbr.aggregate == -1:
            correct = 1
        
    else:
        ael.log("trade_update_cb: Unexpected event %s" % event)

    if correct:
        status = "Caught %d %s" % (trade.trdnbr, event) 
        statuslist.append(status)

        counter = counter + 1
        correct_aggregates()
    
#start()
#stop()


