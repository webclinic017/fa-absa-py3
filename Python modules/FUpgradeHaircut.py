"""----------------------------------------------------------------------------
2003-04-01

MODULE
    upgrade_haircut - Module which updates the haircut for repo trades.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION

DATA-PREP
    The variables that should be set are:

    update_repo_reverse int integer that indicates that trades in Repo/Reverse 
    	    	    	    should be updated
    update_buy_sellback int integer that indicates that trades in BuySellback
    	    	    	    should be updated
    verbosity	int 	    Integer that indicate the level of information that
    	    	    	    will be generated in the AEL console

REFERENCES

----------------------------------------------------------------------------"""

try:
    import string
except ImportError:
    print 'The module string was not found.'
    print
try:
    import ael
except ImportError:
    print 'The module ael was not found.'
    print
try:
    import time
except ImportError:
    print 'The module time was not found.'
    print


######################################################################
### sv     SqlValue returns string of arg if not 'None' or NULL
######################################################################
def sv(val):
    if val == None:
        return 'NULL'
    else:
        return `val`
	

######################################################################
### check_trade
######################################################################
def check_trade(trdnbr):

    trade = ael.Trade[int(trdnbr)]

    if trade == None:
        print 'Got trade from sybase that is not accessible from ael'
        print 'Skipping trdnbr = ', trdnbr
        return 0
    else:
        return 1
	
######################################################################
### Read instrument/trade table to get Repo/Reverse trades 
######################################################################
def get_repo_trades(instype):

    if verbosity == 1:
        print 'Reading trades in', instype
	
    q = ' \
    SELECT \
               t.trdnbr, \
               i.insaddr,\
               i.insid, \
               i.ref_value, \
               i.contr_size, \
               t.quantity, \
               t.premium \
    FROM \
                instrument i,\
                trade t \
    WHERE \
                i.instype =  %d \
    AND		i.insaddr = t.insaddr  \
    AND     	t.type = %d \
    ORDER BY t.trdnbr' %\
    	(ael.enum_from_string('InsType', instype ),
	 ael.enum_from_string('TradeType', 'Normal'))
	

    repo_trades = ael.dbsql(q)

    if verbosity == 1 and repo_trades:
        print 'The database contains', len(repo_trades[0]), 'trades in ', instype

    res = []
    if repo_trades:
    	for trd in repo_trades[0]:
            res.append(trd)

    return res

######################################################################
### undins_dirty_value
######################################################################
def undins_dirty_value(undins, startdate, quote):
    #Initiate the dirty_quote to the quote passed
    dirty_quote = quote

    if (undins.quote_type == 'Yield'):
    	dirty_quote = undins.dirty_from_yield(startdate, 'None', 'None', quote)

    elif (undins.quote_type == 'Clean'):
    	dirty_quote = dirty_quote + undins.interest_accrued(None, startdate, undins.curr.insid)/undins.contr_size*100

    elif (undins.quote_type == 'Pctpct of Nom'):
    	dirty_quote = dirty_quote / 10
	dirty_quote = dirty_quote + undins.interest_accrued(None, startdate, undins.curr.insid)/undins.contr_size*100

    elif (undins.quote_type == 'Per 1000 of Nom'):
    	dirty_quote = dirty_quote / 10
	dirty_quote = dirty_quote + undins.interest_accrued(None, startdate, undins.curr.insid)/undins.contr_size*100

    elif (undins.quote_type == 'Per 100 Units'):
    	dirty_quote = dirty_quote / 100

    elif (undins.quote_type == 'Per Million'):
    	dirty_quote = dirty_quote / 1000000

    elif (undins.quote_type == 'Per 10 000 Units'):
    	dirty_quote = dirty_quote / 10000

    elif (undins.quote_type == 'Per Contract'):
    	dirty_quote = dirty_quote / undins.contr_size

    elif (undins.quote_type == 'Per 100 contracts'):
    	dirty_quote = dirty_quote / (undins.contr_size * 100)
    

#    elif (undins.quote_type == '100-rate'):
#    elif (undins.quote_type == 'Unadj Clean'):
#    elif (undins.quote_type == 'Simple Rate'):


    # We now have the dirty price. Make it to a value    
    if undins.quote_type == 'Pctpct of Nom' or \
    	undins.quote_type == 'Pct of Nominal' or \
	undins.quote_type == 'Clean' or \
	undins.quote_type == 'Unadj Clean' or \
	undins.quote_type == '100-rate' or \
	undins.quote_type == 'Yield' or \
	undins.quote_type == 'Simple Rate' or \
	undins.quote_type == 'Discount Rate' or \
	undins.quote_type == 'Per 1000 of Nom' or \
	undins.quote_type == 'Per 1000 Clean':
	dirty_value = dirty_quote * undins.contr_size / 100

    elif undins.quote_type == 'Per 100 Units' or \
    	undins.quote_type == 'Per 10 000 Units' or \
	undins.quote_type == 'Per Million' or \
    	undins.quote_type == 'Per Unit':
        dirty_value = dirty_quote
    
    elif undins.quote_type == 'Per Contract' or \
    	undins.quote_type == 'Per 100 Contracts':
	dirty_value = dirty_quote * undins.contr_size
	
    elif undins.quote_type == 'None':
    	print 'None is not a supported quotetype for underlying instrument'
	dirty_value = 0	
    elif undins.quote_type == 'Coupon':
    	dirty_value = quote * undins.contr_size    	
    else:
    	print 'Quotetype ', undins.quote_type, 'not handled'
	 
    return dirty_value


######################################################################
### calculate_repo_reverse_haircut
######################################################################
def calculate_repo_reverse_haircut(trdnbr):
    haircut = 0
    trd = ael.Trade[int(trdnbr)]
    ins = trd.insaddr
    undins = ins.und_insaddr
    und_contr_size = undins.contr_size
    for l in ins.legs():
    	startdate = l.start_day
    
    nominal = trd.quantity * ins.contr_size
    premium = trd.premium
    amount = trd.quantity * ins.ref_value
    dirty_value = undins_dirty_value(undins, startdate, ins.ref_price)


    if (abs(nominal * und_contr_size) > 0.00001):
    	haircut = abs((100 * amount * dirty_value / (nominal * und_contr_size))) - 100.0 


    if haircut < 0.001: 
    	haircut = 0
#    haircut = round(haircut,4)
    

    return haircut


######################################################################
### calculate_buy_sellback_haircut
######################################################################
def calculate_buy_sellback_haircut(trdnbr):
    haircut = 0
    trd = ael.Trade[int(trdnbr)]
    ins = trd.insaddr
    undins = ins.und_insaddr
    und_contr_size = undins.contr_size
    startdate = trd.value_day

    premium = trd.premium
    amount = trd.quantity
    dirty_value = undins_dirty_value(undins, startdate, trd.price)
    
    if(abs(premium) > 0.0001):
      haircut = abs((100 * amount * dirty_value) / premium ) - 100.0; 

    if haircut < 0.001: 
    	haircut = 0
#    haircut = round(haircut, 4)    

    return haircut  



######################################################################
### do_update_haircut
######################################################################
def do_update_haircut(trdnbr, rr):

    if rr:
        haircut = calculate_repo_reverse_haircut(trdnbr)
    else:
    	haircut = calculate_buy_sellback_haircut(trdnbr)

    if haircut:
    	if verbosity == 1:
            print 'Setting haircut for trd', trdnbr, 'to', haircut
	
    	u = ' \
    	UPDATE \
            trade \
    	SET \
            haircut   = ' + sv(haircut) + ' \
    	WHERE \
            trdnbr = ' + trdnbr
    
        res = ael.dbsql(u)

    return
    
######################################################################
### update_haircut
######################################################################
def update_haircut(trd, rr):

    for row in trd:
        trdnbr = sv(row[0])

        trd_ok = check_trade(trdnbr)

        if trd_ok:
            do_update_haircut(trdnbr, rr)
            
    return


"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""

if __name__ == "__main__":
    import sys, getopt
     
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
	    	    	    	   'a:u:r:b:p:v:h:')
        if len(opts) < 3:
            print len(opts)
            raise getopt.error, ''
    except getopt.error, msg:
        print msg
        m = '''Usage: upgrade_haircut.py -a ads_address -u username -r update_repo_reverse
        -b update_buy_sellback [-p password -v verbosity -h help]'''
        print m
        sys.exit(2)

    atlas_passw = ''
    update_repo_reverse = 0
    update_buy_sellback = 0
    verbosity = 1
    
    for o, a in opts:
        if o == '-a': ads_address = a
        if o == '-u': atlas_user = a
        if o == '-p': atlas_passw = a
        if o == '-v': verbosity = a
	if o == '-r': update_repo_reverse = a
	if o == '-b': update_buy_sellback = a
        if o == '-h': help_text()

    ael.connect(str(ads_address), str(atlas_user), str(atlas_passw))

    if update_repo_reverse:
    	repo_trades = get_repo_trades('Repo/Reverse')
    	if repo_trades:
            update_haircut(repo_trades, 1)
	    
    if update_buy_sellback:
    	buse_trades = get_repo_trades('BuySellback')
	if buse_trades:
	    update_haircut(buse_trades, 0)
	
    ael.disconnect()

    print
    print "upgrade_haircut finished", time.ctime(time.time())

else:
   
    verbosity = 1
    #Set the update_repo_reverse to 0 if no trades in repo/reverse 
    #are traded with haircut
    update_repo_reverse = 1
    #Set the update_buy_sellback to 0 if no trades in buysellback 
    #are traded with haircut
    update_buy_sellback = 1
    
   
    if update_repo_reverse:
    	repo_trades = get_repo_trades('Repo/Reverse')
    	if repo_trades:
            update_haircut(repo_trades, 1)
	    
    if update_buy_sellback:
    	buse_trades = get_repo_trades('BuySellback')
	if buse_trades:
	    update_haircut(buse_trades, 0)
	            
    print
    print "upgrade_haircut finished", time.ctime(time.time())


