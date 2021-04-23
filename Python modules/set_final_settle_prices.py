""" Exercise_assign:1.1.2 """

"""----------------------------------------------------------------------------
MODULE
        set_final_exercise_prices.py - Sets the final settlement prices in
        all Exercise/Assign/Abandon trades done on the specified date.

DESCRIPTION
        Sets the final settlement price from the exchange into trades with
        trade type Exercise, Assign and Abandon made on the date specified as
        input. The premium of the trades are updated accordingly.

        When instrument is cash-settled the final settlement prices from the
        exchange should be stored on the MtM Market called "SETTLEMENT",
        from which they are selected in this script.
        
        If physical delivery is used, the settlement trade could either be
        done to the strike price or to the market price. The closing trade
        of the option (with trade type Exercise/Assign/Abandon) should then
        get a price according to the method.
        
NOTE            
        In this script, only trades in status set to "Exchange" are searched
        through. If exercised trades have another status, the get_trades
        function needs to be changed.

DATA-PREP       
        A Party of type MtM Market and with the name "SETTLEMENT" is required.

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import ael
import sys, getopt, os



# Select all trades in status "Exchange" and trade type set to
# Exercise, Assign or Abandon where trade time equals the input date

def get_trades(exer_date):
    exer_trades = []
    all_trades = ael.Trade.select('status = "Exchange"')
    for t in all_trades:
        if ((t.type == 'Exercise' or t.type == 'Assign' or t.type == 'Abandon')
            and ael.date_from_time(t.time) == ael.date(exer_date)
	    and (t.insaddr.instype == 'Option' or t.insaddr.instype == 'Future/Forward')):
            exer_trades.append(t)
    return exer_trades


# Find the physical delivery trade corresponding to the exercise trade
   
def get_physical_trade(t_exer):
    if not t_exer.insaddr.und_insaddr:
        return None
    und = ael.Instrument.read('insaddr=%d'
                              %(t_exer.insaddr.und_insaddr.insaddr))
    trades = ael.Trade.select('contract_trdnbr=%d' %(t_exer.contract_trdnbr))
    for t in trades:
        if t.insaddr.insaddr == und.insaddr:
            return t
    

# Update the payment of type Exercise Cash or create it if it doesn't exist

def update_exercise_payment(t_exer, settle, mode):
    found = 0
    excess_lots = t_exer.insaddr.contr_size - t_exer.insaddr.phys_contr_size
    if t_exer.insaddr.instype == 'Option':
    	if t_exer.insaddr.call_option == 1:
    	    trade_price = settle - t_exer.insaddr.strike_price
    	else:
    	    trade_price = t_exer.insaddr.strike_price - settle
    else:
    	trade_price = settle
    
    premium = t_exer.premium_from_quote(t_exer.acquire_day, trade_price)
    new_amount = premium * excess_lots / t_exer.insaddr.contr_size
    payments = ael.Payment.select('trdnbr=%d' %(t_exer.trdnbr))

    for p in payments:

	if (p.type == 'Exercise Cash' and mode == 'Strike'):
	    found=1
	    payment_clone = p.clone()
	    payment_clone.amount = new_amount
    	    payment_clone.commit()	    
	    
    t_exer_clone = t_exer.clone()
    payments_clone = t_exer_clone.payments()
    for p in payments_clone:
	if (p.type == 'Exercise Cash' and mode == 'Market'):
	    found=1
	    p.delete()
    
    t_exer_clone.commit()
    
    
    if not found and mode == 'Strike':
    	t_exer_clone 	    = t_exer.clone()
    	new_payment 	    = ael.Payment.new(t_exer_clone)
    	new_payment.ptynbr  = t_exer.counterparty_ptynbr
    	new_payment.type    = 'Exercise Cash'
    	new_payment.amount  = new_amount
    	new_payment.curr    = t_exer.insaddr.curr
    	new_payment.payday  = t_exer.spot_date(ael.date_from_time(t_exer.time))
	t_exer_clone.commit()

	

"""----------------------------------------------------------------------------
FUNCTION 
 set_final_settle_prices - Sets the final settlement price in all
        Exercising derivatives trades, and potential corresponding physical
        delivery trades, done on the specified date.

DESCRIPTION
        Cash settled instruments: Read the price on the SETTLEMENT market
        first. If there is no such price, read the settle price from the
        market on which the trade was done. Set the price of the closing
        derivative trade to the difference between the settle price and the
        strike and change the premium accordingly.
 
        Physical settled instruments: Either the physical trade is done to
        market, in which case the exercise trade should carry the difference
        between strike and the settlement price, or the physical trade is done
        to the strike in which case the exercise trade should get the price
        and premium zero.

ARGUMENTS
 The function takes the following arguments:
        1) trades - The Exercise trades found in get_trades().
        2) exer_date - Only Exercised trades done on this date are handled,
           i.e. the trade time of the trade with type Exercise, Assign or
           Abandon should equal this date. The settlement prices should also
           have been entered on this date.
        3) mode - This could either be set to Strike or to Market. This
           depends on whether the physical delivery trade is done to the
           strike price or to market price.
 
RETURNS
 Nothing.
----------------------------------------------------------------------------"""

def set_final_settle_prices(trades, exer_date, mode):
    settle_market = ael.Party.read('ptyid = "SETTLEMENT"')
    if not settle_market:
        print 'The MtM Market "SETTLEMENT" does not exist'
        return

    if not trades:
    	print 'No Exercise/Assign trades made on date %s' %(exer_date)
    	return

    for t in trades:
        p_der = 0.0 #price to be set in the derivative trade
    	
	#First find the settlement price for the underlying instrument
	#Check if t.insaddr.settlement is cash.
	
	if t.insaddr.settlement == 'Cash':
            mkt_nbr = settle_market.ptynbr
	else:
	    if t.market_ptynbr.ptynbr: mkt_nbr = t.market_ptynbr.ptynbr
	                  	    
        und = t.insaddr.und_insaddr

	settle_price=0
        try:
            settle_price = \
            ael.Price.read('insaddr=%d and day="%s" and curr=%d and ptynbr=%d'
                           %(und.insaddr, exer_date, t.curr.insaddr, mkt_nbr))

    	    if not settle_price:
	    	temp_price = \
            	ael.Price.read('insaddr=%d  and curr=%d and ptynbr=%d'
                    %(und.insaddr,   t.curr.insaddr, mkt_nbr))
    	    	if (temp_price.day == ael.date(exer_date)):
		    settle_price = temp_price
		    
	except:
	    if not settle_price: #Check the trade's market instead of SETTLEMENT
                if t.market_ptynbr:
                    mkt_nbr = t.market_ptynbr.ptynbr
        
                else:
                    print 'Trade %d: No price was found on "SETTLEMENT" market and the trade has no market set via market_ptynbr' %(t.trdnbr)
                    continue
                    
                settle_price = \
            	    ael.Price.read('insaddr=%d and day="%s" and curr=%d and ptynbr=%d'
                                %(und.insaddr, exer_date, t.curr.insaddr, mkt_nbr))
    	        if not settle_price:
    	    	    for p in und.prices():
    	    	        if (p.ptynbr.ptynbr == mkt_nbr and \
    	    	    	    p.curr.insaddr == t.curr.insaddr and \
    	    	    	    p.day == ael.date(exer_date)):
    	    	    	    settle_price = p

        if not settle_price:
            print 'No %s settlement price for "%s" on %s (%s market)'\
                  %(t.curr.insid, und.insid, exer_date, t.market_ptynbr.ptyid)
            continue
            
        if not (settle_price.bits & 256):
            print 'Settle bit for "%s" is zero on %s.'\
                  %(t.insaddr.insid, exer_date),\
                  'No valid settlement price for trade %d' %(t.trdnbr)
            continue

        #A settlement price has been found
        if t.insaddr.settlement == 'Cash':
            if t.insaddr.call_option:
                p_der = settle_price.settle - t.insaddr.strike_price
            else:
                p_der = t.insaddr.strike_price - settle_price.settle
            
        else:  #Physical settlement
            p_phys = 0.0 #price to be set in the physical trade
            t_phys = get_physical_trade(t)
            if not t_phys:
                print 'Physical settlement trade does not exist for trade %d.'\
                      %(t.trdnbr)
                continue
                
            if mode == 'Market':
                p_phys = settle_price.settle
    	        if t.insaddr.instype == 'Option':
            	    if t.insaddr.call_option:
                        p_der = settle_price.settle - t.insaddr.strike_price
                    else:
                    	p_der = t.insaddr.strike_price - settle_price.settle
	    	else: #Future
		    p_der = settle_price.settle
		
            else: #Physical is done to the strike price
                p_der = 0.0
    	        if t.insaddr.instype == 'Option':
                    p_phys = t.insaddr.strike_price
		else: #Future
		    p_phys = settle_price.settle

            if (abs(t.insaddr.phys_contr_size) > 0.000001 and \
	    	abs(t.insaddr.phys_contr_size - t.insaddr.contr_size) > 0.000001):
	        update_exercise_payment(t, settle_price.settle, mode)

            phys_clone = t_phys.clone()
            phys_clone.price = p_phys
            phys_clone.premium = \
                phys_clone.premium_from_quote(phys_clone.acquire_day, p_phys)
            phys_clone.commit()
                    
        der_clone = t.clone()
        der_clone.price = p_der
        der_clone.premium = der_clone.premium_from_quote(t.acquire_day, p_der)
        der_clone.commit()
        ael.poll
        

######################################################################
######################################################################
### Main
######################################################################

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:p:d:m:',
                               ['user=', 'passw=', 'date=', 'mode=' ])

    except getopt.error, msg:
       print msg
       print """Usage: ael <config-name> set_final_exercise_prices.py [options]
       -u, --user   The ARENA database user in CAPITAL LETTERS
       -p, --passw  The ARENA database user's password
       -d, --date   Exercise trades done on this date are handled
       -m, --mode   The price mode used for physical delivery trades
                    The mode could either be 'Market' or 'Strike'
       """
       sys.exit(2)

    #Default values
    password = ""
    user = ""
    exer_date = ""
    mode = 'Strike'
    
    for o, a in opts:
        if o in ['-u', '--user']: user = a
        if o in ['-p', '--passw']: password = a
        if o in ['-d', '--date']: exer_date = a
        if o in ['-m', '--mode']: mode = a

    if not user:
        print 'User (and possibly password) is mandatory'
        sys.exit(2)
        
    ael.connect(os.environ['ADS_ADDRESS'], user, password)
    if not exer_date: exer_date = ael.date_today().to_string()
    trades = get_trades(exer_date)
    set_final_settle_prices(trades, exer_date, mode)
    ael.disconnect()

else:
    ael_variables = \
    [('exer_date', 'Date', 'string', [], str(ael.date_today()), 1),
     ('mode', 'Mode', 'string', ['Market', 'Strike'], 'Strike', 1)]
    
    def ael_main(in_data):
        trades = get_trades(in_data['exer_date'])
        set_final_settle_prices(trades, in_data['exer_date'], in_data['mode'])

	    




