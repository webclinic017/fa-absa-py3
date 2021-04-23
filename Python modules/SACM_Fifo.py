""" ========== ACMB  R P L / U P L  FIFO  C a l c u l a t i o n s ========== 
HISTORY: 2004-03-02 CA tested dev done for workability for ACMB, 2003-10-24 FK Corrected bugg in avg_cost() calc.

DESCRIPTION: This module calculates (RPL)/UPL and avg_price using a FIFO style
using the price, quantity values in a trade directly.
"""
import ael
import string, os, re, time


CALENDAR=CURR=ael.Instrument['ZAR']
def CurrName():
    global CURR
    return CURR.insid



#------------------------------------------------------------------------------------------
# cs_rpl and cs_upl calculation: The rpl and upl calculation could be seen as as
# modified open_average calculation done on day level.
#------------------------------------------------------------------------------------------
VERSION="ACMB_Fifo 0.2: %s" % time.strftime("%c", time.localtime(time.time()))
#print VERSION
ael.log(VERSION)
#print VERSION
#############################################
# GLOBALS
#############################################
do_log=0
do_log_avg=0
do_log_trds=0
do_log_price='No'
avg_method='FIFO' # when arena functions are used


logged_hist_price={}
portfolio_addinfo_lookup={} # (prfnbr,tag) : value
logged_missing_fx={} # (curr.insid,d.to_time()):None, always curr.insid=>CurrName() i.e. CHF.
logged_zero_price={} # (insid,day):None
logged_special={}    # insid:None
OTCInsType=['Swap', 'Cap', 'Floor', 'FRA', 'CreditDefaultSwap']
SETTLE_MARKET='Settlement'  # Name on the Settlement market
SettleMarket=ael.Party[SETTLE_MARKET] # Settlement market object

# Bid/Ask valuation
UnIssuer=ael.Party['United Stat-863024'] # The United States issuer.
UsdCurr=ael.Instrument['USD']

PAYTYPES_AS_COST=['Extension Fee'] # List of fees that should be included as cost

#############################################
# Help functions
#############################################


def nowstr():
    return time.strftime("%c", time.localtime(time.time()))

add_chf_day_map={}
def add_chf_days(args,day='2002-09-16',n=0,*rest):
    """ Neeeded to fix date handling when grouping """
    global add_chf_day_map
    if type(args) == type([]):
        if len(args[0]) == 3:
            [dummy, day, n]=args[0]
        elif len(args[0]) == 2:
            [day, n]=args[0]
    d=ael.date(day)
    [dummy, d2]=get_period(d, n)
    t2=d2.to_time()
    s2=add_chf_day_map.get(t2)
    if not s2:
        s2=str(d2)
        add_chf_day_map[t2]=s2
    #return str(ael.date(day).add_banking_day(CALENDAR,n))
    return s2

def mean(trades,m=0.0,q=0.0,log=0):
    if zero(q):pm=m
    else:
        pm=m*q
    for t in trades:
        pm=pm+(TP(t, 'Mean')*t.quantity)
        q=q+t.quantity
    if log: print "mean=", m
    if not zero(q): return pm/q
    else: return pm # ! cash
    
def sign(v):
    if v > 0.0: return 1
    elif v < 0.0: return -1
    else: return 0


# -------- Predicates --------------
def is_domestic_instrument(ins):
    global CURR
    if ins.curr == CURR: return 1
    return 0

def is_frw_trade(t):
    """ is_frw_trade(ael_entity trade):
    	Checks if a trade is a forward trade. d is normally date(t.time) """
    global CALENDAR
    
    d=ttod(t.time)
    if t.value_day > d.add_banking_day(CALENDAR, t.insaddr.spot_banking_days_offset):
     	return 1
    return 0
    
def zero(a,b=0.0,prec=0.00001):
    if abs(a-b) < prec: # Change precision here
        return 1
    return 0

def is_expired(ins):
    """ Perhaps define only on Bond,Option and Future/Forward.
    	Note that in this version an instrument is expired on expiry date"""
    if ins.exp_day and ins.exp_day <= ael.date_today():
        return 1
    return 0

   
# ---------- Trade Time Operations -----------------
def TP(t,source=''):
    "returns the trade price adjusted for payments included as cost"
    global PAYTYPES_AS_COST, do_log
    if not t.payments() or t.quantity==0.0: return t.price
    if t.trade_curr: tcurr=t.trade_curr
    else: tcurr=t.curr
    tcurr_name=t.curr.insid
    pm=t.price*t.quantity
    d=TTTOD(t)
    for p in t.payments():
        if not p.type in PAYTYPES_AS_COST:continue
        if not p.curr or p.curr == tcurr:
            fx=1.0
        else:
            fx=p.curr.used_price(d, tcurr_name)
            if zero(fx): fx=p.curr.mtm_price(d, tcurr_name)
    	pm=pm+(p.amount*fx)
    if do_log: print "(%s) Adjusted trade price from %.4lf => %.4lf" % (source, t.price, pm/t.quantity)
    return pm/t.quantity


#-- Time/date operations

trade_date_map={} # MemFix plus opt
def TTTOD(t):
    """TTTOD : trade time to true date. Converts forward trades"""
    global trade_date_map, CURR
    if trade_date_map.has_key(t.trdnbr):
        (d, old_time, s)=trade_date_map[t.trdnbr]
        if old_time == t.time: return d
    if is_frw_trade(t):
        d=t.value_day.add_banking_day(CALENDAR, -t.insaddr.spot_banking_days_offset)
        #d=d.adjust_to_banking_day(CURR)
	s=str(d)
	#print "is forward"
    else:
        d=ttod(t.time)
        #d=d.adjust_to_banking_day(CURR)
        s=str(d)
    trade_date_map[t.trdnbr]=(d, t.time, s)
    return d

def TTTODS(t):
    """ TTTODS: trade time to date string, optimization:
        should be called after call to TTTOD"""
    global trade_date_map
    return trade_date_map[t.trdnbr][2] # s
        
        
def ttods(t):
    """ Time to day string e.g. 2002-09-30"""
    s=time.strftime("%Y-%m-%d", time.gmtime(t)) # time is in UTC
    #s=str(ael.date_from_time(t))
    return s
    
def ttos(t):
    """ Time to string e.g. 2002-09-30 15:00:00"""
    s=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
    return s


string_date_map={} # MemFix
def ttod(t):
    """ttod(time) : time to ael_date"""
    global string_date_map
    s=ttods(t)
    d=string_date_map.get(s)
    if not d:
        d=ael.date(s)
        string_date_map[s]=d
    return d

#----------------------------------------------------------

date_periods={}
def get_period(fd, offset):
    """ MemFix: Generates all days between fd and offset and
        return the interval as a list.
        If offset is an int [fd,fd.add_banking_day(offset) will be returned"""
    global date_periods
    t1=fd.to_time()
    if type(offset) == type(0): # i.e an int
        t2=offset
    else:
        t2=offset.to_time()
    key=(t1, t2)
    period=date_periods.get(key)
    if not period:
        period=[fd]
        if type(offset) == type(0):
            period.append(fd.add_banking_day(CALENDAR, offset))
        else:
            while fd < offset:
                fd=fd.add_banking_day(CALENDAR, 1)
                period.append(fd)
        date_periods[key]=period
    return period


#--------------------------------------------------------------------
def Qty(trades):
    return reduce(lambda x, y: x+y.quantity, trades, 0)

def Premium(trades):
    pm=0.0
    for t in trades:
        pm=pm+(TP(t, 'Premium')*t.quantity)
    return -1.0*pm


def QtyX(values):
    """ values = [(price,quantity,trade)]"""
    return reduce(lambda x, y: x+y[1], values, 0.0)

def PremiumX(values):
    """ values = [(price,quantity,trade)]"""
    pm=0.0
    for p, q, t in values:
        pm=pm+(p*q)
    return -1.0*pm



def first(l):
    """ Returns the first element and removes it from l.
        Note: pop() is faster than del """
    if not l: return (None, [])
    l.reverse()
    f=l.pop()
    l.reverse()
    return f
    
#--------------------------------------------------------------------
# Cost calculations
#--------------------------------------------------------------------

def calc_avg_cost_fifo(trades,ACnew=0.0,QTYnew=0.0):
    """ avg_cost_fifo calculations. Returns both avg and rpl"""
    global do_log_avg
    if not trades:
        return (ACnew, QTYnew)
    trades.sort(lambda x, y: x.time-y.time) # Sort trades in time order
    if do_log_avg: print "\n\n%s\ncalc_avg_cost_fifo  begin\n%s" % (70*'#', 70*'#')
    Q=P=RPL=0.0
    Qnew=trades[0].nominal_amount()
    ACnew=trades[0].price
#    PREMnew = trades[0].premium
    open_trades=[(trades[0].price, trades[0].nominal_amount(), trades[0])] # List of open trades values
    
    Qleft=Pleft=0.0         # part not closed when decreasing. =PREMleft
#    print len(trades[1:]), 'line 275'
    for t in trades[1:]:
        if do_log_avg: print "\n\ncalc_avg_cost_fifo:: Q(%.2lf) A(%.2lf) RPL(%.2lf)" % (Qnew, ACnew, RPL)
        if do_log_avg:
            print "N(%d) P(%.2lf) Q(%.lf) T(%s) VD(%s) TD(%s)" % (t.trdnbr, t.price, t.nominal_amount(), ttos(t.time), t.value_day, TTTOD(t))
    	if t.trdnbr in(268210, 268225, 268164): print "N(%d) P(%.2lf) Q(%.lf) T(%s) VD(%s) TD(%s)" % (t.trdnbr, t.price, t.nominal_amount(), ttos(t.time), t.value_day, TTTOD(t))
        Q=t.nominal_amount()
        P=t.price
#	PREM=t.premium
        Qold=Qnew
        ACold=ACnew
#	PREMold=PREMnew
        if zero(Qold): # Startup
            if do_log_avg: print "Increase, startup"
            Qnew=Q
            ACnew=P
#	    PREMnew=PREM
            open_trades=[(t.price, t.nominal_amount(), t)]
        elif sign(Qold) == sign(Q): # Increase
            if do_log_avg: print "Increase"
            ACnew=((ACold*Qold)+(P*Q))/(Qold+Q)
            Qnew=Qold+Q
#	    PREMnew = ((PREMold*Qold)+(P*Q))/(Qold+Q)
            open_trades.append((t.price, t.nominal_amount(), t))
        elif zero(Qold+Q) or sign(Qold) == sign(Qold+Q): # Decrease, still open
            if do_log_avg: print "Decrease"
	    
#	    print open_trades
            while open_trades:
                (P1, Q1, T1)=first(open_trades) # pops!
                if do_log_avg: print "Q1(%.2lf) P1(%.2lf) Q(%.2lf) P(%.2lf) L(%.lf)" % (Q1, P1, Q, P, Qleft)
                if zero(Qold+Q):
                    if do_log_avg: print "zero(Qold+Q)"
                    ACnew=0.0
                    Qnew=0.0
#		    PREMnew=0.0
                    RPL=RPL+((P1-P)*(-Q1))
		    
		    if t == trades[len(trades)-1]:
			open_trades = []
                    
		    
		    break # We are done
                elif abs(Q1) > abs(Q): # Close a part
                    if do_log_avg: print "Close a part"
                    PMopen=-PremiumX(open_trades)
                    ACnew=((P1*(Q1+Q))+PMopen)/(Q1+Q+QtyX(open_trades))
                    Qnew=Qold+Q
                    RPL=RPL+((P1-P)*Q)
		    
                    open_trades.insert(0, (P1, Q1+Q, T1))
		    
                    break # We are done
                else: # Close Out first trade
                    if do_log_avg: print "Close Out first trade"
                    PMopen=-PremiumX(open_trades)
                    Qold=Qnew=QtyX(open_trades)
                    ACold=ACnew=PMopen/Qnew
                    RPL=RPL+((P1-P)*(-Q1))
		    if zero(Q+Q1):
		    	if do_log_avg: print "We are done"
		    	break # We are done
		    else:
                    	Q=Q+Q1
			
        else: #zero pass though
            if do_log_avg: print "zero pass though"
            while open_trades:
                (P1, Q1, T1)=first(open_trades) # pops!
                RPL=RPL+((P1-P)*Q1)
            ACnew=P
            Qnew=Qold+Q
            open_trades=[(P, Qnew, t)]
    
        
    for alltrds in trades:
    	pop_FIFO(alltrds, 0.0)
    ael.poll()
    for openfifo in open_trades:
    	pop_FIFO(openfifo[2], openfifo[1])
    ael.poll()
                
    return (ACnew, RPL)
    

def pop_FIFO(t, value):

    if abs(t.nominal_amount()) <= 0.000001 : value = 0.0
    saved = 0
    value_str = str(value)
    for addinfo in t.additional_infos():
    	if addinfo.addinf_specnbr.field_name == 'FIFO_POS':
#	    print addinfo.value, value, t.trdnbr, '368'
    	    if not addinfo.value and value_str:
	    	ai=ael.AdditionalInfoSpec['FIFO_POS']    
		addinfoclone = addinfo.clone()
    	    	t_c = ael.Trade[t.trdnbr].clone()
		addinfoclone.value= value
	    	addinfoclone.commit()
		saved = 1 
	    elif  addinfo.value and value_str and addinfo.value != value_str:
	    	ai=ael.AdditionalInfoSpec['FIFO_POS']    
		addinfoclone = addinfo.clone()
    	    	t_c = ael.Trade[t.trdnbr].clone()
		addinfoclone.value= value_str
	    	addinfoclone.commit()
		saved = 1 
	    else: 
	    	saved = 1
	    
    if saved == 0:
    	t_c = ael.Trade[t.trdnbr].clone()
	x=ael.AdditionalInfo.new(t_c)
#	x.recaddr = t.trdnbr
	value_str= str(value)
    	x.value= value_str
	ai=ael.AdditionalInfoSpec['FIFO_POS']
	x.addinf_specnbr=ai.specnbr
	x.commit()
    	saved = 1



####################################################################
# EXPORTED FUNCTIONS
####################################################################

def avg_price_fifo(args,*rest):

    """ Returns the avg_price using a fifo style for all trades
        with a time <= end_day.
        Should be called from sql as:
        avg_price_fifo(t,end_day,used_price(t)"""
	
    if not args: return 0.0
    cut_off_day=args[0][1]
    if type(cut_off_day) == type(''):
        cut_off_day=ael.date(cut_off_day)
    trades=[]
    for arg in args:
        t=arg[0]
        if ttod(t.time) <= cut_off_day and t.status not in ('Void', 'Simulated') and t.insaddr.instype not in ('PromisLoan', 'Option', 'CD', 'Bill'):
            trades.append(t)
    (ac, rpl)=calc_avg_cost_fifo(trades)
#    print ac,rpl
    return ac
    

