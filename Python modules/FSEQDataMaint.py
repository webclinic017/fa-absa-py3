""" SEQ_VERSION_NR = PRIME 2.8.1 """




"""----------------------------------------------------------------------------
MODULE
    FSEQDataMaint - Data maintenance for Structured Equity Products
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    The functions included in the module will update exotic option valuation data.

NOTE
    - The functions are searching for a specific category field. All options 
      with that category field will be updated.
      
      Average options        => Category = Average
      Barrier options        => Category = Barrier
      Double barrier options => Category = Double Barrier
      Cliquet options        => Category = Cliquet
      Forward Start options  => Category = FwdStart
      Ladder options         => Category = Ladder
    
    - The prices stored by default are the MtM prices. Therefore the daily
      mark to market procedure should be performed before the exotic options
      are updated.
    
    - Maintenance functions included are:
    
     UpdateAveragePrice()        - Updates average option time series
     UpdateBarrierStatus()       - Updates barrier option knock status
     UpdateDoubleBarrierStatus() - Updates double barrier option knock status
     UpdateCliquetPrice()        - Updates the resets for cliquet and forward 
                                   start options.
     UpdateLadderRungs()         - Updates a passed rung with a correct price.

----------------------------------------------------------------------------"""
import ael
import FTimeSeries
import FEqBarrier
import FEqDblBarrier

"""----------------------------------------------------------------------------

AVERAGE OPTION MAINTENANCE

----------------------------------------------------------------------------"""

F_AVERAGE_TIMESERIES    = 'FAveragePrices'    # The timeseries where averages are stored
F_AVERAGE_FUTAVGVAL     = -1                  # Value stored in timeseries for unknown average points
F_STRIKE_TIMESERIES     = 'FAverageStrike'    # The timeseries where prices are stored to calculate a strike
F_AVERAGE_TIMESERIESRUN = 0                   # The run_nbr of the average timeseries

"""----------------------------------------------------------------------------
FUNCTION    
    UpdateAveragePrice() - Part of a Mark to Mark procedure

DESCRIPTION
    Pricing update routine. In the Time Serie 'FAveragePrices' future values are 
    set to -1. The routine updates the -1 to used_price for the underlying instrument.
    This routine should be run every evening. 
    
ARGUMENTS
    Takes no argument 
RETURNS
    Does not return anything 
----------------------------------------------------------------------------"""
def UpdateAveragePrice(*rest):
    print "\nUpdating Average options ..."
    cl_average = ael.ChoiceList.read('list="Category" and entry="Average"') 
    averages = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_average.seqnbr))  
    old_nbr     = 0
    saved_nbr   = 0 
    future_nbr  = 0
    ts_prices = ael.TimeSeriesSpec[F_AVERAGE_TIMESERIES]
    ts_strike = ael.TimeSeriesSpec[F_STRIKE_TIMESERIES]
    for i in averages:
        for t in i.time_series():
            if t.ts_specnbr == ts_prices or t.ts_specnbr == ts_strike:
                if t.run_no == F_AVERAGE_TIMESERIESRUN: und_ins = i.und_insaddr
                else: und_ins = ael.Instrument[t.run_no]

                today = ael.date_today()
                if (t.day < today) and (t.value >= 0): old_nbr = old_nbr + 1
                elif t.day > today:
                    if t.value == F_AVERAGE_FUTAVGVAL:
                        future_nbr = future_nbr + 1
                    else:
                        # Future asian dates have values assigned to them.
                        t_clone = t.clone()
                        t_clone.value = -1
                        t_clone.commit()
                        ael.poll()
                        print "Instrument:  ", i.insid
                        print "Underlying:  ", und_ins.insid
                        print "Average date:", t.day
                        print "Run Number:  ", t.run_no
                        print "New Value  : ", -1
                        print "TimeSeries   ", t.ts_specnbr.field_name
                        print "---------------------------------------"
                        saved_nbr = saved_nbr + 1

                else:
                    t_clone = t.clone()
                    if i.fix_fx:
                        t_clone.value = und_ins.mtm_price(t.day, und_ins.curr.insid)
                    else:
		    	if i.mtm_from_feed:
                            t_clone.value = und_ins.used_price(t.day, i.strike_curr.insid) 
			else:
			    t_clone.value = und_ins.mtm_price(t.day, i.strike_curr.insid)
			
                    t_clone.commit()
                    ael.poll()
                    print "Instrument:  ", i.insid
                    print "Underlying:  ", und_ins.insid
                    print "Average date:", t.day
                    print "Run Number:  ", t.run_no
                    print "Saved Price: ", t.value, 
                    print und_ins.curr.insid
                    print "TimeSeries   ", t.ts_specnbr.field_name
                    print "---------------------------------------"
                    saved_nbr = saved_nbr + 1
                    
    print "=============================="
    print "AVERAGE OPTIONS"
    print "New prices saved:     ", saved_nbr 
    print "Future average dates: ", future_nbr
    print "=============================="

#UpdateAveragePrice() 


"""----------------------------------------------------------------------------

SINGLE / DOUBLE BARRIER OPTION MAINTENANCE

----------------------------------------------------------------------------"""

F_BARRIER_EXCEPT        = 'f_eq_barrier_xcp'  # This exception is thrown by all barrier and double barrier routines.
F_BARRIER_TIMESERIES    ='FBarrierMonitorDays'# The timeseries where barrier monitor dates are stored.
F_BARRIER_TIMESERIESRUN = 0                   # The run_nbr of barrier time series. 
F_BARRIER_CROSSED       = 'FBarrier Crossed'
F_BARRIER_CROSSED_DATE  = 'FBarrier Cross Date'
F_BARRIER_MONITOR_FRQ   = 'FBarrierMonitorFrq'
F_SECOND_BARRIER        = 'FBarrier2'  
F_BARRIER_CONTINUOUS    = 'Continuous'
F_BARRIER_DAILY         = 'Daily'
F_BARRIER_MONTHLY       = 'Monthly'
F_BARRIER_WEEKLY        = 'Weekly'
F_BARRIER_YEARLY        = 'Yearly'
F_BARRIER_DAILY_LAST_MONTH = 'DailyLastMonth'
F_BARRIER_WEEKLY_LAST_MONTH = 'WeeklyLastMonth'
F_BARRIER_DAILY_LAST_TWO_WEEKS = 'DailyLastTwoWeeks'

    
"""----------------------------------------------------------------------------
FUNCTION    
    UpdateBarrierStatus() 

DESCRIPTION
    The function checks if the barrier level has been crossed, both for discrete
    and continuous barrier options. If the barrier has been reached, the additional
    info fields "FBarrier Crossed" and "FBarrier Cross Date" will be updated.  

ARGUMENTS
    i       Instrument  Barrier Option 
----------------------------------------------------------------------------"""
def UpdateBarrierStatus(*rest):
    print "\nUpdating Barrier options ..."
    cl_b = ael.ChoiceList.read('list="Category" and entry="Barrier"') 
    barriers = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_b.seqnbr))  
    
    for i in barriers: 
        barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        if i.exp_day > ael.date_valueday() and barr_freq != F_BARRIER_CONTINUOUS:
            FEqBarrier.create_barrier_timeserie(i)

    tsSpec = ael.TimeSeriesSpec[F_BARRIER_TIMESERIES]
    if tsSpec == None: 
        print "\n## !! EXCEPTION !! ##"
        print "NO VALID BARRIER TIME SERIES EXISTS!\n"
    else:
        tmp = ael.dbsql("select day,seqnbr,recaddr from time_series where ts_specnbr=" + str(tsSpec.specnbr) + "and value=" + '-1' + "and run_no=" + str(F_BARRIER_TIMESERIESRUN))[0]
        updated_nbr = 0
        # ts is a vector [(date,seqnbr,recaddr)]. All entries have the value -1.
        ts = map(lambda x:[ael.date(x[0][0:10]), x[1], x[2]], tmp)
        for x in ts:
            # x[2] = recaddr
            i = ael.Instrument[x[2]]
            if i != None :
                if i.exp_day > ael.date_valueday():
                    c = i.category_chlnbr
                    # If the category is set to "Barrier"...
                    if c != None and c.entry == 'Barrier': 
                        barrier_status = i.add_info(F_BARRIER_CROSSED)
                        if barrier_status != "Yes" and barrier_status != "Yes TEMP?":
                            # x[0] = Date of Time Series entry.
                            if x[0] < ael.date_valueday(): pass
                            if x[0] == ael.date_valueday():
                                # x[1] = sequence number of the Time Series. 
                                price = i.used_und_price() 
                                if price != 0.0:
                                    if i.exotic_type == "Down & Out" or i.exotic_type == "Down & In":
                                        res = (price - i.barrier)/(1.0*price)*100
                                    elif i.exotic_type == "Up & Out" or i.exotic_type == "Up & In":
                                        res = (i.barrier - price)/(1.0*price)*100
                                    else: 
                                        pass
                                else:
                                    print "No underlying price exist for ", i.und_insaddr.insid
                                    res = 10000000
                                barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
                                if res <= 0 and barr_freq != F_BARRIER_CONTINUOUS:
                                    FEqBarrier.update_addinfo(i, "Yes")
                                    updated_nbr = updated_nbr + 1
                                tsOld = ael.TimeSeries[x[1]]
                                tsUpdate = tsOld.clone()
                                tsUpdate.value = i.used_und_price()
                                tsUpdate.commit()
        print "=============================="
        print "BARRIER OPTIONS"
        print "Updated Barrier status:   ", updated_nbr 
        print "=============================="
        
#UpdateBarrierStatus()  


"""----------------------------------------------------------------------------
FUNCTION    
    UpdateDoubleBarrierStatus() 

DESCRIPTION
    The function checks if any of the barrier levels have been crossed, both for 
    discrete and continuous double barrier options. If any of the barriers has 
    been reached, the additional info fields "FBarrier Crossed" and "FBarrier 
    Cross Date" will be updated.   

ARGUMENTS
    i       Instrument  Double Barrier Option
----------------------------------------------------------------------------"""
def UpdateDoubleBarrierStatus(*rest):
    print "\nUpdating Double Barrier options ..."
    cl_dbl_b = ael.ChoiceList.read('list="Category" and entry="DoubleBarrier"') 
    dbl_barriers = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_dbl_b.seqnbr))  
    
    for i in dbl_barriers: 
        barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        if i.exp_day > ael.date_valueday() and barr_freq != F_BARRIER_CONTINUOUS:
            FEqBarrier.create_barrier_timeserie(i)

    tsSpec = ael.TimeSeriesSpec[F_BARRIER_TIMESERIES]
    if tsSpec == None: 
        print "\n## !! EXCEPTION !! ##"
        print "NO VALID BARRIER TIME SERIES EXISTS!\n"
    else:
        tmp = ael.dbsql("select day,seqnbr,recaddr from time_series where ts_specnbr=" + str(tsSpec.specnbr) + "and value=" + '-1' + "and run_no=" + str(F_BARRIER_TIMESERIESRUN))[0]
        updated_nbr = 0
        # ts is a vector [(date,seqnbr,recaddr)]. All entries have the value -1.
        ts = map(lambda x:[ael.date(x[0][0:10]), x[1], x[2]], tmp)
        for x in ts:
            # x[2] = recaddr
            i = ael.Instrument[x[2]]
            if i != None :
                c = i.category_chlnbr
                # If the category is set to "DoubleBarrier"...
                if c != None and c.entry == 'DoubleBarrier': 
                    barrier_status = i.add_info(F_BARRIER_CROSSED)
                    if barrier_status != "Yes" and barrier_status != "Yes TEMP?":
                        # x[0] = Date of Time Series entry.
                        if x[0] < ael.date_valueday(): pass
                        if x[0] == ael.date_valueday():
                            # x[1] = sequence number of the Time Series. 
                            price = i.und_insaddr.mtm_price() 
                            lower_barrier = FEqDblBarrier.get_lower_barrier(i)
                            upper_barrier = FEqDblBarrier.get_upper_barrier(i)
                            if price != 0.0:
                                res_upper = (upper_barrier - price)/(1.0*price)*100
                                res_lower = (price - lower_barrier)/(1.0*price)*100
                            else:
                                print "No underlying price exist for ", i.und_insaddr.insid
                                res_upper = 999
                                res_lower = 999
                            barr_freq = i.add_info(F_BARRIER_MONITOR_FRQ)    
                            if (res_upper <= 0 or res_lower <=0) and barr_freq != F_BARRIER_CONTINUOUS:
                                FEqBarrier.update_addinfo(i, "Yes")
                                updated_nbr = updated_nbr + 1
                            tsOld = ael.TimeSeries[x[1]]
                            tsUpdate = tsOld.clone()
                            tsUpdate.value = i.used_und_price()
                            tsUpdate.commit()
        print "=============================="
        print "DOUBLE BARRIER OPTIONS"
        print "Updated Double barrier status: ", updated_nbr 
        print "=============================="
    
#UpdateDoubleBarrierStatus()


"""----------------------------------------------------------------------------

FORWARD START / CLIQUET OPTION MAINTENANCE

----------------------------------------------------------------------------"""

F_CLIQUET_EXCEPT        = 'f_eq_cliquet_xcp'    
F_CLIQUET_TIMESERIES    = 'FCliquetResetDays' # The timeseries where the reset days are stored.
F_CLIQUET_TIMESERIESRUN = 0                   # The run_nbr of cliquet time series. 


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
def perform_update(i, fwd_saved_nbr):
    fwd_start_type = i.add_info('FFwdStart')
    if fwd_start_type != "":
        mapped_module = i.used_context_parameter('Valuation Function')
        if mapped_module != "FEqCliquet.pv":
            try: fwd_date = ael.date_from_string(i.add_info('FFwdStartDay'))
            except: fwd_date = -1
            if fwd_date != -1:
                if (fwd_date < ael.date_today() and i.strike_price <= 0.0) or \
                    fwd_date == ael.date_today():
                    close_price = i.und_insaddr.mtm_price(fwd_date, i.strike_curr.insid)
                    if close_price != 0.0:
                        i_clone = i.clone()
                        alpha = float(i.add_info('FFwdStartAlpha'))
                        i_clone.strike_price = alpha * close_price
                        if fwd_start_type == 'Fwd Start Perf':
                            i_clone.contr_size = i.contr_size / (1.0*close_price)
                        i_clone.commit()
                        ael.poll()
                        print "\nUpdated Forward Start Option"
                        print "Instrument:\t\t", i.insid
                        print "Underlying:\t\t", i.und_insaddr.insid
                        print "Alpha:\t\t\t", alpha
                        print "MtM price:\t\t", i.und_insaddr.mtm_price(fwd_date, i.strike_curr.insid)
                        print "New Strike price:\t", i.strike_price
                        if fwd_start_type == 'Fwd Start Perf':
                            print "New Contract Size:\t:", i.contr_size
                        print "---------------------------------------"
                        fwd_saved_nbr = fwd_saved_nbr + 1
                    else:
                        print "\n## !! EXCEPTION !! ##"
                        print "Error:\t\tMtM price for underlying equals zero at forward start day !"
                        print "Instr:\t\t", i.insid
                        print "Fwd Start Day:\t", fwd_date
                        print "Underlying:\t", i.und_insaddr.insid
                        print "---------------------------------------"
    return fwd_saved_nbr

def UpdateCliquetPrice(*rest):
    print "\nUpdating Cliquet options ..."
    tsSpec = ael.TimeSeriesSpec[F_CLIQUET_TIMESERIES]
    if tsSpec == None: 
        print "\n## !! EXCEPTION !! ##"
        print "NO VALID CLIQUET TIME SERIES EXISTS!\n"
    else:    
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
                # If the category is set to "Cliquet"...
                if c != None and c.entry == 'Cliquet': 
                    # x[0] = Date of Time Series entry.
                    if x[0] <= ael.date_valueday():
                        # x[1] = sequence number of the Time Series. 
                        tsOld = ael.TimeSeries[x[1]]
                        tsUpdate = tsOld.clone()
                        tsUpdate.value = i.und_insaddr.mtm_price(x[0])
                        tsUpdate.commit()
                        print "The reset date", x[0], "for the option", i.insid, "has been updated."
                        print "---------------------------------------"
                        cl_saved_nbr = cl_saved_nbr + 1

        print "=============================="
        print "CLIQUET OPTIONS"
        print "Non set Cliquet prices:  ", cl_old_nbr
        print "Updated Cliquet prices:  ", cl_saved_nbr 
        print "=============================="

    print "\nUpdating Forward Start options ..."
    cl_fwdstart = ael.ChoiceList.read('list="Category" and entry="FwdStart"') 
    fwdstarts = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_fwdstart.seqnbr )) 
    
    cl_average = ael.ChoiceList.read('list="Category" and entry="Average"') 
    averages = ael.Instrument.select("category_chlnbr.seqnbr=" + str(cl_average.seqnbr )) 

    fwd_saved_nbr   = 0 
    for i in averages:
        fwd_saved_nbr = perform_update(i, fwd_saved_nbr)
    for i in fwdstarts:
        fwd_saved_nbr = perform_update(i, fwd_saved_nbr)
        
    print "=============================="
    print "FORWARD START OPTIONS"
    print "Updated Fwd Start Options:    ", fwd_saved_nbr 
    print "=============================="
                    

#UpdateCliquetPrice()  


"""----------------------------------------------------------------------------

LADDER OPTION MAINTENANCE

----------------------------------------------------------------------------"""

F_LADDER_TIMESERIES     = 'FLadderRungs'

"""----------------------------------------------------------------------------
FUNCTION        
    UpdateLadderRungs() - Part of a Mark to Mark procedure

DESCRIPTION
    Pricing update routine. If the date in the Time Serie 'FLadderRungs' 
    is equal to the expiry date then this means that the rung in question
    has so far not been breached by the underlying asset, while if the date
    is prior the expiry date then the asset price reached the rung at that
    time. The routine updates the Time Series 'FLadderRungs'. This routine 
    should be run every evening. 
        
ARGUMENTS
    Takes no argument 

RETURNS
    Does not return anything                            
----------------------------------------------------------------------------"""
def UpdateLadderRungs(*rest):
    print "\nUpdating Ladder options ..."
    cl_ladder = ael.ChoiceList.read('list="Category" and entry="Ladder"') 
    seqnbr_ladder = cl_ladder.seqnbr 
    ladders = ael.Instrument.select("category_chlnbr.seqnbr=" + str(seqnbr_ladder))  
    saved_nbr = 0;future_nbr = 0
    for i in ladders: 
        mon_freq = i.add_info(F_BARRIER_MONITOR_FRQ)
        if i.exp_day > ael.date_valueday() and mon_freq != F_BARRIER_CONTINUOUS:
            FEqBarrier.create_barrier_timeserie(i)

    tsSpec = ael.TimeSeriesSpec[F_BARRIER_TIMESERIES]
    tmp = ael.dbsql("select day,seqnbr,recaddr from time_series where ts_specnbr=" + str(tsSpec.specnbr) + "and value=" + '-1' + "and run_no=" + str(F_BARRIER_TIMESERIESRUN))[0]
    time_series = map(lambda x:[ael.date(x[0][0:10]), x[1], x[2]], tmp)
    for x in time_series:
        [date, seq_nbr, insaddr] = x
        i = ael.Instrument[insaddr]
        if i != None :
            if i.exp_day > ael.date_valueday():
                c = i.category_chlnbr
                # Check category
                if c != None and c.entry == 'Ladder': 
                    if date < ael.date_valueday(): pass
                    if date == ael.date_valueday():
                        price = i.und_insaddr.mtm_price() 
                        if price != 0.0: 
                            rungs = []
                            ts_specnbr = ael.TimeSeriesSpec[F_LADDER_TIMESERIES]
                            for t in i.time_series():
                                if (t.ts_specnbr == ts_specnbr and t.day == i.exp_day):
                                    rungs.append([t.value, t.run_no, t.seqnbr])
                            future_nbr = future_nbr + len(rungs)
                            if rungs != []:
                                [rung_value, run_no, seqnbr] = min(rungs)
                                if i.call_option:
                                    res = rung_value - price
                                else:     
                                    res = price - rung_value

                                if res <= 0:
                                    t = ael.TimeSeries[seqnbr]
                                    if t.ts_specnbr == ts_specnbr:
                                        t_clone = t.clone()
                                        t_clone.day = ael.date_valueday()
                                        t_clone.commit()
                                        print "The rung", rung_value, "for the option", i.insid, "has been updated."
                                        print "---------------------------------------"
                                        saved_nbr = saved_nbr + 1
                                        break
        
    print "=============================="
    print "LADDER OPTIONS"
    print "Non set Rungs:          ", future_nbr-saved_nbr
    print "Updated Rungs:          ", saved_nbr
    print "=============================="  
    
#UpdateLadderRungs()      
    
    
    
"""----------------------------------------------------------------------------
UpdateAllExoticOptions - the function calls the exotic option maintenance 
                         functions available.
----------------------------------------------------------------------------"""
def UpdateAllExoticOptions():
    UpdateAveragePrice()   
    UpdateBarrierStatus()  
    UpdateDoubleBarrierStatus()
    UpdateCliquetPrice()       
    UpdateLadderRungs()
    print "=============================="
    print "ALL EXOTIC MAINTENANCE IS DONE"
    print "=============================="  
    
UpdateAllExoticOptions()


