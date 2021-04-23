""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FTimesSeries 
     
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Handles timeseries for a given instrument

----------------------------------------------------------------------------"""
import ael
import sys
from math import *

RUN_NUMBER_FIX=0
EXCEPT_TIMESERIES = 'time_series_exception'

"""----------------------------------------------------------------------------
FUNCTION    
    make_TimeSeries_entry() 

DESCRIPTION
    Enters a value at a specified date for an instrument and a TimeSeries.
    
ARGUMENTS
    ins          Instrument      The TimeSeries belongs to this instrument   
    run_no       int             Number to separate different TimeSeries for the same instrument.
    date         date            AEL date to enter in the TimeSeries.
    value        float           The corresponding value to the specified date. 
    
RETURNS
    Has no return value.                
----------------------------------------------------------------------------"""
def make_TimeSeries_entry(ins, series_name, run_no, date, value):
    # store new value in TimeSeries
    try:
        if ins.time_series() != []:
            clear_single_TimeSeries_entry(ins, series_name, run_no, date)
        
        ts_specnbr = ael.TimeSeriesSpec[series_name]
        if ts_specnbr == None: raise 'EXCEPT_TIMESERIES', 'The Time Series ' + series_name + ' is invalid.'
        ts = ael.TimeSeries.new() 
        ts.recaddr = ins.insaddr 
        ts.ts_specnbr = ts_specnbr.specnbr 
        ts.day = date
        ts.run_no = run_no 
        ts.value = value 
        ts.commit()
        ael.poll()
    except EXCEPT_TIMESERIES, msg:
        print 'ERROR in make_TimeSeries_entry():', msg
        raise EXCEPT_TIMESERIES, "The entry at " + str(date) + " for the instrument " + ins.insid + " could not be made."

"""----------------------------------------------------------------------------
FUNCTION    
    clear_TimeSeries() 

DESCRIPTION
    Removes all entries of TimeSeries type with a certain run number for a 
    specified instrument.
    
    
ARGUMENTS
    ins          Instrument      The TimeSeries belongs to this instrument   
    run_no       int             Number to separate different TimeSeries for 
                                 the same instrument.
    
RETURNS
    Has no return value.                
----------------------------------------------------------------------------"""
def clear_TimeSeries(ins,series_name,run_no=None,*rest):
    try:
        ts_specnbr = ael.TimeSeriesSpec[series_name]
        if ts_specnbr == None: raise 'EXCEPT_TIMESERIES', 'The Time Series ' + series_name + ' is invalid.'
        for t in ins.time_series():
            if ((t.run_no == run_no) or run_no == None) and (t.ts_specnbr == ts_specnbr):
                t.delete()
        print "\nEntries has been deleted for the instrument ", ins.insid, " in the time series ", series_name
        ael.poll()
        return ins.insid
    except EXCEPT_TIMESERIES, msg:
        print 'ERROR in clear_TimeSeries():', msg
        raise EXCEPT_TIMESERIES, "No TimeSeries for the instrument " + ins.insid + " could be deleted."

"""----------------------------------------------------------------------------
FUNCTION    
    clear_single_TimeSeries_entry() 

DESCRIPTION
    Removes all entries of TimeSeries type for a specified instrument.
    
ARGUMENTS
    ins         Instrument      The TimeSeries belongs to this instrument.   
    date        Date            This AEL date and its corresponding value are deleted.
    run_no      int             Number to separate different TimeSeries for the same instrument.
    
RETURNS
    Has no return value.                
----------------------------------------------------------------------------"""
def clear_single_TimeSeries_entry(ins,series_name,run_no,date,*rest):
    try:
        ts_specnbr = ael.TimeSeriesSpec[series_name]
        if ts_specnbr == None: raise 'EXCEPT_TIMESERIES', 'The Time Series ' + series_name + ' is invalid.'
        for t in ins.time_series():
            if (t.day == date) and (t.run_no == run_no) and (t.ts_specnbr == ts_specnbr):
                t.delete()
                #print "Deleted the time series entry ", str(date), "for the instrument ", ins.insid
        ael.poll()
        return ins.insid
    except EXCEPT_TIMESERIES, msg:
        print 'ERROR in clear_single_TimeSeries_entry():', msg
        raise EXCEPT_TIMESERIES, "The TimeSeries entry " + str(date) +  " for the instrument " + ins.insid + " could not be deleted."


"""----------------------------------------------------------------------------
FUNCTION    
    update_single_TimeSeries_entry() 

DESCRIPTION
    Updates the value of a certain TimeSeries entry.
    
ARGUMENTS
    ins         Instrument      The TimeSeries belongs to this instrument.   
    date        Date            This AEL date and its corresponding value are deleted.
    run_no      int             Number to separate different TimeSeries for the same instrument.
    
RETURNS
    Has no return value.                
----------------------------------------------------------------------------"""
def update_single_TimeSeries_entry(ins,series_name,run_no,date,new_value,*rest):
    try:
        ts_specnbr = ael.TimeSeriesSpec[series_name]
        if ts_specnbr == None: raise 'EXCEPT_TIMESERIES', 'The Time Series ' + series_name + ' is invalid.'
        for t in ins.time_series():
            if (t.day == date) and (t.run_no == run_no) and (t.ts_specnbr == ts_specnbr):
                t_clone = t.clone()
                t_clone.value = new_value
                t_clone.commit()
        ael.poll()
    except EXCEPT_TIMESERIES, msg:
        print 'ERROR in update_single_TimeSeries_entry():', msg
        raise EXCEPT_TIMESERIES, "The TimeSeries entry " + str(date) +  " for the instrument " + ins.insid + " could not be updated."

"""----------------------------------------------------------------------------
FUNCTION    
    get_TimeSeries()                 

DESCRIPTION
    Gets all entries of a TimeSeries type for a specified instrument.
    
ARGUMENTS
    ins          Instrument      The TimeSeries belongs to this instrument   
    run_no       int             Number to separate different TimeSeries for the same instrument.
   
RETURNS
    TimeSeries_entries           [(date,float)]  A vector with pairs, consisting 
                                 of the date and its corresponding value.                                
----------------------------------------------------------------------------"""
def get_TimeSeries(ins,series_name,run_no, *rest):
    try:
        TimeSeries_entries = []
        ts_specnbr = ael.TimeSeriesSpec[series_name]
        if ts_specnbr == None: raise 'EXCEPT_TIMESERIES', 'The Time Series ' + series_name + ' is invalid.'
        for t in ins.time_series():
            if (t.run_no == run_no) and (t.ts_specnbr == ts_specnbr):
                TimeSeries_entries.append((t.day, t.value))
        TimeSeries_entries.sort()
        return TimeSeries_entries
    except EXCEPT_TIMESERIES, msg:
        print 'ERROR in get_TimeSeries():', msg
        raise EXCEPT_TIMESERIES, "No TimeSeries for the instrument " + ins.insid + " could be collected."

"""----------------------------------------------------------------------------
FUNCTION    
    get_average_TimeSeries()                 

DESCRIPTION
    Gets all entries of a TimeSeries type for a specified instrument.
    
ARGUMENTS
    ins          Instrument      The TimeSeries belongs to this instrument   
    run_no       int             Number to separate different TimeSeries for the same instrument.
   
RETURNS
    TimeSeries_entries           [(date,float)]  A vector with pairs, consisting 
                                 of the date and its corresponding value.                                
----------------------------------------------------------------------------"""
def get_average_TimeSeries(ins,series_name,run_no,*rest):
    try:
        TimeSeries_entries = {}
        ts_specnbr = ael.TimeSeriesSpec[series_name]
        if ts_specnbr == None: raise 'EXCEPT_TIMESERIES', 'The Time Series ' + series_name + ' is invalid.'

        for t in ins.time_series():
            if t.ts_specnbr == ts_specnbr:
                if t.run_no == run_no:
                    if not TimeSeries_entries.has_key(ins.und_insaddr.insid):
                        TimeSeries_entries[ins.und_insaddr.insid] = ([(t.day, t.value)]) 
                    else:
                        TimeSeries_entries[ins.und_insaddr.insid].append((t.day, t.value)) 
                else:
                    if TimeSeries_entries.has_key(ael.Instrument[t.run_no].insid):
                        TimeSeries_entries[ael.Instrument[t.run_no].insid].append((t.day, t.value))
                    else:
                        TimeSeries_entries[ael.Instrument[t.run_no].insid] = ([(t.day, t.value)])
        return [TimeSeries_entries, TimeSeries_entries.keys(), TimeSeries_entries.values()]
    except EXCEPT_TIMESERIES, msg:
        print 'ERROR in get_TimeSeries():', msg
        raise EXCEPT_TIMESERIES, "No TimeSeries for the instrument " + ins.insid + " could be collected."

    
"""----------------------------------------------------------------------------
FUNCTION    
    make_periodic_TimeSeries_entries()   

DESCRIPTION
    Creates evenly spaced entries for a specified instrument in a chosen TimeSeries.                
    
ARGUMENTS
    ins             Instrument      The TimeSeries belongs to this instrument   
    series_name     string          The name of the TimeSeries, e.g 'FAveragePrices'
    run_no          int             Number to separate different TimeSeries for the same instrument.
    start           date            First date entry in the TimeSeries
    end             date            Last date entry in the TimeSeries
    period          string          Evenly distributed time period, e.g daily, weekly or monthly
    value           float           Corresponding value to the specified date.
    adjust          string          If true, the dates are adjusted to banking dates.
    
RETURNS
    ret_val         string          ASQL needs a return value.
----------------------------------------------------------------------------"""
def make_periodic_TimeSeries_entries(ins,series_name,run_no,start,end,period,value,adjust = 'Yes', *rest):
    
    if start >= end and (period != "-1m" and period != "-1w" and period != "-1y"):
        raise EXCEPT_TIMESERIES, 'Invalid start (' + str(start)+ ') and end (' + str(end) + '). Start must be greater then end.'
    try:
        d = start
        if period == 'daily'   : 
            period = '1d'
        elif period == 'weekly' :
            period = '1w'
        elif period == 'monthly':
            period = '1m'
        elif period == 'quarterly':
            period = '3m'
        elif period=='DailyLastMonth':
            d = end.add_period('-1m')
            period = '1d'
        elif period == 'yearly':
            period = '1y'
        else:
            #Assuming a valid period
            try:        
                tmp = ael.date_today().add_period(period)
                period = period
            except:
                raise EXCEPT_TIMESERIES, 'The period ' + period + \
                ' is invalid. Must be daily, weekly, monthly, yearly or another valid period.'
        if d <= end:
            while d <= end: 
                # adjust_to_banking_day actually changes the value of d,
                # create a new date object
                tmp = d.add_days(0)

                if adjust == 'Yes': 
                    und_ins = ael.Instrument[run_no]
                    if run_no != RUN_NUMBER_FIX and und_ins != None: curr = und_ins.curr 
                    else: curr = ins.curr

                    tmp2 = tmp.adjust_to_banking_day(curr).add_days(0)
                    if tmp2 > end: break
                    elif tmp2 < start: print 'Date is before start day!!!'
                    else: make_TimeSeries_entry(ins, series_name, run_no, tmp2, value)
                else:
                    if tmp > end: break
                    else: make_TimeSeries_entry(ins, series_name, run_no, tmp, value)  
                d = d.add_period(period)
        else:
            while end <= d:
                # adjust_to_banking_day actually changes the value of d,
                # create a new date object
                tmp = d.add_days(0)

                if adjust == 'Yes': 
                    und_ins = ael.Instrument[run_no]
                    if run_no != RUN_NUMBER_FIX and und_ins != None: curr = und_ins.curr 
                    else: curr = ins.curr

                    tmp2 = tmp.adjust_to_banking_day(curr).add_days(0)
                    if tmp2 < end: break
                    elif tmp2 > start: print 'Date is before start day!!!'
                    else: make_TimeSeries_entry(ins, series_name, run_no, tmp2, value)
                else:
                    if tmp < end: break
                    else: make_TimeSeries_entry(ins, series_name, run_no, tmp, value)  
                d = d.add_period(period)
        print "Periodic TimeSeries created."
        print 'instr. \t= ', ins.insid
        print 'series \t= ', series_name
        print 'run_no \t= ', run_no
        print 'start \t= ', start
        print 'end \t= ', end
        print 'period \t= ', period
        print 'val \t= ', value    
        print
        # ASQL needs a return value
        return 'return_value'
    except EXCEPT_TIMESERIES, msg:
        raise EXCEPT_TIMESERIES, msg





"""----------------------------------------------------------------------------
make_periodic_TimeSeries_runno_fix() 
    The function creates a periodic TimeSeries with the default run number 
    specified above. 
----------------------------------------------------------------------------"""
def make_periodic_TimeSeries_runno_fix(i,series_name,start,end,period,value,adjust = 'Yes', *rest):
    try:
        und_instype = i.und_insaddr.instype
        if (und_instype == 'EquityIndex' or und_instype == 'Combination') \
          and (series_name == 'FAveragePrices' or series_name == 'FAverageStrike'):
            if i.add_info("FAverageIn") == "" and i.add_info("FFwdStart") == "" and \
               (i.add_info("FAverageType") == "ArithmeticFix" or i.add_info("FAverageType") == "GeometricFix"): 
                stock_links = ael.CombinationLink.select('owner_insaddr='+str(i.und_insaddr.insaddr))
                dim = len(stock_links)
                if dim != 0 and dim != 1:
                    page_nodnbr = 0
                    pages = ael.ListNode.select()
                    for page in pages: 
                        if page.id == "NonSplitIndexes":
                            page_nodnbr = page.nodnbr
                            break
                    ins_dict = {}
                    if page_nodnbr != 0:
                        page = ael.ListNode[page_nodnbr]
                        leafs = page.leafs()
                        for leaf in leafs:
                            ins_dict[leaf.insaddr.insid] = leaf.insaddr
                    else:
                        print "\n## !! EXCEPTION !! ##"
                        print "The page NonSplitIndexes does not exist. The underlying EquityIndex will be considered as a single underlying instrument."
                        print
                    if page_nodnbr != 0 and not ins_dict.has_key(i.und_insaddr.insid):
                        for stock_link in stock_links:
                            run_no = stock_link.member_insaddr.insaddr
                            make_periodic_TimeSeries_entries(i, series_name, run_no, start, end, period, value, adjust, rest)
                        return 'return_value'
            make_periodic_TimeSeries_entries(i, series_name, RUN_NUMBER_FIX, start, end, period, value, adjust, rest)
        else:make_periodic_TimeSeries_entries(i, series_name, RUN_NUMBER_FIX, start, end, period, value, adjust, rest)
    except EXCEPT_TIMESERIES, msg:
        print "\n## !! EXCEPTION !! ##"
        print '\nModule:  FTimeSeries'
        print 'Error : ', msg
        print 'Instr : ', i.insid

    # ASQL needs a return value
    return 'return_value'
    
"""----------------------------------------------------------------------------
make_ladder_TimeSeries() 
    The function creates rungs with the date set to option expiry.
----------------------------------------------------------------------------"""
def make_ladder_TimeSeries(i,ladder_timeseries,no_rungs,*rest):
    try:
        j = 0
        while j < float(no_rungs):
            make_TimeSeries_entry(i, ladder_timeseries, j, i.exp_day, -1)
            j = j + 1
        print "\n## !! TIME SERIES CREATED !! ##"
        print '\nInstr. \t= ', i.insid
        print 'Series \t= ', ladder_timeseries
        print 'Number Rungs = ', no_rungs
    
        return 'return_value'
    except EXCEPT_TIMESERIES, msg:
        print "\n## !! EXCEPTION !! ##"
        print '\nModule:  FTimeSeries'
        print 'Error : ', msg
        print 'Instr : ', i.insid


