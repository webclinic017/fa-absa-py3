# Module: Alive
# Version: 0.5
# Description: The module contains a number of ASQL functions to be used when
#   calculating how much of a specific trade has been realised, according to
#   book-keeping norms.
#   The following functions are available:
#   alive_reset()
#   alive()
#   ub()
#   ib()
#   deprec_premium()
#   interest()
#   is_agio()
#   agio_val()
#   last_trade()
#   portfolio_cost()
# EndDescription

import ael, math, copy
import string

global verbose, verbose_detail
verbose = 0   # Debugging printing is off. Can be set on with set_verbose()
    	      # or by giving a parameter to alive_reset
verbose_detail = 0
    
def alive(tf, trade, vdate, valtrade, acctype, *rest):
    # Return the fraction of a specific trade still alive
    if last_used_tf and tf.fltid != last_used_tf.fltid: 
    	raise 'Must run alive_reset() on this tradefilter first!'
    if not acctype: acctype = 'OPENAVG'
    if acctype != 'OPENAVG' and acctype != 'FIFO':
    	raise 'Acctype must be OPENAVG or FIFO'
    if not valtrade: valtrdnbr = 0
    else: valtrdnbr = valtrade.trdnbr
    if verbose: print 'Alive for', trade.trdnbr, tf.fltid, vdate, valtrdnbr
    if type(vdate) == type('string'): vd = str(ael.date(vdate))
    elif type(vdate) == type(ael.date('991231')): vd = str(vdate)
    else:
    	raise 'Date missing', thedate
    if verbose_detail: print '1->', tfactor_list[trade.insaddr.insaddr], trade.trdnbr
    if verbose_detail: print '2->', tfactor_list[trade.insaddr.insaddr][trade.trdnbr]
    dtup = (vd, valtrdnbr)
    if not tfactor_list[trade.insaddr.insaddr][trade.trdnbr].has_key(dtup):
    	print 'No alive factor found for instr,trade and date', trade.insaddr.insid, dtup
    	raise 'No alive factor found for trade and date', dtup
    else:
    	if tfactor_list[trade.insaddr.insaddr][trade.trdnbr][dtup] == -1:
	    print 'alive=-1 for:', trade.insaddr.insid, trade.trdnbr, dtup
    	return tfactor_list[trade.insaddr.insaddr][trade.trdnbr][dtup]

def alive_reset(tf,strstart,strend,acctype, verb, *rest):
    # Build up the matrices of alive factors, short and long positions etc
    global last_used_tf, ordered_instr_trades, ordered_datestup_list
    global ub_list, ib_list, long_list, short_list, tfactor_list
    set_verbose(verb)
    if verbose: print '-------------Resetting alive-----------'
    ib_list = {}
    ub_list = {}
    tfactor_list = {}
    ordered_datestup_list = {}
    last_used_tf = tf # Keep this to compare in alive
    current_long = current_short = 0
    ordered_trades = tf.trades().members()
    # If the sorting order changes, change in agio_val() break function too.
    ordered_trades.sort(value_day_trade_time_trdnbr_order)
    if strend: remove_trades_after_date(ordered_trades, strend)
    ordered_instr_trades = order_trades_by_instr(ordered_trades)
    if verbose: print 'OIT:', ordered_instr_trades
    for i in ordered_instr:
	tfactor_list[i.insaddr] = {}
	ib_list[i.insaddr] = {}
	ub_list[i.insaddr] = {}
	iblist = {} # { (valday, trdnbr) : ib }
	ublist = {}
        tflist = {}
	dtup = ()
        # The below 2 only necessary for FIFO, but define them to allow debug printing
    	long_list = {}
    	short_list = {}
	current_long = current_short = 0
    	ordered_trades = ordered_instr_trades[i.insaddr]
    # Calculate long and short for spreadAverage calculations.
    # The nicest would be to enter 0 trades for strstart and strend, but we 
    # can't do that yet, so we enter 0 values in the ublist and iblist instead.
    	next_rc = 0
        cmp_with_start = 0
        if strstart: 
    	    cmp_with_start = 1
	    startdate = ael.date(strstart)
        cmp_with_end = 0
        if strend: 
    	    cmp_with_end = 1
	    enddate = ael.date(strend)
    	for t in ordered_trades:
    	    if cmp_with_start:
	    	if t.value_day > startdate:
    	    	    dtup_start = (str(startdate), 0)
	    	    if not ublist.has_key(dtup_start):
		    	if dtup and ublist.has_key(dtup): # Previous trade, if there was one
	    	    	    ublist[dtup_start] = iblist[dtup_start] = ublist[dtup]
	    	    	else: ublist[dtup_start] = iblist[dtup_start] = 0
		    cmp_with_start = 0 # Don't compare anymore
            	    if acctype == 'FIFO': 
	    	    	if not long_list.has_key(dtup_start):
	    	    	    long_list[dtup_start] = current_long
	    	    	    short_list[dtup_start] = current_short
    	    if cmp_with_end:
	    	if t.value_day > enddate:
    	    	    dtup_end = (str(ael.date(strend)), 0)
	    	    if not ublist.has_key(dtup_end):
		    	if ublist.has_key(dtup): # Previous trade, if there was one
	    	    	    ublist[dtup_end] = iblist[dtup_end] = ublist[dtup]
	    	    	else: ublist[dtup_end] = iblist[dtup_end] = 0
		    cmp_with_end = 0 # Don't compare anymore
            	    if acctype == 'FIFO': 
	    	    	if not long_list.has_key(dtup_end):
	    	    	    long_list[dtup_end] = current_long
	    	    	    short_list[dtup_end] = current_short
 	    dtup = (str(t.value_day), t.trdnbr)
    	    iblist[dtup] = current_long + current_short
     	    if t.quantity > 0: current_long = current_long + t.quantity
    	    else: current_short = current_short + t.quantity
    	    if acctype == 'FIFO':
            	long_list[dtup] = current_long
    	    	short_list[dtup] = current_short
    	    ublist[dtup] = current_long + current_short
    	    if verbose: print 'Curr', dtup, t.quantity, current_long, current_short
     	if cmp_with_start: # Still haven't added strstart, i.e. it was after all trades
    	    dtup_start = (str(startdate), 0)
	    if not ublist.has_key(dtup_start):
	    	ublist[dtup_start] = iblist[dtup_start] = ublist[dtup]
            if acctype == 'FIFO': 
	    	if not long_list.has_key(dtup_start):
	    	    long_list[dtup_start] = current_long
	    	    short_list[dtup_start] = current_short
     	if cmp_with_end: # Still haven't added strend, i.e. it was after all trades
    	    dtup_end = (str(ael.date(strend)), 0)
	    if not ublist.has_key(dtup_end):
	    	ublist[dtup_end] = iblist[dtup_end] = ublist[dtup]
            if acctype == 'FIFO': 
	    	if not long_list.has_key(dtup_end):
	    	    long_list[dtup_end] = current_long
	    	    short_list[dtup_end] = current_short
    	if verbose and acctype == 'FIFO':
    	    print 'LONG', long_list
    	    print 'SHORT', short_list
    	ordered_dates_tup = datetup_list_fr_ordered_trades(ordered_trades, strstart, strend)
	ordered_datestup_list[i.insaddr] = ordered_dates_tup
	if verbose: print 'For', i.insid, 'the ordered dates are', ordered_dates_tup
    	for t in ordered_trades:
    	    factor_list = {}
    	    vday = str(t.value_day)
	    tq = t.quantity
	    after_val_day = 0
	    next_factor = 0.0
            if acctype == 'OPENAVG': 
	        for dtup in ordered_dates_tup:
		    td, tn = dtup
            	    if iblist.has_key(dtup): ib = iblist[dtup]
    	    	    else: ib = 0
            	    if ublist.has_key(dtup): ub = ublist[dtup]
    	    	    else: ub = 0
    	    	    dq = ub - ib	
	    	    if td < vday or (td == vday and tn != t.trdnbr and not after_val_day):
	    	        factor_list[dtup] = -1
		    	continue
	    	    factor_list[dtup] = next_factor
		    if not after_val_day:  # First factor of this trade
	    	    	after_val_day = 1
		    	if dq * ib < 0 and abs(dq) < abs(ib):
			    if verbose: print 'Pushing', dq, ib, next_factor
		    	else:
		    	    next_factor = min(ub / tq, 1.0)
		    	    if verbose: print 'First', t.trdnbr, t.insaddr.insid, vday, dtup, ub/tq, next_factor 
	    	    else:
	    	    	if not next_factor : pass # trade is closed => always zero
		    	else:
		    	    if dq * ib < 0:  # different signs
		    	    	if abs(dq) > abs(ib):	# Closing
    	    	    	    	    if verbose: print 'Closing (t,d,dq,ib,next)', t.trdnbr, vday, dtup, dq, ib, next_factor
	    	    	    	    next_factor = 0.0
			    	else:
			            if verbose: print 'Diminishing', factor_list[dtup], ub/ib, vday, dtup, dq, ub, ib
			            next_factor = factor_list[dtup] * (ub / ib)
		    	    else:
		    	    	next_factor = factor_list[dtup]
	    else: # acctype == 'FIFO'
    	    	prev_pos = 0.0
            	if verbose: print 't.trdnbr,dtup,longV,shortV,dq,tdq,longT'
	    	for dtup in ordered_dates_tup:
		    td, tn = dtup
            	    if short_list.has_key(dtup): shortV = short_list[dtup]
    	    	    else: shortV = 0.0
            	    if long_list.has_key(dtup): longV = long_list[dtup]
    	    	    else: longV = 0.0
	    	    longT = long_list[(str(t.value_day), t.trdnbr)]
	    	    shortT = short_list[(str(t.value_day), t.trdnbr)]
    	    	    if tq > 0: tdq = longT + shortV
	    	    else: tdq = longV + shortT
	    	    dq = longV + shortV - prev_pos
	    	    prev_pos = longV + shortV
	    	    if verbose: print 'Sorting on day', t.trdnbr, dtup, longV, shortV, dq, tdq, longT
	    	    if td < vday or (td == vday and tn != t.trdnbr and not after_val_day): 
	    	    	factor_list[dtup] = -1
		    	continue
	    	    factor_list[dtup] = next_factor
	    	    if not after_val_day:  # First factor of this trade
	    	    	after_val_day = 1
    	            	if tq > 0:
		    	    if tdq < 0: next_factor = 0
		    	    else: next_factor = min(tdq/tq, 1)
		    	else:
		    	    if tdq > 0: next_factor = 0
		    	    else: next_factor = min(tdq/tq, 1)
    	            	if verbose: print 'First', t.trdnbr, dtup, tdq, dq, next_factor 
	    	    else:
	    	    	if not next_factor : pass # trade is closed => always zero
		    	else:
		    	    if tq > 0:
		    	    	if tdq < 0: next_factor = 0
			    	else: next_factor = min(tdq/tq, 1)
		    	    else:
		    	    	if tdq > 0: next_factor = 0
			    	else: next_factor = min(tdq/tq, 1)
		    	if verbose: print 'And', t.trdnbr, dtup, tdq, dq, next_factor 
	    if verbose: print 'DD', t.insaddr.insaddr, t.trdnbr, factor_list
	    tflist[t.trdnbr] = factor_list
	# if verbose: print 'TFLIST',tflist
	tfactor_list[i.insaddr] = tflist
	ib_list[i.insaddr] = iblist
	ub_list[i.insaddr] = ublist
    	if verbose:
	    print 'TF', tfactor_list
            print 'IB', ib_list
    	    print 'UB', ub_list
    return 0.0

def ub(trade, adate, valtrade, *rest):
    if valtrade: tnr = valtrade.trdnbr
    else: tnr = 0
    return ub_list[trade.insaddr.insaddr][(str(adate), tnr)]

def ib(trade, adate, valtrade,*rest):
    if valtrade: tnr = valtrade.trdnbr
    else: tnr = 0
    return ib_list[trade.insaddr.insaddr][(str(adate), tnr)]

def deprec_premium(trade, valday,valtrade,*rest):
    # Return depreciated premium between a day and the previous, in the
    # date sequence of the trade
    if valtrade: tnr = valtrade.trdnbr
    else: tnr = 0 
    if valday == trade.value_day: prevvalday = valday
    else: 
    	pvday, vnr = datetup_before(ordered_datestup_list[trade.insaddr.insaddr], valday, tnr)
	prevvalday = ael.date(pvday)
    # print ordered_datestup_list[trade.insaddr.insaddr]
    # print 'deprec_prem,tnr,pvday, vday:',tnr,prevvalday,valday,'=',trade.deprec_premium(prevvalday, valday)
    return trade.deprec_premium(prevvalday, valday)

def interest(t, valday, valtrade, curr, *rest):
    # Calculate interest for a trade, which is sum of settled, accrued and due
    if valtrade and valtrade != '0': 
    	tnr = valtrade.trdnbr
    else: tnr = 0
    if verbose: vnr = -1    
    #vnr = -1    
    if valday == t.value_day: prevvalday = valday
    else: 
    	pvday, vnr = datetup_before(ordered_datestup_list[t.insaddr.insaddr], valday, tnr)
	prevvalday = ael.date(pvday)
    i = t.interest_settled(prevvalday, valday, curr) + \
    	t.interest_accrued(prevvalday, valday, curr) + \
	t.interest_due(prevvalday, valday, curr)
    if verbose: print 'Interest', t.insaddr.insid, t.trdnbr, prevvalday, valday, vnr, i
    # print 'Interest',t.insaddr.insid,t.trdnbr,prevvalday,valday,vnr, i
    return i

def is_agio(trd, adate, valtrade,*rest):
    # Return 0 if this is not a trade which has agio
    if valtrade: tnr = valtrade.trdnbr
    else: tnr = 0
    sd = str(adate)
    tq = trd.quantity
    ib = ib_list[trd.insaddr.insaddr][(sd, tnr)]
    if trd.value_day == adate and tq * ib < 0:
    	if verbose: print 'IS_AGIO', trd.trdnbr, trd.value_day, tnr, sd, tq, ib
        if abs(tq) > abs(ib): return 1
	else: return 2
    else: return 0

def agio_val(trade,pf,valday,valtrade,method,curr,*rest):
    if valtrade: tnr = valtrade.trdnbr
    else: tnr = 0
    cpf = 0
    ordered_trades = ordered_instr_trades[trade.insaddr.insaddr]
    cpf = portfolio_cost(ordered_trades, valday, curr, valtrade)
    cpt = trade.cost(valday, curr)
    svd = str(valday)
    ib = ib_list[trade.insaddr.insaddr][(svd, tnr)]
    q = trade.quantity
    isa = is_agio(trade, valday, valtrade, method)
    if isa == 1: res = ib / q * cpt - cpf
    elif isa == 2:
    	if method == 'OPENAVG': res = q / ib * cpf - cpt
	else: 
	    ua = trade.cost(trade.value_day, curr)
	    for t in ordered_trades:
	    	d1 = t.value_day
		# This works if sorting was done on value_day AND time, and time are different
		# if t.value_day == trade.value_day and t.time >= trade.time: 
		#     if verbose: print 'Break on ',t.value_day,trade.value_day,t.time,trade.time
		#     break
		# This works if sorting was done on value_day AND time AND trdnbr
		if t.value_day == trade.value_day and t.time == trade.time and t.trdnbr >= trade.trdnbr:
		    if verbose: print 'Break on ', t.value_day, trade.value_day, t.time, trade.time
		    break
		d2, vnr = datetup_after(ordered_datestup_list[t.insaddr.insaddr], trade.value_day, tnr)
	    	a1 = alive(pf, t, trade.value_day, trade, method)
		if a1 == -1: a1 = 0.0
	    	uaTrade = t.cost(trade.value_day, curr)
		if vnr: vtrade2 = ael.Trade[vnr]
		else: vtrade2 = None
		a2 = alive(pf, t, d2, vtrade2, method)
		if a2 == -1: a2 = 0.0
		if verbose: print 'UA for', trade.trdnbr, 'when', t.trdnbr, d1, a1, uaTrade, d2, a2, ua
		ua = ua + uaTrade * (a1 - a2)
    	    res = -ua		
    else: res = 0
    if verbose: print 'AgioVal', method, trade.trdnbr, valday, tnr, cpf, cpt, ib, q, isa, '=', res
    return res

def last_trade(anytrade,*rest):	# anytrade is used to get instr
    # Find last trade in correct direction of an ordered trade sequence
    rev_instr_trades = copy.copy(ordered_instr_trades[anytrade.insaddr.insaddr])
    rev_instr_trades.reverse()
    ##print 'REV',
    ##for t in rev_instr_trades:
    ##	print t.trdnbr
    last_trade = rev_instr_trades[0]
    dtup = (str(last_trade.value_day), last_trade.trdnbr)
    ##print 'DTUP',dtup
    ##print 'UBLIST',ub_list
    ubil = ub_list[anytrade.insaddr.insaddr]
    ##print 'UBIL',ubil
    ubl = ubil[dtup]
    ##print 'UBlast',ubl
    for trade in rev_instr_trades:
    	if ubl * trade.quantity > 0: break
    if verbose: print 'Last Trade', trade.trdnbr, trade.quantity
    return trade.trdnbr

def remove_trades_after_date(ordered_trades, strend):
    enddate = ael.date(strend)
    i = 0
    for t in ordered_trades:
        if t.value_day > enddate: 
	    del ordered_trades[i:]
	    break
	i = i + 1

def portfolio_cost(ordered_trades, valday, curr, valtrade):
    # Calculate cost for all trades in pf up to valday
    if valtrade: tnr = valtrade.trdnbr
    else: tnr = 0
    res = 0.0
    for t in ordered_trades:
    	if t.value_day == valday: break
	vd = str(valday)
	res = res + t.cost(valday, curr) * tfactor_list[t.insaddr.insaddr][t.trdnbr][(vd, tnr)]
    return res

def order_trades_by_instr(trades):
    # Returns a list of lists with trades of instruments. Also sets
    # global ordered_instr as list of instruments in this array
    orTbyI = {}
    global ordered_instr
    ordered_instr = []
    for t in trades:
    	if not orTbyI.has_key(t.insaddr.insaddr): 
	    orTbyI[t.insaddr.insaddr] = []
	    ordered_instr.append(t.insaddr)
	orTbyI[t.insaddr.insaddr].append(t)
    return orTbyI

def datetup_list_fr_ordered_trades(tradelist, strstart, strend):
    datetup_list = []
    cmp_with_start = 0
    if strstart: 
    	cmp_with_start = 1
	startdate = ael.date(strstart)
    cmp_with_end = 0
    if strend: 
    	cmp_with_end = 1
	enddate = ael.date(strend)
    for t in tradelist:
    	if cmp_with_start:
	    if t.value_day > startdate: # We passed startdate, so enter it
	    	datetup_list.append((str(startdate), 0))
		cmp_with_start = 0
    	    elif t.value_day == startdate: # Don't have to repeat
	    	cmp_with_start = 0
   	if cmp_with_end:
	    if t.value_day > enddate: # We passed enddate, so add it
	    	datetup_list.append((str(enddate), 0))
		cmp_with_end = 0
    	    elif t.value_day == enddate: # Don't have to repeat
	    	cmp_with_end = 0
	
	# Here we add the date, i.e. the trade value_day
    	datetup_list.append((str(t.value_day), t.trdnbr))
		
    if cmp_with_start: # 
    	datetup_list.append((str(startdate), 0))
    if cmp_with_end: # 
    	datetup_list.append((str(enddate), 0))
    
    if verbose: print 'DateList', datetup_list
    return datetup_list

def datetup_before(ordered_strdatetups, date, vtnr):
    if type(date) == type('string'): sdate = str(ael.date(strdate))
    else: sdate = str(date)
    prev_dtup = None
    for dtup in ordered_strdatetups:
    	td, tn = dtup
    	if td == sdate and tn == vtnr: break
	prev_dtup = dtup
    if not prev_dtup: prev_dtup = dtup
    return prev_dtup

def datetup_after(ordered_strdatetups, date, vtnr):
    if type(date) == type('string'): sdate = str(ael.date(strdate))
    else: sdate = str(date)
    next_dtup = (str(ael.BIG_DATE), 0)
    use_next = 0
    for dtup in ordered_strdatetups:
    	td, tn = dtup
	next_dtup = dtup
	if use_next: break
    	if td == sdate and tn == vtnr: use_next = 1
    return next_dtup
    
def value_day_order(t1, t2):
    if t1.value_day > t2.value_day: return 1
    elif t1.value_day < t2.value_day: return -1
    else: return 0 
    
def trade_time_order(t1, t2):
    if t1.time > t2.time: return 1
    elif t1.time < t2.time: return -1
    else: return 0 

def value_day_trade_time_order(t1, t2):
    # Order first by value day and, if equal, by trade time
    if t1.value_day > t2.value_day: return 1
    elif t1.value_day < t2.value_day: return -1
    else:
        if t1.time > t2.time: return 1
    	elif t1.time < t2.time: return -1
    	else: return 0 

def value_day_trade_time_trdnbr_order(t1, t2):
    # Order first by value day and, if equal, by trade time
    if t1.value_day > t2.value_day: return 1
    elif t1.value_day < t2.value_day: return -1
    else:
        if t1.time > t2.time: return 1
    	elif t1.time < t2.time: return -1
        else:
	    if t1.trdnbr > t2.trdnbr: return 1
    	    elif t1.trdnbr < t2.trdnbr: return -1
    	    else: return 0 

def set_verbose(set,*rest):
    global verbose
    if not set or set == '0': verbose = 0
    else: verbose = 1
    return 0
